# VERIFY: Nghiệm thu Phân Tách 2 Giai Đoạn (AI Nhận Diện Bảng PPCT Trước, Bù Đắp YCCĐ & Tích Hợp Sau) Và Table View 8 Cột

## Kết luận
PASS

## Đối chiếu scope
1. **Giai Đoạn 1: Nạp File $\rightarrow$ AI Nhận Diện Toàn Bộ Bảng PPCT Gốc $\rightarrow$ Đẩy Lên Màn Hình**:
   - Khi tải file PDF/DOCX: `parseFiles()` gọi `recognizePpctWithAi(text)` sử dụng prompt `ppctRecognitionPrompt`.
   - AI đọc văn bản file gốc và trích xuất cấu trúc JSON `{ ppct: [{ lesson, periods, tietCT, week, devices, location, isHeader }] }` trung thực theo file gửi lên.
   - Không gọi prompt sinh YCCĐ, NLS hay AI ở giai đoạn này.
   - Đẩy trực tiếp bảng PPCT nhận diện lên Mục 3 dưới dạng Bảng 8 cột (Table View) có checkbox từng tiết con để giáo viên tick chọn 12 tiết AI.
2. **Giai Đoạn 2: Bấm Sinh Phụ Lục $\rightarrow$ Lúc Này Mới Bù Đắp & Tích Hợp**:
   - Khi người dùng bấm **⚡ Sinh trọn bộ Phụ lục**:
     * AI sinh mã NLS (CV 3456) tự động và sinh mã AI (QĐ 2422) chính xác vào đúng 12 tiết đã tick ở Giai đoạn 1.
     * Phụ lục 1: AI tự động viết và bù đắp đầy đủ cột `Yêu cầu cần đạt` chuẩn CT GDPT 2018; tự hoàn thiện Thiết bị (TT 38), Phòng bộ môn (TT 14), Kiểm tra đánh giá (4 mốc).
     * Phụ lục 3: Bảo toàn bảng PPCT nguồn + bổ sung đúng 1 cột cuối `Mã NLS & AI`.
3. **Hiển Thị Bảng Mục 3 (Table View 8 Cột)**:
   - Đầy đủ 8 cột: `STT | Bài học | Số tiết | Tiết CT | Tuần | Thiết bị | Địa điểm | Tích hợp AI (QĐ 2422)`.
   - Dòng tiêu đề chương gộp đủ `colspan="8"` in đậm.
   - Sửa số tiết trực tiếp trên ô input $\rightarrow$ mở rộng/thu gọn checkbox tiết con tương ứng.
4. **Xuất Word 2 Màu**:
   - NLS Màu Xanh (`0070C0`) và NLAI Màu Tím (`7030A0`), đầy đủ 6 phần chuẩn theo `Phụ lục 1 - Lớp 6 - Toán.docx`.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` $\rightarrow$ PASS (kiểm tra recognizer Giai đoạn 1, tách riêng prompt nhận diện và prompt sinh phụ lục, 8 cột table view, sửa số tiết, xuất Word 2 màu).
- `node tests/xaydungphuluc-integration-smoke.js` $\rightarrow$ PASS.
- Kiểm tra cú pháp JavaScript nội tuyến của `xaydungphuluc.html` qua `node --check` $\rightarrow$ PASS 100%.

## Pass / Fail từng tiêu chí
1. Tải file PPCT (PDF/DOCX) $\rightarrow$ AI đọc và đẩy toàn bộ bảng PPCT gốc lên màn hình Mục 3 $\rightarrow$ **PASS**.
2. Giai đoạn nạp file không bị gọi lẫn prompt sinh YCCĐ / NLS / AI $\rightarrow$ **PASS**.
3. Checkbox tick chọn 12 tiết AI và chỉnh sửa số tiết trực quan trên bảng 8 cột $\rightarrow$ **PASS**.
4. Khi bấm Sinh Phụ lục: AI mới bù đắp YCCĐ cho Phụ lục 1 và gắn mã NLS/AI vào đúng tiết đã chọn $\rightarrow$ **PASS**.
5. Xuất Word & Preview 2 màu (NLS Xanh `0070C0` - NLAI Tím `7030A0`) $\rightarrow$ **PASS**.

## Bug
- Không có lỗi tồn đọng.
