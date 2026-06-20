<?php
require_once __DIR__ . '/helpers.php';

$appTimezone = defined('APP_TIMEZONE') ? (string)APP_TIMEZONE : 'Asia/Ho_Chi_Minh';
try {
    date_default_timezone_set($appTimezone);
    $pdo->exec("SET time_zone = '+07:00'");
} catch (Throwable $e) {
    // Keep PHP timezone when MySQL session offset is restricted.
}

set_exception_handler(function (Throwable $e) {
    $payload = ['error' => 'Có lỗi khi xử lý link rút gọn.'];
    if (defined('APP_DEBUG') && APP_DEBUG) {
        $payload['detail'] = $e->getMessage();
    }
    respond($payload, 500);
});

function short_link_schema(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS short_links (
        id INT AUTO_INCREMENT PRIMARY KEY,
        code VARCHAR(12) NOT NULL,
        target_url TEXT NOT NULL,
        title VARCHAR(200) DEFAULT NULL,
        note TEXT DEFAULT NULL,
        owner_id INT NOT NULL,
        click_count INT NOT NULL DEFAULT 0,
        max_clicks INT DEFAULT NULL,
        expires_at DATETIME DEFAULT NULL,
        is_active TINYINT(1) NOT NULL DEFAULT 1,
        last_clicked_at DATETIME DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_short_link_code (code),
        INDEX idx_short_links_owner (owner_id),
        INDEX idx_short_links_active (is_active),
        INDEX idx_short_links_expires (expires_at),
        CONSTRAINT fk_short_link_owner FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    $pdo->exec("CREATE TABLE IF NOT EXISTS short_link_clicks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        link_id INT NOT NULL,
        clicked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        ip_hash VARCHAR(64) DEFAULT NULL,
        user_agent VARCHAR(255) DEFAULT NULL,
        referer VARCHAR(255) DEFAULT NULL,
        INDEX idx_short_link_clicks_link (link_id),
        INDEX idx_short_link_clicks_time (clicked_at),
        CONSTRAINT fk_short_link_click_link FOREIGN KEY (link_id) REFERENCES short_links(id) ON DELETE CASCADE
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}

function short_link_alphabet_code(int $length = 8): string
{
    $alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    $value = '';
    for ($i = 0; $i < $length; $i++) {
        $value .= $alphabet[random_int(0, strlen($alphabet) - 1)];
    }
    return $value;
}

function short_link_unique_code(PDO $pdo, ?string $preferred = null): string
{
    $preferred = strtoupper(trim((string)$preferred));
    if ($preferred !== '') {
        if (!preg_match('/^[A-Z0-9]{4,12}$/', $preferred)) {
            respond(['error' => 'Mã tùy chọn chỉ gồm 4–12 ký tự A–Z hoặc 2–9.'], 422);
        }
        $stmt = $pdo->prepare('SELECT id FROM short_links WHERE code = ? LIMIT 1');
        $stmt->execute([$preferred]);
        if ($stmt->fetch()) {
            respond(['error' => 'Mã rút gọn đã được dùng, hãy chọn mã khác.'], 409);
        }
        return $preferred;
    }

    do {
        $code = short_link_alphabet_code(8);
        $stmt = $pdo->prepare('SELECT id FROM short_links WHERE code = ? LIMIT 1');
        $stmt->execute([$code]);
    } while ($stmt->fetch());

    return $code;
}

function short_link_normalize_url(string $url): string
{
    $url = trim($url);
    if ($url === '') {
        respond(['error' => 'Vui lòng nhập đường dẫn đích.'], 422);
    }
    if (!preg_match('#^https?://#i', $url)) {
        $url = 'https://' . $url;
    }
    if (!filter_var($url, FILTER_VALIDATE_URL)) {
        respond(['error' => 'Đường dẫn đích không hợp lệ.'], 422);
    }
    $parts = parse_url($url);
    $scheme = strtolower((string)($parts['scheme'] ?? ''));
    if (!in_array($scheme, ['http', 'https'], true)) {
        respond(['error' => 'Chỉ hỗ trợ link http hoặc https.'], 422);
    }
    return $url;
}

function short_link_datetime($value): ?string
{
    $value = trim((string)$value);
    if ($value === '') {
        return null;
    }
    $timestamp = strtotime($value);
    return $timestamp === false ? null : date('Y-m-d H:i:s', $timestamp);
}

function short_link_public_base(): string
{
    $scheme = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
    $host = $_SERVER['HTTP_HOST'] ?? 'localhost';
    $scriptDir = str_replace('\\', '/', dirname($_SERVER['SCRIPT_NAME'] ?? '/api'));
    $root = preg_replace('#/api$#', '', rtrim($scriptDir, '/'));
    if ($root === '') {
        $root = '';
    }
    return $scheme . '://' . $host . $root;
}

function short_link_public_url(string $code): string
{
    return short_link_public_base() . '/s/' . rawurlencode($code);
}

function short_link_current_user(PDO $pdo): ?array
{
    if (empty($_SESSION['user_id'])) {
        return null;
    }
    $stmt = $pdo->prepare('SELECT * FROM users WHERE id = ? AND is_active = 1 LIMIT 1');
    $stmt->execute([(int)$_SESSION['user_id']]);
    return $stmt->fetch() ?: null;
}

function short_link_require_teacher(PDO $pdo): array
{
    $user = short_link_current_user($pdo);
    if (!$user || ($user['role'] ?? '') !== 'teacher') {
        respond(['error' => 'Cần đăng nhập bằng tài khoản giáo viên.'], 401);
    }
    return $user;
}

function short_link_row_status(array $row): array
{
    $now = time();
    $expired = false;
    $maxed = false;
    if (!empty($row['expires_at'])) {
        $expired = strtotime((string)$row['expires_at']) < $now;
    }
    if (!empty($row['max_clicks'])) {
        $maxed = (int)$row['click_count'] >= (int)$row['max_clicks'];
    }
    $inactive = !(bool)($row['is_active'] ?? 1);
    $usable = !$inactive && !$expired && !$maxed;

    $status = 'active';
    $statusLabel = 'Đang hoạt động';
    if ($inactive) {
        $status = 'inactive';
        $statusLabel = 'Đã tắt';
    } elseif ($expired) {
        $status = 'expired';
        $statusLabel = 'Đã hết hạn';
    } elseif ($maxed) {
        $status = 'maxed';
        $statusLabel = 'Đủ lượt click';
    }

    return compact('status', 'statusLabel', 'usable', 'expired', 'maxed', 'inactive');
}

function short_link_public_item(array $row): array
{
    $meta = short_link_row_status($row);
    return [
        'id' => (int)$row['id'],
        'code' => $row['code'],
        'short_url' => short_link_public_url($row['code']),
        'target_url' => $row['target_url'],
        'title' => $row['title'],
        'note' => $row['note'],
        'click_count' => (int)$row['click_count'],
        'max_clicks' => $row['max_clicks'] !== null ? (int)$row['max_clicks'] : null,
        'expires_at' => $row['expires_at'],
        'is_active' => (bool)$row['is_active'],
        'last_clicked_at' => $row['last_clicked_at'],
        'created_at' => $row['created_at'],
        'updated_at' => $row['updated_at'],
        'status' => $meta['status'],
        'status_label' => $meta['statusLabel'],
        'usable' => $meta['usable'],
    ];
}

function short_link_owned_row(PDO $pdo, int $id, int $ownerId): array
{
    $stmt = $pdo->prepare('SELECT * FROM short_links WHERE id = ? AND owner_id = ? LIMIT 1');
    $stmt->execute([$id, $ownerId]);
    $row = $stmt->fetch();
    if (!$row) {
        respond(['error' => 'Không tìm thấy link hoặc bạn không có quyền.'], 404);
    }
    return $row;
}

short_link_schema($pdo);

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$action = $_GET['action'] ?? ($_POST['action'] ?? '');
if ($method === 'POST' && $action === '') {
    $body = json_body();
    $action = (string)($body['action'] ?? '');
}

if ($method === 'GET' && $action === 'list') {
    $teacher = short_link_require_teacher($pdo);
    $stmt = $pdo->prepare('SELECT * FROM short_links WHERE owner_id = ? ORDER BY created_at DESC, id DESC');
    $stmt->execute([(int)$teacher['id']]);
    $rows = $stmt->fetchAll();
    $items = array_map('short_link_public_item', $rows);
    $totalClicks = array_sum(array_map(static fn($item) => (int)$item['click_count'], $items));
    respond([
        'ok' => true,
        'items' => $items,
        'stats' => [
            'total_links' => count($items),
            'active_links' => count(array_filter($items, static fn($item) => $item['usable'])),
            'total_clicks' => $totalClicks,
        ],
    ]);
}

if ($method === 'GET' && $action === 'stats') {
    $teacher = short_link_require_teacher($pdo);
    $id = (int)($_GET['id'] ?? 0);
    if ($id <= 0) {
        respond(['error' => 'Thiếu id link.'], 422);
    }
    short_link_owned_row($pdo, $id, (int)$teacher['id']);
    $stmt = $pdo->prepare('SELECT clicked_at, ip_hash, user_agent, referer FROM short_link_clicks WHERE link_id = ? ORDER BY clicked_at DESC, id DESC LIMIT 100');
    $stmt->execute([$id]);
    respond(['ok' => true, 'clicks' => $stmt->fetchAll()]);
}

if ($method === 'POST' && $action === 'create') {
    $teacher = short_link_require_teacher($pdo);
    $body = json_body();
    $targetUrl = short_link_normalize_url((string)($body['target_url'] ?? ''));
    $title = trim((string)($body['title'] ?? ''));
    $note = trim((string)($body['note'] ?? ''));
    $customCode = (string)($body['custom_code'] ?? '');
    $maxClicks = $body['max_clicks'] ?? null;
    $maxClicks = ($maxClicks === '' || $maxClicks === null) ? null : max(1, (int)$maxClicks);
    $expiresAt = short_link_datetime($body['expires_at'] ?? null);
    $code = short_link_unique_code($pdo, $customCode !== '' ? $customCode : null);

    $stmt = $pdo->prepare('INSERT INTO short_links (code, target_url, title, note, owner_id, max_clicks, expires_at) VALUES (?, ?, ?, ?, ?, ?, ?)');
    $stmt->execute([
        $code,
        $targetUrl,
        $title !== '' ? mb_substr($title, 0, 200) : null,
        $note !== '' ? $note : null,
        (int)$teacher['id'],
        $maxClicks,
        $expiresAt,
    ]);

    $id = (int)$pdo->lastInsertId();
    $stmt = $pdo->prepare('SELECT * FROM short_links WHERE id = ? LIMIT 1');
    $stmt->execute([$id]);
    $row = $stmt->fetch();
    respond(['ok' => true, 'item' => short_link_public_item($row)], 201);
}

if ($method === 'POST' && $action === 'update') {
    $teacher = short_link_require_teacher($pdo);
    $body = json_body();
    $id = (int)($body['id'] ?? 0);
    if ($id <= 0) {
        respond(['error' => 'Thiếu id link.'], 422);
    }
    $row = short_link_owned_row($pdo, $id, (int)$teacher['id']);

    $targetUrl = array_key_exists('target_url', $body)
        ? short_link_normalize_url((string)$body['target_url'])
        : $row['target_url'];
    $title = array_key_exists('title', $body) ? trim((string)$body['title']) : (string)($row['title'] ?? '');
    $note = array_key_exists('note', $body) ? trim((string)$body['note']) : (string)($row['note'] ?? '');
    $maxClicks = array_key_exists('max_clicks', $body)
        ? (($body['max_clicks'] === '' || $body['max_clicks'] === null) ? null : max(1, (int)$body['max_clicks']))
        : ($row['max_clicks'] !== null ? (int)$row['max_clicks'] : null);
    $expiresAt = array_key_exists('expires_at', $body)
        ? short_link_datetime($body['expires_at'])
        : $row['expires_at'];
    $isActive = array_key_exists('is_active', $body) ? ((bool)$body['is_active'] ? 1 : 0) : (int)$row['is_active'];

    $stmt = $pdo->prepare('UPDATE short_links SET target_url = ?, title = ?, note = ?, max_clicks = ?, expires_at = ?, is_active = ? WHERE id = ? AND owner_id = ?');
    $stmt->execute([
        $targetUrl,
        $title !== '' ? mb_substr($title, 0, 200) : null,
        $note !== '' ? $note : null,
        $maxClicks,
        $expiresAt,
        $isActive,
        $id,
        (int)$teacher['id'],
    ]);

    $stmt = $pdo->prepare('SELECT * FROM short_links WHERE id = ? LIMIT 1');
    $stmt->execute([$id]);
    respond(['ok' => true, 'item' => short_link_public_item($stmt->fetch())]);
}

if ($method === 'POST' && $action === 'delete') {
    $teacher = short_link_require_teacher($pdo);
    $body = json_body();
    $id = (int)($body['id'] ?? 0);
    if ($id <= 0) {
        respond(['error' => 'Thiếu id link.'], 422);
    }
    short_link_owned_row($pdo, $id, (int)$teacher['id']);
    $stmt = $pdo->prepare('DELETE FROM short_links WHERE id = ? AND owner_id = ?');
    $stmt->execute([$id, (int)$teacher['id']]);
    respond(['ok' => true]);
}

respond(['error' => 'Action không hợp lệ.'], 400);