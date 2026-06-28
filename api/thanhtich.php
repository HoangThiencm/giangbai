<?php
require_once __DIR__ . '/helpers.php';

session_start();

const THANHTICH_SCHEMA_VERSION = '20260628-v1';
const THANHTICH_SCHOOL = 'THCS Trần Phú';

function tt_current_teacher(PDO $pdo): array
{
    $userId = (int)($_SESSION['user_id'] ?? 0);
    if ($userId <= 0) {
        respond(['error' => 'Vui lòng đăng nhập lại.'], 401);
    }
    $stmt = $pdo->prepare("SELECT id, username, full_name, role, is_active FROM users WHERE id = ? LIMIT 1");
    $stmt->execute([$userId]);
    $user = $stmt->fetch();
    if (!$user || !(bool)$user['is_active'] || ($user['role'] ?? '') !== 'teacher') {
        respond(['error' => 'Chức năng thống kê thành tích chỉ dành cho giáo viên.'], 403);
    }
    return $user;
}

function tt_maybe_ensure_schema(PDO $pdo): void
{
    if (schema_is_ready('thanhtich', THANHTICH_SCHEMA_VERSION)) {
        return;
    }
    tt_ensure_schema($pdo);
    schema_mark_ready('thanhtich', THANHTICH_SCHEMA_VERSION);
}

function tt_ensure_schema(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS achievement_school_years (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(40) NOT NULL UNIQUE,
        created_by INT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_achievement_school_years_name (name)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    $pdo->exec("CREATE TABLE IF NOT EXISTS achievement_entries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        academic_year VARCHAR(40) NOT NULL DEFAULT '',
        participant_type ENUM('teacher', 'student') NOT NULL,
        campaign_name VARCHAR(300) NOT NULL,
        organizer VARCHAR(300) NOT NULL DEFAULT '',
        scope_level VARCHAR(40) NOT NULL DEFAULT 'school',
        event_date DATE DEFAULT NULL,
        participant_count INT NOT NULL DEFAULT 0,
        prize_count INT NOT NULL DEFAULT 0,
        prize_summary VARCHAR(500) DEFAULT NULL,
        note TEXT DEFAULT NULL,
        created_by INT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_achievement_entries_year (academic_year),
        INDEX idx_achievement_entries_type (participant_type),
        INDEX idx_achievement_entries_organizer (organizer)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    $pdo->exec("CREATE TABLE IF NOT EXISTS achievement_winners (
        id INT AUTO_INCREMENT PRIMARY KEY,
        entry_id INT NOT NULL,
        full_name VARCHAR(180) NOT NULL,
        class_or_role VARCHAR(120) DEFAULT NULL,
        prize_rank VARCHAR(80) NOT NULL DEFAULT '',
        prize_title VARCHAR(300) DEFAULT NULL,
        note TEXT DEFAULT NULL,
        order_index INT NOT NULL DEFAULT 0,
        INDEX idx_achievement_winners_entry (entry_id),
        CONSTRAINT fk_achievement_winner_entry FOREIGN KEY (entry_id) REFERENCES achievement_entries(id) ON DELETE CASCADE
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}

function tt_truncate(string $value, int $length): string
{
    return function_exists('mb_substr') ? mb_substr($value, 0, $length) : substr($value, 0, $length);
}

function tt_academic_year($value): string
{
    $year = trim((string)$value);
    if ($year !== '' && !preg_match('/^\d{4}-\d{4}$/', $year)) {
        throw new RuntimeException('Năm học phải theo định dạng 2025-2026.');
    }
    return tt_truncate($year, 40);
}

function tt_participant_type($value): string
{
    return in_array($value, ['teacher', 'student'], true) ? $value : 'student';
}

function tt_scope_level($value): string
{
    $allowed = ['school', 'district', 'province', 'national', 'international'];
    return in_array($value, $allowed, true) ? $value : 'school';
}

function tt_scope_label(string $scope): string
{
    return [
        'school' => 'Cấp trường',
        'district' => 'Cấp huyện',
        'province' => 'Cấp tỉnh',
        'national' => 'Cấp quốc gia',
        'international' => 'Cấp quốc tế',
    ][$scope] ?? 'Cấp trường';
}

function tt_date($value): ?string
{
    $value = trim((string)$value);
    if ($value === '') {
        return null;
    }
    $time = strtotime($value);
    return $time ? date('Y-m-d', $time) : null;
}

function tt_presets(): array
{
    return [
        'organizers' => [
            'Bộ Giáo dục',
            'Sở Giáo dục',
            'Phòng Văn hoá',
            'Khác',
        ],
        'campaigns_teacher' => [
            'Hội thi giáo viên dạy giỏi cấp trường',
            'Hội thi giáo viên chủ nhiệm giỏi',
            'Hội thi giáo viên làm chủ công nghệ thông tin',
            'Cuộc thi sáng tạo KHKT dành cho giáo viên',
            'Hội thi giáo viên giỏi cấp huyện',
            'Hội thi giáo viên giỏi cấp tỉnh',
            'Phong trào thi đua dạy tốt - học tốt',
            'Cuộc thi viết chữ đẹp',
        ],
        'campaigns_student' => [
            'Hội thi học sinh giỏi',
            'Cuộc thi Olympic Toán học',
            'Cuộc thi Olympic Vật lý',
            'Cuộc thi Olympic Hóa học',
            'Cuộc thi Olympic Tiếng Anh',
            'Cuộc thi Tin học trẻ',
            'Cuộc thi sáng tạo KHKT học sinh',
            'Hội thi văn nghệ học sinh',
            'Hội thi thể dục thể thao học sinh',
            'Cuộc thi vẽ tranh, thi viết văn',
            'Phong trào Đội viên vững vàng',
            'Cuộc thi tìm hiểu lịch sử, địa lý',
            'Cuộc thi an toàn giao thông',
            'Cuộc thi phòng chống tệ nạn xã hội',
        ],
        'prize_ranks' => [
            'Giải Nhất',
            'Giải Nhì',
            'Giải Ba',
            'Giải Khuyến khích',
            'Giải A',
            'Giải B',
            'Giải C',
            'Bằng khen',
            'Huy chương Vàng',
            'Huy chương Bạc',
            'Huy chương Đồng',
            'Cá nhân xuất sắc',
            'Tập thể xuất sắc',
        ],
        'scope_levels' => [
            ['value' => 'school', 'label' => 'Cấp trường'],
            ['value' => 'district', 'label' => 'Cấp huyện'],
            ['value' => 'province', 'label' => 'Cấp tỉnh'],
            ['value' => 'national', 'label' => 'Cấp quốc gia'],
            ['value' => 'international', 'label' => 'Cấp quốc tế'],
        ],
    ];
}

function tt_normalize_winners($rows): array
{
    if (!is_array($rows)) {
        return [];
    }
    $clean = [];
    $order = 0;
    foreach (array_slice($rows, 0, 200) as $row) {
        if (!is_array($row)) {
            continue;
        }
        $fullName = trim((string)($row['full_name'] ?? ''));
        if ($fullName === '') {
            continue;
        }
        $clean[] = [
            'full_name' => tt_truncate($fullName, 180),
            'class_or_role' => tt_truncate(trim((string)($row['class_or_role'] ?? '')), 120),
            'prize_rank' => tt_truncate(trim((string)($row['prize_rank'] ?? '')), 80),
            'prize_title' => tt_truncate(trim((string)($row['prize_title'] ?? '')), 300),
            'note' => trim((string)($row['note'] ?? '')) !== '' ? tt_truncate(trim((string)$row['note']), 500) : null,
            'order_index' => $order++,
        ];
    }
    return $clean;
}

function tt_entry(PDO $pdo, int $id): ?array
{
    $stmt = $pdo->prepare('SELECT e.*, u.full_name AS creator_name FROM achievement_entries e LEFT JOIN users u ON u.id = e.created_by WHERE e.id = ? LIMIT 1');
    $stmt->execute([$id]);
    $entry = $stmt->fetch();
    if (!$entry) {
        return null;
    }
    return tt_attach_winners($pdo, $entry);
}

function tt_attach_winners(PDO $pdo, array $entry): array
{
    $stmt = $pdo->prepare('SELECT id, full_name, class_or_role, prize_rank, prize_title, note, order_index FROM achievement_winners WHERE entry_id = ? ORDER BY order_index, id');
    $stmt->execute([(int)$entry['id']]);
    $winners = $stmt->fetchAll();
    foreach ($winners as &$winner) {
        $winner['id'] = (int)$winner['id'];
        $winner['order_index'] = (int)$winner['order_index'];
    }
    unset($winner);

    $entry['id'] = (int)$entry['id'];
    $entry['participant_count'] = (int)$entry['participant_count'];
    $entry['prize_count'] = (int)$entry['prize_count'];
    $entry['created_by'] = (int)$entry['created_by'];
    $entry['scope_label'] = tt_scope_label((string)$entry['scope_level']);
    $entry['winners'] = $winners;
    $entry['winner_count'] = count($winners);
    return $entry;
}

function tt_save_entry(PDO $pdo, array $user, array $input): array
{
    $id = (int)($input['id'] ?? 0);
    $academicYear = tt_academic_year($input['academic_year'] ?? '');
    if ($academicYear === '') {
        throw new RuntimeException('Cần chọn năm học.');
    }

    $campaignName = tt_truncate(trim((string)($input['campaign_name'] ?? '')), 300);
    if ($campaignName === '') {
        throw new RuntimeException('Vui lòng nhập tên phong trào/cuộc thi.');
    }

    $participantType = tt_participant_type($input['participant_type'] ?? 'student');
    $organizer = tt_truncate(trim((string)($input['organizer'] ?? '')), 300);
    $scopeLevel = tt_scope_level($input['scope_level'] ?? 'school');
    $eventDate = tt_date($input['event_date'] ?? null);
    $participantCount = max(0, (int)($input['participant_count'] ?? 0));
    $prizeSummary = tt_truncate(trim((string)($input['prize_summary'] ?? '')), 500);
    $note = trim((string)($input['note'] ?? ''));
    $note = $note !== '' ? $note : null;
    $winners = tt_normalize_winners($input['winners'] ?? []);
    $prizeCount = max(0, (int)($input['prize_count'] ?? 0));
    if ($prizeCount < count($winners)) {
        $prizeCount = count($winners);
    }

    $pdo->beginTransaction();
    try {
        if ($id > 0) {
            $existing = $pdo->prepare('SELECT id FROM achievement_entries WHERE id = ? LIMIT 1');
            $existing->execute([$id]);
            if (!$existing->fetch()) {
                throw new RuntimeException('Không tìm thấy bản ghi thành tích.');
            }
            $stmt = $pdo->prepare('UPDATE achievement_entries SET academic_year=?, participant_type=?, campaign_name=?, organizer=?, scope_level=?, event_date=?, participant_count=?, prize_count=?, prize_summary=?, note=? WHERE id=?');
            $stmt->execute([$academicYear, $participantType, $campaignName, $organizer, $scopeLevel, $eventDate, $participantCount, $prizeCount, $prizeSummary !== '' ? $prizeSummary : null, $note, $id]);
            $pdo->prepare('DELETE FROM achievement_winners WHERE entry_id = ?')->execute([$id]);
        } else {
            $stmt = $pdo->prepare('INSERT INTO achievement_entries (academic_year, participant_type, campaign_name, organizer, scope_level, event_date, participant_count, prize_count, prize_summary, note, created_by) VALUES (?,?,?,?,?,?,?,?,?,?,?)');
            $stmt->execute([$academicYear, $participantType, $campaignName, $organizer, $scopeLevel, $eventDate, $participantCount, $prizeCount, $prizeSummary !== '' ? $prizeSummary : null, $note, (int)$user['id']]);
            $id = (int)$pdo->lastInsertId();
        }

        if ($winners) {
            $insert = $pdo->prepare('INSERT INTO achievement_winners (entry_id, full_name, class_or_role, prize_rank, prize_title, note, order_index) VALUES (?,?,?,?,?,?,?)');
            foreach ($winners as $winner) {
                $insert->execute([
                    $id,
                    $winner['full_name'],
                    $winner['class_or_role'] !== '' ? $winner['class_or_role'] : null,
                    $winner['prize_rank'],
                    $winner['prize_title'] !== '' ? $winner['prize_title'] : null,
                    $winner['note'],
                    $winner['order_index'],
                ]);
            }
        }

        $pdo->commit();
    } catch (Throwable $e) {
        if ($pdo->inTransaction()) {
            $pdo->rollBack();
        }
        throw $e;
    }

    return tt_entry($pdo, $id) ?: [];
}

function tt_school_years(PDO $pdo): array
{
    $rows = $pdo->query('SELECT name FROM achievement_school_years ORDER BY name DESC')->fetchAll();
    return array_map(static fn(array $row): string => (string)$row['name'], $rows);
}

function tt_summary(PDO $pdo, string $year): array
{
    $stmt = $pdo->prepare("SELECT participant_type, scope_level, organizer, COUNT(*) AS competition_count, SUM(participant_count) AS participants, SUM(prize_count) AS prizes FROM achievement_entries WHERE academic_year = ? GROUP BY participant_type, scope_level, organizer ORDER BY participant_type, organizer");
    $stmt->execute([$year]);
    $groups = $stmt->fetchAll();

    $winnerStmt = $pdo->prepare("SELECT e.participant_type, w.prize_rank, COUNT(*) AS count FROM achievement_winners w INNER JOIN achievement_entries e ON e.id = w.entry_id WHERE e.academic_year = ? GROUP BY e.participant_type, w.prize_rank ORDER BY e.participant_type, count DESC");
    $winnerStmt->execute([$year]);
    $prizeBreakdown = $winnerStmt->fetchAll();

    $totals = [
        'competitions' => 0,
        'participants' => 0,
        'prizes' => 0,
        'teacher_competitions' => 0,
        'student_competitions' => 0,
        'teacher_prizes' => 0,
        'student_prizes' => 0,
    ];
    foreach ($groups as $group) {
        $totals['competitions'] += (int)$group['competition_count'];
        $totals['participants'] += (int)$group['participants'];
        $totals['prizes'] += (int)$group['prizes'];
        if ($group['participant_type'] === 'teacher') {
            $totals['teacher_competitions'] += (int)$group['competition_count'];
            $totals['teacher_prizes'] += (int)$group['prizes'];
        } else {
            $totals['student_competitions'] += (int)$group['competition_count'];
            $totals['student_prizes'] += (int)$group['prizes'];
        }
    }

    return [
        'academic_year' => $year,
        'totals' => $totals,
        'by_organizer' => $groups,
        'prize_breakdown' => $prizeBreakdown,
    ];
}

tt_maybe_ensure_schema($pdo);
$user = tt_current_teacher($pdo);
$action = trim((string)($_GET['action'] ?? 'meta'));

if ($action === 'meta') {
    $years = tt_school_years($pdo);
    $currentYear = (int)date('n') >= 8 ? date('Y') . '-' . ((int)date('Y') + 1) : ((int)date('Y') - 1) . '-' . date('Y');
    if (!in_array($currentYear, $years, true)) {
        array_unshift($years, $currentYear);
    }
    respond([
        'ok' => true,
        'school' => THANHTICH_SCHOOL,
        'school_years' => $years,
        'current_year' => $currentYear,
        'presets' => tt_presets(),
        'user' => ['name' => $user['full_name'], 'username' => $user['username']],
    ]);
}

if ($action === 'list') {
    $year = tt_academic_year($_GET['year'] ?? '');
    $type = trim((string)($_GET['type'] ?? 'all'));
    $search = tt_truncate(trim((string)($_GET['q'] ?? '')), 120);

    $sql = 'SELECT e.*, u.full_name AS creator_name FROM achievement_entries e LEFT JOIN users u ON u.id = e.created_by WHERE 1=1';
    $params = [];
    if ($year !== '') {
        $sql .= ' AND e.academic_year = ?';
        $params[] = $year;
    }
    if (in_array($type, ['teacher', 'student'], true)) {
        $sql .= ' AND e.participant_type = ?';
        $params[] = $type;
    }
    if ($search !== '') {
        $sql .= ' AND (e.campaign_name LIKE ? OR e.organizer LIKE ? OR e.prize_summary LIKE ?)';
        $like = '%' . $search . '%';
        $params[] = $like;
        $params[] = $like;
        $params[] = $like;
    }
    $sql .= ' ORDER BY e.event_date DESC, e.updated_at DESC, e.id DESC';

    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $entries = $stmt->fetchAll();
    foreach ($entries as &$entry) {
        $entry = tt_attach_winners($pdo, $entry);
    }
    unset($entry);

    respond(['ok' => true, 'entries' => $entries]);
}

if ($action === 'summary') {
    $year = tt_academic_year($_GET['year'] ?? '');
    if ($year === '') {
        respond(['error' => 'Cần chọn năm học để tổng hợp.'], 422);
    }
    respond(['ok' => true, 'summary' => tt_summary($pdo, $year)]);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $action === 'create_school_year') {
    $input = json_body();
    try {
        $year = tt_academic_year($input['academic_year'] ?? '');
    } catch (RuntimeException $e) {
        respond(['error' => $e->getMessage()], 422);
    }
    try {
        $stmt = $pdo->prepare('INSERT INTO achievement_school_years (name, created_by) VALUES (?, ?)');
        $stmt->execute([$year, (int)$user['id']]);
    } catch (Throwable $e) {
        // Year already exists.
    }
    respond(['ok' => true, 'academic_year' => $year, 'message' => 'Đã tạo hoặc chọn năm học ' . $year . '.']);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $action === 'save') {
    try {
        $entry = tt_save_entry($pdo, $user, json_body());
        respond(['ok' => true, 'entry' => $entry, 'message' => 'Đã lưu thành tích.']);
    } catch (RuntimeException $e) {
        respond(['error' => $e->getMessage()], 422);
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $action === 'delete') {
    $input = json_body();
    $id = (int)($input['id'] ?? 0);
    if ($id <= 0) {
        respond(['error' => 'Thiếu mã bản ghi.'], 422);
    }
    $stmt = $pdo->prepare('DELETE FROM achievement_entries WHERE id = ?');
    $stmt->execute([$id]);
    if ($stmt->rowCount() <= 0) {
        respond(['error' => 'Không tìm thấy bản ghi.'], 404);
    }
    respond(['ok' => true, 'message' => 'Đã xóa bản ghi thành tích.']);
}

respond(['error' => 'Endpoint không tồn tại.'], 404);