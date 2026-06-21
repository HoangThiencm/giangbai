<?php
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/hf_fallback.php';

set_time_limit(300);

function tronde_build_multipart(): ?array
{
    $multipart = [];
    foreach ($_POST as $key => $value) {
        $multipart[$key] = is_array($value) ? json_encode($value, JSON_UNESCAPED_UNICODE) : (string)$value;
    }
    foreach ($_FILES as $field => $file) {
        if (!is_array($file) || empty($file['tmp_name']) || !is_uploaded_file($file['tmp_name'])) {
            continue;
        }
        $multipart[$field] = new CURLFile(
            $file['tmp_name'],
            (string)($file['type'] ?? 'application/octet-stream'),
            (string)($file['name'] ?? 'file')
        );
    }
    return count($multipart) > 0 ? $multipart : null;
}

function tronde_ocr_answers_local(): ?array
{
    if (empty($_FILES['file']) || !is_uploaded_file($_FILES['file']['tmp_name'])) {
        return null;
    }

    $apiKey = trim((string)($_POST['api_key'] ?? ''));
    $model = trim((string)($_POST['model'] ?? hf_default_gemini_model()));
    $keys = hf_load_gemini_keys($apiKey !== '' ? [$apiKey] : []);
    if (empty($keys)) return null;

    $blob = file_get_contents($_FILES['file']['tmp_name']);
    if ($blob === false || $blob === '') return null;

    $prompt = <<<'PROMPT'
Trích xuất bảng đáp án trắc nghiệm từ ảnh.
Trả về JSON duy nhất dạng:
{"answers":{"1":"A","2":"B"},"total":2}
Chỉ dùng A/B/C/D cho đáp án.
PROMPT;

    $vision = hf_call_gemini_vision($keys, $prompt, base64_encode($blob), $model, 3);
    if (!$vision['ok']) return null;

    $answers = [];
    $total = 0;

    if (is_array($vision['data'])) {
        $first = $vision['data'][0] ?? $vision['data'];
        if (is_array($first) && isset($first['answers']) && is_array($first['answers'])) {
            $answers = $first['answers'];
            $total = (int)($first['total'] ?? count($answers));
        } else {
            foreach ($vision['data'] as $row) {
                if (!is_array($row)) continue;
                $idx = (string)($row['index'] ?? $row['question'] ?? '');
                $ans = strtoupper(trim((string)($row['answer'] ?? '')));
                if ($idx !== '' && $ans !== '') {
                    $answers[$idx] = $ans;
                }
            }
            $total = count($answers);
        }
    }

    if (empty($answers)) return null;

    return ['answers' => $answers, 'total' => $total];
}

function tronde_read_answers_from_docx_local(): ?array
{
    if (empty($_FILES['file']) || !is_uploaded_file($_FILES['file']['tmp_name'])) {
        return null;
    }

    if (!class_exists('ZipArchive')) return null;

    $zip = new ZipArchive();
    if ($zip->open($_FILES['file']['tmp_name']) !== true) return null;

    $xml = $zip->getFromName('word/document.xml');
    $zip->close();
    if ($xml === false || $xml === '') return null;

    $text = strip_tags(str_replace(['</w:p>', '</w:tr>'], "\n", $xml));
    $text = html_entity_decode($text, ENT_QUOTES | ENT_XML1, 'UTF-8');
    $text = preg_replace("/\r\n|\r/", "\n", $text) ?? $text;

    $answers = [];
    $lines = preg_split('/\n+/u', $text) ?: [];
    foreach ($lines as $line) {
        $line = trim($line);
        if ($line === '') continue;
        if (preg_match('/^(?:Câu|Cau|Question)?\s*(\d+)\s*[:.\-]?\s*([ABCDabcd])/u', $line, $m)) {
            $answers[(string)(int)$m[1]] = strtoupper($m[2]);
            continue;
        }
        if (preg_match('/^(\d+)\s*[\.\)]\s*([ABCDabcd])/u', $line, $m)) {
            $answers[(string)(int)$m[1]] = strtoupper($m[2]);
        }
    }

    if (empty($answers)) return null;
    return ['answers' => $answers, 'total' => count($answers)];
}

$method = $_SERVER['REQUEST_METHOD'];
$route = trim((string)($_GET['route'] ?? ''), '/');
if ($route === '' && !empty($_SERVER['PATH_INFO'])) {
    $route = trim((string)$_SERVER['PATH_INFO'], '/');
}

if ($method !== 'POST' || $route === '') {
    respond(['error' => 'Route không hợp lệ.'], 404);
}

$local = null;
if ($route === 'ocr-answers-from-image') {
    $local = tronde_ocr_answers_local();
} elseif ($route === 'read-answers-from-file') {
    $local = tronde_read_answers_from_docx_local();
}

if ($local !== null) {
    header('X-Giangbai-Source: hosting');
    respond($local);
}

$multipart = tronde_build_multipart();
if ($multipart === null) {
    respond(['error' => 'Thiếu dữ liệu upload.'], 422);
}

$binaryRoutes = ['auto-clean-docx', 'mix-word-exam'];
if (in_array($route, $binaryRoutes, true)) {
    hf_proxy_binary_or_respond('POST', '/' . $route, $multipart, 300);
}

hf_proxy_json_or_respond('POST', '/' . $route, null, $multipart, 300);