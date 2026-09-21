const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const indexHtml = fs.readFileSync(path.join(root, "index.html"), "utf8");
const jsScript = fs.readFileSync(path.join(root, "js", "change-password.js"), "utf8");
const phpScript = fs.readFileSync(path.join(root, "api", "change_password.php"), "utf8");

assert.match(indexHtml, /id="btnOpenChangePassword"/, "index.html phải có nút Đổi mật khẩu");
assert.match(indexHtml, /ChangePasswordModal\.open\(\)/, "nút Đổi mật khẩu phải gọi ChangePasswordModal.open()");
assert.match(indexHtml, /js\/change-password\.js/, "index.html phải nhúng js/change-password.js");
assert.match(indexHtml, /https:\/\/www\.hoangthiencm\.id\.vn\/trochoi\.html/, "index.html phải có đường link trochoi.html");
assert.match(indexHtml, /Game giáo dục/, "index.html phải hiển thị Game giáo dục thay cho SmartQuiz");

assert.match(jsScript, /ChangePasswordModal/, "module định nghĩa ChangePasswordModal");
assert.match(jsScript, /ensureModal/, "có hàm ensureModal");
assert.match(jsScript, /open\s*:/, "có hàm open");
assert.match(jsScript, /close\s*:/, "có hàm close");
assert.match(jsScript, /toggleVisibility/, "có hàm toggleVisibility để ẩn hiện mật khẩu");
assert.match(jsScript, /submit\s*:/, "có hàm submit");
assert.match(jsScript, /api\/change_password\.php/, "gọi endpoint api/change_password.php");

assert.match(phpScript, /require_once\s+__DIR__\s*\.\s*'\/helpers\.php'/, "PHP nhúng helpers.php");
assert.match(phpScript, /\$_SESSION\['user_id'\]/, "PHP kiểm tra session user_id");
assert.match(phpScript, /password_verify/, "PHP xác thực mật khẩu cũ bằng password_verify");
assert.match(phpScript, /password_hash/, "PHP mã hóa mật khẩu mới bằng password_hash");
assert.match(phpScript, /UPDATE\s+users\s+SET\s+password_hash/, "PHP cập nhật CSDL bảng users");

console.log("change-password smoke: PASS");
