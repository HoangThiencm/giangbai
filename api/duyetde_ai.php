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
    if (strlen($value) > 12000000) {
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
    if (!is_string($encoded) || strlen($encoded) > 14 * 1024 * 1024) {
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

function duyetde_normalize_muc_do(string $raw): string
{
    $s = strtolower(trim($raw));
    $s = str_replace(['_', '-'], ' ', $s);
    if (preg_match('/van dung cao|vận dụng cao|vdc|high/u', $s)) {
        return 'van_dung_cao';
    }
    if (preg_match('/van dung|vận dụng|apply/u', $s)) {
        return 'van_dung';
    }
    if (preg_match('/thong hieu|thông hiểu|understand/u', $s)) {
        return 'thong_hieu';
    }
    if (preg_match('/nhan biet|nhận biết|know|nb/u', $s)) {
        return 'nhan_biet';
    }
    return $s !== '' ? str_replace(' ', '_', $s) : 'nhan_biet';
}

function duyetde_normalize_dang_cau(string $raw): string
{
    $s = function_exists('mb_strtolower') ? mb_strtolower(trim($raw), 'UTF-8') : strtolower(trim($raw));
    if (preg_match('/đúng\s*\/?\s*sai|dung sai|true\s*false|tnkq_dung_sai/u', $s)) {
        return 'TNKQ_dung_sai';
    }
    if (preg_match('/tự luận|tu luan|essay|tl_tu_luan/u', $s)) {
        return 'TL_tu_luan';
    }
    if (preg_match('/trả lời ngắn|tra loi ngan|tl_ngan/u', $s)) {
        return 'TL_ngan';
    }
    if (preg_match('/4\s*lựa chọn|nhiều lựa chọn|trac nghiem|tnkq/u', $s)) {
        return 'TNKQ_4_lua_chon';
    }
    return trim($raw) !== '' ? trim($raw) : 'TNKQ_4_lua_chon';
}

function duyetde_normalize_phan_thi(string $raw): string
{
    $s = function_exists('mb_strtolower') ? mb_strtolower(trim($raw), 'UTF-8') : strtolower(trim($raw));
    if (preg_match('/tự luận|tu luan|phần\s*iv|phan\s*iv|phần\s*4/u', $s)) {
        return 'Tự luận';
    }
    if (preg_match('/phần\s*iii|phan\s*iii|phần\s*3|trả lời ngắn/u', $s)) {
        return 'Phần III';
    }
    if (preg_match('/phần\s*ii|phan\s*ii|phần\s*2|đúng\s*\/?\s*sai/u', $s)) {
        return 'Phần II';
    }
    if (preg_match('/phần\s*i\b|phan\s*i\b|phần\s*1|trắc nghiệm/u', $s)) {
        return 'Phần I';
    }
    return trim($raw) !== '' ? trim($raw) : 'Khác';
}

function duyetde_normalize_ngu_lieu(string $raw): string
{
    $s = function_exists('mb_strtolower') ? mb_strtolower(trim($raw), 'UTF-8') : strtolower(trim($raw));
    if (preg_match('/đồ thị|do thi|graph/u', $s)) {
        return 'Đồ thị';
    }
    if (preg_match('/bảng biểu|bang bieu|table/u', $s)) {
        return 'Bảng biểu';
    }
    if (preg_match('/thực tế|thuc te|ngữ liệu/u', $s)) {
        return 'Thực tế';
    }
    if ($s === '') {
        return 'Thuần túy';
    }
    return trim($raw);
}

function duyetde_muc_do_label(string $code): string
{
    $map = [
        'nhan_biet' => 'Nhận biết',
        'thong_hieu' => 'Thông hiểu',
        'van_dung' => 'Vận dụng',
        'van_dung_cao' => 'Vận dụng cao',
    ];
    return $map[$code] ?? $code;
}

function duyetde_normalize_subitems($raw): array
{
    if (!is_array($raw)) {
        return [];
    }
    $out = [];
    foreach ($raw as $item) {
        if (!is_array($item)) {
            continue;
        }
        $y = trim((string)($item['y'] ?? $item['ky_hieu'] ?? ''));
        $out[] = [
            'y' => $y !== '' ? $y : chr(97 + count($out)),
            'muc_do' => duyetde_normalize_muc_do((string)($item['muc_do'] ?? '')),
            'diem' => (float)($item['diem'] ?? $item['so_diem'] ?? 0),
            'yccd' => trim((string)($item['yccd'] ?? $item['yeu_cau'] ?? '')),
            'yeu_cau_ngu_lieu' => duyetde_normalize_ngu_lieu((string)($item['yeu_cau_ngu_lieu'] ?? '')),
        ];
    }
    return $out;
}

function duyetde_normalize_matrix_index($raw): array
{
    $data = is_array($raw) ? $raw : [];
    $overview = is_array($data['tong_quan'] ?? null) ? $data['tong_quan'] : [];
    $ratio = is_array($overview['ti_le_phan_tram'] ?? null) ? $overview['ti_le_phan_tram'] : [];
    $items = is_array($data['danh_sach_chi_tieu'] ?? $data['items'] ?? null) ? ($data['danh_sach_chi_tieu'] ?? $data['items']) : [];
    $specs = [];
    $n = 0;
    foreach ($items as $item) {
        if (!is_array($item)) {
            continue;
        }
        $n++;
        $id = trim((string)($item['id'] ?? ''));
        if ($id === '') {
            $id = 'SPEC_' . str_pad((string)$n, 2, '0', STR_PAD_LEFT);
        }
        $subs = duyetde_normalize_subitems($item['cac_y_con'] ?? []);
        $dangCau = duyetde_normalize_dang_cau((string)($item['dang_cau'] ?? ''));
        $diem = (float)($item['so_diem'] ?? $item['diem'] ?? 0);
        if ($subs && $diem <= 0) {
            foreach ($subs as $sub) {
                $diem += (float)$sub['diem'];
            }
        }
        $specs[] = [
            'id' => $id,
            'chu_de' => trim((string)($item['chu_de'] ?? '')),
            'don_vi_kien_thuc' => trim((string)($item['don_vi_kien_thuc'] ?? $item['don_vi'] ?? '')),
            'phan_thi' => duyetde_normalize_phan_thi((string)($item['phan_thi'] ?? $item['phan'] ?? '')),
            'dang_cau' => $dangCau,
            'vi_tri_du_kien' => trim((string)($item['vi_tri_du_kien'] ?? $item['vi_tri_cau'] ?? '')),
            'muc_do' => duyetde_normalize_muc_do((string)($item['muc_do'] ?? ($subs[0]['muc_do'] ?? ''))),
            'yccd' => trim((string)($item['yccd'] ?? $item['yccd_yeu_cau_can_dat'] ?? '')),
            'so_diem' => $diem,
            'yeu_cau_ngu_lieu' => duyetde_normalize_ngu_lieu((string)($item['yeu_cau_ngu_lieu'] ?? '')),
            'cac_y_con' => $subs,
        ];
    }
    $counts = ['nhan_biet' => 0, 'thong_hieu' => 0, 'van_dung' => 0, 'van_dung_cao' => 0];
    $sumPoints = 0.0;
    foreach ($specs as $spec) {
        if ($spec['cac_y_con']) {
            foreach ($spec['cac_y_con'] as $sub) {
                $counts[$sub['muc_do']] = ($counts[$sub['muc_do']] ?? 0) + 1;
                $sumPoints += (float)$sub['diem'];
            }
        } else {
            $counts[$spec['muc_do']] = ($counts[$spec['muc_do']] ?? 0) + 1;
            $sumPoints += (float)$spec['so_diem'];
        }
    }
    $totalSlots = max(1, array_sum($counts));
    $computedRatio = [
        'nhan_biet' => round(($counts['nhan_biet'] / $totalSlots) * 100),
        'thong_hieu' => round(($counts['thong_hieu'] / $totalSlots) * 100),
        'van_dung' => round(($counts['van_dung'] / $totalSlots) * 100),
        'van_dung_cao' => round(($counts['van_dung_cao'] / $totalSlots) * 100),
    ];
    return [
        'tong_quan' => [
            'mon' => trim((string)($overview['mon'] ?? '')),
            'lop' => (int)($overview['lop'] ?? 0),
            'thoi_gian_phut' => (int)($overview['thoi_gian_phut'] ?? 0),
            'tong_diem' => isset($overview['tong_diem']) ? (float)$overview['tong_diem'] : round($sumPoints, 2),
            'ti_le_phan_tram' => [
                'nhan_biet' => (float)($ratio['nhan_biet'] ?? $computedRatio['nhan_biet']),
                'thong_hieu' => (float)($ratio['thong_hieu'] ?? $computedRatio['thong_hieu']),
                'van_dung' => (float)($ratio['van_dung'] ?? $computedRatio['van_dung']),
                'van_dung_cao' => (float)($ratio['van_dung_cao'] ?? $computedRatio['van_dung_cao']),
            ],
            'so_chi_tieu' => count($specs),
            'ti_le_tinh_tu_chi_tieu' => $computedRatio,
            'tong_diem_tinh_tu_chi_tieu' => round($sumPoints, 2),
        ],
        'danh_sach_chi_tieu' => $specs,
    ];
}

function duyetde_ratio_text(array $ratio): string
{
    return implode('-', [
        (int)($ratio['nhan_biet'] ?? 0),
        (int)($ratio['thong_hieu'] ?? 0),
        (int)($ratio['van_dung'] ?? 0),
        (int)($ratio['van_dung_cao'] ?? 0),
    ]);
}

function duyetde_group_specs_by_part(array $index): array
{
    $order = ['Phần I', 'Phần II', 'Phần III', 'Tự luận'];
    $groups = [];
    foreach ($index['danh_sach_chi_tieu'] ?? [] as $spec) {
        $part = (string)($spec['phan_thi'] ?? 'Khác');
        $groups[$part][] = $spec;
    }
    $sorted = [];
    foreach ($order as $part) {
        if (!empty($groups[$part])) {
            $sorted[$part] = $groups[$part];
            unset($groups[$part]);
        }
    }
    foreach ($groups as $part => $specs) {
        $sorted[$part] = $specs;
    }
    return $sorted ?: ['Toàn đề' => []];
}

function duyetde_find_spec(array $index, string $specId): ?array
{
    foreach ($index['danh_sach_chi_tieu'] ?? [] as $spec) {
        if ((string)($spec['id'] ?? '') === $specId) {
            return $spec;
        }
    }
    return null;
}

function duyetde_normalize_eval_questions(array $questions): array
{
    $out = [];
    foreach ($questions as $q) {
        if (!is_array($q)) {
            continue;
        }
        $q['trang_thai'] = duyetde_normalize_status((string)($q['trang_thai'] ?? ''));
        $q['needs_recheck'] = false;
        $q['teacher_action'] = (string)($q['teacher_action'] ?? '');
        $q['cau_hien_tai'] = (string)($q['cau_hien_tai'] ?? $q['cau_hoi_goc'] ?? '');
        $q['spec_id'] = trim((string)($q['spec_id'] ?? $q['ma_tran']['spec_id'] ?? $q['ma_tran']['dong'] ?? ''));
        $out[] = $q;
    }
    return $out;
}

function duyetde_count_statuses(array $questions): array
{
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
    return $counts;
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

if ($action === 'extract_matrix_index') {
    $parts = array_merge(
        [['text' => "Bạn là chuyên gia đo lường đánh giá theo CTGDPT 2018. NHIỆM VỤ CHẶNG 1 — Structural Indexing:\nChỉ đọc Bảng ma trận / Bảng đặc tả (PDF/bảng nhiều ô gộp, 6–10 trang). KHÔNG đọc đề thi. KHÔNG đối chiếu đề.\nBóc tách thành SpecificationMatrixIndex JSON phẳng, mỗi chỉ tiêu = 1 dòng.\nBẮT BUỘC xử lý 4 bẫy:\n1) Phần II Đúng/Sai: mỗi câu có 4 ý a,b,c,d với mức độ và điểm khác nhau — bắt buộc mảng cac_y_con.\n2) Ma trận không đánh số câu (chỉ ghi số lượng): vẫn tạo chỉ tiêu Target Specs, vi_tri_du_kien để trống hoặc ghi \"slot\".\n3) Ngữ liệu: yeu_cau_ngu_lieu = Thuần túy | Thực tế | Đồ thị | Bảng biểu.\n4) Tỷ lệ toàn đề: tong_quan.ti_le_phan_tram (thường 40-30-20-10) và tong_diem (thường 10.0).\nHồ sơ: {$profileLine}\nmuc_do chỉ dùng: nhan_biet | thong_hieu | van_dung | van_dung_cao.\ndang_cau: TNKQ_4_lua_chon | TNKQ_dung_sai | TL_ngan | TL_tu_luan.\nphan_thi: Phần I | Phần II | Phần III | Tự luận.\nid dạng SPEC_01, SPEC_02, ...\nTrả JSON duy nhất đúng schema:\n{\"tong_quan\":{\"mon\":\"\",\"lop\":0,\"thoi_gian_phut\":0,\"tong_diem\":10.0,\"ti_le_phan_tram\":{\"nhan_biet\":40,\"thong_hieu\":30,\"van_dung\":20,\"van_dung_cao\":10}},\"danh_sach_chi_tieu\":[{\"id\":\"SPEC_01\",\"chu_de\":\"\",\"don_vi_kien_thuc\":\"\",\"phan_thi\":\"Phần I\",\"dang_cau\":\"TNKQ_4_lua_chon\",\"vi_tri_du_kien\":\"Câu 1\",\"muc_do\":\"nhan_biet\",\"yccd\":\"\",\"so_diem\":0.25,\"yeu_cau_ngu_lieu\":\"Thuần túy\",\"cac_y_con\":[]}]}"]],
        duyetde_file_parts($body, 'matrix', 'Ma trận đề'),
        duyetde_file_parts($body, 'spec', 'Bảng đặc tả')
    );
    if (count($parts) < 2) {
        respond(['ok' => false, 'error' => 'Thiếu PDF/văn bản ma trận hoặc bảng đặc tả để bóc tách chỉ mục.'], 422);
    }
    $result = call_gemini_with_rotation($keys, [
        'contents' => [['role' => 'user', 'parts' => $parts]],
        'generationConfig' => [
            'temperature' => 0.1,
            'responseMimeType' => 'application/json',
        ],
    ], $model, 120);
    if (empty($result['ok'])) {
        respond(['ok' => false, 'error' => $result['error'] ?? 'Không bóc tách được ma trận.'], (int)($result['status'] ?? 502));
    }
    $parsed = duyetde_parse_json_object((string)($result['text'] ?? ''));
    if (!$parsed) {
        respond(['ok' => false, 'error' => 'AI không trả JSON chỉ mục ma trận hợp lệ.', 'raw' => duyetde_clip_text((string)($result['text'] ?? ''), 4000)], 502);
    }
    $index = duyetde_normalize_matrix_index($parsed);
    if (!$index['danh_sach_chi_tieu']) {
        respond(['ok' => false, 'error' => 'Không nhận diện được chỉ tiêu nào trong ma trận/đặc tả.', 'matrix_index' => $index], 422);
    }
    $overview = $index['tong_quan'];
    respond([
        'ok' => true,
        'action' => $action,
        'matrix_index' => $index,
        'summary' => [
            'so_chi_tieu' => (int)$overview['so_chi_tieu'],
            'ti_le' => duyetde_ratio_text($overview['ti_le_phan_tram']),
            'tong_diem' => (float)$overview['tong_diem'],
            'thoi_gian_phut' => (int)$overview['thoi_gian_phut'],
        ],
        'model' => $result['model'] ?? $model,
    ]);
}

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
    $index = duyetde_normalize_matrix_index($body['matrix_index'] ?? $body['specification_matrix_index'] ?? null);
    if (!$index['danh_sach_chi_tieu']) {
        respond(['ok' => false, 'error' => 'Thiếu Specification Matrix Index. Hãy bóc tách ma trận (extract_matrix_index) và xác nhận trước khi đối chiếu. Không gửi 8–9 trang PDF ma trận kèm đề thi.'], 422);
    }
    $examParts = duyetde_file_parts($body, 'exam', 'Đề thi');
    $answerParts = duyetde_file_parts($body, 'answer', 'Đáp án/Hướng dẫn chấm gốc (nếu có)');
    if (!$examParts) {
        respond(['ok' => false, 'error' => 'Thiếu nội dung đề thi.'], 422);
    }
    $solutionJson = $body['solution'] ?? null;
    $solutionText = is_array($solutionJson)
        ? json_encode($solutionJson, JSON_UNESCAPED_UNICODE)
        : trim((string)($body['solution_text'] ?? ''));
    $groups = duyetde_group_specs_by_part($index);
    $questions = [];
    $warnings = [];
    $timeNotes = [];
    $figureNotes = [];
    $batchErrors = [];
    foreach ($groups as $partName => $specs) {
        if (!$specs) {
            continue;
        }
        $specJson = json_encode($specs, JSON_UNESCAPED_UNICODE);
        $prompt = "Bạn là chuyên gia giáo dục. CHẶNG 2 — Slot Matching & Batching.\nHồ sơ: {$profileLine}\nChỉ đối chiếu PHẦN: {$partName}. KHÔNG đọc lại toàn bộ 8–9 trang PDF ma trận. Chỉ dùng Bảng chỉ mục JSON dưới đây.\nThuật toán khớp:\n- Nếu vi_tri_du_kien có mã câu: ánh xạ đúng câu đó.\n- Nếu không có mã câu: tìm câu cùng chủ đề/phần thi, khớp ngữ nghĩa với yccd (Target Specs → Slot Matching).\n- Cảnh báo chỉ tiêu không có câu, hoặc câu không thuộc chỉ tiêu nào.\n- Phần II TNKQ_dung_sai: chấm từng ý trong cac_y_con (mức độ + điểm riêng).\n- Kiểm tra yeu_cau_ngu_lieu (Thuần túy/Thực tế/Đồ thị/Bảng biểu).\n- Ước lượng thời gian làm bài từng câu (giây) và nêu hình vẽ/đồ thị nếu có.\n3 tiêu chí: Ma trận, Hình thức, Nội dung.\n4 trạng thái: Đạt | Cần chỉnh sửa | Không đạt | Chưa đủ dữ liệu để kết luận.\nCâu lệch: viết lại cau_de_xuat, dap_an_de_xuat, huong_dan_cham_de_xuat.\nTrả JSON: {\"questions\":[{\"so_cau\":\"\",\"spec_id\":\"SPEC_01\",\"phan_thi\":\"{$partName}\",\"cau_hoi_goc\":\"\",\"trang_thai\":\"Đạt\",\"thoi_gian_giay\":0,\"hinh_ve\":\"\",\"ma_tran\":{\"spec_id\":\"SPEC_01\",\"dong\":\"\",\"chu_de\":\"\",\"don_vi_kien_thuc\":\"\",\"muc_do\":\"\",\"diem\":\"\",\"yccd\":\"\",\"yeu_cau_ngu_lieu\":\"\"},\"hinh_thuc\":{\"nhan_xet\":\"\"},\"noi_dung\":{\"nhan_xet\":\"\"},\"cac_y_con\":[],\"nhan_xet\":\"\",\"can_cu\":\"\",\"cau_de_xuat\":\"\",\"dap_an_de_xuat\":\"\",\"huong_dan_cham_de_xuat\":\"\"}],\"chi_tieu_chua_khop\":[],\"cau_thua\":[],\"thoi_gian_phut_uoc_tinh\":0,\"canh_bao_thoi_luong\":\"\"}";
        $parts = array_merge(
            [['text' => $prompt]],
            $examParts,
            $answerParts,
            [['text' => "Bảng chỉ mục JSON của {$partName} (KHÔNG phải PDF ma trận):\n" . duyetde_clip_text((string)$specJson, 50000)]]
        );
        if ($solutionText !== '') {
            $parts[] = ['text' => "Lời giải tham khảo (Pha 1):\n" . duyetde_clip_text($solutionText, 40000)];
        }
        $result = call_gemini_with_rotation($keys, [
            'contents' => [['role' => 'user', 'parts' => $parts]],
            'generationConfig' => [
                'temperature' => 0.15,
                'responseMimeType' => 'application/json',
            ],
        ], $model, 90);
        if (empty($result['ok'])) {
            $batchErrors[] = $partName . ': ' . ($result['error'] ?? 'lỗi AI');
            continue;
        }
        $parsed = duyetde_parse_json_object((string)($result['text'] ?? ''));
        if (!$parsed) {
            $batchErrors[] = $partName . ': JSON không hợp lệ';
            continue;
        }
        $questions = array_merge($questions, duyetde_normalize_eval_questions(is_array($parsed['questions'] ?? null) ? $parsed['questions'] : []));
        foreach ((array)($parsed['chi_tieu_chua_khop'] ?? []) as $miss) {
            $warnings[] = is_string($miss) ? ($partName . ': thiếu câu cho ' . $miss) : ($partName . ': chỉ tiêu chưa khớp');
        }
        foreach ((array)($parsed['cau_thua'] ?? []) as $extra) {
            $warnings[] = is_string($extra) ? ($partName . ': câu thừa ' . $extra) : ($partName . ': câu không thuộc ma trận');
        }
        if (!empty($parsed['canh_bao_thoi_luong'])) {
            $timeNotes[] = (string)$parsed['canh_bao_thoi_luong'];
        }
        if (!empty($parsed['thoi_gian_phut_uoc_tinh'])) {
            $timeNotes[] = $partName . ': ~' . $parsed['thoi_gian_phut_uoc_tinh'] . ' phút';
        }
        foreach (is_array($parsed['questions'] ?? null) ? $parsed['questions'] : [] as $q) {
            if (!empty($q['hinh_ve'])) {
                $figureNotes[] = 'Câu ' . ($q['so_cau'] ?? '') . ': ' . $q['hinh_ve'];
            }
        }
    }
    if (!$questions && $batchErrors) {
        respond(['ok' => false, 'error' => 'Không thẩm định được đề. ' . implode(' | ', $batchErrors)], 502);
    }
    $counts = duyetde_count_statuses($questions);
    $overview = $index['tong_quan'];
    $ratioText = duyetde_ratio_text($overview['ti_le_phan_tram']);
    $pointGap = abs(((float)$overview['tong_diem']) - ((float)$overview['tong_diem_tinh_tu_chi_tieu']));
    if ($pointGap > 0.2) {
        $warnings[] = 'Lệch tổng điểm ma trận: khai báo ' . $overview['tong_diem'] . ' nhưng cộng chỉ tiêu ra ' . $overview['tong_diem_tinh_tu_chi_tieu'];
    }
    $eval = [
        'tong_so_cau' => count($questions),
        'so_cau_dat' => $counts['Đạt'],
        'so_cau_can_chinh_sua' => $counts['Cần chỉnh sửa'],
        'so_cau_khong_dat' => $counts['Không đạt'],
        'so_cau_chua_du_du_lieu' => $counts['Chưa đủ dữ liệu để kết luận'],
        'ket_luan' => $counts['Không đạt'] ? 'Chưa đạt — có câu lệch ma trận/đặc tả.' : ($counts['Cần chỉnh sửa'] ? 'Cần chỉnh sửa hình thức/diễn đạt.' : 'Khớp ma trận theo bảng chỉ mục.'),
        'questions' => $questions,
        'ti_le_ma_tran' => $ratioText,
        'tong_diem_ma_tran' => $overview['tong_diem'],
        'thoi_gian_quy_dinh' => $overview['thoi_gian_phut'],
        'canh_bao_thoi_luong' => implode(' | ', array_unique($timeNotes)),
        'canh_bao_ti_le' => implode(' | ', $warnings),
        'hinh_ve_do_thi' => $figureNotes,
        'batch_errors' => $batchErrors,
        'used_matrix_index' => true,
    ];
    respond(['ok' => true, 'action' => $action, 'evaluation' => $eval, 'matrix_index' => $index, 'model' => $model]);
}

if ($action === 'recheck_question' || $action === 'recheck_single_question') {
    $question = is_array($body['question'] ?? null) ? $body['question'] : [];
    $questionText = trim((string)($question['cau_hien_tai'] ?? $question['cau_de_xuat'] ?? $question['cau_hoi'] ?? $body['question_text'] ?? ''));
    if ($questionText === '') {
        respond(['ok' => false, 'error' => 'Thiếu nội dung câu hỏi cần kiểm tra lại.'], 422);
    }
    $spec = is_array($body['spec'] ?? null) ? $body['spec'] : null;
    $maTran = is_array($question['ma_tran'] ?? null) ? $question['ma_tran'] : [];
    $specId = trim((string)($body['spec_id'] ?? $question['spec_id'] ?? $maTran['spec_id'] ?? ''));
    if (!$spec && $specId !== '' && is_array($body['matrix_index'] ?? null)) {
        $spec = duyetde_find_spec(duyetde_normalize_matrix_index($body['matrix_index']), $specId);
    }
    if (is_array($spec)) {
        $spec = duyetde_normalize_matrix_index(['danh_sach_chi_tieu' => [$spec]])['danh_sach_chi_tieu'][0] ?? $spec;
    }
    if (!$spec) {
        respond(['ok' => false, 'error' => 'Thiếu đúng 1 SPEC_id trong bảng chỉ mục. Không đọc lại 8–9 trang PDF ma trận khi kiểm tra lại câu sửa.'], 422);
    }
    $specJson = json_encode($spec, JSON_UNESCAPED_UNICODE);
    $soCau = trim((string)($question['so_cau'] ?? ''));
    $parts = [[
        'text' => "Bạn là chuyên gia giáo dục. CHẶNG 3 — Recheck 1 câu, 1 chỉ tiêu.\nHồ sơ: {$profileLine}\nChỉ đối chiếu câu đã sửa với ĐÚNG 1 dòng chỉ mục JSON. CẤM đọc lại toàn bộ ma trận PDF.\nCâu số: {$soCau}\nCâu gốc: " . trim((string)($question['cau_hoi_goc'] ?? '')) . "\nCâu đã sửa:\n{$questionText}\nĐáp án/HD chấm mới: " . trim((string)($question['dap_an_de_xuat'] ?? $question['dap_an'] ?? '')) . "\nChỉ tiêu JSON:\n{$specJson}\nKiểm tra mức độ, điểm, YCCĐ, ngữ liệu, các ý con (nếu TNKQ_dung_sai).\n4 trạng thái: Đạt | Cần chỉnh sửa | Không đạt | Chưa đủ dữ liệu để kết luận.\nTrả JSON duy nhất: {\"so_cau\":\"\",\"spec_id\":\"\",\"trang_thai\":\"Đạt\",\"nhan_xet\":\"\",\"can_cu\":\"\",\"ma_tran\":{\"spec_id\":\"\",\"dong\":\"\",\"chu_de\":\"\",\"muc_do\":\"\",\"diem\":\"\"},\"hinh_thuc\":{\"nhan_xet\":\"\"},\"noi_dung\":{\"nhan_xet\":\"\"},\"cau_de_xuat\":\"\",\"dap_an_de_xuat\":\"\",\"huong_dan_cham_de_xuat\":\"\"}",
    ]];
    $result = call_gemini_with_rotation($keys, [
        'contents' => [['role' => 'user', 'parts' => $parts]],
        'generationConfig' => [
            'temperature' => 0.1,
            'responseMimeType' => 'application/json',
        ],
    ], $model, 25);
    if (empty($result['ok'])) {
        respond(['ok' => false, 'error' => $result['error'] ?? 'Không kiểm tra lại được câu hỏi.'], (int)($result['status'] ?? 502));
    }
    $parsed = duyetde_parse_json_object((string)($result['text'] ?? ''));
    if (!$parsed) {
        respond(['ok' => false, 'error' => 'AI không trả JSON kiểm tra lại hợp lệ.', 'raw' => duyetde_clip_text((string)($result['text'] ?? ''), 4000)], 502);
    }
    $parsed['trang_thai'] = duyetde_normalize_status((string)($parsed['trang_thai'] ?? ''));
    $parsed['needs_recheck'] = false;
    $parsed['spec_id'] = (string)($parsed['spec_id'] ?? $spec['id'] ?? $specId);
    respond(['ok' => true, 'action' => 'recheck_question', 'result' => $parsed, 'model' => $result['model'] ?? $model]);
}

respond(['error' => 'Hành động AI không hợp lệ. Dùng extract_matrix_index, generate_solution, evaluate_exam hoặc recheck_question.'], 422);
