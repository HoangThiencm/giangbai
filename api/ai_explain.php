<?php
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/ai_usage_log.php';
require_once __DIR__ . '/ai_smart_quota.php';
require_once __DIR__ . '/ai_runtime_config.php';
require_once __DIR__ . '/ai_explain_cache.php';
require_once __DIR__ . '/ai_student_quota.php';
require_once __DIR__ . '/ai_router.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(['error' => 'Method not allowed.'], 405);
}

$data = json_body();
$mode = trim((string)($data['mode'] ?? 'explain'));
$text = trim($data['text'] ?? '');
$question = trim($data['question'] ?? '');
$lessonTitle = trim($data['lesson_title'] ?? 'bai hoc');
$subject = trim($data['subject'] ?? 'Toan');
$lessonContext = trim($data['lesson_context'] ?? '');
$lessonId = (int)($data['lesson_id'] ?? 0);
$forceProvider = strtolower(trim((string)($data['force_provider'] ?? '')));
if (!in_array($forceProvider, ['', 'ds2api'], true)) $forceProvider = '';

$currentUserId = !empty($_SESSION['user_id']) ? (int)$_SESSION['user_id'] : null;
$currentUserRole = '';
if ($currentUserId) {
    $userStmt = $pdo->prepare('SELECT role FROM users WHERE id = ? AND is_active = 1 LIMIT 1');
    $userStmt->execute([$currentUserId]);
    $currentUserRole = (string)($userStmt->fetchColumn() ?: '');
}

$history = [];
if (!empty($data['history']) && is_array($data['history'])) {
    foreach (array_slice($data['history'], -8) as $turn) {
        if (!is_array($turn)) continue;
        $role = ($turn['role'] ?? '') === 'assistant' ? 'assistant' : 'user';
        $content = trim((string)($turn['content'] ?? ''));
        if ($content !== '') {
            $history[] = ['role' => $role, 'content' => $content];
        }
    }
}

if ($mode === 'chat') {
    if ($question === '') {
        respond(['error' => 'Thieu cau hoi.'], 422);
    }
} elseif ($text === '') {
    respond(['error' => 'Thieu noi dung can giai thich.'], 422);
}

function build_explain_prompt(string $subject, string $lessonTitle, string $text): string
{
    return "Ban la giao vien Toan THCS giai thich cho hoc sinh lop 6-9. Muc tieu: giup hoc sinh HIEU RO chinh xac doan noi dung ho vua chon, KHONG lam roi them.\n\nQuy tac BAT BUOC:\n- Luon bam sat 100% doan van ban hoc sinh cung cap. Khong lan man, khong them kien thuc ngoai bai.\n- Giai thich bang tieng Viet don gian, cau ngan, tu de hieu voi hoc sinh THCS.\n- Tranh hoan toan cac tu mo ho: co the, thuong thi, noi chung, hau nhu, ve co ban.\n- Neu la khai niem: dung \"nghia la...\", \"duoc hieu la...\".\n- Neu la cong thuc: giai thich tung ky hieu va cach dung.\n- Khong dung Markdown, khong tieu de, khong **, khong chao hoi dai.\n- Ket thuc bang mot cau tom tat y chinh ro rang, ket thuc bang dau cham.\n\nMon: {$subject}\nBai: {$lessonTitle}\nDOAN NOI DUNG CAN GIAI THICH:\n{$text}\n\nTra loi bang 4-7 cau ngan, ro rang, bam sat doan tren.";
}

function build_chat_prompt(string $subject, string $lessonTitle, string $lessonContext, array $history, string $question): string
{
    $historyText = '';
    foreach ($history as $turn) {
        $role = ($turn['role'] ?? '') === 'assistant' ? 'Tro ly' : 'Hoc sinh';
        $content = trim((string)($turn['content'] ?? ''));
        if ($content !== '') {
            $historyText .= "{$role}: {$content}\n";
        }
    }

    $contextBlock = $lessonContext !== '' ? "TOM TAT BAI DANG HOC:\n{$lessonContext}\n\n" : '';

    return "Ban la tro ly hoc tap than thien cho hoc sinh THCS. Hoc sinh co the hoi ve bai dang hoc hoac mot cau hoi kien thuc khac.\n\nQuy tac BAT BUOC:\n- Tra loi truc tiep dung cau hoi cua hoc sinh.\n- Neu cau hoi lien quan bai dang hoc, uu tien dung noi dung bai hoc duoc cung cap.\n- Neu cau hoi nam ngoai bai dang hoc, van tra loi bang kien thuc pho thong chinh xac, phu hop lua tuoi; khong tu choi chi vi cau hoi nam ngoai bai.\n- Neu khong chac chan ve thong tin, noi ro muc do khong chac chan, khong bia dat.\n- Giai thich don gian, cau ngan. Giu ky hieu Toan/LaTeX khi can.\n- Khong dung Markdown, khong **, khong loi chao dai.\n- Tra loi gon, ro rang, ket thuc bang dau cham.\n\nMon dang hoc: {$subject}\nBai dang hoc: {$lessonTitle}\n{$contextBlock}"
        . ($historyText !== '' ? "LICH SU CHAT GAN DAY:\n{$historyText}\n" : '')
        . "CAU HOI CUA HOC SINH:\n{$question}\n\nTra loi.";
}

function answer_looks_complete(string $answer): bool
{
    $answer = trim($answer);
    if ($answer === '') return false;
    return (bool)preg_match('/[.!?。！？…]$/u', $answer);
}

function gemini_payload(string $prompt, int $maxTokens = 900): string
{
    return json_encode([
        'contents' => [[
            'parts' => [[ 'text' => $prompt ]]
        ]],
        'generationConfig' => [
            'temperature' => 0.2,
            'maxOutputTokens' => $maxTokens,
        ],
    ], JSON_UNESCAPED_UNICODE);
}

function shopaikey_payload(string $model, string $prompt, int $maxTokens = 900): string
{
    return json_encode([
        'model' => $model,
        'messages' => [
            ['role' => 'user', 'content' => $prompt],
        ],
        'temperature' => 0.2,
        'max_tokens' => $maxTokens,
    ], JSON_UNESCAPED_UNICODE);
}

function light_ai_normalize(string $text): string
{
    $text = preg_replace('/\[\[?AI\]\]?/u', '', $text) ?? $text;
    $text = preg_replace('/\s+/u', ' ', trim($text)) ?? trim($text);
    return trim($text);
}

function light_ai_lower(string $text): string
{
    return function_exists('mb_strtolower') ? mb_strtolower($text, 'UTF-8') : strtolower($text);
}

function light_ai_length(string $text): int
{
    return function_exists('mb_strlen') ? mb_strlen($text, 'UTF-8') : strlen($text);
}

function light_ai_substr(string $text, int $start, int $length): string
{
    return function_exists('mb_substr') ? mb_substr($text, $start, $length, 'UTF-8') : substr($text, $start, $length);
}

function light_ai_keywords(string $text): array
{
    $text = light_ai_lower($text);
    $text = preg_replace('/[^\p{L}\p{N}]+/u', ' ', $text) ?? '';
    $stopWords = array_flip([
        'là', 'và', 'của', 'có', 'cho', 'trong', 'với', 'các', 'một', 'những', 'được', 'không',
        'em', 'bài', 'học', 'này', 'đó', 'thì', 'khi', 'để', 'từ', 'hay', 'như', 'theo', 'về',
        'gì', 'sao', 'nào', 'ạ', 'ơi', 'giúp', 'mình', 'cần', 'phải', 'làm', 'thế', 'tại', 'vì'
    ]);
    $tokens = preg_split('/\s+/u', $text, -1, PREG_SPLIT_NO_EMPTY) ?: [];
    $keywords = [];
    foreach ($tokens as $token) {
        if (light_ai_length($token) < 2 || isset($stopWords[$token])) continue;
        $keywords[$token] = true;
    }
    return array_keys($keywords);
}

function light_ai_segments(string $context): array
{
    $rawSegments = preg_split('/(?:\r?\n){1,}|(?<=[.!?])\s+/u', $context) ?: [];
    $segments = [];
    $buffer = '';
    foreach ($rawSegments as $raw) {
        $part = light_ai_normalize($raw);
        if ($part === '') continue;
        $buffer = $buffer === '' ? $part : $buffer . ' ' . $part;
        if (light_ai_length($buffer) >= 55) {
            $segments[] = light_ai_substr($buffer, 0, 520);
            $buffer = '';
        }
    }
    if ($buffer !== '') $segments[] = light_ai_substr($buffer, 0, 520);
    return array_slice($segments, 0, 45);
}

function light_ai_intent(string $question): string
{
    $question = light_ai_lower($question);
    if (preg_match('/công thức|quy tắc|tính thế nào|tính như nào|tính sao/u', $question)) return 'formula';
    if (preg_match('/ví dụ|minh hoạ|chẳng hạn/u', $question)) return 'example';
    if (preg_match('/là gì|nghĩa là gì|khái niệm|định nghĩa/u', $question)) return 'definition';
    if (preg_match('/bước|cách làm|làm thế nào|giải như/u', $question)) return 'method';
    return 'general';
}

function light_ai_best_segment(string $question, string $context): ?array
{
    $queryKeywords = light_ai_keywords($question);
    if (count($queryKeywords) < 1) return null;
    $intent = light_ai_intent($question);
    $best = null;
    foreach (light_ai_segments($context) as $segment) {
        $segmentKeywords = array_flip(light_ai_keywords($segment));
        $overlap = 0;
        foreach ($queryKeywords as $keyword) {
            if (isset($segmentKeywords[$keyword])) $overlap++;
        }
        $lowerSegment = light_ai_lower($segment);
        $bonus = 0;
        if ($intent === 'formula' && (str_contains($segment, '=') || str_contains($lowerSegment, 'công thức') || str_contains($lowerSegment, 'quy tắc'))) $bonus = 1;
        if ($intent === 'example' && (str_contains($lowerSegment, 'ví dụ') || str_contains($lowerSegment, 'minh hoạ'))) $bonus = 1;
        if ($intent === 'definition' && (str_contains($lowerSegment, 'là ') || str_contains($lowerSegment, 'gọi là'))) $bonus = 1;
        $score = $overlap * 2 + $bonus;
        if ($best === null || $score > $best['score']) {
            $best = ['text' => $segment, 'score' => $score, 'overlap' => $overlap, 'bonus' => $bonus, 'intent' => $intent];
        }
    }
    // Một từ chung như “giải” hoặc “bài” không đủ để lấy nhầm đoạn lý thuyết.
    return $best && ($best['overlap'] >= 2 || ($best['overlap'] >= 1 && $best['bonus'] >= 1)) ? $best : null;
}

function light_ai_parse_linear_side(string $expression): ?array
{
    $expression = light_ai_lower($expression);
    $expression = str_replace(['×', '·', ',', ' '], ['*', '*', '.', ''], $expression);
    if ($expression === '' || !preg_match('/^[0-9x*+\-.]+$/', $expression)) return null;
    if ($expression[0] !== '+' && $expression[0] !== '-') $expression = '+' . $expression;
    preg_match_all('/([+-])([^+-]+)/', $expression, $terms, PREG_SET_ORDER);
    if (empty($terms)) return null;

    $xCoefficient = 0.0;
    $constant = 0.0;
    foreach ($terms as $termMatch) {
        $sign = $termMatch[1] === '-' ? -1.0 : 1.0;
        $term = $termMatch[2];
        if ($term === '') return null;
        if (str_contains($term, 'x')) {
            if (substr_count($term, 'x') !== 1) return null;
            $coefficient = str_replace(['x', '*'], '', $term);
            if ($coefficient !== '' && !is_numeric($coefficient)) return null;
            $xCoefficient += $sign * ($coefficient === '' ? 1.0 : (float)$coefficient);
        } elseif (is_numeric($term)) {
            $constant += $sign * (float)$term;
        } else {
            return null;
        }
    }
    return ['x' => $xCoefficient, 'constant' => $constant];
}

function light_ai_number(float $number): string
{
    if (abs($number) < 0.0000001) $number = 0.0;
    if (abs($number - round($number)) < 0.0000001) return (string)(int)round($number);
    return rtrim(rtrim(number_format($number, 6, '.', ''), '0'), '.');
}

function light_ai_linear_term(float $coefficient): string
{
    if (abs($coefficient - 1) < 0.0000001) return 'x';
    if (abs($coefficient + 1) < 0.0000001) return '-x';
    return light_ai_number($coefficient) . 'x';
}

function try_light_ai_linear_equation(string $input): ?array
{
    // Never reduce a higher-degree equation to a linear substring. For
    // example, 2x^2+3x+1=0 used to be misread as 3x+1=0.
    if (preg_match('/x\s*(?:\^|\*\*)\s*[2-9]|x\s*[²³⁴⁵⁶⁷⁸⁹]/iu', $input)) return null;
    if (!preg_match('/([0-9xX×*+\-.,\s]+)=([0-9xX×*+\-.,\s]+)/u', $input, $match)) return null;
    $left = light_ai_parse_linear_side($match[1]);
    $right = light_ai_parse_linear_side($match[2]);
    if ($left === null || $right === null) return null;

    $coefficient = $left['x'] - $right['x'];
    $rightSide = $right['constant'] - $left['constant'];
    if (abs($coefficient) < 0.0000001) return null;
    $solution = $rightSide / $coefficient;
    $equation = trim($match[1]) . ' = ' . trim($match[2]);
    $middle = light_ai_linear_term($coefficient) . ' = ' . light_ai_number($rightSide);
    $answer = 'Ta có ' . $equation . '. Chuyển các hạng có x về một vế và các số về vế kia: ' . $middle . '. ';
    $answer .= abs($coefficient - 1) < 0.0000001
        ? 'Vậy x = ' . light_ai_number($solution) . '.'
        : 'Chia hai vế cho ' . light_ai_number($coefficient) . ', được x = ' . light_ai_number($solution) . '.';
    return [
        'answer' => $answer,
        'provider' => 'light_ai_math',
        'model' => 'bo-giai-phuong-trinh-bac-nhat',
        'confidence' => 'high',
    ];
}

function light_ai_answer(string $lessonTitle, string $question, string $source, string $intent): string
{
    $source = light_ai_normalize($source);
    $source = light_ai_substr($source, 0, 460);
    $prefixes = [
        'formula' => 'Công thức hoặc quy tắc trong bài là',
        'example' => 'Ví dụ trong bài:',
        'definition' => 'Trong bài “' . $lessonTitle . '” có nội dung:',
        'method' => 'Hướng dẫn từ bài học:',
        'general' => 'Phần liên quan trong bài:',
    ];
    $prefix = $prefixes[$intent] ?? $prefixes['general'];
    $guidance = $intent === 'method'
        ? ' Em hãy xem lại phần này và làm từng bước.'
        : ($intent === 'formula'
            ? ' Thay số hoặc ký hiệu vào đúng công thức rồi tính.'
            : ' Ghi nhớ ý chính rồi áp dụng.');
    return $prefix . ' ' . rtrim($source, ".!? \t") . '. ' . $guidance;
}

function try_light_ai_explain(array $config, string $mode, string $lessonTitle, string $text, string $question, string $lessonContext): ?array
{
    if (empty($config['light_ai_enabled'])) return null;

    $mathResult = try_light_ai_linear_equation($mode === 'chat' ? $question : $text);
    if ($mathResult !== null) return $mathResult;

    if ($mode !== 'chat') {
        $selected = light_ai_normalize($text);
        if (light_ai_length($selected) < 12) return null;
        return [
            'answer' => light_ai_answer($lessonTitle, $selected, $selected, str_contains($selected, '=') ? 'formula' : 'definition'),
            'provider' => 'light_ai',
            'model' => 'noi-dung-bai-hoc',
            'confidence' => 'high',
        ];
    }

    $matched = light_ai_best_segment($question, $lessonContext);
    if ($matched === null) return null;
    return [
        'answer' => light_ai_answer($lessonTitle, $question, $matched['text'], $matched['intent']),
        'provider' => 'light_ai',
        'model' => 'noi-dung-bai-hoc',
        'confidence' => $matched['score'] >= 4 ? 'high' : 'medium',
    ];
}

function call_gemini(string $model, string $key, string $payload): array
{
    $url = 'https://generativelanguage.googleapis.com/v1beta/models/' . rawurlencode($model) . ':generateContent?key=' . rawurlencode($key);
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_TIMEOUT => 30,
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);
    return [$raw, $status, $curlError];
}

function call_openai_compatible_chat(
    string $baseUrl,
    string $key,
    string $payload,
    int $timeout = 45,
    array $extraHeaders = []
): array
{
    $url = rtrim($baseUrl, '/') . '/chat/completions';
    $headers = ['Content-Type: application/json'];
    if (trim($key) !== '') {
        $headers[] = 'Authorization: Bearer ' . $key;
    }
    foreach ($extraHeaders as $header) {
        if (is_string($header) && trim($header) !== '') $headers[] = trim($header);
    }
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => $headers,
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_CONNECTTIMEOUT => 8,
        CURLOPT_TIMEOUT => $timeout,
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);
    return [$raw, $status, $curlError];
}

function call_shopaikey(string $baseUrl, string $key, string $payload): array
{
    return call_openai_compatible_chat($baseUrl, $key, $payload, 45);
}

function call_ds2api(string $baseUrl, string $key, string $payload): array
{
    // DS2API officially accepts both Bearer and x-api-key. Send both to remain
    // compatible with Vercel/runtime variants that only inspect one source.
    $extraHeaders = trim($key) !== '' ? ['x-api-key: ' . trim($key)] : [];
    return call_openai_compatible_chat($baseUrl, $key, $payload, 60, $extraHeaders);
}

function call_cloudflare_worker(string $workerUrl, string $secret, array $payload): array
{
    $ch = curl_init(rtrim($workerUrl, '/') . '/chat');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'X-Giangbai-Worker-Secret: ' . $secret,
        ],
        CURLOPT_POSTFIELDS => json_encode($payload, JSON_UNESCAPED_UNICODE),
        CURLOPT_CONNECTTIMEOUT => 8,
        CURLOPT_TIMEOUT => 35,
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);
    return [$raw, $status, $curlError];
}

function extract_gemini_answer(array $response): string
{
    $parts = $response['candidates'][0]['content']['parts'] ?? [];
    $answer = '';
    foreach ($parts as $part) {
        if (!empty($part['text'])) $answer .= $part['text'];
    }
    return trim($answer);
}

function extract_shopaikey_answer(array $response): string
{
    return trim((string)($response['choices'][0]['message']['content'] ?? ''));
}

function should_retry_provider(int $status, string $errorMessage = ''): bool
{
    if ($status === 429 || $status >= 500) return true;
    $message = strtolower($errorMessage);
    return str_contains($message, 'quota')
        || str_contains($message, 'rate limit')
        || str_contains($message, 'resource exhausted')
        || str_contains($message, 'overloaded');
}

function complete_answer_if_needed(string $provider, callable $caller, string $answer, array $meta): array
{
    $finishReason = $meta['finish_reason'] ?? '';
    $needsMore = ($finishReason === 'MAX_TOKENS' || $finishReason === 'length' || !answer_looks_complete($answer));
    if (!$needsMore || strlen($answer) >= 3600) {
        return [$answer, $meta];
    }

    $continuePrompt = "Day la cau tra loi dang bi ngat giua chung. Hay viet tiep phan con thieu de ket thuc tron ven 1-2 cau, khong lap lai phan da co, khong Markdown.\n\nPhan da co:\n{$answer}";
    [$raw2, $status2, $curlError2, $response2] = $caller($continuePrompt, 300);
    if ($raw2 === false || $raw2 === '' || $status2 < 200 || $status2 >= 300) {
        return [$answer, array_merge($meta, ['continue_error' => $curlError2 ?: 'Khong noi tiep duoc cau tra loi.'])];
    }

    $more = $provider === 'gemini'
        ? extract_gemini_answer($response2)
        : extract_shopaikey_answer($response2); // ds2api + shopaikey: OpenAI format
    if ($more !== '') {
        $answer = rtrim($answer) . ' ' . ltrim($more);
    }
    return [$answer, $meta];
}

function try_gemini_explain(array $config, string $prompt): ?array
{
    if (empty($config['gemini_enabled'])) return null;
    $keys = $config['gemini_keys'] ?? [];
    if (empty($keys)) return null;

    $model = $config['gemini_model'] ?? 'gemini-2.5-flash';
    $lastKeyFile = sys_get_temp_dir() . DIRECTORY_SEPARATOR . 'giangbai_gemini_last_key.txt';
    $lastUsedKey = is_file($lastKeyFile) ? trim((string)@file_get_contents($lastKeyFile)) : '';
    if ($lastUsedKey !== '') {
        $keys = array_merge(array_values(array_filter($keys, fn($key) => $key !== $lastUsedKey)), [$lastUsedKey]);
    }

    $lastError = 'Khong goi duoc Gemini.';
    foreach ($keys as $key) {
        $caller = function (string $textPrompt, int $maxTokens = 900) use ($model, $key) {
            [$raw, $status, $curlError] = call_gemini($model, $key, gemini_payload($textPrompt, $maxTokens));
            $response = is_string($raw) && $raw !== '' ? (json_decode($raw, true) ?: []) : [];
            return [$raw, $status, $curlError, $response];
        };

        [$raw, $status, $curlError, $response] = $caller($prompt);
        if ($raw === false || $raw === '') {
            $lastError = $curlError ?: 'Gemini khong phan hoi.';
            continue;
        }

        if ($status >= 200 && $status < 300) {
            $answer = extract_gemini_answer($response);
            if ($answer === '') {
                $lastError = 'Gemini tra ve noi dung rong.';
                continue;
            }
            $finishReason = $response['candidates'][0]['finishReason'] ?? '';
            [$answer, ] = complete_answer_if_needed('gemini', $caller, $answer, ['finish_reason' => $finishReason]);
            @file_put_contents($lastKeyFile, $key, LOCK_EX);
            return array_merge([
                'answer' => $answer,
                'provider' => 'gemini',
                'model' => $model,
            ], ai_usage_extract_gemini_tokens($response));
        }

        $lastError = $response['error']['message'] ?? ('Gemini loi HTTP ' . $status);
        if (should_retry_provider($status, $lastError)) {
            continue;
        }
    }

    return ['error' => $lastError, 'provider' => 'gemini'];
}

function try_ds2api_explain(array $config, string $prompt): ?array
{
    if (empty($config['ds2api_enabled'])) return null;
    $baseUrl = normalize_ds2api_base_url((string)($config['ds2api_base_url'] ?? ''));
    $apiKey = ds2api_effective_api_key((string)($config['ds2api_api_key'] ?? ''));
    if ($baseUrl === '') return null;
    if ($apiKey === '') {
        return [
            'error' => 'DS2API chưa có client API key. Key phải trùng với một key trong config.keys của DS2API Admin.',
            'provider' => 'ds2api',
        ];
    }

    $model = trim((string)($config['ds2api_model'] ?? 'deepseek-v4-flash')) ?: 'deepseek-v4-flash';

    $caller = function (string $textPrompt, int $maxTokens = 900) use ($baseUrl, $apiKey, $model) {
        [$raw, $status, $curlError] = call_ds2api($baseUrl, $apiKey, shopaikey_payload($model, $textPrompt, $maxTokens));
        $response = is_string($raw) && $raw !== '' ? (json_decode($raw, true) ?: []) : [];
        return [$raw, $status, $curlError, $response];
    };

    [$raw, $status, $curlError, $response] = $caller($prompt);
    if ($raw === false || $raw === '') {
        return ['error' => $curlError ?: 'DS2API khong phan hoi.', 'provider' => 'ds2api'];
    }

    if ($status >= 200 && $status < 300) {
        $answer = extract_shopaikey_answer($response);
        if ($answer === '') {
            return ['error' => 'DS2API tra ve noi dung rong.', 'provider' => 'ds2api'];
        }
        $finishReason = $response['choices'][0]['finish_reason'] ?? '';
        [$answer, ] = complete_answer_if_needed('ds2api', $caller, $answer, ['finish_reason' => $finishReason]);
        return array_merge([
            'answer' => $answer,
            'provider' => 'ds2api',
            'model' => $model,
        ], ai_usage_extract_shopaikey_tokens($response));
    }

    if ($status === 401) {
        $errorMessage = 'DS2API từ chối API key (HTTP 401). Kiểm tra key này có trong config.keys của DS2API Admin và cấu hình Vercel đã được đồng bộ.';
    } else {
        $errorMessage = $response['error']['message'] ?? ($response['message'] ?? ('DS2API lỗi HTTP ' . $status));
    }
    return ['error' => $errorMessage, 'provider' => 'ds2api'];
}

function try_shopaikey_explain(array $config, string $prompt): ?array
{
    if (empty($config['shopaikey_enabled'])) return null;
    $apiKey = trim((string)($config['shopaikey_api_key'] ?? ''));
    if ($apiKey === '') return null;

    $model = trim((string)($config['shopaikey_model'] ?? 'deepseek-v4-flash')) ?: 'deepseek-v4-flash';
    $baseUrl = trim((string)($config['shopaikey_base_url'] ?? 'https://api.shopaikey.com/v1'));

    $caller = function (string $textPrompt, int $maxTokens = 900) use ($baseUrl, $apiKey, $model) {
        [$raw, $status, $curlError] = call_shopaikey($baseUrl, $apiKey, shopaikey_payload($model, $textPrompt, $maxTokens));
        $response = is_string($raw) && $raw !== '' ? (json_decode($raw, true) ?: []) : [];
        return [$raw, $status, $curlError, $response];
    };

    [$raw, $status, $curlError, $response] = $caller($prompt);
    if ($raw === false || $raw === '') {
        return ['error' => $curlError ?: 'ShopAIKey khong phan hoi.', 'provider' => 'shopaikey'];
    }

    if ($status >= 200 && $status < 300) {
        $answer = extract_shopaikey_answer($response);
        if ($answer === '') {
            return ['error' => 'ShopAIKey tra ve noi dung rong.', 'provider' => 'shopaikey'];
        }
        $finishReason = $response['choices'][0]['finish_reason'] ?? '';
        [$answer, ] = complete_answer_if_needed('shopaikey', $caller, $answer, ['finish_reason' => $finishReason]);
        return array_merge([
            'answer' => $answer,
            'provider' => 'shopaikey',
            'model' => $model,
        ], ai_usage_extract_shopaikey_tokens($response));
    }

    $errorMessage = $response['error']['message'] ?? ($response['message'] ?? ('ShopAIKey loi HTTP ' . $status));
    return ['error' => $errorMessage, 'provider' => 'shopaikey'];
}

function ai_explain_cache_eligible(string $mode, string $text, string $question): bool
{
    $minLen = 8;
    if ($mode === 'chat') {
        return mb_strlen(ai_explain_cache_normalize($question)) >= $minLen;
    }
    return mb_strlen(ai_explain_cache_normalize($text)) >= $minLen;
}

function ai_explain_respond_success(
    string $cacheKey,
    string $mode,
    string $subject,
    string $lessonTitle,
    array $result,
    bool $fromCache = false,
    ?array $quotaStatus = null
): void {
    $answer = trim((string)($result['answer'] ?? ''));
    $complete = !empty($result['complete']) || answer_looks_complete($answer);

    // Conversational answers should always reflect the current provider and
    // current history, so student chat is intentionally never cached.
    if (!$fromCache && $mode !== 'chat' && $answer !== '' && $complete) {
        ai_explain_cache_put($cacheKey, [
            'answer' => $answer,
            'complete' => true,
            'provider' => (string)($result['provider'] ?? ''),
            'model' => (string)($result['model'] ?? ''),
            'mode' => $mode,
            'subject' => $subject,
            'lesson_title' => $lessonTitle,
        ]);
    }

    $payload = [
        'ok' => true,
        'answer' => $answer,
        'complete' => $complete,
        'provider' => (string)($result['provider'] ?? ($fromCache ? 'cache' : '')),
        'model' => (string)($result['model'] ?? ''),
        'quota' => $quotaStatus ?? ai_smart_quota_status(),
        'student_quota' => ai_student_quota_status($GLOBALS['ai_explain_user_id'] ?? null, (string)($GLOBALS['ai_explain_user_role'] ?? '')),
    ];
    if (!empty($result['router_tier'])) {
        $payload['router_tier'] = (string)$result['router_tier'];
    }
    if ($fromCache) {
        $payload['cached'] = true;
        if (!empty($result['hits'])) {
            $payload['cache_hits'] = (int)$result['hits'];
        }
    }
    if (!empty($result['fallback'])) {
        $payload['fallback'] = true;
    }
    respond($payload);
}

$runtime = load_ai_runtime_config();
// The student chat currently doubles as a DS2API verification surface.
// When requested by the first-party UI, do not let fallback providers hide a
// DS2API authentication, model, network, or upstream error.
if ($mode === 'chat' && $forceProvider === 'ds2api') {
    $runtime['ai_test_ds2api_only'] = true;
}
$GLOBALS['ai_explain_user_id'] = $currentUserId;
$GLOBALS['ai_explain_user_role'] = $currentUserRole;

$prompt = $mode === 'chat'
    ? build_chat_prompt($subject, $lessonTitle, $lessonContext, $history, $question)
    : build_explain_prompt($subject, $lessonTitle, $text);

$cacheKey = ai_explain_cache_make_key($mode, $lessonId, $subject, $lessonTitle, $text, $question, $lessonContext, $history);
// Test-only mode must hit DS2API on every request; a cached answer would make
// the UI look successful without exercising DS2API at all.
if ($mode !== 'chat'
    && empty($runtime['ai_test_ds2api_only'])
    && ai_explain_cache_eligible($mode, $text, $question)) {
    $cached = ai_explain_cache_get($cacheKey);
    if (is_array($cached) && trim((string)($cached['answer'] ?? '')) !== '') {
        ai_usage_record([
            'provider' => 'explain_cache',
            'module' => 'lotrinh',
            'mode' => $mode,
            'model' => (string)($cached['model'] ?? 'cache'),
            'ok' => true,
        ]);
        ai_explain_respond_success($cacheKey, $mode, $subject, $lessonTitle, $cached, true);
    }
}

ai_student_quota_require($currentUserId, $currentUserRole);

function try_cloudflare_ai_explain(array $config, array $payload): ?array
{
    $workerUrl = trim((string)($config['cloudflare_worker_url'] ?? ''));
    $secret = trim((string)($config['cloudflare_worker_secret'] ?? ''));
    if ($workerUrl === '' || $secret === '') return null;

    [$raw, $status, $curlError] = call_cloudflare_worker($workerUrl, $secret, $payload);
    $response = is_string($raw) && $raw !== '' ? (json_decode($raw, true) ?: []) : [];
    if ($status >= 200 && $status < 300) {
        $answer = trim((string)($response['answer'] ?? ''));
        if ($answer !== '') {
            $usage = is_array($response['usage'] ?? null) ? $response['usage'] : [];
            return [
                'answer' => $answer,
                'provider' => 'cloudflare_workers_ai',
                'model' => trim((string)($response['model'] ?? 'Workers AI')),
                'prompt_tokens' => (int)($usage['prompt_tokens'] ?? 0),
                'completion_tokens' => (int)($usage['completion_tokens'] ?? 0),
                'total_tokens' => (int)($usage['total_tokens'] ?? 0),
            ];
        }
    }
    $error = trim((string)($response['error'] ?? ''));
    if ($error === '') {
        $error = $curlError !== ''
            ? 'Không kết nối được Worker: ' . $curlError
            : 'Worker không trả dữ liệu (HTTP ' . $status . ').';
    }
    return [
        'error' => $error,
        'provider' => 'cloudflare_workers_ai',
    ];
}

$workerPayload = [
    'mode' => $mode,
    'subject' => $subject,
    'lesson_title' => $lessonTitle,
    'text' => $text,
    'question' => $question,
    'lesson_context' => $lessonContext,
    'history' => $history,
    'model' => $runtime['cloudflare_ai_model'],
];
function ai_explain_log_result(string $mode, array $result, bool $ok, bool $fallback = false): void
{
    ai_usage_record([
        'provider' => (string)($result['provider'] ?? 'cloudflare_workers_ai'),
        'module' => 'lotrinh',
        'mode' => $mode,
        'model' => (string)($result['model'] ?? ''),
        'ok' => $ok,
        'fallback' => $fallback,
        'prompt_tokens' => (int)($result['prompt_tokens'] ?? 0),
        'completion_tokens' => (int)($result['completion_tokens'] ?? 0),
        'total_tokens' => (int)($result['total_tokens'] ?? 0),
        'estimated_usd' => isset($result['estimated_usd']) ? (float)$result['estimated_usd'] : 0.0,
        'error' => $ok ? '' : (string)($result['error'] ?? ''),
    ]);
}

$quotaCfg = ai_smart_quota_load_config();

$routerOut = ai_router_run([
    'config' => $runtime,
    'mode' => $mode,
    'subject' => $subject,
    'lessonTitle' => $lessonTitle,
    'text' => $text,
    'question' => $question,
    'lessonContext' => $lessonContext,
    'history' => $history,
    'prompt' => $prompt,
    'workerPayload' => $workerPayload,
    'log' => 'ai_explain_log_result',
    'providers' => [
        'light' => function () use ($runtime, $mode, $lessonTitle, $text, $question, $lessonContext) {
            return try_light_ai_explain($runtime, $mode, $lessonTitle, $text, $question, $lessonContext);
        },
        'ds2api' => function () use ($runtime, $prompt) {
            return try_ds2api_explain($runtime, $prompt);
        },
        'cloudflare' => function () use ($runtime, $workerPayload) {
            return try_cloudflare_ai_explain($runtime, $workerPayload);
        },
        'gemini' => function () use ($runtime, $prompt) {
            return try_gemini_explain($runtime, $prompt);
        },
        'shopaikey' => function () use ($runtime, $prompt) {
            return try_shopaikey_explain($runtime, $prompt);
        },
    ],
]);

if (!empty($routerOut['blocked'])) {
    respond([
        'error' => $routerOut['error'] ?? 'Hôm nay đã hết quota AI miễn phí.',
        'code' => $routerOut['code'] ?? 'quota_exhausted_block',
        'quota' => $routerOut['quota'] ?? ai_smart_quota_status(),
        'student_quota' => ai_student_quota_status($currentUserId, $currentUserRole),
    ], 503);
}

if (!empty($routerOut['error'])) {
    respond([
        'error' => $routerOut['error'],
        'quota' => $routerOut['quota'] ?? ai_smart_quota_status(),
        'student_quota' => ai_student_quota_status($currentUserId, $currentUserRole),
        'tiers_tried' => $routerOut['tiers_tried'] ?? [],
    ], 502);
}

$result = $routerOut['result'] ?? [];
if (!empty($routerOut['used_api'])) {
    ai_student_quota_consume($currentUserId, $currentUserRole);
    if (($result['provider'] ?? '') === 'cloudflare_workers_ai') {
        $neurons = ai_smart_quota_estimate_neurons(
            (string)($result['model'] ?? $runtime['cloudflare_ai_model']),
            (int)($result['prompt_tokens'] ?? 0),
            (int)($result['completion_tokens'] ?? 0),
            (int)$quotaCfg['avg_neurons_per_call']
        );
        ai_smart_quota_add_neurons($neurons);
    }
}

$quotaStatus = $routerOut['quota'] ?? ai_smart_quota_status();
ai_explain_respond_success($cacheKey, $mode, $subject, $lessonTitle, $result, false, $quotaStatus);
