<?php
require_once __DIR__ . '/helpers.php';

session_start();

const TIMETABLE_SCHEMA_VERSION = '20260629-v1';
const TIMETABLE_PROJECT_KEY = 'school_default';

function tkb_current_teacher(PDO $pdo): array
{
    $userId = (int)($_SESSION['user_id'] ?? 0);
    if ($userId <= 0) {
        respond(['error' => 'Vui lòng đăng nhập lại.'], 401);
    }

    $stmt = $pdo->prepare("SELECT id, username, full_name, role, is_active, allowed_pages_json FROM users WHERE id = ? LIMIT 1");
    $stmt->execute([$userId]);
    $user = $stmt->fetch();
    if (!$user || !(bool)$user['is_active'] || ($user['role'] ?? '') !== 'teacher') {
        respond(['error' => 'Chức năng xếp thời khóa biểu chỉ dành cho giáo viên.'], 403);
    }

    $allowedPages = teacher_allowed_pages_resolved($user);
    if (!in_array('thoikhoabieu', $allowedPages, true)) {
        respond(['error' => 'Tài khoản chưa được cấp quyền Xếp thời khóa biểu.'], 403);
    }

    return $user;
}

function tkb_maybe_ensure_schema(PDO $pdo): void
{
    if (schema_is_ready('thoikhoabieu', TIMETABLE_SCHEMA_VERSION)) {
        return;
    }
    tkb_ensure_schema($pdo);
    schema_mark_ready('thoikhoabieu', TIMETABLE_SCHEMA_VERSION);
}

function tkb_ensure_schema(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS timetable_projects (
        id INT AUTO_INCREMENT PRIMARY KEY,
        project_key VARCHAR(80) NOT NULL UNIQUE,
        name VARCHAR(180) NOT NULL DEFAULT 'Thời khóa biểu nhà trường',
        school_year VARCHAR(40) NOT NULL DEFAULT '',
        project_json LONGTEXT NOT NULL,
        result_json LONGTEXT DEFAULT NULL,
        created_by INT NOT NULL,
        updated_by INT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_timetable_projects_updated (updated_at),
        INDEX idx_timetable_projects_school_year (school_year),
        CONSTRAINT fk_timetable_project_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
        CONSTRAINT fk_timetable_project_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE CASCADE
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}

function tkb_project_payload(?array $row): ?array
{
    if (!$row) {
        return null;
    }

    return [
        'id' => (int)$row['id'],
        'project_key' => $row['project_key'],
        'name' => $row['name'],
        'school_year' => $row['school_year'],
        'project' => json_decode((string)$row['project_json'], true) ?: null,
        'result' => $row['result_json'] ? (json_decode((string)$row['result_json'], true) ?: null) : null,
        'created_at' => $row['created_at'],
        'updated_at' => $row['updated_at'],
        'created_by' => (int)$row['created_by'],
        'updated_by' => (int)$row['updated_by'],
    ];
}

function tkb_read_project(PDO $pdo): ?array
{
    $stmt = $pdo->prepare('SELECT * FROM timetable_projects WHERE project_key = ? LIMIT 1');
    $stmt->execute([TIMETABLE_PROJECT_KEY]);
    $row = $stmt->fetch();
    return tkb_project_payload($row ?: null);
}

function tkb_trim_text($value, int $limit): string
{
    $text = trim((string)$value);
    return function_exists('mb_substr') ? mb_substr($text, 0, $limit) : substr($text, 0, $limit);
}

function tkb_clean_project($project): array
{
    if (!is_array($project)) {
        throw new RuntimeException('Thiếu dữ liệu thời khóa biểu.');
    }

    return [
        'teachers' => array_values(array_slice(is_array($project['teachers'] ?? null) ? $project['teachers'] : [], 0, 300)),
        'importedAssignments' => array_values(array_slice(is_array($project['importedAssignments'] ?? null) ? $project['importedAssignments'] : [], 0, 3000)),
        'classes' => array_values(array_slice(is_array($project['classes'] ?? null) ? $project['classes'] : [], 0, 200)),
        'rooms' => array_values(array_slice(is_array($project['rooms'] ?? null) ? $project['rooms'] : [], 0, 300)),
        'assignments' => array_values(array_slice(is_array($project['assignments'] ?? null) ? $project['assignments'] : [], 0, 6000)),
        'rules' => is_array($project['rules'] ?? null) ? $project['rules'] : [],
    ];
}

function tkb_save_project(PDO $pdo, array $user, array $input): array
{
    $name = tkb_trim_text($input['name'] ?? 'Thời khóa biểu nhà trường', 180);
    if ($name === '') {
        $name = 'Thời khóa biểu nhà trường';
    }
    $schoolYear = tkb_trim_text($input['school_year'] ?? '', 40);
    $project = tkb_clean_project($input['project'] ?? null);
    $result = is_array($input['result'] ?? null) ? $input['result'] : null;

    $projectJson = json_encode($project, JSON_UNESCAPED_UNICODE);
    $resultJson = $result ? json_encode($result, JSON_UNESCAPED_UNICODE) : null;
    if ($projectJson === false || ($result && $resultJson === false)) {
        throw new RuntimeException('Không mã hóa được dữ liệu thời khóa biểu.');
    }

    $existing = $pdo->prepare('SELECT id FROM timetable_projects WHERE project_key = ? LIMIT 1');
    $existing->execute([TIMETABLE_PROJECT_KEY]);
    $row = $existing->fetch();

    if ($row) {
        $stmt = $pdo->prepare('UPDATE timetable_projects SET name = ?, school_year = ?, project_json = ?, result_json = ?, updated_by = ? WHERE project_key = ?');
        $stmt->execute([$name, $schoolYear, $projectJson, $resultJson, (int)$user['id'], TIMETABLE_PROJECT_KEY]);
    } else {
        $stmt = $pdo->prepare('INSERT INTO timetable_projects (project_key, name, school_year, project_json, result_json, created_by, updated_by) VALUES (?, ?, ?, ?, ?, ?, ?)');
        $stmt->execute([TIMETABLE_PROJECT_KEY, $name, $schoolYear, $projectJson, $resultJson, (int)$user['id'], (int)$user['id']]);
    }

    return tkb_read_project($pdo) ?: [];
}

tkb_maybe_ensure_schema($pdo);
$user = tkb_current_teacher($pdo);
$action = trim((string)($_GET['action'] ?? 'latest'));

if ($action === 'latest') {
    respond([
        'ok' => true,
        'project' => tkb_read_project($pdo),
        'user' => ['name' => $user['full_name'], 'username' => $user['username']],
    ]);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $action === 'save') {
    try {
        $project = tkb_save_project($pdo, $user, json_body());
        respond(['ok' => true, 'project' => $project, 'message' => 'Đã lưu thời khóa biểu lên hosting.']);
    } catch (RuntimeException $e) {
        respond(['error' => $e->getMessage()], 422);
    }
}

respond(['error' => 'Endpoint không tồn tại.'], 404);
