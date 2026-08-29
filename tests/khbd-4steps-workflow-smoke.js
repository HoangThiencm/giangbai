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
assert.match(html, /id="dropzoneContainer"[\s\S]{0,900}id="btnAnalyzeVision"/, "Nút Đọc SGK phải nằm ngay dưới dropzone");
assert.match(html, /id="btnAnalyzeVision"[\s\S]*?Đọc sách giáo khoa/, "Nút OCR phải có nhãn 'Đọc sách giáo khoa'");
assert.match(html, /id="dropzoneContainerPpct"[\s\S]{0,1400}id="btnAnalyzePpct"/, "Nút Đọc PPCT phải nằm ngay dưới dropzone PPCT");
assert.match(html, /id="btnAnalyzePpct"[\s\S]*?Đọc PPCT/, "Nút PPCT phải có nhãn 'Đọc PPCT'");
assert.match(html, /id="btnStep3PedagogyDigital"[\s\S]*?ĐỀ XUẤT PPDH, KỸ THUẬT &amp; NĂNG LỰC SỐ \(TT 02\)/, "Card Bước 3 phải có nút đề xuất PPDH & NLS TT 02");
assert.match(html, /id="lessonAiCompetencyCard"/, "Phải có card Năng lực AI độc lập");
assert.match(html, /id="btnStartComposeFromStep4"/, "Bước 4 phải có nút Bắt đầu soạn");
assert.match(html, /id="toggleDigitalCompetency"\s+checked/, "Năng lực số phải checked mặc định");
assert.doesNotMatch(html, /id="toggleAiCompetency"\s+checked/, "Năng lực AI mặc định không checked");
assert.doesNotMatch(html, /data-integration-tab="digital"/, "NLS không còn gộp trong tab tích hợp chung với AI");
assert.doesNotMatch(html, /data-integration-tab="ai"/, "AI không còn gộp trong tab tích hợp chung với NLS");
assert.match(html, /dropzone-active-hint/, "Dropzone phải có gợi ý vùng đang chọn");
assert.match(html, /id="dropzoneContainerPpct"[\s\S]*?tabindex="0"/, "Vùng PPCT phải focus được");

const tab0Subtabs = [
  "tab0-sub-materials",
  "tab0-sub-lesson-info",
  "tab0-sub-pedagogy-digital",
  "tab0-sub-ai-competency",
  "tab0-sub-language-inclusive"
];
assert.match(html, /class="tab0-subtabs-nav"/, "Tab 0 phải có thanh điều hướng 5 tab con");
tab0Subtabs.forEach(id => {
  assert.match(html, new RegExp(`data-tab0-sub="${id}"`), `Phải có nút tab con ${id}`);
  assert.match(html, new RegExp(`id="${id}" class="tab0-subtab-pane`), `Phải có pane ${id}`);
});
assert.match(
  html,
  /id="tab0-sub-materials"[\s\S]*?id="lessonTextbookAnalysis"[\s\S]*?id="lessonPpctAnalysis"[\s\S]*?id="lessonIllustrationCard"/,
  "Tab con 1 phải chứa SGK, PPCT và card hình minh họa"
);
assert.match(
  html,
  /id="tab0-sub-lesson-info"[\s\S]*?id="btnAutoDetectMetadata"[\s\S]*?id="inputSchool"[\s\S]*?id="inputTopicCustom"[\s\S]*?class="class-profile-choice"/,
  "Tab con 2 phải chứa thông tin bài dạy, lớp và đề xuất thông tin"
);
assert.match(
  html,
  /id="tab0-sub-pedagogy-digital"[\s\S]*?id="btnStep3PedagogyDigital"[\s\S]*?id="digitalStandardsPanel"[\s\S]*?id="subjectIntegrationsPanel"/,
  "Tab con 3 phải chứa PPDH, NLS và tích hợp môn"
);
assert.match(
  html,
  /id="tab0-sub-ai-competency"[\s\S]*?id="toggleAiCompetency"[\s\S]*?id="aiStandardsPanel"/,
  "Tab con 4 phải chứa khung Năng lực AI độc lập"
);
assert.match(
  html,
  /id="tab0-sub-language-inclusive"[\s\S]*?id="toggleForeignLanguage"[\s\S]*?id="toggleInclusiveSupport"[\s\S]*?class="support-choice"/,
  "Tab con 5 phải chứa Ngoại ngữ, Hòa nhập và Hỗ trợ chức năng"
);

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
assert.match(appCode, /function applyTimeBudgetGateToPedagogy/, "Phải có Time-Budget Gate cho bài 1 tiết");
assert.match(appCode, /tps-tech/, "Bài 1 tiết ưu tiên Think-Pair-Share");
assert.match(appCode, /TIME-BUDGET GATE/, "Bối cảnh sư phạm phải có Time-Budget Gate");
assert.match(appCode, /FACILITY GATE/, "Bối cảnh sư phạm phải có Facility Gate");
assert.match(appCode, /ensurePedagogyFromLesson\(\{ force: true/, "Bước 3 force chọn PPDH/kỹ thuật 4 pha");
assert.match(appCode, /requestStructuredIntegrationCandidates\("digital"/, "Bước 3 đề xuất NLS, không phải AI");
assert.match(appCode, /kind === "digital" && records\.length < 2/, "NLS không được để dưới 2 mục; phải fallback 2-3");
assert.match(appCode, /items\.some\(entry => selectedIds\.has\(entry\.id\)\) \? " open"/, "Nhóm NLS có mục được tick phải tự mở");
assert.match(appCode, /if \(kind === "digital"\) \{\s*if \(next\.length < 2\)/, "applySuggestedStandardRecords không được ghi NLS rỗng");
assert.match(appCode, /key === "ai"[\s\S]*requestStructuredIntegrationCandidates\("ai"/, "Bật Năng lực AI mới gọi Gemini AI");
assert.match(appCode, /Hãy đọc SGK ở Bước 1\. Khi có nội dung, Gemini sẽ đề xuất đúng 2–3 mục AI/, "Khi bật AI chưa có OCR phải hướng dẫn đọc SGK");
assert.match(appCode, /digital:\s*(?:context\?\.integrations\?\.digital\s*!==\s*false|true)/, "normalizeTeachingContext phải giữ NLS mặc định bật");
assert.doesNotMatch(
  appCode,
  /function normalizeTeachingContext[\s\S]{0,2200}catalogFallbackRecords\("digital"/,
  "Không tự seed NLS khi mới mở trang"
);
assert.match(appCode, /function switchTab0Subtab\(subtabKey\)/, "Phải có hàm chuyển tab con Tab 0");
assert.match(appCode, /TAB0_STEP_TO_SUBTAB/, "Stepper phải map bước 1–4 sang tab con");
assert.match(appCode, /data-tab0-sub/, "Nút tab con phải gắn sự kiện data-tab0-sub");
assert.match(
  appCode,
  /revealTab0WorkflowStep\(step\.getAttribute\("data-step"\)\)/,
  "Bấm stepper phải nhảy đúng tab con"
);
assert.match(
  appCode,
  /switchTab0Subtab\("tab0-sub-pedagogy-digital"\)/,
  "Nút đề xuất Bước 3 phải mở tab con PPDH & NLS"
);
assert.match(
  appCode,
  /switchTab0Subtab\("tab0-sub-materials"\)/,
  "Ctrl+V / nạp PDF phải mở tab con gửi file SGK/PPCT"
);

console.log("✓ Logic JS 4 bước độc lập hoạt động chuẩn xác.");

console.log("\n[TEST 3] Khung mã NLS (CV 3456) và AI (QĐ 2422)...");

const { KHBD_STANDARDS, entriesForGrade, recommendOfficialStandards, detectLessonMathBranch } = require("../js/khbd-standards.js");

assert.strictEqual(KHBD_STANDARDS.digital.framework, "Thông tư 02/2025/TT-BGDĐT & Công văn 3456/BGDĐT-GDPT", "Framework NLS phải ghi rõ TT 02 & CV 3456");
assert.strictEqual(KHBD_STANDARDS.digital.minSelect, 2, "NLS minSelect phải là 2");
assert.strictEqual(KHBD_STANDARDS.digital.maxSelect, 3, "NLS maxSelect phải là 3");

[6, 7, 8, 9].forEach(grade => {
  const rec = recommendOfficialStandards("digital", { grade, vision: "", topic: "Bài học" });
  assert.ok(rec.length >= 2 && rec.length <= 3, `NLS lớp ${grade} phải luôn 2–3 mục, nhận ${rec.length}`);
  const expectTc = grade <= 7 ? /TC1a$/ : /TC2a$/;
  assert.ok(rec.every(item => expectTc.test(String(item.officialCode || ""))), `NLS lớp ${grade} phải đúng dải TC1a/TC2a`);
});

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

console.log("\n[TEST 3b] Bộ lọc chống khiên cưỡng theo dạng bài...");

assert.strictEqual(detectLessonMathBranch("Góc ở vị trí đặc biệt", "Hai đường thẳng song song, góc đồng vị."), "geometry");
assert.strictEqual(detectLessonMathBranch("Phương trình bậc nhất một ẩn", "Giải phương trình đại số."), "algebra");
assert.strictEqual(detectLessonMathBranch("Thống kê", "Bảng tần suất và biểu đồ."), "statistics");

const geoRec = recommendOfficialStandards("digital", {
  grade: 6,
  topic: "Góc ở vị trí đặc biệt",
  vision: "Hai đường thẳng song song. Góc đồng vị, góc so le trong.",
  facilities: {}
});
assert.ok(geoRec.length >= 2 && geoRec.length <= 3, `Hình học phải 2–3 mục NLS, nhận ${geoRec.length}`);
assert.ok(geoRec.every(item => !/^3\.[34]/.test(String(item.officialCode || ""))), "Bài Hình học không được đề xuất Lập trình 3.4 hay Bản quyền 3.3");

const algRec = recommendOfficialStandards("digital", {
  grade: 6,
  topic: "Phương trình bậc nhất",
  vision: "Giải phương trình đại số trên tập số tự nhiên.",
  facilities: {}
});
assert.ok(algRec.every(item => !/^4\.2/.test(String(item.officialCode || ""))), "Bài Đại số không được gán Bảo vệ dữ liệu cá nhân 4.2");

const app = require("../js/khbd-app.js");
app.appState.duration = "01 tiết (45 phút)";
app.appState.selectedGrade = "6";
const gated = app.applyTimeBudgetGateToPedagogy({
  methods: ["pbl", "cooperative"],
  techniques: { A: ["kwl-tech"], B: ["jigsaw-tech", "tablecloth", "tps-tech"], C: ["station"], D: ["mini-project"] }
});
assert.strictEqual(gated.techniques.B.length, 1, "Bài 1 tiết chỉ 1 kỹ thuật pha B");
assert.ok(["tps-tech", "tablecloth"].includes(gated.techniques.B[0]), "Pha B 1 tiết phải là kỹ thuật nhẹ");
assert.ok(!gated.methods.includes("pbl"), "Bài 1 tiết không đề xuất dạy học dự án");

console.log("✓ Bộ lọc dạng bài, Time-Budget và Facility Gate đạt.");

console.log("\n[TEST 4] Prompt engineering NLS & AI...");

assert.match(promptsCode, /3456\/BGDĐT-GDPT/, "Prompt phải dẫn chiếu Công văn 3456/BGDĐT-GDPT");
assert.match(promptsCode, /2422\/QĐ-BGDĐT/, "Prompt phải dẫn chiếu Quyết định 2422/QĐ-BGDĐT");
assert.match(promptsCode, /Trung cấp 1 \(TC1/, "Prompt phải ghi rõ Lớp 6-7 dùng TC1");
assert.match(promptsCode, /Trung cấp 2 \(TC2/, "Prompt phải ghi rõ Lớp 8-9 dùng TC2");
assert.match(promptsCode, /NATURAL_INTEGRATION_GATE/, "Phải có khối prompt chống khiên cưỡng");
assert.match(promptsCode, /CẤM TUYỆT ĐỐI mã Lập trình \(3\.4\)/, "Prompt cấm Lập trình trong bài Hình học");
assert.match(promptsCode, /TIME-BUDGET GATE/, "Prompt phải có Time-Budget Gate");
assert.match(promptsCode, /FACILITY GATE/, "Prompt phải có Facility Gate");
assert.match(promptsCode, /GENERATE_OBJECTIVES[\s\S]*NATURAL_INTEGRATION_GATE|NATURAL_INTEGRATION_GATE[\s\S]*GENERATE_ACTIVITY_A/, "Cổng chống khiên cưỡng được gắn vào prompt soạn bài");

console.log("✓ Prompt Engineering tích hợp đầy đủ quy tắc kiểm tra mã.");

console.log("\n================================================================================");
console.log("🎉 TẤT CẢ CÁC BÀI KIỂM THỬ 4 BƯỚC & CHUẨN MÃ ĐÃ PASS 100%!");
console.log("================================================================================");
