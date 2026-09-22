import json
from pathlib import Path

from csv_cleaner.cli import main


def test_cli_writes_clean_file_and_report(tmp_path: Path):
    src = tmp_path / "input.csv"
    dst = tmp_path / "clean.csv"
    report = tmp_path / "report.json"
    src.write_text(" name ,note\n Ali , x \n Ali , x \n", encoding="utf-8")
    code = main([str(src), "-o", str(dst), "--report", str(report)])
    assert code == 0
    assert dst.read_text(encoding="utf-8") == "name,note\nAli,x\n"
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["duplicates_removed"] == 1


def test_cli_returns_two_for_bad_input(tmp_path: Path):
    src = tmp_path / "bad.csv"
    src.write_text("a,b\n1\n", encoding="utf-8")
    assert main([str(src), "-o", str(tmp_path / "out.csv")]) == 2
