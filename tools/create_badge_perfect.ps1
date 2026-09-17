Add-Type -AssemblyName System.Drawing

$W = 310
$H = 100

$bmp = New-Object System.Drawing.Bitmap $W, $H
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear([System.Drawing.Color]::Transparent)

# 쨍한 로열블루 각진 직사각형 박스 (#005BEA)
$blueBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 0, 91, 234))
$g.FillRectangle($blueBrush, 0, 0, $W, $H)

# 폰트 로드: Georgia 또는 Times New Roman 또는 Arial
$fontFamily = "Georgia"
try {
    $testFont = New-Object System.Drawing.Font($fontFamily, 10)
} catch {
    $fontFamily = "Arial"
}

# 대문자 가운데 정렬 스펙
$fTop = New-Object System.Drawing.Font($fontFamily, 22, [System.Drawing.FontStyle]::Bold)
$fBot = New-Object System.Drawing.Font($fontFamily, 20, [System.Drawing.FontStyle]::Bold)

$whiteBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::White)
$sf = New-Object System.Drawing.StringFormat
$sf.Alignment = [System.Drawing.StringAlignment]::Center
$sf.LineAlignment = [System.Drawing.StringAlignment]::Center

# 대문자 두 줄: HOOKVERSE / STUDIO (가운데 정렬)
$rectTop = New-Object System.Drawing.RectangleF(0, 8, $W, 42)
$rectBot = New-Object System.Drawing.RectangleF(0, 50, $W, 42)

$g.DrawString("HOOKVERSE", $fTop, $whiteBrush, $rectTop, $sf)
$g.DrawString("STUDIO", $fBot, $whiteBrush, $rectBot, $sf)

$outPath = "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\hookverse_top_left_badge.png"
$bmp.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)

$g.Dispose()
$bmp.Dispose()
Write-Host "[+] ✅ HOOKVERSE STUDIO 대문자 가운데정렬 배지 생성 완료: $outPath"
