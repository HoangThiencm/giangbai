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

function hf_parse_user_stored_keys($raw): array
{
    if (function_exists('parse_stored_api_keys')) {
        return parse_stored_api_keys($raw);
    }
    if (is_string($raw) && trim($raw) !== '') {
        $decoded = json_decode($raw, true);
        $raw = is_array($decoded) ? $decoded : (preg_split('/[\r\n,;]+/', $raw) ?: []);
    }
    if (is_array($raw) && isset($raw['keys']) && is_array($raw['keys'])) {
        $raw = $raw['keys'];
    }
    if (!is_array($raw)) return [];
    $secret = '';
    if (defined('API_KEY_ENCRYPTION_SECRET') && is_string(API_KEY_ENCRYPTION_SECRET) && API_KEY_ENCRYPTION_SECRET !== '') {
        $secret = API_KEY_ENCRYPTION_SECRET;
    } elseif (defined('ADMIN_KEY') && is_string(ADMIN_KEY) && ADMIN_KEY !== '') {
        $secret = ADMIN_KEY . '|giangbai-user-api-keys';
    } else {
        $secret = 'giangbai-user-api-keys-fallback';
    }
    $keyMaterial = hash('sha256', $secret, true);
    $out = [];
    foreach ($raw as $item) {
        if (is_array($item) || is_object($item)) continue;
        $value = trim((string)$item);
        if ($value === '') continue;
        if (strncmp($value, 'enc:v1:', 7) === 0) {
            $blob = base64_decode(substr($value, 7), true);
            if (!is_string($blob) || strlen($blob) < 17) continue;
            $plain = openssl_decrypt(substr($blob, 16), 'AES-256-CBC', $keyMaterial, OPENSSL_RAW_DATA, substr($blob, 0, 16));
            $value = is_string($plain) ? trim($plain) : '';
        }
        if (strlen($value) > 10 && !in_array($value, $out, true)) {
            $out[] = $value;
        }
    }
    return $out;
}

function hf_load_gemini_keys(?array $requestKeys = null): array
{
    $keys = hf_normalize_api_keys($requestKeys);
    if (!empty($keys)) return $keys;

    // Nạp key cá nhân của user từ CSDL (ưu tiên hơn key admin/config)
    try {
        $configPath = __DIR__ . '/config.php';
        if (is_file($configPath)) {
            require_once $configPath;
        }
        if (defined('APP_SESSION_NAME') && session_status() === PHP_SESSION_NONE) {
            session_name(APP_SESSION_NAME);
        }
        if (session_status() === PHP_SESSION_NONE) {
            session_start();
        }
        if (!empty($_SESSION['user_id'])) {
            $pdo = $GLOBALS['pdo'] ?? null;
            if (!$pdo instanceof PDO && defined('DB_HOST')) {
                try {
                    $pdo = new PDO(
                        'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4',
                        DB_USER,
                        DB_PASS,
                        [
                            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                            PDO::ATTR_EMULATE_PREPARES => false,
                        ]
                    );
                    $GLOBALS['pdo'] = $pdo;
                } catch (Throwable $e) {
                    $pdo = null;
                }
            }
            if ($pdo instanceof PDO) {
                $userStmt = $pdo->prepare('SELECT gemini_keys FROM users WHERE id = ? LIMIT 1');
                $userStmt->execute([(int)$_SESSION['user_id']]);
                $userRow = $userStmt->fetch();
                if ($userRow && !empty($userRow['gemini_keys'])) {
                    $userKeys = hf_parse_user_stored_keys($userRow['gemini_keys']);
                    if (!empty($userKeys)) return $userKeys;
                }
            }
        }
    } catch (Throwable $e) {
        // fallthrough to admin keys
    }

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