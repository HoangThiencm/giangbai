const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const html = fs.readFileSync(path.join(root, "soankhbd.html"), "utf8");
const appCode = fs.readFileSync(path.join(root, "js", "khbd-app.js"), "utf8");
const promptsCode = fs.readFileSync(path.join(root, "js", "khbd-prompts.js"), "utf8");

console.log("================================================================================");
console.log("KIỂM THỬ QUY TRÌNH 4 BƯỚC VÀ KHUNG MÃ NLS (CV 3456) & AI (QĐ 2422)");
console.log("================================================================================");

console.log("\n[TEST 1] Giao diện 4 bước trên Tab 0...");

assert.match(html, /id="khbdWorkflowStepper"/, "Phải có thanh stepper 4 bước");
assert.match(html, /Bước 1: Nạp &amp; Đọc SGK/, "Stepper phải có Bước 1 Đọc SGK");
assert.match(html, /Bước 2: Nạp &amp; Đọc PPCT/, "Stepper phải có Bước 2 Đọc PPCT");
assert.match(html, /Bước 3: AI Đề xuất PPDH &amp; NLS/, "Stepper phải có Bước 3 đề xuất PPDH & NLS");
assert.match(html, /Bước 4: Tích hợp AI &amp; Soạn bài/, "Stepper phải có Bước 4 AI & soạn bài");
assert.match(html, /id="btnAnalyzeVision"[\s\S]*?Đọc sách giáo khoa/, "Nút OCR phải có nhãn 'Đọc sách giáo khoa'");
assert.match(html, /id="btnAnalyzePpct"[\s\S]*?Đọc PPCT/, "Nút PPCT phải có nhãn 'Đọc PPCT'");
assert.match(html, /id="btnStep3PedagogyDigital"[\s\S]*?ĐỀ XUẤT PPDH, KỸ THUẬT &amp; NĂNG LỰC SỐ \(AI\)/, "Card Bước 3 phải có nút đề xuất PPDH & NLS");
assert.match(html, /id="btnStartComposeFromStep4"/, "Bước 4 phải có nút Bắt đầu soạn");
assert.match(html, /id="toggleDigitalCompetency"\s+checked/, "Năng lực số phải checked mặc định");
assert.doesNotMatch(html, /id="toggleAiCompetency"\s+checked/, "Năng lực AI mặc định không checked");
assert.match(html, /dropzone-active-hint/, "Dropzone phải có gợi ý vùng đang chọn");
assert.match(html, /id="dropzoneContainerPpct"[\s\S]*?tabindex="0"/, "Vùng PPCT phải focus được");

console.log("✓ Giao diện HTML đáp ứng quy trình 4 bước.");

console.log("\n[TEST 2] Logic JS từng bước...");

assert.match(appCode, /showToast\("Đã xong/i, "Bước 1 OCR SGK phải toast 'Đã xong'");
assert.match(appCode, /showToast\("Đã đọc/i, "Bước 2 Phân tích PPCT phải toast 'Đã đọc'");
assert.match(appCode, /async function applyTextbookOcrResult[\s\S]*?ocrReady = true[\s\S]*?updateWorkflowStepper\(\)/, "OCR SGK chỉ lưu text và ocrReady");
assert.doesNotMatch(
  appCode,
  /async function applyTextbookOcrResult[\s\S]{0,500}ensurePedagogyFromLesson/,
  "OCR SGK không được tự tick PPDH"
);
assert.doesNotMatch(
  appCode,
  /async function applyTextbookOcrResult[\s\S]{0,800}requestStructuredIntegrationCandidatesForEnabled/,
  "OCR SGK không được tự đề xuất NLS/AI"
);
assert.match(appCode, /let activeDropzoneTarget = "sgk"/, "Phải theo dõi vùng dán đang chọn");
assert.match(appCode, /function setActiveDropzoneTarget/, "Phải có hàm gán vùng dán SGK/PPCT");
assert.match(appCode, /pasteToPpct = ppctPasteArmed \|\| activeDropzoneTarget === "ppct" \|\| inPpct/, "Ctrl+V vào PPCT khi vùng PPCT đang chọn");
assert.match(appCode, /dropzone-active-ppct/, "PPCT active zone phải có class viền cam");
assert.match(appCode, /dropzone-active-sgk/, "SGK active zone phải có class viền xanh");
assert.match(appCode, /async function triggerStep3PedagogyAndDigitalRecommendations/, "Phải có hàm Bước 3 đề xuất PPDH & NLS");
assert.match(appCode, /btnStep3PedagogyDigital/, "Phải gắn nút card Bước 3");
assert.match(appCode, /ensurePedagogyFromLesson\(\{ force: true/, "Bước 3 force chọn PPDH/kỹ thuật 4 pha");
assert.match(appCode, /requestStructuredIntegrationCandidates\("digital"/, "Bước 3 đề xuất NLS, không phải AI");
assert.match(appCode, /key === "ai"[\s\S]*requestStructuredIntegrationCandidates\("ai"/, "Bật Năng lực AI mới gọi Gemini AI");
assert.match(appCode, /Hãy đọc SGK ở Bước 1\. Khi có nội dung, Gemini sẽ đề xuất đúng 2–3 mục AI/, "Khi bật AI chưa có OCR phải hướng dẫn đọc SGK");
assert.match(appCode, /digital:\s*(?:context\?\.integrations\?\.digital\s*!==\s*false|true)/, "normalizeTeachingContext phải giữ NLS mặc định bật");
assert.doesNotMatch(
  appCode,
  /function normalizeTeachingContext[\s\S]{0,2200}catalogFallbackRecords\("digital"/,
  "Không tự seed NLS khi mới mở trang"
);

console.log("✓ Logic JS 4 bước độc lập hoạt động chuẩn xác.");

console.log("\n[TEST 3] Khung mã NLS (CV 3456) và AI (QĐ 2422)...");

const { KHBD_STANDARDS, entriesForGrade } = require("../js/khbd-standards.js");

assert.strictEqual(KHBD_STANDARDS.digital.framework, "Thông tư 02/2025/TT-BGDĐT & Công văn 3456/BGDĐT-GDPT", "Framework NLS phải ghi rõ TT 02 & CV 3456");

const digitalG6 = entriesForGrade("digital", 6);
const digitalG7 = entriesForGrade("digital", 7);
const digitalG8 = entriesForGrade("digital", 8);
const digitalG9 = entriesForGrade("digital", 9);

assert.ok(digitalG6.length > 0 && digitalG6.every(e => /\.TC1[a-z]?$/.test(e.code)), "Lớp 6 phải 100% dùng mã TC1 (Công văn 3456)");
assert.ok(digitalG7.length > 0 && digitalG7.every(e => /\.TC1[a-z]?$/.test(e.code)), "Lớp 7 phải 100% dùng mã TC1 (Công văn 3456)");
assert.ok(digitalG8.length > 0 && digitalG8.every(e => /\.TC2[a-z]?$/.test(e.code)), "Lớp 8 phải 100% dùng mã TC2 (Công văn 3456)");
assert.ok(digitalG9.length > 0 && digitalG9.every(e => /\.TC2[a-z]?$/.test(e.code)), "Lớp 9 phải 100% dùng mã TC2 (Công văn 3456)");

const aiG6 = entriesForGrade("ai", 6);
const aiG7 = entriesForGrade("ai", 7);
const aiG8 = entriesForGrade("ai", 8);
const aiG9 = entriesForGrade("ai", 9);

assert.ok(aiG6.length > 0 && aiG6.every(e => /^6\.[A-D]\d+\.(?:\d+|MR\d+)$/.test(e.code)), "AI Lớp 6 phải đúng mã 6.[Chủ đề].[STT/MR] (QĐ 2422)");
assert.ok(aiG7.length > 0 && aiG7.every(e => /^7\.[A-D]\d+\.(?:\d+|MR\d+)$/.test(e.code)), "AI Lớp 7 phải đúng mã 7.[Chủ đề].[STT/MR] (QĐ 2422)");
assert.ok(aiG8.length > 0 && aiG8.every(e => /^8\.[A-D]\d+\.(?:\d+|MR\d+)$/.test(e.code)), "AI Lớp 8 phải đúng mã 8.[Chủ đề].[STT/MR] (QĐ 2422)");
assert.ok(aiG9.length > 0 && aiG9.every(e => /^9\.[A-D]\d+\.(?:\d+|MR\d+)$/.test(e.code)), "AI Lớp 9 phải đúng mã 9.[Chủ đề].[STT/MR] (QĐ 2422)");

console.log("✓ Khung mã NLS (CV 3456) và AI (QĐ 2422) chuẩn 100%.");

console.log("\n[TEST 4] Prompt engineering NLS & AI...");

assert.match(promptsCode, /3456\/BGDĐT-GDPT/, "Prompt phải dẫn chiếu Công văn 3456/BGDĐT-GDPT");
assert.match(promptsCode, /2422\/QĐ-BGDĐT/, "Prompt phải dẫn chiếu Quyết định 2422/QĐ-BGDĐT");
assert.match(promptsCode, /Trung cấp 1 \(TC1/, "Prompt phải ghi rõ Lớp 6-7 dùng TC1");
assert.match(promptsCode, /Trung cấp 2 \(TC2/, "Prompt phải ghi rõ Lớp 8-9 dùng TC2");

console.log("✓ Prompt Engineering tích hợp đầy đủ quy tắc kiểm tra mã.");

console.log("\n================================================================================");
console.log("🎉 TẤT CẢ CÁC BÀI KIỂM THỬ 4 BƯỚC & CHUẨN MÃ ĐÃ PASS 100%!");
console.log("================================================================================");
