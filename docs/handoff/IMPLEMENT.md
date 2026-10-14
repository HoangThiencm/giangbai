# IMPLEMENT: Chặn sổ điểm dùng chung giữa hai giáo viên

## Đã làm
1. `api/sodiem.php`: lưu sổ không còn `ON DUPLICATE KEY UPDATE`. Chỉ `UPDATE` đúng `teacher_id` đang đăng nhập. Chưa có dòng thì `INSERT`. Nếu khóa duy nhất cũ không gồm `teacher_id` chặn insert, hệ thống xóa khóa đó rồi insert lại. Không sửa dòng của giáo viên khác. Xóa khóa thất bại thì trả lỗi, không ghi đè.
2. Khi mở hoặc lưu, sổ mới hơn mà phần lớn ô điểm trùng sổ của giáo viên khác (ít nhất 8 ô, khớp từ 85% ô cùng học sinh và cùng cột) bị xóa điểm và nhận xét. Sổ cũ hơn giữ nguyên.
3. Danh sách lớp chỉ còn lớp trong sổ của đúng giáo viên và lớp được gán trên tài khoản. Giáo viên chưa có sổ và chưa được gán lớp thì không thấy mọi lớp của trường.
4. Phản hồi sổ điểm có `Cache-Control: no-store` và `owner_id`. `sodiem.html`, `taobaitap.html` tải kèm mã giáo viên, không dùng cache trình duyệt, và bỏ sổ nếu `owner_id` không đúng tài khoản đang đăng nhập.

## Chưa đụng
- Không đổi Padlet. Không thêm cột mới vào bảng.
- Hai sổ đã lệch nhiều hơn mức trên không bị xóa.

## Kiểm thử
- `php -l api/sodiem.php`
- `node tests/sodiem-smoke.js`
- Chưa đăng nhập hai tài khoản trên trình duyệt.

## Bước tiếp
Hosting chỉ đổi sau khi commit và push `main`. Sau đó đăng xuất, mở lại sổ điểm bằng Ctrl+F5 trên từng tài khoản.
