# IMPLEMENT

Trạng thái: ĐÃ LÀM — chống lộ mã nguồn F12 (security-guard + build-obfuscate + GitHub Actions)

## File đã đổi

- `js/security-guard.js`
- `tools/build-obfuscate.js` (mới)
- `.github/workflows/ftp-deploy.yml`
- `.gitignore`
- `tests/security-f12-smoke.js` (mới)
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

Không đụng HTML trang, PHP API, `vendor/`, `tools/obfuscate.js` (giữ nguyên, không dùng cho CI).

## Nội dung chính

### 1. `js/security-guard.js`

- Bỏ qua bảo vệ khi **localhost hoặc** session debug — khớp comment cũ (trước đây code dùng AND nên F12 vẫn chặn trên máy dev).
- Thêm `[::1]`; `sessionStorage`/`localStorage` bọc try/catch.
- Khóa fallback không còn plaintext; so khớp fingerprint FNV-1a (`7731ce4a`, `c3e3eb18`). `localStorage.admin_key` / `ADMIN_KEY` vẫn dùng được nếu giáo viên tự đặt.
- Chặn phím theo `key`/`code` lẫn `keyCode` (F12, Ctrl+Shift+I/J/C/K/E, Ctrl+U, Ctrl+S ngoài ô soạn).
- Giữ chuột phải trên INPUT/TEXTAREA/contenteditable/math-field.
- Probe DevTools (debugger timing, lệch cửa sổ, getter `stack`) chỉ `console.clear` — không xóa DOM.
- Shortcut admin không đổi: Ctrl+Alt+Shift+D.

### 2. `tools/build-obfuscate.js`

Làm rối JS first-party lúc deploy, không ghi đè git trên máy dev:

```
node tools/build-obfuscate.js              # ghi .deploy-obfuscated/
node tools/build-obfuscate.js --in-place   # chỉ CI
node tools/build-obfuscate.js --dry-run
```

Bỏ qua `vendor/`, `tests/`, `tools/`, `api/`, `*.min.js`, worker TKB, `trochoi.compiled.js`.

- Có `javascript-obfuscator`: compact + string array, `renameGlobals: false`; `security-guard.js` thêm `selfDefending`.
- Không có thư viện: chỉ bọc Base64 IIFE cho `security-guard.js`; file khác chỉ xóa comment (tránh phá `let`/`const` global).

### 3. GitHub Actions

Trước FTP:

1. Node 20
2. `npm install --no-save javascript-obfuscator@4.1.1`
3. `node tools/build-obfuscate.js --in-place`

Vẫn không upload `tools/**`, `tests/**`, `docs/**`, `api/config.php`. Thêm loại `package.json`, `package-lock.json`, `.deploy-obfuscated/**`.

Source trên GitHub giữ bản đọc được; bản trên hosting là bản đã làm rối.

## Test đã chạy

```
node tests/security-f12-smoke.js
node tools/build-obfuscate.js --dry-run
```

Kết quả smoke: **pass** (cú pháp, localhost skip, F12/Ctrl+U/Ctrl+Shift+I, chuột phải INPUT vs DIV, unlock hashed, workflow, dry-run, fallback wrap trên thư mục tạm).

`--dry-run` liệt kê **30** file JS first-party (gồm `js/security-guard.js`, `access-control.js`, `js/khbd-*.js`); không gồm `vendor/`, `tests/`, `tools/`.

## Vấn đề còn lại

- F12 vẫn xem HTML/CSS và script inline trong file `.html` — không thuộc phạm vi (không obfuscate HTML).
- Rào chắn client không thay thế quyền truy cập server (`access-control.js` / PHP session).
- `--in-place` trên máy local làm bẩn working tree; chỉ chạy trong CI hoặc thư mục tạm.
