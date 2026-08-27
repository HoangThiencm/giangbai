const assert = require("assert");
const fs = require("fs");

const app = fs.readFileSync("js/khbd-app.js", "utf8");

assert.match(app, /function requestStructuredIntegrationCandidates\(/, "Phải có yêu cầu đề xuất có cấu trúc");
assert.match(app, /NỘI DUNG OCR SGK/, "Prompt phải lấy đúng nguồn OCR");
assert.match(app, /id đúng nguyên văn trong danh mục/, "Prompt phải yêu cầu id catalog");
assert.match(app, /lessonAnchor/, "JSON phải có neo SGK");
assert.match(app, /fitRationale/, "JSON phải có lý do phù hợp");
assert.match(app, /đoạn OCR nguyên văn, liên tiếp về khái niệm, ví dụ hoặc bài tập/, "Prompt phải yêu cầu neo SGK từ bài học");
assert.match(app, /source\.includes\(anchorText\)/, "Phải xác thực neo SGK xuất hiện trong OCR");
assert.match(app, /anchorTerms\.some\(word => taskText\.includes\(word\)\)/, "Nhiệm vụ phải gắn neo SGK");
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
  global.geminiAPI = { generateContent: async () => { called = true; return '{"candidates":[{"id":"ai-6","lessonAnchor":"Cho tập hợp A = {1; 2; 3}","fitRationale":"Bài tập tập hợp tạo ngữ cảnh để học sinh kiểm tra kết quả.","proposedTask":"GV cho HS đối chiếu kết quả AI với tập hợp A; HS nộp phiếu kiểm tra tập hợp."}]}' } };
  delete global.window;
  const { appState, requestStructuredIntegrationCandidates } = require("../js/khbd-app.js");
  global.document = { getElementById: () => null, querySelectorAll: () => [] };
  appState.selectedGrade = "6";
  appState.content.vision = "Bài 1. Tập hợp. Cho tập hợp A = {1; 2; 3}. Hãy viết tập hợp B gồm các phần tử là số tự nhiên nhỏ hơn 4. Học sinh thảo luận và trình bày kết quả vào vở.";
  appState.teachingContext = { integrations: { ai: true, digital: false }, ocrReady: true, standards: [] };
  const result = await requestStructuredIntegrationCandidates("ai", { silent: true });
  assert.strictEqual(result, true, "Global geminiAPI phải được gọi dù không có window.geminiAPI");
  assert.strictEqual(called, true, "Phải gọi global geminiAPI");
  assert.strictEqual(appState.teachingContext.standards[0].lessonAnchor, "Cho tập hợp A = {1; 2; 3}", "OCR Toán 6 không có từ AI vẫn chấp nhận neo bài tập thật");
}

testGlobalGeminiWithoutWindow().then(() => console.log("khbd structured candidates smoke: passed"));
