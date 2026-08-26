const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const gemini = fs.readFileSync(path.join(root, "js", "khbd-gemini.js"), "utf8");
const api = fs.readFileSync(path.join(root, "api", "user_gemini_keys.php"), "utf8");
const helpers = fs.readFileSync(path.join(root, "api", "helpers.php"), "utf8");
const schema = fs.readFileSync(path.join(root, "database_schema.sql"), "utf8");
const login = fs.readFileSync(path.join(root, "login.html"), "utf8");

assert.match(schema, /mistral_keys TEXT/, "users phải có cột mistral_keys");
assert.match(helpers, /function ensure_users_ai_key_columns/, "Cần migrate cột mistral_keys");
assert.match(helpers, /'mistral_keys' => parse_stored_api_keys/, "me/login trả mistral_keys của user");
assert.match(api, /mistral_keys/, "API user keys lưu Mistral lên CSDL");
assert.match(api, /array_key_exists\('mistral_keys'/, "POST có thể cập nhật mistral_keys độc lập");
assert.match(gemini, /getMistralStorageKey/, "Gemini manager lưu Mistral theo userEmail");
assert.match(gemini, /khbd_user_mistral_keys_/, "Local cache Mistral theo tài khoản");
assert.match(gemini, /saveUserAiKeysToServer/, "Lưu Gemini + Mistral lên CSDL cùng lúc");
assert.match(gemini, /async testMistralApiKey/, "Có kiểm tra Mistral key");
assert.match(login, /khbd_user_mistral_keys_/, "Login nạp Mistral key user vào localStorage");

const geminiProxy = fs.readFileSync(path.join(root, "api", "khbd_gemini.php"), "utf8");
assert.match(geminiProxy, /generativelanguage\.googleapis\.com/, "Proxy máy chủ gọi Gemini");
assert.match(gemini, /fetchViaKhbdProxy/, "Trình duyệt fallback proxy khi không tới Google");
assert.match(gemini, /fetchWithTimeout/, "Không để fetch Gemini treo vô hạn");

console.log("khbd user AI keys smoke: passed");
