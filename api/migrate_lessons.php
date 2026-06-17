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
    'Tap hop la mot nhom cac doi tuong duoc xac dinh ro rang.',
    'Moi doi tuong trong mot tap hop duoc goi la mot phan tu.',
    'Ta thuong dat ten tap hop bang chu cai in hoa.',
    'Co the nhap cong thuc bang LaTeX, vi du: $A=\\{1,2,3\\}$.'
];

$defaultExamples = [
    ['title' => 'Vi du 1', 'body' => 'A = $\\{1,2,3,4\\}$ la tap hop cac so tu nhien nho hon 5.'],
    ['title' => 'Vi du 2', 'body' => 'Neu B = $\\{a,b,c\\}$ thi $a \\in B$ va $d \\notin B$.']
];

$defaultQuestions = [
    [
        'id' => 'q1',
        'skill' => 'khai_niem',
        'prompt' => 'Cau nao mo ta dung nhat ve tap hop?',
        'options' => ['Mot nhom cac doi tuong duoc xac dinh ro rang', 'Mot phep tinh cong', 'Mot so tu nhien bat ky', 'Mot hinh ve'],
        'answer' => 0
    ],
    [
        'id' => 'q2',
        'skill' => 'ky_hieu',
        'prompt' => 'Cho $B=\\{2,4,6,8\\}$. Khang dinh nao dung?',
        'options' => ['$3 \\in B$', '$6 \\in B$', '$8 \\notin B$', '$4 \\notin B$'],
        'answer' => 1
    ]
];

$defaultSkills = [
    ['id' => 'khai_niem', 'name' => 'Hieu khai niem tap hop', 'target' => 80],
    ['id' => 'liet_ke', 'name' => 'Liet ke phan tu cua tap hop', 'target' => 80],
    ['id' => 'ky_hieu', 'name' => 'Dung ky hieu thuoc va khong thuoc', 'target' => 80],
];

$stmt = $pdo->prepare("INSERT INTO lessons (subject, chapter, title, slug, order_index, is_published, goal_text, theory_json, examples_json, questions_json, tasks_json, skills_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON DUPLICATE KEY UPDATE slug = slug");

$stmt->execute([
    'Toán 6',
    'Chương 1: Số tự nhiên',
    'Bài 1: Tập hợp',
    'math6-c1-b1-tap-hop',
    1,
    1,
    'Hoc sinh hieu tap hop la gi, biet viet tap hop bang cach liet ke phan tu va dung ky hieu thuoc, khong thuoc.',
    json_encode($defaultTheory, JSON_UNESCAPED_UNICODE),
    json_encode($defaultExamples, JSON_UNESCAPED_UNICODE),
    json_encode($defaultQuestions, JSON_UNESCAPED_UNICODE),
    json_encode(['Doc ly thuyet ngan', 'Xem vi du mau', 'Lam bai luyen tap'], JSON_UNESCAPED_UNICODE),
    json_encode($defaultSkills, JSON_UNESCAPED_UNICODE)
]);

$draftLessons = [
    ['Toán 7', 'Chương 1', 'Bài 1: Nhập nội dung', 'math7-c1-b1-draft'],
    ['Toán 8', 'Chương 1', 'Bài 1: Nhập nội dung', 'math8-c1-b1-draft'],
    ['Toán 9', 'Chương 1', 'Bài 1: Nhập nội dung', 'math9-c1-b1-draft'],
];

foreach ($draftLessons as $draft) {
    $stmt->execute([
        $draft[0],
        $draft[1],
        $draft[2],
        $draft[3],
        1,
        0,
        'Ban nhap. Giao vien nhap noi dung roi moi mo cho hoc sinh.',
        json_encode([], JSON_UNESCAPED_UNICODE),
        json_encode([], JSON_UNESCAPED_UNICODE),
        json_encode([], JSON_UNESCAPED_UNICODE),
        json_encode([], JSON_UNESCAPED_UNICODE),
        json_encode([], JSON_UNESCAPED_UNICODE)
    ]);
}

respond(['ok' => true, 'message' => 'Da cap nhat schema bai hoc.']);
