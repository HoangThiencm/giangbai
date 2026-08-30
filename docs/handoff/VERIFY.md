# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Khắc phục render chỉ mục trong Preview (`js/khbd-app.js`)**:
   - `sanitizePreviewHtml()` đã bổ sung sao chép an toàn thuộc tính:
     * `start` trên thẻ `<ol>` (kiểm tra `/^\d+$/`).
     * `value` trên thẻ `<li>` (kiểm tra `/^\d+$/`).
     * `type` trên thẻ `<ol>`, `<ul>`, `<li>` (`1`, `a`, `A`, `i`, `I`, `disc`, `circle`, `square`).
   - Các chỉ mục bị ngắt quãng bởi danh sách không thứ tự (như Hoạt động E) hiển thị đúng số thứ tự tăng dần 1., 2., 3., 4.
   - Khớp 100% scope trong PLAN.md.

2. **Cố định bảng Hoạt động 2 Cột (`js/khbd-docx.js`, `js/khbd-app.js`, `js/khbd-prompts.js`)**:
   - Trong `js/khbd-docx.js`: Bảng hoạt động (khi header đồng thời chứa `hoạt động của gv` và `nội dung`) luôn được ép cố định `columnCount = 2` và `columnWidths = [4819, 4820]`. Nếu một hàng bị chia thành nhiều hơn 2 cell (do dấu `|` trong công thức hoặc thừa dấu pipe), toàn bộ các cell từ vị trí thứ 2 trở đi được gộp vào Cột 2 (Nội dung) bằng ` | `, không sinh cột thứ 3 rỗng.
   - Trong `js/khbd-app.js`: `mergeSplitActivityTables` và `splitKhbdMarkdownTableRow` chuẩn hóa và gom các hàng bảng hoạt động về đúng 2 cột.
   - Trong `js/khbd-prompts.js`: `ACTIVITY_TABLE_CONTRACT` cấm sinh cột thứ 3 và hướng dẫn dùng `\vert` / `\|` khi viết ký hiệu gạch đứng.
   - Khớp 100% scope trong PLAN.md.

## Test đã chạy
```
node tests/khbd-list-numbering-smoke.js
node tests/khbd-table-columns-smoke.js
node tests/khbd-docx-layout-smoke.js
node tests/khbd-activity-e-smoke.js
node tests/khbd-sanitize-smoke.js
node tests/khbd-pedagogy-script-smoke.js
```
- Tất cả unit / smoke tests trực tiếp và liên quan đều PASS 100%.

## Pass / Fail từng tiêu chí
1. **Tiêu chí 1**: Các danh sách đánh số trong khung Preview KaTeX hiển thị đúng thứ tự tăng dần 1., 2., 3., 4. (không bị lặp lại toàn bộ số 1). -> **PASS**
2. **Tiêu chí 2**: Bảng tổ chức hoạt động dạy học luôn luôn có đúng 2 cột trong cả bản xem trước và file Word xuất ra (.docx), không xuất hiện cột thứ 3 trống khi có dấu `|` trong công thức. -> **PASS**
3. **Tiêu chí 3**: Tất cả các bài kiểm thử tự động liên quan đều PASS 100%. -> **PASS**

## Bug
Không có.

