Add-Type -AssemblyName System.Drawing

# 1. 좌측 상단 배지 생성
$w = 320
$h = 130
$bmp = New-Object System.Drawing.Bitmap($w, $h)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

# 로열 블루 배경 (#005BEA = 0, 91, 234)
$brushBg = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 0, 91, 234))
$g.FillRectangle($brushBg, 0, 0, $w, $h)

# 세리프 폰트 (Georgia Bold)
$font = New-Object System.Drawing.Font("Georgia", 28, [System.Drawing.FontStyle]::Bold)
$brushText = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)

$g.DrawString("Hookverse", $font, $brushText, 20, 12)
$g.DrawString("Studio", $font, $brushText, 20, 64)

$g.Dispose()
$badgePath = "D:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\hookverse_top_left_badge.png"
$bmp.Save($badgePath, [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
Write-Host "[+] Badge created: $badgePath"

# 2. 우측 상단 엠블럼 검은 사각 박스 완전 투명화 (원형 누끼)
$srcLogo = "D:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\hookverse_studio_logo.png"
$dstLogo = "D:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\hookverse_studio_logo_transparent.png"

if (Test-Path $srcLogo) {
    $srcBmp = [System.Drawing.Bitmap]::FromFile($srcLogo)
    $lw = $srcBmp.Width
    $lh = $srcBmp.Height
    $outBmp = New-Object System.Drawing.Bitmap($lw, $lh, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    
    $cx = $lw / 2.0
    $cy = $lh / 2.0
    $radius = [Math]::Min($lw, $lh) / 2.0 - 4.0
    $r2 = $radius * $radius
    
    for ($y = 0; $y -lt $lh; $y++) {
        for ($x = 0; $x -lt $lw; $x++) {
            $dx = $x - $cx
            $dy = $y - $cy
            $dist2 = $dx * $dx + $dy * $dy
            
            if ($dist2 -le $r2) {
                $c = $srcBmp.GetPixel($x, $y)
                # 원 안쪽에서도 순수 어두운 배경(R<15, G<15, B<15)은 투명화
                if ($c.R -lt 15 -and $c.G -lt 15 -and $c.B -lt 15) {
                    $outBmp.SetPixel($x, $y, [System.Drawing.Color]::FromArgb(0, 0, 0, 0))
                } else {
                    $outBmp.SetPixel($x, $y, $c)
                }
            } else {
                # 원 밖은 100% 완전 투명!
                $outBmp.SetPixel($x, $y, [System.Drawing.Color]::FromArgb(0, 0, 0, 0))
            }
        }
    }
    
    $srcBmp.Dispose()
    $outBmp.Save($dstLogo, [System.Drawing.Imaging.ImageFormat]::Png)
    $outBmp.Dispose()
    Write-Host "[+] Transparent Logo created: $dstLogo"
}
