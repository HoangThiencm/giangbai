# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Thêm 2 chế độ phân bổ linh hoạt: "Theo số tiết dạy bài mới" và "Theo số bài dạy bài mới" cho cả NLS và AI.
- [x] Nhãn hiển thị ghi rõ ràng: "... tiết dạy bài mới" và "... bài dạy bài mới".
- [x] Có ô nhập số lượng trực tiếp (`#nlsCountInput`, `#aiCountInput`) đồng bộ 2 chiều với thanh kéo `%`.
- [x] Gỡ bỏ hoàn toàn giới hạn trần cứng 12 tiết ở AI; người dùng có thể tự do chọn 20 tiết, 35 tiết hoặc kéo 100% (toàn bộ 95 tiết dạy bài mới).
- [x] Không phát sinh lỗi tràn ngăn xếp đệ quy (`RangeError`) hay biến không xác định (`ReferenceError`).
- [x] Đồng bộ đầy đủ sang cả `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html` (SHA-256 trùng khớp 100%).
- [x] Toàn bộ 3 bộ kiểm thử tự động của dự án đạt PASS 100%.

## Test đã chạy
1. `node tests/xaydungphuluc-smoke.js` — **PASS**
2. `node tests/canvas-xaydungphuluc-smoke.js` — **PASS**
3. `node tests/khbd-nls-rate-smoke.js` — **PASS**
4. So sánh SHA-256 hai bản Canvas — **PASS** (`BED1D0B532D2F0D6B85C5847BCA94A8C1468BDEC6F0CDE029A788231DD42E1EE`)
5. Mô phỏng thực tế chuyên sâu trên cả 3 file (`xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`):
   - **NLS theo tiết**: Nhập `20` -> Nhãn: `22% (21/95 tiết dạy bài mới · 14/47 bài)` — **PASS**
   - **NLS theo bài**: Nhập `10` -> Nhãn: `21% (10/47 bài dạy bài mới · 16/95 tiết)` — **PASS**
   - **AI theo tiết (vượt trần cũ 12 tiết)**: Nhập `20` -> Nhãn: `21% (20/95 tiết dạy bài mới · 14/47 bài)` — **PASS**
   - **AI theo tiết**: Nhập `35` -> Nhãn: `37% (35/95 tiết dạy bài mới · 22/47 bài)` — **PASS**
   - **AI kéo 100%**: Chọn toàn bộ 95/95 tiết dạy bài mới, `aiRate.max = 100` — **PASS**
   - **AI theo bài**: Nhập `12` -> Nhãn: `26% (12/47 bài dạy bài mới · 18/95 tiết)` — **PASS**

## Pass / Fail từng tiêu chí
1. Tính năng phân bổ linh hoạt theo số tiết và theo số bài: **PASS**
2. Nhãn hiển thị ghi rõ "tiết dạy bài mới" và "bài dạy bài mới": **PASS**
3. Đồng bộ 2 chiều giữa ô nhập số lượng và thanh trượt: **PASS**
4. Gỡ bỏ trần cứng 12 tiết AI, mở rộng 0–100%: **PASS**
5. Khắc phục lỗi thiếu hàm trong test `khbd-nls-rate-smoke.js`: **PASS**
6. Khắc phục lỗi tương thích và đồng bộ 1:1 trong test `canvas-xaydungphuluc-smoke.js`: **PASS**
7. Không có lỗi runtime hay console error: **PASS**

## Bug
Không còn bug tồn đọng.