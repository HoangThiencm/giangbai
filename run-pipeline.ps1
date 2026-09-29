# ==============================================================================
# Pipeline: Survey (Antigravity) -> Code (Grok CLI) -> Verify (Antigravity)
# ==============================================================================
param(
    # Cau hinh model cho Grok (mac dinh dung 4.7-build-fast va effort medium de tiet kiem quota)
    [string]$GrokModel = "grok-4.7-build-fast",
    [string]$GrokEffort = "medium", # low | medium | high
    
    # Model cho Antigravity (Gemini 3.8 Flash sieu nhanh, phan hoi 20-40s)
    [string]$AgyModel = "gemini-3.8-flash-high"
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Tim git executable (neu chua co trong PATH, tim qua GitHub Desktop)
$gitCmd = "git"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    $ghGit = Get-ChildItem -Path "$env:LOCALAPPDATA\GitHubDesktop\app-*\resources\app\git\cmd\git.exe" -ErrorAction SilentlyContinue | Select-Object -Last 1
    if ($ghGit) {
        $gitCmd = $ghGit.FullName
    }
}

$HandoffDir = "docs\handoff"
if (-not (Test-Path $HandoffDir)) {
    New-Item -ItemType Directory -Force -Path $HandoffDir | Out-Null
}

$TaskFile = "$HandoffDir\TASK.md"
if (-not (Test-Path $TaskFile)) {
    $defaultTask = @"
# TASK
Mo ta tinh nang hoac bug can lam o day...
"@
    Set-Content -Path $TaskFile -Value $defaultTask -Encoding utf8
    Write-Host "[!] Da tao $TaskFile. Vui long ghi yeu cau vao file nay roi chay lai." -ForegroundColor Yellow
    exit 1
}

# Kiem tra noi dung TASK.md co bi bo trong hoac con giu template khong
$taskContent = Get-Content -Raw -Encoding utf8 $TaskFile
if ([string]::IsNullOrWhiteSpace($taskContent) -or $taskContent -match "<\!-- Ghi r") {
    Write-Host "[!] $TaskFile chua co noi dung yeu cau thuc te. Vui long ghi ro yeu cau truoc khi chay." -ForegroundColor Yellow
    exit 1
}

# Xoa sach cac file cu tu lan chay truoc de tranh dung lai plan/prompt cu
Remove-Item "$HandoffDir\PLAN.md" -Force -ErrorAction SilentlyContinue
Remove-Item "$HandoffDir\IMPLEMENT.md" -Force -ErrorAction SilentlyContinue
Remove-Item "$HandoffDir\VERIFY.md" -Force -ErrorAction SilentlyContinue
Remove-Item "$HandoffDir\.lock" -Force -ErrorAction SilentlyContinue

Write-Host "`n>>> [BUOC 1/3] ANTIGRAVITY SURVEY..." -ForegroundColor Cyan
Write-Host "[*] Dang khao sat codebase bang model $AgyModel (uoc tinh 20-40s)..." -ForegroundColor DarkCyan

# 1. Survey: Chi doc codebase va lap ke hoach vao PLAN.md (gioi han dung pham vi trong TASK.md)
$surveyPrompt = @"
Chi survey, KHONG implement, KHONG sua source code du an.

1. Doc ki $TaskFile. Chi tap trung khao sat cac file duoc neu trong TASK.md hoac lien quan truc tiep den yeu cau do. Khong quet toan bo cac file khac trong repo de tiet kiem thoi gian.
2. Ghi de file $HandoffDir\PLAN.md:
   - Muc tieu
   - Danh sach file du kien tac dong
   - Cac buoc thuc hien chi tiet cho Coder
   - Rui ro va giai phap
   - Lenh may kiem thu cu the (test/lint/build/syntax check)
3. Ghi de file $HandoffDir\IMPLEMENT.md la prompt khep kin gui Coder:
   - Yeu cau implement dung $HandoffDir\PLAN.md
   - Khong tu mo rong scope, khong sua file ngoai danh sach
   - Xong viec thi tom tat diff ngan gon
4. Tao file $HandoffDir\.lock voi noi dung LOCK.
"@

agy -p $surveyPrompt --model $AgyModel --dangerously-skip-permissions --print-timeout 20m

if (-not (Test-Path "$HandoffDir\PLAN.md")) {
    throw "Survey that bai: Khong sinh ra duoc $HandoffDir\PLAN.md"
}

# Vong lap Code & Verify (toi da 3 luot neu co loi)
$maxAttempts = 3
$attempt = 1
$passed = $false

while ($attempt -le $maxAttempts -and -not $passed) {
    Write-Host "`n>>> [BUOC 2/3] GROK CODING (Lan $attempt/$maxAttempts)..." -ForegroundColor Green
    Write-Host "[*] Grok dang code bang model $GrokModel (effort: $GrokEffort)..." -ForegroundColor DarkGreen
    
    # 2. Coder: Grok CLI thuc thi voi model va effort da chon
    $implPrompt = Get-Content -Raw -Encoding utf8 "$HandoffDir\IMPLEMENT.md"
    grok -p $implPrompt --model $GrokModel --effort $GrokEffort --always-approve

    Write-Host "`n>>> [BUOC 3/3] ANTIGRAVITY VERIFY (Lan $attempt/$maxAttempts)..." -ForegroundColor Magenta
    Write-Host "[*] Dang kiem thu bang model $AgyModel..." -ForegroundColor DarkCyan

    # 3. Verify: Antigravity chay test may, KHONG sua code
    $verifyPrompt = @"
Chi kiem thu theo $HandoffDir\PLAN.md, TUYET DOI KHONG sua source code du an.

1. Chay cac lenh kiem thu/build/lint da ghi trong PLAN.md.
2. Ghi ket qua vao $HandoffDir\VERIFY.md:
   - Dong dau tien ghi ro: 'STATUS: PASS' hoac 'STATUS: FAIL'
   - Danh sach lenh da chay va ket qua
   - Neu FAIL: Trich xuat log loi chi tiet, file bi loi, nguyen nhan
3. Neu FAIL: Cap nhat lai $HandoffDir\IMPLEMENT.md chi ro bug can Grok sua.
"@

    agy -p $verifyPrompt --model $AgyModel --dangerously-skip-permissions --print-timeout 20m

    # Doc ket qua verify
    if (Test-Path "$HandoffDir\VERIFY.md") {
        $verifyContent = Get-Content -Raw -Encoding utf8 "$HandoffDir\VERIFY.md"
        if ($verifyContent -match "STATUS:\s*PASS") {
            $passed = $true
            Write-Host "`n=== KET QUA: PASS THANH CONG! ===" -ForegroundColor Green
            if (Test-Path "$HandoffDir\.lock") { Remove-Item "$HandoffDir\.lock" -Force }
            break
        } else {
            Write-Host "`n[!] Verify FAIL o lan $attempt. Xem log trong $HandoffDir\VERIFY.md" -ForegroundColor Red
            $attempt++
        }
    } else {
        throw "Khong tim thay file $HandoffDir\VERIFY.md sau khi test."
    }
}

# Am thanh thong bao hoan tat
try {
    [Console]::Beep(1000, 200)
    [Console]::Beep(1200, 200)
    [Console]::Beep(1500, 400)
} catch {}

if ($passed) {
    Write-Host "`n[V] Toan bo quy trinh da PASS thanh cong!" -ForegroundColor Green
    
    # Hoi xac nhan Commit & Push
    $ans = Read-Host "[?] Ban co muon Commit va Push len GitHub khong? (Y/n) [Mac dinh: Y]"
    if ($ans -eq "" -or $ans -match "^[yY]") {
        Write-Host "`nDang tien hanh Commit & Push..." -ForegroundColor Cyan
        & $gitCmd add -A
        & $gitCmd commit -m "Auto-pipeline: Hoan thanh task tu TASK.md"
        & $gitCmd push
        Write-Host "Da Push len GitHub thanh cong!" -ForegroundColor Green
    } else {
        Write-Host "Da bo qua buoc Push. Code van duoc luu tren may ban." -ForegroundColor Yellow
    }
} else {
    Write-Host "`n[X] Da thu $maxAttempts lan nhung van chua PASS hoan toan. Hay kiem tra $HandoffDir\VERIFY.md de xu ly them." -ForegroundColor Red
}