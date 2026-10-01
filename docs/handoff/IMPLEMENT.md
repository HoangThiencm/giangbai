# IMPLEMENT: Nhánh 12 — Chuẩn hoá văn bản (Hành chính / Đảng)

## Đã làm
1. Menu Cấp 1 trong `.agents/workflows/thien.md` và `.agents/rules/tro-ly-thien.md` lên 12 lựa chọn, thêm `12. "12/ Chuẩn hoá văn bản (Hành chính / Đảng)"`.
2. Workflow có kịch bản Nhánh 12: đọc `.docx` tại `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/Dau_vao/`, thẩm định theo Master Prompt, phản hồi 5 phần, xuất `Ket_qua/[Ten_File]_Chuan_Hoa.docx`.
3. Rules có thư mục quy ước Nhánh 12 và mục `## 7. Quy chuẩn kỹ thuật cho Nhánh 12` (Times New Roman 13pt, thụt 1,27 cm, lề A4, `cantSplit`, `tblHeader`, lọc chính quyền 2 cấp). Mục dọn rác chuyển thành mục 8.
4. Tạo `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/Dau_vao/.gitkeep`, `Ket_qua/.gitkeep`, `HUONG_DAN_CHUAN_HOA_VAN_BAN.md`, `PROMPT_CHUAN_HOA_VAN_BAN.md` (mục A–I).
5. Smoke: `tests/trolythien-bai-giang-html-smoke.js` và `tests/trolythien-vehinh-smoke.js` kỳ vọng 12 lựa chọn. Thêm `tests/trolythien-chuan-hoa-van-ban-smoke.js`.

## Kiểm thử
- `node tests/trolythien-chuan-hoa-van-ban-smoke.js` — PASS
- `node tests/trolythien-bai-giang-html-smoke.js` — PASS
- `node tests/trolythien-vehinh-smoke.js` — PASS

## Ngoài phạm vi
Không sửa logic nhánh 1–11. Không thêm script xuất Word ngoài workflow/rules/prompt. Chưa commit, chưa push.

## Bàn giao
Plan xong. Mở Antigravity IDE, chat mới: `/verify`
