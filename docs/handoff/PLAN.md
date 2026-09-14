# PLAN

## Hiện trạng & Phân tích Kiến trúc
- Hiện tại hệ thống trích xuất nội dung DOCX sang Markdown, gửi toàn văn sang Gemini tái tạo lại rồi biên dịch ngược từ Markdown sang Word (.docx / .doc).
- Đúng như đánh giá kiến trúc của người dùng: **Quy trình qua trung gian Markdown không thể cam kết 100% file gốc**, vì sẽ luôn có nguy cơ:
  + Mất cấu trúc ô gộp phức tạp (`w:vMerge`, `w:gridSpan`);
  + Mất định dạng Word chi tiết: font chữ riêng của trường/tổ, tab stop, header/footer, số trang, hình ảnh, shape, watermark;
  + Mất cách xuống dòng và căn lề riêng trong từng ô bảng;
  + AI có thể tự ý viết lại hoặc làm lệch thứ tự câu từ.
- **Giải pháp triệt để:** Triển khai cơ chế **Can thiệp trực tiếp cấu trúc gói OOXML (Direct OOXML Injection)**:
  + Giữ nguyên 100% gói tệp `.docx` gốc (Binary ZIP).
  + AI chỉ sinh các đoạn tích hợp (Delta / Surgical Snippets): mục tiêu NLS/AI cho Mục I, nhiệm vụ tích hợp cho Mục III, và bảng tổng hợp cuối bài.
  + Thư viện `JSZip` giải nén `word/document.xml` trong bộ nhớ, dùng DOMParser chèn đúng các node `<w:p>` và `<w:tbl>` vào các vị trí tương ứng, sau đó nén lại thành file `.docx`.
  + **Kết quả:** Đạt 100% bảo toàn file Word gốc đúng nghĩa (giữ nguyên từng font, lề, header, footer, ảnh và bảng biểu phức tạp), không có bất kỳ rủi ro nào về việc AI viết lại hay phá vỡ cấu trúc.

## Phạm vi
1. **Lưu trữ nhị phân gói DOCX gốc (`currentDocxBuffer`):**
   - Khi người dùng nạp file `.docx`, lưu nguyên vẹn `ArrayBuffer` của tệp vào bộ nhớ trình duyệt.
   - Nạp thư viện `JSZip` (`https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js`).
2. **AI Sinh đoạn tích hợp can thiệp (Surgical / Delta Generation):**
   - Trích xuất tóm tắt ngắn gọn cấu trúc bài dạy để Gemini phân tích (tiết kiệm token, phản hồi cực nhanh dưới 5s).
   - Gemini chỉ trả về JSON chứa đúng 3 phần cần chèn:
     ```json
     {
       "mucTieu": "c) Năng lực số: [1.2.TC1a] ...",
       "hoatDongMuc3": {
         "tenHoatDong": "Hoạt động 2",
         "noiDungChen": "[Tích hợp NLS: 1.2.TC1a] Học sinh..."
       },
       "bangTongHop": [
         {"noiDung": "Hoạt động 2", "nls": "[1.2.TC1a]", "ai": "", "minhChung": "..."}
       ]
     }
     ```
   - Quy tắc nghiêm ngặt: Năng lực nào không chọn thì không sinh, không bao giờ sinh câu "Không tích hợp...".
3. **Module Chèn trực tiếp OOXML (`injectIntegrationIntoDocx`):**
   - Mở `word/document.xml` từ `JSZip`.
   - Tìm đoạn Mục I (sau `Năng lực đặc thù` hoặc `Mục tiêu`): Tạo node `<w:p>` với định dạng màu sắc (NLS xanh lá, AI tím) và chèn vào cây XML.
   - Tìm vị trí hoạt động tại Mục III: Chèn đoạn `<w:p>` tích hợp vào ngay sau hoạt động hoặc trong ô tương ứng.
   - Chèn bảng tổng hợp `<w:tbl>` trước `<w:sectPr>` cuối tài liệu.
   - Lưu đè `word/document.xml` và xuất file `.docx` mới từ `zip.generateAsync`.
4. **Chế độ Dự phòng (Fallback):**
   - Nếu người dùng nạp PDF, TXT hoặc tự soạn thảo không có file DOCX gốc, hệ thống tự động fallback sang chế độ xuất Markdown qua `docxGenerator` / `DocxGenerator` như hiện tại.
   - Nút xuất Word (.doc OMML) tiếp tục phục vụ nhu cầu chỉnh sửa công thức toán Equation.

## Ngoài phạm vi
- Không gửi file DOCX qua máy chủ trung gian (toàn bộ ZIP và XML DOM xử lý 100% trong bộ nhớ trình duyệt).
- Không sửa đổi `soankhbd.html`.
- Không bắt buộc đăng nhập.

## File dự kiến tác động
- `giaoantichhop.html`:
  + Nạp thêm `jszip.min.js`.
  + Thêm biến lưu `currentDocxBuffer` và `currentDocxName`.
  + Viết hàm `injectIntegrationIntoDocx(docxBuffer, deltaData)` thao tác XML DOM.
  + Nâng cấp prompt và hàm `integrateAi` để hỗ trợ chế độ Delta Injection khi có file DOCX gốc.
  + Nút "Xuất .docx" ưu tiên xuất từ file DOCX đã được chèn trực tiếp (giữ 100% gốc).

## Các bước thực hiện
### Bước 1: Nạp JSZip và lưu giữ gói DOCX gốc
- Thêm `<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>` vào `<head>`.
- Trong `readLessonFile`:
  + Khi `ext === 'docx'`: `currentDocxBuffer = await file.arrayBuffer(); currentDocxName = file.name;`
  + Tiếp tục hiển thị preview bằng `convertMammothHtmlToMarkdown` để giáo viên xem trước trên web.

### Bước 2: Xây dựng hàm chèn OOXML can thiệp trực tiếp
- Viết hàm `injectDocxOxml(arrayBuffer, delta)`:
  1. `const zip = await JSZip.loadAsync(arrayBuffer);`
  2. `const xmlText = await zip.file('word/document.xml').async('text');`
  3. `const doc = new DOMParser().parseFromString(xmlText, 'application/xml');`
  4. Tạo node `<w:p>` với thẻ `<w:r>` có styling chuẩn Word (`<w:b/>`, `<w:i/>`, `<w:color w:val="16A34A"/>` cho NLS, `<w:color w:val="9333EA"/>` cho AI).
  5. Quét tìm đoạn "Năng lực đặc thù" hoặc "Mục tiêu": chèn đoạn mục tiêu tích hợp ngay sau đó.
  6. Quét tìm hoạt động phù hợp trong Mục III: chèn đoạn nhiệm vụ tích hợp ngay sau đó.
  7. Tạo bảng `<w:tbl>` tổng hợp và chèn vào cuối `<w:body>`.
  8. `zip.file('word/document.xml', new XMLSerializer().serializeToString(doc));`
  9. Trả về `await zip.generateAsync({type: 'blob'});`

### Bước 3: Chuẩn hóa AI Delta Prompt
- Khi có `currentDocxBuffer`, Gemini chỉ cần trả về JSON delta chứa các đoạn cần chèn (thay vì viết lại 10 trang giáo án).
- Nếu Gemini trả về Markdown thông thường, hàm chèn OOXML vẫn trích xuất được khối Mục tiêu và Hoạt động để cấy ghép vào file gốc.

### Bước 4: Kiểm thử và hoàn thiện xuất file
- Khi giáo viên bấm "Xuất .docx":
  + Nếu có `currentDocxBuffer`: Tải ngay bản DOCX đã cấy ghép trực tiếp (giữ nguyên 100% font, ảnh, bảng biểu phức tạp của file gốc).
  + Nếu không có: Fallback sang `docxGenerator`.

## Rủi ro & Giải pháp
- **Rủi ro:** Cấu trúc XML trong `word/document.xml` của một số phần mềm (WPS Office, LibreOffice) có thể dùng namespace hoặc cấu trúc khác biệt một chút.
  - **Giải pháp:** Sử dụng các bộ chọn linh hoạt (quét textContent trong `<w:t>`) và tạo các node XML với đúng namespace `http://schemas.openxmlformats.org/wordprocessingml/2006/main`. Nếu cấy ghép gặp lỗi, tự động fallback sang `docxGenerator` an toàn.

## Cách kiểm thử
1. Nạp 1 file Word `.docx` có bảng biểu phức tạp (gộp hàng `rowspan`, gộp cột `colspan`), có hình ảnh, header/footer và font chữ tùy chỉnh.
2. Bấm "Bắt đầu tích hợp".
3. Bấm "Xuất .docx" và mở file tải về trong Microsoft Word:
   - Kiểm tra font chữ, căn lề, header, footer, hình ảnh: hoàn toàn nguyên bản 100%.
   - Kiểm tra các bảng biểu phức tạp: không bị lệch cột, không mất ô gộp.
   - Kiểm tra các phần tích hợp: hiển thị đúng tại Mục I và Mục III với màu sắc nổi bật.

## Tiêu chí nghiệm thu
- Cam kết giữ 100% file gốc cho mọi tệp `.docx` được nạp vào qua cơ chế Direct OOXML Injection.
- Không phụ thuộc vào việc AI tái tạo lại bảng biểu hay định dạng.
- Hoạt động mượt mà, độc lập client-side trên trình duyệt.
- Không sửa đổi `soankhbd.html`.
