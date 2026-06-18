<?php
require_once __DIR__ . '/helpers.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(['error' => 'Method not allowed.'], 405);
}

$data = json_body();
$text = trim($data['text'] ?? '');
$lessonTitle = trim($data['lesson_title'] ?? 'bài học');
$subject = trim($data['subject'] ?? 'Toán');

if ($text === '') {
    respond(['error' => 'Thiếu nội dung cần giải thích.'], 422);
}

if (!defined('GEMINI_API_KEYS') || empty(GEMINI_API_KEYS)) {
    respond(['error' => 'AI chưa được cấu hình trên hosting.'], 503);
}

$keys = GEMINI_API_KEYS;
if (is_string($keys)) {
    $keys = array_filter(array_map('trim', explode(',', $keys)));
}
if (!is_array($keys) || empty($keys)) {
    respond(['error' => 'AI chưa có Gemini API key hợp lệ.'], 503);
}

$model = defined('GEMINI_MODEL') ? GEMINI_MODEL : 'gemini-2.5-flash';
$prompt = "Bạn là trợ lý học Toán cho học sinh THCS. Hãy giải thích thật dễ hiểu, ngắn gọn, dùng tiếng Việt, không làm thay toàn bộ bài nếu là bài tập.\n\nMôn: {$subject}\nBài: {$lessonTitle}\nNội dung học sinh chưa hiểu:\n{$text}\n\nTrả lời theo 3 phần ngắn: Ý chính, Giải thích dễ hiểu, Ví dụ nhỏ.";

$payload = json_encode([
    'contents' => [[
        'parts' => [[ 'text' => $prompt ]]
    ]],
    'generationConfig' => [
        'temperature' => 0.35,
        'maxOutputTokens' => 700,
    ],
], JSON_UNESCAPED_UNICODE);

$lastError = 'Không gọi được AI.';
foreach ($keys as $key) {
    $url = 'https://generativelanguage.googleapis.com/v1beta/models/' . rawurlencode($model) . ':generateContent?key=' . rawurlencode($key);
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_TIMEOUT => 25,
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);

    if ($raw === false || $raw === '') {
        $lastError = $curlError ?: 'AI không phản hồi.';
        continue;
    }

    $response = json_decode($raw, true);
    if ($status >= 200 && $status < 300) {
        $parts = $response['candidates'][0]['content']['parts'] ?? [];
        $answer = '';
        foreach ($parts as $part) {
            if (!empty($part['text'])) $answer .= $part['text'];
        }
        if (trim($answer) !== '') {
            respond(['ok' => true, 'answer' => trim($answer)]);
        }
        $lastError = 'AI trả về nội dung rỗng.';
        continue;
    }

    $lastError = $response['error']['message'] ?? ('AI lỗi HTTP ' . $status);
}

respond(['error' => $lastError], 502);
