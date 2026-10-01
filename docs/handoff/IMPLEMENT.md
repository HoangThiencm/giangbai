# IMPLEMENT

Đã sửa lỗi AI vẽ hình trên `vehinh.html` và thêm nhánh 11 của Trợ lý Thiên theo PLAN.

## Đã làm

- `api/vehinh_ai.php`: danh mục model là `gemini-2.5-flash` (mặc định), `gemini-2.5-pro`, `gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-1.5-flash`. Ba tên `gemini-3.6-flash`, `gemini-3.7-flash`, `gemini-3-flash-preview` chỉ còn trong danh sách loại trừ. `thinkingConfig.thinkingBudget` chỉ gửi cho `gemini-2.5-flash` và `gemini-2.5-pro`. cURL timeout 120 giây. Ảnh đề bài được kèm chỉ dẫn bóc dữ kiện và tọa độ. Lỗi trả về có mã HTTP upstream.
- `vehinh.html`: hộp chọn model dùng năm model trên, `gemini-2.5-flash` là lựa chọn khuyên dùng.
- `app.js`: cùng danh mục model. Model lưu trong trình duyệt mà không thuộc danh mục được đưa về `gemini-2.5-flash`. Chỉ có ảnh, không có chữ: câu lệnh yêu cầu đọc đề trong ảnh. Key nạp từ `api/user_gemini_keys.php`, `global_gemini_keys` và `khbd_user_gemini_keys_*`. Backend lỗi mạng, timeout hoặc HTTP 5xx thì trình duyệt gọi thẳng Gemini. Thông báo lỗi có mã HTTP.
- Trợ lý Thiên: menu cấp 1 có 11 nhánh. Nhánh 11 là "11/ Vẽ hình học cực kỳ chính xác (từ đề bài / ảnh)" trong `.agents/rules/tro-ly-thien.md` và `.agents/workflows/thien.md`, kèm thư mục `TROLYTHIEN/11_VE_HINH/Dau_vao/`, `Ket_qua/` và `HUONG_DAN_VE_HINH.md`. Kết quả quy định đủ `.svg`, `_geogebra.txt`, `.html`. Có link `vehinh.html`.

## Kiểm thử

- `node tests/vehinh-boot-smoke.js` — PASS
- `node tests/trolythien-vehinh-smoke.js` — PASS
- `node tests/trolythien-bai-giang-html-smoke.js` — chưa PASS hết file. Phần menu 11 nhánh đã qua. File dừng vì thiếu `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Chay_Bai_12_Bang_Edge.bat` (bị `.gitignore`, không có trên đĩa). Đây là hiện trạng có sẵn, ngoài file của plan này.
- `node tests/game-quiz-importer-smoke.js` — dừng ở assertion cũ bắt `api/vehinh_ai.php` phải timeout 30 giây và fallback `gemini-3.6-flash`. Plan này đổi đúng hai chỗ đó. File test không nằm trong danh sách file của plan nên không sửa.
- `node --check app.js` — PASS
- Chưa mở trình duyệt, chưa gọi Gemini thật. Cần `/verify` bấm Vẽ Hình với ảnh đề và model `gemini-2.5-flash`.

## Chưa làm

- Không commit, không push.
