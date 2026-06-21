<?php
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/ai_usage_log.php';
require_admin_key();

function ai_stats_load_runtime(): array
{
    $config = [
        'shopaikey_api_key' => defined('SHOPAIKEY_API_KEY') && is_string(SHOPAIKEY_API_KEY) ? trim(SHOPAIKEY_API_KEY) : '',
        'shopaikey_base_url' => 'https://api.shopaikey.com/v1',
        'cloudflare_ai_model' => defined('CLOUDFLARE_AI_MODEL') && is_string(CLOUDFLARE_AI_MODEL) ? trim(CLOUDFLARE_AI_MODEL) : '@cf/qwen/qwen3-30b-a3b-fp8',
        'cloudflare_worker_url' => defined('CLOUDFLARE_AI_WORKER_URL') && is_string(CLOUDFLARE_AI_WORKER_URL) ? rtrim(trim(CLOUDFLARE_AI_WORKER_URL), '/') : '',
        'gemini_keys' => defined('GEMINI_API_KEYS') ? (array)GEMINI_API_KEYS : [],
        'gemini_model' => defined('GEMINI_MODEL') && is_string(GEMINI_MODEL) ? trim(GEMINI_MODEL) : 'gemini-2.5-flash',
        'gemini_enabled' => !defined('GEMINI_ENABLED') || (bool)GEMINI_ENABLED,
        'shopaikey_enabled' => !defined('SHOPAIKEY_ENABLED') || (bool)SHOPAIKEY_ENABLED,
        'shopaikey_model' => defined('SHOPAIKEY_MODEL') && is_string(SHOPAIKEY_MODEL) ? trim(SHOPAIKEY_MODEL) : 'deepseek-v4-flash',
    ];

    $globalConfigFile = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'global_config.json';
    if (is_file($globalConfigFile)) {
        $globalConfig = json_decode((string)@file_get_contents($globalConfigFile), true);
        if (is_array($globalConfig)) {
            if (!empty($globalConfig['shopaikey_api_key']) && is_string($globalConfig['shopaikey_api_key'])) {
                $config['shopaikey_api_key'] = trim($globalConfig['shopaikey_api_key']);
            }
            if (!empty($globalConfig['cloudflare_ai_model']) && is_string($globalConfig['cloudflare_ai_model'])) {
                $config['cloudflare_ai_model'] = trim($globalConfig['cloudflare_ai_model']);
            }
            if (!empty($globalConfig['gemini_model']) && is_string($globalConfig['gemini_model'])) {
                $config['gemini_model'] = trim($globalConfig['gemini_model']);
            }
            if (array_key_exists('gemini_enabled', $globalConfig)) {
                $config['gemini_enabled'] = (bool)$globalConfig['gemini_enabled'];
            }
            if (array_key_exists('shopaikey_enabled', $globalConfig)) {
                $config['shopaikey_enabled'] = (bool)$globalConfig['shopaikey_enabled'];
            }
            if (!empty($globalConfig['shopaikey_model']) && is_string($globalConfig['shopaikey_model'])) {
                $config['shopaikey_model'] = trim($globalConfig['shopaikey_model']);
            }
            $fileKeys = [];
            if (array_key_exists('gemini_keys', $globalConfig)) {
                $fileKeys = is_array($globalConfig['gemini_keys'])
                    ? $globalConfig['gemini_keys']
                    : (preg_split('/[\s,]+/', (string)$globalConfig['gemini_keys']) ?: []);
            } elseif (array_key_exists('global_gemini_keys', $globalConfig)) {
                $fileKeys = is_array($globalConfig['global_gemini_keys'])
                    ? $globalConfig['global_gemini_keys']
                    : (preg_split('/[\s,]+/', (string)$globalConfig['global_gemini_keys']) ?: []);
            }
            $fileKeys = array_values(array_unique(array_filter(array_map('trim', $fileKeys))));
            if (!empty($fileKeys)) {
                $config['gemini_keys'] = $fileKeys;
            }
        }
    }

    return $config;
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

function ai_stats_summarize_day(?array $day): array
{
    if (!is_array($day)) {
        return [
            'providers' => [],
            'by_mode' => ['explain' => 0, 'chat' => 0],
            'total_success' => 0,
            'total_calls' => 0,
        ];
    }
    $providers = is_array($day['providers'] ?? null) ? $day['providers'] : [];
    $byMode = is_array($day['by_mode'] ?? null) ? $day['by_mode'] : ['explain' => 0, 'chat' => 0];
    $totalSuccess = 0;
    $totalCalls = 0;
    foreach ($providers as $bucket) {
        if (!is_array($bucket)) continue;
        $totalSuccess += (int)($bucket['success'] ?? 0);
        $totalCalls += (int)($bucket['calls'] ?? 0);
    }
    return [
        'providers' => $providers,
        'by_mode' => $byMode,
        'total_success' => $totalSuccess,
        'total_calls' => $totalCalls,
    ];
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

$runtime = ai_stats_load_runtime();
$store = ai_usage_load_store();
$todayKey = ai_usage_today_key();
$today = ai_stats_summarize_day($store['by_day'][$todayKey] ?? null);

$accountId = defined('CLOUDFLARE_ACCOUNT_ID') && is_string(CLOUDFLARE_ACCOUNT_ID) ? trim(CLOUDFLARE_ACCOUNT_ID) : '';
$apiToken = defined('CLOUDFLARE_API_TOKEN') && is_string(CLOUDFLARE_API_TOKEN) ? trim(CLOUDFLARE_API_TOKEN) : '';
$scriptName = ai_stats_worker_script_name();

$internalToday = [
    'date' => $todayKey,
    'module' => 'lotrinh_ai_explain',
    'note' => 'Chỉ tính lượt gọi qua api/ai_explain.php (AI lộ trình học). Gemini trên trình duyệt (vẽ hình, game, smartquiz…) không đi qua log này.',
    'summary' => $today,
    'recent' => array_slice($store['recent'] ?? [], 0, 30),
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

$geminiInternal = $today['providers']['gemini'] ?? null;
$geminiStats = [
    'configured' => !empty($runtime['gemini_enabled']) && !empty($runtime['gemini_keys']),
    'keys_count' => count($runtime['gemini_keys'] ?? []),
    'model' => $runtime['gemini_model'],
    'requests_today_internal' => is_array($geminiInternal) ? (int)($geminiInternal['success'] ?? 0) : 0,
    'fallback_success_today' => is_array($geminiInternal) ? (int)($geminiInternal['fallback_success'] ?? 0) : 0,
    'tokens_today_internal' => is_array($geminiInternal) ? (int)($geminiInternal['total_tokens'] ?? 0) : 0,
    'message' => 'Gemini free tier không có API quota còn lại theo ngày. Số liệu dưới đây chỉ phản ánh fallback qua api/ai_explain.php.',
    'dashboard_url' => 'https://aistudio.google.com/',
];

respond([
    'ok' => true,
    'generated_at' => (new DateTimeImmutable('now', ai_usage_timezone()))->format(DateTimeInterface::ATOM),
    'today' => $todayKey,
    'timezone' => ai_usage_timezone()->getName(),
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
        'shopaikey' => $shopaikeyStats,
    ],
    'notes' => [
        'Log nội bộ lưu tại data/ai_usage.json trên hosting.',
        'Cloudflare GraphQL cần API token có quyền Account Analytics (Read).',
        'ShopAIKey dùng endpoint OpenAI-compatible /v1/dashboard/billing/*.',
        'Các module gọi Gemini trực tiếp từ trình duyệt không xuất hiện trong log nội bộ.',
    ],
]);