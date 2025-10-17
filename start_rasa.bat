@echo off
REM Rasa Startup Script with Fixed Ports
REM This script ensures consistent port usage

echo Starting Rasa services with fixed ports...
echo.

REM Navigate to the correct directory
cd /d "C:\Users\YOGA\fp_nlp\demo_chatbot"

REM Activate virtual environment
call "C:\Users\YOGA\fp_nlp\.venv\Scripts\Activate.bat"

echo Available commands:
echo 1. Start Rasa Inspector (port 5006)
echo 2. Start Action Server (port 5055)
echo 3. Start Rasa Shell (port 5005)
echo 4. Train model
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Starting Rasa Inspector on port 5006...
    rasa inspect --port 5006
) else if "%choice%"=="2" (
    echo Starting Action Server on port 5055...
    rasa run actions --port 5055
) else if "%choice%"=="3" (
    echo Starting Rasa Shell on port 5005...
    rasa shell --port 5005
) else if "%choice%"=="4" (
    echo Training Rasa model...
    rasa train
) else (
    echo Invalid choice!
)

pause