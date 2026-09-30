# IMPLEMENT — OCR clipboard & đồng bộ API key Quản lý văn bản

Đã implement đúng `docs/handoff/PLAN.md`.

## Đã sửa

1. `vanban-app.js`
   - Thêm `getAvailableGeminiKeys()` và `getAvailableMistralKeys()`: ưu tiên `global_*`, rồi `khbd_user_*_<email>`, `khbd_user_*_default`, các khóa legacy (`khbd_gemini_api_keys`, `gemini_api_keys`, `xdpl_gemini_api_keys`, `geometryAiApiKeys`, `xdpl_mistral_api_keys`). Hết key local mới gọi `AiDesignConfig.getApiKeys()` / `getMistralKeys()`.
   - `hasMistralOcr()` / `hasGeminiVision()` dùng hai hàm trên.
   - `ensureKeysLoaded()` await một lần `syncUserKeysFromServer()`; `ocrImageData()` gọi ở đầu hàm.
   - `extractTextViaGeminiVision()` lấy key từ `getAvailableGeminiKeys()`. Model vẫn `AiDesignConfig.getModule()` khi có, mặc định `gemini-2.5-flash`.
   - `openSystemAiConfig()` ưu tiên `UserAiSettings.openModal('keys')`, fallback `AiDesignConfig.openModal()`. Dùng khi thiếu cả hai loại key và khi bấm `#vanbanAiConfigBtn`.

2. `quanlyvanban-chuyenmon.html`, `quanlyvanban-hanhchinh.html`, `quanlyvanban-dang.html`
   - Trong `<head>`: `<script src="js/user-ai-settings.js?v=20261001"></script>`.

3. `tests/vanban-ocr-clipboard-smoke.js`
   - Khẳng định tên hàm đọc key, khóa `khbd_user_*`, `ensureKeysLoaded` trong `ocrImageData`, và `UserAiSettings.openModal('keys')`.

## Smoke

Exit code 0:

- `node tests/vanban-ocr-clipboard-smoke.js`
- `node tests/vanban-chuyenmon-signature-smoke.js`
- `node tests/vanban-display-saved-smoke.js`
- `python tests/vanban-chuyenmon-root-smoke.py`

## Ngoài phạm vi

Chưa commit, chưa push. Bàn giao Antigravity IDE, chat mới: `/verify`.
