from tests.viewer_utils import load_viewer_source


def test_machine_profile_envelope_copy():
    html = load_viewer_source()

    assert 'id="machine-profile-envelope"' in html
    assert "Machine profile envelope warming up…" in html
    assert "Machine profile envelope unavailable" in html
    assert "add travel_min_mm and travel_max_mm for:" in html
