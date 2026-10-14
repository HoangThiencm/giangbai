# IMPLEMENT: Cô lập sổ điểm theo giáo viên

## Đã làm
1. `api/sodiem.php`: nhánh `GET action=load` chỉ đọc `gradebooks` theo `teacher_id`, `class_name`, `subject`, `academic_year`. Đã xóa `fallbackStmt`. Giáo viên chưa có sổ thì `gradebook` là `null`, `roster` vẫn trả về.
2. `sodiem.html`: `currentTeacherKey()` lấy `userEmail`, rồi `userName`, rồi `default`. Khóa cache là `sodiem:${currentTeacherKey()}:${class}:${subject}:2025-2026`.
3. `taobaitap.html`: `sodiemStorageKey` dùng cùng định danh. `parseSodiemStorageKey` bỏ qua khóa không thuộc giáo viên đang đăng nhập, nên danh sách lớp local không đọc sổ của tài khoản khác.
4. `tests/sodiem-smoke.js`: chặn fallback không có `teacher_id`, và kiểm tra khóa cache ở `sodiem.html` cùng `taobaitap.html`.

## Chưa đụng
- Không đổi schema `gradebooks`. Không đổi `save`. Không đổi `sodiem:last_class` và `sodiem:questions`.
- Không chuyển dữ liệu cache cũ (khóa không có user) sang khóa mới.

## Kiểm thử
- `php -l api/sodiem.php`: không lỗi cú pháp. Dùng `C:\Users\HoangThien\AppData\Local\Temp\php-portable-834\php.exe`.
- `node tests/sodiem-smoke.js`: PASS. Node dùng `C:\Users\HoangThien\AppData\Local\OpenAI\Codex\runtimes\cua_node\cfb32733c877621e\bin\node.exe`.
- Chưa chạy hai tài khoản thật trên trình duyệt.

## Bước tiếp
Antigravity IDE, chat mới: `/verify`
