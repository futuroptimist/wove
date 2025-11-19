from pathlib import Path


def test_machine_profile_envelope_copy():
    html = Path("viewer/index.html").read_text(encoding="utf-8")

    assert 'id="machine-profile-envelope"' in html
    assert "Machine profile envelope warming up…" in html
    assert "Machine profile envelope unavailable" in html
