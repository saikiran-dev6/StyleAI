#!/usr/bin/env bash
set -euo pipefail

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
fi

echo "==> Running Ruff linter..."
ruff check .

echo "==> Running Pytest suite with coverage check (target >= 85%)..."
pytest --cov=styleai --cov-report=term-missing --cov-report=xml --cov-fail-under=85 tests/

echo "==> All linting and test checks passed successfully!"
