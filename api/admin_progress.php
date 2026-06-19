<?php
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/progress_recalc.php';
session_start();

$key = $_SERVER['HTTP_X_ADMIN_KEY'] ?? ($_GET['admin_key'] ?? '');
$isAdmin = defined('ADMIN_KEY') && hash_equals(ADMIN_KEY, $key);
$teacherUser = null;
if (!$isAdmin && !empty($_SESSION['user_id'])) {
    $userStmt = $pdo->prepare('SELECT * FROM users WHERE id = ? LIMIT 1');
    $userStmt->execute([$_SESSION['user_id']]);
    $teacherUser = $userStmt->fetch();
    if (!$teacherUser || !(bool)$teacherUser['is_active'] || ($teacherUser['role'] ?? '') !== 'teacher') {
        $teacherUser = null;
    }
}
if (!$isAdmin && !$teacherUser) {
    respond(['error' => 'Tài khoản không có quyền xem tiến độ học sinh.'], 403);
}

function decode_json_array($value): array
{
    if ($value === null || $value === '') return [];
    $decoded = json_decode($value, true);
    return is_array($decoded) ? $decoded : [];
}

function scoped_lessons_for_progress(PDO $pdo, ?array $teacherUser): array
{
    $lessonStmt = $pdo->query('SELECT * FROM lessons ORDER BY subject ASC, order_index ASC, id ASC');
    $allLessons = $lessonStmt->fetchAll();
    if ($teacherUser) {
        $allowedSubjects = teacher_allowed_subjects($teacherUser);
        return array_values(array_filter($allLessons, function ($lesson) use ($allowedSubjects) {
            return in_array(trim((string)($lesson['subject'] ?? '')), $allowedSubjects, true);
        }));
    }
    return $allLessons;
}

function lesson_allowed_for_progress(array $lessons, int $lessonId): bool
{
    if ($lessonId <= 0) return false;
    foreach ($lessons as $lesson) {
        if ((int)$lesson['id'] === $lessonId) return true;
    }
    return false;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $body = json_body();
    $action = (string)($body['action'] ?? '');
    if ($action === 'recalc_progress') {
        $lessonId = (int)($body['lesson_id'] ?? 0);
        $lessons = scoped_lessons_for_progress($pdo, $teacherUser);
        if ($lessonId <= 0 && !empty($lessons)) {
            $lessonId = (int)$lessons[0]['id'];
        }
        if (!lesson_allowed_for_progress($lessons, $lessonId)) {
            respond(['error' => 'Tài khoản không có quyền cập nhật tiến độ bài học này.'], 403);
        }
        $lesson = null;
        foreach ($lessons as $item) {
            if ((int)$item['id'] === $lessonId) {
                $lesson = $item;
                break;
            }
        }
        if (!$lesson) {
            respond(['error' => 'Không tìm thấy bài học để cập nhật tiến độ.'], 404);
        }
        $result = pr_recalc_lesson_progress($pdo, $lesson, $teacherUser);
        respond([
            'ok' => true,
            'message' => "Đã cập nhật tiến độ cho {$result['updated']}/{$result['checked']} học sinh.",
            'checked' => $result['checked'],
            'updated' => $result['updated'],
            'lesson_id' => $result['lesson_id'],
        ]);
    }
    respond(['error' => 'Thao tác không hợp lệ.'], 400);
}

$lessonId = isset($_GET['lesson_id']) ? (int)$_GET['lesson_id'] : 0;

$lessons = scoped_lessons_for_progress($pdo, $teacherUser);

if ($lessonId <= 0 && !empty($lessons)) {
    $lessonId = (int)$lessons[0]['id'];
}

if ($lessonId > 0 && !lesson_allowed_for_progress($lessons, $lessonId)) {
    respond(['error' => 'Tài khoản không có quyền xem tiến độ bài học này.'], 403);
}

$studentsStmt = $pdo->query("
    SELECT id, username, full_name, class_name, is_active, last_login_at
    FROM users
    WHERE role = 'student' AND is_active = 1
    ORDER BY class_name ASC, full_name ASC, username ASC
");
$students = $studentsStmt->fetchAll();

$managedClasses = $teacherUser ? teacher_managed_classes($teacherUser) : [];
if ($teacherUser) {
    if (!$managedClasses) {
        respond([
            'error' => 'Giáo viên chưa được gán lớp phụ trách. Admin cần điền Lớp phụ trách (vd. 6A) trong cấu hình tài khoản.',
        ], 403);
    }
    $students = array_values(array_filter($students, function ($student) use ($teacherUser) {
        return teacher_can_view_student_class($teacherUser, (string)($student['class_name'] ?? ''));
    }));
}

$progressMap = [];
if ($lessonId > 0) {
    $progressStmt = $pdo->prepare('SELECT * FROM student_lesson_progress WHERE lesson_id = ?');
    $progressStmt->execute([$lessonId]);
    foreach ($progressStmt->fetchAll() as $row) {
        $progressMap[(int)$row['student_id']] = $row;
    }
}

$rows = [];
foreach ($students as $student) {
    $progress = $progressMap[(int)$student['id']] ?? null;
    $skillScores = $progress ? decode_json_array($progress['skill_scores_json']) : [];
    $status = $progress['status'] ?? 'not_started';
    $score = $progress ? (int)$progress['score'] : 0;
    $needsPractice = in_array($status, ['not_started', 'in_progress', 'needs_practice'], true) || $score < 80;

    $state = $progress ? decode_json_array($progress['state_json']) : [];
    $practiceScoreState = isset($state['practiceScore']) ? (int)$state['practiceScore'] : null;

    $rows[] = [
        'student_id' => (int)$student['id'],
        'username' => $student['username'],
        'full_name' => $student['full_name'],
        'class_name' => $student['class_name'] ?: '',
        'is_active' => (bool)$student['is_active'],
        'last_login_at' => $student['last_login_at'],
        'status' => $status,
        'score' => $score,
        'practice_score_state' => $practiceScoreState,
        'skill_scores' => $skillScores,
        'state' => $state,
        'needs_practice' => $needsPractice,
        'updated_at' => $progress['updated_at'] ?? null,
        'completed_at' => $progress['completed_at'] ?? null,
    ];
}

$classNames = [];
foreach ($students as $student) {
    $className = trim((string)($student['class_name'] ?? ''));
    if ($className !== '') {
        $classNames[$className] = true;
    }
}
$classes = array_keys($classNames);
sort($classes, SORT_NATURAL | SORT_FLAG_CASE);

respond([
    'ok' => true,
    'lesson_id' => $lessonId,
    'managed_classes' => $managedClasses,
    'classes' => $classes,
    'lessons' => array_map(function ($lesson) {
        return [
            'id' => (int)$lesson['id'],
            'subject' => $lesson['subject'],
            'chapter' => $lesson['chapter'],
            'title' => $lesson['title'],
            'slug' => $lesson['slug'],
            'skills' => decode_json_array($lesson['skills_json'] ?? ''),
        ];
    }, $lessons),
    'rows' => $rows,
]);