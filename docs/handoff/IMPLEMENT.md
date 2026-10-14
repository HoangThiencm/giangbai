# IMPLEMENT: Cô lập danh sách lớp và điểm theo giáo viên

## Đã làm
1. `api/sodiem.php`: danh sách lớp yêu cầu đăng nhập. Chỉ trả lớp trong sổ của đúng `teacher_id` và lớp được gán trên tài khoản. Không còn gộp mọi lớp từ mọi sổ giáo viên. Giáo viên chưa có sổ và chưa được gán lớp thì mới thấy danh sách lớp của trường, không kèm điểm.
2. Khóa duy nhất của `gradebooks` được chỉnh để gồm `teacher_id`. Lưu sổ của giáo viên này không ghi đè sổ của giáo viên khác.
3. Sổ mới hơn mà điểm và nhận xét trùng sổ cũ hơn của giáo viên khác thì bị xóa phần điểm. Sổ gốc giữ nguyên.
4. `sodiem.html` và `taobaitap.html`: cache và lớp vừa mở gắn `id` tài khoản đang đăng nhập. Tải sổ thành công thì không trộn cache máy. Không còn lấy danh sách lớp chung từ `api/exam.php`.

## Chưa đụng
- Không đổi schema cột. Không đổi Padlet.
- Hai sổ đã lệch nhau (mỗi người đã sửa thêm điểm riêng) không bị xóa.

## Kiểm thử
- `php -l api/sodiem.php`: không lỗi cú pháp. Dùng `C:\Users\HoangThien\AppData\Local\Temp\php-portable-834\php.exe`.
- `node tests/sodiem-smoke.js`: PASS. Node dùng `C:\Users\HoangThien\AppData\Local\OpenAI\Codex\runtimes\cua_node\cfb32733c877621e\bin\node.exe`.
- Chưa đăng nhập hai tài khoản trên trình duyệt.

## Bước tiếp
Antigravity IDE, chat mới: `/verify`
Hosting chỉ đổi sau khi commit và push `main`.
