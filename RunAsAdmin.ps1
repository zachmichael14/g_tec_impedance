# This script checks its execution privileges and elevates it if not running 
# as admin. The impedance.py script can start and stop the GDS service, which 
# requires admin privileges.

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    $pythonScriptPath = "$PSScriptRoot\impedance.py"

    Start-Process powershell -WindowStyle Hidden -Verb RunAs -ArgumentList "-ExecutionPolicy", "Bypass", "-Command", "conda activate impedance; python `"$pythonScriptPath`""
    exit
}

conda activate impedance
python "$PSSCriptRoot\impedance.py" $args