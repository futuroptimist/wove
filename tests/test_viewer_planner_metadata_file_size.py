from .viewer_source import load_viewer_bundle


def test_planner_metadata_tracks_file_size() -> None:
    viewer_html = load_viewer_bundle()

    assert "fileSizeBytes" in viewer_html
    assert "File size" in viewer_html


def test_planner_metadata_tracks_file_name() -> None:
    viewer_html = load_viewer_bundle()

    assert "fileName" in viewer_html
    assert "File name" in viewer_html
