<?php
require_once __DIR__ . '/helpers.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(['error' => 'Method not allowed.'], 405);
}

$data = json_body();
$mode = trim((string)($data['mode'] ?? 'explain'));
$text = trim($data['text'] ?? '');
$question = trim($data['question'] ?? '');
$lessonTitle = trim($data['lesson_title'] ?? 'bai hoc');
$subject = trim($data['subject'] ?? 'Toan');
$lessonContext = trim($data['lesson_context'] ?? '');

$history = [];
if (!empty($data['history']) && is_array($data['history'])) {
    foreach (array_slice($data['history'], -8) as $turn) {
        if (!is_array($turn)) continue;
        $role = ($turn['role'] ?? '') === 'assistant' ? 'assistant' : 'user';
        $content = trim((string)($turn['content'] ?? ''));
        if ($content !== '') {
            $history[] = ['role' => $role, 'content' => $content];
        }
    }
}

if ($mode === 'chat') {
    if ($question === '') {
        respond(['error' => 'Thieu cau hoi.'], 422);
    }
} elseif ($text === '') {
    respond(['error' => 'Thieu noi dung can giai thich.'], 422);
}

function normalize_api_keys($value): array
{
    if (is_string($value)) {
        $value = preg_split('/[\s,]+/', $value) ?: [];
    }
    if (!is_array($value)) return [];
    return array_values(array_unique(array_filter(array_map('trim', $value))));
}

function load_ai_runtime_config(): array
{
    $config = [
        'gemini_keys' => [],
        'gemini_model' => 'gemini-2.5-flash',
        'shopaikey_api_key' => '',
        'shopaikey_model' => 'deepseek-v4-flash',
        'shopaikey_base_url' => 'https://api.shopaikey.com/v1',
    ];

    if (defined('GEMINI_API_KEYS')) {
        $config['gemini_keys'] = normalize_api_keys(GEMINI_API_KEYS);
    }
    if (defined('GEMINI_MODEL') && is_string(GEMINI_MODEL) && trim(GEMINI_MODEL) !== '') {
        $config['gemini_model'] = trim(GEMINI_MODEL);
    }
    if (defined('SHOPAIKEY_API_KEY') && is_string(SHOPAIKEY_API_KEY) && trim(SHOPAIKEY_API_KEY) !== '') {
        $config['shopaikey_api_key'] = trim(SHOPAIKEY_API_KEY);
    }
    if (defined('SHOPAIKEY_MODEL') && is_string(SHOPAIKEY_MODEL) && trim(SHOPAIKEY_MODEL) !== '') {
        $config['shopaikey_model'] = trim(SHOPAIKEY_MODEL);
    }

    $globalConfigFile = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'global_config.json';
    if (is_file($globalConfigFile)) {
        $globalConfig = json_decode((string)@file_get_contents($globalConfigFile), true);
        if (is_array($globalConfig)) {
            $fileKeys = [];
            if (array_key_exists('gemini_keys', $globalConfig)) {
                $fileKeys = normalize_api_keys($globalConfig['gemini_keys']);
            } elseif (array_key_exists('global_gemini_keys', $globalConfig)) {
                $fileKeys = normalize_api_keys($globalConfig['global_gemini_keys']);
            }
            if (!empty($fileKeys)) {
                $config['gemini_keys'] = $fileKeys;
            }
            if (!empty($globalConfig['gemini_model']) && is_string($globalConfig['gemini_model'])) {
                $config['gemini_model'] = trim($globalConfig['gemini_model']);
            }
            if (!empty($globalConfig['shopaikey_api_key']) && is_string($globalConfig['shopaikey_api_key'])) {
                $config['shopaikey_api_key'] = trim($globalConfig['shopaikey_api_key']);
            }
            if (!empty($globalConfig['shopaikey_model']) && is_string($globalConfig['shopaikey_model'])) {
                $config['shopaikey_model'] = trim($globalConfig['shopaikey_model']);
            }
        }
    }

    return $config;
}

function build_explain_prompt(string $subject, string $lessonTitle, string $text): string
{
    return "Ban la tro ly hoc Toan cho hoc sinh THCS. Nhiem vu duy nhat: tra loi dung phan hoc sinh vua hoi trong muc NOI DUNG CAN GIAI THICH, khong tu y chuyen sang chu de khac, khong tom tat ca bai, khong them loi chao, khong noi 'thay se giup', khong dung Markdown, khong dung **, khong dung gach ngang ---.\n\nQuy tac bat buoc:\n- Neu noi dung la mot khai niem/cau/cum tu: giai thich truc tiep khai niem/cau/cum tu do.\n- Neu noi dung la mot cong thuc: giai thich tung ky hieu va y nghia cong thuc do, giu nguyen ky hieu Toan.\n- Neu noi dung la mot bai tap: chi goi y cach lam va diem can chu y, khong lam thay tron ven neu khong duoc yeu cau.\n- Chi dua vi du khi vi du giup lam ro dung noi dung dang hoi; neu dua vi du thi that ngan.\n- Neu noi dung hoi khong ro, noi ro can them thong tin nao, khong bịa.\n- Cau cuoi cung phai ket thuc tron ven bang dau cham, dau hoi hoac dau cham than; khong dung lai giua tu.\n\nMon: {$subject}\nBai: {$lessonTitle}\nNOI DUNG CAN GIAI THICH:\n{$text}\n\nTra loi bang 2-5 cau ngan, bam sat noi dung tren.";
}

function build_chat_prompt(string $subject, string $lessonTitle, string $lessonContext, array $history, string $question): string
{
    $historyText = '';
    foreach ($history as $turn) {
        $role = ($turn['role'] ?? '') === 'assistant' ? 'Tro ly' : 'Hoc sinh';
        $content = trim((string)($turn['content'] ?? ''));
        if ($content !== '') {
            $historyText .= "{$role}: {$content}\n";
        }
    }

    $contextBlock = $lessonContext !== '' ? "TOM TAT BAI DANG HOC:\n{$lessonContext}\n\n" : '';

    return "Ban la tro ly hoc Toan cho hoc sinh THCS. Hoc sinh dang hoc bai va hoi them trong khung chat.\n\nQuy tac bat buoc:\n- Chi tra loi trong pham vi bai hoc va mon Toan THCS, khong lam ho toan bo bai tap neu hoc sinh chi hoi khai niem.\n- Neu la bai tap: goi y cach lam, diem can chu y, khong lam thay tron ven neu hoc sinh khong yeu cau.\n- Giu ky hieu Toan/LaTeX khi can.\n- Khong dung Markdown, khong dung **, khong loi chao dai.\n- Tra loi ngan 2-6 cau, ro rang, ket thuc tron ven bang dau cham.\n\nMon: {$subject}\nBai: {$lessonTitle}\n{$contextBlock}"
        . ($historyText !== '' ? "LICH SU CHAT GAN DAY:\n{$historyText}\n" : '')
        . "CAU HOI MOI CUA HOC SINH:\n{$question}\n\nTra loi cau hoi moi.";
}

function answer_looks_complete(string $answer): bool
{
    $answer = trim($answer);
    if ($answer === '') return false;
    return (bool)preg_match('/[.!?。！？…]$/u', $answer);
}

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

function shopaikey_payload(string $model, string $prompt, int $maxTokens = 900): string
{
    return json_encode([
        'model' => $model,
        'messages' => [
            ['role' => 'user', 'content' => $prompt],
        ],
        'temperature' => 0.2,
        'max_tokens' => $maxTokens,
    ], JSON_UNESCAPED_UNICODE);
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

function call_shopaikey(string $baseUrl, string $key, string $payload): array
{
    $url = rtrim($baseUrl, '/') . '/chat/completions';
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $key,
        ],
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_TIMEOUT => 45,
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);
    return [$raw, $status, $curlError];
}

function extract_gemini_answer(array $response): string
{
    $parts = $response['candidates'][0]['content']['parts'] ?? [];
    $answer = '';
    foreach ($parts as $part) {
        if (!empty($part['text'])) $answer .= $part['text'];
    }
    return trim($answer);
}

function extract_shopaikey_answer(array $response): string
{
    return trim((string)($response['choices'][0]['message']['content'] ?? ''));
}

function should_retry_provider(int $status, string $errorMessage = ''): bool
{
    if ($status === 429 || $status >= 500) return true;
    $message = strtolower($errorMessage);
    return str_contains($message, 'quota')
        || str_contains($message, 'rate limit')
        || str_contains($message, 'resource exhausted')
        || str_contains($message, 'overloaded');
}

function complete_answer_if_needed(string $provider, callable $caller, string $answer, array $meta): array
{
    $finishReason = $meta['finish_reason'] ?? '';
    $needsMore = ($finishReason === 'MAX_TOKENS' || $finishReason === 'length' || !answer_looks_complete($answer));
    if (!$needsMore || strlen($answer) >= 3600) {
        return [$answer, $meta];
    }

    $continuePrompt = "Day la cau tra loi dang bi ngat giua chung. Hay viet tiep phan con thieu de ket thuc tron ven 1-2 cau, khong lap lai phan da co, khong Markdown.\n\nPhan da co:\n{$answer}";
    [$raw2, $status2, $curlError2, $response2] = $caller($continuePrompt, 300);
    if ($raw2 === false || $raw2 === '' || $status2 < 200 || $status2 >= 300) {
        return [$answer, array_merge($meta, ['continue_error' => $curlError2 ?: 'Khong noi tiep duoc cau tra loi.'])];
    }

    $more = $provider === 'gemini'
        ? extract_gemini_answer($response2)
        : extract_shopaikey_answer($response2);
    if ($more !== '') {
        $answer = rtrim($answer) . ' ' . ltrim($more);
    }
    return [$answer, $meta];
}

function try_gemini_explain(array $config, string $prompt): ?array
{
    $keys = $config['gemini_keys'] ?? [];
    if (empty($keys)) return null;

    $model = $config['gemini_model'] ?? 'gemini-2.5-flash';
    $lastKeyFile = sys_get_temp_dir() . DIRECTORY_SEPARATOR . 'giangbai_gemini_last_key.txt';
    $lastUsedKey = is_file($lastKeyFile) ? trim((string)@file_get_contents($lastKeyFile)) : '';
    if ($lastUsedKey !== '') {
        $keys = array_merge(array_values(array_filter($keys, fn($key) => $key !== $lastUsedKey)), [$lastUsedKey]);
    }

    $lastError = 'Khong goi duoc Gemini.';
    foreach ($keys as $key) {
        $caller = function (string $textPrompt, int $maxTokens = 900) use ($model, $key) {
            [$raw, $status, $curlError] = call_gemini($model, $key, gemini_payload($textPrompt, $maxTokens));
            $response = is_string($raw) && $raw !== '' ? (json_decode($raw, true) ?: []) : [];
            return [$raw, $status, $curlError, $response];
        };

        [$raw, $status, $curlError, $response] = $caller($prompt);
        if ($raw === false || $raw === '') {
            $lastError = $curlError ?: 'Gemini khong phan hoi.';
            continue;
        }

        if ($status >= 200 && $status < 300) {
            $answer = extract_gemini_answer($response);
            if ($answer === '') {
                $lastError = 'Gemini tra ve noi dung rong.';
                continue;
            }
            $finishReason = $response['candidates'][0]['finishReason'] ?? '';
            [$answer, ] = complete_answer_if_needed('gemini', $caller, $answer, ['finish_reason' => $finishReason]);
            @file_put_contents($lastKeyFile, $key, LOCK_EX);
            return [
                'answer' => $answer,
                'provider' => 'gemini',
                'model' => $model,
            ];
        }

        $lastError = $response['error']['message'] ?? ('Gemini loi HTTP ' . $status);
        if (should_retry_provider($status, $lastError)) {
            continue;
        }
    }

    return ['error' => $lastError, 'provider' => 'gemini'];
}

function try_shopaikey_explain(array $config, string $prompt): ?array
{
    $apiKey = trim((string)($config['shopaikey_api_key'] ?? ''));
    if ($apiKey === '') return null;

    $model = trim((string)($config['shopaikey_model'] ?? 'deepseek-v4-flash')) ?: 'deepseek-v4-flash';
    $baseUrl = trim((string)($config['shopaikey_base_url'] ?? 'https://api.shopaikey.com/v1'));

    $caller = function (string $textPrompt, int $maxTokens = 900) use ($baseUrl, $apiKey, $model) {
        [$raw, $status, $curlError] = call_shopaikey($baseUrl, $apiKey, shopaikey_payload($model, $textPrompt, $maxTokens));
        $response = is_string($raw) && $raw !== '' ? (json_decode($raw, true) ?: []) : [];
        return [$raw, $status, $curlError, $response];
    };

    [$raw, $status, $curlError, $response] = $caller($prompt);
    if ($raw === false || $raw === '') {
        return ['error' => $curlError ?: 'ShopAIKey khong phan hoi.', 'provider' => 'shopaikey'];
    }

    if ($status >= 200 && $status < 300) {
        $answer = extract_shopaikey_answer($response);
        if ($answer === '') {
            return ['error' => 'ShopAIKey tra ve noi dung rong.', 'provider' => 'shopaikey'];
        }
        $finishReason = $response['choices'][0]['finish_reason'] ?? '';
        [$answer, ] = complete_answer_if_needed('shopaikey', $caller, $answer, ['finish_reason' => $finishReason]);
        return [
            'answer' => $answer,
            'provider' => 'shopaikey',
            'model' => $model,
        ];
    }

    $errorMessage = $response['error']['message'] ?? ($response['message'] ?? ('ShopAIKey loi HTTP ' . $status));
    return ['error' => $errorMessage, 'provider' => 'shopaikey'];
}

$runtime = load_ai_runtime_config();
$prompt = $mode === 'chat'
    ? build_chat_prompt($subject, $lessonTitle, $lessonContext, $history, $question)
    : build_explain_prompt($subject, $lessonTitle, $text);

if (empty($runtime['gemini_keys']) && trim((string)$runtime['shopaikey_api_key']) === '') {
    respond(['error' => 'AI chua co Gemini key hoac ShopAIKey fallback.'], 503);
}

$geminiResult = try_gemini_explain($runtime, $prompt);
if (is_array($geminiResult) && !empty($geminiResult['answer'])) {
    respond([
        'ok' => true,
        'answer' => trim($geminiResult['answer']),
        'complete' => answer_looks_complete($geminiResult['answer']),
        'provider' => $geminiResult['provider'] ?? 'gemini',
        'model' => $geminiResult['model'] ?? $runtime['gemini_model'],
    ]);
}

$fallbackResult = try_shopaikey_explain($runtime, $prompt);
if (is_array($fallbackResult) && !empty($fallbackResult['answer'])) {
    respond([
        'ok' => true,
        'answer' => trim($fallbackResult['answer']),
        'complete' => answer_looks_complete($fallbackResult['answer']),
        'provider' => $fallbackResult['provider'] ?? 'shopaikey',
        'model' => $fallbackResult['model'] ?? $runtime['shopaikey_model'],
        'fallback' => true,
    ]);
}

$errors = [];
if (is_array($geminiResult) && !empty($geminiResult['error'])) $errors[] = $geminiResult['error'];
if (is_array($fallbackResult) && !empty($fallbackResult['error'])) $errors[] = $fallbackResult['error'];
$lastError = $errors ? implode(' | ', $errors) : 'Khong goi duoc AI.';
respond(['error' => $lastError], 502);