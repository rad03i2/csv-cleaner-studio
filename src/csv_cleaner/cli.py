from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .core import CSVError, CleanOptions, clean_file, clean_text


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="csv-cleaner", description="Profile and clean CSV files safely.")
    p.add_argument("input", help="Input CSV path, or - for stdin")
    p.add_argument("-o", "--output", help="Output CSV path (required unless --stdout)")
    p.add_argument("--stdout", action="store_true", help="Write cleaned CSV to stdout")
    p.add_argument("--report", help="Write JSON cleaning report to this path")
    p.add_argument("--delimiter", help="Explicit input delimiter; otherwise auto-detected")
    p.add_argument("--select", help="Comma-separated normalized column names to keep, in order")
    p.add_argument("--drop", help="Comma-separated normalized column names to remove")
    p.add_argument("--keep-duplicates", action="store_true")
    p.add_argument("--keep-empty-rows", action="store_true")
    p.add_argument("--drop-empty-columns", action="store_true")
    p.add_argument("--no-trim", action="store_true")
    p.add_argument("--no-normalize-headers", action="store_true")
    p.add_argument("--lowercase-headers", action="store_true")
    p.add_argument("--version", action="version", version=f"csv-cleaner-studio {__version__} — Radwan Abdulhadi Ahmed / @rad03i2")
    return p


def _names(value: str | None) -> tuple[str, ...]:
    return tuple(x.strip() for x in value.split(",") if x.strip()) if value else ()


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if not args.stdout and not args.output:
        parser().error("--output is required unless --stdout is used")
    if args.stdout and args.output:
        parser().error("choose either --stdout or --output")
    options = CleanOptions(trim=not args.no_trim, normalize_headers=not args.no_normalize_headers,
        deduplicate=not args.keep_duplicates, drop_empty_rows=not args.keep_empty_rows,
        drop_empty_columns=args.drop_empty_columns, lowercase_headers=args.lowercase_headers,
        select=_names(args.select), drop=_names(args.drop))
    try:
        if args.input == "-":
            output, report = clean_text(sys.stdin.read(), options, args.delimiter)
            if args.stdout:
                sys.stdout.write(output)
            else:
                Path(args.output).write_text(output, encoding="utf-8", newline="")
        else:
            if args.stdout:
                text = Path(args.input).read_text(encoding="utf-8-sig")
                output, report = clean_text(text, options, args.delimiter)
                sys.stdout.write(output)
            else:
                report = clean_file(args.input, args.output, options, args.delimiter)
        if args.report:
            Path(args.report).write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if not args.stdout:
            print(f"Cleaned {report.input_rows} -> {report.output_rows} rows; {report.input_columns} -> {report.output_columns} columns.", file=sys.stderr)
        return 0
    except (CSVError, OSError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
