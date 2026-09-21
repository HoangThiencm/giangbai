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
