# PLAN: Thêm Chức Năng Đổi Mật Khẩu Cho Người Dùng

## 1. Tổng Quan Nhiệm Vụ

Hệ thống hiện tại quản lý đăng nhập người dùng (Giáo viên và Học sinh) thông qua CSDL MySQL (`users` table) và PHP Session (`api/login.php`, `api/me.php`). Tuy nhiên, người dùng chưa có cơ chế tự đổi mật khẩu của mình:
- Mật khẩu chỉ có thể được thiết lập khi đăng ký hoặc do Admin cập nhật trong trang quản trị `admin.html` (`api/admin_students.php`).
- Cần bổ sung tính năng **Đổi mật khẩu** trực tiếp cho mọi tài khoản đã đăng nhập (cả Giáo viên lẫn Học sinh) để tăng tính bảo mật và chủ động cho người dùng.

### Mục tiêu cần đạt:
1. Tạo endpoint backend `api/change_password.php` bảo mật, kiểm tra session, xác thực mật khẩu hiện tại bằng `password_verify`, mã hóa mật khẩu mới bằng `password_hash` và cập nhật vào bảng `users`.
2. Tạo module giao diện `js/change-password.js` hiển thị modal đổi mật khẩu thân thiện, thẩm mỹ, có tính năng ẩn/hiện mật khẩu (eye toggle), kiểm tra dữ liệu đầu vào và thông báo trạng thái rõ ràng.
3. Tích hợp nút mở modal **"Đổi mật khẩu"** trên thanh điều hướng (`nav`) trong `index.html` cho cả Giáo viên và Học sinh.
4. Viết bài test tự động `tests/change-password-smoke.js` đảm bảo toàn bộ cấu trúc file, API và giao diện hoạt động chính xác, không gây lỗi hồi quy.

---

## 2. Chi Tiết Thực Hiện Cho Coder

### PHẦN 1: Backend Endpoint (`api/change_password.php`)

Tạo mới file `api/change_password.php` với nội dung hoàn chỉnh:

```php
<?php
require_once __DIR__ . '/helpers.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(['error' => 'Method not allowed.'], 405);
}

if (empty($_SESSION['user_id'])) {
    respond(['error' => 'Chưa đăng nhập. Vui lòng đăng nhập lại.'], 401);
}

$userId = (int)$_SESSION['user_id'];
$data = json_body();

$currentPassword = (string)($data['current_password'] ?? '');
$newPassword = (string)($data['new_password'] ?? '');
$confirmPassword = (string)($data['confirm_password'] ?? '');

if ($currentPassword === '' || $newPassword === '') {
    respond(['error' => 'Vui lòng nhập mật khẩu hiện tại và mật khẩu mới.'], 422);
}

if (strlen($newPassword) < 6) {
    respond(['error' => 'Mật khẩu mới cần có ít nhất 6 ký tự.'], 422);
}

if ($confirmPassword !== '' && $newPassword !== $confirmPassword) {
    respond(['error' => 'Xác nhận mật khẩu mới không khớp.'], 422);
}

if ($currentPassword === $newPassword) {
    respond(['error' => 'Mật khẩu mới không được trùng với mật khẩu hiện tại.'], 422);
}

$stmt = $pdo->prepare('SELECT id, password_hash, is_active FROM users WHERE id = ? LIMIT 1');
$stmt->execute([$userId]);
$user = $stmt->fetch();

if (!$user || !(bool)$user['is_active']) {
    respond(['error' => 'Tài khoản không tồn tại hoặc đã bị khóa.'], 403);
}

if (!password_verify($currentPassword, $user['password_hash'])) {
    respond(['error' => 'Mật khẩu hiện tại không chính xác.'], 400);
}

$newHash = password_hash($newPassword, PASSWORD_DEFAULT);
$updateStmt = $pdo->prepare('UPDATE users SET password_hash = ? WHERE id = ?');
$updateStmt->execute([$newHash, $userId]);

respond([
    'ok' => true,
    'message' => 'Đổi mật khẩu thành công!'
]);
```

---

### PHẦN 2: Frontend Module Modal (`js/change-password.js`)

Tạo mới file `js/change-password.js` với thiết kế tự động tạo DOM (`ensureModal`), quản lý trạng thái, ẩn/hiện mật khẩu và xử lý gọi API:

```javascript
(function (global) {
    'use strict';

    function escapeHtml(str) {
        return String(str ?? '').replace(/[&<>"']/g, function (m) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m];
        });
    }

    function createModalDom() {
        if (document.getElementById('changePasswordModal')) return;

        const modalHtml = `
        <div id="changePasswordModal" class="fixed inset-0 z-[9999] hidden items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm transition-opacity duration-200">
            <div class="relative w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl border border-slate-100 transform transition-all">
                <div class="flex items-center justify-between border-b border-slate-100 pb-4 mb-4">
                    <div class="flex items-center gap-3">
                        <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-amber-600 border border-amber-200">
                            <i class="fas fa-key text-lg"></i>
                        </div>
                        <div>
                            <h3 class="text-lg font-bold text-slate-900">Đổi Mật Khẩu</h3>
                            <p id="changePasswordUserSub" class="text-xs text-slate-500">Cập nhật mật khẩu tài khoản</p>
                        </div>
                    </div>
                    <button type="button" id="btnCpClose" class="text-slate-400 hover:text-slate-600 p-1 rounded-lg transition">
                        <i class="fas fa-times text-lg"></i>
                    </button>
                </div>

                <div id="changePasswordAlert" class="hidden mb-4 rounded-xl p-3 text-sm font-medium border"></div>

                <form id="changePasswordForm" class="space-y-4" onsubmit="ChangePasswordModal.submit(event)">
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1" for="cpCurrentPassword">
                            Mật khẩu hiện tại
                        </label>
                        <div class="relative">
                            <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
                                <i class="fas fa-lock text-sm"></i>
                            </span>
                            <input type="password" id="cpCurrentPassword" required autocomplete="current-password"
                                class="w-full rounded-xl border border-slate-200 py-2.5 pl-10 pr-10 text-sm outline-none transition focus:border-amber-500 focus:ring-2 focus:ring-amber-200"
                                placeholder="Nhập mật khẩu hiện tại">
                            <button type="button" class="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-400 hover:text-slate-600"
                                onclick="ChangePasswordModal.toggleVisibility('cpCurrentPassword', this)">
                                <i class="fas fa-eye text-sm"></i>
                            </button>
                        </div>
                    </div>

                    <div>
                        <label class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1" for="cpNewPassword">
                            Mật khẩu mới
                        </label>
                        <div class="relative">
                            <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
                                <i class="fas fa-shield-alt text-sm"></i>
                            </span>
                            <input type="password" id="cpNewPassword" required minlength="6" autocomplete="new-password"
                                class="w-full rounded-xl border border-slate-200 py-2.5 pl-10 pr-10 text-sm outline-none transition focus:border-amber-500 focus:ring-2 focus:ring-amber-200"
                                placeholder="Tối thiểu 6 ký tự">
                            <button type="button" class="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-400 hover:text-slate-600"
                                onclick="ChangePasswordModal.toggleVisibility('cpNewPassword', this)">
                                <i class="fas fa-eye text-sm"></i>
                            </button>
                        </div>
                    </div>

                    <div>
                        <label class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1" for="cpConfirmPassword">
                            Xác nhận mật khẩu mới
                        </label>
                        <div class="relative">
                            <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
                                <i class="fas fa-check-circle text-sm"></i>
                            </span>
                            <input type="password" id="cpConfirmPassword" required minlength="6" autocomplete="new-password"
                                class="w-full rounded-xl border border-slate-200 py-2.5 pl-10 pr-10 text-sm outline-none transition focus:border-amber-500 focus:ring-2 focus:ring-amber-200"
                                placeholder="Nhập lại mật khẩu mới">
                            <button type="button" class="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-400 hover:text-slate-600"
                                onclick="ChangePasswordModal.toggleVisibility('cpConfirmPassword', this)">
                                <i class="fas fa-eye text-sm"></i>
                            </button>
                        </div>
                    </div>

                    <div class="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                        <button type="button" id="btnCpCancel"
                            class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-50">
                            Hủy
                        </button>
                        <button type="submit" id="btnCpSubmit"
                            class="inline-flex items-center gap-2 rounded-xl bg-amber-500 hover:bg-amber-600 text-white px-5 py-2 text-sm font-bold shadow-md shadow-amber-200 transition">
                            <span>Lưu thay đổi</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);

        document.getElementById('btnCpClose')?.addEventListener('click', () => ChangePasswordModal.close());
        document.getElementById('btnCpCancel')?.addEventListener('click', () => ChangePasswordModal.close());

        const modalOverlay = document.getElementById('changePasswordModal');
        modalOverlay?.addEventListener('click', (e) => {
            if (e.target === modalOverlay) ChangePasswordModal.close();
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !modalOverlay?.classList.contains('hidden')) {
                ChangePasswordModal.close();
            }
        });
    }

    const ChangePasswordModal = {
        ensureModal: function () {
            createModalDom();
        },

        open: function () {
            this.ensureModal();
            const modal = document.getElementById('changePasswordModal');
            if (!modal) return;

            const form = document.getElementById('changePasswordForm');
            if (form) form.reset();

            const alertBox = document.getElementById('changePasswordAlert');
            if (alertBox) {
                alertBox.className = 'hidden mb-4 rounded-xl p-3 text-sm font-medium border';
                alertBox.textContent = '';
            }

            const username = localStorage.getItem('userEmail') || localStorage.getItem('userName') || '';
            const sub = document.getElementById('changePasswordUserSub');
            if (sub && username) {
                sub.textContent = 'Tài khoản: ' + username;
            }

            modal.classList.remove('hidden');
            modal.classList.add('flex');

            setTimeout(() => {
                document.getElementById('cpCurrentPassword')?.focus();
            }, 100);
        },

        close: function () {
            const modal = document.getElementById('changePasswordModal');
            if (!modal) return;
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            const form = document.getElementById('changePasswordForm');
            if (form) form.reset();
        },

        toggleVisibility: function (inputId, btn) {
            const input = document.getElementById(inputId);
            if (!input) return;
            const icon = btn?.querySelector('i');
            if (input.type === 'password') {
                input.type = 'text';
                if (icon) {
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                }
            } else {
                input.type = 'password';
                if (icon) {
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            }
        },

        showAlert: function (message, type) {
            const box = document.getElementById('changePasswordAlert');
            if (!box) return;
            box.classList.remove('hidden', 'bg-rose-50', 'text-rose-700', 'border-rose-200', 'bg-emerald-50', 'text-emerald-700', 'border-emerald-200');
            if (type === 'success') {
                box.classList.add('bg-emerald-50', 'text-emerald-700', 'border-emerald-200');
                box.innerHTML = '<i class="fas fa-check-circle mr-2"></i>' + escapeHtml(message);
            } else {
                box.classList.add('bg-rose-50', 'text-rose-700', 'border-rose-200');
                box.innerHTML = '<i class="fas fa-exclamation-circle mr-2"></i>' + escapeHtml(message);
            }
        },

        submit: async function (e) {
            if (e) e.preventDefault();
            const currentPassword = document.getElementById('cpCurrentPassword')?.value || '';
            const newPassword = document.getElementById('cpNewPassword')?.value || '';
            const confirmPassword = document.getElementById('cpConfirmPassword')?.value || '';
            const submitBtn = document.getElementById('btnCpSubmit');

            if (!currentPassword || !newPassword) {
                this.showAlert('Vui lòng điền đầy đủ các thông tin.', 'error');
                return;
            }

            if (newPassword.length < 6) {
                this.showAlert('Mật khẩu mới cần ít nhất 6 ký tự.', 'error');
                return;
            }

            if (newPassword !== confirmPassword) {
                this.showAlert('Xác nhận mật khẩu mới không trùng khớp.', 'error');
                return;
            }

            if (currentPassword === newPassword) {
                this.showAlert('Mật khẩu mới không được trùng mật khẩu cũ.', 'error');
                return;
            }

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-1.5"></i> Đang xử lý...';
            }

            try {
                const response = await fetch('api/change_password.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({
                        current_password: currentPassword,
                        new_password: newPassword,
                        confirm_password: confirmPassword
                    })
                });

                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.error || 'Có lỗi xảy ra khi đổi mật khẩu.');
                }

                this.showAlert(data.message || 'Đổi mật khẩu thành công!', 'success');
                const form = document.getElementById('changePasswordForm');
                if (form) form.reset();

                setTimeout(() => {
                    ChangePasswordModal.close();
                }, 1600);
            } catch (err) {
                this.showAlert(err.message || 'Không thể đổi mật khẩu.', 'error');
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<span>Lưu thay đổi</span>';
                }
            }
        }
    };

    global.ChangePasswordModal = ChangePasswordModal;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => ChangePasswordModal.ensureModal());
    } else {
        ChangePasswordModal.ensureModal();
    }
})(typeof window !== 'undefined' ? window : this);
```

---

### PHẦN 3: Giao Diện Navbar Trong `index.html`

#### 1. Thêm nút "Đổi mật khẩu" trên Navbar:
Trong file `index.html`, tại khối `<nav>` (khoảng dòng 1174):
Đặt nút `<button ... id="btnOpenChangePassword">` ngay trước nút Đăng xuất:

```html
<button type="button" onclick="ChangePasswordModal.open()" id="btnOpenChangePassword"
    class="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3.5 py-2 text-sm font-bold text-slate-700 shadow-sm transition hover:bg-slate-50 hover:border-slate-300">
    <i class="fas fa-key text-amber-500"></i> Đổi mật khẩu
</button>
```

#### 2. Nhúng Script `js/change-password.js`:
Tại phần nhúng script ở cuối file `index.html` (khoảng dòng 1615, ngay sau `js/user-ai-settings.js`):
Thêm:
```html
<script src="js/change-password.js"></script>
```

#### 3. Đảm bảo quyền truy cập cho Học sinh (`setupStudentPortal`):
Kiểm tra hàm `setupStudentPortal` trong `index.html`:
Chỉ ẩn `btnOpenUserAiSettings` (Cài đặt AI & Key), tuyệt đối **KHÔNG** thêm `btnOpenChangePassword` vào danh sách ẩn. Cả Giáo viên và Học sinh đều được phép đổi mật khẩu.

---

### PHẦN 4: Viết Test Tự Động (`tests/change-password-smoke.js`)

Tạo mới file `tests/change-password-smoke.js` với các kiểm tra toàn diện:

```javascript
const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const indexHtml = fs.readFileSync(path.join(root, "index.html"), "utf8");
const jsScript = fs.readFileSync(path.join(root, "js", "change-password.js"), "utf8");
const phpScript = fs.readFileSync(path.join(root, "api", "change_password.php"), "utf8");

// 1. Kiểm tra index.html
assert.match(indexHtml, /id="btnOpenChangePassword"/, "index.html phải có nút Đổi mật khẩu");
assert.match(indexHtml, /ChangePasswordModal\.open\(\)/, "nút Đổi mật khẩu phải gọi ChangePasswordModal.open()");
assert.match(indexHtml, /js\/change-password\.js/, "index.html phải nhúng js/change-password.js");

// 2. Kiểm tra js/change-password.js
assert.match(jsScript, /ChangePasswordModal/, "module định nghĩa ChangePasswordModal");
assert.match(jsScript, /ensureModal/, "có hàm ensureModal");
assert.match(jsScript, /open\s*:/, "có hàm open");
assert.match(jsScript, /close\s*:/, "có hàm close");
assert.match(jsScript, /toggleVisibility/, "có hàm toggleVisibility để ẩn hiện mật khẩu");
assert.match(jsScript, /submit\s*:/, "có hàm submit");
assert.match(jsScript, /api\/change_password\.php/, "gọi endpoint api/change_password.php");

// 3. Kiểm tra api/change_password.php
assert.match(phpScript, /require_once\s+__DIR__\s*\.\s*'\/helpers\.php'/, "PHP nhúng helpers.php");
assert.match(phpScript, /\$_SESSION\['user_id'\]/, "PHP kiểm tra session user_id");
assert.match(phpScript, /password_verify/, "PHP xác thực mật khẩu cũ bằng password_verify");
assert.match(phpScript, /password_hash/, "PHP mã hóa mật khẩu mới bằng password_hash");
assert.match(phpScript, /UPDATE\s+users\s+SET\s+password_hash/, "PHP cập nhật CSDL bảng users");

console.log("change-password smoke: PASS");
```

---

## 3. Kế Hoạch Kiểm Thử & Nghiệm Thu (Verification Plan)

1. **Kiểm tra cú pháp PHP:**
   ```powershell
   php -l api/change_password.php
   ```
   Kết quả kỳ vọng: `No syntax errors detected in api/change_password.php`.

2. **Chạy test tự động Smoke Test:**
   ```powershell
   node tests/change-password-smoke.js
   ```
   Kết quả kỳ vọng: `change-password smoke: PASS`.

3. **Chạy kiểm tra hồi quy:**
   ```powershell
   node tests/user-ai-settings-smoke.js
   node tests/canvas-tabs-permissions-smoke.js
   ```
   Kết quả kỳ vọng: Tất cả bài test liên quan đến `index.html` và phân quyền đều `PASS`.

4. **Kiểm tra luồng thực tế (Manual/Browser):**
   - Đăng nhập tài khoản Giáo viên hoặc Học sinh -> Bấm nút "Đổi mật khẩu" trên navbar -> Modal mở lên.
   - Bấm icon mắt -> Chuyển đổi giữa ẩn và hiện ký tự mật khẩu.
   - Nhập mật khẩu hiện tại sai -> Thông báo lỗi màu đỏ "Mật khẩu hiện tại không chính xác".
   - Nhập mật khẩu mới < 6 ký tự hoặc không khớp xác nhận -> Báo lỗi phù hợp.
   - Nhập đúng toàn bộ thông tin -> Báo thành công màu xanh, tự động đóng modal.
   - Đăng xuất và đăng nhập lại bằng mật khẩu mới -> Đăng nhập thành công.
