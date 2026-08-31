# PLAN: Bảo Toàn Nguyên Vẹn 100% Cấu Trúc PPCT & Tuần Thực Hiện từ File Tải Lên (Chỉ Bổ Sung Cột Năng Lực Số / Khung AI), Chuẩn Hóa Theo File Mẫu Demo, Bật Progress Bar % và Nâng Cấp Mật Độ Mã

## Hiện trạng
1. **Mất cột "Tuần" và cấu trúc PPCT gốc khi tải file lên**:
   - Khi giáo viên tải lên file PPCT (.docx, .xlsx, .pdf), file gốc đã có đầy đủ: `STT`, `Tuần thực hiện` (từ Tuần 1 đến Tuần 35), `Tên bài học`, `Số tiết`, `Yêu cầu cần đạt`.
   - Trước đây, khi AI tạo nội dung thường tự động tóm tắt hoặc sinh lại danh sách bài mới, dẫn đến việc **bị mất cột Tuần thực hiện**, thiếu bài hoặc làm lệch tiến độ năm học của nhà trường.
   - **Yêu cầu nghiêm ngặt của người dùng**: Khi người dùng tải file PPCT lên, hệ thống phải **giữ lại đủ 100%**, giữ nguyên cột **Tuần thực hiện (Tuần 1 $\rightarrow$ Tuần 35)**, STT, Tên bài, Số tiết; AI chỉ làm nhiệm vụ **bổ sung thêm phần Năng lực số (NLS) / Khung Trí tuệ nhân tạo (AI)** vào đúng từng bài học theo cấu hình.
2. **Cấu trúc bảng chuẩn theo File Mẫu ([GIAO AN/XAYDUNGPHULUC/Phụ lục 1 - Lớp 6 - Toán.docx](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/GIAO%20AN/XAYDUNGPHULUC/Ph%E1%BB%A5%20l%E1%BB%A5c%201%20-%20L%E1%BB%9Bp%206%20-%20To%C3%A1n.docx))**:
   - Bảng Phân phối chương trình phải có đầy đủ cột `Tuần` ở vị trí trang trọng:
     + **Phụ lục 1**: `STT | Tuần | Bài học | Số tiết | Yêu cầu cần đạt | Mã NLS & AI (CV 3456 & QĐ 2422)`.
     + **Phụ lục 3**: `STT | Tuần | Bài học | Số tiết | Thời điểm | Thiết bị dạy học | Địa điểm dạy học | Mã NLS & AI (CV 3456 & QĐ 2422)`.
   - Các bảng phụ trợ đầy đủ: Bảng Thiết bị (TT 38/2021), Bảng Phòng bộ môn (TT 14/2020), Bảng Kiểm tra đánh giá định kỳ (GK1, CK1, GK2, CK2) và Bảng Chữ ký phê duyệt 2 bên.
3. **Các cải tiến giao diện trước đó**:
   - Xóa bỏ hoàn toàn khối "4. Phương pháp & kĩ thuật dạy học".
   - Bổ sung thanh tiến trình thời gian thực nổi ở đáy màn hình (% 0% $\rightarrow$ 100%, spinner xoay, thanh gradient).
   - Nâng cấp dropdown mật độ mã NLS & AI thành các khoảng dải linh hoạt: `1–2 mã/bài`, `2–3 mã/bài`, `3–4 mã/bài`.

## Phạm vi
1. **Cơ chế Bảo toàn Nguyên vẹn PPCT Nguồn từ File Người dùng Tải Lên**:
   - Bóc tách chi tiết dữ liệu bảng từ `.docx`, `.xlsx`, `.pdf` (bao gồm các cột `Tuần`, `STT`, `Bài học`, `Số tiết`, `YCCĐ`).
   - Cập nhật chỉ thị tối thượng trong Siêu Prompt Gemini AI:
     + *"NGUYÊN TẮC BẢO TOÀN PPCT NGUỒN: BẮT BUỘC giữ nguyên 100% danh sách bài học và tuần thực hiện (Tuần 1 đến Tuần 35) từ tệp người dùng tải lên. Tuyệt đối không được xóa bỏ, rút gọn hay gộp tuần. Chỉ thực hiện nhiệm vụ: Giữ nguyên vẹn toàn bộ các dòng và BỔ SUNG thêm cột 'Mã NLS & AI (CV 3456 & QĐ 2422)' theo tỷ lệ (%) và khoảng mật độ mã (1–2, 2–3, 3–4 mã/bài) đã chọn."*
   - Trong trường hợp không tải file: Hệ thống tự động sinh trọn bộ 35 tuần với đầy đủ cột `Tuần` chuẩn theo chương trình GDPT 2018.
2. **Chuẩn hóa Bảng Preview và File Xuất Word (.docx) Khớp File Mẫu**:
   - Cột `Tuần` được tích hợp cố định vào bảng xem trước và bảng xuất Word cho cả Phụ lục 1 và Phụ lục 3.
   - Header 2 cột hành chính chuẩn (UBND Xã/Phường, Trường THCS / Quốc hiệu, Tiêu ngữ).
   - Đầy đủ 5 bảng chuẩn:
     1. Bảng Thiết bị dạy học (TT 38/2021): `STT | Thiết bị | Số lượng | Bài thực hành | Ghi chú`.
     2. Bảng Phòng học bộ môn (TT 14/2020): `STT | Tên phòng | Số lượng | Phạm vi sử dụng | Ghi chú`.
     3. Bảng PPCT Phụ lục 1: `STT | Tuần | Bài học | Số tiết | Yêu cầu cần đạt | Mã NLS & AI`.
     4. Bảng PPCT Phụ lục 3: `STT | Tuần | Bài học | Số tiết | Thời điểm | Thiết bị | Địa điểm | Mã NLS & AI`.
     5. Bảng Kiểm tra đánh giá (4 mốc GK1 Tuần 9, CK1 Tuần 18, GK2 Tuần 27, CK2 Tuần 35) và Bảng Chữ ký phê duyệt 2 bên.
3. **Giao diện & Trải nghiệm Người dùng**:
   - Xóa bỏ hoàn toàn khối "Phương pháp & kĩ thuật dạy học".
   - Thêm Floating Progress Bar thời gian thực nổi bật ở đáy màn hình (% 0% $\rightarrow$ 100%, spinner xoay, thanh gradient).
   - Nâng cấp Dropdown mật độ mã linh hoạt: `1–2 mã/bài`, `2–3 mã/bài`, `3–4 mã/bài`.
4. **Bộ Kiểm thử Tự động ([tests/xaydungphuluc-smoke.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/tests/xaydungphuluc-smoke.js))**:
   - Cập nhật assert kiểm tra cột `Tuần`, bảo toàn PPCT, Floating Progress Bar và dải mật độ mã.

## Ngoài phạm vi
- Không thay đổi các file ngoài `xaydungphuluc.html` và các file test liên quan.

## File dự kiến tác động
- `xaydungphuluc.html` [BẢO TOÀN CỘT TUẦN PPCT NGUỒN, CHUẨN HÓA DOCX THEO FILE MẪU, THÊM PROGRESS BAR %, XÓA KHỐI PHƯƠNG PHÁP, NÂNG CẤP DENSITY]
- `tests/xaydungphuluc-smoke.js` [CẬP NHẬT SMOKE TEST]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Cập nhật Schema Bảng và Siêu Prompt trong `xaydungphuluc.html`**:
   - Thêm cột `Tuần` (`week`) vào cấu trúc JSON của bảng PPCT cho cả Phụ lục 1 và Phụ lục 3.
   - Bổ sung nguyên tắc bảo toàn PPCT nguồn vào `appendixPrompt`: bắt buộc giữ nguyên tất cả các bài học và tuần thực hiện từ tài liệu tải lên, chỉ sinh thêm nội dung NLS & AI.
2. **Bước 2: Nâng cấp Bảng Xem Trước Inline và Hàm Xuất Word `exportDocx`**:
   - Render cột `Tuần` ở vị trí cột thứ 2 trong bảng xem trước.
   - Thêm cột `Tuần` vào file Word `.docx` xuất bản với độ rộng cột tối ưu.
   - Đảm bảo đầy đủ 5 bảng chuẩn theo file mẫu `Phụ lục 1 - Lớp 6 - Toán.docx`.
3. **Bước 3: Xóa Khối Phương pháp, Thêm Floating Progress Bar và Nâng Cấp Dropdown Mật Độ**:
   - Xóa bỏ `<section>` mục 4 và code liên quan đến `methods`.
   - Thêm `#progressContainer` và CSS floating bar ở đáy màn hình.
   - Cập nhật `#nlsDensity` và `#aiDensity` với các dải `1-2`, `2-3`, `3-4`.
4. **Bước 4: Cập nhật và chạy kiểm thử tự động**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`, xác nhận PASS 100%.

## Rủi ro
- **Rủi ro**: File tải lên có định dạng bảng không chuẩn hoặc dạng văn bản thô.
  - *Giải pháp*: Parser trích xuất toàn bộ text kèm cấu trúc dòng; Siêu Prompt của Gemini có chỉ dẫn phân tích thông minh nhận diện cột Tuần, STT, Bài học từ bất kỳ định dạng nào.

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`:
     + Xác nhận bảng PPCT có cột `Tuần` (`week`) và chỉ dẫn bảo toàn PPCT.
     + Xác nhận tồn tại các tùy chọn mật độ `1-2`, `2-3`, `3-4`.
     + Xác nhận tồn tại `progressContainer`, `progressPercent`, `progressBarInner`.
     + Xác nhận không còn khối "Phương pháp & kĩ thuật dạy học".
2. **Kiểm thử thủ công trên trình duyệt**:
   - Tải file PPCT mẫu lên $\rightarrow$ Bấm Sinh Phụ lục.
   - Kiểm tra kết quả xem trước: Toàn bộ danh sách bài học và tuần thực hiện (Tuần 1 $\rightarrow$ Tuần 35) được giữ nguyên vẹn 100%, cột Mã NLS & AI được điền đầy đủ.
   - Xuất file Word $\rightarrow$ Mở kiểm tra file `.docx` có đủ cột Tuần và khớp định dạng chuẩn của file demo.

## Tiêu chí nghiệm thu
1. Bảng PPCT giữ nguyên vẹn 100% danh sách bài học và cột Tuần thực hiện từ file tải lên; AI chỉ bổ sung cột Mã NLS & AI.
2. File Word xuất ra có đầy đủ cột Tuần, chuẩn thể thức theo file mẫu `Phụ lục 1 - Lớp 6 - Toán.docx`.
3. Khối "Phương pháp & kĩ thuật dạy học" được xóa bỏ hoàn toàn.
4. Thanh tiến trình % thời gian thực (Floating Progress Bar) nổi bật, mượt mà khi chạy sinh AI.
5. Dropdown mật độ mã hỗ trợ đầy đủ các dải linh hoạt: `1–2 mã/bài`, `2–3 mã/bài`, `3–4 mã/bài`.
6. Toàn bộ smoke test tự động đều PASS 100%.
