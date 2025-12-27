from .viewer_source import load_viewer_bundle


def test_travel_envelope_cage_copy_present():
    html = load_viewer_bundle()

    assert "Planner travel envelope" in html
    assert "Machine profile travel envelope" in html
    assert "Travel envelope cage" in html


def test_travel_envelope_warns_on_missing_machine_axes():
    html = load_viewer_bundle()

    assert "comparisonDetails?.missingMachine" in html
    assert "machineProfileMissingAxes" in html


def test_travel_envelope_z_span_halos_present():
    html = load_viewer_bundle()

    assert "planner-z-span-halos" in html
    assert "Planner Z-span halos" in html
