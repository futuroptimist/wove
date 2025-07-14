#!/usr/bin/env bash
set -e

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
pytest -q

# docs checks
if command -v pyspelling >/dev/null 2>&1 && [ -f .spellcheck.yaml ]; then
  pyspelling -c .spellcheck.yaml || true
fi
linkchecker README.md docs/ || true
