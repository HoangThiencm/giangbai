<?php
require_once __DIR__ . '/helpers.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(['error' => 'Method not allowed.'], 405);
}

$data = json_body();
$username = trim($data['username'] ?? $data['email'] ?? '');
$password = (string)($data['password'] ?? '');

if ($username === '' || $password === '') {
    respond(['error' => 'Vui lòng nhập tài khoản và mật khẩu.'], 422);
}

ensure_users_ai_key_columns($pdo);
ensure_users_registration_status_column($pdo);

$stmt = $pdo->prepare('SELECT * FROM users WHERE username = ? LIMIT 1');
$stmt->execute([$username]);
$user = $stmt->fetch();

if (!$user || !password_verify($password, $user['password_hash'])) {
    respond(['error' => 'Sai tài khoản hoặc mật khẩu.'], 401);
}

if (($user['registration_status'] ?? '') === 'pending') {
    respond(['error' => 'Tài khoản đang chờ Admin duyệt và cấp quyền sử dụng.'], 403);
}

if (!(bool)$user['is_active']) {
    respond(['error' => 'Tài khoản đã bị khóa. Vui lòng liên hệ giáo viên.'], 403);
}

if (!empty($user['expires_at']) && strtotime($user['expires_at']) < time()) {
    respond(['error' => 'Tài khoản đã hết hạn. Vui lòng liên hệ giáo viên.'], 403);
}

$pdo->prepare('UPDATE users SET last_login_at = NOW() WHERE id = ?')->execute([$user['id']]);
$user = maybe_upgrade_teacher_allowed_pages($pdo, $user);

session_regenerate_id(true);
$_SESSION['user_id'] = (int)$user['id'];
$_SESSION['role'] = $user['role'];

respond([
    'ok' => true,
    'user' => public_user($user),
]);
