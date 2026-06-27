<?php
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/ai_runtime_config.php';
require_once __DIR__ . '/ai_usage_log.php';
require_once __DIR__ . '/ai_student_quota.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

function vehinh_require_login(): void
{
    if (!empty($_SESSION['user_id'])) {
        return;
    }
    respond(['error' => 'Cần đăng nhập để dùng AI vẽ hình.'], 401);
}

function vehinh_extract_gemini_text(array $response): string
{
    $out = '';
    foreach (($response['candidates'] ?? []) as $candidate) {
        foreach (($candidate['content']['parts'] ?? []) as $part) {
            if (isset($part['text'])) {
                $out .= (string)$part['text'];
            }
        }
    }
    return trim($out);
}

function vehinh_extract_openai_text(array $response): string
{
    $message = $response['choices'][0]['message']['content'] ?? '';
    if (is_array($message)) {
        $text = '';
        foreach ($message as $part) {
            if (is_array($part) && isset($part['text'])) {
                $text .= (string)$part['text'];
            }
        }
        return trim($text);
    }
    return trim((string)$message);
}

function vehinh_post_json(string $url, array $headers, array $payload, int $timeout = 60): array
{
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => array_merge(['Content-Type: application/json'], $headers),
        CURLOPT_POSTFIELDS => json_encode($payload, JSON_UNESCAPED_UNICODE),
        CURLOPT_TIMEOUT => $timeout,
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);
    $json = json_decode((string)$raw, true);
    return [
        'ok' => $status >= 200 && $status < 300 && is_array($json),
        'status' => $status,
        'error' => $curlError,
        'json' => is_array($json) ? $json : [],
        'raw' => (string)$raw,
    ];
}

function vehinh_provider_models(): array
{
    return [
        'ds2api' => [
            'deepseek-v4-flash',
            'deepseek-v4-flash-nothinking',
            'deepseek-v4-pro',
            'deepseek-v4-pro-nothinking',
        ],
        'gemini' => [
            'gemini-3-flash-preview',
            'gemini-2.5-flash',
        ],
    ];
}

function vehinh_resolve_model(string $provider, array $runtime, ?string $requestedModel = null): string
{
    $provider = strtolower(trim($provider));
    $allowed = vehinh_provider_models()[$provider] ?? [];
    $runtimeModel = $provider === 'gemini'
        ? trim((string)($runtime['gemini_model'] ?? 'gemini-2.5-flash'))
        : trim((string)($runtime['ds2api_model'] ?? 'deepseek-v4-flash'));
    $fallback = $runtimeModel !== '' ? $runtimeModel : (($allowed[0] ?? '') ?: 'deepseek-v4-flash');
    $requested = trim((string)$requestedModel);
    if ($requested !== '' && in_array($requested, $allowed, true)) {
        return $requested;
    }
    if ($runtimeModel !== '' && in_array($runtimeModel, $allowed, true)) {
        return $runtimeModel;
    }
    return $fallback;
}

function vehinh_call_ds2api(array $runtime, string $systemPrompt, string $userInstruction, ?string $requestedModel = null): array
{
    $baseUrl = normalize_ds2api_base_url((string)($runtime['ds2api_base_url'] ?? ''));
    $apiKey = ds2api_effective_api_key((string)($runtime['ds2api_api_key'] ?? ''));
    $model = vehinh_resolve_model('ds2api', $runtime, $requestedModel);
    if ($baseUrl === '' || $apiKey === '') {
        return ['error' => 'DS2API chưa có Base URL hoặc Client API Key trong Admin/config.php.'];
    }

    $payload = [
        'model' => $model,
        'messages' => [
            ['role' => 'system', 'content' => $systemPrompt],
            ['role' => 'user', 'content' => $userInstruction],
        ],
        'temperature' => 0.2,
        'max_tokens' => 3200,
    ];
    $response = vehinh_post_json($baseUrl . '/chat/completions', [
        'Authorization: Bearer ' . $apiKey,
        'x-api-key: ' . $apiKey,
    ], $payload);
    if (!$response['ok']) {
        $msg = $response['error'] ?: ($response['json']['error']['message'] ?? ('DS2API HTTP ' . $response['status']));
        return ['error' => $msg, 'provider' => 'ds2api', 'model' => $model];
    }
    $text = vehinh_extract_openai_text($response['json']);
    if ($text === '') {
        return ['error' => 'DS2API không trả về nội dung vẽ hình.', 'provider' => 'ds2api', 'model' => $model];
    }
    return array_merge([
        'text' => $text,
        'provider' => 'ds2api',
        'model' => $model,
    ], ai_usage_extract_shopaikey_tokens($response['json']));
}

function vehinh_call_gemini(array $runtime, string $systemPrompt, string $userInstruction, ?array $image, ?string $requestedModel = null): array
{
    $keys = $runtime['gemini_keys'] ?? [];
    $model = vehinh_resolve_model('gemini', $runtime, $requestedModel);
    if (empty($runtime['gemini_enabled']) || empty($keys)) {
        return ['error' => 'Gemini chưa bật hoặc chưa có key trong Admin.'];
    }

    $parts = [['text' => $systemPrompt . "\n\n" . $userInstruction]];
    if (is_array($image) && !empty($image['data']) && !empty($image['mime_type'])) {
        $parts[] = [
            'inlineData' => [
                'mimeType' => (string)$image['mime_type'],
                'data' => (string)$image['data'],
            ],
        ];
    }

    $payload = [
        'contents' => [['parts' => $parts]],
        'generationConfig' => [
            'temperature' => 0.2,
            'maxOutputTokens' => 4096,
        ],
    ];

    $lastError = 'Gemini không phản hồi.';
    foreach ($keys as $key) {
        $key = trim((string)$key);
        if ($key === '') {
            continue;
        }
        $url = 'https://generativelanguage.googleapis.com/v1beta/models/' . rawurlencode($model) . ':generateContent?key=' . rawurlencode($key);
        $response = vehinh_post_json($url, [], $payload);
        if (!$response['ok']) {
            $lastError = $response['error'] ?: ($response['json']['error']['message'] ?? ('Gemini HTTP ' . $response['status']));
            continue;
        }
        $text = vehinh_extract_gemini_text($response['json']);
        if ($text === '') {
            $lastError = 'Gemini không trả về nội dung vẽ hình.';
            continue;
        }
        return array_merge([
            'text' => $text,
            'provider' => 'gemini',
            'model' => $model,
        ], ai_usage_extract_gemini_tokens($response['json']));
    }

    return ['error' => $lastError, 'provider' => 'gemini', 'model' => $model];
}

vehinh_require_login();
$runtime = load_ai_runtime_config();

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $providerModels = vehinh_provider_models();
    $ds2Active = !empty($runtime['ds2api_enabled']) || !empty($runtime['ai_test_ds2api_only']);
    $ds2Ready = $ds2Active
        && trim((string)($runtime['ds2api_base_url'] ?? '')) !== ''
        && trim((string)($runtime['ds2api_api_key'] ?? '')) !== '';
    $geminiReady = !empty($runtime['gemini_enabled']) && !empty($runtime['gemini_keys']);
    respond([
        'ok' => true,
        'default_provider' => $ds2Ready ? 'ds2api' : 'gemini',
        'providers' => [
            'ds2api' => [
                'label' => 'DeepSeek / DS2API',
                'configured' => $ds2Ready,
                'enabled' => $ds2Active,
                'model' => vehinh_resolve_model('ds2api', $runtime),
                'models' => $providerModels['ds2api'],
                'supports_image' => false,
            ],
            'gemini' => [
                'label' => 'Google Gemini',
                'configured' => $geminiReady,
                'enabled' => !empty($runtime['gemini_enabled']),
                'model' => vehinh_resolve_model('gemini', $runtime),
                'models' => $providerModels['gemini'],
                'keys_count' => count($runtime['gemini_keys'] ?? []),
                'supports_image' => true,
            ],
        ],
    ]);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(['error' => 'Method not allowed.'], 405);
}

$data = json_body();
$provider = strtolower(trim((string)($data['provider'] ?? 'ds2api')));
$requestedModel = trim((string)($data['model'] ?? ''));
if (!in_array($provider, ['ds2api', 'gemini'], true)) {
    respond(['error' => 'Nguồn AI vẽ hình không hợp lệ.'], 422);
}

$systemPrompt = trim((string)($data['system_prompt'] ?? ''));
$userInstruction = trim((string)($data['user_instruction'] ?? ''));
$image = is_array($data['image'] ?? null) ? $data['image'] : null;
if ($systemPrompt === '' || $userInstruction === '') {
    respond(['error' => 'Thiếu prompt vẽ hình.'], 422);
}
if ($provider === 'ds2api' && $image) {
    respond(['error' => 'DeepSeek/DS2API hiện chỉ dùng cho mô tả chữ trên trang vẽ hình. Nếu có ảnh, hãy chọn Gemini.'], 422);
}

$currentUserId = !empty($_SESSION['user_id']) ? (int)$_SESSION['user_id'] : null;
$currentUserRole = '';
if ($currentUserId) {
    $userStmt = $pdo->prepare('SELECT role FROM users WHERE id = ? AND is_active = 1 LIMIT 1');
    $userStmt->execute([$currentUserId]);
    $currentUserRole = (string)($userStmt->fetchColumn() ?: '');
}
ai_student_rate_limit_require($currentUserId, $currentUserRole);
ai_student_rate_limit_touch($currentUserId, $currentUserRole);
ai_student_quota_require($currentUserId, $currentUserRole);

$result = $provider === 'gemini'
    ? vehinh_call_gemini($runtime, $systemPrompt, $userInstruction, $image, $requestedModel)
    : vehinh_call_ds2api($runtime, $systemPrompt, $userInstruction, $requestedModel);

$ok = empty($result['error']) && trim((string)($result['text'] ?? '')) !== '';
ai_usage_record([
    'provider' => $provider,
    'module' => 'other',
    'mode' => 'manual',
    'ok' => $ok,
    'model' => (string)($result['model'] ?? ''),
    'error' => (string)($result['error'] ?? ''),
    'prompt_tokens' => (int)($result['prompt_tokens'] ?? 0),
    'completion_tokens' => (int)($result['completion_tokens'] ?? 0),
    'total_tokens' => (int)($result['total_tokens'] ?? 0),
]);

if (!$ok) {
    respond(['error' => (string)($result['error'] ?? 'AI vẽ hình không trả lời.'), 'provider' => $provider], 502);
}

ai_student_quota_consume($currentUserId, $currentUserRole);

respond([
    'ok' => true,
    'text' => (string)$result['text'],
    'provider' => $provider,
    'model' => (string)($result['model'] ?? ''),
]);
