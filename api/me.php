<?php
require_once __DIR__ . '/helpers.php';
session_start();

if (empty($_SESSION['user_id'])) {
    respond(['error' => 'Chưa đăng nhập.'], 401);
}

$stmt = $pdo->prepare('SELECT * FROM users WHERE id = ? LIMIT 1');
$stmt->execute([$_SESSION['user_id']]);
$user = $stmt->fetch();

if (!$user || !(bool)$user['is_active']) {
    respond(['error' => 'Tài khoản không còn hoạt động.'], 403);
}

respond(['ok' => true, 'user' => public_user($user), 'pages' => page_catalog()]);
