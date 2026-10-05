# IMPLEMENT

Nút chữ T trên bút trình chiếu mở và đóng Menu Chuột Phải Sư Phạm tại vị trí con trỏ. Đồng hồ đếm giờ vẫn là một mục trong menu và một nút trên thanh công cụ. Phím T không mở thẳng đồng hồ.

## Đã làm

- `TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html`
- `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html`
- `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html`
- `TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md` (Vá 24, Vá 28, và câu phím T ở Vá 29)

1. `lastPointerX` / `lastPointerY` bắt đầu ở tâm cửa sổ và cập nhật bằng `mousemove` cùng `pointermove`.
2. `toggleContextMenuAt(x, y)` đóng menu khi đang `display: flex`, không thì mở tại tọa độ đã kẹp trong màn hình. Chuột phải gọi `showContextMenuAt` nên vẫn hiện menu.
3. Phím `t`, `T`, `ContextMenu` gọi toggle. Ô `input`, `textarea`, `[contenteditable="true"]` vẫn gõ chữ T bình thường. `Escape` và click ngoài vẫn đóng menu.
4. Menu giữ Laser, Bút vẽ, Dạ quang, Xóa nét, Bảng viết, Đọc bài, Tiến/Lùi. Template và Bài 12 có thêm mục Đồng hồ. Nút `⏱️` trên `#controlBar` vẫn gọi `toggleTimerModal()`.

## Kiểm thử

- `node tests/trolythien-template-smoke.js`: PASS
- `node tests/trolythien-bai-giang-html-smoke.js`: PASS
- Chưa mở trình duyệt. Bấm phím T, chuột phải, và gõ T trong chế độ Thiết kế để Antigravity `/verify`.

## Giới hạn

- Bài 4 có nút `⏱️ Đếm ngược` trên thanh nhưng không có `toggleTimerModal` hay modal đồng hồ. Không thêm cả cụm đồng hồ vì nằm ngoài các bước của plan. Menu Bài 4 có Bảng viết, chưa có mục Đồng hồ.
