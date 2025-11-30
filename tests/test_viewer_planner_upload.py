from pathlib import Path


def test_viewer_includes_planner_upload_control() -> None:
    viewer_html = Path("viewer/index.html").read_text(encoding="utf-8")

    assert 'id="planner-upload"' in viewer_html
    assert "Upload planner JSON" in viewer_html


def test_viewer_allows_drag_and_drop_planner_uploads() -> None:
    viewer_html = Path("viewer/index.html").read_text(encoding="utf-8")

    assert "handlePlannerDrop" in viewer_html
    assert "upload-active" in viewer_html
    assert "Drag and drop a planner JSON" in viewer_html
