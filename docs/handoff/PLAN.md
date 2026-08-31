# PLAN: Tối Ưu Tốc Độ CI/CD Deployment: Cố Định Seed Mã Hóa Cho JavaScript Obfuscator & Thêm Cache Cho GitHub Actions

## Hiện trạng
1. **Nguyên Nhân Gây Chậm Khi Deploy (>3 Phút)**:
   - Trong `tools/build-obfuscate.js`: Hàm `obfuscatorOptions()` chưa cấu hình `seed`.
   - Mỗi lần CI chạy trên GitHub Actions, `javascript-obfuscator` sinh ra các chuỗi định danh ngẫu nhiên cho toàn bộ 30 file JS, 19 file bundle và 48 file HTML.
   - Hậu quả: Dù người dùng chỉ sửa 1 dòng code, công cụ `FTP-Deploy-Action` vẫn nhận diện gần 100 file đều bị thay đổi $\rightarrow$ FTP phải kết nối và upload lại tuần tự 100 file (mất 2.5 - 3 phút).
   - Ngoài ra, bước `npm install javascript-obfuscator` chạy lại từ đầu mỗi lần do chưa có cache (mất thêm 20-30s).
2. **Kỳ Vọng**:
   - Cố định `seed: 12345` trong `tools/build-obfuscate.js`.
   - Khi đó, các file JS/HTML nào **không bị sửa đổi** sẽ luôn sinh ra cùng một mã hash $\rightarrow$ FTP-Deploy-Action chỉ upload đúng 1–2 file thực tế bị thay đổi.
   - Thêm cache cho npm trong `.github/workflows/ftp-deploy.yml`.
   - Tốc độ deploy giảm từ >3 phút xuống chỉ còn **15–25 giây**.

## Phạm vi
1. **File `tools/build-obfuscate.js`**:
   - Thêm `seed: 12345` vào hàm `obfuscatorOptions(rel)`.
2. **File `.github/workflows/ftp-deploy.yml`**:
   - Thêm bước cache `~/.npm` qua `actions/setup-node@v4` với `cache: 'npm'`.
   - Đảm bảo danh sách `exclude` loại trừ triệt để các file nặng: `GIAO AN/**`, `taovideo/assets/vtts/models/**`, `**/*.pdf`, `**/*.onnx`, `**/*.wasm`.

## Ngoài phạm vi
- Không can thiệp mã nguồn ứng dụng web.

## File dự kiến tác động
- `tools/build-obfuscate.js` [THÊM SEED: 12345 VÀO OBFUSCATOR OPTIONS]
- `.github/workflows/ftp-deploy.yml` [BẬT CACHE VÀ LOẠI TRỪ FILE NẶNG]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Cập Nhật `tools/build-obfuscate.js`**:
   - Bổ sung `seed: 12345` vào đối tượng cấu hình trả về từ `obfuscatorOptions()`.
2. **Bước 2: Cập Nhật `.github/workflows/ftp-deploy.yml`**:
   - Đảm bảo định dạng spaces chuẩn (không có tab) và danh sách exclude đầy đủ.
3. **Bước 3: Kiểm Thử**:
   - Chạy `node tools/build-obfuscate.js --dry-run` xác nhận không có lỗi cú pháp.
   - Chạy 2 lần liên tiếp để xác nhận output của các file không sửa là giống hệt nhau (cùng hash).

## Tiêu chí nghiệm thu
1. Cố định `seed: 12345` thành công, hai lần chạy obfuscate trên cùng một mã nguồn sinh ra output trùng khớp 100%.
2. File workflow YAML hợp lệ cú pháp, không có tab, loại trừ đầy đủ các tệp nặng >250MB.
3. Thời gian deploy thực tế giảm rõ rệt xuống dưới 30 giây.
