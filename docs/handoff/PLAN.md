# PLAN: Khắc phục lỗi hiển thị chuỗi \quad lặp lại vô nghĩa trong KaTeX và Bảng Nội dung (soankhbd.html)

Trạng thái: ĐÃ IMPLEMENT (chờ /verify)

## Hiện trạng
- Trong ảnh chụp giao diện `soankhbd.html` (phần xem trước KaTeX & Bảng biểu ở Hoạt động C. Luyện tập, Bài 3.4 về biểu diễn số trên trục số), mục Lời giải xuất hiện một khối lớn toàn các lệnh LaTeX khoảng trắng: `$$\quad \quad \quad \quad \quad \quad \quad \quad \dots$$`.
- **Nguyên nhân gốc rễ**:
  1. Khi gặp bài toán yêu cầu vẽ hình hoặc biểu diễn số trên trục số, mô hình AI (Gemini) cố tình tạo khoảng trống hoặc mô phỏng trục số/vạch chia bằng cách lặp lại hàng chục lệnh khoảng trắng LaTeX `\quad` hoặc `\qquad`.
  2. Trong `js/khbd-prompts.js`, hệ thống prompt chưa có ràng buộc cấm AI sinh chuỗi `\quad` liên tiếp để tạo khoảng trống hoặc vẽ hình giả lập.
  3. Trong `js/khbd-app.js`, các hàm làm sạch `sanitizeLessonMarkdown`, `normalizeGeminiLessonOutput` và `unwrapVietnameseMathForKatex` chưa có bộ lọc regex để nhận diện và loại bỏ/rút gọn các khối LaTeX rác chỉ chứa toàn `\quad`, `\qquad`, `\hspace` hay khoảng trắng vô nghĩa.
  4. Khi Marked.js và KaTeX render, chuỗi này biến thành một mảng khối rác dài làm xấu giao diện và xô lệch bảng; khi xuất sang Word (.docx), `js/khbd-docx.js` chuyển đổi thành hàng trăm dấu cách làm vỡ lề bảng 2 cột.

## Phạm vi
1. **Cập nhật Prompt Engineering (`js/khbd-prompts.js`)**:
   - Thêm quy tắc cấm tuyệt đối trong `ACTIVITY_TABLE_CONTRACT`, `OUTPUT_CONTRACT`, `GENERATE_ACTIVITY_B`, `GENERATE_ACTIVITY_C`, `GENERATE_ACTIVITY_D`:
     * CẤM TUYỆT ĐỐI dùng chuỗi lệnh LaTeX khoảng trắng liên tiếp (`\quad \quad \quad...`, `\qquad`, `\hspace{...}`, `\phantom{...}`) để mô phỏng hình vẽ, giả lập trục số hoặc tạo khoảng trống làm bài.
     * Đối với bài tập vẽ hình/trục số: BẮT BUỘC mô tả lời giải bằng các bước thực hiện tường minh (ví dụ: "Vẽ trục số nằm ngang, chọn điểm 0 làm gốc, chia các đoạn đơn vị bằng nhau... Điểm biểu diễn -5 nằm bên trái gốc 0 cách 5 đơn vị...") hoặc định vị hình minh họa SVG chuẩn SGK `![caption](khbd-ill:id)`.
     * Lời giải trong cột Nội dung phải là các bước giải chi tiết hoàn chỉnh, không để khoảng trống vô nghĩa.

2. **Cập nhật Bộ lọc & Làm sạch Markdown (`js/khbd-app.js`)**:
   - Trong `sanitizeLessonMarkdown(rawOutput)`:
     * Phát hiện và loại bỏ các khối math độc lập `\$\$(?:\s*\\(?:quad|qquad|hspace\{[^}]*\}|phantom\{[^}]*\})\s*)+\$\$` hoặc `\$(?:\s*\\(?:quad|qquad|hspace\{[^}]*\}|phantom\{[^}]*\})\s*)+\$`.
     * Rút gọn chuỗi `(?:\\[q]?quad\s*){3,}` thành tối đa 1 khoảng cách hoặc dấu cách thường.
     * Dọn dẹp các khối math giả lập trục số rác (chỉ chứa `\quad` và dấu gạch nối/mũi tên).
   - Trong `unwrapVietnameseMathForKatex(markdown)` & `renderMathPreview(markdownText, targetElementId)`:
     * Tiền xử lý làm sạch mọi chuỗi `\quad` lặp thừa trước khi chuyển qua Marked.js và KaTeX Auto-render, đảm bảo preview hiển thị đẹp mắt, không lỗi.

3. **Cập nhật Xử lý Xuất Word (`js/khbd-docx.js`)**:
   - Trong `latexToUnicodeMath` và `parseMarkdownToDocxElements`:
     * Lọc bỏ các chuỗi `\quad` lặp lại liên tiếp trước khi chuyển đổi sang Unicode / Paragraph, ngăn chặn việc chèn hàng trăm khoảng trắng làm tràn bảng Word.

## Ngoài phạm vi
- Không can thiệp vào các công thức Toán học LaTeX hợp lệ chứa `\quad` đơn lẻ làm khoảng cách giữa các mệnh đề toán học (ví dụ `$x = 1 \quad \text{hoặc} \quad x = 2$`).
- Không thay đổi cấu trúc bảng 2 cột chuẩn CV 5512.

## File dự kiến tác động
- `js/khbd-prompts.js`
- `js/khbd-app.js`
- `js/khbd-docx.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Bổ sung ràng buộc chống chuỗi `\quad` rác vào `js/khbd-prompts.js`**:
   - Thêm chỉ dẫn cấm chuỗi khoảng trắng LaTeX lặp vào `ACTIVITY_TABLE_CONTRACT` và các prompt Hoạt động B, C, D.
2. **Bước 2: Cập nhật hàm làm sạch `sanitizeLessonMarkdown` trong `js/khbd-app.js`**:
   - Viết regex phát hiện và loại bỏ triệt để các khối `$$\quad \quad ...$$` rác.
   - Thêm xử lý trong `unwrapVietnameseMathForKatex` để bảo vệ KaTeX preview.
3. **Bước 3: Cập nhật bộ chuyển đổi Docx trong `js/khbd-docx.js`**:
   - Thêm bước làm sạch chuỗi `\quad` liên tiếp trước khi render text run / table cell.
4. **Bước 4: Kiểm thử với các bài tập biểu diễn trục số / hình học**:
   - Kiểm tra hiển thị KaTeX preview và file Word xuất ra không còn tình trạng chuỗi `\quad` kéo dài.

## Rủi ro
- **Rủi ro**: Regex làm sạch quá mức có thể ảnh hưởng đến các khoảng cách hợp lệ trong công thức LaTeX phức tạp (ví dụ hệ phương trình có `\quad`).
  - **Khắc phục**: Chỉ lọc bỏ các khối toán CHỈ CHỨA DUY NHẤT chuỗi `\quad`/`\qquad` hoặc khi có từ 3 `\quad` liên tiếp không kèm ký hiệu toán học.

## Cách kiểm thử
1. Thử nghiệm với bài toán biểu diễn trục số (Toán 6 - Bài 3.4):
   - Tạo nội dung Hoạt động C. Luyện tập.
   - Xác nhận cột Nội dung hiển thị lời giải bằng lời văn rõ ràng / tọa độ điểm, không còn khối `$$\quad \quad ...$$`.
2. Kiểm tra phần Preview KaTeX:
   - Xác nhận bảng 2 cột hiển thị gọn gàng, không bị tràn ô hay lỗi font.
3. Kiểm tra Xuất file Word (.docx):
   - Mở file docx, kiểm tra cột Nội dung bảng mục d) căn lề chuẩn, không bị vỡ hàng do khoảng trắng thừa.

## Tiêu chí nghiệm thu
1. Hoàn toàn không còn hiện tượng xuất hiện chuỗi `$$\quad \quad \quad...$$` trong nội dung tạo bởi AI hoặc trong bảng xem trước KaTeX.
2. Lời giải các bài tập vẽ hình/trục số được diễn đạt mạch lạc, chuẩn mực sư phạm.
3. File Word (.docx) xuất ra chuẩn đẹp, bảng 2 cột không bị xô lệch.
