from pathlib import Path


def test_travel_envelope_cage_copy_present():
    html = Path("viewer/index.html").read_text(encoding="utf-8")

    assert "Planner travel envelope" in html
    assert "Machine profile travel envelope" in html
    assert "Travel envelope cage" in html


def test_travel_envelope_warns_on_missing_machine_axes():
    html = Path("viewer/index.html").read_text(encoding="utf-8")

    assert "comparisonDetails?.missingMachine" in html
    assert "machineProfileMissingAxes" in html
