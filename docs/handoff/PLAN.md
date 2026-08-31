# PLAN: Chuyển Đổi Hiển Thị Phụ Lục 3 Thành Bảng Biểu Chuẩn (Table View Đầy Đủ Cột) Kèm Cột Tick Chọn 12 Tiết AI, Đúng Chính Xác Số Tiết Từng Bài Thay Vì Thẻ Card Chia Đều 4 Tiết

## Hiện trạng
1. **Phân Tích Bất Cập Trực Quan Từ Ảnh Chụp (`media_1788175822064.png`)**:
   - Hiện tại, Mục 3 hiển thị dưới dạng **lưới các ô thẻ (Grid cards)** và tự động chia đều mỗi bài 4 tiết (`Tiết 1-4`, `Tiết 5-8`, `Tiết 9-12`...).
   - Cách hiển thị dạng thẻ card này làm mất đi hình thái **Bảng Kế hoạch dạy học / Phụ lục 3 quen thuộc của giáo viên**, đồng thời việc gán cứng 4 tiết cho tất cả các bài là sai lệch với thực tế sư phạm (trong thực tế: Bài 1 chỉ có 1 tiết, Bài 2 có 1 tiết, Bài 5 có 2 tiết, v.v.).
2. **Kỳ Vọng Nghiệp Vụ Của Giáo Viên**:
   - **Hiển thị trực quan dưới dạng BẢNG BIỂU CHUẨN (Table View)**:
     * Thay vì các thẻ card rời rạc, Mục 3 hiển thị thành một **Bảng Phụ lục 3 hoàn chỉnh** với đầy đủ các cột:
       $$\text{STT} \;\vert\; \text{Bài học} \;\vert\; \text{Số tiết} \;\vert\; \text{Tiết CT} \;\vert\; \text{Tuần} \;\vert\; \text{Thiết bị dạy học} \;\vert\; \text{Địa điểm} \;\vert\; \mathbf{\text{Tích hợp AI (QĐ 2422)}}$$
     * Dòng tiêu đề phân chương (`CHƯƠNG I`, `HỌC KÌ I`) gộp toàn bộ các cột, in đậm nổi bật.
     * Cột `Số tiết` hiển thị đúng số tiết thực tế của bài (1 tiết, 2 tiết...) và cho phép giáo viên chỉnh sửa số tiết trực tiếp trên bảng.
     * Cột `Tích hợp AI (QĐ 2422)` hiển thị các nút checkbox `Tiết 1`, `Tiết 2`... để giáo viên tick chọn đúng 12 tiết trọng tâm.
   - Khi tải file Phụ lục 3 lên: Hệ thống nạp và hiển thị ngay 100% bảng dữ liệu gốc của giáo viên vào Bảng biểu Mục 3 này.

## Phạm vi
1. **Chuyển Đổi Giao Diện Mục 3 Sang Dạng Bảng Biểu Sư Phạm Hoàn Chỉnh (Table Layout)**:
   - Thay thế toàn bộ layout thẻ card bằng thẻ `<table>` chuyên nghiệp:
     * Cột `STT`: Số thứ tự (1, 2, 3...).
     * Cột `Bài học`: Tên bài học thật.
     * Cột `Số tiết`: Ô input số tiết thực tế (`1`, `2`, `3`...).
     * Cột `Tiết CT`: Tiết phân phối chương trình thực tế.
     * Cột `Tuần`: Tuần thực hiện.
     * Cột `Thiết bị dạy học`: Danh mục thiết bị.
     * Cột `Địa điểm`: Lớp học / Phòng bộ môn.
     * Cột `Chọn AI (QĐ 2422)`: Các checkbox `Tiết 1`, `Tiết 2`... (hoặc nút tick chọn cả bài).
   - Thanh công cụ trên đầu bảng:
     * `🎯 Đã chọn: X/12 tiết AI`.
     * `✨ Gợi ý 12 tiết chuẩn`.
     * `✕ Bỏ chọn tất cả`.
2. **Dữ Liệu Mẫu Toán 6 Chuẩn Khớp Thực Tế (Không Chia Đều 4 Tiết)**:
   - Nạp đúng 47 bài học Toán 6 từ file mẫu `Phụ lục 1 - Lớp 6 - Toán.docx` với số tiết chuẩn xác: Bài 1 (1 tiết), Bài 2 (1 tiết), Bài 3 (1 tiết), Bài 4 (1 tiết), Bài 5 (2 tiết), Ôn tập chương (5 tiết)...
3. **Cơ Chế Liên Thông Phụ Lục 1 & Phụ Lục 3**:
   - Khi nạp file Phụ lục 3: Bảng Phụ lục 3 giữ nguyên 100% các cột nguồn, Phụ lục 1 tự động được sinh `Yêu cầu cần đạt` chuẩn CT GDPT 2018.
4. **Xuất Word (.docx) & Preview 2 Màu Chuẩn Khung File Mẫu**:
   - Mã NLS Màu Xanh (`0070C0`), Mã NLAI Màu Tím (`7030A0`), đầy đủ 6 phần theo `Phụ lục 1 - Lớp 6 - Toán.docx`.
5. **Đồng Bộ API Key CSDL Hai Chiều (`api/user_gemini_keys.php`)**:
   - Nhận diện đủ 100% key Gemini và Mistral của người dùng.

## Ngoài phạm vi
- Không can thiệp các file ngoài `xaydungphuluc.html` và file test liên quan.

## File dự kiến tác động
- `xaydungphuluc.html` [THAY THẾ GRID CARDS BẰNG BẢNG BIỂU PHỤ LỤC 3 CHUẨN ĐẦY ĐỦ CỘT KÈM CỘT TICK AI, NẠP ĐÚNG SỐ TIẾT TỪNG BÀI TOÁN 6]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG SMOKE TEST CHO TABLE VIEW PHỤ LỤC 3 VÀ CỘT TICK AI]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Tái Cấu Trúc Mục 3 thành Bảng Biểu `<table>` trong `xaydungphuluc.html`**:
   - Render bảng đầy đủ 8 cột: `STT | Bài học | Số tiết | Tiết CT | Tuần | Thiết bị | Địa điểm | Tích hợp AI`.
   - Các dòng tiêu đề chương `isHeader: true` gộp `colspan="8"` in đậm, căn giữa.
2. **Bước 2: Cập Nhật Dữ Liệu Số Tiết Chuẩn Toán 6**:
   - Gán đúng số tiết thực tế của 47 bài Toán 6 (từ 1 đến 5 tiết) thay vì chia đều 4 tiết.
3. **Bước 3: Hoàn Thiện Tương Tác Sửa Số Tiết Trực Tiếp Trên Bảng**:
   - Khi sửa ô số tiết ở dòng nào: Checkbox tiết ở cột cuối tự động cập nhật số lượng `Tiết 1..N` tương ứng.
4. **Bước 4: Chạy và Hoàn Thiện Kiểm Thử**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`, xác nhận PASS 100%.

## Rủi ro
- **Rủi ro**: Bảng có 8 cột bị tràn ngang trên màn hình hẹp.
  - *Giải pháp*: Bọc bảng trong `<div class="overflow-x-auto">` với độ rộng cột hợp lý và chữ tự động xuống dòng rõ ràng.

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy `node tests/xaydungphuluc-smoke.js`:
     + Xác nhận Mục 3 được render dạng bảng `<table>` với đầy đủ các cột `Bài học`, `Số tiết`, `Tiết CT`, `Tuần`, `Thiết bị`, `Địa điểm`, `Tích hợp AI`.
     + Xác nhận Toán 6 nạp đúng số tiết thực tế (Bài 1: 1 tiết, Bài 5: 2 tiết, không bị ép 4 tiết).
2. **Kiểm thử thủ công trên trình duyệt**:
   - Mở `xaydungphuluc.html` $\rightarrow$ Thấy ngay Bảng Phụ lục 3 hoàn chỉnh, thoáng đẹp, có đầy đủ cột và cột tick chọn AI ở cuối.
   - Thử tick chọn các tiết $\rightarrow$ Quan sát bộ đếm và thanh slider AI cập nhật mượt mà.

## Tiêu chí nghiệm thu
1. Mục 3 hiển thị dưới dạng Bảng biểu Phụ lục 3 hoàn chỉnh (Table View) với đầy đủ các cột chuẩn, thay thế hoàn toàn dạng lưới thẻ card.
2. Số tiết của từng bài học được hiển thị chính xác theo thực tế (không bị chia đều 4 tiết).
3. Toàn bộ smoke test tự động đều PASS 100%.
