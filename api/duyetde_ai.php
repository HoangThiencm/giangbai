<?php
require_once __DIR__ . '/helpers.php';
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
if (empty($_SESSION['user_id'])) {
    respond(['error' => 'Chưa đăng nhập.'], 401);
}
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(['error' => 'Method not allowed.'], 405);
}

set_time_limit(180);
$userId = (int)$_SESSION['user_id'];
ensure_users_ai_key_columns($pdo);
$body = json_body();
$action = trim((string)($body['action'] ?? ($_GET['action'] ?? '')));

function duyetde_load_user_gemini_keys(PDO $pdo, int $userId): array
{
    $stmt = $pdo->prepare('SELECT gemini_keys FROM users WHERE id = ? LIMIT 1');
    $stmt->execute([$userId]);
    $row = $stmt->fetch() ?: [];
    $raw = $row['gemini_keys'] ?? null;
    if ($raw && stored_api_keys_need_encryption($raw)) {
        $plain = parse_stored_api_keys($raw);
        if ($plain) {
            $upd = $pdo->prepare('UPDATE users SET gemini_keys = ? WHERE id = ?');
            $upd->execute([encode_stored_api_keys($plain), $userId]);
        }
        return $plain;
    }
    return parse_stored_api_keys($raw);
}

function duyetde_is_rotatable_error(int $status, string $error): bool
{
    if (in_array($status, [429, 403], true)) {
        return true;
    }
    $hay = strtolower($error);
    return str_contains($hay, 'quota')
        || str_contains($hay, 'resource exhausted')
        || str_contains($hay, 'too many')
        || str_contains($hay, 'rate limit')
        || str_contains($hay, 'permission denied');
}

function duyetde_extract_gemini_text($decoded): string
{
    if (!is_array($decoded)) {
        return '';
    }
    $parts = $decoded['candidates'][0]['content']['parts'] ?? [];
    $chunks = [];
    foreach (is_array($parts) ? $parts : [] as $part) {
        if (is_array($part) && isset($part['text'])) {
            $chunks[] = (string)$part['text'];
        }
    }
    return trim(implode("\n", $chunks));
}

function duyetde_parse_json_object(string $text): ?array
{
    $clean = trim($text);
    if ($clean === '') {
        return null;
    }
    if (preg_match('/```(?:json)?\s*([\s\S]*?)```/i', $clean, $m)) {
        $clean = trim($m[1]);
    }
    $decoded = json_decode($clean, true);
    if (is_array($decoded)) {
        return $decoded;
    }
    $start = strpos($clean, '{');
    $end = strrpos($clean, '}');
    if ($start === false || $end === false || $end <= $start) {
        return null;
    }
    $decoded = json_decode(substr($clean, $start, $end - $start + 1), true);
    return is_array($decoded) ? $decoded : null;
}

function duyetde_clip_text(string $text, int $limit = 60000): string
{
    if (function_exists('mb_substr')) {
        return mb_strlen($text) > $limit ? mb_substr($text, 0, $limit) : $text;
    }
    return strlen($text) > $limit ? substr($text, 0, $limit) : $text;
}

function duyetde_normalize_pdf_base64(string $raw): string
{
    $value = trim($raw);
    if (str_contains($value, 'base64,')) {
        $value = explode('base64,', $value, 2)[1] ?? $value;
    }
    $value = preg_replace('/\s+/', '', $value) ?? $value;
    if (strlen($value) > 3500000) {
        return '';
    }
    return $value;
}

function call_gemini_with_rotation(array $keys, array $payload, string $model = 'gemini-2.5-flash', int $timeout = 90): array
{
    if (!$keys) {
        return ['ok' => false, 'error' => 'Tài khoản chưa có Gemini API Key.', 'status' => 422];
    }
    if (!preg_match('/^gemini-[a-z0-9._-]+$/i', $model)) {
        $model = 'gemini-2.5-flash';
    }
    $encoded = json_encode($payload, JSON_UNESCAPED_UNICODE);
    if (!is_string($encoded) || strlen($encoded) > 8 * 1024 * 1024) {
        return ['ok' => false, 'error' => 'Tài liệu gửi AI quá lớn.', 'status' => 413];
    }
    $timeout = max(20, min(120, $timeout));
    $lastStatus = 502;
    $lastError = 'Không gọi được Gemini.';
    $attempted = 0;

    foreach ($keys as $index => $key) {
        $attempted++;
        $url = 'https://generativelanguage.googleapis.com/v1beta/models/' . rawurlencode($model) . ':generateContent?key=' . rawurlencode($key);
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
            CURLOPT_POSTFIELDS => $encoded,
            CURLOPT_CONNECTTIMEOUT => 12,
            CURLOPT_TIMEOUT => $timeout,
        ]);
        $raw = curl_exec($ch);
        $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curlError = curl_error($ch);
        curl_close($ch);

        if (is_string($raw) && $raw !== '') {
            $decoded = json_decode($raw, true);
            if (is_array($decoded) && $status >= 200 && $status < 300) {
                return [
                    'ok' => true,
                    'body' => $decoded,
                    'text' => duyetde_extract_gemini_text($decoded),
                    'model' => $model,
                    'key_index' => $index,
                    'attempted' => $attempted,
                ];
            }
            $lastError = is_array($decoded)
                ? (string)($decoded['error']['message'] ?? ('Gemini HTTP ' . $status))
                : 'Gemini trả về dữ liệu không hợp lệ.';
            $lastStatus = $status ?: 502;
        } elseif ($curlError !== '') {
            $lastError = 'Máy chủ không gọi được Gemini: ' . $curlError;
            $lastStatus = 502;
        }

        if (duyetde_is_rotatable_error($lastStatus, $lastError)) {
            error_log('[duyetde_ai] quota/permission on key #' . ($index + 1) . ' status=' . $lastStatus . ' — rotating');
            continue;
        }
        break;
    }

    return ['ok' => false, 'error' => $lastError, 'status' => $lastStatus, 'attempted' => $attempted];
}

function duyetde_file_parts(array $body, string $prefix, string $label): array
{
    $parts = [];
    $textRaw = $body[$prefix . '_text'] ?? $body[$prefix] ?? '';
    $text = is_string($textRaw) ? duyetde_clip_text(trim($textRaw)) : '';
    if ($text !== '') {
        $parts[] = ['text' => $label . " (văn bản trích xuất):\n" . $text];
    }
    $pdfRaw = $body[$prefix . '_pdf_base64'] ?? $body[$prefix . '_base64'] ?? '';
    $pdf = is_string($pdfRaw) ? duyetde_normalize_pdf_base64($pdfRaw) : '';
    if ($pdf !== '') {
        $parts[] = ['text' => $label . ' (tệp PDF đính kèm để đọc bảng/hình):'];
        $parts[] = ['inline_data' => ['mime_type' => 'application/pdf', 'data' => $pdf]];
    }
    return $parts;
}

function duyetde_normalize_status(string $status): string
{
    $value = trim($status);
    $map = [
        'dat' => 'Đạt',
        'đạt' => 'Đạt',
        'pass' => 'Đạt',
        'can chinh sua' => 'Cần chỉnh sửa',
        'cần chỉnh sửa' => 'Cần chỉnh sửa',
        'can_chinh_sua' => 'Cần chỉnh sửa',
        'revise' => 'Cần chỉnh sửa',
        'khong dat' => 'Không đạt',
        'không đạt' => 'Không đạt',
        'khong_dat' => 'Không đạt',
        'fail' => 'Không đạt',
        'chua du du lieu' => 'Chưa đủ dữ liệu để kết luận',
        'chưa đủ dữ liệu để kết luận' => 'Chưa đủ dữ liệu để kết luận',
        'chua_du_du_lieu' => 'Chưa đủ dữ liệu để kết luận',
        'insufficient' => 'Chưa đủ dữ liệu để kết luận',
    ];
    $key = strtolower($value);
    $key = str_replace(['_', '-'], ' ', $key);
    return $map[$key] ?? (in_array($value, ['Đạt', 'Cần chỉnh sửa', 'Không đạt', 'Chưa đủ dữ liệu để kết luận'], true)
        ? $value
        : 'Chưa đủ dữ liệu để kết luận');
}

$keys = duyetde_load_user_gemini_keys($pdo, $userId);
if (!$keys) {
    respond(['ok' => false, 'error' => 'Tài khoản chưa có Gemini API Key. Hãy lưu key trong phần Hồ sơ đợt duyệt.'], 422);
}

$model = trim((string)($body['model'] ?? 'gemini-2.5-flash'));
$profile = is_array($body['profile'] ?? null) ? $body['profile'] : [];
$profileLine = trim(implode(' · ', array_filter([
    $profile['mon_hoc'] ?? '',
    isset($profile['khoi_lop']) ? ('Khối ' . $profile['khoi_lop']) : '',
    $profile['loai_de'] ?? '',
    $profile['nam_hoc'] ?? '',
    $profile['hoc_ky'] ?? '',
    $profile['to_chuyen_mon'] ?? '',
])));

if ($action === 'generate_solution') {
    $parts = array_merge(
        [['text' => "Bạn là chuyên gia giải đề kiểm tra (Solution Engine). Nhiệm vụ: trích xuất toàn bộ câu hỏi trong đề thi và giải chi tiết từng bước, nêu đáp án cuối cùng, nêu rõ công thức/căn cứ khoa học. Không nhận xét ma trận ở pha này.\nHồ sơ: {$profileLine}\nTrả về JSON duy nhất:\n{\"questions\":[{\"so_cau\":\"1\",\"cau_hoi\":\"...\",\"loi_giai\":\"...\",\"dap_an\":\"...\"}],\"tom_tat\":\"...\"}"]],
        duyetde_file_parts($body, 'exam', 'Đề thi'),
        duyetde_file_parts($body, 'answer', 'Đáp án/Hướng dẫn chấm gốc (nếu có)')
    );
    if (count($parts) < 2) {
        respond(['ok' => false, 'error' => 'Thiếu nội dung đề thi.'], 422);
    }
    $result = call_gemini_with_rotation($keys, [
        'contents' => [['role' => 'user', 'parts' => $parts]],
        'generationConfig' => [
            'temperature' => 0.2,
            'responseMimeType' => 'application/json',
        ],
    ], $model);
    if (empty($result['ok'])) {
        respond(['ok' => false, 'error' => $result['error'] ?? 'Không sinh được lời giải.'], (int)($result['status'] ?? 502));
    }
    $parsed = duyetde_parse_json_object((string)($result['text'] ?? ''));
    if (!$parsed) {
        respond(['ok' => false, 'error' => 'AI không trả JSON lời giải hợp lệ.', 'raw' => duyetde_clip_text((string)($result['text'] ?? ''), 4000)], 502);
    }
    respond(['ok' => true, 'action' => $action, 'solution' => $parsed, 'model' => $result['model'] ?? $model]);
}

if ($action === 'evaluate_exam') {
    $solutionJson = $body['solution'] ?? null;
    $solutionText = is_array($solutionJson)
        ? json_encode($solutionJson, JSON_UNESCAPED_UNICODE)
        : trim((string)($body['solution_text'] ?? ''));
    $parts = array_merge(
        [['text' => "Bạn là chuyên gia giáo dục, thẩm định đề kiểm tra theo Ma trận và Bảng đặc tả (Evaluation Engine).\nHồ sơ: {$profileLine}\nĐánh giá dứt khoát từng câu theo 3 khía cạnh: Ma trận (chuẩn kiến thức, mức độ tư duy, số điểm), Hình thức (câu từ, chính tả, trình bày), Nội dung (tính chính xác khoa học).\nMáy trạng thái bắt buộc, chỉ được dùng đúng 4 giá trị:\n- Đạt: khớp hoàn toàn ma trận/đặc tả về câu hỏi, mức độ nhận thức, đơn vị kiến thức, số điểm.\n- Cần chỉnh sửa: lỗi chính tả, diễn đạt, hình vẽ chưa rõ hoặc tinh chỉnh câu chữ nhỏ.\n- Không đạt: sai mạch kiến thức, sai mức độ tư duy, sai số điểm, hoặc không có trong ma trận/đặc tả.\n- Chưa đủ dữ liệu để kết luận: ma trận/đặc tả mờ, thiếu dữ liệu, câu hỏi không rõ ngữ cảnh. Không được kết luận bừa.\nVới câu Cần chỉnh sửa hoặc Không đạt, bắt buộc viết lại câu hỏi đề xuất, đáp án và hướng dẫn chấm mới, kèm căn cứ dòng/cột ma trận.\nTrả JSON duy nhất:\n{\"tong_so_cau\":0,\"so_cau_dat\":0,\"so_cau_can_chinh_sua\":0,\"so_cau_khong_dat\":0,\"so_cau_chua_du_du_lieu\":0,\"ket_luan\":\"\",\"questions\":[{\"so_cau\":\"1\",\"cau_hoi_goc\":\"\",\"trang_thai\":\"Đạt\",\"ma_tran\":{\"nhan_xet\":\"\",\"dong\":\"\",\"chu_de\":\"\",\"muc_do\":\"\",\"diem\":\"\"},\"hinh_thuc\":{\"nhan_xet\":\"\"},\"noi_dung\":{\"nhan_xet\":\"\"},\"nhan_xet\":\"\",\"can_cu\":\"\",\"cau_de_xuat\":\"\",\"dap_an_de_xuat\":\"\",\"huong_dan_cham_de_xuat\":\"\"}]}"]],
        duyetde_file_parts($body, 'exam', 'Đề thi'),
        duyetde_file_parts($body, 'matrix', 'Ma trận đề'),
        duyetde_file_parts($body, 'spec', 'Bảng đặc tả'),
        duyetde_file_parts($body, 'answer', 'Đáp án/Hướng dẫn chấm gốc (nếu có)')
    );
    if ($solutionText !== '') {
        $parts[] = ['text' => "Lời giải tham khảo (Pha 1):\n" . duyetde_clip_text($solutionText, 80000)];
    }
    if (count($parts) < 3) {
        respond(['ok' => false, 'error' => 'Thiếu đề thi hoặc ma trận/đặc tả để đối chiếu.'], 422);
    }
    $result = call_gemini_with_rotation($keys, [
        'contents' => [['role' => 'user', 'parts' => $parts]],
        'generationConfig' => [
            'temperature' => 0.15,
            'responseMimeType' => 'application/json',
        ],
    ], $model, 110);
    if (empty($result['ok'])) {
        respond(['ok' => false, 'error' => $result['error'] ?? 'Không thẩm định được đề.'], (int)($result['status'] ?? 502));
    }
    $parsed = duyetde_parse_json_object((string)($result['text'] ?? ''));
    if (!$parsed) {
        respond(['ok' => false, 'error' => 'AI không trả JSON thẩm định hợp lệ.', 'raw' => duyetde_clip_text((string)($result['text'] ?? ''), 4000)], 502);
    }
    $questions = is_array($parsed['questions'] ?? null) ? $parsed['questions'] : [];
    foreach ($questions as $i => $q) {
        if (!is_array($q)) {
            continue;
        }
        $questions[$i]['trang_thai'] = duyetde_normalize_status((string)($q['trang_thai'] ?? ''));
        $questions[$i]['needs_recheck'] = false;
        $questions[$i]['teacher_action'] = '';
        $questions[$i]['cau_hien_tai'] = (string)($q['cau_hoi_goc'] ?? '');
    }
    $parsed['questions'] = $questions;
    $counts = [
        'Đạt' => 0,
        'Cần chỉnh sửa' => 0,
        'Không đạt' => 0,
        'Chưa đủ dữ liệu để kết luận' => 0,
    ];
    foreach ($questions as $q) {
        $st = duyetde_normalize_status((string)($q['trang_thai'] ?? ''));
        $counts[$st] = ($counts[$st] ?? 0) + 1;
    }
    $parsed['tong_so_cau'] = count($questions);
    $parsed['so_cau_dat'] = $counts['Đạt'];
    $parsed['so_cau_can_chinh_sua'] = $counts['Cần chỉnh sửa'];
    $parsed['so_cau_khong_dat'] = $counts['Không đạt'];
    $parsed['so_cau_chua_du_du_lieu'] = $counts['Chưa đủ dữ liệu để kết luận'];
    respond(['ok' => true, 'action' => $action, 'evaluation' => $parsed, 'model' => $result['model'] ?? $model]);
}

if ($action === 'recheck_question' || $action === 'recheck_single_question') {
    $question = is_array($body['question'] ?? null) ? $body['question'] : [];
    $questionText = trim((string)($question['cau_hien_tai'] ?? $question['cau_de_xuat'] ?? $question['cau_hoi'] ?? $body['question_text'] ?? ''));
    if ($questionText === '') {
        respond(['ok' => false, 'error' => 'Thiếu nội dung câu hỏi cần kiểm tra lại.'], 422);
    }
    $parts = array_merge(
        [['text' => "Bạn là chuyên gia giáo dục. Chỉ thẩm định LẠI MỘT câu hỏi đã được giáo viên hiệu chỉnh, đối chiếu với ma trận và bảng đặc tả.\nHồ sơ: {$profileLine}\nCâu gốc: " . trim((string)($question['cau_hoi_goc'] ?? '')) . "\nCâu đã sửa:\n{$questionText}\nĐáp án/hướng dẫn chấm mới: " . trim((string)($question['dap_an_de_xuat'] ?? $question['dap_an'] ?? '')) . "\nDùng đúng 4 trạng thái: Đạt | Cần chỉnh sửa | Không đạt | Chưa đủ dữ liệu để kết luận.\nTrả JSON duy nhất: {\"so_cau\":\"" . trim((string)($question['so_cau'] ?? '')) . "\",\"trang_thai\":\"Đạt\",\"nhan_xet\":\"\",\"can_cu\":\"\",\"ma_tran\":{\"nhan_xet\":\"\",\"dong\":\"\",\"chu_de\":\"\",\"muc_do\":\"\",\"diem\":\"\"},\"hinh_thuc\":{\"nhan_xet\":\"\"},\"noi_dung\":{\"nhan_xet\":\"\"},\"cau_de_xuat\":\"\",\"dap_an_de_xuat\":\"\",\"huong_dan_cham_de_xuat\":\"\"}"]],
        duyetde_file_parts($body, 'matrix', 'Ma trận đề'),
        duyetde_file_parts($body, 'spec', 'Bảng đặc tả')
    );
    $result = call_gemini_with_rotation($keys, [
        'contents' => [['role' => 'user', 'parts' => $parts]],
        'generationConfig' => [
            'temperature' => 0.1,
            'responseMimeType' => 'application/json',
        ],
    ], $model);
    if (empty($result['ok'])) {
        respond(['ok' => false, 'error' => $result['error'] ?? 'Không kiểm tra lại được câu hỏi.'], (int)($result['status'] ?? 502));
    }
    $parsed = duyetde_parse_json_object((string)($result['text'] ?? ''));
    if (!$parsed) {
        respond(['ok' => false, 'error' => 'AI không trả JSON kiểm tra lại hợp lệ.', 'raw' => duyetde_clip_text((string)($result['text'] ?? ''), 4000)], 502);
    }
    $parsed['trang_thai'] = duyetde_normalize_status((string)($parsed['trang_thai'] ?? ''));
    $parsed['needs_recheck'] = false;
    respond(['ok' => true, 'action' => 'recheck_question', 'result' => $parsed, 'model' => $result['model'] ?? $model]);
}

respond(['error' => 'Hành động AI không hợp lệ. Dùng generate_solution, evaluate_exam hoặc recheck_question.'], 422);
