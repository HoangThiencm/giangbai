# PLAN: Nạp File Phụ Lục 3 $\rightarrow$ Đọc & Hiển Thị Toàn Bộ Bảng PPCT Chính Xác Lên Hệ Thống $\rightarrow$ Tick Chọn 12 Tiết Tích Hợp Khung Năng Lực AI $\rightarrow$ Sinh & Xuất Trọn Bộ Word 2 Màu

## Hiện trạng & Yêu Cầu Cốt Lõi
- **Quy Trình Chuẩn Sư Phạm 100% Khép Kín**:
  1. **Nạp Tệp Phụ Lục 3**:
     - Giáo viên tải file Phụ lục 3 (DOCX, XLSX, PDF) lên ở Mục 2.
  2. **Đọc & Hiển Thị Toàn Bộ Bảng Phụ Lục 3 Lên Hệ Thống Chính Xác 100%**:
     - Hệ thống bóc tách và hiển thị ngay toàn bộ bảng phân phối chương trình nguồn lên giao diện:
       * Cột `Bài học` (Tên bài học thật).
       * Cột `Số tiết` (Số tiết thật: 1 tiết, 2 tiết, 3 tiết... cho phép tăng/giảm nếu cần).
       * Cột `Tiết CT` (Tiết thứ mấy trong chương trình).
       * Cột `Tuần` (Tuần thực hiện).
       * Cột `Thiết bị dạy học` & `Địa điểm dạy học`.
  3. **Tích Hợp Khung Năng Lực AI (QĐ 2422) Qua Checkbox Trực Tiếp**:
     - Hiển thị checkbox tick chọn trên từng tiết/bài học để giáo viên **tick chọn chính xác 12 tiết tích hợp Khung năng lực AI (QĐ 2422)**.
     - Có bộ đếm trực quan `🎯 Đã chọn: X/12 tiết AI` kèm nút `✨ Gợi ý 12 tiết chuẩn` và `✕ Bỏ chọn tất cả`.
     - Khung Năng lực số (NLS - CV 3456) được tích hợp tự động theo tỷ lệ (%) và mật độ đã cấu hình.
  4. **Sinh Phụ Lục & Xuất Word (.docx) 2 Màu**:
     - Bấm **⚡ Sinh trọn bộ Phụ lục**:
       * *Phụ lục 3 (Giáo viên)*: Bảo toàn 100% toàn bộ bảng nguồn người dùng đã tải lên + bổ sung đúng 01 cột cuối: `Mã NLS & AI (CV 3456 & QĐ 2422)`.
       * *Phụ lục 1 (Tổ chuyên môn)*: Lấy danh sách bài học và số tiết từ Phụ lục 3 $\rightarrow$ AI tự động sinh đầy đủ cột `Yêu cầu cần đạt` chuẩn Chương trình GDPT 2018.
       * File Word xuất ra và Preview thể hiện rõ 2 màu: **Mã NLS Màu Xanh (`0070C0`)** và **Mã NLAI (AI) Màu Tím (`7030A0`)**, đủ 6 phần chuẩn theo file mẫu `Phụ lục 1 - Lớp 6 - Toán.docx`.

## Phạm vi Kỹ Thuật trong `xaydungphuluc.html`
1. **Hiển Thị Toàn Bộ Bảng PPCT Nhận Diện Lên Giao Diện (Mục 3)**:
   - Khi tải file Phụ lục 3: Render toàn bộ danh sách các bài học với đầy đủ thông tin (Tên bài, Số tiết, Tiết CT, Tuần, Thiết bị, Địa điểm) kèm các checkbox chọn tiết AI (`Tiết 1`, `Tiết 2`... `Tiết N`) tương ứng đúng số tiết của bài.
   - Khi chưa tải file: Hiển thị khung chờ thông báo tải file Phụ lục 3 (hoặc nút nạp thử mẫu Toán 6).
2. **Bóc Tách Số Tiết Đa Kênh Chuẩn Xác**:
   - Xử lý sạch các định dạng `"(2 tiết)"`, `"[3 tiết]"`, `"2 tiết"`, khoảng `"1-3"`, `"1, 2"`.
   - Cho phép giáo viên chỉnh sửa tăng/giảm số tiết trực tiếp trên ô input của từng bài.
3. **Liên Thông Sinh Phụ Lục 1 Tự Động Từ Phụ Lục 3**:
   - Phụ lục 1 tự sinh `outcomes` chuẩn GDPT 2018; Phụ lục 3 giữ nguyên bảng nguồn; AI chỉ sinh mã AI cho đúng các tiết đã tick.
4. **Bộ Xuất DOCX 2 Màu**:
   - Tách riêng từng TextRun: NLS Xanh `0070C0` và NLAI Tím `7030A0`.

## File tác động
- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/.lock`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/VERIFY.md`

## Các bước thực hiện
1. Triển khai hiển thị toàn bộ bảng PPCT nhận diện từ file Phụ lục 3 tải lên kèm checkbox chọn 12 tiết AI.
2. Hoàn thiện bộ bóc tách số tiết đa kênh và cho phép tăng/giảm số tiết.
3. Cập nhật và chạy smoke test `node tests/xaydungphuluc-smoke.js` xác nhận PASS 100%.

## Tiêu chí nghiệm thu
1. Tải file Phụ lục 3 lên $\rightarrow$ Đọc và hiển thị toàn bộ bảng PPCT chính xác 100% lên hệ thống kèm checkbox tick chọn 12 tiết AI.
2. Cho phép giáo viên tăng/giảm số tiết trực tiếp trên từng bài; checkbox tiết tự động cập nhật tương ứng.
3. Xuất Word giữ nguyên bảng Phụ lục 3 nguồn, tự sinh YCCĐ cho Phụ lục 1, phân biệt 2 màu NLS Xanh và NLAI Tím.
4. Toàn bộ smoke test tự động đều PASS 100%.
