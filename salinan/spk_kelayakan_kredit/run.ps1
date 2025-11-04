# run.ps1 - Run the main application in PowerShell safely
# Usage: .\run.ps1
$python = "python"  # or set full path to python.exe
$script = Join-Path $PSScriptRoot "main.py"

if (-not (Test-Path $script)) {
    Write-Error "main.py not found in $PSScriptRoot"
    exit 1
}

# Use call operator & to execute properly in PowerShell
& $python $script
