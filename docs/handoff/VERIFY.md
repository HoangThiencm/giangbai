# VERIFY: Nghiệm thu Bảng Biểu Phụ Lục 3 Hoàn Chỉnh (Table View 8 Cột), Phân Bổ Số Tiết Chuẩn Toán 6 (Không Cào Bằng 4 Tiết) Và Cột Tick Chọn 12 Tiết AI

## Kết luận
PASS

## Đối chiếu scope
1. **Chuyển Đổi Hoàn Toàn Sang Dạng Bảng Biểu Chuẩn (Table View 8 Cột)**:
   - Đã thay thế hoàn toàn dạng lưới thẻ card (grid cards) cũ ở Mục 3 bằng thẻ `<table>` chuyên nghiệp trong container cuộn ngang (`overflow-x-auto`).
   - Đầy đủ 8 cột rõ ràng: `STT | Bài học | Số tiết | Tiết CT | Tuần | Thiết bị dạy học | Địa điểm | Tích hợp AI (QĐ 2422)`.
   - Các dòng phân chương/học kỳ (`isHeader: true`) được gộp đủ `colspan="8"` in đậm, căn giữa theo đúng hình thái văn bản PPCT chuẩn Bộ GD&ĐT.
2. **Phân Bổ Số Tiết Chuẩn Xác Cho Từng Bài Học (Toán 6 Không Bị Cào Bằng 4 Tiết)**:
   - Danh sách mẫu Toán 6 nạp đúng 47 bài học thực tế với số tiết chuẩn xác từ `GIAO AN/XAYDUNGPHULUC/Phụ lục 1 - Lớp 6 - Toán.docx`: Bài 1–4: 1 tiết, Bài 5: 2 tiết, Ôn tập chương: 5 tiết...
   - Cột `Số tiết` là ô input trực tiếp: Cho phép giáo viên tăng/giảm số tiết của bất kỳ bài nào; checkbox tiết con ở cột cuối tự động mở rộng/thu gọn và cập nhật tỷ lệ AI đồng bộ.
3. **Cột Tích Hợp AI Trực Quan & Bộ Công Cụ Chọn 12 Tiết**:
   - Cột thứ 8 hiển thị nút chọn "Cả bài" và danh sách checkbox từng tiết con (`Tiết 1`, `Tiết 2`...).
   - Bộ đếm `🎯 Đã chọn: X/12 tiết AI`, nút `✨ Gợi ý 12 tiết chuẩn` và `✕ Bỏ chọn tất cả` hoạt động chính xác.
4. **Cơ Chế Liên Thông Phụ Lục 1 & Phụ Lục 3**:
   - Nạp file Phụ lục 3 $\rightarrow$ Phụ lục 3 giữ nguyên 100% bảng nguồn, Phụ lục 1 tự động sinh đầy đủ cột `Yêu cầu cần đạt` chuẩn CT GDPT 2018.
5. **Xuất Word (.docx) & Preview 2 Màu Chuẩn Khung File Mẫu**:
   - Mã NLS Màu Xanh (`0070C0`), Mã NLAI Màu Tím (`7030A0`), đầy đủ 6 phần theo `Phụ lục 1 - Lớp 6 - Toán.docx`.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` $\rightarrow$ PASS (kiểm tra 8 cột Table View ở Mục 3, dòng gộp header colspan 8, phân bổ số tiết Toán 6 không cào bằng, sửa số tiết trực tiếp, xuất Word 2 màu).
- `node tests/xaydungphuluc-integration-smoke.js` $\rightarrow$ PASS.
- Kiểm tra cú pháp JavaScript nội tuyến của `xaydungphuluc.html` qua `node --check` $\rightarrow$ PASS 100%.

## Pass / Fail từng tiêu chí
1. Mục 3 hiển thị dưới dạng Bảng biểu Phụ lục 3 (Table View 8 cột) $\rightarrow$ **PASS**.
2. Dòng tiêu đề chương gộp đủ `colspan="8"` in đậm $\rightarrow$ **PASS**.
3. Số tiết của từng bài học Toán 6 chuẩn xác (1 tiết, 2 tiết, 3 tiết...), không còn bị chia đều 4 tiết $\rightarrow$ **PASS**.
4. Chỉnh sửa số tiết trực tiếp trên bảng và đồng bộ checkbox tiết con $\rightarrow$ **PASS**.
5. Cột tick chọn 12 tiết AI và nút gợi ý 12 tiết chuẩn $\rightarrow$ **PASS**.
6. Liên thông tự sinh YCCĐ cho Phụ lục 1 từ Phụ lục 3 $\rightarrow$ **PASS**.
7. Xuất Word & Preview 2 màu NLS Xanh `0070C0` / NLAI Tím `7030A0` $\rightarrow$ **PASS**.

## Bug
- Không có lỗi tồn đọng.
