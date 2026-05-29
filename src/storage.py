"""
日报数据落盘模块
保存原始抓取结果和 AI 分析结果，便于复盘与排错。
"""

import json
import os
from datetime import date, datetime


def _json_default(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return str(value)


def save_daily_json(kind, items, output_dir="data", run_date=None):
    """
    保存每日 JSON 数据。

    kind: raw 或 analyzed 等文件名前缀
    items: 可 JSON 序列化的数据列表
    """
    run_date = run_date or datetime.now().date()
    date_str = run_date.isoformat() if hasattr(run_date, "isoformat") else str(run_date)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{kind}_{date_str}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2, default=_json_default)

    print(f"[DATA] Saved {kind}: {output_path} ({len(items)} items)")
    return output_path
