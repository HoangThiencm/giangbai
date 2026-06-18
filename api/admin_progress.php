<?php
require_once __DIR__ . '/helpers.php';
session_start();

$key = $_SERVER['HTTP_X_ADMIN_KEY'] ?? ($_GET['admin_key'] ?? '');
$isAdmin = defined('ADMIN_KEY') && hash_equals(ADMIN_KEY, $key);
$isTeacher = false;
if (!$isAdmin && !empty($_SESSION['user_id'])) {
    $userStmt = $pdo->prepare('SELECT role, is_active FROM users WHERE id = ? LIMIT 1');
    $userStmt->execute([$_SESSION['user_id']]);
    $user = $userStmt->fetch();
    $isTeacher = $user && (bool)$user['is_active'] && ($user['role'] ?? '') === 'teacher';
}
if (!$isAdmin && !$isTeacher) {
    respond(['error' => 'Tài khoản không có quyền xem tiến độ học sinh.'], 403);
}

function decode_json_array($value): array
{
    if ($value === null || $value === '') return [];
    $decoded = json_decode($value, true);
    return is_array($decoded) ? $decoded : [];
}

$lessonId = isset($_GET['lesson_id']) ? (int)$_GET['lesson_id'] : 0;

$lessonStmt = $pdo->query('SELECT * FROM lessons ORDER BY subject ASC, order_index ASC, id ASC');
$lessons = $lessonStmt->fetchAll();

if ($lessonId <= 0 && !empty($lessons)) {
    $lessonId = (int)$lessons[0]['id'];
}

$studentsStmt = $pdo->query("
    SELECT id, username, full_name, class_name, is_active, last_login_at
    FROM users
    WHERE role = 'student'
    ORDER BY class_name ASC, full_name ASC, username ASC
");
$students = $studentsStmt->fetchAll();

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

    $rows[] = [
        'student_id' => (int)$student['id'],
        'username' => $student['username'],
        'full_name' => $student['full_name'],
        'class_name' => $student['class_name'] ?: '',
        'is_active' => (bool)$student['is_active'],
        'last_login_at' => $student['last_login_at'],
        'status' => $status,
        'score' => $score,
        'skill_scores' => $skillScores,
        'needs_practice' => $needsPractice,
        'updated_at' => $progress['updated_at'] ?? null,
        'completed_at' => $progress['completed_at'] ?? null,
    ];
}

respond([
    'ok' => true,
    'lesson_id' => $lessonId,
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
