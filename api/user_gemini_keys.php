<?php
require_once __DIR__ . '/helpers.php';
session_start();

if (empty($_SESSION['user_id'])) {
    respond(['error' => 'Chưa đăng nhập.'], 401);
}

$userId = (int)$_SESSION['user_id'];
ensure_users_ai_key_columns($pdo);

function read_user_ai_keys(PDO $pdo, int $userId): array
{
    $stmt = $pdo->prepare('SELECT gemini_keys, mistral_keys FROM users WHERE id = ? LIMIT 1');
    $stmt->execute([$userId]);
    $row = $stmt->fetch() ?: [];
    $gemini = parse_stored_api_keys($row['gemini_keys'] ?? null);
    $mistral = parse_stored_api_keys($row['mistral_keys'] ?? null);
    return [
        'ok' => true,
        'keys' => $gemini,
        'mistral_keys' => $mistral,
        'count' => count($gemini),
        'mistral_count' => count($mistral),
    ];
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
    $json = json_encode($keys, JSON_UNESCAPED_UNICODE);
    $stmt = $pdo->prepare("UPDATE users SET {$column} = ? WHERE id = ?");
    $stmt->execute([$json, $userId]);
}

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

if ($method === 'GET') {
    respond(read_user_ai_keys($pdo, $userId));
}

if ($method === 'POST') {
    $body = json_body();
    $hasGemini = array_key_exists('keys', $body) || array_key_exists('api_keys', $body);
    $hasMistral = array_key_exists('mistral_keys', $body);

    if (!$hasGemini && !$hasMistral) {
        respond(['error' => 'Gửi keys (Gemini) và/hoặc mistral_keys.'], 422);
    }

    if ($hasGemini) {
        save_user_key_column($pdo, $userId, 'gemini_keys', collect_api_keys_from_input($body['keys'] ?? $body['api_keys'] ?? null));
    }
    if ($hasMistral) {
        save_user_key_column($pdo, $userId, 'mistral_keys', collect_api_keys_from_input($body['mistral_keys'] ?? null));
    }

    respond(read_user_ai_keys($pdo, $userId));
}

if ($method === 'DELETE') {
    $stmt = $pdo->prepare('UPDATE users SET gemini_keys = NULL, mistral_keys = NULL WHERE id = ?');
    $stmt->execute([$userId]);

    respond([
        'ok' => true,
        'keys' => [],
        'mistral_keys' => [],
        'count' => 0,
        'mistral_count' => 0,
    ]);
}

respond(['error' => 'Method not allowed.'], 405);
