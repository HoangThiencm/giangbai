<?php
require_once __DIR__ . '/helpers.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

set_exception_handler(function (Throwable $e) {
    $payload = ['error' => 'Lỗi server khi tải lộ trình.'];
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

function column_exists(PDO $pdo, string $table, string $column): bool
{
    try {
        $safeTable = preg_replace('/[^a-zA-Z0-9_]/', '', $table);
        $safeColumn = preg_replace('/[^a-zA-Z0-9_]/', '', $column);
        if ($safeTable === '' || $safeColumn === '') return false;
        $stmt = $pdo->query("SHOW COLUMNS FROM `{$safeTable}` LIKE " . $pdo->quote($safeColumn));
        return (bool)$stmt->fetch();
    } catch (Throwable $e) {
        return false;
    }
}

function lesson_row_to_payload(array $row): array
{
    return [
        'id' => (int)$row['id'],
        'subject' => $row['subject'] ?? 'Toán 6',
        'chapter' => $row['chapter'] ?? '',
        'title' => $row['title'] ?? 'Bài học',
        'slug' => $row['slug'] ?? '',
        'order_index' => (int)($row['order_index'] ?? 0),
        'is_published' => (bool)($row['is_published'] ?? 0),
        'goal' => $row['goal_text'] ?? '',
        'theory' => parse_json_or_default($row['theory_json'] ?? null, []),
        'examples' => parse_json_or_default($row['examples_json'] ?? null, []),
        'self_practice' => parse_json_or_default($row['self_practice_json'] ?? null, []),
        'questions' => parse_json_or_default($row['questions_json'] ?? null, []),
        'essay_exercises' => parse_json_or_default($row['essay_json'] ?? null, []),
        'fill_exercises' => parse_json_or_default($row['fill_json'] ?? null, []),
        'drag_exercises' => parse_json_or_default($row['drag_json'] ?? null, []),
        'videos' => parse_json_or_default($row['videos_json'] ?? null, []),
        'tasks' => parse_json_or_default($row['tasks_json'] ?? null, []),
        'skills' => parse_json_or_default($row['skills_json'] ?? null, []),
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

function current_session_user(PDO $pdo): ?array
{
    if (empty($_SESSION['user_id'])) return null;
    $stmt = $pdo->prepare('SELECT * FROM users WHERE id = ? LIMIT 1');
    $stmt->execute([$_SESSION['user_id']]);
    $user = $stmt->fetch();
    if (!$user || !(bool)$user['is_active']) return null;
    return $user;
}

function ensure_lesson_schema(PDO $pdo): void
{
    try {
        $pdo->exec("CREATE TABLE IF NOT EXISTS lessons (
            id INT AUTO_INCREMENT PRIMARY KEY,
            subject VARCHAR(80) NOT NULL,
            chapter VARCHAR(160) NOT NULL,
            title VARCHAR(180) NOT NULL,
            slug VARCHAR(120) NOT NULL UNIQUE,
            order_index INT NOT NULL DEFAULT 0,
            is_published TINYINT(1) NOT NULL DEFAULT 0,
            goal_text TEXT DEFAULT NULL,
            theory_json LONGTEXT DEFAULT NULL,
            examples_json LONGTEXT DEFAULT NULL,
            questions_json LONGTEXT DEFAULT NULL,
            essay_json LONGTEXT DEFAULT NULL,
            fill_json LONGTEXT DEFAULT NULL,
            drag_json LONGTEXT DEFAULT NULL,
            videos_json LONGTEXT DEFAULT NULL,
            tasks_json LONGTEXT DEFAULT NULL,
            skills_json LONGTEXT DEFAULT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

        $columns = [
            'goal_text TEXT DEFAULT NULL',
            'theory_json LONGTEXT DEFAULT NULL',
            'examples_json LONGTEXT DEFAULT NULL',
            'self_practice_json LONGTEXT DEFAULT NULL',
            'self_practice_drive_folder_id VARCHAR(160) DEFAULT NULL',
            'questions_json LONGTEXT DEFAULT NULL',
            'essay_json LONGTEXT DEFAULT NULL',
            'fill_json LONGTEXT DEFAULT NULL',
            'drag_json LONGTEXT DEFAULT NULL',
            'videos_json LONGTEXT DEFAULT NULL',
            'tasks_json LONGTEXT DEFAULT NULL',
            'skills_json LONGTEXT DEFAULT NULL'
        ];
        foreach ($columns as $definition) {
            $name = trim(strtok($definition, ' '));
            if (!column_exists($pdo, 'lessons', $name)) {
                $pdo->exec("ALTER TABLE lessons ADD COLUMN $definition");
            }
        }
    } catch (Throwable $e) {
        // Student pages should still load if schema migration must be run from admin/setup.
    }
}

ensure_lesson_schema($pdo);

function ensure_progress_schema(PDO $pdo): void
{
    try {
        $pdo->exec("CREATE TABLE IF NOT EXISTS student_lesson_progress (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            lesson_id INT NOT NULL,
            status ENUM('not_started', 'in_progress', 'needs_practice', 'mastered') NOT NULL DEFAULT 'not_started',
            score INT NOT NULL DEFAULT 0,
            skill_scores_json TEXT DEFAULT NULL,
            state_json TEXT DEFAULT NULL,
            started_at DATETIME DEFAULT NULL,
            completed_at DATETIME DEFAULT NULL,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE KEY uniq_student_lesson (student_id, lesson_id)
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    } catch (Throwable $e) {
        // Table creation may fail if DB credentials are wrong; student pages still load.
    }

    // Each column migration runs independently so one failure does not block others
    $columns = [
        'skill_scores_json TEXT DEFAULT NULL',
        'state_json TEXT DEFAULT NULL',
        'started_at DATETIME DEFAULT NULL',
        'completed_at DATETIME DEFAULT NULL'
    ];
    foreach ($columns as $definition) {
        try {
            $name = trim(strtok($definition, ' '));
            if (!column_exists($pdo, 'student_lesson_progress', $name)) {
                $pdo->exec("ALTER TABLE student_lesson_progress ADD COLUMN $definition");
            }
        } catch (Throwable $e) {
            // Column may already exist or table not ready yet; continue with next column
        }
    }
}

ensure_progress_schema($pdo);

$method = $_SERVER['REQUEST_METHOD'];
$requestData = $method === 'POST' ? json_body() : [];
$action = $_GET['action'] ?? ($_POST['action'] ?? ($requestData['action'] ?? ''));
$adminKey = $_SERVER['HTTP_X_ADMIN_KEY'] ?? ($_GET['admin_key'] ?? '');
$isAdmin = defined('ADMIN_KEY') && hash_equals(ADMIN_KEY, $adminKey);
$sessionUser = current_session_user($pdo);
$canManageLessons = $isAdmin || (($sessionUser['role'] ?? '') === 'teacher');

if ($method === 'GET' && $canManageLessons && !empty($_GET['admin'])) {
    $stmt = $pdo->query('SELECT * FROM lessons ORDER BY order_index ASC, id ASC');
    respond(['ok' => true, 'lessons' => array_map('lesson_row_to_payload', $stmt->fetchAll())]);
}

if ($method === 'GET') {
    $user = ensure_login();
    if (!table_exists($pdo, 'lessons')) {
        respond([
            'error' => 'Chưa có bảng lessons trên database.',
            'detail' => 'Chạy api/migrate_lessons.php một lần để tạo bảng và dữ liệu mẫu.'
        ], 500);
    }
    $stmt = $pdo->query('SELECT * FROM lessons ORDER BY order_index ASC, id ASC');
    $lessons = array_map('lesson_row_to_payload', $stmt->fetchAll());
    $requestedSubject = trim((string)($_GET['subject'] ?? ''));

    if ($user['role'] === 'student') {
        $allowedSubjects = subjects_for_allowed_pages(json_decode($user['allowed_pages_json'] ?? '[]', true));
        if ($requestedSubject !== '') {
            if (!in_array($requestedSubject, $allowedSubjects, true)) {
                respond(['error' => 'Em chưa được mở lộ trình ' . $requestedSubject . '.'], 403);
            }
            $lessons = array_values(array_filter(
                $lessons,
                fn($lesson) => trim((string)($lesson['subject'] ?? '')) === $requestedSubject
            ));
        } elseif ($allowedSubjects) {
            $lessons = array_values(array_filter(
                $lessons,
                fn($lesson) => in_array(trim((string)($lesson['subject'] ?? '')), $allowedSubjects, true)
            ));
        }
        $lessons = array_values(array_filter($lessons, fn($lesson) => $lesson['is_published']));
    }

    $progressMap = [];
    if (table_exists($pdo, 'student_lesson_progress')) {
        $progressStmt = $pdo->prepare('SELECT * FROM student_lesson_progress WHERE student_id = ?');
        $progressStmt->execute([$user['id']]);
        foreach ($progressStmt->fetchAll() as $row) {
            $progressMap[(int)$row['lesson_id']] = [
                'status' => $row['status'] ?? 'not_started',
                'score' => (int)($row['score'] ?? 0),
                'skillScores' => parse_json_or_default($row['skill_scores_json'] ?? null, []),
                'state' => parse_json_or_default($row['state_json'] ?? null, []),
                'startedAt' => $row['started_at'] ?? null,
                'completedAt' => $row['completed_at'] ?? null,
            ];
        }
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
    $data = $requestData;
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

    $startedAt = mysql_datetime_or_null($data['started_at'] ?? null);
    $completedAt = mysql_datetime_or_null($data['completed_at'] ?? null);

    $stmt = $pdo->prepare('SELECT id FROM student_lesson_progress WHERE student_id = ? AND lesson_id = ? LIMIT 1');
    $stmt->execute([$user['id'], $lessonId]);
    $exists = $stmt->fetch();

    if ($exists) {
        $update = $pdo->prepare('
            UPDATE student_lesson_progress
            SET status = ?, score = ?, skill_scores_json = ?, state_json = ?, started_at = COALESCE(?, started_at), completed_at = ?
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
    $data = $requestData;
    $lessonId = (int)($data['lesson_id'] ?? 0);
    if ($lessonId <= 0) respond(['error' => 'Thiếu lesson_id.'], 422);

    $stmt = $pdo->prepare('DELETE FROM student_lesson_progress WHERE student_id = ? AND lesson_id = ?');
    $stmt->execute([$user['id'], $lessonId]);
    respond(['ok' => true]);
}

function find_lesson_by_id_or_slug(PDO $pdo, int $id, string $slug): ?array
{
    if ($id > 0) {
        $stmt = $pdo->prepare('SELECT * FROM lessons WHERE id = ? LIMIT 1');
        $stmt->execute([$id]);
        $row = $stmt->fetch();
        if ($row) return $row;
    }
    if ($slug !== '') {
        $stmt = $pdo->prepare('SELECT * FROM lessons WHERE slug = ? LIMIT 1');
        $stmt->execute([$slug]);
        $row = $stmt->fetch();
        if ($row) return $row;
    }
    return null;
}

function unique_lesson_slug(PDO $pdo, string $baseSlug): string
{
    $baseSlug = trim($baseSlug);
    if ($baseSlug === '') $baseSlug = 'bai-hoc';
    $candidate = $baseSlug;
    $suffix = 2;
    while (true) {
        $stmt = $pdo->prepare('SELECT id FROM lessons WHERE slug = ? LIMIT 1');
        $stmt->execute([$candidate]);
        if (!$stmt->fetch()) return $candidate;
        $candidate = $baseSlug . '-copy' . ($suffix > 2 ? '-' . $suffix : '');
        $suffix++;
        if ($suffix > 50) {
            return $baseSlug . '-' . time();
        }
    }
}

if ($method === 'POST' && $action === 'save_content') {
    $data = $requestData;
    require_lesson_manager($isAdmin, $sessionUser, trim($data['subject'] ?? 'Toán 6'));
    $lessonId = (int)($data['id'] ?? 0);
    $slug = trim($data['slug'] ?? '');
    if ($slug === '') respond(['error' => 'Thiếu slug.'], 422);

    $payload = [
        'subject' => trim($data['subject'] ?? 'Toán 6'),
        'chapter' => trim($data['chapter'] ?? ''),
        'title' => trim($data['title'] ?? ''),
        'goal_text' => trim($data['goal_text'] ?? ''),
        'theory_json' => json_encode($data['theory'] ?? [], JSON_UNESCAPED_UNICODE),
        'examples_json' => json_encode($data['examples'] ?? [], JSON_UNESCAPED_UNICODE),
        'self_practice_json' => json_encode($data['self_practice'] ?? [], JSON_UNESCAPED_UNICODE),
        'questions_json' => json_encode($data['questions'] ?? [], JSON_UNESCAPED_UNICODE),
        'essay_json' => json_encode($data['essay_exercises'] ?? [], JSON_UNESCAPED_UNICODE),
        'fill_json' => json_encode($data['fill_exercises'] ?? [], JSON_UNESCAPED_UNICODE),
        'drag_json' => json_encode($data['drag_exercises'] ?? [], JSON_UNESCAPED_UNICODE),
        'videos_json' => json_encode($data['videos'] ?? [], JSON_UNESCAPED_UNICODE),
        'tasks_json' => json_encode($data['tasks'] ?? [], JSON_UNESCAPED_UNICODE),
        'skills_json' => json_encode($data['skills'] ?? [], JSON_UNESCAPED_UNICODE),
        'order_index' => (int)($data['order_index'] ?? 0),
        'is_published' => !empty($data['is_published']) ? 1 : 0,
    ];

    $existing = find_lesson_by_id_or_slug($pdo, $lessonId, '');

    if ($existing) {
        $conflict = $pdo->prepare('SELECT id FROM lessons WHERE slug = ? AND id != ? LIMIT 1');
        $conflict->execute([$slug, (int)$existing['id']]);
        if ($conflict->fetch()) {
            respond(['error' => 'Slug đã được bài khác sử dụng.'], 422);
        }
        $update = $pdo->prepare('
            UPDATE lessons
            SET subject = ?, chapter = ?, title = ?, slug = ?, goal_text = ?, theory_json = ?, examples_json = ?, self_practice_json = ?, questions_json = ?, essay_json = ?, fill_json = ?, drag_json = ?, videos_json = ?, tasks_json = ?, skills_json = ?, order_index = ?, is_published = ?
            WHERE id = ?
        ');
        $update->execute([
            $payload['subject'],
            $payload['chapter'],
            $payload['title'],
            $slug,
            $payload['goal_text'],
            $payload['theory_json'],
            $payload['examples_json'],
            $payload['self_practice_json'],
            $payload['questions_json'],
            $payload['essay_json'],
            $payload['fill_json'],
            $payload['drag_json'],
            $payload['videos_json'],
            $payload['tasks_json'],
            $payload['skills_json'],
            $payload['order_index'],
            $payload['is_published'],
            (int)$existing['id']
        ]);
        respond(['ok' => true, 'id' => (int)$existing['id'], 'slug' => $slug]);
    }

    $stmt = $pdo->prepare('SELECT id FROM lessons WHERE slug = ? LIMIT 1');
    $stmt->execute([$slug]);
    $existingBySlug = $stmt->fetch();

    if ($existingBySlug) {
        $update = $pdo->prepare('
            UPDATE lessons
            SET subject = ?, chapter = ?, title = ?, goal_text = ?, theory_json = ?, examples_json = ?, self_practice_json = ?, questions_json = ?, essay_json = ?, fill_json = ?, drag_json = ?, videos_json = ?, tasks_json = ?, skills_json = ?, order_index = ?, is_published = ?
            WHERE slug = ?
        ');
        $update->execute([
            $payload['subject'],
            $payload['chapter'],
            $payload['title'],
            $payload['goal_text'],
            $payload['theory_json'],
            $payload['examples_json'],
            $payload['self_practice_json'],
            $payload['questions_json'],
            $payload['essay_json'],
            $payload['fill_json'],
            $payload['drag_json'],
            $payload['videos_json'],
            $payload['tasks_json'],
            $payload['skills_json'],
            $payload['order_index'],
            $payload['is_published'],
            $slug
        ]);
        respond(['ok' => true, 'id' => (int)$existingBySlug['id'], 'slug' => $slug]);
    }

    $insert = $pdo->prepare('
        INSERT INTO lessons (subject, chapter, title, slug, order_index, is_published, goal_text, theory_json, examples_json, self_practice_json, questions_json, essay_json, fill_json, drag_json, videos_json, tasks_json, skills_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        $payload['self_practice_json'],
        $payload['questions_json'],
        $payload['essay_json'],
        $payload['fill_json'],
        $payload['drag_json'],
        $payload['videos_json'],
        $payload['tasks_json'],
        $payload['skills_json']
    ]);
    respond(['ok' => true, 'id' => (int)$pdo->lastInsertId(), 'slug' => $slug]);
}

if ($method === 'POST' && $action === 'delete_lesson') {
    $data = $requestData;
    $lessonId = (int)($data['id'] ?? 0);
    $slug = trim($data['slug'] ?? '');
    $lesson = find_lesson_by_id_or_slug($pdo, $lessonId, $slug);
    if (!$lesson) respond(['error' => 'Không tìm thấy bài học.'], 404);
    require_lesson_manager($isAdmin, $sessionUser, trim($lesson['subject'] ?? ''));

    $id = (int)$lesson['id'];
    if (table_exists($pdo, 'student_lesson_progress')) {
        $pdo->prepare('DELETE FROM student_lesson_progress WHERE lesson_id = ?')->execute([$id]);
    }
    $pdo->prepare('DELETE FROM lessons WHERE id = ?')->execute([$id]);
    respond(['ok' => true, 'deleted_id' => $id]);
}

if ($method === 'POST' && $action === 'duplicate_lesson') {
    $data = $requestData;
    $lessonId = (int)($data['id'] ?? 0);
    $slug = trim($data['slug'] ?? '');
    $lesson = find_lesson_by_id_or_slug($pdo, $lessonId, $slug);
    if (!$lesson) respond(['error' => 'Không tìm thấy bài học.'], 404);
    require_lesson_manager($isAdmin, $sessionUser, trim($lesson['subject'] ?? ''));

    $newSlug = unique_lesson_slug($pdo, $lesson['slug'] . '-copy');
    $newTitle = trim($lesson['title'] ?? 'Bài học');
    if (!preg_match('/\(bản sao\)$/iu', $newTitle)) {
        $newTitle .= ' (bản sao)';
    }
    $orderStmt = $pdo->prepare('SELECT COALESCE(MAX(order_index), 0) + 1 FROM lessons WHERE subject = ?');
    $orderStmt->execute([$lesson['subject']]);
    $nextOrder = (int)$orderStmt->fetchColumn();

    $insert = $pdo->prepare('
        INSERT INTO lessons (subject, chapter, title, slug, order_index, is_published, goal_text, theory_json, examples_json, self_practice_json, questions_json, essay_json, fill_json, drag_json, videos_json, tasks_json, skills_json)
        VALUES (?, ?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ');
    $insert->execute([
        $lesson['subject'],
        $lesson['chapter'],
        $newTitle,
        $newSlug,
        $nextOrder,
        $lesson['goal_text'] ?? '',
        $lesson['theory_json'] ?? '[]',
        $lesson['examples_json'] ?? '[]',
        $lesson['self_practice_json'] ?? '[]',
        $lesson['questions_json'] ?? '[]',
        $lesson['essay_json'] ?? '[]',
        $lesson['fill_json'] ?? '[]',
        $lesson['drag_json'] ?? '[]',
        $lesson['videos_json'] ?? '[]',
        $lesson['tasks_json'] ?? '[]',
        $lesson['skills_json'] ?? '[]'
    ]);

    respond([
        'ok' => true,
        'id' => (int)$pdo->lastInsertId(),
        'slug' => $newSlug,
        'title' => $newTitle
    ]);
}

if ($method === 'POST' && $action === 'rename_chapter') {
    $data = $requestData;
    $subject = trim($data['subject'] ?? '');
    require_lesson_manager($isAdmin, $sessionUser, $subject);
    $oldChapter = trim($data['old_chapter'] ?? '');
    $newChapter = trim($data['new_chapter'] ?? '');
    if ($subject === '' || $oldChapter === '' || $newChapter === '') {
        respond(['error' => 'Cần môn học, tên chương cũ và tên chương mới.'], 422);
    }
    if ($oldChapter === $newChapter) {
        respond(['ok' => true, 'updated' => 0]);
    }

    $update = $pdo->prepare('UPDATE lessons SET chapter = ? WHERE subject = ? AND chapter = ?');
    $update->execute([$newChapter, $subject, $oldChapter]);
    respond(['ok' => true, 'updated' => $update->rowCount()]);
}

respond(['error' => 'Method not allowed.'], 405);
