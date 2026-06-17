<?php
require_once __DIR__ . '/helpers.php';
require_admin_key();

function column_exists(PDO $pdo, string $table, string $column): bool
{
    $stmt = $pdo->prepare("SHOW COLUMNS FROM `$table` LIKE ?");
    $stmt->execute([$column]);
    return (bool)$stmt->fetch();
}

function add_column_if_missing(PDO $pdo, string $table, string $definition): void
{
    $name = trim(strtok($definition, ' '));
    if (!column_exists($pdo, $table, $name)) {
        $pdo->exec("ALTER TABLE `$table` ADD COLUMN $definition");
    }
}

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
    tasks_json LONGTEXT DEFAULT NULL,
    skills_json LONGTEXT DEFAULT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

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
    UNIQUE KEY uniq_student_lesson (student_id, lesson_id),
    CONSTRAINT fk_progress_student FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_progress_lesson FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

add_column_if_missing($pdo, 'lessons', 'goal_text TEXT DEFAULT NULL');
add_column_if_missing($pdo, 'lessons', 'theory_json LONGTEXT DEFAULT NULL');
add_column_if_missing($pdo, 'lessons', 'examples_json LONGTEXT DEFAULT NULL');
add_column_if_missing($pdo, 'lessons', 'questions_json LONGTEXT DEFAULT NULL');
add_column_if_missing($pdo, 'lessons', 'tasks_json LONGTEXT DEFAULT NULL');
add_column_if_missing($pdo, 'lessons', 'skills_json LONGTEXT DEFAULT NULL');
add_column_if_missing($pdo, 'student_lesson_progress', 'state_json TEXT DEFAULT NULL');

$defaultTheory = [
    "Tập hợp là một nhóm các đối tượng được xác định rõ ràng.",
    "Mỗi đối tượng trong một tập hợp được gọi là một phần tử.",
    "Ta thường đặt tên tập hợp bằng các chữ cái in hoa.",
    "Các phần tử thường được viết trong dấu ngoặc nhọn { }."
];

$defaultExamples = [
    ["title" => "Ví dụ 1", "body" => "A = {1, 2, 3, 4} là tập hợp các số tự nhiên nhỏ hơn 5."],
    ["title" => "Ví dụ 2", "body" => "Nếu B = {a, b, c} thì a ∈ B và d ∉ B."],
    ["title" => "Ví dụ 3", "body" => "C = {T, O, A, N} là tập hợp các chữ cái trong từ TOAN."]
];

$defaultQuestions = [
    ["id" => "q1", "skill" => "khai_niem", "prompt" => "Câu nào mô tả đúng nhất về tập hợp?", "options" => ["Một nhóm các đối tượng được xác định rõ ràng", "Một phép tính cộng nhiều số", "Một số tự nhiên bất kỳ", "Một hình vẽ trong vở"], "answer" => 0],
    ["id" => "q2", "skill" => "viet_tap_hop", "prompt" => "Cách viết nào đúng cho tập hợp A gồm các số 1, 2, 3?", "options" => ["A = (1, 2, 3)", "A = {1, 2, 3}", "A = [1, 2, 3]", "A = 1 + 2 + 3"], "answer" => 1],
    ["id" => "q3", "skill" => "ky_hieu", "prompt" => "Cho B = {2, 4, 6, 8}. Khẳng định nào đúng?", "options" => ["3 ∈ B", "6 ∈ B", "8 ∉ B", "4 ∉ B"], "answer" => 1]
];

$defaultSkills = [
    ["id" => "khai_niem", "name" => "Hiểu khái niệm tập hợp", "target" => 80],
    ["id" => "liet_ke", "name" => "Liệt kê phần tử của tập hợp", "target" => 80],
    ["id" => "ky_hieu", "name" => "Dùng ký hiệu ∈ và ∉", "target" => 80],
    ["id" => "viet_tap_hop", "name" => "Viết tập hợp đúng quy ước", "target" => 80]
];

$stmt = $pdo->prepare("INSERT INTO lessons (subject, chapter, title, slug, order_index, is_published, goal_text, theory_json, examples_json, questions_json, tasks_json, skills_json)
    VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?)
    ON DUPLICATE KEY UPDATE
        subject = VALUES(subject),
        chapter = VALUES(chapter),
        title = VALUES(title),
        order_index = VALUES(order_index),
        is_published = VALUES(is_published),
        goal_text = VALUES(goal_text),
        theory_json = VALUES(theory_json),
        examples_json = VALUES(examples_json),
        questions_json = VALUES(questions_json),
        tasks_json = VALUES(tasks_json),
        skills_json = VALUES(skills_json)");
$stmt->execute([
    'Toán 6',
    'Chương 1: Số tự nhiên',
    'Bài 1: Tập hợp',
    'math6-c1-b1-tap-hop',
    1,
    'Học sinh hiểu tập hợp là gì, biết viết tập hợp bằng cách liệt kê phần tử và dùng đúng ký hiệu thuộc, không thuộc.',
    json_encode($defaultTheory, JSON_UNESCAPED_UNICODE),
    json_encode($defaultExamples, JSON_UNESCAPED_UNICODE),
    json_encode($defaultQuestions, JSON_UNESCAPED_UNICODE),
    json_encode(["Đọc lý thuyết ngắn", "Xem 3 ví dụ mẫu", "Làm 8 câu luyện tập"], JSON_UNESCAPED_UNICODE),
    json_encode($defaultSkills, JSON_UNESCAPED_UNICODE)
]);

respond(['ok' => true, 'message' => 'Đã cập nhật schema bài học.']);
