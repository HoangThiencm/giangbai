# IMPLEMENT

## Phạm vi đã triển khai
- Cập nhật sodiem.html và api/sodiem.php theo PLAN.md.
- Thêm nút **Dán ảnh (Ctrl+V)**, đọc ảnh trực tiếp từ clipboard khi được cấp quyền, bắt dán ảnh trên toàn cửa sổ, tự chuyển đến tab Đề & câu hỏi và hiển thị thông báo thành công.
- Dropdown lớp tự nạp danh mục từ API mới, có hai tuyến dự phòng tương thích, nhớ lớp gần nhất và tự nạp sổ khi mở trang.
- API lớp trả về danh sách lớp từ cả học sinh CSDL và sổ điểm; API tải sổ luôn trả roster chính thức. Quyền sổ điểm chấp nhận giáo viên và quản trị viên.
- Nạp sổ bằng gộp an toàn roster, bản lưu CSDL và local cache theo mã/SBD hoặc họ tên; bảo toàn điểm, nhận xét, cột điểm và lịch sử thay vì thay bằng roster rỗng.
- persist() không ghi khi chưa chọn lớp.

## Kiểm tra
- git diff --check: PASS.
- Không chạy được smoke test Node: Windows Defender chặn node.exe của runtime Codex là tệp có thể là virus/PUA.
- Không chạy được PHP lint: môi trường hiện tại không có lệnh php.

## Ghi chú
- Không sửa các thay đổi đang có ngoài phạm vi kế hoạch.
