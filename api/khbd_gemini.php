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
// Không giữ khóa phiên trong khi chờ mạng; mọi key dùng chung một hạn chót.
session_write_close();
$deadline = microtime(true) + $timeout;
$transport = null;

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
    $remainingMs = (int)floor(($deadline - microtime(true)) * 1000);
    if ($remainingMs <= 0) break;
    $attempted++;
    $url = 'https://generativelanguage.googleapis.com/v1beta/models/' . rawurlencode($model) . ':generateContent?key=' . rawurlencode($key);
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_POSTFIELDS => $encoded,
        CURLOPT_CONNECTTIMEOUT_MS => min(10000, $remainingMs),
        CURLOPT_TIMEOUT_MS => min($perKeyTimeout * 1000, $remainingMs),
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    $curlErrno = curl_errno($ch);
    $transport = [
        'errno' => $curlErrno,
        'connect_ms' => (int)round(curl_getinfo($ch, CURLINFO_CONNECT_TIME) * 1000),
        'tls_ms' => (int)round(curl_getinfo($ch, CURLINFO_APPCONNECT_TIME) * 1000),
        'ttfb_ms' => (int)round(curl_getinfo($ch, CURLINFO_STARTTRANSFER_TIME) * 1000),
        'total_ms' => (int)round(curl_getinfo($ch, CURLINFO_TOTAL_TIME) * 1000),
    ];
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
        : ($curlErrno === 28 ? 'Hết thời gian chờ phản hồi Gemini. Chưa xác định được lỗi do kết nối hay thời gian xử lý.' : ($curlErrno ? 'Lỗi kết nối khi gọi Gemini (mã ' . $curlErrno . ').' : 'Gemini trả về dữ liệu không hợp lệ.'));
    // Không trả khóa API hoặc URL có khóa trong thông báo từ dịch vụ.
    foreach ($keys as $secret) $lastError = str_replace([$secret, rawurlencode($secret)], '[ẩn]', $lastError);
    $lastError = preg_replace('~https?://\S+~i', '[địa chỉ dịch vụ]', $lastError);
    if ($curlErrno === 28 || $curlErrno === 7 || khbd_gemini_should_rotate($lastStatus, $lastError)) {
        error_log('[khbd_gemini] retry key #' . ($keyIndex + 1) . '; HTTP ' . $lastStatus . '; ' . json_encode($transport));
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
    'code' => ($transport['errno'] ?? 0) === 28 ? 'GEMINI_TIMEOUT' : (($transport['errno'] ?? 0) ? 'GEMINI_TRANSPORT_ERROR' : 'GEMINI_RESPONSE_ERROR'),
    'diagnostics' => $transport,
], in_array($lastStatus, [400, 401, 403, 404, 429], true) ? $lastStatus : 502);
