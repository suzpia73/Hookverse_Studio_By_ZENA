Add-Type -AssemblyName System.Drawing

$p = "D:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\review\snap_at_13s.jpg"
$bmp = [System.Drawing.Bitmap]::FromFile($p)
Write-Host "Width: $($bmp.Width), Height: $($bmp.Height)"
$bmp.Dispose()
