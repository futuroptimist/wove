from pathlib import Path


def test_planner_metadata_tracks_file_size() -> None:
    viewer_html = Path("viewer/index.html").read_text(encoding="utf-8")

    assert "fileSizeBytes" in viewer_html
    assert "File size" in viewer_html
