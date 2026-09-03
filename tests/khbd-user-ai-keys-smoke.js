const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const gemini = fs.readFileSync(path.join(root, "js", "khbd-gemini.js"), "utf8");
const app = fs.readFileSync(path.join(root, "js", "khbd-app.js"), "utf8");
const api = fs.readFileSync(path.join(root, "api", "user_gemini_keys.php"), "utf8");
const helpers = fs.readFileSync(path.join(root, "api", "helpers.php"), "utf8");
const schema = fs.readFileSync(path.join(root, "database_schema.sql"), "utf8");
const login = fs.readFileSync(path.join(root, "login.html"), "utf8");
const access = fs.readFileSync(path.join(root, "access-control.js"), "utf8");
const designConfig = fs.readFileSync(path.join(root, "ai-design-config.js"), "utf8");
const indexHtml = fs.readFileSync(path.join(root, "index.html"), "utf8");
const runtime = fs.readFileSync(path.join(root, "api", "ai_runtime_config.php"), "utf8");
const hf = fs.readFileSync(path.join(root, "api", "hf_fallback.php"), "utf8");

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

assert.match(api, /session_status\(\) === PHP_SESSION_NONE/, "session_start phải an toàn, không gọi trùng");
assert.match(api, /'keys'\s*=>\s*\$gemini\['keys'\]/, "GET payload trả keys Gemini plain");
assert.match(api, /'mistral_keys'\s*=>\s*\$mistral\['keys'\]/, "GET payload trả mistral_keys plain");
assert.match(api, /masked_keys/, "Giữ masked_keys cho duyetde.html");
assert.match(api, /array_key_exists\('gemini_keys'/, "POST nhận alias gemini_keys");
assert.match(api, /looks_like_masked_api_key/, "Nhận diện masked key khi client submit lại");
assert.match(api, /mask_user_api_key\(\$realKey\) === \$trimmed/, "Khôi phục key thật từ DB khi gặp mask");
assert.match(api, /'keys'\s*=>\s*\[\]/, "DELETE trả keys rỗng");
assert.match(api, /'mistral_keys'\s*=>\s*\[\]/, "DELETE trả mistral_keys rỗng");

assert.match(access, /localStorage\.setItem\('global_gemini_keys'/, "access-control đồng bộ global_gemini_keys");
assert.match(access, /localStorage\.setItem\('global_mistral_keys'/, "access-control đồng bộ global_mistral_keys");
assert.match(access, /user\.gemini_keys\.length > 0/, "Chỉ ghi global Gemini khi user có key");
assert.match(access, /user\.mistral_keys\.length > 0/, "Chỉ ghi global Mistral khi user có key");

const loginGlobalGemini = login.match(/localStorage\.setItem\('global_gemini_keys'/g) || [];
const loginGlobalMistral = login.match(/localStorage\.setItem\('global_mistral_keys'/g) || [];
assert.strictEqual(loginGlobalGemini.length, 2, "login.html ghi global_gemini_keys ở cả 2 luồng");
assert.strictEqual(loginGlobalMistral.length, 2, "login.html ghi global_mistral_keys ở cả 2 luồng");

assert.match(designConfig, /cfg\.gemini_keys\.filter\(Boolean\)\.length > 0/, "ai-design-config không ghi đè global_gemini_keys bằng mảng rỗng");
assert.match(designConfig, /cfg\.mistral_keys\.filter\(Boolean\)\.length > 0/, "ai-design-config không ghi đè global_mistral_keys bằng mảng rỗng");
assert.match(indexHtml, /config\.gemini_keys\.filter\(Boolean\)\.length > 0/, "index.html không ghi đè global_gemini_keys bằng mảng rỗng");
assert.match(indexHtml, /config\.mistral_keys\.filter\(Boolean\)\.length > 0/, "index.html không ghi đè global_mistral_keys bằng mảng rỗng");

assert.match(runtime, /\$_SESSION\['user_id'\]/, "ai_runtime_config nạp key theo session user");
assert.match(runtime, /SELECT gemini_keys FROM users WHERE id = \?/, "ai_runtime_config đọc gemini_keys từ bảng users");
assert.match(runtime, /parse_stored_api_keys/, "ai_runtime_config giải mã key user qua parse_stored_api_keys");

assert.match(hf, /function hf_load_gemini_keys/, "hf_fallback có hf_load_gemini_keys");
assert.match(hf, /\$_SESSION\['user_id'\]/, "hf_load_gemini_keys nạp key theo session user");
assert.match(hf, /SELECT gemini_keys FROM users WHERE id = \?/, "hf_fallback đọc gemini_keys từ bảng users");
assert.match(hf, /hf_parse_user_stored_keys|parse_stored_api_keys/, "hf_fallback giải mã key user từ CSDL");

assert.match(gemini, /persistGlobalKeys/, "khbd-gemini đồng bộ global_gemini_keys / global_mistral_keys");
assert.match(gemini, /localStorage\.setItem\('global_gemini_keys'/, "sync/save Gemini ghi global_gemini_keys");
assert.match(gemini, /localStorage\.setItem\('global_mistral_keys'/, "sync/save Mistral ghi global_mistral_keys");
assert.match(gemini, /saved_to_db/, "Phân biệt lưu CSDL vs offline");
assert.match(gemini, /not_logged_in/, "Nhận diện chưa đăng nhập khi POST 401");

assert.match(app, /if \(mistralRaw !== ""\)/, "Không gửi mistral_keys rỗng khi chỉ lưu Gemini");
assert.match(app, /Đăng nhập để lưu lên CSDL/, "Toast báo rõ khi chưa đăng nhập / lưu offline");
assert.match(app, /result && result\.saved_to_db/, "Toast phân biệt lưu CSDL vs trên máy");

console.log("khbd user AI keys smoke: passed");
