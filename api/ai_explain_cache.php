<?php
/**
 * Cache câu trả lời AI lộ trình — cùng bài + cùng nội dung hỏi thì dùng lại.
 */
require_once __DIR__ . '/ai_usage_log.php';

const AI_EXPLAIN_CACHE_VERSION = 'v3';

function ai_explain_cache_file_path(): string
{
    $dir = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'data';
    if (!is_dir($dir)) {
        @mkdir($dir, 0755, true);
    }
    return $dir . DIRECTORY_SEPARATOR . 'ai_explain_cache.json';
}

function ai_explain_cache_default_store(): array
{
    return [
        'version' => 1,
        'updated_at' => null,
        'total_hits' => 0,
        'entries' => [],
        'order' => [],
    ];
}

function ai_explain_cache_load_config(): array
{
    $defaults = [
        'enabled' => true,
        'max_entries' => 3000,
        'ttl_days' => 90,
    ];

    $file = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'global_config.json';
    if (!is_file($file)) {
        return $defaults;
    }
    $global = json_decode((string)@file_get_contents($file), true);
    if (!is_array($global)) {
        return $defaults;
    }
    if (array_key_exists('ai_explain_cache_enabled', $global)) {
        $defaults['enabled'] = (bool)$global['ai_explain_cache_enabled'];
    }
    if (!empty($global['ai_explain_cache_max_entries'])) {
        $defaults['max_entries'] = max(100, min(20000, (int)$global['ai_explain_cache_max_entries']));
    }
    if (!empty($global['ai_explain_cache_ttl_days'])) {
        $defaults['ttl_days'] = max(1, min(365, (int)$global['ai_explain_cache_ttl_days']));
    }
    return $defaults;
}

function ai_explain_cache_normalize(string $text): string
{
    $text = preg_replace('/\[\[?AI\]\]?/u', '', $text) ?? $text;
    $text = preg_replace('/\s+/u', ' ', trim($text)) ?? trim($text);
    return trim($text);
}

function ai_explain_cache_history_fingerprint(array $history): string
{
    $parts = [];
    foreach (array_slice($history, -8) as $turn) {
        if (!is_array($turn)) {
            continue;
        }
        $role = ($turn['role'] ?? '') === 'assistant' ? 'a' : 'u';
        $content = ai_explain_cache_normalize((string)($turn['content'] ?? ''));
        if ($content === '') {
            continue;
        }
        $parts[] = $role . ':' . $content;
    }
    return implode('|', $parts);
}

function ai_explain_cache_make_key(
    string $mode,
    int $lessonId,
    string $subject,
    string $lessonTitle,
    string $text,
    string $question,
    string $lessonContext,
    array $history
): string {
    $mode = $mode === 'chat' ? 'chat' : 'explain';
    $subject = ai_explain_cache_normalize($subject);
    $lessonTitle = ai_explain_cache_normalize($lessonTitle);
    $lessonKey = $lessonId > 0 ? (string)$lessonId : ai_explain_cache_normalize($lessonTitle);

    if ($mode === 'chat') {
        $question = ai_explain_cache_normalize($question);
        $contextHash = substr(hash('sha256', ai_explain_cache_normalize($lessonContext)), 0, 16);
        $historyHash = substr(hash('sha256', ai_explain_cache_history_fingerprint($history)), 0, 16);
        $payload = implode("\n", [
            AI_EXPLAIN_CACHE_VERSION,
            $mode,
            $lessonKey,
            $subject,
            $question,
            $contextHash,
            $historyHash,
        ]);
    } else {
        $text = ai_explain_cache_normalize($text);
        $payload = implode("\n", [
            AI_EXPLAIN_CACHE_VERSION,
            $mode,
            $lessonKey,
            $subject,
            $text,
        ]);
    }

    return hash('sha256', $payload);
}

function ai_explain_cache_mutate(callable $mutator): bool
{
    $path = ai_explain_cache_file_path();
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
        $store = ai_explain_cache_default_store();
        if (is_string($raw) && trim($raw) !== '') {
            $decoded = json_decode($raw, true);
            if (is_array($decoded)) {
                $store = array_merge($store, $decoded);
                if (!is_array($store['entries'] ?? null)) {
                    $store['entries'] = [];
                }
                if (!is_array($store['order'] ?? null)) {
                    $store['order'] = [];
                }
            }
        }

        $mutator($store, ai_explain_cache_load_config());

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

function ai_explain_cache_is_expired(array $entry, int $ttlDays): bool
{
    $createdAt = trim((string)($entry['created_at'] ?? ''));
    if ($createdAt === '') {
        return true;
    }
    try {
        $created = new DateTimeImmutable($createdAt, ai_usage_timezone());
    } catch (Throwable $e) {
        return true;
    }
    $expires = $created->modify('+' . max(1, $ttlDays) . ' days');
    return $expires < new DateTimeImmutable('now', ai_usage_timezone());
}

function ai_explain_cache_touch_order(array &$order, string $key): void
{
    $order = array_values(array_filter($order, static fn($item) => $item !== $key));
    $order[] = $key;
}

function ai_explain_cache_prune(array &$store, array $cfg): void
{
    $maxEntries = max(100, (int)($cfg['max_entries'] ?? 3000));
    $ttlDays = max(1, (int)($cfg['ttl_days'] ?? 90));
    $entries = is_array($store['entries'] ?? null) ? $store['entries'] : [];
    $order = is_array($store['order'] ?? null) ? $store['order'] : [];

    foreach (array_keys($entries) as $key) {
        if (!is_array($entries[$key]) || ai_explain_cache_is_expired($entries[$key], $ttlDays)) {
            unset($entries[$key]);
            $order = array_values(array_filter($order, static fn($item) => $item !== $key));
        }
    }

    while (count($order) > $maxEntries) {
        $oldest = array_shift($order);
        if ($oldest !== null) {
            unset($entries[$oldest]);
        }
    }

    $store['entries'] = $entries;
    $store['order'] = $order;
}

/**
 * @return array{answer:string,complete:bool,provider:string,model:string,cached:bool,hits:int}|null
 */
function ai_explain_cache_get(string $cacheKey): ?array
{
    $cfg = ai_explain_cache_load_config();
    if (empty($cfg['enabled'])) {
        return null;
    }

    $found = null;
    ai_explain_cache_mutate(function (array &$store, array $config) use ($cacheKey, &$found) {
        ai_explain_cache_prune($store, $config);
        $entry = $store['entries'][$cacheKey] ?? null;
        if (!is_array($entry)) {
            return;
        }
        $answer = trim((string)($entry['answer'] ?? ''));
        if ($answer === '') {
            unset($store['entries'][$cacheKey]);
            $store['order'] = array_values(array_filter(
                $store['order'] ?? [],
                static fn($item) => $item !== $cacheKey
            ));
            return;
        }

        $now = (new DateTimeImmutable('now', ai_usage_timezone()))->format(DateTimeInterface::ATOM);
        $entry['hits'] = (int)($entry['hits'] ?? 0) + 1;
        $entry['last_hit_at'] = $now;
        $store['entries'][$cacheKey] = $entry;
        $store['total_hits'] = (int)($store['total_hits'] ?? 0) + 1;
        ai_explain_cache_touch_order($store['order'], $cacheKey);

        $found = [
            'answer' => $answer,
            'complete' => !empty($entry['complete']),
            'provider' => (string)($entry['provider'] ?? 'cache'),
            'model' => (string)($entry['model'] ?? ''),
            'cached' => true,
            'hits' => (int)$entry['hits'],
        ];
    });

    return $found;
}

function ai_explain_cache_put(string $cacheKey, array $payload): void
{
    $cfg = ai_explain_cache_load_config();
    if (empty($cfg['enabled'])) {
        return;
    }

    $answer = trim((string)($payload['answer'] ?? ''));
    if ($answer === '' || empty($payload['complete'])) {
        return;
    }

    ai_explain_cache_mutate(function (array &$store, array $config) use ($cacheKey, $payload) {
        ai_explain_cache_prune($store, $config);
        $now = (new DateTimeImmutable('now', ai_usage_timezone()))->format(DateTimeInterface::ATOM);
        $existing = is_array($store['entries'][$cacheKey] ?? null) ? $store['entries'][$cacheKey] : [];

        $store['entries'][$cacheKey] = [
            'answer' => trim((string)$payload['answer']),
            'complete' => !empty($payload['complete']),
            'provider' => (string)($payload['provider'] ?? ''),
            'model' => (string)($payload['model'] ?? ''),
            'mode' => (string)($payload['mode'] ?? 'explain'),
            'subject' => (string)($payload['subject'] ?? ''),
            'lesson_title' => (string)($payload['lesson_title'] ?? ''),
            'created_at' => (string)($existing['created_at'] ?? $now),
            'updated_at' => $now,
            'last_hit_at' => (string)($existing['last_hit_at'] ?? $now),
            'hits' => (int)($existing['hits'] ?? 0),
        ];
        ai_explain_cache_touch_order($store['order'], $cacheKey);
    });
}

function ai_explain_cache_stats(): array
{
    $cfg = ai_explain_cache_load_config();
    $path = ai_explain_cache_file_path();
    if (!is_file($path)) {
        return [
            'enabled' => !empty($cfg['enabled']),
            'entries' => 0,
            'total_hits' => 0,
            'max_entries' => (int)$cfg['max_entries'],
            'ttl_days' => (int)$cfg['ttl_days'],
        ];
    }
    $raw = @file_get_contents($path);
    $store = is_string($raw) ? json_decode($raw, true) : null;
    if (!is_array($store)) {
        return [
            'enabled' => !empty($cfg['enabled']),
            'entries' => 0,
            'total_hits' => 0,
            'max_entries' => (int)$cfg['max_entries'],
            'ttl_days' => (int)$cfg['ttl_days'],
        ];
    }
    return [
        'enabled' => !empty($cfg['enabled']),
        'entries' => count(is_array($store['entries'] ?? null) ? $store['entries'] : []),
        'total_hits' => (int)($store['total_hits'] ?? 0),
        'max_entries' => (int)$cfg['max_entries'],
        'ttl_days' => (int)$cfg['ttl_days'],
        'updated_at' => (string)($store['updated_at'] ?? ''),
    ];
}
