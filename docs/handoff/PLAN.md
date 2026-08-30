# PLAN: Khóa chuẩn tổng thời lượng 90 phút (chống lặp Hoạt động D) và Triệt tiêu 7 trang dòng chấm trong Phụ lục Phiếu học tập

## Hiện trạng
1. **Vấn đề 1: Phân chia sai thời lượng (Hoạt động B bị gán 75 phút thay vì 45 phút, tổng bài 120-131 phút) và Bị lặp 2 lần Hoạt động D**:
   - Khi bài học khai báo 02 tiết (90 phút), mẫu prompt 1-click `GENERATE_ACTIVITIES_AE` và mẫu riêng `GENERATE_ACTIVITY_B` chưa khóa cứng phân bổ số phút cho các hoạt động nhánh con (2.1, 2.2,...). AI tự ý gán nhánh 2.1 là 45 phút, nhánh 2.2 là 30 phút, khiến riêng Hoạt động B bị đội lên 75 phút, kéo tổng thời gian cả bài lên 120–131 phút.
   - Hoạt động D (`## D. HOẠT ĐỘNG 4: VẬN DỤNG (11 phút)`) bị xuất lặp lại 2 lần trong giáo án tổng hợp do hàm cắt/dedupe chưa lọc triệt để khi AI vô tình trả về nhiều hơn 1 khối D hoặc khi ghép nối các hoạt động.

2. **Vấn đề 2: Mục IV. Phụ lục F (Phiếu học tập) sinh ra 7 trang toàn dòng chấm chấm `........................................`**:
   - Khi tạo Phụ lục F (`GENERATE_PORTFOLIO_WORKSHEETS`), để chừa chỗ trống cho học sinh làm bài dưới bảng KWL / phiếu học tập, AI sinh ra 50–80 dòng liên tiếp toàn dấu chấm `................................................................................`.
   - Trong `js/khbd-docx.js`, mỗi dòng chấm được phân tích thành 1 đoạn văn Word (Paragraph) độc lập có khoảng đệm dòng (line spacing & space after). Hàng chục dòng chấm này làm phình tài liệu ra thành **7 trang giấy trắng** toàn dấu chấm vô nghĩa.

## Phạm vi
1. **Khắc phục Vấn đề 1: Khóa cứng thời lượng 90 phút và Dedupe Hoạt động D (`js/khbd-prompts.js`, `js/khbd-app.js`)**:
   - Trong `js/khbd-prompts.js`:
     * Cập nhật `GENERATE_ACTIVITIES_AE`, `GENERATE_ACTIVITY_B`, `GENERATE_ACTIVITIES_AD`, `OUTPUT_CONTRACT`:
       + Khóa cứng thời lượng Hoạt động B = `{time_budget_B}`. Ghi rõ trong chỉ thị: **Nếu chia N nhánh con (2.1, 2.2,...), tổng số phút của N nhánh con cộng lại BẮT BUỘC ĐÚNG BẰNG {time_budget_B}** (Ví dụ 45 phút chia 2 nhánh thì bắt buộc là 23 phút và 22 phút; TUYỆT ĐỐI CẤM gán 45 phút + 30 phút = 75 phút).
       + Khóa cứng tổng thời lượng cả bài (A + B + C + D + E) = `{duration}` (02 tiết = đúng 90 phút).
       + Trong `GENERATE_ACTIVITIES_AE`, khóa đúng 5 marker duy nhất, nghiêm cấm xuất lặp lại marker hoặc tiêu đề Hoạt động D.
   - Trong `js/khbd-app.js`:
     * Tăng cường `clipKhbdActivityMarkdown("D", text)` và `parseKhbdSections`: Nếu phát hiện lặp lại tiêu đề D (`## D. HOẠT ĐỘNG 4`), chỉ giữ lại duy nhất 1 khối D chuẩn mực.
     * Bổ sung hàm chuẩn hóa thời lượng (`normalizeActivityTimeHeadings`): Tự động phát hiện và điều chỉnh lại số phút trên tiêu đề các hoạt động khớp với `calculateActivityTimeBudgets` nếu AI sinh sai tổng thời gian.

2. **Khắc phục Vấn đề 2: Triệt tiêu các trang dòng chấm rác trong Phụ lục F và file Word (`js/khbd-prompts.js`, `js/khbd-docx.js`, `js/khbd-app.js`)**:
   - Trong `js/khbd-prompts.js`:
     * Cập nhật `GENERATE_PORTFOLIO_WORKSHEETS`: Nghiêm cấm AI sinh các dòng chấm chấm lặp lại liên tiếp; yêu cầu toàn bộ câu hỏi và phần trả lời của học sinh phải nằm gọn trong các ô của BẢNG (Table) hoặc tối đa 1–2 dòng chấm ngắn cho mỗi câu hỏi; khống chế dung lượng Phụ lục F chỉ gọn gàng trong 1–2 trang in Word.
   - Trong `js/khbd-docx.js` & `js/khbd-app.js`:
     * Cài đặt bộ lọc rút gọn dòng chấm lặp lại (`collapseDottedLines` / `stripExcessiveDottedLines`): Khi phát hiện từ 3 dòng liên tiếp chỉ chứa dấu chấm/gạch ngang (`/^\s*[.\-_…\s]{10,}\s*$/`), tự động rút gọn chỉ giữ lại tối đa 1–2 dòng, ngăn chặn triệt để việc sinh 7 trang dấu chấm trong Word.

3. **Bộ kiểm thử tự động (Unit / Smoke Tests)**:
   - Viết test `tests/khbd-dotted-lines-smoke.js` kiểm tra bộ lọc dọn sạch các dòng chấm lặp lại không để phình trang Word.
   - Viết test `tests/khbd-activity-d-dedupe-smoke.js` kiểm tra dedupe Hoạt động D và bảo toàn tổng thời gian 90 phút cho bài 2 tiết.

## Ngoài phạm vi
- Không thay đổi công thức tính toán `calculateActivityTimeBudgets`.
- Không thay đổi cấu trúc sư phạm 4 bước CV 5512.

## File dự kiến tác động
- `js/khbd-prompts.js`
- `js/khbd-app.js`
- `js/khbd-docx.js`
- `tests/khbd-dotted-lines-smoke.js`
- `tests/khbd-activity-d-dedupe-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Cập nhật `js/khbd-prompts.js`**:
   - Siết chặt quy tắc thời lượng Hoạt động B và toàn bài trong `GENERATE_ACTIVITIES_AE` và `GENERATE_ACTIVITY_B`.
   - Cập nhật `GENERATE_PORTFOLIO_WORKSHEETS` cấm sinh các khối dòng chấm rác kéo dài.
2. **Bước 2: Cập nhật `js/khbd-docx.js` & `js/khbd-app.js`**:
   - Thêm bộ lọc `collapseDottedLines` trong `parseMarkdownToDocxElements` và `sanitizeLessonMarkdown`.
   - Tăng cường `clipKhbdActivityMarkdown` dedupe triệt để cho Hoạt động D và chuẩn hóa số phút tiêu đề.
3. **Bước 3: Viết các bài kiểm thử tự động**:
   - Viết `tests/khbd-dotted-lines-smoke.js` và `tests/khbd-activity-d-dedupe-smoke.js`.
4. **Bước 4: Chạy toàn bộ test suites**:
   - Xác nhận tất cả bài kiểm thử đều PASS 100%.

## Rủi ro
- **Rủi ro**: Lọc nhầm dòng chấm trong bảng kẻ mẫu in ngắn (như `Họ và tên: ....................`).
  - **Khắc phục**: Bộ lọc chỉ rút gọn khi có từ 3 dòng chấm riêng biệt liên tiếp đứng ngoài bảng.

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy `node tests/khbd-dotted-lines-smoke.js`: Kiểm tra khối văn bản chứa 50 dòng chấm được rút gọn về 1 dòng duy nhất khi qua bộ lọc Word.
   - Chạy `node tests/khbd-activity-d-dedupe-smoke.js`: Kiểm tra văn bản chứa 2 khối Hoạt động D bị cắt chỉ giữ lại 1 khối duy nhất; kiểm tra tổng số phút 5 hoạt động đúng 90 phút.
2. **Kiểm thử thủ công trên giao diện**:
   - Tạo bài học 2 tiết, mở tab Hoạt động D và Phụ lục F:
     * Kiểm tra không còn bị lặp lại tiêu đề `## D. HOẠT ĐỘNG 4`.
     * Kiểm tra Hoạt động B có số phút là (45 phút) và các nhánh con (23p, 22p), tổng bài đúng 90 phút.
     * Xuất file Word (.docx), mở lên kiểm tra: Phụ lục F gọn gàng 1–2 trang, hoàn toàn không còn 7 trang dòng chấm `....................`.

## Tiêu chí nghiệm thu
1. Giáo án 2 tiết có tổng thời lượng các hoạt động A, B, C, D, E khớp chính xác 100% bằng 90 phút (Hoạt động B đúng 45 phút, các nhánh con cộng lại đúng 45 phút), không lặp lại Hoạt động D.
2. Mục IV. Phụ lục F được trình bày gọn gàng trong bảng hoặc 1–2 dòng điền, loại bỏ hoàn toàn hiện tượng sinh 7 trang giấy trắng toàn dòng chấm `.....`.
3. Tất cả bài kiểm thử liên quan đều PASS 100%.
