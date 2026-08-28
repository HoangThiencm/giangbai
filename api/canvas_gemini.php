<?php
/**
 * Gemini runtime dành riêng cho canvas_soankhbd.html.
 * Key chỉ nằm trong api/config.php hoặc global_config.json do Admin quản lý;
 * người dùng Canvas không gửi, không thấy và không lưu API key cá nhân.
 */
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/ai_runtime_config.php';

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(['ok' => false, 'error' => 'Method not allowed.'], 405);
}

$body = json_body();
$payload = $body['payload'] ?? null;
if (!is_array($payload) || empty($payload['contents'])) {
    respond(['ok' => false, 'error' => 'Thiếu nội dung gửi Gemini.'], 422);
}

$encoded = json_encode($payload, JSON_UNESCAPED_UNICODE);
if (!is_string($encoded) || strlen($encoded) > 8 * 1024 * 1024) {
    respond(['ok' => false, 'error' => 'Tài liệu quá lớn để Canvas gửi tới Gemini.'], 413);
}

$runtime = load_ai_runtime_config();
$keys = $runtime['gemini_keys'] ?? [];
if (empty($runtime['gemini_enabled']) || empty($keys)) {
    respond(['ok' => false, 'error' => 'Gemini Canvas chưa được Admin cấu hình khóa hệ thống.'], 503);
}

// Model Canvas do Admin cấu hình trên máy chủ quyết định, không nhận từ trình duyệt.
$model = trim((string)($runtime['gemini_model'] ?? 'gemini-2.5-flash'));
if (!preg_match('/^gemini-[a-z0-9._-]+$/i', $model)) {
    $model = 'gemini-2.5-flash';
}
$timeout = max(10, min(90, (int)($body['timeout'] ?? 75)));
$lastStatus = 502;
$lastError = 'Không gọi được Gemini Canvas.';

foreach ($keys as $key) {
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

    if (is_string($raw) && $raw !== '') {
        $decoded = json_decode($raw, true);
        if (is_array($decoded) && $status >= 200 && $status < 300) {
            respond(['ok' => true, 'body' => $decoded, 'model' => $model]);
        }
        $lastError = is_array($decoded)
            ? (string)($decoded['error']['message'] ?? ('Gemini HTTP ' . $status))
            : ('Gemini trả về dữ liệu không hợp lệ.');
        $lastStatus = $status ?: 502;
    } elseif ($curlError !== '') {
        $lastError = 'Máy chủ không gọi được Gemini: ' . $curlError;
    }
}

respond(['ok' => false, 'error' => $lastError], $lastStatus >= 400 && $lastStatus < 500 ? $lastStatus : 502);
