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
    $seen = [];
    foreach ($rows as $row) {
        $period = (int)$row['period'];
        $slot = calendar_feed_period_slot((string)$row['session'], $period);
        if (!$allDay && !$slot) {
            continue;
        }
        $uid = 'baogiang-' . ($teacher['id'] ?? '') . '-' . $row['date'] . '-' . $row['period'] . '-' . $row['session'] . '@giangbai';
        if (isset($seen[$uid])) {
            $uid = 'baogiang-' . ($teacher['id'] ?? '') . '-' . $row['date'] . '-' . $row['period'] . '-' . $row['session'] . '-' . $row['class_name'] . '@giangbai';
        }
        $seen[$uid] = true;
        $summary = '[Tiết ' . $row['period'] . '] ' . $row['subject'] . ' ' . $row['class_name'];
        $description = "Môn: {$row['subject']}\nLớp: {$row['class_name']}\nTiết: {$row['period']}\nGiáo viên: " . (string)($teacher['name'] ?? '');
        $when = $allDay
            ? [
                'DTSTART;VALUE=DATE:' . str_replace('-', '', $row['date']),
                'DTEND;VALUE=DATE:' . (new DateTimeImmutable($row['date']))->modify('+1 day')->format('Ymd'),
            ]
            : [
                'DTSTART;TZID=Asia/Ho_Chi_Minh:' . str_replace('-', '', $row['date']) . 'T' . str_replace(':', '', $slot[0]) . '00',
                'DTEND;TZID=Asia/Ho_Chi_Minh:' . str_replace('-', '', $row['date']) . 'T' . str_replace(':', '', $slot[1]) . '00',
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
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode([
        'ok' => true,
        'teacher_id' => $teacherId,
        'https_url' => $https,
        'webcal_url' => preg_replace('/^https?:/', 'webcal:', $https),
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
header('Content-Type: text/calendar; charset=utf-8');
header('Content-Disposition: inline; filename="lich_bao_giang.ics"');
header('Cache-Control: public, max-age=900');
echo calendar_feed_ics($teacher, $built['rows'], $allDay);
