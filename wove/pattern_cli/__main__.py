"""Entry point for ``python -m wove.pattern_cli``."""

from __future__ import annotations

from . import main

if __name__ == "__main__":  # pragma: no cover - exercised via CLI tests
    raise SystemExit(main())
