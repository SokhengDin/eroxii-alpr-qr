#!/usr/bin/env bash
set -euo pipefail

echo "================================================="
echo " eroxii-alpr-qr  |  Linux / macOS Auto Setup"
echo "================================================="

# ── Check Python ──────────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] python3 not found."
    echo "        Ubuntu/Debian : sudo apt install python3 python3-venv python3-pip"
    echo "        RHEL/Fedora   : sudo dnf install python3"
    exit 1
fi

PY_VER=$(python3 --version)
echo "[INFO] $PY_VER"

# ── Serial port permissions (Linux only) ──────────────────────────────────────
if [[ "$(uname -s)" == "Linux" ]]; then
    if ! groups | grep -q "dialout"; then
        echo "[INFO] Adding $USER to dialout group (serial port access) ..."
        sudo usermod -aG dialout "$USER"
        echo "[WARN] Log out and back in for group change to take effect."
    else
        echo "[INFO] User already in dialout group."
    fi
fi

# ── Create virtual environment ────────────────────────────────────────────────
if [[ ! -d ".venv" ]]; then
    echo "[INFO] Creating virtual environment ..."
    python3 -m venv .venv
else
    echo "[INFO] Virtual environment already exists."
fi

# ── Install dependencies ──────────────────────────────────────────────────────
echo "[INFO] Installing dependencies ..."
source .venv/bin/activate
pip install --upgrade pip --quiet
pip install -e . --quiet

# ── Create .env from example if not present ───────────────────────────────────
if [[ ! -f ".env" ]]; then
    echo "[INFO] Creating .env from .env.example ..."
    cp .env.example .env
    echo "[WARN] Edit .env and set SERIAL_PORT and AI_BASE_URL before starting."
else
    echo "[INFO] .env already exists — skipping."
fi

echo ""
echo "================================================="
echo " Setup complete!"
echo " 1. Edit .env  (set SERIAL_PORT & AI_BASE_URL)"
echo "    Linux serial port is usually /dev/ttyUSB0"
echo " 2. Run:"
echo "    source .venv/bin/activate"
echo "    python main.py"
echo "================================================="
