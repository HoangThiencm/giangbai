<?php
require_once __DIR__ . '/helpers.php';

function site_features_public_map($value): array
{
    if (!is_array($value)) {
        return [];
    }
    $blocked = [
        'gemini_keys', 'mistral_keys', 'groq_keys', 'api_keys', 'api_key',
        'github_pat', 'github_token', 'shopaikey_api_key', 'hf_token', 'password',
    ];
    $safe = [];
    foreach ($value as $key => $item) {
        if (in_array(strtolower((string)$key), $blocked, true) || is_array($item)) {
            continue;
        }
        $safe[$key] = $item;
    }
    return $safe;
}

$path = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'global_config.json';
$cfg = [];
if (is_file($path)) {
    $decoded = json_decode((string)file_get_contents($path), true);
    if (is_array($decoded)) {
        $cfg = $decoded;
    }
}

$userFeatures = [];
foreach (($cfg['user_features'] ?? []) as $account => $flags) {
    if (!is_string($account) || $account === '') {
        continue;
    }
    $userFeatures[$account] = site_features_public_map($flags);
}

respond([
    'ok' => true,
    'features' => site_features_public_map($cfg['features'] ?? []),
    'user_features' => $userFeatures,
    'gemini_model' => trim((string)($cfg['gemini_model'] ?? '')),
    'gemini_enabled' => !array_key_exists('gemini_enabled', $cfg) || (bool)$cfg['gemini_enabled'],
    'groq_model' => trim((string)($cfg['groq_model'] ?? '')),
    'mistral_ocr_model' => trim((string)($cfg['mistral_ocr_model'] ?? '')),
    'mistral_enabled' => !array_key_exists('mistral_enabled', $cfg) || (bool)$cfg['mistral_enabled'],
]);
