# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Module 1: Trích xuất SGK & Đề mục Hoạt động B**:
  - `canvasTextbookAnalysisPrompt`: Ràng buộc trích xuất đúng đề mục cấp 1 (`1.`, `2.`, `I.`, `II.`), cấm tách tiêu đề con in đậm thành section mới.
  - `mergeCanvasTextbookSections` & `normalizeCanvasTextbookSection`: Tự động sáp nhập các tiểu mục không có số cấp 1 vào mục lớn trước đó.
  - `GENERATE_ACTIVITY_B`: Bắt buộc duyệt tuần tự từ phần tử đầu tiên, Hoạt động 2.1 là Mục 1, Hoạt động 2.2 là Mục 2, không bỏ sót Mục 1, không nhảy cóc.
- **Module 2: UX/UI Bộ chọn bài PPCT & Nguồn sự thật**:
  - Có ô tìm kiếm và 4 tab lọc nhanh: `Tất cả` | `Có NLS` | `Có AI` | `Có NLS + AI`.
  - Hiển thị badge `[NLS]` (xanh dương) và `[AI]` (tím) trên từng bài học.
  - Card tóm tắt bài học hiển thị đầy đủ: Tên bài, Tiết CT, Thời lượng, Tuần, Mã NLS, Mã AI.
  - Nạp và kế thừa mã NLS/AI từ PPCT sang Bước 3 & Bước 4, đổi nhãn Bước 3 thành `Kế hoạch PPDH & Tích hợp NLS/AI (Ưu tiên từ PPCT)`.
- **Module 3: Chuẩn hóa xuất file Word (.docx)**:
  - Căn lề chuẩn: Top 1.5cm (850 dxa), Bottom 1.5cm (850 dxa), Left 2.0cm (1134 dxa), Right 1.5cm (850 dxa).
  - Spacing After 3pt (60 dxa), Line spacing Single (240 dxa), Căn đều 2 lề (Justified), Table width 9922 dxa (2 cột 4961 dxa).
  - Header bảng 2 cột: Cột trái `Trường [Tên trường]`, Cột phải `Giáo viên: [Tên GV]`; Dòng Chương; Dòng `TIẾT [X] - BÀI [Y]: [TÊN BÀI]`; Dòng Thời lượng thực hiện in nghiêng.
  - Footer: Cột trái `Môn: [Tên môn]`, Giữa `- Trang [Page] -`, Cột phải `Năm học: [Năm học]`.
  - Truyền đầy đủ `lessonScope` vào Header.

## Test đã chạy
- `node tests/khbd-textbook-exact-structure-smoke.js`
- `node tests/docx-export-format-smoke.js`
- `node tests/canvas-soankhbd-smoke.js`
- `node tests/khbd-docx-layout-smoke.js`
- `node tests/khbd-4steps-workflow-smoke.js`
- `node tests/khbd-activity-b-subsections-smoke.js`
- `node tests/canvas-textbook-analysis-smoke.js`
- `node tests/ppct-settings-import-smoke.js`

## Pass / Fail từng tiêu chí
- [PASS] Mục 1 không bị mất trong giáo án Hoạt động B ("1. PHÉP NHÂN SỐ TỰ NHIÊN" -> Hoạt động 2.1; "2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ" -> Hoạt động 2.2).
- [PASS] Bộ lọc bài PPCT (Tất cả, NLS, AI, NLS+AI), badge và Card tóm tắt hoạt động chính xác.
- [PASS] Ưu tiên NLS/AI từ PPCT sang Bước 3 & 4.
- [PASS] File Word xuất ra đúng cấu hình lề A4, spacing, header 2 cột Trường/GV, Chương, Tiết-Bài, thời lượng và footer 3 phần.
- [PASS] 100% test suites vượt qua.

## Bug
Không phát hiện lỗi.
