from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


class CSVError(ValueError):
    """Raised for invalid CSV input or cleaning options."""


@dataclass(frozen=True)
class CleanOptions:
    trim: bool = True
    normalize_headers: bool = True
    deduplicate: bool = True
    drop_empty_rows: bool = True
    drop_empty_columns: bool = False
    lowercase_headers: bool = False
    select: tuple[str, ...] = ()
    drop: tuple[str, ...] = ()


@dataclass(frozen=True)
class CleanReport:
    input_rows: int
    output_rows: int
    input_columns: int
    output_columns: int
    duplicates_removed: int
    empty_rows_removed: int
    empty_columns_removed: tuple[str, ...]
    delimiter: str
    output_sha256: str

    def to_dict(self) -> dict:
        return asdict(self)


def _header(value: str, lower: bool) -> str:
    value = re.sub(r"\s+", "_", value.strip())
    value = re.sub(r"[^\w.-]", "_", value, flags=re.UNICODE)
    value = re.sub(r"_+", "_", value).strip("_") or "column"
    return value.lower() if lower else value


def _unique_headers(headers: Iterable[str], normalize: bool, lower: bool) -> list[str]:
    result: list[str] = []
    counts: dict[str, int] = {}
    for raw in headers:
        base = _header(raw, lower) if normalize else raw.strip()
        if not base:
            base = "column"
        counts[base] = counts.get(base, 0) + 1
        result.append(base if counts[base] == 1 else f"{base}_{counts[base]}")
    return result


def _sniff(text: str) -> csv.Dialect:
    try:
        return csv.Sniffer().sniff(text[:8192], delimiters=",;\t|")
    except csv.Error:
        return csv.excel


def clean_text(text: str, options: CleanOptions = CleanOptions(), delimiter: str | None = None) -> tuple[str, CleanReport]:
    if not text.strip():
        raise CSVError("input CSV is empty")
    if delimiter is not None and (len(delimiter) != 1 or delimiter in "\r\n\""):
        raise CSVError("delimiter must be one safe character")
    dialect = _sniff(text)
    source_delimiter = delimiter or dialect.delimiter
    rows = list(csv.reader(text.splitlines(), delimiter=source_delimiter))
    if not rows or not rows[0]:
        raise CSVError("CSV must contain a header row")
    width = len(rows[0])
    if any(len(row) != width for row in rows[1:]):
        raise CSVError("CSV has inconsistent column counts")

    headers = _unique_headers(rows[0], options.normalize_headers, options.lowercase_headers)
    data = rows[1:]
    if options.trim:
        data = [[cell.strip() for cell in row] for row in data]

    empty_removed = 0
    if options.drop_empty_rows:
        kept = []
        for row in data:
            if all(not cell for cell in row):
                empty_removed += 1
            else:
                kept.append(row)
        data = kept

    duplicate_removed = 0
    if options.deduplicate:
        seen: set[tuple[str, ...]] = set()
        kept = []
        for row in data:
            key = tuple(row)
            if key in seen:
                duplicate_removed += 1
            else:
                seen.add(key)
                kept.append(row)
        data = kept

    indexes = list(range(width))
    empty_columns: list[str] = []
    if options.drop_empty_columns:
        for i, name in enumerate(headers):
            if all(not row[i] for row in data):
                empty_columns.append(name)
        indexes = [i for i in indexes if headers[i] not in empty_columns]

    available = [headers[i] for i in indexes]
    unknown = (set(options.select) | set(options.drop)) - set(available)
    if unknown:
        raise CSVError("unknown column(s): " + ", ".join(sorted(unknown)))
    if options.select:
        indexes = [headers.index(name) for name in options.select if name not in options.drop]
    elif options.drop:
        indexes = [i for i in indexes if headers[i] not in options.drop]
    if not indexes:
        raise CSVError("cleaning would remove every column")

    out_headers = [headers[i] for i in indexes]
    out_rows = [[row[i] for i in indexes] for row in data]
    import io
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(out_headers)
    writer.writerows(out_rows)
    output = buffer.getvalue()
    report = CleanReport(
        input_rows=len(rows) - 1, output_rows=len(out_rows), input_columns=width,
        output_columns=len(out_headers), duplicates_removed=duplicate_removed,
        empty_rows_removed=empty_removed, empty_columns_removed=tuple(empty_columns),
        delimiter=source_delimiter, output_sha256=hashlib.sha256(output.encode()).hexdigest(),
    )
    return output, report


def clean_file(source: Path | str, destination: Path | str, options: CleanOptions = CleanOptions(), delimiter: str | None = None) -> CleanReport:
    src, dst = Path(source), Path(destination)
    if not src.is_file():
        raise CSVError(f"input file does not exist: {src}")
    if src.resolve() == dst.resolve():
        raise CSVError("refusing to overwrite the input file")
    try:
        text = src.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise CSVError("input must be UTF-8/UTF-8-BOM; convert its encoding first") from exc
    output, report = clean_text(text, options, delimiter)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(output, encoding="utf-8", newline="")
    return report
