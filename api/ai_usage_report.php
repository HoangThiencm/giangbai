<?php
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/ai_usage_log.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(['error' => 'Method not allowed.'], 405);
}

$key = $_SERVER['HTTP_X_ADMIN_KEY'] ?? ($_GET['admin_key'] ?? '');
$isAdmin = defined('ADMIN_KEY') && is_string(ADMIN_KEY) && ADMIN_KEY !== '' && hash_equals(ADMIN_KEY, (string)$key);

$sessionOk = false;
if (!$isAdmin && !empty($_SESSION['user_id'])) {
    $userStmt = $pdo->prepare('SELECT is_active FROM users WHERE id = ? LIMIT 1');
    $userStmt->execute([(int)$_SESSION['user_id']]);
    $user = $userStmt->fetch();
    $sessionOk = $user && (bool)$user['is_active'];
}

if (!$isAdmin && !$sessionOk) {
    respond(['error' => 'Cần đăng nhập để ghi log AI (Mistral/Gemini trình duyệt).'], 403);
}

$data = json_body();
$provider = trim((string)($data['provider'] ?? ''));
if ($provider === '' || !in_array($provider, ai_usage_allowed_providers(), true)) {
    respond(['error' => 'Provider không hợp lệ.'], 422);
}

$module = ai_usage_normalize_module((string)($data['module'] ?? 'other'));
$mode = ai_usage_normalize_mode((string)($data['mode'] ?? 'explain'));
$model = trim((string)($data['model'] ?? ''));
$ok = !empty($data['ok']);

ai_usage_record([
    'provider' => $provider,
    'module' => $module,
    'mode' => $mode,
    'model' => $model,
    'ok' => $ok,
    'fallback' => !empty($data['fallback']),
    'prompt_tokens' => max(0, (int)($data['prompt_tokens'] ?? 0)),
    'completion_tokens' => max(0, (int)($data['completion_tokens'] ?? 0)),
    'total_tokens' => max(0, (int)($data['total_tokens'] ?? 0)),
    'estimated_usd' => isset($data['estimated_usd']) ? (float)$data['estimated_usd'] : 0.0,
    'error' => $ok ? '' : trim((string)($data['error'] ?? 'Lỗi không xác định')),
]);

respond(['ok' => true]);