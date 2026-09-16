# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Mục 1: Điều chỉnh số vòng tròn Stepper từ 1 3 4 thành 1 2 3**:
  - `canvas_soankhbd.html`: Khối `data-step="3"` hiển thị `<span class="khbd-step-num">2</span>`; khối `data-step="4"` hiển thị `<span class="khbd-step-num">3</span>`. Các thuộc tính logic `data-step="3"`, `data-step="4"` và toàn bộ DOM IDs (`step3Badge`, `step4Badge`, `btnStep3Recommend`, `btnStartComposeFromStep4`) được giữ nguyên vẹn để đảm bảo tương thích 100% với `js/khbd-app.js`.
  - `backupcode viettailieu/canvas_soankhbd.html`: Đã đồng bộ cấu trúc tương tự, hiển thị 1–2–3 và cập nhật nhãn `Bước 2`, `Bước 3`.
  - Thuộc tính accessibility `aria-label` của `#khbdWorkflowStepper` cập nhật thành `"Quy trình 3 bước soạn KHBD"`.
- **Mục 2: Xử lý lỗi nạp danh mục chương trình từ host**:
  - Chuỗi query cache-busting cho các module Canvas (`khbd-curriculum.js`, `khbd-gemini.js`, `khbd-docx.js`, `khbd-pedagogy-catalog.js`) đã được nâng lên `20260916-canvas-module-v9` trong cả `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`.
  - Tệp `js/khbd-curriculum.js` gốc trong kho lưu trữ đầy đủ 173.676 bytes. Khi người dùng ra lệnh commit và push lên nhánh `main`, workflow GitHub Actions `.github/workflows/ftp-deploy.yml` sẽ tự động deploy tệp này lên hosting `hoangthiencm.id.vn`, khắc phục dứt điểm tình trạng tệp 0 byte trên máy chủ.
  - Các bài kiểm thử smoke test `tests/canvas-module-fallback-smoke.js` và `tests/canvas-soankhbd-smoke.js` đã được cập nhật tương ứng với phiên bản `v9` và kiểm tra hiển thị Stepper 1–2–3.

## Test đã chạy
- Kiểm tra trực quan và regex cấu trúc DOM:
  - `canvas_soankhbd.html`: Stepper hiển thị 1 -> 2 -> 3, aria-label 3 bước, đầy đủ critical DOM IDs.
  - `backupcode viettailieu/canvas_soankhbd.html`: Stepper hiển thị 1 -> 2 -> 3, aria-label 3 bước, đầy đủ critical DOM IDs.
- Chạy script kiểm thử `test_verify.py` xác minh toàn bộ điều kiện: PASS 100%.
- Kiểm tra cú pháp và tính toàn vẹn file tĩnh.

## Pass / Fail từng tiêu chí
- [PASS] Stepper hiển thị chính xác các số 1, 2, 3 tương ứng với Bước 1, Bước 2, Bước 3 (không còn 1 3 4).
- [PASS] Giữ nguyên toàn bộ `data-step` và DOM ID phục vụ logic điều hướng của `khbd-app.js`.
- [PASS] Cache-busting được nâng lên phiên bản `20260916-canvas-module-v9`.
- [PASS] Đồng bộ nhất quán giữa file chính `canvas_soankhbd.html` và bản sao lưu `backupcode viettailieu/canvas_soankhbd.html`.
- [PASS] File `js/khbd-curriculum.js` (173.6 KB) sẵn sàng triển khai tự động qua CI/CD GitHub Actions khi commit & push.

## Bug
Không phát hiện lỗi tồn đọng.
