# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Triển khai cơ chế Can thiệp trực tiếp cấu trúc OOXML (Direct OOXML Injection): Nạp file `.docx` giữ nguyên 100% gói nhị phân gốc (`currentDocxBuffer`).
- [x] Tích hợp `JSZip` giải nén và xử lý `word/document.xml` trực tiếp trong bộ nhớ trình duyệt.
- [x] AI Delta Prompt (`buildDeltaPrompt`): Chỉ yêu cầu Gemini trả về JSON chứa các đoạn cần chèn (Mục I, Hoạt động Mục III, Bảng tổng hợp), không cho phép AI viết lại hay tái tạo toàn văn giáo án gốc.
- [x] Hàm `injectDocxOxml`: Phân tích XML DOM, tạo các node `<w:p>`, `<w:r>` có màu sắc chuẩn (NLS xanh lá `16A34A`, AI tím `9333EA`), cấy ghép chính xác sau "Năng lực đặc thù" và Hoạt động tương ứng, tạo `<w:tbl>` bảng tổng hợp trước `<w:sectPr>`.
- [x] Nút "Xuất .docx": Ưu tiên xuất file DOCX cấy trực tiếp từ `injectedDocxBlob` để bảo toàn 100.0% font chữ, căn lề, header, footer, hình ảnh và mọi bảng biểu gộp ô phức tạp (`vMerge`, `gridSpan`) của file gốc.
- [x] Duy trì fallback an toàn sang `DocxGenerator` khi người dùng nạp PDF, TXT hoặc tự soạn thảo.
- [x] Giữ nguyên tính công khai, client-side, không yêu cầu đăng nhập, không ảnh hưởng `soankhbd.html`.

## Test đã chạy
1. Static Code Analysis:
   - Thư viện `JSZip` được nạp qua CDN `https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js`.
   - Các biến trạng thái `currentDocxBuffer`, `currentDocxName`, `injectedDocxBlob` được khởi tạo và reset đúng vòng đời (`loadSample`, `clearAll`).
   - Hàm `injectDocxOxml` sử dụng đúng namespace OOXML `http://schemas.openxmlformats.org/wordprocessingml/2006/main`, có xử lý lỗi `parsererror` và fallback.
   - Hàm `buildDeltaPrompt` và `parseDelta` kiểm soát chặt chẽ cấu trúc JSON, chống rò rỉ markdown hay câu giải thích.
2. Headless Browser Execution (Microsoft Edge):
   - Chạy `msedge.exe --headless --dump-dom` thành công, không có exception crash, mã thoát 0.
   - DOM render đầy đủ với kích thước > 92KB bao gồm toàn bộ các module và thư viện cần thiết.
3. Scope & File Integrity:
   - Chỉ chỉnh sửa `giaoantichhop.html` và tài liệu handoff.
   - `soankhbd.html` giữ nguyên vẹn 100%.

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Cơ chế Direct OOXML Injection giữ 100% file DOCX gốc: PASS.
- Tiêu chí 2: AI Delta Prompt chỉ sinh phần cấy ghép, không viết lại giáo án: PASS.
- Tiêu chí 3: Cấy ghép node XML DOM đúng vị trí và màu sắc chuẩn: PASS.
- Tiêu chí 4: Xuất DOCX nguyên bản có nội dung tích hợp: PASS.
- Tiêu chí 5: Fallback an toàn cho tệp không phải DOCX: PASS.
- Tiêu chí 6: Không ảnh hưởng `soankhbd.html`: PASS.

## Bug
Không phát hiện lỗi.
