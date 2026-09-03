/**
 * Cài đặt AI & API Key cá nhân trên trang chủ giáo viên.
 * Lưu key lên CSDL (api/user_gemini_keys.php) và đồng bộ localStorage cho toàn hệ thống.
 */
(function (global) {
    const GEMINI_MODELS = [
        { id: 'gemini-3.7-flash', label: 'Gemini 3.7 Flash (Mặc định)' },
        { id: 'gemini-3.6-flash', label: 'Gemini 3.6 Flash' },
        { id: 'gemini-3.5-flash', label: 'Gemini 3.5 Flash' },
        { id: 'gemini-3.5-flash-lite', label: 'Gemini 3.5 Flash Lite' },
        { id: 'gemini-2.5-flash', label: 'Gemini 2.5 Flash' },
        { id: 'gemini-2.5-flash-lite', label: 'Gemini 2.5 Flash Lite' },
        { id: 'gemini-2.5-pro', label: 'Gemini 2.5 Pro' },
        { id: 'gemini-3-flash-preview', label: 'Gemini 3 Flash Preview' },
    ];

    function isStudent() {
        return String(localStorage.getItem('userRole') || '') === 'student';
    }

    function accountKey() {
        return String(localStorage.getItem('userEmail') || 'default').trim().toLowerCase();
    }

    function parseKeys(text) {
        return Array.from(new Set(String(text || '')
            .split(/[\r\n,;]+/)
            .map((k) => k.trim())
            .filter((k) => k.length > 10)));
    }

    function currentModel() {
        return localStorage.getItem('khbd_gemini_model')
            || localStorage.getItem('default_gemini_module')
            || 'gemini-2.5-flash';
    }

    function persistModel(modelId) {
        const value = String(modelId || '').trim() || 'gemini-2.5-flash';
        localStorage.setItem('default_gemini_module', value);
        localStorage.setItem('khbd_gemini_model', value);
        return value;
    }

    function persistLocalKeys(geminiKeys, mistralKeys, options) {
        const gemini = Array.isArray(geminiKeys) ? geminiKeys.filter(Boolean) : [];
        const mistral = Array.isArray(mistralKeys) ? mistralKeys.filter(Boolean) : [];
        const wipeEmpty = !!(options && options.wipeEmpty);
        const owner = accountKey();
        if (gemini.length > 0) {
            localStorage.setItem('global_gemini_keys', JSON.stringify(gemini));
            localStorage.setItem('khbd_user_gemini_keys_' + owner, JSON.stringify(gemini));
        } else if (wipeEmpty) {
            localStorage.removeItem('global_gemini_keys');
            localStorage.removeItem('khbd_user_gemini_keys_' + owner);
        }
        if (mistral.length > 0) {
            localStorage.setItem('global_mistral_keys', JSON.stringify(mistral));
            localStorage.setItem('khbd_user_mistral_keys_' + owner, JSON.stringify(mistral));
        } else if (wipeEmpty) {
            localStorage.removeItem('global_mistral_keys');
            localStorage.removeItem('khbd_user_mistral_keys_' + owner);
        }
    }

    function showToast(message, type) {
        let host = document.getElementById('userAiSettingsToast');
        if (!host) {
            host = document.createElement('div');
            host.id = 'userAiSettingsToast';
            host.className = 'pointer-events-none fixed bottom-5 right-5 z-[10000] flex max-w-sm flex-col gap-2';
            document.body.appendChild(host);
        }
        const el = document.createElement('div');
        const tone = type === 'success'
            ? 'border-emerald-200 bg-emerald-50 text-emerald-800'
            : type === 'warning'
                ? 'border-amber-200 bg-amber-50 text-amber-800'
                : 'border-rose-200 bg-rose-50 text-rose-800';
        el.className = 'pointer-events-auto rounded-xl border px-4 py-3 text-sm font-semibold shadow-lg ' + tone;
        el.textContent = message;
        host.appendChild(el);
        setTimeout(() => el.remove(), 4200);
    }

    function formatTime(value) {
        if (!value) return 'Chưa lưu';
        const date = new Date(value);
        if (Number.isNaN(date.getTime())) return String(value);
        return date.toLocaleString('vi-VN');
    }

    function setStatus(text, tone) {
        const el = document.getElementById('userAiSettingsStatus');
        if (!el) return;
        el.textContent = text || '';
        el.className = 'min-h-[1.25rem] text-sm font-semibold ' + (
            tone === 'success' ? 'text-emerald-700'
                : tone === 'warning' ? 'text-amber-700'
                    : tone === 'error' ? 'text-rose-600'
                        : 'text-slate-500'
        );
    }

    function setLoginHint(show) {
        const el = document.getElementById('userAiLoginHint');
        if (el) el.classList.toggle('hidden', !show);
    }

    async function api(method, body) {
        const opts = {
            method,
            credentials: 'include',
            cache: 'no-store',
            headers: {},
        };
        if (body !== undefined) {
            opts.headers['Content-Type'] = 'application/json';
            opts.body = JSON.stringify(body);
        }
        const res = await fetch('api/user_gemini_keys.php', opts);
        const data = await res.json().catch(() => ({}));
        return { res, data };
    }

    function modelOptionsHtml(selected) {
        const ids = GEMINI_MODELS.map((m) => m.id);
        const extra = selected && !ids.includes(selected)
            ? `<option value="${selected}">${selected}</option>`
            : '';
        return extra + GEMINI_MODELS.map((m) => (
            `<option value="${m.id}"${m.id === selected ? ' selected' : ''}>${m.label}</option>`
        )).join('');
    }

    function ensureModal() {
        if (document.getElementById('userAiSettingsModal')) return;
        const wrap = document.createElement('div');
        wrap.id = 'userAiSettingsModal';
        wrap.className = 'hidden fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 p-3 backdrop-blur-sm sm:p-4';
        wrap.innerHTML = `
            <div class="flex max-h-[94vh] w-full max-w-2xl flex-col overflow-hidden rounded-2xl bg-white shadow-2xl">
                <div class="flex items-center justify-between bg-slate-800 px-5 py-4 text-white">
                    <div>
                        <h3 class="flex items-center gap-2 text-base font-bold sm:text-lg">
                            <i class="fas fa-sliders-h text-indigo-300"></i> Cài đặt AI &amp; Key
                        </h3>
                        <p class="mt-1 text-xs font-medium text-slate-300">Key lưu theo tài khoản trên CSDL, đồng bộ mọi công cụ.</p>
                    </div>
                    <button type="button" id="userAiSettingsClose" class="text-xl transition hover:text-red-400" title="Đóng">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="space-y-5 overflow-y-auto px-5 py-5">
                    <div id="userAiLoginHint" class="hidden rounded-xl border border-amber-200 bg-amber-50 px-3 py-2 text-sm font-semibold text-amber-800">
                        Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại để lưu key lên CSDL.
                    </div>
                    <div>
                        <label for="userAiGeminiModel" class="mb-1.5 block text-sm font-bold text-slate-700">Module Gemini mặc định</label>
                        <select id="userAiGeminiModel" class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500">
                            ${modelOptionsHtml(currentModel())}
                        </select>
                        <p class="mt-1 text-xs text-slate-500">Lưu vào <code>default_gemini_module</code> và <code>khbd_gemini_model</code>.</p>
                    </div>
                    <div>
                        <div class="mb-1.5 flex flex-wrap items-center justify-between gap-2">
                            <label for="userAiGeminiKeys" class="text-sm font-bold text-slate-700">Gemini API Keys</label>
                            <label class="inline-flex cursor-pointer items-center gap-2 rounded-lg border border-slate-300 bg-slate-50 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:border-indigo-300 hover:bg-indigo-50">
                                <i class="fas fa-file-upload text-indigo-500"></i> Nạp file .txt
                                <input type="file" id="userAiGeminiFile" class="hidden" accept=".txt,text/plain" />
                            </label>
                        </div>
                        <textarea id="userAiGeminiKeys" rows="5" class="w-full rounded-lg border border-slate-300 px-3 py-2 font-mono text-xs outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Mỗi dòng một API key Gemini"></textarea>
                    </div>
                    <div>
                        <div class="mb-1.5 flex flex-wrap items-center justify-between gap-2">
                            <label for="userAiMistralKeys" class="text-sm font-bold text-slate-700">Mistral API Keys (OCR / đọc SGK)</label>
                            <label class="inline-flex cursor-pointer items-center gap-2 rounded-lg border border-slate-300 bg-slate-50 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:border-violet-300 hover:bg-violet-50">
                                <i class="fas fa-file-upload text-violet-500"></i> Nạp file .txt
                                <input type="file" id="userAiMistralFile" class="hidden" accept=".txt,text/plain" />
                            </label>
                        </div>
                        <textarea id="userAiMistralKeys" rows="3" class="w-full rounded-lg border border-slate-300 px-3 py-2 font-mono text-xs outline-none focus:ring-2 focus:ring-violet-500" placeholder="Mỗi dòng một API key Mistral"></textarea>
                    </div>
                    <div id="userAiMeta" class="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-600">
                        Chưa có dữ liệu key.
                    </div>
                    <div id="userAiTestResults" class="hidden space-y-1 rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs"></div>
                    <p id="userAiSettingsStatus" class="min-h-[1.25rem] text-sm font-semibold text-slate-500"></p>
                </div>
                <div class="flex flex-col gap-2 border-t border-slate-200 bg-slate-50 px-5 py-3 sm:flex-row sm:items-center sm:justify-between">
                    <button type="button" id="userAiDeleteBtn" class="rounded-lg border border-rose-200 px-4 py-2 text-sm font-bold text-rose-600 hover:bg-rose-50">Xóa key</button>
                    <div class="flex flex-wrap gap-2">
                        <button type="button" id="userAiTestBtn" class="rounded-lg border border-indigo-200 bg-white px-4 py-2 text-sm font-bold text-indigo-700 hover:bg-indigo-50">Kiểm tra Key</button>
                        <button type="button" id="userAiSaveBtn" class="rounded-lg bg-indigo-600 px-5 py-2 text-sm font-bold text-white hover:bg-indigo-700">Lưu lên CSDL</button>
                    </div>
                </div>
            </div>`;
        document.body.appendChild(wrap);
        wrap.addEventListener('click', (e) => {
            if (e.target === wrap) UserAiSettings.closeModal();
        });
        document.getElementById('userAiSettingsClose').addEventListener('click', () => UserAiSettings.closeModal());
        document.getElementById('userAiGeminiFile').addEventListener('change', (e) => {
            const file = e.target.files && e.target.files[0];
            if (file) UserAiSettings.handleFile(file, 'gemini');
            e.target.value = '';
        });
        document.getElementById('userAiMistralFile').addEventListener('change', (e) => {
            const file = e.target.files && e.target.files[0];
            if (file) UserAiSettings.handleFile(file, 'mistral');
            e.target.value = '';
        });
        document.getElementById('userAiTestBtn').addEventListener('click', () => UserAiSettings.testGeminiKeys());
        document.getElementById('userAiSaveBtn').addEventListener('click', () => UserAiSettings.saveSettings());
        document.getElementById('userAiDeleteBtn').addEventListener('click', () => UserAiSettings.deleteKeys());
    }

    function fillForm(payload) {
        const geminiArea = document.getElementById('userAiGeminiKeys');
        const mistralArea = document.getElementById('userAiMistralKeys');
        const modelSelect = document.getElementById('userAiGeminiModel');
        const meta = document.getElementById('userAiMeta');
        const keys = Array.isArray(payload?.keys) ? payload.keys : [];
        const mistral = Array.isArray(payload?.mistral_keys) ? payload.mistral_keys : [];
        if (geminiArea) geminiArea.value = keys.join('\n');
        if (mistralArea) mistralArea.value = mistral.join('\n');
        const model = currentModel();
        if (modelSelect) {
            modelSelect.innerHTML = modelOptionsHtml(model);
            modelSelect.value = model;
        }
        if (meta) {
            const geminiCount = Number(payload?.count ?? keys.length) || 0;
            const mistralCount = Number(payload?.mistral_count ?? mistral.length) || 0;
            meta.textContent = `Gemini: ${geminiCount} key · Mistral: ${mistralCount} key · Lưu gần nhất: ${formatTime(payload?.updated_at || payload?.mistral_updated_at)}`;
        }
    }

    function badgeHtml(geminiCount, mistralCount) {
        if (geminiCount > 0) {
            return `<i class="fas fa-key text-emerald-300"></i> API Key sẵn sàng · Gemini ${geminiCount}${mistralCount ? ' · Mistral ' + mistralCount : ''}`;
        }
        return `<i class="fas fa-key text-amber-300"></i> Chưa nạp API Key — bấm để cài đặt`;
    }

    const UserAiSettings = {
        ensureModal,

        async openModal() {
            if (isStudent()) return;
            ensureModal();
            setLoginHint(false);
            setStatus('Đang tải cài đặt...', '');
            const modal = document.getElementById('userAiSettingsModal');
            modal.classList.remove('hidden');
            fillForm({
                keys: [],
                mistral_keys: [],
                count: 0,
                mistral_count: 0,
            });
            try {
                const { res, data } = await api('GET');
                if (res.status === 401) {
                    setLoginHint(true);
                    setStatus('Vui lòng đăng nhập lại để nạp key từ CSDL.', 'warning');
                    showToast('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.', 'warning');
                    return;
                }
                if (!res.ok || !data.ok) {
                    setStatus(data.error || 'Không tải được key từ máy chủ.', 'error');
                    return;
                }
                fillForm(data);
                setStatus('', '');
            } catch {
                setStatus('Không kết nối được máy chủ. Có thể chỉnh model trên máy.', 'warning');
            }
        },

        closeModal() {
            const el = document.getElementById('userAiSettingsModal');
            if (el) el.classList.add('hidden');
        },

        handleFile(file, type) {
            if (!file) return;
            const reader = new FileReader();
            reader.onload = () => {
                const keys = parseKeys(reader.result);
                const targetId = type === 'mistral' ? 'userAiMistralKeys' : 'userAiGeminiKeys';
                const area = document.getElementById(targetId);
                if (area) area.value = keys.join('\n');
                if (!keys.length) {
                    setStatus('Không tìm thấy API Key hợp lệ (> 10 ký tự) trong file txt.', 'warning');
                    showToast('Không tìm thấy API Key hợp lệ trong file txt.', 'warning');
                    return;
                }
                setStatus(`Đã nạp ${keys.length} key từ tệp.`, 'success');
            };
            reader.onerror = () => {
                setStatus('Không đọc được tệp.', 'error');
            };
            reader.readAsText(file);
        },

        async testGeminiKeys() {
            ensureModal();
            setStatus('Đang kiểm tra Gemini key trên máy chủ...', '');
            const resultsBox = document.getElementById('userAiTestResults');
            if (resultsBox) {
                resultsBox.classList.add('hidden');
                resultsBox.innerHTML = '';
            }
            try {
                const geminiLines = parseKeys(document.getElementById('userAiGeminiKeys')?.value || '');
                if (geminiLines.length) {
                    const saveRes = await api('POST', { keys: geminiLines });
                    if (saveRes.res.status === 401) {
                        setLoginHint(true);
                        setStatus('Vui lòng đăng nhập lại để kiểm tra key.', 'warning');
                        showToast('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.', 'warning');
                        return;
                    }
                }
                const { res, data } = await api('POST', { action: 'test' });
                if (res.status === 401) {
                    setLoginHint(true);
                    setStatus('Vui lòng đăng nhập lại để kiểm tra key.', 'warning');
                    showToast('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.', 'warning');
                    return;
                }
                const rows = Array.isArray(data.results) ? data.results : [];
                if (resultsBox) {
                    resultsBox.classList.remove('hidden');
                    resultsBox.innerHTML = rows.length
                        ? rows.map((row) => {
                            const ok = !!row.valid;
                            return `<div class="${ok ? 'text-emerald-700' : 'text-rose-600'}">${ok ? '✓' : '✕'} Key ${row.index || ''} ${row.masked || ''} — ${ok ? 'hợp lệ' : (row.error || 'lỗi')}</div>`;
                        }).join('')
                        : `<div class="text-amber-700">${data.error || 'Chưa có Gemini API Key để kiểm tra.'}</div>`;
                }
                if (data.ok && data.valid_count > 0) {
                    setStatus(`Kiểm tra xong: ${data.valid_count}/${data.tested || rows.length} key hợp lệ.`, 'success');
                } else {
                    setStatus(data.error || 'Không có key hợp lệ.', 'warning');
                }
            } catch {
                setStatus('Không gọi được máy chủ để kiểm tra key.', 'error');
            }
        },

        async saveSettings() {
            ensureModal();
            const model = persistModel(document.getElementById('userAiGeminiModel')?.value);
            const geminiLines = parseKeys(document.getElementById('userAiGeminiKeys')?.value || '');
            const mistralLines = parseKeys(document.getElementById('userAiMistralKeys')?.value || '');
            persistLocalKeys(geminiLines, mistralLines, { wipeEmpty: true });
            setStatus('Đang lưu lên CSDL...', '');
            try {
                const { res, data } = await api('POST', {
                    keys: geminiLines,
                    mistral_keys: mistralLines,
                });
                if (res.status === 401) {
                    setLoginHint(true);
                    setStatus('Đã lưu trên máy. Đăng nhập lại để lưu lên CSDL.', 'warning');
                    showToast('Đã lưu trên máy. Vui lòng đăng nhập lại để lưu lên CSDL.', 'warning');
                    UserAiSettings.updateBadge();
                    return;
                }
                if (!res.ok || !data.ok) {
                    setStatus(data.error || 'Lưu CSDL thất bại. Key vẫn được giữ trên máy.', 'error');
                    showToast(data.error || 'Lưu CSDL thất bại.', 'error');
                    UserAiSettings.updateBadge();
                    return;
                }
                fillForm(data);
                persistLocalKeys(data.keys || geminiLines, data.mistral_keys || mistralLines, { wipeEmpty: true });
                persistModel(model);
                UserAiSettings.updateBadge();
                setStatus('Đã lưu lên CSDL và đồng bộ toàn hệ thống.', 'success');
                showToast(`Đã lưu lên CSDL: Gemini ${(data.keys || geminiLines).length} key, Mistral ${(data.mistral_keys || mistralLines).length} key.`, 'success');
            } catch {
                setStatus('Đã lưu trên máy. Không kết nối được CSDL.', 'warning');
                showToast('Đã lưu trên máy. Không kết nối được CSDL.', 'warning');
                UserAiSettings.updateBadge();
            }
        },

        async deleteKeys() {
            if (!confirm('Xóa toàn bộ Gemini và Mistral API Key khỏi CSDL tài khoản này?')) return;
            ensureModal();
            setStatus('Đang xóa key...', '');
            try {
                const { res, data } = await api('DELETE');
                if (res.status === 401) {
                    setLoginHint(true);
                    setStatus('Vui lòng đăng nhập lại để xóa key trên CSDL.', 'warning');
                    showToast('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.', 'warning');
                    return;
                }
                if (!res.ok || !data.ok) {
                    setStatus(data.error || 'Không xóa được key trên CSDL.', 'error');
                    return;
                }
                persistLocalKeys([], [], { wipeEmpty: true });
                fillForm({ keys: [], mistral_keys: [], count: 0, mistral_count: 0, updated_at: null });
                UserAiSettings.updateBadge();
                setStatus('Đã xóa toàn bộ key khỏi CSDL.', 'success');
                showToast('Đã xóa API Key khỏi CSDL.', 'success');
            } catch {
                setStatus('Không kết nối được máy chủ để xóa key.', 'error');
            }
        },

        async updateBadge() {
            const hero = document.getElementById('heroKeyStatus');
            const navBtn = document.getElementById('btnOpenUserAiSettings');
            if (navBtn) navBtn.classList.toggle('hidden', isStudent());
            if (!hero) return;
            let geminiCount = 0;
            let mistralCount = 0;
            try {
                const rawG = JSON.parse(localStorage.getItem('global_gemini_keys') || '[]');
                const rawM = JSON.parse(localStorage.getItem('global_mistral_keys') || '[]');
                if (Array.isArray(rawG)) geminiCount = rawG.filter(Boolean).length;
                if (Array.isArray(rawM)) mistralCount = rawM.filter(Boolean).length;
            } catch { /* ignore */ }
            try {
                const { res, data } = await api('GET');
                if (res.ok && data.ok) {
                    geminiCount = Number(data.count || (data.keys || []).length) || 0;
                    mistralCount = Number(data.mistral_count || (data.mistral_keys || []).length) || 0;
                    persistLocalKeys(data.keys || [], data.mistral_keys || []);
                }
            } catch { /* keep local counts */ }
            hero.innerHTML = badgeHtml(geminiCount, mistralCount);
        },

        init() {
            if (isStudent()) {
                const navBtn = document.getElementById('btnOpenUserAiSettings');
                if (navBtn) navBtn.classList.add('hidden');
                return;
            }
            UserAiSettings.updateBadge();
        },
    };

    global.UserAiSettings = UserAiSettings;
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => UserAiSettings.init());
    } else {
        UserAiSettings.init();
    }
})(window);
