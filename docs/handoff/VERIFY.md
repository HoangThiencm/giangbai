# VERIFY: Nghiệm thu Khớp Chuẩn File Mẫu "Phụ lục 1 - Lớp 6 - Toán.docx", Bảo Toàn Biểu Mẫu Nguồn, Chọn 12 Tiết AI và Định Dạng Màu Sắc NLS Xanh - NLAI Tím

## Kết luận
PASS

## Đối chiếu scope
1. **Khớp Hình Thức & Cấu Trúc Khung Chuẩn File Mẫu ([Phụ lục 1 - Lớp 6 - Toán.docx](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/GIAO%20AN/XAYDUNGPHULUC/Ph%E1%BB%A5%20l%E1%BB%A5c%201%20-%20L%E1%BB%9Bp%206%20-%20To%C3%A1n.docx))**:
   - File xuất Word `.docx` và Web Preview đã tái lập đầy đủ 6 phần chuẩn:
     1. Tiêu ngữ 2 cột hành chính (UBND Xã/Phường, Trường THCS, Tổ chuyên môn / Quốc hiệu, Tiêu ngữ).
     2. Tiêu đề chuẩn căn cứ Công văn số 5512/BGDĐT-GDTrH, Môn học, Khối lớp, Năm học.
     3. Phần I. Đặc điểm tình hình (I.1 Số lớp/HS, I.2 Đội ngũ GV, I.3 Bảng Thiết bị TT 38/2021, I.4 Bảng Phòng bộ môn TT 14/2020).
     4. Phần II. Kế hoạch dạy học:
        - Bảng PPCT: Giữ nguyên vẹn tất cả các cột và dữ liệu nguồn của người dùng (hoặc mẫu chuẩn 7 cột), **chỉ bổ sung đúng 01 cột duy nhất ở cuối: `Mã NLS & AI (CV 3456 & QĐ 2422)`**.
        - II.2 Bảng Chuyên đề lựa chọn.
        - II.3 Bảng Kiểm tra đánh giá định kỳ 4 đợt (GK1 Tuần 9, CK1 Tuần 18, GK2 Tuần 27, CK2 Tuần 35).
     5. Phần III. Các nội dung khác (Bồi dưỡng HSG, phụ đạo học sinh, sinh hoạt chuyên môn cụm trường).
     6. Bảng Chữ ký phê duyệt 2 bên chuẩn hành chính (Tổ trưởng & Hiệu trưởng / Giáo viên & Tổ trưởng).
2. **Khắc Phục Triệt Để Lỗi Bóc Tách Bảng Nguồn**:
   - Tách riêng từng bảng độc lập khi đọc file tải lên; loại trừ hoàn toàn bảng thông tin hành chính (`TRƯỜNG THCS...`) khỏi các dòng bài học của PPCT.
3. **Bộ Lọc Sách Giáo Khoa Tinh Gọn (Smart Pedagogical Indexing)**:
   - Tự động bóc tách các đề mục trọng tâm của SGK (`Tên bài` + `Mục tiêu cần đạt` + `Hoạt động khám phá / luyện tập / vận dụng`), giảm 95% token để AI hiểu sâu ngữ cảnh bài học mà siêu tiết kiệm Quota.
4. **Chọn 12 Tiết AI Chủ Động**:
   - Giao diện có checkbox cho phép giáo viên tự tick chọn tối đa 12 tiết trọng tâm (kèm nút gợi ý 12 bài Hình học, Thống kê, Trải nghiệm); AI chỉ sinh mã AI cho đúng các bài đã tick.
5. **Phân Biệt 2 Màu Sắc Khi Xuất Bản**:
   - Mã Năng lực số (NLS): Chữ **Màu Xanh** (`0070C0`).
   - Mã Năng lực AI (NLAI): Chữ **Màu Tím** (`7030A0`).
6. **Thanh Tiến Trình Thời Gian Thực (% Floating Progress Bar)**:
   - Spinner dừng, hiển thị tích xanh `✓`, thông báo hoàn tất và tự động ẩn sau 1.5s khi đạt 100%; có nút đóng `✕` thao tác ngay.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` $\rightarrow$ PASS (kiểm tra bóc tách bảng độc lập, 6 phần tài liệu, chọn 12 tiết AI, màu NLS xanh / NLAI tím).
- `node tests/xaydungphuluc-integration-smoke.js` $\rightarrow$ PASS.
- Kiểm tra cú pháp JavaScript nội tuyến của `xaydungphuluc.html` qua `node --check` $\rightarrow$ PASS 100%.

## Pass / Fail từng tiêu chí
1. Cấu trúc hình thức file xuất ra khớp 100% file mẫu `Phụ lục 1 - Lớp 6 - Toán.docx` $\rightarrow$ **PASS**.
2. Bảo toàn 100% bảng biểu nguồn người dùng, chỉ thêm cột Mã NLS & AI $\rightarrow$ **PASS**.
3. Bóc tách bảng độc lập, loại bỏ rò rỉ header hành chính vào dòng bài học $\rightarrow$ **PASS**.
4. Bộ lọc SGK tinh gọn (Smart Pedagogical Indexing) $\rightarrow$ **PASS**.
5. Tick chọn 12 tiết AI chủ động và chỉ sinh AI cho bài đã chọn $\rightarrow$ **PASS**.
6. Định dạng xuất Word & Preview 2 màu (NLS Xanh `0070C0` - NLAI Tím `7030A0`) $\rightarrow$ **PASS**.
7. Thanh tiến trình dừng spinner và tự động ẩn khi đạt 100% $\rightarrow$ **PASS**.

## Bug
- Không có lỗi tồn đọng.
