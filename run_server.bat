@echo off
echo Starting Agribot Server...
cd /d %~dp0
set PYTHONPATH=%PYTHONPATH%;%~dp0
waitress-serve --host=0.0.0.0 --port=5000 app:app > server.log 2>&1