from pathlib import Path

from orderlab.csv_report import revenue_from_csv


def generate_report(source: Path, output: Path) -> None:
    revenue = revenue_from_csv(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>OrderLab Report</title>
</head>
<body>
  <h1>OrderLab Report</h1>
  <p>Revenue: {revenue:,} KRW</p>
</body>
</html>
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    generate_report(root / "data/sample_orders.csv", root / "site/index.html")
