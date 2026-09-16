# Báo cáo: Sinh đủ N nhánh Hoạt động B + bộ chọn PPCT NLS/AI + Word lề/header/footer

## 1. Hoạt động B: khung mẫu động theo N mục lớn SGK

- `js/khbd-prompts.js`: `activityBBranchSkeleton` + `expandActivityBSkeleton` thay khung tĩnh chỉ có 2.1 bằng đủ `Hoạt động 2.1` … `2.N` (tên đề mục nguyên văn + phút phân bổ).
- Chỉ thay dòng khung mẫu thật (`\n## B. HOẠT ĐỘNG 2:…`), không cắt đoạn hướng dẫn phía trên.
- Lệnh cấm: *Bài học có N mục lớn thì BẮT BUỘC phải sinh đủ N nhánh… TUYỆT ĐỐI CẤM dừng lại hoặc bỏ dở sau khi chỉ sinh Hoạt động 2.1* (trong template, khung mẫu và DANH SÁCH TIỂU MỤC).
- `js/khbd-app.js`: `assertPhasePedagogyOutput` ném lỗi nếu `expectedBranches >= 2` mà thiếu `Hoạt động 2.2`.
- Ví dụ Phép nhân / Phép chia: prompt B có
  - `### Hoạt động 2.1: 1. PHÉP NHÂN SỐ TỰ NHIÊN`
  - `### Hoạt động 2.2: 2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ`

## 2. Bộ chọn bài PPCT (Bước 2–3)

- `soankhbd.html` / `canvas_soankhbd.html`: ô tìm, bộ lọc `Tất cả | Có NLS | Có AI | Có NLS + AI`, badge `[NLS]` / `[AI]`, thẻ tóm tắt (tên bài, Tiết CT, thời lượng, tuần, mã NLS/AI).
- Chọn bài → nạp tên bài, tiết CT, thời lượng, khóa/ưu tiên NLS & AI từ PPCT.
- Bước 3: *Kế hoạch PPDH & Tích hợp NLS/AI (Ưu tiên từ PPCT)*.

## 3. Xuất Word

- `js/khbd-docx.js`: A4, lề 850/850/1134/850 dxa, Before 0 / After 60 / Line 240, bảng 9922 (2 cột 4961), căn đều.
- Header 2 cột không viền: `Trường [Tên trường]` | `Giáo viên: [Tên GV]`; Chương IN HOA ĐẬM; `TIẾT X - BÀI Y: TÊN BÀI` 14pt; thời lượng nghiêng.
- Footer: `Môn: …` | `- Trang X -` | `Năm học: …`.

## Kiểm thử

- `node tests/khbd-textbook-exact-structure-smoke.js`: PASS (TEST 6: khung mẫu cuối prompt đủ 2.1 và 2.2)
- `node tests/khbd-activity-b-subsections-smoke.js`: PASS (3 nhánh; thiếu 2.2 thì throw)
- `node tests/docx-export-format-smoke.js`: PASS
- `node tests/canvas-soankhbd-smoke.js`: PASS
- `node tests/khbd-4steps-workflow-smoke.js`: PASS
- `node tests/ppct-settings-import-smoke.js`: PASS
- `node tests/khbd-docx-layout-smoke.js`: PASS

Không commit. `docs/handoff/PLAN.md` không bị sửa.
