@echo off
echo Starting Interview AI Assistant...

REM Start the backend server
start cmd /k "cd backend && python server.py"

REM Wait for the server to start
timeout /t 5

REM Start the desktop application
python app.py
