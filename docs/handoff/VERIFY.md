# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Module 1: Sinh đủ N nhánh Hoạt động B (khung mẫu động theo N mục lớn SGK)**:
  - `js/khbd-prompts.js`: Đã cài đặt `activityBBranchSkeleton` và `expandActivityBSkeleton`, tự động sinh khung mẫu đủ `Hoạt động 2.1` ... `2.N` dựa theo số lượng mục lớn SGK bóc tách được (kèm tên đề mục nguyên văn và số phút phân bổ).
  - Lệnh cấm rõ ràng: *Bài học có N mục lớn thì BẮT BUỘC phải sinh đủ N nhánh... TUYỆT ĐỐI CẤM dừng lại hoặc bỏ dở sau khi chỉ sinh Hoạt động 2.1*.
  - `js/khbd-app.js`: `assertPhasePedagogyOutput` kiểm tra nghiêm ngặt: nếu `expectedBranches >= 2` mà thiếu `Hoạt động 2.2` thì báo lỗi bắt AI sinh lại, không lưu giáo án thiếu nhánh.
- **Module 2: UX/UI Bộ chọn bài PPCT & Nguồn sự thật (Bước 2 & 3)**:
  - Có ô tìm kiếm và 4 tab lọc nhanh: `Tất cả` | `Có NLS` | `Có AI` | `Có NLS + AI`.
  - Hiển thị badge `[NLS]` (xanh dương) và `[AI]` (tím) trên từng bài học.
  - Card tóm tắt bài học hiển thị đầy đủ: Tên bài, Tiết CT, Thời lượng, Tuần, Mã NLS, Mã AI.
  - Tự động nạp và ưu tiên/khóa NLS & AI từ PPCT sang Bước 3 & Bước 4; Nhãn Bước 3: `Kế hoạch PPDH & Tích hợp NLS/AI (Ưu tiên từ PPCT)`.
- **Module 3: Chuẩn hóa xuất file Word (.docx)**:
  - Căn lề chuẩn: Top 1.5cm (850 dxa), Bottom 1.5cm (850 dxa), Left 2.0cm (1134 dxa), Right 1.5cm (850 dxa).
  - Spacing: Before 0pt, After 3pt (60 dxa), Line Single (240 dxa), Căn đều 2 lề (Justified), Bảng 2 cột 9922 dxa (mỗi cột 4961 dxa).
  - Header 2 cột: Cột trái `Trường [Tên trường]`, Cột phải `Giáo viên: [Tên GV]`; Dòng Chương (IN HOA ĐẬM); Dòng `TIẾT [X] - BÀI [Y]: [TÊN BÀI]`; Dòng Thời lượng thực hiện in nghiêng.
  - Footer 3 phần: `Môn: ...` | `- Trang [Page] -` | `Năm học: ...`.

## Test đã chạy
- `node tests/khbd-textbook-exact-structure-smoke.js`
- `node tests/khbd-activity-b-subsections-smoke.js`
- `node tests/docx-export-format-smoke.js`
- `node tests/canvas-soankhbd-smoke.js`
- `node tests/khbd-4steps-workflow-smoke.js`
- `node tests/ppct-settings-import-smoke.js`
- `node tests/khbd-docx-layout-smoke.js`

## Pass / Fail từng tiêu chí
- [PASS] Sinh đầy đủ $N$ nhánh Hoạt động 2.1, 2.2... khi bài có $N$ mục lớn; không bị dừng lại sau 2.1.
- [PASS] Đề mục nguyên văn, Mục 1 làm Hoạt động 2.1, Mục 2 làm Hoạt động 2.2.
- [PASS] Bộ chọn bài PPCT có tìm kiếm, 4 bộ lọc NLS/AI, badge và card tóm tắt hoạt động chuẩn.
- [PASS] Ưu tiên NLS/AI từ PPCT sang Bước 3 và 4.
- [PASS] Xuất file Word chuẩn A4, lề, spacing, header 2 cột, footer 3 phần và hiển thị tiết dạy.
- [PASS] 100% test suites PASS.

## Bug
Không phát hiện lỗi.
