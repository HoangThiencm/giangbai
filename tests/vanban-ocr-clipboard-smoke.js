const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

const app = fs.readFileSync(path.join(__dirname, '..', 'vanban-app.js'), 'utf8');

[
    'async function syncUserKeysFromServer()',
    "fetch('api/user_gemini_keys.php'",
    "credentials: 'include'",
    "cache: 'no-store'",
    'global_gemini_keys',
    'global_mistral_keys',
    'd.mistral_keys',
    'AiDesignConfig.loadHostingFallbackConfig()',
    'id="vanbanAiConfigBtn"',
    'Cấu hình AI',
    'AiDesignConfig.openModal()',
    'function hasGeminiVision()',
    'function getAvailableGeminiKeys()',
    'function getAvailableMistralKeys()',
    'khbd_user_gemini_keys_',
    'khbd_user_mistral_keys_',
    'khbd_user_gemini_keys_default',
    'khbd_user_mistral_keys_default',
    'async function ensureKeysLoaded()',
    'await ensureKeysLoaded()',
    'function openSystemAiConfig()',
    "UserAiSettings.openModal('keys')",
    'AiDesignConfig.getApiKeys()',
    'async function extractTextViaGeminiVision(dataUrl)',
    'gemini-2.5-flash',
    'inline_data',
    "mode: 'gemini-vision'",
    'async function ocrImageData(dataUrl)',
    'window.MistralOcr.ocrImageDataUrl(dataUrl)',
    'Ảnh chụp cần API Key (Mistral hoặc Gemini)',
    'ingestClipboardImage',
    'await ocrImageData(dataUrl)',
].forEach(token => assert.ok(app.includes(token), token));

assert.match(app, /function init\(\) \{[\s\S]*syncUserKeysFromServer\(\);/);
assert.match(app, /async function ocrImageData\(dataUrl\) \{[\s\S]*await ensureKeysLoaded\(\);/);
assert.ok(!app.includes('Ảnh vùng chữ ký cần Mistral OCR'), 'clipboard image must not require Mistral only');

console.log('vanban-ocr-clipboard-smoke: PASS');
