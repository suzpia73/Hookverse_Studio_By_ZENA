Add-Type -AssemblyName System.Drawing
$imgPath = "C:\Users\june2\.gemini\antigravity-ide\brain\61a5625b-e4de-46aa-9bbf-aae3a36edc6a\cut02_full_detail_view_1789653205064.png"
$src = [System.Drawing.Bitmap]::FromFile($imgPath)
$rect = New-Object System.Drawing.Rectangle(385, 43, 390, 745)
$crop = $src.Clone($rect, $src.PixelFormat)
$outPath = "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\IMF2화\IMF전날밤의비밀_ep02_cut02_master.jpg"
$crop.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$src.Dispose()
$crop.Dispose()
Write-Host "[OK] Clean Cut 02 Master Cropped: $outPath"
