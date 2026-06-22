<?php
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/ai_usage_log.php';
require_once __DIR__ . '/ai_smart_quota.php';
require_once __DIR__ . '/ai_explain_cache.php';
require_once __DIR__ . '/ai_runtime_config.php';
require_once __DIR__ . '/ai_student_quota.php';
session_start();

$key = $_SERVER['HTTP_X_ADMIN_KEY'] ?? ($_GET['admin_key'] ?? '');
$isAdmin = defined('ADMIN_KEY') && hash_equals(ADMIN_KEY, $key);
$teacherUser = null;
if (!$isAdmin && !empty($_SESSION['user_id'])) {
    $userStmt = $pdo->prepare('SELECT * FROM users WHERE id = ? LIMIT 1');
    $userStmt->execute([$_SESSION['user_id']]);
    $teacherUser = $userStmt->fetch();
    if (!$teacherUser || !(bool)$teacherUser['is_active'] || ($teacherUser['role'] ?? '') !== 'teacher') {
        $teacherUser = null;
    }
}
if (!$isAdmin && !$teacherUser) {
    respond(['error' => 'Tài khoản không có quyền xem thống kê AI.'], 403);
}

function ai_stats_teacher_tab_enabled(): bool
{
    $globalConfigFile = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'global_config.json';
    if (!is_file($globalConfigFile)) {
        return true;
    }
    $globalConfig = json_decode((string)@file_get_contents($globalConfigFile), true);
    if (!is_array($globalConfig)) {
        return true;
    }
    $features = is_array($globalConfig['features'] ?? null) ? $globalConfig['features'] : [];
    return ($features['teacher_ai_stats'] ?? true) !== false;
}

if ($teacherUser) {
    if (!ai_stats_teacher_tab_enabled()) {
        respond(['error' => 'Admin đã tắt tab Theo dõi AI cho giáo viên.'], 403);
    }
    $allowedPages = normalize_pages(json_decode($teacherUser['allowed_pages_json'] ?? '[]', true));
    if (!in_array('theodoiai', $allowedPages, true)) {
        respond(['error' => 'Tài khoản chưa được admin cấp quyền xem thống kê AI.'], 403);
    }
}



function ai_stats_http_get(string $url, array $headers = [], int $timeout = 20): array
{
    $ch = curl_init($url);
    $curlHeaders = [];
    foreach ($headers as $key => $value) {
        $curlHeaders[] = $key . ': ' . $value;
    }
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => $curlHeaders,
        CURLOPT_TIMEOUT => $timeout,
        CURLOPT_CONNECTTIMEOUT => 8,
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    $json = is_string($raw) && $raw !== '' ? json_decode($raw, true) : null;
    return [
        'ok' => $status >= 200 && $status < 300,
        'status' => $status,
        'error' => $error,
        'raw' => is_string($raw) ? $raw : '',
        'json' => is_array($json) ? $json : null,
    ];
}

function ai_stats_fetch_shopaikey(string $apiKey, string $baseUrl): array
{
    $apiKey = trim($apiKey);
    if ($apiKey === '') {
        return [
            'configured' => false,
            'available' => false,
            'message' => 'Chưa cấu hình ShopAIKey API key.',
        ];
    }

    $base = rtrim($baseUrl, '/');
    $headers = [
        'Authorization' => 'Bearer ' . $apiKey,
        'Accept' => 'application/json',
    ];

    $subscription = ai_stats_http_get($base . '/dashboard/billing/subscription', $headers);
    $usage = ai_stats_http_get($base . '/dashboard/billing/usage', $headers);

    $hardLimitUsd = null;
    $softLimitUsd = null;
    $accessUntil = null;
    if ($subscription['ok'] && is_array($subscription['json'])) {
        $payload = $subscription['json'];
        $hardLimitUsd = isset($payload['hard_limit_usd']) ? (float)$payload['hard_limit_usd'] : null;
        $softLimitUsd = isset($payload['soft_limit_usd']) ? (float)$payload['soft_limit_usd'] : null;
        $accessUntil = $payload['access_until'] ?? null;
        if ($hardLimitUsd === null && isset($payload['data']['hard_limit_usd'])) {
            $hardLimitUsd = (float)$payload['data']['hard_limit_usd'];
        }
    }

    $totalUsageUsd = null;
    if ($usage['ok'] && is_array($usage['json'])) {
        $payload = $usage['json'];
        if (isset($payload['total_usage'])) {
            $totalUsageUsd = ((float)$payload['total_usage']) / 100;
        } elseif (isset($payload['total_usage_usd'])) {
            $totalUsageUsd = (float)$payload['total_usage_usd'];
        } elseif (isset($payload['data']['total_usage'])) {
            $totalUsageUsd = ((float)$payload['data']['total_usage']) / 100;
        }
    }

    $remainingUsd = null;
    if ($hardLimitUsd !== null && $totalUsageUsd !== null) {
        $remainingUsd = max(0, round($hardLimitUsd - $totalUsageUsd, 4));
    }

    $available = $subscription['ok'] || $usage['ok'];
    $message = $available
        ? 'Đã lấy số liệu từ ShopAIKey API.'
        : 'Không gọi được ShopAIKey API (HTTP '
            . max($subscription['status'], $usage['status'])
            . '). Xem thêm trên dashboard ShopAIKey.';

    return [
        'configured' => true,
        'available' => $available,
        'message' => $message,
        'requests' => null,
        'used_usd' => $totalUsageUsd,
        'remaining_usd' => $remainingUsd,
        'hard_limit_usd' => $hardLimitUsd,
        'soft_limit_usd' => $softLimitUsd,
        'access_until' => $accessUntil,
        'dashboard_url' => 'https://shopaikey.com/',
        'raw_status' => [
            'subscription' => $subscription['status'],
            'usage' => $usage['status'],
        ],
    ];
}

function ai_stats_worker_script_name(): string
{
    if (defined('CLOUDFLARE_WORKER_SCRIPT_NAME') && is_string(CLOUDFLARE_WORKER_SCRIPT_NAME) && trim(CLOUDFLARE_WORKER_SCRIPT_NAME) !== '') {
        return trim(CLOUDFLARE_WORKER_SCRIPT_NAME);
    }
    $workerUrl = defined('CLOUDFLARE_AI_WORKER_URL') && is_string(CLOUDFLARE_AI_WORKER_URL) ? trim(CLOUDFLARE_AI_WORKER_URL) : '';
    if ($workerUrl !== '') {
        $host = parse_url($workerUrl, PHP_URL_HOST);
        if (is_string($host) && $host !== '') {
            $parts = explode('.', $host);
            if (!empty($parts[0])) {
                return $parts[0];
            }
        }
    }
    return '';
}

function ai_stats_fetch_cloudflare(string $accountId, string $apiToken, string $scriptName, string $dayKey): array
{
    $accountId = trim($accountId);
    $apiToken = trim($apiToken);
    $scriptName = trim($scriptName);
    if ($accountId === '' || $apiToken === '' || $scriptName === '') {
        return [
            'configured' => false,
            'available' => false,
            'message' => 'Chưa cấu hình CLOUDFLARE_ACCOUNT_ID / CLOUDFLARE_API_TOKEN / CLOUDFLARE_WORKER_SCRIPT_NAME trong api/config.php.',
        ];
    }

    $tz = ai_usage_timezone();
    $start = new DateTimeImmutable($dayKey . ' 00:00:00', $tz);
    $end = $start->modify('+1 day');
    $query = <<<'GQL'
query GetWorkersAnalytics($accountTag: string!, $datetimeStart: string!, $datetimeEnd: string!, $scriptName: string!) {
  viewer {
    accounts(filter: { accountTag: $accountTag }) {
      workersInvocationsAdaptive(
        limit: 5000
        filter: {
          scriptName: $scriptName
          datetime_geq: $datetimeStart
          datetime_leq: $datetimeEnd
        }
      ) {
        sum { requests errors subrequests }
        dimensions { datetime status }
      }
    }
  }
}
GQL;

    $payload = json_encode([
        'query' => $query,
        'variables' => [
            'accountTag' => $accountId,
            'datetimeStart' => $start->setTimezone(new DateTimeZone('UTC'))->format('Y-m-d\TH:i:s\Z'),
            'datetimeEnd' => $end->setTimezone(new DateTimeZone('UTC'))->format('Y-m-d\TH:i:s\Z'),
            'scriptName' => $scriptName,
        ],
    ], JSON_UNESCAPED_UNICODE);

    $ch = curl_init('https://api.cloudflare.com/client/v4/graphql');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => [
            'Authorization: Bearer ' . $apiToken,
            'Content-Type: application/json',
            'Accept: application/json',
        ],
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_TIMEOUT => 25,
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);

    $json = is_string($raw) && $raw !== '' ? json_decode($raw, true) : null;
    if ($status < 200 || $status >= 300 || !is_array($json)) {
        return [
            'configured' => true,
            'available' => false,
            'message' => $curlError !== '' ? $curlError : ('Cloudflare GraphQL HTTP ' . $status),
            'script_name' => $scriptName,
        ];
    }
    if (!empty($json['errors'])) {
        $first = $json['errors'][0]['message'] ?? 'Cloudflare GraphQL lỗi.';
        return [
            'configured' => true,
            'available' => false,
            'message' => (string)$first,
            'script_name' => $scriptName,
        ];
    }

    $rows = $json['data']['viewer']['accounts'][0]['workersInvocationsAdaptive'] ?? [];
    if (!is_array($rows)) {
        $rows = [];
    }

    $requests = 0;
    $errors = 0;
    foreach ($rows as $row) {
        if (!is_array($row)) continue;
        $sum = $row['sum'] ?? [];
        $requests += (int)($sum['requests'] ?? 0);
        $errors += (int)($sum['errors'] ?? 0);
    }

    return [
        'configured' => true,
        'available' => true,
        'message' => 'Đã lấy số liệu Worker từ Cloudflare GraphQL.',
        'script_name' => $scriptName,
        'requests_today' => $requests,
        'errors_today' => $errors,
        'success_today' => max(0, $requests - $errors),
        'dashboard_url' => 'https://dash.cloudflare.com/',
    ];
}

function ai_stats_sum_by_mode(array $byMode): int
{
    $total = 0;
    foreach ($byMode as $count) {
        $total += max(0, (int)$count);
    }
    return $total;
}

function ai_stats_sum_module_success(array $byModule): int
{
    $total = 0;
    foreach ($byModule as $bucket) {
        if (!is_array($bucket)) {
            continue;
        }
        $total += max(0, (int)($bucket['success'] ?? 0));
    }
    return $total;
}

function ai_stats_modes_for_module(string $module): array
{
    return [
        'lotrinh' => ['explain', 'chat'],
        'thitructuyen' => ['ocr', 'vision', 'normalize', 'answer_sheet', 'manual'],
        'vanban' => ['document'],
    ][$module] ?? [];
}

function ai_stats_infer_module_success_from_modes(array $byMode, string $module): int
{
    $total = 0;
    foreach (ai_stats_modes_for_module($module) as $mode) {
        $total += max(0, (int)($byMode[$mode] ?? 0));
    }
    return $total;
}

function ai_stats_count_recent_module_success(array $recent, string $todayKey, string $module): int
{
    $total = 0;
    foreach ($recent as $item) {
        if (!is_array($item) || empty($item['ok'])) {
            continue;
        }
        $ts = (string)($item['ts'] ?? '');
        if ($todayKey !== '' && !str_starts_with($ts, $todayKey)) {
            continue;
        }
        if (ai_usage_normalize_module((string)($item['module'] ?? 'other')) !== $module) {
            continue;
        }
        $total++;
    }
    return $total;
}

function ai_stats_enrich_by_module(array $byModule, array $byMode, array $recent = [], string $todayKey = ''): array
{
    foreach (['lotrinh', 'thitructuyen', 'vanban'] as $moduleId) {
        $targetSuccess = max(
            (int)($byModule[$moduleId]['success'] ?? 0),
            ai_stats_infer_module_success_from_modes($byMode, $moduleId),
            ai_stats_count_recent_module_success($recent, $todayKey, $moduleId)
        );
        if ($targetSuccess <= 0) {
            continue;
        }

        if (!isset($byModule[$moduleId]) || !is_array($byModule[$moduleId])) {
            $byModule[$moduleId] = ['calls' => 0, 'success' => 0, 'error' => 0, 'providers' => []];
        }
        $byModule[$moduleId]['success'] = $targetSuccess;
        $byModule[$moduleId]['calls'] = max((int)($byModule[$moduleId]['calls'] ?? 0), $targetSuccess);
    }

    return $byModule;
}

function ai_stats_summarize_day(?array $day, array $recent = [], string $todayKey = ''): array
{
    if (!is_array($day)) {
        return [
            'providers' => [],
            'by_mode' => [],
            'by_module' => [],
            'total_success' => 0,
            'total_calls' => 0,
        ];
    }
    $providers = is_array($day['providers'] ?? null) ? $day['providers'] : [];
    $byMode = is_array($day['by_mode'] ?? null) ? $day['by_mode'] : [];
    $byModule = is_array($day['by_module'] ?? null) ? $day['by_module'] : [];
    $byModule = ai_stats_enrich_by_module($byModule, $byMode, $recent, $todayKey);
    $totalSuccess = 0;
    $totalCalls = 0;
    foreach ($providers as $bucket) {
        if (!is_array($bucket)) continue;
        $totalSuccess += (int)($bucket['success'] ?? 0);
        $totalCalls += (int)($bucket['calls'] ?? 0);
    }
    $totalSuccess = max(
        $totalSuccess,
        ai_stats_sum_by_mode($byMode),
        ai_stats_sum_module_success($byModule)
    );
    $totalCalls = max($totalCalls, $totalSuccess);
    return [
        'providers' => $providers,
        'by_mode' => $byMode,
        'by_module' => $byModule,
        'total_success' => $totalSuccess,
        'total_calls' => $totalCalls,
    ];
}

function ai_stats_module_catalog(): array
{
    return [
        [
            'id' => 'lotrinh',
            'label' => ai_usage_module_label('lotrinh'),
            'providers' => ['cloudflare_workers_ai', 'gemini', 'shopaikey', 'light_ai', 'light_ai_math', 'explain_cache'],
            'note' => 'Giải thích & chat · cache, Light AI, Cloudflare, Gemini, ShopAIKey',
        ],
        [
            'id' => 'thitructuyen',
            'label' => ai_usage_module_label('thitructuyen'),
            'providers' => ['mistral_ocr', 'gemini_browser'],
            'note' => 'Mistral quét PDF + Gemini nhận diện câu hỏi (trình duyệt / hosting fallback)',
        ],
        [
            'id' => 'vanban',
            'label' => ai_usage_module_label('vanban'),
            'providers' => [],
            'note' => 'Tự nhận diện mẫu (pdf.js + regex), không gọi AI',
        ],
    ];
}

function ai_stats_enrich_today_providers(array $today, array $cloudflareStats): array
{
    $providers = is_array($today['providers'] ?? null) ? $today['providers'] : [];
    $internal = is_array($providers['cloudflare_workers_ai'] ?? null)
        ? $providers['cloudflare_workers_ai']
        : ['calls' => 0, 'success' => 0, 'error' => 0];

    $cfBucket = $internal;
    if (!empty($cloudflareStats['available'])) {
        $cfBucket['worker_requests_today'] = (int)($cloudflareStats['requests_today'] ?? 0);
        $cfBucket['worker_success_today'] = (int)($cloudflareStats['success_today'] ?? 0);
        $cfBucket['worker_errors_today'] = (int)($cloudflareStats['errors_today'] ?? 0);
    }
    $providers['cloudflare_workers_ai'] = $cfBucket;
    return $providers;
}

function ai_stats_build_history(array $byDay, int $days = 14): array
{
    $keys = array_keys($byDay);
    rsort($keys);
    $keys = array_slice($keys, 0, $days);
    $history = [];
    foreach (array_reverse($keys) as $key) {
        $summary = ai_stats_summarize_day($byDay[$key] ?? null);
        $history[] = [
            'date' => $key,
            'total_success' => $summary['total_success'],
            'total_calls' => $summary['total_calls'],
            'providers' => $summary['providers'],
        ];
    }
    return $history;
}

$runtime = load_ai_runtime_config();
$store = ai_usage_load_store();
$todayKey = ai_usage_today_key();
$today = ai_stats_summarize_day($store['by_day'][$todayKey] ?? null, $store['recent'] ?? [], $todayKey);

$accountId = defined('CLOUDFLARE_ACCOUNT_ID') && is_string(CLOUDFLARE_ACCOUNT_ID) ? trim(CLOUDFLARE_ACCOUNT_ID) : '';
$apiToken = defined('CLOUDFLARE_API_TOKEN') && is_string(CLOUDFLARE_API_TOKEN) ? trim(CLOUDFLARE_API_TOKEN) : '';
$scriptName = ai_stats_worker_script_name();

$internalToday = [
    'date' => $todayKey,
    'note' => 'Log nội bộ từ mọi module: lộ trình (api/ai_explain.php), thi trực tuyến (trình duyệt + hosting), quản lý văn bản.',
    'summary' => $today,
    'recent' => array_slice($store['recent'] ?? [], 0, 30),
    'modules' => ai_stats_module_catalog(),
];

$shopaikeyStats = ai_stats_fetch_shopaikey(
    $runtime['shopaikey_enabled'] ? (string)$runtime['shopaikey_api_key'] : '',
    (string)$runtime['shopaikey_base_url']
);
$internalShop = $today['providers']['shopaikey'] ?? null;
if (is_array($internalShop)) {
    $shopaikeyStats['requests_today_internal'] = (int)($internalShop['success'] ?? 0);
    $shopaikeyStats['estimated_usd_today_internal'] = (float)($internalShop['estimated_usd'] ?? 0);
}
$shopaikeyTotalInternal = 0;
foreach ($store['by_day'] ?? [] as $dayBucket) {
    if (!is_array($dayBucket)) continue;
    $shopBucket = $dayBucket['providers']['shopaikey'] ?? null;
    if (is_array($shopBucket)) {
        $shopaikeyTotalInternal += (int)($shopBucket['success'] ?? 0);
    }
}
$shopaikeyStats['requests_total_internal'] = $shopaikeyTotalInternal;
if ($shopaikeyStats['requests'] === null && $shopaikeyTotalInternal > 0) {
    $shopaikeyStats['requests_hint'] = 'ShopAIKey API không trả tổng requests; hiển thị số lượt fallback đã log trong GiangBai.';
}

$cloudflareStats = ai_stats_fetch_cloudflare($accountId, $apiToken, $scriptName, $todayKey);
$internalCf = $today['providers']['cloudflare_workers_ai'] ?? null;
if (is_array($internalCf)) {
    $cloudflareStats['requests_today_internal'] = (int)($internalCf['success'] ?? 0);
    $cloudflareStats['errors_today_internal'] = (int)($internalCf['error'] ?? 0);
}
$today['providers'] = ai_stats_enrich_today_providers($today, $cloudflareStats);
$internalToday['summary'] = $today;

$geminiInternal = $today['providers']['gemini'] ?? null;
$geminiBrowserInternal = $today['providers']['gemini_browser'] ?? null;
$mistralInternal = $today['providers']['mistral_ocr'] ?? null;

$geminiStats = [
    'configured' => !empty($runtime['gemini_enabled']) && !empty($runtime['gemini_keys']),
    'keys_count' => count($runtime['gemini_keys'] ?? []),
    'model' => $runtime['gemini_model'],
    'requests_today_internal' => is_array($geminiInternal) ? (int)($geminiInternal['success'] ?? 0) : 0,
    'fallback_success_today' => is_array($geminiInternal) ? (int)($geminiInternal['fallback_success'] ?? 0) : 0,
    'tokens_today_internal' => is_array($geminiInternal) ? (int)($geminiInternal['total_tokens'] ?? 0) : 0,
    'message' => 'Fallback server khi hết Cloudflare (lộ trình). Khác với Gemini trình duyệt của Thi trực tuyến.',
    'dashboard_url' => 'https://aistudio.google.com/',
];

$geminiBrowserStats = [
    'requests_today_internal' => is_array($geminiBrowserInternal) ? (int)($geminiBrowserInternal['success'] ?? 0) : 0,
    'errors_today_internal' => is_array($geminiBrowserInternal) ? (int)($geminiBrowserInternal['error'] ?? 0) : 0,
    'tokens_today_internal' => is_array($geminiBrowserInternal) ? (int)($geminiBrowserInternal['total_tokens'] ?? 0) : 0,
    'message' => 'Gemini gọi từ trình duyệt / hosting fallback cho Thi trực tuyến.',
];

$mistralStats = [
    'configured' => true,
    'requests_today_internal' => is_array($mistralInternal) ? (int)($mistralInternal['success'] ?? 0) : 0,
    'errors_today_internal' => is_array($mistralInternal) ? (int)($mistralInternal['error'] ?? 0) : 0,
    'message' => 'Mistral OCR quét PDF cho Thi trực tuyến (log từ trình duyệt).',
    'dashboard_url' => 'https://console.mistral.ai/',
];

$smartQuota = ai_smart_quota_status();

respond([
    'ok' => true,
    'generated_at' => (new DateTimeImmutable('now', ai_usage_timezone()))->format(DateTimeInterface::ATOM),
    'today' => $todayKey,
    'timezone' => ai_usage_timezone()->getName(),
    'smart_quota' => $smartQuota,
    'config' => [
        'cloudflare_model' => $runtime['cloudflare_ai_model'],
        'cloudflare_worker_url' => $runtime['cloudflare_worker_url'],
        'gemini_model' => $runtime['gemini_model'],
        'shopaikey_model' => $runtime['shopaikey_model'],
    ],
    'internal' => $internalToday,
    'history' => ai_stats_build_history($store['by_day'] ?? [], 14),
    'providers' => [
        'cloudflare' => $cloudflareStats,
        'gemini' => $geminiStats,
        'gemini_browser' => $geminiBrowserStats,
        'mistral_ocr' => $mistralStats,
        'shopaikey' => $shopaikeyStats,
    ],
    'explain_cache' => ai_explain_cache_stats(),
    'ai_router' => ai_router_runtime_status($runtime),
    'student_quota_defaults' => ai_student_quota_load_config(),
    'notes' => [
        'Log nội bộ lưu tại data/ai_usage.json trên hosting.',
        'Cloudflare GraphQL đếm mọi request Worker; log nội bộ tách theo module (lộ trình, thi trực tuyến…).',
        'Lộ trình: Router AI — cache → light_ai (miễn phí) → Cloudflare → Gemini → ShopAIKey/DeepSeek (cuối cùng).',
        'Cache theo lesson_id + câu hỏi tại data/ai_explain_cache.json — không tốn quota.',
        'Quota học sinh: data/ai_student_quota.json — mặc định 25 lượt API/ngày (cache không tính).',
        'Thi trực tuyến: Mistral OCR + Gemini trình duyệt được ghi qua api/ai_usage_report.php.',
        'Smart Quota: Neurons Cloudflare ~10.000/ngày free; hết thì fallback Gemini, cuối cùng ShopAIKey.',
        'Ma trận đề / KTTX / game gọi Gemini trực tiếp — chưa ghi log (sẽ bổ sung sau nếu cần).',
    ],
]);