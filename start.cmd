@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run setup.cmd first.
  pause
  exit /b 1
)
echo Open http://127.0.0.1:8000 in your browser.
".venv\Scripts\python.exe" -m uvicorn app:app --host 127.0.0.1 --port 8000 --no-access-log
pause
