<?php
/**
 * Bản quyền App Desktop Trợ lý sư phạm.
 * verify: máy giáo viên gửi Email + Mã máy.
 * list, approve, revoke, delete: trang admin, cần Admin Key.
 */
header('Content-Type: application/json; charset=utf-8');

function license_respond(array $payload, int $status = 200): void
{
    http_response_code($status);
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

function license_body(): array
{
    $raw = file_get_contents('php://input');
    if (!$raw) {
        return [];
    }
    $data = json_decode($raw, true);
    return is_array($data) ? $data : [];
}

function license_admin_key(): string
{
    $env = getenv('TLHT_ADMIN_KEY');
    if (is_string($env) && $env !== '') {
        return $env;
    }
    $config = __DIR__ . '/config.php';
    if (is_file($config)) {
        require_once $config;
    }
    return defined('ADMIN_KEY') ? (string) ADMIN_KEY : '';
}

function license_require_admin(): void
{
    $expected = license_admin_key();
    $given = $_SERVER['HTTP_X_ADMIN_KEY'] ?? ($_GET['admin_key'] ?? '');
    if ($expected === '' || !is_string($given) || !hash_equals($expected, $given)) {
        license_respond(['ok' => false, 'error' => 'Sai Admin Key hoặc không có quyền quản trị.'], 401);
    }
}

function license_store_path(): string
{
    $override = getenv('TLHT_LICENSE_STORE');
    if (is_string($override) && $override !== '') {
        return $override;
    }
    return __DIR__ . '/storage/licenses.json';
}

function license_empty(): array
{
    return ['licenses' => []];
}

function license_normalize_email(string $email): string
{
    return strtolower(trim($email));
}

function license_normalize_device(string $device): string
{
    return strtoupper(trim($device));
}

function license_valid_email(string $email): bool
{
    return (bool) preg_match('/^[^@\s]+@[^@\s]+\.[^@\s]+$/', $email);
}

function license_valid_device(string $device): bool
{
    return (bool) preg_match('/^TLHT-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/', $device);
}

function license_with_store(callable $change): void
{
    $path = license_store_path();
    $dir = dirname($path);
    if (!is_dir($dir) && !mkdir($dir, 0775, true) && !is_dir($dir)) {
        license_respond(['ok' => false, 'error' => 'Không tạo được thư mục lưu bản quyền.'], 500);
    }
    $handle = fopen($path, 'c+');
    if ($handle === false) {
        license_respond(['ok' => false, 'error' => 'Không mở được kho bản quyền.'], 500);
    }
    if (!flock($handle, LOCK_EX)) {
        fclose($handle);
        license_respond(['ok' => false, 'error' => 'Không khóa được kho bản quyền.'], 500);
    }
    $raw = stream_get_contents($handle);
    $data = json_decode($raw ?: '', true);
    if (!is_array($data) || !isset($data['licenses']) || !is_array($data['licenses'])) {
        $data = license_empty();
    }
    $write = false;
    $result = $change($data, $write);
    if ($write) {
        rewind($handle);
        ftruncate($handle, 0);
        fwrite($handle, json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
        fflush($handle);
    }
    flock($handle, LOCK_UN);
    fclose($handle);
    license_respond($result['payload'], $result['status'] ?? 200);
}

function license_find_index(array $rows, string $email, string $device): int
{
    foreach ($rows as $index => $row) {
        if (!is_array($row)) {
            continue;
        }
        $rowEmail = license_normalize_email((string) ($row['email'] ?? ''));
        $rowDevice = license_normalize_device((string) ($row['device_id'] ?? ''));
        if ($rowEmail === $email && $rowDevice === $device) {
            return (int) $index;
        }
    }
    return -1;
}

$body = license_body();
$action = strtolower(trim((string) ($body['action'] ?? ($_GET['action'] ?? 'verify'))));
$email = license_normalize_email((string) ($body['email'] ?? ($_GET['email'] ?? '')));
$device = license_normalize_device((string) ($body['device_id'] ?? ($_GET['device_id'] ?? '')));

if ($action !== 'verify') {
    license_require_admin();
}

if (in_array($action, ['verify', 'approve', 'revoke', 'delete'], true)) {
    if (!license_valid_email($email) || !license_valid_device($device)) {
        license_respond(['ok' => false, 'error' => 'Thiếu Email hoặc Mã máy hợp lệ.'], 422);
    }
}

license_with_store(function (array &$data, bool &$write) use ($action, $email, $device): array {
    $rows = $data['licenses'];
    $now = gmdate('c');

    if ($action === 'list') {
        $query = strtolower(trim((string) ($_GET['q'] ?? '')));
        $items = [];
        foreach ($rows as $row) {
            if (!is_array($row)) {
                continue;
            }
            $blob = strtolower(($row['email'] ?? '') . ' ' . ($row['device_id'] ?? '') . ' ' . ($row['status'] ?? ''));
            if ($query !== '' && strpos($blob, $query) === false) {
                continue;
            }
            $items[] = $row;
        }
        return ['payload' => ['ok' => true, 'licenses' => $items]];
    }

    $index = license_find_index($rows, $email, $device);

    if ($action === 'verify') {
        if ($index < 0) {
            $rows[] = [
                'email' => $email,
                'device_id' => $device,
                'status' => 'pending',
                'updated_at' => $now,
            ];
            $data['licenses'] = $rows;
            $write = true;
            return ['payload' => [
                'ok' => false,
                'status' => 'pending',
                'email' => $email,
                'device_id' => $device,
                'message' => 'Đã ghi nhận máy trên hoangthiencm.id.vn. Chờ Thầy Thiên duyệt.',
            ]];
        }
        $status = strtolower((string) ($rows[$index]['status'] ?? 'pending'));
        if ($status === 'active') {
            return ['payload' => [
                'ok' => true,
                'status' => 'active',
                'email' => $email,
                'device_id' => $device,
                'message' => 'Máy đã được duyệt trên hoangthiencm.id.vn.',
            ]];
        }
        $message = $status === 'revoked'
            ? 'Máy này đã bị khóa trên hoangthiencm.id.vn.'
            : 'Máy đang chờ Thầy Thiên duyệt trên hoangthiencm.id.vn.';
        return ['payload' => [
            'ok' => false,
            'status' => $status,
            'email' => $email,
            'device_id' => $device,
            'message' => $message,
        ]];
    }

    if ($action === 'approve') {
        $record = [
            'email' => $email,
            'device_id' => $device,
            'status' => 'active',
            'updated_at' => $now,
        ];
        if ($index < 0) {
            $rows[] = $record;
        } else {
            $rows[$index] = $record;
        }
        $data['licenses'] = $rows;
        $write = true;
        return ['payload' => ['ok' => true, 'license' => $record]];
    }

    if ($action === 'revoke') {
        if ($index < 0) {
            return ['payload' => ['ok' => false, 'error' => 'Không thấy máy cần khóa.'], 'status' => 404];
        }
        $rows[$index]['status'] = 'revoked';
        $rows[$index]['updated_at'] = $now;
        $data['licenses'] = $rows;
        $write = true;
        return ['payload' => ['ok' => true, 'license' => $rows[$index]]];
    }

    if ($action === 'delete') {
        if ($index < 0) {
            return ['payload' => ['ok' => false, 'error' => 'Không thấy máy cần xóa.'], 'status' => 404];
        }
        array_splice($rows, $index, 1);
        $data['licenses'] = array_values($rows);
        $write = true;
        return ['payload' => ['ok' => true]];
    }

    return ['payload' => ['ok' => false, 'error' => 'Hành động không hỗ trợ.'], 'status' => 400];
});
