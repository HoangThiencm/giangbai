# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Sửa lỗi vẽ hình AI trên `vehinh.html`**:
   - `api/vehinh_ai.php`: Danh mục model chuyển sang các model thực tế gồm `gemini-2.5-flash` (mặc định), `gemini-2.5-pro`, `gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-1.5-flash`. Loại bỏ `gemini-3.6-flash`, `gemini-3.7-flash`, `gemini-3-flash-preview` khỏi danh sách gọi.
   - `api/vehinh_ai.php`: `thinkingConfig` có điều kiện thông qua `vehinh_model_supports_thinking`, không gửi cho model không hỗ trợ tránh lỗi HTTP 400. cURL timeout tăng lên 120s. Bổ sung prompt xử lý ảnh đề bài.
   - `vehinh.html`: Danh mục dropdown cập nhật model chuẩn, `gemini-2.5-flash` làm mặc định khuyên dùng.
   - `app.js`: Tự động nhận diện trường hợp chỉ có ảnh mà không có prompt chữ, gửi chỉ dẫn đọc và bóc tách đề bài từ ảnh. Quét nạp key từ `user_gemini_keys.php`, `global_gemini_keys` và `khbd_user_gemini_keys_*`. Tích hợp client-side direct fallback tự động gọi trực tiếp Gemini API khi backend lỗi mạng/timeout/5xx.
   - Cú pháp `app.js` chuẩn xác (`node --check app.js` PASS).

2. **Thêm chức năng vẽ hình cực kỳ chính xác vào Trợ lý Thiên**:
   - `.agents/rules/tro-ly-thien.md`: Menu Cấp 1 tăng lên 11 lựa chọn (thêm nhánh "11/ Vẽ hình học cực kỳ chính xác (từ đề bài / ảnh)"). Quy định thư mục làm việc tại `TROLYTHIEN/11_VE_HINH/Dau_vao/` và `TROLYTHIEN/11_VE_HINH/Ket_qua/`. Quy chuẩn kỹ thuật Mục 6 yêu cầu tính tọa độ giải tích Oxy và xuất đủ 3 file `.svg`, `_geogebra.txt`, `.html`.
   - `.agents/workflows/thien.md`: Bảng chọn menu 11 lựa chọn, quy trình Nhánh 11 nhận diện đề bài từ chat hoặc ảnh trong thư mục `Dau_vao/`.
   - Cấu trúc thư mục: `TROLYTHIEN/11_VE_HINH/Dau_vao/.gitkeep`, `TROLYTHIEN/11_VE_HINH/Ket_qua/.gitkeep` và tài liệu hướng dẫn `TROLYTHIEN/11_VE_HINH/HUONG_DAN_VE_HINH.md` đã được tạo đầy đủ.

## Test đã chạy
- `& "C:\Users\HoangThien\AppData\Local\Temp\node-portable\node-v20.19.0-win-x64\node.exe" tests/vehinh-boot-smoke.js`: PASS.
- `& "C:\Users\HoangThien\AppData\Local\Temp\node-portable\node-v20.19.0-win-x64\node.exe" tests/trolythien-vehinh-smoke.js`: PASS.
- `& "C:\Users\HoangThien\AppData\Local\Temp\node-portable\node-v20.19.0-win-x64\node.exe" --check app.js`: PASS.

## Pass / Fail từng tiêu chí
- [x] Tiêu chí 1: Không còn lỗi "AI vẽ hình không phản hồi" do model ảo `gemini-3.6-flash`, lỗi 400 của `thinkingConfig` hoặc cURL timeout 30s.
- [x] Tiêu chí 2: Trang `vehinh.html` và `app.js` hỗ trợ đầy đủ xử lý ảnh đề bài khi ô nhập chữ rỗng, có fallback gọi trực tiếp từ trình duyệt khi backend gặp sự cố.
- [x] Tiêu chí 3: Trợ lý Thiên mở rộng menu 11 nhánh tương tác, hỗ trợ tiếp nhận đề bài qua chat hoặc ảnh trong thư mục `TROLYTHIEN/11_VE_HINH/Dau_vao/`.
- [x] Tiêu chí 4: Quy chuẩn xuất kết quả giải tích chính xác toán học gồm 3 file (`.svg`, `_geogebra.txt`, `.html`) tại `TROLYTHIEN/11_VE_HINH/Ket_qua/`.
- [x] Tiêu chí 5: Các bài kiểm thử phạm vi plan (`vehinh-boot-smoke.js`, `trolythien-vehinh-smoke.js`, cú pháp `app.js`) đạt 100% PASS.

## Bug
Không phát hiện bug mới trong phạm vi thay đổi của PLAN.
