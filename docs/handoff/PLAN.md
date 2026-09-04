# PLAN: Chuyển Đổi Ô Nhập Môn Và Lớp Thành Danh Mục Chọn (Select Dropdown) Trong Nghiên Cứu Bài Học

## Hiện trạng
1. **Vấn đề giao diện nhập liệu ở Bước 1**:
   - Trong `nghiencuubaihoc.html` (Bước 1 - Khởi tạo hồ sơ), trường **Môn** (`#fMon`) và **Lớp** (`#fLop`) hiện là các thẻ `<input type="text">` tự do:
     ```html
     <label class="text-xs font-bold">Môn<input id="fMon" class="mt-1 w-full rounded-lg border p-2" value="${esc(state.meta.monHoc)}"></label>
     <label class="text-xs font-bold">Lớp<input id="fLop" class="mt-1 w-full rounded-lg border p-2" value="${esc(state.meta.lop)}"></label>
     ```
   - Nhược điểm:
     + Người dùng phải gõ tay thủ công, bất tiện trên cả máy tính lẫn thiết bị di động.
     + Thiếu chuẩn hóa tên gọi (ví dụ: người gõ "Toán", người gõ "Toán học", người gõ "Lớp 6", "6", "K6"...), gây khó khăn cho việc tra cứu tự động YCCĐ trong `window.KHBD_YCCD` và tra cứu danh mục NLS/AI trong `window.KHBD_STANDARDS`.
     + Trường **Bộ SGK** (`#fSgk`) cũng đang là ô nhập tay, chưa có gợi ý các bộ SGK chính thức theo CTGDPT 2018 (Kết nối tri thức, Chân trời sáng tạo, Cánh diều).

## Phạm vi
1. **Chuyển trường Môn (`#fMon`) thành danh mục chọn `<select>`**:
   - Cung cấp danh sách môn học chuẩn theo Chương trình GDPT 2018 cấp THCS và phổ thông:
     + Toán học (mặc định)
     + Tin học
     + Khoa học tự nhiên
     + Ngữ văn
     + Tiếng Anh
     + Lịch sử và Địa lí
     + Giáo dục công dân
     + Công nghệ
     + Hoạt động trải nghiệm, hướng nghiệp
     + Khác...
   - Hỗ trợ giữ nguyên và hiển thị đúng nếu hồ sơ cũ đã lưu môn học khác hoặc giá trị tùy biến.
2. **Chuyển trường Lớp (`#fLop`) thành danh mục chọn `<select>`**:
   - Cung cấp danh sách khối lớp chuẩn THCS:
     + Lớp 6 (value="6", mặc định)
     + Lớp 7 (value="7")
     + Lớp 8 (value="8")
     + Lớp 9 (value="9")
     + Mở rộng hỗ trợ các khối lớp liên thông: Lớp 4, Lớp 5, Lớp 10, Lớp 11, Lớp 12.
3. **Chuẩn hóa trường Bộ SGK (`#fSgk`)**:
   - Chuyển thành `<select id="fSgk">` (hoặc input kèm `<datalist>` gợi ý) với các bộ SGK hiện hành:
     + Kết nối tri thức với cuộc sống
     + Chân trời sáng tạo
     + Cánh diều
     + Cùng khám phá
     + SGK hiện hành khác
4. **Bảo toàn dữ liệu cũ và đồng bộ trạng thái**:
   - Cập nhật hàm `captureMeta()` và `stepBody()` đảm bảo việc đọc giá trị từ `<select>` và khôi phục giá trị đã lưu trong `state.meta` khi mở lại hồ sơ từ CSDL (`loadSessionById()`) diễn ra chính xác 100%.
   - Xử lý tương thích mềm: nếu dữ liệu cũ có "Toán", hệ thống tự động map khớp với option "Toán học".
5. **Cập nhật bộ kiểm thử tự động**:
   - Cập nhật `tests/nghiencuubaihoc-smoke.js` để kiểm tra các thẻ `<select id="fMon">`, `<select id="fLop">`, `<select id="fSgk">` và các tùy chọn tương ứng.

## Ngoài phạm vi
- Không thay đổi các bước nghiệp vụ sư phạm từ Bước 2 đến Bước 12.
- Không thay đổi cấu trúc bảng cơ sở dữ liệu `nghien_cuu_bai_hoc_sessions` trong `api/nghiencuubaihoc.php`.
- Không can thiệp vào các trang khác (`soankhbd.html`, `xaydungphuluc.html`, `duyetgiaoan.html`, `duyetde.html`).

## File dự kiến tác động
- `nghiencuubaihoc.html` [SỬA: Chuyển các trường Môn, Lớp, Bộ SGK thành `<select>` dropdown chuẩn]
- `tests/nghiencuubaihoc-smoke.js` [SỬA: Bổ sung assertion kiểm tra các thẻ select và options của Môn, Lớp, Bộ SGK]
- `docs/handoff/PLAN.md` [GHI ĐÈ: Kế hoạch bàn giao cho Coder]
- `docs/handoff/.lock` [GHI MỚI: Khóa handoff cho Coder]

## Các bước thực hiện
1. **Bước 1: Cập nhật giao diện trong `nghiencuubaihoc.html`**:
   - Định nghĩa danh mục mảng chuẩn:
     ```javascript
     const SUBJECT_OPTIONS = ['Toán học', 'Tin học', 'Khoa học tự nhiên', 'Ngữ văn', 'Tiếng Anh', 'Lịch sử và Địa lí', 'Giáo dục công dân', 'Công nghệ', 'Hoạt động trải nghiệm, hướng nghiệp', 'Khác'];
     const GRADE_OPTIONS = ['6', '7', '8', '9', '4', '5', '10', '11', '12'];
     const SGK_OPTIONS = ['Kết nối tri thức với cuộc sống', 'Chân trời sáng tạo', 'Cánh diều', 'Cùng khám phá', 'SGK hiện hành khác'];
     ```
   - Trong hàm `stepBody()` (Bước 1):
     + Thay thế `<input id="fMon">` bằng `<select id="fMon" class="mt-1 w-full rounded-lg border border-slate-300 bg-white p-2">...`
     + Thay thế `<input id="fLop">` bằng `<select id="fLop" class="mt-1 w-full rounded-lg border border-slate-300 bg-white p-2">...`
     + Thay thế `<input id="fSgk">` bằng `<select id="fSgk" class="mt-1 w-full rounded-lg border border-slate-300 bg-white p-2">...`
   - Đảm bảo option đang được chọn khớp với `state.meta.monHoc`, `state.meta.lop`, `state.meta.boSgk`. Nếu giá trị hiện tại chưa có trong danh sách chuẩn, tự động bổ sung một `<option>` để không làm mất dữ liệu tùy biến của người dùng.
2. **Bước 2: Chuẩn hóa hàm đọc dữ liệu `captureMeta()`**:
   - Đảm bảo `captureMeta()` đọc đúng `.value` từ các phần tử `<select>`.
3. **Bước 3: Cập nhật bộ kiểm thử `tests/nghiencuubaihoc-smoke.js`**:
   - Bổ sung kiểm tra sự tồn tại của `select id="fMon"`, `select id="fLop"`, `select id="fSgk"`.
   - Kiểm tra các tùy chọn chuẩn 'Toán học', 'Tin học', 'Khoa học tự nhiên', 'Lớp 6', 'Lớp 7', 'Lớp 8', 'Lớp 9', 'Kết nối tri thức', 'Cánh diều'.
4. **Bước 4: Chạy kiểm thử tự động**:
   - Chạy `node tests/nghiencuubaihoc-smoke.js`.
   - Chạy các smoke test liên quan.

## Rủi ro
- Hồ sơ cũ lưu giá trị "Toán" có thể không khớp chính xác chuỗi "Toán học":
  - *Giải pháp*: Trong hàm sinh `<option>`, thêm cơ chế chuẩn hóa mềm (normalize): nếu giá trị đã lưu là "Toán" thì tự động đánh dấu selected cho option "Toán học", hoặc tự động thêm `<option value="${val}" selected>` nếu là giá trị tùy biến.

## Cách kiểm thử
1. **Kiểm thử tự động**:
   ```powershell
   node tests/nghiencuubaihoc-smoke.js
   ```
2. **Kiểm thử thủ công**:
   - Mở `nghiencuubaihoc.html`:
     + Tại Bước 1, quan sát thấy ô **Môn**, **Lớp**, **Bộ SGK** đã trở thành danh sách thả xuống (dropdown) đẹp mắt.
     + Bấm chọn thử: Môn = "Toán học", Lớp = "6", Bộ SGK = "Kết nối tri thức với cuộc sống".
     + Chuyển sang Bước 2 rồi quay lại Bước 1: giá trị đã chọn vẫn được bảo lưu chính xác.
     + Lưu hồ sơ lên CSDL và mở lại: giá trị đã chọn hiển thị đúng trong dropdown.

## Tiêu chí nghiệm thu
1. Trường Môn (`#fMon`) là dropdown `<select>` chứa các môn học chuẩn, mặc định "Toán học".
2. Trường Lớp (`#fLop`) là dropdown `<select>` chứa các khối lớp chuẩn THCS (6, 7, 8, 9) và phổ thông, mặc định "6".
3. Trường Bộ SGK (`#fSgk`) là dropdown `<select>` chứa các bộ SGK chuẩn hiện hành.
4. Việc chuyển bước, lưu CSDL và mở lại hồ sơ bảo toàn chính xác giá trị đã chọn.
5. Bài test `tests/nghiencuubaihoc-smoke.js` chạy PASS 100%.
6. File handoff `docs/handoff/PLAN.md` và `docs/handoff/.lock` được thiết lập chuẩn xác.