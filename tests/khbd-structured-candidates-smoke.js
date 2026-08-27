const assert = require("assert");
const fs = require("fs");

const app = fs.readFileSync("js/khbd-app.js", "utf8");

assert.match(app, /function requestStructuredIntegrationCandidates\(/, "Phải có yêu cầu đề xuất có cấu trúc");
assert.match(app, /NỘI DUNG OCR SGK/, "Prompt phải lấy đúng nguồn OCR");
assert.match(app, /id đúng nguyên văn trong danh mục/, "Prompt phải yêu cầu id catalog");
assert.match(app, /trích dẫn nguyên văn, liên tiếp từ OCR/, "Prompt phải yêu cầu trích dẫn OCR");
assert.match(app, /source\.includes\(normalizeEvidenceText\(evidence\)\)/, "Phải xác thực minh chứng xuất hiện trong OCR");
assert.match(app, /if \(!byId\.has\(id\) \|\| used\.has\(id\)/, "Phải chặn id ngoài danh mục và trùng lặp");
assert.match(app, /current\.length && !current\.every\(item => item\.autoSuggested\)/, "Không được ghi đè lựa chọn thủ công");
assert.match(app, /không được thay bằng heuristic/i, "Lỗi Gemini không được tự tick bằng heuristic");
assert.match(app, /hasOcrReadyLessonContent\(\)/, "Chỉ yêu cầu Gemini sau khi OCR sẵn sàng");
assert.match(app, /typeof geminiAPI === "undefined"/, "Phải kiểm tra Gemini API toàn cục an toàn");
assert.doesNotMatch(app, /window\.geminiAPI/, "Không được phụ thuộc Gemini API là thuộc tính window");
assert.match(app, /const selectable = enabled && hasOcrReadyLessonContent\(\)/, "Text dán tay chưa qua OCR không được mở checkbox");

async function testGlobalGeminiWithoutWindow() {
  const saved = new Map();
  global.localStorage = { getItem: key => saved.get(key) || null, setItem: (key, value) => saved.set(key, value) };
  global.KHBD_STANDARDS = { ai: { framework: "AI", source: "test", date: "2026", maxSelect: 3, entries: [{ id: "ai-6", code: "6.A1.1", label: "AI", grades: [6] }] } };
  global.standardToRecord = (kind, entry, grade, autoSuggested) => ({ framework: "AI", catalogId: entry.id, officialCode: entry.code, grade, autoSuggested });
  global.getSystemRole = () => "test";
  let called = false;
  global.geminiAPI = { generateContent: async () => { called = true; return '{"candidates":[]}'; } };
  delete global.window;
  const { appState, requestStructuredIntegrationCandidates } = require("../js/khbd-app.js");
  global.document = { getElementById: () => null, querySelectorAll: () => [] };
  appState.selectedGrade = "6";
  appState.content.vision = "Nội dung OCR đã sẵn sàng và đủ dài để kiểm tra kết quả từ sách giáo khoa của bài học.";
  appState.teachingContext = { integrations: { ai: true, digital: false }, ocrReady: true, standards: [] };
  const result = await requestStructuredIntegrationCandidates("ai", { silent: true });
  assert.strictEqual(result, true, "Global geminiAPI phải được gọi dù không có window.geminiAPI");
  assert.strictEqual(called, true, "Phải gọi global geminiAPI");
}

testGlobalGeminiWithoutWindow().then(() => console.log("khbd structured candidates smoke: passed"));
