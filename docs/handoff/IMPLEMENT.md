# IMPLEMENT: Chuẩn hóa KHBD V2.0 (NLS/AI, hình vẽ, công thức)

## Đã làm
- Khóa ma trận sư phạm trong `.agents/rules/soankhbd.md`, `PROMPT_SOAN_GIAO_AN.md` và `HUONG_DAN_SOAN_KHBD_HANG_LOAT.md`: chỉ tích hợp NLS/AI khi cột Ghi chú PPCT có mã; bài số học lý thuyết không chèn ảnh; Mindmap chỉ ở Hoạt động 2.1 của tiết luyện tập chung / ôn tập; checklist trước khi xuất.
- `sanitizeKhbdMathSource` trong `TROLYTHIEN/engine/export_khbd_engine.js`: khôi phục Vertical Tab + `dots` thành `\vdots`, Form Feed + `rac` thành `\frac`, xóa ký tự điều khiển, rút `\ \vdots \` về `\vdots`, đổi `dots` giữa hai toán hạng thành `\vdots`, đổi `\not\vdots` thành `\nmid`. Cảnh báo khi Word khóa file (ghi `_Moi.docx`).
- `js/khbd-docx.js` dùng cùng lớp lọc trước `latexToUnicodeMath` và `normalizeLatexForMath`. Equation giữ `⋮` (U+22EE).
- `tools/export_all_8_khbd.js` cảnh báo khi đường dẫn ra là `_Moi.docx`.
- Ba bài 03, 04, 08 đổi dòng tích hợp sang `***(Tích hợp NLS …)***` và `***(Tích hợp AI …)***`. Năm bài còn lại không có dòng đó. Ảnh Mindmap chỉ còn ở bài 01, 02, 06.

## Kiểm thử
- `node tests/khbd-math-sanitize-smoke.js`: PASS (chuỗi `$36 \vdots x$`, `$48 \dots x$`, `100 - x \dots 4`, `a \not\vdots b`, `\frac{24}{108}`, VT/`dots`, FF/`frac`, và đối chiếu 8 file Markdown).
- `node tools/export_all_8_khbd.js`: 8/8 ghi đè thành công, không bị EBUSY.
- Giải nén `word/document.xml`: không file nào còn chữ `dots`. Số `m:oMath` và `⋮`: 01 (27/0), 02 (41/0), 03 (84/14), 04 (41/2), 05 (28/0), 06 (39/9), 07 (74/3), 08 (79/1). Bài 01 và 02 không có phép chia hết nên không có `⋮`.

## Chưa kiểm
- Chưa mở 8 file trên Microsoft Word (viền, lề, ngắt dòng). Phần này để `/verify`.

## Việc tiếp
- Antigravity, chat mới: `/verify`.
