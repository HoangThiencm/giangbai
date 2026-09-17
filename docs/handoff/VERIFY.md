# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Module 1: Chuẩn hóa ký hiệu Hình học Việt Nam: Dấu đồng dạng chữ S nằm ngang `∽` (Unicode `U+223D`), ký hiệu góc `\widehat` và `\hat` giữ nguyên mũ góc qua OMML Accent `<m:acc>`, ký hiệu cung `\wideparen` thành `⌒AB`, ngoặc vuông delimiter `[` cho THPT.
- [x] Module 2: Khắc phục triệt để lỗi Cột 2 bảng mục d) rỗng hoặc chỉ có `---`: prompt yêu cầu Cột 2 bắt buộc có kiến thức ghi bảng; `semanticSplitActivityRow` và `repairActivityTablesRightColumn` tự động bóc tách nội dung ghi bảng (Quy tắc, Ví dụ, Lời giải) từ Cột 1 sang Cột 2 hoặc trích xuất từ `c) Sản phẩm`.
- [x] Module 3: Khắc phục triệt để lỗi Hoạt động 4 (Vận dụng) thiếu 4 phần: prompt siết chặt cấu trúc `### a) b) c) d)` cho Hoạt động C, D; `ensureActivityFourPartStructure` tự động chuẩn hóa `- Mục tiêu:` $\rightarrow$ `### a) Mục tiêu:` và tự động bổ sung `b) Nội dung:`, `c) Sản phẩm:`, `d) Tổ chức thực hiện:` nếu bị thiếu trước bảng.
- [x] Module 4: Chuẩn hóa các quy chuẩn sư phạm Toán học: Cấm dùng ngoặc vuông `[` trong phương trình tích ở cấp THCS (dùng "hoặc" hoặc chia trường hợp), số thập phân dùng dấu phẩy `,`, tọa độ và cặp nghiệm dùng dấu chấm phẩy `;`, hàm lượng giác dùng $\tan, \cot$, hai tam giác đồng dạng viết đúng thứ tự đỉnh tương ứng.

## Test đã chạy
1. `node tests/khbd-table-columns-smoke.js` — PASS:
   - Kiểm tra tỷ lệ cột bảng Word và CSS (66.67% / 33.33%).
   - Cứu hộ Cột 2 rỗng/`---`: bóc tách khối kiến thức bảng từ Cột 1 sang Cột 2 thành công.
   - Khôi phục cấu trúc 4 phần Hoạt động D bị thiếu `b)`, `c)`, `d)` thành công.
2. `node tests/khbd-docx-math-smoke.js` — PASS:
   - Kiểm tra `\backsim` và `\sim` ra chữ S nằm ngang `∽` (`U+223D`), không chứa dấu ngã sóng quốc tế `∼` (`U+223C`).
   - Kiểm tra góc `\widehat{ABC}` tạo OMML `<m:acc>`, cung `\wideparen{AB}` tạo `⌒AB`, ngoặc vuông `\left[` tạo `begChr="["`.
3. `node tests/khbd-activity-b-subsections-smoke.js` — PASS (Ánh xạ tiểu mục SGK và Hoạt động B).
4. `node tests/khbd-activities-ad-standard-smoke.js` — PASS (4 hoạt động A–D chuẩn CV 5512).
5. `node tests/khbd-pedagogy-script-smoke.js` — PASS (Kịch bản sư phạm thực chiến & tương thích DOCX).
6. `node tests/canvas-prompts-integrity-smoke.js` — PASS (Tính toàn vẹn prompt hệ thống).
7. `node tests/docx-export-format-smoke.js` — PASS (Định dạng Word lề, header, footer, bảng).

## Pass / Fail từng tiêu chí
- **Tiêu chí 1 (Cấu trúc 4 phần CV 5512)**: PASS — Mọi hoạt động (A, B các nhánh, C, D) đều đảm bảo có đủ `### a) Mục tiêu:`, `### b) Nội dung:`, `### c) Sản phẩm:`, `### d) Tổ chức thực hiện:`.
- **Tiêu chí 2 (Cột 2 bảng mục d))**: PASS — Cột 2 không bị rỗng hoặc `---`, tự động nhận kiến thức ghi bảng từ Cột 1 hoặc `c) Sản phẩm`.
- **Tiêu chí 3 (Ký hiệu đồng dạng `∽`)**: PASS — Render chuẩn chữ S nằm ngang `U+223D`.
- **Tiêu chí 4 (Ký hiệu góc `\widehat`)**: PASS — Giữ nguyên ký hiệu mũ góc qua OMML `<m:acc>`.
- **Tiêu chí 5 (Quy chuẩn sư phạm Toán)**: PASS — Đúng chuẩn phương trình tích THCS (không `[`), số thập phân phẩy, tọa độ chấm phẩy, $\tan/\cot$.
- **Tiêu chí 6 (Test suites)**: PASS — 7/7 bộ test chạy thành công 100%.

## Bug
Không phát hiện bug tồn đọng.
