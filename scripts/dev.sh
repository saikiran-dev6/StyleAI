#!/usr/bin/env bash
set -euo pipefail

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
fi

export FLASK_ENV=development
export APP_HOST=0.0.0.0
export APP_PORT=8080

echo "==> Starting StyleAI local development server on http://localhost:8080"
python app.py
