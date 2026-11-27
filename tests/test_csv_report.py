import pytest

from orderlab.csv_report import revenue_from_csv


def test_csv_revenue(sample_csv):
    assert revenue_from_csv(sample_csv) == 35_000


@pytest.mark.parametrize("contents", ["", "price,quantity\n"])
def test_csv_empty(tmp_path, contents):
    path = tmp_path / "empty.csv"
    path.write_text(contents, encoding="utf-8")
    assert revenue_from_csv(path) == 0


def test_csv_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        revenue_from_csv(tmp_path / "missing.csv")


def test_csv_invalid_number(tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_text("price,quantity\ninvalid,2\n", encoding="utf-8")
    with pytest.raises(ValueError):
        revenue_from_csv(path)
