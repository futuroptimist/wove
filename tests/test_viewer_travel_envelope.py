from pathlib import Path


def test_travel_envelope_cage_copy_present():
    html = Path("viewer/index.html").read_text(encoding="utf-8")

    assert "Planner travel envelope" in html
    assert "Machine profile travel envelope" in html
    assert "Travel envelope cage" in html
