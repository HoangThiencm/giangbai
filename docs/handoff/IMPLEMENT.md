# IMPLEMENT: Đồng bộ Gemini và Mistral API keys

## Đã triển khai

- Bổ sung danh sách `mistralKeys` cùng các hàm chuẩn hóa, loại trùng và lưu cục bộ theo từng tài khoản.
- Trang tải các khóa cục bộ trước, rồi gọi `GET api/user_gemini_keys.php` với phiên đăng nhập để nhận `keys` và `mistral_keys`. Lỗi mạng hoặc chưa đăng nhập giữ nguyên bản cục bộ.
- Mở hộp thoại khóa cũng đồng bộ lại từ CSDL. Hộp thoại có hai vùng nhập Gemini và Mistral; thao tác lưu gửi `POST` JSON gồm cả hai danh sách và cập nhật bộ nhớ đệm theo phản hồi hợp lệ.
- Badge hiển thị riêng số lượng từng nhà cung cấp, ví dụ `🔑 6 Gemini · 2 Mistral`; không hiện nội dung khóa trong badge hoặc log.
- Kiểm tra live vẫn chỉ kiểm tra Gemini. Khóa Mistral không bị ép theo định dạng Gemini.

## File thay đổi

- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/IMPLEMENT.md`

`docs/handoff/.lock` được giữ với nội dung `LOCK`. Không sửa `docs/handoff/PLAN.md` hoặc `docs/handoff/VERIFY.md`.

## Kiểm thử

- `node tests/xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.
- `git diff --check` — PASS.
