# IMPLEMENT: Sửa xuất Word và đồng bộ Gemini API Key cho KTTX

## Phạm vi đã triển khai

- Xóa toàn bộ script tag khỏi ba template Word: xuất đề/đáp án, ma trận và bản đặc tả. Các script tải thư viện hợp lệ của trang vẫn được giữ nguyên.
- Chuẩn hóa ba template với `meta charset='utf-8'`; loại bỏ thẻ `</div>` mồ côi trong template xuất đề.
- Thêm `syncUserKeysFromServer()` gọi `api/user_gemini_keys.php` cùng session hiện tại; key hợp lệ từ tài khoản được chuẩn hóa và cache vào `global_gemini_keys`.
- Khi không kết nối được hoặc chưa có key trên máy chủ, ứng dụng an toàn dùng cache localStorage hiện có. React đồng bộ khi mount và hiển thị rõ số Gemini API Key đã nạp cùng nguồn dữ liệu.
- Thêm `tests/kttx-smoke.js` kiểm tra cấu trúc Babel/template Word và luồng đồng bộ key.

## File đã sửa

- `kttx.html`
- `tests/kttx-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

## Kiểm thử đã chạy

- `node tests/kttx-smoke.js` — PASS
- `node tests/run-all-tests.js` — FAIL ở `tests/khbd-1click-chain-smoke.js`: assertion có sẵn về hướng dẫn Bước 4 sang Tab 2, 3, 4; không thuộc phạm vi KTTX.
- `git diff --check` — PASS

## Vấn đề còn lại

- Chưa thực hiện kiểm tra thủ công file `.doc` trong Microsoft Word.
- Chưa commit hoặc push theo yêu cầu.
