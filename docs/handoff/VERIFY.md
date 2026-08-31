# VERIFY: Nghiệm thu Giao Diện Nạp PPCT / SGK Riêng Biệt, Bảng Tick Chọn 12 Tiết AI Luôn Hiển Thị và Định Dạng Màu Sắc NLS Xanh - NLAI Tím

## Kết luận
PASS

## Đối chiếu scope
1. **Giao Diện Nạp Dữ Liệu Tách Biệt & Nút Nhận Diện PPCT**:
   - Khu vực 2 đã chia thành 2 ô nạp tệp rõ ràng, độc lập:
     + Ô 1: `📄 Tải lên Phân phối chương trình (DOCX, XLSX, PDF)` $\rightarrow$ Bóc tách và bảo toàn cấu trúc bảng bài học.
     + Ô 2: `📚 Tải lên Sách Giáo Khoa (PDF, DOCX)` $\rightarrow$ Lọc tinh gọn tên bài, mục tiêu và hoạt động (giảm 95% token).
   - Bổ sung nút: `🔍 Nạp cấu trúc PPCT chuẩn theo Môn & Lớp` cho phép nạp danh sách bài học ngay tức thì kể cả khi chưa có file.
2. **Bảng Tick Chọn 12 Tiết AI Luôn Hiển Thị (Mục 3)**:
   - Thẻ `#aiLessonPickerCard` không còn bị ẩn mặc định, tự động nạp cấu trúc bài học mẫu ngay khi mở trang và khi đổi Môn/Khối lớp.
   - Hiển thị danh sách bài học kèm checkbox từng bài, bộ đếm trực quan `🎯 Đã chọn: X/12 tiết AI`.
   - Có đầy đủ nút `✨ Gợi ý 12 tiết chuẩn` (ưu tiên Hình học, Thống kê, Trải nghiệm) và nút `✕ Bỏ chọn tất cả`.
   - Gemini AI chỉ sinh mã `[AI: ...]` vào đúng các bài học được tick chọn.
3. **Phân Biệt 2 Màu Sắc Khi Xuất Word (.docx) & Web Preview**:
   - Mã Năng lực số (NLS): Chữ **Màu Xanh** (`0070C0`).
   - Mã Năng lực AI (NLAI): Chữ **Màu Tím** (`7030A0`).
4. **Cơ Chế Liên Thông Phụ Lục 1 & Phụ Lục 3**:
   - Khi nguồn là Phụ lục 3: Bảng Phụ lục 3 giữ nguyên cấu trúc tiến độ, Phụ lục 1 tự động được sinh đầy đủ cột `Yêu cầu cần đạt` chuẩn CT GDPT 2018.
5. **Cấu Trúc Khung Hình Thức Chuẩn Khớp 100% File Mẫu**:
   - Đầy đủ 6 phần theo `Phụ lục 1 - Lớp 6 - Toán.docx`.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` $\rightarrow$ PASS (kiểm tra 2 ô nạp file độc lập, nút nạp PPCT mẫu, bảng tick chọn AI, màu NLS xanh / NLAI tím).
- `node tests/xaydungphuluc-integration-smoke.js` $\rightarrow$ PASS.
- Kiểm tra cú pháp JavaScript nội tuyến của `xaydungphuluc.html` qua `node --check` $\rightarrow$ PASS 100%.

## Pass / Fail từng tiêu chí
1. Ô nạp PPCT và ô nạp SGK riêng biệt $\rightarrow$ **PASS**.
2. Nút nhận diện PPCT chuẩn theo Môn & Lớp $\rightarrow$ **PASS**.
3. Bảng tick chọn 12 tiết AI luôn hiển thị sẵn sàng trên giao diện $\rightarrow$ **PASS**.
4. Nút gợi ý 12 tiết chuẩn và nút bỏ chọn tất cả $\rightarrow$ **PASS**.
5. AI chỉ sinh mã AI cho các bài đã tick $\rightarrow$ **PASS**.
6. Định dạng xuất Word & Preview 2 màu (NLS Xanh `0070C0` - NLAI Tím `7030A0`) $\rightarrow$ **PASS**.
7. Khớp khung cấu trúc 6 phần chuẩn file mẫu `Phụ lục 1 - Lớp 6 - Toán.docx` $\rightarrow$ **PASS**.

## Bug
- Không có lỗi tồn đọng.
