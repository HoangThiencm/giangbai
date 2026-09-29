# ==============================================================================
# Pipeline: Survey (Antigravity) -> Code (Grok CLI) -> Verify (Antigravity)
# ==============================================================================
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$HandoffDir = "docs\handoff"
if (-not (Test-Path $HandoffDir)) {
    New-Item -ItemType Directory -Force -Path $HandoffDir | Out-Null
}

$TaskFile = "$HandoffDir\TASK.md"
if (-not (Test-Path $TaskFile)) {
    @"
# Task
Mô tả tính năng hoặc bug cần làm ở đây...
"@ | Set-Content -Encoding utf8 $TaskFile
    Write-Host "[!] Đã tạo $TaskFile. Vui lòng ghi yêu cầu vào file này rồi chạy lại." -ForegroundColor Yellow
    exit 1
}

Write-Host "`n>>> [BƯỚC 1/3] ANTIGRAVITY SURVEY..." -ForegroundColor Cyan

# 1. Survey: Chỉ đọc codebase và lập kế hoạch vào PLAN.md
agy -p @"
Chỉ survey, KHÔNG implement, KHÔNG sửa source code dự án.

1. Đọc kĩ $TaskFile và codebase liên quan.
2. Ghi đè file $HandoffDir\PLAN.md:
   - Mục tiêu
   - Danh sách file dự kiến tác động
   - Các bước thực hiện chi tiết cho Coder
   - Rủi ro & giải pháp
   - Lệnh máy kiểm thử cụ thể (test/lint/build/syntax check)
3. Ghi đè file $HandoffDir\IMPLEMENT.md là prompt khép kín gửi Coder:
   - Yêu cầu implement đúng $HandoffDir\PLAN.md
   - Không tự mở rộng scope, không sửa file ngoài danh sách
   - Xong việc thì tóm tắt diff ngắn gọn
4. Tạo file $HandoffDir\.lock với nội dung LOCK.
"@ --print-timeout 20m

if (-not (Test-Path "$HandoffDir\PLAN.md")) {
    throw "Survey thất bại: Không sinh ra được $HandoffDir\PLAN.md"
}

# Vòng lặp Code & Verify (tối đa 3 lượt nếu có lỗi)
$maxAttempts = 3
$attempt = 1
$passed = $false

while ($attempt -le $maxAttempts -and -not $passed) {
    Write-Host "`n>>> [BƯỚC 2/3] GROK CODING (Lần $attempt/$maxAttempts)..." -ForegroundColor Green
    
    # 2. Coder: Grok CLI thực thi
    $implPrompt = Get-Content -Raw -Encoding utf8 "$HandoffDir\IMPLEMENT.md"
    grok -p $implPrompt

    Write-Host "`n>>> [BƯỚC 3/3] ANTIGRAVITY VERIFY (Lần $attempt/$maxAttempts)..." -ForegroundColor Magenta

    # 3. Verify: Antigravity chạy test máy, KHÔNG sửa code
    agy -p @"
Chỉ kiểm thử theo $HandoffDir\PLAN.md, TUYỆT ĐỐI KHÔNG sửa source code dự án.

1. Chạy các lệnh kiểm thử/build/lint đã ghi trong PLAN.md.
2. Ghi kết quả vào $HandoffDir\VERIFY.md:
   - Dòng đầu tiên ghi rõ: 'STATUS: PASS' hoặc 'STATUS: FAIL'
   - Danh sách lệnh đã chạy và kết quả
   - Nếu FAIL: Trích xuất log lỗi chi tiết, file bị lỗi, nguyên nhân
3. Nếu FAIL: Cập nhật lại $HandoffDir\IMPLEMENT.md chỉ rõ bug cần Grok sửa.
"@ --print-timeout 20m

    # Đọc kết quả verify
    if (Test-Path "$HandoffDir\VERIFY.md") {
        $verifyContent = Get-Content -Raw -Encoding utf8 "$HandoffDir\VERIFY.md"
        if ($verifyContent -match "STATUS:\s*PASS") {
            $passed = $true
            Write-Host "`n=== KẾT QUẢ: PASS THÀNH CÔNG! ===" -ForegroundColor Green
            if (Test-Path "$HandoffDir\.lock") { Remove-Item "$HandoffDir\.lock" -Force }
            break
        } else {
            Write-Host "`n[!] Verify FAIL ở lần $attempt. Xem log trong $HandoffDir\VERIFY.md" -ForegroundColor Red
            $attempt++
        }
    } else {
        throw "Không tìm thấy file $HandoffDir\VERIFY.md sau khi test."
    }
}

if (-not $passed) {
    Write-Host "`n[X] Đã thử $maxAttempts lần nhưng vẫn chưa PASS hoàn toàn. Hãy kiểm tra $HandoffDir\VERIFY.md để xử lý thêm." -ForegroundColor Red
}