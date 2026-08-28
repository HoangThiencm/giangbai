<?php
require_once __DIR__ . '/helpers.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(['error' => 'Method not allowed.'], 405);
}

ensure_users_registration_status_column($pdo);
ensure_users_expires_option_column($pdo);

$data = json_body();
$username = trim((string)($data['username'] ?? ''));
$password = (string)($data['password'] ?? '');
$fullName = trim((string)($data['full_name'] ?? ''));
$role = ($data['role'] ?? 'teacher') === 'student' ? 'student' : 'teacher';

if (!preg_match('/^[A-Za-z0-9._@-]{3,80}$/', $username)) {
    respond(['error' => 'Tài khoản gồm 3–80 ký tự: chữ, số, dấu chấm, gạch dưới hoặc @.'], 422);
}
if (mb_strlen($fullName) < 2 || mb_strlen($fullName) > 120) {
    respond(['error' => 'Vui lòng nhập họ và tên hợp lệ.'], 422);
}
if (strlen($password) < 6) {
    respond(['error' => 'Mật khẩu cần có ít nhất 6 ký tự.'], 422);
}

$existing = $pdo->prepare('SELECT id FROM users WHERE username = ? LIMIT 1');
$existing->execute([$username]);
if ($existing->fetch()) {
    respond(['error' => 'Tài khoản này đã được đăng ký.'], 409);
}

$stmt = $pdo->prepare('
    INSERT INTO users (username, password_hash, full_name, role, class_name, allowed_pages_json, is_active, registration_status, expires_at, expires_option)
    VALUES (?, ?, ?, ?, NULL, ?, 0, ?, NULL, ?)
');
$stmt->execute([
    $username,
    password_hash($password, PASSWORD_DEFAULT),
    $fullName,
    $role,
    json_encode([], JSON_UNESCAPED_UNICODE),
    'pending',
    'forever',
]);

respond(['ok' => true, 'message' => 'Đã gửi yêu cầu đăng ký. Vui lòng chờ Admin duyệt và cấp quyền.'], 201);
