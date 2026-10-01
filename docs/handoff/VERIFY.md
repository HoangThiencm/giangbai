# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Khởi tạo đầy đủ thư mục `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/Dau_vao/` và `Ket_qua/` kèm `.gitkeep`: ĐẠT.
- Tạo tài liệu `HUONG_DAN_CHUAN_HOA_VAN_BAN.md` và Master Prompt `PROMPT_CHUAN_HOA_VAN_BAN.md` (đủ 9 phần A–I, tích hợp bộ lọc mô hình 2 cấp chính quyền): ĐẠT.
- Nâng cấp Menu Cấp 1 trong `.agents/workflows/thien.md` và `.agents/rules/tro-ly-thien.md` lên đúng 12 lựa chọn, tích hợp `12. "12/ Chuẩn hoá văn bản (Hành chính / Đảng)"`: ĐẠT.
- Workflow và Rules bổ sung quy trình chuẩn hoá tệp Word `.docx` đầu vào, thẩm định thể thức theo NĐ 30/2020/NĐ-CP hoặc QĐ 399-QĐ/TW (HD 05-HD/VPTW), trả kết quả 5 phần và xuất file Word `.docx` thành phẩm tại `Ket_qua/`: ĐẠT.
- Cập nhật smoke tests hiện có (`trolythien-bai-giang-html-smoke.js`, `trolythien-vehinh-smoke.js`) và thêm test mới `trolythien-chuan-hoa-van-ban-smoke.js`: ĐẠT.

## Test đã chạy
1. `node tests/trolythien-chuan-hoa-van-ban-smoke.js` — PASS
2. `node tests/trolythien-bai-giang-html-smoke.js` — PASS
3. `node tests/trolythien-vehinh-smoke.js` — PASS

## Pass / Fail từng tiêu chí
1. Menu Cấp 1 có đúng 12 lựa chọn trong workflow và rules: PASS.
2. Thư mục `Dau_vao` và `Ket_qua` của Nhánh 12 tồn tại: PASS.
3. Master Prompt chứa đầy đủ 9 phần (A, B, C, D, E, F, G, H, I): PASS.
4. Quy chuẩn kỹ thuật in ấn (Times New Roman 13pt, thụt dòng 1,27 cm, lề A4, `cantSplit`, `tblHeader`): PASS.
5. Không làm hồi quy các nhánh 10 và 11: PASS.

## Bug
Không phát hiện lỗi.
