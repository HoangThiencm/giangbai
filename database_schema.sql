CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(160) NOT NULL,
    role ENUM('teacher', 'student') NOT NULL DEFAULT 'student',
    class_name VARCHAR(80) DEFAULT NULL,
    allowed_pages_json TEXT DEFAULT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    expires_at DATETIME DEFAULT NULL,
    expires_option VARCHAR(20) NOT NULL DEFAULT 'forever',
    last_login_at DATETIME DEFAULT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS lessons (
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
    videos_json LONGTEXT DEFAULT NULL,
    tasks_json LONGTEXT DEFAULT NULL,
    skills_json LONGTEXT DEFAULT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS student_lesson_progress (
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
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS exams (
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
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS exam_submissions (
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
    INDEX idx_submissions_score (score),
    CONSTRAINT fk_submissions_exam FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO lessons (subject, chapter, title, slug, order_index, is_published)
VALUES
    ('Toán 6', 'Chương 1: Số tự nhiên', 'Bài 1: Tập hợp', 'math6-c1-b1-tap-hop', 1, 1),
    ('Toán 7', 'Chương 1', 'Bài 1: Nhập nội dung', 'math7-c1-b1-draft', 1, 0),
    ('Toán 8', 'Chương 1', 'Bài 1: Nhập nội dung', 'math8-c1-b1-draft', 1, 0),
    ('Toán 9', 'Chương 1', 'Bài 1: Nhập nội dung', 'math9-c1-b1-draft', 1, 0)
ON DUPLICATE KEY UPDATE slug = VALUES(slug);
