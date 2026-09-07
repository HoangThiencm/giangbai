<?php
/**
 * Proxy Gemini cho soạn KHBD: khi trình duyệt không tới được
 * generativelanguage.googleapis.com thì gọi từ máy chủ.
 * Dùng đúng API key của user (gửi kèm hoặc lấy từ CSDL).
 */
require_once __DIR__ . '/helpers.php';
session_start();

if (empty($_SESSION['user_id'])) {
    respond(['error' => 'Chưa đăng nhập.'], 401);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(['error' => 'Method not allowed.'], 405);
}

ensure_users_ai_key_columns($pdo);
$body = json_body();

$model = trim((string)($body['model'] ?? 'gemini-2.5-flash'));
if (!preg_match('/^gemini-[a-z0-9._-]+$/i', $model)) {
    respond(['ok' => false, 'error' => 'Model Gemini không hợp lệ.'], 422);
}

$requestedKey = trim((string)($body['key'] ?? ''));
$keys = [];
if (strlen($requestedKey) > 10) {
    $keys = [$requestedKey];
} else {
    $stmt = $pdo->prepare('SELECT gemini_keys FROM users WHERE id = ? LIMIT 1');
    $stmt->execute([(int)$_SESSION['user_id']]);
    $row = $stmt->fetch() ?: [];
    $keys = parse_stored_api_keys($row['gemini_keys'] ?? null);
}
if (!$keys) {
    respond(['ok' => false, 'error' => 'Thiếu Gemini API Key của tài khoản.'], 422);
}

$payload = $body['payload'] ?? null;
if (!is_array($payload) || empty($payload['contents'])) {
    respond(['ok' => false, 'error' => 'Thiếu nội dung gửi Gemini.'], 422);
}

$encoded = json_encode($payload, JSON_UNESCAPED_UNICODE);
if (!is_string($encoded) || strlen($encoded) > 8 * 1024 * 1024) {
    respond(['ok' => false, 'error' => 'Payload Gemini quá lớn để gửi qua máy chủ. Hãy Đọc nội dung SGK (Mistral) trước.'], 413);
}

$timeout = (int)($body['timeout'] ?? 60);
$timeout = max(10, min(90, $timeout));

function khbd_gemini_should_rotate(int $status, string $error): bool
{
    if (in_array($status, [403, 429], true)) return true;
    $message = strtolower($error);
    return str_contains($message, 'quota')
        || str_contains($message, 'resource exhausted')
        || str_contains($message, 'rate limit')
        || str_contains($message, 'too many requests')
        || str_contains($message, 'operation timed out')
        || str_contains($message, 'timed out')
        || str_contains($message, 'could not connect');
}

$lastStatus = 502;
$lastError = 'Máy chủ không nhận được phản hồi từ Gemini.';
$attempted = 0;
$perKeyTimeout = count($keys) > 1 ? min($timeout, 40) : $timeout;

foreach ($keys as $keyIndex => $key) {
    $attempted++;
    $url = 'https://generativelanguage.googleapis.com/v1beta/models/' . rawurlencode($model) . ':generateContent?key=' . rawurlencode($key);
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_POSTFIELDS => $encoded,
        CURLOPT_CONNECTTIMEOUT => 10,
        CURLOPT_TIMEOUT => $perKeyTimeout,
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);

    $decoded = is_string($raw) && $raw !== '' ? json_decode($raw, true) : null;
    if (is_array($decoded) && $status >= 200 && $status < 300) {
        respond([
            'ok' => true,
            'status' => $status,
            'body' => $decoded,
            'via' => 'server',
            'key_attempt' => $attempted,
        ]);
    }

    $lastStatus = $status ?: 502;
    $lastError = is_array($decoded)
        ? (string)($decoded['error']['message'] ?? ('Gemini HTTP ' . $lastStatus))
        : ($curlError !== '' ? ('Máy chủ cũng không tới được Gemini: ' . $curlError) : 'Gemini trả về dữ liệu không hợp lệ.');
    if (khbd_gemini_should_rotate($lastStatus, $lastError)) {
        error_log('[khbd_gemini] quota/rate limit on key #' . ($keyIndex + 1) . '; trying next key');
        continue;
    }
    break;
}

respond([
    'ok' => false,
    'status' => $lastStatus,
    'error' => $lastError,
    'via' => 'server',
    'key_attempts' => $attempted,
], in_array($lastStatus, [400, 401, 403, 404, 429], true) ? $lastStatus : 502);
