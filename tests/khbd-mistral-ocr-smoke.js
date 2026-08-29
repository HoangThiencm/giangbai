const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const client = fs.readFileSync(path.join(root, "mistral-ocr-client.js"), "utf8");
const app = fs.readFileSync(path.join(root, "js", "khbd-app.js"), "utf8");
const html = fs.readFileSync(path.join(root, "soankhbd.html"), "utf8");

assert.match(client, /include_image_base64:\s*false/, "OCR KHBD không kéo ảnh base64 thừa");
assert.match(client, /function isReady/, "MistralOcr.isReady để soankhbd kiểm tra key");
assert.match(client, /opts\.module \|\| 'thitructuyen'/, "Giữ module mặc định thi trực tuyến");
assert.match(client, /moduleName/, "Cho phép ghi log module soankhbd");
assert.match(html, /mistral-ocr-client\.js/, "soankhbd nạp mistral-ocr-client");
assert.match(html, /ai-usage-reporter\.js/, "soankhbd nạp usage reporter cho OCR");
assert.match(app, /module:\s*"soankhbd"/, "OCR KHBD ghi log đúng module");
assert.match(app, /async function extractTextbookOcrText/, "Có hàm nhận diện SGK bằng Mistral");
assert.match(app, /canUseMistralOcr\(\)/, "Nút đọc SGK ưu tiên Mistral");
assert.match(app, /function getUserMistralKeys/, "OCR dùng Mistral key của user");
assert.match(app, /global_mistral_keys/, "OCR đọc thêm key Mistral global");
assert.match(app, /AiDesignConfig\.getMistralKeys/, "OCR đọc thêm key từ AiDesignConfig");
assert.match(app, /MistralOcr\.getKeys/, "OCR đọc thêm key từ MistralOcr");
assert.match(app, /if \(hasSgkMedia\) await readTextbookWithMistral\(\)/, "Phân tích SGK bắt buộc đi Mistral OCR trước");
assert.match(app, /ocrDocument\(part\.dataUrl, mistralKeys/, "OCR PDF truyền key Mistral của user");
assert.match(html, /id="textareaMistralKeys"/, "Modal API Key có ô nhập Mistral");
assert.match(html, /dùng Mistral OCR/, "Modal giải thích Mistral đọc SGK");
assert.doesNotMatch(html, /Đọc nội dung SGK \(Gemini\)/, "Không còn nhãn Gemini trên nút đọc SGK");
assert.match(app, /Đang nhận diện SGK bằng Mistral OCR/, "Ưu tiên hiển thị tiến trình Mistral OCR");
assert.match(app, /async function extractPpctOcrText/, "Có hàm nhận diện PPCT bằng Mistral");
assert.match(app, /Đang nhận diện PPCT bằng Mistral OCR/, "Đọc PPCT ưu tiên Mistral OCR");
assert.match(app, /await extractPpctOcrText\(/, "handleGeneratePpctAnalysis gọi Mistral OCR trước Gemini");

console.log("khbd mistral ocr smoke: passed");
