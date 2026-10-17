#!/usr/bin/env bash
# Eye of the Storm — Launcher wrapper
# Handles venv activation automatically

DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -f "$DIR/venv/bin/activate" ]; then
    source "$DIR/venv/bin/activate"
fi

python3 "$DIR/main.py" "$@"
