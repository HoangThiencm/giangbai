<?php
/**
 * Đọc cấu hình AI runtime — gộp api/config.php + global_config.json (Admin đã lưu).
 */

function normalize_api_keys($value): array
{
    if (is_string($value)) {
        $value = preg_split('/[\s,]+/', $value) ?: [];
    }
    if (!is_array($value)) return [];
    return array_values(array_unique(array_filter(array_map('trim', $value))));
}

/** Base URL có thể là https://host hoặc https://host/v1 — luôn chuẩn hóa về .../v1 */
function normalize_ds2api_base_url(string $baseUrl): string
{
    $baseUrl = rtrim(trim($baseUrl), '/');
    if ($baseUrl === '') return '';
    if (preg_match('#/v1$#i', $baseUrl)) return $baseUrl;
    return $baseUrl . '/v1';
}

/** DS2API tự host dùng session DeepSeek trên server — không cần Bearer key thật. */
function ds2api_effective_api_key(string $key): string
{
    $key = trim($key);
    if ($key === '' || $key === 'sk' || $key === 'sk-') return '';
    return $key;
}

function load_ai_runtime_config(): array
{
    $config = [
        'ds2api_enabled' => true,
        'ds2api_base_url' => 'https://freeapideepseek.vercel.app',
        'ds2api_api_key' => '',
        'ds2api_model' => 'deepseek-v4-flash',
        'cloudflare_worker_url' => '',
        'cloudflare_worker_secret' => '',
        'cloudflare_ai_model' => '@cf/qwen/qwen3-30b-a3b-fp8',
        'gemini_enabled' => true,
        'gemini_keys' => [],
        'gemini_model' => 'gemini-2.5-flash',
        'shopaikey_api_key' => '',
        'shopaikey_enabled' => true,
        'shopaikey_model' => 'deepseek-v4-flash',
        'shopaikey_base_url' => 'https://api.shopaikey.com/v1',
        'light_ai_enabled' => true,
    ];

    if (defined('CLOUDFLARE_AI_WORKER_URL') && is_string(CLOUDFLARE_AI_WORKER_URL)) {
        $config['cloudflare_worker_url'] = rtrim(trim(CLOUDFLARE_AI_WORKER_URL), '/');
    }
    if (defined('CLOUDFLARE_AI_WORKER_SECRET') && is_string(CLOUDFLARE_AI_WORKER_SECRET)) {
        $config['cloudflare_worker_secret'] = trim(CLOUDFLARE_AI_WORKER_SECRET);
    }
    if (defined('CLOUDFLARE_AI_MODEL') && is_string(CLOUDFLARE_AI_MODEL) && trim(CLOUDFLARE_AI_MODEL) !== '') {
        $config['cloudflare_ai_model'] = trim(CLOUDFLARE_AI_MODEL);
    }
    if (defined('GEMINI_ENABLED')) {
        $config['gemini_enabled'] = (bool)GEMINI_ENABLED;
    }
    if (defined('SHOPAIKEY_ENABLED')) {
        $config['shopaikey_enabled'] = (bool)SHOPAIKEY_ENABLED;
    }
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
    if (defined('DS2API_ENABLED')) {
        $config['ds2api_enabled'] = (bool)DS2API_ENABLED;
    }
    if (defined('DS2API_BASE_URL') && is_string(DS2API_BASE_URL) && trim(DS2API_BASE_URL) !== '') {
        $config['ds2api_base_url'] = rtrim(trim(DS2API_BASE_URL), '/');
    }
    if (defined('DS2API_API_KEY') && is_string(DS2API_API_KEY)) {
        $config['ds2api_api_key'] = trim(DS2API_API_KEY);
    }
    if (defined('DS2API_MODEL') && is_string(DS2API_MODEL) && trim(DS2API_MODEL) !== '') {
        $config['ds2api_model'] = trim(DS2API_MODEL);
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
            if (array_key_exists('gemini_enabled', $globalConfig)) {
                $config['gemini_enabled'] = (bool)$globalConfig['gemini_enabled'];
            }
            if (!empty($globalConfig['cloudflare_ai_model']) && is_string($globalConfig['cloudflare_ai_model'])) {
                $config['cloudflare_ai_model'] = trim($globalConfig['cloudflare_ai_model']);
            }
            if (!empty($globalConfig['shopaikey_api_key']) && is_string($globalConfig['shopaikey_api_key'])) {
                $config['shopaikey_api_key'] = trim($globalConfig['shopaikey_api_key']);
            }
            if (!empty($globalConfig['shopaikey_model']) && is_string($globalConfig['shopaikey_model'])) {
                $config['shopaikey_model'] = trim($globalConfig['shopaikey_model']);
            }
            if (array_key_exists('shopaikey_enabled', $globalConfig)) {
                $config['shopaikey_enabled'] = (bool)$globalConfig['shopaikey_enabled'];
            }
            if (array_key_exists('light_ai_enabled', $globalConfig)) {
                $config['light_ai_enabled'] = (bool)$globalConfig['light_ai_enabled'];
            }
            if (!empty($globalConfig['ds2api_base_url']) && is_string($globalConfig['ds2api_base_url'])) {
                $config['ds2api_base_url'] = rtrim(trim($globalConfig['ds2api_base_url']), '/');
            }
            if (!empty($globalConfig['ds2api_api_key']) && is_string($globalConfig['ds2api_api_key'])) {
                $config['ds2api_api_key'] = trim($globalConfig['ds2api_api_key']);
            }
            if (!empty($globalConfig['ds2api_model']) && is_string($globalConfig['ds2api_model'])) {
                $config['ds2api_model'] = trim($globalConfig['ds2api_model']);
            }
            if (array_key_exists('ds2api_enabled', $globalConfig)) {
                $config['ds2api_enabled'] = (bool)$globalConfig['ds2api_enabled'];
            }
        }
    }

    $config['ds2api_base_url'] = normalize_ds2api_base_url((string)($config['ds2api_base_url'] ?? ''));
    $config['ds2api_api_key'] = ds2api_effective_api_key((string)($config['ds2api_api_key'] ?? ''));

    return $config;
}

function ai_router_runtime_status(?array $config = null): array
{
    $config = $config ?? load_ai_runtime_config();
    $ds2Ready = !empty($config['ds2api_enabled'])
        && trim((string)($config['ds2api_base_url'] ?? '')) !== '';
    $cfReady = trim((string)($config['cloudflare_worker_url'] ?? '')) !== ''
        && trim((string)($config['cloudflare_worker_secret'] ?? '')) !== '';
    $geminiReady = !empty($config['gemini_enabled']) && !empty($config['gemini_keys']);
    $shopReady = !empty($config['shopaikey_enabled']) && trim((string)($config['shopaikey_api_key'] ?? '')) !== '';

    $tiers = [
        ['id' => 'cache', 'label' => 'Cache câu hỏi', 'ready' => true, 'cost' => 'free'],
        ['id' => 'light_ai', 'label' => 'Light AI (nội dung bài)', 'ready' => !empty($config['light_ai_enabled']), 'cost' => 'free'],
        ['id' => 'ds2api', 'label' => 'DS2API ' . ($config['ds2api_model'] ?? 'deepseek-v4-flash'), 'ready' => $ds2Ready, 'cost' => 'free_web'],
        ['id' => 'cloudflare', 'label' => 'Cloudflare ' . ($config['cloudflare_ai_model'] ?? ''), 'ready' => $cfReady, 'cost' => 'free'],
        ['id' => 'gemini', 'label' => 'Gemini ' . ($config['gemini_model'] ?? ''), 'ready' => $geminiReady, 'cost' => 'free', 'keys' => count($config['gemini_keys'] ?? [])],
        ['id' => 'shopaikey', 'label' => 'ShopAIKey ' . ($config['shopaikey_model'] ?? ''), 'ready' => $shopReady, 'cost' => 'paid_last'],
    ];

    $readyCount = count(array_filter($tiers, fn($t) => !empty($t['ready'])));

    return [
        'active' => true,
        'ready_tiers' => $readyCount,
        'tiers' => $tiers,
        'cloudflare_worker_configured' => $cfReady,
        'gemini_keys_count' => count($config['gemini_keys'] ?? []),
        'shopaikey_configured' => $shopReady,
        'ds2api_configured' => $ds2Ready,
        'message' => $readyCount >= 3
            ? 'Router dùng cấu hình Admin + config.php hiện có — không cần thiết lập thêm.'
            : 'Thiếu một số tầng AI — kiểm tra config.php (DS2API/Worker) hoặc Admin (Gemini/ShopAIKey).',
    ];
}