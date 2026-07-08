<?php
/**
 * Smart Quota — cân bằng Cloudflare Neurons / fallback Gemini / ShopAIKey.
 */
require_once __DIR__ . '/ai_usage_log.php';

function ai_smart_quota_load_config(): array
{
    $defaults = [
        'enabled' => true,
        'daily_limit' => 10000,
        'warn_remaining_pct' => 20,
        'critical_remaining_pct' => 10,
        'exhausted_mode' => 'fallback',
        'avg_neurons_per_call' => 750,
    ];

    $file = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'global_config.json';
    if (!is_file($file)) {
        return $defaults;
    }
    $global = json_decode((string)@file_get_contents($file), true);
    if (!is_array($global)) {
        return $defaults;
    }

    if (array_key_exists('smart_quota_enabled', $global)) {
        $defaults['enabled'] = (bool)$global['smart_quota_enabled'];
    }
    if (!empty($global['cloudflare_neurons_daily_limit'])) {
        $defaults['daily_limit'] = max(100, (int)$global['cloudflare_neurons_daily_limit']);
    }
    if (isset($global['smart_quota_warn_pct'])) {
        $defaults['warn_remaining_pct'] = max(1, min(99, (int)$global['smart_quota_warn_pct']));
    }
    if (isset($global['smart_quota_critical_pct'])) {
        $defaults['critical_remaining_pct'] = max(0, min(99, (int)$global['smart_quota_critical_pct']));
    }
    if (!empty($global['smart_quota_exhausted_mode']) && in_array($global['smart_quota_exhausted_mode'], ['fallback', 'block'], true)) {
        $defaults['exhausted_mode'] = $global['smart_quota_exhausted_mode'];
    }
    if (!empty($global['smart_quota_avg_neurons'])) {
        $defaults['avg_neurons_per_call'] = max(50, (int)$global['smart_quota_avg_neurons']);
    }

    if ($defaults['critical_remaining_pct'] > $defaults['warn_remaining_pct']) {
        $defaults['critical_remaining_pct'] = max(0, $defaults['warn_remaining_pct'] - 5);
    }

    return $defaults;
}

function ai_smart_quota_neuron_rates(string $model): array
{
    $model = strtolower(trim($model));
    $map = [
        '@cf/qwen/qwen3-30b-a3b-fp8' => ['in' => 4625, 'out' => 30475],
        '@cf/meta/llama-3.2-3b-instruct' => ['in' => 4625, 'out' => 30475],
        '@cf/meta/llama-3.1-8b-instruct-fp8-fast' => ['in' => 4119, 'out' => 34868],
        '@cf/mistral/mistral-7b-instruct-v0.1' => ['in' => 10000, 'out' => 17300],
    ];
    return $map[$model] ?? ['in' => 5000, 'out' => 25000];
}

function ai_smart_quota_estimate_neurons(string $model, int $promptTokens, int $completionTokens, int $fallbackAvg = 750): int
{
    $rates = ai_smart_quota_neuron_rates($model);
    if ($promptTokens <= 0 && $completionTokens <= 0) {
        return max(50, $fallbackAvg);
    }
    $neurons = (($promptTokens / 1_000_000) * $rates['in']) + (($completionTokens / 1_000_000) * $rates['out']);
    return max(50, (int)ceil($neurons));
}

function ai_smart_quota_get_day_neurons(): int
{
    $store = ai_usage_load_store();
    $day = $store['by_day'][ai_usage_today_key()] ?? null;
    if (!is_array($day)) {
        return 0;
    }
    return max(0, (int)($day['cloudflare_neurons'] ?? 0));
}

function ai_smart_quota_add_neurons(int $neurons): void
{
    if ($neurons <= 0) {
        return;
    }
    ai_usage_mutate_store(function (array &$store) use ($neurons) {
        $dayKey = ai_usage_today_key();
        if (!isset($store['by_day'][$dayKey]) || !is_array($store['by_day'][$dayKey])) {
            $store['by_day'][$dayKey] = ['providers' => [], 'by_mode' => [], 'by_module' => []];
        }
        $current = max(0, (int)($store['by_day'][$dayKey]['cloudflare_neurons'] ?? 0));
        $store['by_day'][$dayKey]['cloudflare_neurons'] = $current + $neurons;
    });
}

function ai_smart_quota_force_exhausted(): void
{
    $cfg = ai_smart_quota_load_config();
    ai_usage_mutate_store(function (array &$store) use ($cfg) {
        $dayKey = ai_usage_today_key();
        if (!isset($store['by_day'][$dayKey]) || !is_array($store['by_day'][$dayKey])) {
            $store['by_day'][$dayKey] = ['providers' => [], 'by_mode' => [], 'by_module' => []];
        }
        $store['by_day'][$dayKey]['cloudflare_neurons'] = (int)$cfg['daily_limit'];
        $store['by_day'][$dayKey]['cloudflare_quota_forced'] = true;
    });
}

function ai_smart_quota_is_exhaustion_error(string $message): bool
{
    $text = strtolower($message);
    return str_contains($text, 'neuron')
        || str_contains($text, 'quota')
        || str_contains($text, 'limit exceeded')
        || str_contains($text, 'rate limit')
        || str_contains($text, 'exceeded');
}

function ai_smart_quota_status(?array $cfg = null): array
{
    $cfg = $cfg ?? ai_smart_quota_load_config();
    $limit = (int)$cfg['daily_limit'];
    $used = ai_smart_quota_get_day_neurons();
    $remaining = max(0, $limit - $used);
    $remainingPct = $limit > 0 ? round(($remaining / $limit) * 100, 1) : 0.0;
    $usedPct = $limit > 0 ? round(($used / $limit) * 100, 1) : 0.0;

    if (!$cfg['enabled']) {
        return [
            'enabled' => false,
            'level' => 'disabled',
            'allow_cloudflare' => true,
            'exhausted_mode' => $cfg['exhausted_mode'],
            'daily_limit' => $limit,
            'neurons_used' => $used,
            'neurons_remaining' => $remaining,
            'remaining_pct' => 100.0,
            'used_pct' => $usedPct,
            'message' => 'Smart Quota đang tắt — không theo dõi quota Cloudflare.',
            'teacher_notice' => '',
            'student_notice' => '',
            'resets_at_utc' => '00:00 UTC',
        ];
    }

    $level = 'normal';
    $teacherNotice = '';
    $studentNotice = '';
    $allowCloudflare = true;

    if ($remaining <= 0) {
        $level = 'exhausted';
        $allowCloudflare = false;
        $teacherNotice = 'Hôm nay đã hết quota Cloudflare (0 Neurons). '
            . ($cfg['exhausted_mode'] === 'block'
                ? 'AI lộ trình tạm tắt — thử lại sau 00:00 UTC hoặc bật fallback Gemini trong cấu hình.'
                : 'Hệ thống chuyển sang Gemini trước, DeepSeek (ShopAIKey) chỉ khi Gemini không được.');
        $studentNotice = $cfg['exhausted_mode'] === 'block'
            ? 'Hôm nay đã hết quota Cloudflare, vui lòng thử lại ngày mai hoặc hỏi giáo viên.'
            : 'Cloudflare hết quota — đang chuyển sang Gemini (sau đó DeepSeek nếu cần).';
    } elseif ($remainingPct <= (float)$cfg['critical_remaining_pct']) {
        $level = 'critical';
        $teacherNotice = "Cloudflare còn ~{$remainingPct}% quota ({$remaining}/{$limit} Neurons). Sắp chuyển fallback.";
    } elseif ($remainingPct <= (float)$cfg['warn_remaining_pct']) {
        $level = 'warn';
        $teacherNotice = "Cloudflare còn ~{$remainingPct}% quota hôm nay ({$remaining}/{$limit} Neurons).";
    }

    return [
        'enabled' => true,
        'level' => $level,
        'allow_cloudflare' => $allowCloudflare,
        'exhausted_mode' => $cfg['exhausted_mode'],
        'daily_limit' => $limit,
        'neurons_used' => $used,
        'neurons_remaining' => $remaining,
        'remaining_pct' => $remainingPct,
        'used_pct' => $usedPct,
        'warn_remaining_pct' => (int)$cfg['warn_remaining_pct'],
        'critical_remaining_pct' => (int)$cfg['critical_remaining_pct'],
        'message' => $teacherNotice !== '' ? $teacherNotice : 'Quota Cloudflare ổn định.',
        'teacher_notice' => $teacherNotice,
        'student_notice' => $studentNotice,
        'resets_at_utc' => '00:00 UTC',
    ];
}

function ai_smart_quota_allows_cloudflare(): bool
{
    return ai_smart_quota_status()['allow_cloudflare'];
}

function ai_smart_quota_should_block_all(): bool
{
    $status = ai_smart_quota_status();
    return $status['enabled']
        && $status['level'] === 'exhausted'
        && $status['exhausted_mode'] === 'block';
}
