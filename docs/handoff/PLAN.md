# PLAN: Khắc Phục Triệt Để Lỗi Bóc Tách Bảng PPCT (Không Trộn Header Hành Chính Vào Bảng), Phân Định Chính Xác Bảng PPCT Nguồn và Định Dạng Preview/Docx 7 Cột Chuẩn

## Hiện trạng
1. **Phân tích Nguyên nhân Lỗi Nghiêm Trọng trong Ảnh Chụp Người Dùng (`media_1788150427146.png`)**:
   - Khi người dùng tải file Word/Excel/PDF lên (ví dụ `Phụ lục 1 - Lớp 6 - Toán.docx` hoặc file PPCT đầy đủ), tài liệu chứa nhiều bảng và văn bản hành chính khác nhau:
     + Bảng 1: Thông tin hành chính (`UBND XÃ... TRƯỜNG THCS TRẦN PHÚ... Quốc hiệu - Tiêu ngữ...`)
     + Bảng 2: Thiết bị dạy học (`STT | Thiết bị | Số lượng | Bài thực hành | Ghi chú`)
     + Bảng 3: Phòng học bộ môn (`STT | Tên phòng | Số lượng | Phạm vi sử dụng | Ghi chú`)
     + Bảng 4: **Phân phối chương trình (PPCT)** (`STT | Bài học | Số tiết | ...`)
     + Bảng 5: Kiểm tra đánh giá (`Bài KTĐG | Thời gian | Thời điểm | ...`)
     + Bảng 6: Chữ ký phê duyệt (`TỔ TRƯỞNG | HIỆU TRƯỞNG`)
   - Hàm `parseFiles()` và `extractPpctRows()` trong [xaydungphuluc.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/xaydungphuluc.html) trước đây gộp toàn bộ text của tất cả các bảng vào một chuỗi thô rồi quét theo từng dòng.
   - Hậu quả: Bảng 1 (Thông tin hành chính `TRƯỜNG THCS TRẦN PHÚ...`) và văn bản mở đầu bị hiểu nhầm là dòng Bài học số 1 của PPCT! Đoạn văn bản dài hàng nghìn ký tự bị nhồi vào cột `Bài học` và `Số tiết`, làm vỡ nát toàn bộ bảng xem trước, đẩy các cột `Tiết CT`, `Tuần`, `Thiết bị`, `Địa điểm`, `Mã NLS & AI` ra khỏi màn hình như trong ảnh chụp của người dùng.

## Phạm vi
1. **Thuật Toán Bóc Tách Bảng Thông Minh & Phân Định Độc Lập Các Bảng Trong File Nguồn**:
   - Khi đọc file `.docx` (qua `mammoth.convertToHtml`), `.xlsx` (qua `XLSX.utils.sheet_to_json`), `.pdf`, `.txt`:
     + **Tách riêng từng bảng HTML/Sheet độc lập**, không gộp chung vào một chuỗi thô.
     + **Nhận diện đúng Bảng PPCT**: Bảng nào có header chứa `Bài học` / `Tên bài` / `Tiết CT` / `Tuần` / `Nội dung dạy học` mới được bóc tách làm `sourcePpctRows`.
     + **Tuyệt đối loại trừ Bảng Hành chính**: Bảng chứa `UBND`, `TRƯỜNG`, `CỘNG HÒA XÃ HỘI`, `TỔ TRƯỞNG`, `HIỆU TRƯỞNG` chỉ dùng để điền tự động vào các ô thông tin trường lớp, không bao giờ được đưa vào dòng bài học PPCT.
     + **Tách riêng Bảng Thiết bị** (chứa `Thiết bị dạy học`, `TT 38`) $\rightarrow$ nạp vào `results.devices`.
     + **Tách riêng Bảng Phòng bộ môn** (chứa `Tên phòng`, `TT 14`) $\rightarrow$ nạp vào `results.rooms`.
     + **Tách riêng Bảng Kiểm tra đánh giá** (chứa `Bài kiểm tra`, `Giữa kỳ`, `Cuối kỳ`) $\rightarrow$ nạp vào `results.assessments`.
2. **Khớp Chính Xác Từng Cột Của Bảng PPCT Nguồn**:
   - Khi duyệt qua các dòng của bảng PPCT:
     + Nếu dòng là Tiêu đề chương / Học kỳ (ví dụ `HỌC KÌ I`, `1. SỐ HỌC 6`, `CHƯƠNG I. ...`, `HỌC KÌ II`): Đánh dấu `isHeader: true`, giữ nguyên văn bản làm dòng banner gộp cột.
     + Nếu dòng là Bài học: Tách chuẩn xác từng cột:
       * `lesson`: Tên bài học sạch (ví dụ: `Bài 1. Tập hợp`, `Bài 2. Cách ghi số tự nhiên`).
       * `periods`: Số tiết (ví dụ: `1`, `2`).
       * `tietCT`: Tiết PPCT (ví dụ: `1`, `2`, `3`, `4`).
       * `week`: Tuần thực hiện (ví dụ: `1`, `2`, `3`).
       * `devices`: Thiết bị dạy học (ví dụ: `Ti vi, thước`).
       * `location`: Địa điểm dạy học (ví dụ: `Lớp học`).
       * `integration`: Để trống để AI điền mã NLS & AI tương ứng.
3. **Định Dạng Bảng Xem Trước (Preview) & Xuất Word (.docx) Chuẩn Xác, Chống Tràn Cột**:
   - CSS bảng xem trước: Cài đặt `table-layout: fixed; width: 100%; word-break: break-word;` với tỷ lệ độ rộng cột rõ ràng:
     + `Bài học`: 30%
     + `Số tiết`: 7% (căn giữa)
     + `Tiết CT`: 8% (căn giữa)
     + `Tuần`: 7% (căn giữa)
     + `Thiết bị dạy học (*)`: 12%
     + `Địa điểm dạy học (**)`: 11%
     + `Mã NLS & AI (CV 3456 & QĐ 2422)`: 25%
   - Dòng tiêu đề chương `isHeader: true` tự động gộp 7 cột (`colspan="7"` trên Web và `columnSpan: 7` trên Word .docx), in đậm, căn giữa nổi bật.
   - File Word `.docx` xuất ra có đầy đủ chú thích `(*)` TT 38/2021, `(**)` TT 14/2020 và bảng chữ ký phê duyệt 2 bên chuẩn hành chính.
4. **Siêu Prompt Gemini và Cơ Chế Bảo Toàn PPCT Nguồn**:
   - Chỉ thị AI: Giữ nguyên 100% các dòng bài học và tuần thực hiện từ file người dùng tải lên, chỉ điền nội dung vào cột `integration` theo tỷ lệ NLS (%), tỷ lệ AI (%) và dải mật độ mã (`1–2`, `2–3`, `3–4 mã/bài`) đã chọn. Dòng `isHeader: true` để trống cột mã NLS/AI.
5. **Cập nhật Bộ Kiểm thử Tự động ([tests/xaydungphuluc-smoke.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/tests/xaydungphuluc-smoke.js))**:
   - Thêm test parse trực tiếp file `GIAO AN/XAYDUNGPHULUC/Phụ lục 1 - Lớp 6 - Toán.docx`:
     + Xác nhận KHÔNG có dòng hành chính ("TRƯỜNG THCS...", "CỘNG HÒA XÃ HỘI...") bị lẫn vào `sourcePpctRows`.
     + Xác nhận nhận diện đúng các bài học (`Bài 1. Tập hợp`, `Bài 2. Cách ghi số tự nhiên`...), số tiết, tiết CT, tuần.

## Ngoài phạm vi
- Không can thiệp các file ngoài `xaydungphuluc.html` và file test liên quan.

## File dự kiến tác động
- `xaydungphuluc.html` [NÂNG CẤP THUẬT TOÁN BÓC TÁCH TỪNG BẢNG HTML/DOCX, LOẠI BỎ BẢNG HÀNH CHÍNH KHỎI PPCT, ĐỊNH DẠNG TABLE-LAYOUT FIXED 7 CỘT]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG TEST PARSE DOCX MẪU CHUẨN XÁC]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Nâng cấp Hàm Trích Xuất Bảng `extractDocxTables(html)` trong `xaydungphuluc.html`**:
   - Phân tích DOM các thẻ `<table>` trong tài liệu `mammoth.convertToHtml`.
   - Với mỗi `<table>`:
     + Đọc dòng header đầu tiên.
     + Nếu header chứa `UBND` hoặc `CỘNG HÒA XÃ HỘI` hoặc `TỔ TRƯỞNG`: Trích xuất thông tin trường/tổ vào form, bỏ qua không đưa vào PPCT.
     + Nếu header chứa `Thiết bị dạy học`: Nạp vào mảng Thiết bị (`results.devices`).
     + If header chứa `Tên phòng`: Nạp vào mảng Phòng bộ môn (`results.rooms`).
     + If header chứa `Bài kiểm tra`: Nạp vào mảng Đánh giá (`results.assessments`).
     + If header chứa `Bài học` / `Tên bài` / `Tiết CT` / `Tuần`: Bóc tách thành `sourcePpctRows` với các trường chuẩn `lesson`, `periods`, `tietCT`, `week`, `devices`, `location`, `isHeader`.
2. **Bước 2: Chuẩn Hóa Hàm `ppctRow` và `preserveSourceSchedule`**:
   - Đảm bảo các dòng bài học luôn sạch sẽ, không bị dính văn bản hành chính.
   - Dòng tiêu đề phân cấp (`isHeader: true`) gộp 7 cột sạch sẽ.
3. **Bước 3: Nâng Cấp Giao Diện Bảng Xem Trước Inline và Hàm Xuất Word `exportDocx`**:
   - Thêm style `table-layout: fixed; width: 100%; word-break: break-word;` cho bảng xem trước để hiển thị đầy đủ 7 cột không bị tràn màn hình.
   - Đảm bảo xuất Word `.docx` 7 cột chuẩn tỷ lệ và gộp cột cho các dòng chương/học kỳ.
4. **Bước 4: Cập nhật và chạy kiểm thử tự động**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`, xác nhận PASS 100%.

## Rủi ro
- **Rủi ro**: File tải lên có các tên cột biến thể khác nhau (ví dụ "Nội dung bài dạy", "Tiết theo PPCT", "Tuần thứ").
  - *Giải pháp*: Hàm `normalizeHeaderKey` sử dụng biểu thức chính quy đa dạng để nhận diện chính xác mọi biến thể tên cột sư phạm phổ biến.

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`:
     + Kiểm tra thuật toán bóc tách trên file `GIAO AN/XAYDUNGPHULUC/Phụ lục 1 - Lớp 6 - Toán.docx`.
     + Xác nhận dòng đầu tiên của PPCT là `Bài 1. Tập hợp` (hoặc dòng banner `HỌC KÌ I`), tuyệt đối không có dòng hành chính "TRƯỜNG THCS...".
     + Xác nhận bảng xem trước và file Word có đủ 7 cột.
2. **Kiểm thử thủ công trên trình duyệt**:
   - Mở `xaydungphuluc.html`, tải file `Phụ lục 1 - Lớp 6 - Toán.docx` lên.
   - Bấm **⚡ Sinh trọn bộ Phụ lục**:
     + Xác nhận bảng phân phối chương trình hiển thị ngay ngắn, chuẩn 7 cột: `Bài học`, `Số tiết`, `Tiết CT`, `Tuần`, `Thiết bị dạy học (*)`, `Địa điểm dạy học (**)`, `Mã NLS & AI (CV 3456 & QĐ 2422)`.
     + Toàn bộ tên bài học sạch sẽ, đúng bài 1, bài 2, bài 3..., không bị chèn văn bản hành chính vào bảng như trong ảnh lỗi trước đó.
     + Xuất file Word `.docx` và mở kiểm tra bố cục hoàn hảo.

## Tiêu chí nghiệm thu
1. Bóc tách độc lập các bảng trong tài liệu; không bao giờ để văn bản hành chính (tên trường, quốc hiệu, thông tin mở đầu) bị lẫn vào các dòng bài học của bảng PPCT.
2. Bảng PPCT hiển thị đầy đủ 7 cột chuẩn, căn chỉnh ngay ngắn, không bị tràn màn hình; các dòng phân chương `HỌC KÌ I`, `CHƯƠNG I` gộp 7 cột nổi bật.
3. Giữ nguyên 100% dữ liệu gốc từ file tải lên; AI chỉ điền vào cột Mã NLS & AI.
4. Toàn bộ smoke test tự động đều PASS 100%.
