const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const indexHtml = fs.readFileSync(path.join(root, "index.html"), "utf8");
const settings = fs.readFileSync(path.join(root, "js", "user-ai-settings.js"), "utf8");

assert.match(indexHtml, /id="btnOpenUserAiSettings"/, "index.html phải có nút Cài đặt AI trên navbar");
assert.match(indexHtml, /onclick="UserAiSettings\.openModal\(\)"/, "nút Setting phải gọi UserAiSettings.openModal()");
assert.match(indexHtml, /Cài đặt AI & Key/, "nhãn nút Setting phải là Cài đặt AI & Key");
assert.match(indexHtml, /fa-sliders-h/, "nút Setting dùng icon sliders");
assert.match(indexHtml, /<script src="js\/user-ai-settings\.js"><\/script>/, "index.html nhúng js/user-ai-settings.js");
assert.match(indexHtml, /id="heroKeyStatus"/, "hero giáo viên có badge trạng thái API Key");
assert.ok(
    indexHtml.indexOf('<script src="js/user-ai-settings.js"></script>')
        < indexHtml.indexOf("(async function setupTeacherLotrinhHub"),
    "script user-ai-settings.js phải nằm trước script khởi tạo trang chủ"
);

assert.match(settings, /window\.UserAiSettings|global\.UserAiSettings/, "module gắn UserAiSettings ra window");
assert.match(settings, /ensureModal/, "có ensureModal");
assert.match(settings, /openModal/, "có openModal");
assert.match(settings, /closeModal/, "có closeModal");
assert.match(settings, /handleFile/, "có handleFile nạp file txt");
assert.match(settings, /testGeminiKeys/, "có testGeminiKeys");
assert.match(settings, /saveSettings/, "có saveSettings");
assert.match(settings, /deleteKeys/, "có deleteKeys");
assert.match(settings, /updateBadge/, "có updateBadge");
assert.match(settings, /userAiSettingsModal/, "modal #userAiSettingsModal");
assert.match(settings, /userAiGeminiKeys/, "textarea Gemini keys");
assert.match(settings, /userAiMistralKeys/, "textarea Mistral keys");
assert.match(settings, /userAiGeminiModel/, "dropdown module Gemini");
assert.match(settings, /default_gemini_module/, "lưu default_gemini_module");
assert.match(settings, /khbd_gemini_model/, "đồng bộ khbd_gemini_model");
assert.match(settings, /global_gemini_keys/, "đồng bộ global_gemini_keys");
assert.match(settings, /global_mistral_keys/, "đồng bộ global_mistral_keys");
assert.match(settings, /api\/user_gemini_keys\.php/, "gọi api/user_gemini_keys.php");
assert.match(settings, /action:\s*'test'/, "Kiểm tra Key gửi POST action=test");
assert.match(settings, /api\('DELETE'\)/, "gọi DELETE api/user_gemini_keys.php");
assert.match(settings, /gemini-2\.5-flash/, "dropdown có gemini-2.5-flash");
assert.match(settings, /gemini-3-flash-preview/, "dropdown có gemini-3-flash-preview");
assert.match(settings, /gemini-2\.5-pro/, "dropdown có gemini-2.5-pro");
assert.match(settings, /accept="\.txt,text\/plain"/, "nạp key từ file .txt");
assert.match(settings, /Đăng nhập lại/, "báo rõ khi hết phiên đăng nhập");
assert.match(settings, /heroKeyStatus/, "updateBadge cập nhật #heroKeyStatus");
assert.match(settings, /isStudent\(\)|userRole.*student/, "không hiện cài đặt AI cho học sinh");

console.log("user-ai-settings smoke: passed");
