# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Đã chuyển đổi các trường nhập liệu tự do ở Bước 1 sang danh mục chọn (`<select>` dropdown) trực quan, chuẩn hóa:
  + Trường **Môn** (`#fMon`): Chuyển thành `<select>` gồm các môn học chuẩn (*Toán học, Tin học, Khoa học tự nhiên, Ngữ văn, Tiếng Anh, Lịch sử và Địa lí, Giáo dục công dân, Công nghệ, Hoạt động trải nghiệm, hướng nghiệp, Khác*).
  + Trường **Lớp** (`#fLop`): Chuyển thành `<select>` gồm các khối lớp chuẩn THCS (*Lớp 6, Lớp 7, Lớp 8, Lớp 9*) và mở rộng phổ thông (*Lớp 4, Lớp 5, Lớp 10, Lớp 11, Lớp 12*).
  + Trường **Bộ SGK** (`#fSgk`): Chuyển thành `<select>` gồm các bộ sách chuẩn hiện hành (*Kết nối tri thức với cuộc sống, Chân trời sáng tạo, Cánh diều, Cùng khám phá, SGK hiện hành khác*).
- Hỗ trợ tương thích ngược và bảo toàn dữ liệu:
  + Hàm `normalizeSubject()` tự động map giá trị cũ "Toán" sang "Toán học".
  + Hàm `optionList()` tự động bổ sung `<option>` cho bất kỳ giá trị tùy biến nào ngoài danh mục chuẩn để không làm mất dữ liệu đã lưu của người dùng.
  + Hàm `captureMeta()` đọc chính xác giá trị từ các thẻ `<select>` khi chuyển bước hoặc lưu CSDL.
- Không sửa source các module khác ngoài `nghiencuubaihoc.html` và test suite.
- File khóa handoff `docs/handoff/.lock` được giữ nguyên vẹn.

## Test đã chạy
1. `node tests/nghiencuubaihoc-smoke.js` -> PASS
2. `node tests/xaydungphuluc-integration-smoke.js` -> PASS
3. `node tests/duyetgiaoan-integration-smoke.js` -> PASS
4. `node tests/duyetgiaoan-smoke.js` -> PASS
5. `node tests/user-ai-settings-smoke.js` -> PASS
6. `node tests/security-f12-smoke.js` -> PASS

## Pass / Fail từng tiêu chí
1. `#fMon` là dropdown `<select>` chọn nhanh môn học, mặc định "Toán học": PASS
2. `#fLop` là dropdown `<select>` chọn nhanh khối lớp, mặc định "6" (hiển thị "Lớp 6"): PASS
3. `#fSgk` là dropdown `<select>` chọn bộ SGK chuẩn hiện hành: PASS
4. Không còn các thẻ `<input id="fMon">`, `<input id="fLop">`, `<input id="fSgk">` dạng text tự do: PASS
5. Dữ liệu cũ được bảo lưu chính xác và tương thích mềm: PASS
6. Bài test `tests/nghiencuubaihoc-smoke.js` chạy PASS 100%: PASS
7. Toàn bộ test suite liên quan không phát sinh lỗi hồi quy: PASS

## Bug
Không phát hiện lỗi.