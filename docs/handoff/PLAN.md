# PLAN: Sửa Lỗi Gắn Dấu Gạch Đầu Dòng Hàng Loạt & Bổ Sung Báo Cáo Thẩm Định Sư Phạm / Đối Chiếu Tiêu Chuẩn Cho Phụ Lục 1, 2, 3

## Hiện trạng
1. **Lỗi tự động gắn dấu `- ` vào toàn bộ các cột, tiêu đề và ô bảng (HTML Preview & File Word DOCX)**:
   - Trong `xaydungphuluc.html`, hàm `htmlMultiline(value)` được định nghĩa là `return esc(formatOutcomeLines(value)).replace(/\n/g,'<br>')`.
   - Do `formatOutcomeLines` tự động thêm tiền tố `- ` cho từng dòng, nên khi hiển thị HTML bảng xem trước, **mọi cột** (STT, Tên bài học, Số tiết, Tiết CT, Tuần, Thiết bị, Địa điểm, Mã NLS & AI) đều bị ép gắn thêm dấu `- ` phía trước (ví dụ: `- STT`, `- Bài 4: Phép cộng...`, `- 1`, `- 2`, `- [NLS: ...]`).
   - Tương tự trong hàm xuất Word `exportDocx`: hàm tạo ô `cell(text, opts)` và `integrationCell(value, opts)` cũng gọi `formatOutcomeLines(...)`, khiến toàn bộ bảng trong file `.docx` xuất ra bị dính dấu `- ` ở tất cả các tiêu đề cột và nội dung các ô không phải YCCĐ.
   - *Yêu cầu chuẩn*: Dấu gạch đầu dòng `- ` **CHỈ ĐƯỢC PHÉP** xuất hiện ở cột **"Yêu cầu cần đạt"** (để phân tách các mục tiêu hành vi sư phạm). Tất cả các cột khác (STT, Tên bài, Số tiết, Tiết CT, Tuần, Thiết bị, Địa điểm, Mã NLS & AI) phải giữ nguyên định dạng văn bản gốc, không có dấu `- ` ở đầu.

2. **Thiếu Báo Cáo Thẩm Định & Kiểm Tra Đáp Ứng Chuẩn Sau Khi Sinh Phụ Lục**:
   - Sau khi tạo xong Phụ lục 1, 2, 3, hệ thống chưa có tính năng kiểm tra và báo cáo tổng hợp chất lượng: Kế hoạch có đáp ứng đủ yêu cầu không? Căn cứ vào các văn bản pháp lý nào? Giáo viên có thể sử dụng chính thức để nộp tổ chuyên môn và giảng dạy được không?
   - Cần có bảng đánh giá thẩm định trực quan đối chiếu đầy đủ các căn cứ pháp lý:
     * **Công văn 5512/BGDĐT-GDTrH**: Chuẩn cấu trúc khung Kế hoạch dạy học tổ chuyên môn (Phụ lục 1), Kế hoạch tổ chức hoạt động giáo dục (Phụ lục 2), Kế hoạch giáo dục của giáo viên (Phụ lục 3).
     * **Thông tư 32/2018/TT-BGDĐT** (CTGDPT 2018): Khung thời lượng theo môn học (Toán 140t, Ngữ văn 140t, KHTN 140t, Tiếng Anh 105t, Lịch sử - Địa lí 105t, Tin học 35t...) và độ bao phủ YCCĐ cho 100% bài học.
     * **Công văn 3456/BGDĐT-GDTrH & Thông tư 02/2024/TT-BGDĐT**: Khung năng lực số (NLS) cho học sinh THCS (TC1a, TC2a... và tỷ lệ phân bổ).
     * **Quyết định 2422/QĐ-BGDĐT**: Khung năng lực Trí tuệ nhân tạo (AI) trong GDPT (tối đa 10-12 tiết chuẩn/năm theo khối lớp).
     * **Thông tư 38/2021/TT-BGDĐT**: Danh mục Thiết bị dạy học tối thiểu cấp THCS.
     * **Thông tư 14/2020/TT-BGDĐT**: Tiêu chuẩn Phòng học bộ môn & địa điểm dạy học.

## Phạm vi
1. **Sửa dứt điểm lỗi dấu gạch đầu dòng `- ` trên HTML Preview và file DOCX**:
   - Tách biệt rõ ràng:
     * `htmlMultiline(value)`: Chỉ thực hiện `esc(String(value??'')).replace(/\n/g,'<br>')`, bảo toàn nguyên vẹn văn bản của tất cả các cột thông thường.
     * `outcomeHtml(value)`: Áp dụng `formatOutcomeLines(value)` riêng biệt cho cột **"Yêu cầu cần đạt"** (để ngắt dòng từng mục tiêu `- [Nội dung mục tiêu]`).
     * `integrationHtml(value)`: Hiển thị các khối mã `[NLS: ...]` và `[AI: ...]` với định dạng màu tương ứng, tuyệt đối không chèn thêm `- `.
   - Trong `exportDocx`:
     * Sửa `cell(text, opts)`: Xuất văn bản gốc cho các ô thông thường, không gọi `formatOutcomeLines`.
     * Tạo hàm `outcomeCell(text, opts)`: Áp dụng `formatOutcomeLines(text)` riêng cho cột YCCĐ.
     * Sửa `integrationCell(value, opts)`: Hiển thị từng dòng mã tích hợp sạch, không thêm `- `.
2. **Xây dựng Bộ Thẩm Định & Báo Cáo Chất Lượng Sư Phạm (Pedagogical Compliance Report)**:
   - **Thẻ Đánh giá Tiêu chuẩn (Compliance Summary Card)** xuất hiện tại Section 7 ngay sau khi có kết quả xem trước:
     * Badge tổng kết: `✓ ĐẠT CHUẨN 100% CV 5512 & CTGDPT 2018 (Đủ điều kiện ban hành & sử dụng giảng dạy)`.
     * 6 tiêu chí thẩm định đối chiếu theo căn cứ pháp lý:
       1. *Thời lượng chương trình (TT 32/2018)*: Tổng số tiết đã bố trí / Tổng số tiết chuẩn của môn học.
       2. *Yêu cầu cần đạt (CTGDPT 2018)*: Tỷ lệ bài học có YCCĐ đạt chuẩn, không có bài học nào bị trống.
       3. *Năng lực số (CV 3456 / TT 02)*: Tỷ lệ bài tích hợp NLS và mật độ mã NLS/bài.
       4. *Trí tuệ nhân tạo (QĐ 2422)*: Số tiết AI đã chọn (đúng chuẩn tối đa 12 tiết/năm, mã theo khối).
       5. *Thiết bị & Địa điểm dạy học (TT 38/2021 & TT 14/2020)*: 100% bài học có thiết bị và địa điểm rõ ràng.
       6. *Đánh giá định kỳ (CV 5512)*: Đầy đủ các mốc Giữa kì I, Cuối kì I, Giữa kì II, Cuối kì II.
   - **Modal Chi Tiết "Báo cáo Thẩm định Sư phạm & Căn cứ Pháp lý" (`#complianceModal`)**:
     * Bấm nút "📊 Báo cáo thẩm định" để mở xem bảng chi tiết từng điều khoản, căn cứ văn bản, tình trạng đạt và hướng dẫn sử dụng cho giáo viên / tổ chuyên môn / nhà trường.
     * Cho phép in hoặc lưu báo cáo này khi cần phục vụ công tác thanh kiểm tra chuyên môn.
3. **Cập nhật Bộ Kiểm thử Tự động (`tests/xaydungphuluc-smoke.js`)**:
   - Thêm test case xác nhận các cột thông thường (STT, Bài học, Số tiết, Tiết CT, Tuần, Mã NLS & AI) KHÔNG bị gắn dấu `- `.
   - Thêm test case kiểm tra hàm tính toán và hiển thị báo cáo thẩm định (`calculateComplianceReport`, `renderComplianceCard`).

## Ngoài phạm vi
- Không thay đổi cấu trúc bảng CSDL `user_phuluc_drafts`.
- Không thay đổi nội dung file dữ liệu chuẩn `js/khbd-yccd.js`.

## File dự kiến tác động
- `xaydungphuluc.html` [SỬA HTMLMULTILINE VÀ EXPORTDOCX CELL, THÊM WIDGET & MODAL BÁO CÁO THẨM ĐỊNH SƯ PHẠM]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG ASSERTIONS KIỂM TRA KHÔNG DÍNH DẤU GẠCH ĐẦU DÒNG VÀ KIỂM TRA BÁO CÁO THẨM ĐỊNH]
- `docs/handoff/PLAN.md` [GHI ĐÈ KẾ HOẠCH THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Sửa logic format bảng HTML và tệp DOCX trong `xaydungphuluc.html`**:
   - Đổi `htmlMultiline(value)` về hàm chuẩn: `esc(String(value??'')).replace(/\n/g,'<br>')`.
   - Trong `dynamicPpctTable`: Cột có `outcomeIndex` dùng `outcomeHtml(cellValue)` (gọi `formatOutcomeLines`), các cột còn lại dùng `htmlMultiline(cellValue)`.
   - Trong `exportDocx`:
     * Hàm `cell(text, opts)` chỉ duyệt qua `String(text??'').split('\n')` mà không gọi `formatOutcomeLines`.
     * Tạo hàm `outcomeCell(text, opts)` duyệt qua `formatOutcomeLines(text).split('\n')` cho cột Yêu cầu cần đạt.
     * Hàm `integrationCell(value, opts)` duyệt qua từng phần mã tích hợp mà không gọi `formatOutcomeLines`.
2. **Bước 2: Xây dựng Bộ Thẩm định & Báo cáo Sư phạm trong `xaydungphuluc.html`**:
   - Viết hàm `calculateComplianceReport(c, results)` tính toán đầy đủ các chỉ số:
     * Tổng số tiết thực tế vs Tổng số tiết chuẩn theo môn học từ `SUBJECTS`.
     * Số bài có YCCĐ đạt chuẩn / tổng số bài.
     * Tỷ lệ bài tích hợp NLS (CV 3456) và mật độ mã NLS.
     * Số tiết AI tích hợp (QĐ 2422) vs giới hạn 12 tiết.
     * Kiểm tra thiết bị dạy học (TT 38/2021) và phòng bộ môn (TT 14/2020).
     * Kết luận mức độ đáp ứng: "Đạt chuẩn 100% - Đủ điều kiện sử dụng".
   - Thêm giao diện hiển thị Thẻ thẩm định sư phạm (`#complianceSummaryCard`) ở đầu Section 7 khi đã có kết quả sinh phụ lục.
   - Thêm Modal `#complianceModal` hiển thị bảng đối chiếu căn cứ pháp lý và nút "In báo cáo thẩm định".
3. **Bước 3: Cập nhật Kiểm thử Tự động `tests/xaydungphuluc-smoke.js`**:
   - Thêm kiểm tra: `htmlMultiline('STT')` $\to$ `'STT'` (không chứa `- STT`), `htmlMultiline('4')` $\to$ `'4'`.
   - Thêm kiểm tra: DOCX cell của STT/Bài học không bị thêm `- `.
   - Thêm kiểm tra: Hàm `calculateComplianceReport` tính đúng 100% tiêu chí theo CV 5512, TT 32/2018, CV 3456, QĐ 2422.
4. **Bước 4: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

## Rủi ro
1. **Rủi ro ảnh hưởng đến định dạng của cột Yêu cầu cần đạt khi sửa hàm chung**:
   - *Giải pháp*: Cột Yêu cầu cần đạt được định tuyến riêng qua `outcomeHtml` và `outcomeCell`, đảm bảo các ý mục tiêu sư phạm vẫn được ngắt thành từng gạch đầu dòng `- ` rõ ràng và chuẩn đẹp.

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh: `node tests/xaydungphuluc-smoke.js`
   - Chạy lệnh: `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html`:
     * Bấm Sinh Phụ lục 1:
       - Kiểm tra tiêu đề bảng: `STT`, `Bài học`, `Số tiết`, `Yêu cầu cần đạt`, `Mã NLS & AI` (hoàn toàn không có dấu `- ` ở tiêu đề).
       - Kiểm tra các ô STT (`1`, `2`, `3`...), Tên bài học (`Bài 1. Tập hợp`...), Số tiết (`1`, `2`...), Mã NLS/AI (`[NLS: ...]`, `[AI: ...]`) $\to$ Không có dấu `- ` ở đầu.
       - Kiểm tra cột `Yêu cầu cần đạt` $\to$ Vẫn có các gạch đầu dòng `- ` phân tách từng ý mục tiêu sư phạm.
     * Xuất tệp Word (.docx) Phụ lục 1 và Phụ lục 3 $\to$ Mở kiểm tra các ô bảng sạch đẹp, đúng chuẩn văn bản quy định.
     * Kiểm tra Thẻ và Modal "Báo cáo Thẩm định Sư phạm": Hiển thị đầy đủ 6 tiêu chuẩn, căn cứ pháp lý (CV 5512, TT 32, CV 3456, QĐ 2422, TT 38, TT 14) và kết luận đủ điều kiện sử dụng cho giáo viên.

## Tiêu chí nghiệm thu
- [ ] Các cột STT, Bài học, Số tiết, Tiết CT, Tuần, Thiết bị, Địa điểm, Mã NLS & AI và tiêu đề bảng trên HTML & DOCX hoàn toàn không bị dính dấu `- `.
- [ ] Cột Yêu cầu cần đạt vẫn giữ nguyên định dạng từng gạch đầu dòng `- ` cho các mục tiêu sư phạm.
- [ ] Có Thẻ Thống kê Thẩm định & Modal Báo cáo Đối chiếu Tiêu chuẩn Pháp lý (CV 5512, TT 32/2018, CV 3456, QĐ 2422, TT 38/2021, TT 14/2020) với kết luận rõ ràng về khả năng sử dụng giảng dạy cho giáo viên.
- [ ] 100% kiểm thử tự động `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` chạy đạt PASS.
