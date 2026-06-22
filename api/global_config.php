<?php
require_once __DIR__ . '/helpers.php';
require_admin_key();

$configFile = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'global_config.json';
$method = $_SERVER['REQUEST_METHOD'];

function read_global_config_file(string $path): array
{
    if (!file_exists($path)) {
        return ['features' => new stdClass(), 'user_features' => new stdClass()];
    }

    $raw = file_get_contents($path);
    $data = json_decode($raw ?: '{}', true);
    return is_array($data) ? $data : ['features' => new stdClass(), 'user_features' => new stdClass()];
}

if ($method === 'GET') {
    respond(['ok' => true, 'config' => read_global_config_file($configFile)]);
}

if ($method !== 'POST') {
    respond(['error' => 'Method not allowed.'], 405);
}

$data = json_body();
$nextConfig = $data['config'] ?? null;

if (!is_array($nextConfig)) {
    respond(['error' => 'Thieu cau hinh can luu.'], 422);
}

if (!isset($nextConfig['features']) || !is_array($nextConfig['features'])) {
    $nextConfig['features'] = [];
}
if (!isset($nextConfig['user_features']) || !is_array($nextConfig['user_features'])) {
    $nextConfig['user_features'] = [];
}
if (isset($nextConfig['gemini_keys'])) {
    $keys = is_array($nextConfig['gemini_keys']) ? $nextConfig['gemini_keys'] : preg_split('/[\r\n,]+/', (string)$nextConfig['gemini_keys']);
    $nextConfig['gemini_keys'] = array_values(array_unique(array_filter(array_map('trim', $keys ?: []))));
}
if (isset($nextConfig['gemini_model'])) {
    $nextConfig['gemini_model'] = trim((string)$nextConfig['gemini_model']) ?: 'gemini-2.5-flash';
}
if (isset($nextConfig['cloudflare_ai_model'])) {
    $model = trim((string)$nextConfig['cloudflare_ai_model']);
    $nextConfig['cloudflare_ai_model'] = preg_match('#^@cf/[a-z0-9._-]+/[a-z0-9._-]+$#i', $model)
        ? $model
        : '@cf/qwen/qwen3-30b-a3b-fp8';
}
if (isset($nextConfig['gemini_enabled'])) {
    $nextConfig['gemini_enabled'] = (bool)$nextConfig['gemini_enabled'];
}
if (isset($nextConfig['mistral_keys'])) {
    $keys = is_array($nextConfig['mistral_keys']) ? $nextConfig['mistral_keys'] : preg_split('/[\r\n,]+/', (string)$nextConfig['mistral_keys']);
    $nextConfig['mistral_keys'] = array_values(array_unique(array_filter(array_map('trim', $keys ?: []))));
}
if (isset($nextConfig['mistral_ocr_model'])) {
    $model = trim((string)$nextConfig['mistral_ocr_model']) ?: 'mistral-ocr-latest';
    $nextConfig['mistral_ocr_model'] = preg_match('/^mistral-ocr/i', $model) ? $model : 'mistral-ocr-latest';
}
if (isset($nextConfig['mistral_enabled'])) {
    $nextConfig['mistral_enabled'] = (bool)$nextConfig['mistral_enabled'];
}
if (isset($nextConfig['light_ai_enabled'])) {
    $nextConfig['light_ai_enabled'] = (bool)$nextConfig['light_ai_enabled'];
}
if (array_key_exists('ai_explain_cache_enabled', $nextConfig)) {
    $nextConfig['ai_explain_cache_enabled'] = (bool)$nextConfig['ai_explain_cache_enabled'];
}
if (isset($nextConfig['ai_explain_cache_max_entries'])) {
    $nextConfig['ai_explain_cache_max_entries'] = max(100, min(20000, (int)$nextConfig['ai_explain_cache_max_entries']));
}
if (isset($nextConfig['ai_explain_cache_ttl_days'])) {
    $nextConfig['ai_explain_cache_ttl_days'] = max(1, min(365, (int)$nextConfig['ai_explain_cache_ttl_days']));
}
if (isset($nextConfig['shopaikey_api_key'])) {
    $nextConfig['shopaikey_api_key'] = trim((string)$nextConfig['shopaikey_api_key']);
}
if (isset($nextConfig['shopaikey_model'])) {
    $nextConfig['shopaikey_model'] = trim((string)$nextConfig['shopaikey_model']) ?: 'deepseek-v4-flash';
}
if (isset($nextConfig['shopaikey_enabled'])) {
    $nextConfig['shopaikey_enabled'] = (bool)$nextConfig['shopaikey_enabled'];
}
if (isset($nextConfig['hf_fallback_url'])) {
    $nextConfig['hf_fallback_url'] = rtrim(trim((string)$nextConfig['hf_fallback_url']), '/');
}
if (array_key_exists('hf_fallback_enabled', $nextConfig)) {
    $nextConfig['hf_fallback_enabled'] = (bool)$nextConfig['hf_fallback_enabled'];
}
if (array_key_exists('smart_quota_enabled', $nextConfig)) {
    $nextConfig['smart_quota_enabled'] = (bool)$nextConfig['smart_quota_enabled'];
}
if (isset($nextConfig['cloudflare_neurons_daily_limit'])) {
    $nextConfig['cloudflare_neurons_daily_limit'] = max(100, (int)$nextConfig['cloudflare_neurons_daily_limit']);
}
if (isset($nextConfig['smart_quota_warn_pct'])) {
    $nextConfig['smart_quota_warn_pct'] = max(1, min(99, (int)$nextConfig['smart_quota_warn_pct']));
}
if (isset($nextConfig['smart_quota_critical_pct'])) {
    $nextConfig['smart_quota_critical_pct'] = max(0, min(99, (int)$nextConfig['smart_quota_critical_pct']));
}
if (isset($nextConfig['smart_quota_exhausted_mode'])) {
    $mode = (string)$nextConfig['smart_quota_exhausted_mode'];
    $nextConfig['smart_quota_exhausted_mode'] = in_array($mode, ['fallback', 'block'], true) ? $mode : 'fallback';
}
if (isset($nextConfig['smart_quota_avg_neurons'])) {
    $nextConfig['smart_quota_avg_neurons'] = max(50, (int)$nextConfig['smart_quota_avg_neurons']);
}

$json = json_encode($nextConfig, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
if ($json === false) {
    respond(['error' => 'Khong ma hoa duoc cau hinh.'], 500);
}

$tmpFile = $configFile . '.tmp';
if (file_put_contents($tmpFile, $json . PHP_EOL, LOCK_EX) === false || !rename($tmpFile, $configFile)) {
    @unlink($tmpFile);
    respond(['error' => 'Khong ghi duoc global_config.json. Kiem tra quyen ghi tren hosting.'], 500);
}

respond(['ok' => true, 'config' => $nextConfig]);
