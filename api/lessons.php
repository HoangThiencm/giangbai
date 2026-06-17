<?php
require_once __DIR__ . '/helpers.php';
session_start();

function parse_json_or_default($value, $default)
{
    if ($value === null || $value === '') return $default;
    $decoded = json_decode($value, true);
    return is_array($decoded) ? $decoded : $default;
}

function lesson_row_to_payload(array $row): array
{
    return [
        'id' => (int)$row['id'],
        'subject' => $row['subject'],
        'chapter' => $row['chapter'],
        'title' => $row['title'],
        'slug' => $row['slug'],
        'order_index' => (int)$row['order_index'],
        'is_published' => (bool)$row['is_published'],
        'goal' => $row['goal_text'] ?: '',
        'theory' => parse_json_or_default($row['theory_json'], []),
        'examples' => parse_json_or_default($row['examples_json'], []),
        'questions' => parse_json_or_default($row['questions_json'], []),
        'tasks' => parse_json_or_default($row['tasks_json'], []),
        'skills' => parse_json_or_default($row['skills_json'], []),
    ];
}

function ensure_login(): array
{
    if (empty($_SESSION['user_id'])) {
        respond(['error' => 'Chưa đăng nhập.'], 401);
    }
    $stmt = $GLOBALS['pdo']->prepare('SELECT * FROM users WHERE id = ? LIMIT 1');
    $stmt->execute([$_SESSION['user_id']]);
    $user = $stmt->fetch();
    if (!$user || !(bool)$user['is_active']) {
        respond(['error' => 'Tài khoản không còn hoạt động.'], 403);
    }
    return $user;
}

function ensure_lesson_schema(PDO $pdo): void
{
    $columns = [
        'goal_text TEXT DEFAULT NULL',
        'theory_json LONGTEXT DEFAULT NULL',
        'examples_json LONGTEXT DEFAULT NULL',
        'questions_json LONGTEXT DEFAULT NULL',
        'tasks_json LONGTEXT DEFAULT NULL',
        'skills_json LONGTEXT DEFAULT NULL'
    ];
    foreach ($columns as $definition) {
        $name = trim(strtok($definition, ' '));
        $stmt = $pdo->prepare("SHOW COLUMNS FROM lessons LIKE ?");
        $stmt->execute([$name]);
        if (!$stmt->fetch()) {
            $pdo->exec("ALTER TABLE lessons ADD COLUMN $definition");
        }
    }
}

ensure_lesson_schema($pdo);

function ensure_progress_schema(PDO $pdo): void
{
    $stmt = $pdo->prepare("SHOW COLUMNS FROM student_lesson_progress LIKE ?");
    $stmt->execute(['state_json']);
    if (!$stmt->fetch()) {
        $pdo->exec("ALTER TABLE student_lesson_progress ADD COLUMN state_json TEXT DEFAULT NULL");
    }
}

ensure_progress_schema($pdo);

$method = $_SERVER['REQUEST_METHOD'];
$action = $_GET['action'] ?? ($_POST['action'] ?? '');
$adminKey = $_SERVER['HTTP_X_ADMIN_KEY'] ?? ($_GET['admin_key'] ?? '');
$isAdmin = defined('ADMIN_KEY') && hash_equals(ADMIN_KEY, $adminKey);

if ($method === 'GET' && $isAdmin && !empty($_GET['admin'])) {
    $stmt = $pdo->query('SELECT * FROM lessons ORDER BY order_index ASC, id ASC');
    respond(['ok' => true, 'lessons' => array_map('lesson_row_to_payload', $stmt->fetchAll())]);
}

if ($method === 'GET') {
    $user = ensure_login();
    $stmt = $pdo->query('SELECT * FROM lessons ORDER BY order_index ASC, id ASC');
    $lessons = array_map('lesson_row_to_payload', $stmt->fetchAll());

    if ($user['role'] === 'student') {
        $lessons = array_values(array_filter($lessons, fn($lesson) => $lesson['is_published']));
    }

    $progressStmt = $pdo->prepare('SELECT * FROM student_lesson_progress WHERE student_id = ?');
    $progressStmt->execute([$user['id']]);
    $progressRows = $progressStmt->fetchAll();
    $progressMap = [];
    foreach ($progressRows as $row) {
        $progressMap[(int)$row['lesson_id']] = [
            'status' => $row['status'],
            'score' => (int)$row['score'],
            'skillScores' => parse_json_or_default($row['skill_scores_json'], []),
            'state' => parse_json_or_default($row['state_json'], []),
            'startedAt' => $row['started_at'],
            'completedAt' => $row['completed_at'],
        ];
    }

    respond([
        'ok' => true,
        'user' => public_user($user),
        'lessons' => $lessons,
        'progress' => $progressMap,
    ]);
}

if ($method === 'POST' && $action === 'save_progress') {
    $user = ensure_login();
    $data = json_body();
    $lessonId = (int)($data['lesson_id'] ?? 0);
    if ($lessonId <= 0) respond(['error' => 'Thiếu lesson_id.'], 422);

    $status = $data['status'] ?? 'not_started';
    if (!in_array($status, ['not_started', 'in_progress', 'needs_practice', 'mastered'], true)) {
        $status = 'not_started';
    }
    $score = max(0, min(100, (int)($data['score'] ?? 0)));
    $skillScores = $data['skill_scores'] ?? [];
    if (!is_array($skillScores)) $skillScores = [];
    $state = $data['state'] ?? [];
    if (!is_array($state)) $state = [];

    $startedAt = !empty($data['started_at']) ? $data['started_at'] : null;
    $completedAt = !empty($data['completed_at']) ? $data['completed_at'] : null;

    $stmt = $pdo->prepare('SELECT id FROM student_lesson_progress WHERE student_id = ? AND lesson_id = ? LIMIT 1');
    $stmt->execute([$user['id'], $lessonId]);
    $exists = $stmt->fetch();

    if ($exists) {
        $update = $pdo->prepare('
            UPDATE student_lesson_progress
            SET status = ?, score = ?, skill_scores_json = ?, state_json = ?, started_at = COALESCE(?, started_at), completed_at = COALESCE(?, completed_at)
            WHERE student_id = ? AND lesson_id = ?
        ');
        $update->execute([$status, $score, json_encode($skillScores, JSON_UNESCAPED_UNICODE), json_encode($state, JSON_UNESCAPED_UNICODE), $startedAt, $completedAt, $user['id'], $lessonId]);
    } else {
        $insert = $pdo->prepare('
            INSERT INTO student_lesson_progress (student_id, lesson_id, status, score, skill_scores_json, state_json, started_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ');
        $insert->execute([$user['id'], $lessonId, $status, $score, json_encode($skillScores, JSON_UNESCAPED_UNICODE), json_encode($state, JSON_UNESCAPED_UNICODE), $startedAt, $completedAt]);
    }

    respond(['ok' => true]);
}

if ($method === 'POST' && $action === 'reset_progress') {
    $user = ensure_login();
    $data = json_body();
    $lessonId = (int)($data['lesson_id'] ?? 0);
    if ($lessonId <= 0) respond(['error' => 'Thiếu lesson_id.'], 422);

    $stmt = $pdo->prepare('DELETE FROM student_lesson_progress WHERE student_id = ? AND lesson_id = ?');
    $stmt->execute([$user['id'], $lessonId]);
    respond(['ok' => true]);
}

if ($method === 'POST' && $action === 'save_content') {
    if (!$isAdmin) respond(['error' => 'Sai Admin Key.'], 401);
    $data = json_body();
    $slug = trim($data['slug'] ?? '');
    if ($slug === '') respond(['error' => 'Thiếu slug.'], 422);

    $payload = [
        'subject' => trim($data['subject'] ?? 'Toán 6'),
        'chapter' => trim($data['chapter'] ?? ''),
        'title' => trim($data['title'] ?? ''),
        'goal_text' => trim($data['goal_text'] ?? ''),
        'theory_json' => json_encode($data['theory'] ?? [], JSON_UNESCAPED_UNICODE),
        'examples_json' => json_encode($data['examples'] ?? [], JSON_UNESCAPED_UNICODE),
        'questions_json' => json_encode($data['questions'] ?? [], JSON_UNESCAPED_UNICODE),
        'tasks_json' => json_encode($data['tasks'] ?? [], JSON_UNESCAPED_UNICODE),
        'skills_json' => json_encode($data['skills'] ?? [], JSON_UNESCAPED_UNICODE),
        'order_index' => (int)($data['order_index'] ?? 0),
        'is_published' => !empty($data['is_published']) ? 1 : 0,
    ];

    $stmt = $pdo->prepare('SELECT id FROM lessons WHERE slug = ? LIMIT 1');
    $stmt->execute([$slug]);
    $existing = $stmt->fetch();

    if ($existing) {
        $update = $pdo->prepare('
            UPDATE lessons
            SET subject = ?, chapter = ?, title = ?, goal_text = ?, theory_json = ?, examples_json = ?, questions_json = ?, tasks_json = ?, skills_json = ?, order_index = ?, is_published = ?
            WHERE slug = ?
        ');
        $update->execute([
            $payload['subject'],
            $payload['chapter'],
            $payload['title'],
            $payload['goal_text'],
            $payload['theory_json'],
            $payload['examples_json'],
            $payload['questions_json'],
            $payload['tasks_json'],
            $payload['skills_json'],
            $payload['order_index'],
            $payload['is_published'],
            $slug
        ]);
    } else {
        $insert = $pdo->prepare('
            INSERT INTO lessons (subject, chapter, title, slug, order_index, is_published, goal_text, theory_json, examples_json, questions_json, tasks_json, skills_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ');
        $insert->execute([
            $payload['subject'],
            $payload['chapter'],
            $payload['title'],
            $slug,
            $payload['order_index'],
            $payload['is_published'],
            $payload['goal_text'],
            $payload['theory_json'],
            $payload['examples_json'],
            $payload['questions_json'],
            $payload['tasks_json'],
            $payload['skills_json']
        ]);
    }

    respond(['ok' => true]);
}

respond(['error' => 'Method not allowed.'], 405);
