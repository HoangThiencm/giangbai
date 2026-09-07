<?php
// Gửi lịch báo giảng cá nhân. Thông tin Gmail chỉ nằm trong api/config.php trên hosting.
require_once __DIR__ . '/helpers.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

function baogiang_mail_configured(): bool
{
    return defined('BAOGIANG_GMAIL_FROM')
        && filter_var((string) BAOGIANG_GMAIL_FROM, FILTER_VALIDATE_EMAIL)
        && defined('BAOGIANG_GMAIL_APP_PASSWORD')
        && strlen(preg_replace('/\s+/', '', (string) BAOGIANG_GMAIL_APP_PASSWORD)) >= 16;
}

function baogiang_smtp_read($socket): string
{
    $response = '';
    while (($line = fgets($socket, 1024)) !== false) {
        $response .= $line;
        if (preg_match('/^\d{3}\s/', $line)) break;
    }
    return $response;
}

function baogiang_smtp_expect($socket, string $command, array $codes): void
{
    if ($command !== '') fwrite($socket, $command . "\r\n");
    $response = baogiang_smtp_read($socket);
    $code = (int) substr($response, 0, 3);
    if (!in_array($code, $codes, true)) {
        throw new RuntimeException('Gmail SMTP từ chối yêu cầu: ' . trim($response));
    }
}

function baogiang_send_gmail(string $recipient, string $subject, string $body): void
{
    $from = trim((string) BAOGIANG_GMAIL_FROM);
    $appPassword = preg_replace('/\s+/', '', (string) BAOGIANG_GMAIL_APP_PASSWORD);
    $socket = @stream_socket_client('ssl://smtp.gmail.com:465', $errno, $errstr, 15, STREAM_CLIENT_CONNECT);
    if (!$socket) throw new RuntimeException("Không kết nối được Gmail SMTP: $errstr ($errno)");
    stream_set_timeout($socket, 30);
    try {
        baogiang_smtp_expect($socket, '', [220]);
        baogiang_smtp_expect($socket, 'EHLO giangbai.local', [250]);
        baogiang_smtp_expect($socket, 'AUTH LOGIN', [334]);
        baogiang_smtp_expect($socket, base64_encode($from), [334]);
        baogiang_smtp_expect($socket, base64_encode($appPassword), [235]);
        baogiang_smtp_expect($socket, 'MAIL FROM:<' . $from . '>', [250]);
        baogiang_smtp_expect($socket, 'RCPT TO:<' . $recipient . '>', [250, 251]);
        baogiang_smtp_expect($socket, 'DATA', [354]);
        $encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
        $headers = "From: <$from>\r\nTo: <$recipient>\r\nSubject: $encodedSubject\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64";
        $encodedBody = rtrim(chunk_split(base64_encode($body), 76, "\r\n"));
        baogiang_smtp_expect($socket, $headers . "\r\n\r\n" . $encodedBody . "\r\n.", [250]);
        baogiang_smtp_expect($socket, 'QUIT', [221]);
    } finally {
        fclose($socket);
    }
}

if (empty($_SESSION['user_id'])) {
    respond(['ok' => false, 'error' => 'Hãy đăng nhập trước khi gửi lịch báo giảng.'], 401);
}

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'GET') {
    respond([
        'ok' => true,
        'configured' => baogiang_mail_configured(),
        'from' => defined('BAOGIANG_GMAIL_FROM') ? (string) BAOGIANG_GMAIL_FROM : '',
        'self_only' => !defined('BAOGIANG_GMAIL_TO_SELF_ONLY') || BAOGIANG_GMAIL_TO_SELF_ONLY === true,
    ]);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(['ok' => false, 'error' => 'Method not allowed.'], 405);
}
if (!baogiang_mail_configured()) {
    respond(['ok' => false, 'error' => 'Chưa cấu hình Gmail App Password trong api/config.php trên hosting.'], 422);
}

$payload = json_body();
$subject = trim((string) ($payload['subject'] ?? ''));
$body = trim((string) ($payload['body'] ?? ''));
if ($subject === '' || $body === '') {
    respond(['ok' => false, 'error' => 'Nội dung email chưa đầy đủ.'], 422);
}
if (mb_strlen($subject) > 200 || mb_strlen($body) > 30000) {
    respond(['ok' => false, 'error' => 'Nội dung email quá dài.'], 422);
}

try {
    // Chế độ cá nhân: luôn gửi lại chính Gmail đã cấu hình, không nhận người nhận từ trình duyệt.
    baogiang_send_gmail((string) BAOGIANG_GMAIL_FROM, $subject, $body);
    respond(['ok' => true, 'message' => 'Đã gửi lịch báo giảng tới email cá nhân.']);
} catch (Throwable $e) {
    respond(['ok' => false, 'error' => $e->getMessage()], 502);
}
