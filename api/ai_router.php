<?php
/**
 * AI Router — miễn phí trước, ShopAIKey/DeepSeek chỉ khi thật sự cần.
 *
 * Thứ tự chính (AI Explain lộ trình):
 *   light_ai (miễn phí) → DS2API (DeepSeek web) → Cloudflare (quota neurons)
 *
 * Khi DS2API / Cloudflare không đủ:
 *   → Gemini
 *   → ShopAIKey / DeepSeek API (cuối cùng)
 *
 * Escalation chỉ khi tier trước không cho câu trả lời chấp nhận được.
 */
require_once __DIR__ . '/ai_smart_quota.php';

function ai_router_refusal_patterns(): array
{
    return [
        'không thể',
        'khong the',
        'không rõ',
        'khong ro',
        'thiếu thông tin',
        'thieu thong tin',
        'không đủ',
        'khong du',
        'xin lỗi',
        'xin loi',
        'tôi không',
        'toi khong',
    ];
}

function ai_router_text_len(string $text): int
{
    return function_exists('mb_strlen') ? mb_strlen($text, 'UTF-8') : strlen($text);
}

function ai_router_lower(string $text): string
{
    return function_exists('mb_strtolower') ? mb_strtolower($text, 'UTF-8') : strtolower($text);
}

function ai_router_question_is_hard(string $mode, string $question, string $text): bool
{
    $probe = $mode === 'chat' ? $question : $text;
    $probe = ai_router_lower(trim($probe));
    if ($probe === '') {
        return false;
    }
    if (ai_router_text_len($probe) >= 280) {
        return true;
    }
    return (bool)preg_match(
        '/chứng minh|chung minh|giải chi tiết|giai chi tiet|tại sao|tai sao|vì sao|vi sao|chứng tỏ|chung to|bài toán khó|bai toan kho/u',
        $probe
    );
}

function ai_router_quality_acceptable(array $result, string $mode, string $question, string $text): bool
{
    $answer = trim((string)($result['answer'] ?? ''));
    if ($answer === '') {
        return false;
    }

    $provider = (string)($result['provider'] ?? '');
    if ($provider === 'light_ai' && (($result['confidence'] ?? '') !== 'high')) {
        return false;
    }

    $lower = ai_router_lower($answer);
    foreach (ai_router_refusal_patterns() as $pattern) {
        if (str_contains($lower, $pattern)) {
            return false;
        }
    }

    $minLen = ai_router_question_is_hard($mode, $question, $text) ? 55 : 28;
    if (ai_router_text_len($answer) < $minLen) {
        return false;
    }

    if (!empty($result['complete'])) {
        return true;
    }

    if (function_exists('answer_looks_complete') && answer_looks_complete($answer)) {
        return true;
    }

    return ai_router_text_len($answer) >= 90;
}

function ai_router_pick_best(array $candidates): ?array
{
    $best = null;
    foreach ($candidates as $candidate) {
        if (!is_array($candidate) || empty($candidate['answer'])) {
            continue;
        }
        if ($best === null || ai_router_text_len((string)$candidate['answer']) > ai_router_text_len((string)$best['answer'])) {
            $best = $candidate;
        }
    }
    return $best;
}

/**
 * @param array $ctx config, mode, subject, lessonTitle, text, question, lessonContext, history, prompt, workerPayload, providers (callables), log callable
 */
function ai_router_run(array $ctx): array
{
    $config = $ctx['config'] ?? [];
    $mode = (string)($ctx['mode'] ?? 'explain');
    $question = (string)($ctx['question'] ?? '');
    $text = (string)($ctx['text'] ?? '');
    $prompt = (string)($ctx['prompt'] ?? '');
    $workerPayload = $ctx['workerPayload'] ?? [];
    $providers = $ctx['providers'] ?? [];
    $log = $ctx['log'] ?? null;

    $errors = [];
    $candidates = [];
    $quotaStatus = ai_smart_quota_status();
    $usedFallback = false;
    $tiersTried = [];
    $geminiTriedAsCfFallback = false;

    $tryLight = $providers['light'] ?? null;
    if (is_callable($tryLight)) {
        $light = $tryLight();
        if (is_array($light) && !empty($light['answer'])) {
            $tiersTried[] = 'light_ai';
            if (ai_router_quality_acceptable($light, $mode, $question, $text)) {
                if (is_callable($log)) {
                    $log($mode, $light, true, false);
                }
                return [
                    'result' => array_merge($light, [
                        'complete' => true,
                        'router_tier' => 'light_ai',
                        'tiers_tried' => $tiersTried,
                    ]),
                    'quota' => $quotaStatus,
                    'used_api' => false,
                ];
            }
            $candidates[] = $light;
        }
    }

    $tryDs2api = $providers['ds2api'] ?? null;
    if (is_callable($tryDs2api)) {
        $ds2 = $tryDs2api();
        if (is_array($ds2) && !empty($ds2['answer'])) {
            $tiersTried[] = 'ds2api';
            $ds2['complete'] = !empty($ds2['complete']) || (function_exists('answer_looks_complete') && answer_looks_complete((string)$ds2['answer']));
            if (ai_router_quality_acceptable($ds2, $mode, $question, $text)) {
                if (is_callable($log)) {
                    $log($mode, $ds2, true, false);
                }
                return [
                    'result' => array_merge($ds2, [
                        'router_tier' => 'ds2api',
                        'tiers_tried' => $tiersTried,
                    ]),
                    'quota' => $quotaStatus,
                    'used_api' => true,
                ];
            }
            $candidates[] = $ds2;
            $usedFallback = true;
        } elseif (is_array($ds2) && !empty($ds2['error'])) {
            $errors[] = 'DS2API: ' . $ds2['error'];
            if (is_callable($log)) {
                $log($mode, $ds2, false, false);
            }
        }
    }

    $tryCloudflare = $providers['cloudflare'] ?? null;
    $cloudflareSkippedQuota = false;
    if (is_callable($tryCloudflare) && ai_smart_quota_allows_cloudflare()) {
        $cf = $tryCloudflare();
        if (is_array($cf) && !empty($cf['answer'])) {
            $tiersTried[] = 'cloudflare';
            $cf['complete'] = !empty($cf['complete']) || (function_exists('answer_looks_complete') && answer_looks_complete((string)$cf['answer']));
            if (ai_router_quality_acceptable($cf, $mode, $question, $text)) {
                if (is_callable($log)) {
                    $log($mode, $cf, true, false);
                }
                return [
                    'result' => array_merge($cf, [
                        'router_tier' => 'cloudflare',
                        'tiers_tried' => $tiersTried,
                    ]),
                    'quota' => $quotaStatus,
                    'used_api' => true,
                    'neurons' => $ctx['estimate_neurons'] ?? null,
                ];
            }
            $candidates[] = $cf;
            $usedFallback = true;
        } elseif (is_array($cf) && !empty($cf['error'])) {
            $errors[] = 'Cloudflare: ' . $cf['error'];
            if (is_callable($log)) {
                $log($mode, $cf, false, false);
            }
            if (ai_smart_quota_is_exhaustion_error((string)$cf['error'])) {
                ai_smart_quota_force_exhausted();
                $quotaStatus = ai_smart_quota_status();
            }
        }
    } else {
        $cloudflareSkippedQuota = true;
        $quotaStatus = ai_smart_quota_status();
    }

    if ($cloudflareSkippedQuota && ai_smart_quota_should_block_all()) {
        return [
            'blocked' => true,
            'code' => 'quota_exhausted_block',
            'error' => $quotaStatus['student_notice'] ?: 'Hôm nay đã hết quota Cloudflare, vui lòng thử lại ngày mai.',
            'quota' => $quotaStatus,
        ];
    }

    // === Fallback after Cloudflare ===
    // When Cloudflare quota exhausted or low quality:
    //   1. Gemini is the primary fallback (as requested)
    //   2. ShopAIKey / DeepSeek only as last resort if Gemini fails
    $tryGemini = $providers['gemini'] ?? null;
    if (is_callable($tryGemini)) {
        $gemini = $tryGemini();
        if (is_array($gemini) && !empty($gemini['answer'])) {
            $tiersTried[] = 'gemini';
            $gemini['complete'] = !empty($gemini['complete']) || (function_exists('answer_looks_complete') && answer_looks_complete((string)$gemini['answer']));
            $gemini['fallback'] = $usedFallback || $cloudflareSkippedQuota;
            $isCfQuotaFallback = $cloudflareSkippedQuota || $usedFallback;

            // When this is fallback due to Cloudflare quota, accept Gemini answer readily
            // (only skip to DeepSeek if Gemini completely failed to produce content)
            if ($isCfQuotaFallback || ai_router_quality_acceptable($gemini, $mode, $question, $text)) {
                if (is_callable($log)) {
                    $log($mode, $gemini, true, !empty($gemini['fallback']));
                }
                return [
                    'result' => array_merge($gemini, [
                        'router_tier' => 'gemini',
                        'tiers_tried' => $tiersTried,
                    ]),
                    'quota' => $quotaStatus,
                    'used_api' => true,
                ];
            }
            $candidates[] = $gemini;
            $usedFallback = true;
            if ($isCfQuotaFallback) {
                $geminiTriedAsCfFallback = true;
            }
        } elseif (is_array($gemini) && !empty($gemini['error'])) {
            $errors[] = (string)$gemini['error'];
            if (is_callable($log)) {
                $log($mode, $gemini, false, $usedFallback);
            }
        }
    }

    // ShopAIKey (DeepSeek) — last resort only (after Gemini failed or no Gemini keys)
    $shopaikeyEnabled = !empty($config['shopaikey_enabled']) && trim((string)($config['shopaikey_api_key'] ?? '')) !== '';
    $tryShopaikey = $providers['shopaikey'] ?? null;
    if ($shopaikeyEnabled && is_callable($tryShopaikey)) {
        // Only attempt ShopAIKey if we are intentionally falling back past Gemini
        if ($cloudflareSkippedQuota || $usedFallback || $geminiTriedAsCfFallback) {
            $shop = $tryShopaikey();
            if (is_array($shop) && !empty($shop['answer'])) {
                $tiersTried[] = 'shopaikey';
                $shop['complete'] = !empty($shop['complete']) || (function_exists('answer_looks_complete') && answer_looks_complete((string)$shop['answer']));
                $shop['fallback'] = true;
                if (is_callable($log)) {
                    $log($mode, $shop, true, true);
                }
                return [
                    'result' => array_merge($shop, [
                        'router_tier' => 'shopaikey',
                        'tiers_tried' => $tiersTried,
                    ]),
                    'quota' => $quotaStatus,
                    'used_api' => true,
                ];
            }
            if (is_array($shop) && !empty($shop['error'])) {
                $errors[] = (string)$shop['error'];
                if (is_callable($log)) {
                    $log($mode, $shop, false, true);
                }
            }
        }
    }

    $best = ai_router_pick_best($candidates);
    if ($best !== null) {
        if (is_callable($log)) {
            $log($mode, $best, true, !empty($best['fallback']));
        }
        return [
            'result' => array_merge($best, [
                'router_tier' => (string)($best['provider'] ?? 'fallback'),
                'tiers_tried' => $tiersTried,
                'quality_relaxed' => true,
            ]),
            'quota' => $quotaStatus,
            'used_api' => ($best['provider'] ?? '') !== 'light_ai',
        ];
    }

    if ($cloudflareSkippedQuota && empty($config['gemini_keys']) && !$shopaikeyEnabled) {
        return [
            'blocked' => true,
            'code' => 'quota_exhausted_block',
            'error' => $quotaStatus['student_notice'] ?: 'Hôm nay đã hết quota miễn phí. Thử lại ngày mai.',
            'quota' => $quotaStatus,
        ];
    }

    return [
        'error' => $errors ? implode(' | ', $errors) : 'Không gọi được AI.',
        'quota' => $quotaStatus,
        'tiers_tried' => $tiersTried,
    ];
}