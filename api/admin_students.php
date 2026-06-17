<?php
require_once __DIR__ . '/helpers.php';
require_admin_key();

$method = $_SERVER['REQUEST_METHOD'];
$data = json_body();

if ($method === 'GET') {
    $stmt = $pdo->query("SELECT * FROM users ORDER BY role ASC, class_name ASC, full_name ASC, id DESC");
    $users = array_map('public_user', $stmt->fetchAll());
    respond(['ok' => true, 'users' => $users, 'pages' => page_catalog()]);
}

if ($method !== 'POST') {
    respond(['error' => 'Method not allowed.'], 405);
}

$action = $data['action'] ?? '';

if ($action === 'create') {
    $username = trim($data['username'] ?? '');
    $password = (string)($data['password'] ?? '');
    $fullName = trim($data['full_name'] ?? '');
    $role = ($data['role'] ?? 'student') === 'teacher' ? 'teacher' : 'student';
    $className = trim($data['class_name'] ?? '');
    $allowedPages = normalize_pages($data['allowed_pages'] ?? ['lotrinh']);

    if ($username === '' || $password === '' || $fullName === '') {
        respond(['error' => 'Thiếu tài khoản, mật khẩu hoặc họ tên.'], 422);
    }

    $hash = password_hash($password, PASSWORD_DEFAULT);
    try {
        $stmt = $pdo->prepare('
            INSERT INTO users (username, password_hash, full_name, role, class_name, allowed_pages_json, is_active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        ');
        $stmt->execute([$username, $hash, $fullName, $role, $className ?: null, json_encode($allowedPages, JSON_UNESCAPED_UNICODE)]);
        respond(['ok' => true, 'id' => (int)$pdo->lastInsertId()]);
    } catch (PDOException $e) {
        respond(['error' => 'Tài khoản đã tồn tại hoặc dữ liệu không hợp lệ.'], 409);
    }
}

if ($action === 'update') {
    $id = (int)($data['id'] ?? 0);
    if ($id <= 0) respond(['error' => 'Thiếu ID tài khoản.'], 422);

    $fullName = trim($data['full_name'] ?? '');
    $className = trim($data['class_name'] ?? '');
    $role = ($data['role'] ?? 'student') === 'teacher' ? 'teacher' : 'student';
    $isActive = !empty($data['is_active']) ? 1 : 0;
    $allowedPages = normalize_pages($data['allowed_pages'] ?? ['lotrinh']);

    $stmt = $pdo->prepare('
        UPDATE users
        SET full_name = ?, class_name = ?, role = ?, is_active = ?, allowed_pages_json = ?
        WHERE id = ?
    ');
    $stmt->execute([$fullName, $className ?: null, $role, $isActive, json_encode($allowedPages, JSON_UNESCAPED_UNICODE), $id]);

    if (!empty($data['password'])) {
        $hash = password_hash((string)$data['password'], PASSWORD_DEFAULT);
        $pdo->prepare('UPDATE users SET password_hash = ? WHERE id = ?')->execute([$hash, $id]);
    }

    respond(['ok' => true]);
}

if ($action === 'delete') {
    $id = (int)($data['id'] ?? 0);
    if ($id <= 0) respond(['error' => 'Thiếu ID tài khoản.'], 422);
    $pdo->prepare('DELETE FROM users WHERE id = ?')->execute([$id]);
    respond(['ok' => true]);
}

respond(['error' => 'Action không hợp lệ.'], 400);
