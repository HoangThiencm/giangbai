# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Chuẩn hóa cột Biểu hiện năng lực số trong Phụ lục 1: Loại bỏ nhãn `[NLS: …]`, chỉ hiển thị mã và nội dung (VD: `1.1.TC2a - Sử dụng công cụ số để tìm kiếm thông tin theo yêu cầu`).
- [x] Chuẩn hóa cột Biểu hiện năng lực AI trong Phụ lục 1: Loại bỏ nhãn `[AI: …]`, chỉ hiển thị mã, nội dung và phạm vi tiết (VD: `8.A1.1 - Nhận diện vai trò dữ liệu đầu vào trong mô hình AI (Áp dụng: tiết 1, 2).`).
- [x] Hàng không chọn tiết AI trong Phụ lục 1 luôn tự động điền một dấu `-`.
- [x] Giữ nguyên nhãn phân biệt `[NLS:` và `[AI:` trong cột gộp Phụ lục 3 và cấu trúc PPCT gốc.
- [x] Báo cáo thẩm định sư phạm và xuất file Word (.docx) hoạt động chính xác với định dạng mã sạch, giữ đúng màu xanh NLS `#0070C0` và tím AI `#7030A0`.
- [x] Đồng bộ code 1-1 sang `backupcode viettailieu/canvas_xaydungphuluc.html`.
- [x] Backend `api/user_phuluc_draft.php` đã mở CORS, preflight OPTIONS 204 và fallback nhận diện `username`.
- [x] Bộ 4 nút cứu hộ nháp LocalStorage và File JSON trên Canvas hoạt động mượt mà độc lập.

## Test đã chạy
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-integration-smoke.js`: PASS.
- Kiểm tra cú pháp script inline bằng Node vm: PASS.

## Pass / Fail từng tiêu chí
- [x] Bỏ `[NLS: ` và `]` trong cột Biểu hiện năng lực số: PASS.
- [x] Bỏ `[AI: ` và `]` trong cột Biểu hiện năng lực AI: PASS.
- [x] Tự động điền dấu `-` cho các dòng không có AI: PASS.
- [x] Hiển thị và màu sắc trên giao diện HTML: PASS.
- [x] Xuất DOCX định dạng mã sạch: PASS.
- [x] Báo cáo thẩm định sư phạm đạt chuẩn: PASS.
- [x] Cứu hộ nháp Local/JSON trong Canvas: PASS.
- [x] Toàn bộ test tự động: PASS.

## Bug
Không có.
