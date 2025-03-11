# This script checks its execution privileges and elevates it if not running 
# as admin. The impedance.py script can start and stop the GDS service, which 
# requires admin privileges.

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "Privileges escalated."

    $pythonScriptPath = "$PSScriptRoot\main.py"

    Start-Process powershell -WindowStyle Hidden -Verb RunAs -ArgumentList "-ExecutionPolicy", "Bypass", "-Command", "conda activate impedance; python `"$pythonScriptPath`""
    
    Write-Host "Starting, please wait..."
    Start-Sleep(4)
    
    # Close the PowerShell window
    Stop-Process -Id $PID
}

conda activate impedance
python "$PSSCriptRoot\main.py" $args
