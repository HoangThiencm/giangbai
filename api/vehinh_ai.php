<?php
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/ai_runtime_config.php';
require_once __DIR__ . '/ai_usage_log.php';
require_once __DIR__ . '/ai_student_quota.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

function vehinh_require_login(?array $clientKeys = null): void
{
    if (!empty($_SESSION['user_id'])) {
        return;
    }
    if (is_array($clientKeys) && !empty($clientKeys)) {
        return;
    }
    respond(['error' => 'Cần đăng nhập hoặc cung cấp Gemini API Key để dùng AI vẽ hình.'], 401);
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

function vehinh_post_json(string $url, array $headers, array $payload, int $timeout = 120): array
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

function vehinh_deprecated_models(): array
{
    return [
        'gemini-3.6-flash',
        'gemini-3.7-flash',
        'gemini-3-flash-preview',
    ];
}

function vehinh_provider_models(): array
{
    return [
        'gemini' => [
            'gemini-2.5-flash',
            'gemini-2.5-pro',
            'gemini-2.0-flash',
            'gemini-2.0-flash-lite',
            'gemini-1.5-flash',
        ],
    ];
}

function vehinh_model_supports_thinking(string $model): bool
{
    return in_array($model, ['gemini-2.5-flash', 'gemini-2.5-pro'], true);
}

function vehinh_is_usable_model(string $model, array $allowed): bool
{
    $model = trim($model);
    if ($model === '' || in_array($model, vehinh_deprecated_models(), true)) {
        return false;
    }
    if (in_array($model, $allowed, true)) {
        return true;
    }
    return (bool)preg_match('/^gemini-[\w.\-]+$/i', $model);
}

function vehinh_resolve_model(array $runtime, ?string $requestedModel = null): string
{
    $allowed = vehinh_provider_models()['gemini'] ?? [];
    $defaultFallback = $allowed[0] ?? 'gemini-2.5-flash';
    $requested = trim((string)$requestedModel);
    if (vehinh_is_usable_model($requested, $allowed)) {
        return $requested;
    }
    $runtimeModel = trim((string)($runtime['gemini_model'] ?? ''));
    if (vehinh_is_usable_model($runtimeModel, $allowed) && in_array($runtimeModel, $allowed, true)) {
        return $runtimeModel;
    }
    return $defaultFallback;
}

function vehinh_call_gemini(array $runtime, string $systemPrompt, string $userInstruction, ?array $image, ?string $requestedModel = null, ?string $requestedFallback = null): array
{
    $keys = $runtime['gemini_keys'] ?? [];
    $allowed = vehinh_provider_models()['gemini'] ?? [];
    $initialModel = vehinh_resolve_model($runtime, $requestedModel);
    if (empty($runtime['gemini_enabled']) || empty($keys)) {
        return ['error' => 'Gemini chưa bật hoặc chưa có key trong Cài đặt / Admin.', 'status' => 0];
    }

    if (is_array($image) && !empty($image['data'])) {
        $systemPrompt .= "\n\nẢNH ĐỀ BÀI: Đọc toàn bộ chữ và hình trong ảnh. Bóc tách giả thiết, kết luận, số đo và ký hiệu. Tính tọa độ giải tích (giao điểm, tiếp điểm, trung điểm, trực tâm, trọng tâm) trước khi sinh mã. Nếu ảnh mờ, nghiêng hoặc thiếu dữ kiện, nêu phần cần người dùng xác nhận, không đoán bừa.";
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

    $modelCandidates = [];
    $pushModel = static function (string $model) use (&$modelCandidates, $allowed): void {
        $model = trim($model);
        if ($model === '' || in_array($model, $modelCandidates, true) || !vehinh_is_usable_model($model, $allowed)) {
            return;
        }
        $modelCandidates[] = $model;
    };
    $pushModel($initialModel);
    $pushModel((string)$requestedFallback);
    $catalog = $allowed;
    foreach ($catalog as $catalogModel) {
        $pushModel((string)$catalogModel);
    }
    if (!$modelCandidates) {
        $modelCandidates[] = 'gemini-2.5-flash';
    }

    $lastError = 'Gemini không phản hồi.';
    $lastStatus = 0;
    foreach ($modelCandidates as $model) {
        $generationConfig = [
            'temperature' => 0.2,
            'maxOutputTokens' => 8192,
        ];
        if (vehinh_model_supports_thinking($model)) {
            $generationConfig['thinkingConfig'] = [
                'thinkingBudget' => 0,
            ];
        }
        $payload = [
            'contents' => [['parts' => $parts]],
            'generationConfig' => $generationConfig,
        ];
        foreach ($keys as $key) {
            $key = trim((string)$key);
            if ($key === '') {
                continue;
            }
            $url = 'https://generativelanguage.googleapis.com/v1beta/models/' . rawurlencode($model) . ':generateContent?key=' . rawurlencode($key);
            $response = vehinh_post_json($url, [], $payload, 120);
            if (!$response['ok']) {
                $status = (int)$response['status'];
                $errMsg = (string)($response['error'] ?: ($response['json']['error']['message'] ?? ('Gemini HTTP ' . $status)));
                $lastError = $status > 0 ? ('HTTP ' . $status . ': ' . $errMsg) : $errMsg;
                $lastStatus = $status;
                if ($status === 404 || $status === 400 || stripos($errMsg, 'not found') !== false || stripos($errMsg, 'no longer available') !== false || stripos($errMsg, 'not supported') !== false) {
                    break;
                }
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
    }

    return ['error' => $lastError, 'provider' => 'gemini', 'model' => $initialModel, 'status' => $lastStatus];
}

$runtime = load_ai_runtime_config();

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $providerModels = vehinh_provider_models();
    $geminiReady = !empty($runtime['gemini_enabled']) && !empty($runtime['gemini_keys']);
    respond([
        'ok' => true,
        'default_provider' => 'gemini',
        'providers' => [
            'gemini' => [
                'label' => 'Google Gemini',
                'configured' => $geminiReady,
                'enabled' => !empty($runtime['gemini_enabled']),
                'model' => vehinh_resolve_model($runtime),
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
$requestedModel = trim((string)($data['model'] ?? ''));
$requestedFallback = trim((string)($data['fallback_model'] ?? ''));

// Nếu server chưa nạp được key từ session/DB, hỗ trợ dùng key gửi từ client (Cài đặt cá nhân / hệ thống)
$clientKeys = normalize_api_keys($data['api_keys'] ?? ($data['keys'] ?? []));
vehinh_require_login($clientKeys);
if (empty($runtime['gemini_keys']) && !empty($clientKeys)) {
    $runtime['gemini_keys'] = $clientKeys;
    $runtime['gemini_enabled'] = true;
}

$systemPrompt = trim((string)($data['system_prompt'] ?? ''));
$userInstruction = trim((string)($data['user_instruction'] ?? ''));
$image = is_array($data['image'] ?? null) ? $data['image'] : null;
if ($systemPrompt === '' || $userInstruction === '') {
    respond(['error' => 'Thiếu prompt vẽ hình.'], 422);
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

$result = vehinh_call_gemini($runtime, $systemPrompt, $userInstruction, $image, $requestedModel, $requestedFallback);

$ok = empty($result['error']) && trim((string)($result['text'] ?? '')) !== '';
ai_usage_record([
    'provider' => 'gemini',
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
    $upstreamStatus = (int)($result['status'] ?? 0);
    $detail = (string)($result['error'] ?? 'AI vẽ hình không trả lời.');
    respond([
        'error' => $detail,
        'provider' => 'gemini',
        'model' => (string)($result['model'] ?? ''),
        'upstream_status' => $upstreamStatus,
    ], 502);
}

ai_student_quota_consume($currentUserId, $currentUserRole);

respond([
    'ok' => true,
    'text' => (string)$result['text'],
    'provider' => 'gemini',
    'model' => (string)($result['model'] ?? ''),
]);
