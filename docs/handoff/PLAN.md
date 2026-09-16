# PLAN

## Hiện trạng & Vấn đề cần giải quyết
1. **Lỗi phân tích SGK & Đánh số Hoạt động 2.1**:
   - Khi phân tích ảnh/PDF SGK bài "Phép nhân và phép chia số tự nhiên", AI bóc tách nhầm chữ in đậm *"Tính chất của phép nhân"* thành đề mục lớn riêng lẻ.
   - Khi sinh Hoạt động B (`GENERATE_ACTIVITY_B`), AI bỏ qua Mục 1 (`1. PHÉP NHÂN SỐ TỰ NHIÊN`), sinh thẳng từ `Hoạt động 2.2: Tính chất của phép nhân`... làm mất toàn bộ kiến thức căn bản của Mục 1.
2. **UX/UI Bộ chọn bài học PPCT (Bước 2)**:
   - Dropdown hiện tại nhồi nhét Chương + Bài + Tiết CT thành một dòng rất dài, 89 dòng gây khó tìm kiếm.
   - Mất thông tin NLS (Năng lực số) và AI (Trí tuệ nhân tạo) ngay tại nơi chọn bài, dù trong PPCT JSON đã có trường `digital_competency` và `ai_competency`.
   - Bước 3 có tiêu đề *"Đề xuất PPDH & NLS"* gây hiểu lầm là AI tự sinh NLS, trong khi PPCT mới là nguồn chuẩn quy định NLS/AI cho bài học đó.
3. **Chuẩn hóa xuất file Word (.docx) theo ảnh mẫu và cấu hình chuẩn**:
   - Nhập/chọn tiết dạy (VD: `Tiết 1` hoặc `Tiết 23-24`) nhưng khi xuất file Word không hiển thị thông tin tiết dạy.
   - Header chưa có định dạng bảng 2 cột chuẩn: `Trường [Tên trường]` bên trái và `Giáo viên: [Tên GV]` bên phải, chưa có dòng `CHƯƠNG...`, dòng `TIẾT X - BÀI Y: TÊN BÀI` và dòng `Thời lượng thực hiện: N tiết (M phút)`.
   - Footer chưa có phân chia: Môn bên trái, `- Trang X -` ở giữa, Năm học bên phải.
   - Thông số lề và khoảng cách đoạn văn chưa chuẩn: Lề Trên 1.5cm (850 dxa), Dưới 1.5cm (850 dxa), Trái 2.0cm (1134 dxa), Phải 1.5cm (850 dxa); Space Before 0pt, Space After 3pt (60 dxa), Line spacing Single (240 dxa), Căn đều 2 lề (Justified).

---

## Phạm vi thực hiện

### 1. Khắc phục trích xuất SGK & Đảm bảo thứ tự Đề mục Hoạt động B
- **File**: `js/khbd-app.js`, `js/khbd-prompts.js`, `canvas_soankhbd.html`.
- **Trích xuất**: Ràng buộc AI phân tích hình ảnh/PDF bám sát SGK, chỉ trích xuất các Đề mục cấp 1 chính thức (được đánh số to `1.`, `2.` hoặc `I.`, `II.`). Cấm tách các đề mục con in đậm (*Tính chất...*, *Quy tắc...*) hoặc ví dụ (*Ví dụ 1, 2, 3...*) thành section riêng.
- **Normalize**: Hàm `normalizeCanvasTextbookSection` tự động sáp nhập các tiểu mục không có số cấp 1 vào mục lớn đứng trước.
- **Hoạt động B**: Bắt buộc sinh từ phần tử đầu tiên:
  - `Hoạt động 2.1: [Tên chính xác Mục 1]` (chứa đầy đủ định nghĩa, tính chất, HĐ khám phá, Luyện tập, Vận dụng của Mục 1).
  - `Hoạt động 2.2: [Tên chính xác Mục 2]` (chứa phép chia hết, chia có dư, Ví dụ 3, 4, Luyện tập 3, Vận dụng 3).

### 2. Nâng cấp Bộ chọn bài học PPCT & Tôn trọng "PPCT là nguồn sự thật" (Bước 2 & Bước 3)
- **File**: `canvas_soankhbd.html`, `soankhbd.html`, `js/khbd-app.js`.
- **Lesson Picker UI**:
  - Thiết kế bộ chọn bài trực quan thay thế dropdown cũ: có ô tìm kiếm và **Bộ lọc nhanh (Filter Tabs)**: `Tất cả` | `Có NLS` | `Có AI` | `Có NLS + AI`.
  - Hiển thị badge trực quan: `[NLS]` (xanh dương), `[AI]` (tím) ngay bên cạnh tên bài và tiết CT.
  - Khi chọn bài, hiển thị **Thẻ tóm tắt thông tin bài học (Lesson Summary Card)**: Tên bài, Tiết CT, Thời lượng, Tuần, Mã NLS, Mã AI.
- **Kế thừa dữ liệu NLS/AI vào Bước 3 & Bước 4**:
  - Đổi nhãn/hướng dẫn Bước 3: *"Kế hoạch PPDH & Tích hợp NLS/AI (Ưu tiên từ PPCT)"*.
  - Tự động nạp và khóa/ưu tiên năng lực NLS & AI từ PPCT sang Bước 3 và Bước 4, không để AI tự ý ghi đè hay xóa bỏ mã năng lực đã quy định trong PPCT.

### 3. Chuẩn hóa xuất file Word (.docx) theo ảnh mẫu & Quy chuẩn kỹ thuật
- **File**: `js/khbd-docx.js`, `js/khbd-app.js`.
- **Cấu hình lề & Page Setup**:
  - Khổ giấy: A4 dọc.
  - Lề trang: Top = `850 dxa` (1.5cm), Bottom = `850 dxa` (1.5cm), Left = `1134 dxa` (2.0cm), Right = `850 dxa` (1.5cm).
  - Spacing đoạn văn mặc định: `spaceBefore = 0`, `spaceAfter = 60` (3pt), `lineSpacing = 240` (Single), `alignment = docx.AlignmentType.JUSTIFIED`.
  - Độ rộng bảng 2 cột: `tableWidth = 9922 dxa`, `columnWidths = [4961, 4961]`.
- **Header trang trọng**:
  - Bảng 2 cột (không viền):
    - Cột trái: `Trường [Tên trường]` (VD: `Trường THCS Trần Phú`).
    - Cột phải: `Giáo viên: [Tên giáo viên]` (VD: `Giáo viên: Hoàng Tấn Thiên`).
  - Dòng Chương (nếu có): Căn giữa, IN HOA ĐẬM (VD: `CHƯƠNG I: TẬP HỢP CÁC SỐ TỰ NHIÊN`).
  - Dòng Tiết & Tên bài: Căn giữa, IN HOA ĐẬM, cỡ chữ 14pt (VD: `TIẾT 1 - BÀI 1: TẬP HỢP` hoặc `TIẾT 23, 24 - BÀI 12: BỘI CHUNG. BỘI CHUNG NHỎ NHẤT`).
  - Dòng Thời lượng: Căn giữa, chữ nghiêng (VD: `Thời lượng thực hiện: 2 tiết (90 phút)`).
- **Footer trang trọng**:
  - Bảng footer 3 phần (hoặc tab stops): Cột trái: `Môn: [Tên môn]`; Giữa: `- Trang [Page] -` (dùng `docx.PageNumber.CURRENT`); Cột phải: `Năm học: [Năm học]`.
- **Dữ liệu Tiết dạy**:
  - Đảm bảo `appState.teachingContext.lesson_scope` (hoặc `session` / `period`) được truyền trọn vẹn vào `DocxGenerator.createDocumentHeader` để hiển thị đúng `TIẾT [X] - BÀI [Y]`.

---

## Ngoài phạm vi
- Không thay đổi logic backend không liên quan.
- Không xóa bỏ các tùy chọn tải JSON/Word khác.

---

## File dự kiến tác động
- `js/khbd-app.js`
- `js/khbd-docx.js`
- `js/khbd-prompts.js`
- `canvas_soankhbd.html`
- `soankhbd.html`
- `tests/khbd-textbook-exact-structure-smoke.js`
- `tests/canvas-soankhbd-smoke.js`
- `tests/docx-export-format-smoke.js` (Tạo mới để kiểm tra Word export)

---

## Các bước thực hiện
1. **Khâu trích xuất SGK & Prompt Hoạt động B**:
   - Cập nhật `canvasTextbookAnalysisPrompt` và `normalizeCanvasTextbookSection` trong `js/khbd-app.js`.
   - Cập nhật prompt template `GENERATE_ACTIVITY_B` trong `js/khbd-prompts.js` đảm bảo luôn bắt đầu từ `Hoạt động 2.1: [Mục 1]` đến `Hoạt động 2.2: [Mục 2]`.
2. **Bộ chọn bài học PPCT & Tôn trọng PPCT**:
   - Cập nhật giao diện `canvas_soankhbd.html` và `soankhbd.html`: Tạo UI Lesson Picker có search input, filter tabs (`Tất cả`, `Có NLS`, `Có AI`, `Có NLS + AI`), danh sách bài học có badge `[NLS]`, `[AI]` và Card tóm tắt bài học đã chọn.
   - Cập nhật `js/khbd-app.js`: Render danh sách bài theo filter, nạp đầy đủ metadata (`lesson_scope`, `duration`, `digital_competency`, `ai_competency`) vào state, tự động map sang Bước 3 & Bước 4.
3. **Chuẩn hóa DocxGenerator trong `js/khbd-docx.js`**:
   - Cập nhật `DocxGenerator`:
     - Lề trang: Top 850, Bottom 850, Left 1134, Right 850.
     - Spacing: Before 0, After 60, Line 240, Justified. Table width 9922 (2 cột: 4961).
     - `createDocumentHeader`: Header bảng 2 cột Trường / Giáo viên, Dòng Chương, Dòng `TIẾT X - BÀI Y: TÊN BÀI`, Dòng `Thời lượng thực hiện`.
     - `createDocumentFooter`: Môn / Trang số / Năm học.
4. **Viết và chạy Test kiểm thử tự động**:
   - Cập nhật `tests/khbd-textbook-exact-structure-smoke.js` & `tests/canvas-soankhbd-smoke.js`.
   - Tạo test `tests/docx-export-format-smoke.js` kiểm tra xuất Word đúng header, footer, lề trang, spacing và hiển thị Tiết dạy.
   - Chạy toàn bộ test suites.

---

## Rủi ro & Cách khắc phục
- **Rủi ro**: Nếu bài học không có thông tin Chương hoặc Tiết dạy.
  - **Khắc phục**: Xử lý fallback mềm dẻo: Nếu không có Chương thì ẩn dòng Chương; nếu không có Tiết dạy thì hiển thị `BÀI [Y]: [TÊN BÀI]`.
- **Rủi ro**: Giáo viên chọn bài thủ công không qua PPCT.
  - **Khắc phục**: Cho phép nhập tay và hệ thống vẫn giữ nguyên các cấu trúc bảng và header/footer Word hoàn chỉnh.

---

## Tiêu chí nghiệm thu
1. **Trích xuất SGK & Hoạt động B**:
   - Phân tích SGK trích xuất đúng 2 Mục lớn (`1. PHÉP NHÂN SỐ TỰ NHIÊN` và `2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ`).
   - Giáo án Hoạt động B bắt đầu tuần tự từ `Hoạt động 2.1: 1. PHÉP NHÂN SỐ TỰ NHIÊN` đến `Hoạt động 2.2: 2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ`, không bị mất Mục 1.
2. **Bộ chọn bài PPCT**:
   - Có bộ lọc `Tất cả`, `Có NLS`, `Có AI`, `Có NLS + AI` hoạt động mượt mà.
   - Hiển thị rõ badge `[NLS]` (xanh), `[AI]` (tím) cho từng bài.
   - Chọn bài xong hiển thị Card tóm tắt và tự động điền Tiết CT, Thời lượng, Tuần, Mã NLS, Mã AI sang các bước sau.
3. **Xuất file Word (.docx)**:
   - File docx có lề: Trên 1.5cm, Dưới 1.5cm, Trái 2.0cm, Phải 1.5cm. Spacing After 3pt, Line spacing Single, Justified.
   - Header đầy đủ: Trường / Giáo viên (2 cột), Chương (nếu có), `TIẾT X - BÀI Y: TÊN BÀI`, Thời lượng thực hiện.
   - Footer đầy đủ: Môn / - Trang X - / Năm học.
4. **Toàn bộ test suites PASS 100%**.
