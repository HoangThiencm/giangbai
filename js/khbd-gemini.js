/**
 * js/khbd-gemini.js
 * Module giao tiếp Gemini API (REST v1beta) với cơ chế Xoay vòng Key (Key Rotation),
 * Hỗ trợ Multimodal (ảnh base64), chuyển đổi Model AI, fallback đọc global_gemini_keys từ hệ thống.
 */

class GeminiAPIManager {
  constructor() {
    this.apiKeys = [];
    this.mistralKeys = [];
    this.currentKeyIndex = 0;
    this.selectedModel = "gemini-3.7-flash";
    this.availableModels = [
      { id: "gemini-3.7-flash", name: "Gemini 3.7 Flash (Mới nhất & Tối ưu nhất - Mặc định)", recommended: true },
      { id: "gemini-3.6-flash", name: "Gemini 3.6 Flash", recommended: false },
      { id: "gemini-3.5-flash", name: "Gemini 3.5 Flash", recommended: false },
      { id: "gemini-3.5-flash-lite", name: "Gemini 3.5 Flash Lite (Nhẹ, Nhanh & Tiết kiệm Token)", recommended: false },
      { id: "gemini-2.5-flash", name: "Gemini 2.5 Flash (Nhẹ & Nhanh)", recommended: false },
      { id: "gemini-2.5-flash-lite", name: "Gemini 2.5 Flash Lite (Tối ưu Free Tier - Nhanh & Tiết kiệm Token)", recommended: false },
      { id: "gemini-3-flash-preview", name: "Gemini 3 Flash Preview (Thử nghiệm)", recommended: false }
    ];

    this.onKeyRotatedCallback = null;
    this.onStatusCallback = null;
    this._requestQueue = Promise.resolve();
    this._lastRequestEndedAt = 0;
    this.init();
  }

  init() {
    this.loadKeysFromLocalStorage();
    this.loadMistralKeysFromLocalStorage();
    this.loadModelFromLocalStorage();
  }

  getStorageKey() {
    return 'khbd_user_gemini_keys_' + (localStorage.getItem('userEmail') || 'default');
  }

  getMistralStorageKey() {
    return 'khbd_user_mistral_keys_' + (localStorage.getItem('userEmail') || 'default');
  }

  static cleanKeyList(keysArray) {
    return Array.from(new Set((Array.isArray(keysArray) ? keysArray : [])
      .map(k => String(k || "").trim())
      .filter(k => k.length > 10)));
  }

  // Tải danh sách keys từ localStorage theo tài khoản cá nhân
  loadKeysFromLocalStorage() {
    try {
      const storageKey = this.getStorageKey();
      const saved = localStorage.getItem(storageKey)
        || localStorage.getItem('global_gemini_keys')
        || localStorage.getItem('gemini_api_keys')
        || localStorage.getItem('khbd_user_gemini_keys_default');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          this.apiKeys = GeminiAPIManager.cleanKeyList(parsed);
          return;
        }
      }
      this.apiKeys = [];
    } catch (e) {
      console.warn("Lỗi đọc keys từ localStorage:", e);
      this.apiKeys = [];
    }
  }

  // Lưu danh sách keys vào localStorage theo tài khoản cá nhân
  saveKeysToLocalStorage() {
    try {
      const storageKey = this.getStorageKey();
      const json = JSON.stringify(this.apiKeys || []);
      localStorage.setItem(storageKey, json);
      localStorage.setItem('global_gemini_keys', json);
      localStorage.setItem('khbd_user_gemini_keys_default', json);
    } catch (e) {
      console.error("Lỗi lưu keys vào localStorage:", e);
    }
  }

  loadMistralKeysFromLocalStorage() {
    try {
      const saved = localStorage.getItem(this.getMistralStorageKey())
        || localStorage.getItem('global_mistral_keys')
        || localStorage.getItem('mistral_api_keys')
        || localStorage.getItem('khbd_user_mistral_keys_default');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          this.mistralKeys = GeminiAPIManager.cleanKeyList(parsed);
          return;
        }
      }
      this.mistralKeys = [];
    } catch (e) {
      console.warn("Lỗi đọc Mistral keys từ localStorage:", e);
      this.mistralKeys = [];
    }
  }

  saveMistralKeysToLocalStorage() {
    try {
      const json = JSON.stringify(this.mistralKeys || []);
      localStorage.setItem(this.getMistralStorageKey(), json);
      localStorage.setItem('global_mistral_keys', json);
      localStorage.setItem('khbd_user_mistral_keys_default', json);
    } catch (e) {
      console.error("Lỗi lưu Mistral keys vào localStorage:", e);
    }
  }

  applyServerKeyPayload(data) {
    if (!data || typeof data !== "object") return;
    if (Array.isArray(data.keys)) {
      this.apiKeys = GeminiAPIManager.cleanKeyList(data.keys);
      this.currentKeyIndex = 0;
      this.saveKeysToLocalStorage();
    }
    if (Array.isArray(data.mistral_keys)) {
      this.mistralKeys = GeminiAPIManager.cleanKeyList(data.mistral_keys);
      this.saveMistralKeysToLocalStorage();
    }
  }

  // Đồng bộ danh sách keys từ máy chủ CSDL (nếu có session đăng nhập)
  async syncKeysFromServer() {
    try {
      if (typeof fetch !== "function") return this.apiKeys;
      const res = await fetch('api/user_gemini_keys.php', {
        method: 'GET',
        cache: 'no-store',
        credentials: 'include'
      }).catch(() => null);
      if (res && res.ok) {
        const data = await res.json().catch(() => ({}));
        if (data.ok) {
          const serverGemini = Array.isArray(data.keys) ? data.keys : [];
          const serverMistral = Array.isArray(data.mistral_keys) ? data.mistral_keys : [];
          if (serverGemini.length > 0) {
            this.apiKeys = GeminiAPIManager.cleanKeyList(serverGemini);
            this.saveKeysToLocalStorage();
          }
          if (serverMistral.length > 0) {
            this.mistralKeys = GeminiAPIManager.cleanKeyList(serverMistral);
            this.saveMistralKeysToLocalStorage();
          }
        }
      }
    } catch {
      // Bỏ qua trong im lặng nếu chạy không có backend session
    }
    return this.apiKeys;
  }

  async saveUserAiKeysToServer(payload) {
    const body = {};
    if (Array.isArray(payload?.keys)) {
      this.apiKeys = GeminiAPIManager.cleanKeyList(payload.keys);
      this.currentKeyIndex = 0;
      this.saveKeysToLocalStorage();
      body.keys = this.apiKeys;
    }
    if (Array.isArray(payload?.mistral_keys)) {
      this.mistralKeys = GeminiAPIManager.cleanKeyList(payload.mistral_keys);
      this.saveMistralKeysToLocalStorage();
      body.mistral_keys = this.mistralKeys;
    }
    if (!Object.keys(body).length) {
      return { ok: true, keys: this.apiKeys, mistral_keys: this.mistralKeys, count: this.apiKeys.length, mistral_count: this.mistralKeys.length };
    }

    try {
      const res = await fetch('api/user_gemini_keys.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(body)
      }).catch(() => null);
      if (res && res.ok) {
        const data = await res.json().catch(() => ({}));
        if (data.ok) this.applyServerKeyPayload(data);
        return data;
      }
    } catch {
      // Lưu offline/local an toàn
    }
    return { ok: true, keys: this.apiKeys, mistral_keys: this.mistralKeys, count: this.apiKeys.length, mistral_count: this.mistralKeys.length };
  }

  // Lưu danh sách Gemini keys lên máy chủ CSDL và localStorage
  async saveKeysToServer(keysArray) {
    return this.saveUserAiKeysToServer({ keys: keysArray });
  }

  async saveMistralKeysToServer(keysArray) {
    return this.saveUserAiKeysToServer({ mistral_keys: keysArray });
  }

  // Tải Model đã chọn (hoặc lấy mặc định từ hệ thống)
  loadModelFromLocalStorage() {
    const savedModel = localStorage.getItem("khbd_gemini_model") || localStorage.getItem("default_gemini_module");
    if (savedModel && this.availableModels.some(m => m.id === savedModel)) {
      this.selectedModel = savedModel;
    } else {
      this.selectedModel = "gemini-3.7-flash";
    }
  }

  setModel(modelId) {
    this.selectedModel = modelId;
    localStorage.setItem("khbd_gemini_model", modelId);
  }

  // Cập nhật danh sách API Keys
  setApiKeys(keysArray) {
    this.apiKeys = Array.from(new Set(keysArray
      .map(k => k.trim())
      .filter(k => k.length > 10)));
    this.currentKeyIndex = 0;
    this.saveKeysToLocalStorage();
  }

  // Lấy key hiện tại
  getCurrentKey() {
    if (this.apiKeys.length === 0) return null;
    if (this.currentKeyIndex >= this.apiKeys.length) {
      this.currentKeyIndex = 0;
    }
    return this.apiKeys[this.currentKeyIndex];
  }

  // Xoay vòng sang key tiếp theo
  rotateKey(reason = "") {
    if (this.apiKeys.length <= 1) return;
    const prevIndex = this.currentKeyIndex;
    this.currentKeyIndex = (this.currentKeyIndex + 1) % this.apiKeys.length;
    console.warn(`[Key Rotation] Chuyển từ Key #${prevIndex + 1} sang Key #${this.currentKeyIndex + 1}. Lý do: ${reason}`);
    
    if (typeof this.onKeyRotatedCallback === "function") {
      this.onKeyRotatedCallback({
        prevIndex,
        newIndex: this.currentKeyIndex,
        totalKeys: this.apiKeys.length,
        reason
      });
    }
  }

  waitForRetry(ms, signal = null) {
    return new Promise((resolve, reject) => {
      if (signal?.aborted) {
        reject(new DOMException("Yêu cầu đã bị hủy.", "AbortError"));
        return;
      }
      const timer = setTimeout(resolve, Math.max(0, ms));
      if (signal) signal.addEventListener("abort", () => {
        clearTimeout(timer);
        reject(new DOMException("Yêu cầu đã bị hủy.", "AbortError"));
      }, { once: true });
    });
  }

  getMinRequestGapMs() {
    return (this.apiKeys && this.apiKeys.length >= 2) ? 3500 : 7000;
  }

  emitGeminiStatus(info, options = {}) {
    const payload = typeof info === "string" ? { message: info } : (info || {});
    if (payload.message) console.warn("[Gemini]", payload.message);
    if (typeof options.onStatus === "function") options.onStatus(payload);
    if (typeof this.onStatusCallback === "function") this.onStatusCallback(payload);
  }

  isTransientGeminiError(status, errMsg) {
    if (status === 500 || status === 502 || status === 503 || status === 504) return true;
    const m = String(errMsg || "").toLowerCase();
    return /high demand|unavailable|try again later/.test(m);
  }

  isDailyQuotaError(errMsg) {
    const m = String(errMsg || "").toLowerCase();
    if (/high demand/.test(m)) return false;
    if (/retry in\s*[\d.]+/.test(m)) return false;
    if (m.includes("quota") && m.includes("exhausted")) return true;
    if (/daily/.test(m) && /(limit|quota)/.test(m)) return true;
    return false;
  }

  parseRetryAfterMs(errMsg, response, backoffStep = 0) {
    const retryMatch = String(errMsg || "").match(/retry in ([\d.]+)\s*s/i);
    if (retryMatch) {
      return Math.min(25000, Math.max(2000, Math.ceil(parseFloat(retryMatch[1]) * 1000) + 400));
    }
    const retryAfter = typeof response?.headers?.get === "function"
      ? (response.headers.get("Retry-After") || response.headers.get("retry-after"))
      : null;
    if (retryAfter != null && String(retryAfter).trim() !== "") {
      const raw = String(retryAfter).trim();
      const asSeconds = Number(raw);
      if (Number.isFinite(asSeconds) && asSeconds >= 0) {
        return Math.min(25000, Math.max(2000, Math.ceil(asSeconds * 1000)));
      }
      const asDate = Date.parse(raw);
      if (!Number.isNaN(asDate)) {
        return Math.min(25000, Math.max(2000, asDate - Date.now()));
      }
    }
    return Math.min(25000, 2000 * Math.pow(2, backoffStep));
  }

  async _waitMinRequestGap(signal, options = {}) {
    if (options._testFastRetry) return;
    if (!this._lastRequestEndedAt) return;
    const remaining = this._lastRequestEndedAt + this.getMinRequestGapMs() - Date.now();
    if (remaining > 0) {
      await this.waitForRetry(remaining, signal);
    }
  }

  _fallbackModelId() {
    return "gemini-2.5-flash";
  }

  isUserAbort(err, signal) {
    return err?.name === "AbortError" && signal?.aborted;
  }

  async fetchWithTimeout(url, init = {}, timeoutMs = 0) {
    if (!timeoutMs || timeoutMs <= 0) {
      return fetch(url, init);
    }
    const ctrl = new AbortController();
    const external = init.signal;
    let timedOut = false;
    const onExternalAbort = () => ctrl.abort();
    if (external) {
      if (external.aborted) {
        throw new DOMException("Yêu cầu đã bị hủy.", "AbortError");
      }
      external.addEventListener("abort", onExternalAbort, { once: true });
    }
    const timer = setTimeout(() => {
      timedOut = true;
      ctrl.abort();
    }, timeoutMs);
    try {
      return await fetch(url, { ...init, signal: ctrl.signal });
    } catch (err) {
      if (err?.name === "AbortError" && timedOut && !external?.aborted) {
        const timeoutErr = new Error(`Hết thời gian chờ ${Math.round(timeoutMs / 1000)}s khi gọi Gemini.`);
        timeoutErr.name = "TimeoutError";
        throw timeoutErr;
      }
      throw err;
    } finally {
      clearTimeout(timer);
      if (external) external.removeEventListener("abort", onExternalAbort);
    }
  }

  async fetchGeminiGenerate(model, key, payload, signal, timeoutMs, options = {}) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`;
    return await this.fetchWithTimeout(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal
    }, timeoutMs);
  }

  // Kiểm tra tính hợp lệ của 1 API Key
  async testApiKey(key, model = "gemini-3.7-flash") {
    const payload = {
      contents: [{ role: "user", parts: [{ text: "Xin chào, hãy trả lời 'OK'." }] }],
      generationConfig: {
        maxOutputTokens: 10,
        thinkingConfig: {
          thinkingBudget: 0
        }
      }
    };
    const res = await this.fetchGeminiGenerate(model, key, payload, null, 15000);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error?.message || `HTTP ${res.status}: ${res.statusText}`);
    }
    return true;
  }

  async testMistralApiKey(key) {
    const res = await this.fetchWithTimeout("https://api.mistral.ai/v1/models", {
      method: "GET",
      headers: { Authorization: `Bearer ${key}` }
    }, 15000);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.message || err.error?.message || `HTTP ${res.status}: ${res.statusText}`);
    }
    return true;
  }

  /**
   * Gửi yêu cầu sinh nội dung (Content Generation)
   * @param {string} prompt Nội dung câu lệnh
   * @param {Array<{mimeType: string, dataUrl?: string, base64?: string}>} images Ảnh image/* hoặc PDF application/pdf
   * @param {string} systemRole Chỉ dẫn hệ thống
   * @param {number} temperature Độ sáng tạo (0.0 - 1.0)
   */
  async generateContent(prompt, images = [], systemRole = null, temperature = 0.3, signal = null, options = {}) {
    const run = this._requestQueue.then(() =>
      this._generateContentInternal(prompt, images, systemRole, temperature, signal, options || {})
    );
    this._requestQueue = run.then(() => undefined, () => undefined);
    return run;
  }

  async _generateContentInternal(prompt, images = [], systemRole = null, temperature = 0.3, signal = null, options = {}) {
    // Luôn đảm bảo nạp keys mới nhất nếu trước đó chưa có
    if (!this.apiKeys || this.apiKeys.length === 0) {
      this.loadKeysFromLocalStorage();
    }

    if (!this.apiKeys || this.apiKeys.length === 0) {
      throw new Error("Bạn chưa cấu hình Gemini API Key cá nhân. Vui lòng bấm 'Quản lý API Key' để dán key hoặc nạp file .txt của bạn.");
    }

    const totalKeys = this.apiKeys.length;
    const fallbackModel = this._fallbackModelId();
    const selectedModel = this.selectedModel;
    let activeModel = selectedModel;
    let usedFallback = false;
    const modelCount = (selectedModel !== fallbackModel) ? 2 : 1;
    const maxAttempts = Math.max(totalKeys * modelCount + 3, 6);
    let attempts = 0;
    let lastError = null;
    let backoffStep = 0;
    let rotatedOnThisCall = 0;

    const waitMs = (ms) => (options._testFastRetry ? 1 : ms);

    const maybeFallback = (reason) => {
      if (usedFallback || activeModel === fallbackModel) return false;
      if (!this.availableModels.some(m => m.id === fallbackModel)) return false;
      const from = activeModel;
      activeModel = fallbackModel;
      usedFallback = true;
      const msg = `Đổi model tạm thời ${from} → ${fallbackModel} (${reason}, không lưu cài đặt).`;
      this.emitGeminiStatus({ type: "fallback", message: msg, model: activeModel }, options);
      return true;
    };

    // Chuẩn bị parts
    const parts = [];

    // Thêm các ảnh trước nếu có
    if (Array.isArray(images) && images.length > 0) {
      images.forEach(img => {
        let b64 = img.dataUrl || img.base64 || img.data || (typeof img === "string" ? img : "");
        if (b64 && typeof b64 === "string") {
          // Bỏ header data:image/...;base64, nếu có
          if (b64.includes(",")) {
            b64 = b64.split(",")[1];
          }
          parts.push({
            inlineData: {
              mimeType: img.mimeType || "image/jpeg",
              data: b64
            }
          });
        }
      });
    }

    // Thêm prompt text
    parts.push({ text: prompt });

    const payload = {
      contents: [{ role: "user", parts }],
      generationConfig: {
        temperature: temperature,
        topP: 0.95,
        maxOutputTokens: options.maxOutputTokens || (images.length ? 16384 : 8192),
        thinkingConfig: {
          thinkingBudget: (options.thinkingBudget !== undefined) ? options.thinkingBudget : 0
        }
      }
    };

    if (systemRole) {
      payload.systemInstruction = {
        parts: [{ text: systemRole }]
      };
    }

    await this._waitMinRequestGap(signal, options);

    try {
      while (attempts < maxAttempts) {
        if (signal?.aborted) throw new DOMException("Yêu cầu đã bị hủy.", "AbortError");
        const currentKey = this.getCurrentKey();
        const timeoutMs = options._testFastRetry ? 0 : (options.timeoutMs || 75000);

        try {
          this.emitGeminiStatus({
            type: "call",
            message: `Đang gọi Gemini (${activeModel})...`,
            model: activeModel
          }, options);
          const response = await this.fetchGeminiGenerate(
            activeModel,
            currentKey,
            payload,
            signal,
            timeoutMs,
            options
          );

          if (response.ok) {
            const data = await response.json();
            const candidate = data.candidates?.[0];

            if (!candidate) {
              throw new Error("Không nhận được phản hồi hợp lệ từ Gemini API.");
            }

            if (candidate.finishReason === "MAX_TOKENS") {
              console.warn("[Gemini] Phản hồi chạm giới hạn token (MAX_TOKENS). Đã tăng hạn mức output để đảm bảo trích xuất trọn vẹn.");
            }

            const textParts = candidate.content?.parts?.map(p => p.text || "").join("").trim();
            if (!textParts) {
              throw new Error("Gemini không trả về nội dung văn bản. Hãy thử lại với yêu cầu ngắn hơn hoặc model khác.");
            }
            if (usedFallback) {
              console.warn(`[Gemini] Dùng model ${activeModel} (fallback phiên gọi, không ghi đè khbd_gemini_model).`);
            }
            return textParts;
          }

          // Xử lý các lỗi HTTP
          const errJson = await response.json().catch(() => ({}));
          const errMsg = errJson.error?.message || `HTTP ${response.status}: ${response.statusText}`;
          lastError = new Error(errMsg);
          const transient = this.isTransientGeminiError(response.status, errMsg);
          const dailyQuota = this.isDailyQuotaError(errMsg);
          const quotaLike = response.status === 429 || response.status === 403
            || /quota|exhausted/i.test(errMsg);

          // Hết hạn mức ngày: xoay key; hết key thì ném lỗi rõ.
          if (dailyQuota) {
            if (this.apiKeys.length > 1 && rotatedOnThisCall < this.apiKeys.length - 1) {
              console.warn(`Key #${this.currentKeyIndex + 1} hết hạn mức ngày. Chuyển key và thử lại.`);
              this.rotateKey(`Lỗi HTTP ${response.status}: ${errMsg.substring(0, 80)}...`);
              rotatedOnThisCall++;
              attempts++;
              await this.waitForRetry(waitMs(800), signal);
              continue;
            }
            attempts++;
            throw new Error(`Hết hạn mức Gemini (429). ${errMsg}`);
          }

          // 429/403/quota: xoay key nếu còn key.
          if ((response.status === 429 || response.status === 403 || (quotaLike && !transient))
            && this.apiKeys.length > 1 && rotatedOnThisCall < this.apiKeys.length - 1) {
            console.warn(`Key #${this.currentKeyIndex + 1} lỗi ${response.status}/quota. Chuyển key và thử lại.`);
            this.rotateKey(`Lỗi HTTP ${response.status}: ${errMsg.substring(0, 80)}...`);
            rotatedOnThisCall++;
            attempts++;
            await this.waitForRetry(waitMs(800), signal);
            continue;
          }

          // Rate / high-demand / 5xx: chờ rồi thử lại; có thể đổi model. 403 (key sai) không retry vô hạn.
          if (transient || response.status === 429 || (quotaLike && response.status !== 403)) {
            const retryMs = this.parseRetryAfterMs(errMsg, response, backoffStep);
            const isLastKey = this.apiKeys.length <= 1 || rotatedOnThisCall >= this.apiKeys.length - 1;
            if (transient) {
              maybeFallback("quá tải/503");
            } else if (response.status === 429 && isLastKey) {
              maybeFallback("429 rate-limit key cuối");
            }
            attempts++;
            if (attempts < maxAttempts) {
              const secs = Math.max(1, Math.round(retryMs / 1000));
              this.emitGeminiStatus({
                type: "retry",
                message: `Đang chờ Gemini (quá tải), thử lại sau ${secs}s...`,
                waitSeconds: secs,
                model: activeModel
              }, options);
              await this.waitForRetry(waitMs(retryMs), signal);
              backoffStep++;
              continue;
            }
            throw new Error(`Lỗi Gemini API (${response.status}): ${errMsg}`);
          }

          // Lỗi khác không phụ thuộc key (ví dụ prompt sai/quá dài): dừng ngay.
          throw new Error(`Lỗi Gemini API (${response.status}): ${errMsg}`);

        } catch (err) {
          if (err?.name === "AbortError") throw err;
          if (err?.name === "TimeoutError" || (err.name === "TypeError" && /fetch/i.test(String(err.message || "")))) {
            lastError = new Error(`Không kết nối được Gemini: ${err.message}. Thử VPN, đổi mạng, hoặc chọn Gemini 2.5 Flash.`);
            attempts++;
            if (attempts < maxAttempts) {
              this.emitGeminiStatus({
                type: "retry",
                message: lastError.message,
                model: activeModel
              }, options);
              maybeFallback("không kết nối được");
              await this.waitForRetry(waitMs(1200), signal);
              continue;
            }
            throw lastError;
          }
          lastError = err;
          throw err;
        }
      }

      throw new Error(`Tất cả ${totalKeys} API keys đều thất bại hoặc hết hạn mức. Lỗi cuối cùng: ${lastError?.message || "Không xác định"}`);
    } finally {
      this._lastRequestEndedAt = Date.now();
    }
  }

  getImageModels() {
    return ["gemini-2.5-flash-image", "gemini-2.0-flash-preview-image-generation"];
  }

  extractInlineImage(data) {
    const parts = data?.candidates?.[0]?.content?.parts || [];
    for (const part of parts) {
      const inline = part.inlineData || part.inline_data;
      if (inline && inline.data) {
        const mime = inline.mimeType || inline.mime_type || "image/png";
        return `data:${mime};base64,${inline.data}`;
      }
    }
    return null;
  }

  async generateImage(prompt, options = {}) {
    const run = this._requestQueue.then(() => this._generateImageInternal(prompt, options || {}));
    this._requestQueue = run.then(() => undefined, () => undefined);
    return run;
  }

  async _generateImageInternal(prompt, options = {}) {
    if (!this.apiKeys || this.apiKeys.length === 0) this.loadKeysFromLocalStorage();
    if (!this.apiKeys || this.apiKeys.length === 0) {
      throw new Error("Bạn chưa cấu hình Gemini API Key cá nhân. Vui lòng bấm 'Quản lý API Key'.");
    }
    const payload = {
      contents: [{ role: "user", parts: [{ text: String(prompt || "").trim() }] }],
      generationConfig: {
        responseModalities: ["TEXT", "IMAGE"],
        temperature: 0.35
      }
    };
    let lastError = null;
    const models = this.getImageModels();
    for (const model of models) {
      try {
        this.emitGeminiStatus({ type: "call", message: `Đang tạo ảnh (${model})...`, model }, options);
        const response = await this.fetchGeminiGenerate(
          model,
          this.getCurrentKey(),
          payload,
          options.signal || null,
          options.timeoutMs || 90000,
          options
        );
        if (!response.ok) {
          const errJson = await response.json().catch(() => ({}));
          throw new Error(errJson.error?.message || `HTTP ${response.status}`);
        }
        const data = await response.json();
        const image = this.extractInlineImage(data);
        if (image) return image;
        lastError = new Error(`${model} không trả về dữ liệu ảnh.`);
      } catch (error) {
        lastError = error;
        console.warn(`[Gemini] Tạo ảnh bằng ${model} chưa thành công:`, error);
      }
    }
    throw lastError || new Error("Không tạo được ảnh minh họa.");
  }
}

// Khởi tạo instance toàn cục
const geminiAPI = new GeminiAPIManager();

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { GeminiAPIManager, geminiAPI };
}
