<?php
require_once __DIR__ . '/helpers.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

const PHANCONG_SCHEMA_VERSION = '20261126-v5';

function phancong_current_user(PDO $pdo, bool $required = true): ?array
{
    // 1. Kiểm tra Admin Key nếu có
    $adminKey = $_SERVER['HTTP_X_ADMIN_KEY'] ?? ($_GET['admin_key'] ?? '');
    if ($adminKey !== '' && defined('ADMIN_KEY') && hash_equals(ADMIN_KEY, $adminKey)) {
        return [
            'id' => 0,
            'username' => 'admin',
            'full_name' => 'Quản trị viên',
            'role' => 'admin',
            'is_admin_key' => true
        ];
    }

    $userId = (int)($_SESSION['user_id'] ?? 0);
    if ($userId <= 0) {
        if ($required) {
            respond(['error' => 'Vui lòng đăng nhập tài khoản Giáo viên hoặc Quản trị viên để lưu CSDL.'], 401);
        }
        return null;
    }

    $stmt = $pdo->prepare("SELECT id, username, full_name, role, is_active, allowed_pages_json FROM users WHERE id = ? LIMIT 1");
    $stmt->execute([$userId]);
    $user = $stmt->fetch();
    if (!$user || !(bool)$user['is_active']) {
        if ($required) {
            respond(['error' => 'Tài khoản không hợp lệ hoặc đã bị khóa.'], 403);
        }
        return null;
    }

    $role = (string)($user['role'] ?? '');
    if ($role === 'admin' || $role === 'superadmin') {
        return $user;
    }

    if ($role !== 'teacher') {
        if ($required) {
            respond(['error' => 'Chức năng phân công chuyên môn chỉ dành cho giáo viên hoặc quản trị viên.'], 403);
        }
        return null;
    }

    $allowedPages = json_decode((string)($user['allowed_pages_json'] ?? '[]'), true);
    if (!is_array($allowedPages) || !in_array('phancongtochuyenmon', $allowedPages, true)) {
        if ($required) {
            respond(['error' => 'Tài khoản chưa được cấp quyền Quản lý tổ chuyên môn.'], 403);
        }
        return null;
    }

    return $user;
}

function phancong_owner_id(array $currentUser): int
{
    $ownerId = (int)($currentUser['id'] ?? 0);
    if ($ownerId <= 0) {
        respond(['error' => 'Cần đăng nhập bằng tài khoản có phiên hợp lệ để dùng dữ liệu phân công riêng.'], 403);
    }
    return $ownerId;
}

function phancong_public_user(array $currentUser): array
{
    return [
        'id' => (int)$currentUser['id'],
        'username' => (string)$currentUser['username'],
        'full_name' => (string)$currentUser['full_name'],
        'role' => (string)$currentUser['role'],
    ];
}

function phancong_maybe_ensure_schema(PDO $pdo): void
{
    if (schema_is_ready('phancong_chuyenmon', PHANCONG_SCHEMA_VERSION)) {
        return;
    }
    try {
        phancong_ensure_schema($pdo);
        schema_mark_ready('phancong_chuyenmon', PHANCONG_SCHEMA_VERSION);
    } catch (Throwable $e) {
        if (!phancong_table_exists($pdo, 'phancong_chuyenmon')) {
            throw $e;
        }
        schema_mark_ready('phancong_chuyenmon', PHANCONG_SCHEMA_VERSION);
    }
}

function phancong_table_exists(PDO $pdo, string $table): bool
{
    try {
        $stmt = $pdo->prepare('SHOW TABLES LIKE ?');
        $stmt->execute([$table]);
        return (bool)$stmt->fetch();
    } catch (Throwable $e) {
        return false;
    }
}

function phancong_column_exists(PDO $pdo, string $column): bool
{
    $stmt = $pdo->prepare("SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'phancong_chuyenmon' AND COLUMN_NAME = ?
        LIMIT 1");
    $stmt->execute([$column]);
    return (bool)$stmt->fetch();
}

function phancong_index_exists(PDO $pdo, string $indexName): bool
{
    $stmt = $pdo->prepare("SELECT 1 FROM INFORMATION_SCHEMA.STATISTICS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'phancong_chuyenmon' AND INDEX_NAME = ?
        LIMIT 1");
    $stmt->execute([$indexName]);
    return (bool)$stmt->fetch();
}

function phancong_ensure_schema(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS phancong_chuyenmon (
        id INT AUTO_INCREMENT PRIMARY KEY,
        owner_id INT DEFAULT NULL,
        plan_key VARCHAR(80) NOT NULL DEFAULT 'default',
        title VARCHAR(200) NOT NULL DEFAULT 'Phân công chuyên môn',
        school_year VARCHAR(40) NOT NULL DEFAULT '',
        semester VARCHAR(20) NOT NULL DEFAULT 'HK1',
        data_json LONGTEXT NOT NULL,
        created_by INT DEFAULT NULL,
        updated_by INT DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_phancong_key (plan_key),
        INDEX idx_phancong_owner_plan (owner_id, plan_key),
        UNIQUE KEY uq_phancong_owner_plan (owner_id, plan_key),
        INDEX idx_phancong_updated (updated_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");

    if (!phancong_column_exists($pdo, 'owner_id')) {
        $pdo->exec('ALTER TABLE phancong_chuyenmon ADD COLUMN owner_id INT DEFAULT NULL AFTER id');
    }

    if (!phancong_index_exists($pdo, 'idx_phancong_owner_plan')) {
        $pdo->exec('ALTER TABLE phancong_chuyenmon ADD INDEX idx_phancong_owner_plan (owner_id, plan_key)');
    }

    if (!phancong_index_exists($pdo, 'uq_phancong_owner_plan')) {
        $duplicates = $pdo->query('SELECT COUNT(*) FROM (SELECT owner_id, plan_key FROM phancong_chuyenmon WHERE owner_id IS NOT NULL GROUP BY owner_id, plan_key HAVING COUNT(*) > 1) AS duplicate_owner_plans')->fetchColumn();
        if ((int)$duplicates === 0) {
            $pdo->exec('ALTER TABLE phancong_chuyenmon ADD UNIQUE INDEX uq_phancong_owner_plan (owner_id, plan_key)');
        }
    }

    $pdo->exec("CREATE TABLE IF NOT EXISTS phancong_weekly_timetables (
        id INT AUTO_INCREMENT PRIMARY KEY,
        owner_id INT NOT NULL,
        plan_key VARCHAR(80) NOT NULL DEFAULT 'default',
        school_year VARCHAR(40) NOT NULL DEFAULT '',
        week_key VARCHAR(16) NOT NULL,
        week_num INT NOT NULL DEFAULT 0,
        start_date VARCHAR(10) NOT NULL DEFAULT '',
        end_date VARCHAR(10) NOT NULL DEFAULT '',
        timetables_json LONGTEXT NOT NULL,
        updated_by INT DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uq_phancong_owner_plan_week (owner_id, plan_key, week_key),
        INDEX idx_phancong_weekly_owner_plan_num (owner_id, plan_key, week_num)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");

    $pdo->exec("CREATE TABLE IF NOT EXISTS phancong_backups (
        id INT AUTO_INCREMENT PRIMARY KEY,
        owner_id INT NOT NULL,
        plan_key VARCHAR(80) NOT NULL DEFAULT 'default',
        reason VARCHAR(255) NOT NULL DEFAULT '',
        school_year VARCHAR(40) NOT NULL DEFAULT '',
        semester VARCHAR(20) NOT NULL DEFAULT 'HK1',
        data_json LONGTEXT NOT NULL,
        weekly_json LONGTEXT DEFAULT NULL,
        created_by INT DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_phancong_backups_owner_plan (owner_id, plan_key, created_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");
}

function phancong_create_backup(PDO $pdo, int $ownerId, string $planKey, string $reason, int $userId, bool $skipIfIdentical = false): ?array
{
    $stmt = $pdo->prepare("SELECT title, school_year, semester, data_json, updated_at FROM phancong_chuyenmon WHERE owner_id = ? AND plan_key = ? LIMIT 1");
    $stmt->execute([$ownerId, $planKey]);
    $current = $stmt->fetch();
    if (!$current || empty($current['data_json'])) {
        return null;
    }

    if ($skipIfIdentical) {
        $lastStmt = $pdo->prepare("SELECT id, data_json, created_at, reason FROM phancong_backups WHERE owner_id = ? AND plan_key = ? ORDER BY id DESC LIMIT 1");
        $lastStmt->execute([$ownerId, $planKey]);
        $lastRow = $lastStmt->fetch();
        if ($lastRow && md5((string)$lastRow['data_json']) === md5((string)$current['data_json'])) {
            return [
                'id' => (int)$lastRow['id'],
                'plan_key' => $planKey,
                'reason' => (string)$lastRow['reason'],
                'created_at' => (string)$lastRow['created_at'],
                'reused' => true,
            ];
        }
    }

    $loadedWeeks = phancong_load_weekly_timetables($pdo, $ownerId, $planKey);
    $weeklyJson = json_encode($loadedWeeks['map'], JSON_UNESCAPED_UNICODE) ?: '{}';
    $cleanReason = trim($reason) !== '' ? substr(trim($reason), 0, 250) : 'Sao lưu CSDL';

    $ins = $pdo->prepare("INSERT INTO phancong_backups (owner_id, plan_key, reason, school_year, semester, data_json, weekly_json, created_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
    $ins->execute([
        $ownerId,
        $planKey,
        $cleanReason,
        (string)($current['school_year'] ?? ''),
        (string)($current['semester'] ?? 'HK1'),
        (string)$current['data_json'],
        $weeklyJson,
        $userId,
    ]);
    $backupId = (int)$pdo->lastInsertId();

    // Giữ tối đa 40 bản sao lưu gần nhất cho mỗi kế hoạch để tránh phình CSDL.
    $keepStmt = $pdo->prepare("SELECT id FROM phancong_backups WHERE owner_id = ? AND plan_key = ? ORDER BY id DESC LIMIT 1 OFFSET 40");
    $keepStmt->execute([$ownerId, $planKey]);
    $cutoff = $keepStmt->fetchColumn();
    if ($cutoff) {
        $del = $pdo->prepare("DELETE FROM phancong_backups WHERE owner_id = ? AND plan_key = ? AND id <= ?");
        $del->execute([$ownerId, $planKey, (int)$cutoff]);
    }

    return [
        'id' => $backupId,
        'plan_key' => $planKey,
        'reason' => $cleanReason,
        'school_year' => (string)($current['school_year'] ?? ''),
        'semester' => (string)($current['semester'] ?? 'HK1'),
        'created_at' => date('Y-m-d H:i:s'),
    ];
}

function phancong_infer_week_key(array $stateData, string $isoDate): string
{
    $start = (string)($stateData['bao_giang']['start_date'] ?? '');
    if (!preg_match('/^\\d{4}-\\d{2}-\\d{2}$/', $start)) {
        $year = 0;
        if (preg_match('/(20\\d{2})\\s*[-–]/', (string)($stateData['info']['school_year'] ?? ''), $m)) $year = (int)$m[1];
        if (!$year) $year = (int)substr($isoDate, 0, 4);
        $start = sprintf('%04d-09-05', $year);
    }
    try {
        $first = new DateTimeImmutable($start);
        $first = $first->modify('monday this week');
        $date = new DateTimeImmutable($isoDate ?: date('Y-m-d'));
        $weeks = (int)floor(($date->getTimestamp() - $first->getTimestamp()) / 604800) + 1;
        return $weeks >= 1 && $weeks <= 45 ? 'W' . $weeks : '';
    } catch (Throwable $e) { return ''; }
}

function phancong_extract_teacher_timetables(array $stateData): array
{
    $result = [];
    foreach (($stateData['teachers'] ?? []) as $teacher) {
        if (!is_array($teacher) || !isset($teacher['id']) || !is_array($teacher['timetable'] ?? null)) continue;
        $hasLesson = false;
        foreach (['morning', 'afternoon'] as $session) foreach (($teacher['timetable'][$session] ?? []) as $day) {
            if (is_array($day) && count($day)) { $hasLesson = true; break 2; }
        }
        if ($hasLesson) $result[(string)$teacher['id']] = $teacher['timetable'];
    }
    return $result;
}

function phancong_load_weekly_timetables(PDO $pdo, int $ownerId, string $planKey): array
{
    $stmt = $pdo->prepare('SELECT week_key, week_num, start_date, end_date, timetables_json, updated_at FROM phancong_weekly_timetables WHERE owner_id = ? AND plan_key = ? ORDER BY week_num');
    $stmt->execute([$ownerId, $planKey]); $map = []; $meta = [];
    foreach ($stmt->fetchAll() as $row) {
        $data = json_decode((string)$row['timetables_json'], true);
        if (!is_array($data)) continue;
        $key = (string)$row['week_key']; $map[$key] = $data;
        $meta[$key] = ['updated_at' => $row['updated_at'], 'start_date' => $row['start_date'], 'end_date' => $row['end_date'], 'teacher_count' => count($data)];
    }
    return ['map' => $map, 'meta' => $meta];
}

function phancong_sync_weekly_timetables(PDO $pdo, int $ownerId, string $planKey, string $schoolYear, array $weeklyMap, int $userId, array $stateData = []): void
{
    $upsert = $pdo->prepare('INSERT INTO phancong_weekly_timetables (owner_id, plan_key, school_year, week_key, week_num, start_date, end_date, timetables_json, updated_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE school_year = VALUES(school_year), week_num = VALUES(week_num), start_date = VALUES(start_date), end_date = VALUES(end_date), timetables_json = VALUES(timetables_json), updated_by = VALUES(updated_by)');
    foreach ($weeklyMap as $key => $timetables) {
        if (!preg_match('/^W([1-9]\\d?)$/', (string)$key, $m) || !is_array($timetables) || !$timetables) continue;
        $week = (int)$m[1]; $monday = phancong_week_dates($schoolYear, $week, $stateData);
        $upsert->execute([$ownerId, $planKey, $schoolYear, $key, $week, $monday['start'], $monday['end'], json_encode($timetables, JSON_UNESCAPED_UNICODE), $userId]);
    }
}

function phancong_week_dates(string $schoolYear, int $week, array $stateData = []): array
{
    preg_match('/(20\\d{2})/', $schoolYear, $m); $year = (int)($m[1] ?? date('Y'));
    $configured = (string)($stateData['bao_giang']['start_date'] ?? '');
    $start = new DateTimeImmutable(preg_match('/^\d{4}-\d{2}-\d{2}$/', $configured) ? $configured : sprintf('%04d-09-05', $year));
    $start = $start->modify('monday this week')->modify('+' . max(0, $week - 1) . ' weeks');
    return ['start' => $start->format('Y-m-d'), 'end' => $start->modify('+6 days')->format('Y-m-d')];
}

try {
    phancong_maybe_ensure_schema($pdo);

    $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
    $action = $_GET['action'] ?? $_POST['action'] ?? '';
    if (!$action) {
        $action = ($method === 'POST') ? 'save' : 'get';
    }

    if ($action === 'get') {
        $currentUser = phancong_current_user($pdo, true);
        $ownerId = phancong_owner_id($currentUser);
        $planKey = trim((string)($_GET['plan_key'] ?? 'default'));
        if ($planKey === '') {
            $planKey = 'default';
        }

        $stmt = $pdo->prepare("SELECT id, plan_key, title, school_year, semester, data_json, created_by, updated_by, created_at, updated_at FROM phancong_chuyenmon WHERE owner_id = ? AND plan_key = ? ORDER BY updated_at DESC LIMIT 1");
        $stmt->execute([$ownerId, $planKey]);
        $row = $stmt->fetch();

        if (!$row || empty($row['data_json'])) {
            respond([
                'ok' => true,
                'data' => null,
                'plan' => null,
                'current_user' => phancong_public_user($currentUser),
                'message' => 'Chưa có dữ liệu phân công trên CSDL.'
            ]);
        }

        $parsedData = json_decode((string)$row['data_json'], true);
        if (!is_array($parsedData)) {
            $parsedData = null;
        }

        $loadedWeeks = phancong_load_weekly_timetables($pdo, $ownerId, $planKey);
        if (is_array($parsedData)) {
            if (!is_array($parsedData['weekly_timetables'] ?? null)) $parsedData['weekly_timetables'] = [];
            foreach ($loadedWeeks['map'] as $weekKey => $teachers) {
                foreach ($teachers as $tid => $tt) $parsedData['weekly_timetables'][$weekKey][(string)$tid] = $tt;
            }
        }
        respond([
            'ok' => true,
            'data' => $parsedData,
            'weekly_meta' => $loadedWeeks['meta'],
            'current_user' => phancong_public_user($currentUser),
            'plan' => [
                'id' => (int)$row['id'],
                'plan_key' => $row['plan_key'],
                'title' => $row['title'],
                'school_year' => $row['school_year'],
                'semester' => $row['semester'],
                'created_at' => $row['created_at'],
                'updated_at' => $row['updated_at']
            ]
        ]);
    }

    if ($action === 'system_data') {
        $currentUser = phancong_current_user($pdo, true);
        $ownerId = phancong_owner_id($currentUser);

        // 1. Lấy danh sách giáo viên từ bảng users
        $teachersStmt = $pdo->query("SELECT id, username, full_name, class_name, allowed_pages_json FROM users WHERE role = 'teacher' AND is_active = 1 ORDER BY full_name ASC");
        $dbTeachers = [];
        while ($t = $teachersStmt->fetch()) {
            $dbTeachers[] = [
                'id' => 'u_' . $t['id'],
                'user_id' => (int)$t['id'],
                'username' => $t['username'],
                'name' => $t['full_name'],
                'class_name' => $t['class_name'] ?? '',
                'role' => 'GV',
                'allowance' => 0,
                'qlpm' => false
            ];
        }

        // 2. Lấy danh sách lớp học thực tế từ học sinh trong users
        $classesStmt = $pdo->query("SELECT DISTINCT class_name FROM users WHERE role = 'student' AND is_active = 1 AND class_name IS NOT NULL AND TRIM(class_name) != '' ORDER BY class_name ASC");
        $dbClasses = [];
        while ($c = $classesStmt->fetch()) {
            $name = trim((string)$c['class_name']);
            if ($name !== '' && !in_array($name, $dbClasses, true)) {
                $dbClasses[] = $name;
            }
        }
        natsort($dbClasses);
        $dbClasses = array_values($dbClasses);

        // 3. Lấy danh sách các kế hoạch phân công đã lưu
        $plansStmt = $pdo->prepare("SELECT id, plan_key, title, school_year, semester, updated_at FROM phancong_chuyenmon WHERE owner_id = ? ORDER BY updated_at DESC");
        $plansStmt->execute([$ownerId]);
        $plans = $plansStmt->fetchAll();

        respond([
            'ok' => true,
            'teachers' => $dbTeachers,
            'classes' => $dbClasses,
            'plans' => $plans,
            'current_user' => phancong_public_user($currentUser)
        ]);
    }

    if ($action === 'get_week_timetable') {
        $currentUser = phancong_current_user($pdo, true);
        $ownerId = phancong_owner_id($currentUser);
        $planKey = trim((string)($_GET['source_plan_key'] ?? $_GET['plan_key'] ?? 'default')) ?: 'default';
        $weekKey = strtoupper(trim((string)($_GET['week_key'] ?? '')));
        if (!preg_match('/^W([1-9]\\d?)$/', $weekKey)) respond(['error' => 'Tuần TKB không hợp lệ.'], 422);
        $stmt = $pdo->prepare('SELECT timetables_json, school_year, start_date, end_date, updated_at FROM phancong_weekly_timetables WHERE owner_id = ? AND plan_key = ? AND week_key = ? LIMIT 1');
        $stmt->execute([$ownerId, $planKey, $weekKey]); $row = $stmt->fetch();
        if (!$row) respond(['ok' => true, 'data' => null, 'message' => 'Chưa có TKB tuần này trên CSDL.']);
        respond(['ok' => true, 'week_key' => $weekKey, 'plan_key' => $planKey, 'data' => json_decode((string)$row['timetables_json'], true), 'meta' => ['school_year' => $row['school_year'], 'start_date' => $row['start_date'], 'end_date' => $row['end_date'], 'updated_at' => $row['updated_at']]]);
    }

    if ($action === 'backup') {
        $currentUser = phancong_current_user($pdo, true);
        $ownerId = phancong_owner_id($currentUser);
        $userId = (int)($currentUser['id'] ?? 0);
        $body = json_body();
        $planKey = trim((string)($body['plan_key'] ?? $_GET['plan_key'] ?? 'default')) ?: 'default';
        $reason = trim((string)($body['reason'] ?? 'Sao lưu CSDL thủ công trước khi xử lý'));
        $backup = phancong_create_backup($pdo, $ownerId, $planKey, $reason, $userId, false);
        $stmt = $pdo->prepare("SELECT plan_key, title, school_year, semester, data_json, updated_at FROM phancong_chuyenmon WHERE owner_id = ? AND plan_key = ? LIMIT 1");
        $stmt->execute([$ownerId, $planKey]);
        $row = $stmt->fetch();
        $parsed = ($row && !empty($row['data_json'])) ? json_decode((string)$row['data_json'], true) : null;
        $loadedWeeks = phancong_load_weekly_timetables($pdo, $ownerId, $planKey);
        if (is_array($parsed)) {
            if (!is_array($parsed['weekly_timetables'] ?? null)) $parsed['weekly_timetables'] = [];
            foreach ($loadedWeeks['map'] as $wk => $teachers) {
                foreach ($teachers as $tid => $tt) $parsed['weekly_timetables'][$wk][(string)$tid] = $tt;
            }
        }
        if (!$backup) {
            respond(['error' => 'Chưa có dữ liệu trên CSDL để tạo bản sao lưu.'], 404);
        }
        respond([
            'ok' => true,
            'message' => 'Đã sao lưu CSDL an toàn trên máy chủ (Mã #' . $backup['id'] . ')!',
            'backup' => $backup,
            'snapshot' => $parsed,
        ]);
    }

    if ($action === 'list_backups') {
        $currentUser = phancong_current_user($pdo, true);
        $ownerId = phancong_owner_id($currentUser);
        $planKey = trim((string)($_GET['plan_key'] ?? 'default')) ?: 'default';
        $stmt = $pdo->prepare("SELECT id, plan_key, reason, school_year, semester, created_at FROM phancong_backups WHERE owner_id = ? AND plan_key = ? ORDER BY id DESC LIMIT 30");
        $stmt->execute([$ownerId, $planKey]);
        respond([
            'ok' => true,
            'backups' => $stmt->fetchAll() ?: [],
        ]);
    }

    if ($action === 'restore_backup') {
        $currentUser = phancong_current_user($pdo, true);
        $ownerId = phancong_owner_id($currentUser);
        $userId = (int)($currentUser['id'] ?? 0);
        $body = json_body();
        $backupId = (int)($body['backup_id'] ?? $_POST['backup_id'] ?? 0);
        if ($backupId <= 0) respond(['error' => 'Thiếu mã bản sao lưu cần khôi phục.'], 422);

        $stmt = $pdo->prepare("SELECT id, plan_key, reason, school_year, semester, data_json, weekly_json, created_at FROM phancong_backups WHERE id = ? AND owner_id = ? LIMIT 1");
        $stmt->execute([$backupId, $ownerId]);
        $backupRow = $stmt->fetch();
        if (!$backupRow) respond(['error' => 'Không tìm thấy bản sao lưu hợp lệ.'], 404);

        $planKey = (string)$backupRow['plan_key'];
        phancong_create_backup($pdo, $ownerId, $planKey, 'Tự động sao lưu trước khi khôi phục bản #' . $backupId, $userId, true);

        $restoredData = json_decode((string)$backupRow['data_json'], true);
        if (!is_array($restoredData)) respond(['error' => 'Dữ liệu trong bản sao lưu không hợp lệ.'], 500);
        $restoredWeekly = json_decode((string)($backupRow['weekly_json'] ?? '{}'), true);
        if (is_array($restoredWeekly) && $restoredWeekly) {
            if (!is_array($restoredData['weekly_timetables'] ?? null)) $restoredData['weekly_timetables'] = [];
            foreach ($restoredWeekly as $wk => $teachers) {
                if (!is_array($teachers)) continue;
                foreach ($teachers as $tid => $tt) $restoredData['weekly_timetables'][$wk][(string)$tid] = $tt;
            }
        }
        $cleanJson = json_encode($restoredData, JSON_UNESCAPED_UNICODE);
        $title = (string)($restoredData['info']['title'] ?? 'Phân công chuyên môn');
        $schoolYear = (string)($backupRow['school_year'] ?: ($restoredData['info']['school_year'] ?? ''));
        $semester = (string)($backupRow['semester'] ?: ($restoredData['info']['semester'] ?? 'HK1'));

        $check = $pdo->prepare("SELECT id FROM phancong_chuyenmon WHERE owner_id = ? AND plan_key = ? LIMIT 1");
        $check->execute([$ownerId, $planKey]);
        $existing = $check->fetch();
        if ($existing) {
            $upd = $pdo->prepare("UPDATE phancong_chuyenmon SET title = ?, school_year = ?, semester = ?, data_json = ?, updated_by = ?, updated_at = NOW() WHERE id = ? AND owner_id = ?");
            $upd->execute([$title, $schoolYear, $semester, $cleanJson, $userId, (int)$existing['id'], $ownerId]);
        } else {
            $ins = $pdo->prepare("INSERT INTO phancong_chuyenmon (owner_id, plan_key, title, school_year, semester, data_json, created_by, updated_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
            $ins->execute([$ownerId, $planKey, $title, $schoolYear, $semester, $cleanJson, $userId, $userId]);
        }
        $pdo->prepare("DELETE FROM phancong_weekly_timetables WHERE owner_id = ? AND plan_key = ?")->execute([$ownerId, $planKey]);
        if (is_array($restoredData['weekly_timetables'] ?? null)) {
            phancong_sync_weekly_timetables($pdo, $ownerId, $planKey, $schoolYear, $restoredData['weekly_timetables'], $userId, $restoredData);
        }
        respond([
            'ok' => true,
            'message' => 'Đã khôi phục CSDL từ bản sao lưu #' . $backupId . ' (' . $backupRow['created_at'] . ')!',
            'plan_key' => $planKey,
        ]);
    }

    if ($action === 'legacy_candidates') {
        $currentUser = phancong_current_user($pdo, true);
        $ownerId = phancong_owner_id($currentUser);
        $stmt = $pdo->prepare("SELECT id, plan_key, title, school_year, semester, created_at, updated_at,
            CASE WHEN created_by = ? THEN 'created_by' ELSE 'updated_by_only' END AS recovery_type
            FROM phancong_chuyenmon
            WHERE owner_id IS NULL AND (created_by = ? OR updated_by = ?)
            ORDER BY updated_at DESC, id DESC");
        $stmt->execute([$ownerId, $ownerId, $ownerId]);
        $candidates = $stmt->fetchAll();

        respond([
            'ok' => true,
            'candidates' => $candidates,
            'current_user' => phancong_public_user($currentUser),
        ]);
    }

    if ($action === 'recover_legacy') {
        $currentUser = phancong_current_user($pdo, true);
        $ownerId = phancong_owner_id($currentUser);
        $body = json_body();
        $legacyId = (int)($body['id'] ?? $_POST['id'] ?? 0);
        if ($legacyId <= 0) {
            respond(['error' => 'Thiếu mã dữ liệu cũ cần khôi phục.'], 422);
        }

        try {
            $pdo->beginTransaction();
            $candidateStmt = $pdo->prepare("SELECT id, plan_key, created_by, updated_by
                FROM phancong_chuyenmon
                WHERE id = ? AND owner_id IS NULL AND (created_by = ? OR updated_by = ?)
                FOR UPDATE");
            $candidateStmt->execute([$legacyId, $ownerId, $ownerId]);
            $candidate = $candidateStmt->fetch();
            if (!$candidate) {
                $pdo->rollBack();
                respond(['error' => 'Không tìm thấy dữ liệu cũ phù hợp để khôi phục.'], 404);
            }

            $conflictStmt = $pdo->prepare('SELECT id FROM phancong_chuyenmon WHERE owner_id = ? AND plan_key = ? LIMIT 1');
            $conflictStmt->execute([$ownerId, $candidate['plan_key']]);
            if ($conflictStmt->fetch()) {
                $pdo->rollBack();
                respond(['error' => 'Đã có kế hoạch cùng mã trong tài khoản này; dữ liệu cũ chưa được khôi phục.'], 409);
            }

            $recoverStmt = $pdo->prepare('UPDATE phancong_chuyenmon SET owner_id = ? WHERE id = ? AND owner_id IS NULL');
            $recoverStmt->execute([$ownerId, $legacyId]);
            if ($recoverStmt->rowCount() !== 1) {
                $pdo->rollBack();
                respond(['error' => 'Dữ liệu cũ đã thay đổi, vui lòng tải lại danh sách.'], 409);
            }
            $pdo->commit();

            respond([
                'ok' => true,
                'message' => 'Đã khôi phục kế hoạch cũ vào tài khoản của bạn.',
                'id' => $legacyId,
                'plan_key' => $candidate['plan_key'],
            ]);
        } catch (PDOException $e) {
            if ($pdo->inTransaction()) $pdo->rollBack();
            if ($e->getCode() === '23000') {
                respond(['error' => 'Đã có kế hoạch cùng mã trong tài khoản này; dữ liệu cũ chưa được khôi phục.'], 409);
            }
            throw $e;
        } catch (Throwable $e) {
            if ($pdo->inTransaction()) $pdo->rollBack();
            throw $e;
        }
    }

    if ($action === 'save') {
        $currentUser = phancong_current_user($pdo, true);
        $ownerId = phancong_owner_id($currentUser);
        $body = json_body();
        if (empty($body) && !empty($_POST)) {
            $body = $_POST;
        }

        $planKey = trim((string)($body['plan_key'] ?? 'default'));
        if ($planKey === '') {
            $planKey = 'default';
        }

        $title = trim((string)($body['title'] ?? 'Phân công chuyên môn'));
        if ($title === '') {
            $title = 'Phân công chuyên môn';
        }

        $schoolYear = trim((string)($body['school_year'] ?? ''));
        $semester = trim((string)($body['semester'] ?? 'HK1'));

        $data = $body['data'] ?? null;
        if ($data === null) {
            respond(['error' => 'Dữ liệu phân công (data) không được để trống.'], 400);
        }

        $incomingState = is_string($data) ? json_decode($data, true) : $data;
        if (!is_array($incomingState)) {
            respond(['error' => 'Dữ liệu phân công không hợp lệ.'], 400);
        }

        $userId = (int)($currentUser['id'] ?? 0);

        // Lock the previous state so a concurrent save cannot discard a weekly snapshot.
        $checkStmt = $pdo->prepare("SELECT id, data_json, updated_at FROM phancong_chuyenmon WHERE owner_id = ? AND plan_key = ? LIMIT 1");
        $checkStmt->execute([$ownerId, $planKey]);
        $existing = $checkStmt->fetch();

        $loadedWeeks = phancong_load_weekly_timetables($pdo, $ownerId, $planKey);
        $incomingState['weekly_timetables'] = is_array($incomingState['weekly_timetables'] ?? null) ? $incomingState['weekly_timetables'] : [];
        foreach ($loadedWeeks['map'] as $key => $teachers) {
            foreach ($teachers as $tid => $tt) if (!array_key_exists((string)$tid, $incomingState['weekly_timetables'][$key] ?? [])) $incomingState['weekly_timetables'][$key][(string)$tid] = $tt;
        }
        if ($existing) {
            $oldState = json_decode((string)$existing['data_json'], true) ?: [];
            $oldTimetables = phancong_extract_teacher_timetables($oldState);
            $newTimetables = phancong_extract_teacher_timetables($incomingState);
            $tkbOrPhaseChanged = (json_encode($oldTimetables) !== json_encode($newTimetables))
                || (json_encode($oldState['phases'] ?? []) !== json_encode($incomingState['phases'] ?? []))
                || (json_encode($oldState['phase_assignments'] ?? []) !== json_encode($incomingState['phase_assignments'] ?? []));
            if ($tkbOrPhaseChanged) {
                phancong_create_backup($pdo, $ownerId, $planKey, 'Tự động sao lưu trước khi cập nhật TKB / Đợt phân công', $userId, true);
            }
            $oldWeekKey = (string)($oldState['info']['active_timetable_week'] ?? '');
            if ($oldWeekKey === '') $oldWeekKey = phancong_infer_week_key($oldState, substr((string)$existing['updated_at'], 0, 10));
            if ($oldTimetables && preg_match('/^W[1-9]\\d?$/', $oldWeekKey) && empty($loadedWeeks['map'][$oldWeekKey]) && empty($incomingState['weekly_timetables'][$oldWeekKey])) {
                $incomingState['weekly_timetables'][$oldWeekKey] = $oldTimetables;
            }
        }
        $dataJson = json_encode($incomingState, JSON_UNESCAPED_UNICODE);
        if (!$dataJson || $dataJson === 'null') respond(['error' => 'Dữ liệu phân công không hợp lệ.'], 400);

        if ($existing) {
            $updateStmt = $pdo->prepare("UPDATE phancong_chuyenmon SET title = ?, school_year = ?, semester = ?, data_json = ?, updated_by = ?, updated_at = NOW() WHERE id = ? AND owner_id = ?");
            $updateStmt->execute([$title, $schoolYear, $semester, $dataJson, $userId, (int)$existing['id'], $ownerId]);
        } else {
            $insertStmt = $pdo->prepare("INSERT INTO phancong_chuyenmon (owner_id, plan_key, title, school_year, semester, data_json, created_by, updated_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
            $insertStmt->execute([$ownerId, $planKey, $title, $schoolYear, $semester, $dataJson, $userId, $userId]);
        }
        phancong_sync_weekly_timetables($pdo, $ownerId, $planKey, $schoolYear, $incomingState['weekly_timetables'], $userId, $incomingState);

        // Fetch updated record info
        $fetchStmt = $pdo->prepare("SELECT updated_at FROM phancong_chuyenmon WHERE owner_id = ? AND plan_key = ? LIMIT 1");
        $fetchStmt->execute([$ownerId, $planKey]);
        $updatedRow = $fetchStmt->fetch();
        $updatedAt = $updatedRow['updated_at'] ?? date('Y-m-d H:i:s');

        respond([
            'ok' => true,
            'message' => 'Đã lưu vào CSDL thành công!',
            'plan_key' => $planKey,
            'updated_at' => $updatedAt
        ]);
    }

    if ($action === 'reset') {
        $currentUser = phancong_current_user($pdo, true);
        $ownerId = phancong_owner_id($currentUser);
        $body = json_body();
        $planKey = trim((string)($body['plan_key'] ?? $_GET['plan_key'] ?? 'default'));
        if ($planKey === '') {
            $planKey = 'default';
        }

        $userId = (int)($currentUser['id'] ?? 0);
        phancong_create_backup($pdo, $ownerId, $planKey, 'Tự động sao lưu trước khi đặt lại CSDL', $userId, false);
        $pdo->prepare("DELETE FROM phancong_weekly_timetables WHERE owner_id = ? AND plan_key = ?")->execute([$ownerId, $planKey]);
        $stmt = $pdo->prepare("DELETE FROM phancong_chuyenmon WHERE owner_id = ? AND plan_key = ?");
        $stmt->execute([$ownerId, $planKey]);

        respond([
            'ok' => true,
            'message' => 'Đã đặt lại dữ liệu trong CSDL thành công!',
            'plan_key' => $planKey
        ]);
    }

    respond(['error' => 'Hành động không hợp lệ.'], 400);

} catch (Throwable $e) {
    respond(['error' => 'Lỗi máy chủ: ' . $e->getMessage()], 500);
}
