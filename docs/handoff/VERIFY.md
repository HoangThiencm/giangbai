# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Mục 1: Khắc phục lỗi `getSystemRole is not defined` & deploy `js/khbd-prompts.js`**:
  - `js/khbd-prompts.js`: Đã thêm chú thích deploy `// Deploy version: 20260916-textbook-exact-v15` tạo git diff sẵn sàng cho GitHub Actions FTP deploy tải lại file đầy đủ 138.942 bytes lên hosting.
  - `js/khbd-app.js`: Đã bọc kiểm tra an toàn `typeof getSystemRole === "function"` tại dòng 6846 trong hàm `analyzeCanvasTextbookSafely`, loại bỏ hoàn toàn nguy cơ văng `ReferenceError` khi gọi OCR SGK trên Canvas.
  - `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`: Đã nâng query version của `khbd-prompts.js` lên `?v=20260916-textbook-exact-v15` và đặt fallback stub `window.getSystemRole = function () { return ""; };` trước khi nạp `khbd-app.js`.
- **Mục 2: Điều chỉnh số bước Stepper từ 1 3 4 thành 1 2 3**:
  - Cả hai file Canvas (`canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`) đều hiển thị chuỗi số bước `1` -> `2` -> `3`.
  - Giữ nguyên toàn bộ thuộc tính logic `data-step="3"`, `data-step="4"` và các ID DOM phục vụ tương thích 100% với luồng điều hướng của `khbd-app.js`.
  - Thuộc tính `aria-label` cập nhật thành `"Quy trình 3 bước soạn KHBD"`.
- **Mục 3: Khắc phục lỗi nạp danh mục chương trình (Curriculum Module) từ host**:
  - `js/khbd-curriculum.js` (dòng 9) đã cập nhật lên `const KHBD_CURRICULUM_DEPLOY_VERSION = "canvas-module-v9";`. Tệp có git diff để workflow GitHub Actions FTP Deploy tự động tải lại tệp đầy đủ 173.676 bytes lên máy chủ `hoangthiencm.id.vn`.
  - Cache-busting các module Canvas trong HTML đồng bộ phiên bản `20260916-canvas-module-v9`.

## Test đã chạy
- `python C:\Users\HoangThien\.gemini\antigravity\brain\7ddd6240-4311-4b35-b755-f9a3e9f49765\scratch\test_verify.py`: PASS (Kiểm tra Stepper 1-2-3, aria-label, critical DOM IDs).
- `python C:\Users\HoangThien\.gemini\antigravity\brain\7ddd6240-4311-4b35-b755-f9a3e9f49765\scratch\verify_all.py`: ALL CHECKS PASSED (Kiểm tra đầy đủ điều kiện code an toàn, query cache-buster v15/v9, và version diff cho cả prompts lẫn curriculum).
- `git diff --check`: Không có lỗi cú pháp hoặc khoảng trắng trong các file mã nguồn.

## Pass / Fail từng tiêu chí
- [PASS] Stepper hiển thị chính xác chuỗi số 1, 2, 3 tương ứng với Bước 1, Bước 2, Bước 3 (không còn 1 3 4).
- [PASS] Giữ nguyên toàn bộ `data-step` và DOM ID phục vụ logic điều hướng của `khbd-app.js`.
- [PASS] `analyzeCanvasTextbookSafely` có kiểm tra phòng vệ an toàn `typeof getSystemRole === "function"`.
- [PASS] `canvas_soankhbd.html` và bản backup nâng cache-busting `khbd-prompts.js` lên v15 và có fallback stub.
- [PASS] `js/khbd-prompts.js` có git diff sẵn sàng cho FTP deploy tự động tải file 138KB lên host.
- [PASS] `js/khbd-curriculum.js` có git diff với phiên bản `canvas-module-v9` sẵn sàng cho FTP deploy tự động tải file 173KB lên host.

## Bug
Không phát hiện lỗi tồn đọng.
