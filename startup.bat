@echo off
set "PROJECT_DIR=%~dp0"
set "PROJECT_DIR=%PROJECT_DIR:~0,-1%"

cd /d "%PROJECT_DIR%"
start "" "%PROJECT_DIR%\.venv\Scripts\pythonw.exe" "%PROJECT_DIR%\main.py"
