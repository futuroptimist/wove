from pathlib import Path


def test_viewer_includes_planner_upload_control() -> None:
    viewer_html = Path("viewer/index.html").read_text(encoding="utf-8")

    assert 'id="planner-upload"' in viewer_html
    assert "Upload planner JSON" in viewer_html

