<?php
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/google_drive.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

set_exception_handler(function (Throwable $e) {
    $payload = ['error' => 'Có lỗi khi xử lý bài tập nộp giáo viên.'];
    if (defined('APP_DEBUG') && APP_DEBUG) {
        $payload['detail'] = $e->getMessage();
    }
    respond($payload, 500);
});

function lsp_files_from_input($source): array
{
    if (!$source) return [];
    if (!is_array($source['name'])) return [$source];
    $files = [];
    foreach ($source['name'] as $index => $name) {
        $files[] = [
            'name' => $name,
            'type' => $source['type'][$index] ?? '',
            'tmp_name' => $source['tmp_name'][$index] ?? '',
            'error' => $source['error'][$index] ?? UPLOAD_ERR_NO_FILE,
            'size' => $source['size'][$index] ?? 0,
        ];
    }
    return $files;
}

function lsp_schema(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS lesson_self_practice_submissions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        lesson_id INT NOT NULL,
        student_id INT NOT NULL,
        item_index INT NOT NULL DEFAULT 0,
        item_title VARCHAR(220) DEFAULT NULL,
        note TEXT DEFAULT NULL,
        submitted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_lsp_submissions_lesson (lesson_id),
        INDEX idx_lsp_submissions_student (student_id),
        INDEX idx_lsp_submissions_lesson_student (lesson_id, student_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    $pdo->exec("CREATE TABLE IF NOT EXISTS lesson_self_practice_files (
        id INT AUTO_INCREMENT PRIMARY KEY,
        submission_id INT NOT NULL,
        drive_file_id VARCHAR(160) NOT NULL,
        original_name VARCHAR(255) NOT NULL,
        stored_name VARCHAR(255) NOT NULL,
        mime_type VARCHAR(160) DEFAULT NULL,
        size_bytes BIGINT NOT NULL DEFAULT 0,
        view_url TEXT NOT NULL,
        download_url TEXT DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_lsp_files_submission (submission_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    try {
        if (!column_exists($pdo, 'lessons', 'self_practice_json')) {
            $pdo->exec('ALTER TABLE lessons ADD COLUMN self_practice_json LONGTEXT DEFAULT NULL');
        }
        if (!column_exists($pdo, 'lessons', 'self_practice_drive_folder_id')) {
            $pdo->exec('ALTER TABLE lessons ADD COLUMN self_practice_drive_folder_id VARCHAR(160) DEFAULT NULL');
        }
    } catch (Throwable $e) {
        // Schema upgrade may be deferred on restricted hosting.
    }
}

function column_exists(PDO $pdo, string $table, string $column): bool
{
    try {
        $safeTable = preg_replace('/[^a-zA-Z0-9_]/', '', $table);
        $stmt = $pdo->query("SHOW COLUMNS FROM `{$safeTable}` LIKE " . $pdo->quote($column));
        return (bool)$stmt->fetch();
    } catch (Throwable $e) {
        return false;
    }
}

function lsp_current_user(PDO $pdo): array
{
    if (empty($_SESSION['user_id'])) {
        respond(['error' => 'Chưa đăng nhập.'], 401);
    }
    $stmt = $pdo->prepare('SELECT * FROM users WHERE id = ? LIMIT 1');
    $stmt->execute([$_SESSION['user_id']]);
    $user = $stmt->fetch();
    if (!$user || !(bool)$user['is_active']) {
        respond(['error' => 'Tài khoản không còn hoạt động.'], 403);
    }
    return $user;
}

function lsp_lesson_by_id(PDO $pdo, int $lessonId): ?array
{
    $stmt = $pdo->prepare('SELECT * FROM lessons WHERE id = ? LIMIT 1');
    $stmt->execute([$lessonId]);
    $row = $stmt->fetch();
    return $row ?: null;
}

function lsp_parse_items(?string $json): array
{
    if ($json === null || $json === '') return [];
    $decoded = json_decode($json, true);
    return is_array($decoded) ? $decoded : [];
}

function lsp_submission_row(array $row, array $files = []): array
{
    return [
        'id' => (int)$row['id'],
        'lesson_id' => (int)$row['lesson_id'],
        'student_id' => (int)$row['student_id'],
        'student_name' => (string)($row['student_name'] ?? ''),
        'class_name' => (string)($row['class_name'] ?? ''),
        'item_index' => (int)$row['item_index'],
        'item_title' => (string)($row['item_title'] ?? ''),
        'note' => (string)($row['note'] ?? ''),
        'submitted_at' => (string)$row['submitted_at'],
        'files' => $files,
    ];
}

function lsp_files_for_submissions(PDO $pdo, array $submissionIds): array
{
    if (!$submissionIds) return [];
    $placeholders = implode(',', array_fill(0, count($submissionIds), '?'));
    $stmt = $pdo->prepare("SELECT * FROM lesson_self_practice_files WHERE submission_id IN ($placeholders) ORDER BY id ASC");
    $stmt->execute($submissionIds);
    $rows = $stmt->fetchAll();
    $map = [];
    foreach ($rows as $row) {
        $sid = (int)$row['submission_id'];
        if (!isset($map[$sid])) $map[$sid] = [];
        $map[$sid][] = [
            'id' => (int)$row['id'],
            'original_name' => (string)$row['original_name'],
            'stored_name' => (string)$row['stored_name'],
            'mime_type' => (string)($row['mime_type'] ?? ''),
            'size_bytes' => (int)$row['size_bytes'],
            'view_url' => (string)$row['view_url'],
            'download_url' => (string)($row['download_url'] ?? ''),
        ];
    }
    return $map;
}

function lsp_ensure_lesson_folder(PDO $pdo, array $lesson): string
{
    $folderId = trim((string)($lesson['self_practice_drive_folder_id'] ?? ''));
    if ($folderId !== '') return $folderId;

    $folderId = drive_lotrinh_self_practice_folder(
        (string)($lesson['subject'] ?? 'Lop trinh'),
        (string)($lesson['title'] ?? 'Bai hoc'),
        (int)$lesson['id']
    );
    $pdo->prepare('UPDATE lessons SET self_practice_drive_folder_id = ? WHERE id = ?')
        ->execute([$folderId, (int)$lesson['id']]);
    return $folderId;
}

if (!schema_is_ready('lesson_self_practice', '20260624-v1')) {
    lsp_schema($pdo);
    schema_mark_ready('lesson_self_practice', '20260624-v1');
}

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$action = trim((string)($_GET['action'] ?? $_POST['action'] ?? 'list'));

if ($method === 'GET' && $action === 'list') {
    $user = lsp_current_user($pdo);
    $lessonId = (int)($_GET['lesson_id'] ?? 0);
    if ($lessonId <= 0) respond(['error' => 'Thiếu lesson_id.'], 422);

    $lesson = lsp_lesson_by_id($pdo, $lessonId);
    if (!$lesson) respond(['error' => 'Không tìm thấy bài học.'], 404);

    $role = (string)($user['role'] ?? '');
    $isTeacher = in_array($role, ['teacher', 'admin'], true);

    if ($isTeacher) {
        $stmt = $pdo->prepare("SELECT s.*, u.full_name AS student_name, u.class_name
            FROM lesson_self_practice_submissions s
            LEFT JOIN users u ON u.id = s.student_id
            WHERE s.lesson_id = ?
            ORDER BY s.submitted_at DESC, s.id DESC");
        $stmt->execute([$lessonId]);
        $rows = $stmt->fetchAll();
        if ($role === 'teacher') {
            $rows = array_values(array_filter($rows, function ($row) use ($user) {
                return teacher_can_view_student_class($user, (string)($row['class_name'] ?? ''));
            }));
        }
        $ids = array_map(fn($row) => (int)$row['id'], $rows);
        $fileMap = lsp_files_for_submissions($pdo, $ids);
        $submissions = array_map(fn($row) => lsp_submission_row($row, $fileMap[(int)$row['id']] ?? []), $rows);
        respond([
            'ok' => true,
            'lesson_id' => $lessonId,
            'items' => lsp_parse_items($lesson['self_practice_json'] ?? null),
            'submissions' => $submissions,
            'role' => 'teacher',
        ]);
    }

    if ($role !== 'student') {
        respond(['error' => 'Chỉ học sinh hoặc giáo viên mới xem được bài nộp.'], 403);
    }

    $stmt = $pdo->prepare("SELECT s.*
        FROM lesson_self_practice_submissions s
        WHERE s.lesson_id = ? AND s.student_id = ?
        ORDER BY s.submitted_at DESC, s.id DESC");
    $stmt->execute([$lessonId, (int)$user['id']]);
    $rows = $stmt->fetchAll();
    $ids = array_map(fn($row) => (int)$row['id'], $rows);
    $fileMap = lsp_files_for_submissions($pdo, $ids);
    $submissions = array_map(function ($row) use ($user, $fileMap) {
        $row['student_name'] = (string)($user['full_name'] ?? $user['username'] ?? '');
        $row['class_name'] = (string)($user['class_name'] ?? '');
        return lsp_submission_row($row, $fileMap[(int)$row['id']] ?? []);
    }, $rows);

    respond([
        'ok' => true,
        'lesson_id' => $lessonId,
        'items' => lsp_parse_items($lesson['self_practice_json'] ?? null),
        'submissions' => $submissions,
        'role' => 'student',
    ]);
}

if ($method === 'POST' && $action === 'submit') {
    $user = lsp_current_user($pdo);
    if ((string)($user['role'] ?? '') !== 'student') {
        respond(['error' => 'Chỉ học sinh mới nộp bài tập.'], 403);
    }

    $lessonId = (int)($_POST['lesson_id'] ?? 0);
    $itemIndex = (int)($_POST['item_index'] ?? -1);
    $note = trim((string)($_POST['note'] ?? ''));
    if ($lessonId <= 0) respond(['error' => 'Thiếu lesson_id.'], 422);

    $lesson = lsp_lesson_by_id($pdo, $lessonId);
    if (!$lesson) respond(['error' => 'Không tìm thấy bài học.'], 404);
    if (!(bool)($lesson['is_published'] ?? 0)) {
        respond(['error' => 'Bài học chưa mở cho học sinh.'], 403);
    }

    $items = lsp_parse_items($lesson['self_practice_json'] ?? null);
    if (!$items) respond(['error' => 'Bài học chưa có bài tập nộp giáo viên.'], 422);

    if ($itemIndex !== -1) {
        respond(['error' => 'Chỉ nộp chung một lần cho cả bài học.'], 422);
    }

    $itemTitle = 'Bài tập nộp giáo viên';

    $dupStmt = $pdo->prepare('SELECT id FROM lesson_self_practice_submissions WHERE lesson_id = ? AND student_id = ? AND item_index = -1 LIMIT 1');
    $dupStmt->execute([$lessonId, (int)$user['id']]);
    if ($dupStmt->fetch()) {
        respond(['error' => 'Em đã nộp bài cho bài học này.'], 422);
    }

    $files = array_values(array_filter(
        lsp_files_from_input($_FILES['files'] ?? null),
        fn($file) => (int)($file['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_NO_FILE
    ));
    if (!$files) respond(['error' => 'Vui lòng chọn ít nhất một tệp đính kèm.'], 422);

    $maxFiles = 10;
    $maxBytes = 25 * 1024 * 1024;
    $allowed = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'zip', 'rar', 'txt'];
    if (count($files) > $maxFiles) respond(['error' => "Tối đa {$maxFiles} tệp mỗi lần nộp."], 422);

    foreach ($files as $file) {
        if ((int)$file['error'] !== UPLOAD_ERR_OK) {
            respond(['error' => 'Một tệp tải lên bị lỗi (mã ' . (int)$file['error'] . ').'], 422);
        }
        if ((int)$file['size'] < 1 || (int)$file['size'] > $maxBytes) {
            respond(['error' => 'Tệp ' . $file['name'] . ' vượt giới hạn 25 MB.'], 422);
        }
        $extension = strtolower(pathinfo((string)$file['name'], PATHINFO_EXTENSION));
        if ($extension === '' || !in_array($extension, $allowed, true)) {
            respond(['error' => 'Không cho phép loại tệp .' . $extension . '.'], 422);
        }
        if (!is_uploaded_file($file['tmp_name'])) {
            respond(['error' => 'Tệp tải lên không hợp lệ.'], 422);
        }
    }

    $studentName = trim((string)($user['full_name'] ?? $user['username'] ?? 'Hoc sinh'));
    $className = trim((string)($user['class_name'] ?? ''));
    $identifier = (string)(int)$user['id'];

    $lessonFolder = lsp_ensure_lesson_folder($pdo, $lesson);
    $studentFolder = drive_participant_folder($lessonFolder, $className, $studentName, $identifier);

    $uploaded = [];
    foreach ($files as $index => $file) {
        $original = (string)$file['name'];
        $fieldKey = 'bai-nop';
        $storedName = drive_submission_stored_name($className, $studentName, $identifier, $index + 1, $original, $fieldKey);
        $invalid = drive_validate_upload($file['tmp_name'], $original);
        if ($invalid) respond(['error' => $invalid], 422);
        $mime = drive_detect_mime($file['tmp_name'], $original, (string)($file['type'] ?? ''));
        $drive = drive_upload_file($studentFolder, $storedName, $mime, $file['tmp_name']);
        $uploaded[] = [
            'drive_file_id' => $drive['file_id'],
            'original_name' => $original,
            'stored_name' => $drive['stored_name'],
            'mime_type' => $drive['mime_type'] ?? $mime,
            'size_bytes' => (int)$file['size'],
            'view_url' => $drive['view_url'],
            'download_url' => $drive['download_url'],
        ];
    }

    $pdo->beginTransaction();
    try {
        $stmt = $pdo->prepare('INSERT INTO lesson_self_practice_submissions (lesson_id, student_id, item_index, item_title, note) VALUES (?, ?, ?, ?, ?)');
        $stmt->execute([$lessonId, (int)$user['id'], $itemIndex, $itemTitle, $note !== '' ? $note : null]);
        $submissionId = (int)$pdo->lastInsertId();
        $fileStmt = $pdo->prepare('INSERT INTO lesson_self_practice_files (submission_id, drive_file_id, original_name, stored_name, mime_type, size_bytes, view_url, download_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
        foreach ($uploaded as $file) {
            $fileStmt->execute([
                $submissionId,
                $file['drive_file_id'],
                $file['original_name'],
                $file['stored_name'],
                $file['mime_type'],
                $file['size_bytes'],
                $file['view_url'],
                $file['download_url'],
            ]);
        }
        $pdo->commit();
    } catch (Throwable $e) {
        if ($pdo->inTransaction()) $pdo->rollBack();
        throw $e;
    }

    respond([
        'ok' => true,
        'submission_id' => $submissionId,
        'submitted_at' => date('c'),
        'file_count' => count($uploaded),
        'message' => 'Đã nộp bài tập lên Google Drive.',
    ]);
}

respond(['error' => 'Endpoint không tồn tại.'], 404);