from tests.viewer_utils import load_viewer_source


def test_planner_metadata_tracks_file_size() -> None:
    viewer_html = load_viewer_source()

    assert "fileSizeBytes" in viewer_html
    assert "File size" in viewer_html


def test_planner_metadata_tracks_file_name() -> None:
    viewer_html = load_viewer_source()

    assert "fileName" in viewer_html
    assert "File name" in viewer_html
