/**
 * Ghi log AI từ trình duyệt → api/ai_usage_report.php (fire-and-forget).
 */
(function (global) {
    const ENDPOINT = 'api/ai_usage_report.php';

    function extractGeminiTokens(raw) {
        const meta = raw?.usageMetadata;
        if (!meta || typeof meta !== 'object') {
            return { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 };
        }
        const prompt = Number(meta.promptTokenCount) || 0;
        const completion = Number(meta.candidatesTokenCount) || 0;
        const total = Number(meta.totalTokenCount) || (prompt + completion);
        return { prompt_tokens: prompt, completion_tokens: completion, total_tokens: total };
    }

    function report(entry) {
        if (!entry || typeof entry !== 'object') return;
        const provider = String(entry.provider || '').trim();
        if (!provider) return;

        const payload = {
            provider,
            module: entry.module || 'other',
            mode: entry.mode || 'explain',
            model: entry.model || '',
            ok: !!entry.ok,
            fallback: !!entry.fallback,
            prompt_tokens: Number(entry.prompt_tokens) || 0,
            completion_tokens: Number(entry.completion_tokens) || 0,
            total_tokens: Number(entry.total_tokens) || 0,
            error: entry.ok ? '' : String(entry.error || 'Lỗi không xác định'),
        };

        try {
            fetch(ENDPOINT, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
                keepalive: true,
            }).catch(() => {});
        } catch {
            // ignore
        }
    }

    global.AiUsageReporter = {
        report,
        extractGeminiTokens,
    };
})(window);