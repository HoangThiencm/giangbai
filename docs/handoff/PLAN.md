# PLAN: Loại bỏ Khối "Thông tin bài dạy" Rườm rà trên Giao diện Tích hợp Giáo án (giaoantichhop.html)

## Hiện trạng & Phân tích
1. **Phản ánh của giáo viên:**
   - Khối **"Thông tin bài dạy"** (gồm: Môn học, Khối lớp, Tên bài dạy, Thời lượng (tiết)) chiếm vị trí lớn ngay giữa giao diện nạp giáo án và ghi chú PPCT.
   - Khi giáo viên đã nạp file giáo án gốc (DOCX/PDF/TXT), toàn bộ thông tin môn học, bài dạy, thời lượng đã có sẵn trong file.
   - Việc bắt buộc nhìn thấy và nhập các ô này là thừa thãi, rườm rà, gây xao nhãng quy trình làm việc chính.
2. **Cơ chế Direct OOXML Injection hiện tại:**
   - Khi cấy vào DOCX, hệ thống dùng `buildDeltaPrompt()` trích xuất nội dung trực tiếp từ file DOCX và ghi chú PPCT, không hề phụ thuộc vào các ô nhập `subject`, `title`, `duration`.
   - File Word cấy giữ nguyên 100% phần đầu và nội dung gốc của giáo viên.
3. **Phụ thuộc kỹ thuật cần xử lý khi ẩn/loại bỏ UI:**
   - `grade`: Được dùng để lọc danh mục chuẩn NLS/AI (`entriesForGrade(kind, grade)`). Nếu bỏ dropdown khối lớp chính, cần:
     + Tự động nhận diện khối lớp từ nội dung giáo án / PPCT / mã AI (ví dụ `8.A1.2` -> Lớp 8).
     + Dự phòng giá trị mặc định (Lớp 8 hoặc tự động chuyển khi phát hiện mã khối lớp khác).
     + Di chuyển bộ chọn Khối lớp tinh gọn vào bên trong `<details>` "Chọn thêm chuẩn chính thức nếu PPCT chưa đủ" (chỉ khi giáo viên mở tra cứu chuẩn thủ công mới thấy).
   - `title`: Được dùng làm tên file xuất dự phòng khi không có `currentDocxName`. Fallback sang tên file nạp hoặc `safeFileName` mặc định.
   - `duration`: Được dùng trong `selectionLimit()` (1 tiết -> 1 mã; >= 2 tiết -> 2 mã). Mặc định là 2 tiết (cho phép chọn tối đa 2 mã theo chuẩn phổ biến), hoặc tự nhận diện nếu giáo án ghi 1 tiết.
   - `subject`, `teacher`: Chuyển thành các trường ẩn (`type="hidden"`) để không gây lỗi tham chiếu khi gọi `buildPrompt()`, `loadSample()`, `clearAll()`, hay `suggestStandards()`.

## Phạm vi Thay đổi
1. **Giao diện HTML (`giaoantichhop.html`):**
   - Xóa bỏ hoàn toàn khối tiêu đề `<h2 class="font-extrabold text-lg mb-4"><i class="fa-solid fa-pen-to-square text-emerald-600 mr-2"></i>Thông tin bài dạy</h2>` và lưới 4 ô nhập (`grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-3`).
   - Di chuyển một dropdown Khối lớp nhỏ gọn vào bên trong `<details>` mục tra cứu danh mục chuẩn (để giáo viên chỉ đổi khối lớp khi cần tra cứu thêm chuẩn ngoài PPCT).
   - Đưa các trường `subject`, `title`, `duration` thành các input ẩn (`type="hidden"`).
2. **Logic JavaScript (`giaoantichhop.html`):**
   - Trong `readLessonFile(file)`: Tự động trích xuất tên bài từ `file.name` gán vào `currentDocxName` hoặc giá trị ngầm của `title`.
   - Tự động nhận diện khối lớp khi phân tích PPCT (`parsePpctIntegration`): phát hiện mã bắt đầu bằng `6.`, `7.`, `8.`, `9.` hoặc chuỗi "Toán 6/7/8/9", "Lớp 6/7/8/9" để tự động cập nhật `grade`.
   - Đảm bảo `fields = ['subject','grade','title','duration', ...]` vẫn tìm thấy các phần tử (dạng hidden) để không bị vỡ các hàm reset/load mẫu (`loadSample`, `clearAll`, `suggestStandards`).
   - Luồng giao diện sau khi tinh gọn chỉ còn 2 khối thao tác chính ở cột trái:
     1. **Nạp giáo án gốc** (Dropzone DOCX, PDF, TXT)
     2. **Ghi chú PPCT & nhận diện tích hợp** (Dán text hoặc dán ảnh)
     -> Nút **BẮT ĐẦU TÍCH HỢP VÀO GIÁO ÁN**.

## Tiêu chí Nghiệm thu (Verification Checklist)
- [ ] Giao diện cột trái không còn xuất hiện khối "Thông tin bài dạy" và 4 ô nhập (Môn học, Khối lớp, Tên bài dạy, Thời lượng).
- [ ] Giao diện sạch sẽ, liền mạch từ "Nạp giáo án gốc" đến "Ghi chú PPCT & nhận diện tích hợp".
- [ ] Tính năng nạp giáo án mẫu, xóa trắng hoạt động bình thường không có lỗi console.
- [ ] Nhận diện PPCT và cấy Direct OOXML vẫn hoạt động chuẩn xác 100%.
- [ ] Xuất file Word vẫn giữ nguyên định dạng và tên file hợp lý.
- [ ] Kiểm tra Edge Headless DOM dump đạt kết quả hiển thị tốt, 0 lỗi JavaScript.
