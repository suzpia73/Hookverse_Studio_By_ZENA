Add-Type -AssemblyName System.Drawing
$imgPath = "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\IMF2화\IMF전날밤의비밀_ep02_cut01_flow.png"
$src = [System.Drawing.Bitmap]::FromFile($imgPath)
# 하단 UI 바 배제: Y 43~790 (높이 745)
$rect = New-Object System.Drawing.Rectangle(385, 43, 390, 745)
$crop = $src.Clone($rect, $src.PixelFormat)
$outPath = "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\IMF2화\IMF전날밤의비밀_ep02_cut01_master.jpg"
$crop.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$src.Dispose()
$crop.Dispose()
Write-Host "[OK] Clean Master Cropped: $outPath"
