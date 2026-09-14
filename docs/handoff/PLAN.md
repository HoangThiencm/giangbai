# PLAN: Mở bài theo lớp cho Giáo viên & Tái cấu trúc danh sách tài khoản Admin

## Hiện trạng
1. **Lộ trình học & Cơ chế mở bài:**
   - Trong CSDL bảng `lessons`, trạng thái xuất bản chỉ có một cột duy nhất `is_published TINYINT(1) DEFAULT 0`. Khi giáo viên bật xuất bản một bài, tất cả học sinh có quyền vào môn đó đều thấy bài học, không có cách nào mở riêng cho lớp 6/1 mà giữ đóng cho lớp 6/2.
   - `api/lessons.php`: Ở luồng GET danh sách bài học của học sinh (`$user['role'] === 'student'`), chỉ lọc qua `$lesson['is_published']`. Chưa có logic kiểm tra lớp học (`class_name`) của học sinh đối với bài học.
   - `admin-lesson-manager.js`: Giao diện "Thiết kế bài học" chỉ có 1 checkbox "Công khai / Mở cho HS" (`#lessonPublished`), khi lưu chỉ gửi cờ boolean `is_published`. Chưa hỗ trợ chọn lớp mở bài.
   - `api/helpers.php`: Đã có sẵn hàm `normalize_teacher_class_name` và `teacher_managed_classes` hỗ trợ phân tách chuỗi lớp của giáo viên (ví dụ `"6/1, 6/2"`) thành mảng `['6/1', '6/2']`.
   - `lotrinh.js`: Chưa có bộ lọc hiển thị hoặc thao tác mở bài nhanh theo từng lớp cho giáo viên trực tiếp trên thanh lộ trình.

2. **Quản lý danh sách đăng ký trong Admin (`admin.html`):**
   - Hiện tại toàn bộ tài khoản (Giáo viên, Học sinh của mọi lớp 6/1, 6/2, 7/1..., tài khoản chờ duyệt, tài khoản đang hoạt động) đều được đổ chung vào một bảng duy nhất `#tableBody`.
   - Khi số lượng đăng ký tăng lên, danh sách bị trộn lẫn ("quá lộn xộn"), gây khó khăn cho quản trị viên khi cần tìm kiếm, kiểm tra, phê duyệt hoặc quản lý học sinh theo từng lớp và theo dõi giáo viên.
   - Giao diện Admin đã có hệ thống tab điều hướng (Tạo tài khoản, THCS Trần Phú, Theo dõi AI, Cài đặt hệ thống), nhưng bảng tài khoản trong tab `accounts` chưa được phân tầng.

---

## Phạm vi
1. **Phân quyền và giao diện Mở bài theo lớp (Lộ trình học các lớp):**
   - Nâng cấp cấu trúc CSDL bảng `lessons`: bổ sung trường `published_classes_json` (lưu mảng JSON danh sách lớp được mở, ví dụ `["6/1", "6/2"]`).
   - Cập nhật backend `api/lessons.php`:
     - Tự động chạy migration an toàn thêm cột `published_classes_json` nếu chưa tồn tại.
     - Cập nhật API GET: Với học sinh, chỉ trả về bài học nếu bài đó đang mở công khai toàn khối (`published_classes_json` rỗng / `null` / chứa `*`) HOẶC lớp của học sinh nằm trong danh sách lớp được mở bài đó. Chặn truy cập trực tiếp bằng ID/slug nếu không đúng lớp.
     - Cập nhật API POST lưu bài (`save_content`): Nhận và lưu mảng `published_classes`.
     - Bổ sung action API mở/khóa nhanh theo lớp cho giáo viên (`update_published_classes` hoặc `toggle_class_publish`) với kiểm tra chặt chẽ quyền phụ trách lớp của giáo viên (`teacher_managed_classes`).
   - Nâng cấp giao diện thiết kế bài (`admin-lesson-manager.js`):
     - Tại khu vực "Công khai / Mở cho HS": Bổ sung tùy chọn linh hoạt:
       - Mở cho toàn khối / tất cả các lớp.
       - Mở riêng cho từng lớp (danh sách checkbox hiển thị các lớp giáo viên đang dạy, ví dụ: `[x] 6/1`, `[ ] 6/2`; đối với admin hiển thị tất cả các lớp học sinh hiện có).
     - Hiển thị nhãn/badge lớp đã mở trong dropdown chọn bài và danh sách bài học.
   - Nâng cấp giao diện lộ trình (`lotrinh.js`):
     - Với tài khoản giáo viên: Thêm bộ chọn lớp phụ trách trên thanh điều hướng lộ trình (`Tất cả` | `6/1` | `6/2`) để giáo viên có thể quan sát lộ trình hiển thị đúng theo góc nhìn của từng lớp, kèm nút gạt mở/đóng bài nhanh cho lớp đang chọn.
     - Với tài khoản học sinh: Hiển thị đúng các bài được giáo viên mở cho lớp của mình; thanh tiến trình chương và thống kê hoàn thành tự động tính trên tập bài đã mở cho lớp đó.

2. **Tái cấu trúc danh sách đăng ký tài khoản trong Admin (`admin.html`):**
   - Chia khu vực danh sách tài khoản thành 2 Tab nghiệp vụ độc lập:
     - **Tab 1: Học sinh (Students):**
       - Thống kê riêng cho học sinh: Tổng số HS, Số HS đang hoạt động, Số HS chờ duyệt.
       - Thanh phân nhóm lớp học động (Class Pills / Sub-tabs) tự sinh từ dữ liệu thực tế: `[Tất cả (Tổng)]`, `[Lớp 6/1 (N)]`, `[Lớp 6/2 (N)]`, ..., `[Chưa xếp lớp (N)]`.
       - Lọc nhanh theo lớp khi nhấp vào từng sub-tab; hiển thị bảng danh sách học sinh thuộc đúng lớp đã chọn.
       - Ô tìm kiếm học sinh (họ tên, username/email) và lọc trạng thái (Tất cả, Đang hoạt động, Chờ duyệt, Đang khóa).
       - Giữ đầy đủ các nút hành động nghiệp vụ: Duyệt học sinh, Cài đặt tài khoản, Chuyển lớp, Nâng khối Toán (`promote`), Xóa tài khoản.
     - **Tab 2: Giáo viên (Teachers):**
       - Thống kê riêng cho giáo viên: Tổng số GV, GV hoạt động, GV chờ duyệt.
       - Bảng danh sách chuyên biệt cho giáo viên, hiển thị rõ ràng: Họ tên, Tên đăng nhập, Lớp phụ trách (ví dụ: `6/1, 6/2`), Chức năng & Phân quyền trang được cấp, Trạng thái, Ngày hết hạn.
       - Các nút hành động: Duyệt tài khoản, Cài đặt phân quyền, Cấp full chức năng, Xóa tài khoản.
   - Ghi nhớ tab và lớp đang chọn vào `localStorage` (`admin_users_role_tab`, `admin_selected_class_tab`) để trải nghiệm liền mạch sau khi tải lại trang hoặc sau thao tác duyệt/sửa.

---

## Ngoài phạm vi
- Không thay đổi bảng `users` hay cơ chế đăng nhập, băm mật khẩu hiện tại.
- Không thay đổi cấu trúc bảng `student_lesson_progress` (tiến độ bài học của học sinh vẫn gắn với `student_id` và `lesson_id`).
- Không tác động vào các module khác ngoài lộ trình học và trang quản trị người dùng (không sửa `quanlyvanban`, `soankhbd`, `thoikhoabieu`...).

---

## File dự kiến tác động
1. `api/lessons.php`:
   - Thêm cột `published_classes_json` vào bảng `lessons` trong `ensure_lesson_schema`.
   - Cập nhật luồng lọc bài học GET cho học sinh theo lớp học.
   - Cập nhật payload bài học trả về (`published_classes`).
   - Xử lý lưu `published_classes` trong action `save_content`.
   - Thêm action cập nhật nhanh quyền mở bài theo lớp (`update_published_classes`) cho giáo viên.
2. `admin-lesson-manager.js`:
   - Bổ sung UI chọn lớp mở bài trong form biên tập bài học (tất cả các lớp hoặc tick chọn các lớp phụ trách).
   - Đọc và điền danh sách lớp khi nạp bài học; gom dữ liệu `published_classes` khi bấm Lưu bài học.
   - Hiển thị badge trạng thái mở theo lớp trên thanh danh sách bài học.
3. `lotrinh.js`:
   - Bổ sung bộ chọn lọc theo lớp cho giáo viên trên thanh lộ trình để xem và đổi trạng thái mở bài theo lớp tiện lợi.
   - Cập nhật tính toán tiến độ học sinh dựa trên danh sách bài thực tế được mở cho lớp của học sinh.
4. `admin.html`:
   - Tái cấu trúc khu vực hiển thị danh sách tài khoản: tạo tab cấp con hoặc tab chính riêng biệt giữa **Học sinh** và **Giáo viên**.
   - Thêm thanh sub-tabs lọc theo từng lớp cho tab Học sinh kèm số lượng đếm tự động.
   - Tách hàm render bảng thành 2 bảng chuyên biệt (`renderStudentsTable` và `renderTeachersTable`).
   - Bổ sung ô tìm kiếm và lọc trạng thái người dùng trong từng tab.

---

## Các bước thực hiện
### Bước 1: Nâng cấp Backend `api/lessons.php`
1. Bổ sung `'published_classes_json TEXT DEFAULT NULL'` vào danh sách cột kiểm tra của hàm `ensure_lesson_schema($pdo)`.
2. Sửa hàm `lesson_row_to_summary` và `lesson_row_to_payload`:
   - Trích xuất `published_classes` từ `published_classes_json` (mặc định mảng rỗng nếu null).
3. Cập nhật xử lý GET danh sách bài và chi tiết bài:
   - Với `$user['role'] === 'student'`:
     - Lấy lớp của học sinh: `$studentClass = trim((string)($user['class_name'] ?? ''));`
     - Bài được xem nếu: `$lesson['is_published'] == 1` VÀ (`empty($lesson['published_classes'])` HOẶC `in_array('*', $lesson['published_classes'], true)` HOẶC `in_array($studentClass, $lesson['published_classes'], true)`).
   - Với giáo viên và admin: trả về đủ danh sách bài kèm mảng `published_classes` để phục vụ hiển thị trên giao diện quản trị.
4. Cập nhật xử lý POST `save_content`:
   - Nhận `$data['published_classes']` (mảng string), encode thành JSON lưu vào `published_classes_json`.
5. Bổ sung action `update_published_classes`:
   - Nhận `lesson_id` và `published_classes`.
   - Kiểm tra quyền: nếu là giáo viên, đảm bảo các lớp được cập nhật nằm trong `teacher_managed_classes($user)`.
   - Cập nhật `published_classes_json` và đồng bộ cờ `is_published` (nếu mảng lớp rỗng thì `is_published = 0`, ngược lại `1`).

### Bước 2: Nâng cấp Giao diện Soạn bài `admin-lesson-manager.js`
1. Trong template tạo giao diện biên tập `#lessonEditorPanel`:
   - Mở rộng khu vực `#lessonPublished`: thêm container `#lessonClassScopeContainer` chứa:
     - Checkbox "Áp dụng tất cả các lớp".
     - Khung danh sách checkbox các lớp phụ trách (được tải từ `teacher_managed_classes` của giáo viên đăng nhập hoặc danh sách lớp học sinh nếu là admin).
2. Viết hàm đồng bộ dữ liệu giao diện:
   - Khi chọn/nạp bài: tick chọn đúng các lớp từ `lesson.published_classes`.
   - Khi bấm lưu bài: thu thập mảng lớp đã chọn đưa vào payload `published_classes`.
3. Cập nhật hiển thị trong dropdown `#lessonSelect`: kèm thông tin lớp mở bài (ví dụ: `Bài 1: Tập hợp [Mở: 6/1, 6/2]`).

### Bước 3: Nâng cấp Giao diện Lộ trình `lotrinh.js`
1. Bổ sung thanh công cụ xem/chọn lớp cho giáo viên trên header hoặc sidebar lộ trình:
   - Danh sách nút chuyển lớp: `[Tất cả]` `[Lớp 6/1]` `[Lớp 6/2]`...
   - Khi chọn một lớp, các bài học sẽ hiển thị huy hiệu trạng thái: "Đang mở cho lớp 6/1" hoặc "Đang đóng với lớp 6/1".
   - Nút bật/tắt nhanh trạng thái mở bài cho lớp đó mà không bắt buộc phải mở toàn bộ trình soạn thảo.
2. Đảm bảo phía học sinh chỉ thấy danh sách bài đã được mở cho lớp của mình và không thể mở bài chưa cho phép.

### Bước 4: Tái cấu trúc Danh sách Đăng ký Admin trong `admin.html`
1. Thiết kế lại khu vực bảng danh sách tài khoản:
   - Tạo bộ chuyển Tab trên đầu bảng:
     - Tab **Học sinh** (Icon `fa-user-graduate`, kèm badge tổng số HS).
     - Tab **Giáo viên** (Icon `fa-chalkboard-teacher`, kèm badge tổng số GV).
2. Xây dựng giao diện Tab Học sinh:
   - Thanh Sub-tabs / Pills chọn lớp:
     - Quét toàn bộ danh sách học sinh để trích xuất danh sách lớp không trùng lặp (ví dụ: 6/1, 6/2, 7/1...), sắp xếp tự nhiên.
     - Hiển thị nút `Tất cả các lớp (N)` và các nút cho từng lớp `Lớp 6/1 (n1)`, `Lớp 6/2 (n2)`..., `Chưa xếp lớp (n0)`.
   - Ô tìm kiếm và lọc trạng thái học sinh (Tất cả, Đang hoạt động, Chờ duyệt, Khóa).
   - Render bảng học sinh chuyên biệt: Cột Họ tên, Lớp, Trạng thái (Hoạt động/Chờ duyệt), Ngày hết hạn, Hành động (Duyệt, Cài đặt, Lên khối, Xóa).
3. Xây dựng giao diện Tab Giáo viên:
   - Render bảng giáo viên chuyên biệt: Cột Họ tên & Tài khoản, Lớp phụ trách (`class_name`), Quyền module / chức năng đã cấp, Trạng thái, Ngày hết hạn, Hành động (Cài đặt, Cấp full, Xóa).
4. Cập nhật hàm `renderTable` thành bộ điều phối:
   - Phân loại `cachedUsers` thành `students` và `teachers`.
   - Gọi render vào đúng tab đang active.
   - Lưu trạng thái tab và lớp vào `localStorage` để giữ nguyên trạng thái khi thao tác.

---

## Rủi ro
1. **Dữ liệu bài học cũ chưa có `published_classes_json`:**
   - *Khắc phục:* Xử lý mặc định null hoặc rỗng = "áp dụng cho tất cả các lớp", đảm bảo học sinh các khóa trước không bị mất quyền truy cập vào các bài học cũ đã xuất bản.
2. **Học sinh chưa được gán lớp (`class_name` rỗng):**
   - *Khắc phục:* Nếu bài học mở dạng "Tất cả các lớp", học sinh chưa có lớp vẫn xem được. Nếu bài mở theo lớp cụ thể, hiển thị thông báo rõ ràng nhắc học sinh liên hệ giáo viên/admin xếp lớp.
3. **Giáo viên dạy nhiều lớp có tên lớp nhập không đồng nhất (ví dụ `6/1`, `6.1`, `Lớp 6/1`):**
   - *Khắc phục:* Tận dụng hàm chuẩn hóa lớp có sẵn `normalize_teacher_class_name` và chuẩn hóa chuỗi so sánh lớp (trim, chữ thường hoặc regex cơ bản) để đối chiếu chính xác.
4. **Trang admin tải lại làm mất vị trí tab/lớp đang duyệt:**
   - *Khắc phục:* Lưu tab chính (Học sinh/Giáo viên) và tab lớp học vào `localStorage`, khôi phục vị trí ngay khi gọi `loadUsers()`.

---

## Cách kiểm thử
1. **Kiểm thử phân quyền mở bài theo lớp:**
   - Tạo 2 tài khoản học sinh: `hs_61` (lớp 6/1) và `hs_62` (lớp 6/2).
   - Đăng nhập tài khoản giáo viên (dạy lớp 6/1, 6/2):
     - Mở bài số 1 cho cả 6/1 và 6/2 $\to$ Đăng nhập cả 2 học sinh kiểm tra đều thấy bài 1.
     - Mở bài số 2 chỉ cho lớp 6/1 $\to$ Đăng nhập `hs_61` thấy bài 2; đăng nhập `hs_62` không thấy bài 2 trong danh sách và không mở được bài 2 bằng link trực tiếp.
     - Đổi bài số 2 mở tiếp cho 6/2 $\to$ `hs_62` lập tức thấy bài 2 hiển thị.
2. **Kiểm thử giao diện Admin:**
   - Đăng nhập Admin với secret key:
     - Kiểm tra hiển thị tách biệt rõ ràng 2 Tab: **Học sinh** và **Giáo viên**.
     - Nhấp chọn Tab **Giáo viên**: Bảng chỉ hiển thị các tài khoản giáo viên, hiển thị rõ cột "Lớp phụ trách" và chức năng được mở.
     - Nhấp chọn Tab **Học sinh**: Thấy danh sách các sub-tab lớp (ví dụ `Tất cả`, `6/1`, `6/2`...).
     - Bấm chọn sub-tab `Lớp 6/1`: Bảng chỉ hiển thị đúng các học sinh thuộc lớp 6/1; số lượng đếm trên badge khớp hoàn toàn.
     - Thử duyệt tài khoản học sinh chờ duyệt từ lớp 6/1, đảm bảo cập nhật trạng thái thành công và giữ nguyên ở sub-tab lớp 6/1.
     - Thử tìm kiếm tên học sinh trong ô tìm kiếm, kiểm tra kết quả lọc tức thời.

---

## Tiêu chí nghiệm thu
1. Giáo viên phụ trách nhiều lớp (ví dụ 6/1, 6/2) có thể tùy chọn mở bài cho tất cả các lớp hoặc mở riêng cho từng lớp cụ thể.
2. Học sinh lớp 6/1 chỉ nhìn thấy và học các bài được mở cho lớp 6/1 (hoặc bài mở cho toàn khối); không xem được các bài mở riêng cho lớp khác.
3. Trong Admin, danh sách đăng ký được phân tách gọn gàng thành Tab Học sinh và Tab Giáo viên.
4. Trong Tab Học sinh của Admin, có các sub-tab chia theo từng lớp học, hiển thị số lượng học sinh từng lớp, cho phép quản trị viên xem, tìm kiếm và quản lý học sinh theo từng lớp một cách trực quan, khoa học.
5. Không làm ảnh hưởng đến các dữ liệu bài học và tài khoản đã tạo trước đó.
