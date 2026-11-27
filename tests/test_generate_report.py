from generate_report import generate_report


def test_generate_report(sample_csv, tmp_path):
    output = tmp_path / "site" / "index.html"
    generate_report(sample_csv, output)
    html = output.read_text(encoding="utf-8")
    assert "<h1>OrderLab Report</h1>" in html
    assert "Revenue: 35,000 KRW" in html
