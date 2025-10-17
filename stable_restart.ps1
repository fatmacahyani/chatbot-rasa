# Script untuk restart dengan konfigurasi stabil
Write-Host "=== Stable RASA Restart ===" -ForegroundColor Cyan

# Hentikan semua proses RASA
Write-Host "Stopping all RASA processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.MainWindowTitle -like "*rasa*"} | Stop-Process -Force -ErrorAction SilentlyContinue
taskkill /f /im python.exe 2>$null

Start-Sleep -Seconds 3

# Navigasi ke direktori proyek
$projectPath = "C:\Users\YOGA\fp_nlp\demo_chatbot"
Set-Location $projectPath

# Update endpoints.yml dengan konfigurasi stabil
$stableEndpoints = @"
# Stable endpoint configuration
action_endpoint:
  url: "http://localhost:5055/webhook"

# Explicit tracker store configuration
tracker_store:
  type: InMemoryTrackerStore

# Event broker for better session management
event_broker:
  type: file
  path: events.log

# Session configuration
session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true
"@

Write-Host "Updating endpoints.yml for stability..." -ForegroundColor Green
$stableEndpoints | Out-File -FilePath "endpoints.yml" -Encoding UTF8

# Aktivasi virtual environment
& "fp_nlp\.venv\Scripts\activate"

# Start Action Server dengan restart otomatis
Write-Host "Starting Action Server with auto-restart..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; fp_nlp\.venv\Scripts\activate; while(`$true) { try { Write-Host 'Starting Action Server...' -ForegroundColor Green; rasa run actions --port 5055 } catch { Write-Host 'Action Server crashed, restarting...' -ForegroundColor Red; Start-Sleep 2 } }"

# Tunggu Action Server siap
Start-Sleep -Seconds 10

# Verifikasi Action Server
$maxRetries = 3
for ($i = 1; $i -le $maxRetries; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5055/health" -TimeoutSec 5 -ErrorAction Stop
        Write-Host "✓ Action Server verified!" -ForegroundColor Green
        break
    } catch {
        Write-Host "Attempt $i/$maxRetries - Waiting for Action Server..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    }
}

# Start Inspector dengan session cleanup
Write-Host "Starting Inspector with session cleanup..." -ForegroundColor Green
rasa inspect --port 5007 --cors "*" --debug