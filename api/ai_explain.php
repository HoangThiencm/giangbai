<?php
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/ai_usage_log.php';
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

function normalize_api_keys($value): array
{
    if (is_string($value)) {
        $value = preg_split('/[\s,]+/', $value) ?: [];
    }
    if (!is_array($value)) return [];
    return array_values(array_unique(array_filter(array_map('trim', $value))));
}

function load_ai_runtime_config(): array
{
    $config = [
        'cloudflare_worker_url' => '',
        'cloudflare_worker_secret' => '',
        'cloudflare_ai_model' => '@cf/qwen/qwen3-30b-a3b-fp8',
        'gemini_enabled' => true,
        'gemini_keys' => [],
        'gemini_model' => 'gemini-2.5-flash',
        'shopaikey_api_key' => '',
        'shopaikey_enabled' => true,
        'shopaikey_model' => 'deepseek-v4-flash',
        'shopaikey_base_url' => 'https://api.shopaikey.com/v1',
    ];

    if (defined('CLOUDFLARE_AI_WORKER_URL') && is_string(CLOUDFLARE_AI_WORKER_URL)) {
        $config['cloudflare_worker_url'] = rtrim(trim(CLOUDFLARE_AI_WORKER_URL), '/');
    }
    if (defined('CLOUDFLARE_AI_WORKER_SECRET') && is_string(CLOUDFLARE_AI_WORKER_SECRET)) {
        $config['cloudflare_worker_secret'] = trim(CLOUDFLARE_AI_WORKER_SECRET);
    }
    if (defined('CLOUDFLARE_AI_MODEL') && is_string(CLOUDFLARE_AI_MODEL) && trim(CLOUDFLARE_AI_MODEL) !== '') {
        $config['cloudflare_ai_model'] = trim(CLOUDFLARE_AI_MODEL);
    }
    if (defined('GEMINI_ENABLED')) {
        $config['gemini_enabled'] = (bool)GEMINI_ENABLED;
    }
    if (defined('SHOPAIKEY_ENABLED')) {
        $config['shopaikey_enabled'] = (bool)SHOPAIKEY_ENABLED;
    }
    if (defined('GEMINI_API_KEYS')) {
        $config['gemini_keys'] = normalize_api_keys(GEMINI_API_KEYS);
    }
    if (defined('GEMINI_MODEL') && is_string(GEMINI_MODEL) && trim(GEMINI_MODEL) !== '') {
        $config['gemini_model'] = trim(GEMINI_MODEL);
    }
    if (defined('SHOPAIKEY_API_KEY') && is_string(SHOPAIKEY_API_KEY) && trim(SHOPAIKEY_API_KEY) !== '') {
        $config['shopaikey_api_key'] = trim(SHOPAIKEY_API_KEY);
    }
    if (defined('SHOPAIKEY_MODEL') && is_string(SHOPAIKEY_MODEL) && trim(SHOPAIKEY_MODEL) !== '') {
        $config['shopaikey_model'] = trim(SHOPAIKEY_MODEL);
    }

    $globalConfigFile = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'global_config.json';
    if (is_file($globalConfigFile)) {
        $globalConfig = json_decode((string)@file_get_contents($globalConfigFile), true);
        if (is_array($globalConfig)) {
            $fileKeys = [];
            if (array_key_exists('gemini_keys', $globalConfig)) {
                $fileKeys = normalize_api_keys($globalConfig['gemini_keys']);
            } elseif (array_key_exists('global_gemini_keys', $globalConfig)) {
                $fileKeys = normalize_api_keys($globalConfig['global_gemini_keys']);
            }
            if (!empty($fileKeys)) {
                $config['gemini_keys'] = $fileKeys;
            }
            if (!empty($globalConfig['gemini_model']) && is_string($globalConfig['gemini_model'])) {
                $config['gemini_model'] = trim($globalConfig['gemini_model']);
            }
            if (array_key_exists('gemini_enabled', $globalConfig)) {
                $config['gemini_enabled'] = (bool)$globalConfig['gemini_enabled'];
            }
            if (!empty($globalConfig['cloudflare_ai_model']) && is_string($globalConfig['cloudflare_ai_model'])) {
                $config['cloudflare_ai_model'] = trim($globalConfig['cloudflare_ai_model']);
            }
            if (!empty($globalConfig['shopaikey_api_key']) && is_string($globalConfig['shopaikey_api_key'])) {
                $config['shopaikey_api_key'] = trim($globalConfig['shopaikey_api_key']);
            }
            if (!empty($globalConfig['shopaikey_model']) && is_string($globalConfig['shopaikey_model'])) {
                $config['shopaikey_model'] = trim($globalConfig['shopaikey_model']);
            }
            if (array_key_exists('shopaikey_enabled', $globalConfig)) {
                $config['shopaikey_enabled'] = (bool)$globalConfig['shopaikey_enabled'];
            }
        }
    }

    return $config;
}

function build_explain_prompt(string $subject, string $lessonTitle, string $text): string
{
    return "Ban la tro ly hoc Toan cho hoc sinh THCS. Nhiem vu duy nhat: tra loi dung phan hoc sinh vua hoi trong muc NOI DUNG CAN GIAI THICH, khong tu y chuyen sang chu de khac, khong tom tat ca bai, khong them loi chao, khong noi 'thay se giup', khong dung Markdown, khong dung **, khong dung gach ngang ---.\n\nQuy tac bat buoc:\n- Neu noi dung la mot khai niem/cau/cum tu: giai thich truc tiep khai niem/cau/cum tu do.\n- Neu noi dung la mot cong thuc: giai thich tung ky hieu va y nghia cong thuc do, giu nguyen ky hieu Toan.\n- Neu noi dung la mot bai tap: chi goi y cach lam va diem can chu y, khong lam thay tron ven neu khong duoc yeu cau.\n- Chi dua vi du khi vi du giup lam ro dung noi dung dang hoi; neu dua vi du thi that ngan.\n- Neu noi dung hoi khong ro, noi ro can them thong tin nao, khong bịa.\n- Cau cuoi cung phai ket thuc tron ven bang dau cham, dau hoi hoac dau cham than; khong dung lai giua tu.\n\nMon: {$subject}\nBai: {$lessonTitle}\nNOI DUNG CAN GIAI THICH:\n{$text}\n\nTra loi bang 2-5 cau ngan, bam sat noi dung tren.";
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

    return "Ban la tro ly hoc Toan cho hoc sinh THCS. Hoc sinh dang hoc bai va hoi them trong khung chat.\n\nQuy tac bat buoc:\n- Chi tra loi trong pham vi bai hoc va mon Toan THCS, khong lam ho toan bo bai tap neu hoc sinh chi hoi khai niem.\n- Neu la bai tap: goi y cach lam, diem can chu y, khong lam thay tron ven neu hoc sinh khong yeu cau.\n- Giu ky hieu Toan/LaTeX khi can.\n- Khong dung Markdown, khong dung **, khong loi chao dai.\n- Tra loi ngan 2-6 cau, ro rang, ket thuc tron ven bang dau cham.\n\nMon: {$subject}\nBai: {$lessonTitle}\n{$contextBlock}"
        . ($historyText !== '' ? "LICH SU CHAT GAN DAY:\n{$historyText}\n" : '')
        . "CAU HOI MOI CUA HOC SINH:\n{$question}\n\nTra loi cau hoi moi.";
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
        'formula' => 'Quy tắc hoặc công thức liên quan trong bài là',
        'example' => 'Ví dụ gần nhất trong bài cho em là',
        'definition' => 'Theo nội dung bài “' . $lessonTitle . '”, ý cần hiểu là',
        'method' => 'Gợi ý từ nội dung bài là',
        'general' => 'Phần liên quan trực tiếp trong bài là',
    ];
    $prefix = $prefixes[$intent] ?? $prefixes['general'];
    $guidance = $intent === 'method'
        ? ' Em hãy đối chiếu từng dữ kiện của câu hỏi với phần này rồi làm từng bước.'
        : ($intent === 'formula'
            ? ' Khi làm bài, hãy thay đúng số hoặc ký hiệu vào công thức rồi tính cẩn thận.'
            : ' Em hãy ghi nhớ các từ khóa trong phần này trước khi làm bài.');
    return $prefix . ': ' . rtrim($source, ".!? \t") . '.' . $guidance;
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

function call_shopaikey(string $baseUrl, string $key, string $payload): array
{
    $url = rtrim($baseUrl, '/') . '/chat/completions';
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $key,
        ],
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_TIMEOUT => 45,
    ]);
    $raw = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);
    return [$raw, $status, $curlError];
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
        : extract_shopaikey_answer($response2);
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

$runtime = load_ai_runtime_config();
$prompt = $mode === 'chat'
    ? build_chat_prompt($subject, $lessonTitle, $lessonContext, $history, $question)
    : build_explain_prompt($subject, $lessonTitle, $text);

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
        'provider' => (string)($result['provider'] ?? 'unknown'),
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

$cloudflareResult = try_cloudflare_ai_explain($runtime, $workerPayload);
if (is_array($cloudflareResult) && !empty($cloudflareResult['answer'])) {
    ai_explain_log_result($mode, $cloudflareResult, true, false);
    respond([
        'ok' => true,
        'answer' => trim($cloudflareResult['answer']),
        'complete' => answer_looks_complete($cloudflareResult['answer']),
        'provider' => 'cloudflare_workers_ai',
        'model' => $cloudflareResult['model'] ?? 'Workers AI',
    ]);
}
if (is_array($cloudflareResult) && !empty($cloudflareResult['error'])) {
    ai_explain_log_result($mode, $cloudflareResult, false, false);
}

if ($cloudflareResult === null && (empty($runtime['gemini_enabled']) || empty($runtime['gemini_keys'])) && (empty($runtime['shopaikey_enabled']) || trim((string)$runtime['shopaikey_api_key']) === '')) {
    respond(['error' => 'Chưa cấu hình Cloudflare Workers AI, Gemini hoặc ShopAIKey.'], 503);
}

$geminiResult = try_gemini_explain($runtime, $prompt);
if (is_array($geminiResult) && !empty($geminiResult['answer'])) {
    $usedFallback = is_array($cloudflareResult) && !empty($cloudflareResult['error']);
    ai_explain_log_result($mode, $geminiResult, true, $usedFallback);
    respond([
        'ok' => true,
        'answer' => trim($geminiResult['answer']),
        'complete' => answer_looks_complete($geminiResult['answer']),
        'provider' => $geminiResult['provider'] ?? 'gemini',
        'model' => $geminiResult['model'] ?? $runtime['gemini_model'],
        'fallback' => $usedFallback,
    ]);
}
if (is_array($geminiResult) && !empty($geminiResult['error'])) {
    ai_explain_log_result($mode, $geminiResult, false, false);
}

$fallbackResult = try_shopaikey_explain($runtime, $prompt);
if (is_array($fallbackResult) && !empty($fallbackResult['answer'])) {
    ai_explain_log_result($mode, $fallbackResult, true, true);
    respond([
        'ok' => true,
        'answer' => trim($fallbackResult['answer']),
        'complete' => answer_looks_complete($fallbackResult['answer']),
        'provider' => $fallbackResult['provider'] ?? 'shopaikey',
        'model' => $fallbackResult['model'] ?? $runtime['shopaikey_model'],
        'fallback' => true,
    ]);
}
if (is_array($fallbackResult) && !empty($fallbackResult['error'])) {
    ai_explain_log_result($mode, $fallbackResult, false, false);
}

$errors = [];
if (is_array($cloudflareResult) && !empty($cloudflareResult['error'])) $errors[] = 'Cloudflare Workers AI: ' . $cloudflareResult['error'];
if (is_array($geminiResult) && !empty($geminiResult['error'])) $errors[] = $geminiResult['error'];
if (is_array($fallbackResult) && !empty($fallbackResult['error'])) $errors[] = $fallbackResult['error'];
$lastError = $errors ? implode(' | ', $errors) : 'Khong goi duoc AI.';
respond(['error' => $lastError], 502);
