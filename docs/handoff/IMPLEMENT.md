# IMPLEMENT: Nâng cấp quản lý ngày nghỉ / lịch nghỉ tổ chuyên môn

## Phạm vi đã thực hiện

- `phancongtochuyenmon.html`: thay ngày đơn lẻ bằng khoảng từ ngày–đến ngày, thêm buổi nghỉ, lý do có gợi ý và danh sách chọn giáo viên; hiển thị ngoại lệ theo thẻ với khoảng ngày, số ngày, buổi, đối tượng, lý do và nút xóa.
- `phancongtochuyenmon.html`: dữ liệu mới lưu `start_date`, `end_date`, `session`, `teacher_id`, `teacher_name`, `target`, `reason`, đồng thời giữ `date` bằng ngày bắt đầu để đọc tương thích dữ liệu cũ. Bộ lọc lịch báo giảng áp dụng đúng khoảng ngày, buổi và giáo viên.
- `api/calendar_feed.php`: feed iCal/web kiểm tra ngoại lệ theo khoảng ngày bao gồm hai đầu mút, buổi và giáo viên theo mã hoặc tên.

## Kiểm thử

- Kiểm tra cú pháp JavaScript nội tuyến của `phancongtochuyenmon.html` bằng Node: đạt.
- `git diff --check`: đạt, không có lỗi khoảng trắng.
- Không chạy được `php -l api/calendar_feed.php` vì môi trường hiện không có PHP trong `PATH`.

## Lưu ý

- Chưa có kiểm thử end-to-end với dữ liệu TKB và thiết bị lịch thực tế; cần xác nhận thêm trên giao diện sau khi nạp danh sách giáo viên và TKB.

---

# IMPLEMENT: Công cụ Sửa lỗi chính tả AI

## Phạm vi đã thực hiện

- Tạo `sualoichinhta.html`: giao diện responsive, dùng `access-control.js`, quản lý Gemini API Key cá nhân, nhập/dán văn bản, đọc `.txt`/`.docx`, chia tuần tự văn bản dài thành đoạn an toàn, highlight lỗi, áp dụng từng lỗi/tất cả, sao chép và tải tệp kết quả.
- Tạo `api/sualoichinhta_ai.php`: chỉ dùng Gemini API Key mã hóa của tài khoản trong session; xoay key với lỗi quota/quyền hoặc model không khả dụng, fallback ba model Gemini, Structured Output JSON và lọc đề xuất không khớp văn bản nguồn.
- Đăng ký quyền `sualoichinhta` trong `access-control.js`, thêm card công cụ và liên kết vào `index.html`, cùng lựa chọn phân quyền trong `admin.html`.

## Kiểm thử

- Đã kiểm tra cú pháp JavaScript nội tuyến của `sualoichinhta.html` bằng Node và kiểm tra whitespace của diff: đạt.
- Không chạy được `php -l api/sualoichinhta_ai.php` vì môi trường hiện không có PHP trong `PATH`.
- Chưa thể thực hiện kiểm thử Gemini end-to-end vì cần một phiên đăng nhập và Gemini API Key cá nhân hợp lệ.
