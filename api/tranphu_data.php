<?php
require_once __DIR__ . '/helpers.php';

/** Shared reference lists declared by Admin.
 * Teachers pick a list when creating a submission/reporting campaign.
 */

function tranphu_system_list_codes(): array
{
    return ['school', 'teachers', 'party'];
}

function tranphu_default_fields_json(): string
{
    return json_encode([
        ['key' => 'full_name', 'label' => 'Họ và tên', 'required' => true],
        ['key' => 'group_name', 'label' => 'Tổ/đơn vị hoặc lớp', 'required' => false],
        ['key' => 'role_label', 'label' => 'Chức vụ/Vai trò', 'required' => false],
        ['key' => 'contact', 'label' => 'Email/SĐT', 'required' => false],
    ], JSON_UNESCAPED_UNICODE);
}

function tranphu_slug_code(string $title): string
{
    $value = $title;
    if (function_exists('iconv')) {
        $converted = @iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE', $title);
        if (is_string($converted) && $converted !== '') $value = $converted;
    }
    $slug = trim(preg_replace('/[^a-z0-9]+/', '_', strtolower($value)), '_');
    return $slug !== '' ? substr($slug, 0, 32) : 'danh_sach';
}

function tranphu_unique_list_code(PDO $pdo, string $title, string $preferred = ''): string
{
    $base = $preferred !== '' ? preg_replace('/[^a-z0-9_]+/', '', strtolower($preferred)) : tranphu_slug_code($title);
    if ($base === '') $base = 'danh_sach';
    $code = substr($base, 0, 36);
    $suffix = 0;
    while (tranphu_list($pdo, $code)) {
        $suffix++;
        $code = substr($base, 0, 30) . '_' . $suffix;
    }
    return $code;
}

function tranphu_schema(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS school_reference_lists (
        id INT AUTO_INCREMENT PRIMARY KEY,
        list_code VARCHAR(40) NOT NULL UNIQUE,
        title VARCHAR(160) NOT NULL,
        fields_json LONGTEXT DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    $pdo->exec("CREATE TABLE IF NOT EXISTS school_reference_people (
        id INT AUTO_INCREMENT PRIMARY KEY,
        list_id INT NOT NULL,
        full_name VARCHAR(180) NOT NULL,
        group_name VARCHAR(180) DEFAULT NULL,
        role_label VARCHAR(160) DEFAULT NULL,
        contact VARCHAR(180) DEFAULT NULL,
        data_json LONGTEXT DEFAULT NULL,
        source_row INT DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_reference_person (list_id, full_name, group_name),
        INDEX idx_reference_people_list (list_id),
        CONSTRAINT fk_reference_people_list FOREIGN KEY (list_id) REFERENCES school_reference_lists(id) ON DELETE CASCADE
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    $schoolFields = json_encode([
        ['key' => 'full_name', 'label' => 'Họ và tên', 'required' => true],
        ['key' => 'role_label', 'label' => 'Chức vụ', 'required' => false],
    ], JSON_UNESCAPED_UNICODE);
    $homeroomTeacherFields = json_encode([
        ['key' => 'full_name', 'label' => 'Họ và tên', 'required' => true],
        ['key' => 'group_name', 'label' => 'Lớp chủ nhiệm', 'required' => false],
    ], JSON_UNESCAPED_UNICODE);
    $partyFields = json_encode([
        ['key' => 'full_name', 'label' => 'Họ tên', 'required' => true],
        ['key' => 'role_label', 'label' => 'Ghi chú / Chức vụ', 'required' => false],
    ], JSON_UNESCAPED_UNICODE);
    $defaults = [
        ['school', 'Toàn trường', $schoolFields],
        ['teachers', 'Danh sách giáo viên chủ nhiệm', $homeroomTeacherFields],
        ['party', 'Danh sách đảng viên', $partyFields],
    ];
    $stmt = $pdo->prepare('INSERT IGNORE INTO school_reference_lists (list_code, title, fields_json) VALUES (?, ?, ?)');
    foreach ($defaults as [$code, $title, $fields]) $stmt->execute([$code, $title, $fields]);
    // The party-member list has a deliberately smaller two-column template.
    $pdo->prepare('UPDATE school_reference_lists SET title = ?, fields_json = ? WHERE list_code = ?')->execute(['Toàn trường', $schoolFields, 'school']);
    $pdo->prepare('UPDATE school_reference_lists SET title = ?, fields_json = ? WHERE list_code = ?')->execute(['Danh sách giáo viên chủ nhiệm', $homeroomTeacherFields, 'teachers']);
    $pdo->prepare('UPDATE school_reference_lists SET fields_json = ? WHERE list_code = ?')->execute([$partyFields, 'party']);
}

function tranphu_admin(): bool
{
    $key = $_SERVER['HTTP_X_ADMIN_KEY'] ?? ($_GET['admin_key'] ?? '');
    return defined('ADMIN_KEY') && is_string($key) && hash_equals(ADMIN_KEY, $key);
}

function tranphu_current_teacher(PDO $pdo): ?array
{
    if (empty($_SESSION['user_id'])) return null;
    $stmt = $pdo->prepare("SELECT * FROM users WHERE id = ? AND role = 'teacher' AND is_active = 1 LIMIT 1");
    $stmt->execute([(int)$_SESSION['user_id']]);
    return $stmt->fetch() ?: null;
}

function tranphu_require_reader(PDO $pdo): void
{
    if (tranphu_admin() || tranphu_current_teacher($pdo)) return;
    respond(['error' => 'Cần đăng nhập giáo viên hoặc Admin Key để xem danh sách trường.'], 401);
}

function tranphu_require_admin(): void
{
    if (!tranphu_admin()) respond(['error' => 'Sai Admin Key hoặc không có quyền quản trị.'], 401);
}

function tranphu_list(PDO $pdo, string $code): ?array
{
    $stmt = $pdo->prepare('SELECT * FROM school_reference_lists WHERE list_code = ? LIMIT 1');
    $stmt->execute([$code]);
    return $stmt->fetch() ?: null;
}

function tranphu_normalize_header(string $value): string
{
    if (function_exists('iconv')) {
        $converted = @iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE', $value);
        if (is_string($converted)) $value = $converted;
    }
    return strtolower(trim(preg_replace('/[^a-zA-Z0-9]+/', ' ', $value)));
}

function tranphu_normalize_rows($rows): array
{
    if (!is_array($rows)) return [];
    $clean = [];
    $seen = [];
    foreach (array_slice($rows, 0, 5000) as $rowIndex => $row) {
        if (!is_array($row)) continue;
        $fullName = trim((string)($row['full_name'] ?? $row['name'] ?? ''));
        if ($fullName === '') continue;
        $group = trim((string)($row['group_name'] ?? $row['group'] ?? ''));
        $role = trim((string)($row['role_label'] ?? $row['role'] ?? ''));
        $contact = trim((string)($row['contact'] ?? ''));
        $key = function_exists('mb_strtolower') ? mb_strtolower($fullName . '|' . $group, 'UTF-8') : strtolower($fullName . '|' . $group);
        if (isset($seen[$key])) continue;
        $seen[$key] = true;
        $extra = is_array($row['extra'] ?? null) ? $row['extra'] : [];
        $clean[] = [
            'full_name' => function_exists('mb_substr') ? mb_substr($fullName, 0, 180) : substr($fullName, 0, 180),
            'group_name' => $group !== '' ? (function_exists('mb_substr') ? mb_substr($group, 0, 180) : substr($group, 0, 180)) : null,
            'role_label' => $role !== '' ? (function_exists('mb_substr') ? mb_substr($role, 0, 160) : substr($role, 0, 160)) : null,
            'contact' => $contact !== '' ? (function_exists('mb_substr') ? mb_substr($contact, 0, 180) : substr($contact, 0, 180)) : null,
            'extra' => $extra,
            'source_row' => (int)($row['source_row'] ?? ($rowIndex + 2)),
        ];
    }
    return $clean;
}

tranphu_schema($pdo);
$method = $_SERVER['REQUEST_METHOD'];
$action = trim((string)($_GET['action'] ?? 'options'));

if ($method === 'GET' && $action === 'options') {
    tranphu_require_reader($pdo);
    $systemCodes = tranphu_system_list_codes();
    $rows = $pdo->query("SELECT l.id, l.list_code, l.title, l.fields_json, COUNT(p.id) AS people_count
        FROM school_reference_lists l LEFT JOIN school_reference_people p ON p.list_id = l.id
        GROUP BY l.id ORDER BY FIELD(l.list_code, 'school', 'teachers', 'party'), l.created_at, l.title")->fetchAll();
    foreach ($rows as &$row) {
        $row['id'] = (int)$row['id'];
        $row['people_count'] = (int)$row['people_count'];
        $row['fields'] = json_decode((string)$row['fields_json'], true) ?: [];
        $row['is_system'] = in_array((string)$row['list_code'], $systemCodes, true);
        unset($row['fields_json']);
    }
    respond(['ok' => true, 'lists' => $rows]);
}

if ($method === 'GET' && $action === 'people') {
    tranphu_require_reader($pdo);
    $code = trim((string)($_GET['list'] ?? ''));
    $list = tranphu_list($pdo, $code);
    if (!$list) respond(['error' => 'Không tìm thấy danh sách.'], 404);
    $stmt = $pdo->prepare('SELECT id, full_name, group_name, role_label, contact, data_json FROM school_reference_people WHERE list_id = ? ORDER BY group_name, full_name');
    $stmt->execute([(int)$list['id']]);
    $people = $stmt->fetchAll();
    foreach ($people as &$person) {
        $person['id'] = (int)$person['id'];
        $person['extra'] = json_decode((string)$person['data_json'], true) ?: [];
        unset($person['data_json']);
    }
    respond(['ok' => true, 'list' => ['code' => $list['list_code'], 'title' => $list['title']], 'people' => $people]);
}

if ($method === 'POST' && $action === 'import') {
    tranphu_require_admin();
    $data = json_body();
    $code = trim((string)($data['list_code'] ?? ''));
    $list = tranphu_list($pdo, $code);
    if (!$list) respond(['error' => 'Danh sách không hợp lệ.'], 422);
    $rows = tranphu_normalize_rows($data['rows'] ?? []);
    if (!$rows) respond(['error' => 'Không đọc được dòng dữ liệu hợp lệ. Cần có cột Họ và tên.'], 422);
    $pdo->beginTransaction();
    try {
        $pdo->prepare('DELETE FROM school_reference_people WHERE list_id = ?')->execute([(int)$list['id']]);
        $insert = $pdo->prepare('INSERT INTO school_reference_people (list_id, full_name, group_name, role_label, contact, data_json, source_row) VALUES (?, ?, ?, ?, ?, ?, ?)');
        foreach ($rows as $row) {
            $insert->execute([(int)$list['id'], $row['full_name'], $row['group_name'], $row['role_label'], $row['contact'], json_encode($row['extra'], JSON_UNESCAPED_UNICODE), $row['source_row']]);
        }
        $pdo->commit();
    } catch (Throwable $e) {
        if ($pdo->inTransaction()) $pdo->rollBack();
        throw $e;
    }
    respond(['ok' => true, 'count' => count($rows), 'message' => 'Đã thay thế danh sách bằng ' . count($rows) . ' dòng dữ liệu.']);
}

if ($method === 'POST' && $action === 'clear') {
    tranphu_require_admin();
    $data = json_body();
    $list = tranphu_list($pdo, trim((string)($data['list_code'] ?? '')));
    if (!$list) respond(['error' => 'Danh sách không hợp lệ.'], 422);
    $stmt = $pdo->prepare('DELETE FROM school_reference_people WHERE list_id = ?');
    $stmt->execute([(int)$list['id']]);
    respond(['ok' => true, 'count' => $stmt->rowCount()]);
}

if ($method === 'POST' && $action === 'create-list') {
    tranphu_require_admin();
    $data = json_body();
    $title = trim((string)($data['title'] ?? ''));
    if ($title === '') respond(['error' => 'Vui lòng nhập tên danh sách.'], 422);
    $preferred = trim((string)($data['list_code'] ?? ''));
    $code = tranphu_unique_list_code($pdo, $title, $preferred);
    $fields = tranphu_default_fields_json();
    $stmt = $pdo->prepare('INSERT INTO school_reference_lists (list_code, title, fields_json) VALUES (?, ?, ?)');
    $stmt->execute([$code, function_exists('mb_substr') ? mb_substr($title, 0, 160) : substr($title, 0, 160), $fields]);
    $list = tranphu_list($pdo, $code);
    respond([
        'ok' => true,
        'message' => 'Đã tạo danh sách báo cáo mới.',
        'list' => [
            'id' => (int)$list['id'],
            'list_code' => $list['list_code'],
            'title' => $list['title'],
            'people_count' => 0,
            'is_system' => false,
            'fields' => json_decode((string)$list['fields_json'], true) ?: [],
        ],
    ]);
}

if ($method === 'POST' && $action === 'delete-list') {
    tranphu_require_admin();
    $data = json_body();
    $code = trim((string)($data['list_code'] ?? ''));
    $list = tranphu_list($pdo, $code);
    if (!$list) respond(['error' => 'Danh sách không hợp lệ.'], 422);
    if (in_array($code, tranphu_system_list_codes(), true)) {
        respond(['error' => 'Không thể xóa danh mục hệ thống. Chỉ xóa dữ liệu bên trong.'], 422);
    }
    $used = $pdo->prepare("SELECT COUNT(*) FROM submission_assignments WHERE source_list_code = ?");
    $used->execute([$code]);
    if ((int)$used->fetchColumn() > 0) {
        respond(['error' => 'Danh sách đang được dùng bởi một hoặc nhiều đợt nộp. Hãy đổi danh sách của các đợt đó trước.'], 409);
    }
    $pdo->prepare('DELETE FROM school_reference_lists WHERE id = ?')->execute([(int)$list['id']]);
    respond(['ok' => true, 'message' => 'Đã xóa danh sách.']);
}

respond(['error' => 'Endpoint không tồn tại.'], 404);
