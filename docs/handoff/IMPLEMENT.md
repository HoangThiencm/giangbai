# IMPLEMENT

Trạng thái: ĐÃ LÀM — vá VERIFY FAIL: obfuscation tối đa + overlay khóa DevTools

## File đã đổi

- `tools/build-obfuscate.js`
- `js/security-guard.js`
- `tests/security-f12-smoke.js`
- `docs/handoff/IMPLEMENT.md`

Không đụng HTML trang, PHP API, `vendor/`, workflow FTP (giữ bước obfuscate đã có).

## Nội dung chính

Sửa đúng 5 hạng mục FAIL trong báo cáo VERIFY:

### 1. `tools/build-obfuscate.js` — cấu hình javascript-obfuscator tối đa

Áp dụng cho **mọi** file first-party (không còn nhánh riêng `security-guard`):

- `stringArrayThreshold: 1` (100% chuỗi vào string array)
- `transformObjectKeys: true`
- `debugProtection: true`
- `debugProtectionInterval: 1500`
- `selfDefending: true`

Giữ `renameGlobals: false` để không phá global (`TkbEngine`, v.v.). Fallback khi thiếu thư viện không đổi (Base64 chỉ `security-guard.js`).

### 2. `js/security-guard.js` — overlay khóa màn hình

Khi phát hiện DevTools (lệch kích thước cửa sổ, debugger trap, getter `stack`):

- `console.clear`
- Overlay full-viewport `#__gb_devtools_lock__` (“Phát hiện DevTools…”)
- Không xóa DOM bên dưới

Localhost / session debug vẫn bỏ qua toàn bộ bảo vệ. Ctrl+Alt+Shift+D vẫn mở khóa rồi reload. Overlay tự ẩn khi hết tín hiệu DevTools > 3s.

## Test đã chạy

```
node tests/security-f12-smoke.js
```

Kết quả: **pass** (5 hạng mục VERIFY: threshold 1, transformObjectKeys, debugProtection 1500, selfDefending toàn cục, overlay khóa màn hình; localhost không overlay; các tiêu chí F12 cũ vẫn giữ).

## Vấn đề còn lại

- `debugProtection` + `selfDefending` + `transformObjectKeys` trên mọi JS có thể làm chậm trang hoặc phá file dùng key động. Chỉ chạy lúc CI `--in-place`.
- HTML inline vẫn đọc được trên tab Sources — ngoài phạm vi.
- Overlay lệch cửa sổ có thể dương tính giả (thanh bookmark / dock lớn).
