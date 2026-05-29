import json
from datetime import datetime

from src.storage import save_daily_json


def test_save_daily_json_serializes_datetimes(tmp_path):
    output_path = save_daily_json(
        "raw",
        [{"title": "Test", "raw_date": datetime(2026, 5, 30, 8, 15)}],
        output_dir=str(tmp_path),
        run_date=datetime(2026, 5, 30).date(),
    )

    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert output_path.endswith("raw_2026-05-30.json")
    assert data[0]["raw_date"] == "2026-05-30T08:15:00"
