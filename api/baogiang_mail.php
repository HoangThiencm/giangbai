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

function baogiang_send_gmail(string $recipient, string $subject, string $body, string $html = ''): void
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
        $headers = "From: <$from>\r\nTo: <$recipient>\r\nSubject: $encodedSubject\r\nMIME-Version: 1.0";
        $encodedBody = rtrim(chunk_split(base64_encode($body), 76, "\r\n"));
        if ($html !== '') {
            $boundary = '=_BaoGiang_' . bin2hex(random_bytes(12));
            $encodedHtml = rtrim(chunk_split(base64_encode($html), 76, "\r\n"));
            $message = $headers . "\r\nContent-Type: multipart/alternative; boundary=\"$boundary\"\r\n\r\n"
                . "--$boundary\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n$encodedBody\r\n"
                . "--$boundary\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n$encodedHtml\r\n"
                . "--$boundary--";
        } else {
            $message = $headers . "\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . $encodedBody;
        }
        baogiang_smtp_expect($socket, $message . "\r\n.", [250]);
        baogiang_smtp_expect($socket, 'QUIT', [221]);
    } finally {
        fclose($socket);
    }
}

if (empty($_SESSION['user_id'])) {
    respond(['ok' => false, 'error' => 'Hãy đăng nhập trước khi gửi lịch báo giảng.'], 401);
}

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'GET') {
    $selfOnly = !defined('BAOGIANG_GMAIL_TO_SELF_ONLY') || BAOGIANG_GMAIL_TO_SELF_ONLY === true;
    respond([
        'ok' => true,
        'configured' => baogiang_mail_configured(),
        'from' => defined('BAOGIANG_GMAIL_FROM') ? (string) BAOGIANG_GMAIL_FROM : '',
        'self_only' => $selfOnly,
        'delivery_mode' => $selfOnly ? 'self' : 'direct',
        'direct_delivery' => !$selfOnly,
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
$html = trim((string) ($payload['html'] ?? ''));
$deliveries = [];

if (is_array($payload['deliveries'] ?? null)) {
    foreach ($payload['deliveries'] as $item) {
        if (!is_array($item)) continue;
        $deliveries[] = [
            'to' => trim((string) ($item['to'] ?? '')),
            'subject' => trim((string) ($item['subject'] ?? $subject)),
            'body' => trim((string) ($item['body'] ?? $body)),
            'html' => trim((string) ($item['html'] ?? $html)),
        ];
    }
} else {
    $recipients = is_array($payload['recipients'] ?? null) ? $payload['recipients'] : [$payload['recipient'] ?? BAOGIANG_GMAIL_FROM];
    foreach ($recipients as $recipient) {
        $deliveries[] = ['to' => trim((string) $recipient), 'subject' => $subject, 'body' => $body, 'html' => $html];
    }
}

$selfOnly = !defined('BAOGIANG_GMAIL_TO_SELF_ONLY') || BAOGIANG_GMAIL_TO_SELF_ONLY === true;
$deliveries = array_slice($deliveries, 0, 50);
$sentCount = 0;
$errors = [];
foreach ($deliveries as $delivery) {
    if (!filter_var($delivery['to'], FILTER_VALIDATE_EMAIL)) {
        $errors[] = 'Địa chỉ email không hợp lệ: ' . ($delivery['to'] ?: '(trống)');
        continue;
    }
    $to = $selfOnly ? (string) BAOGIANG_GMAIL_FROM : $delivery['to'];
    if ($delivery['subject'] === '' || $delivery['body'] === '') {
        $errors[] = 'Nội dung email chưa đầy đủ cho ' . $to;
        continue;
    }
    if (mb_strlen($delivery['subject']) > 200 || mb_strlen($delivery['body']) > 30000 || mb_strlen($delivery['html']) > 200000) {
        $errors[] = 'Nội dung email quá dài cho ' . $to;
        continue;
    }
    try {
        baogiang_send_gmail($to, $delivery['subject'], $delivery['body'], $delivery['html']);
        $sentCount++;
        if ($sentCount < count($deliveries)) usleep(150000);
    } catch (Throwable $e) {
        $errors[] = $to . ': ' . $e->getMessage();
    }
}
if (!$sentCount) respond(['ok' => false, 'error' => $errors[0] ?? 'Không có email hợp lệ để gửi.'], 422);
$message = $selfOnly
    ? "Đã gửi $sentCount email về email cá nhân vì chế độ chỉ gửi cho chính mình đang bật. Để gửi trực tiếp cho giáo viên, đặt BAOGIANG_GMAIL_TO_SELF_ONLY thành false trong api/config.php."
    : "Đã gửi email thành công cho $sentCount giáo viên.";
respond(['ok' => true, 'sent_count' => $sentCount, 'message' => $message, 'errors' => $errors, 'delivery_mode' => $selfOnly ? 'self' : 'direct', 'direct_delivery' => !$selfOnly]);
