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
    $allowedModels = ['@cf/qwen/qwen3-30b-a3b-fp8', '@cf/meta/llama-3.2-3b-instruct'];
    $model = trim((string)$nextConfig['cloudflare_ai_model']);
    $nextConfig['cloudflare_ai_model'] = in_array($model, $allowedModels, true) ? $model : '@cf/qwen/qwen3-30b-a3b-fp8';
}
if (isset($nextConfig['gemini_enabled'])) {
    $nextConfig['gemini_enabled'] = (bool)$nextConfig['gemini_enabled'];
}
if (isset($nextConfig['light_ai_enabled'])) {
    $nextConfig['light_ai_enabled'] = (bool)$nextConfig['light_ai_enabled'];
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
