# IMPLEMENT: Sửa lỗi Build GitHub Actions (Workflow Deploy website to hosting)

## Phạm vi đã thực hiện

1. **Sửa cú pháp trong `build_all_khbd_5512.js`:**
   - Tại dòng 198, thay thế các backtick thô chưa được escape bên trong template literal (`"Toán 6 Kết nối tri thức"` và `""`) thành chuỗi chuẩn có escape `\"` nhằm ngăn việc template string bị đóng sớm và loại bỏ hoàn toàn `SyntaxError: Unexpected token`.

2. **Cập nhật `tools/build-obfuscate.js`:**
   - Thêm `build_all_khbd_5512.js` và `compile_9_khbd_docx.js` vào tập hợp `SKIP_FILE_NAMES` để tiến trình obfuscate tự động bỏ qua hai script biên dịch KHBD offline ở thư mục gốc.

3. **Cập nhật `.github/workflows/ftp-deploy.yml`:**
   - Thêm `build_all_khbd_5512.js`, `compile_9_khbd_docx.js` và `*.py` vào danh sách `exclude` của action `SamKirkland/FTP-Deploy-Action@v4.4.0` để không tải các công cụ/script biên dịch offline lên hosting FTP.

## Kiểm thử & Xác minh

- Đã phân tích AST/cặp backtick trong `build_all_khbd_5512.js`: toàn bộ 7 khối template literal đều cân bằng, không còn backtick unescaped hay lỗi cú pháp.
- Đã chạy kiểm thử mô phỏng logic lọc tệp của `tools/build-obfuscate.js`: kết quả 33 tệp JS được thu thập, 2 tệp `build_all_khbd_5512.js` và `compile_9_khbd_docx.js` được bỏ qua hoàn toàn.
- Kiểm tra `git status` và `git diff`: chỉ đúng 3 tệp thuộc phạm vi quy định trong `docs/handoff/PLAN.md` được sửa đổi.
- Đã khôi phục tệp `docs/handoff/.lock`.

## Việc tiếp theo

Antigravity IDE, chat mới: `/verify`.
