# PLAN: Chuẩn Hóa Riêng Biệt Cột Cho Phụ Lục 1 (Có YCCĐ) và Phụ Lục 3 (Tiết CT, Tuần, Thiết Bị, Địa Điểm Không YCCĐ), Tích Hợp Lọc SGK Tinh Gọn, Chọn 12 Tiết AI và Định Dạng Màu Sắc (NLS Xanh - NLAI Tím)

## Hiện trạng
1. **Thống Nhất Biểu Mẫu Chuẩn Theo Đúng Từng Phụ Lục (CV 5512)**:
   - **Phụ lục 1 (Khung kế hoạch dạy học của Tổ chuyên môn)**:
     * Cấu trúc bảng PPCT chuẩn khớp 100% file mẫu `Phụ lục 1 - Lớp 6 - Toán.docx`:
       $$\text{STT} \;\vert\; \text{Bài học} \;\vert\; \text{Số tiết} \;\vert\; \mathbf{\text{Yêu cầu cần đạt}} \;\vert\; \mathbf{\text{Mã NLS \& AI (CV 3456 \& QĐ 2422)}}$$
     * Có đầy đủ 6 phần hành chính: Tiêu ngữ 2 cột, Căn cứ CV 5512, Mục I.1-I.4 (Bảng Thiết bị TT 38, Bảng Phòng TT 14), Mục II.1-II.3 (Bảng PPCT + Cột NLS/AI, Bảng Chuyên đề, Bảng KTĐG 4 mốc), Mục III, và Bảng Chữ ký (Tổ trưởng & Hiệu trưởng).
   - **Phụ lục 3 (Kế hoạch giáo dục của Giáo viên)**:
     * Cấu trúc bảng PPCT chuẩn khớp 100% theo ảnh mẫu người dùng cung cấp (không có cột YCCĐ để bảng thoáng đẹp, chuẩn A4):
       $$\text{Bài học} \;\vert\; \text{Số tiết} \;\vert\; \text{Tiết CT} \;\vert\; \text{Tuần} \;\vert\; \text{Thiết bị dạy học (*)} \;\vert\; \text{Địa điểm dạy học (**)} \;\vert\; \mathbf{\text{Mã NLS \& AI (CV 3456 \& QĐ 2422)}}$$
     * Có đầy đủ chú thích `(*)` TT 38, `(**)` TT 14 và chữ ký phê duyệt 2 bên (Giáo viên & Tổ trưởng duyệt).
2. **Khắc Phục Triệt Để Lỗi Bóc Tách Bảng Nguồn**:
   - Khi tải file lên, hệ thống tách riêng từng bảng độc lập, loại trừ bảng hành chính (`TRƯỜNG THCS...`), chỉ bóc tách đúng các dòng bài học vào bảng PPCT.
3. **Bộ Lọc Sư Phạm Tinh Gọn Khi Tải SGK (Smart Pedagogical Indexing)**:
   - Khi tải tệp SGK (PDF/DOCX ~150–200 trang), hệ thống tự động bóc tách các đề mục trọng tâm: `Tên bài` + `Mục tiêu cần đạt` + `Hoạt động khám phá / luyện tập / vận dụng` $\rightarrow$ Giảm 95% token (từ 140k xuống 5k–8k token), giúp AI hiểu sâu nội dung từng bài trong bộ sách mà siêu tiết kiệm Quota và chạy siêu nhanh (2–3 giây).
4. **Bảng Chọn Tiết AI Chủ Động (Tick 12 Tiết Trọng Tâm)**:
   - Giáo viên có thể tick chọn chính xác 12 tiết trọng tâm trên bảng PPCT (kèm nút gợi ý 12 tiết chuẩn về Hình học, Thống kê, Trải nghiệm); AI chỉ sinh mã AI cho các tiết đã tick.
5. **Phân Biệt Màu Sắc Xuất Bản**:
   - Web Preview và file Word `.docx` phân biệt rõ 2 màu:
     + Mã Năng lực số (NLS): Chữ **Màu Xanh** (`0070C0`).
     + Mã Năng lực AI (NLAI): Chữ **Màu Tím** (`7030A0`).
6. **Thanh Tiến Trình Thời Gian Thực (% Floating Progress Bar)**:
   - Khi đạt 100%: Dừng spinner, hiển thị tích xanh `✓`, thông báo hoàn tất và tự động ẩn mượt mà sau 1.5 giây; có nút đóng `✕`.

## Phạm vi
1. **Phân Định Cột Bảng Độc Lập Cho Phụ Lục 1 và Phụ Lục 3**:
   - **Phụ lục 1**: `STT`, `Bài học`, `Số tiết`, `Yêu cầu cần đạt`, `Mã NLS & AI (CV 3456 & QĐ 2422)`.
   - **Phụ lục 3**: `Bài học`, `Số tiết`, `Tiết CT`, `Tuần`, `Thiết bị dạy học (*)`, `Địa điểm dạy học (**)`, `Mã NLS & AI (CV 3456 & QĐ 2422)`.
2. **Trình Bóc Tách Bảng Thông Minh & Lọc SGK Tinh Gọn**:
   - Bóc tách độc lập Bảng PPCT, Bảng Thiết bị, Bảng Phòng bộ môn, Bảng KTĐG; bỏ qua bảng hành chính.
   - Trích xuất cấu trúc các bài học và hoạt động chính từ tệp SGK làm ngữ cảnh sư phạm cho Gemini AI.
3. **Cột Tick Chọn Tiết AI Trên Giao Diện PPCT**:
   - Hiển thị danh sách bài học kèm checkbox `Chọn AI`, thanh đếm `Đã chọn: X/12 tiết` và nút `Gợi ý 12 tiết chuẩn`.
   - Siêu Prompt Gemini AI chỉ điền mã `[AI: ...]` vào các bài có `aiSelected: true`.
4. **Bộ Xuất Word (.docx) & Web Preview 2 Màu Chuẩn Hình Thức File Mẫu**:
   - Tái lập đầy đủ cấu trúc 6 phần chuẩn theo `Phụ lục 1 - Lớp 6 - Toán.docx`.
   - Xuất riêng từng đoạn TextRun: NLS Màu Xanh (`0070C0`), NLAI Màu Tím (`7030A0`).
5. **Bộ Kiểm thử Tự động ([tests/xaydungphuluc-smoke.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/tests/xaydungphuluc-smoke.js))**:
   - Cập nhật bài test kiểm tra cấu trúc cột chuẩn riêng cho Phụ lục 1 và Phụ lục 3, bóc tách bảng độc lập, chọn 12 tiết AI và xuất Word 2 màu.

## Ngoài phạm vi
- Không can thiệp các file ngoài `xaydungphuluc.html` và file test liên quan.

## File dự kiến tác động
- `xaydungphuluc.html` [PHÂN ĐỊNH CỘT CHUẨN PL1 CÓ YCCĐ / PL3 CÓ TIẾT CT-TUẦN-THIẾT BỊ-ĐỊA ĐIỂM, BỘ LỌC SGK, CHỌN 12 TIẾT AI, MÀU NLS XANH / AI TÍM, CHUẨN HÓA DOCX]
- `tests/xaydungphuluc-smoke.js` [CẬP NHẬT SMOKE TEST]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Cấu Hình Danh Mục Cột Riêng Biệt Cho Từng Phụ Lục trong `xaydungphuluc.html`**:
   - Phụ lục 1: `[['stt','STT'],['lesson','Bài học'],['periods','Số tiết'],['outcomes','Yêu cầu cần đạt'],['integration','Mã NLS & AI (CV 3456 & QĐ 2422)']]`.
   - Phụ lục 3: `[['lesson','Bài học'],['periods','Số tiết'],['tietCT','Tiết CT'],['week','Tuần'],['devices','Thiết bị dạy học (*)'],['location','Địa điểm dạy học (**)'],['integration','Mã NLS & AI (CV 3456 & QĐ 2422)']]`.
2. **Bước 2: Nâng Cấp Bộ Bóc Tách Bảng Độc Lập & Bộ Lọc SGK**:
   - Tách riêng các bảng khi đọc file tải lên; lọc nội dung SGK tinh gọn (mục tiêu & hoạt động chính).
3. **Bước 3: Bổ Sung Vùng Chọn Tiết AI Trên Biểu Mẫu**:
   - Checkbox `aiSelected` cho từng dòng bài học, thanh đếm 12 tiết và nút gợi ý 12 tiết chuẩn.
4. **Bước 4: Nâng Cấp Siêu Prompt Gemini AI**:
   - Phụ lục 1: Sinh đủ cột `Yêu cầu cần đạt` + `Mã NLS & AI`.
   - Phụ lục 3: Giữ nguyên các cột của người dùng (`Tiết CT`, `Tuần`, `Thiết bị`, `Địa điểm`) + Sinh `Mã NLS & AI` (cho đúng các tiết đã chọn AI).
5. **Bước 5: Nâng Cấp Trình Xuất Word (.docx) & Web Preview 2 Màu**:
   - Xuất đầy đủ 6 phần khớp 100% với file mẫu `Phụ lục 1 - Lớp 6 - Toán.docx`.
   - Phân biệt màu sắc: NLS Màu Xanh (`0070C0`), NLAI Màu Tím (`7030A0`).
6. **Bước 6: Cập nhật và chạy kiểm thử tự động**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`, xác nhận PASS 100%.

## Tiêu chí nghiệm thu
1. Phụ lục 1 có đầy đủ cột `Yêu cầu cần đạt` và cột `Mã NLS & AI` theo đúng chuẩn CV 5512 và file mẫu `Phụ lục 1 - Lớp 6 - Toán.docx`.
2. Phụ lục 3 có đầy đủ các cột `Bài học`, `Số tiết`, `Tiết CT`, `Tuần`, `Thiết bị dạy học (*)`, `Địa điểm dạy học (**)`, và `Mã NLS & AI` theo đúng mẫu ảnh chụp của người dùng.
3. Giáo viên có thể tick chọn đích danh 12 tiết AI; AI chỉ sinh mã AI cho các tiết đã chọn.
4. File Word xuất ra và Preview thể hiện rõ: NLS Màu Xanh (`0070C0`), NLAI Màu Tím (`7030A0`).
5. Toàn bộ smoke test tự động đều PASS 100%.
