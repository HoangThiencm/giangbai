# PLAN: Khắc phục lỗi Sổ điểm rò rỉ dữ liệu & Lỗi Padlet công khai bị ép đăng nhập

## 1. Hiện trạng & Nguyên nhân gốc rễ

---

### Vấn đề 1: Sổ điểm của user này ở user khác (khác máy) vẫn thấy
- **Hiện tượng:** Giáo viên B ở Máy 2 đăng nhập vào hệ thống, mở sổ điểm lớp 10A1 môn Toán thì thấy toàn bộ điểm số, nhận xét mà Giáo viên A ở Máy 1 đã nhập trước đó.
- **Nguyên nhân gốc rễ:** Nằm tại backend `api/sodiem.php` (dòng 56–60):
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
  Khi Giáo viên B chưa từng lưu sổ điểm của riêng mình (`!$book`), hệ thống tự động chạy câu lệnh `fallbackStmt` tìm kiếm trên CSDL bản ghi được cập nhật gần nhất của lớp & môn đó **mà hoàn toàn không lọc theo `teacher_id`**. Kết quả là CSDL trả về trọn vẹn điểm số (`students_data_json`) của Giáo viên A cho Giáo viên B.
- **Nguyên nhân phụ (nếu dùng chung máy):** Trong `sodiem.html` và `taobaitap.html`, key `localStorage` là `sodiem:${class}:${subject}:2025-2026` không phân tách theo tài khoản (`userEmail`/`userName`).

---

### Vấn đề 2: Bảng Padlet đã chọn chế độ tự do / công khai nhưng người xem vẫn bị bắt đăng nhập
- **Hiện tượng:** Giáo viên tạo bảng Padlet, trong phần Cài đặt nâng cao chọn:
  *Ai được tham gia?* $\rightarrow$ **"Mở qua link (ai có link đều xem được)"** (`access_mode = 'public'`). Nhưng khi gửi link cho người khác hoặc mở ở chế độ ẩn danh thì vẫn bị chuyển hướng bắt đăng nhập (`login.html`).
- **Nguyên nhân gốc rễ:** Nằm tại middleware kiểm soát quyền `access-control.js`:
  1. Trong `padlet_ht.html` (dòng 2828): có nhúng `<script src="access-control.js"></script>`.
  2. Trong `access-control.js` (dòng 139–142):
     ```javascript
     const token = localStorage.getItem('authToken');
     ...
     if (isOpenExamLink) {
         return;
     }

     if (!token) {
         window.location.href = 'login.html';
         return;
     }
     ```
  3. `access-control.js` chỉ có biến `isOpenExamLink` dành riêng cho `thitructuyen.html`. Hệ thống **hoàn toàn chưa có cơ chế kiểm tra ngoại lệ cho link Padlet công khai** (`pageKey === 'padlet'` khi có tham số `board` trên URL).
  4. Trong khi đó, ở Backend `api/padlet.php` (dòng 370) và Frontend `padlet_ht.html` (dòng 264, 510) đã xây dựng đầy đủ toàn bộ tính năng cho khách (`guest`): tự nhập tên, xem bài, đăng bài, bình luận, thả cảm xúc mà không cần đăng nhập.
  5. Tuy nhiên, trước khi `padlet_ht.html` kịp gọi API để tải bảng, `access-control.js` đã can thiệp, thấy không có `token` trong `localStorage` và cưỡng bức chuyển hướng người dùng ngay sang `login.html`!
  6. Ngoài ra, nếu người dùng là Học sinh đã đăng nhập nhưng tài khoản chưa được admin cấp quyền `'padlet'` trong `allowed_pages`, dòng 278 của `access-control.js` cũng chặn học sinh mở link bảng Padlet.

---

## 2. Mục tiêu kỹ thuật

1. **Khắc phục triệt để rò rỉ Sổ điểm:**
   - Xóa bỏ hoàn toàn câu lệnh `fallbackStmt` không lọc `teacher_id` trong `api/sodiem.php`.
   - Sổ điểm của giáo viên nào chỉ thuộc về giáo viên đó (`WHERE teacher_id = ?`).
   - Cập nhật key `localStorage` trong `sodiem.html` và `taobaitap.html` để cô lập dữ liệu theo tài khoản.

2. **Mở khóa truy cập link Padlet tự do / công khai:**
   - Cập nhật `access-control.js`: Khi `pageKey === 'padlet'` và trên URL có tham số `board` (ví dụ `padlet_ht.html?board=ABCDEF`):
     - Cho phép bypass bước kiểm tra `if (!token) redirectToLogin()`.
     - Cho phép học sinh vào thẳng link bảng Padlet mà không bị chặn bởi danh sách `allowedPages` (để học sinh tham gia hoạt động bảng do giáo viên chia sẻ).
     - Việc phân quyền xem bảng (`public` hay `class`, đúng lớp hay sai lớp) sẽ do chính `api/padlet.php` kiểm soát và hiển thị giao diện báo lỗi hoặc bảng khóa phù hợp nếu bảng không cho phép khách.
   - Khi truy cập `padlet_ht.html` không có tham số `board` (tức là trang Quản lý bảng của giáo viên): vẫn yêu cầu đăng nhập tài khoản giáo viên như bình thường.

---

## 3. Kế hoạch sửa đổi chi tiết từng file

### File 1: `api/sodiem.php`
- Tại nhánh `if ($method === 'GET' && $action === 'load')`:
  - Xóa bỏ đoạn `fallbackStmt`:
    ```php
    // XÓA ĐOẠN NÀY:
    if (!$book) {
        $fallbackStmt = $pdo->prepare('SELECT columns_config_json, students_data_json, history_log_json, updated_at FROM gradebooks WHERE class_name = ? AND subject = ? AND academic_year = ? ORDER BY updated_at DESC LIMIT 1');
        $fallbackStmt->execute([$class, $subject, $year]);
        $book = $fallbackStmt->fetch();
    }
    ```
  - Chỉ giữ lại câu query chính xác theo `teacher_id`.

### File 2: `sodiem.html`
- Thêm định danh tài khoản vào khóa `key()` trong `localStorage`:
  ```javascript
  function currentTeacherKey() {
      return (localStorage.getItem('userEmail') || localStorage.getItem('userName') || 'default').trim().toLowerCase();
  }
  const key = () => `sodiem:${currentTeacherKey()}:${$('classSelect').value}:${$('subject').value}:2025-2026`;
  ```

### File 3: `taobaitap.html`
- Điều chỉnh hàm `sodiemStorageKey` đồng bộ theo định dạng gắn kèm user identifier.

### File 4: `access-control.js`
- Thêm điều kiện nhận diện link bảng Padlet mở:
  ```javascript
  const isOpenPadletLink = pageKey === 'padlet' && !!getQueryParamInsensitive(params, 'board');
  ```
- Cho phép `isOpenPadletLink` được bypass yêu cầu `token` tương tự như `isOpenExamLink`:
  ```javascript
  if (isOpenExamLink || isOpenPadletLink) {
      return;
  }
  ```
- Đảm bảo nếu là học sinh đang mở `isOpenPadletLink` cũng không bị chặn bởi `canOpenPage(pageKey, allowedPages)`.

### File 5: `tests/sodiem-smoke.js` & `tests/padlet-ui-smoke.js`
- Cập nhật / bổ sung smoke check để đảm bảo:
  - `api/sodiem.php` không có fallback truy vấn thiếu `teacher_id`.
  - `access-control.js` hỗ trợ link `padlet_ht.html?board=...` cho đối tượng tự do không cần token.

---

## 4. Kế hoạch kiểm thử (Verification)
1. **Kiểm thử Sổ điểm:**
   - Mở cửa sổ ẩn danh / thiết bị khác với tài khoản Giáo viên 2. Mở lớp 10A1 môn Toán $\rightarrow$ Phải là bảng điểm trống của Giáo viên 2, không được có bất kỳ điểm số nào của Giáo viên 1.
2. **Kiểm thử Padlet công khai:**
   - Tạo một bảng Padlet, chọn "Mở qua link (ai có link đều xem được)".
   - Lấy link chia sẻ `padlet_ht.html?board=...` mở trong trình duyệt ẩn danh (chưa đăng nhập bất kỳ tài khoản nào).
   - Kiểm tra: Bảng phải tải bình thường, hiển thị giao diện nhập tên người đăng tự do (`guest`), không bị đẩy về `login.html`.
   - Thử nghiệm tài khoản Học sinh bấm vào link $\rightarrow$ mở bình thường.
