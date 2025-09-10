#!/usr/bin/env bash
set -euo pipefail

# Proje kök dizinden çalıştır:
cd "$(dirname "$0")/.."

# Sanal ortamı etkinleştir
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

python src/app.py
