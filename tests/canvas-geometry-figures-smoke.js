'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.join(__dirname, '..');
const app = fs.readFileSync(path.join(root, 'js', 'khbd-app.js'), 'utf8');
const prompts = fs.readFileSync(path.join(root, 'js', 'khbd-prompts.js'), 'utf8');

assert.ok(app.includes('\\"figures\\":[{\\"id\\":\\"Hình 1\\",\\"description\\":'), 'Canvas schema phải yêu cầu figures có id và description');
assert.match(app, /function normalizeCanvasTextbookFigure\(/, 'Canvas phải chuẩn hóa figures từ AI');
assert.match(app, /function mergeCanvasTextbookFigures\(/, 'Canvas phải gộp figures qua các batch');
assert.match(app, /mergeCanvasTextbookFigures\(analyses\.flatMap\(item => item\.figures \|\| \[\]\)\)/, 'Figures phải được dedupe sau tất cả batch');
assert.match(app, /## Hình vẽ trong SGK/, 'Ngữ cảnh SGK phải có heading hình vẽ');
assert.match(app, /function buildSourceFigureFallbackSpecs\(/, 'Phải có fallback từ figures SGK');
assert.match(app, /function hasStrongGeometrySignal\(/, 'Fallback phải dùng detector hình học mạnh riêng');
assert.match(app, /const strongGeometry = hasStrongGeometrySignal\(evidence\)/, 'Fallback không được dùng detector toán rộng cho hình học');
assert.match(app, /if \(!specs\.length\) specs = buildSourceFigureFallbackSpecs\(context\)/, 'Hình học không được rơi ngay vào nhánh không cần hình');
assert.match(app, /không tự thêm số đo, tên đỉnh, ký hiệu/, 'Fallback không được bịa chi tiết hình học');
assert.match(prompts, /BẮT BUỘC trả 1–3 hình sgk, TUYỆT ĐỐI KHÔNG trả \{\"illustrations\":\[\]\}/, 'Prompt phải cấm illustrations rỗng cho hình học/figures');

const start = app.indexOf('function normalizeCanvasTextbookFigure');
const end = app.indexOf('async function prepareCanvasTextbookAnalysisBatches', start);
assert.ok(start >= 0 && end > start, 'Có thể nạp các helper phân tích figures');
const sandbox = {
  parseAiJsonSafely: raw => JSON.parse(raw),
  mergeCanvasTextbookSections: rows => rows || [],
  normalizeCanvasTextbookExercise: row => row,
  normalizeTextbookSubsectionProfiles: rows => rows || []
};
vm.createContext(sandbox);
vm.runInContext(app.slice(start, end), sandbox);
const formatStart = app.indexOf('function formatCanvasTextbookContext');
const formatEnd = app.indexOf('async function applyTextbookOcrResult', formatStart);
assert.ok(formatStart >= 0 && formatEnd > formatStart, 'Có thể nạp formatter ngữ cảnh figures');
vm.runInContext(app.slice(formatStart, formatEnd), sandbox);
const parsed = sandbox.parseCanvasTextbookAnalysis(JSON.stringify({
  figures: [
    { id: 'Hình 1', description: 'Tam giác ABC có góc vuông tại A', subsection: '1. Tam giác vuông' },
    { id: 'Hình 1', description: 'Tam giác ABC có góc vuông tại A', subsection: '1. Tam giác vuông' },
    { id: 'Hình 2', description: 'Đường tròn tâm O', subsection: '2. Đường tròn' }
  ]
}));
assert.strictEqual(parsed.figures.length, 2, 'Figure trùng ở hai batch phải được dedupe');
const context = sandbox.formatCanvasTextbookContext(parsed);
assert.match(context, /## Hình vẽ trong SGK/, 'Context phải xuất heading figures');
assert.match(context, /Hình 1 \(1\. Tam giác vuông\): Tam giác ABC/, 'Context phải giữ mô tả và đề mục nguồn');

const fallbackStart = app.indexOf('function sourceTextbookFigures');
const fallbackEnd = app.indexOf('function buildIllustrationImagePrompt', fallbackStart);
assert.ok(fallbackStart >= 0 && fallbackEnd > fallbackStart, 'Có thể nạp fallback figures');
const fallbackSandbox = {};
vm.createContext(fallbackSandbox);
vm.runInContext(app.slice(fallbackStart, fallbackEnd), fallbackSandbox);
const fallback = fallbackSandbox.buildSourceFigureFallbackSpecs({ textbook_content: context, topic: 'Tam giác vuông' });
assert.strictEqual(fallback.length, 2, 'Fallback phải dựng tối đa ba hình từ figures nguồn');
assert.match(fallback[0].prompt, /không tự thêm số đo/, 'Fallback phải giữ ràng buộc không bịa chi tiết');
assert.strictEqual(fallbackSandbox.buildSourceFigureFallbackSpecs({ textbook_content: 'Bài học số học', topic: 'Phép cộng' }).length, 0, 'Bài không hình học không được ép tạo hình');
assert.strictEqual(fallbackSandbox.buildSourceFigureFallbackSpecs({ textbook_content: 'Tập hợp A và các phép toán trên tập hợp', topic: 'Tập hợp' }).length, 0, 'Tập hợp không có figures không được fallback SVG');
assert.strictEqual(fallbackSandbox.buildSourceFigureFallbackSpecs({ textbook_content: 'Giải phương trình bậc nhất một ẩn', topic: 'Phương trình' }).length, 0, 'Đại số thuần không được fallback SVG');
assert.strictEqual(fallbackSandbox.buildSourceFigureFallbackSpecs({ textbook_content: 'Khám phá tính chất tam giác', topic: 'Tam giác' }).length, 1, 'Tín hiệu hình học mạnh phải có fallback khi AI trả rỗng');

console.log('canvas geometry figures smoke: passed');
