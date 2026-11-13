# PLAN: Sửa lỗi Build GitHub Actions (Workflow Deploy website to hosting)

## 1. Hiện trạng & Nguyên nhân gốc rễ
- **Hiện trạng:**
  - Workflow GitHub Actions `Deploy website to hosting` (trong `.github/workflows/ftp-deploy.yml`) thất bại tại commit `40cbfa8` và merge `14eee39`.
  - Bước bị lỗi là Step 7: `Obfuscate first-party JavaScript` (`node tools/build-obfuscate.js --in-place`).
- **Nguyên nhân gốc rễ:**
  1. Trong commit `40cbfa8`, có 2 file script biên dịch KHBD Word offline được đặt trực tiếp ở thư mục gốc: `build_all_khbd_5512.js` và `compile_9_khbd_docx.js`.
  2. `tools/build-obfuscate.js` quét toàn bộ các file `.js` ở thư mục gốc và đẩy vào `javascript-obfuscator` vì 2 file này chưa nằm trong `SKIP_FILE_NAMES`.
  3. Tại dòng 198 của `build_all_khbd_5512.js`, bên trong template literal (`` `...` ``) có chứa 4 ký tự backtick thô chưa được escape:
     - `Gõ `"Toán 6 Kết nối tri thức"` trong ngoặc kép`
     - `dấu ngoặc kép `""` giúp tìm`
     Điều này làm template string bị đóng sớm và phát sinh lỗi cú pháp `SyntaxError: Unexpected token`, khiến `javascript-obfuscator` dừng tiến trình với mã lỗi 1.

---

## 2. Phạm vi can thiệp (Scope)
Chỉ chỉnh sửa đúng 3 file sau:
1. `build_all_khbd_5512.js`: Sửa cú pháp dòng 198 (escape hoặc thay thế dấu backtick).
2. `tools/build-obfuscate.js`: Bỏ qua các file script offline ở thư mục gốc khỏi tiến trình obfuscate.
3. `.github/workflows/ftp-deploy.yml`: Loại trừ các file script build offline khỏi danh sách upload FTP.

---

## 3. Chi tiết thực hiện

### 3.1. Sửa cú pháp trong `build_all_khbd_5512.js`
- **File:** `build_all_khbd_5512.js`
- **Vị trí:** Dòng 198.
- **Nội dung cũ:**
  ```javascript
  | **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu lên Tivi Thư viện thanh tìm kiếm Google và thanh tìm kiếm DlibK12. Đặt câu hỏi: "Nếu em muốn tìm quyển sách 'Toán 6 Kết nối tri thức', em sẽ gõ từ khóa nào để ra kết quả nhanh nhất?".<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh theo cặp bàn đưa ra các phương án từ khóa.<br>- **GV:** Thử nghiệm gõ trực tiếp các phương án của học sinh lên màn hình Tivi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nhận xét: Gõ `"Toán 6 Kết nối tri thức"` trong ngoặc kép sẽ ra đúng quyển sách cần tìm, không bị lẫn các trang quảng cáo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy tắc vàng trong tìm kiếm số và dẫn dắt vào bài thực hành tại Thư viện số. | **Khởi động:**<br>- Từ khóa tìm kiếm là cầu nối quyết định kết quả.<br>- Sử dụng dấu ngoặc kép `""` giúp tìm chính xác cụm từ.<br>- Tìm kiếm trên Thư viện số DlibK12 giúp tiếp cận học liệu đã được kiểm duyệt sư phạm. |
  ```
- **Nội dung mới:** Thay thế các dấu backtick bên trong chuỗi thành `\` hoặc dùng ngoặc kép chuẩn `""`:
  ```javascript
  | **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu lên Tivi Thư viện thanh tìm kiếm Google và thanh tìm kiếm DlibK12. Đặt câu hỏi: "Nếu em muốn tìm quyển sách 'Toán 6 Kết nối tri thức', em sẽ gõ từ khóa nào để ra kết quả nhanh nhất?".<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh theo cặp bàn đưa ra các phương án từ khóa.<br>- **GV:** Thử nghiệm gõ trực tiếp các phương án của học sinh lên màn hình Tivi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nhận xét: Gõ \"Toán 6 Kết nối tri thức\" trong ngoặc kép sẽ ra đúng quyển sách cần tìm, không bị lẫn các trang quảng cáo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy tắc vàng trong tìm kiếm số và dẫn dắt vào bài thực hành tại Thư viện số. | **Khởi động:**<br>- Từ khóa tìm kiếm là cầu nối quyết định kết quả.<br>- Sử dụng dấu ngoặc kép \"\" giúp tìm chính xác cụm từ.<br>- Tìm kiếm trên Thư viện số DlibK12 giúp tiếp cận học liệu đã được kiểm duyệt sư phạm. |
  ```

### 3.2. Cập nhật `tools/build-obfuscate.js`
- **File:** `tools/build-obfuscate.js`
- **Mục tiêu:** Thêm các script build KHBD vào danh sách bỏ qua `SKIP_FILE_NAMES`.
- **Cập nhật `SKIP_FILE_NAMES`:**
  ```javascript
  const SKIP_FILE_NAMES = new Set([
      'obfuscate.js',
      'build-obfuscate.js',
      'trochoi.compiled.js',
      'thoikhoabieu-worker.js',
      'game-quiz-importer.js',
      'build_all_khbd_5512.js',
      'compile_9_khbd_docx.js'
  ]);
  ```

### 3.3. Cập nhật `.github/workflows/ftp-deploy.yml`
- **File:** `.github/workflows/ftp-deploy.yml`
- **Mục tiêu:** Không upload các file script offline ở thư mục gốc lên hosting qua FTP.
- **Thêm vào danh sách `exclude`:**
  ```yaml
            build_all_khbd_5512.js
            compile_9_khbd_docx.js
            *.py
  ```

---

## 4. Kiểm thử & Xác minh (Verification)
1. **Kiểm tra cú pháp JS:**
   - Dùng Python / AST regex phân tích file `build_all_khbd_5512.js` để đảm bảo không còn backtick unescaped bên trong các template literal.
2. **Kiểm tra logic thu thập file của `build-obfuscate.js`:**
   - Chạy hàm kiểm tra danh sách file JS cần xử lý: đảm bảo `build_all_khbd_5512.js` và `compile_9_khbd_docx.js` không còn xuất hiện trong danh sách kết quả.
3. **Ghi log vào `docs/handoff/IMPLEMENT.md` và `docs/handoff/VERIFY.md`.**
