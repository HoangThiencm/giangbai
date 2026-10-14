# IMPLEMENT: Cô lập sổ điểm theo giáo viên

## Đã làm
1. `api/sodiem.php`: `GET action=load` chỉ đọc sổ của đúng `teacher_id`. Đã xóa fallback sang giáo viên khác. Nếu điểm và nhận xét của sổ này trùng sổ giáo viên khác cùng lớp, môn, năm học thì xóa phần điểm/nhận xét/lịch sử của bản sao và trả `gradebook = null`. `POST action=save` cũng không ghi lại bản sao đó.
2. `sodiem.html`: chờ `api/me.php`, khóa cache là `sodiem:id:${userId}:${lớp}:${môn}:2025-2026`. Cache không có `ownerId` đúng tài khoản đang đăng nhập thì bỏ qua.
3. `taobaitap.html`: cùng khóa theo `user.id` và cùng quy tắc `ownerId`.
4. `tests/sodiem-smoke.js`: chặn fallback, bắt buộc so sánh `teacher_id <> ?`, và kiểm tra khóa theo user id.

## Chưa đụng
- Không đổi schema `gradebooks`.
- Không xóa sổ gốc của giáo viên đã nhập điểm trước.
- Cache trình duyệt cũ (khóa không có user id) không được đọc lại.

## Kiểm thử
- `php -l api/sodiem.php`: không lỗi cú pháp. Dùng `C:\Users\HoangThien\AppData\Local\Temp\php-portable-834\php.exe`.
- `node tests/sodiem-smoke.js`: PASS. Node dùng `C:\Users\HoangThien\AppData\Local\OpenAI\Codex\runtimes\cua_node\cfb32733c877621e\bin\node.exe`.
- Chưa đăng nhập hai tài khoản trên trình duyệt.

## Bước tiếp
Antigravity IDE, chat mới: `/verify`
Trang trên hosting chỉ đổi sau khi commit và push `main`.
