<?php
require_once __DIR__ . '/helpers.php';

session_start();

const TIMETABLE_SCHEMA_VERSION = '20260709-v2';

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

function tkb_column_exists(PDO $pdo, string $table, string $column): bool
{
    $stmt = $pdo->prepare("SHOW COLUMNS FROM `{$table}` LIKE ?");
    $stmt->execute([$column]);
    return (bool)$stmt->fetch();
}

function tkb_ensure_schema(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS timetable_projects (
        id INT AUTO_INCREMENT PRIMARY KEY,
        project_key VARCHAR(80) NOT NULL UNIQUE,
        unit_name VARCHAR(180) NOT NULL DEFAULT 'Nhà trường',
        name VARCHAR(180) NOT NULL DEFAULT 'Đợt xếp TKB',
        school_year VARCHAR(40) NOT NULL DEFAULT '',
        is_locked TINYINT(1) NOT NULL DEFAULT 0,
        project_json LONGTEXT NOT NULL,
        result_json LONGTEXT DEFAULT NULL,
        created_by INT NOT NULL,
        updated_by INT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_timetable_projects_updated (updated_at),
        INDEX idx_timetable_projects_school_year (school_year),
        INDEX idx_timetable_projects_unit (unit_name),
        CONSTRAINT fk_timetable_project_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
        CONSTRAINT fk_timetable_project_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE CASCADE
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    // Migrate bảng cũ (thiếu cột)
    if (!tkb_column_exists($pdo, 'timetable_projects', 'unit_name')) {
        $pdo->exec("ALTER TABLE timetable_projects ADD COLUMN unit_name VARCHAR(180) NOT NULL DEFAULT 'Nhà trường' AFTER project_key");
    }
    if (!tkb_column_exists($pdo, 'timetable_projects', 'is_locked')) {
        $pdo->exec("ALTER TABLE timetable_projects ADD COLUMN is_locked TINYINT(1) NOT NULL DEFAULT 0 AFTER school_year");
    }
}

function tkb_trim_text($value, int $limit): string
{
    $text = trim((string)$value);
    return function_exists('mb_substr') ? mb_substr($text, 0, $limit) : substr($text, 0, $limit);
}

function tkb_slug(string $text): string
{
    $s = strtolower(trim($text));
    $s = preg_replace('/[^a-z0-9]+/i', '-', $s) ?: 'batch';
    $s = trim($s, '-');
    if ($s === '') {
        $s = 'batch';
    }
    return function_exists('mb_substr') ? mb_substr($s, 0, 48) : substr($s, 0, 48);
}

function tkb_project_payload(?array $row): ?array
{
    if (!$row) {
        return null;
    }

    return [
        'id' => (int)$row['id'],
        'project_key' => $row['project_key'],
        'unit_name' => $row['unit_name'] ?? 'Nhà trường',
        'name' => $row['name'],
        'school_year' => $row['school_year'],
        'is_locked' => (bool)($row['is_locked'] ?? 0),
        'project' => json_decode((string)$row['project_json'], true) ?: null,
        'result' => $row['result_json'] ? (json_decode((string)$row['result_json'], true) ?: null) : null,
        'created_at' => $row['created_at'],
        'updated_at' => $row['updated_at'],
        'created_by' => (int)$row['created_by'],
        'updated_by' => (int)$row['updated_by'],
    ];
}

function tkb_list_projects(PDO $pdo, string $unit = '', string $year = ''): array
{
    $sql = 'SELECT id, project_key, unit_name, name, school_year, is_locked, created_at, updated_at, created_by, updated_by FROM timetable_projects WHERE 1=1';
    $params = [];
    if ($unit !== '') {
        $sql .= ' AND unit_name = ?';
        $params[] = $unit;
    }
    if ($year !== '') {
        $sql .= ' AND school_year = ?';
        $params[] = $year;
    }
    $sql .= ' ORDER BY unit_name ASC, school_year DESC, updated_at DESC';
    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $rows = $stmt->fetchAll() ?: [];
    return array_map(static function ($row) {
        return [
            'id' => (int)$row['id'],
            'project_key' => $row['project_key'],
            'unit_name' => $row['unit_name'] ?? 'Nhà trường',
            'name' => $row['name'],
            'school_year' => $row['school_year'],
            'is_locked' => (bool)($row['is_locked'] ?? 0),
            'created_at' => $row['created_at'],
            'updated_at' => $row['updated_at'],
        ];
    }, $rows);
}

function tkb_list_units(PDO $pdo): array
{
    $stmt = $pdo->query("SELECT unit_name, COUNT(*) AS batch_count, MAX(updated_at) AS last_updated
        FROM timetable_projects GROUP BY unit_name ORDER BY unit_name ASC");
    $rows = $stmt ? ($stmt->fetchAll() ?: []) : [];
    return array_map(static function ($row) {
        return [
            'unit_name' => $row['unit_name'] ?: 'Nhà trường',
            'batch_count' => (int)$row['batch_count'],
            'last_updated' => $row['last_updated'],
        ];
    }, $rows);
}

function tkb_get_by_key(PDO $pdo, string $key): ?array
{
    $stmt = $pdo->prepare('SELECT * FROM timetable_projects WHERE project_key = ? LIMIT 1');
    $stmt->execute([$key]);
    $row = $stmt->fetch();
    return tkb_project_payload($row ?: null);
}

function tkb_get_by_id(PDO $pdo, int $id): ?array
{
    $stmt = $pdo->prepare('SELECT * FROM timetable_projects WHERE id = ? LIMIT 1');
    $stmt->execute([$id]);
    $row = $stmt->fetch();
    return tkb_project_payload($row ?: null);
}

function tkb_assert_unlocked(array $row): void
{
    if (!empty($row['is_locked'])) {
        throw new RuntimeException('Đợt xếp TKB này đang bị khóa. Mở khóa trước khi sửa/xóa/xếp lại.');
    }
}

function tkb_empty_project(): array
{
    return [
        'teachers' => [],
        'importedAssignments' => [],
        'classes' => [],
        'rooms' => [],
        'assignments' => [],
        'rules' => [
            'morningPeriods' => 5,
            'afternoonPeriods' => 4,
            'morningFrom' => 1,
            'morningTo' => 5,
            'afternoonFrom' => 1,
            'afternoonTo' => 4,
            'packFromSessionStart' => true,
            'blockedSlots' => '',
            'days' => ['T2', 'T3', 'T4', 'T5', 'T6', 'T7'],
            'maxSameSubjectDay' => 2,
        ],
    ];
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

function tkb_unique_key(PDO $pdo, string $base): string
{
    $key = tkb_slug($base);
    if ($key === '') {
        $key = 'batch';
    }
    $candidate = $key;
    $i = 1;
    while (true) {
        $stmt = $pdo->prepare('SELECT id FROM timetable_projects WHERE project_key = ? LIMIT 1');
        $stmt->execute([$candidate]);
        if (!$stmt->fetch()) {
            return $candidate;
        }
        $i++;
        $candidate = $key . '-' . $i;
        if ($i > 200) {
            return $key . '-' . bin2hex(random_bytes(3));
        }
    }
}

function tkb_create_batch(PDO $pdo, array $user, array $input): array
{
    $unit = tkb_trim_text($input['unit_name'] ?? 'Nhà trường', 180);
    if ($unit === '') {
        $unit = 'Nhà trường';
    }
    $name = tkb_trim_text($input['name'] ?? 'Đợt 1', 180);
    if ($name === '') {
        $name = 'Đợt 1';
    }
    $schoolYear = tkb_trim_text($input['school_year'] ?? '', 40);
    $projectKey = tkb_trim_text($input['project_key'] ?? '', 80);
    if ($projectKey === '') {
        $projectKey = tkb_unique_key($pdo, $unit . '-' . $schoolYear . '-' . $name);
    } else {
        $projectKey = tkb_unique_key($pdo, tkb_slug($projectKey));
    }

    $project = tkb_clean_project($input['project'] ?? tkb_empty_project());
    $projectJson = json_encode($project, JSON_UNESCAPED_UNICODE);
    if ($projectJson === false) {
        throw new RuntimeException('Không mã hóa được dữ liệu.');
    }

    $stmt = $pdo->prepare('INSERT INTO timetable_projects (project_key, unit_name, name, school_year, is_locked, project_json, result_json, created_by, updated_by) VALUES (?, ?, ?, ?, 0, ?, NULL, ?, ?)');
    $stmt->execute([
        $projectKey,
        $unit,
        $name,
        $schoolYear,
        $projectJson,
        (int)$user['id'],
        (int)$user['id'],
    ]);

    $created = tkb_get_by_key($pdo, $projectKey);
    if (!$created) {
        throw new RuntimeException('Tạo đợt thất bại.');
    }
    return $created;
}

function tkb_save_batch(PDO $pdo, array $user, array $input): array
{
    $id = (int)($input['id'] ?? 0);
    $key = tkb_trim_text($input['project_key'] ?? '', 80);
    $row = null;
    if ($id > 0) {
        $row = tkb_get_by_id($pdo, $id);
    } elseif ($key !== '') {
        $row = tkb_get_by_key($pdo, $key);
    }
    if (!$row) {
        // Tương thích cũ: nếu không chỉ định thì tạo/ghi school_default
        $legacy = tkb_get_by_key($pdo, 'school_default');
        if ($legacy) {
            $row = $legacy;
        } else {
            return tkb_create_batch($pdo, $user, array_merge($input, [
                'project_key' => 'school_default',
                'name' => $input['name'] ?? 'Đợt mặc định',
                'unit_name' => $input['unit_name'] ?? 'Nhà trường',
            ]));
        }
    }

    tkb_assert_unlocked($row);

    $unit = tkb_trim_text($input['unit_name'] ?? $row['unit_name'], 180);
    if ($unit === '') {
        $unit = 'Nhà trường';
    }
    $name = tkb_trim_text($input['name'] ?? $row['name'], 180);
    if ($name === '') {
        $name = 'Đợt xếp TKB';
    }
    $schoolYear = tkb_trim_text($input['school_year'] ?? $row['school_year'], 40);
    $project = tkb_clean_project($input['project'] ?? $row['project'] ?? tkb_empty_project());
    $result = array_key_exists('result', $input)
        ? (is_array($input['result']) ? $input['result'] : null)
        : $row['result'];

    $projectJson = json_encode($project, JSON_UNESCAPED_UNICODE);
    $resultJson = $result ? json_encode($result, JSON_UNESCAPED_UNICODE) : null;
    if ($projectJson === false || ($result && $resultJson === false)) {
        throw new RuntimeException('Không mã hóa được dữ liệu thời khóa biểu.');
    }

    $stmt = $pdo->prepare('UPDATE timetable_projects SET unit_name = ?, name = ?, school_year = ?, project_json = ?, result_json = ?, updated_by = ? WHERE id = ?');
    $stmt->execute([$unit, $name, $schoolYear, $projectJson, $resultJson, (int)$user['id'], (int)$row['id']]);

    return tkb_get_by_id($pdo, (int)$row['id']) ?: [];
}

function tkb_update_meta(PDO $pdo, array $user, array $input): array
{
    $id = (int)($input['id'] ?? 0);
    $row = $id > 0 ? tkb_get_by_id($pdo, $id) : null;
    if (!$row && !empty($input['project_key'])) {
        $row = tkb_get_by_key($pdo, tkb_trim_text($input['project_key'], 80));
    }
    if (!$row) {
        throw new RuntimeException('Không tìm thấy đợt TKB.');
    }
    tkb_assert_unlocked($row);

    $unit = tkb_trim_text($input['unit_name'] ?? $row['unit_name'], 180);
    $name = tkb_trim_text($input['name'] ?? $row['name'], 180);
    $schoolYear = tkb_trim_text($input['school_year'] ?? $row['school_year'], 40);
    if ($unit === '') {
        $unit = 'Nhà trường';
    }
    if ($name === '') {
        $name = 'Đợt xếp TKB';
    }

    $stmt = $pdo->prepare('UPDATE timetable_projects SET unit_name = ?, name = ?, school_year = ?, updated_by = ? WHERE id = ?');
    $stmt->execute([$unit, $name, $schoolYear, (int)$user['id'], (int)$row['id']]);
    return tkb_get_by_id($pdo, (int)$row['id']) ?: [];
}

function tkb_set_lock(PDO $pdo, array $user, array $input, bool $locked): array
{
    $id = (int)($input['id'] ?? 0);
    $row = $id > 0 ? tkb_get_by_id($pdo, $id) : null;
    if (!$row && !empty($input['project_key'])) {
        $row = tkb_get_by_key($pdo, tkb_trim_text($input['project_key'], 80));
    }
    if (!$row) {
        throw new RuntimeException('Không tìm thấy đợt TKB.');
    }

    $stmt = $pdo->prepare('UPDATE timetable_projects SET is_locked = ?, updated_by = ? WHERE id = ?');
    $stmt->execute([$locked ? 1 : 0, (int)$user['id'], (int)$row['id']]);
    return tkb_get_by_id($pdo, (int)$row['id']) ?: [];
}

function tkb_delete_batch(PDO $pdo, array $input): void
{
    $id = (int)($input['id'] ?? 0);
    $row = $id > 0 ? tkb_get_by_id($pdo, $id) : null;
    if (!$row && !empty($input['project_key'])) {
        $row = tkb_get_by_key($pdo, tkb_trim_text($input['project_key'], 80));
    }
    if (!$row) {
        throw new RuntimeException('Không tìm thấy đợt TKB.');
    }
    tkb_assert_unlocked($row);

    $stmt = $pdo->prepare('DELETE FROM timetable_projects WHERE id = ?');
    $stmt->execute([(int)$row['id']]);
}

function tkb_delete_unit(PDO $pdo, array $input): int
{
    $unit = tkb_trim_text($input['unit_name'] ?? '', 180);
    if ($unit === '') {
        throw new RuntimeException('Thiếu tên đơn vị.');
    }

    // Không xóa đợt đang khóa
    $check = $pdo->prepare('SELECT COUNT(*) FROM timetable_projects WHERE unit_name = ? AND is_locked = 1');
    $check->execute([$unit]);
    $locked = (int)$check->fetchColumn();
    if ($locked > 0) {
        throw new RuntimeException("Đơn vị còn {$locked} đợt đang khóa. Mở khóa hết trước khi xóa toàn bộ.");
    }

    $stmt = $pdo->prepare('DELETE FROM timetable_projects WHERE unit_name = ?');
    $stmt->execute([$unit]);
    return $stmt->rowCount();
}

function tkb_clear_result(PDO $pdo, array $user, array $input): array
{
    $id = (int)($input['id'] ?? 0);
    $row = $id > 0 ? tkb_get_by_id($pdo, $id) : null;
    if (!$row && !empty($input['project_key'])) {
        $row = tkb_get_by_key($pdo, tkb_trim_text($input['project_key'], 80));
    }
    if (!$row) {
        throw new RuntimeException('Không tìm thấy đợt TKB.');
    }
    tkb_assert_unlocked($row);

    $stmt = $pdo->prepare('UPDATE timetable_projects SET result_json = NULL, updated_by = ? WHERE id = ?');
    $stmt->execute([(int)$user['id'], (int)$row['id']]);
    return tkb_get_by_id($pdo, (int)$row['id']) ?: [];
}

// ---- router ----
tkb_maybe_ensure_schema($pdo);
$user = tkb_current_teacher($pdo);
$action = trim((string)($_GET['action'] ?? 'list'));
$method = strtoupper((string)($_SERVER['REQUEST_METHOD'] ?? 'GET'));

if ($method === 'GET' && $action === 'list') {
    $unit = tkb_trim_text($_GET['unit_name'] ?? '', 180);
    $year = tkb_trim_text($_GET['school_year'] ?? '', 40);
    respond([
        'ok' => true,
        'projects' => tkb_list_projects($pdo, $unit, $year),
        'units' => tkb_list_units($pdo),
        'user' => ['name' => $user['full_name'], 'username' => $user['username']],
    ]);
}

if ($method === 'GET' && ($action === 'latest' || $action === 'get')) {
    $key = tkb_trim_text($_GET['project_key'] ?? '', 80);
    $id = (int)($_GET['id'] ?? 0);
    $project = null;
    if ($id > 0) {
        $project = tkb_get_by_id($pdo, $id);
    } elseif ($key !== '') {
        $project = tkb_get_by_key($pdo, $key);
    } else {
        // Ưu tiên đợt cập nhật gần nhất; fallback school_default
        $list = tkb_list_projects($pdo);
        if ($list) {
            $project = tkb_get_by_key($pdo, $list[0]['project_key']);
        } else {
            $project = tkb_get_by_key($pdo, 'school_default');
        }
    }
    respond([
        'ok' => true,
        'project' => $project,
        'projects' => tkb_list_projects($pdo),
        'units' => tkb_list_units($pdo),
        'user' => ['name' => $user['full_name'], 'username' => $user['username']],
    ]);
}

if ($method === 'POST') {
    $body = json_body();
    try {
        if ($action === 'create') {
            $project = tkb_create_batch($pdo, $user, $body);
            respond(['ok' => true, 'project' => $project, 'message' => 'Đã tạo đợt xếp TKB.', 'projects' => tkb_list_projects($pdo), 'units' => tkb_list_units($pdo)]);
        }
        if ($action === 'save') {
            $project = tkb_save_batch($pdo, $user, $body);
            respond(['ok' => true, 'project' => $project, 'message' => 'Đã lưu thời khóa biểu.', 'projects' => tkb_list_projects($pdo), 'units' => tkb_list_units($pdo)]);
        }
        if ($action === 'update_meta') {
            $project = tkb_update_meta($pdo, $user, $body);
            respond(['ok' => true, 'project' => $project, 'message' => 'Đã cập nhật thông tin đợt.', 'projects' => tkb_list_projects($pdo), 'units' => tkb_list_units($pdo)]);
        }
        if ($action === 'lock') {
            $project = tkb_set_lock($pdo, $user, $body, true);
            respond(['ok' => true, 'project' => $project, 'message' => 'Đã khóa đợt TKB.', 'projects' => tkb_list_projects($pdo)]);
        }
        if ($action === 'unlock') {
            $project = tkb_set_lock($pdo, $user, $body, false);
            respond(['ok' => true, 'project' => $project, 'message' => 'Đã mở khóa đợt TKB.', 'projects' => tkb_list_projects($pdo)]);
        }
        if ($action === 'delete') {
            tkb_delete_batch($pdo, $body);
            respond(['ok' => true, 'message' => 'Đã xóa đợt TKB.', 'projects' => tkb_list_projects($pdo), 'units' => tkb_list_units($pdo)]);
        }
        if ($action === 'delete_unit') {
            $count = tkb_delete_unit($pdo, $body);
            respond(['ok' => true, 'message' => "Đã xóa {$count} đợt TKB của đơn vị.", 'deleted' => $count, 'projects' => tkb_list_projects($pdo), 'units' => tkb_list_units($pdo)]);
        }
        if ($action === 'clear_result') {
            $project = tkb_clear_result($pdo, $user, $body);
            respond(['ok' => true, 'project' => $project, 'message' => 'Đã xóa kết quả xếp (giữ nguyên dữ liệu đầu vào).', 'projects' => tkb_list_projects($pdo)]);
        }
    } catch (RuntimeException $e) {
        respond(['error' => $e->getMessage()], 422);
    }
}

respond(['error' => 'Endpoint không tồn tại.'], 404);
