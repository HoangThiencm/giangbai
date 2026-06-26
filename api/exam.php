<?php
require_once __DIR__ . '/helpers.php';

set_exception_handler(function (Throwable $e) {
    $payload = ['error' => 'Lỗi server thi trực tuyến.'];
    if (!empty($_GET['debug']) || (defined('APP_DEBUG') && APP_DEBUG)) {
        $payload['detail'] = $e->getMessage();
    }
    respond($payload, 500);
});

function parse_json_or_default($value, $default)
{
    if ($value === null || $value === '') return $default;
    $decoded = json_decode($value, true);
    return is_array($decoded) ? $decoded : $default;
}

function mysql_datetime_or_null($value): ?string
{
    $value = trim((string)($value ?? ''));
    if ($value === '') return null;
    try {
        $date = new DateTime($value);
        $date->setTimezone(new DateTimeZone('UTC'));
        return $date->format('Y-m-d H:i:s');
    } catch (Throwable $e) {
        if (preg_match('/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/', $value)) {
            return $value;
        }
        return null;
    }
}

function table_exists(PDO $pdo, string $table): bool
{
    try {
        $safeTable = preg_replace('/[^a-zA-Z0-9_]/', '', $table);
        if ($safeTable === '') return false;
        $stmt = $pdo->query('SHOW TABLES LIKE ' . $pdo->quote($safeTable));
        return (bool)$stmt->fetch();
    } catch (Throwable $e) {
        return false;
    }
}

function ensure_exam_schema(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS exams (
        id VARCHAR(16) PRIMARY KEY,
        teacher_email VARCHAR(160) NOT NULL,
        title VARCHAR(255) NOT NULL,
        school VARCHAR(160) NOT NULL DEFAULT '',
        duration_mins INT NOT NULL DEFAULT 45,
        variants_json LONGTEXT NOT NULL,
        api_keys_backup TEXT DEFAULT NULL,
        start_time DATETIME DEFAULT NULL,
        end_time DATETIME DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_exams_teacher (teacher_email),
        INDEX idx_exams_created (created_at)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    $pdo->exec("CREATE TABLE IF NOT EXISTS exam_submissions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        exam_id VARCHAR(16) NOT NULL,
        student_name VARCHAR(160) NOT NULL DEFAULT '',
        sbd VARCHAR(80) NOT NULL DEFAULT '',
        student_class VARCHAR(80) NOT NULL DEFAULT '',
        score DECIMAL(5,2) NOT NULL DEFAULT 0,
        correct_count INT NOT NULL DEFAULT 0,
        total_questions INT NOT NULL DEFAULT 0,
        details_json LONGTEXT DEFAULT NULL,
        ai_feedback TEXT DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_submissions_exam (exam_id),
        INDEX idx_submissions_score (score)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}

function current_teacher(PDO $pdo): ?array
{
    if (empty($_SESSION['user_id'])) return null;
    $stmt = $pdo->prepare("SELECT * FROM users WHERE id = ? AND role = 'teacher' AND is_active = 1 LIMIT 1");
    $stmt->execute([(int)$_SESSION['user_id']]);
    $user = $stmt->fetch();
    return $user ?: null;
}

function require_teacher(PDO $pdo): array
{
    $teacher = current_teacher($pdo);
    if (!$teacher) {
        respond(['error' => 'Cần đăng nhập tài khoản giáo viên.'], 401);
    }
    return $teacher;
}

function new_exam_id(): string
{
    return bin2hex(random_bytes(4));
}

function exam_row_to_list_item(array $row): array
{
    return [
        'id' => $row['id'],
        'teacher_email' => $row['teacher_email'],
        'title' => $row['title'],
        'school' => $row['school'],
        'duration_mins' => (int)$row['duration_mins'],
        'variants_json' => $row['variants_json'],
        'api_keys_backup' => $row['api_keys_backup'],
        'start_time' => $row['start_time'],
        'end_time' => $row['end_time'],
        'created_at' => $row['created_at'],
    ];
}

function fetch_exam(PDO $pdo, string $examId): ?array
{
    $stmt = $pdo->prepare('SELECT * FROM exams WHERE id = ? LIMIT 1');
    $stmt->execute([$examId]);
    $row = $stmt->fetch();
    return $row ?: null;
}

function exam_status(array $row): string
{
    $now = new DateTime('now', new DateTimeZone('UTC'));
    $start = $row['start_time'] ?? null;
    $end = $row['end_time'] ?? null;
    if ($start) {
        try {
            if ($now < new DateTime($start, new DateTimeZone('UTC'))) return 'not_started';
        } catch (Throwable $e) {
        }
    }
    if ($end) {
        try {
            if ($now > new DateTime($end, new DateTimeZone('UTC'))) return 'expired';
        } catch (Throwable $e) {
        }
    }
    return 'open';
}

function parse_exam_meta(array $variants): array
{
    if (!is_array($variants) || empty($variants[0]['meta']) || !is_array($variants[0]['meta'])) {
        return [];
    }
    return $variants[0]['meta'];
}

function normalize_roster_entry($entry): ?array
{
    if (!is_array($entry)) return null;
    $fullName = trim((string)($entry['full_name'] ?? $entry['name'] ?? ''));
    $sbd = trim((string)($entry['sbd'] ?? $entry['username'] ?? ''));
    if ($fullName === '' || $sbd === '') return null;
    return [
        'student_id' => isset($entry['student_id']) ? (int)$entry['student_id'] : 0,
        'username' => trim((string)($entry['username'] ?? $sbd)),
        'full_name' => $fullName,
        'sbd' => $sbd,
        'class_name' => trim((string)($entry['class_name'] ?? '')),
    ];
}

function normalize_roster($roster): array
{
    if (!is_array($roster)) return [];
    $seen = [];
    $normalized = [];
    foreach ($roster as $entry) {
        $item = normalize_roster_entry($entry);
        if (!$item) continue;
        $key = strtolower($item['sbd']) . '|' . strtolower($item['full_name']);
        if (isset($seen[$key])) continue;
        $seen[$key] = true;
        $normalized[] = $item;
    }
    return $normalized;
}

function fetch_distinct_classes(PDO $pdo): array
{
    $stmt = $pdo->query("
        SELECT DISTINCT class_name
        FROM users
        WHERE role = 'student' AND is_active = 1 AND TRIM(class_name) <> ''
        ORDER BY class_name ASC
    ");
    $classes = [];
    foreach ($stmt->fetchAll() as $row) {
        $name = trim((string)($row['class_name'] ?? ''));
        if ($name !== '') $classes[] = $name;
    }
    return $classes;
}

function fetch_class_roster(PDO $pdo, string $className): array
{
    $className = trim($className);
    if ($className === '') return [];
    $stmt = $pdo->prepare("
        SELECT id, username, full_name, class_name
        FROM users
        WHERE role = 'student' AND is_active = 1 AND class_name = ?
        ORDER BY full_name ASC, username ASC
    ");
    $stmt->execute([$className]);
    $roster = [];
    foreach ($stmt->fetchAll() as $row) {
        $roster[] = [
            'student_id' => (int)$row['id'],
            'username' => trim((string)$row['username']),
            'full_name' => trim((string)$row['full_name']),
            'sbd' => trim((string)$row['username']),
            'class_name' => trim((string)$row['class_name']),
        ];
    }
    return $roster;
}

function build_exam_meta(array $data, PDO $pdo): array
{
    $mode = trim((string)($data['student_mode'] ?? 'free'));
    if (!in_array($mode, ['free', 'class'], true)) $mode = 'free';

    $className = trim((string)($data['class_name'] ?? ''));
    $roster = normalize_roster($data['roster'] ?? []);

    if ($mode === 'class') {
        if ($className === '') {
            respond(['error' => 'Vui lòng chọn lớp khi dùng danh sách từ lớp.'], 422);
        }
        if (count($roster) === 0) {
            $roster = fetch_class_roster($pdo, $className);
        }
        if (count($roster) === 0) {
            respond(['error' => 'Lớp đã chọn không có học sinh hoạt động.'], 422);
        }
        foreach ($roster as $idx => $item) {
            if ($item['class_name'] === '') {
                $roster[$idx]['class_name'] = $className;
            }
        }
    } else {
        $className = '';
        $roster = [];
    }

    $maxAttempts = 0;
    if ($mode === 'class') {
        $maxAttempts = parse_max_attempts($data['max_attempts'] ?? 0);
    }

    $meta = [
        'google_sheet_id' => $data['google_sheet_id'] ?? null,
        'student_mode' => $mode,
        'class_name' => $className,
        'roster' => $roster,
        'max_attempts' => $maxAttempts,
    ];
    if (isset($data['matrixConfig']) && is_array($data['matrixConfig'])) {
        $meta['matrixConfig'] = $data['matrixConfig'];
    }
    if (!empty($data['subject'])) {
        $meta['subject'] = trim((string)$data['subject']);
    }
    if (!empty($data['grade'])) {
        $meta['grade'] = trim((string)$data['grade']);
    }
    return $meta;
}

function roster_matches_submission(array $roster, string $name, string $sbd): bool
{
    $nameKey = strtolower(trim($name));
    $sbdKey = strtolower(trim($sbd));
    if ($nameKey === '' || $sbdKey === '') return false;
    foreach ($roster as $entry) {
        $entryName = strtolower(trim((string)($entry['full_name'] ?? '')));
        $entrySbd = strtolower(trim((string)($entry['sbd'] ?? '')));
        if ($entryName === $nameKey && $entrySbd === $sbdKey) return true;
    }
    return false;
}

function student_submission_key(string $name, string $sbd): string
{
    return strtolower(trim($sbd)) . '|' . strtolower(trim($name));
}

function count_student_submissions(PDO $pdo, string $examId, string $name, string $sbd): int
{
    $stmt = $pdo->prepare('SELECT COUNT(*) FROM exam_submissions WHERE exam_id = ? AND LOWER(TRIM(student_name)) = ? AND LOWER(TRIM(sbd)) = ?');
    $stmt->execute([
        $examId,
        strtolower(trim($name)),
        strtolower(trim($sbd)),
    ]);
    return (int)$stmt->fetchColumn();
}

function parse_max_attempts($value): int
{
    $max = (int)$value;
    return $max < 0 ? 0 : $max;
}

function exam_to_public_payload(array $row): array
{
    $variants = parse_json_or_default($row['variants_json'] ?? null, []);
    $meta = parse_exam_meta($variants);
    $questions = [];
    if (is_array($variants) && !empty($variants[0]['questions']) && is_array($variants[0]['questions'])) {
        $questions = $variants[0]['questions'];
    }
    $studentMode = in_array($meta['student_mode'] ?? '', ['free', 'class'], true) ? $meta['student_mode'] : 'free';
    return [
        'info' => [
            'title' => $row['title'],
            'school' => $row['school'],
            'duration_mins' => (int)$row['duration_mins'],
            'id' => $row['id'],
            'start_time' => $row['start_time'],
            'end_time' => $row['end_time'],
            'status' => exam_status($row),
            'student_mode' => $studentMode,
            'class_name' => trim((string)($meta['class_name'] ?? '')),
            'roster' => $studentMode === 'class' ? normalize_roster($meta['roster'] ?? []) : [],
            'max_attempts' => $studentMode === 'class' ? parse_max_attempts($meta['max_attempts'] ?? 0) : 0,
            'matrixConfig' => $meta['matrixConfig'] ?? null,
            'subject' => $meta['subject'] ?? '',
            'grade' => $meta['grade'] ?? '',
        ],
        'questions' => $questions,
    ];
}

function teacher_owns_exam(array $teacher, array $exam): bool
{
    $owner = strtolower(trim((string)($exam['teacher_email'] ?? '')));
    $username = strtolower(trim((string)($teacher['username'] ?? '')));
    return $owner !== '' && $owner === $username;
}

function parse_route(): array
{
    $route = trim((string)($_GET['route'] ?? ''), '/');
    if ($route === '' && !empty($_SERVER['PATH_INFO'])) {
        $route = trim((string)$_SERVER['PATH_INFO'], '/');
    }
    return $route === '' ? [] : explode('/', $route);
}

ensure_exam_schema($pdo);

$method = $_SERVER['REQUEST_METHOD'];
$parts = parse_route();
$action = $parts[0] ?? '';

if ($method === 'POST' && $action === 'save') {
    $teacher = require_teacher($pdo);
    $data = json_body();
    $title = trim((string)($data['title'] ?? ''));
    if ($title === '') {
        respond(['error' => 'Thiếu tên đề thi.'], 422);
    }

    $questions = $data['questions'] ?? [];
    if (!is_array($questions)) $questions = [];
    $apiKeys = $data['api_keys'] ?? [];
    if (!is_array($apiKeys)) $apiKeys = [];

    $meta = build_exam_meta($data, $pdo);
    $variants = [[
        'exam_code' => 'ROOT',
        'questions' => $questions,
        'meta' => $meta,
    ]];

    $examId = trim((string)($data['id'] ?? ''));
    $payload = [
        'teacher_email' => trim((string)($data['teacher_email'] ?? $teacher['username'])),
        'title' => $title,
        'school' => trim((string)($data['school'] ?? '')),
        'duration_mins' => max(1, (int)($data['duration'] ?? $data['duration_mins'] ?? 45)),
        'variants_json' => json_encode($variants, JSON_UNESCAPED_UNICODE),
        'api_keys_backup' => json_encode($apiKeys, JSON_UNESCAPED_UNICODE),
        'start_time' => mysql_datetime_or_null($data['start_time'] ?? null),
        'end_time' => mysql_datetime_or_null($data['end_time'] ?? null),
    ];

    if ($examId !== '') {
        $existing = fetch_exam($pdo, $examId);
        if (!$existing) respond(['error' => 'Không tìm thấy đề thi.'], 404);
        if (!teacher_owns_exam($teacher, $existing)) respond(['error' => 'Không có quyền sửa đề này.'], 403);
        $stmt = $pdo->prepare('UPDATE exams SET teacher_email = ?, title = ?, school = ?, duration_mins = ?, variants_json = ?, api_keys_backup = ?, start_time = ?, end_time = ? WHERE id = ?');
        $stmt->execute([
            $payload['teacher_email'],
            $payload['title'],
            $payload['school'],
            $payload['duration_mins'],
            $payload['variants_json'],
            $payload['api_keys_backup'],
            $payload['start_time'],
            $payload['end_time'],
            $examId,
        ]);
    } else {
        $examId = new_exam_id();
        $stmt = $pdo->prepare('INSERT INTO exams (id, teacher_email, title, school, duration_mins, variants_json, api_keys_backup, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)');
        $stmt->execute([
            $examId,
            $payload['teacher_email'],
            $payload['title'],
            $payload['school'],
            $payload['duration_mins'],
            $payload['variants_json'],
            $payload['api_keys_backup'],
            $payload['start_time'],
            $payload['end_time'],
        ]);
    }

    respond(['status' => 'ok', 'exam_id' => $examId]);
}

if ($method === 'GET' && $action === 'student-classes') {
    require_teacher($pdo);
    respond(['classes' => fetch_distinct_classes($pdo)]);
}

if ($method === 'GET' && $action === 'class-students') {
    require_teacher($pdo);
    $className = trim((string)($_GET['class_name'] ?? ''));
    if ($className === '') {
        respond(['error' => 'Thiếu tên lớp.'], 422);
    }
    $roster = fetch_class_roster($pdo, $className);
    respond([
        'class_name' => $className,
        'count' => count($roster),
        'roster' => $roster,
    ]);
}

if ($method === 'GET' && $action === 'get' && !empty($parts[1])) {
    $exam = fetch_exam($pdo, $parts[1]);
    if (!$exam) respond(['error' => 'Not Found'], 404);
    respond(exam_to_public_payload($exam));
}

if ($method === 'GET' && $action === 'my-exams') {
    $teacher = require_teacher($pdo);
    $email = trim((string)($_GET['email'] ?? $teacher['username']));
    if (strtolower($email) !== strtolower((string)$teacher['username'])) {
        respond(['error' => 'Không có quyền xem đề của tài khoản khác.'], 403);
    }
    $stmt = $pdo->prepare('SELECT * FROM exams WHERE teacher_email = ? ORDER BY created_at DESC');
    $stmt->execute([$email]);
    $rows = $stmt->fetchAll();
    respond(array_map('exam_row_to_list_item', $rows));
}

if ($method === 'DELETE' && $action === 'delete' && !empty($parts[1])) {
    $teacher = require_teacher($pdo);
    $exam = fetch_exam($pdo, $parts[1]);
    if (!$exam) respond(['error' => 'Not Found'], 404);
    if (!teacher_owns_exam($teacher, $exam)) respond(['error' => 'Không có quyền xóa đề này.'], 403);
    $pdo->prepare('DELETE FROM exam_submissions WHERE exam_id = ?')->execute([$parts[1]]);
    $pdo->prepare('DELETE FROM exams WHERE id = ?')->execute([$parts[1]]);
    respond(['message' => 'Deleted']);
}

if ($method === 'POST' && $action === 'duplicate' && !empty($parts[1])) {
    $teacher = require_teacher($pdo);
    $exam = fetch_exam($pdo, $parts[1]);
    if (!$exam) respond(['error' => 'Exam not found'], 404);
    if (!teacher_owns_exam($teacher, $exam)) respond(['error' => 'Không có quyền nhân bản đề này.'], 403);

    $newId = new_exam_id();
    $newTitle = trim((string)$exam['title']) . ' (Copy)';
    $stmt = $pdo->prepare('INSERT INTO exams (id, teacher_email, title, school, duration_mins, variants_json, api_keys_backup, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)');
    $stmt->execute([
        $newId,
        $exam['teacher_email'],
        $newTitle,
        $exam['school'],
        $exam['duration_mins'],
        $exam['variants_json'],
        $exam['api_keys_backup'],
        $exam['start_time'],
        $exam['end_time'],
    ]);
    respond(['status' => 'ok', 'new_id' => $newId]);
}

if ($method === 'POST' && $action === 'submit') {
    $data = json_body();
    $examId = trim((string)($data['exam_id'] ?? ''));
    if ($examId === '') respond(['error' => 'Thiếu exam_id.'], 422);

    $exam = fetch_exam($pdo, $examId);
    if (!$exam) respond(['error' => 'Not Found'], 404);

    $status = exam_status($exam);
    if ($status === 'not_started') respond(['error' => 'Kỳ thi chưa bắt đầu.'], 403);
    if ($status === 'expired') respond(['error' => 'Kỳ thi đã kết thúc.'], 403);

    $variants = parse_json_or_default($exam['variants_json'] ?? null, []);
    $meta = parse_exam_meta($variants);
    $studentMode = in_array($meta['student_mode'] ?? '', ['free', 'class'], true) ? $meta['student_mode'] : 'free';
    $roster = $studentMode === 'class' ? normalize_roster($meta['roster'] ?? []) : [];
    $questions = [];
    if (is_array($variants) && !empty($variants[0]['questions']) && is_array($variants[0]['questions'])) {
        $questions = $variants[0]['questions'];
    }

    $studentName = trim((string)($data['student_name'] ?? ''));
    $sbd = trim((string)($data['sbd'] ?? ''));
    $studentClass = trim((string)($data['student_class'] ?? ''));

    if ($studentMode === 'class') {
        if (count($roster) === 0) {
            respond(['error' => 'Đề thi chưa có danh sách thí sinh hợp lệ.'], 422);
        }
        if (!roster_matches_submission($roster, $studentName, $sbd)) {
            respond(['error' => 'Thí sinh không có trong danh sách lớp của đề thi.'], 403);
        }
        if ($studentClass === '') {
            $studentClass = trim((string)($meta['class_name'] ?? ''));
        }

        $maxAttempts = parse_max_attempts($meta['max_attempts'] ?? 0);
        if ($maxAttempts > 0) {
            $attemptCount = count_student_submissions($pdo, $examId, $studentName, $sbd);
            if ($attemptCount >= $maxAttempts) {
                respond([
                    'error' => "Bạn đã thi đủ {$maxAttempts} lần cho đề này. Không thể nộp thêm bài.",
                    'attempt_count' => $attemptCount,
                    'max_attempts' => $maxAttempts,
                ], 403);
            }
        }
    }

    $answers = $data['answers'] ?? [];
    if (!is_array($answers)) $answers = [];

    $correct = 0;
    $wrong = [];
    foreach ($questions as $i => $q) {
        $userAns = $answers[(string)$i] ?? $answers[$i] ?? null;
        $trueAns = isset($q['correct_index']) ? (int)$q['correct_index'] : -1;
        if ($userAns !== null && (int)$userAns === $trueAns) {
            $correct++;
        } else {
            $options = $q['options'] ?? [];
            $wrong[] = [
                'q' => $q['question'] ?? '',
                'ans' => ($trueAns >= 0 && isset($options[$trueAns])) ? $options[$trueAns] : '?',
            ];
        }
    }

    $total = count($questions);
    $score = $total > 0 ? round(($correct / $total) * 10, 2) : 0;
    $feedback = "Bạn làm đúng {$correct}/{$total} câu.";

    $stmt = $pdo->prepare('INSERT INTO exam_submissions (exam_id, student_name, sbd, student_class, score, correct_count, total_questions, details_json, ai_feedback) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)');
    $stmt->execute([
        $examId,
        $studentName,
        $sbd,
        $studentClass,
        $score,
        $correct,
        $total,
        json_encode($wrong, JSON_UNESCAPED_UNICODE),
        $feedback,
    ]);

    respond(['score' => $score, 'total' => $total, 'feedback' => $feedback]);
}

if ($method === 'GET' && $action === 'student-attempts') {
    $examId = trim((string)($_GET['exam_id'] ?? ''));
    $studentName = trim((string)($_GET['student_name'] ?? ''));
    $sbd = trim((string)($_GET['sbd'] ?? ''));
    if ($examId === '' || $studentName === '' || $sbd === '') {
        respond(['error' => 'Thiếu thông tin thí sinh.'], 422);
    }

    $exam = fetch_exam($pdo, $examId);
    if (!$exam) respond(['error' => 'Not Found'], 404);

    $variants = parse_json_or_default($exam['variants_json'] ?? null, []);
    $meta = parse_exam_meta($variants);
    $studentMode = in_array($meta['student_mode'] ?? '', ['free', 'class'], true) ? $meta['student_mode'] : 'free';
    $maxAttempts = $studentMode === 'class' ? parse_max_attempts($meta['max_attempts'] ?? 0) : 0;
    $attemptCount = count_student_submissions($pdo, $examId, $studentName, $sbd);
    $remaining = $maxAttempts > 0 ? max(0, $maxAttempts - $attemptCount) : null;

    respond([
        'attempt_count' => $attemptCount,
        'max_attempts' => $maxAttempts,
        'remaining' => $remaining,
        'can_attempt' => $maxAttempts <= 0 || $attemptCount < $maxAttempts,
    ]);
}

if ($method === 'GET' && $action === 'results' && !empty($parts[1])) {
    $teacher = require_teacher($pdo);
    $exam = fetch_exam($pdo, $parts[1]);
    if (!$exam) respond(['error' => 'Not Found'], 404);
    if (!teacher_owns_exam($teacher, $exam)) respond(['error' => 'Không có quyền xem kết quả đề này.'], 403);

    $stmt = $pdo->prepare('SELECT * FROM exam_submissions WHERE exam_id = ? ORDER BY score DESC, created_at DESC');
    $stmt->execute([$parts[1]]);
    respond($stmt->fetchAll());
}

if ($method === 'DELETE' && $action === 'result' && !empty($parts[1])) {
    $teacher = require_teacher($pdo);
    $resultId = (int)$parts[1];
    $stmt = $pdo->prepare('SELECT s.*, e.teacher_email FROM exam_submissions s JOIN exams e ON e.id = s.exam_id WHERE s.id = ? LIMIT 1');
    $stmt->execute([$resultId]);
    $row = $stmt->fetch();
    if (!$row) respond(['error' => 'Không tìm thấy kết quả'], 404);
    $exam = ['teacher_email' => $row['teacher_email']];
    if (!teacher_owns_exam($teacher, $exam)) respond(['error' => 'Không có quyền xóa kết quả này.'], 403);

    $pdo->prepare('DELETE FROM exam_submissions WHERE id = ?')->execute([$resultId]);
    respond(['status' => 'ok', 'message' => 'Đã xóa kết quả', 'id' => $resultId]);
}

if ($method === 'POST' && $action === 'results' && ($parts[1] ?? '') === 'delete-batch') {
    $teacher = require_teacher($pdo);
    $data = json_body();
    $ids = $data['ids'] ?? [];
    if (!is_array($ids) || count($ids) === 0) {
        respond(['error' => 'Thiếu danh sách id'], 400);
    }
    $ids = array_values(array_unique(array_filter(array_map('intval', $ids))));
    if (count($ids) === 0) respond(['error' => 'Thiếu danh sách id'], 400);

    $placeholders = implode(',', array_fill(0, count($ids), '?'));
    $stmt = $pdo->prepare("SELECT s.id, e.teacher_email FROM exam_submissions s JOIN exams e ON e.id = s.exam_id WHERE s.id IN ($placeholders)");
    $stmt->execute($ids);
    $rows = $stmt->fetchAll();
    if (count($rows) !== count($ids)) respond(['error' => 'Một số bản ghi không tồn tại.'], 404);
    foreach ($rows as $row) {
        if (!teacher_owns_exam($teacher, ['teacher_email' => $row['teacher_email']])) {
            respond(['error' => 'Không có quyền xóa một số kết quả.'], 403);
        }
    }

    $del = $pdo->prepare("DELETE FROM exam_submissions WHERE id IN ($placeholders)");
    $del->execute($ids);
    respond(['status' => 'ok', 'deleted' => count($ids)]);
}

respond(['error' => 'Method not allowed.'], 405);