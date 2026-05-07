param(
    [string]$LogDir = "plasma_checker_logs"
)

$logPath = Join-Path $PSScriptRoot "..\$LogDir"

if (-not (Test-Path $logPath)) {
    Write-Host "Log directory not found: $logPath"
    exit 0
}

$logFiles = Get-ChildItem -Path $logPath -Filter "*.log" -File

if ($logFiles.Count -eq 0) {
    Write-Host "No log files found in $logPath"
    exit 0
}

Write-Host "Found $($logFiles.Count) log file(s) in $logPath"
$logFiles | Remove-Item -Force
Write-Host "All log files removed."
