const assert = require("assert");
const fs = require("fs");
const { entriesForGrade } = require("../js/khbd-standards.js");

const app = fs.readFileSync("js/khbd-app.js", "utf8");

assert.match(app, /function requestStructuredIntegrationCandidates\(/, "Phải có yêu cầu đề xuất có cấu trúc");
assert.match(app, /NỘI DUNG OCR SGK/, "Prompt phải lấy đúng nguồn OCR");
assert.match(app, /id catalog \(cột 1\) hoặc mã chính thức \(cột 2\)/, "Prompt phải cho phép id catalog hoặc mã chính thức");
assert.match(app, /lessonAnchor/, "JSON phải có neo SGK");
assert.match(app, /fitRationale/, "JSON phải có lý do phù hợp");
assert.match(app, /Không trả mảng rỗng khi danh mục còn mục có thể tích hợp/, "Prompt không được khuyến khích candidates rỗng");
assert.match(app, /source\.includes\(anchorText\)/, "Vẫn ưu tiên neo SGK xuất hiện trong OCR");
assert.match(app, /foldedAnchor\.length >= 12 && foldedSource\.includes\(foldedAnchor\)/, "Neo lệch dấu câu vẫn được ưu tiên nếu fold ≥ 12");
assert.match(app, /resolveCandidateEntry\(id, entries\)/, "Phải khớp id catalog hoặc mã chính thức");
assert.match(app, /catalogFallbackRecords\(/, "JSON rỗng phải fallback khung lớp");
assert.match(app, /current\.length && !current\.every\(item => item\.autoSuggested\)/, "Không được ghi đè lựa chọn thủ công");
assert.match(app, /hasOcrReadyLessonContent\(\)/, "Chỉ yêu cầu Gemini sau khi OCR sẵn sàng");
assert.match(app, /typeof geminiAPI !== "undefined"/, "Phải kiểm tra Gemini API toàn cục an toàn");
assert.doesNotMatch(app, /window\.geminiAPI/, "Không được phụ thuộc Gemini API là thuộc tính window");
assert.match(app, /const selectable = enabled;/, "Checkbox con chỉnh được khi bật tích hợp, không khóa vì thiếu OCR");
assert.match(app, /catalogFallbackRecords\("digital"/, "NLS phải tự nạp mục con theo lớp");
assert.match(app, /catalogFallbackRecords\("ai"/, "AI phải tự nạp mục con khi bật tích hợp");
assert.match(app, /typeof entriesForGrade === "function"/, "Phải lọc danh mục theo lớp/dải");

const ocrText = "Bài 1. Tập hợp. Cho tập hợp A = {1; 2; 3}. Hãy viết tập hợp B gồm các phần tử là số tự nhiên nhỏ hơn 4. Học sinh thảo luận và trình bày kết quả vào vở.";
const validTask = "GV cho HS đối chiếu kết quả AI với tập hợp A; HS nộp phiếu kiểm tra tập hợp.";
const validRationale = "Bài tập tập hợp tạo ngữ cảnh để học sinh kiểm tra kết quả.";

async function testGlobalGeminiWithoutWindow() {
  const saved = new Map();
  global.localStorage = { getItem: key => saved.get(key) || null, setItem: (key, value) => saved.set(key, value) };
  global.KHBD_STANDARDS = { ai: { framework: "AI", source: "test", date: "2026", maxSelect: 3, entries: [{ id: "ai-6", code: "6.A1.1", label: "AI", grades: [6] }] } };
  global.standardToRecord = (kind, entry, grade, autoSuggested) => ({ framework: "AI", catalogId: entry.id, officialCode: entry.code, grade, autoSuggested });
  global.getSystemRole = () => "test";
  let called = false;
  global.geminiAPI = { generateContent: async () => { called = true; return '{"candidates":[{"id":"ai-6","lessonAnchor":"Cho tập hợp A = {1; 2; 3}","fitRationale":"Bài tập tập hợp tạo ngữ cảnh để học sinh kiểm tra kết quả.","proposedTask":"GV cho HS đối chiếu kết quả AI với tập hợp A; HS nộp phiếu kiểm tra tập hợp."}]}'; } };
  delete global.window;
  const { appState, requestStructuredIntegrationCandidates } = require("../js/khbd-app.js");
  global.document = { getElementById: () => null, querySelectorAll: () => [] };
  appState.selectedGrade = "6";
  appState.content.vision = ocrText;
  appState.teachingContext = { integrations: { ai: true, digital: false }, ocrReady: true, standards: [] };
  const result = await requestStructuredIntegrationCandidates("ai", { silent: true });
  assert.strictEqual(result, true, "Global geminiAPI phải được gọi dù không có window.geminiAPI");
  assert.strictEqual(called, true, "Phải gọi global geminiAPI");
  assert.strictEqual(appState.teachingContext.standards[0].lessonAnchor, "Cho tập hợp A = {1; 2; 3}", "OCR Toán 6 không có từ AI vẫn chấp nhận neo bài tập thật");
}

async function testOfficialCodeAndProseJson() {
  const { appState, requestStructuredIntegrationCandidates, parseStructuredCandidates } = require("../js/khbd-app.js");
  const prose = `Kết quả phân tích:\n{"candidates":[{"id":"6.A1.1","lessonAnchor":"Cho tập hợp A = {1; 2; 3}","fitRationale":"${validRationale}","proposedTask":"${validTask}"}]}\nHết.`;
  const parsed = parseStructuredCandidates(prose, [{ id: "ai-6", code: "6.A1.1", label: "AI", grades: [6] }], ocrText, 3);
  assert.strictEqual(parsed.length, 1, "JSON bọc prose vẫn parse được");
  assert.strictEqual(parsed[0].entry.id, "ai-6", "Phải khớp mã official 6.A1.1 với catalog id");

  global.geminiAPI = { generateContent: async () => prose };
  appState.selectedGrade = "6";
  appState.content.vision = ocrText;
  appState.teachingContext = { integrations: { ai: true, digital: false }, ocrReady: true, standards: [] };
  const result = await requestStructuredIntegrationCandidates("ai", { silent: true });
  assert.strictEqual(result, true, "Gemini trả mã official trong JSON bọc prose vẫn tick");
  assert.strictEqual(appState.teachingContext.standards[0].officialCode, "6.A1.1");
  assert.strictEqual(appState.teachingContext.standards[0].autoSuggested, true);
  assert.strictEqual(appState.teachingContext.standards[0].catalogId, "ai-6");
}

function testFoldedAnchorAndWrongGrade() {
  const { parseStructuredCandidates } = require("../js/khbd-app.js");
  const entries6 = entriesForGrade("ai", 6);
  const foldedRaw = JSON.stringify({
    candidates: [{
      id: "6.A1.1",
      lessonAnchor: "Cho tập hợp A = {1, 2, 3}",
      fitRationale: validRationale,
      proposedTask: validTask
    }]
  });
  const folded = parseStructuredCandidates(foldedRaw, entries6, ocrText, 3);
  assert.strictEqual(folded.length, 1, "Neo lệch dấu câu/khoảng trắng vẫn nhận nếu fold ≥ 12 nằm trong OCR");
  assert.strictEqual(folded[0].entry.code, "6.A1.1");

  const grade7Raw = JSON.stringify({
    candidates: [{
      id: "7.A1.1",
      lessonAnchor: "Cho tập hợp A = {1; 2; 3}",
      fitRationale: validRationale,
      proposedTask: validTask
    }]
  });
  const rejected = parseStructuredCandidates(grade7Raw, entriesForGrade("ai", 6), ocrText, 3);
  assert.deepStrictEqual(rejected, [], "Id lớp 7 khi grade=6 phải bị loại");
}

async function testManualSelectionNotOverwritten() {
  const { appState, requestStructuredIntegrationCandidates } = require("../js/khbd-app.js");
  let called = false;
  global.geminiAPI = { generateContent: async () => { called = true; return '{"candidates":[{"id":"6.A1.1","lessonAnchor":"Cho tập hợp A = {1; 2; 3}","fitRationale":"x","proposedTask":"y"}]}'; } };
  appState.selectedGrade = "6";
  appState.content.vision = ocrText;
  appState.teachingContext = {
    integrations: { ai: true, digital: false },
    ocrReady: true,
    standards: [{ framework: "AI", catalogId: "manual-6", officialCode: "6.A1.2", autoSuggested: false }]
  };
  const result = await requestStructuredIntegrationCandidates("ai", { silent: true });
  assert.strictEqual(result, false, "Có autoSuggested: false thì không ghi đè");
  assert.strictEqual(called, false, "Không được gọi Gemini khi giáo viên đã chọn tay");
  assert.strictEqual(appState.teachingContext.standards[0].autoSuggested, false);
  assert.strictEqual(appState.teachingContext.standards[0].catalogId, "manual-6");
}

function testParaphrasedAnchorStillAccepted() {
  const { parseStructuredCandidates } = require("../js/khbd-app.js");
  const parsed = parseStructuredCandidates(JSON.stringify({
    candidates: [{
      id: "6.A1.1",
      lessonAnchor: "Học sinh xét tập hợp các số tự nhiên đã học",
      fitRationale: "Có thể kiểm chứng kết quả bằng SGK",
      proposedTask: "GV yêu cầu HS đối chiếu kết quả"
    }]
  }), entriesForGrade("ai", 6), ocrText, 3);
  assert.strictEqual(parsed.length, 1, "Id đúng lớp vẫn tick dù neo không khớp nguyên văn OCR");
  assert.strictEqual(parsed[0].entry.code, "6.A1.1");
}

async function testEmptyCandidatesFallbackTicks() {
  const { appState, requestStructuredIntegrationCandidates } = require("../js/khbd-app.js");
  global.geminiAPI = { generateContent: async () => '{"candidates":[]}' };
  appState.selectedGrade = "6";
  appState.content.vision = ocrText;
  appState.teachingContext = { integrations: { ai: true, digital: false }, ocrReady: true, standards: [] };
  const result = await requestStructuredIntegrationCandidates("ai", { silent: true });
  assert.strictEqual(result, true, "candidates rỗng vẫn phải tick fallback khung lớp");
  assert.ok(appState.teachingContext.standards.length >= 1, "Phải có ít nhất 1 mục được chọn");
  assert.ok(appState.teachingContext.standards.every(item => item.autoSuggested), "Fallback vẫn đánh dấu đề xuất tự động");
  assert.ok(appState.teachingContext.standards.every(item => String(item.officialCode || item.catalogId || "").startsWith("6") || String(item.catalogId).includes("6")), "Fallback AI lớp 6 không lấy lớp khác");
}

testGlobalGeminiWithoutWindow()
  .then(testOfficialCodeAndProseJson)
  .then(testFoldedAnchorAndWrongGrade)
  .then(testManualSelectionNotOverwritten)
  .then(testParaphrasedAnchorStillAccepted)
  .then(testEmptyCandidatesFallbackTicks)
  .then(() => console.log("khbd structured candidates smoke: passed"))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
