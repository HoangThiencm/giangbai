<?php
require_once __DIR__ . '/db.php';

function json_body(): array
{
    $raw = file_get_contents('php://input');
    if (!$raw) return [];
    $data = json_decode($raw, true);
    return is_array($data) ? $data : [];
}

function respond(array $payload, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

function require_admin_key(): void
{
    $key = $_SERVER['HTTP_X_ADMIN_KEY'] ?? ($_GET['admin_key'] ?? '');
    if (!defined('ADMIN_KEY') || !hash_equals(ADMIN_KEY, $key)) {
        respond(['error' => 'Sai Admin Key hoặc không có quyền quản trị.'], 401);
    }
}

function page_catalog(): array
{
    return [
        'lotrinhtoan4' => ['title' => 'Lộ trình tự học Toán 4', 'url' => 'lotrinhtoan4.html'],
        'lotrinhtoan6' => ['title' => 'Lộ trình tự học Toán 6', 'url' => 'lotrinhtoan6.html'],
        'lotrinhtoan7' => ['title' => 'Lộ trình tự học Toán 7', 'url' => 'lotrinhtoan7.html'],
        'lotrinhtoan8' => ['title' => 'Lộ trình tự học Toán 8', 'url' => 'lotrinhtoan8.html'],
        'lotrinhtoan9' => ['title' => 'Lộ trình tự học Toán 9', 'url' => 'lotrinhtoan9.html'],
        'gslides' => ['title' => 'Trình chiếu Slides', 'url' => 'gslides.html'],
        'smartquiz' => ['title' => 'Soạn câu hỏi/Game AI', 'url' => 'smartquiz.html'],
        'thitructuyen' => ['title' => 'Thi Online', 'url' => 'thitructuyen.html'],
        'kttx' => ['title' => 'Đề kiểm tra thường xuyên', 'url' => 'kttx.html'],
        'rutgon' => ['title' => 'Link rút gọn & QR', 'url' => 'rutgon.html'],
        'theodoiai' => ['title' => 'Theo dõi AI lộ trình', 'url' => 'theodoi-ai.html'],
    ];
}

function normalize_pages($pages): array
{
    $catalog = page_catalog();
    $aliases = ['lotrinh' => 'lotrinhtoan6'];
    if (!is_array($pages)) return ['lotrinhtoan6'];
    $clean = [];
    foreach ($pages as $page) {
        $page = $aliases[$page] ?? $page;
        if (isset($catalog[$page])) $clean[] = $page;
    }
    return array_values(array_unique($clean)) ?: ['lotrinhtoan6'];
}

function lotrinh_page_subjects(): array
{
    return [
        'lotrinhtoan4' => 'Toán 4',
        'lotrinhtoan6' => 'Toán 6',
        'lotrinhtoan7' => 'Toán 7',
        'lotrinhtoan8' => 'Toán 8',
        'lotrinhtoan9' => 'Toán 9',
    ];
}

function subject_for_lotrinh_page(string $page): ?string
{
    return lotrinh_page_subjects()[$page] ?? null;
}

function lotrinh_route_order(): array
{
    return ['lotrinhtoan4', 'lotrinhtoan6', 'lotrinhtoan7', 'lotrinhtoan8', 'lotrinhtoan9'];
}

function ensure_teacher_lotrinh_scope(array $pages): array
{
    $pages = normalize_pages($pages);
    $lotrinhKeys = array_keys(lotrinh_page_subjects());
    $hasLotrinh = (bool) array_intersect($pages, $lotrinhKeys);
    if (!$hasLotrinh || in_array('lotrinhtoan4', $pages, true)) {
        return $pages;
    }

    $merged = array_values(array_unique(array_merge(['lotrinhtoan4'], $pages)));
    $order = array_flip(lotrinh_route_order());
    $lotrinh = [];
    $other = [];
    foreach ($merged as $page) {
        if (isset($order[$page])) {
            $lotrinh[] = $page;
        } else {
            $other[] = $page;
        }
    }
    usort($lotrinh, static fn(string $a, string $b): int => $order[$a] <=> $order[$b]);

    return array_merge($lotrinh, $other);
}

function maybe_upgrade_teacher_allowed_pages(PDO $pdo, array $user): array
{
    if (($user['role'] ?? '') !== 'teacher') {
        return $user;
    }

    $current = normalize_pages(json_decode($user['allowed_pages_json'] ?? '[]', true));
    $upgraded = ensure_teacher_lotrinh_scope($current);
    if ($upgraded === $current) {
        return $user;
    }

    $json = json_encode($upgraded, JSON_UNESCAPED_UNICODE);
    $pdo->prepare('UPDATE users SET allowed_pages_json = ? WHERE id = ?')
        ->execute([$json, (int)$user['id']]);
    $user['allowed_pages_json'] = $json;

    return $user;
}

function subjects_for_allowed_pages($pages): array
{
    $pages = normalize_pages(is_array($pages) ? $pages : []);
    $subjects = [];
    foreach ($pages as $page) {
        $subject = subject_for_lotrinh_page($page);
        if ($subject) {
            $subjects[] = $subject;
        }
    }
    return array_values(array_unique($subjects));
}

function infer_subject_from_class_name(string $className): ?string
{
    $name = trim($className);
    if ($name === '') {
        return null;
    }

    $subjects = array_values(lotrinh_page_subjects());
    usort($subjects, static fn(string $a, string $b): int => strlen($b) <=> strlen($a));
    foreach ($subjects as $subject) {
        if (mb_stripos($name, $subject) !== false) {
            return $subject;
        }
    }

    if (preg_match('/\b([4-9])[A-Za-z]{0,3}\b/u', $name, $matches)) {
        return 'Toán ' . $matches[1];
    }

    return null;
}

function class_subject_map_from_students(array $students): array
{
    $counts = [];
    foreach ($students as $student) {
        $class = trim((string)($student['class_name'] ?? ''));
        if ($class === '') {
            continue;
        }
        $pages = json_decode((string)($student['allowed_pages_json'] ?? '[]'), true);
        foreach (subjects_for_allowed_pages(is_array($pages) ? $pages : []) as $subject) {
            $counts[$class][$subject] = ($counts[$class][$subject] ?? 0) + 1;
        }
    }

    $map = [];
    foreach ($counts as $class => $subjectCounts) {
        if (!$subjectCounts) {
            continue;
        }
        arsort($subjectCounts);
        $map[$class] = (string) array_key_first($subjectCounts);
    }

    foreach ($students as $student) {
        $class = trim((string)($student['class_name'] ?? ''));
        if ($class === '' || isset($map[$class])) {
            continue;
        }
        $inferred = infer_subject_from_class_name($class);
        if ($inferred) {
            $map[$class] = $inferred;
        }
    }

    return $map;
}

function primary_lotrinh_page($pages): ?string
{
    $pages = normalize_pages(is_array($pages) ? $pages : []);
    foreach (lotrinh_route_order() as $page) {
        if (in_array($page, $pages, true)) {
            return $page;
        }
    }
    return null;
}

function normalize_teacher_class_name(string $raw): string
{
    $parts = preg_split('/[,;|]+/', trim($raw)) ?: [];
    $classes = [];
    foreach ($parts as $part) {
        $className = trim((string)$part);
        if ($className !== '') {
            $classes[] = $className;
        }
    }

    return implode(', ', array_values(array_unique($classes)));
}

function teacher_managed_classes(array $user): array
{
    if (($user['role'] ?? '') !== 'teacher') {
        return [];
    }

    $raw = trim((string)($user['class_name'] ?? ''));
    if ($raw === '') {
        return [];
    }

    $parts = preg_split('/[,;|]+/', $raw) ?: [];
    $classes = [];
    foreach ($parts as $part) {
        $className = trim((string)$part);
        if ($className !== '') {
            $classes[] = $className;
        }
    }

    return array_values(array_unique($classes));
}

function teacher_can_view_student_class(array $user, string $studentClass): bool
{
    $managedClasses = teacher_managed_classes($user);
    if (!$managedClasses) {
        return false;
    }

    $studentClass = trim($studentClass);
    if ($studentClass === '') {
        return false;
    }

    return in_array($studentClass, $managedClasses, true);
}

function teacher_allowed_subjects(array $user): array
{
    if (($user['role'] ?? '') !== 'teacher') {
        return [];
    }

    $pages = normalize_pages(json_decode($user['allowed_pages_json'] ?? '[]', true));
    $subjects = [];
    foreach ($pages as $page) {
        $subject = subject_for_lotrinh_page($page);
        if ($subject) {
            $subjects[] = $subject;
        }
    }

    return array_values(array_unique($subjects));
}

function teacher_can_manage_subject(?array $user, string $subject, bool $isAdmin = false): bool
{
    if ($isAdmin) {
        return true;
    }
    if (!$user || ($user['role'] ?? '') !== 'teacher') {
        return false;
    }

    $subject = trim($subject);
    if ($subject === '') {
        return false;
    }

    return in_array($subject, teacher_allowed_subjects($user), true);
}

function require_lesson_manager(bool $isAdmin, ?array $sessionUser, ?string $subject = null): void
{
    if (!$isAdmin && !$sessionUser) {
        respond(['error' => 'Chưa đăng nhập. Vui lòng đăng nhập lại qua trang Đăng nhập.'], 401);
    }

    $canManageLessons = $isAdmin || (($sessionUser['role'] ?? '') === 'teacher');
    if (!$canManageLessons) {
        respond(['error' => 'Tài khoản không có quyền soạn bài học.'], 403);
    }

    if ($subject !== null && !$isAdmin && !teacher_can_manage_subject($sessionUser, $subject, false)) {
        respond(['error' => 'Tài khoản không có quyền soạn bài học cho lộ trình này.'], 403);
    }
}

function account_duration_options(): array
{
    return [
        'forever' => 'Không giới hạn',
        '1_month' => '1 tháng',
        '3_months' => '3 tháng',
        '9_months' => '9 tháng',
        '1_year' => '1 năm',
    ];
}

function normalize_duration_option(?string $option): string
{
    $option = trim((string)$option);
    $options = account_duration_options();
    return array_key_exists($option, $options) ? $option : 'forever';
}

function resolve_account_expiry(?string $option, ?string $previousOption = null, ?string $currentExpiresAt = null): array
{
    $option = normalize_duration_option($option);
    if ($option === 'forever') {
        return ['expires_option' => 'forever', 'expires_at' => null];
    }

    if ($option === normalize_duration_option($previousOption) && !empty($currentExpiresAt)) {
        return ['expires_option' => $option, 'expires_at' => $currentExpiresAt];
    }

    $date = new DateTime('now');
    if ($option === '1_month') {
        $date->modify('+1 month');
    } elseif ($option === '3_months') {
        $date->modify('+3 months');
    } elseif ($option === '9_months') {
        $date->modify('+9 months');
    } elseif ($option === '1_year') {
        $date->modify('+1 year');
    }

    return ['expires_option' => $option, 'expires_at' => $date->format('Y-m-d H:i:s')];
}

function ensure_users_expires_option_column(PDO $pdo): void
{
    try {
        $stmt = $pdo->query("SHOW COLUMNS FROM users LIKE 'expires_option'");
        if (!$stmt->fetch()) {
            $pdo->exec("ALTER TABLE users ADD COLUMN expires_option VARCHAR(20) NOT NULL DEFAULT 'forever' AFTER expires_at");
        }
    } catch (Throwable $e) {
        // Column migration is best-effort for older databases.
    }
}

function public_user(array $user): array
{
    $pages = json_decode($user['allowed_pages_json'] ?? '[]', true);
    return [
        'id' => (int)$user['id'],
        'username' => $user['username'],
        'full_name' => $user['full_name'],
        'role' => $user['role'],
        'class_name' => $user['class_name'],
        'allowed_pages' => normalize_pages($pages),
        'is_active' => (bool)$user['is_active'],
        'expires_at' => $user['expires_at'],
        'expires_option' => normalize_duration_option($user['expires_option'] ?? 'forever'),
        'last_login_at' => $user['last_login_at'] ?? null,
        'created_at' => $user['created_at'] ?? null,
    ];
}
