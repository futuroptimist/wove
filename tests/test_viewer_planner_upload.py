from tests.viewer_assets import load_viewer_sources


def test_viewer_includes_planner_upload_control() -> None:
    viewer_html = load_viewer_sources()

    assert 'id="planner-upload"' in viewer_html
    assert "Upload planner JSON" in viewer_html


def test_viewer_allows_drag_and_drop_planner_uploads() -> None:
    viewer_html = load_viewer_sources()

    assert "handlePlannerDrop" in viewer_html
    assert "upload-active" in viewer_html
    assert "Drag and drop a planner JSON" in viewer_html
