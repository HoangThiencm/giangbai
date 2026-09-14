<?php
require_once __DIR__ . '/helpers.php';

function sodiem_teacher(PDO $pdo): array {
    if (empty($_SESSION['user_id'])) respond(['error' => 'Cần đăng nhập tài khoản giáo viên.'], 401);
    $stmt = $pdo->prepare("SELECT id FROM users WHERE id = ? AND role = 'teacher' AND is_active = 1 LIMIT 1");
    $stmt->execute([(int)$_SESSION['user_id']]);
    $teacher = $stmt->fetch();
    if (!$teacher) respond(['error' => 'Cần đăng nhập tài khoản giáo viên.'], 401);
    return $teacher;
}

function ensure_gradebook_schema(PDO $pdo): void {
    $pdo->exec("CREATE TABLE IF NOT EXISTS gradebooks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        teacher_id INT NOT NULL,
        class_name VARCHAR(80) NOT NULL,
        subject VARCHAR(80) NOT NULL,
        academic_year VARCHAR(30) NOT NULL DEFAULT '2025-2026',
        columns_config_json TEXT DEFAULT NULL,
        students_data_json LONGTEXT DEFAULT NULL,
        history_log_json LONGTEXT DEFAULT NULL,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_teacher_class_sub (teacher_id, class_name, subject, academic_year),
        INDEX idx_gradebooks_class (class_name)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}

$teacher = sodiem_teacher($pdo);
ensure_gradebook_schema($pdo);
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$action = trim((string)($_GET['action'] ?? ''));

if ($method === 'GET' && $action === 'classes') {
    $rows = $pdo->query("SELECT class_name, COUNT(*) AS count FROM users WHERE role = 'student' AND is_active = 1 AND TRIM(class_name) <> '' GROUP BY class_name ORDER BY class_name")->fetchAll();
    respond(['classes' => array_map(fn($row) => ['class_name' => $row['class_name'], 'count' => (int)$row['count']], $rows)]);
}

if ($method === 'GET' && $action === 'load') {
    $class = trim((string)($_GET['class_name'] ?? ''));
    $subject = trim((string)($_GET['subject'] ?? ''));
    $year = trim((string)($_GET['academic_year'] ?? '2025-2026'));
    if ($class === '' || $subject === '') respond(['error' => 'Thiếu lớp hoặc môn học.'], 422);
    $stmt = $pdo->prepare('SELECT columns_config_json, students_data_json, history_log_json, updated_at FROM gradebooks WHERE teacher_id = ? AND class_name = ? AND subject = ? AND academic_year = ? LIMIT 1');
    $stmt->execute([(int)$teacher['id'], $class, $subject, $year]);
    $book = $stmt->fetch();
    respond(['gradebook' => $book ?: null]);
}

if ($method === 'POST' && $action === 'save') {
    $data = json_body();
    $class = trim((string)($data['class_name'] ?? ''));
    $subject = trim((string)($data['subject'] ?? ''));
    $year = trim((string)($data['academic_year'] ?? '2025-2026'));
    if ($class === '' || $subject === '') respond(['error' => 'Thiếu lớp hoặc môn học.'], 422);
    $stmt = $pdo->prepare('INSERT INTO gradebooks (teacher_id, class_name, subject, academic_year, columns_config_json, students_data_json, history_log_json) VALUES (?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE columns_config_json = VALUES(columns_config_json), students_data_json = VALUES(students_data_json), history_log_json = VALUES(history_log_json)');
    $stmt->execute([(int)$teacher['id'], $class, $subject, $year, json_encode($data['columns'] ?? [], JSON_UNESCAPED_UNICODE), json_encode($data['students'] ?? [], JSON_UNESCAPED_UNICODE), json_encode($data['history'] ?? [], JSON_UNESCAPED_UNICODE)]);
    respond(['status' => 'ok']);
}

respond(['error' => 'Hành động không hợp lệ.'], 404);
