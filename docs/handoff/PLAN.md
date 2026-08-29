# PLAN: Mã hóa triệt để toàn bộ nội dung file HTML (HTML Encryption Loader)

Trạng thái: KẾ HOẠCH ĐÃ DUYỆT

## Hiện trạng

- File `soankhbd.html` (và các file `.html` khác) đang deploy ở dạng plain text HTML.
- Khi người dùng vào tab Sources hoặc xem mã nguồn trang (`Ctrl + U`), họ vẫn đọc được toàn bộ HTML, form ID, quy trình thiết kế bài dạy và các ghi chú comment tiếng Việt.

## Phạm vi

1. **Bổ sung tính năng Mã hóa HTML vào `tools/build-obfuscate.js`**:
   - Khi chạy `--in-place` (trên CI GitHub Actions):
     1. Quét các file HTML (`soankhbd.html`, `lotrinhtoan*.html`, `thitructuyen.html`, `index.html`,...).
     2. Gộp và làm rối các script JS thành bundle như đã thiết kế.
     3. Xóa sạch 100% HTML comments (`<!-- ... -->`).
     4. Mã hóa toàn bộ nội dung HTML của trang thành chuỗi Base64 đã xáo trộn (XOR).
     5. Thay thế file HTML bằng Dynamic HTML Decryption Loader (kèm `js/security-guard.js` ở đầu trang).
2. **Cập nhật `tests/security-f12-smoke.js`**:
   - Kiểm tra file HTML sau build không còn chứa text `<!-- BƯỚC 1` hay các thẻ `<button class="nav-tab-btn">` dạng plain text.
   - Kiểm tra mã giải mã trong sandbox `document.write` ra đúng cấu trúc DOM.

## Ngoài phạm vi

- Không can thiệp API backend PHP (`api/`).
- Giữ nguyên mã nguồn HTML gốc trên máy tính cá nhân (local) để lập trình viên dễ dàng chỉnh sửa giao diện.

## File dự kiến tác động

- `tools/build-obfuscate.js`
- `tests/security-f12-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/PLAN.md`

## Các bước thực hiện

1. **Bước 1: Nâng cấp `tools/build-obfuscate.js`**:
   - Xây dựng hàm `encryptHtmlContent(html)`:
     - Làm sạch comment, minify markup.
     - Mã hóa chuỗi HTML thành Base64 obfuscated payload.
     - Tạo template HTML Loader chứa `security-guard.js` và IIFE tự giải mã `document.write`.
   - Áp dụng cho toàn bộ file HTML khi deploy `--in-place`.
2. **Bước 2: Chạy kiểm thử**:
   - Chạy `node tests/security-f12-smoke.js` kiểm tra tính chính xác và an toàn.
3. **Bước 3: Ghi nhận kết quả vào `docs/handoff/IMPLEMENT.md`**.

## Rủi ro

- Một số trình duyệt có thể cảnh báo nếu dùng `document.write` không đúng thời điểm.
  - *Giải pháp*: Loader thực thi ngay lập tức khi trang đang tải (`document.open() / document.write() / document.close()`) đồng bộ.
- Payload Base64 XOR không phải bảo mật mật mã học — chỉ che view-source / Sources.

## Cách kiểm thử

```
node tests/security-f12-smoke.js
node tools/build-obfuscate.js --dry-run
```

- Mở `soankhbd.html` trên hosting:
  - Tab Sources và `view-source:` **không còn** comment tiếng Việt / `nav-tab-btn` / `tabVision` dạng plain text.
  - Giao diện web hiển thị đầy đủ sau khi loader giải mã.

## Tiêu chí nghiệm thu

1. File `soankhbd.html` và các file HTML không còn chứa markup / comment plain text khi mở tab Sources.
2. Giao diện trang web tự động giải mã và hoạt động không lỗi.
3. `node tests/security-f12-smoke.js` pass.
