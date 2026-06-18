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

$prompt = "Ban la tro ly hoc Toan cho hoc sinh THCS. Nhiem vu duy nhat: tra loi dung phan hoc sinh vua hoi trong muc NOI DUNG CAN GIAI THICH, khong tu y chuyen sang chu de khac, khong tom tat ca bai, khong them loi chao, khong noi 'thay se giup', khong dung Markdown, khong dung **, khong dung gach ngang ---.\n\nQuy tac bat buoc:\n- Neu noi dung la mot khai niem/cau/cum tu: giai thich truc tiep khai niem/cau/cum tu do.\n- Neu noi dung la mot cong thuc: giai thich tung ky hieu va y nghia cong thuc do, giu nguyen ky hieu Toan.\n- Neu noi dung la mot bai tap: chi goi y cach lam va diem can chu y, khong lam thay tron ven neu khong duoc yeu cau.\n- Chi dua vi du khi vi du giup lam ro dung noi dung dang hoi; neu dua vi du thi that ngan.\n- Neu noi dung hoi khong ro, noi ro can them thong tin nao, khong bịa.\n- Cau cuoi cung phai ket thuc tron ven bang dau cham, dau hoi hoac dau cham than; khong dung lai giua tu.\n\nMon: {$subject}\nBai: {$lessonTitle}\nNOI DUNG CAN GIAI THICH:\n{$text}\n\nTra loi bang 2-5 cau ngan, bam sat noi dung tren.";

function gemini_payload(string $prompt, int $maxTokens = 900): string
{
    return json_encode([
        'contents' => [[
            'parts' => [[ 'text' => $prompt ]]
        ]],
        'generationConfig' => [
            'temperature' => 0.2,
            'maxOutputTokens' => $maxTokens,
        ],
    ], JSON_UNESCAPED_UNICODE);
}

function answer_looks_complete(string $answer): bool
{
    $answer = trim($answer);
    if ($answer === '') return false;
    return (bool)preg_match('/[.!?。！？…]$/u', $answer);
}

function call_gemini(string $model, string $key, string $payload): array
{
    $url = 'https://generativelanguage.googleapis.com/v1beta/models/' . rawurlencode($model) . ':generateContent?key=' . rawurlencode($key);
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_TIMEOUT => 30,
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);
    return [$raw, $status, $curlError];
}

$lastError = 'Khong goi duoc AI.';
foreach ($keys as $key) {
    [$raw, $status, $curlError] = call_gemini($model, $key, gemini_payload($prompt));

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
            $finishReason = $response['candidates'][0]['finishReason'] ?? '';
            if (($finishReason === 'MAX_TOKENS' || !answer_looks_complete($answer)) && strlen($answer) < 3600) {
                $continuePrompt = "Day la cau tra loi dang bi ngat giua chung. Hay viet tiep phan con thieu de ket thuc tron ven 1-2 cau, khong lap lai phan da co, khong Markdown.\n\nPhan da co:\n{$answer}";
                [$raw2, $status2, $curlError2] = call_gemini($model, $key, gemini_payload($continuePrompt, 300));
                if ($raw2 !== false && $raw2 !== '' && $status2 >= 200 && $status2 < 300) {
                    $response2 = json_decode($raw2, true);
                    $parts2 = $response2['candidates'][0]['content']['parts'] ?? [];
                    $more = '';
                    foreach ($parts2 as $part2) {
                        if (!empty($part2['text'])) $more .= $part2['text'];
                    }
                    if (trim($more) !== '') {
                        $answer = rtrim($answer) . ' ' . ltrim($more);
                    }
                } elseif ($curlError2) {
                    $lastError = $curlError2;
                }
            }
            @file_put_contents($lastKeyFile, $key, LOCK_EX);
            respond(['ok' => true, 'answer' => trim($answer), 'complete' => answer_looks_complete($answer)]);
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
