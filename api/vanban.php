<?php
require_once __DIR__ . '/helpers.php';

session_start();

function vbd_current_user(PDO $pdo): array
{
    $userId = (int)($_SESSION['user_id'] ?? 0);
    if ($userId <= 0) respond(['error' => 'Vui lòng đăng nhập lại.'], 401);
    $stmt = $pdo->prepare('SELECT id, username, full_name, role, is_active FROM users WHERE id = ? LIMIT 1');
    $stmt->execute([$userId]);
    $user = $stmt->fetch();
    if (!$user || !(bool)$user['is_active'] || ($user['role'] ?? '') !== 'teacher') {
        respond(['error' => 'Chức năng quản lý văn bản chỉ dành cho giáo viên.'], 403);
    }
    return $user;
}

function vbd_ensure_schema(PDO $pdo): void
{
    $pdo->exec("CREATE TABLE IF NOT EXISTS office_documents (
        id INT AUTO_INCREMENT PRIMARY KEY,
        owner_id INT NOT NULL,
        academic_year VARCHAR(40) NOT NULL DEFAULT '',
        direction VARCHAR(12) NOT NULL DEFAULT 'incoming',
        document_number VARCHAR(160) DEFAULT NULL,
        title VARCHAR(500) NOT NULL,
        document_date DATE DEFAULT NULL,
        organization VARCHAR(300) DEFAULT NULL,
        document_type VARCHAR(120) DEFAULT NULL,
        summary_text TEXT DEFAULT NULL,
        source_text MEDIUMTEXT DEFAULT NULL,
        report_required TINYINT(1) NOT NULL DEFAULT 0,
        report_due_at DATE DEFAULT NULL,
        report_status VARCHAR(24) NOT NULL DEFAULT 'not_required',
        report_note TEXT DEFAULT NULL,
        reported_at DATETIME DEFAULT NULL,
        drive_folder_id VARCHAR(160) DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_office_documents_owner (owner_id),
        INDEX idx_office_documents_year (academic_year),
        INDEX idx_office_documents_due (report_due_at),
        INDEX idx_office_documents_direction (direction)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    $pdo->exec("CREATE TABLE IF NOT EXISTS office_school_years (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(40) NOT NULL UNIQUE,
        created_by INT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_office_school_years_name (name)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

    try {
        $column = $pdo->query("SHOW COLUMNS FROM office_documents LIKE 'academic_year'")->fetch();
        if (!$column) $pdo->exec("ALTER TABLE office_documents ADD COLUMN academic_year VARCHAR(40) NOT NULL DEFAULT '' AFTER owner_id");
    } catch (Throwable $e) {
        // Existing installations may need the column added manually if ALTER TABLE is restricted.
    }

    try {
        $column = $pdo->query("SHOW COLUMNS FROM office_documents LIKE 'sector'")->fetch();
        if (!$column) {
            $pdo->exec("ALTER TABLE office_documents ADD COLUMN sector VARCHAR(20) NOT NULL DEFAULT 'hanhchinh' AFTER academic_year");
            $pdo->exec("UPDATE office_documents SET sector = 'hanhchinh' WHERE sector IS NULL OR TRIM(sector) = ''");
        }
    } catch (Throwable $e) {
        // Existing installations may need the column added manually if ALTER TABLE is restricted.
    }

    $pdo->exec("CREATE TABLE IF NOT EXISTS office_document_files (
        id INT AUTO_INCREMENT PRIMARY KEY,
        document_id INT NOT NULL,
        drive_file_id VARCHAR(160) NOT NULL,
        original_name VARCHAR(255) NOT NULL,
        stored_name VARCHAR(255) NOT NULL,
        mime_type VARCHAR(160) DEFAULT NULL,
        size_bytes BIGINT NOT NULL DEFAULT 0,
        view_url TEXT NOT NULL,
        download_url TEXT DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_office_document_files_document (document_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}

function vbd_direction(string $value): string
{
    return in_array($value, ['incoming', 'outgoing'], true) ? $value : 'incoming';
}

function vbd_sector(string $value): string
{
    return in_array($value, ['hanhchinh', 'dang'], true) ? $value : 'hanhchinh';
}

function vbd_sector_label(string $sector): string
{
    return $sector === 'dang' ? 'Đảng' : 'Hành chính';
}

function vbd_status(string $value, bool $required): string
{
    if (!$required) return 'not_required';
    return in_array($value, ['pending', 'in_progress', 'completed'], true) ? $value : 'pending';
}

function vbd_date($value): ?string
{
    $value = trim((string)$value);
    if ($value === '') return null;
    $time = strtotime($value);
    return $time ? date('Y-m-d', $time) : null;
}

function vbd_academic_year($value): string
{
    return vbd_truncate(trim((string)$value), 40);
}

function vbd_truncate(string $value, int $length): string
{
    return function_exists('mb_substr') ? mb_substr($value, 0, $length) : substr($value, 0, $length);
}

function vbd_effective_status(array $document): string
{
    if (!(bool)$document['report_required']) return 'not_required';
    if (($document['report_status'] ?? '') === 'completed') return 'completed';
    $due = vbd_date($document['report_due_at'] ?? null);
    if ($due && $due < date('Y-m-d')) return 'overdue';
    return ($document['report_status'] ?? '') === 'in_progress' ? 'in_progress' : 'pending';
}

function vbd_document(PDO $pdo, int $id, int $ownerId): ?array
{
    $stmt = $pdo->prepare('SELECT * FROM office_documents WHERE id = ? AND owner_id = ? LIMIT 1');
    $stmt->execute([$id, $ownerId]);
    $document = $stmt->fetch();
    return $document ?: null;
}

function vbd_files(PDO $pdo, array $ids): array
{
    if (!$ids) return [];
    $placeholders = implode(',', array_fill(0, count($ids), '?'));
    $stmt = $pdo->prepare("SELECT * FROM office_document_files WHERE document_id IN ($placeholders) ORDER BY id ASC");
    $stmt->execute($ids);
    $result = [];
    foreach ($stmt->fetchAll() as $file) $result[(int)$file['document_id']][] = $file;
    return $result;
}

function vbd_preprocess_source(string $source): string
{
    $lines = preg_split('/\R/u', $source) ?: [];
    $skipKeywords = [
        'ký bởi', 'ngày ký', 'ky boi', 'ngay ky', 'digitally signed', 'certificate',
        'mã xác thực', 'ma xac thuc', 'signature valid', 'signed by', 'chữ ký số',
        'chu ky so', 'xác thực bởi', 'xac thuc boi', 'valid from', 'signing time',
        'timestamp', 'ocsp', 'certificate authority',
    ];
    $filtered = [];
    foreach ($lines as $line) {
        $lower = function_exists('mb_strtolower') ? mb_strtolower($line) : strtolower($line);
        $skip = false;
        foreach ($skipKeywords as $keyword) {
            if (str_contains($lower, $keyword)) {
                $skip = true;
                break;
            }
        }
        if (!$skip) {
            $filtered[] = trim($line);
        }
    }
    $text = trim(implode("\n", $filtered));
    $text = preg_replace('/[ \t]+/u', ' ', $text) ?? $text;
    $text = preg_replace('/\n{3,}/u', "\n\n", $text) ?? $text;
    return trim($text);
}

function vbd_parse_vn_date(string $text): ?string
{
    if (preg_match('/ngày\s*(\d{1,2})\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})/iu', $text, $match)) {
        return sprintf('%04d-%02d-%02d', (int)$match[3], (int)$match[2], (int)$match[1]);
    }
    if (preg_match('/\b(\d{1,2})[\/\-.](\d{1,2})[\/\-.](\d{4})\b/', $text, $match)) {
        return sprintf('%04d-%02d-%02d', (int)$match[3], (int)$match[2], (int)$match[1]);
    }
    return null;
}

function vbd_regex_extract(string $source): array
{
    $text = vbd_preprocess_source($source);
    $head = function_exists('mb_substr') ? mb_substr($text, 0, 3200) : substr($text, 0, 3200);
    $result = [
        'document_number' => '',
        'title' => '',
        'organization' => '',
        'document_type' => '',
        'summary_text' => '',
        'document_date' => null,
        'report_required' => false,
        'report_due_at' => null,
    ];

    $numberPatterns = [
        '/(?:Số|So)\s*(?:văn bản|van ban)?\s*[:\.]?\s*([0-9]{1,6}\s*\/\s*[A-Za-zÀ-ỹ0-9.\-]+)/iu',
        '/(?:Ký hiệu|Ky hieu)\s*[:\.]?\s*([0-9]{1,6}\s*\/\s*[A-Za-zÀ-ỹ0-9.\-]+)/iu',
        '/\b([0-9]{1,6}\/[A-ZĐ]{2,}(?:-[A-Z0-9]+)*(?:\/[A-Z0-9.\-]+)?)\b/u',
        '/\b([0-9]{1,6}-[A-Z]{2,}(?:-[A-Z0-9]+)+)\b/u',
    ];
    foreach ($numberPatterns as $pattern) {
        if (preg_match($pattern, $head, $match)) {
            $result['document_number'] = trim(preg_replace('/\s+/u', '', $match[1]) ?? $match[1]);
            break;
        }
    }

    $orgPatterns = [
        '/((?:ỦY BAN NHÂN DÂN|UBND|PHÒNG GIÁO DỤC|PHÒNG GD|PHONG GD|PHÒNG|PHONG|TRƯỜNG|TRUONG|BAN THƯỜNG VỤ|BAN CHẤP HÀNH|ĐẢNG ỦY|DANG UY|ĐẢNG BỘ|CHI BỘ|CHI UY|SỞ GD|PGD|BỘ GD)[^\n]{0,120})/iu',
    ];
    foreach ($orgPatterns as $pattern) {
        if (preg_match($pattern, $head, $match)) {
            $org = trim(preg_replace('/\s+/u', ' ', $match[1]) ?? $match[1]);
            if (strlen($org) >= 4) {
                $result['organization'] = vbd_truncate($org, 300);
                break;
            }
        }
    }

    $types = ['Công văn', 'Thông báo', 'Quyết định', 'Kế hoạch', 'Tờ trình', 'Báo cáo', 'Hướng dẫn', 'Thông tư', 'Quy định', 'Chỉ thị', 'Nghị quyết'];
    foreach ($types as $type) {
        if (stripos($head, $type) !== false) {
            $result['document_type'] = $type;
            break;
        }
    }

    if (preg_match('/,\s*ngày\s*(\d{1,2})\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})/iu', $head, $match)) {
        $result['document_date'] = sprintf('%04d-%02d-%02d', (int)$match[3], (int)$match[2], (int)$match[1]);
    } else {
        $result['document_date'] = vbd_parse_vn_date($head);
    }

    if (preg_match('/(?:V\/v|Về việc|Trích yếu|VE VIEC)\s*[:\.]?\s*([^\n]{8,240})/iu', $text, $match)) {
        $result['title'] = vbd_truncate(trim($match[1]), 500);
    } elseif (preg_match('/(?:V\/v|Về việc)\s*([^\n]{8,240})/iu', $text, $match)) {
        $result['title'] = vbd_truncate(trim($match[1]), 500);
    }

    if (preg_match('/(?:báo cáo|bao cao|hoàn thành trước|hạn nộp|hạn báo cáo|đề nghị báo cáo)/iu', $text)) {
        $result['report_required'] = true;
    }
    if (preg_match('/(?:trước ngày|hạn|deadline|hoàn thành trước)[^\n]{0,40}?ngày\s*(\d{1,2})\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})/iu', $text, $match)) {
        $result['report_due_at'] = sprintf('%04d-%02d-%02d', (int)$match[3], (int)$match[2], (int)$match[1]);
    }

    if ($result['title'] !== '' && $result['summary_text'] === '') {
        $result['summary_text'] = vbd_truncate($result['title'], 500);
    }

    return $result;
}

function vbd_parse_document(string $source): array
{
    $cleanSource = vbd_preprocess_source($source);
    if (mb_strlen($cleanSource) < 20) {
        throw new RuntimeException('Nội dung văn bản quá ngắn. Chọn PDF có lớp chữ hoặc dán phần đầu văn bản.');
    }

    $parsed = vbd_regex_extract($cleanSource);
    $parsed['document_date'] = vbd_date($parsed['document_date'] ?? null);
    $parsed['report_due_at'] = vbd_date($parsed['report_due_at'] ?? null);
    $parsed['provider'] = 'parser';
    $parsed['model'] = '';

    $filled = array_filter([
        $parsed['document_number'] ?? '',
        $parsed['title'] ?? '',
        $parsed['organization'] ?? '',
        $parsed['document_type'] ?? '',
    ], static fn($v) => trim((string)$v) !== '');
    $count = count($filled);
    $parsed['confidence'] = $count >= 3 ? 'high' : ($count >= 2 ? 'medium' : 'low');
    $parsed['note'] = $count >= 2
        ? 'Tự nhận diện từ nội dung văn bản. Kiểm tra trước khi lưu.'
        : 'Chỉ nhận diện được ít trường — bổ sung thủ công số văn bản, ngày ban hành, trích yếu.';

    return $parsed;
}

function vbd_drive_folder(array $document): string
{
    require_once __DIR__ . '/google_drive.php';
    $root = defined('GOOGLE_DRIVE_ROOT_FOLDER_ID') ? trim((string)GOOGLE_DRIVE_ROOT_FOLDER_ID) : '';
    if ($root === '') throw new RuntimeException('Chưa cấu hình GOOGLE_DRIVE_ROOT_FOLDER_ID trên hosting.');
    $rootFolder = drive_get_or_create_folder($root, '04_QUAN_LY_VAN_BAN');
    $year = vbd_academic_year($document['academic_year'] ?? '');
    if ($year === '') throw new RuntimeException('Cần chọn năm học trước khi tải tệp lên Google Drive.');
    $sectorFolder = drive_get_or_create_folder($rootFolder, vbd_sector((string)($document['sector'] ?? 'hanhchinh')) === 'dang' ? 'DANG' : 'HANH_CHINH');
    $yearFolder = drive_get_or_create_folder($sectorFolder, 'NAM_HOC_' . drive_safe_name($year, 'NAM_HOC'));
    $kindFolder = drive_get_or_create_folder($yearFolder, $document['direction'] === 'outgoing' ? 'VAN_BAN_DI' : 'VAN_BAN_DEN');
    $label = trim((string)($document['document_number'] ?? '')) ?: ('VB-' . (int)$document['id']);
    return drive_get_or_create_folder($kindFolder, drive_safe_name($label . ' - ' . $document['title'], 'Van ban'));
}

function vbd_uploaded_files(string $key): array
{
    if (empty($_FILES[$key])) return [];
    $input = $_FILES[$key];
    if (!is_array($input['name'])) return [$input];
    $files = [];
    foreach ($input['name'] as $index => $name) {
        $files[] = [
            'name' => $name,
            'type' => $input['type'][$index] ?? '',
            'tmp_name' => $input['tmp_name'][$index] ?? '',
            'error' => $input['error'][$index] ?? UPLOAD_ERR_NO_FILE,
            'size' => $input['size'][$index] ?? 0,
        ];
    }
    return $files;
}

vbd_ensure_schema($pdo);
$user = vbd_current_user($pdo);
$action = (string)($_GET['action'] ?? $_POST['action'] ?? 'list');

if ($action === 'list') {
    $sectorFilter = trim((string)($_GET['sector'] ?? ''));
    if ($sectorFilter !== '') {
        $sectorFilter = vbd_sector($sectorFilter);
        $stmt = $pdo->prepare('SELECT * FROM office_documents WHERE owner_id = ? AND sector = ? ORDER BY COALESCE(report_due_at, document_date, DATE(created_at)) ASC, id DESC');
        $stmt->execute([(int)$user['id'], $sectorFilter]);
    } else {
        $stmt = $pdo->prepare('SELECT * FROM office_documents WHERE owner_id = ? ORDER BY COALESCE(report_due_at, document_date, DATE(created_at)) ASC, id DESC');
        $stmt->execute([(int)$user['id']]);
    }
    $documents = $stmt->fetchAll();
    $files = vbd_files($pdo, array_map(static fn(array $row): int => (int)$row['id'], $documents));
    foreach ($documents as &$document) {
        $document['files'] = $files[(int)$document['id']] ?? [];
        $document['effective_status'] = vbd_effective_status($document);
    }
    unset($document);
    $years = $pdo->query('SELECT name FROM office_school_years ORDER BY name DESC')->fetchAll(PDO::FETCH_COLUMN);
    require_once __DIR__ . '/google_drive.php';
    $driveStatus = drive_setup_status();
    respond([
        'ok' => true,
        'documents' => $documents,
        'school_years' => $years,
        'drive_configured' => (bool)($driveStatus['drive_configured'] ?? false),
        'drive_ready' => (bool)($driveStatus['drive_ready'] ?? false),
        'drive_auth_type' => (string)($driveStatus['drive_auth_type'] ?? 'none'),
        'drive_hint' => (string)($driveStatus['drive_hint'] ?? ''),
        'drive_service_account_email' => (string)($driveStatus['drive_service_account_email'] ?? ''),
        'drive_root_folder_id' => (string)($driveStatus['drive_root_folder_id'] ?? ''),
        'drive_root_folder_name' => (string)($driveStatus['drive_root_folder_name'] ?? ''),
        'drive_in_shared_drive' => $driveStatus['drive_in_shared_drive'] ?? null,
        'drive_can_upload' => $driveStatus['drive_can_upload'] ?? null,
        'user' => ['name' => $user['full_name'], 'username' => $user['username']],
    ]);
}

if ($action === 'create_school_year') {
    $input = json_body();
    $year = vbd_academic_year($input['academic_year'] ?? '');
    if ($year === '') respond(['error' => 'Nhập tên năm học, ví dụ 2025-2026.'], 422);
    try {
        $stmt = $pdo->prepare('INSERT INTO office_school_years (name, created_by) VALUES (?, ?)');
        $stmt->execute([$year, (int)$user['id']]);
    } catch (Throwable $e) {
        // Unique name means the school year was already created by another teacher.
    }
    respond(['ok' => true, 'academic_year' => $year, 'message' => 'Đã tạo hoặc chọn năm học ' . $year . '.']);
}

if ($action === 'parse_document' || $action === 'ai_suggest') {
    $input = json_body();
    $source = trim((string)($input['source_text'] ?? ''));
    if (mb_strlen(vbd_preprocess_source($source)) < 20) {
        respond(['error' => 'Chưa đủ nội dung để nhận diện. Chọn PDF hoặc dán phần đầu văn bản (số, ngày, trích yếu).'], 422);
    }
    try {
        respond(['ok' => true, 'suggestion' => vbd_parse_document($source)]);
    } catch (Throwable $e) {
        respond(['error' => $e->getMessage()], 422);
    }
}

if ($action === 'save') {
    $input = json_body();
    $id = (int)($input['id'] ?? 0);
    $title = trim((string)($input['title'] ?? ''));
    if ($title === '') respond(['error' => 'Cần nhập trích yếu hoặc tên văn bản.'], 422);
    $academicYear = vbd_academic_year($input['academic_year'] ?? '');
    if ($academicYear === '') respond(['error' => 'Cần chọn năm học cho văn bản.'], 422);
    $yearStmt = $pdo->prepare('SELECT id FROM office_school_years WHERE name = ? LIMIT 1');
    $yearStmt->execute([$academicYear]);
    if (!$yearStmt->fetch()) respond(['error' => 'Năm học chưa có trong danh mục. Hãy tạo năm học trước.'], 422);
    $direction = vbd_direction((string)($input['direction'] ?? 'incoming'));
    $sector = vbd_sector((string)($input['sector'] ?? $_GET['sector'] ?? 'hanhchinh'));
    $required = !empty($input['report_required']);
    $status = vbd_status((string)($input['report_status'] ?? ''), $required);
    $values = [
        $academicYear,
        $sector,
        $direction,
        trim((string)($input['document_number'] ?? '')) ?: null,
        vbd_truncate($title, 500),
        vbd_date($input['document_date'] ?? null),
        trim((string)($input['organization'] ?? '')) ?: null,
        trim((string)($input['document_type'] ?? '')) ?: null,
        trim((string)($input['summary_text'] ?? '')) ?: null,
        trim((string)($input['source_text'] ?? '')) ?: null,
        $required ? 1 : 0,
        $required ? vbd_date($input['report_due_at'] ?? null) : null,
        $status,
        trim((string)($input['report_note'] ?? '')) ?: null,
    ];
    if ($id > 0) {
        if (!vbd_document($pdo, $id, (int)$user['id'])) respond(['error' => 'Không tìm thấy văn bản cần sửa.'], 404);
        $reportedAt = $status === 'completed' ? date('Y-m-d H:i:s') : null;
        $stmt = $pdo->prepare('UPDATE office_documents SET academic_year=?, sector=?, direction=?, document_number=?, title=?, document_date=?, organization=?, document_type=?, summary_text=?, source_text=?, report_required=?, report_due_at=?, report_status=?, report_note=?, reported_at=? WHERE id=? AND owner_id=?');
        $stmt->execute(array_merge($values, [$reportedAt, $id, (int)$user['id']]));
    } else {
        $reportedAt = $status === 'completed' ? date('Y-m-d H:i:s') : null;
        $stmt = $pdo->prepare('INSERT INTO office_documents (owner_id, academic_year, sector, direction, document_number, title, document_date, organization, document_type, summary_text, source_text, report_required, report_due_at, report_status, report_note, reported_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)');
        $stmt->execute(array_merge([(int)$user['id']], $values, [$reportedAt]));
        $id = (int)$pdo->lastInsertId();
    }
    $document = vbd_document($pdo, $id, (int)$user['id']);
    respond(['ok' => true, 'document' => $document, 'message' => 'Đã lưu văn bản.']);
}

if ($action === 'update_status') {
    $input = json_body();
    $id = (int)($input['id'] ?? 0);
    $document = vbd_document($pdo, $id, (int)$user['id']);
    if (!$document) respond(['error' => 'Không tìm thấy văn bản.'], 404);
    $status = vbd_status((string)($input['report_status'] ?? ''), true);
    $stmt = $pdo->prepare('UPDATE office_documents SET report_required=1, report_status=?, report_note=?, reported_at=? WHERE id=? AND owner_id=?');
    $stmt->execute([$status, trim((string)($input['report_note'] ?? $document['report_note'] ?? '')) ?: null, $status === 'completed' ? date('Y-m-d H:i:s') : null, $id, (int)$user['id']]);
    respond(['ok' => true, 'message' => 'Đã cập nhật trạng thái báo cáo.']);
}

if ($action === 'upload') {
    $id = (int)($_POST['document_id'] ?? 0);
    $document = vbd_document($pdo, $id, (int)$user['id']);
    if (!$document) respond(['error' => 'Hãy lưu văn bản trước khi tải tệp.'], 404);
    $files = vbd_uploaded_files('files');
    if (!$files) respond(['error' => 'Chưa chọn tệp để tải lên.'], 422);
    $maxBytes = (defined('SUBMISSION_MAX_FILE_MB') ? max(1, (int)SUBMISSION_MAX_FILE_MB) : 25) * 1024 * 1024;
    try {
        require_once __DIR__ . '/google_drive.php';
        drive_assert_upload_ready();
        $folderId = trim((string)($document['drive_folder_id'] ?? '')) ?: vbd_drive_folder($document);
        if (empty($document['drive_folder_id'])) {
            $pdo->prepare('UPDATE office_documents SET drive_folder_id=? WHERE id=?')->execute([$folderId, $id]);
        }
        $insert = $pdo->prepare('INSERT INTO office_document_files (document_id, drive_file_id, original_name, stored_name, mime_type, size_bytes, view_url, download_url) VALUES (?,?,?,?,?,?,?,?)');
        $uploaded = [];
        foreach ($files as $index => $file) {
            if ((int)$file['error'] !== UPLOAD_ERR_OK) throw new RuntimeException('Có tệp tải lên bị lỗi.');
            if ((int)$file['size'] < 1 || (int)$file['size'] > $maxBytes) throw new RuntimeException('Mỗi tệp không được vượt quá ' . ($maxBytes / 1024 / 1024) . ' MB.');
            if (!is_uploaded_file($file['tmp_name'])) throw new RuntimeException('Tệp tải lên không hợp lệ.');
            if ($invalid = drive_validate_upload($file['tmp_name'], (string)$file['name'])) throw new RuntimeException($invalid);
            $mime = drive_detect_mime($file['tmp_name'], (string)$file['name'], (string)$file['type']);
            $storedName = drive_safe_name(($document['document_number'] ?: 'VB-' . $id) . ' - ' . $document['title'] . ' - ' . ($index + 1) . ' - ' . $file['name'], 'van-ban');
            $drive = drive_upload_file($folderId, $storedName, $mime, $file['tmp_name']);
            $insert->execute([$id, $drive['file_id'], $file['name'], $drive['stored_name'], $drive['mime_type'] ?? $mime, (int)$file['size'], $drive['view_url'], $drive['download_url']]);
            $uploaded[] = $drive;
        }
        respond(['ok' => true, 'files' => $uploaded, 'message' => 'Đã lưu tệp lên Google Drive.']);
    } catch (Throwable $e) {
        respond(['error' => $e->getMessage()], 502);
    }
}

if ($action === 'delete') {
    $input = json_body();
    $id = (int)($input['id'] ?? 0);
    if (!vbd_document($pdo, $id, (int)$user['id'])) respond(['error' => 'Không tìm thấy văn bản.'], 404);
    $fileStmt = $pdo->prepare('SELECT drive_file_id, view_url, download_url, original_name FROM office_document_files WHERE document_id=?');
    $fileStmt->execute([$id]);
    $files = $fileStmt->fetchAll();
    try {
        if ($files) {
            require_once __DIR__ . '/google_drive.php';
            $driveErrors = [];
            foreach ($files as $file) {
                $label = trim((string)($file['original_name'] ?? 'Tệp đính kèm'));
                $fileId = drive_resolve_file_id(
                    (string)($file['drive_file_id'] ?? ''),
                    (string)($file['view_url'] ?? ''),
                    (string)($file['download_url'] ?? '')
                );
                if ($fileId === '') {
                    $driveErrors[] = $label . ': không xác định được mã tệp trên Drive';
                    continue;
                }
                try {
                    drive_delete_file($fileId);
                } catch (Throwable $fileError) {
                    $driveErrors[] = $label . ': ' . $fileError->getMessage();
                }
            }
            if ($driveErrors) {
                respond([
                    'error' => 'Không xóa hết tệp trên Google Drive. Danh mục văn bản được giữ nguyên. '
                        . implode(' | ', $driveErrors),
                ], 502);
            }
        }
        $pdo->beginTransaction();
        $pdo->prepare('DELETE FROM office_document_files WHERE document_id=?')->execute([$id]);
        $pdo->prepare('DELETE FROM office_documents WHERE id=? AND owner_id=?')->execute([$id, (int)$user['id']]);
        $pdo->commit();
        respond(['ok' => true, 'message' => 'Đã xóa văn bản và toàn bộ tệp đính kèm trên Google Drive.']);
    } catch (Throwable $e) {
        if ($pdo->inTransaction()) $pdo->rollBack();
        respond(['error' => 'Không thể xóa trọn vẹn văn bản: ' . $e->getMessage()], 502);
    }
}

respond(['error' => 'Thao tác không hợp lệ.'], 400);
