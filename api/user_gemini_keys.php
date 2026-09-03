<?php
require_once __DIR__ . '/helpers.php';
if (session_status() === PHP_SESSION_NONE) { session_start(); }

if (empty($_SESSION['user_id'])) {
    respond(['error' => 'Chưa đăng nhập.'], 401);
}

$userId = (int)$_SESSION['user_id'];
ensure_users_ai_key_columns($pdo);

function looks_like_masked_api_key(string $key): bool
{
    return str_contains($key, '...****') || str_ends_with($key, '****');
}

function filter_posted_api_keys(array $keys): array
{
    $clean = [];
    foreach ($keys as $key) {
        $value = trim((string)$key);
        if ($value === '' || looks_like_masked_api_key($value) || is_encrypted_user_api_key($value)) {
            continue;
        }
        if (strlen($value) > 10 && !in_array($value, $clean, true)) {
            $clean[] = $value;
        }
    }
    return $clean;
}

function read_user_key_column_raw(PDO $pdo, int $userId, string $column): ?string
{
    if ($column !== 'gemini_keys' && $column !== 'mistral_keys') {
        respond(['error' => 'Cột key không hợp lệ.'], 400);
    }
    $stmt = $pdo->prepare("SELECT {$column} FROM users WHERE id = ? LIMIT 1");
    $stmt->execute([$userId]);
    $row = $stmt->fetch() ?: [];
    $value = $row[$column] ?? null;
    return is_string($value) ? $value : null;
}

function save_user_key_column(PDO $pdo, int $userId, string $column, array $keys): void
{
    if ($column !== 'gemini_keys' && $column !== 'mistral_keys') {
        respond(['error' => 'Cột key không hợp lệ.'], 400);
    }
    if (empty($keys)) {
        $stmt = $pdo->prepare("UPDATE users SET {$column} = NULL WHERE id = ?");
        $stmt->execute([$userId]);
        return;
    }
    $stmt = $pdo->prepare("UPDATE users SET {$column} = ? WHERE id = ?");
    $stmt->execute([encode_stored_api_keys($keys), $userId]);
}

function maybe_upgrade_user_key_column(PDO $pdo, int $userId, string $column, $raw): array
{
    $plain = parse_stored_api_keys($raw);
    if ($raw && stored_api_keys_need_encryption($raw) && $plain) {
        save_user_key_column($pdo, $userId, $column, $plain);
        $raw = read_user_key_column_raw($pdo, $userId, $column);
    }
    $bundle = stored_api_keys_items($raw);
    return [
        'keys' => $plain,
        'updated_at' => $bundle['updated_at'] ?: null,
    ];
}

function public_ai_keys_payload(PDO $pdo, int $userId): array
{
    $stmt = $pdo->prepare('SELECT gemini_keys, mistral_keys FROM users WHERE id = ? LIMIT 1');
    $stmt->execute([$userId]);
    $row = $stmt->fetch() ?: [];
    $gemini = maybe_upgrade_user_key_column($pdo, $userId, 'gemini_keys', $row['gemini_keys'] ?? null);
    $mistral = maybe_upgrade_user_key_column($pdo, $userId, 'mistral_keys', $row['mistral_keys'] ?? null);
    return [
        'ok' => true,
        'count' => count($gemini['keys']),
        'keys' => $gemini['keys'],
        'masked_keys' => array_values(array_filter(array_map('mask_user_api_key', $gemini['keys']))),
        'updated_at' => $gemini['updated_at'],
        'mistral_count' => count($mistral['keys']),
        'mistral_keys' => $mistral['keys'],
        'masked_mistral_keys' => array_values(array_filter(array_map('mask_user_api_key', $mistral['keys']))),
        'mistral_updated_at' => $mistral['updated_at'],
    ];
}

function test_gemini_api_key(string $key): array
{
    $url = 'https://generativelanguage.googleapis.com/v1beta/models?key=' . rawurlencode($key);
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 8,
        CURLOPT_TIMEOUT => 20,
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);
    $ok = $status >= 200 && $status < 300;
    return [
        'valid' => $ok,
        'status' => $status,
        'error' => $ok ? '' : ($curlError !== '' ? $curlError : ('HTTP ' . $status)),
    ];
}

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$body = $method === 'GET' ? [] : json_body();
$action = trim((string)($body['action'] ?? ($_GET['action'] ?? '')));

if ($method === 'GET') {
    respond(public_ai_keys_payload($pdo, $userId));
}

if ($method === 'POST' && $action === 'test') {
    $stmt = $pdo->prepare('SELECT gemini_keys FROM users WHERE id = ? LIMIT 1');
    $stmt->execute([$userId]);
    $row = $stmt->fetch() ?: [];
    $keys = parse_stored_api_keys($row['gemini_keys'] ?? null);
    if (!$keys) {
        respond(['ok' => false, 'error' => 'Tài khoản chưa có Gemini API Key.', 'results' => []], 422);
    }
    $results = [];
    foreach ($keys as $index => $key) {
        $probe = test_gemini_api_key($key);
        $results[] = [
            'index' => $index + 1,
            'masked' => mask_user_api_key($key),
            'valid' => $probe['valid'],
            'status' => $probe['status'],
            'error' => $probe['error'],
        ];
    }
    $validCount = count(array_filter($results, static fn(array $item): bool => !empty($item['valid'])));
    respond([
        'ok' => $validCount > 0,
        'tested' => count($results),
        'valid_count' => $validCount,
        'results' => $results,
    ]);
}

if ($method === 'POST') {
    $hasGemini = array_key_exists('keys', $body) || array_key_exists('api_keys', $body) || array_key_exists('gemini_keys', $body);
    $hasMistral = array_key_exists('mistral_keys', $body);

    if (!$hasGemini && !$hasMistral) {
        respond(['error' => 'Gửi keys (Gemini) và/hoặc mistral_keys.'], 422);
    }

    if ($hasGemini) {
        $rawInput = $body['keys'] ?? $body['api_keys'] ?? $body['gemini_keys'] ?? null;
        $collected = collect_api_keys_from_input($rawInput);
        // Resolve masked keys: if a submitted key looks masked, restore the real key from DB
        $existingKeys = parse_stored_api_keys(read_user_key_column_raw($pdo, $userId, 'gemini_keys'));
        $resolved = [];
        foreach ($collected as $k) {
            $trimmed = trim((string)$k);
            if (looks_like_masked_api_key($trimmed)) {
                foreach ($existingKeys as $realKey) {
                    if (mask_user_api_key($realKey) === $trimmed) {
                        $resolved[] = $realKey;
                        break;
                    }
                }
                continue;
            }
            $resolved[] = $trimmed;
        }
        $incoming = filter_posted_api_keys($resolved);
        if ($action === 'add') {
            $incoming = array_values(array_unique(array_merge($existingKeys, $incoming)));
        }
        save_user_key_column($pdo, $userId, 'gemini_keys', $incoming);
    }
    if ($hasMistral) {
        $rawMistral = collect_api_keys_from_input($body['mistral_keys'] ?? null);
        $existingMistral = parse_stored_api_keys(read_user_key_column_raw($pdo, $userId, 'mistral_keys'));
        $resolvedMistral = [];
        foreach ($rawMistral as $k) {
            $trimmed = trim((string)$k);
            if (looks_like_masked_api_key($trimmed)) {
                foreach ($existingMistral as $realKey) {
                    if (mask_user_api_key($realKey) === $trimmed) {
                        $resolvedMistral[] = $realKey;
                        break;
                    }
                }
                continue;
            }
            $resolvedMistral[] = $trimmed;
        }
        $incoming = filter_posted_api_keys($resolvedMistral);
        if ($action === 'add') {
            $incoming = array_values(array_unique(array_merge($existingMistral, $incoming)));
        }
        save_user_key_column($pdo, $userId, 'mistral_keys', $incoming);
    }

    respond(public_ai_keys_payload($pdo, $userId));
}

if ($method === 'DELETE') {
    $stmt = $pdo->prepare('UPDATE users SET gemini_keys = NULL, mistral_keys = NULL WHERE id = ?');
    $stmt->execute([$userId]);

    respond([
        'ok' => true,
        'count' => 0,
        'keys' => [],
        'masked_keys' => [],
        'updated_at' => null,
        'mistral_count' => 0,
        'mistral_keys' => [],
        'masked_mistral_keys' => [],
        'mistral_updated_at' => null,
    ]);
}

respond(['error' => 'Method not allowed.'], 405);
