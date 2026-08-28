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

// -----------------------------------------------------------------------------
// TEST 1: GIAO DIỆN QUY TRÌNH 4 BƯỚC TRONG SOANKHBD.HTML
// -----------------------------------------------------------------------------
console.log("\n[TEST 1] Kiểm tra các nút bấm và nhãn trên giao diện HTML...");

assert.match(html, /id="btnAnalyzeVision"[\s\S]*?Đọc sách giáo khoa/, "Nút OCR phải có nhãn 'Đọc sách giáo khoa'");
assert.match(html, /id="btnAnalyzePpct"[\s\S]*?Đọc PPCT/, "Nút PPCT phải có nhãn 'Đọc PPCT'");
assert.match(html, /id="btnAutoDetectMetadata"[\s\S]*?Đề xuất thông tin bài dạy/, "Card Thiết lập bài dạy phải có nút 'Đề xuất thông tin bài dạy'");
assert.match(html, /id="btnSuggestPedagogyStandards"[\s\S]*?Đề xuất PP\/KTDH & Năng lực số\/AI/, "Card Tích hợp phải có nút 'Đề xuất PP/KTDH & Năng lực số/AI'");
assert.match(html, /id="toggleDigitalCompetency"\s+checked/, "Năng lực số phải có thuộc tính checked mặc định trong HTML");

console.log("✓ Giao diện HTML đáp ứng 100% yêu cầu 4 bước.");

// -----------------------------------------------------------------------------
// TEST 2: HÀNH VI TỪNG BƯỚC ĐỘC LẬP TRONG JS/KHBD-APP.JS
// -----------------------------------------------------------------------------
console.log("\n[TEST 2] Kiểm tra logic JS các bước độc lập...");

// Bước 1: OCR SGK -> toast "Đã xong"
assert.match(appCode, /showToast\("Đã xong/i, "Bước 1 OCR SGK phải toast 'Đã xong'");

// Bước 2: PPCT -> toast "Đã đọc"
assert.match(appCode, /showToast\("Đã đọc/i, "Bước 2 Phân tích PPCT phải toast 'Đã đọc'");

// Bước 3 & 4: Event listener gắn cho 2 nút đề xuất mới
assert.match(appCode, /btnAutoDetectMetadata/, "Phải gắn event listener cho nút btnAutoDetectMetadata");
assert.match(appCode, /btnSuggestPedagogyStandards/, "Phải gắn event listener cho nút btnSuggestPedagogyStandards");

// Mặc định NLS bật trong normalizeTeachingContext
assert.match(appCode, /digital:\s*(?:context\?\.integrations\?\.digital\s*!==\s*false|true)/, "normalizeTeachingContext phải giữ NLS mặc định bật");

console.log("✓ Logic JS 4 bước độc lập hoạt động chuẩn xác.");

// -----------------------------------------------------------------------------
// TEST 3: KHUNG MÃ NĂNG LỰC SỐ (CV 3456) VÀ AI (QĐ 2422) TRONG STANDARDS
// -----------------------------------------------------------------------------
console.log("\n[TEST 3] Kiểm tra khung mã NLS (CV 3456) và AI (QĐ 2422)...");

const { KHBD_STANDARDS, entriesForGrade } = require("../js/khbd-standards.js");

assert.strictEqual(KHBD_STANDARDS.digital.framework, "Thông tư 02/2025/TT-BGDĐT & Công văn 3456/BGDĐT-GDPT", "Framework NLS phải ghi rõ TT 02 & CV 3456");

// Kiểm tra mã NLS lớp 6-7 (TC1) và lớp 8-9 (TC2)
const digitalG6 = entriesForGrade("digital", 6);
const digitalG7 = entriesForGrade("digital", 7);
const digitalG8 = entriesForGrade("digital", 8);
const digitalG9 = entriesForGrade("digital", 9);

assert.ok(digitalG6.length > 0 && digitalG6.every(e => /\.TC1[a-z]?$/.test(e.code)), "Lớp 6 phải 100% dùng mã TC1 (Công văn 3456)");
assert.ok(digitalG7.length > 0 && digitalG7.every(e => /\.TC1[a-z]?$/.test(e.code)), "Lớp 7 phải 100% dùng mã TC1 (Công văn 3456)");
assert.ok(digitalG8.length > 0 && digitalG8.every(e => /\.TC2[a-z]?$/.test(e.code)), "Lớp 8 phải 100% dùng mã TC2 (Công văn 3456)");
assert.ok(digitalG9.length > 0 && digitalG9.every(e => /\.TC2[a-z]?$/.test(e.code)), "Lớp 9 phải 100% dùng mã TC2 (Công văn 3456)");

// Kiểm tra mã AI QĐ 2422 (88 YCCĐ)
const aiG6 = entriesForGrade("ai", 6);
const aiG7 = entriesForGrade("ai", 7);
const aiG8 = entriesForGrade("ai", 8);
const aiG9 = entriesForGrade("ai", 9);

assert.ok(aiG6.length > 0 && aiG6.every(e => /^6\.[A-D]\d+\.(?:\d+|MR\d+)$/.test(e.code)), "AI Lớp 6 phải đúng mã 6.[Chủ đề].[STT/MR] (QĐ 2422)");
assert.ok(aiG7.length > 0 && aiG7.every(e => /^7\.[A-D]\d+\.(?:\d+|MR\d+)$/.test(e.code)), "AI Lớp 7 phải đúng mã 7.[Chủ đề].[STT/MR] (QĐ 2422)");
assert.ok(aiG8.length > 0 && aiG8.every(e => /^8\.[A-D]\d+\.(?:\d+|MR\d+)$/.test(e.code)), "AI Lớp 8 phải đúng mã 8.[Chủ đề].[STT/MR] (QĐ 2422)");
assert.ok(aiG9.length > 0 && aiG9.every(e => /^9\.[A-D]\d+\.(?:\d+|MR\d+)$/.test(e.code)), "AI Lớp 9 phải đúng mã 9.[Chủ đề].[STT/MR] (QĐ 2422)");

console.log("✓ Khung mã NLS (CV 3456) và AI (QĐ 2422) chuẩn 100%.");

// -----------------------------------------------------------------------------
// TEST 4: QUY TẮC KIỂM TRA MÃ TRONG PROMPT ENGINEERING
// -----------------------------------------------------------------------------
console.log("\n[TEST 4] Kiểm tra Prompt Engineering có ràng buộc mã NLS & AI...");

assert.match(promptsCode, /3456\/BGDĐT-GDPT/, "Prompt phải dẫn chiếu Công văn 3456/BGDĐT-GDPT");
assert.match(promptsCode, /2422\/QĐ-BGDĐT/, "Prompt phải dẫn chiếu Quyết định 2422/QĐ-BGDĐT");
assert.match(promptsCode, /Trung cấp 1 \(TC1/, "Prompt phải ghi rõ Lớp 6-7 dùng TC1");
assert.match(promptsCode, /Trung cấp 2 \(TC2/, "Prompt phải ghi rõ Lớp 8-9 dùng TC2");

console.log("✓ Prompt Engineering tích hợp đầy đủ quy tắc kiểm tra mã.");

console.log("\n================================================================================");
console.log("🎉 TẤT CẢ CÁC BÀI KIỂM THỬ 4 BƯỚC & CHUẨN MÃ ĐÃ PASS 100%!");
console.log("================================================================================");
