<?php
require_once __DIR__ . '/helpers.php';
if (session_status() === PHP_SESSION_NONE) { session_start(); }
if (empty($_SESSION['user_id'])) { respond(['ok' => false, 'error' => 'Chưa đăng nhập.'], 401); }
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { respond(['ok' => false, 'error' => 'Method not allowed.'], 405); }

set_time_limit(180);
$body = json_body();
$text = trim((string)($body['text'] ?? ''));
if ($text === '') { respond(['ok' => false, 'error' => 'Hãy nhập văn bản cần kiểm tra.'], 422); }
if ((function_exists('mb_strlen') ? mb_strlen($text) : strlen($text)) > 30000) {
    respond(['ok' => false, 'error' => 'Mỗi lần kiểm tra tối đa 30.000 ký tự.'], 413);
}

function spelling_keys(PDO $pdo, int $userId): array {
    $stmt = $pdo->prepare('SELECT gemini_keys FROM users WHERE id = ? LIMIT 1');
    $stmt->execute([$userId]);
    $raw = ($stmt->fetch() ?: [])['gemini_keys'] ?? null;
    $keys = parse_stored_api_keys($raw);
    if ($raw && stored_api_keys_need_encryption($raw) && $keys) {
        save_user_key_column($pdo, $userId, 'gemini_keys', $keys);
    }
    return $keys;
}
function spelling_rotatable(int $status, string $message): bool {
    $message = strtolower($message);
    return in_array($status, [403, 429], true) || str_contains($message, 'quota') || str_contains($message, 'resource exhausted') || str_contains($message, 'rate limit');
}
function spelling_gemini(array $keys, array $payload): array {
    $models = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash'];
    $encoded = json_encode($payload, JSON_UNESCAPED_UNICODE);
    $last = ['ok' => false, 'status' => 502, 'error' => 'Không gọi được Gemini.'];
    foreach ($models as $model) foreach ($keys as $keyIndex => $key) {
        $url = 'https://generativelanguage.googleapis.com/v1beta/models/' . rawurlencode($model) . ':generateContent?key=' . rawurlencode($key);
        $ch = curl_init($url);
        curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_POST => true, CURLOPT_HTTPHEADER => ['Content-Type: application/json'], CURLOPT_POSTFIELDS => $encoded, CURLOPT_CONNECTTIMEOUT => 12, CURLOPT_TIMEOUT => 100]);
        $raw = curl_exec($ch); $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE); $curlError = curl_error($ch); curl_close($ch);
        $decoded = is_string($raw) ? json_decode($raw, true) : null;
        if ($status >= 200 && $status < 300 && is_array($decoded)) return ['ok' => true, 'body' => $decoded, 'model' => $model, 'key_index' => $keyIndex];
        $message = is_array($decoded) ? (string)($decoded['error']['message'] ?? "Gemini HTTP $status") : ($curlError ?: "Gemini HTTP $status");
        $last = ['ok' => false, 'status' => $status ?: 502, 'error' => $message];
        // A model can be absent for a key/project even though another fallback model works.
        if ($status === 404 || str_contains(strtolower($message), 'not found') || str_contains(strtolower($message), 'not available')) continue;
        if (!spelling_rotatable($status, $message)) return $last;
    }
    return $last;
}

ensure_users_ai_key_columns($pdo);
$keys = spelling_keys($pdo, (int)$_SESSION['user_id']);
if (!$keys) { respond(['ok' => false, 'error' => 'Tài khoản chưa có Gemini API Key cá nhân.'], 422); }
$options = is_array($body['options'] ?? null) ? $body['options'] : [];
$checks = [];
if (!empty($options['spelling'])) $checks[] = 'lỗi chính tả và lỗi gõ phím';
if (!empty($options['context'])) $checks[] = 'từ dùng sai ngữ cảnh';
if (!empty($options['punctuation'])) $checks[] = 'dấu câu và khoảng trắng';
if (!$checks) $checks[] = 'lỗi chính tả, lỗi gõ phím, từ sai ngữ cảnh, dấu câu và khoảng trắng';
$schema = ['type' => 'OBJECT', 'properties' => [
    'errors' => ['type' => 'ARRAY', 'items' => ['type' => 'OBJECT', 'properties' => [
        'original_text' => ['type' => 'STRING'], 'suggested_text' => ['type' => 'STRING'], 'error_type' => ['type' => 'STRING'],
        'explanation' => ['type' => 'STRING'], 'context' => ['type' => 'STRING']
    ], 'required' => ['original_text', 'suggested_text', 'error_type', 'explanation', 'context']]]
], 'required' => ['errors']];
$prompt = "Bạn là trợ lý soát lỗi tiếng Việt. Chỉ tìm các lỗi: " . implode(', ', $checks) . ". KHÔNG viết lại câu, KHÔNG thay đổi văn phong, KHÔNG đề xuất nếu không chắc chắn. Với mỗi lỗi, original_text phải là đúng chuỗi xuất hiện nguyên văn, suggested_text chỉ thay phần lỗi. Trả JSON theo schema. Văn bản:\n---\n" . $text . "\n---";
$result = spelling_gemini($keys, ['contents' => [['role' => 'user', 'parts' => [['text' => $prompt]]]], 'generationConfig' => ['temperature' => 0.1, 'responseMimeType' => 'application/json', 'responseSchema' => $schema]]);
if (!$result['ok']) respond(['ok' => false, 'error' => $result['error']], max(400, min(599, (int)$result['status'])));
$parts = $result['body']['candidates'][0]['content']['parts'] ?? [];
$raw = ''; foreach ($parts as $part) if (isset($part['text'])) $raw .= $part['text'];
$data = json_decode(trim($raw), true);
if (!is_array($data)) respond(['ok' => false, 'error' => 'Gemini trả về dữ liệu không đúng định dạng.'], 502);
$errors = [];
foreach (($data['errors'] ?? []) as $item) {
    if (!is_array($item)) continue;
    $from = trim((string)($item['original_text'] ?? '')); $to = trim((string)($item['suggested_text'] ?? ''));
    if ($from === '' || $to === '' || $from === $to || !str_contains($text, $from)) continue;
    $errors[] = ['original_text' => $from, 'suggested_text' => $to, 'error_type' => trim((string)($item['error_type'] ?? 'Lỗi chính tả')), 'explanation' => trim((string)($item['explanation'] ?? '')), 'context' => trim((string)($item['context'] ?? ''))];
}
respond(['ok' => true, 'errors' => $errors, 'model' => $result['model']]);
