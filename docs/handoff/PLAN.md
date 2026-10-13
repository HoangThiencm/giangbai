# PLAN: Sửa lỗi Cài đặt API Key của user & Sửa lỗi Phân quyền Quản lý văn bản (bật mặc định không tắt được)

## 1. Hiện trạng & Nguyên nhân gốc rễ

### Vấn đề 1: "Cài đặt API Key của các user không được"
1. **Thiếu hoàn toàn giao diện nhập API Key trong Admin (`admin.html`):**
   - Khi Admin bấm **"Cài đặt"** trên từng user trong danh sách tài khoản (`openStudentConfig`), modal chỉ có các trường: Họ tên, Lớp, Đổi mật khẩu, Vai trò, Thời hạn, Trạng thái hoạt động và Danh sách checkbox quyền trang (`allowed_pages`).
   - **Không có bất kỳ ô nhập liệu (textarea/input) nào** để Admin xem hoặc nhập `Gemini API Keys` và `Mistral API Keys` cho user đó.
   - Bảng danh sách tài khoản (`renderUsersList`) cũng không hiển thị trạng thái API Key của user (đang dùng key riêng hay key chung hệ thống, số lượng bao nhiêu).
2. **Backend Admin (`api/admin_students.php`) chưa tiếp nhận và lưu API Key:**
   - Khi Admin bấm "Lưu thay đổi" (`window.saveUserConfig`), payload gửi tới `api/admin_students.php` không có trường `gemini_keys` hay `mistral_keys`.
   - Backend `api/admin_students.php` ở cả 2 nhánh `action === 'update'` và `action === 'create'` chỉ thực thi câu lệnh SQL cập nhật `full_name, class_name, role, is_active, allowed_pages_json, expires_at, expires_option`, **hoàn toàn bỏ qua và không lưu `gemini_keys`, `mistral_keys`**.
3. **Trải nghiệm cá nhân user (`js/user-ai-settings.js` & `index.html`):**
   - Nút "Cài đặt AI & Key" (`btnOpenUserAiSettings`) trên navbar gọi `UserAiSettings.openModal()` không truyền tham số.
   - Code `openModal` mặc định chuyển sang tab `overview` ("Tổng quan & Theo dõi"), ẩn sạch các ô textarea nhập key và thanh nút bấm "Lưu lên CSDL", "Kiểm tra Key" (bị `hidden`), khiến giáo viên tưởng rằng tính năng cài đặt key bị lỗi hoặc không có chỗ lưu.

### Vấn đề 2: "Cấp quyền user quản lý văn bản bật mặc định cho mọi user mà tắt ko được"
1. **Backend ép cứng quyền `quanlyvanban` cho mọi giáo viên (`api/helpers.php`):**
   - Trong `teacher_allowed_pages_resolved(array $user)`:
     ```php
     if ($allowEmpty && !in_array('quanlyvanban', $pages, true)) {
         $pages[] = 'quanlyvanban';
     }
     ```
     Hàm này luôn tự động nhét `'quanlyvanban'` vào mảng quyền của giáo viên. Khi Admin tải danh sách user qua `api/admin_students.php` (GET), `public_user()` gọi hàm này, làm toggle "Quản lý văn bản" trong `admin.html` **luôn luôn ở trạng thái BẬT (checked)**.
   - Trong `maybe_upgrade_teacher_allowed_pages(PDO $pdo, array $user)`:
     ```php
     if (!in_array('quanlyvanban', $current, true)) {
         $current[] = 'quanlyvanban';
     }
     ```
     Mỗi khi giáo viên đăng nhập (`api/login.php`) hoặc làm mới phiên (`api/me.php`), hàm này lại tự động nhét `'quanlyvanban'` vào và chạy lệnh `UPDATE users SET allowed_pages_json = ?`, **ghi đè ngược lại vào MySQL ngay cả khi Admin vừa tắt**.
   - Trong `teacher_default_workspace_extras()`:
     Trả về `'quanlyvanban'` làm quyền mặc định cho mọi tài khoản mới.
   - Điều này vi phạm nguyên tắc đặc quyền tối thiểu (least-privilege) và làm rớt kiểm thử `tests/teacher-permissions-smoke.js`.
2. **Frontend `index.html` hardcode luôn hiện thẻ Quản lý văn bản:**
   - Dòng 1061: `setToolCardsVisible('[data-tool="teacher-documents"]', true);` luôn ép hiển thị thẻ văn bản bất kể quyền `allowed_pages` có hay không.
3. **Frontend `access-control.js` bypass toàn bộ giáo viên:**
   - Dòng 111-117: `isPublicVanbanPage` chỉ kiểm tra nếu là `student` thì chặn, còn lại trả về ngay (`return;`), không kiểm tra xem giáo viên có quyền `'quanlyvanban'` trong `allowedPages` hay không.
4. **Backend `api/vanban.php` chưa chặn theo quyền trang:**
   - `vbd_optional_user()` chỉ kiểm tra `role in ['teacher', 'admin', 'superadmin']`, không kiểm tra `in_array('quanlyvanban', teacher_allowed_pages_resolved($user), true)`.

---

## 2. Mục tiêu kỹ thuật
1. **Admin toàn quyền quản lý API Key cho từng user:**
   - Trong `admin.html`: Khi bấm "Cài đặt" tài khoản, có ô nhập Gemini API Keys và Mistral API Keys.
   - Bảng danh sách tài khoản hiển thị trực quan badge trạng thái API Key của từng user.
   - Backend `api/admin_students.php` mã hóa chuẩn `encode_stored_api_keys()` và lưu vào `users.gemini_keys`, `users.mistral_keys`.
2. **Quyền Quản lý văn bản tôn trọng cấu hình của Admin (Bật/Tắt bình thường):**
   - Xóa bỏ toàn bộ logic tự động ép `'quanlyvanban'` trong `api/helpers.php` (`teacher_allowed_pages_resolved`, `maybe_upgrade_teacher_allowed_pages`, `teacher_default_workspace_extras`).
   - Tắt quyền trong `admin.html` -> lưu CSDL không có `'quanlyvanban'` -> reload không bị bật lại -> đăng nhập không bị tự ghi đè.
   - `index.html` chỉ hiển thị thẻ Quản lý văn bản khi user có quyền `'quanlyvanban'`.
   - `access-control.js` và `api/vanban.php` kiểm tra và chặn giáo viên chưa được cấp quyền `'quanlyvanban'`.
3. **Modal Cài đặt AI của user (`js/user-ai-settings.js`):**
   - Khi bấm "Cài đặt AI & Key", mở ngay tab `keys` với đầy đủ ô nhập và nút "Lưu lên CSDL".
4. **Bảo toàn các smoke test hiện có và thêm smoke test mới.**

---

## 3. Danh sách file và thay đổi chi tiết

### File 1: `api/helpers.php`
- **Hàm `teacher_allowed_pages_resolved(array $user)`:**
  - Bỏ đoạn `if ($allowEmpty && !in_array('quanlyvanban', $pages, true)) { $pages[] = 'quanlyvanban'; }`.
  - Trả về đúng `normalize_pages(is_array($raw) ? $raw : [], $allowEmpty);` (khôi phục đúng hợp đồng kiểm thử `tests/teacher-permissions-smoke.js`).
- **Hàm `maybe_upgrade_teacher_allowed_pages(PDO $pdo, array $user)`:**
  - Bỏ đoạn `if (!in_array('quanlyvanban', $current, true)) { $current[] = 'quanlyvanban'; }`.
  - Không tự ý thêm quyền `'quanlyvanban'` khi giáo viên đăng nhập.
- **Hàm `teacher_default_workspace_extras()`:**
  - Bỏ `'quanlyvanban'` khỏi danh sách mặc định.
- **Helper lưu key trong admin:**
  - Đảm bảo các hàm `collect_api_keys_from_input`, `filter_posted_api_keys`, `save_user_key_column`, `encode_stored_api_keys` sẵn sàng để `api/admin_students.php` gọi.

### File 2: `api/admin_students.php`
- **Nhánh `action === 'update'`:**
  - Tiếp nhận `gemini_keys` và `mistral_keys` từ `$data` (nếu có trong request).
  - Sử dụng `collect_api_keys_from_input()` và `filter_posted_api_keys()`.
  - Gọi `save_user_key_column($pdo, $id, 'gemini_keys', $cleanGemini)` và `save_user_key_column($pdo, $id, 'mistral_keys', $cleanMistral)`.
  - Trả về `gemini_keys` và `mistral_keys` đã lưu trong JSON response.
- **Nhánh `action === 'create'`:**
  - Nếu request có truyền `gemini_keys` / `mistral_keys`, lưu cho user mới tạo sau khi lấy `lastInsertId()`.
- **Nhánh `GET`:**
  - `public_user()` đã trả sẵn `gemini_keys` và `mistral_keys`, giữ nguyên hoạt động này.

### File 3: `admin.html`
- **Trong `openStudentConfig(id)`:**
  - Bổ sung khối giao diện nhập API Key trong `#modalAccountConfig`:
    - Label & Textarea `editGeminiKeys`: hiển thị các key Gemini hiện tại của user (mỗi dòng một key).
    - Label & Textarea `editMistralKeys`: hiển thị các key Mistral OCR hiện tại của user (mỗi dòng một key).
    - Ghi chú: "Để trống nếu muốn tài khoản dùng chung key hệ thống."
- **Trong `window.saveUserConfig`:**
  - Đọc dữ liệu từ `editGeminiKeys` và `editMistralKeys`, parse thành mảng và gán vào `payload.gemini_keys`, `payload.mistral_keys`.
  - Cập nhật lại `cachedUsers` với dữ liệu key mới trả về từ máy chủ.
- **Trong `renderUsersList(users)`:**
  - Bổ sung cột/badge trạng thái API Key trên từng dòng user:
    - Nếu có Gemini: badge xanh lá `Gemini (X key)`.
    - Nếu có Mistral: badge tím `Mistral (Y key)`.
    - Nếu chưa có: `Dùng key chung`.
- **Trong `defaultTeacherPages`:**
  - Bỏ `'quanlyvanban'` khỏi mảng gán mặc định ban đầu để tránh tự tick khi tạo tài khoản mới.

### File 4: `index.html`
- **Hàm `applyTeacherAllowedPagesVisibility(allowedSet, features)`:**
  - Thay thế dòng 1061:
    ```javascript
    setToolCardsVisible(
        '[data-tool="teacher-documents"]',
        allowedSet.has('quanlyvanban') && features.quanlyvanban !== false
    );
    ```
- **Hàm `teacherHasWorkspaceHub(allowedSet)`:**
  - Giữ kiểm tra `allowedSet.has('quanlyvanban')`.
- **Nút navbar `btnOpenUserAiSettings`:**
  - Đảm bảo gọi `UserAiSettings.openModal('keys')` hoặc dựa vào default mới của `openModal`.

### File 5: `js/user-ai-settings.js`
- **Hàm `openModal(tabName)`:**
  - Đổi default khi mở modal:
    ```javascript
    UserAiSettings.switchTab(tabName === 'overview' ? 'overview' : 'keys');
    ```
  - Khi bấm mở cài đặt AI, người dùng vào thẳng tab `keys` với đầy đủ ô nhập và nút "Lưu lên CSDL".

### File 6: `access-control.js`
- **Trong `accessControlMain()`:**
  - Với các trang `isPublicVanbanPage`:
    - Nếu người dùng đã đăng nhập với vai trò `teacher`: kiểm tra `allowedPages.includes('quanlyvanban')`. Nếu không có quyền, thông báo "Tài khoản của bạn chưa được cấp quyền Quản lý văn bản" và chuyển hướng về `index.html`.
    - Khách chưa đăng nhập (cấp trên xem công khai) hoặc admin tiếp tục được phép xem theo thiết kế ban đầu.

### File 7: `api/vanban.php`
- **Trong `vbd_optional_user(PDO $pdo)`:**
  - Nếu `$role === 'teacher'`: kiểm tra `$allowed = teacher_allowed_pages_resolved($user);`.
  - Nếu `!in_array('quanlyvanban', $allowed, true)`: respond `403` với thông báo `Tài khoản chưa được cấp quyền Quản lý văn bản.`.

### File 8: `tests/admin-user-api-keys-smoke.js` (Bộ test mới)
- Kiểm thử tĩnh và hợp đồng tích hợp:
  1. `api/helpers.php`: không còn inject cứng `'quanlyvanban'` trong `teacher_allowed_pages_resolved` và `maybe_upgrade_teacher_allowed_pages`.
  2. `tests/teacher-permissions-smoke.js`: chạy PASS 100%.
  3. `api/admin_students.php`: kiểm tra logic nhận và lưu `gemini_keys`, `mistral_keys`.
  4. `admin.html`: kiểm tra form sửa tài khoản có ô nhập `editGeminiKeys`, `editMistralKeys` và gửi đi trong `saveUserConfig`.
  5. `admin.html`: kiểm tra danh sách tài khoản có hiển thị trạng thái API Key.
  6. `index.html`: thẻ `[data-tool="teacher-documents"]` được bật/tắt đúng theo `allowedSet.has('quanlyvanban')`.
  7. `api/vanban.php`: chặn giáo viên không có quyền `quanlyvanban`.

---

## 4. Ngoài phạm vi
- Không thay đổi schema cơ sở dữ liệu (`gemini_keys` và `mistral_keys` đã tồn tại trong bảng `users`).
- Không ảnh hưởng đến key AI hệ thống trong `global_config.json`.
- Không thay đổi các chức năng khác của văn bản (staging, drive sync, ocr).

---

## 5. Kế hoạch xác minh (Verification Plan)
1. Chạy `tests/teacher-permissions-smoke.js` bằng runtime node: phải **PASS** (trước đây đang FAIL).
2. Chạy `tests/user-ai-settings-smoke.js` và `tests/khbd-user-ai-keys-smoke.js`: phải **PASS**.
3. Chạy test mới `tests/admin-user-api-keys-smoke.js`: phải **PASS**.
4. Kiểm tra cú pháp PHP: `php -l` cho `api/helpers.php`, `api/admin_students.php`, `api/vanban.php`.
