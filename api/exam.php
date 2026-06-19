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

function exam_to_public_payload(array $row): array
{
    $variants = parse_json_or_default($row['variants_json'] ?? null, []);
    $questions = [];
    if (is_array($variants) && !empty($variants[0]['questions']) && is_array($variants[0]['questions'])) {
        $questions = $variants[0]['questions'];
    }
    return [
        'info' => [
            'title' => $row['title'],
            'school' => $row['school'],
            'duration_mins' => (int)$row['duration_mins'],
            'id' => $row['id'],
            'start_time' => $row['start_time'],
            'end_time' => $row['end_time'],
            'status' => exam_status($row),
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

    $variants = [[
        'exam_code' => 'ROOT',
        'questions' => $questions,
        'meta' => ['google_sheet_id' => $data['google_sheet_id'] ?? null],
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
    $questions = [];
    if (is_array($variants) && !empty($variants[0]['questions']) && is_array($variants[0]['questions'])) {
        $questions = $variants[0]['questions'];
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
        trim((string)($data['student_name'] ?? '')),
        trim((string)($data['sbd'] ?? '')),
        trim((string)($data['student_class'] ?? '')),
        $score,
        $correct,
        $total,
        json_encode($wrong, JSON_UNESCAPED_UNICODE),
        $feedback,
    ]);

    respond(['score' => $score, 'total' => $total, 'feedback' => $feedback]);
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