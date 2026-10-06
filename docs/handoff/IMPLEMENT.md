# IMPLEMENT

Dán clipboard trong `app_trolythien` nhận cả chữ và ảnh chụp màn hình. Chọn đầu vào được nhiều tệp hoặc cả thư mục. Prompt liệt kê tệp tài liệu trong thư mục đó. Bản `dist\TroLyHoangThien\TroLyHoangThien.exe` đã được đóng gói lại.

## Đã làm

- `ui/kit.py`: `paste_clipboard()` đọc mime. Có chữ thì chèn vào `QTextEdit`. Có ảnh thì lưu PNG vào `app_trolythien/.runtime/clipboard_images/clip_<thời điểm>.png`, gán `attached_items`, và phát `image_attached`. `PasteAwareEdit.insertFromMimeData` làm cùng việc khi bấm Ctrl+V.
- Nút **Chọn tệp…** dùng `QFileDialog.getOpenFileNames`. Nút **Chọn cả thư mục…** dùng `getExistingDirectory`. Nhãn: `Đã chọn thư mục: <tên> (N tệp)` hoặc `Đã chọn N tệp`.
- `ui/tab_vehinh.py`: ảnh đề vừa dán hoặc vừa chọn hiện ngay trên khung xem trước, thu nhỏ `KeepAspectRatio`. Khi có kết quả vẽ, khung chuyển sang ảnh thành phẩm.
- `core/prompt_builder.py`: `_inputs` gặp thư mục thì quét đệ quy `.docx`, `.pdf`, `.md`, `.txt`, `.png`, `.jpg`, `.jpeg` và ghi từng đường dẫn. File khác đuôi không đưa vào prompt.
- `build_exe.bat` chạy lại, exit 0. File exe mới nằm trong `app_trolythien\dist\TroLyHoangThien\`.

## Kiểm thử

- Qt offscreen: dán chữ «Hình bình hành ABCD» vào ô soạn thảo, khung xem trước không bị gắn ảnh.
- Ảnh đỏ trên clipboard: lưu `clip_*.png` dưới `.runtime\clipboard_images`, nhãn «Đã chọn 1 tệp», pixmap xem trước không rỗng.
- Ctrl+V một ảnh khác: không đổ chữ vào ô, lưu PNG mới, xem trước đổi theo ảnh đó.
- `show_result` một PNG xanh: khung xem trước đổi sang ảnh kết quả.
- Thư mục tạm có `giao_an.docx`, `thang9\de.pdf`, `ghi_chu.md` và `nhap.xlsx`: nhãn «Đã chọn thư mục: troly-ho-so (3 tệp)». Prompt duyệt giáo án liệt kê ba tệp tài liệu, không có file xlsx.
- `TroLyHoangThien.exe` còn sống sau 4 giây, rồi bị tắt. Chưa bấm Win+Shift+S trên cửa sổ thật.
- Lượt sau, cùng plan, mã nguồn không đổi. Kiểm tra lại Qt offscreen: dán chữ, dán ảnh, Ctrl+V ảnh, nhãn thư mục 3 tệp, prompt bỏ file `.xlsx`. Bản exe lúc 09:59 mới hơn `kit.py`, `tab_vehinh.py` và `prompt_builder.py`, nên không đóng gói lại.

## Giới hạn

- Không chạy một lượt vẽ hình bằng `agy`. Cầu nối `agy.exe` không đổi.
- Chưa bấm các nút hộp thoại chọn thư mục bằng tay. Hàm gán danh sách và hàm dựng prompt đã được gọi trực tiếp.
- Không sửa trang web của repo.
