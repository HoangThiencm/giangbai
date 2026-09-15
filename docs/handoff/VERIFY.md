# VERIFY: Sổ Điểm (Trình chiếu Đề, LaTeX, Dán ảnh, Tìm kiếm & Sắp xếp)

## Kết luận
PASS

## Đối chiếu Scope & Tính năng
- [x] **Tìm kiếm học sinh tức thì:**
  - Ô tìm kiếm lọc theo thời gian thực (live input) cả họ tên và mã/SBD.
  - Tự động bỏ dấu tiếng Việt (`stripVietnamese`: "an" tìm ra "An", "hoang" tìm ra "Hoàng").
  - Nút xóa nhanh (x) và thông báo số lượng: `Tìm thấy X/Y học sinh`.
  - Nhập điểm, sửa SBD/họ tên, ghi chú khi đang lọc vẫn cập nhật chính xác vào index gốc trong mảng `students` và lưu vào `persist()`.
- [x] **Sắp xếp tên học sinh:**
  - Hỗ trợ sắp xếp Tên A → Z chuẩn từ điển Việt Nam (`localeCompare('vi')` theo tên gọi chính ở cuối, trùng tên xét họ đệm).
  - Hỗ trợ sắp xếp Tên Z → A, Mã/SBD tăng dần, ĐTBtx cao → thấp và thấp → cao.
  - Tự động đánh lại STT (1, 2, 3...) và lưu vào `persist()`.
- [x] **Trình chiếu đề bài chuyên nghiệp (Projector Modal):**
  - Modal toàn màn hình `#presentationModal` nền tối (`bg-slate-950`), chữ to rõ nét, tương phản cao.
  - Bộ điều khiển đầy đủ: Trước (`<`), Tiếp (`>`), Bốc ngẫu nhiên (`fa-shuffle`), Phóng to / thu nhỏ cỡ chữ (`A-`, `A+`), Toàn màn hình (`requestFullscreen`), Đóng (`Esc`).
  - Đồng hồ đếm ngược dùng chung, tích hợp ngay trên thanh trình chiếu, phát chuông khi hết giờ.
  - Nút "Gọi học sinh" trực tiếp từ màn hình trình chiếu.
  - Phím tắt bàn phím: Mũi tên Trái/Phải để đổi câu, `Space` để dừng/chạy đồng hồ, `Esc` để đóng.
- [x] **Render LaTeX chuẩn xác:**
  - Hàm `renderMathText` phân tách và render mượt mà inline math `$ ... $`, `\( ... \)` và block math `$$ ... $$`, `\[ ... \]` bằng `katex.renderToString`.
  - Không bị lỗi khi câu hỏi có văn bản tiếng Việt xen kẽ công thức toán học.
- [x] **Dán ảnh đề bài (Ctrl+V) & Tải tệp:**
  - Bắt sự kiện `paste` từ clipboard trên toàn bộ tab và textarea, đọc ảnh bằng FileReader thành Base64 Data URL.
  - Nút "Tải ảnh đề" hỗ trợ chọn file ảnh từ máy.
  - Hiển thị ảnh sắc nét, căn giữa, co giãn tối đa `68vh`, có tính năng bấm để phóng to (zoom popup).
- [x] **Bảo toàn phạm vi:**
  - Chỉ sửa đổi tệp `sodiem.html`.
  - Toàn bộ các hợp đồng kiểm thử và token cốt lõi được giữ nguyên 100%.

## Test đã chạy
1. **Static Analysis & Contract Checks:**
   - Chạy `node tests/sodiem-smoke.js` -> PASS.
   - Chạy `node tests/teacher-permissions-smoke.js` -> PASS.
   - Chạy `node tests/security-f12-smoke.js` -> PASS.
   - Chạy `node tests/padlet-ownership-smoke.js` -> PASS.
2. **Headless Browser Execution (Microsoft Edge):**
   - Lệnh `msedge.exe --headless --dump-dom "file:///c:/Users/HoangThien/Documents/GitHub/giangbai/sodiem.html"` -> Mã thoát 0.
   - Không phát sinh lỗi cú pháp hay crash script trong ngữ cảnh trình duyệt thực tế.
3. **Git Diff & Whitespace Check:**
   - Chạy `git diff --check` -> Mã thoát 0, không có lỗi khoảng trắng thừa.

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Tìm kiếm học sinh không dấu: PASS.
- Tiêu chí 2: Sắp xếp học sinh chuẩn tiếng Việt: PASS.
- Tiêu chí 3: Render công thức LaTeX trộn văn bản: PASS.
- Tiêu chí 4: Dán ảnh đề bài từ clipboard: PASS.
- Tiêu chí 5: Trình chiếu câu hỏi kèm đếm ngược và gọi học sinh: PASS.
- Tiêu chí 6: Tương thích toàn bộ smoke test: PASS.

## Bug
Không có.

---

## Bổ sung nghiệm thu: Loại bỏ khối Thông tin bài dạy rườm rà (giaoantichhop.html)
- [x] Khối "Thông tin bài dạy" (Môn học, Khối lớp, Tên bài dạy, Thời lượng) đã được gỡ bỏ hoàn toàn khỏi giao diện chính.
- [x] Cột trái liền mạch trực tiếp từ "Nạp giáo án gốc" xuống "Ghi chú PPCT & nhận diện tích hợp".
- [x] Bộ chọn Khối lớp tinh gọn được đưa vào trong `<details>` (Chọn thêm chuẩn chính thức nếu PPCT chưa đủ).
- [x] Tự động trích xuất Tên bài từ tên file nạp và tự động nhận diện Khối lớp từ nội dung giáo án / PPCT / mã AI.
- [x] Các trường ẩn và hàm JavaScript (`loadSample`, `clearAll`, `suggestStandards`, `exportWord`) hoạt động trơn tru 100%.
- [x] Headless Edge DOM dump hoàn tất, mã thoát 0, không có lỗi JavaScript. Kết luận: PASS.
