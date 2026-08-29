# IMPLEMENT

Trạng thái: ĐÃ LÀM — mã hóa HTML lúc deploy (Encrypted HTML Loader)

## File đã đổi

- `tools/build-obfuscate.js`
- `tests/security-f12-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

Không đụng PHP API. HTML trên git giữ nguyên — chỉ mã hóa khi `--in-place` / CI.

## Nội dung chính

Sau bước bundle JS, `tools/build-obfuscate.js`:

1. Xóa comment `<!-- ... -->`, gọn `>\s+<`.
2. XOR + Base64 toàn bộ markup (`encryptHtmlContent`).
3. Ghi vỏ `buildEncryptedHtmlShell`: `js/security-guard.js` + IIFE `document.open/write/close`.
4. `--dry-run` in `ENCRYPT {file.html}`.

View-source chỉ thấy loader + payload; trình duyệt tự giải mã ra DOM đầy đủ (kèm bundle JS).

## Test đã chạy

```
node tests/security-f12-smoke.js
```

Kết quả: **pass** (vỏ mã hóa không còn `<!-- BƯỚC 1` / `nav-tab-btn` / `tabVision`; sandbox `document.write` ra đúng DOM đã giải mã; bundle + CDN/vendor vẫn đúng thứ tự trong payload).

## Vấn đề còn lại

- XOR+Base64 không chống người cố tình giải payload; chỉ che Sources / Ctrl+U.
- `document.write` thay cả document — đúng thiết kế loader; một số extension có thể cảnh báo.
- File JS gốc vẫn nằm trên hosting nếu FTP upload cả cây.
