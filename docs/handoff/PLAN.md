# PLAN: Trích Xuất & Nhận Diện Đầy Đủ Số Tiết Của Bài Học Từ PPCT Nguồn (Hỗ Trợ Định Dạng "(2 tiết)", "Tiết 1-2", "2-3", "2 tiết") và Cho Phép Điều Chỉnh Linh Hoạt

## Hiện trạng
1. **Nguyên Nhân Gây Ra Việc Mọi Bài Học Bị Ép Về 1 Tiết**:
   - Hàm `validPeriodCount(value)` trước đây sử dụng `Number.parseInt(String(value).trim(), 10)`.
   - Khi văn bản cột `Số tiết` hoặc `Tiết CT` trong file PPCT của người dùng có dạng:
     + `"(2 tiết)"` hoặc `"(3 tiết)"` $\rightarrow$ Bắt đầu bằng dấu ngoặc đơn `(` $\rightarrow$ `parseInt` trả về `NaN` $\rightarrow$ Bị ép về `1` tiết!
     + `"2 tiết"`, `"3 tiết"` $\rightarrow$ Nếu có khoảng trắng hoặc ký tự bao quanh $\rightarrow$ Dễ bị trả về `1` tiết.
     + Dạng khoảng tiết `"1-2"`, `"3-5"` trong cột Tiết CT $\rightarrow$ Không tự động tính ra hiệu số tiết (2 tiết, 3 tiết).
   - Trong `defaultPpctRows()` mặc định, hệ thống cũng chỉ gán cứng `periods: '1'` cho 35 tuần mà không phản ánh đúng tổng thời lượng năm học (ví dụ Toán 6 có 140 tiết $\approx$ 4 tiết/tuần).
2. **Kỳ Vọng Của Người Dùng**:
   - Khi tải file PPCT lên: Hệ thống phải **nhận diện chính xác 100% số tiết thực tế của từng bài học** từ file gốc (ví dụ bài 2 tiết thì nhận diện đủ 2 tiết, bài 3 tiết nhận diện đủ 3 tiết).
   - Cung cấp ô nhập liệu số tiết trực quan ngay trên từng dòng bài học ở bảng Mục 3 để giáo viên có thể **điều chỉnh tăng/giảm số tiết của bất kỳ bài học nào** sau khi nhận diện.
   - Khi giáo viên thay đổi số tiết của một bài: Bảng chọn tiết AI (`Tiết 1`, `Tiết 2`, `Tiết 3`...) và tổng số tiết/tỷ lệ % AI tự động cập nhật đồng bộ.

## Phạm vi
1. **Nâng Cấp Hàm Trích Xuất & Chuẩn Hóa Số Tiết `validPeriodCount(value)` & `extractLessonPeriods(row)`**:
   - Nhận diện thông minh mọi biến thể định dạng số tiết trong giáo dục:
     * Dạng số kèm chữ: `"2 tiết"`, `"3 tiet"`, `"(2 tiết)"`, `"[3 tiết]"`, `"4 tiết/tuần"` $\rightarrow$ Trích xuất đúng `2`, `3`, `4`.
     * Dạng khoảng tiết / tiết CT: `"1-2"`, `"3-5"`, `"tiết 6 đến 8"` $\rightarrow$ Tự động tính số tiết: `(to - from + 1)` (ví dụ: `1-2` $\rightarrow$ 2 tiết, `3-5` $\rightarrow$ 3 tiết).
     * Dạng số nguyên thuần túy: `2`, `3`, `4`.
   - Nếu cột `Số tiết` bị trống nhưng có cột `Tiết CT` dạng khoảng: Tự động suy diễn số tiết từ `Tiết CT`.
2. **Đồng Bộ Dữ Liệu Khi Giáo Viên Chỉnh Sửa Số Tiết Trên Giao Diện**:
   - Khi giáo viên sửa ô `Số tiết` của một bài học ở Mục 3:
     + Cập nhật giá trị vào `sourcePpctTable` và `sourcePpctRows`.
     + Cập nhật lại số lượng checkbox tiết (`Tiết 1`, `Tiết 2`, `Tiết 3`...) của bài học đó.
     + Cập nhật lại tổng số tiết của môn học và tự động tính lại tỷ lệ `% AI`.
     + Cập nhật số tiết trong bảng xem trước (Preview) và file Word (.docx) xuất ra.
3. **Cải Tiến Cấu Trúc PPCT Mẫu (Khi Chưa Tải File)**:
   - `defaultPpctRows()` phân bổ số tiết hợp lý theo tổng số tiết năm học của môn học (ví dụ: Môn Toán 140 tiết $\rightarrow$ các bài học mẫu phân bổ 3–4 tiết/bài thay vì chỉ 1 tiết).
4. **Cập Nhật Bộ Kiểm Thử Tự Động ([tests/xaydungphuluc-smoke.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/tests/xaydungphuluc-smoke.js))**:
   - Thêm bài kiểm tra assert xác nhận trích xuất đúng số tiết từ các định dạng: `"(2 tiết)"`, `"3 tiết"`, `"1-2"`, `"3-5"`, và kiểm tra phản ứng khi sửa số tiết trên UI.

## Ngoài phạm vi
- Không can thiệp các file ngoài `xaydungphuluc.html` và file test liên quan.

## File dự kiến tác động
- `xaydungphuluc.html` [NÂNG CẤP THUẬT TOÁN TRÍCH XUẤT SỐ TIẾT ĐA ĐỊNH DẠNG, ĐỒNG BỘ THỜI GIAN THỰC KHI ĐIỀU CHỈNH SỐ TIẾT]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG SMOKE TEST CHO TRÍCH XUẤT VÀ ĐIỀU CHỈNH SỐ TIẾT]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Hoàn Thiện Hàm `validPeriodCount(value)` và `normalizePeriods(value)` trong `xaydungphuluc.html`**:
   - Viết regex bóc tách số từ chuỗi có dấu ngoặc đơn, chữ "tiết", hoặc khoảng gạch nối `"1-2"`.
2. **Bước 2: Cập Nhật Trình Bóc Tách Bảng PPCT**:
   - Đảm bảo khi đọc từng hàng từ bảng Word/Excel/PDF, giá trị số tiết thực tế được giữ nguyên vẹn vào `sourcePpctTable` và `sourcePpctRows`.
3. **Bước 3: Hoàn Thiện Hàm `updatePpctLessonPeriods`**:
   - Đảm bảo khi người dùng sửa số tiết trên UI, danh sách tiết của bài học sinh ra đúng $N$ tiết (`Tiết 1`, `Tiết 2`... `Tiết N`) để người dùng tick chọn chính xác từng tiết lẻ.
4. **Bước 4: Chạy và Hoàn Thiện Kiểm Thử**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`, xác nhận PASS 100%.

## Rủi ro
- **Rủi ro**: Dữ liệu số tiết trong file bị ghi dạng chữ như "hai tiết", "ba tiết".
  - *Giải pháp*: Bổ sung bản đồ chuyển đổi số đếm tiếng Việt cơ bản (một $\rightarrow$ 1, hai $\rightarrow$ 2, ba $\rightarrow$ 3, bốn $\rightarrow$ 4).

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy `node tests/xaydungphuluc-smoke.js`:
     + Test `validPeriodCount("(2 tiết)")` $\rightarrow$ 2.
     + Test `validPeriodCount("Tiết 1-3")` $\rightarrow$ 3.
     + Test `validPeriodCount("4 tiết")` $\rightarrow$ 4.
     + Test sửa số tiết từ 2 lên 4 $\rightarrow$ sinh đủ 4 checkbox tiết.
2. **Kiểm thử thủ công trên trình duyệt**:
   - Tải file `Phụ lục 1 - Lớp 6 - Toán.docx` hoặc file PPCT có bài 2 tiết, 3 tiết lên $\rightarrow$ Quan sát các bài học hiển thị đúng 2 tiết, 3 tiết (không bị biến thành 1 tiết).
   - Thử sửa số tiết của Bài 1 từ 1 thành 3 $\rightarrow$ Quan sát xuất hiện đủ `Tiết 1`, `Tiết 2`, `Tiết 3` và tổng số tiết tăng lên chính xác.

## Tiêu chí nghiệm thu
1. Nhận diện chính xác 100% số tiết của từng bài học từ file PPCT tải lên, kể cả khi số tiết được viết dưới dạng `"(2 tiết)"`, `"3 tiết"`, `"1-2"`.
2. Cho phép giáo viên chỉnh sửa số tiết của từng bài học trực tiếp trên giao diện và tự động đồng bộ sang bảng chọn tiết AI, bảng preview và file Word xuất ra.
3. Toàn bộ smoke test tự động đều PASS 100%.
