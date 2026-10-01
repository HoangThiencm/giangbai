# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Khắc phục triệt để lỗi ngắt dòng Quốc hiệu và Tên cơ quan cấp trên: Đặt cố định bảng Header 2 cột (trái 65 mm, phải 100 mm), triệt tiêu lề ô (`padding = 0`), khóa thuộc tính `noWrap`, bảo đảm `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM` và `ỦY BAN NHÂN DÂN XÃ XUÂN ĐÔNG` nằm trọn vẹn trên 1 dòng duy nhất: ĐẠT.
- Thay thế toàn bộ ký tự gạch chân/underline bằng đường kẻ đồ họa vector thật (`v:line` chuẩn OpenXML stroke 0.75pt, nét liền đen, căn giữa) dưới Tên cơ quan (~28 mm), Tiêu ngữ (~38 mm) và Trích yếu Kế hoạch (~45 mm): ĐẠT.
- Bổ sung đường kẻ ngang nét liền dưới trích yếu Kế hoạch theo đúng Nghị định 30/2020/NĐ-CP (Phụ lục I, Mục II, Điểm 6b): ĐẠT.
- Xóa bỏ đoạn văn rỗng giữa trích yếu và Căn cứ, chuẩn hóa khoảng cách dãn đoạn: ĐẠT.
- Chuẩn hóa cỡ chữ bảng biểu lên 11.5pt, đóng khung kín 4 cạnh, khóa `cantSplit` cho 100% các hàng và `tblHeader` cho dòng tiêu đề: ĐẠT.
- Lược bỏ báo cáo 5 phần dài dòng trong chat; tinh gọn phản hồi thành thông báo ngắn gọn 2–3 dòng kèm link mở file Word trực tiếp: ĐẠT.
- Cập nhật đồng bộ `PROMPT_CHUAN_HOA_VAN_BAN.md`, `HUONG_DAN_CHUAN_HOA_VAN_BAN.md`, `thien.md`, `tro-ly-thien.md` và kiểm thử tự động: ĐẠT.

## Test đã chạy
1. `python tools/standardize_kh_dayhoc.py` — SUCCESS (tái tạo file Word chuẩn hóa tại `Ket_qua/`)
2. `node tests/trolythien-chuan-hoa-van-ban-smoke.js` — PASS
3. `node tests/trolythien-bai-giang-html-smoke.js` — PASS
4. `node tests/trolythien-vehinh-smoke.js` — PASS

## Pass / Fail từng tiêu chí
1. Quốc hiệu và Tên cơ quan cấp trên nằm trọn vẹn trên 1 dòng duy nhất, không rớt chữ: PASS.
2. Các đường kẻ là đối tượng vector graphic line `v:line` thực thụ, không dùng text dash hay underline: PASS.
3. Kế hoạch có đường kẻ ngang dưới trích yếu đúng chuẩn NĐ 30/2020: PASS.
4. Khoảng cách giữa trích yếu và căn cứ liền mạch, không có paragraph rỗng: PASS.
5. Cỡ chữ bảng biểu đạt 11.5pt, chống xé dòng `cantSplit`: PASS.
6. Chat tinh gọn, không tuôn báo cáo dài: PASS.
7. Toàn bộ smoke test đều PASS 100%: PASS.

## Bug
Không phát hiện lỗi.
