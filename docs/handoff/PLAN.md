# PLAN: Khắc phục lỗi hiển thị chỉ mục số trong Preview và cố định chuẩn Bảng 2 cột trong Giáo án / Word

## Hiện trạng
1. **Vấn đề 1: Render chỉ mục số thứ tự trong KaTeX / Markdown Preview bị lặp lại toàn bộ số 1**:
   - Khi AI sinh nội dung Markdown có danh sách đánh số thứ tự (như Hoạt động E: `1. Ôn tập kiến thức:`, `2. Làm bài tập:`, `3. Chuẩn bị bài mới:`, `4. Nhiệm vụ tìm tòi, mở rộng:`) xen kẽ các dòng gạch đầu dòng con không thụt lề (`- ...`), Marked.js bóc tách thành các khối danh sách thứ tự `<ol>` riêng biệt bị ngắt quãng bởi danh sách không thứ tự `<ul>`.
   - Marked.js sinh ra các thẻ `<ol>` tiếp theo có thuộc tính `start` tương ứng: `<ol start="2">`, `<ol start="3">`, `<ol start="4">`.
   - Tuy nhiên, trong hàm `sanitizePreviewHtml()` tại `js/khbd-app.js`, hàm `copyNode` chỉ sao chép các thuộc tính whitelist cơ bản (`href`, `rel`, `target`, `src`, `alt`, `class`, `colspan`, `rowspan`), và loại bỏ thuộc tính `start` trên thẻ `<ol>`, `value` trên thẻ `<li>`, và `type` trên `<ol>/<ul>/<li>`.
   - Khi mất thuộc tính `start`, mỗi thẻ `<ol>` đều bắt đầu đếm lại từ số `1`, dẫn tới trên giao diện xem trước (KaTeX Preview) tất cả các chỉ mục đều hiển thị là `1.` (`1. Ôn tập...`, `1. Làm bài tập...`, `1. Chuẩn bị...`, `1. Nhiệm vụ...`), trong khi file Word xuất ra vẫn đúng.

2. **Vấn đề 2: Bảng tổ chức hoạt động lúc tạo 2 cột, lúc tạo 3 cột (cột 3 trống rỗng)**:
   - Theo hợp đồng sư phạm chuẩn CV 5512, bảng mục d) Tổ chức thực hiện của các hoạt động chỉ có DUY NHẤT 2 cột: `| Hoạt động của GV và HS | Nội dung |`.
   - Trong `js/khbd-docx.js`, hàm `createDocxTableFromMarkdown` tính số cột bằng `columnCount = Math.max(...validLines.map(line => this.splitMarkdownTableRow(line).length))`.
   - Nếu trong nội dung của một hàng, xuất hiện ký tự pipe `|` chưa được escape (ví dụ ký hiệu trị tuyệt đối `$|-5| = 5$`, ký hiệu tập hợp `\{x | x > 0\}`, hoặc AI vô tình xuất thêm ký tự `|` hoặc `||` ở cuối hàng), hàng đó sẽ bị chia tách thành 3 cell.
   - Khi `columnCount` bị nâng lên thành 3, `isActivityTwoCol` bị sai (`false`), dẫn đến `DocxGenerator` tạo ra bảng 3 cột co hẹp (mỗi cột ~3213 dxa) và để trống hoàn toàn cột thứ 3.

## Phạm vi
1. **Khắc phục Vấn đề 1: Whitelist thuộc tính danh sách trong `sanitizePreviewHtml()` (`js/khbd-app.js`)**:
   - Bổ sung sao chép an toàn thuộc tính:
     * `start` trên thẻ `<ol>` (kiểm tra `/^\d+$/`).
     * `value` trên thẻ `<li>` (kiểm tra `/^\d+$/`).
     * `type` trên thẻ `<ol>`, `<ul>`, `<li>` (kiểm tra chuẩn hợp lệ).
2. **Khắc phục Vấn đề 2: Cố định và chuẩn hóa bảng Hoạt động 2 Cột (`js/khbd-docx.js`, `js/khbd-app.js`, `js/khbd-prompts.js`)**:
   - Trong `js/khbd-docx.js`:
     * Khi tiêu đề bảng chứa `hoạt động của gv` hoặc `nội dung`, bảng BẮT BUỘC được cố định chính xác 2 cột (`columnCount = 2`, `columnWidths = [4819, 4820]`).
     * Nếu một hàng dữ liệu bị phân tách thành nhiều hơn 2 cell (do dấu `|` trong công thức hoặc thừa dấu pipe), tự động gộp toàn bộ các cell từ vị trí thứ 2 trở đi (`rawCells.slice(1).join(" | ")`) vào Cột 2 (Nội dung), tuyệt đối không mở thêm cột thứ 3.
   - Trong `js/khbd-app.js`:
     * Bổ sung cơ chế chuẩn hóa bảng hoạt động trong `mergeSplitActivityTables` và `sanitizeLessonMarkdown` để làm sạch các dòng bảng thừa dấu `|`.
   - Trong `js/khbd-prompts.js`:
     * Siết chặt chỉ thị trong `ACTIVITY_TABLE_CONTRACT`, nhấn mạnh tuyệt đối chỉ dùng đúng 2 cột `| Hoạt động của GV và HS | Nội dung |`, cấm sinh 3 cột và hướng dẫn dùng `\vert` hoặc `\|` cho ký hiệu trị tuyệt đối / đoạn thẳng.
3. **Bộ kiểm thử tự động (Unit / Smoke Tests)**:
   - Viết test kiểm tra `sanitizePreviewHtml` giữ đúng số thứ tự `start="2"`, `start="3"`, `start="4"`.
   - Viết test kiểm tra `createDocxTableFromMarkdown` luôn giữ đúng bảng 2 cột dù dữ liệu có chứa công thức có dấu `|`.

## Ngoài phạm vi
- Không thay đổi bảng biểu khác ngoài bảng hoạt động (ví dụ Bảng phân phối chương trình 7 cột giữ nguyên cấu trúc đa cột).
- Không can thiệp vào các hoạt động khác ngoài việc đảm bảo đúng định dạng 2 cột chuẩn.

## File dự kiến tác động
- `js/khbd-app.js`
- `js/khbd-docx.js`
- `js/khbd-prompts.js`
- `tests/khbd-list-numbering-smoke.js`
- `tests/khbd-table-columns-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Cập nhật hàm `sanitizePreviewHtml` trong `js/khbd-app.js`**:
   - Bổ sung sao chép các thuộc tính `start`, `value`, `type` cho `<ol>`, `<ul>`, `<li>` với regex kiểm tra an toàn.
2. **Bước 2: Cập nhật `createDocxTableFromMarkdown` trong `js/khbd-docx.js`**:
   - Cố định bảng hoạt động CV 5512 luôn có 2 cột (`columnCount = 2`).
   - Xử lý gộp các cell thừa `>= 2` vào cell thứ 2 (Nội dung) để tránh tạo cột thứ 3 rỗng.
3. **Bước 3: Tối ưu chuẩn hóa bảng trong `js/khbd-app.js` và cập nhật Prompt trong `js/khbd-prompts.js`**:
   - Cập nhật `mergeSplitActivityTables` và `splitKhbdMarkdownTableRow`.
   - Cập nhật nhắc nhở trong `ACTIVITY_TABLE_CONTRACT` về việc dùng đúng 2 cột và escape `|`.
4. **Bước 4: Viết các bài kiểm thử tự động**:
   - Viết `tests/khbd-list-numbering-smoke.js` và `tests/khbd-table-columns-smoke.js`.
5. **Bước 5: Chạy kiểm thử**:
   - Chạy toàn bộ test suites và kiểm tra thực tế để đảm bảo không hồi quy.

## Rủi ro
- **Rủi ro**: Dấu `|` trong công thức phức tạp nếu bị gộp có thể làm lệch phân tách cột nếu dấu `|` xuất hiện ở Cột 1.
  - **Khắc phục**: Thuật toán `splitKhbdMarkdownTableRow` đã nhận diện khối `$..$` và `$$..$$`, đồng thời việc cố định 2 cột chỉ chia tại dấu `|` phân cách cột đầu tiên hợp lệ.

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy test xác nhận Markdown Hoạt động E sau khi qua `marked.parse()` và `sanitizePreviewHtml()` giữ nguyên `<ol start="2">`, `<ol start="3">`, `<ol start="4">`.
   - Chạy test xác nhận bảng Markdown chứa công thức `$|-5| = 5$` hoặc dấu `|` thừa khi xuất qua `createDocxTableFromMarkdown` luôn tạo đúng bảng 2 cột với độ rộng 4819 / 4820 dxa.
2. **Kiểm thử thủ công trên giao diện**:
   - Mở `soankhbd.html`, kiểm tra tab Hoạt động E: Preview KaTeX hiển thị lần lượt 1., 2., 3., 4.
   - Mở tab Hoạt động B / C / D có chứa bảng tổ chức dạy học: Bấm "Xuất Word mục này" hoặc "Xuất toàn bộ giáo án", mở file Word kiểm tra bảng chỉ có đúng 2 cột ("Hoạt động của GV và HS" và "Nội dung"), không còn cột thứ 3 bị rỗng.

## Tiêu chí nghiệm thu
1. Các danh sách đánh số trong khung Preview KaTeX hiển thị đúng thứ tự tăng dần 1., 2., 3., 4. (không bị lặp lại toàn bộ số 1).
2. Bảng tổ chức hoạt động dạy học luôn luôn có đúng 2 cột trong cả bản xem trước và file Word xuất ra (.docx), không xuất hiện cột thứ 3 trống.
3. Tất cả các bài kiểm thử tự động liên quan đều PASS 100%.
