# PLAN: SỬA LỖI VẼ HÌNH AI TRÊN VEHINH.HTML VÀ TÍCH HỢP CHỨC NĂNG VẼ HÌNH CỰC KỲ CHÍNH XÁC VÀO TRỢ LÝ THIÊN

## Hiện trạng
1. **Lỗi trên trang `vehinh.html` ("Lỗi AI vẽ hình: AI vẽ hình không phản hồi.")**:
   - **Tên model Gemini không hợp lệ**: Trong `api/vehinh_ai.php`, `vehinh.html` và `app.js`, hệ thống đang ưu tiên các model ảo/không tồn tại trên Google Generative AI v1beta: `gemini-3.6-flash`, `gemini-3.7-flash`, `gemini-3-flash-preview`. Khi gửi request tới `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent`, Google API trả về mã lỗi `404 NOT_FOUND` ("models/gemini-3.6-flash is not found for API version v1beta"). Trong `api/vehinh_ai.php`, mã 404 kích hoạt lệnh `break`, nhảy sang fallback `gemini-3.6-flash` (cũng lỗi 404) dẫn tới trả về lỗi HTTP 502.
   - **Cấu hình `thinkingConfig` không tương thích**: Trong `api/vehinh_ai.php`, trường `'thinkingConfig' => ['thinkingBudget' => 0]` bị gửi cứng trong `generationConfig`. Với các model như `gemini-2.0-flash` hoặc các model chuẩn, Google API trả về `400 Bad Request` do không hỗ trợ trường này, khiến request thất bại ngay lập tức.
   - **Timeout quá ngắn cho tác vụ Vision (30s)**: `vehinh_post_json` đặt cURL timeout là 30s. Khi người dùng tải ảnh đề bài (kích thước lớn), AI vừa phải chạy OCR nhận diện ảnh, vừa phân tích hình học và sinh toàn bộ code Fabric.js/GeoGebra nên thời gian xử lý thường vượt quá 30s, gây ngắt kết nối cURL timeout.
   - **Thiếu chỉ dẫn khi người dùng chỉ tải ảnh mà không nhập chữ**: Khi người dùng tải ảnh đề bài vào trang và không gõ chữ ở ô nhập đề, `app.js` gửi `userInstruction = "Phân tích và vẽ hình cho yêu cầu sau: "` mà không hướng dẫn AI đọc đề trong ảnh, gây bối rối cho model.
   - **Cơ chế nạp API Key cục bộ chưa đồng bộ**: `app.js` chỉ đọc key từ `global_gemini_keys` hoặc file txt, không tự động nạp từ `api/user_gemini_keys.php` hay các khóa `khbd_user_gemini_keys_*` như các module khác, khiến giáo viên đã đăng nhập nhưng chưa có `global_gemini_keys` trong trình duyệt bị lỗi thiếu key.
   - **Thiếu fallback gọi trực tiếp từ client**: Khi backend PHP gặp sự cố mạng/proxy hoặc timeout, `vehinh.html` không có cơ chế gọi trực tiếp Gemini API từ trình duyệt với key của người dùng (như `khbd-gemini.js` và `thitructuyen.html`).

2. **Chức năng vẽ hình trong Trợ lý Thiên (`/thien`, "Thiên ơi")**:
   - Hiện tại Trợ lý Thiên có 10 nhánh (1: Duyệt giáo án, 2: Soạn KHBD, 3: Tạo bài tập, 4: Duyệt đề, 5: Game giáo dục, 6: Sổ điểm, 7: Quản lý tổ chuyên môn, 8: Tạo báo cáo, 9: Viết sáng kiến, 10: Tạo bài giảng HTML).
   - Thư mục `TROLYTHIEN/` chưa có phân hệ riêng cho tác vụ Dựng hình hình học (`11_VE_HINH/`).
   - Chưa có workflow xử lý tự động đề bài hình học dán vào chat hoặc ảnh chụp đề bài đặt trong thư mục `Dau_vao/` để xuất ra hình vẽ giải tích cực kỳ chính xác (tỷ lệ chuẩn 100%, file SVG, file GeoGebra script và file HTML preview tương tác).

## Phạm vi
1. **Sửa dứt điểm lỗi vẽ hình AI trên `vehinh.html`**:
   - Cập nhật danh mục model chuẩn của Gemini API trong `api/vehinh_ai.php`, `vehinh.html`, `app.js`: Ưu tiên các model hoạt động thực tế: `gemini-2.5-flash` (mặc định tối ưu đa phương thức và hình vẽ), `gemini-2.5-pro` (suy luận hình học nâng cao), `gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-1.5-flash`. Loại bỏ các tên model lỗi thời/không tồn tại làm model chính.
   - Xử lý tương thích `thinkingConfig`: Chỉ áp dụng `thinkingBudget` cho model hỗ trợ; với các model tiêu chuẩn không gửi `thinkingConfig` để tránh lỗi 400.
   - Nâng timeout cURL trong `api/vehinh_ai.php` từ 30s lên 90s–120s để xử lý thoải mái ảnh chụp đề bài và hình học phức tạp.
   - Nâng cấp `app.js`: Tự động nhận diện trường hợp người dùng chỉ nạp ảnh mà không gõ đề bài, bổ sung câu lệnh rõ ràng yêu cầu AI đọc và trích xuất đề bài từ ảnh. Đồng bộ nạp API key từ `user_gemini_keys.php` và các storage key thông dụng.
   - Thêm cơ chế Client-Side Direct Fallback: Nếu backend PHP báo lỗi hoặc timeout, client tự động dùng key của người dùng gọi trực tiếp Gemini REST API.
   - Cải thiện thông báo lỗi rõ ràng trên UI (hiển thị đúng mã lỗi HTTP và nguyên nhân thay vì chỉ báo chung chung "không phản hồi").

2. **Thêm Phân hệ Vẽ hình cực kỳ chính xác vào Trợ lý Thiên**:
   - Nâng cấp Menu Cấp 1 của Trợ lý Thiên từ 10 lên 11 nhánh: Thêm `"11/ Vẽ hình học cực kỳ chính xác (từ đề bài / ảnh)"`.
   - Tạo cấu trúc thư mục chuẩn trong `TROLYTHIEN/11_VE_HINH/`:
     + `TROLYTHIEN/11_VE_HINH/Dau_vao/` (chứa file ảnh .png, .jpg, file text/docx chứa đề bài).
     + `TROLYTHIEN/11_VE_HINH/Ket_qua/` (chứa các file kết quả: `.svg`, `_geogebra.txt`, `.html`).
     + `TROLYTHIEN/11_VE_HINH/HUONG_DAN_VE_HINH.md` (hướng dẫn quy chuẩn hình học toán học).
   - Xây dựng quy chuẩn giải tích tọa độ chính xác tuyệt đối:
     + Tọa độ toán học giải tích: Hệ trục Oxy chuẩn, tính toán tọa độ giao điểm, tiếp điểm, trung điểm, trực tâm, trọng tâm bằng công thức giải tích chuẩn xác 100%, không vẽ ước lượng hay áng chừng.
     + Ký hiệu sư phạm GDPT 2018: Đoạn thẳng, góc vuông, góc bằng nhau, cạnh bằng nhau, nhãn đỉnh A, B, C... rõ ràng, không bị đè chữ lên nét vẽ.
     + Xuất trọn bộ 3 sản phẩm đầu ra vào `TROLYTHIEN/11_VE_HINH/Ket_qua/`:
       1. File vector standalone `[Ten_Hinh].svg` sắc nét, dễ chèn vào Word/PowerPoint.
       2. File kịch bản `[Ten_Hinh]_geogebra.txt` gồm các lệnh GeoGebra chuẩn (Point, Segment, Circle, Intersect...) nạp trực tiếp vào GeoGebra.
       3. File standalone `[Ten_Hinh].html` xem trước trực quan có nhúng SVG, công cụ tải ảnh PNG/SVG và copy lệnh GeoGebra.
   - Cập nhật quy tắc `.agents/rules/tro-ly-thien.md` và quy trình `.agents/workflows/thien.md` tương thích 11 nhánh.
   - Cung cấp liên kết trực tiếp tới website `vehinh.html` và file cục bộ `file:///.../vehinh.html` khi cần chỉnh sửa tương tác.

## Ngoài phạm vi
- Không can thiệp vào các logic quản lý văn bản, điểm số, trộn đề khác ngoài tác vụ vẽ hình.
- Không xóa bỏ các tính năng thủ công hiện có trên canvas của `vehinh.html` (thước, bút, tẩy, undo/redo).

## File dự kiến tác động
1. `api/vehinh_ai.php` (sửa danh mục model, bỏ thinkingConfig gây lỗi, tăng timeout cURL, cải thiện xử lý ảnh).
2. `vehinh.html` (cập nhật danh sách lựa chọn model chuẩn, nạp key an toàn).
3. `app.js` (cập nhật model catalog, xử lý prompt khi chỉ có ảnh, đồng bộ key, thêm client fallback).
4. `.agents/rules/tro-ly-thien.md` (nâng cấp Menu 11 lựa chọn, quy định thư mục `TROLYTHIEN/11_VE_HINH/`, quy chuẩn hình học).
5. `.agents/workflows/thien.md` (nâng cấp Menu 11 lựa chọn, kịch bản Nhánh 11 nhận diện đề bài từ chat hoặc ảnh trong `Dau_vao`).
6. `TROLYTHIEN/11_VE_HINH/Dau_vao/.gitkeep` (tạo thư mục đầu vào).
7. `TROLYTHIEN/11_VE_HINH/Ket_qua/.gitkeep` (tạo thư mục kết quả).
8. `TROLYTHIEN/11_VE_HINH/HUONG_DAN_VE_HINH.md` (tài liệu quy chuẩn prompt và giải tích vẽ hình cực kỳ chính xác).
9. `tests/vehinh-boot-smoke.js` (cập nhật kiểm thử cho danh mục model và API mới).
10. `tests/trolythien-bai-giang-html-smoke.js` (cập nhật kiểm thử khớp số lượng 11 nhánh của Trợ lý Thiên).
11. `tests/trolythien-vehinh-smoke.js` (tạo test tự động kiểm tra tính toàn vẹn của Phân hệ Vẽ hình 11).

## Các bước thực hiện
1. **Bước 1: Sửa Backend `api/vehinh_ai.php`**
   - Đặt `gemini-2.5-flash` làm model mặc định tối ưu nhất, bổ sung `gemini-2.5-pro`, `gemini-2.0-flash`.
   - Bỏ hoặc điều kiện hóa `thinkingConfig` (không gửi cho các model không hỗ trợ để tránh mã lỗi 400).
   - Tăng cURL timeout lên 90s–120s trong `vehinh_post_json`.
   - Chuẩn hóa prompt hệ thống khi nhận diện ảnh hình học, yêu cầu bóc tách rõ dữ kiện hình học và tọa độ.
2. **Bước 2: Cập nhật Giao diện & Xử lý Client trong `vehinh.html` và `app.js`**
   - Đổi danh sách model hiển thị trong `<select id="ai-model-select">` sang các model thực tế hoạt động (`gemini-2.5-flash` là mặc định khuyên dùng).
   - Cập nhật `DRAWING_AI_MODEL_CATALOG` và `getDefaultDrawingAiConfig()` trong `app.js`.
   - Trong `handleGenerateClick`: khi người dùng chỉ nạp ảnh mà không gõ prompt, tự động gán câu lệnh trích xuất đề bài từ ảnh.
   - Thêm logic nạp key dự phòng từ `api/user_gemini_keys.php` và `khbd_user_gemini_keys_*`.
   - Thêm client direct fallback gọi Gemini nếu `api/vehinh_ai.php` gặp lỗi mạng hoặc 502.
3. **Bước 3: Khởi tạo Cấu trúc Phân hệ `TROLYTHIEN/11_VE_HINH/`**
   - Tạo thư mục `TROLYTHIEN/11_VE_HINH/Dau_vao/` và `TROLYTHIEN/11_VE_HINH/Ket_qua/`.
   - Tạo file hướng dẫn `TROLYTHIEN/11_VE_HINH/HUONG_DAN_VE_HINH.md` thiết lập quy tắc tính toán giải tích tọa độ Cartesian, quy ước ký hiệu toán học, cấu trúc SVG và GeoGebra commands.
4. **Bước 4: Nâng cấp Trợ lý Thiên trong Rules & Workflows**
   - Sửa `.agents/rules/tro-ly-thien.md`:
     + Menu cấp 1 tăng từ 10 lên 11 nhánh (`"11/ Vẽ hình học cực kỳ chính xác (từ đề bài / ảnh)"`).
     + Bổ sung Mục 4 quy ước thư mục cho Nhánh 11 (`TROLYTHIEN/11_VE_HINH/Dau_vao/` và `TROLYTHIEN/11_VE_HINH/Ket_qua/`).
     + Bổ sung Mục 6 quy chuẩn kỹ thuật cho Nhánh 11 (tính toán giải tích chính xác, 3 định dạng xuất SVG + GeoGebra + HTML).
   - Sửa `.agents/workflows/thien.md`:
     + Cập nhật bảng chọn 11 nhánh.
     + Thêm chi tiết `#### Nhánh 11: Khi chọn "11/ Vẽ hình học cực kỳ chính xác (từ đề bài / ảnh)"` hướng dẫn nhận đề từ chat hoặc ảnh trong `Dau_vao/`, xuất kết quả tương ứng.
5. **Bước 5: Viết và Cập nhật Test Suites Tự động**
   - Cập nhật `tests/vehinh-boot-smoke.js` với các model chuẩn mới.
   - Điều chỉnh `tests/trolythien-bai-giang-html-smoke.js` để hỗ trợ menu 11 nhánh.
   - Tạo file test mới `tests/trolythien-vehinh-smoke.js` kiểm tra menu 11 nhánh, đường dẫn thư mục, format file kết quả.
   - Chạy kiểm thử tự động xác nhận 100% PASS.

## Rủi ro
- Ảnh chụp đề bài chất lượng thấp (mờ, nghiêng, thiếu sáng): Cần prompt hướng dẫn AI yêu cầu người dùng xác nhận hoặc làm rõ dữ kiện nếu thông tin bị thiếu.
- Bài toán hình học không gian phức tạp: Cần quy định góc nhìn phối cảnh chuẩn (ví dụ hình chóp, hình lăng trụ với nét đứt khuất chính xác).

## Cách kiểm thử
1. **Kiểm thử `vehinh.html`**:
   - Mở `vehinh.html` trên trình duyệt:
     + Chọn model `gemini-2.5-flash`.
     + Nạp ảnh đề bài hình học (như ảnh bài hình bình hành trong yêu cầu của người dùng).
     + Nhấn "Vẽ Hình (Ctrl+Q)" -> Kiểm tra hệ thống nhận diện đúng đề bài từ ảnh, không còn báo lỗi "AI vẽ hình không phản hồi", hiển thị phân tích AI và dựng hình chính xác lên canvas Fabric.js và khung GeoGebra.
2. **Kiểm thử Trợ lý Thiên (`/thien`)**:
   - Gọi `/thien`: Menu hiển thị đầy đủ 11 lựa chọn.
   - Chọn "11/ Vẽ hình học cực kỳ chính xác (từ đề bài / ảnh)":
     + Thử nghiệm với đề bài dạng văn bản dán vào chat.
     + Thử nghiệm với file ảnh đặt trong `TROLYTHIEN/11_VE_HINH/Dau_vao/`.
     + Kiểm tra kết quả sinh ra trong `TROLYTHIEN/11_VE_HINH/Ket_qua/` gồm đủ `.svg`, `_geogebra.txt`, `.html`.
3. **Chạy các smoke tests tự động**:
   - `python -c "import subprocess; ..."` hoặc chạy qua runner kiểm tra cấu trúc file và cú pháp.

## Tiêu chí nghiệm thu
- Không còn lỗi "AI vẽ hình không phản hồi" trên `vehinh.html` khi nhập đề bài hoặc tải ảnh đề bài.
- `vehinh.html` sử dụng danh mục model Gemini chuẩn (`gemini-2.5-flash` làm mặc định), timeout đủ dài, tự động nhận diện ảnh khi không có chữ.
- Trợ lý Thiên có menu 11 nhánh hoàn chỉnh, có phân hệ `TROLYTHIEN/11_VE_HINH/` với quy trình nhận diện đề bài từ chat hoặc ảnh trong `Dau_vao/` và xuất kết quả chính xác toán học (SVG, GeoGebra, HTML).
- Toàn bộ các bài kiểm thử tự động liên quan đều PASS.
