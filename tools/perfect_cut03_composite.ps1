Add-Type -AssemblyName System.Drawing

$srcPath = "D:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\review\snap_at_13s.jpg"
$outPath = "D:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\IMF2화\IMF전날밤의비밀_ep02_cut03.jpg"

$bmp = [System.Drawing.Bitmap]::FromFile($srcPath)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

# ==========================================
# 1. 부스 밖 유리창 너머: 좁혀오는 검은 양복 추격자들의 그림자/실루엣 합성
# ==========================================
# 우측 유리창 너머 어두운 골목길에 우산을 쓴 검은 양복 실루엣 2명 섀도우 블렌딩
$shadowBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(140, 10, 15, 25))

# 요원 1 (우측 창문 너머 다가오는 검은 우산 실루엣)
$g.FillEllipse($shadowBrush, 820, 720, 190, 75)  # 우산 돔
$g.FillRectangle($shadowBrush, 890, 780, 55, 140) # 몸체/코트

# 요원 2 (좌측 전화기 뒤편 창문 너머 희미한 우산 실루엣)
$shadowBrushFar = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(110, 8, 12, 20))
$g.FillEllipse($shadowBrushFar, 70, 760, 160, 60)
$g.FillRectangle($shadowBrushFar, 135, 810, 45, 110)

# ==========================================
# 2. 뉴라 손에 든 스마트폰 화면: 시청자 정면 배터리 1% OLED 디스플레이 완벽 합성
# ==========================================
# 스마트폰 위치 (뉴라의 양손 안쪽: 약 X: 485, Y: 1045, W: 175, H: 275)
$px = 482
$py = 1045
$pw = 180
$ph = 275

# OLED 블랙 스크린
$screenBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(250, 4, 6, 10))
$borderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(200, 40, 48, 60), 2)
$g.FillRectangle($screenBrush, $px, $py, $pw, $ph)
$g.DrawRectangle($borderPen, $px, $py, $pw, $ph)

# 상단 타임스탬프
$fTime = New-Object System.Drawing.Font("Arial", 9, [System.Drawing.FontStyle]::Bold)
$bTime = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(220, 180, 200, 220))
$g.DrawString("1997.11.21 00:00:15", $fTime, $bTime, ($px + 14), ($py + 15))

# 배터리 1% 아이콘 & 텍스트
# 배터리 외곽선 (빨간 네온)
$batPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 245, 50, 65), 2)
$bx = $px + 28
$by = $py + 55
$bw = 65
$bh = 32
$g.DrawRectangle($batPen, $bx, $by, $bw, $bh)
# 배터리 단자
$g.FillRectangle((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 245, 50, 65))), ($bx + $bw), ($by + 8), 4, 16)
# 1% 잔여 빨간 게이지
$g.FillRectangle((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 30, 50))), ($bx + 3), ($by + 3), 7, ($bh - 6))

# 배터리 1% 텍스트 (빨간 볼드)
$fBat = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
$bBat = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 50, 70))
$g.DrawString("1%", $fBat, $bBat, ($bx + $bw + 12), ($by + 4))

# 경고 문구 (노란색/빨간색 네온)
$fAlert = New-Object System.Drawing.Font("Malgun Gothic", 9, [System.Drawing.FontStyle]::Bold)
$bAlertY = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 250, 204, 21))
$bAlertR = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 100, 100))

$g.DrawString("⚠️ 외환보유고 위기 경고", $fAlert, $bAlertY, ($px + 14), ($py + 115))
$g.DrawString("기지국 신호 없음 (망분리)", $fAlert, $bAlertR, ($px + 14), ($py + 145))

# 디바이스 종료 안내
$fSub = New-Object System.Drawing.Font("Malgun Gothic", 8, [System.Drawing.FontStyle]::Regular)
$bSub = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(190, 160, 175, 190))
$g.DrawString("곧 전원이 종료됩니다...", $fSub, $bSub, ($px + 18), ($py + 195))
$g.DrawString("유선 공중전화 이용 요망", $fSub, $bTime, ($px + 18), ($py + 225))

# 스마트폰 화면에 송글송글 맺힌 빗방울 텍스처
$rainBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(90, 255, 255, 255))
$rnd = New-Object System.Random(19971120)
for ($i = 0; $i -lt 35; $i++) {
    $rx = $rnd.Next($px + 4, $px + $pw - 4)
    $ry = $rnd.Next($py + 4, $py + $ph - 4)
    $rw = $rnd.Next(3, 8)
    $rh = $rw + $rnd.Next(2, 6)
    $g.FillEllipse($rainBrush, $rx, $ry, $rw, $rh)
}

# 스마트폰 화면에서 뉴라 턱선/얼굴로 뿜어지는 붉은빛 앰비언트 글로우 반사
$glowBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(35, 255, 50, 70))
$g.FillEllipse($glowBrush, 490, 930, 160, 110)

$g.Dispose()

# 저장
$bmp.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$bmp.Dispose()
Write-Host "[+] ✅ 컷 03 완벽 복합 완성: $outPath"
