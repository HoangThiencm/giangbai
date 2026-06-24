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
    // Chỉ lấy phần đầu văn bản (header thường nằm trong 2000-2500 ký tự đầu)
    $source = function_exists('mb_substr') ? mb_substr($source, 0, 2500) : substr($source, 0, 2500);

    $lines = preg_split('/\R/u', $source) ?: [];
    $skipKeywords = [
        'ký bởi', 'ngày ký', 'ky boi', 'ngay ky', 'digitally signed', 'certificate',
        'mã xác thực', 'ma xac thuc', 'signature valid', 'signed by', 'chữ ký số',
        'chu ky so', 'xác thực bởi', 'xac thuc boi', 'valid from', 'signing time',
        'timestamp', 'ocsp', 'certificate authority', 'ký số', 'ky so',
        'ngày ký số', 'ngay ky so', 'thời gian ký', 'thoi gian ky',
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

    // Chỉ tìm ở phần đầu văn bản (header) để tránh nhầm với nội dung bên trong hoặc chữ ký số
    $head = function_exists('mb_substr') ? mb_substr($text, 0, 1400) : substr($text, 0, 1400);
    $fullForTitle = function_exists('mb_substr') ? mb_substr($text, 0, 2200) : substr($text, 0, 2200);

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

    // Tìm số văn bản CHÍNH ở phần rất đầu.
    // Hỗ trợ trường hợp text bị tách (Số: rồi sau đó số), hoặc "Số:1176/..." không khoảng trắng.
    // Bỏ qua nếu số nằm sau từ chỉ dẫn chiếu (Căn cứ, Trên cơ sở, Công văn số...)
    $numberPatterns = [
        '/(?:^|[\n\r])\s*(?:Số|So)\s*[:\.]?\s*([0-9]{1,6}\s*\/\s*[A-Za-zÀ-ỹ0-9.\-]+)/iu',
        '/(?:ỦY BAN|PHÒNG|TRƯỜNG|BAN)[^\n]{0,60}?\s*(?:Số|So)\s*[:\.]?\s*([0-9]{1,6}\s*\/\s*[A-Za-zÀ-ỹ0-9.\-]+)/iu',
        '/(?:Số|So)\s*(?:văn bản|van ban)?\s*[:\.]?\s*([0-9]{1,6}\s*\/\s*[A-Za-zÀ-ỹ0-9.\-]+)/iu',
    ];
    foreach ($numberPatterns as $pattern) {
        if (preg_match($pattern, $head, $match)) {
            $num = trim(preg_replace('/\s+/u', '', $match[1]) ?? $match[1]);
            // Kiểm tra context: nếu trước số không có từ dẫn chiếu thì lấy
            $pos = mb_strpos($head, $match[0]);
            $contextBefore = $pos !== false ? mb_substr($head, max(0, $pos - 80), 80) : '';
            if (!preg_match('/(Căn cứ|Trên cơ sở|theo\s*Công văn|Công văn\s*số)\s*$/iu', $contextBefore)) {
                $result['document_number'] = $num;
                break;
            }
        }
    }

    // Fallback mạnh: tìm bất kỳ số dạng NNNN/XXXX-XXXX nào trong 900 ký tự đầu
    // (hữu ích khi text layer tách "Số:" và số ra riêng, hoặc OCR lỗi nhẹ)
    if (empty($result['document_number'])) {
        if (preg_match('/\b([0-9]{3,6}\/[A-ZĐA-Z0-9.\-]{3,})\b/u', $head, $match)) {
            $num = $match[1];
            // Kiểm tra không nằm sau tham chiếu
            $pos = mb_strpos($head, $num);
            $before = $pos !== false ? mb_substr($head, max(0, $pos-100), 100) : '';
            if (!preg_match('/(Căn cứ|Trên cơ sở|theo\s*Công văn|Công văn\s*số)\s*[^0-9]{0,40}$/iu', $before)) {
                $result['document_number'] = $num;
            }
        }
    }

    // Cứu hộ mạnh cho ký số / text layer lỗi: 
    // Nếu thấy "Số" hoặc tên cơ quan ở đầu, quét toàn bộ head để tìm số chính (ưu tiên số đầu tiên sau org)
    if (empty($result['document_number'])) {
        // Tìm số ngay sau "Số:" bất kể có khoảng trắng hay ký tự lạ
        if (preg_match('/Số\s*[:\.]?\s*([0-9]{3,6}\s*\/\s*[A-Za-zÀ-ỹ0-9.\-]+)/iu', $head, $match)) {
            $result['document_number'] = trim(preg_replace('/\s+/u', '', $match[1]));
        } elseif (preg_match('/\b([0-9]{3,6}\/[A-ZĐA-Z0-9.\-]{3,})\b/u', mb_substr($head, 0, 700), $match)) {
            // Lấy số đầu tiên kiểu NNNN/XXXX nếu có "Số" hoặc org name gần đầu
            $earlyContext = mb_substr($head, 0, 400);
            if (preg_match('/(Số|ỦY BAN|PHƯỜNG|PHÒNG)/iu', $earlyContext)) {
                $result['document_number'] = $match[1];
            }
        }
    }

    // Siêu cứu hộ cuối cùng: quét 500 ký tự đầu cho bất kỳ số văn bản nào nếu có "Số:" nhưng chưa có số
    if (empty($result['document_number']) && preg_match('/Số\s*[:\.]?/iu', $head)) {
        if (preg_match('/\b(\d{3,6}\/[A-ZĐA-Z0-9.\-]{2,})\b/u', mb_substr($head, 0, 500), $match)) {
            $result['document_number'] = $match[1];
        }
    }

    // Organization: lấy tên cơ quan ở rất đầu, cắt trước khi gặp "Số:"
    $orgPatterns = [
        '/((?:ỦY BAN NHÂN DÂN|UBND|PHÒNG GIÁO DỤC|PHÒNG GD|PHONG GD|PHÒNG|PHONG|TRƯỜNG|TRUONG|BAN THƯỜNG VỤ|BAN CHẤP HÀNH|ĐẢNG ỦY|DANG UY|ĐẢNG BỘ|CHI BỘ|CHI UY|SỞ GD|PGD|BỘ GD)[^\n]{0,80}?)(?:\n|Số|:)/iu',
        '/((?:ỦY BAN NHÂN DÂN|UBND|PHÒNG GIÁO DỤC|PHÒNG GD|PHONG GD|PHÒNG|PHONG|TRƯỜNG|TRUONG)[^\n]{0,100})/iu',
    ];
    foreach ($orgPatterns as $pattern) {
        if (preg_match($pattern, $head, $match)) {
            $org = trim(preg_replace('/\s+/u', ' ', $match[1]) ?? $match[1]);
            // Loại bỏ phần "Số" nếu bị dính
            $org = preg_replace('/\s*Số\s*:?\s*.*$/iu', '', $org);
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

    // Tìm NGÀY BAN HÀNH sớm nhất ở header (bỏ ngày trong tham chiếu bên dưới)
    $dateHead = mb_substr($head, 0, 900);

    // Ưu tiên pattern có "Hồ Nai, ngày" hoặc tương tự ngay đầu
    if (preg_match('/[A-Za-zÀ-ỹ\.\s]+\s*,\s*ngày\s*(\d{1,2})\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})/iu', $dateHead, $m)) {
        $result['document_date'] = sprintf('%04d-%02d-%02d', (int)$m[3], (int)$m[2], (int)$m[1]);
    } elseif (preg_match('/ngày\s*(\d{1,2})\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})/iu', $dateHead, $m)) {
        // Kiểm tra không nằm sau dòng tham chiếu
        $pos = mb_strpos($dateHead, $m[0]);
        $before = $pos !== false ? mb_substr($dateHead, 0, $pos) : '';
        if (!preg_match('/(Căn cứ|Trên cơ sở|theo|Công văn số)/iu', $before)) {
            $result['document_date'] = sprintf('%04d-%02d-%02d', (int)$m[3], (int)$m[2], (int)$m[1]);
        }
    }

    if (empty($result['document_date'])) {
        $result['document_date'] = vbd_parse_vn_date($dateHead);
    }

    if (preg_match('/(?:V\/v|Về việc|Trích yếu|VE VIEC)\s*[:\.]?\s*([^\n]{8,300})/iu', $fullForTitle, $match)) {
        $result['title'] = vbd_truncate(trim($match[1]), 500);
    } elseif (preg_match('/(?:V\/v|Về việc)\s*([^\n]{8,300})/iu', $fullForTitle, $match)) {
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

    // Luôn giữ summary ngắn gọn, không đổ cả thân văn bản
    if (!empty($result['summary_text']) && mb_strlen($result['summary_text']) > 250) {
        $result['summary_text'] = mb_substr(trim($result['summary_text']), 0, 220) . '...';
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

    // Dọn dẹp summary nếu bị tràn (tránh đổ cả thân văn bản vào tóm tắt)
    if (!empty($parsed['summary_text']) && mb_strlen($parsed['summary_text']) > 280) {
        $parsed['summary_text'] = mb_substr($parsed['summary_text'], 0, 280) . '...';
    }

    // Luôn thử AI cho vanban (quan trọng với ký số / text layer hỗn loạn)
    $aiResult = vbd_try_ai_document_extract($cleanSource);
    if ($aiResult && is_array($aiResult)) {
        $numBad = empty($parsed['document_number']) || 
                  str_starts_with((string)$parsed['document_number'], '/') || 
                  strlen((string)$parsed['document_number']) < 6;

        $hasBodyReference = (bool)preg_match('/(Căn cứ|Trên cơ sở|Công văn số|theo Công văn)/iu', mb_substr($cleanSource, 0, 1200));

        // Dùng AI để sửa nếu regex lấy số kém hoặc có dấu hiệu tham chiếu bên trong
        if ($numBad || empty($parsed['document_date']) || $hasBodyReference) {
            if (!empty($aiResult['document_number'])) $parsed['document_number'] = $aiResult['document_number'];
            if (!empty($aiResult['document_date']))   $parsed['document_date']   = $aiResult['document_date'];
            if (!empty($aiResult['title']) && empty($parsed['title'])) $parsed['title'] = $aiResult['title'];
            if (!empty($aiResult['organization']) && empty($parsed['organization'])) $parsed['organization'] = $aiResult['organization'];
            $parsed['provider'] = 'cloudflare_workers_ai';
            $parsed['model'] = $aiResult['model'] ?? 'document';
            $parsed['note'] = 'Tự nhận diện bằng AI (đã sửa header bị lỗi do ký số / text layer).';
        }
    }

    $parsed['document_date'] = vbd_date($parsed['document_date'] ?? null);
    $parsed['report_due_at'] = vbd_date($parsed['report_due_at'] ?? null);

    if (empty($parsed['provider'])) {
        $parsed['provider'] = 'parser';
        $parsed['model'] = '';
    }

    $filled = array_filter([
        $parsed['document_number'] ?? '',
        $parsed['title'] ?? '',
        $parsed['organization'] ?? '',
        $parsed['document_type'] ?? '',
    ], static fn($v) => trim((string)$v) !== '');
    $count = count($filled);
    $parsed['confidence'] = $count >= 3 ? 'high' : ($count >= 2 ? 'medium' : 'low');
    if (empty($parsed['note'])) {
        $parsed['note'] = $count >= 2
            ? 'Tự nhận diện từ nội dung văn bản. Kiểm tra trước khi lưu.'
            : 'Chỉ nhận diện được ít trường — bổ sung thủ công số văn bản, ngày ban hành, trích yếu.';
    }

    return $parsed;
}

function vbd_try_ai_document_extract(string $source): ?array
{
    // Lấy cấu hình Worker từ config (giống ai_explain)
    $workerUrl = '';
    $secret = '';

    if (defined('CLOUDFLARE_AI_WORKER_URL')) {
        $workerUrl = rtrim(trim((string)CLOUDFLARE_AI_WORKER_URL), '/');
    }
    if (defined('CLOUDFLARE_AI_WORKER_SECRET')) {
        $secret = trim((string)CLOUDFLARE_AI_WORKER_SECRET);
    }

    // Fallback đọc từ global_config.json nếu chưa có
    if (!$workerUrl || !$secret) {
        $globalFile = dirname(__DIR__) . '/global_config.json';
        if (is_file($globalFile)) {
            $g = json_decode((string)@file_get_contents($globalFile), true);
            if (is_array($g)) {
                if (empty($workerUrl) && !empty($g['cloudflare_worker_url'])) {
                    $workerUrl = rtrim(trim($g['cloudflare_worker_url']), '/');
                }
                if (empty($secret) && !empty($g['cloudflare_worker_secret'])) {
                    $secret = trim($g['cloudflare_worker_secret']);
                }
            }
        }
    }

    if (!$workerUrl || !$secret) {
        return null;
    }

    $payload = [
        'mode' => 'document',
        'text' => mb_substr($source, 0, 1800),  // Chỉ gửi phần đầu để AI tập trung header
    ];

    $ch = curl_init($workerUrl . '/chat');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_TIMEOUT => 35,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'X-Giangbai-Worker-Secret: ' . $secret,
        ],
        CURLOPT_POSTFIELDS => json_encode($payload, JSON_UNESCAPED_UNICODE),
    ]);

    $raw = curl_exec($ch);
    $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($status < 200 || $status >= 300 || !$raw) {
        return null;
    }

    $resp = json_decode($raw, true);
    if (!is_array($resp) || empty($resp['ok']) || empty($resp['answer'])) {
        return null;
    }

    // Worker trả về JSON string trong answer
    $json = json_decode($resp['answer'], true);
    if (!is_array($json)) {
        return null;
    }

    return [
        'document_number' => trim((string)($json['document_number'] ?? '')),
        'title' => trim((string)($json['title'] ?? '')),
        'organization' => trim((string)($json['organization'] ?? '')),
        'document_type' => trim((string)($json['document_type'] ?? '')),
        'document_date' => $json['document_date'] ?? null,
        'summary_text' => trim((string)($json['summary_text'] ?? '')),
        'model' => $resp['model'] ?? 'document',
    ];
}

function vbd_local_storage_enabled(): bool
{
    if (defined('VANBAN_LOCAL_STORAGE_FALLBACK')) {
        return (bool)VANBAN_LOCAL_STORAGE_FALLBACK;
    }
    return true;
}

function vbd_local_storage_root(): string
{
    $custom = defined('VANBAN_LOCAL_STORAGE_DIR') ? trim((string)VANBAN_LOCAL_STORAGE_DIR) : '';
    $candidates = array_values(array_filter([
        $custom !== '' ? rtrim($custom, '/\\') : '',
        dirname(__DIR__) . '/storage/vanban',
        __DIR__ . '/storage/vanban',
    ]));
    foreach ($candidates as $path) {
        if (is_dir($path) && is_writable($path)) return $path;
        if (@mkdir($path, 0755, true) && is_dir($path) && is_writable($path)) return $path;
    }
    return $candidates[0] ?? (dirname(__DIR__) . '/storage/vanban');
}

function vbd_request_base_url(): string
{
    $scheme = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
    $host = trim((string)($_SERVER['HTTP_HOST'] ?? 'localhost'));
    $scriptDir = str_replace('\\', '/', dirname((string)($_SERVER['SCRIPT_NAME'] ?? '/api/vanban.php')));
    $root = rtrim(str_replace('/api', '', $scriptDir), '/');
    return $scheme . '://' . $host . ($root !== '' ? $root . '/' : '/');
}

function vbd_local_file_dir(int $documentId, array $document): string
{
    $sector = vbd_sector((string)($document['sector'] ?? 'hanhchinh'));
    $year = preg_replace('/[^0-9-]/', '', (string)($document['academic_year'] ?? 'NAM_HOC')) ?: 'NAM_HOC';
    return vbd_local_storage_root() . '/' . $sector . '/' . $year . '/' . $documentId;
}

function vbd_local_file_path(int $documentId, array $document, string $storedName): string
{
    return vbd_local_file_dir($documentId, $document) . '/' . $storedName;
}

function vbd_local_file_url(int $documentId, string $storedName, bool $download = false): string
{
    $url = vbd_request_base_url() . 'api/vanban.php?action=file&document_id=' . $documentId . '&name=' . rawurlencode($storedName);
    return $download ? $url . '&download=1' : $url;
}

function vbd_is_local_file_id(string $fileId): bool
{
    return str_starts_with(trim($fileId), 'local:');
}

function vbd_is_upload_validation_error(Throwable $e): bool
{
    $msg = $e->getMessage();
    $needles = [
        'Có tệp tải lên bị lỗi',
        'không được vượt quá',
        'Tệp tải lên không hợp lệ',
        'định dạng tệp',
        'Chưa chọn tệp',
    ];
    foreach ($needles as $needle) {
        if (str_contains($msg, $needle)) return true;
    }
    return false;
}

function vbd_should_fallback_to_local(Throwable $e): bool
{
    if (!vbd_local_storage_enabled() || vbd_is_upload_validation_error($e)) return false;
    return true;
}

function vbd_parse_ini_size(string $value): int
{
    $value = trim($value);
    if ($value === '') return 0;
    if (preg_match('/^(\d+(?:\.\d+)?)\s*([KMG])?$/i', $value, $match)) {
        $amount = (float)$match[1];
        $unit = strtoupper($match[2] ?? '');
        $mult = $unit === 'G' ? 1024 * 1024 * 1024 : ($unit === 'M' ? 1024 * 1024 : ($unit === 'K' ? 1024 : 1));
        return (int)floor($amount * $mult);
    }
    return (int)$value;
}

function vbd_upload_chunk_bytes(): int
{
    $configured = defined('VANBAN_UPLOAD_CHUNK_MB') ? max(1, (int)VANBAN_UPLOAD_CHUNK_MB) : 1;
    $chunk = $configured * 1024 * 1024;
    $uploadMax = vbd_parse_ini_size((string)(ini_get('upload_max_filesize') ?: ''));
    if ($uploadMax > 0) {
        // Leave headroom for multipart overhead on shared hosting (often 2M).
        $safe = max(256 * 1024, $uploadMax - 256 * 1024);
        $chunk = min($chunk, $safe);
    }
    return max(256 * 1024, $chunk);
}

function vbd_upload_sessions(): array
{
    if (!isset($_SESSION['vbd_upload_sessions']) || !is_array($_SESSION['vbd_upload_sessions'])) {
        $_SESSION['vbd_upload_sessions'] = [];
    }
    return $_SESSION['vbd_upload_sessions'];
}

function vbd_store_upload_session(array $session): string
{
    $id = bin2hex(random_bytes(16));
    $sessions = vbd_upload_sessions();
    $session['expires_at'] = time() + 7200;
    $sessions[$id] = $session;
    $_SESSION['vbd_upload_sessions'] = $sessions;
    return $id;
}

function vbd_get_upload_session(string $id, int $userId): ?array
{
    $sessions = vbd_upload_sessions();
    $session = $sessions[$id] ?? null;
    if (!is_array($session)) return null;
    if ((int)($session['user_id'] ?? 0) !== $userId) return null;
    if ((int)($session['expires_at'] ?? 0) < time()) return null;
    return $session;
}

function vbd_delete_upload_session(string $id): void
{
    $sessions = vbd_upload_sessions();
    unset($sessions[$id]);
    $_SESSION['vbd_upload_sessions'] = $sessions;
}

function vbd_probe_drive_ready(): ?string
{
    require_once __DIR__ . '/google_drive.php';
    drive_http_set_profile('fast');
    try {
        drive_assert_upload_ready();
        return null;
    } catch (Throwable $e) {
        return $e->getMessage();
    } finally {
        drive_http_set_profile('default');
    }
}

function vbd_boolish($value): bool
{
    if (is_bool($value)) return $value;
    $normalized = strtolower(trim((string)$value));
    return in_array($normalized, ['1', 'true', 'on', 'yes'], true);
}

function vbd_upload_ini_hint(): string
{
    $uploadMb = (int)(ini_get('upload_max_filesize') ?: 0);
    $postMb = (int)(ini_get('post_max_size') ?: 0);
    if ($uploadMb <= 0 && $postMb <= 0) return '';
    return ' Giới hạn hosting hiện tại: upload_max_filesize='
        . (ini_get('upload_max_filesize') ?: '?')
        . ', post_max_size='
        . (ini_get('post_max_size') ?: '?')
        . '.';
}

function vbd_upload_error_message(int $code, string $name): string
{
    $label = $name !== '' ? ('“' . $name . '”') : 'tệp';
    return match ($code) {
        UPLOAD_ERR_INI_SIZE => 'Tệp ' . $label . ' vượt upload_max_filesize trên hosting.' . vbd_upload_ini_hint(),
        UPLOAD_ERR_FORM_SIZE => 'Tệp ' . $label . ' vượt giới hạn form upload.' . vbd_upload_ini_hint(),
        UPLOAD_ERR_PARTIAL => 'Tệp ' . $label . ' chỉ tải lên được một phần. Thử lại.',
        UPLOAD_ERR_NO_FILE => 'Hosting không nhận được nội dung tệp ' . $label . '. Kiểm tra post_max_size/upload_max_filesize.' . vbd_upload_ini_hint(),
        UPLOAD_ERR_NO_TMP_DIR => 'Hosting thiếu thư mục tạm để nhận tệp upload.',
        UPLOAD_ERR_CANT_WRITE => 'Hosting không ghi được tệp tạm khi nhận upload.',
        UPLOAD_ERR_EXTENSION => 'Hosting chặn loại tệp này bằng extension PHP.',
        default => 'Có tệp tải lên bị lỗi (mã ' . $code . ').',
    };
}

function vbd_is_tmp_upload_path(string $tmpName): bool
{
    if ($tmpName === '' || !is_readable($tmpName)) return false;
    if (is_uploaded_file($tmpName)) return true;
    $tmpDir = realpath(sys_get_temp_dir());
    $real = realpath($tmpName);
    return $tmpDir && $real && str_starts_with($real, $tmpDir);
}

function vbd_validate_upload_file(array $file, int $maxBytes): void
{
    $name = trim((string)($file['name'] ?? ''));
    $error = (int)($file['error'] ?? UPLOAD_ERR_NO_FILE);
    if ($error !== UPLOAD_ERR_OK) {
        throw new RuntimeException(vbd_upload_error_message($error, $name));
    }
    if ((int)$file['size'] < 1 || (int)$file['size'] > $maxBytes) {
        throw new RuntimeException('Mỗi tệp không được vượt quá ' . ($maxBytes / 1024 / 1024) . ' MB.');
    }
    if (!vbd_is_tmp_upload_path((string)($file['tmp_name'] ?? ''))) {
        throw new RuntimeException('Tệp tải lên không hợp lệ hoặc hosting chưa nhận được tệp.' . vbd_upload_ini_hint());
    }
    require_once __DIR__ . '/google_drive.php';
    if ($invalid = drive_validate_upload($file['tmp_name'], (string)$file['name'])) {
        throw new RuntimeException($invalid);
    }
}

function vbd_store_local_upload(int $documentId, array $document, array $file, int $index): array
{
    require_once __DIR__ . '/google_drive.php';
    $dir = vbd_local_file_dir($documentId, $document);
    if (!is_dir($dir) && !@mkdir($dir, 0755, true) && !is_dir($dir)) {
        throw new RuntimeException('Không tạo được thư mục lưu tệp trên hosting.');
    }
    $mime = drive_detect_mime($file['tmp_name'], (string)$file['name'], (string)$file['type']);
    $storedName = drive_safe_name(
        ($document['document_number'] ?: 'VB-' . $documentId) . ' - ' . $document['title'] . ' - ' . ($index + 1) . ' - ' . $file['name'],
        'van-ban'
    );
    $dest = vbd_local_file_path($documentId, $document, $storedName);
    if (!move_uploaded_file($file['tmp_name'], $dest)) {
        throw new RuntimeException('Không lưu được tệp trên hosting.');
    }
    return [
        'file_id' => 'local:' . $documentId . ':' . rawurlencode($storedName),
        'stored_name' => $storedName,
        'mime_type' => $mime,
        'view_url' => vbd_local_file_url($documentId, $storedName),
        'download_url' => vbd_local_file_url($documentId, $storedName, true),
        'storage' => 'local',
    ];
}

function vbd_upload_local_files(PDO $pdo, int $id, array $document, array $files, int $maxBytes, ?string $driveError = null): void
{
    $insert = $pdo->prepare('INSERT INTO office_document_files (document_id, drive_file_id, original_name, stored_name, mime_type, size_bytes, view_url, download_url) VALUES (?,?,?,?,?,?,?,?)');
    $uploaded = [];
    foreach ($files as $index => $file) {
        vbd_validate_upload_file($file, $maxBytes);
        $stored = vbd_store_local_upload($id, $document, $file, $index);
        $insert->execute([
            $id,
            $stored['file_id'],
            $file['name'],
            $stored['stored_name'],
            $stored['mime_type'],
            (int)$file['size'],
            $stored['view_url'],
            $stored['download_url'],
        ]);
        $uploaded[] = $stored;
    }
    respond([
        'ok' => true,
        'files' => $uploaded,
        'storage' => 'local',
        'upload_backend' => 'vanban-local-fallback-v3',
        'drive_error' => $driveError,
        'message' => 'Google Drive chưa kết nối được — đã lưu ' . count($uploaded) . ' tệp trên hosting. Khi Drive hoạt động, tải lại tệp để đồng bộ.',
    ]);
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

function vbd_collect_uploaded_files(): array
{
    $files = vbd_uploaded_files('files');
    if ($files) return $files;
    foreach (array_keys($_FILES) as $key) {
        if ($key === 'files' || str_starts_with($key, 'files')) {
            $found = vbd_uploaded_files($key);
            if ($found) return $found;
        }
    }
    return [];
}

function vbd_save_document(PDO $pdo, array $user, array $input): array
{
    $id = (int)($input['id'] ?? 0);
    $title = trim((string)($input['title'] ?? ''));
    if ($title === '') throw new RuntimeException('Cần nhập trích yếu hoặc tên văn bản.');
    $academicYear = vbd_academic_year($input['academic_year'] ?? '');
    if ($academicYear === '') throw new RuntimeException('Cần chọn năm học cho văn bản.');
    $yearStmt = $pdo->prepare('SELECT id FROM office_school_years WHERE name = ? LIMIT 1');
    $yearStmt->execute([$academicYear]);
    if (!$yearStmt->fetch()) throw new RuntimeException('Năm học chưa có trong danh mục. Hãy tạo năm học trước.');
    $direction = vbd_direction((string)($input['direction'] ?? 'incoming'));
    $sector = vbd_sector((string)($input['sector'] ?? $_GET['sector'] ?? 'hanhchinh'));
    $required = vbd_boolish($input['report_required'] ?? false);
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
        if (!vbd_document($pdo, $id, (int)$user['id'])) throw new RuntimeException('Không tìm thấy văn bản cần sửa.');
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
    if (!$document) throw new RuntimeException('Không đọc lại được văn bản sau khi lưu.');
    return $document;
}

function vbd_process_document_upload(PDO $pdo, int $id, array $document, array $files, int $maxBytes): void
{
    try {
        foreach ($files as $file) {
            vbd_validate_upload_file($file, $maxBytes);
        }
    } catch (Throwable $e) {
        respond(['error' => $e->getMessage(), 'upload_backend' => 'vanban-local-fallback-v3'], 422);
    }

    $driveProbeError = vbd_local_storage_enabled() ? vbd_probe_drive_ready() : null;
    if ($driveProbeError !== null) {
        try {
            vbd_upload_local_files($pdo, $id, $document, $files, $maxBytes, $driveProbeError);
        } catch (Throwable $localError) {
            respond([
                'error' => 'Google Drive: ' . $driveProbeError . ' | Lưu trên hosting: ' . $localError->getMessage(),
                'upload_backend' => 'vanban-local-fallback-v3',
            ], 502);
        }
    }

    try {
        require_once __DIR__ . '/google_drive.php';
        $folderId = trim((string)($document['drive_folder_id'] ?? '')) ?: vbd_drive_folder($document);
        if (empty($document['drive_folder_id'])) {
            $pdo->prepare('UPDATE office_documents SET drive_folder_id=? WHERE id=?')->execute([$folderId, $id]);
        }
        $insert = $pdo->prepare('INSERT INTO office_document_files (document_id, drive_file_id, original_name, stored_name, mime_type, size_bytes, view_url, download_url) VALUES (?,?,?,?,?,?,?,?)');
        $uploaded = [];
        foreach ($files as $index => $file) {
            $mime = drive_detect_mime($file['tmp_name'], (string)$file['name'], (string)$file['type']);
            $storedName = drive_safe_name(($document['document_number'] ?: 'VB-' . $id) . ' - ' . $document['title'] . ' - ' . ($index + 1) . ' - ' . $file['name'], 'van-ban');
            $drive = drive_upload_file($folderId, $storedName, $mime, $file['tmp_name']);
            $insert->execute([$id, $drive['file_id'], $file['name'], $drive['stored_name'], $drive['mime_type'] ?? $mime, (int)$file['size'], $drive['view_url'], $drive['download_url']]);
            $uploaded[] = $drive;
        }
        respond([
            'ok' => true,
            'files' => $uploaded,
            'storage' => 'drive',
            'upload_backend' => 'vanban-local-fallback-v3',
            'message' => 'Đã lưu ' . count($uploaded) . ' tệp lên Google Drive.',
        ]);
    } catch (Throwable $e) {
        if (vbd_should_fallback_to_local($e)) {
            try {
                vbd_upload_local_files($pdo, $id, $document, $files, $maxBytes, $e->getMessage());
            } catch (Throwable $localError) {
                respond([
                    'error' => 'Google Drive: ' . $e->getMessage() . ' | Lưu trên hosting: ' . $localError->getMessage(),
                    'upload_backend' => 'vanban-local-fallback-v3',
                ], 502);
            }
        }
        respond([
            'error' => $e->getMessage(),
            'upload_backend' => 'vanban-local-fallback-v3',
        ], 502);
    }
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
    // Only validate the local configuration while loading the dashboard.
    // Do not make every page view depend on Google OAuth/DNS availability.
    $driveStatus = drive_setup_status(false);
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
    try {
        $document = vbd_save_document($pdo, $user, json_body());
        respond(['ok' => true, 'document' => $document, 'message' => 'Đã lưu văn bản.']);
    } catch (RuntimeException $e) {
        respond(['error' => $e->getMessage()], 422);
    }
}

if ($action === 'upload_init') {
    $input = json_body();
    $id = (int)($input['document_id'] ?? 0);
    $document = vbd_document($pdo, $id, (int)$user['id']);
    if (!$document) respond(['error' => 'Hãy lưu văn bản trước khi tải tệp.'], 404);
    $filename = trim((string)($input['filename'] ?? ''));
    $size = (int)($input['size'] ?? 0);
    $mime = trim((string)($input['mime'] ?? '')) ?: 'application/octet-stream';
    $index = max(0, (int)($input['index'] ?? 0));
    $maxBytes = (defined('SUBMISSION_MAX_FILE_MB') ? max(1, (int)SUBMISSION_MAX_FILE_MB) : 25) * 1024 * 1024;
    if ($filename === '') respond(['error' => 'Thiếu tên tệp.'], 422);
    if ($size < 1 || $size > $maxBytes) {
        respond(['error' => 'Mỗi tệp không được vượt quá ' . ($maxBytes / 1024 / 1024) . ' MB.'], 422);
    }
    try {
        require_once __DIR__ . '/google_drive.php';
        drive_assert_upload_ready();
        $folderId = trim((string)($document['drive_folder_id'] ?? '')) ?: vbd_drive_folder($document);
        if (empty($document['drive_folder_id'])) {
            $pdo->prepare('UPDATE office_documents SET drive_folder_id=? WHERE id=?')->execute([$folderId, $id]);
        }
        $storedName = drive_safe_name(
            ($document['document_number'] ?: 'VB-' . $id) . ' - ' . $document['title'] . ' - ' . ($index + 1) . ' - ' . $filename,
            'van-ban'
        );
        $session = drive_begin_resumable_upload($storedName, $mime, $size, [
            'name' => drive_safe_name($storedName),
            'parents' => [$folderId],
        ]);
        $sessionId = vbd_store_upload_session([
            'user_id' => (int)$user['id'],
            'document_id' => $id,
            'upload_url' => $session['upload_url'],
            'mime_type' => $session['mime_type'],
            'stored_name' => $storedName,
            'original_name' => $filename,
            'total_size' => $size,
        ]);
        respond([
            'ok' => true,
            'session_id' => $sessionId,
            'stored_name' => $storedName,
            'mime_type' => $session['mime_type'],
            'chunk_size' => vbd_upload_chunk_bytes(),
            'upload_backend' => 'vanban-chunk-drive-v5',
        ]);
    } catch (Throwable $e) {
        respond(['error' => $e->getMessage(), 'upload_backend' => 'vanban-chunk-drive-v5'], 502);
    }
}

if ($action === 'upload_chunk') {
    @set_time_limit(300);
    $sessionId = trim((string)($_POST['session_id'] ?? ''));
    $offset = (int)($_POST['offset'] ?? 0);
    $total = (int)($_POST['total_size'] ?? 0);
    if ($sessionId === '' || $offset < 0 || $total < 1) {
        respond(['error' => 'Thiếu thông tin phần tệp cần tải.', 'upload_backend' => 'vanban-chunk-drive-v5'], 422);
    }
    $session = vbd_get_upload_session($sessionId, (int)$user['id']);
    if (!$session) {
        respond(['error' => 'Phiên tải lên không hợp lệ hoặc đã hết hạn.', 'upload_backend' => 'vanban-chunk-drive-v5'], 404);
    }
    $document = vbd_document($pdo, (int)($session['document_id'] ?? 0), (int)$user['id']);
    if (!$document) {
        respond(['error' => 'Không tìm thấy văn bản cho phiên tải lên.', 'upload_backend' => 'vanban-chunk-drive-v5'], 404);
    }
    $chunks = vbd_uploaded_files('chunk');
    if (!$chunks) respond(['error' => 'Chưa nhận được phần tệp.', 'upload_backend' => 'vanban-chunk-drive-v5'], 422);
    $chunkFile = $chunks[0];
    $chunkMax = vbd_upload_chunk_bytes();
    try {
        if ((int)$chunkFile['error'] !== UPLOAD_ERR_OK) {
            throw new RuntimeException(vbd_upload_error_message((int)$chunkFile['error'], (string)($chunkFile['name'] ?? 'chunk')));
        }
        if ((int)$chunkFile['size'] < 1 || (int)$chunkFile['size'] > $chunkMax) {
            throw new RuntimeException('Mỗi phần tệp không được vượt quá ' . round($chunkMax / 1024 / 1024, 1) . ' MB.');
        }
        if (!vbd_is_tmp_upload_path((string)($chunkFile['tmp_name'] ?? ''))) {
            throw new RuntimeException('Phần tệp tải lên không hợp lệ.' . vbd_upload_ini_hint());
        }
        $content = file_get_contents($chunkFile['tmp_name']);
        if ($content === false || $content === '') throw new RuntimeException('Không đọc được phần tệp tạm.');
        require_once __DIR__ . '/google_drive.php';
        $result = drive_upload_resumable_chunk(
            (string)$session['upload_url'],
            (string)$session['mime_type'],
            $offset,
            (int)($session['total_size'] ?? $total),
            $content
        );
        if (empty($result['complete'])) {
            respond([
                'ok' => true,
                'complete' => false,
                'uploaded' => (int)($result['uploaded'] ?? ($offset + strlen($content))),
                'upload_backend' => 'vanban-chunk-drive-v5',
            ]);
        }
        $drive = drive_upload_response(
            $result['file'],
            (string)$session['stored_name'],
            (string)$session['mime_type']
        );
        vbd_delete_upload_session($sessionId);
        $insert = $pdo->prepare('INSERT INTO office_document_files (document_id, drive_file_id, original_name, stored_name, mime_type, size_bytes, view_url, download_url) VALUES (?,?,?,?,?,?,?,?)');
        $insert->execute([
            (int)$session['document_id'],
            $drive['file_id'],
            (string)$session['original_name'],
            $drive['stored_name'],
            $drive['mime_type'],
            (int)($session['total_size'] ?? $total),
            $drive['view_url'],
            $drive['download_url'],
        ]);
        respond([
            'ok' => true,
            'complete' => true,
            'file' => $drive,
            'upload_backend' => 'vanban-chunk-drive-v5',
        ]);
    } catch (Throwable $e) {
        respond(['error' => $e->getMessage(), 'upload_backend' => 'vanban-chunk-drive-v5'], 502);
    }
}

if ($action === 'upload_finalize') {
    $input = json_body();
    $id = (int)($input['document_id'] ?? 0);
    $document = vbd_document($pdo, $id, (int)$user['id']);
    if (!$document) respond(['error' => 'Không tìm thấy văn bản.'], 404);
    $fileId = trim((string)($input['drive_file_id'] ?? ''));
    $originalName = trim((string)($input['original_name'] ?? ''));
    $storedName = trim((string)($input['stored_name'] ?? ''));
    $size = (int)($input['size_bytes'] ?? 0);
    $mime = trim((string)($input['mime_type'] ?? '')) ?: 'application/octet-stream';
    if ($fileId === '' || $originalName === '' || $storedName === '') {
        respond(['error' => 'Thiếu thông tin tệp sau khi tải lên Drive.'], 422);
    }
    $viewUrl = trim((string)($input['view_url'] ?? '')) ?: ('https://drive.google.com/file/d/' . $fileId . '/view');
    $downloadUrl = trim((string)($input['download_url'] ?? '')) ?: ('https://drive.google.com/uc?export=download&id=' . $fileId);
    if (defined('GOOGLE_DRIVE_SHARE_MODE') && GOOGLE_DRIVE_SHARE_MODE === 'anyone') {
        require_once __DIR__ . '/google_drive.php';
        drive_share_file_anyone($fileId);
    }
    $insert = $pdo->prepare('INSERT INTO office_document_files (document_id, drive_file_id, original_name, stored_name, mime_type, size_bytes, view_url, download_url) VALUES (?,?,?,?,?,?,?,?)');
    $insert->execute([$id, $fileId, $originalName, $storedName, $mime, max(0, $size), $viewUrl, $downloadUrl]);
    respond([
        'ok' => true,
        'file' => [
            'file_id' => $fileId,
            'stored_name' => $storedName,
            'view_url' => $viewUrl,
            'download_url' => $downloadUrl,
        ],
        'upload_backend' => 'vanban-browser-drive-v4',
    ]);
}

if ($action === 'save_upload') {
    @ini_set('memory_limit', '256M');
    @set_time_limit(300);
    try {
        $input = $_POST;
        $input['sector'] = $input['sector'] ?? ($_GET['sector'] ?? 'hanhchinh');
        $document = vbd_save_document($pdo, $user, $input);
        $files = vbd_collect_uploaded_files();
        if (!$files) {
            respond([
                'ok' => true,
                'document' => $document,
                'message' => 'Đã lưu văn bản.',
                'upload_backend' => 'vanban-local-fallback-v3',
            ]);
        }
        vbd_process_document_upload($pdo, (int)$document['id'], $document, $files, (defined('SUBMISSION_MAX_FILE_MB') ? max(1, (int)SUBMISSION_MAX_FILE_MB) : 25) * 1024 * 1024);
    } catch (RuntimeException $e) {
        respond(['error' => $e->getMessage(), 'upload_backend' => 'vanban-local-fallback-v3'], 422);
    }
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

if ($action === 'drive_check') {
    require_once __DIR__ . '/google_drive.php';
    $status = drive_setup_status(true);
    respond([
        'ok' => true,
        'upload_backend' => 'vanban-chunk-drive-v5',
        'chunk_upload' => true,
        'chunk_size' => vbd_upload_chunk_bytes(),
        'local_storage_root' => vbd_local_storage_root(),
        'local_storage_writable' => is_writable(vbd_local_storage_root()),
        'upload_max_filesize' => (string)(ini_get('upload_max_filesize') ?: ''),
        'post_max_size' => (string)(ini_get('post_max_size') ?: ''),
        'app_max_file_mb' => defined('SUBMISSION_MAX_FILE_MB') ? max(1, (int)SUBMISSION_MAX_FILE_MB) : 25,
    ] + $status);
}

if ($action === 'file') {
    $id = (int)($_GET['document_id'] ?? 0);
    $storedName = basename(str_replace(['\\', '/'], '', trim((string)($_GET['name'] ?? ''))));
    $document = vbd_document($pdo, $id, (int)$user['id']);
    if (!$document || $storedName === '') respond(['error' => 'Không tìm thấy tệp.'], 404);
    $stmt = $pdo->prepare('SELECT * FROM office_document_files WHERE document_id=? AND stored_name=? LIMIT 1');
    $stmt->execute([$id, $storedName]);
    $record = $stmt->fetch();
    if (!$record || !vbd_is_local_file_id((string)($record['drive_file_id'] ?? ''))) {
        respond(['error' => 'Tệp không tồn tại hoặc không được lưu trên hosting.'], 404);
    }
    $path = vbd_local_file_path($id, $document, $storedName);
    if (!is_file($path)) respond(['error' => 'Không tìm thấy tệp trên hosting.'], 404);
    $mime = trim((string)($record['mime_type'] ?? '')) ?: 'application/octet-stream';
    $download = !empty($_GET['download']);
    header('Content-Type: ' . $mime);
    header('Content-Length: ' . (string)filesize($path));
    header('X-Content-Type-Options: nosniff');
    if ($download) {
        header('Content-Disposition: attachment; filename="' . str_replace('"', '', (string)($record['original_name'] ?? $storedName)) . '"');
    } else {
        header('Content-Disposition: inline; filename="' . str_replace('"', '', (string)($record['original_name'] ?? $storedName)) . '"');
    }
    readfile($path);
    exit;
}

if ($action === 'upload') {
    @ini_set('memory_limit', '256M');
    @set_time_limit(300);
    $id = (int)($_POST['document_id'] ?? 0);
    $document = vbd_document($pdo, $id, (int)$user['id']);
    if (!$document) respond(['error' => 'Hãy lưu văn bản trước khi tải tệp.'], 404);
    $files = vbd_collect_uploaded_files();
    if (!$files) {
        respond([
            'error' => 'Chưa chọn tệp để tải lên hoặc hosting không nhận được multipart upload.' . vbd_upload_ini_hint(),
            'upload_backend' => 'vanban-local-fallback-v3',
        ], 422);
    }
    $maxBytes = (defined('SUBMISSION_MAX_FILE_MB') ? max(1, (int)SUBMISSION_MAX_FILE_MB) : 25) * 1024 * 1024;
    vbd_process_document_upload($pdo, $id, $document, $files, $maxBytes);
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
            $document = vbd_document($pdo, $id, (int)$user['id']) ?: [];
            foreach ($files as $file) {
                $label = trim((string)($file['original_name'] ?? 'Tệp đính kèm'));
                $rawId = (string)($file['drive_file_id'] ?? '');
                if (vbd_is_local_file_id($rawId)) {
                    $storedName = trim((string)($file['stored_name'] ?? ''));
                    if ($storedName !== '' && $document) {
                        $path = vbd_local_file_path($id, $document, $storedName);
                        if (is_file($path) && !@unlink($path)) {
                            $driveErrors[] = $label . ': không xóa được tệp trên hosting';
                        }
                    }
                    continue;
                }
                $fileId = drive_resolve_file_id(
                    $rawId,
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
