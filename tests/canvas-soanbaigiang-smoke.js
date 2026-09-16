'use strict';

const fs = require('fs');
const path = require('path');
const assert = require('assert');
const vm = require('vm');

console.log('================================================================');
console.log('KIỂM THỬ: CANVAS_SOANBAIGIANG — BÀI GIẢNG TRÌNH CHIẾU PPTX');
console.log('================================================================');

const root = path.join(__dirname, '..');
const htmlPath = path.join(root, 'canvas_soanbaigiang.html');
const backupPath = path.join(root, 'backupcode viettailieu', 'canvas_soanbaigiang.html');
const slidesPath = path.join(root, 'js', 'khbd-slides.js');
const khbdHtml = fs.readFileSync(path.join(root, 'canvas_soankhbd.html'), 'utf8');

assert.ok(fs.existsSync(htmlPath), 'Phải có canvas_soanbaigiang.html');
assert.ok(fs.existsSync(slidesPath), 'Phải có js/khbd-slides.js');
assert.ok(fs.existsSync(backupPath), 'Phải có backup canvas_soanbaigiang.html');

const html = fs.readFileSync(htmlPath, 'utf8');
const backup = fs.readFileSync(backupPath, 'utf8');
const slidesSrc = fs.readFileSync(slidesPath, 'utf8');

function extractIds(text) {
  return new Set([...String(text).matchAll(/\bid=["']([^"']+)["']/g)].map(m => m[1]));
}

for (const [label, doc] of [['canvas_soanbaigiang.html', html], ['backup', backup]]) {
  const ids = extractIds(doc);
  assert.match(doc, /SOẠN BÀI GIẢNG TRÌNH CHIẾU AI/, `${label} phải đổi tiêu đề bài giảng trình chiếu`);
  assert.match(doc, /HỆ THỐNG SOẠN BÀI GIẢNG TRÌNH CHIẾU AI \(CANVAS SLIDES &(?:amp;)? PPTX\)/, `${label} phải có banner header slides`);
  assert.ok(doc.includes('gemini-3-flash-preview'), `${label} giữ model gemini-3-flash-preview`);
  assert.ok(doc.includes('https://hoangthiencm.id.vn/api/canvas_gemini.php'), `${label} giữ endpoint Canvas Gemini`);
  assert.ok(doc.includes('https://cdn.jsdelivr.net/npm/pptxgenjs@3.12.0/dist/pptxgen.bundle.js'), `${label} nạp PptxGenJS CDN`);
  assert.ok(doc.includes('js/khbd-slides.js'), `${label} nạp khbd-slides.js`);
  assert.doesNotMatch(doc, /https:\/\/hoangthiencm\.id\.vn\/js\/khbd-slides\.js/, `${label} không phụ thuộc bundle slides từ host ngoài`);
  assert.ok(ids.has('slideStage'), `${label} phải có khung slide 16:9 #slideStage`);
  assert.ok(ids.has('btnSlidePrev'), `${label} phải có #btnSlidePrev`);
  assert.ok(ids.has('btnSlideNext'), `${label} phải có #btnSlideNext`);
  assert.ok(ids.has('slideCounter'), `${label} phải có #slideCounter`);
  assert.ok(ids.has('btnPresentFullscreen'), `${label} phải có nút trình chiếu F5`);
  assert.ok(ids.has('btnExportPptx'), `${label} phải có nút tải PPTX`);
  assert.ok(ids.has('btnBuildSlides'), `${label} phải có nút tạo slides`);
  assert.ok(ids.has('slidePresentationOverlay'), `${label} phải có overlay fullscreen`);
  assert.ok(ids.has('khbdWorkflowStepper'), `${label} kế thừa stepper nạp SGK`);
  assert.match(doc, /aspect-ratio:\s*16\s*\/\s*9/, `${label} khung trình chiếu 16:9`);
  assert.match(doc, /Trình chiếu toàn màn hình \(F5\)/, `${label} có nhãn F5`);
  assert.match(doc, /Tải file PowerPoint \(\.pptx\)/, `${label} có nút tải PPTX`);
}

assert.match(khbdHtml, /Soạn Kế hoạch Bài dạy AI — Gemini Canvas/, 'canvas_soankhbd.html không bị đổi tiêu đề');
assert.doesNotMatch(khbdHtml, /js\/khbd-slides\.js/, 'canvas_soankhbd.html không nạp khbd-slides.js');
assert.match(khbdHtml, /5\. Toàn bộ Giáo án \(\.DOCX\)/, 'Tab giáo án Word của KHBD còn nguyên');

assert.match(slidesSrc, /function buildSlideDeck/, 'khbd-slides.js định nghĩa buildSlideDeck');
assert.match(slidesSrc, /async function generateAiLessonSlides/, 'khbd-slides.js gọi Gemini để tạo kịch bản slide thật');
assert.match(slidesSrc, /gemini-3-flash-preview/, 'Kịch bản slides dùng Gemini 3 Flash');
assert.match(slidesSrc, /NGỮ CẢNH SGK THẬT/, 'Prompt slide ràng buộc vào nội dung SGK thực');
[
  'Quan sát tình huống trong SGK và nêu nhận xét ban đầu.',
  'Ví dụ mẫu trong SGK.',
  'Đề bài ví dụ mẫu (SGK).',
  'Bước 1: Đọc hiểu — xác định giả thiết và yêu cầu.',
  'Học sinh làm nháp 1–2 phút.',
  'Đáp án (click để mở): áp dụng đúng quy tắc vừa học, trình bày đủ bước.',
  'Câu hỏi củng cố kiến thức vừa học.'
].forEach((placeholder) => {
  assert.ok(!slidesSrc.includes(placeholder), `Không giữ placeholder legacy: ${placeholder}`);
});
assert.match(slidesSrc, /async function exportToPptx|function exportToPptx/, 'khbd-slides.js định nghĩa exportToPptx');
assert.match(slidesSrc, /Khám phá/, 'Deck có slide Khám phá');
assert.match(slidesSrc, /Kiến thức trọng tâm/, 'Deck có slide kiến thức đóng khung');
assert.match(slidesSrc, /Ví dụ mẫu/, 'Deck có slide ví dụ mẫu');
assert.match(slidesSrc, /Luyện tập tại chỗ/, 'Deck có slide luyện tập');
assert.match(slidesSrc, /step:\s*[1-5]/, 'Có gán step cho hiệu ứng click');

const KhbdSlides = require(slidesPath);
assert.ok(typeof KhbdSlides.buildSlideDeck === 'function', 'export buildSlideDeck');
assert.ok(typeof KhbdSlides.generateAiLessonSlides === 'function', 'export generateAiLessonSlides');
assert.ok(typeof KhbdSlides.exportToPptx === 'function', 'export exportToPptx');

const textbook = `
# Tập hợp các số tự nhiên
## 1. Tập hợp
Định nghĩa tập hợp. Công thức $n = 280\\,650$.
Ví dụ 1: Cho số n. Viết tập hợp các chữ số.
Luyện tập: Bài 1.1

## 2. Cấu tạo số
Quy tắc giá trị vị trí. Ví dụ 2: Tính tổng giá trị các chữ số.
Bài tập 2: Biểu diễn số thành tổng.
`;

const deck = KhbdSlides.buildSlideDeck({
  topic: 'Luyện tập chung',
  subject: 'Toán',
  grade: '6',
  duration: '02 tiết (90 phút)',
  textbook
});

assert.ok(deck.length >= 15, `Bài hoàn chỉnh phải từ 15 slide (nhận ${deck.length})`);
assert.ok(deck.length <= 25, `Bài hoàn chỉnh không vượt 25 slide (nhận ${deck.length})`);
assert.ok(deck.some(s => /Khám phá/i.test(s.title)), 'Có slide khám phá');
assert.ok(deck.some(s => /Kiến thức trọng tâm/i.test(s.title)), 'Có slide kiến thức đóng khung');
assert.ok(deck.some(s => /Ví dụ mẫu/i.test(s.title)), 'Có slide ví dụ mẫu từng bước');
assert.ok(deck.some(s => /Luyện tập/i.test(s.title)), 'Có slide luyện tập tại chỗ');
const example = deck.find(s => /Ví dụ mẫu/i.test(s.title));
assert.ok(example && KhbdSlides.maxStep(example) >= 4, 'Ví dụ mẫu phải nhiều bước click');
const revealed1 = KhbdSlides.visibleItems(example, 1);
const revealed2 = KhbdSlides.visibleItems(example, 2);
assert.ok(revealed1.length >= 1, 'Click 1 hiện câu hỏi/đề');
assert.ok(revealed2.length > revealed1.length, 'Click tiếp hiện thêm lời giải');

(async function () {
  let thrown = null;
  try { await KhbdSlides.exportToPptx([]); } catch (err) { thrown = err; }
  assert.ok(thrown, 'exportToPptx deck rỗng phải báo lỗi');

  const aiTypes = ['title', 'intro', 'explore', 'rule', 'example', 'practice', 'summary'];
  const aiResponse = {
    slides: Array.from({ length: 15 }, (_, i) => ({
      type: aiTypes[i % aiTypes.length],
      title: `Slide SGK ${i + 1}`,
      content: `Nội dung Bài 5 đã đọc ${i + 1}`,
      steps: i === 4 ? ['Bước giải 1', 'Bước giải 2'] : [],
      mathFormula: i === 3 ? 'a+b=c' : ''
    }))
  };
  global.geminiAPI = { selectedModel: '', generateContent: async (prompt) => {
    assert.match(prompt, /NGỮ CẢNH SGK THẬT/, 'Gửi ngữ cảnh SGK thực vào Gemini');
    assert.match(prompt, /Bài 5/, 'Gửi đúng nội dung bài đã đọc vào Gemini');
    return JSON.stringify(aiResponse);
  }};
  const aiDeck = await KhbdSlides.generateAiLessonSlides({ topic: 'Bài 5', subject: 'Toán', grade: '6', duration: '2 tiết', textbook: 'Bài 5: nội dung SGK thật.' });
  assert.equal(global.geminiAPI.selectedModel, 'gemini-3-flash-preview', 'Ép đúng model Gemini Canvas');
  assert.equal(aiDeck.length, 15, 'Dùng nguyên kịch bản AI 15 slide');
  assert.ok(aiDeck.every(s => s.meta.aiGenerated), 'Deck đánh dấu là dữ liệu do AI tạo');
  delete global.geminiAPI;

  const scriptBlocks = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].map(m => m[1]);
  for (let i = 0; i < scriptBlocks.length; i++) {
    const code = scriptBlocks[i].trim();
    if (!code) continue;
    try { new vm.Script(code); } catch (err) {
      assert.fail(`Lỗi cú pháp script #${i + 1} canvas_soanbaigiang.html: ${err.message}`);
    }
  }

  console.log('✓ canvas_soanbaigiang: nhân bản độc lập, 16:9, F5, PPTX, 15–25 slide step-by-step.');
  console.log('✓ canvas_soankhbd.html không bị đụng.');
  console.log('\n================================================================');
  console.log('🎉 KIỂM THỬ CANVAS_SOANBAIGIANG ĐÃ PASS 100%!');
  console.log('================================================================\n');
})().catch(function (err) {
  console.error(err);
  process.exit(1);
});
