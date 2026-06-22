<?php
require_once __DIR__ . '/bootstrap.php';
require_once __DIR__ . '/hf_fallback.php';
require_once __DIR__ . '/ai_usage_log.php';

set_time_limit(180);

function exam_ai_progress_path(string $pageId): string
{
    $safe = preg_replace('/[^a-zA-Z0-9_-]/', '', $pageId);
    return sys_get_temp_dir() . DIRECTORY_SEPARATOR . 'giangbai_exam_ai_progress_' . $safe . '.txt';
}

function exam_ai_progress_set(string $pageId, int $value): void
{
    if ($pageId === '') return;
    @file_put_contents(exam_ai_progress_path($pageId), (string)max(0, min(100, $value)), LOCK_EX);
}

function exam_ai_progress_get(string $pageId): int
{
    if ($pageId === '') return 0;
    return (int)@file_get_contents(exam_ai_progress_path($pageId));
}

function exam_ai_log_gemini(string $mode, string $model, bool $ok, string $error = ''): void
{
    ai_usage_record([
        'provider' => 'gemini_browser',
        'module' => 'thitructuyen',
        'mode' => $mode,
        'model' => $model,
        'ok' => $ok,
        'error' => $ok ? '' : $error,
    ]);
}

function exam_ai_clean_text(string $text): string
{
    $text = trim($text);
    $text = preg_replace('/^[A-D]\.\s*/', '', $text) ?? $text;
    $text = str_replace(["\n", "\r"], ' ', $text);
    return trim(preg_replace('/\s+/u', ' ', $text) ?? $text);
}

function exam_ai_normalize_key(string $text): string
{
    return strtolower(preg_replace('/\s+/u', '', $text) ?? $text);
}

function exam_ai_is_duplicate(array $q1, array $q2List): bool
{
    $text1 = exam_ai_normalize_key((string)($q1['question'] ?? ''));
    if (strlen($text1) < 20) {
        $opts = is_array($q1['options'] ?? null) ? implode('', $q1['options']) : '';
        $text1 .= exam_ai_normalize_key($opts);
    }

    foreach ($q2List as $q2) {
        $text2 = exam_ai_normalize_key((string)($q2['question'] ?? ''));
        if (strlen($text2) < 20) {
            $opts = is_array($q2['options'] ?? null) ? implode('', $q2['options']) : '';
            $text2 .= exam_ai_normalize_key($opts);
        }

        similar_text($text1, $text2, $pct);
        if ($pct > 85) return true;

        if (strlen($text1) > 50 && strlen($text2) > 50) {
            if (str_contains($text1, $text2) || str_contains($text2, $text1)) return true;
        }
    }

    return false;
}

function exam_ai_decode_image(string $imageData): ?string
{
    try {
        if (str_contains($imageData, 'base64,')) {
            $imageData = explode('base64,', $imageData, 2)[1] ?? $imageData;
        }
        $bytes = base64_decode($imageData, true);
        return $bytes === false ? null : $bytes;
    } catch (Throwable $e) {
        return null;
    }
}

function exam_ai_process_paper_local(): ?array
{
    if (empty($_FILES['file']) || !is_uploaded_file($_FILES['file']['tmp_name'])) {
        return null;
    }

    $tmp = $_FILES['file']['tmp_name'];
    $name = (string)($_FILES['file']['name'] ?? 'upload');
    $ext = strtolower(pathinfo($name, PATHINFO_EXTENSION));

    if ($ext === 'pdf' && class_exists('Imagick')) {
        try {
            $imagick = new Imagick();
            $imagick->setResolution(150, 150);
            $imagick->readImage($tmp);
            $pages = [];
            $index = 0;
            foreach ($imagick as $page) {
                $index++;
                $page->setImageFormat('jpeg');
                $page->setImageCompressionQuality(80);
                $blob = $page->getImageBlob();
                $b64 = base64_encode($blob);
                $pages[] = [
                    'id' => bin2hex(random_bytes(8)),
                    'page_index' => $index,
                    'image_data' => 'data:image/jpeg;base64,' . $b64,
                    'status' => 'pending',
                    'q_count' => 0,
                ];
            }
            $imagick->clear();
            if (!empty($pages)) return ['status' => 'ok', 'pages' => $pages];
        } catch (Throwable $e) {
            return null;
        }
    }

    if (in_array($ext, ['jpg', 'jpeg', 'png', 'webp'], true)) {
        $blob = file_get_contents($tmp);
        if ($blob === false) return null;
        $mime = $ext === 'png' ? 'image/png' : ($ext === 'webp' ? 'image/webp' : 'image/jpeg');
        $b64 = base64_encode($blob);
        return [
            'status' => 'ok',
            'pages' => [[
                'id' => bin2hex(random_bytes(8)),
                'page_index' => 1,
                'image_data' => 'data:' . $mime . ';base64,' . $b64,
                'status' => 'pending',
                'q_count' => 0,
            ]],
        ];
    }

    return null;
}

function exam_ai_normalize_segment_local(array $data): ?array
{
    $apiKeys = hf_load_gemini_keys($data['api_keys'] ?? []);
    if (empty($apiKeys)) {
        return ['status' => 'error', 'message' => 'Thiếu Gemini API key. Bấm Cấu hình AI trên trang Thi trực tuyến.', 'data' => []];
    }

    $model = trim((string)($data['model'] ?? hf_default_gemini_model()));
    $pageId = trim((string)($data['page_id'] ?? ''));
    $imgBytes = exam_ai_decode_image((string)($data['image_data'] ?? ''));
    if ($imgBytes === null) {
        return ['status' => 'error', 'message' => 'Invalid Image Data', 'data' => []];
    }

    exam_ai_progress_set($pageId, 0);

    $prompt = <<<'PROMPT'
Trích xuất câu hỏi trắc nghiệm từ phần ảnh này.

YÊU CẦU QUAN TRỌNG:
1. ĐỌC KỸ: Tìm đủ các câu có đánh số (Câu X, Bài X...).
2. CHUẨN HÓA NGHIÊM NGẶT TOÁN HỌC (LATEX):
   - Bắt buộc dùng LaTeX cho TẤT CẢ công thức, ký hiệu toán học.
   - Inline Math: $...$
   - Display Math: $$...$$
3. ĐÁP ÁN: Tách riêng 4 lựa chọn A, B, C, D vào mảng "options".
4. KHÔNG BỊA ĐẶT nội dung bị cắt.
5. Nếu thấy đáp án ở đầu ảnh mà không có câu hỏi -> tạo câu "[[Tiếp nối]]".

OUTPUT JSON (Mảng): [{"question": "...", "options": ["...",...], "correct_index": -1}, ...]
PROMPT;

    exam_ai_progress_set($pageId, 20);
    $imgBase64 = base64_encode($imgBytes);
    $vision = hf_call_gemini_vision($apiKeys, $prompt, $imgBase64, $model, 3);
    exam_ai_progress_set($pageId, 80);

    if (!$vision['ok'] || !is_array($vision['data'])) {
        exam_ai_progress_set($pageId, 100);
        exam_ai_log_gemini('vision', $model, false, (string)($vision['error'] ?? 'Gemini Vision lỗi'));
        return [
            'status' => 'error',
            'message' => (string)($vision['error'] ?? 'Gemini Vision không trả về dữ liệu. Thử đổi model hoặc bật fallback HF.'),
            'data' => [],
        ];
    }
    exam_ai_log_gemini('vision', $model, true);

    $merged = [];
    foreach ($vision['data'] as $q) {
        if (!is_array($q)) continue;
        if (isset($q['options']) && is_array($q['options'])) {
            $q['options'] = array_map('exam_ai_clean_text', $q['options']);
        }
        $qText = (string)($q['question'] ?? '');
        if (preg_match('/(Câu|Question|Bài)\s*(\d+)/iu', $qText, $m)) {
            $merged[(int)$m[2]] = $q;
        } else {
            $merged[] = $q;
        }
    }

    ksort($merged, SORT_NUMERIC);
    $rawQuestions = [];
    foreach ($merged as $q) {
        if (!isset($q['options']) || !is_array($q['options'])) {
            $q['options'] = ['', '', '', ''];
        }
        $q['status'] = 'done';
        if (empty($q['id'])) {
            $q['id'] = bin2hex(random_bytes(8));
        }
        $rawQuestions[] = $q;
    }

    $unique = [];
    foreach ($rawQuestions as $q) {
        if (!exam_ai_is_duplicate($q, $unique)) {
            $unique[] = $q;
        }
    }

    exam_ai_progress_set($pageId, 100);
    return ['status' => 'ok', 'data' => $unique];
}

function exam_ai_normalize_manual_local(array $data): ?array
{
    $apiKeys = hf_load_gemini_keys($data['api_keys'] ?? []);
    if (empty($apiKeys)) return null;

    $model = trim((string)($data['model'] ?? hf_default_gemini_model()));
    $imgBytes = exam_ai_decode_image((string)($data['cropped_data'] ?? ''));
    if ($imgBytes === null) return null;

    $prompt = <<<'PROMPT'
Bạn là trợ lý AI chuyên trích xuất câu hỏi từ hình ảnh.
Trích xuất câu hỏi trắc nghiệm từ VÙNG ẢNH ĐƯỢC CUNG CẤP.
Toán học bắt buộc dùng LaTeX chuẩn: $x^2$, $\frac{a}{b}$, $\Delta$.
OUTPUT JSON (Mảng):
[{"question": "...", "options": ["A", "B", "C", "D"], "correct_index": -1}, ...]
Nếu không có câu hỏi, trả về [].
PROMPT;

    $vision = hf_call_gemini_vision($apiKeys, $prompt, base64_encode($imgBytes), $model, 3);
    if (!$vision['ok'] || !is_array($vision['data'])) {
        exam_ai_log_gemini('manual', $model, false, (string)($vision['error'] ?? 'Gemini manual lỗi'));
        return null;
    }
    exam_ai_log_gemini('manual', $model, true);

    $final = [];
    foreach ($vision['data'] as $q) {
        if (!is_array($q)) continue;
        $q['id'] = bin2hex(random_bytes(8));
        $q['status'] = 'manual';
        if (!isset($q['options']) || !is_array($q['options'])) {
            $q['options'] = ['', '', '', ''];
        }
        $final[] = $q;
    }

    return ['status' => 'ok', 'data' => $final];
}

function exam_ai_import_answer_sheet_local(array $data): ?array
{
    $apiKeys = hf_load_gemini_keys($data['api_keys'] ?? []);
    if (empty($apiKeys)) return null;

    $model = trim((string)($data['model'] ?? hf_default_gemini_model()));
    $imgBytes = exam_ai_decode_image((string)($data['image_data'] ?? ''));
    if ($imgBytes === null) return null;

    $prompt = <<<'PROMPT'
Trích xuất danh sách đáp án từ ảnh bảng đáp án này.
Output JSON: [{"index": 1, "answer": "A"}, {"index": 2, "answer": "C"}...]
PROMPT;

    $vision = hf_call_gemini_vision($apiKeys, $prompt, base64_encode($imgBytes), $model, 3);
    if (!$vision['ok'] || !is_array($vision['data'])) {
        exam_ai_log_gemini('answer_sheet', $model, false, (string)($vision['error'] ?? 'Gemini answer sheet lỗi'));
        return null;
    }
    exam_ai_log_gemini('answer_sheet', $model, true);

    return ['status' => 'ok', 'data' => $vision['data']];
}

function exam_ai_build_multipart_from_upload(): ?array
{
    if (empty($_FILES['file']) || !is_uploaded_file($_FILES['file']['tmp_name'])) {
        return null;
    }
    $tmp = $_FILES['file']['tmp_name'];
    $name = (string)($_FILES['file']['name'] ?? 'upload.bin');
    $type = (string)($_FILES['file']['type'] ?? 'application/octet-stream');
    return ['file' => new CURLFile($tmp, $type, $name)];
}

$method = $_SERVER['REQUEST_METHOD'];
$route = trim((string)($_GET['route'] ?? ''), '/');
$parts = $route === '' ? [] : explode('/', $route);
$action = $parts[0] ?? '';

if ($method === 'GET' && $action === 'progress' && !empty($parts[1])) {
    $pageId = $parts[1];
    header('Content-Type: text/event-stream; charset=utf-8');
    header('Cache-Control: no-cache');
    header('Connection: keep-alive');
    header('X-Giangbai-Source: hosting');

    $lastValue = -1;
    $deadline = time() + 180;
    while (time() < $deadline) {
        $value = exam_ai_progress_get($pageId);
        if ($value !== $lastValue) {
            $lastValue = $value;
            echo 'data: ' . $value . "\n\n";
            if (function_exists('ob_get_level') && ob_get_level() > 0) {
                @ob_flush();
            }
            flush();
        }
        if ($value >= 100) break;
        usleep(200000);
    }
    exit;
}

if ($method === 'POST' && $action === 'process_paper') {
    $local = exam_ai_process_paper_local();
    if ($local !== null) {
        header('X-Giangbai-Source: hosting');
        respond($local);
    }

    $multipart = exam_ai_build_multipart_from_upload();
    if ($multipart === null) {
        respond(['error' => 'Thiếu file upload.'], 422);
    }
    hf_proxy_json_or_respond('POST', '/api/exam/process_paper', null, $multipart, 180);
}

if ($method === 'POST' && $action === 'normalize_segment') {
    $data = json_body();
    $local = exam_ai_normalize_segment_local($data);
    if ($local !== null) {
        header('X-Giangbai-Source: hosting');
        respond($local);
    }
    hf_proxy_json_or_respond('POST', '/api/exam/normalize_segment', $data, null, 180);
}

if ($method === 'POST' && $action === 'normalize_manual') {
    $data = json_body();
    $local = exam_ai_normalize_manual_local($data);
    if ($local !== null) {
        header('X-Giangbai-Source: hosting');
        respond($local);
    }
    hf_proxy_json_or_respond('POST', '/api/exam/normalize_manual', $data, null, 180);
}

if ($method === 'POST' && $action === 'import_answer_sheet') {
    $data = json_body();
    $local = exam_ai_import_answer_sheet_local($data);
    if ($local !== null) {
        header('X-Giangbai-Source: hosting');
        respond($local);
    }
    hf_proxy_json_or_respond('POST', '/api/exam/import_answer_sheet', $data, null, 180);
}

respond(['error' => 'Route không hợp lệ.'], 404);