# PLAN: Thiết Kế Trực Quan Vùng Nhận Diện PPCT, Nút Import SGK PDF Riêng Biệt, Bảng Tick Chọn 12 Tiết AI Luôn Hiển Thị & Định Dạng Màu Sắc NLS Xanh - NLAI Tím

## Hiện trạng
1. **Vấn Đề Giao Diện Người Dùng (UI/UX)**:
   - Thẻ chọn tiết AI (`#aiLessonPickerCard`) trước đây bị ẩn mặc định (`hidden`) và chỉ kích hoạt sau khi upload file có chứa PPCT. Do đó, người dùng mở trang không thấy nút nhận diện PPCT, không thấy nút tải riêng SGK PDF, và không thấy bảng tick chọn 12 tiết AI ở đâu.
   - Khu vực tải file chỉ có 1 nút upload chung chung, không phân định rõ ràng giữa **Tệp Phân phối chương trình** và **Tệp Sách giáo khoa (PDF/DOCX)**.
2. **Kỳ Vọng Của Giáo Viên**:
   - Có nút **🔍 Nhận diện cấu trúc PPCT** (hoặc tự động nạp cấu trúc bài học ngay khi chọn Môn / Lớp hoặc tải file).
   - Có nút riêng **📚 Tải tệp Sách Giáo Khoa (PDF/DOCX)** để nạp ngữ cảnh SGK tinh gọn.
   - Bảng phân phối chương trình kèm **cột checkbox "Tích hợp AI" trên từng bài học** luôn hiển thị rõ ràng, kèm bộ đếm `Đã chọn: X/12 tiết` và nút `✨ Gợi ý 12 tiết chuẩn`.
   - Xuất Word và Preview hiển thị rõ ràng 2 màu: **Mã NLS Màu Xanh (`0070C0`)** và **Mã NLAI Màu Tím (`7030A0`)**.
   - Cơ chế liên thông tự sinh cột `Yêu cầu cần đạt` cho Phụ lục 1 khi người dùng nạp Phụ lục 3.

## Phạm vi
1. **Thiết Kế Lại Khu Vực Nạp Dữ Liệu & Nhận Diện PPCT (Mục 2 Trên Giao Diện)**:
   - Chia thành 2 ô nạp tài liệu riêng biệt, trực quan:
     * **Ô 1**: `📄 Tải lên Phân phối chương trình (DOCX, XLSX, PDF)` $\rightarrow$ Nhận diện ngay toàn bộ cấu trúc bài học.
     * **Ô 2**: `📚 Tải lên Sách Giáo Khoa (PDF, DOCX)` $\rightarrow$ Bóc tách ngữ cảnh SGK tinh gọn (giảm 95% token).
   - Thêm nút: `🔍 Nạp cấu trúc PPCT chuẩn theo Môn & Lớp` (cho phép giáo viên xem và tick chọn 12 tiết AI ngay lập tức kể cả khi chưa có sẵn file để tải lên).
2. **Bảng Tick Chọn Tiết AI Luôn Hiển Thị (Mục 3 Trên Giao Diện)**:
   - Luôn hiển thị danh sách bài học của PPCT (nguồn tải lên hoặc mẫu chuẩn theo môn/lớp) với cột checkbox `Chọn AI (tối đa 12 tiết)`.
   - Thanh công cụ trên đầu bảng:
     * Bộ đếm nổi bật: `🎯 Đã chọn: X/12 tiết AI`.
     * Nút `✨ Gợi ý 12 tiết chuẩn (Hình học, Thống kê, Trải nghiệm)`.
     * Nút `✕ Bỏ chọn tất cả`.
3. **Phân Biệt 2 Màu Sắc Khi Xuất Bản**:
   - Web Preview và file Word `.docx` xuất bản:
     * Mã NLS: Chữ **Màu Xanh** (`0070C0`).
     * Mã NLAI: Chữ **Màu Tím** (`7030A0`).
4. **Cơ Chế Liên Thông Phụ Lục 1 - Phụ Lục 3**:
   - Nạp file Phụ lục 3 $\rightarrow$ AI tự động sinh `outcomes` chuẩn GDPT 2018 cho Phụ lục 1, và bảo toàn nguyên vẹn bảng tiến độ cho Phụ lục 3.
5. **Cập Nhật Bộ Kiểm Thử Tự Động ([tests/xaydungphuluc-smoke.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/tests/xaydungphuluc-smoke.js))**:
   - Kiểm tra sự hiện diện của nút nạp SGK riêng, nút nhận diện PPCT, bảng tick chọn AI luôn sẵn sàng, và xuất Word 2 màu.

## Ngoài phạm vi
- Không can thiệp các trang khác ngoài `xaydungphuluc.html` và file test liên quan.

## File dự kiến tác động
- `xaydungphuluc.html` [THIẾT KẾ LẠI GIAO DIỆN NẠP PPCT/SGK RIÊNG BIỆT, NÚT NHẬN DIỆN PPCT, BẢNG TICK CHỌN 12 TIẾT AI LUÔN HIỂN THỊ, XUẤT WORD 2 MÀU]
- `tests/xaydungphuluc-smoke.js` [CẬP NHẬT SMOKE TEST]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Nâng Cấp Giao Diện Nạp Dữ Liệu trong `xaydungphuluc.html`**:
   - Bố trí 2 thẻ tải file song song: `📄 Tải PPCT` và `📚 Tải SGK PDF/Word`.
   - Thêm nút `🔍 Nạp cấu trúc PPCT mẫu theo Môn & Lớp` để khởi tạo danh sách bài học ngay lập tức.
2. **Bước 2: Mở Khóa Bảng Tick Chọn 12 Tiết AI Luôn Hoạt Động**:
   - Loại bỏ class `hidden` khỏi vùng chọn AI, tự động nạp danh sách bài học mặc định của môn Toán 6 (hoặc môn đang chọn) khi vừa mở trang.
   - Thêm checkbox trên từng dòng bài học, thanh đếm `X/12 tiết` và nút gợi ý 12 tiết chuẩn.
3. **Bước 3: Tích Hợp Cơ Chế Lọc SGK & Siêu Prompt Gemini**:
   - Gắn ngữ cảnh SGK tinh gọn vào prompt.
   - AI chỉ sinh mã `[AI: ...]` vào đúng các bài học được tick chọn.
4. **Bước 4: Xuất DOCX và Preview Phân Tách 2 Màu Xanh (`0070C0`) và Tím (`7030A0`)**:
   - Tái lập đầy đủ 6 phần chuẩn theo `Phụ lục 1 - Lớp 6 - Toán.docx`.
5. **Bước 5: Cập nhật và chạy kiểm thử tự động**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`, xác nhận PASS 100%.

## Rủi ro
- **Rủi ro**: Giáo viên đổi môn học hoặc khối lớp sau khi đã chọn file/tick AI.
  - *Giải pháp*: Tự động cập nhật lại danh sách bài học tương ứng với môn học/khối lớp mới và giữ trải nghiệm mượt mà.

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy `node tests/xaydungphuluc-smoke.js`:
     + Xác nhận giao diện có nút tải PPCT, nút tải SGK riêng biệt, nút nhận diện PPCT.
     + Xác nhận bảng tick chọn AI hiển thị ngay khi mở trang.
     + Xác nhận xuất Word có mã màu `0070C0` (NLS) và `7030A0` (NLAI).
2. **Kiểm thử thủ công trên trình duyệt**:
   - Mở `xaydungphuluc.html` $\rightarrow$ Thấy ngay 2 ô nạp (PPCT và SGK), thấy ngay bảng danh sách bài học có checkbox tick chọn AI.
   - Bấm `Gợi ý 12 tiết chuẩn` $\rightarrow$ Bộ đếm nhảy `12/12 tiết`.
   - Bấm `⚡ Sinh trọn bộ Phụ lục` $\rightarrow$ Sinh đúng 12 bài có mã AI màu Tím, các bài còn lại có mã NLS màu Xanh.

## Tiêu chí nghiệm thu
1. Giao diện có nút tải PPCT riêng, nút tải SGK PDF riêng và nút nhận diện PPCT từ môn/lớp.
2. Bảng tick chọn 12 tiết AI luôn hiển thị sẵn sàng, trực quan, có bộ đếm và nút gợi ý 12 tiết chuẩn.
3. File Word xuất ra và Preview phân biệt rõ: NLS Màu Xanh (`0070C0`), NLAI Màu Tím (`7030A0`).
4. Toàn bộ smoke test tự động đều PASS 100%.
