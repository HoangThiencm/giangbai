<?php
/** Gemini proxy for Canvas. Keys remain exclusively on the server. */
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/ai_runtime_config.php';

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'OPTIONS') { http_response_code(204); exit; }

function canvas_gemini_call(string $model, string $key, string $encoded, int $timeout): array {
    $url = 'https://generativelanguage.googleapis.com/v1beta/models/' . rawurlencode($model) . ':generateContent?key=' . rawurlencode($key);
    $ch = curl_init($url);
    $connectTimeout = min(10, max(1, $timeout - 1));
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_POST => true, CURLOPT_HTTPHEADER => ['Content-Type: application/json'], CURLOPT_POSTFIELDS => $encoded, CURLOPT_CONNECTTIMEOUT => $connectTimeout, CURLOPT_TIMEOUT => max(1, $timeout)]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);
    $decoded = is_string($raw) && $raw !== '' ? json_decode($raw, true) : null;
    $error = is_array($decoded) ? (string)($decoded['error']['message'] ?? ('Gemini HTTP ' . $status)) : ($curlError !== '' ? 'Máy chủ không gọi được Gemini: ' . $curlError : 'Gemini trả về dữ liệu không hợp lệ.');
    return ['ok' => is_array($decoded) && $status >= 200 && $status < 300, 'body' => $decoded, 'status' => $status ?: 502, 'error' => $error];
}

function canvas_model(string $value): string {
    $value = trim($value);
    return preg_match('/^gemini-[a-z0-9._-]+$/i', $value) ? $value : 'gemini-3-flash-preview';
}

$method = $_SERVER['REQUEST_METHOD'] ?? '';
if ($method !== 'POST') respond(['ok' => false, 'error' => 'Method not allowed.'], 405);
$body = json_body();
$payload = $body['payload'] ?? null;
if (!is_array($payload) || empty($payload['contents'])) respond(['ok' => false, 'error' => 'Thiếu nội dung gửi Gemini.'], 422);
$encoded = json_encode($payload, JSON_UNESCAPED_UNICODE);
if (!is_string($encoded) || strlen($encoded) > 8 * 1024 * 1024) respond(['ok' => false, 'error' => 'Tài liệu quá lớn để Canvas gửi tới Gemini.'], 413);

$runtime = load_ai_runtime_config();
$systemKeys = $runtime['gemini_keys'] ?? [];
$systemAvailable = !empty($runtime['gemini_enabled']) && !empty($systemKeys);
if (!$systemAvailable) respond(['ok' => false, 'error' => 'Gemini Canvas chưa được Admin cấu hình khóa hệ thống.', 'meta' => ['tier' => 'system', 'route' => 'system_unavailable', 'fallback_used' => false, 'system_key_available' => false]], 503);

// preferred_model is the current Canvas contract; model is accepted for older Canvas pages.
$preferredModel = canvas_model((string)($body['preferred_model'] ?? $body['model'] ?? 'gemini-3-flash-preview'));
$timeout = max(10, min(85, (int)($body['timeout'] ?? 85)));
$deadline = microtime(true) + $timeout;
$last = ['status' => 502, 'error' => 'Không gọi được Gemini Canvas.'];

foreach ($systemKeys as $key) {
    // All system keys share this single request budget, rather than each key
    // receiving a fresh long cURL timeout.
    $remaining = (int)floor($deadline - microtime(true));
    if ($remaining < 2) {
        respond(['ok' => false, 'error' => 'Gemini Canvas đã hết thời hạn xử lý chung. Hãy giảm số trang SGK hoặc thử lại.', 'meta' => ['tier' => 'system_key', 'route' => 'system_deadline', 'model' => $preferredModel, 'fallback_used' => false, 'system_key_available' => true]], 504);
    }
    $attemptTimeout = min(55, max(1, $remaining));
    $attempt = canvas_gemini_call($preferredModel, $key, $encoded, $attemptTimeout);
    if ($attempt['ok']) {
        respond([
            'ok' => true,
            // Unmodified Gemini body lets the frontend read candidates and safety diagnostics.
            'body' => $attempt['body'],
            'model' => $preferredModel,
            'tier' => 'system_key',
            'fallback_used' => false,
            'system_key_available' => true,
            'meta' => ['tier' => 'system_key', 'route' => 'system', 'model' => $preferredModel, 'fallback_used' => false, 'system_key_available' => true]
        ]);
    }
    $last = $attempt;
}

if (microtime(true) >= $deadline) {
    respond(['ok' => false, 'error' => 'Gemini Canvas đã hết thời hạn xử lý chung. Hãy giảm số trang SGK hoặc thử lại.', 'meta' => ['tier' => 'system_key', 'route' => 'system_deadline', 'model' => $preferredModel, 'fallback_used' => false, 'system_key_available' => true]], 504);
}

respond([
    'ok' => false,
    'error' => $last['error'],
    'meta' => ['tier' => 'system_key', 'route' => 'system_failed', 'model' => $preferredModel, 'fallback_used' => false, 'system_key_available' => true]
], $last['status'] >= 400 && $last['status'] < 500 ? $last['status'] : 502);
