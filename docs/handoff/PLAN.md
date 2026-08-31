# PLAN: Tích Hợp Toàn Diện Bộ Lọc Sách Giáo Khoa Thông Minh, Chọn Đích Danh 12 Tiết AI, Phân Biệt Màu Sắc (NLS Xanh - NLAI Tím) và Tái Lập 100% Khung Hình Thức File Mẫu "Phụ lục 1 - Lớp 6 - Toán.docx"

## Hiện trạng
1. **Khớp Hình Thức & Cấu Trúc Toàn Diện theo File Mẫu Chuẩn ([Phụ lục 1 - Lớp 6 - Toán.docx](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/GIAO%20AN/XAYDUNGPHULUC/Ph%E1%BB%A5%20l%E1%BB%A5c%201%20-%20L%E1%BB%9Bp%206%20-%20To%C3%A1n.docx))**:
   - File xuất Word `.docx` và bảng xem trước Web Preview phải có đầy đủ 6 phần chuẩn:
     1. Tiêu ngữ 2 cột hành chính (UBND Xã/Phường, Trường THCS, Tổ chuyên môn / Quốc hiệu, Tiêu ngữ).
     2. Tiêu đề chuẩn căn cứ Công văn số 5512/BGDĐT-GDTrH, Môn học, Khối lớp, Năm học.
     3. Phần I. Đặc điểm tình hình (I.1 Số lớp/HS, I.2 Đội ngũ GV, I.3 Bảng Thiết bị TT 38/2021, I.4 Bảng Phòng bộ môn TT 14/2020).
     4. Phần II. Kế hoạch dạy học:
        - **Bảng PPCT**: Giữ nguyên 100% tất cả các cột và dữ liệu của người dùng tải lên (hoặc biểu mẫu chuẩn: `Bài học`, `Số tiết`, `Tiết CT`, `Tuần`, `Thiết bị dạy học (*)`, `Địa điểm dạy học (**)`).
        - **CHỈ BỔ SUNG 01 CỘT DUY NHẤT Ở CUỐI BẢNG**: `Mã NLS & AI (CV 3456 & QĐ 2422)`.
        - II.2 Bảng Chuyên đề lựa chọn.
        - II.3 Bảng Kiểm tra đánh giá định kỳ 4 đợt (GK1 Tuần 9, CK1 Tuần 18, GK2 Tuần 27, CK2 Tuần 35).
     5. Phần III. Các nội dung khác (Bồi dưỡng HSG, phụ đạo học sinh, sinh hoạt chuyên môn cụm trường).
     6. Bảng Chữ ký phê duyệt 2 bên chuẩn hành chính (Tổ trưởng & Hiệu trưởng / Giáo viên & Tổ trưởng).
2. **Khắc Phục Triệt Để Lỗi Bóc Tách Bảng PPCT**:
   - Tách riêng từng bảng HTML/Word độc lập, loại trừ hoàn toàn bảng thông tin hành chính (`TRƯỜNG THCS...`) khỏi các dòng bài học của PPCT.
3. **Bộ Lọc Sư Phạm Tinh Gọn Khi Tải SGK (Smart Pedagogical Indexing)**:
   - Khi tải tệp Sách giáo khoa (PDF/DOCX ~150–200 trang), hệ thống tự động bóc tách các đề mục trọng tâm: `Tên bài` + `Mục tiêu cần đạt` + `Hoạt động khám phá / luyện tập / vận dụng` $\rightarrow$ Giảm dung lượng token 95% (từ 140k xuống 5k–8k token), giúp AI hiểu sâu nội dung từng bài trong bộ sách mà siêu tiết kiệm Quota.
4. **Bảng Chọn Tiết AI Chủ Động (Tick 12 Tiết)**:
   - Giáo viên có thể tick chọn chính xác 12 tiết trọng tâm trên bảng PPCT (kèm nút gợi ý 12 tiết chuẩn về Hình học, Thống kê, Trải nghiệm); AI chỉ sinh mã AI cho các tiết đã tick.
5. **Phân Biệt Màu Sắc Xuất Bản**:
   - Web Preview và file Word `.docx` phân biệt rõ 2 màu:
     + Mã Năng lực số (NLS): Chữ **Màu Xanh** (`0070C0`).
     + Mã Năng lực AI (NLAI): Chữ **Màu Tím** (`7030A0`).
6. **Thanh Tiến Trình Thời Gian Thực (% Floating Progress Bar)**:
   - Khi đạt 100%: Dừng spinner, hiển thị tích xanh `✓`, thông báo hoàn tất và tự động ẩn mượt mà sau 1.5 giây; có nút đóng `✕`.

## Phạm vi
1. **Trình Bóc Tách Bảng Thông Minh & Lọc SGK Tinh Gọn**:
   - Khi tải file `.docx` / `.xlsx` / `.pdf`:
     + Nhận diện riêng Bảng PPCT, Bảng Thiết bị, Bảng Phòng bộ môn, Bảng KTĐG; bỏ qua bảng hành chính.
     + Nếu có tệp SGK, trích xuất cấu trúc các bài học và hoạt động chính để làm ngữ cảnh sư phạm cho Gemini AI.
2. **Cột Tick Chọn Tiết AI Trên Giao Diện PPCT**:
   - Hiển thị danh sách bài học kèm checkbox `Chọn AI`, thanh đếm `Đã chọn: X/12 tiết` và nút `Gợi ý 12 tiết chuẩn`.
   - Siêu Prompt Gemini AI chỉ điền mã `[AI: ...]` vào các bài có `aiSelected: true`.
3. **Bộ Xuất Word (.docx) & Web Preview 2 Màu Chuẩn Hình Thức File Mẫu**:
   - Tái lập đầy đủ 6 phần chuẩn theo `Phụ lục 1 - Lớp 6 - Toán.docx`.
   - Xuất riêng từng đoạn TextRun: NLS Màu Xanh (`0070C0`), NLAI Màu Tím (`7030A0`).
   - Đầy đủ chú thích `(*)` TT 38/2021, `(**)` TT 14/2020 và chữ ký 2 bên.
4. **Bộ Kiểm thử Tự động ([tests/xaydungphuluc-smoke.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/tests/xaydungphuluc-smoke.js))**:
   - Cập nhật bài test kiểm tra bóc tách bảng độc lập, chọn 12 tiết AI, xuất Word 2 màu và cấu trúc 6 phần.

## Ngoài phạm vi
- Không can thiệp các file ngoài `xaydungphuluc.html` và file test liên quan.

## File dự kiến tác động
- `xaydungphuluc.html` [TÍCH HỢP BỘ LỌC SGK, CHỌN 12 TIẾT AI, MÀU NLS XANH / AI TÍM, CHUẨN HÓA DOCX 6 PHẦN THEO FILE MẪU]
- `tests/xaydungphuluc-smoke.js` [CẬP NHẬT SMOKE TEST]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Nâng Cấp Bộ Bóc Tách Bảng Độc Lập & Bộ Lọc SGK trong `xaydungphuluc.html`**:
   - Tách riêng Bảng PPCT, Thiết bị, Phòng bộ môn, KTĐG khi đọc file tải lên; loại bỏ bảng hành chính.
   - Tạo hàm lọc SGK tinh gọn (trích xuất mục tiêu & hoạt động từng bài).
2. **Bước 2: Bổ Sung Vùng Chọn Tiết AI Trên Biểu Mẫu**:
   - Thêm checkbox `aiSelected` cho từng dòng bài học, thanh đếm 12 tiết và nút gợi ý 12 tiết chuẩn.
3. **Bước 3: Nâng Cấp Siêu Prompt Gemini AI**:
   - Truyền ngữ cảnh SGK tinh gọn và danh sách các bài học đã tick chọn AI.
   - AI sinh mã NLS cho toàn bộ theo tỷ lệ/mật độ, và CHỈ sinh mã AI cho các bài đã tick chọn.
4. **Bước 4: Nâng Cấp Trình Xuất Word (.docx) & Web Preview 2 Màu**:
   - Xuất đầy đủ 6 phần khớp 100% với `Phụ lục 1 - Lớp 6 - Toán.docx`.
   - Phân biệt màu sắc: NLS Màu Xanh (`0070C0`), NLAI Màu Tím (`7030A0`).
5. **Bước 5: Cập nhật và chạy kiểm thử tự động**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`, xác nhận PASS 100%.

## Rủi ro
- **Rủi ro**: File Word xuất ra bị sai màu nếu thư viện `docx.js` nhận mã màu không hợp lệ.
  - *Giải pháp*: Sử dụng mã màu hex không có dấu `#` theo chuẩn docx (`0070C0` cho Xanh dương, `7030A0` cho Tím).

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy `node tests/xaydungphuluc-smoke.js`:
     + Xác nhận bóc tách bảng PPCT không bị dính bảng hành chính.
     + Xác nhận có logic chọn 12 tiết AI và bộ lọc SGK.
     + Xác nhận xuất Word có mã màu `0070C0` (NLS) và `7030A0` (NLAI).
     + Xác nhận cấu trúc tài liệu đầy đủ 6 phần như file `Phụ lục 1 - Lớp 6 - Toán.docx`.
2. **Kiểm thử thủ công trên trình duyệt**:
   - Tải file PPCT và SGK lên $\rightarrow$ Kiểm tra danh sách bài học hiển thị sạch sẽ.
   - Bấm `Gợi ý 12 tiết chuẩn` hoặc tự tick chọn các bài $\rightarrow$ Bấm Sinh Phụ lục.
   - Xuất file Word `.docx` $\rightarrow$ Mở kiểm tra cấu trúc giống hệt `Phụ lục 1 - Lớp 6 - Toán.docx`, chữ NLS màu Xanh và chữ NLAI màu Tím nổi bật, chuẩn mực.

## Tiêu chí nghiệm thu
1. Cấu trúc hình thức tổng thể của file xuất ra khớp 100% với file mẫu `Phụ lục 1 - Lớp 6 - Toán.docx`.
2. Bảng PPCT giữ nguyên 100% các cột và dữ liệu của người dùng, chỉ bổ sung thêm 01 cột duy nhất ở cuối: `Mã NLS & AI (CV 3456 & QĐ 2422)`.
3. Giáo viên có thể tick chọn đích danh 12 tiết AI; AI chỉ sinh mã AI cho các tiết đã chọn.
4. File Word xuất ra và Preview thể hiện rõ: NLS Màu Xanh (`0070C0`), NLAI Màu Tím (`7030A0`).
5. Toàn bộ smoke test tự động đều PASS 100%.
