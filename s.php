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
        escape_inapp TINYINT(1) NOT NULL DEFAULT 1,
        last_clicked_at DATETIME DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_short_link_code (code),
        INDEX idx_short_links_owner (owner_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    $column = $pdo->query("SHOW COLUMNS FROM short_links LIKE 'escape_inapp'")->fetch();
    if (!$column) {
        $pdo->exec('ALTER TABLE short_links ADD COLUMN escape_inapp TINYINT(1) NOT NULL DEFAULT 1 AFTER is_active');
    }

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

function short_redirect_escape(string $value): string
{
    return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function short_redirect_android_intent(string $targetUrl, ?string $package = 'com.android.chrome'): string
{
    $parts = parse_url($targetUrl);
    $scheme = strtolower((string)($parts['scheme'] ?? 'https'));
    $authority = (string)($parts['host'] ?? '');
    if (!empty($parts['port'])) {
        $authority .= ':' . (int)$parts['port'];
    }
    $path = (string)($parts['path'] ?? '/');
    $query = isset($parts['query']) ? '?' . $parts['query'] : '';
    $fallback = ';S.browser_fallback_url=' . rawurlencode($targetUrl);
    $packagePart = $package ? ';package=' . $package : '';
    return 'intent://' . $authority . $path . $query . '#Intent;scheme=' . $scheme . $packagePart . $fallback . ';end';
}

function short_redirect_bridge(string $targetUrl, bool $isAndroid): void
{
    $safeTarget = short_redirect_escape($targetUrl);
    $chromeUrl = preg_replace('#^https:#i', 'googlechromes:', $targetUrl);
    $chromeUrl = preg_replace('#^http:#i', 'googlechrome:', (string)$chromeUrl);
    $safeChromeUrl = short_redirect_escape((string)$chromeUrl);

    header('Content-Type: text/html; charset=utf-8');
    header('Cache-Control: no-store, no-cache, must-revalidate');
    header('Pragma: no-cache');

    if ($isAndroid) {
        $chromeIntent = short_redirect_escape(short_redirect_android_intent($targetUrl));
        $genericIntent = short_redirect_escape(short_redirect_android_intent($targetUrl, null));
        echo '<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            . '<title>Đang mở trình duyệt…</title><style>body{font-family:system-ui,sans-serif;background:#f8fafc;color:#0f172a;display:grid;place-items:center;min-height:100vh;margin:0;padding:24px}.box{max-width:420px;background:#fff;border:1px solid #e2e8f0;border-radius:20px;padding:28px;text-align:center;box-shadow:0 18px 40px rgba(15,23,42,.08)}a{color:#4f46e5;font-weight:700}</style></head><body><div class="box"><h1>Đang mở bằng trình duyệt…</h1><p>Nếu Chrome chưa mở, hãy chạm <a id="open" href="' . $chromeIntent . '">vào đây</a>.</p><p><a href="' . $safeTarget . '">Tiếp tục trong ứng dụng</a></p></div><script>const chromeIntent=' . json_encode(htmlspecialchars_decode($chromeIntent, ENT_QUOTES)) . ';const genericIntent=' . json_encode(htmlspecialchars_decode($genericIntent, ENT_QUOTES)) . ';location.href=chromeIntent;setTimeout(()=>{location.href=genericIntent},1200);</script></body></html>';
        exit;
    }

    echo '<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        . '<title>Mở bằng trình duyệt</title><style>body{font-family:system-ui,-apple-system,sans-serif;background:linear-gradient(160deg,#eef2ff,#f8fafc);color:#172554;min-height:100vh;margin:0;padding:24px;box-sizing:border-box}.box{max-width:460px;margin:7vh auto;background:#fff;border-radius:24px;padding:28px;box-shadow:0 20px 55px rgba(30,41,59,.16);position:relative}.arrow{position:fixed;right:24px;top:10px;color:#4f46e5;font-size:42px;animation:bounce 1s infinite;transform:rotate(-35deg)}.step{display:flex;gap:12px;align-items:flex-start;margin:18px 0}.num{background:#4f46e5;color:#fff;border-radius:50%;width:28px;height:28px;display:grid;place-items:center;font-weight:800;flex:none}button,a.btn{display:block;width:100%;box-sizing:border-box;border:0;border-radius:12px;padding:13px 16px;margin-top:10px;text-align:center;font:700 15px system-ui;text-decoration:none;cursor:pointer}.copy{background:#4f46e5;color:#fff}.chrome{background:#eef2ff;color:#3730a3}.continue{color:#64748b;font-size:14px;text-align:center;margin-top:18px}@keyframes bounce{50%{transform:rotate(-35deg) translateY(-8px)}}</style></head><body><div class="arrow">↗</div><main class="box"><h1>Mở link bằng trình duyệt</h1><p>Zalo có thể chặn Google, Gemini hoặc một số tính năng của trang này.</p><div class="step"><span class="num">1</span><span>Chạm dấu <strong>…</strong> ở góc trên bên phải.</span></div><div class="step"><span class="num">2</span><span>Chọn <strong>Mở bằng trình duyệt</strong> (Safari hoặc Chrome).</span></div><button class="copy" id="copy">Sao chép liên kết</button><a class="btn chrome" href="' . $safeChromeUrl . '">Thử mở bằng Google Chrome</a><a class="continue" href="' . $safeTarget . '">Vẫn tiếp tục trên Zalo</a></main><script>document.getElementById("copy").addEventListener("click",async()=>{try{await navigator.clipboard.writeText(' . json_encode($targetUrl) . ');document.getElementById("copy").textContent="Đã sao chép liên kết"}catch(e){prompt("Sao chép liên kết này:",' . json_encode($targetUrl) . ')}})</script></body></html>';
    exit;
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

$isZalo = (bool)preg_match('/(Zalo|ZaloTheme)/i', $ua);
$isInApp = (bool)preg_match('/(Zalo|FB_IAB|FBAN|FBAV|Instagram|MicroMessenger|Line|Snapchat|Bytedance|TikTok)/i', $ua);
$isAndroid = (bool)preg_match('/Android/i', $ua);
$isIOS = (bool)preg_match('/(iPhone|iPad|iPod)/i', $ua);
$escapeInApp = (bool)($row['escape_inapp'] ?? 1);

if ($isInApp && $escapeInApp) {
    short_redirect_bridge($targetUrl, $isAndroid && !$isIOS);
}

header('Cache-Control: no-store, no-cache, must-revalidate');
header('Pragma: no-cache');
header('Location: ' . $targetUrl, true, 302);
exit;
