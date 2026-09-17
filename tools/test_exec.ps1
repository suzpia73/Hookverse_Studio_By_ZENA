Write-Host "Testing Python and FFmpeg inside PS script..."
$py = "C:\Users\june2\AppData\Local\Programs\Python\Python314\python.exe"
if (Test-Path $py) {
    Write-Host "Found Python at $py"
    & $py --version
} else {
    Write-Host "Python not found at $py"
}
