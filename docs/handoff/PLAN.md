# PLAN

## Hiện trạng
1. **Khảo sát thiết bị phần cứng (Cây bút trình chiếu / Bút tương tác):**
   - Thiết bị trong ảnh là bút trình chiếu / bút bảng tương tác thông minh kết nối máy tính qua USB receiver (2.4GHz) hoặc Bluetooth theo chuẩn USB HID.
   - Nút khoanh đỏ có ký hiệu chữ **`T`** (thường biểu thị Text, Timer, Tab, hoặc nút chức năng phụ trên thiết bị thuyết trình).
   - Khi bấm nút này, phần cứng phát ra tín hiệu bàn phím tiêu chuẩn (mã phím `t` / `T` - `keyCode: 84`, `code: KeyT` hoặc `Tab` / `ContextMenu`) hoặc sự kiện chuột phụ (Right Click / Barrel Button).

2. **Khảo sát mã nguồn HTML hiện tại (`TROLYTHIEN/10_BAI_GIANG_HTML/`):**
   - File template gốc: `TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html` (dòng 4708-4712) và file bài dạy thực tế `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html` (dòng 8958-8960):
     - Sự kiện `keydown` hiện đang gán cố định phím `t` / `T` để mở modal Đồng hồ đếm ngược (`toggleTimerModal()`).
   - File template gốc (dòng 5296-5339) và file Bài 12 (dòng 9540-9583):
     - Menu Chuột Phải Sư Phạm (`#contextMenu`) hiện chỉ mở thông qua sự kiện chuột phải vật lý `window.addEventListener('contextmenu', ...)` hoặc nhấn giữ cảm ứng.
     - Chưa có cơ chế cho phép kích hoạt Menu Chuột Phải Sư Phạm thông qua phím tắt trên bút trình chiếu hoặc phím `T`.
     - Chưa lưu vết tọa độ con trỏ liên tục (`lastPointerX`, `lastPointerY`) khiến việc gọi mở menu từ phím tắt chưa định vị được chính xác vị trí con trỏ chuột/ngòi bút.

## Phạm vi
- Cấu hình và thiết kế lại cơ chế tiếp nhận sự kiện trong bài giảng HTML để nút khoanh đỏ (phím `T` / `ContextMenu` / `barrel button`) trên cây bút hoạt động như **Chuột Phải** (kích hoạt Menu Chuột Phải Sư Phạm).
- Bổ sung bộ theo dõi tọa độ con trỏ (`mousemove` / `pointermove`) để Menu Chuột Phải mở ra chuẩn xác ngay tại vị trí trỏ chuột / ngòi bút hiện tại (hoặc tâm màn hình nếu chưa có tọa độ di chuyển).
- Bổ sung cơ chế Bật/Tắt (Toggle): Nhấn nút `T` lần 1 mở menu; nhấn lần 2 (hoặc `Escape` / click ngoài) tự động đóng menu.
- Giữ nguyên các chức năng trong Menu Chuột Phải (Laser, Bút vẽ, Dạ quang, Xóa nét, Bảng viết, Đồng hồ, Đọc bài, Chuyển bước). Đồng hồ đếm giờ chuyển vào làm 1 mục trong Menu Chuột Phải và trên thanh công cụ.
- Áp dụng thay đổi cho:
  + `TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html`
  + `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html`
  + `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html`
  + Cập nhật quy chuẩn kỹ thuật tại `TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md` (mục Vá 24 & Vá 28).

## Ngoài phạm vi
- Không nạp lại firmware hoặc can thiệp vi mạch phần cứng của cây bút.
- Không thay đổi các chức năng khác không liên quan đến trình chiếu bài giảng HTML.

## File dự kiến tác động
1. `TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html`
2. `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html`
3. `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html`
4. `TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md`

## Các bước thực hiện
1. **Lưu vết tọa độ con trỏ (Pointer Tracking):**
   - Thêm biến toàn cục `let lastPointerX = window.innerWidth / 2; let lastPointerY = window.innerHeight / 2;`
   - Bắt sự kiện `window.addEventListener('mousemove', ...)` và `window.addEventListener('pointermove', ...)` cập nhật `lastPointerX`, `lastPointerY`.
2. **Xây dựng hàm mở/đóng Menu Chuột Phải linh hoạt (`toggleContextMenuAt(x, y)`):**
   - Kiểm tra trạng thái `#contextMenu`: nếu đang hiển thị (`display === 'flex'`) thì đóng lại (`hideContextMenu()`).
   - Nếu đang đóng: tính toán tọa độ an toàn (tránh tràn mép phải và đáy màn hình), cập nhật trạng thái các nút (Laser, Bút vẽ), hiển thị menu tại `(x, y)`.
3. **Tái cấu trúc bộ xử lý phím `keydown`:**
   - Khi nhận phím `t`, `T`, hoặc `ContextMenu`:
     - Nếu đang focus trong ô nhập liệu (`input`, `textarea`, `contenteditable="true"`), bỏ qua để giáo viên gõ chữ bình thường.
     - Nếu không trong ô nhập liệu: gọi `e.preventDefault()`, sau đó gọi `toggleContextMenuAt(lastPointerX, lastPointerY)`.
4. **Đồng bộ hóa các file bài giảng:**
   - Cập nhật code tương ứng vào `master_lecture_template.html` và các file HTML bài giảng mẫu trong thư mục `Ket_qua/`.
5. **Cập nhật quy chuẩn thiết kế:**
   - Cập nhật `PROMPT_TAO_BAI_GIANG_HTML.md` ghi rõ: Nút `T` trên bút trình chiếu được map làm phím tắt tương đương Chuột Phải (Quick Context Menu).

## Rủi ro
1. **Xung đột khi soạn thảo văn bản:** Nếu người dùng đang chỉnh sửa trực tiếp nội dung slide (chế độ Thiết kế) và gõ chữ "t" hoặc "T".
   - *Biện pháp:* Điều kiện lọc `if (e.target.closest('input, textarea, [contenteditable="true"]')) return;` ngăn chặn triệt để, cho phép gõ ký tự "t" bình thường.
2. **Tọa độ hiển thị menu khi chưa di chuột:** Khi bài giảng vừa mở và giáo viên chưa chạm chuột, tọa độ có thể là (0, 0).
   - *Biện pháp:* Khởi tạo tọa độ mặc định ở giữa màn hình (`innerWidth / 2`, `innerHeight / 2`).

## Cách kiểm thử
1. Mở bài giảng `Bai_12...html` hoặc `master_lecture_template.html` trên trình duyệt Edge / Chrome.
2. Di chuột đến một vị trí bất kỳ trên slide, bấm phím `T` trên bàn phím (hoặc bấm nút khoanh đỏ trên cây bút): Menu Chuột Phải Sư Phạm xuất hiện ngay tại vị trí trỏ chuột.
3. Bấm lại phím `T`: Menu Chuột Phải đóng lại.
4. Click chuột phải bằng chuột máy tính: Menu Chuột Phải vẫn xuất hiện bình thường.
5. Click vào chế độ Thiết kế, click vào tiêu đề văn bản, gõ phím `T`: chữ "T" xuất hiện vào nội dung văn bản, không bị kích hoạt menu.

## Tiêu chí nghiệm thu
- Bấm nút khoanh đỏ (`T`) trên cây bút mở/đóng Menu Chuột Phải Sư Phạm mượt mà, đúng tọa độ.
- Các nút chức năng trong menu (Laser, Bút vẽ, Dạ quang, Xóa nét, Bảng viết, Đồng hồ đếm giờ) hoạt động chính xác khi chọn.
- Không gây xung đột khi gõ chữ và không phá vỡ các phím điều hướng slide khác.
