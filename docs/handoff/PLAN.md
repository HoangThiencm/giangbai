# PLAN

Trạng thái: KẾ HOẠCH ĐÃ DUYỆT

## Hiện trạng

- `js/security-guard.js` đã được nhúng đầu trang trên nhiều HTML. Chặn chuột phải (trừ ô soạn), F12, Ctrl+U, Ctrl+Shift+I/J/C/K, Ctrl+S ngoài input; có debugger trap, đo lệch kích thước cửa sổ, tắt một phần `console`.
- Comment ghi bỏ qua bảo vệ khi localhost **hoặc** debug, nhưng code đang dùng `isLocalhost && isDebugUnlocked` nên localhost vẫn bị chặn F12.
- Khóa mở debug `htcm@admin` / `hoangthien` nằm plaintext trong file, đọc được khi View Source / F12.
- `tools/obfuscate.js` ghi đè file gốc + tạo `.bak` — không dùng được cho CI (làm bẩn git).
- `.github/workflows/ftp-deploy.yml` upload source JS nguyên văn lên hosting.

## Phạm vi

1. Nâng cấp `js/security-guard.js` (cùng kiến trúc IIFE, không thêm dependency).
2. Tạo `tools/build-obfuscate.js`: làm rối JS first-party lúc build/deploy, không ghi đè source trên máy dev trừ `--in-place`.
3. Cấu hình GitHub Actions FTP: cài obfuscator, chạy `--in-place` trước khi upload.
4. Smoke test + ghi `docs/handoff/IMPLEMENT.md`.

## Ngoài phạm vi

- Không chặn copy/select (học sinh cần chọn bài).
- Không obfuscate HTML inline, `vendor/`, tests, PHP API.
- Không thêm security-guard vào từng trang HTML còn thiếu.
- Không đổi access-control, không sửa `.htaccess`.
- Không coi F12-block là bảo mật tuyệt đối — chỉ rào chắn + làm rối mã client.

## File dự kiến tác động

- `js/security-guard.js`
- `tools/build-obfuscate.js` (tạo mới)
- `.github/workflows/ftp-deploy.yml`
- `.gitignore` (`node_modules/`, `.deploy-obfuscated/`, `package-lock.json`)
- `tests/security-f12-smoke.js` (tạo mới)
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/PLAN.md`

## Các bước thực hiện

1. Sửa skip thành `localhost || debug`; fingerprint khóa fallback; chặn phím theo `key`/`code` lẫn `keyCode`; thêm probe console; không xóa DOM khi nghi DevTools.
2. Tool build: mặc định ghi `.deploy-obfuscated/`; `--in-place` cho CI; skip vendor/tests/tools; ưu tiên `javascript-obfuscator`, fallback Base64 chỉ với `security-guard.js`.
3. Workflow: setup Node 20 → `npm install --no-save javascript-obfuscator@4.1.1` → `node tools/build-obfuscate.js --in-place` → FTP (vẫn loại `tools/**`, `tests/**`, `package-lock.json`).
4. Smoke test tĩnh + vm (F12, localhost, unlock) + dry-run tool + workflow.

## Rủi ro

- Obfuscator có thể làm hỏng JS dùng `let`/`const` global nếu fallback bọc `Function`. Mitigation: fallback chỉ wrap `security-guard.js`; file khác chỉ gọn comment khi thiếu thư viện. CI bắt buộc cài `javascript-obfuscator` (`renameGlobals: false`).
- Đo lệch kích thước cửa sổ dương tính giả (bookmark bar, dock). Mitigation: chỉ `console.clear`, không xóa trang.
- F12 vẫn xem được HTML inline. Nằm ngoài phạm vi.

## Cách kiểm thử

```
node tests/security-f12-smoke.js
```

Tuỳ chọn:

```
node tools/build-obfuscate.js --dry-run
```

## Tiêu chí nghiệm thu

1. Localhost (hoặc session debug) không gắn listener chặn F12.
2. Production chặn F12, Ctrl+U, Ctrl+Shift+I; chuột phải trên DIV bị chặn, trên INPUT không.
3. `security-guard.js` không còn plaintext `htcm@admin` / `hoangthien`; Ctrl+Alt+Shift+D + khóa hashed vẫn mở debug.
4. `tools/build-obfuscate.js --dry-run` liệt kê `js/security-guard.js`, không liệt kê `vendor/*.min.js` hay `tests/`.
5. `--in-place --fallback-only` trên thư mục tạm làm rối `security-guard.js`, không sửa file trong git.
6. Workflow deploy chạy obfuscate trước FTP.
7. `node tests/security-f12-smoke.js` pass.

<!-- User chốt bằng cách đổi dòng trạng thái thành: KẾ HOẠCH ĐÃ DUYỆT -->
