#!/usr/bin/env bash
set -e

# style checks
flake8 .
isort --check-only .
black --check .

# run tests
echo "Running tests"
pytest -q
