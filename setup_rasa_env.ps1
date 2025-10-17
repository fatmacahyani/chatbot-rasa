# Rasa Environment Setup Script
# This script sets default ports via environment variables

Write-Host "Setting up Rasa environment with default ports..." -ForegroundColor Green

# Navigate to the correct directory
Set-Location "C:\Users\YOGA\fp_nlp\demo_chatbot"

# Activate virtual environment
& "C:\Users\YOGA\fp_nlp\.venv\Scripts\Activate.ps1"

# Set environment variables for default ports
$env:RASA_SERVER_PORT = "5006"
$env:ACTION_SERVER_PORT = "5055"

Write-Host "Environment variables set:" -ForegroundColor Yellow
Write-Host "  RASA_SERVER_PORT = $env:RASA_SERVER_PORT"
Write-Host "  ACTION_SERVER_PORT = $env:ACTION_SERVER_PORT"
Write-Host ""

Write-Host "Now you can use simplified commands:" -ForegroundColor Cyan
Write-Host "  rasa inspect           # Will use port 5006"
Write-Host "  rasa run actions       # Will use port 5055"
Write-Host "  rasa shell --port 5005 # Still need to specify for shell"
Write-Host ""

Write-Host "Available commands:" -ForegroundColor Yellow
Write-Host "1. Start Rasa Inspector (port 5006)"
Write-Host "2. Start Action Server (port 5055)"
Write-Host "3. Start Rasa Shell (port 5005)"
Write-Host "4. Train model"
Write-Host "5. Start Inspector + Action Server (both)"
Write-Host "6. Just set environment and exit"
Write-Host ""

$choice = Read-Host "Enter your choice (1-6)"

switch ($choice) {
    "1" {
        Write-Host "Starting Rasa Inspector on default port 5006..." -ForegroundColor Cyan
        rasa inspect
    }
    "2" {
        Write-Host "Starting Action Server on default port 5055..." -ForegroundColor Cyan
        rasa run actions
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
        Start-Process powershell -ArgumentList "-Command", "Set-Location 'C:\Users\YOGA\fp_nlp\demo_chatbot'; & 'C:\Users\YOGA\fp_nlp\.venv\Scripts\Activate.ps1'; `$env:ACTION_SERVER_PORT='5055'; rasa run actions"
        Start-Sleep -Seconds 3
        Write-Host "Starting Inspector..."
        rasa inspect
    }
    "6" {
        Write-Host "Environment is set up. You can now run 'rasa inspect' without --port parameter." -ForegroundColor Green
        return
    }
    default {
        Write-Host "Invalid choice!" -ForegroundColor Red
    }
}

Read-Host "Press Enter to exit"