from main import build_average_gdp_report
from main import read_files
from main import parse_args
import sys

def test_average_gdp_basic():
    rows = [
        {"country": "A", "gdp": "100"},
        {"country": "A", "gdp": "300"},
        {"country": "B", "gdp": "200"},
    ]

    result = build_average_gdp_report(rows)

    assert result == [
        ("A", 200.0),
        ("B", 200.0),
    ]

def test_sorting_desc():
    rows = [
        {"country": "A", "gdp": "100"},
        {"country": "B", "gdp": "300"},
    ]

    result = build_average_gdp_report(rows)

    assert result[0][0] == "B"
    assert result[1][0] == "A"

def test_read_files_success(tmp_path):
    file = tmp_path / "data.csv" # встроенная фикстура pytest
    file.write_text(
        "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
        "United States,2023,25462,2.1,3.4,3.7,339,North America\n"
        "United States,2022,23315,2.1,8.0,3.6,338,North America\n"
        "United States,2021,22994,5.9,4.7,5.3,337,North America\n"
        "China,2023,17963,5.2,2.5,5.2,1425,Asia\n"
        "China,2022,17734,3.0,2.0,5.6,1423,Asia\n"
        "China,2021,17734,8.4,1.0,5.1,1420,Asia\n"
        "Germany,2023,4086,-0.3,6.2,3.0,83,Europe\n"
        "Germany,2022,4072,1.8,8.7,3.1,83,Europe\n"
        "Germany,2021,4257,2.6,3.1,3.6,83,Europe\n"
    )

    rows = read_files([str(file)])

    assert len(rows) == 9
    assert rows[0]["country"] == "United States"


def test_parse_args_valid(monkeypatch):
    test_args = [
        "main.py",
        "--files", "file1.csv", "file2.csv",
        "--report", "average-gdp"
    ]

    monkeypatch.setattr(sys, "argv", test_args)

    args = parse_args()

    assert args.files == ["file1.csv", "file2.csv"]
    assert args.report == "average-gdp"