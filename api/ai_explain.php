<?php
require_once __DIR__ . '/helpers.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(['error' => 'Method not allowed.'], 405);
}

$data = json_body();
$text = trim($data['text'] ?? '');
$lessonTitle = trim($data['lesson_title'] ?? 'bai hoc');
$subject = trim($data['subject'] ?? 'Toan');

if ($text === '') {
    respond(['error' => 'Thieu noi dung can giai thich.'], 422);
}

function normalize_gemini_keys($value): array
{
    if (is_string($value)) {
        $value = preg_split('/[\s,]+/', $value) ?: [];
    }
    if (!is_array($value)) return [];
    return array_values(array_unique(array_filter(array_map('trim', $value))));
}

$keys = [];
$model = 'gemini-2.5-flash';

if (defined('GEMINI_API_KEYS')) {
    $keys = normalize_gemini_keys(GEMINI_API_KEYS);
}
if (defined('GEMINI_MODEL') && is_string(GEMINI_MODEL) && trim(GEMINI_MODEL) !== '') {
    $model = trim(GEMINI_MODEL);
}

$globalConfigFile = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'global_config.json';
if (is_file($globalConfigFile)) {
    $globalConfig = json_decode((string)@file_get_contents($globalConfigFile), true);
    if (is_array($globalConfig)) {
        $fileKeys = [];
        if (array_key_exists('gemini_keys', $globalConfig)) {
            $fileKeys = normalize_gemini_keys($globalConfig['gemini_keys']);
        } elseif (array_key_exists('global_gemini_keys', $globalConfig)) {
            $fileKeys = normalize_gemini_keys($globalConfig['global_gemini_keys']);
        }
        if (!empty($fileKeys)) {
            $keys = $fileKeys;
        }
        if (!empty($globalConfig['gemini_model']) && is_string($globalConfig['gemini_model'])) {
            $model = trim($globalConfig['gemini_model']);
        }
    }
}

if (empty($keys)) {
    respond(['error' => 'AI chua co Gemini API key hop le.'], 503);
}

$lastKeyFile = sys_get_temp_dir() . DIRECTORY_SEPARATOR . 'giangbai_gemini_last_key.txt';
$lastUsedKey = is_file($lastKeyFile) ? trim((string)@file_get_contents($lastKeyFile)) : '';
if ($lastUsedKey !== '') {
    $keys = array_merge(array_values(array_filter($keys, fn($key) => $key !== $lastUsedKey)), [$lastUsedKey]);
}

$prompt = "Ban la tro ly hoc Toan cho hoc sinh THCS. Hay giai thich that de hieu, ngan gon, dung tieng Viet, khong lam thay toan bo bai neu la bai tap.\n\nMon: {$subject}\nBai: {$lessonTitle}\nNoi dung hoc sinh chua hieu:\n{$text}\n\nTra loi theo 3 phan ngan: Y chinh, Giai thich de hieu, Vi du nho.";

$payload = json_encode([
    'contents' => [[
        'parts' => [[ 'text' => $prompt ]]
    ]],
    'generationConfig' => [
        'temperature' => 0.35,
        'maxOutputTokens' => 700,
    ],
], JSON_UNESCAPED_UNICODE);

$lastError = 'Khong goi duoc AI.';
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
        $lastError = $curlError ?: 'AI khong phan hoi.';
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
            @file_put_contents($lastKeyFile, $key, LOCK_EX);
            respond(['ok' => true, 'answer' => trim($answer)]);
        }
        $lastError = 'AI tra ve noi dung rong.';
        continue;
    }

    $lastError = $response['error']['message'] ?? ('AI loi HTTP ' . $status);
    if ($status === 429 || $status >= 500) {
        continue;
    }
}

respond(['error' => $lastError], 502);
