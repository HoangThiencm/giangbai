# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Mục 1: Khóa ma trận sư phạm và đồng bộ quy chuẩn tích hợp NLS/AI đúng 100% theo PPCT (chỉ 3 bài 03, 04, 08 có mã; 5 bài còn lại để trống).
- [x] Mục 2: Sơ đồ tư duy (Mindmap) đã được chuyển ra ngoài bảng, đặt độc lập tại mục b) Nội dung của Hoạt động 2.1 (01, 02, 06); bảng mục d) sạch sẽ không bị chèn hình làm méo cột. Các bài số học lý thuyết không có hình thừa.
- [x] Mục 3: Xử lý triệt để lỗi phân số `\frac` bị rụng `\f` thành `rac` (ví dụ `rac24108` $\rightarrow$ phân số $\frac{24}{108}$). Đã khôi phục toàn bộ 38 phân số trong Bài 11 (`KHBD_07`) và Bài 12 (`KHBD_08`) thành cấu trúc Equation Office Math `<m:f>` chuẩn Word với tử số `<m:num>` và mẫu số `<m:den>`.
- [x] Mục 4: Ký hiệu chia hết `\vdots` hiển thị đúng `⋮` (U+22EE), không có chữ `dots` hay ký tự rác `v`.
- [x] Mục 5: Xuất thành công toàn bộ 8 file Word `.docx` vào `TROLYTHIEN/1_SOAN_KHBD/Ket_qua/` chuẩn Công văn 5512 V2.0.

## Test đã chạy
1. `node tests/khbd-math-sanitize-smoke.js`: PASS (bao gồm các test case phục hồi `\frac`, `rac{...}`, `frac{...}`, `\vdots`, `\nmid`).
2. `node tools/export_all_8_khbd.js`: Xuất 8/8 file Word thành công không gặp lỗi EBUSY.
3. Kiểm tra XML giải nén `word/document.xml`:
   - Phân số toán học `<m:f>`: Bài 07 có 12 phân số chuẩn; Bài 08 có 26 phân số chuẩn.
   - Số chữ rác `rac`: 0 ở tất cả 8 file.
   - Số chữ rác `dots`: 0 ở tất cả 8 file.
   - Ký tự rác `<m:t>v</m:t>`: 0 ở tất cả 8 file.

## Pass / Fail từng tiêu chí
- [x] Tiêu chí 1: Phân số hiển thị dạng phân số toán học thực sự $\frac{a}{b}$ (thẻ `<m:f>`), không hiển thị chuỗi dính liền `rac24108`. PASS.
- [x] Tiêu chí 2: Phân bố NLS/AI đúng PPCT (chỉ 3 bài 03, 04, 08; in đậm in nghiêng). PASS.
- [x] Tiêu chí 3: Mindmap chỉ đặt tại mục b) Nội dung (ngoài bảng) của 3 bài 01, 02, 06. PASS.
- [x] Tiêu chí 4: Bảng 2 cột lề 0pt, chuẩn Công văn 5512 V2.0. PASS.
- [x] Tiêu chí 5: Ký hiệu chia hết `⋮` chuẩn xác. PASS.

## Bug
Không còn tồn tại bug nào.
