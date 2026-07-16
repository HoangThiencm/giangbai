<?php
require_once __DIR__ . '/helpers.php';

ensure_student_notifications_schema($pdo);
$user = ensure_login();
if (($user['role'] ?? '') !== 'student') {
    respond(['error' => 'Chức năng thông báo dành cho học sinh.'], 403);
}

$method = $_SERVER['REQUEST_METHOD'];
$action = trim((string)($_GET['action'] ?? 'list'));

if ($method === 'GET' && $action === 'list') {
    $subject = trim((string)($_GET['subject'] ?? ''));
    $sql = 'SELECT id, event_key, notification_type, entity_id, subject, title, message, created_at, read_at FROM student_notifications WHERE student_id = ? AND read_at IS NULL';
    $params = [(int)$user['id']];
    if ($subject !== '') {
        $sql .= ' AND subject = ?';
        $params[] = $subject;
    }
    $sql .= ' ORDER BY created_at DESC, id DESC LIMIT 30';
    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    respond(['notifications' => $stmt->fetchAll()]);
}

if ($method === 'POST' && $action === 'read') {
    $data = json_body();
    $id = (int)($data['id'] ?? 0);
    if ($id <= 0) respond(['error' => 'Thiếu mã thông báo.'], 422);
    $pdo->prepare('UPDATE student_notifications SET read_at = COALESCE(read_at, CURRENT_TIMESTAMP) WHERE id = ? AND student_id = ?')
        ->execute([$id, (int)$user['id']]);
    respond(['ok' => true]);
}

if ($method === 'POST' && $action === 'read-all') {
    $data = json_body();
    $subject = trim((string)($data['subject'] ?? ''));
    $sql = 'UPDATE student_notifications SET read_at = COALESCE(read_at, CURRENT_TIMESTAMP) WHERE student_id = ? AND read_at IS NULL';
    $params = [(int)$user['id']];
    if ($subject !== '') {
        $sql .= ' AND subject = ?';
        $params[] = $subject;
    }
    $pdo->prepare($sql)->execute($params);
    respond(['ok' => true]);
}

respond(['error' => 'Không tìm thấy thao tác thông báo.'], 404);
