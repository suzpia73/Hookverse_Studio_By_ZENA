Add-Type -AssemblyName System.Drawing

$srcPath = "D:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\review\snap_at_13s.jpg"
$outPath = "D:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\IMF2화\IMF전날밤의비밀_ep02_cut03.jpg"

$bmp = [System.Drawing.Bitmap]::FromFile($srcPath)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

# ==========================================
# 뉴라 손에 든 스마트폰 화면: 시청자 정면 배터리 1% OLED 디스플레이 자연스러운 결합
# ==========================================
$px = 485
$py = 1045
$pw = 175
$ph = 270

# 1. 얇은 스마트폰 베젤 및 OLED 디스플레이
$screenBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(245, 5, 8, 12))
$borderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(180, 80, 95, 110), 2)
$g.FillRectangle($screenBrush, $px, $py, $pw, $ph)
$g.DrawRectangle($borderPen, $px, $py, $pw, $ph)

# 2. 상단 타임스탬프 & 상태
$fSmall = New-Object System.Drawing.Font("Arial", 8, [System.Drawing.FontStyle]::Bold)
$bDim = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(200, 160, 180, 200))
$g.DrawString("1997.11.21 00:00:15", $fSmall, $bDim, ($px + 12), ($py + 14))

# 3. 중앙 대형 배터리 1% 아이콘 & 게이지
$bx = $px + 18
$by = $py + 50
$bw = 72
$bh = 36
$batPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 239, 68, 68), 3) # 선명한 네온 레드 (#EF4444)
$g.DrawRectangle($batPen, $bx, $by, $bw, $bh)
# 배터리 양극 단자
$g.FillRectangle((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 239, 68, 68))), ($bx + $bw), ($by + 10), 4, 16)
# 1% 잔여 빨간 게이지
$g.FillRectangle((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 248, 113, 113))), ($bx + 4), ($by + 4), 8, ($bh - 8))

# 4. 배터리 1% 텍스트 (시청자가 0.1초 만에 인지할 수 있는 크기)
$fBat = New-Object System.Drawing.Font("Arial", 20, [System.Drawing.FontStyle]::Bold)
$bBat = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 239, 68, 68))
$g.DrawString("1%", $fBat, $bBat, ($bx + $bw + 12), ($by + 2))

# 5. 경고 메시지 (시네마틱 텍스트)
$fAlert = New-Object System.Drawing.Font("Malgun Gothic", 9, [System.Drawing.FontStyle]::Bold)
$bWarnY = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 250, 204, 21)) # 골든 옐로우
$bWarnR = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 248, 113, 113))

$g.DrawString("⚠️ 외환보유고 고갈 위기", $fAlert, $bWarnY, ($px + 12), ($py + 112))
$g.DrawString("기지국 연결 불가 (오프라인)", $fAlert, $bWarnR, ($px + 12), ($py + 140))

# 6. 하단 안내
$fSub = New-Object System.Drawing.Font("Malgun Gothic", 8, [System.Drawing.FontStyle]::Regular)
$g.DrawString("곧 전원이 종료됩니다...", $fSub, $bDim, ($px + 14), ($py + 185))
$g.DrawString("유선 공중전화 이용 권장", $fSub, $bWarnY, ($px + 14), ($py + 215))

# 7. 화면 위 맺힌 빗방울 텍스처
$rainBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(85, 255, 255, 255))
$rnd = New-Object System.Random(19971120)
for ($i = 0; $i -lt 28; $i++) {
    $rx = $rnd.Next($px + 3, $px + $pw - 3)
    $ry = $rnd.Next($py + 3, $py + $ph - 3)
    $rw = $rnd.Next(3, 7)
    $rh = $rw + $rnd.Next(2, 5)
    $g.FillEllipse($rainBrush, $rx, $ry, $rw, $rh)
}

# 8. 스마트폰 화면에서 뿜어져 나오는 붉은빛 글로우가 뉴라 얼굴/손을 자연스럽게 감쌈
$glowBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(25, 239, 68, 68))
$g.FillEllipse($glowBrush, 475, 960, 195, 90)

$g.Dispose()

$bmp.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$bmp.Dispose()
Write-Host "[+] ✅ Clean cut 03 created: $outPath"
