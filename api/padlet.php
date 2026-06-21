<?php
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/google_drive.php';

date_default_timezone_set(defined('APP_TIMEZONE') ? (string)APP_TIMEZONE : 'Asia/Ho_Chi_Minh');

set_exception_handler(function (Throwable $e) {
    $payload = ['error' => 'Có lỗi khi xử lý Bảng chia sẻ.'];
    if (defined('APP_DEBUG') && APP_DEBUG) $payload['detail'] = $e->getMessage();
    respond($payload, 500);
});

function padlet_schema(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS padlet_boards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        public_code VARCHAR(24) NOT NULL UNIQUE,
        owner_id INT NOT NULL,
        title VARCHAR(220) NOT NULL,
        description TEXT DEFAULT NULL,
        layout_type ENUM('wall','columns','stream','grid','timeline','map') NOT NULL DEFAULT 'wall',
        bg_theme VARCHAR(30) NOT NULL DEFAULT 'teal',
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
        INDEX idx_padlet_boards_code (public_code)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    $pdo->exec("CREATE TABLE IF NOT EXISTS padlet_columns (
        id INT AUTO_INCREMENT PRIMARY KEY,
        board_id INT NOT NULL,
        title VARCHAR(160) NOT NULL,
        color VARCHAR(30) NOT NULL DEFAULT 'teal',
        order_index INT NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_padlet_columns_board (board_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    $pdo->exec("CREATE TABLE IF NOT EXISTS padlet_posts (
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
        card_color VARCHAR(30) NOT NULL DEFAULT 'white',
        status ENUM('pending','published','rejected') NOT NULL DEFAULT 'pending',
        pinned TINYINT(1) NOT NULL DEFAULT 0,
        order_index INT NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_padlet_posts_board (board_id),
        INDEX idx_padlet_posts_column (column_id),
        INDEX idx_padlet_posts_status (status)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    $pdo->exec("CREATE TABLE IF NOT EXISTS padlet_post_files (
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
        INDEX idx_padlet_files_post (post_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    $pdo->exec("CREATE TABLE IF NOT EXISTS padlet_comments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        post_id INT NOT NULL,
        author_user_id INT DEFAULT NULL,
        author_name VARCHAR(180) NOT NULL,
        author_role VARCHAR(100) DEFAULT NULL,
        body TEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_padlet_comments_post (post_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    $pdo->exec("CREATE TABLE IF NOT EXISTS padlet_reactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        post_id INT NOT NULL,
        visitor_key VARCHAR(100) NOT NULL,
        reaction VARCHAR(20) NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_padlet_reaction (post_id, visitor_key, reaction),
        INDEX idx_padlet_reactions_post (post_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}

function padlet_column_exists(PDO $pdo, string $table, string $column): bool
{
    $stmt = $pdo->prepare('SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = ? AND COLUMN_NAME = ?');
    $stmt->execute([$table, $column]);
    return (int)$stmt->fetchColumn() > 0;
}

function padlet_migrate(PDO $pdo): void
{
    try {
        $pdo->exec("ALTER TABLE padlet_boards MODIFY layout_type ENUM('wall','columns','stream','grid','timeline','map') NOT NULL DEFAULT 'wall'");
    } catch (Throwable $e) { /* bảng mới đã đúng ENUM */ }
    if (!padlet_column_exists($pdo, 'padlet_boards', 'bg_theme')) {
        $pdo->exec("ALTER TABLE padlet_boards ADD COLUMN bg_theme VARCHAR(30) NOT NULL DEFAULT 'teal' AFTER layout_type");
    }
    if (!padlet_column_exists($pdo, 'padlet_posts', 'link_title')) {
        $pdo->exec("ALTER TABLE padlet_posts ADD COLUMN link_title VARCHAR(300) DEFAULT NULL AFTER link_url");
    }
    if (!padlet_column_exists($pdo, 'padlet_posts', 'link_image')) {
        $pdo->exec("ALTER TABLE padlet_posts ADD COLUMN link_image TEXT DEFAULT NULL AFTER link_title");
    }
    if (!padlet_column_exists($pdo, 'padlet_posts', 'location_label')) {
        $pdo->exec("ALTER TABLE padlet_posts ADD COLUMN location_label VARCHAR(200) DEFAULT NULL AFTER link_image");
    }
    if (!padlet_column_exists($pdo, 'padlet_posts', 'map_lat')) {
        $pdo->exec("ALTER TABLE padlet_posts ADD COLUMN map_lat DECIMAL(10,7) DEFAULT NULL AFTER location_label");
    }
    if (!padlet_column_exists($pdo, 'padlet_posts', 'map_lng')) {
        $pdo->exec("ALTER TABLE padlet_posts ADD COLUMN map_lng DECIMAL(10,7) DEFAULT NULL AFTER map_lat");
    }
}

function padlet_layout_type(string $value): string
{
    return in_array($value, ['wall', 'columns', 'stream', 'grid', 'timeline', 'map'], true) ? $value : 'wall';
}

function padlet_bg_theme(string $value): string
{
    return in_array($value, ['teal', 'blue', 'violet', 'rose', 'amber', 'slate', 'emerald'], true) ? $value : 'teal';
}

function padlet_youtube_id(string $url): ?string
{
    if (!preg_match('~(?:youtube\.com/(?:watch\?v=|shorts/|embed/)|youtu\.be/)([\w-]{11})~i', $url, $m)) return null;
    return $m[1];
}

function padlet_link_preview(string $url): array
{
    $out = ['title' => '', 'image' => ''];
    if ($url === '' || !filter_var($url, FILTER_VALIDATE_URL)) return $out;
    if ($yt = padlet_youtube_id($url)) {
        $out['image'] = "https://img.youtube.com/vi/{$yt}/hqdefault.jpg";
        $out['title'] = 'YouTube Video';
        return $out;
    }
    if (!function_exists('curl_init')) return $out;
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_MAXREDIRS => 4,
        CURLOPT_TIMEOUT => 8,
        CURLOPT_CONNECTTIMEOUT => 5,
        CURLOPT_USERAGENT => 'Mozilla/5.0 (compatible; GiangBaiPadlet/1.0)',
        CURLOPT_SSL_VERIFYPEER => true,
    ]);
    $html = curl_exec($ch);
    curl_close($ch);
    if (!is_string($html) || $html === '') return $out;
    if (preg_match('/<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)/i', $html, $m)
        || preg_match('/<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:title/i', $html, $m)) {
        $out['title'] = padlet_trim_text(html_entity_decode($m[1], ENT_QUOTES | ENT_HTML5, 'UTF-8'), 300);
    } elseif (preg_match('/<title[^>]*>([^<]+)<\/title>/i', $html, $m)) {
        $out['title'] = padlet_trim_text(html_entity_decode(trim($m[1]), ENT_QUOTES | ENT_HTML5, 'UTF-8'), 300);
    }
    if (preg_match('/<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)/i', $html, $m)
        || preg_match('/<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image/i', $html, $m)) {
        $out['image'] = trim($m[1]);
    }
    return $out;
}

function padlet_current_user(PDO $pdo): ?array
{
    if (empty($_SESSION['user_id'])) return null;
    $stmt = $pdo->prepare('SELECT * FROM users WHERE id = ? AND is_active = 1 LIMIT 1');
    $stmt->execute([(int)$_SESSION['user_id']]);
    return $stmt->fetch() ?: null;
}

function padlet_require_teacher(PDO $pdo): array
{
    $user = padlet_current_user($pdo);
    if (!$user || ($user['role'] ?? '') !== 'teacher') respond(['error' => 'Cần đăng nhập bằng tài khoản giáo viên.'], 401);
    return $user;
}

function padlet_code(PDO $pdo): string
{
    do {
        $alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
        $code = '';
        for ($index = 0; $index < 8; $index++) $code .= $alphabet[random_int(0, strlen($alphabet) - 1)];
        $stmt = $pdo->prepare('SELECT id FROM padlet_boards WHERE public_code = ? LIMIT 1');
        $stmt->execute([$code]);
    } while ($stmt->fetch());
    return $code;
}

function padlet_board(PDO $pdo, int $id = 0, string $code = ''): ?array
{
    if ($id) {
        $stmt = $pdo->prepare('SELECT * FROM padlet_boards WHERE id = ? LIMIT 1');
        $stmt->execute([$id]);
    } else {
        $stmt = $pdo->prepare('SELECT * FROM padlet_boards WHERE public_code = ? LIMIT 1');
        $stmt->execute([strtoupper(trim($code))]);
    }
    return $stmt->fetch() ?: null;
}

function padlet_require_owner(PDO $pdo, array $teacher, int $id): array
{
    $board = padlet_board($pdo, $id);
    if (!$board || (int)$board['owner_id'] !== (int)$teacher['id']) respond(['error' => 'Không tìm thấy bảng hoặc bạn không có quyền quản lý.'], 404);
    return $board;
}

function padlet_columns(PDO $pdo, int $boardId): array
{
    $stmt = $pdo->prepare('SELECT * FROM padlet_columns WHERE board_id = ? ORDER BY order_index, id');
    $stmt->execute([$boardId]);
    $rows = $stmt->fetchAll();
    foreach ($rows as &$row) { $row['id'] = (int)$row['id']; $row['order_index'] = (int)$row['order_index']; }
    return $rows;
}

function padlet_trim_text(string $value, int $length): string
{
    return function_exists('mb_substr') ? mb_substr($value, 0, $length) : substr($value, 0, $length);
}

function padlet_normalize_columns($input): array
{
    $colors = ['teal','blue','violet','amber','rose','emerald'];
    $out = [];
    if (is_array($input)) foreach (array_slice($input, 0, 12) as $item) {
        $title = trim((string)(is_array($item) ? ($item['title'] ?? '') : $item));
        if ($title === '') continue;
        $out[] = ['id' => (int)(is_array($item) ? ($item['id'] ?? 0) : 0), 'title' => padlet_trim_text($title, 160), 'color' => in_array(($item['color'] ?? ''), $colors, true) ? $item['color'] : 'teal'];
    }
    return $out ?: [['id' => 0, 'title' => 'Bài đăng', 'color' => 'teal']];
}

function padlet_access(PDO $pdo, array $board, ?array $user): ?array
{
    if ($user && ($user['role'] ?? '') === 'teacher' && (int)$board['owner_id'] === (int)$user['id']) return $user;
    if ($board['access_mode'] === 'public') return $user;
    if (!$user) respond(['error' => 'Bảng này dành cho thành viên lớp. Vui lòng đăng nhập.'], 401);
    if (($user['role'] ?? '') !== 'student' || trim((string)$user['class_name']) !== trim((string)$board['target_class'])) {
        respond(['error' => 'Tài khoản không thuộc lớp được phép tham gia bảng này.'], 403);
    }
    return $user;
}

function padlet_visitor_key(): string
{
    if (empty($_SESSION['padlet_visitor_key'])) $_SESSION['padlet_visitor_key'] = bin2hex(random_bytes(16));
    return (string)$_SESSION['padlet_visitor_key'];
}

function padlet_file_input(): array
{
    $source = $_FILES['files'] ?? null;
    if (!$source) return [];
    if (!is_array($source['name'])) return [$source];
    $files = [];
    foreach ($source['name'] as $index => $name) $files[] = ['name' => $name, 'type' => $source['type'][$index] ?? '', 'tmp_name' => $source['tmp_name'][$index] ?? '', 'error' => $source['error'][$index] ?? UPLOAD_ERR_NO_FILE, 'size' => $source['size'][$index] ?? 0];
    return $files;
}

function padlet_payload(PDO $pdo, array $board, bool $includeAll = false): array
{
    $columns = padlet_columns($pdo, (int)$board['id']);
    $sql = 'SELECT * FROM padlet_posts WHERE board_id = ?' . ($includeAll ? '' : " AND status = 'published'") . ' ORDER BY pinned DESC, order_index ASC, created_at DESC';
    $stmt = $pdo->prepare($sql); $stmt->execute([(int)$board['id']]); $posts = $stmt->fetchAll();
    $postIds = array_map(fn($row) => (int)$row['id'], $posts);
    $filesByPost = []; $commentsByPost = []; $reactionsByPost = [];
    if ($postIds) {
        $marks = implode(',', array_fill(0, count($postIds), '?'));
        $fileStmt = $pdo->prepare("SELECT * FROM padlet_post_files WHERE post_id IN ($marks) ORDER BY id"); $fileStmt->execute($postIds);
        foreach ($fileStmt->fetchAll() as $file) { $file['id'] = (int)$file['id']; $filesByPost[(int)$file['post_id']][] = $file; }
        $commentStmt = $pdo->prepare("SELECT * FROM padlet_comments WHERE post_id IN ($marks) ORDER BY created_at ASC"); $commentStmt->execute($postIds);
        foreach ($commentStmt->fetchAll() as $comment) { $comment['id'] = (int)$comment['id']; $commentsByPost[(int)$comment['post_id']][] = $comment; }
        $reactionStmt = $pdo->prepare("SELECT post_id, reaction, COUNT(*) AS count FROM padlet_reactions WHERE post_id IN ($marks) GROUP BY post_id, reaction"); $reactionStmt->execute($postIds);
        foreach ($reactionStmt->fetchAll() as $reaction) $reactionsByPost[(int)$reaction['post_id']][$reaction['reaction']] = (int)$reaction['count'];
    }
    foreach ($posts as &$post) {
        $post['id'] = (int)$post['id']; $post['column_id'] = $post['column_id'] ? (int)$post['column_id'] : null; $post['pinned'] = (bool)$post['pinned'];
        $post['files'] = $filesByPost[(int)$post['id']] ?? []; $post['comments'] = $commentsByPost[(int)$post['id']] ?? []; $post['reactions'] = $reactionsByPost[(int)$post['id']] ?? [];
    }
    return ['board' => $board, 'columns' => $columns, 'posts' => $posts];
}

padlet_schema($pdo);
padlet_migrate($pdo);
$method = $_SERVER['REQUEST_METHOD'];
$action = trim((string)($_GET['action'] ?? ''));

if ($method === 'GET' && $action === 'manager') {
    $teacher = padlet_require_teacher($pdo);
    $stmt = $pdo->prepare("SELECT b.*, COUNT(DISTINCT p.id) AS post_count, SUM(p.status = 'pending') AS pending_count FROM padlet_boards b LEFT JOIN padlet_posts p ON p.board_id = b.id WHERE b.owner_id = ? GROUP BY b.id ORDER BY b.created_at DESC");
    $stmt->execute([(int)$teacher['id']]);
    $boards = $stmt->fetchAll();
    foreach ($boards as &$board) { $board['id'] = (int)$board['id']; $board['post_count'] = (int)$board['post_count']; $board['pending_count'] = (int)$board['pending_count']; }
    respond(['ok' => true, 'user' => public_user($teacher), 'boards' => $boards]);
}

if ($method === 'GET' && $action === 'board-detail') {
    $teacher = padlet_require_teacher($pdo);
    $board = padlet_require_owner($pdo, $teacher, (int)($_GET['id'] ?? 0));
    respond(['ok' => true, 'board' => $board, 'columns' => padlet_columns($pdo, (int)$board['id'])]);
}

if ($method === 'GET' && $action === 'classes') {
    padlet_require_teacher($pdo);
    $classes = $pdo->query("SELECT DISTINCT TRIM(class_name) AS class_name FROM users WHERE role = 'student' AND class_name IS NOT NULL AND TRIM(class_name) <> '' ORDER BY class_name")->fetchAll(PDO::FETCH_COLUMN);
    respond(['ok' => true, 'classes' => $classes]);
}

if ($method === 'GET' && $action === 'link-preview') {
    $url = trim((string)($_GET['url'] ?? ''));
    if ($url === '' || !filter_var($url, FILTER_VALIDATE_URL)) respond(['error' => 'Liên kết không hợp lệ.'], 422);
    $preview = padlet_link_preview($url);
    respond(['ok' => true, 'preview' => $preview, 'youtube_id' => padlet_youtube_id($url)]);
}

if ($method === 'POST' && $action === 'save-board') {
    $teacher = padlet_require_teacher($pdo); $data = json_body(); $id = (int)($data['id'] ?? 0);
    $title = trim((string)($data['title'] ?? '')); if ($title === '') respond(['error' => 'Vui lòng nhập tên bảng.'], 422);
    $layout = padlet_layout_type((string)($data['layout_type'] ?? 'wall'));
    $bgTheme = padlet_bg_theme((string)($data['bg_theme'] ?? 'teal'));
    $access = ($data['access_mode'] ?? '') === 'class' ? 'class' : 'public';
    $targetClass = $access === 'class' ? trim((string)($data['target_class'] ?? '')) : '';
    if ($access === 'class' && $targetClass === '') respond(['error' => 'Vui lòng chọn lớp cho bảng theo lớp.'], 422);
    $columns = padlet_normalize_columns($data['columns'] ?? []);
    $academic = trim((string)($data['academic_year'] ?? ''));
    $status = ($data['status'] ?? '') === 'closed' ? 'closed' : 'open';
    $pdo->beginTransaction();
    try {
        if ($id) {
            $board = padlet_require_owner($pdo, $teacher, $id);
            $stmt = $pdo->prepare('UPDATE padlet_boards SET title=?, description=?, layout_type=?, bg_theme=?, access_mode=?, target_class=?, status=?, academic_year=?, moderation_enabled=?, comments_enabled=?, reactions_enabled=? WHERE id=?');
            $stmt->execute([$title, trim((string)($data['description'] ?? '')), $layout, $bgTheme, $access, $targetClass ?: null, $status, $academic ?: null, !empty($data['moderation_enabled']) ? 1 : 0, !empty($data['comments_enabled']) ? 1 : 0, !empty($data['reactions_enabled']) ? 1 : 0, $id]);
        } else {
            $code = padlet_code($pdo);
            $stmt = $pdo->prepare('INSERT INTO padlet_boards (public_code, owner_id, title, description, layout_type, bg_theme, access_mode, target_class, status, academic_year, moderation_enabled, comments_enabled, reactions_enabled) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)');
            $stmt->execute([$code, (int)$teacher['id'], $title, trim((string)($data['description'] ?? '')), $layout, $bgTheme, $access, $targetClass ?: null, $status, $academic ?: null, !empty($data['moderation_enabled']) ? 1 : 0, !empty($data['comments_enabled']) ? 1 : 0, !empty($data['reactions_enabled']) ? 1 : 0]);
            $id = (int)$pdo->lastInsertId();
        }
        // Keep IDs of existing columns because posts reference them. If a column is
        // removed, move its posts to the first remaining column before deleting it.
        $current = padlet_columns($pdo, $id);
        $currentById = [];
        foreach ($current as $item) $currentById[(int)$item['id']] = $item;
        $seen = [];
        $insertColumn = $pdo->prepare('INSERT INTO padlet_columns (board_id, title, color, order_index) VALUES (?, ?, ?, ?)');
        $updateColumn = $pdo->prepare('UPDATE padlet_columns SET title = ?, color = ?, order_index = ? WHERE id = ? AND board_id = ?');
        $resolvedColumns = [];
        foreach ($columns as $index => $column) {
            $columnId = (int)($column['id'] ?? 0);
            if ($columnId && isset($currentById[$columnId])) {
                $updateColumn->execute([$column['title'], $column['color'], $index, $columnId, $id]);
            } else {
                $insertColumn->execute([$id, $column['title'], $column['color'], $index]);
                $columnId = (int)$pdo->lastInsertId();
            }
            $seen[$columnId] = true;
            $resolvedColumns[] = $columnId;
        }
        $fallbackColumnId = $resolvedColumns[0];
        $movePosts = $pdo->prepare('UPDATE padlet_posts SET column_id = ? WHERE board_id = ? AND column_id = ?');
        $deleteColumn = $pdo->prepare('DELETE FROM padlet_columns WHERE id = ? AND board_id = ?');
        foreach ($currentById as $columnId => $_column) {
            if (isset($seen[$columnId])) continue;
            $movePosts->execute([$fallbackColumnId, $id, $columnId]);
            $deleteColumn->execute([$columnId, $id]);
        }
        $pdo->commit();
    } catch (Throwable $e) { if ($pdo->inTransaction()) $pdo->rollBack(); throw $e; }
    respond(['ok' => true, 'board' => padlet_board($pdo, $id)]);
}

if ($method === 'POST' && $action === 'delete-board') {
    $teacher = padlet_require_teacher($pdo); $data = json_body(); $board = padlet_require_owner($pdo, $teacher, (int)($data['id'] ?? 0)); $id = (int)$board['id'];
    $pdo->beginTransaction();
    try {
        $pdo->prepare('DELETE f FROM padlet_post_files f INNER JOIN padlet_posts p ON p.id = f.post_id WHERE p.board_id = ?')->execute([$id]);
        $pdo->prepare('DELETE c FROM padlet_comments c INNER JOIN padlet_posts p ON p.id = c.post_id WHERE p.board_id = ?')->execute([$id]);
        $pdo->prepare('DELETE r FROM padlet_reactions r INNER JOIN padlet_posts p ON p.id = r.post_id WHERE p.board_id = ?')->execute([$id]);
        $pdo->prepare('DELETE FROM padlet_posts WHERE board_id = ?')->execute([$id]); $pdo->prepare('DELETE FROM padlet_columns WHERE board_id = ?')->execute([$id]); $pdo->prepare('DELETE FROM padlet_boards WHERE id = ?')->execute([$id]); $pdo->commit();
    } catch (Throwable $e) { if ($pdo->inTransaction()) $pdo->rollBack(); throw $e; }
    respond(['ok' => true, 'message' => 'Đã xóa bảng và dữ liệu hệ thống. Tệp trên Drive được giữ lại để an toàn.']);
}

if ($method === 'GET' && $action === 'board') {
    $board = padlet_board($pdo, 0, (string)($_GET['code'] ?? '')); if (!$board) respond(['error' => 'Không tìm thấy bảng chia sẻ.'], 404);
    $user = padlet_current_user($pdo); $accessUser = padlet_access($pdo, $board, $user); $canManage = $accessUser && ($accessUser['role'] ?? '') === 'teacher' && (int)$board['owner_id'] === (int)$accessUser['id'];
    $payload = padlet_payload($pdo, $board, $canManage);
    $payload['ok'] = true; $payload['can_manage'] = $canManage; $payload['user'] = $accessUser ? public_user($accessUser) : null;
    respond($payload);
}

if ($method === 'POST' && $action === 'post') {
    $board = padlet_board($pdo, 0, (string)($_POST['code'] ?? '')); if (!$board) respond(['error' => 'Không tìm thấy bảng chia sẻ.'], 404);
    if ($board['status'] !== 'open') respond(['error' => 'Bảng này đã đóng, không nhận bài đăng mới.'], 403);
    $user = padlet_access($pdo, $board, padlet_current_user($pdo));
    $body = trim((string)($_POST['body'] ?? '')); $link = trim((string)($_POST['link_url'] ?? ''));
    if ($link !== '' && !filter_var($link, FILTER_VALIDATE_URL)) respond(['error' => 'Liên kết không hợp lệ.'], 422);
    if ($user) { $name = $user['full_name']; $role = $user['role'] === 'teacher' ? 'Giáo viên' : 'Học sinh'; $group = $user['class_name'] ?? ''; }
    else { $name = trim((string)($_POST['author_name'] ?? '')); $role = trim((string)($_POST['author_role'] ?? '')); $group = trim((string)($_POST['author_group'] ?? '')); if ($name === '') respond(['error' => 'Vui lòng nhập họ tên người đăng.'], 422); }
    $files = array_values(array_filter(padlet_file_input(), fn($file) => (int)$file['error'] !== UPLOAD_ERR_NO_FILE));
    if ($body === '' && $link === '' && !$files) respond(['error' => 'Hãy nhập nội dung, liên kết hoặc đính kèm tệp.'], 422);
    if (count($files) > 5) respond(['error' => 'Mỗi bài đăng tối đa 5 tệp.'], 422);
    $columnId = (int)($_POST['column_id'] ?? 0); $columnStmt = $pdo->prepare('SELECT id, title FROM padlet_columns WHERE id = ? AND board_id = ? LIMIT 1'); $columnStmt->execute([$columnId, (int)$board['id']]); $column = $columnStmt->fetch();
    if (!$column) { $columns = padlet_columns($pdo, (int)$board['id']); $column = $columns[0] ?? null; } if (!$column) respond(['error' => 'Bảng chưa có cột để đăng bài.'], 422);
    $colors = ['white','sky','amber','violet','rose','emerald']; $cardColor = in_array(($_POST['card_color'] ?? ''), $colors, true) ? $_POST['card_color'] : 'white';
    $linkTitle = trim((string)($_POST['link_title'] ?? ''));
    $linkImage = trim((string)($_POST['link_image'] ?? ''));
    if ($link !== '' && ($linkTitle === '' || $linkImage === '')) {
        $preview = padlet_link_preview($link);
        if ($linkTitle === '') $linkTitle = $preview['title'] ?: '';
        if ($linkImage === '') $linkImage = $preview['image'] ?: '';
    }
    $locationLabel = padlet_trim_text(trim((string)($_POST['location_label'] ?? '')), 200);
    $mapLat = $_POST['map_lat'] ?? null;
    $mapLng = $_POST['map_lng'] ?? null;
    $mapLat = is_numeric($mapLat) ? round((float)$mapLat, 7) : null;
    $mapLng = is_numeric($mapLng) ? round((float)$mapLng, 7) : null;
    if ($mapLat !== null && ($mapLat < -90 || $mapLat > 90)) $mapLat = null;
    if ($mapLng !== null && ($mapLng < -180 || $mapLng > 180)) $mapLng = null;
    $status = (bool)$board['moderation_enabled'] ? 'pending' : 'published';
    $order = (int)$pdo->query('SELECT COALESCE(MAX(order_index), 0) + 1 FROM padlet_posts WHERE board_id = ' . (int)$board['id'])->fetchColumn();
    $pdo->beginTransaction();
    try {
        $stmt = $pdo->prepare('INSERT INTO padlet_posts (board_id, column_id, author_user_id, author_name, author_role, author_group, body, link_url, link_title, link_image, location_label, map_lat, map_lng, card_color, status, order_index) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)');
        $stmt->execute([(int)$board['id'], (int)$column['id'], $user ? (int)$user['id'] : null, $name, $role ?: null, $group ?: null, $body ?: null, $link ?: null, $linkTitle ?: null, $linkImage ?: null, $locationLabel ?: null, $mapLat, $mapLng, $cardColor, $status, $order]); $postId = (int)$pdo->lastInsertId();
        $pdo->commit();
    } catch (Throwable $e) { if ($pdo->inTransaction()) $pdo->rollBack(); throw $e; }
    if ($files) {
        $folderId = trim((string)($board['drive_folder_id'] ?? ''));
        if ($folderId === '') { $folderId = drive_board_folder($board['public_code'], $board['title'], $board['academic_year'] ?? null); $pdo->prepare("UPDATE padlet_boards SET drive_folder_id = ? WHERE id = ? AND (drive_folder_id IS NULL OR drive_folder_id = '')")->execute([$folderId, (int)$board['id']]); }
        $columnFolder = drive_get_or_create_folder($folderId, (string)$column['title']); $personFolder = drive_participant_folder($columnFolder, $group, $name, date('Ymd-His'));
        $insertFile = $pdo->prepare('INSERT INTO padlet_post_files (post_id, drive_file_id, original_name, stored_name, mime_type, size_bytes, view_url, download_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
        foreach ($files as $index => $file) {
            if ((int)$file['error'] !== UPLOAD_ERR_OK || !is_uploaded_file($file['tmp_name'])) continue;
            if ((int)$file['size'] > 25 * 1024 * 1024) respond(['error' => 'Mỗi tệp bảng chia sẻ tối đa 25 MB.'], 422);
            $original = (string)$file['name']; $mime = function_exists('finfo_open') ? (string)(new finfo(FILEINFO_MIME_TYPE))->file($file['tmp_name']) : ((string)$file['type'] ?: 'application/octet-stream');
            $drive = drive_upload_file($personFolder, date('Ymd-His') . '-' . ($index + 1) . '-' . drive_safe_name($original), $mime, $file['tmp_name']);
            $insertFile->execute([$postId, $drive['file_id'], $original, $drive['stored_name'], $mime, (int)$file['size'], $drive['view_url'], $drive['download_url']]);
        }
    }
    respond(['ok' => true, 'message' => $status === 'pending' ? 'Bài đăng đã gửi và đang chờ giáo viên duyệt.' : 'Bài đăng đã xuất hiện trên bảng.']);
}

if ($method === 'POST' && $action === 'comment') {
    $data = json_body(); $board = padlet_board($pdo, 0, (string)($data['code'] ?? '')); if (!$board) respond(['error' => 'Không tìm thấy bảng.'], 404); if (!(bool)$board['comments_enabled']) respond(['error' => 'Bảng này không cho phép bình luận.'], 403);
    $user = padlet_access($pdo, $board, padlet_current_user($pdo)); $postId = (int)($data['post_id'] ?? 0); $body = trim((string)($data['body'] ?? '')); if ($body === '') respond(['error' => 'Bình luận không được để trống.'], 422);
    $check = $pdo->prepare("SELECT id FROM padlet_posts WHERE id = ? AND board_id = ? AND status = 'published' LIMIT 1"); $check->execute([$postId, (int)$board['id']]); if (!$check->fetch()) respond(['error' => 'Không tìm thấy bài đăng.'], 404);
    $name = $user ? $user['full_name'] : trim((string)($data['author_name'] ?? '')); if ($name === '') respond(['error' => 'Vui lòng nhập họ tên để bình luận.'], 422);
    $role = $user ? (($user['role'] ?? '') === 'teacher' ? 'Giáo viên' : 'Học sinh') : trim((string)($data['author_role'] ?? ''));
    $stmt = $pdo->prepare('INSERT INTO padlet_comments (post_id, author_user_id, author_name, author_role, body) VALUES (?, ?, ?, ?, ?)'); $stmt->execute([$postId, $user ? (int)$user['id'] : null, $name, $role ?: null, padlet_trim_text($body, 1500)]);
    respond(['ok' => true]);
}

if ($method === 'POST' && $action === 'reaction') {
    $data = json_body(); $board = padlet_board($pdo, 0, (string)($data['code'] ?? '')); if (!$board) respond(['error' => 'Không tìm thấy bảng.'], 404); if (!(bool)$board['reactions_enabled']) respond(['error' => 'Bảng này không cho phép phản hồi.'], 403);
    padlet_access($pdo, $board, padlet_current_user($pdo)); $postId = (int)($data['post_id'] ?? 0); $reaction = (string)($data['reaction'] ?? ''); if (!in_array($reaction, ['👍','❤️','⭐'], true)) respond(['error' => 'Phản hồi không hợp lệ.'], 422);
    $check = $pdo->prepare("SELECT id FROM padlet_posts WHERE id = ? AND board_id = ? AND status = 'published' LIMIT 1"); $check->execute([$postId, (int)$board['id']]); if (!$check->fetch()) respond(['error' => 'Không tìm thấy bài đăng.'], 404);
    $visitor = padlet_visitor_key(); $exists = $pdo->prepare('SELECT id FROM padlet_reactions WHERE post_id = ? AND visitor_key = ? AND reaction = ? LIMIT 1'); $exists->execute([$postId, $visitor, $reaction]);
    if ($exists->fetch()) $pdo->prepare('DELETE FROM padlet_reactions WHERE post_id = ? AND visitor_key = ? AND reaction = ?')->execute([$postId, $visitor, $reaction]);
    else $pdo->prepare('INSERT INTO padlet_reactions (post_id, visitor_key, reaction) VALUES (?, ?, ?)')->execute([$postId, $visitor, $reaction]);
    respond(['ok' => true]);
}

if ($method === 'POST' && $action === 'moderate') {
    $teacher = padlet_require_teacher($pdo); $data = json_body(); $board = padlet_require_owner($pdo, $teacher, (int)($data['board_id'] ?? 0)); $postId = (int)($data['post_id'] ?? 0); $operation = (string)($data['operation'] ?? '');
    $check = $pdo->prepare('SELECT id FROM padlet_posts WHERE id = ? AND board_id = ? LIMIT 1'); $check->execute([$postId, (int)$board['id']]); if (!$check->fetch()) respond(['error' => 'Không tìm thấy bài đăng.'], 404);
    if (in_array($operation, ['publish','reject'], true)) $pdo->prepare('UPDATE padlet_posts SET status = ? WHERE id = ?')->execute([$operation === 'publish' ? 'published' : 'rejected', $postId]);
    elseif ($operation === 'pin') $pdo->prepare('UPDATE padlet_posts SET pinned = 1 - pinned WHERE id = ?')->execute([$postId]);
    elseif ($operation === 'delete') { $pdo->prepare('DELETE FROM padlet_post_files WHERE post_id = ?')->execute([$postId]); $pdo->prepare('DELETE FROM padlet_comments WHERE post_id = ?')->execute([$postId]); $pdo->prepare('DELETE FROM padlet_reactions WHERE post_id = ?')->execute([$postId]); $pdo->prepare('DELETE FROM padlet_posts WHERE id = ?')->execute([$postId]); }
    else respond(['error' => 'Thao tác không hợp lệ.'], 422);
    respond(['ok' => true]);
}

if ($method === 'POST' && $action === 'reorder') {
    $teacher = padlet_require_teacher($pdo); $data = json_body(); $board = padlet_require_owner($pdo, $teacher, (int)($data['board_id'] ?? 0)); $type = (string)($data['type'] ?? 'posts'); $ids = array_values(array_filter(array_map('intval', $data['ids'] ?? [])));
    if (!$ids) respond(['error' => 'Không có thứ tự mới.'], 422);
    if ($type === 'columns') {
        $stmt = $pdo->prepare('UPDATE padlet_columns SET order_index = ? WHERE id = ? AND board_id = ?');
        foreach ($ids as $index => $id) $stmt->execute([$index, $id, (int)$board['id']]);
    } else {
        $columnId = (int)($data['column_id'] ?? 0);
        $column = $pdo->prepare('SELECT id FROM padlet_columns WHERE id = ? AND board_id = ? LIMIT 1');
        $column->execute([$columnId, (int)$board['id']]);
        if (!$column->fetch()) respond(['error' => 'Cột đích không hợp lệ.'], 422);
        $stmt = $pdo->prepare('UPDATE padlet_posts SET column_id = ?, order_index = ? WHERE id = ? AND board_id = ?');
        foreach ($ids as $index => $id) $stmt->execute([$columnId, $index, $id, (int)$board['id']]);
    }
    respond(['ok' => true]);
}

respond(['error' => 'Endpoint không tồn tại.'], 404);
