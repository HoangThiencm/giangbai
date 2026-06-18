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
        'lotrinhtoan6' => ['title' => 'Lộ trình tự học Toán 6', 'url' => 'lotrinhtoan6.html'],
        'lotrinhtoan7' => ['title' => 'Lộ trình tự học Toán 7', 'url' => 'lotrinhtoan7.html'],
        'lotrinhtoan8' => ['title' => 'Lộ trình tự học Toán 8', 'url' => 'lotrinhtoan8.html'],
        'lotrinhtoan9' => ['title' => 'Lộ trình tự học Toán 9', 'url' => 'lotrinhtoan9.html'],
        'gslides' => ['title' => 'Trình chiếu Slides', 'url' => 'gslides.html'],
        'smartquiz' => ['title' => 'Soạn câu hỏi/Game AI', 'url' => 'smartquiz.html'],
        'thitructuyen' => ['title' => 'Thi Online', 'url' => 'thitructuyen.html'],
        'kttx' => ['title' => 'Đề kiểm tra thường xuyên', 'url' => 'kttx.html'],
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
        'last_login_at' => $user['last_login_at'] ?? null,
        'created_at' => $user['created_at'] ?? null,
    ];
}
