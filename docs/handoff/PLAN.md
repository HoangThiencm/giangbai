# PLAN: Sửa Lỗi AI Nhận Diện Và Hiển Thị Bảng Phân Phối Chương Trình (PPCT) Khi Tải Tệp Lên Trong xaydungphuluc.html

## Hiện trạng
1. **Khảo sát lỗi "AI chạy xong tắt luôn không báo gì và không hiển thị PPCT"**:
   - **Mất cấu trúc bảng khi đọc DOCX**: Khi người dùng tải file Word (.docx), hàm `parseFiles` chỉ truyền `mammoth.extractRawText` (chuỗi văn bản phẳng làm mất toàn bộ hàng/cột của bảng) sang `recognizePpctWithAi`. AI nhận một chuỗi rời rạc hàng trăm dòng không phân tách tab/cột nên không thể nhận diện chính xác cấu trúc PPCT.
   - **Schema JSON quá cứng nhắc, thiếu linh hoạt**: Hàm `normalizeRecognizedPpct` chỉ chấp nhận duy nhất thuộc tính `data.ppct`. Nếu Gemini/Mistral trả về mảng trực tiếp `[...]` hoặc đối tượng với các key thông dụng khác (`schedule`, `plan`, `data`, `lessons`, `items`, `rows`, `table`), hoặc dùng tên thuộc tính tiếng Việt / snake_case (`ten_bai`, `bai_hoc`, `so_tiet`, `tiet_ct`, `tuan`, `thiet_bi`, `dia_diem`), `data.ppct` sẽ là `undefined` -> `normalizeRecognizedPpct` trả về mảng rỗng `[]` -> `recognizePpctWithAi` ném lỗi ngoại lệ.
   - **`sourcePpctTable` ghi đè và vô hiệu hóa kết quả AI**: Khi parse bảng từ file, biến `rawTable` (từ DOM regex) được gán vào `sourcePpctTable`. Sau đó, các hàm giao diện (`aiPickerRows`, `aiCandidates`, `dynamicPpctTable`, `preservedPpctTable`) lại ưu tiên dùng `sourcePpctTable` nếu nó tồn tại. Dù AI có nhận diện thành công vào `sourcePpctRows`, hệ thống vẫn dùng dữ liệu thô/lỗi từ `sourcePpctTable`.
   - **Không cập nhật và hiển thị vào Mục 7 (Xem trước & xuất Word) khi tải tệp**: Khi người dùng tải file lên, `parseFiles` chỉ cập nhật mảng dữ liệu mà không khởi tạo lại `results['1']`, `results['3']` và không gọi `renderPreview()`. Vùng xem trước ở Mục 7 vẫn hiển thị "Chưa có nội dung. Chọn cấu hình và bấm Sinh Phụ lục", khiến người dùng có cảm giác AI chạy xong nhưng không hiển thị gì.
   - **Thanh tiến trình tự ẩn sau 1.5s gây cảm giác "tắt luôn không báo gì"**: Hàm `setProgress(100, ..., true, 1500)` tự động ẩn hộp tiến trình sau 1.5 giây mà không để lại thông báo xác nhận nổi bật ở khu vực chính ngoài một toast nhỏ dưới góc màn hình.
   - **Trùng lặp 3 khối mã nguồn trong `xaydungphuluc.html`**: File `xaydungphuluc.html` hiện có 3 khối mã lặp đè lên nhau (các hàm `parseFiles`, `normalizeAppendix`, `dynamicPpctTable`, `exportDocx`, `renderPreview`, `getConfig`, `preservedPpctTable` được định nghĩa 2-3 lần) gây xung đột biến toàn cục và khó bảo trì.

---

## Phạm vi
1. **Trích xuất dữ liệu tệp nguồn thông minh**:
   - Khi đọc tệp `.docx`, chuyển đổi bảng HTML (`mammoth.convertToHtml` -> `extractDocxTables`) thành dạng bảng phân tách tab (TSV/Markdown) có đầy đủ hàng cột để gửi cho AI thay vì chuỗi văn bản thô phẳng.
   - Khi đọc tệp `.xlsx` hoặc `.pdf`, chuẩn hóa định dạng dòng/cột trước khi gửi cho AI.
2. **Nâng cấp AI Recognizer linh hoạt & Chống lỗi**:
   - Tối ưu hóa prompt nhận diện PPCT: hướng dẫn AI trích xuất đầy đủ các cột (Bài học, Số tiết, Tiết CT, Tuần, Thiết bị, Địa điểm, dòng tiêu đề Phân cấp/Chương/Học kì).
   - Nâng cấp `normalizeRecognizedPpct` để hỗ trợ đa dạng cấu trúc trả về: mảng trực tiếp `[...]`, đối tượng `{ ppct: [...] }`, `{ schedule: [...] }`, `{ data: [...] }`, `{ plan: [...] }`, `{ lessons: [...] }` và hỗ trợ đầy đủ các biến thể tên trường (tiếng Anh, tiếng Việt, snake_case, camelCase).
   - Tự động nhận diện dòng tiêu đề `isHeader` qua quy tắc `isPpctHeaderRow` nếu AI quên đánh dấu.
3. **Đồng bộ dữ liệu và hiển thị trực tiếp lên giao diện**:
   - Khi AI nhận diện xong, đồng bộ đồng thời cả `sourcePpctRows` và `sourcePpctTable` (chuẩn hóa bảng 6-7 cột đồng nhất).
   - Cập nhật tức thì Mục 3: Bảng chọn tiết AI (`updateAiPicker()`).
   - Cập nhật tức thì Mục 7: Xem trước & xuất Word (`renderPreview()`) với dữ liệu PPCT vừa nhận diện (gắn vào `results['1']` và `results['3']`).
   - Hiển thị thẻ thông báo kết quả nổi bật ở Mục 2 (`#fileList`) và ghi log chi tiết vào `#log`.
4. **Dọn dẹp và hợp nhất mã nguồn**:
   - Hợp nhất và loại bỏ các định nghĩa hàm trùng lặp trong thẻ `<script>` của `xaydungphuluc.html`.
   - Cập nhật bộ test `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` đảm bảo pass 100%.

---

## Ngoài phạm vi
- Không thay đổi các quy chuẩn sư phạm (CV 5512, TT 38/2021, TT 14/2020, NLS CV 3456, AI QĐ 2422).
- Không can thiệp vào các trang khác như `soankhbd.html`, `admin.html`, `index.html`.
- Không thay đổi logic bảo mật API key.

---

## File dự kiến tác động
- `xaydungphuluc.html` [SỬA LOGIC NHẬN DIỆN, ĐỒNG BỘ SOURCE TABLE, RENDER PREVIEW NGAY SAU KHI TẢI TỆP, HỢP NHẤT MÃ TRÙNG LẶP]
- `tests/xaydungphuluc-smoke.js` [CẬP NHẬT KIỂM THỬ NHẬN DIỆN PPCT, BẢO TOÀN DỮ LIỆU VÀ RENDER PREVIEW]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi hoàn thành triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

---

## Các bước thực hiện
1. **Bước 1: Nâng cấp trích xuất văn bản có cấu trúc bảng từ tệp DOCX/XLSX/PDF**:
   - Trong `parseFiles`:
     * Với `.docx`: Lấy `htmlDoc = (await mammoth.convertToHtml({ arrayBuffer: buf })).value`, bóc tách `tables = extractDocxTables(htmlDoc)`. Tạo chuỗi bảng dạng TSV/Markdown từ `tables`. Nếu có bảng, ưu tiên gửi văn bản dạng bảng có tab/xuống dòng cho AI; nếu không có bảng mới dùng `extractRawText`.
     * Với `.xlsx`: Giữ nguyên bóc tách dạng tab-separated sheets.
     * Với `.pdf`: Ghép nối các trang có cấu trúc hàng rõ ràng.
2. **Bước 2: Cải tiến `ppctRecognitionPrompt` và `normalizeRecognizedPpct`**:
   - Cập nhật prompt chỉ rõ schema và ví dụ mẫu: `schema {"ppct":[{"lesson":"Tên bài","periods":"2","tietCT":"1-2","week":"Tuần 1","devices":"Máy chiếu","location":"Lớp học","isHeader":false}]}`.
   - Viết lại hàm `normalizeRecognizedPpct(data)`:
     * Kiểm tra linh hoạt: `const raw = Array.isArray(data) ? data : (data.ppct || data.schedule || data.plan || data.data || data.lessons || data.items || data.rows || data.table || []);`
     * Với mỗi item, lấy:
       - `lesson`: `row.lesson || row.ten_bai || row.tenBai || row.bai_hoc || row.baiHoc || row.title || row.name || row.noi_dung || ''`
       - `periods`: `row.periods || row.so_tiet || row.soTiet || row.duration || ''`
       - `tietCT`: `row.tietCT || row.tietCt || row.tiet_ct || row.tietPPCT || row.periodCT || row.stt || ''`
       - `week`: `row.week || row.tuan || row.thoi_diem || row.time || ''`
       - `devices`: `row.devices || row.thiet_bi || row.thietBi || row.equipment || ''`
       - `location`: `row.location || row.dia_diem || row.diaDiem || row.room || ''`
       - `isHeader`: `Boolean(row.isHeader || row.is_header || row.header || isPpctHeaderRow(lesson))`
     * Chuẩn hóa và lọc các dòng hợp lệ (không chứa tiêu đề hành chính).
3. **Bước 3: Đồng bộ `sourcePpctTable` và `sourcePpctRows` sau khi AI nhận diện**:
   - Khi AI nhận diện được `ppctRows`:
     * Gán `sourcePpctRows = ppctRows;`
     * Xây dựng `sourcePpctTable = ppctTableFromRows(sourcePpctRows);`
     * Nếu tệp có các bảng thiết bị, phòng học, kiểm tra đánh giá (`sourceDevices`, `sourceRooms`, `sourceAssessments`) thì lưu trữ đầy đủ.
4. **Bước 4: Cập nhật giao diện tức thì (Mục 3 và Mục 7) & Thông báo rõ ràng**:
   - Gọi `updateAiPicker()` để hiển thị danh sách bài học và tiết học trong Mục 3.
   - Khởi tạo dữ liệu xem trước ban đầu với PPCT vừa tải lên:
     * `results['1'] = fallback('1', getConfig());`
     * `results['3'] = fallback('3', getConfig());`
     * Gán bảng PPCT nguồn vào `results['1'].scheduleTable` và `results['3'].planTable`.
     * Gọi `renderPreview()` để hiển thị ngay bảng PPCT trực quan trong Mục 7 (Xem trước & xuất Word).
   - Cập nhật `#fileList` với thông điệp thành công màu xanh nổi bật: `✓ Đã nhận diện thành công ${count} dòng PPCT từ tệp ${esc(f.name)}. Xem chi tiết tại Mục 3 và Mục 7.`
   - Ghi thông tin vào `#log`.
5. **Bước 5: Hợp nhất và loại bỏ các định nghĩa hàm trùng lặp trong `xaydungphuluc.html`**:
   - Rà soát toàn bộ thẻ `<script>` trong `xaydungphuluc.html`, loại bỏ triệt để các phiên bản cũ của `parseFiles`, `normalizeAppendix`, `dynamicPpctTable`, `exportDocx`, `renderPreview`, `getConfig`, `preservedPpctTable`.
   - Đảm bảo chỉ có 1 định nghĩa duy nhất, chuẩn xác cho mỗi hàm.
6. **Bước 6: Cập nhật và chạy kiểm thử `tests/xaydungphuluc-smoke.js`**:
   - Bổ sung test cases: nhận diện từ JSON dạng mảng, nhận diện từ JSON có key tiếng Việt/snake_case, kiểm tra `sourcePpctTable` được đồng bộ và `renderPreview` hiển thị dữ liệu PPCT sau khi parse.
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js` đảm bảo pass 100%.

---

## Rủi ro & Giải pháp
1. **Rủi ro AI trả về cấu trúc JSON không theo chuẩn quy ước**:
   - *Giải pháp*: `normalizeRecognizedPpct` xử lý bao quát mọi kiểu dữ liệu (mảng, object bọc ngoài, snake_case, tiếng Việt, camelCase).
2. **Rủi ro tệp DOCX có bảng phức tạp (merged cells, header lặp lại)**:
   - *Giải pháp*: Bóc tách cả qua DOM HTML (`mammoth.convertToHtml`) lẫn regex, tạo chuỗi dữ liệu bảng TSV rõ ràng cho AI.
3. **Rủi ro người dùng không biết PPCT đã tải xong**:
   - *Giải pháp*: Tự động cập nhật bảng ở Mục 3 và bảng Xem trước ở Mục 7 ngay lập tức, kèm thông báo thành công xanh rõ ràng ở Mục 2.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy `node tests/xaydungphuluc-smoke.js`
   - Chạy `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công (Kịch bản người dùng)**:
   - Mở `xaydungphuluc.html` trên trình duyệt.
   - Tải tệp DOCX PPCT mẫu (hoặc file phân phối chương trình bất kỳ).
   - Kiểm tra:
     * Thanh tiến trình chạy và hoàn tất.
     * Thông báo xanh hiển thị số dòng PPCT nhận diện được tại Mục 2.
     * Bảng Mục 3 hiển thị đầy đủ các bài học và cho phép tick chọn tiết AI.
     * Bảng Mục 7 (Xem trước) hiển thị ngay bảng phân phối chương trình từ tệp nguồn.
     * Bấm "Sinh trọn bộ Phụ lục", hệ thống sinh YCCĐ / NLS / AI chính xác dựa trên bảng PPCT nguồn.

---

## Tiêu chí nghiệm thu
- [x] Khi tải file DOCX/XLSX/PDF lên, AI nhận diện chính xác danh sách bài học, số tiết, tiết CT, tuần, thiết bị, địa điểm và các dòng phân cấp chương/học kỳ.
- [x] Hỗ trợ linh hoạt mọi định dạng JSON trả về từ AI (mảng trực tiếp, object bọc ngoài, tên trường tiếng Anh/tiếng Việt/snake_case).
- [x] `sourcePpctTable` và `sourcePpctRows` được đồng bộ nhất quán từ kết quả AI.
- [x] Sau khi nhận diện xong, dữ liệu PPCT được hiển thị ngay lập tức ở Mục 3 (chọn tiết AI) và Mục 7 (bảng xem trước), không còn tình trạng chạy xong tắt im lặng.
- [x] Không còn hàm bị định nghĩa trùng lặp nhiều lần trong `xaydungphuluc.html`.
- [x] Bộ test `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js` vượt qua 100%.