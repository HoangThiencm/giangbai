<?php
require_once __DIR__ . '/helpers.php';

session_start();

// v4: bỏ FOREIGN KEY trong CREATE (tránh 500 trên hosting khi users.id/engine lệch)
const TIMETABLE_SCHEMA_VERSION = '20260709-v4-nofk';

/**
 * Auth TKB: giáo viên có quyền trang thoikhoabieu, hoặc admin/superadmin (quản lý toàn bộ).
 */
function tkb_current_user(PDO $pdo): array
{
    $userId = (int)($_SESSION['user_id'] ?? 0);
    if ($userId <= 0) {
        respond(['error' => 'Vui lòng đăng nhập lại.'], 401);
    }

    $stmt = $pdo->prepare("SELECT id, username, full_name, role, is_active, allowed_pages_json FROM users WHERE id = ? LIMIT 1");
    $stmt->execute([$userId]);
    $user = $stmt->fetch();
    if (!$user || !(bool)$user['is_active']) {
        respond(['error' => 'Tài khoản không hợp lệ hoặc đã bị khóa.'], 403);
    }

    $role = (string)($user['role'] ?? '');
    if ($role === 'admin' || $role === 'superadmin') {
        return $user;
    }

    if ($role !== 'teacher') {
        respond(['error' => 'Chức năng xếp thời khóa biểu chỉ dành cho giáo viên hoặc admin.'], 403);
    }

    $allowedPages = teacher_allowed_pages_resolved($user);
    if (!in_array('thoikhoabieu', $allowedPages, true)) {
        respond(['error' => 'Tài khoản chưa được cấp quyền Xếp thời khóa biểu.'], 403);
    }

    return $user;
}

/** @deprecated alias — giữ tên cũ cho call site */
function tkb_current_teacher(PDO $pdo): array
{
    return tkb_current_user($pdo);
}

function tkb_maybe_ensure_schema(PDO $pdo): void
{
    if (schema_is_ready('thoikhoabieu', TIMETABLE_SCHEMA_VERSION)) {
        return;
    }
    try {
        tkb_ensure_schema($pdo);
        schema_mark_ready('thoikhoabieu', TIMETABLE_SCHEMA_VERSION);
    } catch (Throwable $e) {
        // Không chặn GET nếu bảng đã tồn tại; chỉ fail rõ khi thật sự không tạo được
        if (!tkb_table_exists($pdo, 'timetable_projects')) {
            throw $e;
        }
        // Bảng đã có → đánh dấu ready để tránh lặp 500 mỗi request
        schema_mark_ready('thoikhoabieu', TIMETABLE_SCHEMA_VERSION);
    }
}

function tkb_table_exists(PDO $pdo, string $table): bool
{
    try {
        $stmt = $pdo->prepare('SHOW TABLES LIKE ?');
        $stmt->execute([$table]);
        return (bool)$stmt->fetch();
    } catch (Throwable $e) {
        return false;
    }
}

function tkb_column_exists(PDO $pdo, string $table, string $column): bool
{
    try {
        $stmt = $pdo->prepare("SHOW COLUMNS FROM `{$table}` LIKE ?");
        $stmt->execute([$column]);
        return (bool)$stmt->fetch();
    } catch (Throwable $e) {
        return false;
    }
}

function tkb_ensure_schema(PDO $pdo): void
{
    // Không dùng FOREIGN KEY — nhiều hosting lỗi 150/errno 121 khi users engine/charset khác
    $pdo->exec("CREATE TABLE IF NOT EXISTS timetable_projects (
        id INT AUTO_INCREMENT PRIMARY KEY,
        project_key VARCHAR(80) NOT NULL,
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
        UNIQUE KEY uq_timetable_project_key (project_key),
        INDEX idx_timetable_projects_updated (updated_at),
        INDEX idx_timetable_projects_school_year (school_year),
        INDEX idx_timetable_projects_unit (unit_name),
        INDEX idx_timetable_projects_created_by (created_by)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");

    // Migrate bảng cũ (thiếu cột) — mỗi ALTER độc lập
    $alters = [
        'unit_name' => "ALTER TABLE timetable_projects ADD COLUMN unit_name VARCHAR(180) NOT NULL DEFAULT 'Nhà trường' AFTER project_key",
        'is_locked' => "ALTER TABLE timetable_projects ADD COLUMN is_locked TINYINT(1) NOT NULL DEFAULT 0 AFTER school_year",
        'school_year' => "ALTER TABLE timetable_projects ADD COLUMN school_year VARCHAR(40) NOT NULL DEFAULT '' AFTER name",
        'project_json' => "ALTER TABLE timetable_projects ADD COLUMN project_json LONGTEXT NULL",
        'result_json' => "ALTER TABLE timetable_projects ADD COLUMN result_json LONGTEXT NULL",
    ];
    foreach ($alters as $col => $sql) {
        if (!tkb_column_exists($pdo, 'timetable_projects', $col)) {
            try {
                $pdo->exec($sql);
            } catch (Throwable $e) {
                // bỏ qua nếu đã có / không đủ quyền — request vẫn chạy nếu cột cần thiết đã đủ
            }
        }
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

function tkb_is_admin_user(array $user): bool
{
    $role = (string)($user['role'] ?? '');
    return $role === 'admin' || $role === 'superadmin';
}

/** Chỉ owner (created_by) hoặc admin được xem/sửa đợt. */
function tkb_assert_access(array $user, array $row): void
{
    if (tkb_is_admin_user($user)) {
        return;
    }
    if ((int)($row['created_by'] ?? 0) === (int)($user['id'] ?? 0)) {
        return;
    }
    throw new RuntimeException('Bạn không có quyền truy cập đợt TKB này (chỉ người tạo hoặc admin).');
}

function tkb_list_projects(PDO $pdo, array $user, string $unit = '', string $year = ''): array
{
    $sql = 'SELECT id, project_key, unit_name, name, school_year, is_locked, created_at, updated_at, created_by, updated_by FROM timetable_projects WHERE 1=1';
    $params = [];
    if (!tkb_is_admin_user($user)) {
        $sql .= ' AND created_by = ?';
        $params[] = (int)$user['id'];
    }
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
            'created_by' => (int)$row['created_by'],
            'created_at' => $row['created_at'],
            'updated_at' => $row['updated_at'],
        ];
    }, $rows);
}

function tkb_list_units(PDO $pdo, array $user): array
{
    if (tkb_is_admin_user($user)) {
        $stmt = $pdo->query("SELECT unit_name, COUNT(*) AS batch_count, MAX(updated_at) AS last_updated
            FROM timetable_projects GROUP BY unit_name ORDER BY unit_name ASC");
        $rows = $stmt ? ($stmt->fetchAll() ?: []) : [];
    } else {
        $stmt = $pdo->prepare("SELECT unit_name, COUNT(*) AS batch_count, MAX(updated_at) AS last_updated
            FROM timetable_projects WHERE created_by = ? GROUP BY unit_name ORDER BY unit_name ASC");
        $stmt->execute([(int)$user['id']]);
        $rows = $stmt->fetchAll() ?: [];
    }
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

function tkb_require_project(PDO $pdo, array $user, array $input): array
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
        throw new RuntimeException('Không tìm thấy đợt TKB.');
    }
    tkb_assert_access($user, $row);
    return $row;
}

function tkb_empty_project(): array
{
    return [
        // V1 nghiệp vụ nhà trường (UI Cấu hình)
        'school' => [
            'principal' => '',
            'vicePrincipals' => '',
            'note' => '',
        ],
        'departments' => [],
        'subjects' => [],
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
            'fixedSlots' => '',
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

    $schoolIn = is_array($project['school'] ?? null) ? $project['school'] : [];
    $school = [
        'principal' => tkb_trim_text($schoolIn['principal'] ?? '', 180),
        'vicePrincipals' => tkb_trim_text($schoolIn['vicePrincipals'] ?? '', 500),
        'note' => tkb_trim_text($schoolIn['note'] ?? '', 1000),
    ];

    $rules = is_array($project['rules'] ?? null) ? $project['rules'] : [];
    // Giữ fixedSlots / blockedSlots nếu client gửi (không strip keys lạ trong rules array)
    if (!array_key_exists('fixedSlots', $rules)) {
        $rules['fixedSlots'] = '';
    }

    return [
        'school' => $school,
        'departments' => array_values(array_slice(is_array($project['departments'] ?? null) ? $project['departments'] : [], 0, 200)),
        'subjects' => array_values(array_slice(is_array($project['subjects'] ?? null) ? $project['subjects'] : [], 0, 300)),
        'teachers' => array_values(array_slice(is_array($project['teachers'] ?? null) ? $project['teachers'] : [], 0, 300)),
        'importedAssignments' => array_values(array_slice(is_array($project['importedAssignments'] ?? null) ? $project['importedAssignments'] : [], 0, 3000)),
        'classes' => array_values(array_slice(is_array($project['classes'] ?? null) ? $project['classes'] : [], 0, 200)),
        'rooms' => array_values(array_slice(is_array($project['rooms'] ?? null) ? $project['rooms'] : [], 0, 300)),
        'assignments' => array_values(array_slice(is_array($project['assignments'] ?? null) ? $project['assignments'] : [], 0, 6000)),
        'rules' => $rules,
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
        // Không có đợt → tạo đợt mới thuộc user hiện tại
        return tkb_create_batch($pdo, $user, array_merge($input, [
            'name' => $input['name'] ?? 'Đợt 1',
            'unit_name' => $input['unit_name'] ?? 'Nhà trường',
        ]));
    }

    tkb_assert_access($user, $row);
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
    $row = tkb_require_project($pdo, $user, $input);
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
    $row = tkb_require_project($pdo, $user, $input);

    $stmt = $pdo->prepare('UPDATE timetable_projects SET is_locked = ?, updated_by = ? WHERE id = ?');
    $stmt->execute([$locked ? 1 : 0, (int)$user['id'], (int)$row['id']]);
    return tkb_get_by_id($pdo, (int)$row['id']) ?: [];
}

function tkb_delete_batch(PDO $pdo, array $user, array $input): void
{
    $row = tkb_require_project($pdo, $user, $input);
    tkb_assert_unlocked($row);

    $stmt = $pdo->prepare('DELETE FROM timetable_projects WHERE id = ?');
    $stmt->execute([(int)$row['id']]);
}

function tkb_delete_unit(PDO $pdo, array $user, array $input): int
{
    $unit = tkb_trim_text($input['unit_name'] ?? '', 180);
    if ($unit === '') {
        throw new RuntimeException('Thiếu tên đơn vị.');
    }

    // Chỉ xóa đợt thuộc user (admin: toàn đơn vị)
    if (tkb_is_admin_user($user)) {
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

    $check = $pdo->prepare('SELECT COUNT(*) FROM timetable_projects WHERE unit_name = ? AND created_by = ? AND is_locked = 1');
    $check->execute([$unit, (int)$user['id']]);
    $locked = (int)$check->fetchColumn();
    if ($locked > 0) {
        throw new RuntimeException("Bạn còn {$locked} đợt đang khóa trong đơn vị này. Mở khóa trước khi xóa.");
    }

    $stmt = $pdo->prepare('DELETE FROM timetable_projects WHERE unit_name = ? AND created_by = ?');
    $stmt->execute([$unit, (int)$user['id']]);
    return $stmt->rowCount();
}

function tkb_clear_result(PDO $pdo, array $user, array $input): array
{
    $row = tkb_require_project($pdo, $user, $input);
    tkb_assert_unlocked($row);

    $stmt = $pdo->prepare('UPDATE timetable_projects SET result_json = NULL, updated_by = ? WHERE id = ?');
    $stmt->execute([(int)$user['id'], (int)$row['id']]);
    return tkb_get_by_id($pdo, (int)$row['id']) ?: [];
}

// ---- router ----
try {
    tkb_maybe_ensure_schema($pdo);
    $user = tkb_current_user($pdo);
    $action = trim((string)($_GET['action'] ?? 'list'));
    $method = strtoupper((string)($_SERVER['REQUEST_METHOD'] ?? 'GET'));

    if ($method === 'GET' && $action === 'list') {
        $unit = tkb_trim_text($_GET['unit_name'] ?? '', 180);
        $year = tkb_trim_text($_GET['school_year'] ?? '', 40);
        respond([
            'ok' => true,
            'projects' => tkb_list_projects($pdo, $user, $unit, $year),
            'units' => tkb_list_units($pdo, $user),
            'user' => ['name' => $user['full_name'], 'username' => $user['username'], 'id' => (int)$user['id']],
        ]);
    }

    if ($method === 'GET' && ($action === 'latest' || $action === 'get')) {
        $key = tkb_trim_text($_GET['project_key'] ?? '', 80);
        $id = (int)($_GET['id'] ?? 0);
        $project = null;
        try {
            if ($id > 0) {
                $project = tkb_get_by_id($pdo, $id);
                if ($project) {
                    tkb_assert_access($user, $project);
                }
            } elseif ($key !== '') {
                $project = tkb_get_by_key($pdo, $key);
                if ($project) {
                    tkb_assert_access($user, $project);
                }
            } else {
                $list = tkb_list_projects($pdo, $user);
                if ($list) {
                    $project = tkb_get_by_key($pdo, $list[0]['project_key']);
                }
            }
        } catch (RuntimeException $e) {
            // Không có quyền / không tìm thấy → trả null, không lộ dữ liệu
            $project = null;
        }
        respond([
            'ok' => true,
            'project' => $project,
            'projects' => tkb_list_projects($pdo, $user),
            'units' => tkb_list_units($pdo, $user),
            'user' => ['name' => $user['full_name'], 'username' => $user['username'], 'id' => (int)$user['id']],
        ]);
    }

    if ($method === 'POST') {
        $body = json_body();
        try {
            if ($action === 'create') {
                $project = tkb_create_batch($pdo, $user, $body);
                respond(['ok' => true, 'project' => $project, 'message' => 'Đã tạo đợt xếp TKB.', 'projects' => tkb_list_projects($pdo, $user), 'units' => tkb_list_units($pdo, $user)]);
            }
            if ($action === 'save') {
                $project = tkb_save_batch($pdo, $user, $body);
                respond(['ok' => true, 'project' => $project, 'message' => 'Đã lưu thời khóa biểu.', 'projects' => tkb_list_projects($pdo, $user), 'units' => tkb_list_units($pdo, $user)]);
            }
            if ($action === 'update_meta') {
                $project = tkb_update_meta($pdo, $user, $body);
                respond(['ok' => true, 'project' => $project, 'message' => 'Đã cập nhật thông tin đợt.', 'projects' => tkb_list_projects($pdo, $user), 'units' => tkb_list_units($pdo, $user)]);
            }
            if ($action === 'lock') {
                $project = tkb_set_lock($pdo, $user, $body, true);
                respond(['ok' => true, 'project' => $project, 'message' => 'Đã khóa đợt TKB.', 'projects' => tkb_list_projects($pdo, $user)]);
            }
            if ($action === 'unlock') {
                $project = tkb_set_lock($pdo, $user, $body, false);
                respond(['ok' => true, 'project' => $project, 'message' => 'Đã mở khóa đợt TKB.', 'projects' => tkb_list_projects($pdo, $user)]);
            }
            if ($action === 'delete') {
                tkb_delete_batch($pdo, $user, $body);
                respond(['ok' => true, 'message' => 'Đã xóa đợt TKB.', 'projects' => tkb_list_projects($pdo, $user), 'units' => tkb_list_units($pdo, $user)]);
            }
            if ($action === 'delete_unit') {
                $count = tkb_delete_unit($pdo, $user, $body);
                respond(['ok' => true, 'message' => "Đã xóa {$count} đợt TKB của đơn vị.", 'deleted' => $count, 'projects' => tkb_list_projects($pdo, $user), 'units' => tkb_list_units($pdo, $user)]);
            }
            if ($action === 'clear_result') {
                $project = tkb_clear_result($pdo, $user, $body);
                respond(['ok' => true, 'project' => $project, 'message' => 'Đã xóa kết quả xếp (giữ nguyên dữ liệu đầu vào).', 'projects' => tkb_list_projects($pdo, $user)]);
            }
        } catch (RuntimeException $e) {
            respond(['error' => $e->getMessage()], 422);
        }
    }

    respond(['error' => 'Endpoint không tồn tại.'], 404);
} catch (Throwable $e) {
    // Tránh 500 HTML trắng — trả JSON để UI/console đọc được
    $msg = $e->getMessage();
    if ($msg === '') {
        $msg = 'Lỗi máy chủ TKB.';
    }
    respond([
        'error' => $msg,
        'hint' => 'Kiểm tra bảng timetable_projects, session đăng nhập, quyền trang thoikhoabieu. Deploy api/thoikhoabieu.php bản mới nhất.',
    ], 500);
}
