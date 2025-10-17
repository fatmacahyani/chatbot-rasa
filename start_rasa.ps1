# Rasa Startup Script with Fixed Ports
# This script ensures consistent port usage

Write-Host "Starting Rasa services with fixed ports..." -ForegroundColor Green
Write-Host ""

# Navigate to the correct directory
Set-Location "C:\Users\YOGA\fp_nlp\demo_chatbot"

# Activate virtual environment
& "C:\Users\YOGA\fp_nlp\.venv\Scripts\Activate.ps1"

Write-Host "Available commands:" -ForegroundColor Yellow
Write-Host "1. Start Rasa Inspector (port 5006)"
Write-Host "2. Start Action Server (port 5055)"
Write-Host "3. Start Rasa Shell (port 5005)"
Write-Host "4. Train model"
Write-Host "5. Start Inspector + Action Server (both)"
Write-Host ""

$choice = Read-Host "Enter your choice (1-5)"

switch ($choice) {
    "1" {
        Write-Host "Starting Rasa Inspector on port 5006..." -ForegroundColor Cyan
        rasa inspect --port 5006
    }
    "2" {
        Write-Host "Starting Action Server on port 5055..." -ForegroundColor Cyan
        rasa run actions --port 5055
    }
    "3" {
        Write-Host "Starting Rasa Shell on port 5005..." -ForegroundColor Cyan
        rasa shell --port 5005
    }
    "4" {
        Write-Host "Training Rasa model..." -ForegroundColor Cyan
        rasa train
    }
    "5" {
        Write-Host "Starting both Inspector and Action Server..." -ForegroundColor Cyan
        Write-Host "Starting Action Server in background..."
        Start-Process powershell -ArgumentList "-Command", "Set-Location 'C:\Users\YOGA\fp_nlp\demo_chatbot'; & 'C:\Users\YOGA\fp_nlp\.venv\Scripts\Activate.ps1'; rasa run actions --port 5055"
        Start-Sleep -Seconds 3
        Write-Host "Starting Inspector..."
        rasa inspect --port 5006
    }
    default {
        Write-Host "Invalid choice!" -ForegroundColor Red
    }
}

Read-Host "Press Enter to exit"