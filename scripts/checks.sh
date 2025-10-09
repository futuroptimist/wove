#!/usr/bin/env bash
set -e

# Ensure runtime dependencies are installed for the checks below.
if [ -f requirements.txt ]; then
  python -m pip install --disable-pip-version-check -r requirements.txt >/dev/null
fi

# python checks
flake8 . --exclude=.venv || true
isort --check-only . --skip .venv || true
black --check . --exclude ".venv/" || true

# js checks
if [ -f package.json ]; then
  npm ci
  npx playwright install --with-deps
  npm run lint
  npm run format:check
  npm test -- --coverage
fi

echo "Running tests"
python -m pytest -q

# docs checks
if command -v pyspelling >/dev/null 2>&1 && [ -f .spellcheck.yaml ]; then
  pyspelling -c .spellcheck.yaml || true
fi
linkchecker README.md docs/ || true
