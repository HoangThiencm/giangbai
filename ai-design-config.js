/**
 * Cấu hình AI trên từng trang công cụ (không còn ở hub giáo viên).
 */
(function (global) {
    const LS = {
        gemini: 'global_gemini_keys',
        groq: 'global_groq_keys',
        hf: 'hf_tokens',
        mistral: 'global_mistral_keys',
        geminiModel: 'default_gemini_module',
        groqModel: 'default_groq_model',
        mistralModel: 'default_mistral_ocr_model',
        pdfEngine: 'pdf_scan_engine',
        hfFallback: 'hf_fallback_enabled',
        hfUrl: 'hf_fallback_url',
    };

    function parseJson(key, fallback) {
        try {
            const raw = localStorage.getItem(key);
            return raw ? JSON.parse(raw) : fallback;
        } catch {
            return fallback;
        }
    }

    function readLines(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(String(e.target.result || '').trim().split('\n').map((l) => l.trim()).filter(Boolean));
            reader.onerror = () => reject(new Error('Không đọc được file.'));
            reader.readAsText(file);
        });
    }

    function ensureModal() {
        if (document.getElementById('aiDesignConfigModal')) return;
        const wrap = document.createElement('div');
        wrap.id = 'aiDesignConfigModal';
        wrap.className = 'hidden fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm';
        wrap.innerHTML = `
            <div class="flex max-h-[92vh] w-full max-w-lg flex-col overflow-hidden rounded-2xl bg-white shadow-2xl">
                <div class="flex items-center justify-between bg-slate-800 p-4 text-white">
                    <h3 class="flex items-center gap-2 font-bold"><i class="fas fa-sliders-h"></i> Cấu hình AI</h3>
                    <button type="button" id="aiDesignConfigClose" class="text-xl transition hover:text-red-400" title="Đóng"><i class="fas fa-times"></i></button>
                </div>
                <div class="space-y-5 overflow-y-auto p-5">
                    <div>
                        <label class="mb-2 block text-sm font-bold text-slate-700">Google Gemini (API Keys)</label>
                        <div id="adcGeminiStatus" class="mb-2"></div>
                        <label class="flex cursor-pointer items-center justify-center gap-2 rounded border border-slate-300 bg-slate-100 px-4 py-2 text-sm font-medium text-slate-600 transition hover:border-indigo-300 hover:bg-indigo-50">
                            <i class="fas fa-file-upload text-indigo-500"></i> Chọn file Keys.txt
                            <input type="file" id="adcGeminiFile" class="hidden" accept=".txt,text/plain" />
                        </label>
                        <label class="mt-2 block text-sm font-bold text-slate-700">Model Gemini</label>
                        <select id="adcGeminiModel" class="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500">
                            <option value="gemini-3-flash-preview">Gemini 3 Flash (Mới nhất)</option>
                            <option value="gemini-2.5-flash">Gemini 2.5 Flash (Ổn định)</option>
                        </select>
                    </div>
                    <hr class="border-slate-200" />
                    <div>
                        <label class="mb-2 block text-sm font-bold text-slate-700">Mistral OCR (API Keys)</label>
                        <p class="mb-2 text-xs text-slate-500">Quét PDF → văn bản cực nhanh. Dùng cho tách trang + OCR trước khi nhận diện câu hỏi.</p>
                        <div id="adcMistralStatus" class="mb-2"></div>
                        <label class="flex cursor-pointer items-center justify-center gap-2 rounded border border-slate-300 bg-slate-100 px-4 py-2 text-sm font-medium text-slate-600 transition hover:border-sky-300 hover:bg-sky-50">
                            <i class="fas fa-file-upload text-sky-500"></i> Chọn file Mistral Keys.txt
                            <input type="file" id="adcMistralFile" class="hidden" accept=".txt,text/plain" />
                        </label>
                        <div class="mt-2 flex gap-2">
                            <input type="text" id="adcMistralPaste" placeholder="Hoặc dán 1 API key Mistral" class="flex-1 rounded border p-2 text-sm outline-none focus:ring-2 focus:ring-sky-500" />
                            <button type="button" id="adcMistralSave" class="rounded bg-sky-600 px-3 py-2 text-sm font-bold text-white hover:bg-sky-700">Lưu</button>
                        </div>
                        <label class="mt-2 block text-sm font-bold text-slate-700">Quét PDF</label>
                        <select id="adcPdfEngine" class="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-sky-500">
                            <option value="browser">Trình duyệt (pdf.js) — mặc định</option>
                            <option value="mistral">Mistral OCR — nhanh, ra văn bản</option>
                            <option value="server">Hosting / HuggingFace — khi không có Mistral</option>
                        </select>
                    </div>
                    <hr class="border-slate-200" />
                    <div>
                        <label class="mb-2 block text-sm font-bold text-slate-700">Groq AI (API Keys)</label>
                        <div id="adcGroqStatus" class="mb-2"></div>
                        <label class="flex cursor-pointer items-center justify-center gap-2 rounded border border-slate-300 bg-slate-100 px-4 py-2 text-sm font-medium text-slate-600 transition hover:border-orange-300 hover:bg-orange-50">
                            <i class="fas fa-file-upload text-orange-500"></i> Chọn file Groq Keys.txt
                            <input type="file" id="adcGroqFile" class="hidden" accept=".txt,text/plain" />
                        </label>
                        <label class="mt-2 block text-sm font-bold text-slate-700">Model Groq</label>
                        <select id="adcGroqModel" class="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-orange-500">
                            <option value="llama-3.3-70b-versatile">Llama 3.3 70B (Khuyên dùng)</option>
                            <option value="qwen3-32b">Qwen 3 32B</option>
                            <option value="meta-llama/llama-4-scout-17b-16e-instruct">Llama 4 Scout 17B</option>
                            <option value="llama-3.1-8b-instant">Llama 3.1 8B (Nhanh)</option>
                        </select>
                    </div>
                    <hr class="border-slate-200" />
                    <div>
                        <label class="mb-2 block text-sm font-bold text-slate-700">Hugging Face (Tokens)</label>
                        <div id="adcHfContainer"></div>
                    </div>
                    <div>
                        <label class="mb-2 block text-sm font-bold text-slate-700">Fallback hosting → HuggingFace</label>
                        <div id="adcHfFallbackContainer"></div>
                    </div>
                    <div class="flex gap-2 rounded border border-amber-100 bg-amber-50 p-3 text-xs text-amber-900">
                        <i class="fas fa-info-circle mt-0.5"></i>
                        <span>Lưu ngay trên trình duyệt (Local Storage). Bấm <strong>Xong</strong> để đóng.</span>
                    </div>
                </div>
                <div class="flex items-center justify-between gap-3 border-t border-slate-200 bg-slate-50 px-5 py-3">
                    <p class="text-xs text-slate-500">Cấu hình chỉ áp dụng trang công cụ AI</p>
                    <button type="button" id="adcDoneBtn" class="shrink-0 rounded-lg bg-indigo-600 px-5 py-2 text-sm font-bold text-white hover:bg-indigo-700">Xong</button>
                </div>
            </div>`;
        document.body.appendChild(wrap);
        wrap.addEventListener('click', (e) => { if (e.target === wrap) AiDesignConfig.closeModal(); });
        document.getElementById('aiDesignConfigClose').addEventListener('click', () => AiDesignConfig.closeModal());
        document.getElementById('adcDoneBtn').addEventListener('click', () => AiDesignConfig.closeModal());
        document.getElementById('adcGeminiFile').addEventListener('change', (e) => AiDesignConfig.handleFile(e.target.files[0], 'gemini'));
        document.getElementById('adcGroqFile').addEventListener('change', (e) => AiDesignConfig.handleFile(e.target.files[0], 'groq'));
        document.getElementById('adcMistralFile').addEventListener('change', (e) => AiDesignConfig.handleFile(e.target.files[0], 'mistral'));
        document.getElementById('adcMistralSave').addEventListener('click', () => AiDesignConfig.saveMistralKey());
        document.getElementById('adcGeminiModel').addEventListener('change', (e) => {
            localStorage.setItem(LS.geminiModel, e.target.value);
        });
        document.getElementById('adcGroqModel').addEventListener('change', (e) => {
            localStorage.setItem(LS.groqModel, e.target.value);
        });
        document.getElementById('adcPdfEngine').addEventListener('change', (e) => {
            localStorage.setItem(LS.pdfEngine, e.target.value);
        });
    }

    const AiDesignConfig = {
        getApiKeys: () => parseJson(LS.gemini, []).filter(Boolean),
        getGroqKeys: () => parseJson(LS.groq, []).filter(Boolean),
        getHFTokens: () => parseJson(LS.hf, []).filter(Boolean),
        getMistralKeys: () => parseJson(LS.mistral, []).filter(Boolean),
        getModule: () => localStorage.getItem(LS.geminiModel) || 'gemini-2.5-flash',
        getGroqModule: () => localStorage.getItem(LS.groqModel) || 'llama-3.3-70b-versatile',
        getMistralModel: () => localStorage.getItem(LS.mistralModel) || 'mistral-ocr-latest',
        getPdfEngine: () => localStorage.getItem(LS.pdfEngine) || 'browser',

        openModal() {
            ensureModal();
            AiDesignConfig.render();
            document.getElementById('aiDesignConfigModal').classList.remove('hidden');
        },

        closeModal() {
            const el = document.getElementById('aiDesignConfigModal');
            if (el) el.classList.add('hidden');
        },

        async loadHostingFallbackConfig() {
            try {
                const res = await fetch('global_config.json', { cache: 'no-store' });
                if (!res.ok) return;
                const cfg = await res.json();
                // Admin là nguồn cấu hình chung. Đồng bộ ở đây để khi mở thẳng
                // một công cụ, giáo viên không cần ghé qua trang chủ trước.
                if (Array.isArray(cfg.gemini_keys)) {
                    localStorage.setItem(LS.gemini, JSON.stringify(cfg.gemini_keys.filter(Boolean)));
                }
                if (cfg.gemini_model) localStorage.setItem(LS.geminiModel, String(cfg.gemini_model));
                if (Array.isArray(cfg.groq_keys)) {
                    localStorage.setItem(LS.groq, JSON.stringify(cfg.groq_keys.filter(Boolean)));
                }
                if (cfg.groq_model) localStorage.setItem(LS.groqModel, String(cfg.groq_model));
                if (Array.isArray(cfg.mistral_keys)) {
                    localStorage.setItem(LS.mistral, JSON.stringify(cfg.mistral_keys.filter(Boolean)));
                }
                if (cfg.mistral_ocr_model) localStorage.setItem(LS.mistralModel, String(cfg.mistral_ocr_model));
                if (cfg.hf_fallback_url) {
                    localStorage.setItem(LS.hfUrl, String(cfg.hf_fallback_url).replace(/\/$/, ''));
                }
                localStorage.setItem(LS.hfFallback, cfg.hf_fallback_enabled === false ? 'false' : 'true');
            } catch (_) { /* noop */ }
        },

        setHfFallbackEnabled(enabled, options) {
            const opts = options || {};
            if (global.GiangBaiApi) {
                GiangBaiApi.setFallbackEnabled(enabled, { silent: !!opts.silent });
            } else {
                localStorage.setItem(LS.hfFallback, enabled ? 'true' : 'false');
            }
            if (!opts.skipRender) AiDesignConfig.render();
        },

        onHfFallbackCheckbox(el) {
            const enabled = !!el.checked;
            AiDesignConfig.setHfFallbackEnabled(enabled, { silent: true, skipRender: true });
            const note = document.getElementById('adcHfFallbackNote');
            if (note) {
                note.textContent = enabled ? '✓ Đã bật fallback HF' : '✓ Đã tắt — chỉ hosting';
                note.classList.remove('hidden');
            }
        },

        async handleFile(file, type) {
            if (!file) return;
            const lines = await readLines(file);
            if (type === 'gemini') {
                const keys = lines.filter((l) => l.length > 5 && !l.startsWith('hf_') && !l.startsWith('gsk_'));
                if (!keys.length) return alert('Không tìm thấy Gemini Key hợp lệ.');
                localStorage.setItem(LS.gemini, JSON.stringify(keys));
                localStorage.setItem(LS.geminiModel, 'gemini-2.5-flash');
                alert(`Đã nạp ${keys.length} Gemini Keys.`);
            } else if (type === 'groq') {
                const keys = lines.filter((l) => l.length > 5);
                if (!keys.length) return alert('Không tìm thấy Groq Key hợp lệ.');
                localStorage.setItem(LS.groq, JSON.stringify(keys));
                localStorage.setItem(LS.groqModel, 'llama-3.3-70b-versatile');
                alert(`Đã nạp ${keys.length} Groq Keys.`);
            } else if (type === 'mistral') {
                const keys = lines.filter((l) => l.length > 8);
                if (!keys.length) return alert('Không tìm thấy Mistral Key hợp lệ.');
                localStorage.setItem(LS.mistral, JSON.stringify(keys));
                alert(`Đã nạp ${keys.length} Mistral Keys.`);
            } else if (type === 'hf') {
                const tokens = lines.filter((l) => l.startsWith('hf_'));
                if (!tokens.length) return alert("Không tìm thấy token bắt đầu bằng 'hf_'.");
                localStorage.setItem(LS.hf, JSON.stringify(tokens));
                alert(`Đã nạp ${tokens.length} HF Tokens.`);
            }
            AiDesignConfig.render();
        },

        saveHFToken() {
            const input = document.getElementById('adcHfTokenInput');
            const token = (input?.value || '').trim();
            if (!token) return alert('Vui lòng nhập Token!');
            if (!token.startsWith('hf_')) return alert("Token HF phải bắt đầu bằng 'hf_'.");
            localStorage.setItem(LS.hf, JSON.stringify([token]));
            alert('Đã lưu Token Hugging Face.');
            AiDesignConfig.render();
        },

        clearHFToken() {
            if (!confirm('Xóa tất cả Token Hugging Face?')) return;
            localStorage.removeItem(LS.hf);
            AiDesignConfig.render();
        },

        saveMistralKey() {
            const input = document.getElementById('adcMistralPaste');
            const key = (input?.value || '').trim();
            if (!key) return alert('Vui lòng nhập Mistral API key.');
            localStorage.setItem(LS.mistral, JSON.stringify([key]));
            if (input) input.value = '';
            alert('Đã lưu Mistral API key.');
            AiDesignConfig.render();
        },

        statusHtml(count, tone, label) {
            const tones = {
                green: 'border-green-200 bg-green-50 text-green-700',
                orange: 'border-orange-200 bg-orange-50 text-orange-700',
                sky: 'border-sky-200 bg-sky-50 text-sky-700',
            };
            const cls = tones[tone] || tones.green;
            if (count > 0) {
                return `<div class="flex items-center justify-between rounded border p-2.5 text-sm ${cls}">
                    <span class="font-bold"><i class="fas fa-check-circle"></i> ${label} (${count})</span>
                </div>`;
            }
            return `<div class="rounded border border-red-200 bg-red-50 p-2 text-sm italic text-red-600"><i class="fas fa-exclamation-triangle"></i> Chưa cấu hình.</div>`;
        },

        render() {
            ensureModal();
            const gemini = document.getElementById('adcGeminiStatus');
            const groq = document.getElementById('adcGroqStatus');
            const mistral = document.getElementById('adcMistralStatus');
            const hf = document.getElementById('adcHfContainer');
            const hfFb = document.getElementById('adcHfFallbackContainer');
            if (gemini) gemini.innerHTML = AiDesignConfig.statusHtml(AiDesignConfig.getApiKeys().length, 'green', 'Gemini');
            if (groq) groq.innerHTML = AiDesignConfig.statusHtml(AiDesignConfig.getGroqKeys().length, 'orange', 'Groq');
            if (mistral) mistral.innerHTML = AiDesignConfig.statusHtml(AiDesignConfig.getMistralKeys().length, 'sky', 'Mistral OCR');

            const geminiSel = document.getElementById('adcGeminiModel');
            const groqSel = document.getElementById('adcGroqModel');
            const pdfSel = document.getElementById('adcPdfEngine');
            if (geminiSel) geminiSel.value = AiDesignConfig.getModule();
            if (groqSel) groqSel.value = AiDesignConfig.getGroqModule();
            if (pdfSel) pdfSel.value = AiDesignConfig.getPdfEngine();

            if (hf) {
                const tokens = AiDesignConfig.getHFTokens();
                if (tokens.length) {
                    hf.innerHTML = `<div class="flex items-center justify-between rounded border border-purple-200 bg-purple-50 p-2.5 text-sm">
                        <span class="font-bold text-purple-700"><i class="fas fa-robot"></i> HF: ${tokens.length} token</span>
                        <button type="button" onclick="AiDesignConfig.clearHFToken()" class="text-xs text-red-500 underline">Xóa</button>
                    </div>`;
                } else {
                    hf.innerHTML = `
                        <label class="mb-2 flex cursor-pointer items-center justify-center gap-2 rounded border border-purple-300 bg-purple-50 px-3 py-2 text-sm font-medium text-purple-700">
                            <i class="fas fa-file-upload"></i> Nạp Tokens.txt
                            <input type="file" id="adcHfFile" class="hidden" accept=".txt,text/plain" />
                        </label>
                        <div class="flex gap-2">
                            <input type="text" id="adcHfTokenInput" placeholder="Hoặc dán token hf_..." class="flex-1 rounded border p-2 text-sm outline-none focus:ring-2 focus:ring-purple-500" />
                            <button type="button" onclick="AiDesignConfig.saveHFToken()" class="rounded bg-purple-600 px-3 py-2 text-sm font-bold text-white">Lưu</button>
                        </div>`;
                    const hfFile = document.getElementById('adcHfFile');
                    if (hfFile) hfFile.onchange = (e) => AiDesignConfig.handleFile(e.target.files[0], 'hf');
                }
            }

            if (hfFb) {
                const enabled = localStorage.getItem(LS.hfFallback) !== 'false';
                const url = localStorage.getItem(LS.hfUrl) || 'https://hoangthiencm-giangbai.hf.space';
                hfFb.innerHTML = `
                    <div class="rounded border border-slate-200 bg-slate-50 p-3 text-sm">
                        <label class="flex cursor-pointer items-center gap-2 font-semibold text-slate-700">
                            <input type="checkbox" ${enabled ? 'checked' : ''} onchange="AiDesignConfig.onHfFallbackCheckbox(this)" />
                            Bật fallback HuggingFace khi hosting lỗi
                        </label>
                        <p id="adcHfFallbackNote" class="hidden text-xs font-bold text-emerald-700 mt-1"></p>
                        <p class="mt-2 text-xs text-slate-500">URL: <code>${url}</code></p>
                    </div>`;
            }
        },

        mountBar(containerId, options) {
            const opts = options || {};
            const host = document.getElementById(containerId);
            if (!host) return;
            const isTeacher = localStorage.getItem('userRole') === 'teacher';
            host.className = (opts.className || 'flex flex-wrap items-center justify-end gap-2 px-3 py-2') + (host.className ? ` ${host.className}` : '');
            host.innerHTML = `
                ${isTeacher ? '' : `<button type="button" id="${containerId}-cfg-btn" class="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-bold text-slate-700 shadow-sm hover:bg-slate-50">
                    <i class="fas fa-sliders-h text-indigo-500"></i> Cấu hình AI
                </button>`}
                <span id="${containerId}-hf-slot"></span>`;
            document.getElementById(`${containerId}-cfg-btn`)?.addEventListener('click', () => AiDesignConfig.openModal());
            if (global.GiangBaiApi) {
                GiangBaiApi.mountFallbackToggle(`${containerId}-hf-slot`, { compact: true, ...(opts.hfToggle || {}) });
            }
            AiDesignConfig.loadHostingFallbackConfig().finally(() => AiDesignConfig.render());
        },
    };

    global.AiDesignConfig = AiDesignConfig;
    global.SystemConfig = Object.assign(global.SystemConfig || {}, {
        getApiKeys: AiDesignConfig.getApiKeys,
        getGroqKeys: AiDesignConfig.getGroqKeys,
        getHFTokens: AiDesignConfig.getHFTokens,
        getModule: AiDesignConfig.getModule,
        getGroqModule: AiDesignConfig.getGroqModule,
        openModal: AiDesignConfig.openModal,
    });
})(window);
