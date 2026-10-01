# IMPLEMENT: Sửa thể thức Nhánh 12

## Đã làm
1. `tools/standardize_kh_dayhoc.py` dựng lại `KH_TO_CHUC_DAY_HOC_TRUC_TUYEN_2026_2027_TRANPHU_Chuan_Hoa.docx`.
   - Header cố định: cột trái 65 mm, cột phải 100 mm, lề ô 0. Quốc hiệu 12pt đậm và `ỦY BAN NHÂN DÂN XÃ XUÂN ĐÔNG` 12pt có `noWrap`, mỗi cụm một run.
   - Đường kẻ `v:line` 0.75pt dưới tên đơn vị (~28 mm), tiêu ngữ (~38 mm) và trích yếu (~45 mm). Đã bỏ ký tự `────` và đoạn trống `p_sp2`.
   - Bảng lộ trình 11,5pt, `cantSplit`, `tblHeader`, khung 4 cạnh.
2. Prompt mục H đổi thành phản hồi chat 2–3 dòng. Workflow, rules và hướng dẫn đồng bộ: không xuất báo cáo 5 phần; header một dòng; đường kẻ vector.
3. `tests/trolythien-chuan-hoa-van-ban-smoke.js` kiểm tra quy chuẩn mới và XML của tệp Word.

## Kiểm thử
- `python tools/standardize_kh_dayhoc.py` — SUCCESS
- `node tests/trolythien-chuan-hoa-van-ban-smoke.js` — PASS
- `node tests/trolythien-bai-giang-html-smoke.js` — PASS
- `node tests/trolythien-vehinh-smoke.js` — PASS

## Ngoài phạm vi
Không đổi nội dung chuyên môn của kế hoạch. Không sửa nhánh 1–11. Chưa commit, chưa push.

## Bàn giao
Plan xong. Mở Antigravity IDE, chat mới: `/verify`
