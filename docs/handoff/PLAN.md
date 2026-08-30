# PLAN: Khắc phục lỗi hiển thị gạch dưới `_Trạm X:_` trong Word và Khóa chuẩn tổng thời lượng 90 phút cho bài 02 tiết

## Hiện trạng
1. **Vấn đề 1: Ký tự gạch dưới `_Trạm 1 (Khám phá số nguyên âm):_` và rò rỉ dòng phân cách bảng trong Word**:
   - Khi AI sinh Markdown có cú pháp in nghiêng bằng dấu gạch dưới (như `_Trạm 1 (Khám phá số nguyên âm):_`, `_Trạm 2:..._`), hàm `parseInlineTextToRuns` trong `js/khbd-docx.js` chỉ nhận diện cú pháp `*...*` và `**...**` mà bỏ sót cú pháp `_..._` và `__...__`.
   - Do đó, thư viện docx không bóc tách được định dạng in nghiêng mà xuất nguyên văn các ký tự gạch dưới `_` ra file Word.
   - Ngoài ra, ở cuối bảng nội dung đôi khi rò rỉ dòng tiêu đề bài hoặc ký tự pipe thừa (`Bài 13: ... |`, `---`, `|`) tạo thành các ô/đường kẻ đơn lẻ thừa trong tài liệu Word (như ảnh người dùng cung cấp).

2. **Vấn đề 2: Khai báo bài học 02 tiết nhưng tổng thời gian các hoạt động bị đội lên 135 phút**:
   - Khi khai báo 02 tiết (tương đương 90 phút), hàm `calculateActivityTimeBudgets` tính toán phân bổ chuẩn (A: 7 phút, B: 45 phút, C: 23 phút, D: 11 phút, E: 4 phút; tổng đúng 90 phút).
   - Tuy nhiên, trong `PROMPTS.GENERATE_ACTIVITY_B` tại `js/khbd-prompts.js`, tiêu đề chỉ ghi `## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI` mà thiếu placeholder `{time_budget_B}`.
   - Đồng thời, prompt chưa có chỉ thị khóa cứng tổng thời lượng của các hoạt động nhánh con (2.1, 2.2, 2.3...), khiến AI tự tiện gán mỗi nhánh 25–30 phút (hoặc 3 trạm x 30 phút = 90 phút riêng cho mục B), cộng thêm các hoạt động C, D, A làm tổng thời gian toàn bài bị đội lên tới 135 phút (vượt quá thời lượng 2 tiết).

## Phạm vi
1. **Khắc phục Vấn đề 1: Xử lý định dạng `_italic_`, `__bold__` và dọn rác bảng trong Word (`js/khbd-docx.js`, `js/khbd-prompts.js`, `js/khbd-app.js`)**:
   - Trong `js/khbd-docx.js`:
     * Cập nhật `parseInlineTextToRuns` nhận diện cú pháp `_..._` (in nghiêng) và `__...__` (in đậm) của Markdown, chuyển đổi thành docx `TextRun` có `italics: true` / `bold: true` và bóc bỏ dấu gạch dưới `_`.
     * Trong `parseMarkdownToDocxElements`, bổ sung bộ lọc loại bỏ các dòng rác phân cách bảng đơn lẻ (`|`, `---`, `|---|`, dòng chỉ có dấu pipe rò rỉ).
   - Trong `js/khbd-prompts.js`:
     * Chỉ thị AI dùng phân cấp gạch đầu dòng chuẩn (`- `, `+ `, `* `), không dùng cú pháp `_Trạm X:_` gây hiểu nhầm.
   - Trong `js/khbd-app.js`:
     * Tăng cường `mergeSplitActivityTables` và `sanitizeLessonMarkdown` để dọn sạch các dòng pipe rác cuối bảng.

2. **Khắc phục Vấn đề 2: Khóa cứng tổng thời lượng các hoạt động khớp 100% thời lượng bài dạy (`js/khbd-prompts.js`, `js/khbd-app.js`)**:
   - Trong `js/khbd-prompts.js`:
     * Đưa `{time_budget_B}` vào tiêu đề Hoạt động B: `## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC ({time_budget_B})`.
     * Bổ sung quy tắc bắt buộc trong `ACTIVITY_TABLE_CONTRACT` và `PROMPTS.GENERATE_ACTIVITY_B`: **Tổng số phút của tất cả các hoạt động con (2.1, 2.2, 2.3...) trong Hoạt động B cộng lại BẮT BUỘC ĐÚNG BẰNG {time_budget_B}** (Ví dụ Hoạt động B là 45 phút chia 3 hoạt động nhánh thì mỗi nhánh là 15 phút; CẤM để mỗi nhánh 25–30 phút).
     * Bổ sung quy tắc khóa tổng thời lượng toàn bài trong `PROMPTS.OUTPUT_CONTRACT`: **Tổng thời lượng A + B + C + D + E BẮT BUỘC PHẢI KHỚP 100% VỚI THỜI LƯỢNG TIẾT DẠY LÀ {duration}** (02 tiết = đúng 90 phút, 01 tiết = đúng 45 phút, 03 tiết = đúng 135 phút).
   - Trong `js/khbd-app.js`:
     * Đảm bảo `getGenerationPromptContext` luôn truyền chuẩn xác `appState.duration` (ví dụ "02 tiết (90 phút)") vào các mẫu prompt.

3. **Bộ kiểm thử tự động (Unit / Smoke Tests)**:
   - Viết test `tests/khbd-docx-format-smoke.js` kiểm tra `parseInlineTextToRuns` bóc tách đúng `_italic_`, `__bold__`, `*italic*`, `**bold**`.
   - Cập nhật test `tests/khbd-time-budgets-smoke.js` kiểm tra `{time_budget_B}` được thay thế chuẩn và tổng thời gian các hoạt động trong template luôn khớp 100% với duration.

## Ngoài phạm vi
- Không thay đổi công thức tính toán `calculateActivityTimeBudgets` (hàm đã phân bổ đúng 90 phút cho 2 tiết).
- Không thay đổi cấu trúc sư phạm 4 bước CV 5512.

## File dự kiến tác động
- `js/khbd-docx.js`
- `js/khbd-prompts.js`
- `js/khbd-app.js`
- `tests/khbd-docx-format-smoke.js`
- `tests/khbd-time-budgets-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Cập nhật `parseInlineTextToRuns` và `parseMarkdownToDocxElements` trong `js/khbd-docx.js`**:
   - Hỗ trợ đầy đủ `_..._` và `__...__`.
   - Lọc bỏ các dòng pipe rác/separator rò rỉ cuối bảng.
2. **Bước 2: Cập nhật các mẫu prompt trong `js/khbd-prompts.js`**:
   - Thêm `{time_budget_B}` vào tiêu đề Hoạt động B.
   - Thêm chỉ thị bắt buộc tổng các nhánh con trong B bằng `{time_budget_B}` và tổng toàn bài bằng `{duration}`.
   - Hướng dẫn AI không dùng dấu gạch dưới `_Trạm X:_`.
3. **Bước 3: Tinh chỉnh hàm lọc rò rỉ bảng trong `js/khbd-app.js`**:
   - Đảm bảo `sanitizeLessonMarkdown` dọn sạch các dòng thừa dấu `|` hoặc `---` đơn độc.
4. **Bước 4: Viết bài test tự động**:
   - Viết `tests/khbd-docx-format-smoke.js` và cập nhật `tests/khbd-time-budgets-smoke.js`.
5. **Bước 5: Chạy toàn bộ test suites**:
   - Xác nhận tất cả bài test liên quan đều PASS 100%.

## Rủi ro
- **Rủi ro**: Dấu gạch dưới `_` trong công thức toán học (`x_1`, `a_{ij}`) nếu parse nhầm thành in nghiêng có thể làm hỏng công thức.
  - **Khắc phục**: Thuật toán `parseInlineTextToRuns` đã ưu tiên bóc tách công thức LaTeX `$..$` và `$$..$$` trước khi parse các thẻ định dạng inline.

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy `node tests/khbd-docx-format-smoke.js`: Kiểm tra chuỗi `_Trạm 1 (Khám phá):_` chuyển đổi thành TextRun có `italics: true` và text là `Trạm 1 (Khám phá):`.
   - Chạy `node tests/khbd-time-budgets-smoke.js`: Kiểm tra prompt Activity B chứa đúng `{time_budget_B}` và quy tắc tổng thời gian 90 phút cho 2 tiết.
2. **Kiểm thử thủ công trên giao diện**:
   - Mở `soankhbd.html`, chọn bài 02 tiết và tạo các hoạt động:
     * Kiểm tra tiêu đề Hoạt động B hiển thị rõ số phút phân bổ (ví dụ: `(45 phút)`).
     * Kiểm tra các hoạt động con (2.1, 2.2,...) có số phút cộng lại đúng bằng 45 phút.
     * Xuất file Word (.docx), mở lên kiểm tra: Không còn ký tự `_Trạm 1:_` thô, văn bản in nghiêng đẹp mắt, không có dòng rác `|` hay `---` rò rỉ.

## Tiêu chí nghiệm thu
1. File Word xuất ra hiển thị định dạng in nghiêng chuẩn mực, bóc sạch ký tự gạch dưới `_Trạm X:_` và không rò rỉ đường kẻ/dấu pipe thừa.
2. Tiêu đề Hoạt động B và toàn bộ các hoạt động con có thời lượng chuẩn xác, tổng thời lượng toàn bộ giáo án 2 tiết đúng 90 phút (không bị đội lên 135 phút).
3. Toàn bộ các bài kiểm thử liên quan đều PASS 100%.


