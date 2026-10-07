# IMPLEMENT: Nút "Thêm bình luận" và định danh người bình luận (Padlet)

## Đã làm
- `padlet_ht.html` `postCard`: thanh `post-action` hiện khi `canManage || can_delete || comments_enabled`. Nút **Thêm bình luận** (`far fa-comment-dots`, gọi `openComments`) chỉ khi `b.comments_enabled`. Duyệt, Từ chối, Ghim, Sửa, Xóa giữ nguyên điều kiện quản lý / `can_delete`.
- `#commentModal`: badge `#commentUserBadge` / `#commentUserName`; khối khách có nhãn, ô họ tên `required` (placeholder bắt buộc), ô lớp/vai trò.
- `openComments`: tài khoản đăng nhập hiện badge và ẩn form khách (bỏ `required` trên ô họ tên); khách điền sẵn `localStorage` `padlet_guest_name` / `padlet_guest_role`, không có tên thì lấy `#postAuthorName`. Danh sách bình luận có avatar chữ cái đầu, tên đậm, badge vai trò, thời gian.
- `submitComment`: khách thiếu họ tên thì toast và focus, không gửi. Gửi thành công thì nhớ localStorage (khách), xóa nội dung, toast, `loadBoard()`, rồi mở lại danh sách nếu modal còn mở.

## Smoke
- `node tests/padlet-ownership-smoke.js` — PASS
- `node tests/padlet-ui-smoke.js` — PASS
- `node tests/padlet-comment-ui-smoke.js` — PASS

## Ngoài phạm vi
- Không đổi `api/padlet.php` (server đã bắt buộc họ tên và gán vai trò Giáo viên/Học sinh khi đã đăng nhập).
- Chưa commit, chưa push. Kiểm tra trình duyệt để `/verify`.

---

# IMPLEMENT: Skill toàn cục Trợ lý Sư phạm Hoàng Thiên cho Codex/ChatGPT

## Đã làm

- Tạo skill toàn cục `C:\Users\HoangThien\.codex\skills\tro-ly-thien\SKILL.md` để nhận diện lời gọi `Thiên ơi`, `/thien` và các yêu cầu KHBD, bài tập, duyệt giáo án/đề, bài giảng HTML, vẽ hình, báo cáo, sáng kiến, chuẩn hóa văn bản hoặc chép ghi âm.
- Tạo `references\quy-trinh-nhanh.md` với menu 13 nhánh, menu con bài tập đủ 10 dạng, nguồn/thư mục đầu vào–kết quả, quy tắc thực hiện trực tiếp và liên kết tệp cục bộ kiểu Codex (không dùng `file:///`).
- Skill thay `ask_question` Antigravity bằng hội thoại chat và yêu cầu thực hiện trực tiếp nghiệp vụ giảng dạy, không chuyển sang quy trình Manager–Planner–Coder.

## Validation

- Đã chạy `quick_validate.py` theo skill-creator; môi trường Python hiện có không cài module `yaml` nên validator dừng tại `ModuleNotFoundError: No module named 'yaml'` trước khi kiểm tra cấu trúc. Đã kiểm tra thủ công: frontmatter có `name`/`description`, không còn TODO/scaffold và chỉ có `SKILL.md` cùng reference cần thiết.

## Ngoài phạm vi / ngoại lệ

- Không sửa `docs/handoff/PLAN.md` vì đây là kế hoạch Padlet không liên quan, theo chỉ dẫn.
- Không sửa `.agents/` hoặc `TROLYTHIEN/`; không commit.

---

# IMPLEMENT: Menu Trợ lý Thiên cho Codex

## Đã làm

- Tạo `TROLYTHIEN/tro-ly-thien-menu.html`: trang HTML tự chứa, tiếng Việt, có 13 thẻ chức năng theo đúng menu Trợ lý Thiên.
- Mỗi lựa chọn hiển thị prompt có thể chỉnh sửa và nút Sao chép (Clipboard API kèm fallback bôi chọn/exeCommand). Giao diện nêu rõ thao tác bấm chọn → sao chép → dán/gửi trong chat Codex; không tuyên bố đã gửi tin nhắn.
- Nhánh **Tạo bài tập** có đủ 10 dạng. Các nhánh Game giáo dục, Sổ điểm, Quản lý tổ chuyên môn và Vẽ hình có nút mở nhanh bằng HTTPS.
- Bố cục lưới đáp ứng màn hình hẹp, không dùng `file:///` hoặc liên kết `codex://`.

## Kiểm tra

- Kiểm tra tĩnh nội dung HTML: đủ 13 mục chính, 10 dạng bài tập, textarea prompt, nút sao chép và fallback `document.execCommand('copy')`.
- Chưa kiểm tra trực tiếp bằng trình duyệt trong lượt triển khai này.

## Giới hạn

- Một trang HTML độc lập không có quyền gửi prompt trực tiếp vào Codex; người dùng cần dán và gửi thủ công sau khi sao chép.
