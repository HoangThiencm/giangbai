<?php
require_once __DIR__ . '/helpers.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

const PHANCONG_SCHEMA_VERSION = '20260824-v1';

function phancong_current_user(PDO $pdo, bool $required = true): ?array
{
    $userId = (int)($_SESSION['user_id'] ?? 0);
    if ($userId <= 0) {
        if ($required) {
            respond(['error' => 'Vui lòng đăng nhập lại.'], 401);
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

    $allowedPages = teacher_allowed_pages_resolved($user);
    if (!in_array('phancongtochuyenmon', $allowedPages, true)) {
        if ($required) {
            respond(['error' => 'Tài khoản chưa được cấp quyền Phân công chuyên môn.'], 403);
        }
        return null;
    }

    return $user;
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

function phancong_ensure_schema(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS phancong_chuyenmon (
        id INT AUTO_INCREMENT PRIMARY KEY,
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
        INDEX idx_phancong_updated (updated_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");
}

try {
    phancong_maybe_ensure_schema($pdo);

    $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
    $action = $_GET['action'] ?? $_POST['action'] ?? '';
    if (!$action) {
        $action = ($method === 'POST') ? 'save' : 'get';
    }

    if ($action === 'get') {
        $currentUser = phancong_current_user($pdo, false);
        $planKey = trim((string)($_GET['plan_key'] ?? 'default'));
        if ($planKey === '') {
            $planKey = 'default';
        }

        $stmt = $pdo->prepare("SELECT id, plan_key, title, school_year, semester, data_json, created_by, updated_by, created_at, updated_at FROM phancong_chuyenmon WHERE plan_key = ? ORDER BY updated_at DESC LIMIT 1");
        $stmt->execute([$planKey]);
        $row = $stmt->fetch();

        if (!$row || empty($row['data_json'])) {
            respond([
                'ok' => true,
                'data' => null,
                'plan' => null,
                'message' => 'Chưa có dữ liệu phân công trên CSDL.'
            ]);
        }

        $parsedData = json_decode((string)$row['data_json'], true);
        if (!is_array($parsedData)) {
            $parsedData = null;
        }

        respond([
            'ok' => true,
            'data' => $parsedData,
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
        $currentUser = phancong_current_user($pdo, false);

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
        $plansStmt = $pdo->query("SELECT id, plan_key, title, school_year, semester, updated_at FROM phancong_chuyenmon ORDER BY updated_at DESC");
        $plans = $plansStmt->fetchAll();

        respond([
            'ok' => true,
            'teachers' => $dbTeachers,
            'classes' => $dbClasses,
            'plans' => $plans,
            'current_user' => $currentUser ? [
                'id' => (int)$currentUser['id'],
                'username' => $currentUser['username'],
                'full_name' => $currentUser['full_name'],
                'role' => $currentUser['role']
            ] : null
        ]);
    }

    if ($action === 'save') {
        $currentUser = phancong_current_user($pdo, true);
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

        $dataJson = is_string($data) ? $data : json_encode($data, JSON_UNESCAPED_UNICODE);
        if (!$dataJson || $dataJson === 'null') {
            respond(['error' => 'Dữ liệu phân công không hợp lệ.'], 400);
        }

        $userId = (int)($currentUser['id'] ?? 0);

        // Check if plan_key exists
        $checkStmt = $pdo->prepare("SELECT id FROM phancong_chuyenmon WHERE plan_key = ? LIMIT 1");
        $checkStmt->execute([$planKey]);
        $existing = $checkStmt->fetch();

        if ($existing) {
            $updateStmt = $pdo->prepare("UPDATE phancong_chuyenmon SET title = ?, school_year = ?, semester = ?, data_json = ?, updated_by = ?, updated_at = NOW() WHERE id = ?");
            $updateStmt->execute([$title, $schoolYear, $semester, $dataJson, $userId, (int)$existing['id']]);
        } else {
            $insertStmt = $pdo->prepare("INSERT INTO phancong_chuyenmon (plan_key, title, school_year, semester, data_json, created_by, updated_by) VALUES (?, ?, ?, ?, ?, ?, ?)");
            $insertStmt->execute([$planKey, $title, $schoolYear, $semester, $dataJson, $userId, $userId]);
        }

        // Fetch updated record info
        $fetchStmt = $pdo->prepare("SELECT updated_at FROM phancong_chuyenmon WHERE plan_key = ? LIMIT 1");
        $fetchStmt->execute([$planKey]);
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
        $body = json_body();
        $planKey = trim((string)($body['plan_key'] ?? $_GET['plan_key'] ?? 'default'));
        if ($planKey === '') {
            $planKey = 'default';
        }

        $stmt = $pdo->prepare("DELETE FROM phancong_chuyenmon WHERE plan_key = ?");
        $stmt->execute([$planKey]);

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
