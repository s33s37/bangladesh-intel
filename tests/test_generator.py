from pathlib import Path

from src.generator import _dedup_items, generate_html


def test_generate_html_writes_index_and_archive(tmp_path):
    output_path = generate_html([], output_dir=str(tmp_path), model_name="test-model")

    assert Path(output_path).name == "index.html"
    assert (tmp_path / "index.html").exists()
    assert list(tmp_path.glob("report_*.html"))


def test_dedup_does_not_merge_fallback_items():
    items = [
        {"title": "Bangladesh garment exports face tariff pressure", "summary_cn": "来源消息：Bangladesh garment exports face tariff pressure", "reason": "无AI密钥", "source": "A"},
        {"title": "Chinese-backed solar park reaches financial close", "summary_cn": "来源消息：Chinese-backed solar park reaches financial close", "reason": "无AI密钥", "source": "B"},
    ]

    assert len(_dedup_items(items)) == 2
