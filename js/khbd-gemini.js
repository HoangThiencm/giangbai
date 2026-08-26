/**
 * js/khbd-gemini.js
 * Module giao tiếp Gemini API (REST v1beta) với cơ chế Xoay vòng Key (Key Rotation),
 * Hỗ trợ Multimodal (ảnh base64), chuyển đổi Model AI, fallback đọc global_gemini_keys từ hệ thống.
 */

class GeminiAPIManager {
  constructor() {
    this.apiKeys = [];
    this.currentKeyIndex = 0;
    this.selectedModel = "gemini-3.7-flash";
    this.availableModels = [
      { id: "gemini-3.7-flash", name: "Gemini 3.7 Flash (Mới nhất & Tối ưu nhất - Mặc định)", recommended: true },
      { id: "gemini-3.6-flash", name: "Gemini 3.6 Flash", recommended: false },
      { id: "gemini-3.5-flash", name: "Gemini 3.5 Flash", recommended: false },
      { id: "gemini-2.5-flash", name: "Gemini 2.5 Flash (Nhẹ & Nhanh)", recommended: false },
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
    this.loadModelFromLocalStorage();
  }

  getStorageKey() {
    return 'khbd_user_gemini_keys_' + (localStorage.getItem('userEmail') || 'default');
  }

  // Tải danh sách keys từ localStorage theo tài khoản cá nhân
  loadKeysFromLocalStorage() {
    try {
      const storageKey = this.getStorageKey();
      const saved = localStorage.getItem(storageKey);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          this.apiKeys = parsed.map(k => k.trim()).filter(k => k.length > 0);
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
      localStorage.setItem(storageKey, JSON.stringify(this.apiKeys));
    } catch (e) {
      console.error("Lỗi lưu keys vào localStorage:", e);
    }
  }

  // Đồng bộ danh sách keys từ máy chủ CSDL
  async syncKeysFromServer() {
    try {
      const res = await fetch('api/user_gemini_keys.php', {
        method: 'GET',
        cache: 'no-store',
        credentials: 'include'
      });
      if (res.ok) {
        const data = await res.json();
        if (data.ok && Array.isArray(data.keys)) {
          if (data.keys.length > 0) {
            this.apiKeys = data.keys.map(k => k.trim()).filter(k => k.length > 10);
            this.saveKeysToLocalStorage();
          } else if (this.apiKeys && this.apiKeys.length > 0) {
            // Tự động migrate keys cũ từ localStorage lên CSDL máy chủ
            await this.saveKeysToServer(this.apiKeys);
          }
        }
      }
    } catch (e) {
      console.warn("Không thể đồng bộ keys từ server:", e);
    }
    return this.apiKeys;
  }

  // Lưu danh sách keys lên máy chủ CSDL và localStorage
  async saveKeysToServer(keysArray) {
    const cleanKeys = Array.from(new Set((Array.isArray(keysArray) ? keysArray : [])
      .map(k => String(k || '').trim())
      .filter(k => k.length > 10)));
    this.apiKeys = cleanKeys;
    this.currentKeyIndex = 0;
    this.saveKeysToLocalStorage();

    try {
      const res = await fetch('api/user_gemini_keys.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ keys: this.apiKeys })
      });
      if (res.ok) {
        const data = await res.json();
        if (data.ok && Array.isArray(data.keys)) {
          this.apiKeys = data.keys;
          this.saveKeysToLocalStorage();
        }
        return data;
      }
    } catch (e) {
      console.error("Lỗi khi lưu keys lên máy chủ:", e);
    }
    return { ok: false, keys: this.apiKeys, count: this.apiKeys.length };
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
    return (this.apiKeys && this.apiKeys.length >= 2) ? 2500 : 6000;
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

  // Kiểm tra tính hợp lệ của 1 API Key
  async testApiKey(key, model = "gemini-3.7-flash") {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`;
    const payload = {
      contents: [{ role: "user", parts: [{ text: "Xin chào, hãy trả lời 'OK'." }] }],
      generationConfig: { maxOutputTokens: 10 }
    };

    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error?.message || `HTTP ${res.status}: ${res.statusText}`);
    }
    return true;
  }

  /**
   * Gửi yêu cầu sinh nội dung (Content Generation)
   * @param {string} prompt Nội dung câu lệnh
   * @param {Array<{mimeType: string, base64: string}>} images Danh sách ảnh (nếu có)
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
        maxOutputTokens: options.maxOutputTokens || (images.length ? 16384 : 8192)
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
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${activeModel}:generateContent?key=${currentKey}`;

        try {
          const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
            signal
          });

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
          if (err.name === "TypeError" && String(err.message).includes("fetch")) {
            throw new Error(`Lỗi kết nối mạng: Không thể gọi đến máy chủ Gemini API. Vui lòng kiểm tra Internet hoặc thử lại.`);
          }
          lastError = err;
          // Transient 5xx đã continue trong nhánh HTTP; các lỗi còn lại (400, hết hạn mức, ...) ném ra.
          throw err;
        }
      }

      throw new Error(`Tất cả ${totalKeys} API keys đều thất bại hoặc hết hạn mức. Lỗi cuối cùng: ${lastError?.message || "Không xác định"}`);
    } finally {
      this._lastRequestEndedAt = Date.now();
    }
  }
}

// Khởi tạo instance toàn cục
const geminiAPI = new GeminiAPIManager();

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { GeminiAPIManager, geminiAPI };
}
