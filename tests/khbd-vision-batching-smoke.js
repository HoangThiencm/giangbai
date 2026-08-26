const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const app = fs.readFileSync(path.join(root, "js", "khbd-app.js"), "utf8");
const html = fs.readFileSync(path.join(root, "soankhbd.html"), "utf8");
const prompts = fs.readFileSync(path.join(root, "js", "khbd-prompts.js"), "utf8");

assert.match(app, /pdfAttachments/, "Cần lưu PDF gốc trong appState.pdfAttachments");
assert.match(app, /async function prepareGeminiMedia/, "Cần prepareGeminiMedia cho payload Gemini");
assert.match(app, /async function buildPdfMediaPart/, "Cần cắt/gửi PDF native");
assert.match(app, /mimeType:\s*"application\/pdf"/, "Payload PDF phải là application/pdf");
assert.match(app, /compressDataUrl\(image\.dataUrl\)/, "Ảnh chụp/dán vẫn nén trước khi gửi");
assert.match(app, /function parseKhbdSections/, "1-click cần tách marker I/II/A–D");
assert.match(app, /getPromptTemplate\("GENERATE_CORE_LESSON"/, "1-click bước 1 là GENERATE_CORE_LESSON");
assert.match(app, /getPromptTemplate\("GENERATE_ACTIVITIES_AD"/, "1-click bước 2 là GENERATE_ACTIVITIES_AD");
assert.doesNotMatch(app, /analyzeTextbookInBatches\(promptVision/, "1-click không dump SGK theo đợt");
assert.doesNotMatch(app, /const VISION_BATCH_SIZE\s*=\s*4/, "Không còn batch JPEG 4 trang");
assert.doesNotMatch(app, /async function analyzeTextbookInBatches/, "Không còn analyzeTextbookInBatches");
assert.match(app, /images\.length \? images : await prepareGeminiMedia\(\)/, "executeAIGeneration đính prepareGeminiMedia");
assert.match(app, /repairWithGemini: false/, "1-click tắt repair Gemini extra");
assert.match(app, /MAX_IMAGE_BYTES/, "Phải giữ chốt dung lượng từng tệp");
assert.match(app, /MAX_TOTAL_IMAGE_BYTES/, "Phải giữ chốt tổng dung lượng");
assert.match(html, /data-tab="tabVision"/, "Tab gộp phải dùng tabVision");
assert.doesNotMatch(html, /data-tab="tabConfig"/, "Không còn tab cấu hình riêng");
assert.match(html, /id="lessonTextbookAnalysis"/, "Kết quả phân tích SGK phải ở cùng tab thiết lập");
assert.match(html, /pdf-lib@1\.17\.1/, "Cần pdf-lib để cắt trang PDF native");
assert.match(prompts, /GENERATE_CORE_LESSON/, "Cần prompt I+II gộp");
assert.match(prompts, /GENERATE_ACTIVITIES_AD/, "Cần prompt A–D gộp");
assert.doesNotMatch(prompts, /TRÍCH XUẤT ĐẦY ĐỦ, TRỌN VẸN TOÀN BỘ/, "ANALYZE_TEXTBOOK không dump toàn văn SGK");
assert.match(prompts, /CẤM trích nguyên văn toàn bộ SGK/, "ANALYZE_TEXTBOOK phải cấm dump nguyên văn");

console.log("khbd vision batching smoke: passed");
