<?php
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/ai_smart_quota.php';
require_once __DIR__ . '/ai_student_quota.php';
session_start();

if (empty($_SESSION['user_id'])) {
    respond(['error' => 'Chưa đăng nhập.'], 401);
}

$stmt = $pdo->prepare('SELECT role, is_active FROM users WHERE id = ? LIMIT 1');
$stmt->execute([$_SESSION['user_id']]);
$user = $stmt->fetch();
if (!$user || !(bool)$user['is_active']) {
    respond(['error' => 'Tài khoản không hợp lệ.'], 403);
}

$role = (string)($user['role'] ?? '');
if (!in_array($role, ['teacher', 'admin'], true)) {
    respond(['error' => 'Chỉ giáo viên mới xem được quota AI.'], 403);
}

respond([
    'ok' => true,
    'today' => ai_usage_today_key(),
    'smart_quota' => ai_smart_quota_status(),
    'student_quota' => ai_student_quota_status((int)$_SESSION['user_id'], $role),
]);