@echo off
cd /d "%~dp0"
echo Close the running app terminal before continuing.
echo This archives the previous fictional demo history and restores starting balances.
pause
".venv\Scripts\python.exe" reset_demo.py --confirm
pause
