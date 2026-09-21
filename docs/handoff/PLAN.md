# PLAN: Thêm Chức Năng Đổi Mật Khẩu & Đổi SmartQuiz Thành Game Giáo Dục

## 1. Tổng Quan Nhiệm Vụ

Bản kế hoạch này bao gồm 2 yêu cầu:
1. **Thêm chức năng Đổi mật khẩu**: Cho phép người dùng (cả Giáo viên và Học sinh) tự đổi mật khẩu cá nhân khi đã đăng nhập hệ thống, gồm backend `api/change_password.php`, frontend modal `js/change-password.js`, nút điều hướng trên Navbar của `index.html` và test tự động `tests/change-password-smoke.js`.
2. **Cập nhật trang chủ (`index.html`)**: Thay thế mục `SmartQuiz` thành **`Game giáo dục`** và cập nhật đường link chuyển hướng sang `https://www.hoangthiencm.id.vn/trochoi.html`.

---

## 2. Chi Tiết Thực Hiện Cho Coder

### PHẦN 1: Cập Nhật Trang Chủ (`index.html`) — Đổi SmartQuiz thành Game Giáo Dục

Tại file `index.html`, thực hiện 3 điểm chỉnh sửa:

#### 1. Cập nhật bảng liên kết `TOOL_PAGE_LINKS` (khoảng dòng 963):
Thay:
```javascript
smartquiz: 'smartquiz.html',
```
Bằng:
```javascript
smartquiz: 'https://www.hoangthiencm.id.vn/trochoi.html',
```

#### 2. Cập nhật thẻ công cụ giáo viên trên Grid (`#mainToolsGrid`, khoảng dòng 1364):
Thay khối thẻ:
```html
<a href="smartquiz.html" data-tool="smartquiz" class="tool-tile tool-tile--colored tool-tile--smartquiz">
    <span class="tool-tile-glow"></span>
    <span class="tool-tile-watermark"><i class="fas fa-wand-magic-sparkles"></i></span>
    <div class="tool-tile-content">
        <span class="tool-tile-eyebrow">Giảng dạy</span>
        <h3 class="tool-tile-title">Soạn câu hỏi game</h3>
        <p class="tool-tile-desc">Nhập chủ đề — AI soạn câu hỏi và slide dạy học tức thì.</p>
    </div>
    <span class="tool-tile-go"><i class="fas fa-arrow-right"></i></span>
</a>
```
Bằng:
```html
<a href="https://www.hoangthiencm.id.vn/trochoi.html" data-tool="smartquiz" class="tool-tile tool-tile--colored tool-tile--smartquiz">
    <span class="tool-tile-glow"></span>
    <span class="tool-tile-watermark"><i class="fas fa-gamepad"></i></span>
    <div class="tool-tile-content">
        <span class="tool-tile-eyebrow">Giảng dạy</span>
        <h3 class="tool-tile-title">Game giáo dục</h3>
        <p class="tool-tile-desc">Trò chơi giáo dục tương tác, ôn tập kiến thức sinh động.</p>
    </div>
    <span class="tool-tile-go"><i class="fas fa-arrow-right"></i></span>
</a>
```

#### 3. Cập nhật mục hoạt động cho Học sinh trong `setupStudentPortal` (khoảng dòng 1746):
Thay mục:
```javascript
{
    key: 'smartquiz',
    title: 'Trò chơi ôn luyện SmartQuiz',
    badge: 'Mini-game',
    desc: 'Tham gia các câu hỏi tương tác, trò chơi ôn tập kiến thức sinh động.',
    url: 'smartquiz.html',
    icon: 'fa-gamepad',
    color: 'from-pink-500 to-rose-600',
    actionText: 'Vào chơi ôn tập'
},
```
Bằng:
```javascript
{
    key: 'smartquiz',
    title: 'Game giáo dục',
    badge: 'Trò chơi',
    desc: 'Tham gia các trò chơi giáo dục tương tác, ôn tập kiến thức sinh động.',
    url: 'https://www.hoangthiencm.id.vn/trochoi.html',
    icon: 'fa-gamepad',
    color: 'from-pink-500 to-rose-600',
    actionText: 'Vào chơi'
},
```

---

### PHẦN 2: Thêm Chức Năng Đổi Mật Khẩu Cho Người Dùng

#### 1. Backend Endpoint (`api/change_password.php` - Tạo mới):
Tạo file `api/change_password.php`:
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

#### 2. Frontend Module Modal (`js/change-password.js` - Tạo mới):
Tạo file `js/change-password.js`:
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

#### 3. Nút "Đổi mật khẩu" trên Navbar `index.html`:
Trong `<nav>` (khoảng dòng 1174, ngay trước nút Đăng xuất):
Thêm:
```html
<button type="button" onclick="ChangePasswordModal.open()" id="btnOpenChangePassword"
    class="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3.5 py-2 text-sm font-bold text-slate-700 shadow-sm transition hover:bg-slate-50 hover:border-slate-300">
    <i class="fas fa-key text-amber-500"></i> Đổi mật khẩu
</button>
```

Và nhúng script `js/change-password.js` tại cuối file `index.html` (ngay sau `js/user-ai-settings.js`):
```html
<script src="js/change-password.js"></script>
```

---

### PHẦN 3: Bài Test Tự Động (`tests/change-password-smoke.js`)

Tạo mới file `tests/change-password-smoke.js`:
```javascript
const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const indexHtml = fs.readFileSync(path.join(root, "index.html"), "utf8");
const jsScript = fs.readFileSync(path.join(root, "js", "change-password.js"), "utf8");
const phpScript = fs.readFileSync(path.join(root, "api", "change_password.php"), "utf8");

// 1. Kiểm tra index.html có nút Đổi mật khẩu & link Game giáo dục
assert.match(indexHtml, /id="btnOpenChangePassword"/, "index.html phải có nút Đổi mật khẩu");
assert.match(indexHtml, /ChangePasswordModal\.open\(\)/, "nút Đổi mật khẩu phải gọi ChangePasswordModal.open()");
assert.match(indexHtml, /js\/change-password\.js/, "index.html phải nhúng js/change-password.js");
assert.match(indexHtml, /https:\/\/www\.hoangthiencm\.id\.vn\/trochoi\.html/, "index.html phải có đường link trochoi.html");
assert.match(indexHtml, /Game giáo dục/, "index.html phải hiển thị Game giáo dục thay cho SmartQuiz");

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
2. **Chạy test tự động:**
   ```powershell
   node tests/change-password-smoke.js
   node tests/user-ai-settings-smoke.js
   node tests/canvas-tabs-permissions-smoke.js
   ```
3. **Kiểm tra giao diện:**
   - Mở `index.html`: mục SmartQuiz đã đổi thành **Game giáo dục**, khi bấm chuyển hướng sang `https://www.hoangthiencm.id.vn/trochoi.html`.
   - Nút **Đổi mật khẩu** hiển thị rõ ràng trên Navbar cho cả Giáo viên và Học sinh, mở modal đổi mật khẩu hoạt động trơn tru.
