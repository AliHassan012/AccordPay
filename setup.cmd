@echo off
setlocal
cd /d "%~dp0"
if not exist "runtime\tmp" mkdir "runtime\tmp"
set "TEMP=%~dp0runtime\tmp"
set "TMP=%TEMP%"
set "BUILD_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if not exist "%BUILD_PYTHON%" set "BUILD_PYTHON=python"
if not exist ".venv\Scripts\python.exe" (
  "%BUILD_PYTHON%" -m venv .venv
  if errorlevel 1 goto failed
)
".venv\Scripts\python.exe" -m pip install --no-cache-dir -r requirements.txt
if errorlevel 1 goto failed
".venv\Scripts\python.exe" init_env.py
if errorlevel 1 goto failed
echo Setup complete. Enter your private values in .env, then open start.cmd.
pause
exit /b 0
:failed
echo Setup failed. Keep this message and ask for help.
pause
exit /b 1
