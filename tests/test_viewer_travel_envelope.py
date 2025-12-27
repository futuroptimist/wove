from tests.viewer_utils import load_viewer_source


def test_travel_envelope_cage_copy_present():
    html = load_viewer_source()

    assert "Planner travel envelope" in html
    assert "Machine profile travel envelope" in html
    assert "Travel envelope cage" in html


def test_travel_envelope_warns_on_missing_machine_axes():
    html = load_viewer_source()

    assert "comparisonDetails?.missingMachine" in html
    assert "machineProfileMissingAxes" in html


def test_travel_envelope_z_span_halos_present():
    html = load_viewer_source()

    assert "planner-z-span-halos" in html
    assert "Planner Z-span halos" in html
