@echo off
setlocal EnableDelayedExpansion

echo =================================================
echo  eroxii-alpr-qr  ^|  Setup
echo =================================================

:: ── Check Python ──────────────────────────────────────────────────────────────
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.12+ from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo [INFO] Python %PY_VER%

:: ── Create .venv ──────────────────────────────────────────────────────────────
if not exist ".venv" (
    echo [INFO] Creating .venv ...
    python -m venv .venv
) else (
    echo [INFO] .venv already exists.
)

:: ── Install dependencies ──────────────────────────────────────────────────────
echo [INFO] Installing dependencies ...
call .venv\Scripts\activate.bat
pip install -e . --quiet

:: ── Create .env ───────────────────────────────────────────────────────────────
if not exist ".env" (
    echo [INFO] Creating .env from .env.example ...
    copy .env.example .env >nul
    echo [WARN] Edit .env before running.
) else (
    echo [INFO] .env already exists.
)

echo.
echo [DONE] Run: python main.py
pause
