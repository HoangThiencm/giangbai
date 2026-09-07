# PLAN: Khảo sát & Xử lý Triệt để Lỗi Công thức Hệ Phương trình (begincases / endcases) trong soankhbd và canvas_soankhbd

## Hiện trạng
1. **Hiện tượng lỗi**:
   - Khi xuất file Word (.docx) từ `soankhbd.html` hoặc `canvas_soankhbd.html`, ở bảng hoạt động giáo án (ví dụ cột Nội dung bảng d Hoạt động 3/4), các hệ phương trình toán học hiển thị dạng văn bản nghiêng lỗi:
     `begincasesx + y = 17 (1)\ 10x + 3y = 100 (2)endcases`
     thay vì hiển thị thành dấu ngoặc nhọn lớn `{` ôm các phương trình toán học chuẩn Word Equation (OMML).
2. **Nguyên nhân gốc rễ trong mã nguồn**:
   - **Tại `js/khbd-docx.js` (`createNativeMath`)**:
     + Khi gặp mã LaTeX hệ phương trình `$\begin{cases} x + y = 17 (1) \\ 10x + 3y = 100 (2) \end{cases}$`:
     + Bộ phân tích `createNativeMath` không hỗ trợ môi trường `\begin{...}` và `\end{...}`. Lệnh `\begin` bị `readCommandName()` đọc thành tên lệnh `"begin"`. Do không nằm trong bảng lệnh đã ánh xạ và `this.latexToUnicodeMath("\\begin")` trả về `"\\begin"`, nhánh fallback lấy chuỗi trần `"begin"`.
     + Khối `{cases}` tiếp tục bị đọc thành từng chữ cái riêng biệt `c`, `a`, `s`, `e`, `s`.
     + Ký hiệu xuống dòng `\\` bên trong hệ phương trình bị `readCommandName()` cắt thành 1 ký tự `\` duy nhất.
     + Ký hiệu kết thúc `\end{cases}` bị biến thành `end` và `cases`.
     + Vì không phát sinh ngoại lệ, hàm trả về đối tượng `docx.Math` chứa dãy ký tự rác `begincases... \ ... endcases`, Word kết xuất thành công thức Cambria Math dạng chữ rác như hình ảnh phản ánh.
   - **Tại `js/khbd-docx.js` (`latexToUnicodeMath`)**:
     + Hàm fallback Unicode cũng chưa có bộ lọc cho `\begin{cases}` / `\end{cases}`, chỉ xóa ngoặc nhọn `{}` bằng regex `replace(/[{}]/g, "")`, dẫn đến việc nếu rơi vào fallback thì vẫn bị chuỗi `\begincases ... \endcases`.
   - **Tại `js/khbd-app.js` (`unwrapVietnameseMathForKatex` / `rewriteMathSpanForVietnamese`)**:
     + Hàm `rewriteMathSpanForVietnamese` tự động bóc tách các nhãn `\text{...}` tiếng Việt ra ngoài dấu `$ ... $`. Khi gặp hệ phương trình có nhãn chú thích tiếng Việt (ví dụ `\text{ (quả)}`), việc bóc tách làm vỡ môi trường `\begin{cases}` thành các đoạn `$ ... $` cụt đầu cụt đuôi, gây lỗi render KaTeX trên màn hình Preview.
   - **Tại `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`**:
     + Đang nạp cứng `<script src="https://hoangthiencm.id.vn/js/khbd-docx.js"></script>` ở dòng 891 mà không có cơ chế chuyển đổi sang file cục bộ `js/khbd-docx.js` khi chạy môi trường local (`file:` hoặc `localhost`), khiến bản canvas không nhận được bản sửa lỗi khi chạy thử nghiệm hoặc kiểm thử offline.

## Phạm vi
- **Xử lý toàn diện tại `js/khbd-docx.js`**:
  + Thêm cơ chế nhận diện và phân tích môi trường hệ phương trình `\begin{cases} ... \end{cases}` và `\left\{ ... \right.`.
  + Tách các dòng phương trình theo ký hiệu xuống dòng `\\` và phân tách cột nhãn căn lề `&`.
  + Chuyển đổi chuẩn xác sang đối tượng OMML Delimiter (`m:d`) trong Word:
    * `begChr` là dấu ngoặc nhọn `{`.
    * `endChr` để trống `""` (không có dấu đóng).
    * Chứa khối `m:eqArr` (Equation Array) với các phần tử dòng `m:e`, mỗi dòng là một phương trình toán học chuẩn.
  + Cập nhật `latexToUnicodeMath` để chuyển đổi sạch sang Unicode dạng `{ (dòng 1); (dòng 2)` nếu chạy ở chế độ fallback, loại bỏ vĩnh viễn chuỗi `begincases` / `endcases`.
- **Xử lý tại `js/khbd-app.js`**:
  + Điều chỉnh `unwrapVietnameseMathForKatex`: Bảo toàn nguyên khối công thức, không phân rã các biểu thức nằm trong môi trường LaTeX (`\begin{...}` hoặc `\left\{`).
- **Đồng bộ nạp script trong `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`**:
  + Cho phép tự động nạp `js/khbd-docx.js` cục bộ khi chạy ở môi trường `file:` / `localhost`, giữ nguyên URL `https://hoangthiencm.id.vn/js/khbd-docx.js` khi chạy trên Gemini Canvas.
- **Kiểm thử tự động**:
  + Mở rộng `tests/khbd-docx-math-smoke.js` và `tests/khbd-katex-vn-smoke.js` để bao quát toàn bộ các biến thể hệ phương trình.

## Ngoài phạm vi
- Không thay đổi cấu trúc bảng biểu Công văn 5512 hay các quy tắc định dạng lề, font chữ khác của giáo án DOCX.
- Không thay đổi logic sinh đề bài hay cấu trúc prompt chính của AI.
- Không sửa source trong lượt lệnh `/survey` này.

## File dự kiến tác động
- `js/khbd-docx.js`
- `js/khbd-app.js`
- `canvas_soankhbd.html`
- `backupcode viettailieu/canvas_soankhbd.html`
- `tests/khbd-docx-math-smoke.js`
- `tests/khbd-katex-vn-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/VERIFY.md`

## Các bước thực hiện
1. **Khảo sát & Lập tài liệu bàn giao**:
   - Hoàn thành ghi đè `docs/handoff/PLAN.md` và ghi `docs/handoff/.lock`.
2. **Nâng cấp bộ phân tích toán học trong `js/khbd-docx.js`**:
   - Trong `createNativeMath`: Thêm bộ nhận diện `\begin{cases}` ... `\end{cases}` và `\begin{aligned}`.
   - Xây dựng cây OMML với `XmlComponent`: Tạo thẻ `<m:d>` chứa `<m:dPr><m:begChr m:val="{"/><m:endChr m:val=""/></m:dPr>` và `<m:e><m:eqArr>...</m:eqArr></m:e>`.
   - Mỗi hàng phương trình ngăn cách bởi `\\` được parse thành một thẻ `<m:e>` bên trong `<m:eqArr>`.
   - Xử lý làm sạch nhãn và ký tự `&` trong hệ phương trình.
   - Trong `latexToUnicodeMath`: Thêm quy tắc thay thế regex loại bỏ `\begin{cases}` và `\end{cases}`, thay `\\` bằng dấu xuống dòng hoặc chấm phẩy.
3. **Cập nhật hàm bảo vệ tiếng Việt trong `js/khbd-app.js`**:
   - Kiểm tra điều kiện trong `unwrapVietnameseMathForKatex`: Nếu chuỗi công thức chứa `\begin{` hoặc `\left\{` thì bỏ qua việc cắt rời `\text{...}` để bảo toàn tính toàn vẹn cú pháp cho KaTeX.
4. **Đồng bộ hóa nạp script trong `canvas_soankhbd.html`**:
   - Thêm điều kiện kiểm tra `isLocal` để nạp `js/khbd-docx.js` cục bộ khi mở file trực tiếp hoặc localhost.
   - Đồng bộ sang `backupcode viettailieu/canvas_soankhbd.html`.
5. **Cập nhật & Bổ sung bài kiểm thử**:
   - Thêm ca kiểm thử hệ phương trình 2 ẩn có đánh số `(1)`, `(2)` vào `tests/khbd-docx-math-smoke.js`.
   - Thêm ca kiểm thử `unwrapVietnameseMathForKatex` với hệ phương trình chứa nhãn vào `tests/khbd-katex-vn-smoke.js`.
   - Chạy kiểm thử toàn bộ dự án (`khbd-docx-math-smoke`, `khbd-docx-format-smoke`, `khbd-katex-vn-smoke`, `canvas-soankhbd-smoke`).
6. **Kiểm thử thực tế & Hoàn thiện tài liệu**:
   - Xuất file `.docx` mẫu và giải nén kiểm tra `word/document.xml`.
   - Cập nhật `docs/handoff/IMPLEMENT.md` và `docs/handoff/VERIFY.md`.

## Rủi ro
- **Xung đột cấu trúc OMML trong các phiên bản Word cũ**: Nếu Word 2010/2013 không render được `m:eqArr` lồng trong `m:d`.
  + *Giải pháp*: Cấu trúc `<m:d><m:dPr><m:begChr m:val="{"/><m:endChr m:val=""/></m:dPr><m:e><m:eqArr><m:e>...</m:e></m:eqArr></m:e></m:d>` là chuẩn ECMA-376 Part 1 (Office Open XML Math) được Microsoft Word hỗ trợ từ Word 2007 trở lên.
- **Hồi quy với các công thức toán thông thường**: Việc can thiệp vào `createNativeMath` có thể ảnh hưởng đến phân số (`\frac`), căn bậc (`\sqrt`), tích phân hoặc chỉ số.
  + *Giải pháp*: Chỉ rẽ nhánh xử lý riêng biệt khi gặp `\begin{cases}` hoặc `\begin{aligned}`, tất cả các nhánh công thức đơn khác giữ nguyên logic hiện hành.

## Cách kiểm thử
1. **Kiểm thử tự động bằng script**:
   - Chạy `node tests/khbd-docx-math-smoke.js`:
     + Kiểm tra buffer DOCX tạo ra có chứa XML `<m:dPr><m:begChr m:val="{"/><m:endChr m:val=""/></m:dPr>`.
     + Kiểm tra có chứa `<m:eqArr>` và các thẻ hàng `<m:e>`.
     + Khẳng định không xuất hiện chuỗi `begincases` hoặc `endcases` trong XML xuất ra.
   - Chạy `node tests/khbd-katex-vn-smoke.js`:
     + Đảm bảo hệ phương trình có chữ tiếng Việt giữ nguyên cấu trúc khối.
   - Chạy `node tests/canvas-soankhbd-smoke.js`:
     + Xác nhận file `canvas_soankhbd.html` và bản backup pass 100% cú pháp và DOM ID.
2. **Kiểm thử tích hợp**:
   - Chạy toàn bộ các test khbd hiện có: `khbd-docx-format-smoke.js`, `khbd-docx-layout-smoke.js`, `khbd-docx-illustration-fallback-smoke.js`.

## Tiêu chí nghiệm thu
1. File Word (.docx) tạo ra khi có hệ phương trình:
   - Hiển thị dấu ngoặc nhọn lớn chuẩn Word ôm các phương trình.
   - Tuyệt đối không còn xuất hiện văn bản rác `begincases` hay `endcases`.
   - Ký tự chú thích phương trình `(1)`, `(2)` được giữ nguyên vẹn.
2. Màn hình KaTeX Preview trong cả `soankhbd.html` và `canvas_soankhbd.html` hiển thị hệ phương trình sắc nét, không báo lỗi đỏ hoặc vỡ khung.
3. Toàn bộ các bài kiểm thử liên quan đều PASS 100%.
