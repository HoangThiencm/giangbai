<?php
require_once __DIR__ . '/helpers.php';
session_start();

if (empty($_SESSION['user_id'])) {
    respond(['error' => 'Chưa đăng nhập.'], 401);
}

$userId = (int)$_SESSION['user_id'];
ensure_users_gemini_keys_column($pdo);

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

if ($method === 'GET') {
    $stmt = $pdo->prepare('SELECT gemini_keys FROM users WHERE id = ? LIMIT 1');
    $stmt->execute([$userId]);
    $row = $stmt->fetch();

    $keys = [];
    $raw = $row['gemini_keys'] ?? null;
    if (is_string($raw) && trim($raw) !== '') {
        $decoded = json_decode($raw, true);
        if (is_array($decoded)) {
            foreach ($decoded as $k) {
                $k = trim((string)$k);
                if (strlen($k) > 10 && !in_array($k, $keys, true)) {
                    $keys[] = $k;
                }
            }
        }
    }

    respond([
        'ok' => true,
        'keys' => $keys,
        'count' => count($keys),
    ]);
}

if ($method === 'POST') {
    $body = json_body();
    $rawInput = $body['keys'] ?? $body['api_keys'] ?? null;

    $inputItems = [];
    if (is_array($rawInput)) {
        $inputItems = $rawInput;
    } elseif (is_string($rawInput)) {
        $inputItems = preg_split('/[\r\n,;]+/', $rawInput) ?: [];
    }

    $cleanKeys = [];
    foreach ($inputItems as $item) {
        $k = trim((string)$item);
        if (strlen($k) > 10 && !in_array($k, $cleanKeys, true)) {
            $cleanKeys[] = $k;
        }
    }

    if (empty($cleanKeys)) {
        $stmt = $pdo->prepare('UPDATE users SET gemini_keys = NULL WHERE id = ?');
        $stmt->execute([$userId]);
    } else {
        $json = json_encode($cleanKeys, JSON_UNESCAPED_UNICODE);
        $stmt = $pdo->prepare('UPDATE users SET gemini_keys = ? WHERE id = ?');
        $stmt->execute([$json, $userId]);
    }

    respond([
        'ok' => true,
        'keys' => $cleanKeys,
        'count' => count($cleanKeys),
    ]);
}

if ($method === 'DELETE') {
    $stmt = $pdo->prepare('UPDATE users SET gemini_keys = NULL WHERE id = ?');
    $stmt->execute([$userId]);

    respond([
        'ok' => true,
        'keys' => [],
        'count' => 0,
    ]);
}

respond(['error' => 'Method not allowed.'], 405);
