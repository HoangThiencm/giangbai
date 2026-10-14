<?php
require_once __DIR__ . '/helpers.php';

header('Cache-Control: no-store, no-cache, must-revalidate, private');
header('Pragma: no-cache');
header('Vary: Cookie');

function sodiem_teacher(PDO $pdo): array {
    if (empty($_SESSION['user_id'])) respond(['error' => 'Cần đăng nhập tài khoản giáo viên.'], 401);
    $stmt = $pdo->prepare("SELECT id, role, class_name FROM users WHERE id = ? AND role IN ('teacher', 'admin') AND is_active = 1 LIMIT 1");
    $stmt->execute([(int)$_SESSION['user_id']]);
    $teacher = $stmt->fetch();
    if (!$teacher) respond(['error' => 'Cần đăng nhập tài khoản giáo viên.'], 401);
    return $teacher;
}

function ensure_gradebook_schema(PDO $pdo): void {
    $pdo->exec("CREATE TABLE IF NOT EXISTS gradebooks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        teacher_id INT NOT NULL,
        class_name VARCHAR(80) NOT NULL,
        subject VARCHAR(80) NOT NULL,
        academic_year VARCHAR(30) NOT NULL DEFAULT '2025-2026',
        columns_config_json TEXT DEFAULT NULL,
        students_data_json LONGTEXT DEFAULT NULL,
        history_log_json LONGTEXT DEFAULT NULL,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_teacher_class_sub (teacher_id, class_name, subject, academic_year),
        INDEX idx_gradebooks_class (class_name)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    sodiem_ensure_owner_unique($pdo);
}

function sodiem_unique_indexes(PDO $pdo): array {
    $indexes = [];
    foreach ($pdo->query('SHOW INDEX FROM gradebooks')->fetchAll() as $row) {
        $name = (string)($row['Key_name'] ?? '');
        if ($name === '' || $name === 'PRIMARY' || (int)($row['Non_unique'] ?? 1) === 1) continue;
        $indexes[$name][(int)($row['Seq_in_index'] ?? 0)] = (string)($row['Column_name'] ?? '');
    }
    $ordered = [];
    foreach ($indexes as $name => $columns) {
        ksort($columns);
        $ordered[$name] = array_values($columns);
    }
    return $ordered;
}

function sodiem_drop_shared_unique(PDO $pdo): void {
    $wanted = ['teacher_id', 'class_name', 'subject', 'academic_year'];
    foreach (sodiem_unique_indexes($pdo) as $name => $columns) {
        if ($columns === $wanted || in_array('teacher_id', $columns, true)) continue;
        if (!preg_match('/^[A-Za-z0-9_]+$/', $name)) continue;
        $pdo->exec('ALTER TABLE gradebooks DROP INDEX `' . $name . '`');
    }
}

function sodiem_ensure_owner_unique(PDO $pdo): void {
    $wanted = ['teacher_id', 'class_name', 'subject', 'academic_year'];
    try {
        sodiem_drop_shared_unique($pdo);
    } catch (Throwable $e) {
    }
    $hasOwnerKey = false;
    foreach (sodiem_unique_indexes($pdo) as $columns) {
        if ($columns === $wanted) $hasOwnerKey = true;
    }
    if (!$hasOwnerKey) {
        try {
            $pdo->exec('ALTER TABLE gradebooks ADD UNIQUE KEY uniq_teacher_class_sub (teacher_id, class_name, subject, academic_year)');
        } catch (Throwable $e) {
        }
    }
}

function sodiem_mark_map(?string $json): array {
    $rows = json_decode((string)$json, true);
    if (!is_array($rows)) return [];
    $map = [];
    foreach ($rows as $row) {
        if (!is_array($row)) continue;
        $scoresIn = $row['scores'] ?? [];
        if (!is_array($scoresIn)) $scoresIn = [];
        $scores = [];
        foreach ($scoresIn as $column => $score) {
            if ($score === '' || $score === null) continue;
            $scores[(string)$column] = (string)$score;
        }
        ksort($scores);
        $comment = trim((string)($row['comment'] ?? ''));
        if (!$scores && $comment === '') continue;
        $name = trim((string)($row['name'] ?? $row['full_name'] ?? ''));
        if ($name === '') $name = trim((string)($row['sbd'] ?? $row['username'] ?? ''));
        if ($name === '') continue;
        $map[$name] = ['scores' => $scores, 'comment' => $comment];
    }
    ksort($map);
    return $map;
}

function sodiem_marks_are_copied(array $mine, array $other): bool {
    if (!$mine || !$other) return false;
    foreach ($mine as $key => $mark) {
        if (!isset($other[$key]) || $other[$key] != $mark) return false;
    }
    return true;
}

function sodiem_score_cells(array $map): array {
    $cells = [];
    foreach ($map as $name => $mark) {
        $scores = $mark['scores'] ?? [];
        if (!is_array($scores)) continue;
        foreach ($scores as $column => $score) {
            $cells[$name . "\0" . $column] = (string)$score;
        }
    }
    return $cells;
}

function sodiem_marks_overlap(array $mine, array $other): bool {
    if (sodiem_marks_are_copied($mine, $other)) return true;
    $left = sodiem_score_cells($mine);
    $right = sodiem_score_cells($other);
    if (!$left || !$right) return false;
    $same = 0;
    $conflict = 0;
    foreach ($left as $key => $score) {
        if (!isset($right[$key])) continue;
        if ($right[$key] === $score) $same++;
        else $conflict++;
    }
    if ($same < 8) return false;
    $compared = $same + $conflict;
    if ($compared === 0 || ($same / $compared) < 0.85) return false;
    $smaller = min(count($left), count($right));
    return $smaller > 0 && ($same / $smaller) >= 0.6;
}

function sodiem_other_mark_maps(PDO $pdo, int $teacherId, string $class, string $subject, string $year): array {
    $stmt = $pdo->prepare('SELECT id, students_data_json, updated_at FROM gradebooks WHERE class_name = ? AND subject = ? AND academic_year = ? AND teacher_id <> ?');
    $stmt->execute([$class, $subject, $year, $teacherId]);
    $books = [];
    foreach ($stmt->fetchAll() as $row) {
        $map = sodiem_mark_map($row['students_data_json'] ?? '');
        if ($map) $books[] = ['id' => (int)$row['id'], 'updated_at' => (string)($row['updated_at'] ?? ''), 'map' => $map];
    }
    return $books;
}

function sodiem_is_newer_copy(array $book, array $other): bool {
    $mineTime = strtotime((string)($book['updated_at'] ?? '')) ?: 0;
    $otherTime = strtotime((string)($other['updated_at'] ?? '')) ?: 0;
    if ($mineTime === $otherTime) return (int)($book['id'] ?? 0) > (int)($other['id'] ?? 0);
    return $mineTime > $otherTime;
}

function sodiem_clear_copied_students(array $students): array {
    foreach ($students as &$student) {
        if (!is_array($student)) continue;
        $student['scores'] = [];
        $student['comment'] = '';
    }
    unset($student);
    return $students;
}

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$action = trim((string)($_GET['action'] ?? ''));
ensure_gradebook_schema($pdo);

$teacher = sodiem_teacher($pdo);

if ($method === 'GET' && $action === 'classes') {
    $details = [];
    $owned = $pdo->prepare("SELECT class_name FROM gradebooks WHERE teacher_id = ? AND TRIM(class_name) <> '' GROUP BY class_name");
    $owned->execute([(int)$teacher['id']]);
    foreach ($owned->fetchAll() as $row) {
        $className = trim((string)$row['class_name']);
        if ($className !== '') $details[$className] = 0;
    }
    foreach (teacher_managed_classes($teacher) as $className) {
        $details[$className] = $details[$className] ?? 0;
    }
    if ($details) {
        $school = $pdo->query("SELECT class_name, COUNT(*) AS count FROM users WHERE role = 'student' AND is_active = 1 AND TRIM(class_name) <> '' GROUP BY class_name")->fetchAll();
        foreach ($school as $row) {
            $className = trim((string)$row['class_name']);
            if (isset($details[$className])) $details[$className] = (int)$row['count'];
        }
    }
    $classes = array_keys($details);
    sort($classes, SORT_NATURAL | SORT_FLAG_CASE);
    respond(['classes' => $classes, 'details' => array_map(fn($className) => ['class_name' => $className, 'count' => $details[$className]], $classes)]);
}

if ($method === 'GET' && $action === 'load') {
    $class = trim((string)($_GET['class_name'] ?? ''));
    $subject = trim((string)($_GET['subject'] ?? ''));
    $year = trim((string)($_GET['academic_year'] ?? '2025-2026'));
    if ($class === '' || $subject === '') respond(['error' => 'Thiếu lớp hoặc môn học.'], 422);
    $stmt = $pdo->prepare('SELECT id, columns_config_json, students_data_json, history_log_json, updated_at FROM gradebooks WHERE teacher_id = ? AND class_name = ? AND subject = ? AND academic_year = ? LIMIT 1');
    $stmt->execute([(int)$teacher['id'], $class, $subject, $year]);
    $book = $stmt->fetch();
    if ($book) {
        $mine = sodiem_mark_map($book['students_data_json'] ?? '');
        foreach (sodiem_other_mark_maps($pdo, (int)$teacher['id'], $class, $subject, $year) as $other) {
            if (!sodiem_marks_overlap($mine, $other['map']) || !sodiem_is_newer_copy($book, $other)) continue;
            $clear = $pdo->prepare('UPDATE gradebooks SET students_data_json = ?, history_log_json = ? WHERE teacher_id = ? AND class_name = ? AND subject = ? AND academic_year = ?');
            $clear->execute(['[]', '[]', (int)$teacher['id'], $class, $subject, $year]);
            $book = null;
            break;
        }
    }
    if ($book) $book['owner_id'] = (int)$teacher['id'];
    $rosterStmt = $pdo->prepare("SELECT id, username, full_name, class_name FROM users WHERE role = 'student' AND is_active = 1 AND class_name = ? ORDER BY full_name, username");
    $rosterStmt->execute([$class]);
    respond(['gradebook' => $book ?: null, 'roster' => $rosterStmt->fetchAll(), 'owner_id' => (int)$teacher['id']]);
}

function sodiem_insert_gradebook(PDO $pdo, int $teacherId, string $class, string $subject, string $year, string $columnsJson, string $studentsJson, string $historyJson): void {
    $stmt = $pdo->prepare('INSERT INTO gradebooks (teacher_id, class_name, subject, academic_year, columns_config_json, students_data_json, history_log_json) VALUES (?, ?, ?, ?, ?, ?, ?)');
    try {
        $stmt->execute([$teacherId, $class, $subject, $year, $columnsJson, $studentsJson, $historyJson]);
        return;
    } catch (PDOException $e) {
        if (!in_array((string)$e->getCode(), ['23000', '23001'], true)) throw $e;
    }
    try {
        sodiem_drop_shared_unique($pdo);
    } catch (Throwable $e) {
        respond(['error' => 'Không lưu được vì sổ này đang dùng chung khóa với giáo viên khác.'], 409);
    }
    try {
        $stmt->execute([$teacherId, $class, $subject, $year, $columnsJson, $studentsJson, $historyJson]);
    } catch (PDOException $e) {
        respond(['error' => 'Không lưu đè sổ điểm của giáo viên khác.'], 409);
    }
}

if ($method === 'POST' && $action === 'save') {
    $data = json_body();
    $class = trim((string)($data['class_name'] ?? ''));
    $subject = trim((string)($data['subject'] ?? ''));
    $year = trim((string)($data['academic_year'] ?? '2025-2026'));
    if ($class === '' || $subject === '') respond(['error' => 'Thiếu lớp hoặc môn học.'], 422);
    $columns = $data['columns'] ?? [];
    $students = $data['students'] ?? [];
    $history = $data['history'] ?? [];
    if (!is_array($students)) $students = [];
    if (!is_array($history)) $history = [];
    $mine = sodiem_mark_map(json_encode($students, JSON_UNESCAPED_UNICODE));
    $cleared = false;
    foreach (sodiem_other_mark_maps($pdo, (int)$teacher['id'], $class, $subject, $year) as $other) {
        if (!sodiem_marks_overlap($mine, $other['map'])) continue;
        $students = sodiem_clear_copied_students($students);
        $history = [];
        $cleared = true;
        break;
    }
    $columnsJson = json_encode($columns, JSON_UNESCAPED_UNICODE);
    $studentsJson = json_encode($students, JSON_UNESCAPED_UNICODE);
    $historyJson = json_encode($history, JSON_UNESCAPED_UNICODE);
    $teacherId = (int)$teacher['id'];
    $update = $pdo->prepare('UPDATE gradebooks SET columns_config_json = ?, students_data_json = ?, history_log_json = ? WHERE teacher_id = ? AND class_name = ? AND subject = ? AND academic_year = ?');
    $update->execute([$columnsJson, $studentsJson, $historyJson, $teacherId, $class, $subject, $year]);
    $exists = $pdo->prepare('SELECT id FROM gradebooks WHERE teacher_id = ? AND class_name = ? AND subject = ? AND academic_year = ? LIMIT 1');
    $exists->execute([$teacherId, $class, $subject, $year]);
    if (!$exists->fetch()) sodiem_insert_gradebook($pdo, $teacherId, $class, $subject, $year, $columnsJson, $studentsJson, $historyJson);
    respond(['status' => 'ok', 'cleared' => $cleared, 'owner_id' => $teacherId]);
}

respond(['error' => 'Hành động không hợp lệ.'], 404);
