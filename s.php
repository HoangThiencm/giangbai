<?php
require_once __DIR__ . '/api/db.php';

try {
    date_default_timezone_set(defined('APP_TIMEZONE') ? (string)APP_TIMEZONE : 'Asia/Ho_Chi_Minh');
} catch (Throwable $e) {
    // Ignore invalid timezone on restricted hosts.
}

function short_redirect_fail(int $status, string $message): void
{
    http_response_code($status);
    header('Content-Type: text/html; charset=utf-8');
    echo '<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        . '<title>Link không khả dụng</title>'
        . '<style>body{font-family:system-ui,sans-serif;background:#f8fafc;color:#0f172a;display:grid;place-items:center;min-height:100vh;margin:0;padding:24px}'
        . '.box{max-width:420px;background:#fff;border:1px solid #e2e8f0;border-radius:20px;padding:28px;box-shadow:0 18px 40px rgba(15,23,42,.08);text-align:center}'
        . 'h1{font-size:1.2rem;margin:0 0 8px}p{margin:0;color:#64748b;line-height:1.6}</style></head><body>'
        . '<div class="box"><h1>Link không khả dụng</h1><p>' . htmlspecialchars($message, ENT_QUOTES, 'UTF-8') . '</p></div></body></html>';
    exit;
}

function short_redirect_schema(PDO $pdo): void
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
        INDEX idx_short_links_owner (owner_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    $pdo->exec("CREATE TABLE IF NOT EXISTS short_link_clicks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        link_id INT NOT NULL,
        clicked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        ip_hash VARCHAR(64) DEFAULT NULL,
        user_agent VARCHAR(255) DEFAULT NULL,
        referer VARCHAR(255) DEFAULT NULL,
        INDEX idx_short_link_clicks_link (link_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}

$code = strtoupper(trim((string)($_GET['c'] ?? '')));
if ($code === '' && !empty($_SERVER['REQUEST_URI']) && preg_match('#/s/([A-Za-z0-9]+)#', (string)$_SERVER['REQUEST_URI'], $matches)) {
    $code = strtoupper($matches[1]);
}

if ($code === '' || !preg_match('/^[A-Z0-9]{4,12}$/', $code)) {
    short_redirect_fail(404, 'Mã link rút gọn không hợp lệ.');
}

short_redirect_schema($pdo);

$stmt = $pdo->prepare('SELECT * FROM short_links WHERE code = ? LIMIT 1');
$stmt->execute([$code]);
$row = $stmt->fetch();

if (!$row) {
    short_redirect_fail(404, 'Không tìm thấy link rút gọn này.');
}

if (!(bool)$row['is_active']) {
    short_redirect_fail(410, 'Link đã bị tắt bởi giáo viên.');
}

if (!empty($row['expires_at']) && strtotime((string)$row['expires_at']) < time()) {
    short_redirect_fail(410, 'Link đã hết hạn sử dụng.');
}

if (!empty($row['max_clicks']) && (int)$row['max_clicks'] > 0 && (int)$row['click_count'] >= (int)$row['max_clicks']) {
    short_redirect_fail(410, 'Link đã đạt giới hạn lượt truy cập.');
}

$targetUrl = trim((string)$row['target_url']);
if ($targetUrl === '' || !preg_match('#^https?://#i', $targetUrl)) {
    short_redirect_fail(500, 'Đường dẫn đích không hợp lệ.');
}

$ip = (string)($_SERVER['REMOTE_ADDR'] ?? '');
$ua = substr((string)($_SERVER['HTTP_USER_AGENT'] ?? ''), 0, 255);
$referer = substr((string)($_SERVER['HTTP_REFERER'] ?? ''), 0, 255);
$ipHash = $ip !== '' ? hash('sha256', $ip) : null;

$pdo->beginTransaction();
try {
    $update = $pdo->prepare('UPDATE short_links SET click_count = click_count + 1, last_clicked_at = NOW() WHERE id = ?');
    $update->execute([(int)$row['id']]);

    $log = $pdo->prepare('INSERT INTO short_link_clicks (link_id, ip_hash, user_agent, referer) VALUES (?, ?, ?, ?)');
    $log->execute([(int)$row['id'], $ipHash, $ua !== '' ? $ua : null, $referer !== '' ? $referer : null]);
    $pdo->commit();
} catch (Throwable $e) {
    if ($pdo->inTransaction()) {
        $pdo->rollBack();
    }
}

header('Cache-Control: no-store, no-cache, must-revalidate');
header('Pragma: no-cache');
header('Location: ' . $targetUrl, true, 302);
exit;