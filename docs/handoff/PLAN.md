# PLAN: Khắc phục lỗi rò rỉ dữ liệu Sổ điểm giữa các tài khoản (User Cô lập Sổ điểm)

## 1. Hiện trạng & Nguyên nhân gốc rễ

Hiện tượng: Khi User B đăng nhập vào hệ thống, mở sổ điểm của một lớp thì thấy toàn bộ điểm số, nhận xét mà User A (giáo viên khác) đã nhập trước đó.

Có 2 nguyên nhân cốt lõi gây ra lỗi này:

### Nguyên nhân 1: Backend fallback nạp sổ điểm của giáo viên khác (`api/sodiem.php`)
- Trong `api/sodiem.php` (dòng 53–60):
  ```php
  $stmt = $pdo->prepare('SELECT columns_config_json, students_data_json, history_log_json, updated_at FROM gradebooks WHERE teacher_id = ? AND class_name = ? AND subject = ? AND academic_year = ? LIMIT 1');
  $stmt->execute([(int)$teacher['id'], $class, $subject, $year]);
  $book = $stmt->fetch();
  if (!$book) {
      $fallbackStmt = $pdo->prepare('SELECT columns_config_json, students_data_json, history_log_json, updated_at FROM gradebooks WHERE class_name = ? AND subject = ? AND academic_year = ? ORDER BY updated_at DESC LIMIT 1');
      $fallbackStmt->execute([$class, $subject, $year]);
      $book = $fallbackStmt->fetch();
  }
  ```
- **Hành vi sai lệch:** Khi Giáo viên B chưa từng lưu sổ điểm cho lớp và môn học đó (`!$book`), đoạn fallback `fallbackStmt` đã tự ý truy vấn sổ điểm được cập nhật gần nhất của lớp & môn đó **mà không lọc theo `teacher_id`**.
- Kết quả: Toàn bộ `students_data_json` (chứa điểm số, nhận xét cá nhân của giáo viên trước đó) bị trả về cho Giáo viên B.
- Khi autosave của Giáo viên B chạy, dữ liệu này thậm chí còn được sao chép sang bản ghi của Giáo viên B hoặc gây sai lệch dữ liệu toàn hệ thống.

### Nguyên nhân 2: Frontend dùng chung key localStorage trên cùng một thiết bị (`sodiem.html` & `taobaitap.html`)
- Trong `sodiem.html` (dòng 26):
  ```javascript
  const key=()=>`sodiem:${$('classSelect').value}:${$('subject').value}:2025-2026`;
  ```
- Tương tự trong `taobaitap.html` (dòng 14292):
  ```javascript
  const sodiemStorageKey = (className, subject) => `sodiem:${className}:${subject || 'Toán'}:${SODIEM_YEAR}`;
  ```
- **Hành vi sai lệch:** Khóa `localStorage` chỉ phân biệt theo tên lớp, môn học và năm học, **hoàn toàn không gắn với định danh user/tài khoản** (`userId` hoặc `userEmail`).
- Nếu hai giáo viên dùng chung máy tính / trình duyệt (ví dụ máy tính phòng hội đồng hoặc phòng tin học):
  - Giáo viên A nhập điểm -> lưu vào cache trình duyệt.
  - Giáo viên B đăng nhập sau đó -> hàm `loadBook()` đọc `cached` từ `localStorage` và gọi `mergeStudents(roster, bookStudents, cachedStudents)`, làm cho dữ liệu của Giáo viên A tự động nạp vào màn hình của Giáo viên B.

---

## 2. Mục tiêu kỹ thuật
1. **Cô lập dữ liệu tuyệt đối ở cấp độ Backend (`api/sodiem.php`):**
   - Loại bỏ hoàn toàn câu lệnh `fallbackStmt` lấy sổ điểm của giáo viên khác.
   - Sổ điểm của giáo viên nào chỉ giáo viên đó được nạp và chỉnh sửa (`WHERE teacher_id = ?`).
   - Nếu giáo viên chưa có sổ điểm cho lớp đó: trả về `gradebook = null` kèm theo danh sách học sinh (`roster`) của lớp để giáo viên bắt đầu chấm mới từ đầu.
   - Nếu cần kế thừa cấu hình cột điểm mặc định từ trường/hệ thống, chỉ tái sử dụng `columns_config_json` (nếu cần), **tuyệt đối không bao giờ lấy `students_data_json` và `history_log_json` của giáo viên khác**.

2. **Cô lập cache dữ liệu theo người dùng ở Frontend (`sodiem.html` & `taobaitap.html`):**
   - Thêm định danh người dùng hiện tại (ví dụ: `localStorage.getItem('userEmail') || localStorage.getItem('userName') || 'teacher'`) vào khóa cache `localStorage`.
   - Ví dụ format: `sodiem:${userKey}:${className}:${subject}:${academicYear}`.
   - Khi đổi tài khoản hoặc đăng xuất, cache của tài khoản này không bị đọc lầm sang tài khoản khác.

3. **Cập nhật và bổ sung bài kiểm thử (`tests/sodiem-smoke.js`):**
   - Bổ sung test kiểm tra: Backend `api/sodiem.php` không được chứa câu truy vấn fallback không có `teacher_id`.
   - Kiểm tra khóa lưu trữ frontend phải phân tách theo user scope.

---

## 3. Kế hoạch sửa đổi chi tiết từng file

### File 1: `api/sodiem.php`
- Tại nhánh `if ($method === 'GET' && $action === 'load')`:
  - Xóa bỏ đoạn `if (!$book) { $fallbackStmt = ... $book = $fallbackStmt->fetch(); }`.
  - Giữ lại truy vấn chính xác theo `teacher_id`:
    ```php
    $stmt = $pdo->prepare('SELECT columns_config_json, students_data_json, history_log_json, updated_at FROM gradebooks WHERE teacher_id = ? AND class_name = ? AND subject = ? AND academic_year = ? LIMIT 1');
    $stmt->execute([(int)$teacher['id'], $class, $subject, $year]);
    $book = $stmt->fetch();
    ```
  - Nếu `$book` không tồn tại, trả về `gradebook => null`, giữ nguyên danh sách `roster`.

### File 2: `sodiem.html`
- Cập nhật hàm tạo `key()` lưu `localStorage`:
  ```javascript
  function currentTeacherKey() {
      return (localStorage.getItem('userEmail') || localStorage.getItem('userName') || 'default').trim().toLowerCase();
  }
  const key = () => `sodiem:${currentTeacherKey()}:${$('classSelect').value}:${$('subject').value}:2025-2026`;
  ```
- Đảm bảo khi nạp dữ liệu offline/cache, chỉ lấy cache của đúng giáo viên đang đăng nhập.

### File 3: `taobaitap.html`
- Cập nhật hàm `sodiemStorageKey` đồng bộ theo định dạng có gắn kèm `userEmail` hoặc `userName`.

### File 4: `tests/sodiem-smoke.js`
- Thêm kiểm thử tĩnh:
  - Khẳng định `api/sodiem.php` không có fallback query bỏ quên `teacher_id`.
  - Khẳng định `sodiem.html` có gắn định danh người dùng vào `key` của sổ điểm.

---

## 4. Kế hoạch kiểm thử (Verification)
1. Chạy static smoke test:
   `node tests/sodiem-smoke.js`
2. Mô phỏng kiểm thử 2 tài khoản giáo viên:
   - Giáo viên 1 (ID: 101) nhập điểm cho lớp 10A1 môn Toán -> Lưu thành công.
   - Giáo viên 2 (ID: 102) đăng nhập, mở lớp 10A1 môn Toán -> Sổ điểm phải sạch sẽ, không có bất kỳ điểm số nào của Giáo viên 1.
   - Thử nghiệm trên cùng 1 trình duyệt: Giáo viên 2 không bị merge cache từ Giáo viên 1.
