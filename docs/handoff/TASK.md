# TASK: MP-01 — Mô phỏng cắt ghép diện tích hình bình hành thành hình chữ nhật (MVP Tầng 1)

## 1. Mô tả yêu cầu
Xây dựng và phản biện kiểm thử mô phỏng hình học tương tác offline: **MP-01 — Cắt ghép diện tích hình bình hành thành hình chữ nhật** thuộc Nhánh 2: Tạo bài tập & Học liệu tương tác (Trợ lý Sư phạm Hoàng Thiên).

Mô phỏng phục vụ giảng dạy Bài 20, Toán 6 Tập một (Bộ sách Kết nối tri thức với cuộc sống), bám sát hoạt động khám phá HĐ1 (Tr. 92, PDF 93) và HĐ2 (Tr. 93, PDF 94):
1. **Khám phá bảo toàn diện tích:** Cắt tam giác vuông bên trái của hình bình hành, trượt ngang sang phải để ghép khít vào phần khuyết bên phải tạo thành hình chữ nhật.
2. **Khám phá công thức $S = a \cdot h$:** So sánh kích thước hình chữ nhật mới với đáy $a$ và chiều cao $h$ của hình bình hành ban đầu.

## 2. File và phạm vi liên quan
- **Mã nguồn HTML chính:** `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/MP01_Dien_Tich_Hinh_Binh_Hanh.html`
- **Đặc tả sư phạm 5 trường:** `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/DAC_TA_MO_PHONG_MP01_DIEN_TICH_HINH_BINH_HANH.md`
- **Đặc tả kỹ thuật MVP:** `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/DAC_TA_KY_THUAT_MP01_MVP.md`
- **Quy chuẩn xây dựng mô phỏng (v1.6.0):** `TROLYTHIEN/2_TAO_BAI_TAP/QUY_CHUAN_XAY_DUNG_MO_PHONG.md`
- **Handoff Plan:** `docs/handoff/PLAN.md`

## 3. Ràng buộc kỹ thuật & Sư phạm bắt buộc (Strict Gates)
1. **Single-file HTML Standalone:** Chạy offline qua `file:///`, không thư viện ngoài, không CDN, không Google Fonts (dùng font hệ thống chuẩn).
2. **Hệ tọa độ SVG & Lưới ô vuông:**
   - Đơn vị lưới $u = 50\text{ px}$.
   - Hình bình hành đáy $a = 4\text{ ô} = 200\text{ px}$, chiều cao $h = 3\text{ ô} = 150\text{ px}$, độ lệch ngang $1\text{ ô} = 50\text{ px}$.
   - Tọa độ đỉnh: $D(150, 250), H(200, 250), C(350, 250), A(200, 100), B(400, 100), H'(400, 250)$.
   - Quãng trượt ngang $\Delta X = 200\text{ px} = a$, khóa cứng phương đứng $\Delta Y = 0$.
3. **Cơ chế tương tác Pointer Events:**
   - CSS `touch-action: none;`, `setPointerCapture`.
   - Vùng chạm tay kéo đỏ đường kính $\ge 50\text{ px}$.
   - Bỏ click trên rãnh trượt (chống nhảy cóc).
   - Đạt $100\% \implies$ khóa kéo (`isLocked = true`), giữ hình tĩnh tuyệt đối.
4. **Hộp câu hỏi quan sát trung tính:**
   - 2 nút trung tính: `[ Không thay đổi ]` và `[ Có thay đổi ]`.
   - Không dùng màu xanh lá gợi ý trước đáp án.
   - Sau khi học sinh chọn: hiển thị lời dẫn giải thích khách quan rồi mới hiện công thức $S = a \cdot h$.
5. **Nút Giáo viên:** `[ 🎬 Tự động ghép (GV) ]` chạy mẫu $2.5\text{s}$ bằng `requestAnimationFrame`.

## 4. Mục tiêu phản biện tự động (Dành cho Grok / agy CLI)
- Độc lập kiểm tra và phản biện chéo toàn bộ mã nguồn `MP01_Dien_Tich_Hinh_Binh_Hanh.html` đối chiếu với `DAC_TA_KY_THUAT_MP01_MVP.md`.
- Rà soát các bẫy kỹ thuật: sai số tọa độ, tràn khung SVG, trượt tay kéo trên cảm ứng, mất bóng mờ, lỗi hiển thị Math/công thức.
