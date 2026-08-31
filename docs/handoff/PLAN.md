# PLAN: Phân Tách 2 Giai Đoạn Rõ Ràng: (1) AI Đọc File PDF/DOCX Đẩy Bảng PPCT Lên Màn Hình Để Tick Chọn 12 Tiết AI $\rightarrow$ (2) Bấm Sinh Mới Bù Đắp YCCĐ & Tích Hợp NLS/AI Xuất Word 2 Màu

## Hiện trạng & Phân Định Rạch Ròi 2 Giai Đoạn Nghiệp Vụ

### Giai Đoạn 1: Nạp File $\rightarrow$ AI Nhận Diện Bảng PPCT Gốc $\rightarrow$ Đẩy Lên Màn Hình Để Tick Chọn 12 Tiết AI
- **Hành động của giáo viên**: Tải file PPCT (PDF, DOCX, XLSX) lên ở Mục 2.
- **Hành động của AI & Hệ thống**:
  1. AI (Gemini/Mistral) đọc toàn bộ nội dung file PDF/DOCX được gửi lên.
  2. AI trích xuất **chính xác và đầy đủ toàn bộ bảng phân phối chương trình theo đúng file gốc** (Tên bài học, Số tiết, Tiết CT, Tuần, Thiết bị dạy học, Địa điểm dạy học).
  3. Đẩy ngay bảng PPCT này ra màn hình Mục 3 (dạng Table View 8 cột).
  4. Giáo viên nhìn thấy toàn bộ bảng PPCT từ file của mình; có thể chỉnh sửa số tiết trực tiếp và **tick chọn 12 tiết tích hợp Khung năng lực AI (QĐ 2422)** (kèm bộ đếm `🎯 Đã chọn: X/12 tiết AI` và nút `✨ Gợi ý 12 tiết chuẩn`).

---

### Giai Đoạn 2: Bấm "⚡ Sinh Trọn Bộ Phụ Lục (1, 2, 3)" $\rightarrow$ Lúc Này Mới Bù Đắp & Tích Hợp
- **Hành động của giáo viên**: Sau khi đã tick chọn xong các tiết AI, bấm nút **⚡ Sinh trọn bộ Phụ lục**.
- **Hành động của AI & Hệ thống**:
  1. **Tích hợp Năng Lực Số (NLS) & Trí Tuệ Nhân Tạo (AI)**:
     - Tích hợp NLS (CV 3456) tự động theo tỷ lệ (%) và mật độ cấu hình.
     - Tích hợp AI (QĐ 2422) **chính xác vào đúng các tiết mà giáo viên đã tick chọn ở Giai đoạn 1**.
  2. **Bù đắp & Hoàn thiện Phụ lục 1 (Tổ chuyên môn)**:
     - Lấy danh sách Bài học & Số tiết từ bảng PPCT $\rightarrow$ AI tự động **viết và bù đắp đầy đủ cột `Yêu cầu cần đạt` (outcomes) chuẩn Chương trình GDPT 2018**.
     - Tự động hoàn thiện Mục I (Thiết bị tối thiểu TT 38/2021, Phòng bộ môn TT 14/2020), Kiểm tra đánh giá định kỳ (GK1 Tuần 9, CK1 Tuần 18, GK2 Tuần 27, CK2 Tuần 35) và Mục III Nội dung khác.
  3. **Hoàn thiện Phụ lục 2 (Hoạt động giáo dục)**:
     - Tự sinh 4–6 hoạt động STEM/STEAM, CLB, trải nghiệm có tích hợp NLS và AI.
  4. **Hoàn thiện Phụ lục 3 (Giáo viên)**:
     - Giữ nguyên vẹn 100% các cột bảng tiến độ PPCT gốc của giáo viên + nối thêm đúng 01 cột cuối `Mã NLS & AI (CV 3456 & QĐ 2422)`.
  5. **Xuất Word (.docx) & Xem Trước 2 Màu Chuẩn Mực**:
     - **Mã NLS Màu Xanh (`0070C0`)** và **Mã NLAI Màu Tím (`7030A0`)**.
     - Cấu trúc tài liệu đầy đủ 6 phần chuẩn theo file mẫu [Phụ lục 1 - Lớp 6 - Toán.docx](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/GIAO%20AN/XAYDUNGPHULUC/Ph%E1%BB%A5%20l%E1%BB%A5c%201%20-%20L%E1%BB%9Bp%206%20-%20To%C3%A1n.docx).

## Phạm vi Kỹ Thuật trong `xaydungphuluc.html`
1. **Hàm Gọi AI Nhận Diện PPCT Khi Tải File (`recognizePpctWithAi(text)`)**:
   - Khi người dùng tải file PPCT PDF/DOCX: Đọc text thô và gọi AI trích xuất trung thực bảng PPCT nguồn sang cấu trúc JSON `{ ppct: [{ lesson, periods, tietCT, week, devices, location, isHeader }] }`.
   - Nạp vào hệ thống và hiển thị ngay ra bảng Mục 3 (`updateAiPicker()`).
2. **Giao Diện Bảng Biểu Phụ Lục 3 Mục 3 (Table View 8 Cột)**:
   - Cột 1..7: `STT | Bài học | Số tiết | Tiết CT | Tuần | Thiết bị | Địa điểm`.
   - Cột 8: Checkbox chọn từng tiết (`Tiết 1`, `Tiết 2`...) để giáo viên tick chọn 12 tiết AI.
   - Sửa số tiết trực tiếp trên ô input $\rightarrow$ tự động mở rộng/thu gọn checkbox tiết con.
3. **Quá Trình Sinh Phụ Lục Khi Bấm Nút (Giai Đoạn 2)**:
   - Phụ lục 1: AI tự động sinh cột `outcomes` chuẩn GDPT 2018.
   - Phụ lục 3: Nối cột `integration` (chỉ xuất mã AI cho đúng các tiết đã tick).
   - Xuất Word 2 màu NLS Xanh `0070C0` / NLAI Tím `7030A0`.

## File tác động
- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/.lock`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/VERIFY.md`

## Các bước thực hiện
1. **Bước 1**: Cập nhật `parseFiles` trong `xaydungphuluc.html` để khi tải file PDF/DOCX sẽ gọi AI nhận diện toàn bộ bảng PPCT gốc và render ngay ra bảng 8 cột Mục 3.
2. **Bước 2**: Giữ nguyên tương tác chỉnh sửa số tiết và tick chọn 12 tiết AI tại Mục 3.
3. **Bước 3**: Khi bấm Sinh trọn bộ Phụ lục $\rightarrow$ AI tiến hành bù đắp YCCĐ cho Phụ lục 1 và tích hợp mã NLS Xanh / AI Tím.
4. **Bước 4**: Cập nhật và chạy kiểm thử tự động `node tests/xaydungphuluc-smoke.js` xác nhận PASS 100%.

## Tiêu chí nghiệm thu
1. Giai đoạn 1: File PDF/DOCX tải lên được AI đọc và đẩy toàn bộ bảng PPCT gốc lên màn hình Mục 3 (Table View 8 cột) để giáo viên tick chọn 12 tiết AI.
2. Giai đoạn 2: Khi bấm Sinh Phụ lục, AI mới tiến hành bù đắp YCCĐ cho Phụ lục 1 và tích hợp mã NLS/AI vào đúng các tiết đã chọn.
3. Xuất Word (.docx) phân biệt rõ ràng 2 màu: NLS Xanh (`0070C0`) và NLAI Tím (`7030A0`).
4. Toàn bộ smoke test tự động đều PASS 100%.
