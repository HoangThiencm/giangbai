<?php

function hf_read_global_config(): array
{
    $path = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'global_config.json';
    if (!is_file($path)) return [];
    $data = json_decode((string)@file_get_contents($path), true);
    return is_array($data) ? $data : [];
}

function hf_fallback_enabled(): bool
{
    $cfg = hf_read_global_config();
    if (array_key_exists('hf_fallback_enabled', $cfg)) {
        return (bool)$cfg['hf_fallback_enabled'];
    }
    return true;
}

function hf_client_allows_server_fallback(): bool
{
    $client = strtolower(trim((string)($_SERVER['HTTP_X_GIANGBAI_CLIENT_HF_FALLBACK'] ?? '')));
    if (in_array($client, ['0', 'false', 'off', 'no'], true)) {
        return false;
    }
    return true;
}

function hf_should_proxy(): bool
{
    return hf_fallback_enabled() && hf_client_allows_server_fallback();
}

function hf_fallback_base_url(): string
{
    if (defined('HF_FALLBACK_URL') && is_string(HF_FALLBACK_URL) && trim(HF_FALLBACK_URL) !== '') {
        return rtrim(trim(HF_FALLBACK_URL), '/');
    }
    $cfg = hf_read_global_config();
    $url = trim((string)($cfg['hf_fallback_url'] ?? $cfg['omr_backend_url'] ?? ''));
    if ($url !== '') return rtrim($url, '/');
    return 'https://hoangthiencm-giangbai.hf.space';
}

function hf_proxy_request(string $method, string $path, ?array $jsonBody = null, ?array $multipart = null, int $timeout = 180): array
{
    $url = hf_fallback_base_url() . $path;
    $ch = curl_init($url);
    $opts = [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CUSTOMREQUEST => strtoupper($method),
        CURLOPT_TIMEOUT => $timeout,
        CURLOPT_FOLLOWLOCATION => true,
    ];

    if (is_array($multipart) && count($multipart) > 0) {
        $opts[CURLOPT_POSTFIELDS] = $multipart;
    } elseif ($jsonBody !== null) {
        $opts[CURLOPT_POSTFIELDS] = json_encode($jsonBody, JSON_UNESCAPED_UNICODE);
        $opts[CURLOPT_HTTPHEADER] = ['Content-Type: application/json'];
    }

    curl_setopt_array($ch, $opts);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $contentType = (string)curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
    $error = curl_error($ch);
    curl_close($ch);

    return [
        'raw' => $raw === false ? '' : $raw,
        'status' => $status,
        'content_type' => $contentType,
        'error' => $error,
    ];
}

function hf_proxy_json_or_respond(string $method, string $path, ?array $jsonBody = null, ?array $multipart = null, int $timeout = 180): void
{
    if (!hf_should_proxy()) {
        respond([
            'status' => 'error',
            'message' => 'Hosting không xử lý được và fallback HuggingFace đang tắt. Bật nút "HF dự phòng" trên menu để thử lại.',
            'data' => [],
        ], 502);
    }

    $proxy = hf_proxy_request($method, $path, $jsonBody, $multipart, $timeout);
    if ($proxy['raw'] === '' && $proxy['error'] !== '') {
        respond(['error' => 'Không kết nối được HuggingFace: ' . $proxy['error']], 502);
    }

    $status = $proxy['status'] > 0 ? $proxy['status'] : 502;
    header('X-Giangbai-Source: hf-fallback');
    if ($proxy['content_type'] !== '') {
        header('Content-Type: ' . $proxy['content_type']);
    } else {
        header('Content-Type: application/json; charset=utf-8');
    }
    http_response_code($status);
    echo $proxy['raw'];
    exit;
}

function hf_proxy_binary_or_respond(string $method, string $path, ?array $multipart = null, int $timeout = 300): void
{
    if (!hf_should_proxy()) {
        respond(['error' => 'Hosting không xử lý được và fallback HuggingFace đang tắt.'], 502);
    }

    $proxy = hf_proxy_request($method, $path, null, $multipart, $timeout);
    if ($proxy['raw'] === '' && $proxy['error'] !== '') {
        respond(['error' => 'Không kết nối được HuggingFace: ' . $proxy['error']], 502);
    }

    $status = $proxy['status'] > 0 ? $proxy['status'] : 502;
    header('X-Giangbai-Source: hf-fallback');
    if ($proxy['content_type'] !== '') {
        header('Content-Type: ' . $proxy['content_type']);
    }
    http_response_code($status);
    echo $proxy['raw'];
    exit;
}

function hf_normalize_api_keys($value): array
{
    if (is_string($value)) {
        $value = preg_split('/[\s,]+/', $value) ?: [];
    }
    if (!is_array($value)) return [];
    return array_values(array_unique(array_filter(array_map('trim', $value))));
}

function hf_load_gemini_keys(?array $requestKeys = null): array
{
    $keys = hf_normalize_api_keys($requestKeys);
    if (!empty($keys)) return $keys;

    if (defined('GEMINI_API_KEYS')) {
        $keys = hf_normalize_api_keys(GEMINI_API_KEYS);
        if (!empty($keys)) return $keys;
    }

    $cfg = hf_read_global_config();
    foreach (['gemini_keys', 'global_gemini_keys'] as $field) {
        if (!empty($cfg[$field])) {
            $keys = hf_normalize_api_keys($cfg[$field]);
            if (!empty($keys)) return $keys;
        }
    }

    return [];
}

function hf_default_gemini_model(): string
{
    if (defined('GEMINI_MODEL') && is_string(GEMINI_MODEL) && trim(GEMINI_MODEL) !== '') {
        return trim(GEMINI_MODEL);
    }
    $cfg = hf_read_global_config();
    $model = trim((string)($cfg['gemini_model'] ?? ''));
    return $model !== '' ? $model : 'gemini-2.5-flash';
}

function hf_call_gemini_vision(array $apiKeys, string $prompt, string $imageBase64, string $model, int $retries = 3): array
{
    $keys = hf_normalize_api_keys($apiKeys);
    if (empty($keys)) return ['ok' => false, 'error' => 'Thiếu Gemini API key.'];

    shuffle($keys);
    $lastError = 'Gemini không phản hồi.';
    $attempts = min(count($keys), max(1, $retries));

    for ($i = 0; $i < $attempts; $i++) {
        $key = $keys[$i];
        $payload = json_encode([
            'contents' => [[
                'parts' => [
                    ['text' => $prompt],
                    ['inline_data' => ['mime_type' => 'image/jpeg', 'data' => $imageBase64]],
                ],
            ]],
            'generationConfig' => [
                'temperature' => 0.1,
                'maxOutputTokens' => 8192,
            ],
        ], JSON_UNESCAPED_UNICODE);

        $url = 'https://generativelanguage.googleapis.com/v1beta/models/' . rawurlencode($model) . ':generateContent?key=' . rawurlencode($key);
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
            CURLOPT_POSTFIELDS => $payload,
            CURLOPT_TIMEOUT => 150,
        ]);
        $raw = curl_exec($ch);
        $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curlError = curl_error($ch);
        curl_close($ch);

        if ($raw === false || $raw === '') {
            $lastError = $curlError !== '' ? $curlError : $lastError;
            continue;
        }
        if ($status < 200 || $status >= 300) {
            $lastError = 'Gemini HTTP ' . $status;
            continue;
        }

        $response = json_decode($raw, true);
        if (!is_array($response)) {
            $lastError = 'Gemini trả về JSON không hợp lệ.';
            continue;
        }

        $text = '';
        $parts = $response['candidates'][0]['content']['parts'] ?? [];
        foreach ($parts as $part) {
            if (!empty($part['text'])) $text .= $part['text'];
        }
        $text = trim($text);
        if ($text === '') {
            $lastError = 'Gemini không trả về nội dung.';
            continue;
        }

        if (str_contains($text, '```json')) {
            $text = trim(explode('```', explode('```json', $text)[1] ?? '')[0] ?? $text);
        } elseif (str_contains($text, '```')) {
            $text = trim(str_replace('```', '', $text));
        }

        $decoded = json_decode($text, true);
        if (is_array($decoded)) {
            if (isset($decoded[0]) || array_is_list($decoded)) {
                return ['ok' => true, 'data' => $decoded];
            }
            return ['ok' => true, 'data' => [$decoded]];
        }

        return ['ok' => true, 'data' => $text];
    }

    return ['ok' => false, 'error' => $lastError];
}