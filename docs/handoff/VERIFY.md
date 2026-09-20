# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `js/khbd-prompts.js`:
  + `ACTIVITY_TABLE_CONTRACT_COMPACT`: Đã bổ sung yêu cầu bắt buộc đủ 4 mục chuẩn CV 5512 (`#### a) Mục tiêu:`, `#### b) Nội dung:`, `#### c) Sản phẩm:`, `#### d) Tổ chức thực hiện:`) và bảng kịch bản 4 bước quy chuẩn (`+ Bước 1: Chuyển giao nhiệm vụ:` … `+ Bước 4: Kết luận, nhận định:`).
- `js/khbd-app.js`:
  + `repairActivityBlockFourParts`: Đã nhận diện đủ 4 cờ `hasA`, `hasB`, `hasC`, `hasD`.
  + Tự động khôi phục `#### a) Mục tiêu:` khi thiếu bằng câu chuẩn sư phạm tĩnh, giải quyết dứt điểm lỗi mất mục tiêu.
  + Khôi phục `b) Nội dung` và `c) Sản phẩm` bằng câu sư phạm tĩnh chuẩn mực khi thiếu.
  + Đã xóa bỏ hoàn toàn logic cắt thô `.slice(0, 400)` bóc tách `step1` và Cột 2, bảo vệ nguyên vẹn công thức LaTeX và kịch bản 4 bước của bảng.
- `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`:
  + Đồng bộ guard fallback docx `typeof window.docxGenerator !== "undefined" || typeof window.DocxGenerator !== "undefined"`.
- `tests/khbd-table-columns-smoke.js`:
  + Thêm test case Hoạt động B thiếu `a) Mục tiêu` tự bổ sung, giữ đủ Bước 1..4, không cắt xén LaTeX và không còn `.slice(0, 400)`.
- `tests/canvas-soankhbd-smoke.js`:
  + Cập nhật kiểm tra guard fallback docx đồng bộ cả 2 HTML.

## Test đã chạy
- `node tests/canvas-prompts-integrity-smoke.js` (PASS)
- `node tests/canvas-soankhbd-smoke.js` (PASS)
- `node tests/khbd-table-columns-smoke.js` (PASS)
- `node tests/khbd-pedagogy-rate-smoke.js` (PASS)
- `node tests/khbd-nls-ai-bold-italic-smoke.js` (PASS)
- `node tests/khbd-competencies-smoke.js` (PASS)
- `node tests/khbd-docx-math-smoke.js` (PASS)
- `node tests/khbd-pedagogy-script-smoke.js` (PASS)
- `node tests/khbd-review-practice-lesson-smoke.js` (PASS)

## Pass / Fail từng tiêu chí
- [PASS] Hoạt động B có đầy đủ 4 mục `#### a) Mục tiêu:`, `#### b) Nội dung:`, `#### c) Sản phẩm:`, `#### d) Tổ chức thực hiện:`.
- [PASS] Bảng kịch bản Cột 1 giữ nguyên vẹn 4 bước quy chuẩn (`+ Bước 1:`, `+ Bước 2:`, `+ Bước 3:`, `+ Bước 4:`).
- [PASS] Không còn hiện tượng cắt xén 400 ký tự làm gãy LaTeX (`$-5x^2y; $x^3 - \frac{1`) và đứt cụt chữ.
- [PASS] Không còn nhãn đúp `- - GV:` / `- - HS:`.
- [PASS] Chế độ Soạn rút gọn (COMPACT) bảo đảm khung cấu trúc chuẩn CV 5512.
- [PASS] Fallback CDN jsDelivr cho 3 thư viện (prompts, catalog, docx) hoạt động ổn định trên cả hai file HTML.

## Bug
Không có.
