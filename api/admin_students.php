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
    $allowedPages = normalize_pages($data['allowed_pages'] ?? ['lotrinhtoan6']);

    if ($username === '' || $password === '' || $fullName === '') {
        respond(['error' => 'Thieu tai khoan, mat khau hoac ho ten.'], 422);
    }

    $hash = password_hash($password, PASSWORD_DEFAULT);

    try {
        $stmt = $pdo->prepare('
            INSERT INTO users (username, password_hash, full_name, role, class_name, allowed_pages_json, is_active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        ');
        $stmt->execute([$username, $hash, $fullName, $role, $className ?: null, json_encode($allowedPages, JSON_UNESCAPED_UNICODE)]);
        respond(['ok' => true, 'id' => (int)$pdo->lastInsertId(), 'mode' => 'created']);
    } catch (PDOException $e) {
        $existing = $pdo->prepare('SELECT id FROM users WHERE username = ? LIMIT 1');
        $existing->execute([$username]);
        $user = $existing->fetch();

        if (!$user) {
            respond(['error' => 'Tai khoan da ton tai hoac du lieu khong hop le.'], 409);
        }

        $update = $pdo->prepare('
            UPDATE users
            SET password_hash = ?, full_name = ?, role = ?, class_name = ?, allowed_pages_json = ?, is_active = 1
            WHERE id = ?
        ');
        $update->execute([$hash, $fullName, $role, $className ?: null, json_encode($allowedPages, JSON_UNESCAPED_UNICODE), $user['id']]);
        respond(['ok' => true, 'id' => (int)$user['id'], 'mode' => 'updated']);
    }
}

if ($action === 'update') {
    $id = (int)($data['id'] ?? 0);
    if ($id <= 0) respond(['error' => 'Thieu ID tai khoan.'], 422);

    $fullName = trim($data['full_name'] ?? '');
    $className = trim($data['class_name'] ?? '');
    $role = ($data['role'] ?? 'student') === 'teacher' ? 'teacher' : 'student';
    $isActive = !empty($data['is_active']) ? 1 : 0;
    $allowedPages = normalize_pages($data['allowed_pages'] ?? ['lotrinhtoan6']);

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
    if ($id <= 0) respond(['error' => 'Thieu ID tai khoan.'], 422);
    $pdo->prepare('DELETE FROM users WHERE id = ?')->execute([$id]);
    respond(['ok' => true]);
}

if ($action === 'import_batch') {
    $rows = $data['rows'] ?? [];
    if (!is_array($rows) || count($rows) === 0) {
        respond(['error' => 'Khong co du lieu hoc sinh de import.'], 422);
    }

    $defaultPassword = trim((string)($data['default_password'] ?? '123456'));
    if ($defaultPassword === '') {
        respond(['error' => 'Can mat khau mac dinh cho hoc sinh.'], 422);
    }

    $defaultClass = trim((string)($data['default_class_name'] ?? ''));
    $allowedPages = normalize_pages($data['allowed_pages'] ?? ['lotrinhtoan6']);
    $pagesJson = json_encode($allowedPages, JSON_UNESCAPED_UNICODE);

    $created = 0;
    $updated = 0;
    $failed = [];

    $insert = $pdo->prepare('
        INSERT INTO users (username, password_hash, full_name, role, class_name, allowed_pages_json, is_active)
        VALUES (?, ?, ?, ?, ?, ?, 1)
    ');
    $update = $pdo->prepare('
        UPDATE users
        SET password_hash = ?, full_name = ?, role = ?, class_name = ?, allowed_pages_json = ?, is_active = 1
        WHERE id = ?
    ');
    $find = $pdo->prepare('SELECT id FROM users WHERE username = ? LIMIT 1');

    foreach ($rows as $index => $row) {
        if (!is_array($row)) continue;

        $lineNo = (int)($row['line'] ?? ($index + 1));
        $username = trim((string)($row['username'] ?? ''));
        $fullName = trim((string)($row['full_name'] ?? ''));
        $password = trim((string)($row['password'] ?? ''));
        $className = trim((string)($row['class_name'] ?? ''));
        $role = (($row['role'] ?? 'student') === 'teacher') ? 'teacher' : 'student';

        if ($username === '' && $fullName === '') continue;
        if ($username === '' || $fullName === '') {
            $failed[] = ['line' => $lineNo, 'username' => $username, 'error' => 'Thieu tai khoan hoac ho ten.'];
            continue;
        }

        if ($password === '') $password = $defaultPassword;
        if ($className === '') $className = $defaultClass;

        $hash = password_hash($password, PASSWORD_DEFAULT);

        try {
            $find->execute([$username]);
            $existing = $find->fetch();
            if ($existing) {
                $update->execute([
                    $hash,
                    $fullName,
                    $role,
                    $className !== '' ? $className : null,
                    $pagesJson,
                    (int)$existing['id'],
                ]);
                $updated++;
            } else {
                $insert->execute([
                    $username,
                    $hash,
                    $fullName,
                    $role,
                    $className !== '' ? $className : null,
                    $pagesJson,
                ]);
                $created++;
            }
        } catch (PDOException $e) {
            $failed[] = ['line' => $lineNo, 'username' => $username, 'error' => 'Khong luu duoc tai khoan.'];
        }
    }

    respond([
        'ok' => true,
        'created' => $created,
        'updated' => $updated,
        'failed' => $failed,
        'total' => $created + $updated,
    ]);
}

respond(['error' => 'Action khong hop le.'], 400);
