<?php
/**
 * Telegram webhook for the document register. Configure this URL with
 * setWebhook and the same TELEGRAM_VANBAN_WEBHOOK_SECRET from config.php.
 */
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/db.php';
define('VBD_SKIP_BOOT', true);
require_once __DIR__ . '/vanban.php';

function tvb_reply(array $payload = [], int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

function tvb_config(string $name, $default = '')
{
    return defined($name) ? constant($name) : $default;
}

function tvb_allowed_chat(int $chatId): bool
{
    $allowed = tvb_config('TELEGRAM_VANBAN_ALLOWED_CHATS', []);
    if (is_string($allowed)) $allowed = preg_split('/\s*,\s*/', trim($allowed));
    if (!is_array($allowed)) return false;
    foreach ($allowed as $id) {
        if ((string)$id === (string)$chatId) return true;
    }
    return false;
}

function tvb_ensure_schema(PDO $pdo): void
{
    vbd_maybe_ensure_schema($pdo);
    $pdo->exec("CREATE TABLE IF NOT EXISTS office_telegram_updates (
        update_id BIGINT NOT NULL PRIMARY KEY,
        chat_id BIGINT NOT NULL,
        document_id INT DEFAULT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'processing',
        error_message VARCHAR(500) DEFAULT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_office_telegram_updates_document (document_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    $pdo->exec("CREATE TABLE IF NOT EXISTS office_telegram_edits (
        chat_id BIGINT NOT NULL PRIMARY KEY,
        document_id INT NOT NULL,
        field_key VARCHAR(40) NOT NULL,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}

function tvb_claim_update(PDO $pdo, int $updateId, int $chatId): bool
{
    $stmt = $pdo->prepare("INSERT IGNORE INTO office_telegram_updates (update_id, chat_id, status) VALUES (?, ?, 'processing')");
    $stmt->execute([$updateId, $chatId]);
    if ($stmt->rowCount() === 1) return true;
    $stmt = $pdo->prepare("SELECT status FROM office_telegram_updates WHERE update_id = ? LIMIT 1");
    $stmt->execute([$updateId]);
    $row = $stmt->fetch();
    if (in_array(($row['status'] ?? ''), ['completed', 'failed', 'ignored'], true)) return false;
    $pdo->prepare("UPDATE office_telegram_updates SET status='processing', error_message=NULL WHERE update_id=?")->execute([$updateId]);
    return true;
}

function tvb_finish_update(PDO $pdo, int $updateId, string $status, ?int $documentId = null, string $error = ''): void
{
    $pdo->prepare('UPDATE office_telegram_updates SET status=?, document_id=COALESCE(?, document_id), error_message=? WHERE update_id=?')
        ->execute([$status, $documentId, $error !== '' ? vbd_truncate($error, 500) : null, $updateId]);
}

function tvb_api(string $method, array $data): array
{
    $token = trim((string)tvb_config('TELEGRAM_VANBAN_BOT_TOKEN'));
    if ($token === '') throw new RuntimeException('Chưa cấu hình TELEGRAM_VANBAN_BOT_TOKEN.');
    $ch = curl_init('https://api.telegram.org/bot' . $token . '/' . $method);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_TIMEOUT => 20,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_POSTFIELDS => json_encode($data, JSON_UNESCAPED_UNICODE),
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    $decoded = is_string($raw) ? json_decode($raw, true) : null;
    if ($status < 200 || $status >= 300 || !is_array($decoded) || empty($decoded['ok'])) {
        $detail = is_array($decoded) ? (string)($decoded['description'] ?? '') : '';
        if ($detail === '') $detail = $error !== '' ? $error : 'không phản hồi hợp lệ';
        throw new RuntimeException('Telegram API ' . $method . ': ' . $detail);
    }
    return $decoded['result'] ?? [];
}

function tvb_safe_name(string $name, string $fallback): string
{
    $name = basename(str_replace(["\0", '\\', '/'], '', trim($name)));
    return $name === '' || $name === '.' || $name === '..' ? $fallback : vbd_truncate($name, 220);
}

function tvb_download_file(string $fileId, string $name, int $declaredSize): string
{
    $max = 20 * 1024 * 1024;
    if ($declaredSize < 1 || $declaredSize > $max) throw new RuntimeException('Tệp Telegram phải nhỏ hơn hoặc bằng 20 MB.');
    $meta = tvb_api('getFile', ['file_id' => $fileId]);
    $remotePath = trim((string)($meta['file_path'] ?? ''));
    if ($remotePath === '' || str_contains($remotePath, '..')) throw new RuntimeException('Telegram không trả về đường dẫn tệp hợp lệ.');
    $dir = rtrim(sys_get_temp_dir(), '/\\') . DIRECTORY_SEPARATOR . 'giangbai-telegram-vanban';
    if (!is_dir($dir) && !@mkdir($dir, 0700, true) && !is_dir($dir)) throw new RuntimeException('Không tạo được thư mục tạm Telegram.');
    $path = $dir . DIRECTORY_SEPARATOR . bin2hex(random_bytes(12)) . '-' . tvb_safe_name($name, 'van-ban.bin');
    $token = trim((string)tvb_config('TELEGRAM_VANBAN_BOT_TOKEN'));
    $in = curl_init('https://api.telegram.org/file/bot' . $token . '/' . $remotePath);
    $out = fopen($path, 'wb');
    if (!$out) throw new RuntimeException('Không mở được tệp tạm.');
    curl_setopt_array($in, [CURLOPT_FILE => $out, CURLOPT_FOLLOWLOCATION => false, CURLOPT_TIMEOUT => 90, CURLOPT_FAILONERROR => true]);
    $ok = curl_exec($in);
    $error = curl_error($in);
    curl_close($in);
    fclose($out);
    clearstatcache(true, $path);
    if (!$ok || !is_file($path) || (int)filesize($path) < 1 || (int)filesize($path) > $max) {
        @unlink($path);
        throw new RuntimeException('Không tải được tệp từ Telegram' . ($error ? ': ' . $error : '.'));
    }
    return $path;
}

function tvb_extract_text(string $path, string $name, string $caption = ''): string
{
    $extension = strtolower(pathinfo($name, PATHINFO_EXTENSION));
    $text = trim($caption);
    if ($extension === 'docx' && class_exists('ZipArchive')) {
        $zip = new ZipArchive();
        if ($zip->open($path) === true) {
            $xml = $zip->getFromName('word/document.xml');
            $zip->close();
            if (is_string($xml)) $text .= "\n" . trim(preg_replace('/\s+/u', ' ', strip_tags(str_replace('</w:p>', "\n", $xml))));
        }
    } elseif ($extension === 'pdf') {
        if (function_exists('exec')) {
            $output = [];
            $code = 1;
            @exec('pdftotext -f 1 -l 3 -enc UTF-8 ' . escapeshellarg($path) . ' - 2>/dev/null', $output, $code);
            if ($code === 0) $text .= "\n" . implode("\n", $output);
        }
        if (vbd_text_len($text) < 30 && function_exists('vbd_pdf_extract_text')) {
            $extracted = vbd_pdf_extract_text($path, 3);
            if ($extracted !== '') $text .= "\n" . $extracted;
        }
    }
    if (vbd_text_len($text) < 30 && in_array($extension, ['jpg', 'jpeg', 'png', 'webp'], true) && function_exists('exec')) {
        $output = [];
        $code = 1;
        // Optional hosting capability: OCR is used when Tesseract with Vietnamese
        // language data is installed; captions remain a safe fallback otherwise.
        @exec('tesseract ' . escapeshellarg($path) . ' stdout -l vie+eng 2>/dev/null', $output, $code);
        if ($code === 0) $text .= "\n" . implode("\n", $output);
    }
    // Last-resort text layer recovery for hosts without pdftotext. It is harmless
    // for scanned files, which will be saved and marked as low-confidence.
    if (vbd_text_len($text) < 30 && in_array($extension, ['pdf', 'txt'], true)) {
        $raw = (string)@file_get_contents($path, false, null, 0, 1024 * 1024);
        if ($raw !== '') {
            preg_match_all('/[\p{L}\p{N}][\p{L}\p{N}\s,.;:()\/-]{15,}/u', $raw, $matches);
            $text .= "\n" . implode("\n", array_slice($matches[0] ?? [], 0, 80));
        }
    }
    return vbd_text_cut(vbd_preprocess_source($text), 9000);
}

function tvb_message_file(array $message): ?array
{
    if (!empty($message['document']) && is_array($message['document'])) {
        $file = $message['document'];
        return ['id' => (string)($file['file_id'] ?? ''), 'name' => tvb_safe_name((string)($file['file_name'] ?? ''), 'telegram-document.bin'), 'mime' => (string)($file['mime_type'] ?? ''), 'size' => (int)($file['file_size'] ?? 0)];
    }
    if (!empty($message['photo']) && is_array($message['photo'])) {
        $photos = $message['photo'];
        $photo = end($photos);
        if (is_array($photo)) return ['id' => (string)($photo['file_id'] ?? ''), 'name' => 'telegram-photo-' . (string)($message['message_id'] ?? 'image') . '.jpg', 'mime' => 'image/jpeg', 'size' => (int)($photo['file_size'] ?? 0)];
    }
    return null;
}

function tvb_owner(PDO $pdo): array
{
    $id = (int)tvb_config('TELEGRAM_VANBAN_DEFAULT_OWNER_ID', 0);
    if ($id < 1) throw new RuntimeException('Chưa cấu hình TELEGRAM_VANBAN_DEFAULT_OWNER_ID.');
    $stmt = $pdo->prepare('SELECT id, username, full_name, role, is_active FROM users WHERE id=? LIMIT 1');
    $stmt->execute([$id]);
    $user = $stmt->fetch();
    if (!$user || !(bool)$user['is_active']) throw new RuntimeException('Tài khoản chủ sở hữu Telegram không hợp lệ.');
    return $user;
}

function tvb_html(string $value): string
{
    return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function tvb_summary(array $document, string $fileName, bool $confirmed = false): string
{
    $lines = [
        $confirmed ? '✅ <b>ĐÃ XÁC NHẬN VĂN BẢN</b>' : '📄 <b>ĐÃ TIẾP NHẬN VĂN BẢN</b>',
        '<b>Lĩnh vực:</b> ' . tvb_html(vbd_sector_label(vbd_sector((string)($document['sector'] ?? 'hanhchinh')))),
        '<b>Thể loại:</b> ' . tvb_html((string)($document['document_type'] ?: 'Chưa nhận diện')),
        '<b>Số/Ký hiệu:</b> ' . tvb_html((string)($document['document_number'] ?: 'Chưa nhận diện')),
        '<b>Ngày ban hành:</b> ' . tvb_html((string)($document['document_date'] ?: 'Chưa nhận diện')),
        '<b>Cơ quan:</b> ' . tvb_html((string)($document['organization'] ?: 'Chưa nhận diện')),
        '<b>Trích yếu:</b> ' . tvb_html((string)($document['title'] ?: 'Chưa nhận diện')),
    ];
    if (!empty($document['report_due_at'])) $lines[] = '<b>Hạn báo cáo:</b> ' . tvb_html((string)$document['report_due_at']);
    $lines[] = '<b>Tệp:</b> ' . tvb_html($fileName) . ' (đã lưu hệ thống)';
    return implode("\n", $lines);
}

function tvb_sector_button(string $sector, string $current, string $icon, string $label): string
{
    if ($sector === $current) return '[• ' . $icon . ' ' . $label . ' •]';
    return $icon . ' ' . $label;
}

function tvb_keyboard(int $documentId, string $currentSector = 'hanhchinh'): array
{
    $currentSector = vbd_sector($currentSector);
    $rows = [[
        ['text' => tvb_sector_button('hanhchinh', $currentSector, '🏛', 'Hành chính'), 'callback_data' => 'sector:' . $documentId . ':hanhchinh'],
        ['text' => tvb_sector_button('chuyenmon', $currentSector, '🎓', 'Chuyên môn'), 'callback_data' => 'sector:' . $documentId . ':chuyenmon'],
        ['text' => tvb_sector_button('dang', $currentSector, '🚩', 'Đảng'), 'callback_data' => 'sector:' . $documentId . ':dang'],
    ], [
        ['text' => '✏️ Sửa từng mục', 'callback_data' => 'e:' . $documentId . ':s'],
    ], [['text' => '✅ Xác nhận chính xác', 'callback_data' => 'confirm:' . $documentId]]];
    $web = trim((string)tvb_config('TELEGRAM_VANBAN_WEB_URL'));
    if ($web !== '') $rows[2][] = ['text' => '🔗 Mở trên Web', 'url' => rtrim($web, '/') . '?document_id=' . $documentId];
    return ['inline_keyboard' => $rows];
}

function tvb_answer_callback(array $callback, string $text, bool $showAlert = false): void
{
    try {
        tvb_api('answerCallbackQuery', [
            'callback_query_id' => (string)($callback['id'] ?? ''),
            'text' => $text,
            'show_alert' => $showAlert,
        ]);
    } catch (Throwable $error) {
        if (stripos($error->getMessage(), 'query is too old') === false && stripos($error->getMessage(), 'query ID is invalid') === false) {
            throw $error;
        }
    }
}

function tvb_edit_callback_message(int $chatId, array $callback, array $document, int $documentId, bool $confirmed): void
{
    try {
        tvb_api('editMessageText', [
            'chat_id' => $chatId,
            'message_id' => (int)($callback['message']['message_id'] ?? 0),
            'text' => tvb_summary($document, 'Tệp đã lưu', $confirmed),
            'parse_mode' => 'HTML',
            'reply_markup' => tvb_keyboard($documentId, (string)($document['sector'] ?? 'hanhchinh')),
        ]);
    } catch (Throwable $error) {
        if (stripos($error->getMessage(), 'message is not modified') === false) throw $error;
    }
}

function tvb_lower(string $text): string
{
    return function_exists('mb_strtolower') ? mb_strtolower($text, 'UTF-8') : strtolower($text);
}

function tvb_edit_steps(): array
{
    return ['document_type', 'document_number', 'document_date', 'organization', 'title'];
}

function tvb_edit_labels(): array
{
    return [
        'document_type' => 'Thể loại',
        'document_number' => 'Số/Ký hiệu',
        'document_date' => 'Ngày ban hành',
        'organization' => 'Cơ quan ban hành',
        'title' => 'Trích yếu',
    ];
}

function tvb_type_choices(): array
{
    return [
        'kh' => 'Kế hoạch',
        'qd' => 'Quyết định',
        'cv' => 'Công văn',
        'tb' => 'Thông báo',
        'bc' => 'Báo cáo',
        'hd' => 'Hướng dẫn',
    ];
}

function tvb_normalize_type(string $text): string
{
    $clean = trim(preg_replace('/\s+/u', ' ', $text) ?? $text);
    $key = tvb_lower($clean);
    $map = [
        'kh' => 'Kế hoạch', 'kế hoạch' => 'Kế hoạch', 'ke hoach' => 'Kế hoạch',
        'qd' => 'Quyết định', 'qđ' => 'Quyết định', 'quyết định' => 'Quyết định', 'quyet dinh' => 'Quyết định',
        'cv' => 'Công văn', 'công văn' => 'Công văn', 'cong van' => 'Công văn',
        'tb' => 'Thông báo', 'thông báo' => 'Thông báo', 'thong bao' => 'Thông báo',
        'bc' => 'Báo cáo', 'báo cáo' => 'Báo cáo', 'bao cao' => 'Báo cáo',
        'hd' => 'Hướng dẫn', 'hướng dẫn' => 'Hướng dẫn', 'huong dan' => 'Hướng dẫn',
        'nq' => 'Nghị quyết', 'nghị quyết' => 'Nghị quyết', 'nghi quyet' => 'Nghị quyết',
        'ttr' => 'Tờ trình', 'tờ trình' => 'Tờ trình', 'to trinh' => 'Tờ trình',
    ];
    return $map[$key] ?? vbd_truncate($clean, 120);
}

function tvb_normalize_date(string $text): ?string
{
    $text = trim($text);
    if (preg_match('/^(\d{4})-(\d{2})-(\d{2})$/', $text, $match) && checkdate((int)$match[2], (int)$match[3], (int)$match[1])) {
        return sprintf('%04d-%02d-%02d', (int)$match[1], (int)$match[2], (int)$match[3]);
    }
    $ymd = vbd_parse_vn_date($text);
    if (!$ymd || !preg_match('/^(\d{4})-(\d{2})-(\d{2})$/', $ymd, $match)) return null;
    return checkdate((int)$match[2], (int)$match[3], (int)$match[1]) ? $ymd : null;
}

function tvb_edit_command(string $text): string
{
    $key = tvb_lower(trim($text));
    if (in_array($key, ['giữ', 'giu', 'giữ nguyên', 'giu nguyen', '.', '-'], true)) return 'keep';
    if (in_array($key, ['xóa', 'xoa', 'xoá'], true)) return 'clear';
    if (in_array($key, ['hủy', 'huy', 'huỷ', 'hủy sửa', 'huy sua'], true)) return 'cancel';
    return '';
}

function tvb_load_document(PDO $pdo, int $documentId, int $ownerId): ?array
{
    $stmt = $pdo->prepare('SELECT * FROM office_documents WHERE id=? AND (owner_id=? OR owner_id=0 OR owner_id IS NULL) LIMIT 1');
    $stmt->execute([$documentId, $ownerId]);
    $row = $stmt->fetch();
    return $row ?: null;
}

function tvb_edit_load(PDO $pdo, int $chatId): ?array
{
    $stmt = $pdo->prepare('SELECT chat_id, document_id, field_key FROM office_telegram_edits WHERE chat_id=? LIMIT 1');
    $stmt->execute([$chatId]);
    $row = $stmt->fetch();
    return $row ?: null;
}

function tvb_edit_save(PDO $pdo, int $chatId, int $documentId, string $field): void
{
    $pdo->prepare('INSERT INTO office_telegram_edits (chat_id, document_id, field_key) VALUES (?,?,?) ON DUPLICATE KEY UPDATE document_id=VALUES(document_id), field_key=VALUES(field_key)')
        ->execute([$chatId, $documentId, $field]);
}

function tvb_edit_clear(PDO $pdo, int $chatId): void
{
    $pdo->prepare('DELETE FROM office_telegram_edits WHERE chat_id=?')->execute([$chatId]);
}

function tvb_needs_manual(array $document): bool
{
    if (trim((string)($document['document_type'] ?? '')) === '') return true;
    if (trim((string)($document['document_number'] ?? '')) === '') return true;
    $title = trim((string)($document['title'] ?? ''));
    return $title === '' || str_starts_with($title, 'Văn bản Telegram:');
}

function tvb_edit_current(array $document, string $field): string
{
    $value = trim((string)($document[$field] ?? ''));
    if ($value === '' || $value === 'Chưa nhận diện') return 'Chưa có';
    return $value;
}

function tvb_edit_prompt(array $document, string $field, string $ack = ''): string
{
    $steps = tvb_edit_steps();
    $index = array_search($field, $steps, true);
    $n = ($index === false ? 0 : (int)$index) + 1;
    $label = tvb_edit_labels()[$field] ?? 'Mục';
    $hint = 'Gửi nội dung đúng, gõ <b>giữ</b> để nhận đề xuất, <b>xóa</b> để bỏ trống, hoặc <b>hủy</b> để dừng.';
    if ($field === 'document_date') $hint = 'Gửi ngày dạng <b>12/11/2026</b>. ' . $hint;
    if ($field === 'document_type') $hint = 'Bấm một thể loại bên dưới, hoặc gõ thể loại khác. ' . $hint;
    $body = '✏️ <b>Mục ' . $n . '/' . count($steps) . ': ' . tvb_html($label) . '</b>'
        . "\n" . 'Bot đang đề xuất: <b>' . tvb_html(tvb_edit_current($document, $field)) . '</b>'
        . "\n" . $hint;
    return $ack === '' ? $body : $ack . "\n\n" . $body;
}

function tvb_edit_keyboard(int $documentId, string $field): array
{
    $rows = [];
    if ($field === 'document_type') {
        $rows[] = [
            ['text' => 'Kế hoạch', 'callback_data' => 'e:' . $documentId . ':t:kh'],
            ['text' => 'Quyết định', 'callback_data' => 'e:' . $documentId . ':t:qd'],
            ['text' => 'Công văn', 'callback_data' => 'e:' . $documentId . ':t:cv'],
        ];
        $rows[] = [
            ['text' => 'Thông báo', 'callback_data' => 'e:' . $documentId . ':t:tb'],
            ['text' => 'Báo cáo', 'callback_data' => 'e:' . $documentId . ':t:bc'],
            ['text' => 'Hướng dẫn', 'callback_data' => 'e:' . $documentId . ':t:hd'],
        ];
    }
    $rows[] = [
        ['text' => 'Giữ đề xuất', 'callback_data' => 'e:' . $documentId . ':k'],
        ['text' => 'Xóa mục', 'callback_data' => 'e:' . $documentId . ':c'],
        ['text' => 'Hủy sửa', 'callback_data' => 'e:' . $documentId . ':x'],
    ];
    return ['inline_keyboard' => $rows];
}

function tvb_edit_send(int $chatId, array $document, string $field, string $ack = ''): void
{
    tvb_api('sendMessage', [
        'chat_id' => $chatId,
        'text' => tvb_edit_prompt($document, $field, $ack),
        'parse_mode' => 'HTML',
        'reply_markup' => tvb_edit_keyboard((int)$document['id'], $field),
    ]);
}

function tvb_edit_begin(PDO $pdo, int $chatId, array $document, string $lead): void
{
    $field = tvb_edit_steps()[0];
    tvb_edit_save($pdo, $chatId, (int)$document['id'], $field);
    tvb_edit_send($chatId, $document, $field, $lead);
}

function tvb_edit_apply(PDO $pdo, int $ownerId, int $documentId, string $field, ?string $value): void
{
    $ownerClause = 'id=? AND (owner_id=? OR owner_id=0 OR owner_id IS NULL)';
    if ($field === 'title') {
        $stored = trim((string)($value ?? ''));
        if ($stored === '') $stored = 'Chưa nhận diện';
        $pdo->prepare('UPDATE office_documents SET title=?, summary_text=? WHERE ' . $ownerClause)->execute([$stored, $stored, $documentId, $ownerId]);
        return;
    }
    $columns = [
        'document_type' => 'document_type',
        'document_number' => 'document_number',
        'document_date' => 'document_date',
        'organization' => 'organization',
    ];
    $column = $columns[$field] ?? '';
    if ($column === '') return;
    $stored = $field === 'document_date' ? ($value ?: null) : (($value ?? '') !== '' ? $value : null);
    $pdo->prepare('UPDATE office_documents SET ' . $column . '=? WHERE ' . $ownerClause)->execute([$stored, $documentId, $ownerId]);
}

function tvb_edit_finish(PDO $pdo, int $chatId, array $document): void
{
    tvb_edit_clear($pdo, $chatId);
    tvb_api('sendMessage', [
        'chat_id' => $chatId,
        'text' => '✅ Đã sửa xong văn bản #' . (int)$document['id'] . ".\n" . tvb_summary($document, 'Tệp đã lưu'),
        'parse_mode' => 'HTML',
        'reply_markup' => tvb_keyboard((int)$document['id'], (string)($document['sector'] ?? 'hanhchinh')),
    ]);
}

function tvb_edit_advance(PDO $pdo, int $chatId, array $document, string $field, string $ack): void
{
    $steps = tvb_edit_steps();
    $index = array_search($field, $steps, true);
    $next = $index === false ? null : ($steps[$index + 1] ?? null);
    if ($next === null) {
        tvb_edit_finish($pdo, $chatId, $document);
        return;
    }
    tvb_edit_save($pdo, $chatId, (int)$document['id'], $next);
    tvb_edit_send($chatId, $document, $next, $ack);
}

function tvb_edit_value(string $field, string $text): ?string
{
    $text = trim($text);
    if ($text === '') return null;
    if ($field === 'document_type') return tvb_normalize_type($text);
    if ($field === 'document_number') {
        $number = vbd_normalize_doc_number($text);
        return $number === '' ? null : vbd_truncate($number, 160);
    }
    if ($field === 'document_date') return tvb_normalize_date($text);
    if ($field === 'organization') return vbd_truncate(trim(preg_replace('/\s+/u', ' ', $text) ?? $text), 300);
    if ($field === 'title') return vbd_truncate(trim(preg_replace('/\s+/u', ' ', $text) ?? $text), 500);
    return null;
}

function tvb_process_edit_callback(PDO $pdo, array $callback, int $documentId, string $action, string $code = ''): void
{
    $chatId = (int)($callback['message']['chat']['id'] ?? 0);
    $owner = tvb_owner($pdo);
    $document = tvb_load_document($pdo, $documentId, (int)$owner['id']);
    if (!$document) {
        tvb_answer_callback($callback, 'Không tìm thấy văn bản cần sửa.');
        return;
    }
    if ($action === 's') {
        tvb_answer_callback($callback, 'Bắt đầu sửa từng mục');
        tvb_edit_begin($pdo, $chatId, $document, 'Sửa từng mục. Mục nào đúng thì bấm <b>Giữ đề xuất</b>.');
        return;
    }
    if ($action === 'x') {
        tvb_answer_callback($callback, 'Đã dừng sửa');
        tvb_edit_clear($pdo, $chatId);
        tvb_api('sendMessage', [
            'chat_id' => $chatId,
            'text' => 'Đã dừng sửa. Các mục đã nhập vẫn được giữ.' . "\n" . tvb_summary($document, 'Tệp đã lưu'),
            'parse_mode' => 'HTML',
            'reply_markup' => tvb_keyboard($documentId, (string)($document['sector'] ?? 'hanhchinh')),
        ]);
        return;
    }
    $edit = tvb_edit_load($pdo, $chatId);
    if (!$edit || (int)$edit['document_id'] !== $documentId) {
        tvb_answer_callback($callback, 'Phiên sửa đã hết. Bấm Sửa từng mục lại.');
        return;
    }
    $field = (string)$edit['field_key'];
    if (!in_array($field, tvb_edit_steps(), true)) {
        tvb_edit_clear($pdo, $chatId);
        tvb_answer_callback($callback, 'Phiên sửa đã hết. Bấm Sửa từng mục lại.');
        return;
    }
    if ($action === 't') {
        $choices = tvb_type_choices();
        if ($field !== 'document_type' || !isset($choices[$code])) {
            tvb_answer_callback($callback, 'Hãy trả lời mục đang hỏi.');
            return;
        }
        tvb_edit_apply($pdo, (int)$owner['id'], $documentId, 'document_type', $choices[$code]);
        $document = tvb_load_document($pdo, $documentId, (int)$owner['id']) ?? $document;
        tvb_answer_callback($callback, 'Đã ghi thể loại');
        tvb_edit_advance($pdo, $chatId, $document, $field, 'Đã ghi Thể loại: <b>' . tvb_html($choices[$code]) . '</b>');
        return;
    }
    if ($action === 'c') {
        tvb_edit_apply($pdo, (int)$owner['id'], $documentId, $field, null);
        $document = tvb_load_document($pdo, $documentId, (int)$owner['id']) ?? $document;
        tvb_answer_callback($callback, 'Đã xóa mục');
        $label = tvb_edit_labels()[$field] ?? 'Mục';
        tvb_edit_advance($pdo, $chatId, $document, $field, 'Đã xóa ' . tvb_html($label) . '.');
        return;
    }
    tvb_answer_callback($callback, 'Giữ đề xuất');
    $label = tvb_edit_labels()[$field] ?? 'Mục';
    tvb_edit_advance($pdo, $chatId, $document, $field, 'Giữ ' . tvb_html($label) . ': <b>' . tvb_html(tvb_edit_current($document, $field)) . '</b>');
}

function tvb_process_edit_text(PDO $pdo, int $chatId, string $text): bool
{
    if ($text === '' || str_starts_with($text, '/')) return false;
    $edit = tvb_edit_load($pdo, $chatId);
    if (!$edit) return false;
    $owner = tvb_owner($pdo);
    $documentId = (int)$edit['document_id'];
    $field = (string)$edit['field_key'];
    $document = tvb_load_document($pdo, $documentId, (int)$owner['id']);
    if (!$document || !in_array($field, tvb_edit_steps(), true)) {
        tvb_edit_clear($pdo, $chatId);
        return false;
    }
    $command = tvb_edit_command($text);
    if ($command === 'cancel') {
        tvb_edit_clear($pdo, $chatId);
        tvb_api('sendMessage', [
            'chat_id' => $chatId,
            'text' => 'Đã dừng sửa. Các mục đã nhập vẫn được giữ.' . "\n" . tvb_summary($document, 'Tệp đã lưu'),
            'parse_mode' => 'HTML',
            'reply_markup' => tvb_keyboard($documentId, (string)($document['sector'] ?? 'hanhchinh')),
        ]);
        return true;
    }
    if ($command === 'keep') {
        $label = tvb_edit_labels()[$field] ?? 'Mục';
        tvb_edit_advance($pdo, $chatId, $document, $field, 'Giữ ' . tvb_html($label) . ': <b>' . tvb_html(tvb_edit_current($document, $field)) . '</b>');
        return true;
    }
    if ($command === 'clear') {
        tvb_edit_apply($pdo, (int)$owner['id'], $documentId, $field, null);
        $document = tvb_load_document($pdo, $documentId, (int)$owner['id']) ?? $document;
        $label = tvb_edit_labels()[$field] ?? 'Mục';
        tvb_edit_advance($pdo, $chatId, $document, $field, 'Đã xóa ' . tvb_html($label) . '.');
        return true;
    }
    $value = tvb_edit_value($field, $text);
    if ($value === null) {
        $again = $field === 'document_date'
            ? 'Chưa đọc được ngày. Gửi theo dạng 12/11/2026, hoặc bấm Giữ đề xuất.'
            : 'Nội dung trống. Gửi lại mục này, hoặc bấm Giữ đề xuất.';
        tvb_api('sendMessage', ['chat_id' => $chatId, 'text' => $again]);
        return true;
    }
    tvb_edit_apply($pdo, (int)$owner['id'], $documentId, $field, $value);
    $document = tvb_load_document($pdo, $documentId, (int)$owner['id']) ?? $document;
    $label = tvb_edit_labels()[$field] ?? 'Mục';
    tvb_edit_advance($pdo, $chatId, $document, $field, 'Đã ghi ' . tvb_html($label) . ': <b>' . tvb_html($value) . '</b>');
    return true;
}

function tvb_process_callback(PDO $pdo, array $callback): void
{
    $chatId = (int)($callback['message']['chat']['id'] ?? 0);
    if (!tvb_allowed_chat($chatId)) return;
    $data = (string)($callback['data'] ?? '');
    if (preg_match('/^e:(\d+):t:([a-z]{2})$/', $data, $match)) {
        tvb_process_edit_callback($pdo, $callback, (int)$match[1], 't', $match[2]);
        return;
    }
    if (preg_match('/^e:(\d+):(s|k|c|x)$/', $data, $match)) {
        tvb_process_edit_callback($pdo, $callback, (int)$match[1], $match[2]);
        return;
    }
    $owner = tvb_owner($pdo);
    $documentId = 0;
    $confirmed = false;
    $popup = 'Đã cập nhật.';
    $sectorName = '';
    $ownerClause = 'id=? AND (owner_id=? OR owner_id=0 OR owner_id IS NULL)';
    if (preg_match('/^sector:(\d+):(hanhchinh|chuyenmon|dang)$/', $data, $match)) {
        $documentId = (int)$match[1];
        $labels = ['hanhchinh' => 'Hành chính', 'chuyenmon' => 'Chuyên môn', 'dang' => 'Đảng'];
        $sectorName = $labels[$match[2]] ?? 'lĩnh vực';
        $popup = 'Đã chọn ' . $sectorName;
        $pdo->prepare('UPDATE office_documents SET sector=? WHERE ' . $ownerClause)->execute([$match[2], $documentId, (int)$owner['id']]);
    } elseif (preg_match('/^confirm:(\d+)$/', $data, $match)) {
        $documentId = (int)$match[1];
        $confirmed = true;
        $popup = 'Đã xác nhận';
    } else {
        tvb_answer_callback($callback, 'Thao tác không hợp lệ.');
        return;
    }
    $stmt = $pdo->prepare('SELECT * FROM office_documents WHERE ' . $ownerClause . ' LIMIT 1');
    $stmt->execute([$documentId, (int)$owner['id']]);
    $document = $stmt->fetch();
    if (!$document) {
        tvb_answer_callback($callback, 'Không tìm thấy văn bản cần cập nhật.');
        return;
    }
    if ($confirmed) {
        tvb_edit_clear($pdo, $chatId);
        tvb_answer_callback($callback, $popup, true);
        tvb_api('sendMessage', ['chat_id' => $chatId, 'text' => "✅ Đã xác nhận thông tin văn bản #{$documentId}.", 'parse_mode' => 'HTML']);
    } else {
        tvb_answer_callback($callback, $popup, false);
        tvb_api('sendMessage', ['chat_id' => $chatId, 'text' => "🔄 Đã chuyển lĩnh vực sang: <b>{$sectorName}</b>", 'parse_mode' => 'HTML']);
    }
    tvb_edit_callback_message($chatId, $callback, $document, $documentId, $confirmed);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') tvb_reply(['error' => 'Method not allowed'], 405);
$secret = trim((string)tvb_config('TELEGRAM_VANBAN_WEBHOOK_SECRET'));
$supplied = (string)($_SERVER['HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN'] ?? '');
if ($secret === '' || $supplied === '' || !hash_equals($secret, $supplied)) tvb_reply(['error' => 'Forbidden'], 403);
$payload = json_decode((string)file_get_contents('php://input'), true);
if (!is_array($payload) || !isset($payload['update_id'])) tvb_reply(['ok' => true]);

try {
    $updateId = (int)($payload['update_id'] ?? 0);
    tvb_ensure_schema($pdo);
    if (!empty($payload['callback_query']) && is_array($payload['callback_query'])) {
        tvb_process_callback($pdo, $payload['callback_query']);
        tvb_reply(['ok' => true]);
    }
    $message = $payload['message'] ?? $payload['channel_post'] ?? null;
    if (!is_array($message)) tvb_reply(['ok' => true]);
    $chatId = (int)($message['chat']['id'] ?? 0);
    if (!tvb_allowed_chat($chatId)) tvb_reply(['ok' => true]);
    if (!tvb_claim_update($pdo, $updateId, $chatId)) tvb_reply(['ok' => true]);
    $file = tvb_message_file($message);
    if (!$file || $file['id'] === '') {
        $text = trim((string)($message['text'] ?? ''));
        if (tvb_process_edit_text($pdo, $chatId, $text)) {
            tvb_finish_update($pdo, $updateId, 'completed');
            tvb_reply(['ok' => true]);
        }
        tvb_finish_update($pdo, $updateId, 'ignored');
        tvb_reply(['ok' => true]);
    }
    tvb_edit_clear($pdo, $chatId);
    $processingMessage = tvb_api('sendMessage', ['chat_id' => $chatId, 'text' => '⏳ Đang tiếp nhận và phân tích văn bản...']);
    $temporary = tvb_download_file($file['id'], $file['name'], $file['size']);
    try {
        $source = tvb_extract_text($temporary, $file['name'], (string)($message['caption'] ?? ''));
        try { $parsed = vbd_parse_document($source); } catch (Throwable $ignored) { $parsed = ['sector' => vbd_detect_sector($source), 'confidence' => 'low']; }
        $year = vbd_current_academic_year();
        $owner = tvb_owner($pdo);
        $pdo->prepare('INSERT IGNORE INTO office_school_years (name, created_by) VALUES (?, ?)')->execute([$year, (int)$owner['id']]);
        $title = trim((string)($parsed['title'] ?? '')) ?: trim((string)($message['caption'] ?? '')) ?: ('Văn bản Telegram: ' . $file['name']);
        $document = vbd_save_document($pdo, $owner, [
            'academic_year' => $year, 'sector' => vbd_sector((string)($parsed['sector'] ?? vbd_detect_sector($source))), 'direction' => 'incoming',
            'document_number' => $parsed['document_number'] ?? '', 'title' => $title, 'document_date' => $parsed['document_date'] ?? null,
            'organization' => $parsed['organization'] ?? '', 'document_type' => $parsed['document_type'] ?? '',
            'summary_text' => $parsed['summary_text'] ?? $title, 'source_text' => $source,
            'report_required' => !empty($parsed['report_required']), 'report_due_at' => $parsed['report_due_at'] ?? null,
        ]);
        tvb_finish_update($pdo, $updateId, 'processing', (int)$document['id']);
        vbd_store_downloaded_document_file($pdo, $document, $temporary, $file['name'], $file['mime']);
        tvb_api('editMessageText', ['chat_id' => $chatId, 'message_id' => (int)$processingMessage['message_id'], 'text' => tvb_summary($document, $file['name']), 'parse_mode' => 'HTML', 'reply_markup' => tvb_keyboard((int)$document['id'], (string)($document['sector'] ?? 'hanhchinh'))]);
        if (tvb_needs_manual($document)) {
            tvb_edit_begin($pdo, $chatId, $document, 'Nhận diện chưa đủ. Bot hỏi lần lượt từng mục. Mục đúng thì bấm <b>Giữ đề xuất</b>.');
        }
        tvb_finish_update($pdo, $updateId, 'completed', (int)$document['id']);
    } finally {
        if (isset($temporary) && is_string($temporary)) @unlink($temporary);
    }
    tvb_reply(['ok' => true]);
} catch (Throwable $error) {
    if (isset($updateId)) tvb_finish_update($pdo, $updateId, 'failed', null, $error->getMessage());
    tvb_reply(['error' => 'Webhook failed'], 500);
}
