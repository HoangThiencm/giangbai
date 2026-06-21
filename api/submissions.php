<?php
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/google_drive.php';

// Assignment times are entered as local browser times. Keep PHP and the MySQL
// session on the same application timezone so shared hosting UTC defaults do not
// delay an assignment by seven hours in Viet Nam.
$submissionTimezone = defined('APP_TIMEZONE') ? (string)APP_TIMEZONE : 'Asia/Ho_Chi_Minh';
try {
    date_default_timezone_set($submissionTimezone);
    $pdo->exec("SET time_zone = '+07:00'");
} catch (Throwable $e) {
    // Time comparisons still use PHP's configured timezone if MySQL rejects the
    // session offset on a restricted hosting account.
}

set_exception_handler(function (Throwable $e) {
    $payload = ['error' => 'Có lỗi khi xử lý chức năng nộp bài.'];
    if (defined('APP_DEBUG') && APP_DEBUG) $payload['detail'] = $e->getMessage();
    respond($payload, 500);
});

function submission_schema(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS submission_assignments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        public_code VARCHAR(24) NOT NULL UNIQUE,
        owner_id INT NOT NULL,
        title VARCHAR(220) NOT NULL,
        description TEXT DEFAULT NULL,
        instructions TEXT DEFAULT NULL,
        submission_type VARCHAR(20) NOT NULL DEFAULT 'file',
        academic_year VARCHAR(30) DEFAULT NULL,
        form_fields_json LONGTEXT DEFAULT NULL,
        require_files TINYINT(1) NOT NULL DEFAULT 1,
        access_mode ENUM('public', 'class', 'selected', 'school_list') NOT NULL DEFAULT 'public',
        target_class VARCHAR(100) DEFAULT NULL,
        source_list_code VARCHAR(40) DEFAULT NULL,
        status ENUM('draft', 'open', 'closed') NOT NULL DEFAULT 'open',
        open_at DATETIME DEFAULT NULL,
        due_at DATETIME DEFAULT NULL,
        allow_multiple TINYINT(1) NOT NULL DEFAULT 0,
        max_files INT NOT NULL DEFAULT 5,
        max_file_mb INT NOT NULL DEFAULT 25,
        allowed_extensions VARCHAR(500) NOT NULL DEFAULT 'pdf,doc,docx,xls,xlsx,ppt,pptx,jpg,jpeg,png,zip,rar,txt',
        drive_folder_id VARCHAR(160) DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_submission_assignments_owner (owner_id),
        INDEX idx_submission_assignments_status (status)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    $pdo->exec("CREATE TABLE IF NOT EXISTS submission_participants (
        id INT AUTO_INCREMENT PRIMARY KEY,
        assignment_id INT NOT NULL,
        linked_user_id INT DEFAULT NULL,
        participant_code VARCHAR(40) NOT NULL,
        full_name VARCHAR(180) NOT NULL,
        role_label VARCHAR(100) DEFAULT NULL,
        group_name VARCHAR(160) DEFAULT NULL,
        contact VARCHAR(180) DEFAULT NULL,
        reopened TINYINT(1) NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_assignment_participant_code (assignment_id, participant_code),
        INDEX idx_submission_participants_user (linked_user_id),
        INDEX idx_submission_participants_assignment (assignment_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    $pdo->exec("CREATE TABLE IF NOT EXISTS assignment_submissions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        assignment_id INT NOT NULL,
        participant_id INT DEFAULT NULL,
        linked_user_id INT DEFAULT NULL,
        submitter_name VARCHAR(180) NOT NULL,
        submitter_role VARCHAR(100) DEFAULT NULL,
        group_name VARCHAR(160) DEFAULT NULL,
        identifier VARCHAR(180) DEFAULT NULL,
        note TEXT DEFAULT NULL,
        report_data_json LONGTEXT DEFAULT NULL,
        submitted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_assignment_submissions_assignment (assignment_id),
        INDEX idx_assignment_submissions_participant (participant_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    $pdo->exec("CREATE TABLE IF NOT EXISTS assignment_submission_files (
        id INT AUTO_INCREMENT PRIMARY KEY,
        submission_id INT NOT NULL,
        drive_file_id VARCHAR(160) NOT NULL,
        original_name VARCHAR(255) NOT NULL,
        stored_name VARCHAR(255) NOT NULL,
        mime_type VARCHAR(160) DEFAULT NULL,
        size_bytes BIGINT NOT NULL DEFAULT 0,
        view_url TEXT NOT NULL,
        download_url TEXT DEFAULT NULL,
        field_key VARCHAR(120) DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_assignment_submission_files_submission (submission_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    // Safe in-place upgrades for installations created before report forms were
    // added. Shared hosting databases usually allow ALTER TABLE for their owner.
    $upgrades = [
        ['submission_assignments', 'submission_type', "VARCHAR(20) NOT NULL DEFAULT 'file'"],
        ['submission_assignments', 'academic_year', 'VARCHAR(30) DEFAULT NULL'],
        ['submission_assignments', 'form_fields_json', 'LONGTEXT DEFAULT NULL'],
        ['submission_assignments', 'require_files', 'TINYINT(1) NOT NULL DEFAULT 1'],
        ['submission_assignments', 'source_list_code', 'VARCHAR(40) DEFAULT NULL'],
        ['submission_participants', 'reopened', 'TINYINT(1) NOT NULL DEFAULT 0'],
        ['assignment_submissions', 'report_data_json', 'LONGTEXT DEFAULT NULL'],
        ['assignment_submission_files', 'field_key', 'VARCHAR(120) DEFAULT NULL'],
    ];
    foreach ($upgrades as [$table, $column, $definition]) {
        try {
            $check = $pdo->query("SHOW COLUMNS FROM `$table` LIKE " . $pdo->quote($column));
            if (!$check->fetch()) $pdo->exec("ALTER TABLE `$table` ADD COLUMN `$column` $definition");
        } catch (Throwable $e) {
            // A later API response will expose missing schema through APP_DEBUG;
            // keep public pages available when ALTER is temporarily restricted.
        }
    }
    try {
        $pdo->exec("ALTER TABLE submission_assignments MODIFY access_mode ENUM('public', 'class', 'selected', 'school_list') NOT NULL DEFAULT 'public'");
    } catch (Throwable $e) {
        // Existing hosts may restrict ALTER permissions; old modes keep working.
    }
}

function submission_current_user(PDO $pdo): ?array
{
    if (empty($_SESSION['user_id'])) return null;
    $stmt = $pdo->prepare('SELECT * FROM users WHERE id = ? AND is_active = 1 LIMIT 1');
    $stmt->execute([(int)$_SESSION['user_id']]);
    return $stmt->fetch() ?: null;
}

function submission_require_teacher(PDO $pdo): array
{
    $user = submission_current_user($pdo);
    if (!$user || ($user['role'] ?? '') !== 'teacher') {
        respond(['error' => 'Cần đăng nhập bằng tài khoản giáo viên.'], 401);
    }
    return $user;
}

function submission_code(int $length = 10): string
{
    $alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    $value = '';
    for ($i = 0; $i < $length; $i++) $value .= $alphabet[random_int(0, strlen($alphabet) - 1)];
    return $value;
}

function submission_unique_public_code(PDO $pdo): string
{
    do {
        $code = submission_code(8);
        $stmt = $pdo->prepare('SELECT id FROM submission_assignments WHERE public_code = ? LIMIT 1');
        $stmt->execute([$code]);
    } while ($stmt->fetch());
    return $code;
}

function submission_datetime($value): ?string
{
    $value = trim((string)$value);
    if ($value === '') return null;
    $timestamp = strtotime($value);
    return $timestamp === false ? null : date('Y-m-d H:i:s', $timestamp);
}

function submission_field_key(string $value, int $index): string
{
    $value = trim($value);
    if (function_exists('iconv')) {
        $converted = @iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE', $value);
        if (is_string($converted)) $value = $converted;
    }
    $value = strtolower(preg_replace('/[^a-zA-Z0-9]+/', '_', $value));
    $value = trim($value, '_');
    return substr($value ?: ('field_' . ($index + 1)), 0, 100);
}

function submission_normalize_form_fields($input): array
{
    if (!is_array($input)) return [];
    $types = ['text', 'textarea', 'number', 'date', 'select', 'heading'];
    $fields = [];
    $used = [];
    foreach (array_slice($input, 0, 40) as $index => $raw) {
        if (!is_array($raw)) continue;
        $label = trim((string)($raw['label'] ?? ''));
        if ($label === '') continue;
        $type = in_array(($raw['type'] ?? ''), $types, true) ? $raw['type'] : 'text';
        $base = submission_field_key((string)($raw['key'] ?? $label), $index);
        $key = $base;
        $suffix = 2;
        while (isset($used[$key])) $key = substr($base, 0, 94) . '_' . $suffix++;
        $used[$key] = true;
        $optionsRaw = $raw['options'] ?? [];
        if (is_string($optionsRaw)) $optionsRaw = preg_split('/[,;\r\n]+/', $optionsRaw) ?: [];
        $options = [];
        if (is_array($optionsRaw)) {
            foreach ($optionsRaw as $option) {
                $option = trim((string)$option);
                if ($option !== '' && !in_array($option, $options, true)) $options[] = substr($option, 0, 180);
            }
        }
        $fields[] = [
            'key' => $key,
            'label' => substr($label, 0, 220),
            'type' => $type,
            'required' => $type !== 'heading' && !empty($raw['required']),
            'allow_evidence' => $type !== 'heading' && !empty($raw['allow_evidence']),
            'evidence_required' => $type !== 'heading' && !empty($raw['allow_evidence']) && !empty($raw['evidence_required']),
            'options' => $type === 'select' ? array_slice($options, 0, 50) : [],
        ];
    }
    return $fields;
}

function submission_form_fields(array $assignment): array
{
    $decoded = json_decode((string)($assignment['form_fields_json'] ?? '[]'), true);
    return submission_normalize_form_fields(is_array($decoded) ? $decoded : []);
}

function submission_report_data($value): array
{
    $decoded = is_array($value) ? $value : json_decode((string)$value, true);
    return is_array($decoded) ? $decoded : [];
}

function submission_assignment(PDO $pdo, int $id): ?array
{
    $stmt = $pdo->prepare('SELECT * FROM submission_assignments WHERE id = ? LIMIT 1');
    $stmt->execute([$id]);
    return $stmt->fetch() ?: null;
}

function submission_assignment_by_code(PDO $pdo, string $code): ?array
{
    $stmt = $pdo->prepare('SELECT * FROM submission_assignments WHERE public_code = ? LIMIT 1');
    $stmt->execute([strtoupper(trim($code))]);
    return $stmt->fetch() ?: null;
}

function submission_require_owner(PDO $pdo, array $teacher, int $id): array
{
    $assignment = submission_assignment($pdo, $id);
    if (!$assignment || (int)$assignment['owner_id'] !== (int)$teacher['id']) {
        respond(['error' => 'Không tìm thấy đợt nộp hoặc bạn không có quyền quản lý.'], 404);
    }
    return $assignment;
}

function submission_public_status(array $assignment): string
{
    if ($assignment['status'] !== 'open') return (string)$assignment['status'];
    $now = time();
    if (!empty($assignment['open_at']) && strtotime($assignment['open_at']) > $now) return 'not_started';
    if (!empty($assignment['due_at']) && strtotime($assignment['due_at']) < $now) return 'expired';
    return 'open';
}

function submission_public_assignment(array $assignment): array
{
    return [
        'code' => $assignment['public_code'],
        'title' => $assignment['title'],
        'description' => $assignment['description'] ?? '',
        'instructions' => $assignment['instructions'] ?? '',
        'submission_type' => in_array(($assignment['submission_type'] ?? ''), ['file', 'report'], true) ? $assignment['submission_type'] : 'file',
        'academic_year' => $assignment['academic_year'] ?? '',
        'form_fields' => submission_form_fields($assignment),
        'require_files' => (bool)($assignment['require_files'] ?? 1),
        'access_mode' => $assignment['access_mode'],
        'target_class' => $assignment['target_class'] ?? '',
        'source_list_code' => $assignment['source_list_code'] ?? '',
        'status' => submission_public_status($assignment),
        'open_at' => $assignment['open_at'],
        'due_at' => $assignment['due_at'],
        'allow_multiple' => (bool)$assignment['allow_multiple'],
        'max_files' => (int)$assignment['max_files'],
        'max_file_mb' => (int)$assignment['max_file_mb'],
        'allowed_extensions' => array_values(array_filter(array_map('trim', explode(',', strtolower($assignment['allowed_extensions']))))),
    ];
}

function submission_participant_by_access(PDO $pdo, array $assignment, ?array $user, string $code): ?array
{
    if ($user) {
        $stmt = $pdo->prepare('SELECT * FROM submission_participants WHERE assignment_id = ? AND linked_user_id = ? LIMIT 1');
        $stmt->execute([(int)$assignment['id'], (int)$user['id']]);
        $participant = $stmt->fetch();
        if ($participant) return $participant;
    }
    $code = strtoupper(trim($code));
    if ($code === '') return null;
    $stmt = $pdo->prepare('SELECT * FROM submission_participants WHERE assignment_id = ? AND participant_code = ? LIMIT 1');
    $stmt->execute([(int)$assignment['id'], $code]);
    return $stmt->fetch() ?: null;
}

function submission_participant_payload(?array $participant): ?array
{
    if (!$participant) return null;
    return [
        'id' => (int)$participant['id'],
        'full_name' => $participant['full_name'],
        'role_label' => $participant['role_label'] ?? '',
        'group_name' => $participant['group_name'] ?? '',
        'contact' => $participant['contact'] ?? '',
    ];
}

function submission_teacher_assignments(PDO $pdo, int $ownerId): array
{
    $stmt = $pdo->prepare("SELECT a.*,
        (SELECT COUNT(*) FROM submission_participants p WHERE p.assignment_id = a.id) AS participant_count,
        (SELECT COUNT(*) FROM assignment_submissions s WHERE s.assignment_id = a.id) AS submission_count,
        (SELECT COUNT(DISTINCT s.participant_id) FROM assignment_submissions s INNER JOIN submission_participants p2 ON p2.id = s.participant_id WHERE s.assignment_id = a.id) AS completed_participant_count
        FROM submission_assignments a WHERE a.owner_id = ? ORDER BY a.created_at DESC");
    $stmt->execute([$ownerId]);
    $rows = [];
    foreach ($stmt->fetchAll() as $row) {
        $row['id'] = (int)$row['id'];
        $row['allow_multiple'] = (bool)$row['allow_multiple'];
        $row['max_files'] = (int)$row['max_files'];
        $row['max_file_mb'] = (int)$row['max_file_mb'];
        $row['participant_count'] = (int)$row['participant_count'];
        $row['submission_count'] = (int)$row['submission_count'];
        $row['completed_participant_count'] = (int)$row['completed_participant_count'];
        $rows[] = $row;
    }
    return $rows;
}

function submission_teacher_directory(PDO $pdo, array $teacher): array
{
    $managedClasses = teacher_managed_classes($teacher);
    $where = "is_active = 1 AND (role = 'teacher'";
    $params = [];
    if ($managedClasses) {
        $where .= ' OR class_name IN (' . implode(',', array_fill(0, count($managedClasses), '?')) . ')';
        $params = $managedClasses;
    } else {
        $where .= " OR role = 'student'";
    }
    $where .= ')';
    $stmt = $pdo->prepare("SELECT id, username, full_name, role, class_name FROM users WHERE $where ORDER BY role, class_name, full_name");
    $stmt->execute($params);
    $users = [];
    $classes = [];
    foreach ($stmt->fetchAll() as $row) {
        $row['id'] = (int)$row['id'];
        $users[] = $row;
        if (($row['role'] ?? '') === 'student' && trim((string)$row['class_name']) !== '') $classes[$row['class_name']] = true;
    }
    $classNames = array_keys($classes);
    sort($classNames, SORT_NATURAL | SORT_FLAG_CASE);
    return ['users' => $users, 'classes' => $classNames];
}

function submission_normalize_people($people): array
{
    if (!is_array($people)) return [];
    $result = [];
    $seen = [];
    foreach ($people as $person) {
        if (!is_array($person)) continue;
        $name = trim((string)($person['full_name'] ?? ''));
        // Manual entries are deliberately account-independent. Existing accounts
        // are accepted only through selected_user_ids, which is permission-checked.
        $userId = 0;
        if ($name === '') continue;
        $code = strtoupper(preg_replace('/[^A-Z0-9_-]/', '', (string)($person['participant_code'] ?? '')));
        if ($code === '') $code = submission_code(8);
        while (isset($seen[$code])) $code = submission_code(8);
        $seen[$code] = true;
        $result[] = [
            'linked_user_id' => $userId ?: null,
            'participant_code' => $code,
            'full_name' => $name,
            'role_label' => trim((string)($person['role_label'] ?? '')),
            'group_name' => trim((string)($person['group_name'] ?? '')),
            'contact' => trim((string)($person['contact'] ?? '')),
        ];
    }
    return $result;
}

function submission_school_list_people(PDO $pdo, string $listCode): array
{
    $stmt = $pdo->prepare("SELECT p.full_name, p.group_name, p.role_label, p.contact
        FROM school_reference_people p JOIN school_reference_lists l ON l.id = p.list_id
        WHERE l.list_code = ? ORDER BY p.group_name, p.full_name");
    $stmt->execute([$listCode]);
    return $stmt->fetchAll();
}

function submission_build_participants(PDO $pdo, string $mode, string $className, string $schoolListCode, array $data, array $teacher): array
{
    if ($mode === 'public') return [];
    $people = $mode === 'selected' ? submission_normalize_people($data['participants'] ?? []) : [];
    $selectedIds = array_values(array_unique(array_filter(array_map('intval', $data['selected_user_ids'] ?? []))));
    $managedClasses = teacher_managed_classes($teacher);

    if ($mode === 'class') {
        if ($className === '') respond(['error' => 'Vui lòng chọn lớp/nhóm.'], 422);
        if ($managedClasses && !in_array($className, $managedClasses, true)) {
            respond(['error' => 'Bạn không được phân công quản lý lớp/nhóm này.'], 403);
        }
        $stmt = $pdo->prepare("SELECT id, username, full_name, role, class_name FROM users WHERE is_active = 1 AND class_name = ? ORDER BY full_name");
        $stmt->execute([$className]);
        $accounts = $stmt->fetchAll();
    } elseif ($mode === 'school_list') {
        if ($schoolListCode === '') respond(['error' => 'Vui lòng chọn danh sách của trường.'], 422);
        try {
            $schoolPeople = submission_school_list_people($pdo, $schoolListCode);
        } catch (Throwable $e) {
            respond(['error' => 'Danh sách THCS Trần Phú chưa được khai báo.'], 422);
        }
        foreach ($schoolPeople as $schoolPerson) {
            $people[] = [
                'linked_user_id' => null,
                'participant_code' => submission_code(8),
                'full_name' => trim((string)$schoolPerson['full_name']),
                'role_label' => trim((string)($schoolPerson['role_label'] ?? '')),
                'group_name' => trim((string)($schoolPerson['group_name'] ?? '')),
                'contact' => trim((string)($schoolPerson['contact'] ?? '')),
            ];
        }
        $accounts = [];
    } elseif ($selectedIds) {
        $directory = submission_teacher_directory($pdo, $teacher);
        $allowedUserIds = array_map(fn($row) => (int)$row['id'], $directory['users']);
        if (array_diff($selectedIds, $allowedUserIds)) {
            respond(['error' => 'Danh sách có tài khoản ngoài phạm vi bạn được quản lý.'], 403);
        }
        $placeholders = implode(',', array_fill(0, count($selectedIds), '?'));
        $stmt = $pdo->prepare("SELECT id, username, full_name, role, class_name FROM users WHERE is_active = 1 AND id IN ($placeholders)");
        $stmt->execute($selectedIds);
        $accounts = $stmt->fetchAll();
    } else {
        $accounts = [];
    }

    $existingUsers = [];
    foreach ($people as $person) if ($person['linked_user_id']) $existingUsers[(int)$person['linked_user_id']] = true;
    foreach ($accounts as $account) {
        if (isset($existingUsers[(int)$account['id']])) continue;
        $people[] = [
            'linked_user_id' => (int)$account['id'],
            'participant_code' => submission_code(8),
            'full_name' => trim((string)$account['full_name']),
            'role_label' => $account['role'] === 'teacher' ? 'Giáo viên' : 'Học sinh',
            'group_name' => trim((string)$account['class_name']),
            'contact' => trim((string)$account['username']),
        ];
    }
    if (!$people) respond(['error' => 'Danh sách chỉ định đang trống.'], 422);
    return $people;
}

function submission_sync_participants(PDO $pdo, int $assignmentId, array $people): void
{
    $existingStmt = $pdo->prepare('SELECT * FROM submission_participants WHERE assignment_id = ?');
    $existingStmt->execute([$assignmentId]);
    $existing = $existingStmt->fetchAll();
    $byUser = [];
    $byCode = [];
    foreach ($existing as $row) {
        if ($row['linked_user_id']) $byUser[(int)$row['linked_user_id']] = $row;
        $byCode[strtoupper((string)$row['participant_code'])] = $row;
    }

    $insert = $pdo->prepare('INSERT INTO submission_participants (assignment_id, linked_user_id, participant_code, full_name, role_label, group_name, contact) VALUES (?, ?, ?, ?, ?, ?, ?)');
    $update = $pdo->prepare('UPDATE submission_participants SET linked_user_id=?, participant_code=?, full_name=?, role_label=?, group_name=?, contact=? WHERE id=? AND assignment_id=?');
    $keptIds = [];
    foreach ($people as $person) {
        if ($person['linked_user_id'] && $person['full_name'] === '') {
            $lookup = $pdo->prepare('SELECT full_name, role, class_name, username FROM users WHERE id = ? LIMIT 1');
            $lookup->execute([$person['linked_user_id']]);
            $account = $lookup->fetch();
            if (!$account) continue;
            $person['full_name'] = $account['full_name'];
            $person['role_label'] = $person['role_label'] ?: ($account['role'] === 'teacher' ? 'Giáo viên' : 'Học sinh');
            $person['group_name'] = $person['group_name'] ?: $account['class_name'];
            $person['contact'] = $person['contact'] ?: $account['username'];
        }
        $matched = $person['linked_user_id'] ? ($byUser[(int)$person['linked_user_id']] ?? null) : ($byCode[strtoupper($person['participant_code'])] ?? null);
        if ($matched) {
            // Preserve the original access code and row id so previous submissions
            // remain attached when a teacher edits the assignment.
            $person['participant_code'] = $matched['participant_code'];
            $update->execute([
                $person['linked_user_id'], $person['participant_code'], $person['full_name'],
                $person['role_label'] ?: null, $person['group_name'] ?: null, $person['contact'] ?: null,
                (int)$matched['id'], $assignmentId,
            ]);
            $keptIds[] = (int)$matched['id'];
        } else {
            $insert->execute([
                $assignmentId, $person['linked_user_id'], $person['participant_code'], $person['full_name'],
                $person['role_label'] ?: null, $person['group_name'] ?: null, $person['contact'] ?: null,
            ]);
            $keptIds[] = (int)$pdo->lastInsertId();
        }
    }

    if ($keptIds) {
        $placeholders = implode(',', array_fill(0, count($keptIds), '?'));
        $delete = $pdo->prepare("DELETE FROM submission_participants WHERE assignment_id = ? AND id NOT IN ($placeholders)");
        $delete->execute(array_merge([$assignmentId], $keptIds));
    } else {
        $pdo->prepare('DELETE FROM submission_participants WHERE assignment_id = ?')->execute([$assignmentId]);
    }
}

function submission_files_from_input($source): array
{
    if (!$source) return [];
    if (!is_array($source['name'])) return [$source];
    $files = [];
    foreach ($source['name'] as $index => $name) {
        $files[] = [
            'name' => $name,
            'type' => $source['type'][$index] ?? '',
            'tmp_name' => $source['tmp_name'][$index] ?? '',
            'error' => $source['error'][$index] ?? UPLOAD_ERR_NO_FILE,
            'size' => $source['size'][$index] ?? 0,
        ];
    }
    return $files;
}

function submission_files_input(): array
{
    return submission_files_from_input($_FILES['files'] ?? null);
}

function submission_participants_for_teacher(PDO $pdo, int $assignmentId): array
{
    $stmt = $pdo->prepare("SELECT p.*,
        (SELECT COUNT(*) FROM assignment_submissions s WHERE s.participant_id = p.id) AS submission_count,
        (SELECT MAX(s.submitted_at) FROM assignment_submissions s WHERE s.participant_id = p.id) AS last_submitted_at
        FROM submission_participants p WHERE p.assignment_id = ? ORDER BY p.group_name, p.full_name");
    $stmt->execute([$assignmentId]);
    $rows = $stmt->fetchAll();
    foreach ($rows as &$row) {
        $row['id'] = (int)$row['id'];
        $row['linked_user_id'] = $row['linked_user_id'] ? (int)$row['linked_user_id'] : null;
        $row['submission_count'] = (int)$row['submission_count'];
        $row['reopened'] = (bool)($row['reopened'] ?? false);
    }
    return $rows;
}

function submission_rows_for_teacher(PDO $pdo, int $assignmentId): array
{
    $stmt = $pdo->prepare('SELECT * FROM assignment_submissions WHERE assignment_id = ? ORDER BY submitted_at DESC');
    $stmt->execute([$assignmentId]);
    $rows = $stmt->fetchAll();
    $fileStmt = $pdo->prepare('SELECT id, drive_file_id, original_name, mime_type, size_bytes, view_url, download_url, field_key FROM assignment_submission_files WHERE submission_id = ? ORDER BY id');
    foreach ($rows as &$row) {
        $row['id'] = (int)$row['id'];
        $row['participant_id'] = $row['participant_id'] ? (int)$row['participant_id'] : null;
        $row['report_data'] = submission_report_data($row['report_data_json'] ?? null);
        unset($row['report_data_json']);
        $fileStmt->execute([$row['id']]);
        $row['files'] = $fileStmt->fetchAll();
    }
    return $rows;
}

submission_schema($pdo);
$method = $_SERVER['REQUEST_METHOD'];
$action = trim((string)($_GET['action'] ?? ''));

if ($method === 'GET' && $action === 'bootstrap') {
    $teacher = submission_require_teacher($pdo);
    $directory = submission_teacher_directory($pdo, $teacher);
    respond([
        'ok' => true,
        'user' => public_user($teacher),
        'assignments' => submission_teacher_assignments($pdo, (int)$teacher['id']),
        'classes' => $directory['classes'],
        'users' => $directory['users'],
        'drive_configured' => defined('GOOGLE_DRIVE_CREDENTIALS_JSON') && trim((string)GOOGLE_DRIVE_CREDENTIALS_JSON) !== '' && defined('GOOGLE_DRIVE_ROOT_FOLDER_ID') && trim((string)GOOGLE_DRIVE_ROOT_FOLDER_ID) !== '',
    ]);
}

if ($method === 'POST' && $action === 'save') {
    $teacher = submission_require_teacher($pdo);
    $data = json_body();
    $id = (int)($data['id'] ?? 0);
    $title = trim((string)($data['title'] ?? ''));
    if ($title === '') respond(['error' => 'Vui lòng nhập tên đợt nộp.'], 422);
    $mode = in_array(($data['access_mode'] ?? ''), ['public', 'class', 'selected', 'school_list'], true) ? $data['access_mode'] : 'public';
    $className = $mode === 'class' ? trim((string)($data['target_class'] ?? '')) : '';
    $schoolListCode = $mode === 'school_list' ? trim((string)($data['school_list_code'] ?? '')) : '';
    $status = in_array(($data['status'] ?? ''), ['draft', 'open', 'closed'], true) ? $data['status'] : 'open';
    $submissionType = ($data['submission_type'] ?? '') === 'report' ? 'report' : 'file';
    $formFields = $submissionType === 'report' ? submission_normalize_form_fields($data['form_fields'] ?? []) : [];
    if ($submissionType === 'report' && !$formFields) respond(['error' => 'Báo cáo cần có ít nhất một trường thông tin.'], 422);
    $academicYear = trim((string)($data['academic_year'] ?? ''));
    $requireFiles = $submissionType === 'file' || !empty($data['require_files']);
    $openAt = submission_datetime($data['open_at'] ?? null);
    $dueAt = submission_datetime($data['due_at'] ?? null);
    if ($openAt && $dueAt && strtotime($openAt) >= strtotime($dueAt)) respond(['error' => 'Hạn nộp phải sau thời gian mở.'], 422);
    $serverMax = defined('SUBMISSION_MAX_FILE_MB') ? max(1, (int)SUBMISSION_MAX_FILE_MB) : 25;
    $maxFiles = max(1, min(20, (int)($data['max_files'] ?? 5)));
    $maxFileMb = max(1, min($serverMax, (int)($data['max_file_mb'] ?? $serverMax)));
    $extensions = strtolower(preg_replace('/[^a-z0-9,]/', '', (string)($data['allowed_extensions'] ?? 'pdf,doc,docx,xls,xlsx,ppt,pptx,jpg,jpeg,png,zip,rar,txt')));
    if ($extensions === '') respond(['error' => 'Cần cho phép ít nhất một loại tệp.'], 422);
    $people = submission_build_participants($pdo, $mode, $className, $schoolListCode, $data, $teacher);

    $pdo->beginTransaction();
    try {
        if ($id) {
            $existing = submission_require_owner($pdo, $teacher, $id);
            $stmt = $pdo->prepare('UPDATE submission_assignments SET title=?, description=?, instructions=?, submission_type=?, academic_year=?, form_fields_json=?, require_files=?, access_mode=?, target_class=?, source_list_code=?, status=?, open_at=?, due_at=?, allow_multiple=?, max_files=?, max_file_mb=?, allowed_extensions=? WHERE id=?');
            $stmt->execute([$title, trim((string)($data['description'] ?? '')), trim((string)($data['instructions'] ?? '')), $submissionType, $academicYear ?: null, json_encode($formFields, JSON_UNESCAPED_UNICODE), $requireFiles ? 1 : 0, $mode, $className ?: null, $schoolListCode ?: null, $status, $openAt, $dueAt, !empty($data['allow_multiple']) ? 1 : 0, $maxFiles, $maxFileMb, $extensions, $id]);
        } else {
            $publicCode = submission_unique_public_code($pdo);
            $stmt = $pdo->prepare('INSERT INTO submission_assignments (public_code, owner_id, title, description, instructions, submission_type, academic_year, form_fields_json, require_files, access_mode, target_class, source_list_code, status, open_at, due_at, allow_multiple, max_files, max_file_mb, allowed_extensions) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)');
            $stmt->execute([$publicCode, (int)$teacher['id'], $title, trim((string)($data['description'] ?? '')), trim((string)($data['instructions'] ?? '')), $submissionType, $academicYear ?: null, json_encode($formFields, JSON_UNESCAPED_UNICODE), $requireFiles ? 1 : 0, $mode, $className ?: null, $schoolListCode ?: null, $status, $openAt, $dueAt, !empty($data['allow_multiple']) ? 1 : 0, $maxFiles, $maxFileMb, $extensions]);
            $id = (int)$pdo->lastInsertId();
        }
        submission_sync_participants($pdo, $id, $people);
        $pdo->commit();
    } catch (Throwable $e) {
        if ($pdo->inTransaction()) $pdo->rollBack();
        throw $e;
    }
    $saved = submission_assignment($pdo, $id);
    respond(['ok' => true, 'assignment' => $saved, 'participants' => submission_participants_for_teacher($pdo, $id)]);
}

if ($method === 'GET' && $action === 'detail') {
    $teacher = submission_require_teacher($pdo);
    $assignment = submission_require_owner($pdo, $teacher, (int)($_GET['id'] ?? 0));
    respond([
        'ok' => true,
        'assignment' => $assignment,
        'participants' => submission_participants_for_teacher($pdo, (int)$assignment['id']),
        'submissions' => submission_rows_for_teacher($pdo, (int)$assignment['id']),
    ]);
}

if ($method === 'GET' && $action === 'download-zip') {
    $teacher = submission_require_teacher($pdo);
    $assignment = submission_require_owner($pdo, $teacher, (int)($_GET['id'] ?? 0));
    if (!class_exists('ZipArchive')) {
        respond(['error' => 'Hosting chưa bật PHP extension ZipArchive. Hãy bật extension zip để tải tất cả tệp thành ZIP.'], 500);
    }
    $stmt = $pdo->prepare("SELECT f.drive_file_id, f.original_name, f.size_bytes, s.submitter_name, s.group_name
        FROM assignment_submission_files f JOIN assignment_submissions s ON s.id = f.submission_id
        WHERE s.assignment_id = ? ORDER BY s.group_name, s.submitter_name, f.id");
    $stmt->execute([(int)$assignment['id']]);
    $files = $stmt->fetchAll();
    if (!$files) respond(['error' => 'Đợt này chưa có tệp nào để đóng gói.'], 422);
    $maxZipBytes = (defined('SUBMISSION_ZIP_MAX_MB') ? max(10, (int)SUBMISSION_ZIP_MAX_MB) : 500) * 1024 * 1024;
    $totalBytes = array_sum(array_map(fn($file) => (int)$file['size_bytes'], $files));
    if ($totalBytes > $maxZipBytes) {
        respond(['error' => 'Tổng dung lượng vượt giới hạn ZIP của hosting (' . round($maxZipBytes / 1024 / 1024) . ' MB). Hãy tải trực tiếp thư mục trên Google Drive hoặc tăng SUBMISSION_ZIP_MAX_MB.'], 422);
    }
    $temp = tempnam(sys_get_temp_dir(), 'giangbai_zip_');
    if ($temp === false) respond(['error' => 'Hosting không tạo được tệp ZIP tạm.'], 500);
    $zip = new ZipArchive();
    if ($zip->open($temp, ZipArchive::CREATE | ZipArchive::OVERWRITE) !== true) {
        @unlink($temp);
        respond(['error' => 'Không thể khởi tạo tệp ZIP.'], 500);
    }
    try {
        $usedNames = [];
        foreach ($files as $file) {
            $group = drive_safe_name((string)($file['group_name'] ?? ''), 'CHUA_PHAN_NHOM');
            $person = drive_safe_name((string)($file['submitter_name'] ?? ''), 'Nguoi nop');
            $name = drive_safe_name((string)$file['original_name'], 'tep');
            $entry = $group . '/' . $person . '/' . $name;
            $base = $entry;
            $index = 2;
            while (isset($usedNames[$entry])) {
                $entry = preg_replace('/(\.[^.]+)?$/', '-' . $index++ . '$0', $base);
            }
            $usedNames[$entry] = true;
            $content = drive_download_file((string)$file['drive_file_id']);
            if (!$zip->addFromString($entry, $content)) throw new RuntimeException('Không thêm được tệp ' . $name . ' vào ZIP.');
        }
        $zip->close();
        $safe = preg_replace('/[^A-Za-z0-9_-]+/', '-', drive_safe_name((string)$assignment['title'], 'bao-cao'));
        while (ob_get_level()) ob_end_clean();
        header('Content-Type: application/zip');
        header('Content-Disposition: attachment; filename="' . trim($safe, '-') . '-' . $assignment['public_code'] . '.zip"');
        header('Content-Length: ' . filesize($temp));
        readfile($temp);
        @unlink($temp);
        exit;
    } catch (Throwable $e) {
        $zip->close();
        @unlink($temp);
        throw $e;
    }
}

if ($method === 'POST' && $action === 'status') {
    $teacher = submission_require_teacher($pdo);
    $data = json_body();
    $assignment = submission_require_owner($pdo, $teacher, (int)($data['id'] ?? 0));
    $status = in_array(($data['status'] ?? ''), ['draft', 'open', 'closed'], true) ? $data['status'] : 'closed';
    $pdo->prepare('UPDATE submission_assignments SET status = ? WHERE id = ?')->execute([$status, (int)$assignment['id']]);
    respond(['ok' => true, 'status' => $status]);
}

if ($method === 'POST' && $action === 'delete') {
    $teacher = submission_require_teacher($pdo);
    $data = json_body();
    $assignment = submission_require_owner($pdo, $teacher, (int)($data['id'] ?? 0));
    $assignmentId = (int)$assignment['id'];
    $pdo->beginTransaction();
    try {
        // Delete database records explicitly so this also works for older
        // installations whose automatically-created tables have no FK cascade.
        $pdo->prepare('DELETE f FROM assignment_submission_files f INNER JOIN assignment_submissions s ON s.id = f.submission_id WHERE s.assignment_id = ?')->execute([$assignmentId]);
        $pdo->prepare('DELETE FROM assignment_submissions WHERE assignment_id = ?')->execute([$assignmentId]);
        $pdo->prepare('DELETE FROM submission_participants WHERE assignment_id = ?')->execute([$assignmentId]);
        $pdo->prepare('DELETE FROM submission_assignments WHERE id = ?')->execute([$assignmentId]);
        $pdo->commit();
    } catch (Throwable $e) {
        if ($pdo->inTransaction()) $pdo->rollBack();
        throw $e;
    }
    respond([
        'ok' => true,
        'message' => 'Đã xóa đợt báo cáo và toàn bộ dữ liệu nộp trong hệ thống. Tệp trên Google Drive được giữ lại để an toàn.',
    ]);
}

if ($method === 'GET' && $action === 'public') {
    $assignment = submission_assignment_by_code($pdo, (string)($_GET['code'] ?? ''));
    if (!$assignment) respond(['error' => 'Đường link nộp bài không tồn tại.'], 404);
    $user = submission_current_user($pdo);
    $participant = $assignment['access_mode'] === 'public' ? null : submission_participant_by_access($pdo, $assignment, $user, (string)($_GET['participant_code'] ?? ''));
    respond([
        'ok' => true,
        'assignment' => submission_public_assignment($assignment),
        'participant' => submission_participant_payload($participant),
        'needs_access_code' => $assignment['access_mode'] !== 'public' && !$participant,
        'signed_in_as' => $user ? ['full_name' => $user['full_name'], 'role' => $user['role'], 'class_name' => $user['class_name']] : null,
    ]);
}

if ($method === 'POST' && $action === 'submit') {
    $assignment = submission_assignment_by_code($pdo, (string)($_POST['code'] ?? ''));
    if (!$assignment) respond(['error' => 'Đường link nộp bài không tồn tại.'], 404);
    if (submission_public_status($assignment) !== 'open') respond(['error' => 'Đợt nộp bài hiện chưa mở hoặc đã kết thúc.'], 403);
    $user = submission_current_user($pdo);
    $participant = null;
    if ($assignment['access_mode'] !== 'public') {
        $participant = submission_participant_by_access($pdo, $assignment, $user, (string)($_POST['participant_code'] ?? ''));
        if (!$participant) respond(['error' => 'Mã người nộp không đúng hoặc bạn không có tên trong danh sách.'], 403);
    }

    if ($participant) {
        $name = trim((string)$participant['full_name']);
        $role = trim((string)$participant['role_label']);
        $group = trim((string)$participant['group_name']);
        $identifier = trim((string)$participant['contact']) ?: (string)$participant['participant_code'];
    } else {
        $name = trim((string)($_POST['submitter_name'] ?? ''));
        $role = trim((string)($_POST['submitter_role'] ?? ''));
        $group = trim((string)($_POST['group_name'] ?? ''));
        $identifier = trim((string)($_POST['identifier'] ?? ''));
        if ($name === '' || $identifier === '') respond(['error' => 'Vui lòng nhập họ tên và mã/SĐT/email để nhận diện bài nộp.'], 422);
    }

    if (!(bool)$assignment['allow_multiple']) {
        if ($participant) {
            $dup = $pdo->prepare('SELECT id FROM assignment_submissions WHERE assignment_id = ? AND participant_id = ? LIMIT 1');
            $dup->execute([(int)$assignment['id'], (int)$participant['id']]);
        } else {
            $dup = $pdo->prepare('SELECT id FROM assignment_submissions WHERE assignment_id = ? AND identifier = ? LIMIT 1');
            $dup->execute([(int)$assignment['id'], $identifier]);
        }
        if ($dup->fetch()) respond(['error' => 'Người này đã nộp bài. Đợt nộp không cho phép nộp nhiều lần.'], 409);
    }

    $submissionType = in_array(($assignment['submission_type'] ?? ''), ['file', 'report'], true) ? $assignment['submission_type'] : 'file';
    $reportData = submission_report_data($_POST['report_data'] ?? null);
    $formFields = $submissionType === 'report' ? submission_form_fields($assignment) : [];
    if ($submissionType === 'report') {
        foreach ($formFields as $field) {
            if ($field['type'] === 'heading') continue;
            $value = trim((string)($reportData[$field['key']] ?? ''));
            if ($field['required'] && $value === '') respond(['error' => 'Thiếu trường bắt buộc: ' . $field['label']], 422);
            if ($field['type'] === 'number' && $value !== '' && !is_numeric($value)) respond(['error' => 'Trường "' . $field['label'] . '" phải là số.'], 422);
            if ($field['type'] === 'select' && $value !== '' && !in_array($value, $field['options'], true)) respond(['error' => 'Lựa chọn của trường "' . $field['label'] . '" không hợp lệ.'], 422);
        }
    }

    $generalFiles = array_values(array_filter(submission_files_input(), fn($file) => (int)$file['error'] !== UPLOAD_ERR_NO_FILE));
    $uploadQueue = array_map(fn($file) => ['file' => $file, 'field_key' => null], $generalFiles);
    foreach ($formFields as $field) {
        if (!$field['allow_evidence']) continue;
        $evidenceFiles = array_values(array_filter(submission_files_from_input($_FILES['evidence_' . $field['key']] ?? null), fn($file) => (int)$file['error'] !== UPLOAD_ERR_NO_FILE));
        if ($field['evidence_required'] && !$evidenceFiles) respond(['error' => 'Thiếu tệp minh chứng: ' . $field['label']], 422);
        foreach ($evidenceFiles as $file) $uploadQueue[] = ['file' => $file, 'field_key' => $field['key']];
    }
    if ((bool)($assignment['require_files'] ?? true) && !$generalFiles) respond(['error' => 'Vui lòng chọn ít nhất một tệp đính kèm.'], 422);
    if (count($uploadQueue) > (int)$assignment['max_files']) respond(['error' => 'Số tệp vượt quá giới hạn của đợt nộp.'], 422);
    $allowed = array_values(array_filter(array_map('trim', explode(',', strtolower($assignment['allowed_extensions'])))));
    $maxBytes = (int)$assignment['max_file_mb'] * 1024 * 1024;
    foreach ($uploadQueue as $queued) {
        $file = $queued['file'];
        if ((int)$file['error'] !== UPLOAD_ERR_OK) respond(['error' => 'Một tệp tải lên bị lỗi (mã ' . (int)$file['error'] . ').'], 422);
        if ((int)$file['size'] < 1 || (int)$file['size'] > $maxBytes) respond(['error' => 'Tệp ' . $file['name'] . ' vượt giới hạn ' . (int)$assignment['max_file_mb'] . ' MB.'], 422);
        $extension = strtolower(pathinfo((string)$file['name'], PATHINFO_EXTENSION));
        if ($extension === '' || !in_array($extension, $allowed, true)) respond(['error' => 'Không cho phép loại tệp .' . $extension . '.'], 422);
        if (!is_uploaded_file($file['tmp_name'])) respond(['error' => 'Tệp tải lên không hợp lệ.'], 422);
    }

    $uploaded = [];
    if ($uploadQueue) {
        $folderId = trim((string)($assignment['drive_folder_id'] ?? ''));
        if ($folderId === '') {
            $folderId = drive_assignment_folder(
                $assignment['title'],
                (string)($assignment['submission_type'] ?? 'file'),
                $assignment['academic_year'] ?? null
            );
            $pdo->prepare('UPDATE submission_assignments SET drive_folder_id = ? WHERE id = ? AND (drive_folder_id IS NULL OR drive_folder_id = \'\')')->execute([$folderId, (int)$assignment['id']]);
        }
        foreach ($uploadQueue as $index => $queued) {
            $file = $queued['file'];
            $original = (string)$file['name'];
            $storedName = drive_submission_stored_name($group, $name, $identifier, $index + 1, $original, $queued['field_key']);
            $invalid = drive_validate_upload($file['tmp_name'], $original);
            if ($invalid) respond(['error' => $invalid], 422);
            $mime = drive_detect_mime($file['tmp_name'], $original, (string)($file['type'] ?? ''));
            $drive = drive_upload_file($folderId, $storedName, $mime, $file['tmp_name']);
            $uploaded[] = [
                'drive_file_id' => $drive['file_id'], 'original_name' => $original, 'stored_name' => $drive['stored_name'],
                'mime_type' => $drive['mime_type'] ?? $mime, 'size_bytes' => (int)$file['size'], 'view_url' => $drive['view_url'], 'download_url' => $drive['download_url'],
                'field_key' => $queued['field_key'],
            ];
        }
    }

    $pdo->beginTransaction();
    try {
        $stmt = $pdo->prepare('INSERT INTO assignment_submissions (assignment_id, participant_id, linked_user_id, submitter_name, submitter_role, group_name, identifier, note, report_data_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)');
        $stmt->execute([(int)$assignment['id'], $participant ? (int)$participant['id'] : null, $participant && $participant['linked_user_id'] ? (int)$participant['linked_user_id'] : ($user ? (int)$user['id'] : null), $name, $role ?: null, $group ?: null, $identifier ?: null, trim((string)($_POST['note'] ?? '')) ?: null, $submissionType === 'report' ? json_encode($reportData, JSON_UNESCAPED_UNICODE) : null]);
        $submissionId = (int)$pdo->lastInsertId();
        $fileStmt = $pdo->prepare('INSERT INTO assignment_submission_files (submission_id, drive_file_id, original_name, stored_name, mime_type, size_bytes, view_url, download_url, field_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)');
        foreach ($uploaded as $file) $fileStmt->execute([$submissionId, $file['drive_file_id'], $file['original_name'], $file['stored_name'], $file['mime_type'], $file['size_bytes'], $file['view_url'], $file['download_url'], $file['field_key']]);
        $pdo->commit();
    } catch (Throwable $e) {
        if ($pdo->inTransaction()) $pdo->rollBack();
        throw $e;
    }
    respond(['ok' => true, 'submission_id' => $submissionId, 'submitted_at' => date('c'), 'file_count' => count($uploaded)]);
}

respond(['error' => 'Endpoint không tồn tại.'], 404);
