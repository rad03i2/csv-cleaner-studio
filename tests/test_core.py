import csv
import io
from pathlib import Path

import pytest

from csv_cleaner import CSVError, CleanOptions, clean_file, clean_text


def rows(text):
    return list(csv.reader(io.StringIO(text)))


def test_default_cleaning_trims_normalizes_and_deduplicates():
    source = " Full Name , Age ,Age\n Alice , 20 ,20\n Alice ,20,20\n,,,\n"
    # four cells in final row makes input malformed, so use valid empty row below
    source = " Full Name , Age ,Age\n Alice , 20 ,20\n Alice ,20,20\n,,\n"
    output, report = clean_text(source)
    assert rows(output) == [["Full_Name", "Age", "Age_2"], ["Alice", "20", "20"]]
    assert report.duplicates_removed == 1
    assert report.empty_rows_removed == 1


def test_semicolon_is_detected():
    output, report = clean_text("name;city\nAli;Mosul\n")
    assert report.delimiter == ";"
    assert rows(output)[1] == ["Ali", "Mosul"]


def test_drop_empty_column_and_select_order():
    opts = CleanOptions(drop_empty_columns=True, select=("b", "a"))
    output, report = clean_text("a,b,empty\n1,2,\n3,4,\n", opts)
    assert rows(output) == [["b", "a"], ["2", "1"], ["4", "3"]]
    assert report.empty_columns_removed == ("empty",)


def test_unknown_column_is_rejected():
    with pytest.raises(CSVError, match="unknown column"):
        clean_text("a,b\n1,2\n", CleanOptions(drop=("missing",)))


def test_inconsistent_rows_are_rejected():
    with pytest.raises(CSVError, match="inconsistent"):
        clean_text("a,b\n1\n")


def test_input_is_never_overwritten(tmp_path: Path):
    path = tmp_path / "data.csv"
    path.write_text("a\n1\n", encoding="utf-8")
    with pytest.raises(CSVError, match="overwrite"):
        clean_file(path, path)


def test_file_cleaning_and_hash(tmp_path: Path):
    src, dst = tmp_path / "in.csv", tmp_path / "out.csv"
    src.write_text(" name \n Alice \n", encoding="utf-8")
    report = clean_file(src, dst)
    assert dst.read_text(encoding="utf-8") == "name\nAlice\n"
    assert len(report.output_sha256) == 64
