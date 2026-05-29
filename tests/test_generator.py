from pathlib import Path

from src.generator import generate_html


def test_generate_html_writes_index_and_archive(tmp_path):
    output_path = generate_html([], output_dir=str(tmp_path), model_name="test-model")

    assert Path(output_path).name == "index.html"
    assert (tmp_path / "index.html").exists()
    assert list(tmp_path.glob("report_*.html"))
