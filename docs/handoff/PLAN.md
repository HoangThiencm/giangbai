# PLAN

## Hiện trạng
1. **Vấn đề Dán đề bài trong Vẽ hình học (`VeHinhTab` & `DualInput`):**
   - Hiện tại hàm `paste_clipboard()` trong `DualInput` chỉ gọi `QApplication.clipboard().text()`.
   - Khi giáo viên chụp ảnh màn hình đề bài toán hình học (dùng Snipping Tool hoặc phím Windows + Shift + S), nội dung trong Clipboard là dạng ảnh (`QImage`/`QPixmap`), không có text thuần. Do đó khi bấm "Dán từ Clipboard" hoặc `Ctrl+V`, app không nhận được gì và không hiển thị gì cả.
   - Khung xem trước trong `VeHinhTab` hiện chỉ hiển thị ảnh sau khi vẽ xong, chưa hiển thị ảnh đề bài vừa dán hoặc vừa chọn.
2. **Vấn đề Duyệt cả thư mục hồ sơ (`DuyetTab` & các phân hệ xử lý hàng loạt):**
   - Trong nghiệp vụ gốc của Trợ lý Hoàng Thiên (`3_DUYET_GIAO_AN`, `4_DUYET_DE`, `1_SOAN_KHBD_HANG_LOAT`), giáo viên thường đưa cả một thư mục chứa nhiều file giáo án/đề thi của cả tổ chuyên môn vào để duyệt toàn diện một lần.
   - Hiện tại `DualInput` chỉ có nút `QFileDialog.getOpenFileName` chọn đúng 1 file đơn lẻ, không có nút chọn cả thư mục và không hỗ trợ chọn nhiều tệp cùng lúc.
   - Hàm `_inputs` trong `core/prompt_builder.py` chưa có cơ chế tự động quét đệ quy các tệp con khi người dùng chọn một thư mục.

## Phạm vi
- **Nâng cấp cơ chế Dán thông minh (Smart Paste cho cả Văn bản và Ảnh chụp màn hình):**
  - Trong `DualInput` (`app_trolythien/ui/kit.py`):
    + Hỗ trợ kiểm tra mime data của Clipboard:
      * Nếu Clipboard chứa **Văn bản**: Chèn trực tiếp văn bản vào ô nhập `QTextEdit`.
      * Nếu Clipboard chứa **Ảnh chụp màn hình**: Tự động lưu thành file ảnh PNG tạm thời trong `app_trolythien/.runtime/clipboard_images/`, gán làm tệp đầu vào, hiển thị tên file trên nhãn đính kèm và phát tín hiệu `image_attached(str)`.
    + Override sự kiện dán `insertFromMimeData` của `QTextEdit` để khi người dùng ấn phím tắt `Ctrl+V` vào ô soạn thảo, nếu trong clipboard là ảnh thì cũng tự động nhận diện và lưu ảnh đính kèm.
  - Trong `VeHinhTab` (`app_trolythien/ui/tab_vehinh.py`):
    + Khi người dùng dán ảnh từ clipboard hoặc chọn file ảnh đề bài, khung xem trước sẽ lập tức hiển thị ngay bức ảnh đề bài đó để giáo viên quan sát trực quan.
    + Khi AI vẽ xong, khung xem trước tự động chuyển sang hiển thị hình vẽ thành phẩm.
- **Bổ sung chức năng Chọn cả thư mục & Chọn nhiều tệp (Folder & Multi-file Batch Input):**
  - Trong `DualInput` (`ui/kit.py`):
    + Thêm nút bấm **"Chọn cả thư mục…"** (`QFileDialog.getExistingDirectory`).
    + Nâng cấp nút **"Chọn tệp…"** cho phép chọn nhiều file cùng lúc (`QFileDialog.getOpenFileNames`).
    + Hiển thị nhãn thông tin rõ ràng: ví dụ *"Đã chọn thư mục: Giaocan_Thang9 (8 tệp)"* hoặc *"Đã chọn 5 tệp"*.
  - Trong `core/prompt_builder.py` (`_inputs`):
    + Kiểm tra nếu phần tử trong `files` là một thư mục (`path.is_dir()`): Quét toàn bộ các tệp tài liệu con bên trong thư mục đó (`*.docx`, `*.pdf`, `*.md`, `*.txt`) và đưa danh sách đường dẫn đầy đủ vào prompt cho AI đọc và duyệt toàn bộ.
- **Cập nhật bản đóng gói `.exe`:**
  - Chạy lại `app_trolythien/build_exe.bat` để cập nhật bản phân phối trong `app_trolythien/dist/TroLyHoangThien/`.

## Ngoài phạm vi
- Không thay đổi logic chạy ngầm của `agy.exe`.
- Không ảnh hưởng đến các phân hệ khác ngoài việc được hưởng lợi từ tính năng chọn thư mục và dán ảnh thông minh.

## File dự kiến tác động
1. `app_trolythien/ui/kit.py`:
   - Nâng cấp `DualInput` hỗ trợ dán ảnh clipboard, chọn cả thư mục (`getExistingDirectory`) và chọn nhiều tệp (`getOpenFileNames`).
2. `app_trolythien/ui/tab_vehinh.py`:
   - Kết nối tín hiệu hiển thị ảnh đề bài ngay khi dán/chọn ảnh vào khung xem trước.
3. `app_trolythien/core/prompt_builder.py`:
   - Cập nhật hàm `_inputs` để duyệt toàn bộ tệp khi đầu vào là một thư mục.
4. `app_trolythien/dist/TroLyHoangThien/`:
   - Cập nhật bản đóng gói hoàn chỉnh.

## Các bước thực hiện
1. **Cập nhật `app_trolythien/ui/kit.py`:**
   - Trong `DualInput`:
     - Thêm phương thức `paste_clipboard()`:
       ```python
       mime = QApplication.clipboard().mimeData()
       if mime.hasImage():
           image = QApplication.clipboard().image()
           # Lưu vào .runtime/clipboard_images/clip_<timestamp>.png
           # Gán self.attached = [path] và phát tín hiệu
       elif mime.hasText():
           self.editor.insertPlainText(mime.text())
       ```
     - Thêm nút `browse_folder = QPushButton("Chọn cả thư mục…")` kết nối tới hộp thoại `QFileDialog.getExistingDirectory`.
     - Sửa nút `browse` dùng `QFileDialog.getOpenFileNames` để chọn nhiều tệp.
     - Quản lý danh sách `self.attached_items: list[str]` hỗ trợ cả danh sách file lẫn thư mục.
2. **Cập nhật `app_trolythien/ui/tab_vehinh.py`:**
   - Bắt sự kiện khi dán/chọn ảnh đề bài: hiển thị ngay ảnh đề bài lên `self.preview`.
   - Giữ nguyên hiển thị ảnh kết quả sau khi AI hoàn thành.
3. **Cập nhật `app_trolythien/core/prompt_builder.py`:**
   - Trong `_inputs(pasted, files)`:
     - Duyệt từng mục trong `files`. Nếu là thư mục (`is_dir()`), quét danh sách tệp tài liệu bên trong và liệt kê chi tiết từng tệp cho AI xử lý.
4. **Kiểm thử tính năng:**
   - Kiểm tra dán text thuần: Text hiển thị trong ô soạn thảo.
   - Kiểm tra dán ảnh chụp màn hình: Ảnh được lưu và hiển thị preview.
   - Kiểm tra chọn thư mục trong tab Duyệt giáo án: Nhận diện đủ danh sách file trong thư mục.
5. **Đóng gói lại:**
   - Chạy `app_trolythien/build_exe.bat` để cập nhật `TroLyHoangThien.exe`.

## Rủi ro
1. **Ảnh clipboard có dung lượng lớn:**
   - *Biện pháp:* Tự động nén lưu định dạng PNG tiêu chuẩn, hiển thị thu nhỏ với tỷ lệ phù hợp (`KeepAspectRatio`).
2. **Thư mục chọn chứa quá nhiều file rác:**
   - *Biện pháp:* Bộ lọc chỉ lấy các đuôi tệp văn bản/tài liệu hợp lệ (`.docx`, `.pdf`, `.md`, `.txt`, `.png`, `.jpg`).

## Cách kiểm thử
1. Mở `app_trolythien/main.py`.
2. Vào Tab **Vẽ hình học**:
   - Dùng Win+Shift+S chụp một góc màn hình, quay lại app bấm "Dán từ Clipboard" (hoặc Ctrl+V) -> ảnh đề bài xuất hiện ngay ở khung xem trước và có thông báo đính kèm ảnh.
   - Thử dán một đoạn chữ đề bài -> chữ xuất hiện rõ trong ô soạn thảo.
3. Vào Tab **Duyệt giáo án**:
   - Bấm nút "Chọn cả thư mục…" và chọn một thư mục chứa nhiều file giáo án -> nhãn hiển thị số lượng file trong thư mục, prompt sinh ra liệt kê đầy đủ danh sách file đó.
4. Chạy `build_exe.bat` và kiểm tra file `.exe` trong `dist/TroLyHoangThien/`.

## Tiêu chí nghiệm thu
- Dán được cả chữ và ảnh chụp màn hình từ Clipboard (ảnh hiện ngay ở khung xem trước).
- Có nút chọn cả thư mục cho các phân hệ duyệt hồ sơ/hàng loạt, AI nhận diện và quét toàn bộ tệp trong thư mục.
- Bản `.exe` trong `dist/TroLyHoangThien/` được cập nhật và chạy mượt mà.
