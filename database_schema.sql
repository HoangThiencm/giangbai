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
    student_id INT DEFAULT NULL,
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
    INDEX idx_submissions_student (student_id),
    INDEX idx_submissions_score (score),
    CONSTRAINT fk_submissions_exam FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
    CONSTRAINT fk_exam_submissions_student FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE SET NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS exam_assignments (
    exam_id VARCHAR(16) NOT NULL,
    student_id INT NOT NULL,
    subject VARCHAR(80) NOT NULL DEFAULT '',
    grade VARCHAR(20) NOT NULL DEFAULT '',
    class_name VARCHAR(80) NOT NULL DEFAULT '',
    assigned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (exam_id, student_id),
    INDEX idx_exam_assignments_student_subject (student_id, subject),
    INDEX idx_exam_assignments_exam (exam_id),
    CONSTRAINT fk_exam_assignments_exam FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
    CONSTRAINT fk_exam_assignments_student FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS student_notifications (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    event_key VARCHAR(160) NOT NULL,
    notification_type ENUM('lesson', 'exam') NOT NULL,
    entity_id VARCHAR(40) NOT NULL,
    subject VARCHAR(80) NOT NULL DEFAULT '',
    title VARCHAR(255) NOT NULL,
    message TEXT DEFAULT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    read_at DATETIME DEFAULT NULL,
    UNIQUE KEY uniq_student_notification (student_id, event_key),
    INDEX idx_student_notifications_unread (student_id, read_at, created_at),
    CONSTRAINT fk_student_notifications_student FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS app_schema_migrations (
    migration_key VARCHAR(120) PRIMARY KEY,
    completed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS submission_assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    public_code VARCHAR(24) NOT NULL UNIQUE,
    owner_id INT NOT NULL,
    title VARCHAR(220) NOT NULL,
    description TEXT DEFAULT NULL,
    instructions TEXT DEFAULT NULL,
    submission_type VARCHAR(20) NOT NULL DEFAULT 'file',
    academic_year VARCHAR(30) DEFAULT NULL,
    form_fields_json LONGTEXT DEFAULT NULL,
    require_files TINYINT(1) NOT NULL DEFAULT 1,
    access_mode ENUM('public', 'class', 'selected', 'school_list') NOT NULL DEFAULT 'public',
    target_class VARCHAR(100) DEFAULT NULL,
    source_list_code VARCHAR(40) DEFAULT NULL,
    status ENUM('draft', 'open', 'closed') NOT NULL DEFAULT 'open',
    open_at DATETIME DEFAULT NULL,
    due_at DATETIME DEFAULT NULL,
    allow_multiple TINYINT(1) NOT NULL DEFAULT 0,
    max_files INT NOT NULL DEFAULT 5,
    max_file_mb INT NOT NULL DEFAULT 25,
    allowed_extensions VARCHAR(500) NOT NULL DEFAULT 'pdf,doc,docx,xls,xlsx,ppt,pptx,jpg,jpeg,png,zip,rar,txt',
    drive_folder_id VARCHAR(160) DEFAULT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_submission_assignments_owner (owner_id),
    INDEX idx_submission_assignments_status (status),
    CONSTRAINT fk_submission_assignment_owner FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS submission_participants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_id INT NOT NULL,
    linked_user_id INT DEFAULT NULL,
    participant_code VARCHAR(40) NOT NULL,
    full_name VARCHAR(180) NOT NULL,
    role_label VARCHAR(100) DEFAULT NULL,
    group_name VARCHAR(160) DEFAULT NULL,
    contact VARCHAR(180) DEFAULT NULL,
    reopened TINYINT(1) NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uniq_assignment_participant_code (assignment_id, participant_code),
    INDEX idx_submission_participants_user (linked_user_id),
    CONSTRAINT fk_submission_participant_assignment FOREIGN KEY (assignment_id) REFERENCES submission_assignments(id) ON DELETE CASCADE,
    CONSTRAINT fk_submission_participant_user FOREIGN KEY (linked_user_id) REFERENCES users(id) ON DELETE SET NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS assignment_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_id INT NOT NULL,
    participant_id INT DEFAULT NULL,
    linked_user_id INT DEFAULT NULL,
    submitter_name VARCHAR(180) NOT NULL,
    submitter_role VARCHAR(100) DEFAULT NULL,
    group_name VARCHAR(160) DEFAULT NULL,
    identifier VARCHAR(180) DEFAULT NULL,
    note TEXT DEFAULT NULL,
    report_data_json LONGTEXT DEFAULT NULL,
    submitted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_assignment_submissions_assignment (assignment_id),
    INDEX idx_assignment_submissions_participant (participant_id),
    CONSTRAINT fk_assignment_submission_assignment FOREIGN KEY (assignment_id) REFERENCES submission_assignments(id) ON DELETE CASCADE,
    CONSTRAINT fk_assignment_submission_participant FOREIGN KEY (participant_id) REFERENCES submission_participants(id) ON DELETE SET NULL,
    CONSTRAINT fk_assignment_submission_user FOREIGN KEY (linked_user_id) REFERENCES users(id) ON DELETE SET NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS assignment_submission_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    submission_id INT NOT NULL,
    drive_file_id VARCHAR(160) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    stored_name VARCHAR(255) NOT NULL,
    mime_type VARCHAR(160) DEFAULT NULL,
    size_bytes BIGINT NOT NULL DEFAULT 0,
    view_url TEXT NOT NULL,
    download_url TEXT DEFAULT NULL,
    field_key VARCHAR(120) DEFAULT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_assignment_submission_files_submission (submission_id),
    CONSTRAINT fk_assignment_file_submission FOREIGN KEY (submission_id) REFERENCES assignment_submissions(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS padlet_boards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    public_code VARCHAR(24) NOT NULL UNIQUE,
    owner_id INT NOT NULL,
    title VARCHAR(220) NOT NULL,
    description TEXT DEFAULT NULL,
    layout_type ENUM('wall','columns','stream','grid','timeline','map','whiteboard','mindmap','presentation','venn','question') NOT NULL DEFAULT 'wall',
    bg_theme VARCHAR(30) NOT NULL DEFAULT 'teal',
    color_mode ENUM('light','dark') NOT NULL DEFAULT 'light',
    font_family VARCHAR(30) NOT NULL DEFAULT 'inter',
    post_size ENUM('standard','wide') NOT NULL DEFAULT 'standard',
    post_position ENUM('first','last') NOT NULL DEFAULT 'first',
    show_author TINYINT(1) NOT NULL DEFAULT 1,
    default_column_id INT DEFAULT NULL,
    prompt_text TEXT DEFAULT NULL,
    access_mode ENUM('public','class') NOT NULL DEFAULT 'public',
    target_class VARCHAR(100) DEFAULT NULL,
    status ENUM('open','closed') NOT NULL DEFAULT 'open',
    academic_year VARCHAR(30) DEFAULT NULL,
    moderation_enabled TINYINT(1) NOT NULL DEFAULT 1,
    comments_enabled TINYINT(1) NOT NULL DEFAULT 1,
    reactions_enabled TINYINT(1) NOT NULL DEFAULT 1,
    drive_folder_id VARCHAR(160) DEFAULT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_padlet_boards_owner (owner_id),
    INDEX idx_padlet_boards_code (public_code),
    CONSTRAINT fk_padlet_board_owner FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS padlet_columns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    board_id INT NOT NULL,
    parent_id INT DEFAULT NULL,
    title VARCHAR(160) NOT NULL,
    color VARCHAR(30) NOT NULL DEFAULT 'teal',
    order_index INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_padlet_columns_board (board_id),
    CONSTRAINT fk_padlet_column_board FOREIGN KEY (board_id) REFERENCES padlet_boards(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS padlet_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    board_id INT NOT NULL,
    column_id INT DEFAULT NULL,
    author_user_id INT DEFAULT NULL,
    author_name VARCHAR(180) NOT NULL,
    author_role VARCHAR(100) DEFAULT NULL,
    author_group VARCHAR(160) DEFAULT NULL,
    body TEXT DEFAULT NULL,
    link_url TEXT DEFAULT NULL,
    link_title VARCHAR(300) DEFAULT NULL,
    link_image TEXT DEFAULT NULL,
    location_label VARCHAR(200) DEFAULT NULL,
    map_lat DECIMAL(10,7) DEFAULT NULL,
    map_lng DECIMAL(10,7) DEFAULT NULL,
    venn_zone VARCHAR(10) DEFAULT NULL,
    pos_x INT DEFAULT NULL,
    pos_y INT DEFAULT NULL,
    card_color VARCHAR(30) NOT NULL DEFAULT 'white',
    status ENUM('pending','published','rejected') NOT NULL DEFAULT 'pending',
    pinned TINYINT(1) NOT NULL DEFAULT 0,
    order_index INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_padlet_posts_board (board_id),
    INDEX idx_padlet_posts_column (column_id),
    INDEX idx_padlet_posts_status (status),
    CONSTRAINT fk_padlet_post_board FOREIGN KEY (board_id) REFERENCES padlet_boards(id) ON DELETE CASCADE,
    CONSTRAINT fk_padlet_post_column FOREIGN KEY (column_id) REFERENCES padlet_columns(id) ON DELETE SET NULL,
    CONSTRAINT fk_padlet_post_author FOREIGN KEY (author_user_id) REFERENCES users(id) ON DELETE SET NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS padlet_post_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    drive_file_id VARCHAR(160) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    stored_name VARCHAR(255) NOT NULL,
    mime_type VARCHAR(160) DEFAULT NULL,
    size_bytes BIGINT NOT NULL DEFAULT 0,
    view_url TEXT NOT NULL,
    download_url TEXT DEFAULT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_padlet_files_post (post_id),
    CONSTRAINT fk_padlet_file_post FOREIGN KEY (post_id) REFERENCES padlet_posts(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS padlet_comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    author_user_id INT DEFAULT NULL,
    author_name VARCHAR(180) NOT NULL,
    author_role VARCHAR(100) DEFAULT NULL,
    body TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_padlet_comments_post (post_id),
    CONSTRAINT fk_padlet_comment_post FOREIGN KEY (post_id) REFERENCES padlet_posts(id) ON DELETE CASCADE,
    CONSTRAINT fk_padlet_comment_author FOREIGN KEY (author_user_id) REFERENCES users(id) ON DELETE SET NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS padlet_reactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    visitor_key VARCHAR(100) NOT NULL,
    reaction VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uniq_padlet_reaction (post_id, visitor_key, reaction),
    INDEX idx_padlet_reactions_post (post_id),
    CONSTRAINT fk_padlet_reaction_post FOREIGN KEY (post_id) REFERENCES padlet_posts(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS short_links (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(12) NOT NULL,
    target_url TEXT NOT NULL,
    title VARCHAR(200) DEFAULT NULL,
    note TEXT DEFAULT NULL,
    owner_id INT NOT NULL,
    click_count INT NOT NULL DEFAULT 0,
    max_clicks INT DEFAULT NULL,
    expires_at DATETIME DEFAULT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    last_clicked_at DATETIME DEFAULT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uniq_short_link_code (code),
    INDEX idx_short_links_owner (owner_id),
    INDEX idx_short_links_active (is_active),
    INDEX idx_short_links_expires (expires_at),
    CONSTRAINT fk_short_link_owner FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS short_link_clicks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    link_id INT NOT NULL,
    clicked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_hash VARCHAR(64) DEFAULT NULL,
    user_agent VARCHAR(255) DEFAULT NULL,
    referer VARCHAR(255) DEFAULT NULL,
    INDEX idx_short_link_clicks_link (link_id),
    INDEX idx_short_link_clicks_time (clicked_at),
    CONSTRAINT fk_short_link_click_link FOREIGN KEY (link_id) REFERENCES short_links(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS achievement_school_years (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(40) NOT NULL UNIQUE,
    created_by INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_achievement_school_years_name (name)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS achievement_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    academic_year VARCHAR(40) NOT NULL DEFAULT '',
    participant_type ENUM('teacher', 'student') NOT NULL,
    campaign_name VARCHAR(300) NOT NULL,
    organizer VARCHAR(300) NOT NULL DEFAULT '',
    scope_level VARCHAR(40) NOT NULL DEFAULT 'school',
    event_date DATE DEFAULT NULL,
    participant_count INT NOT NULL DEFAULT 0,
    prize_count INT NOT NULL DEFAULT 0,
    prize_summary VARCHAR(500) DEFAULT NULL,
    note TEXT DEFAULT NULL,
    created_by INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_achievement_entries_year (academic_year),
    INDEX idx_achievement_entries_type (participant_type),
    INDEX idx_achievement_entries_organizer (organizer)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS achievement_winners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entry_id INT NOT NULL,
    full_name VARCHAR(180) NOT NULL,
    class_or_role VARCHAR(120) DEFAULT NULL,
    prize_rank VARCHAR(80) NOT NULL DEFAULT '',
    prize_title VARCHAR(300) DEFAULT NULL,
    note TEXT DEFAULT NULL,
    order_index INT NOT NULL DEFAULT 0,
    INDEX idx_achievement_winners_entry (entry_id),
    CONSTRAINT fk_achievement_winner_entry FOREIGN KEY (entry_id) REFERENCES achievement_entries(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS timetable_projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_key VARCHAR(80) NOT NULL UNIQUE,
    name VARCHAR(180) NOT NULL DEFAULT 'Thời khóa biểu nhà trường',
    school_year VARCHAR(40) NOT NULL DEFAULT '',
    project_json LONGTEXT NOT NULL,
    result_json LONGTEXT DEFAULT NULL,
    created_by INT NOT NULL,
    updated_by INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_timetable_projects_updated (updated_at),
    INDEX idx_timetable_projects_school_year (school_year),
    CONSTRAINT fk_timetable_project_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_timetable_project_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO lessons (subject, chapter, title, slug, order_index, is_published)
VALUES
    ('Toán 6', 'Chương 1: Số tự nhiên', 'Bài 1: Tập hợp', 'math6-c1-b1-tap-hop', 1, 1),
    ('Toán 7', 'Chương 1', 'Bài 1: Nhập nội dung', 'math7-c1-b1-draft', 1, 0),
    ('Toán 8', 'Chương 1', 'Bài 1: Nhập nội dung', 'math8-c1-b1-draft', 1, 0),
    ('Toán 9', 'Chương 1', 'Bài 1: Nhập nội dung', 'math9-c1-b1-draft', 1, 0)
ON DUPLICATE KEY UPDATE slug = VALUES(slug);
