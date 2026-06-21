<?php

function ai_usage_timezone(): DateTimeZone
{
    $tz = defined('APP_TIMEZONE') && is_string(APP_TIMEZONE) && APP_TIMEZONE !== ''
        ? APP_TIMEZONE
        : 'Asia/Ho_Chi_Minh';
    try {
        return new DateTimeZone($tz);
    } catch (Throwable $e) {
        return new DateTimeZone('Asia/Ho_Chi_Minh');
    }
}

function ai_usage_today_key(): string
{
    return (new DateTimeImmutable('now', ai_usage_timezone()))->format('Y-m-d');
}

function ai_usage_file_path(): string
{
    $dir = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'data';
    if (!is_dir($dir)) {
        @mkdir($dir, 0755, true);
    }
    return $dir . DIRECTORY_SEPARATOR . 'ai_usage.json';
}

function ai_usage_default_store(): array
{
    return [
        'version' => 1,
        'updated_at' => null,
        'by_day' => [],
        'recent' => [],
    ];
}

function ai_usage_load_store(): array
{
    $path = ai_usage_file_path();
    if (!is_file($path)) {
        return ai_usage_default_store();
    }
    $raw = @file_get_contents($path);
    if (!is_string($raw) || trim($raw) === '') {
        return ai_usage_default_store();
    }
    $data = json_decode($raw, true);
    if (!is_array($data)) {
        return ai_usage_default_store();
    }
    if (!isset($data['by_day']) || !is_array($data['by_day'])) {
        $data['by_day'] = [];
    }
    if (!isset($data['recent']) || !is_array($data['recent'])) {
        $data['recent'] = [];
    }
    $data['version'] = 1;
    return $data;
}

function ai_usage_save_store(array $store): bool
{
    $store['updated_at'] = (new DateTimeImmutable('now', ai_usage_timezone()))->format(DateTimeInterface::ATOM);
    $path = ai_usage_file_path();
    $json = json_encode($store, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    if (!is_string($json)) {
        return false;
    }
    return @file_put_contents($path, $json, LOCK_EX) !== false;
}

function ai_usage_mutate_store(callable $mutator): bool
{
    $path = ai_usage_file_path();
    $dir = dirname($path);
    if (!is_dir($dir)) {
        @mkdir($dir, 0755, true);
    }

    $fp = @fopen($path, 'c+');
    if ($fp === false) {
        return false;
    }

    try {
        if (!@flock($fp, LOCK_EX)) {
            return false;
        }

        rewind($fp);
        $raw = stream_get_contents($fp);
        $store = ai_usage_default_store();
        if (is_string($raw) && trim($raw) !== '') {
            $decoded = json_decode($raw, true);
            if (is_array($decoded)) {
                $store = $decoded;
                if (!isset($store['by_day']) || !is_array($store['by_day'])) {
                    $store['by_day'] = [];
                }
                if (!isset($store['recent']) || !is_array($store['recent'])) {
                    $store['recent'] = [];
                }
                $store['version'] = 1;
            }
        }

        $mutator($store);

        $store['updated_at'] = (new DateTimeImmutable('now', ai_usage_timezone()))->format(DateTimeInterface::ATOM);
        $json = json_encode($store, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        if (!is_string($json)) {
            return false;
        }

        rewind($fp);
        ftruncate($fp, 0);
        $written = fwrite($fp, $json);
        fflush($fp);
        return $written !== false;
    } finally {
        @flock($fp, LOCK_UN);
        fclose($fp);
    }
}

function ai_usage_provider_bucket(array &$day, string $provider): array
{
    if (!isset($day['providers']) || !is_array($day['providers'])) {
        $day['providers'] = [];
    }
    if (!isset($day['providers'][$provider]) || !is_array($day['providers'][$provider])) {
        $day['providers'][$provider] = [
            'calls' => 0,
            'success' => 0,
            'error' => 0,
            'fallback_success' => 0,
            'prompt_tokens' => 0,
            'completion_tokens' => 0,
            'total_tokens' => 0,
            'estimated_usd' => 0.0,
        ];
    }
    return $day['providers'][$provider];
}

function ai_usage_estimate_shopaikey_usd(string $model, int $promptTokens, int $completionTokens): float
{
    $model = strtolower(trim($model));
    $rates = [
        'deepseek-v4-flash' => ['in' => 0.07, 'out' => 0.27],
        'deepseek-chat' => ['in' => 0.27, 'out' => 1.10],
        'deepseek-reasoner' => ['in' => 0.55, 'out' => 2.19],
    ];
    $rate = $rates[$model] ?? ['in' => 0.14, 'out' => 0.28];
    return round((($promptTokens / 1_000_000) * $rate['in']) + (($completionTokens / 1_000_000) * $rate['out']), 6);
}

function ai_usage_tokens_from_meta(array $meta): array
{
    $prompt = max(0, (int)($meta['prompt_tokens'] ?? 0));
    $completion = max(0, (int)($meta['completion_tokens'] ?? 0));
    $total = max(0, (int)($meta['total_tokens'] ?? ($prompt + $completion)));
    return [$prompt, $completion, $total];
}

/**
 * @param array{
 *   provider:string,
 *   mode?:string,
 *   model?:string,
 *   ok?:bool,
 *   fallback?:bool,
 *   prompt_tokens?:int,
 *   completion_tokens?:int,
 *   total_tokens?:int,
 *   estimated_usd?:float,
 *   error?:string
 * } $entry
 */
function ai_usage_record(array $entry): void
{
    $provider = trim((string)($entry['provider'] ?? ''));
    if ($provider === '') {
        return;
    }

    $mode = ($entry['mode'] ?? '') === 'chat' ? 'chat' : 'explain';
    $model = trim((string)($entry['model'] ?? ''));
    $ok = !empty($entry['ok']);
    $fallback = !empty($entry['fallback']);
    [$promptTokens, $completionTokens, $totalTokens] = ai_usage_tokens_from_meta($entry);

    $estimatedUsd = isset($entry['estimated_usd'])
        ? (float)$entry['estimated_usd']
        : 0.0;
    if ($provider === 'shopaikey' && $estimatedUsd <= 0 && ($promptTokens > 0 || $completionTokens > 0)) {
        $estimatedUsd = ai_usage_estimate_shopaikey_usd($model, $promptTokens, $completionTokens);
    }

    ai_usage_mutate_store(function (array &$store) use ($provider, $mode, $model, $ok, $fallback, $promptTokens, $completionTokens, $totalTokens, $estimatedUsd, $entry) {
        $dayKey = ai_usage_today_key();
        if (!isset($store['by_day'][$dayKey]) || !is_array($store['by_day'][$dayKey])) {
            $store['by_day'][$dayKey] = ['providers' => [], 'by_mode' => ['explain' => 0, 'chat' => 0]];
        }
        $day = &$store['by_day'][$dayKey];
        $bucket = &ai_usage_provider_bucket($day, $provider);

        $bucket['calls']++;
        if ($ok) {
            $bucket['success']++;
            if ($fallback) {
                $bucket['fallback_success']++;
            }
        } else {
            $bucket['error']++;
        }
        $bucket['prompt_tokens'] += $promptTokens;
        $bucket['completion_tokens'] += $completionTokens;
        $bucket['total_tokens'] += $totalTokens;
        if ($estimatedUsd > 0) {
            $bucket['estimated_usd'] = round((float)$bucket['estimated_usd'] + $estimatedUsd, 6);
        }

        if (!isset($day['by_mode']) || !is_array($day['by_mode'])) {
            $day['by_mode'] = ['explain' => 0, 'chat' => 0];
        }
        if ($ok) {
            $day['by_mode'][$mode] = (int)($day['by_mode'][$mode] ?? 0) + 1;
        }

        $recentItem = [
            'ts' => (new DateTimeImmutable('now', ai_usage_timezone()))->format(DateTimeInterface::ATOM),
            'provider' => $provider,
            'mode' => $mode,
            'model' => $model,
            'ok' => $ok,
            'fallback' => $fallback,
            'prompt_tokens' => $promptTokens,
            'completion_tokens' => $completionTokens,
            'total_tokens' => $totalTokens,
            'estimated_usd' => $estimatedUsd > 0 ? $estimatedUsd : null,
            'error' => $ok ? null : trim((string)($entry['error'] ?? '')),
        ];
        array_unshift($store['recent'], $recentItem);
        $store['recent'] = array_slice($store['recent'], 0, 120);

        $dayKeys = array_keys($store['by_day']);
        rsort($dayKeys);
        $keep = array_slice($dayKeys, 0, 90);
        $store['by_day'] = array_intersect_key($store['by_day'], array_flip($keep));
    });
}

function ai_usage_extract_gemini_tokens(array $response): array
{
    $meta = $response['usageMetadata'] ?? [];
    if (!is_array($meta)) {
        return ['prompt_tokens' => 0, 'completion_tokens' => 0, 'total_tokens' => 0];
    }
    $prompt = (int)($meta['promptTokenCount'] ?? 0);
    $completion = (int)($meta['candidatesTokenCount'] ?? 0);
    $total = (int)($meta['totalTokenCount'] ?? ($prompt + $completion));
    return [
        'prompt_tokens' => $prompt,
        'completion_tokens' => $completion,
        'total_tokens' => $total,
    ];
}

function ai_usage_extract_shopaikey_tokens(array $response): array
{
    $usage = $response['usage'] ?? [];
    if (!is_array($usage)) {
        return ['prompt_tokens' => 0, 'completion_tokens' => 0, 'total_tokens' => 0];
    }
    $prompt = (int)($usage['prompt_tokens'] ?? 0);
    $completion = (int)($usage['completion_tokens'] ?? 0);
    $total = (int)($usage['total_tokens'] ?? ($prompt + $completion));
    return [
        'prompt_tokens' => $prompt,
        'completion_tokens' => $completion,
        'total_tokens' => $total,
    ];
}