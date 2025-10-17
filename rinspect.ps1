# Rasa Inspect with Auto Port 5006
# Usage: Just run .\rinspect.ps1 instead of "rasa inspect --port 5006"

Write-Host "Starting Rasa Inspector on port 5006..." -ForegroundColor Green

# Set working directory to script location
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

# Activate virtual environment and run inspector
& "C:\Users\YOGA\fp_nlp\.venv\Scripts\python.exe" -m rasa inspect --port 5006