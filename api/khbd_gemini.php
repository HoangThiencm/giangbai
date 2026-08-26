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

$key = trim((string)($body['key'] ?? ''));
if (strlen($key) <= 10) {
    $stmt = $pdo->prepare('SELECT gemini_keys FROM users WHERE id = ? LIMIT 1');
    $stmt->execute([(int)$_SESSION['user_id']]);
    $row = $stmt->fetch() ?: [];
    $stored = parse_stored_api_keys($row['gemini_keys'] ?? null);
    $key = $stored[0] ?? '';
}
if (strlen($key) <= 10) {
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

$url = 'https://generativelanguage.googleapis.com/v1beta/models/' . rawurlencode($model) . ':generateContent?key=' . rawurlencode($key);
$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
    CURLOPT_POSTFIELDS => $encoded,
    CURLOPT_CONNECTTIMEOUT => 10,
    CURLOPT_TIMEOUT => $timeout,
]);
$raw = curl_exec($ch);
$status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlError = curl_error($ch);
curl_close($ch);

if ($raw === false || $raw === '') {
    respond([
        'ok' => false,
        'status' => 0,
        'error' => $curlError !== ''
            ? ('Máy chủ cũng không tới được Gemini: ' . $curlError)
            : 'Máy chủ không nhận được phản hồi từ Gemini.',
        'via' => 'server',
    ], 502);
}

$decoded = json_decode($raw, true);
if (!is_array($decoded)) {
    respond([
        'ok' => false,
        'status' => $status,
        'error' => 'Gemini trả về dữ liệu không hợp lệ.',
        'via' => 'server',
    ], 502);
}

respond([
    'ok' => $status >= 200 && $status < 300,
    'status' => $status,
    'body' => $decoded,
    'via' => 'server',
], $status >= 200 && $status < 300 ? 200 : (in_array($status, [400, 401, 403, 404, 429], true) ? $status : 502));
