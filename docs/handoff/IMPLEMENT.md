# IMPLEMENT: Ký hiệu hình học VN, cột 2 rỗng, cấu trúc 4 phần CV 5512

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Module 1 — Word OMML (đã có, giữ)
- `\sim` / `\backsim` → `∽` (U+223D); `\widehat`/`\hat` → OMML `<m:acc>`; `\wideparen` → `⌒AB`; `\left[` array → `begChr="["`.

## Module 2 — Cột 2 không rỗng / `---`
- Prompt: Cột phải bắt buộc có kiến thức ghi bảng; cấm trống/`---`; cấm nhét quy tắc/ví dụ vào Bước 4 HS.
- `semanticSplitActivityRow`: nếu Cột 2 rỗng/`---` và Cột 1 có khối `Quy tắc` / `Ví dụ` / `Lời giải` / tiêu đề IN HOA sau Bước 4 → bóc sang Cột 2.
- `repairActivityTablesRightColumn`: fallback từ `c) Sản phẩm`.
- `assertPhasePedagogyOutput`: báo lỗi khi Cột 2 rỗng/`---`.

## Module 3 — 4 phần CV 5512
- Prompt C, D, `GENERATE_ACTIVITIES_AD`/`AE`: `BẮT BUỘC ĐỦ 4 MỤC` a/b/c/d, cấm nhảy từ Mục tiêu vào bảng.
- `ensureActivityFourPartStructure`: `- Mục tiêu:` → `### a) Mục tiêu:`; tự chèn b/c/d thiếu (b từ Bước 1, c từ Bước 3, d trước bảng).
- Áp dụng trong `clipKhbdActivityMarkdown` và `applyActivityOutput`.
- `assertPhasePedagogyOutput` kiểm tra đủ a/b/c/d.

## Module 4 — Sư phạm Toán
- THCS cấm `[` phương trình tích; số thập phân dấu phẩy; tọa độ `;`; `\tan`/`\cot`; đồng dạng `\backsim` và thứ tự đỉnh.

Kiểm thử:
- `node tests/khbd-table-columns-smoke.js` — PASS (cứu Cột 2, khôi phục 4 phần D)
- `node tests/khbd-activity-b-subsections-smoke.js` — PASS
- `node tests/khbd-docx-math-smoke.js` — PASS (`∽`, `<m:acc>`)
- `node tests/khbd-activities-ad-standard-smoke.js` — PASS
- `node tests/khbd-pedagogy-script-smoke.js` — PASS
- `node tests/canvas-prompts-integrity-smoke.js` — PASS

Không thêm chức năng ngoài plan. Cần `/verify` trên Antigravity: Hoạt động 2.2/2.3 cột Nội dung có kiến thức; Hoạt động 4 đủ a/b/c/d.
