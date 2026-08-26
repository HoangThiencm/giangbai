const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const app = fs.readFileSync(path.join(root, "js", "khbd-app.js"), "utf8");
const html = fs.readFileSync(path.join(root, "soankhbd.html"), "utf8");

assert.match(app, /const VISION_BATCH_SIZE\s*=\s*4/, "Cần có batching nội bộ theo request");
assert.match(app, /function chunkVisionPages[\s\S]*?pages\.slice\(index, index \+ batchSize\)/, "Batch phải bao phủ lần lượt mọi trang");
assert.match(app, /async function analyzeTextbookInBatches[\s\S]*?chunkVisionPages\(appState\.images \|\| \[\]\)/, "Nút đọc SGK phải dùng batching");
assert.match(app, /analyzeTextbookInBatches\(promptVision/, "One-click phải dùng cùng batching");
assert.match(app, /compressDataUrl\(image\.dataUrl\)/, "Payload ảnh phải được nén trước khi gửi");
assert.doesNotMatch(app, /MAX_IMAGES|MAX_VISION_IMAGES|slice\(0, MAX_VISION_IMAGES\)/, "Không được giới hạn số ảnh/trang hoặc cắt trang đầu");
assert.match(app, /MAX_IMAGE_BYTES/, "Phải giữ chốt dung lượng từng tệp");
assert.match(app, /MAX_TOTAL_IMAGE_BYTES/, "Phải giữ chốt tổng dung lượng");
assert.match(html, /data-tab="tabVision"/, "Tab gộp phải dùng tabVision");
assert.doesNotMatch(html, /data-tab="tabConfig"/, "Không còn tab cấu hình riêng");
assert.match(html, /id="lessonTextbookAnalysis"/, "Kết quả phân tích SGK phải ở cùng tab thiết lập");

console.log("khbd vision batching smoke: passed");
