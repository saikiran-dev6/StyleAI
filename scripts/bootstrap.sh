#!/usr/bin/env bash
set -euo pipefail

echo "==> Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

# Source virtualenv
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
fi

echo "==> Installing Python dependencies..."
pip install --upgrade pip
if [ -f "requirements.lock.txt" ]; then
    pip install -r requirements.lock.txt
else
    pip install -r requirements.in
fi

if [ ! -f ".env" ]; then
    echo "==> Creating .env from .env.example..."
    cp .env.example .env
fi

echo "==> Environment bootstrap complete."
