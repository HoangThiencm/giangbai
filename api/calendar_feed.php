<?php
require_once __DIR__ . '/db.php';

function calendar_feed_secret(): string
{
    $material = defined('ADMIN_KEY') ? (string)ADMIN_KEY : 'giangbai-calendar-feed';
    return hash('sha256', 'calendar-feed|' . $material);
}

function calendar_feed_token(int $ownerId, string $teacherId): string
{
    return hash_hmac('sha256', $ownerId . '|' . $teacherId, calendar_feed_secret());
}

function calendar_feed_ics_escape(string $value): string
{
    return str_replace(
        ["\\", "\r\n", "\n", "\r", ',', ';'],
        ["\\\\", '\\n', '\\n', '\\n', '\\,', '\\;'],
        $value
    );
}

function calendar_feed_fold(string $line): string
{
    if (strlen($line) <= 73) {
        return $line;
    }
    $parts = [substr($line, 0, 73)];
    for ($index = 73; $index < strlen($line); $index += 72) {
        $parts[] = ' ' . substr($line, $index, 72);
    }
    return implode("\r\n", $parts);
}

function calendar_feed_period_slot(string $session, int $period): ?array
{
    $morning = [1 => ['07:15', '08:00'], 2 => ['08:05', '08:50'], 3 => ['09:05', '09:50'], 4 => ['09:55', '10:40'], 5 => ['10:45', '11:30']];
    $afternoon = [
        1 => ['13:30', '14:15'], 2 => ['14:20', '15:05'], 3 => ['15:20', '16:05'], 4 => ['16:10', '16:55'], 5 => ['17:00', '17:45'],
        6 => ['13:30', '14:15'], 7 => ['14:20', '15:05'], 8 => ['15:20', '16:05'], 9 => ['16:10', '16:55'], 10 => ['17:00', '17:45'],
    ];
    $table = $session === 'morning' ? $morning : $afternoon;
    return $table[$period] ?? $afternoon[$period] ?? $morning[$period] ?? null;
}

function calendar_feed_cell(mixed $cell): ?array
{
    if (is_string($cell)) {
        $cell = trim($cell);
        if ($cell === '') {
            return null;
        }
        $parts = preg_split('/\s+/', $cell) ?: [];
        $className = count($parts) > 1 ? (string)array_pop($parts) : '';
        return ['subject' => trim(implode(' ', $parts)), 'class_name' => $className];
    }
    if (!is_array($cell)) {
        return null;
    }
    $subject = trim((string)($cell['subject'] ?? ''));
    $className = trim((string)($cell['class_name'] ?? ($cell['className'] ?? '')));
    if ($subject === '' || $className === '') {
        return null;
    }
    return ['subject' => $subject, 'class_name' => $className];
}

function calendar_feed_off(array $exceptions, string $date, array $row): bool
{
    foreach ($exceptions as $ex) {
        if (!is_array($ex) || ($ex['type'] ?? '') !== 'off' || (string)($ex['date'] ?? '') !== $date) {
            continue;
        }
        $scope = (string)($ex['scope'] ?? 'all');
        if ($scope === 'all' || $scope === '') {
            return true;
        }
        if (($scope === 'teacher' || $scope === 'self') && (string)($ex['teacher_id'] ?? '') === (string)$row['teacher_id']) {
            return true;
        }
        if ($scope === 'class' && strcasecmp((string)($ex['target'] ?? ''), (string)$row['class_name']) === 0) {
            return true;
        }
        if ($scope === 'subject' && strcasecmp((string)($ex['target'] ?? ''), (string)$row['subject']) === 0) {
            return true;
        }
    }
    return false;
}

function calendar_feed_rows(array $data, string $teacherId): array
{
    $teachers = is_array($data['teachers'] ?? null) ? $data['teachers'] : [];
    $teacher = null;
    foreach ($teachers as $item) {
        if (is_array($item) && (string)($item['id'] ?? '') === $teacherId) {
            $teacher = $item;
            break;
        }
    }
    if (!$teacher) {
        return ['teacher' => null, 'rows' => []];
    }
    $bao = is_array($data['bao_giang'] ?? null) ? $data['bao_giang'] : [];
    $start = (string)($bao['start_date'] ?? '');
    if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $start)) {
        $start = date('Y-m-d');
    }
    $cursor = DateTimeImmutable::createFromFormat('Y-m-d', $start) ?: new DateTimeImmutable('today');
    $end = $cursor->modify('+280 days');
    $timetable = is_array($teacher['timetable'] ?? null) ? $teacher['timetable'] : [];
    $exceptions = is_array($bao['exceptions'] ?? null) ? $bao['exceptions'] : [];
    $rows = [];
    for ($date = $cursor; $date <= $end; $date = $date->modify('+1 day')) {
        $weekday = (int)$date->format('N');
        if ($weekday === 7) {
            continue;
        }
        $dayKey = (string)($weekday + 1);
        $iso = $date->format('Y-m-d');
        foreach (['morning', 'afternoon'] as $session) {
            $cells = $timetable[$session][$dayKey] ?? [];
            if (!is_array($cells)) {
                continue;
            }
            foreach ($cells as $period => $cell) {
                $parsed = calendar_feed_cell($cell);
                if (!$parsed) {
                    continue;
                }
                $row = [
                    'date' => $iso,
                    'session' => $session,
                    'period' => (string)$period,
                    'subject' => $parsed['subject'],
                    'class_name' => $parsed['class_name'],
                    'teacher_id' => $teacherId,
                ];
                if (!calendar_feed_off($exceptions, $iso, $row)) {
                    $rows[] = $row;
                }
            }
        }
    }
    usort($rows, static function (array $a, array $b): int {
        return [$a['date'], $a['session'] === 'morning' ? 0 : 1, (int)$a['period']]
            <=> [$b['date'], $b['session'] === 'morning' ? 0 : 1, (int)$b['period']];
    });
    return ['teacher' => $teacher, 'rows' => $rows];
}

function calendar_feed_ics(array $teacher, array $rows, bool $allDay): string
{
    $stamp = gmdate('Ymd\THis\Z');
    $events = [];
    $groups = [];
    foreach ($rows as $row) {
        $groups[$row['date'] . '|' . $row['session']][] = $row;
    }
    foreach ($groups as $group) {
        $row = $group[0];
        $last = $group[count($group) - 1];
        $slot = calendar_feed_period_slot((string)$row['session'], (int)$row['period']);
        $endSlot = calendar_feed_period_slot((string)$last['session'], (int)$last['period']) ?? $slot;
        if (!$allDay && !$slot) {
            continue;
        }
        $uid = 'baogiang-' . ($teacher['id'] ?? '') . '-' . $row['date'] . '-' . $row['session'] . '@giangbai';
        $heading = $row['session'] === 'afternoon' ? 'BUỔI CHIỀU' : 'BUỔI SÁNG';
        $summary = $row['session'] === 'afternoon' ? 'Buổi chiều' : 'Buổi sáng';
        $linesText = [];
        foreach ($group as $item) {
            $linesText[] = '- Tiết ' . $item['period'] . ': ' . $item['subject'] . ' ' . $item['class_name'];
        }
        $description = $heading . ":\n" . implode("\n", $linesText) . "\nGiáo viên: " . (string)($teacher['name'] ?? '');
        $when = $allDay
            ? [
                'DTSTART;VALUE=DATE:' . str_replace('-', '', $row['date']),
                'DTEND;VALUE=DATE:' . (new DateTimeImmutable($row['date']))->modify('+1 day')->format('Ymd'),
            ]
            : [
                'DTSTART;TZID=Asia/Ho_Chi_Minh:' . str_replace('-', '', $row['date']) . 'T' . str_replace(':', '', $slot[0]) . '00',
                'DTEND;TZID=Asia/Ho_Chi_Minh:' . str_replace('-', '', $row['date']) . 'T' . str_replace(':', '', $endSlot[1]) . '00',
            ];
        $lines = array_merge([
            'BEGIN:VEVENT',
            'UID:' . calendar_feed_ics_escape($uid),
            'DTSTAMP:' . $stamp,
        ], $when, [
            'SUMMARY:' . calendar_feed_ics_escape($summary),
            'LOCATION:' . calendar_feed_ics_escape('Lớp ' . $row['class_name']),
            'DESCRIPTION:' . calendar_feed_ics_escape($description),
            'END:VEVENT',
        ]);
        $events[] = implode("\r\n", array_map('calendar_feed_fold', $lines));
    }
    $name = calendar_feed_ics_escape('Lịch báo giảng ' . (string)($teacher['name'] ?? ''));
    $body = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//GiangBai//Lich bao giang//VI',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
        'X-WR-CALNAME:' . $name,
        'BEGIN:VTIMEZONE',
        'TZID:Asia/Ho_Chi_Minh',
        'BEGIN:STANDARD',
        'DTSTART:19700101T000000',
        'TZOFFSETFROM:+0700',
        'TZOFFSETTO:+0700',
        'TZNAME:ICT',
        'END:STANDARD',
        'END:VTIMEZONE',
        implode("\r\n", $events),
        'END:VCALENDAR',
        '',
    ];
    return implode("\r\n", $body);
}

function calendar_feed_page(array $teacher, array $rows): string
{
    $byDate = [];
    foreach ($rows as $row) {
        $byDate[$row['date']][] = $row;
    }
    $days = '';
    $names = [1 => 'Thứ Hai', 2 => 'Thứ Ba', 3 => 'Thứ Tư', 4 => 'Thứ Năm', 5 => 'Thứ Sáu', 6 => 'Thứ Bảy', 7 => 'Chủ Nhật'];
    foreach ($byDate as $date => $dayRows) {
        $stamp = DateTimeImmutable::createFromFormat('Y-m-d', $date);
        $label = $stamp ? ($names[(int)$stamp->format('N')] . ', ngày ' . $stamp->format('d/m/Y')) : $date;
        $body = '';
        foreach (['morning' => ['Buổi sáng', '#fff7ed', '#9a3412'], 'afternoon' => ['Buổi chiều', '#eff6ff', '#1d4ed8']] as $session => $meta) {
            $items = array_values(array_filter($dayRows, static fn(array $row): bool => $row['session'] === $session));
            if (!$items) {
                continue;
            }
            $body .= '<tr><td colspan="5" style="padding:9px 10px;background:' . $meta[1] . ';color:' . $meta[2] . ';font-weight:700;border-top:2px solid #cbd5e1;">' . $meta[0] . '</td></tr>';
            foreach ($items as $index => $row) {
                $bg = $index % 2 ? '#f8fafc' : '#ffffff';
                $body .= '<tr style="background:' . $bg . '"><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;white-space:nowrap;">Tiết ' . htmlspecialchars((string)$row['period']) . '</td><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;text-align:center;font-weight:700;color:#1e3a8a;">' . htmlspecialchars((string)$row['class_name']) . '</td><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;"><span style="display:inline-block;background:#e0f2fe;color:#0369a1;padding:3px 7px;border-radius:999px;font-weight:700;font-size:12px;">' . htmlspecialchars((string)$row['subject']) . '</span></td><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;">Chưa khai báo PPCT</td><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;text-align:center;color:#047857;font-weight:700;">—</td></tr>';
            }
        }
        $days .= '<div style="margin:0 0 18px;border:1px solid #dbeafe;border-radius:10px;overflow:hidden;"><div style="padding:11px 12px;background:#dbeafe;color:#1e3a8a;font-weight:700;font-size:15px;">' . htmlspecialchars($label) . '</div><div style="overflow-x:auto;"><table style="border-collapse:collapse;width:100%;min-width:640px;font-size:13px;"><thead><tr style="background:#f8fafc;color:#475569;"><th align="left" style="padding:9px 8px;">Tiết</th><th style="padding:9px 8px;">Lớp</th><th align="left" style="padding:9px 8px;">Môn</th><th align="left" style="padding:9px 8px;">Bài dạy</th><th style="padding:9px 8px;">PPCT</th></tr></thead><tbody>' . $body . '</tbody></table></div></div>';
    }
    if ($days === '') {
        $days = '<p style="color:#64748b;">Chưa có tiết trong 14 ngày tới.</p>';
    }
    $name = htmlspecialchars((string)($teacher['name'] ?? 'Giáo viên'));
    return '<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="apple-mobile-web-app-title" content="Báo Giảng"><title>Sổ báo giảng</title></head><body style="margin:0;background:#f1f5f9;font-family:Arial,sans-serif;color:#0f172a;"><div style="max-width:980px;margin:0 auto;padding:16px;"><div style="padding:20px;background:#1e3a8a;color:#fff;border-radius:14px;"><div style="font-size:13px;letter-spacing:.08em;text-transform:uppercase;">Sổ báo giảng</div><div style="font-size:24px;font-weight:700;margin-top:6px;">' . $name . '</div></div><p style="color:#475569;">Trên iPhone: bấm nút Chia sẻ của Safari, chọn Thêm vào Màn hình chính. Lần sau chạm biểu tượng Báo Giảng để mở sổ toàn màn hình.</p>' . $days . '</div></body></html>';
}

function calendar_feed_base_url(): string
{
    $https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || ((string)($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');
    $scheme = $https ? 'https' : 'http';
    $host = (string)($_SERVER['HTTP_HOST'] ?? 'localhost');
    $script = (string)($_SERVER['SCRIPT_NAME'] ?? '/api/calendar_feed.php');
    return $scheme . '://' . $host . $script;
}

function calendar_feed_owner_id(): int
{
    $userId = (int)($_SESSION['user_id'] ?? 0);
    if ($userId <= 0) {
        http_response_code(401);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => false, 'error' => 'Vui lòng đăng nhập để lấy link đồng bộ lịch.'], JSON_UNESCAPED_UNICODE);
        exit;
    }
    return $userId;
}

function calendar_feed_plan(PDO $pdo, int $ownerId): ?array
{
    $stmt = $pdo->prepare('SELECT data_json FROM phancong_chuyenmon WHERE owner_id = ? ORDER BY updated_at DESC LIMIT 1');
    $stmt->execute([$ownerId]);
    $row = $stmt->fetch();
    if (!$row) {
        return null;
    }
    $data = json_decode((string)($row['data_json'] ?? ''), true);
    return is_array($data) ? $data : null;
}

$teacherId = trim((string)($_GET['teacher_id'] ?? ''));
$action = trim((string)($_GET['action'] ?? ''));
$allDay = !isset($_GET['all_day']) || (string)$_GET['all_day'] !== '0';

if ($action === 'link') {
    $ownerId = calendar_feed_owner_id();
    if ($teacherId === '') {
        http_response_code(400);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => false, 'error' => 'Thiếu giáo viên cần đồng bộ.'], JSON_UNESCAPED_UNICODE);
        exit;
    }
    $token = calendar_feed_token($ownerId, $teacherId);
    $query = http_build_query([
        'teacher_id' => $teacherId,
        'owner_id' => $ownerId,
        'token' => $token,
        'all_day' => $allDay ? '1' : '0',
    ]);
    $https = calendar_feed_base_url() . '?' . $query;
    $page = calendar_feed_base_url() . '?' . http_build_query([
        'format' => 'html',
        'teacher_id' => $teacherId,
        'owner_id' => $ownerId,
        'token' => $token,
    ]);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode([
        'ok' => true,
        'teacher_id' => $teacherId,
        'https_url' => $https,
        'webcal_url' => preg_replace('/^https?:/', 'webcal:', $https),
        'page_url' => $page,
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

$ownerId = (int)($_GET['owner_id'] ?? 0);
$token = (string)($_GET['token'] ?? '');
$expected = $ownerId > 0 && $teacherId !== '' ? calendar_feed_token($ownerId, $teacherId) : '';
if ($expected === '' || !hash_equals($expected, $token)) {
    http_response_code(403);
    header('Content-Type: text/plain; charset=utf-8');
    echo 'Link đồng bộ không hợp lệ.';
    exit;
}

$data = calendar_feed_plan($pdo, $ownerId);
$built = calendar_feed_rows(is_array($data) ? $data : [], $teacherId);
$teacher = $built['teacher'] ?: ['id' => $teacherId, 'name' => ''];
if ((string)($_GET['format'] ?? '') === 'html') {
    $today = date('Y-m-d');
    $until = date('Y-m-d', strtotime('+14 days'));
    $visible = array_values(array_filter($built['rows'], static fn(array $row): bool => $row['date'] >= $today && $row['date'] <= $until));
    header('Content-Type: text/html; charset=utf-8');
    echo calendar_feed_page($teacher, $visible);
    exit;
}
header('Content-Type: text/calendar; charset=utf-8');
header('Content-Disposition: inline; filename="lich_bao_giang.ics"');
header('Cache-Control: public, max-age=900');
echo calendar_feed_ics($teacher, $built['rows'], $allDay);
