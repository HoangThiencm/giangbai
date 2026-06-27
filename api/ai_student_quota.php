<?php
/**
 * Quota AI theo học sinh / ngày — chỉ tính lượt gọi API thật (không tính cache, light_ai).
 */
require_once __DIR__ . '/ai_usage_log.php';

function ai_student_quota_file_path(): string
{
    $dir = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'data';
    if (!is_dir($dir)) {
        @mkdir($dir, 0755, true);
    }
    return $dir . DIRECTORY_SEPARATOR . 'ai_student_quota.json';
}

function ai_student_quota_load_config(): array
{
    $defaults = [
        'enabled' => true,
        'daily_limit' => 30,
        'min_interval_sec' => 2,
        'max_interval_sec' => 3,
        'teacher_unlimited' => true,
    ];

    $file = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'global_config.json';
    if (!is_file($file)) {
        return $defaults;
    }
    $global = json_decode((string)@file_get_contents($file), true);
    if (!is_array($global)) {
        return $defaults;
    }
    if (array_key_exists('ai_student_quota_enabled', $global)) {
        $defaults['enabled'] = (bool)$global['ai_student_quota_enabled'];
    }
    if (isset($global['ai_student_daily_limit'])) {
        $defaults['daily_limit'] = max(5, min(200, (int)$global['ai_student_daily_limit']));
    }
    if (array_key_exists('ai_student_teacher_unlimited', $global)) {
        $defaults['teacher_unlimited'] = (bool)$global['ai_student_teacher_unlimited'];
    }
    if (isset($global['ai_student_min_interval_sec'])) {
        $defaults['min_interval_sec'] = max(0, min(30, (int)$global['ai_student_min_interval_sec']));
    }
    if (isset($global['ai_student_max_interval_sec'])) {
        $defaults['max_interval_sec'] = max(0, min(60, (int)$global['ai_student_max_interval_sec']));
    }
    if ($defaults['max_interval_sec'] < $defaults['min_interval_sec']) {
        $defaults['max_interval_sec'] = $defaults['min_interval_sec'];
    }
    return $defaults;
}

function ai_student_quota_should_enforce(?int $userId, string $role, array $cfg): bool
{
    if (!$cfg['enabled'] || $userId === null || $userId <= 0) {
        return false;
    }
    if ($cfg['teacher_unlimited'] && in_array($role, ['teacher', 'admin'], true)) {
        return false;
    }
    return true;
}

function ai_student_rate_limit_wait_sec(array $cfg): int
{
    $minSec = (int)($cfg['min_interval_sec'] ?? 0);
    $maxSec = (int)($cfg['max_interval_sec'] ?? $minSec);
    if ($minSec <= 0) {
        return 0;
    }
    if ($maxSec < $minSec) {
        $maxSec = $minSec;
    }
    return $minSec === $maxSec ? $minSec : random_int($minSec, $maxSec);
}

function ai_student_rate_limit_require(?int $userId, string $role): void
{
    $cfg = ai_student_quota_load_config();
    if (!ai_student_quota_should_enforce($userId, $role, $cfg)) {
        return;
    }

    $requiredWait = ai_student_rate_limit_wait_sec($cfg);
    if ($requiredWait <= 0) {
        return;
    }

    $lastAt = 0.0;
    ai_student_quota_mutate(function (array &$store) use ($userId, &$lastAt) {
        if (!isset($store['last_request_at']) || !is_array($store['last_request_at'])) {
            $store['last_request_at'] = [];
        }
        $lastAt = (float)($store['last_request_at'][$userId] ?? 0);
    });

    if ($lastAt <= 0) {
        return;
    }

    $elapsed = microtime(true) - $lastAt;
    if ($elapsed >= $requiredWait) {
        return;
    }

    $retryAfter = max(1, (int)ceil($requiredWait - $elapsed));
    respond([
        'error' => "Em hỏi hơi nhanh — chờ {$retryAfter} giây rồi thử lại nhé.",
        'code' => 'student_rate_limited',
        'retry_after_sec' => $retryAfter,
        'student_quota' => ai_student_quota_status($userId, $role),
    ], 429);
}

function ai_student_rate_limit_touch(?int $userId, string $role): void
{
    $cfg = ai_student_quota_load_config();
    if (!ai_student_quota_should_enforce($userId, $role, $cfg)) {
        return;
    }
    if (ai_student_rate_limit_wait_sec($cfg) <= 0) {
        return;
    }

    ai_student_quota_mutate(function (array &$store) use ($userId) {
        if (!isset($store['last_request_at']) || !is_array($store['last_request_at'])) {
            $store['last_request_at'] = [];
        }
        $store['last_request_at'][$userId] = microtime(true);
        if (count($store['last_request_at']) > 5000) {
            arsort($store['last_request_at']);
            $store['last_request_at'] = array_slice($store['last_request_at'], 0, 3000, true);
        }
    });
}

function ai_student_quota_default_store(): array
{
    return [
        'version' => 1,
        'by_day' => [],
    ];
}

function ai_student_quota_mutate(callable $mutator): bool
{
    $path = ai_student_quota_file_path();
    $fp = @fopen($path, 'c+');
    if (!$fp) {
        return false;
    }
    if (!flock($fp, LOCK_EX)) {
        fclose($fp);
        return false;
    }
    rewind($fp);
    $raw = stream_get_contents($fp);
    $store = is_string($raw) && $raw !== '' ? (json_decode($raw, true) ?: []) : ai_student_quota_default_store();
    if (!is_array($store['by_day'] ?? null)) {
        $store['by_day'] = [];
    }
    $mutator($store);
    $json = json_encode($store, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    if ($json === false) {
        flock($fp, LOCK_UN);
        fclose($fp);
        return false;
    }
    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, $json);
    fflush($fp);
    flock($fp, LOCK_UN);
    fclose($fp);
    return true;
}

function ai_student_quota_status(?int $userId, string $role): array
{
    $cfg = ai_student_quota_load_config();
    $limit = (int)$cfg['daily_limit'];
    $day = ai_usage_today_key();

    if (!$cfg['enabled'] || $userId === null || $userId <= 0) {
        return [
            'enabled' => false,
            'allowed' => true,
            'used' => 0,
            'limit' => $limit,
            'remaining' => $limit,
            'day' => $day,
            'role' => $role,
        ];
    }

    if ($cfg['teacher_unlimited'] && in_array($role, ['teacher', 'admin'], true)) {
        return [
            'enabled' => true,
            'allowed' => true,
            'used' => 0,
            'limit' => 0,
            'remaining' => -1,
            'unlimited' => true,
            'day' => $day,
            'role' => $role,
        ];
    }

    $used = 0;
    ai_student_quota_mutate(function (array &$store) use ($day, $userId, &$used) {
        $bucket = $store['by_day'][$day]['users'][$userId] ?? 0;
        $used = (int)$bucket;
    });

    $remaining = max(0, $limit - $used);
    return [
        'enabled' => true,
        'allowed' => $used < $limit,
        'used' => $used,
        'limit' => $limit,
        'remaining' => $remaining,
        'day' => $day,
        'role' => $role,
        'notice' => $used >= $limit
            ? "Hôm nay em đã dùng hết {$limit} lượt hỏi AI. Mai hỏi tiếp hoặc ôn lại phần đã giải thích nhé."
            : '',
    ];
}

function ai_student_quota_consume(?int $userId, string $role): void
{
    $cfg = ai_student_quota_load_config();
    if (!$cfg['enabled'] || $userId === null || $userId <= 0) {
        return;
    }
    if ($cfg['teacher_unlimited'] && in_array($role, ['teacher', 'admin'], true)) {
        return;
    }

    $day = ai_usage_today_key();
    ai_student_quota_mutate(function (array &$store) use ($day, $userId) {
        if (!isset($store['by_day'][$day])) {
            $store['by_day'][$day] = ['users' => []];
        }
        if (!isset($store['by_day'][$day]['users'])) {
            $store['by_day'][$day]['users'] = [];
        }
        $store['by_day'][$day]['users'][$userId] = (int)($store['by_day'][$day]['users'][$userId] ?? 0) + 1;
        if (count($store['by_day']) > 45) {
            ksort($store['by_day']);
            $store['by_day'] = array_slice($store['by_day'], -30, null, true);
        }
    });
}

function ai_student_quota_require(?int $userId, string $role): void
{
    $status = ai_student_quota_status($userId, $role);
    if (!empty($status['allowed'])) {
        return;
    }
    respond([
        'error' => $status['notice'] ?: 'Hôm nay đã hết lượt hỏi AI.',
        'code' => 'student_quota_exhausted',
        'student_quota' => $status,
    ], 429);
}