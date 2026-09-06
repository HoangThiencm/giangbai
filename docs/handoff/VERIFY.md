# VERIFY

## Kết luận
FAIL

## Đối chiếu scope
- Sửa lỗi Tải/Lưu CSDL và cứu hộ nháp Canvas: Code đã sửa ở local nhưng **chưa deploy lên hosting live `hoangthiencm.id.vn`**. Hosting live vẫn chạy file cũ chưa có CORS, khiến Canvas gọi API bị chặn CORS và báo lỗi `Failed to fetch`.
- Yêu cầu mới 1 (Loại bỏ tiền tố `[NLS: ` và `[AI: ` cùng dấu `]` trong 2 cột Phụ lục 1): Chưa triển khai trong cả `xaydungphuluc.html` lẫn `backupcode viettailieu/canvas_xaydungphuluc.html`.
- Yêu cầu mới 2 (Tự động điền dấu `-` cho các dòng không có AI): Chưa cập nhật logic làm sạch hiển thị để đảm bảo luôn điền `-`.

## Test đã chạy
- `curl.exe -i -X OPTIONS "https://hoangthiencm.id.vn/api/user_phuluc_draft.php?action=list&user_account=hoangthiencm@gmail.com"` -> Trả về `401 Unauthorized`, **không có header CORS**. Chứng minh hosting `hoangthiencm.id.vn` chưa được deploy code mới.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-integration-smoke.js`: PASS.

## Pass / Fail từng tiêu chí
- [x] Tính năng cứu hộ nháp LocalStorage và File JSON (offline trong Canvas): PASS (dùng được ngay).
- [ ] Kết nối CSDL live từ Canvas: FAIL (Hosting chưa deploy code PHP mới mở CORS; request bị chặn CORS với lỗi `Failed to fetch`).
- [ ] Bỏ `[NLS: ` và `]` trong cột Biểu hiện năng lực số: FAIL (chưa triển khai code).
- [ ] Bỏ `[AI: ` và `]` trong cột Biểu hiện năng lực AI: FAIL (chưa triển khai code).
- [ ] Tự động điền 1 dấu `-` cho những dòng không có AI: FAIL (chưa triển khai code).

## Bug
1. **Lỗi `Failed to fetch` khi tải CSDL trong Canvas**:
   - Nguyên nhân: File `api/user_phuluc_draft.php` mới chỉ sửa ở local, chưa được push lên branch `main` nên GitHub Actions chưa FTP deploy lên hosting `hoangthiencm.id.vn`. Hosting live vẫn chạy code cũ, chặn preflight `OPTIONS` và không trả header `Access-Control-Allow-Origin: *`.
   - Khắc phục: Sau khi Coder hoàn thành toàn bộ yêu cầu và verify PASS, user duyệt push lên `main` để deploy lên hosting (hoặc tải trực tiếp file `api/user_phuluc_draft.php` lên hosting). Đồng thời trong `canvas_xaydungphuluc.html`, bỏ header tùy biến `X-User-Account` ở request GET (chỉ truyền qua query param `?user_account=...`) để tránh trigger preflight OPTIONS không cần thiết.
2. **Chưa triển khai chuẩn hóa mã NLS/AI và dấu `-`**:
   - Chưa bỏ `[NLS:` / `[AI:` trong `xaydungphuluc.html` và `canvas_xaydungphuluc.html`.
   - File liên quan: `xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`.
