# Báo cáo triển khai: SGK Mục 1, bộ chọn PPCT, xuất Word chuẩn

## 1. Trích xuất SGK & Hoạt động B

- `canvasTextbookAnalysisPrompt`: chỉ lấy đề mục cấp 1 (`1.`, `2.`, `I.`, `II.`); cấm tách tiêu đề con in đậm thành section.
- `mergeCanvasTextbookSections`: sáp nhập tiểu mục không số vào mục lớn đứng trước.
- `GENERATE_ACTIVITY_B`: bắt buộc `Hoạt động 2.1` = Mục 1, cấm bắt đầu từ 2.2.

## 2. Bộ chọn bài PPCT (Bước 2–4)

- UI: ô tìm kiếm, lọc `Tất cả` | `Có NLS` | `Có AI` | `Có NLS + AI`, badge `[NLS]`/`[AI]`, card tóm tắt (tên bài, tiết CT, thời lượng, tuần, mã NLS/AI).
- `applyPpctCatalogRow` nạp `lesson_scope`, thời lượng, bật/khóa NLS-AI từ PPCT sang Bước 3–4.
- Nhãn Bước 3: `Kế hoạch PPDH & Tích hợp NLS/AI (Ưu tiên từ PPCT)`.

## 3. Xuất Word

- Lề: trên/dưới/phải 850, trái 1134; spacing After 60, line 240, bảng 9922 (4961+4961).
- Header: bảng 2 cột Trường / Giáo viên; Chương (nếu có); `TIẾT X - BÀI Y: TÊN BÀI`; thời lượng nghiêng.
- Footer: Môn / `- Trang X -` / Năm học.
- Truyền `lessonScope` vào header.

Cache-bust `textbook-exact-v13`. Test mới: `tests/docx-export-format-smoke.js`.

## Kiểm thử

- `node tests/khbd-textbook-exact-structure-smoke.js`: PASS (gồm TEST 6 phép nhân/chia)
- `node tests/docx-export-format-smoke.js`: PASS
- `node tests/canvas-soankhbd-smoke.js`: PASS
- `node tests/khbd-docx-layout-smoke.js`: PASS
- `node tests/khbd-4steps-workflow-smoke.js`: PASS
- `node tests/khbd-activity-b-subsections-smoke.js`: PASS
- `node tests/canvas-textbook-analysis-smoke.js`: PASS
- `node tests/ppct-settings-import-smoke.js`: PASS

Không commit, push hoặc deploy. `docs/handoff/PLAN.md` không bị sửa.
