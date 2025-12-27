from tests.viewer_assets import load_viewer_sources


def test_machine_profile_envelope_copy():
    html = load_viewer_sources()

    assert 'id="machine-profile-envelope"' in html
    assert "Machine profile envelope warming up…" in html
    assert "Machine profile envelope unavailable" in html
    assert "add travel_min_mm and travel_max_mm for:" in html
