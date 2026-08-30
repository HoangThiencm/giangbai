'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

console.log('==================================================');
console.log('BẮT ĐẦU KIỂM THỬ LUỒNG ĐỀ XUẤT PPDH / NLS / AI');
console.log('==================================================');

const appCode = fs.readFileSync(path.join(__dirname, '..', 'js', 'khbd-app.js'), 'utf8');

console.log('-> 1. Kiểm tra mã nguồn: silent, loading, 1 toast hoàn tất...');
assert.match(appCode, /ensurePedagogyFromLesson\(\{ force: true, silent: true/, 'Bước 3 chạy heuristic im lặng');
assert.match(appCode, /requestStructuredIntegrationCandidates\("digital", \{ silent: true/, 'Bước 3 gọi NLS im lặng');
assert.match(appCode, /⏳ Đang phân tích SGK & đề xuất/, 'Nút đề xuất có trạng thái loading');
assert.match(appCode, /btnStep3Recommend/);
assert.match(appCode, /btnStep3PedagogyDigital/);
assert.match(appCode, /btnSuggestPedagogyStandards/);
assert.match(
  appCode,
  /✅ Đã đề xuất PPDH, kỹ thuật dạy học 4 pha và Năng lực số \(NLS\) bám sát nội dung SGK/,
  'Đúng 1 toast hoàn tất Bước 3'
);
assert.match(
  appCode,
  /async function triggerStep3PedagogyAndDigitalRecommendations[\s\S]*try \{[\s\S]*\} finally \{/,
  'Bước 3 phải try/finally để không treo nút'
);
assert.match(appCode, /requestStructuredIntegrationCandidates\("ai", \{ silent: true/, 'Bật AI gọi Gemini im lặng');
assert.match(appCode, /Hãy đọc SGK ở Bước 1\. Khi có nội dung, Gemini sẽ đề xuất đúng 2–3 mục AI/);
assert.match(appCode, /current\.length && !current\.every\(item => item\.autoSuggested\)/, 'Không ghi đè lựa chọn thủ công');
assert.doesNotMatch(
  appCode,
  /async function triggerStep3PedagogyAndDigitalRecommendations[\s\S]*?ensurePedagogyFromLesson\(\{ force: true, silent: false/,
  'Không còn toast trung gian heuristic trong Bước 3'
);
console.log('  -> Mã nguồn: PASS');

function fakeEl(id) {
  const attrs = {};
  const el = {
    id,
    disabled: false,
    hidden: false,
    checked: id === 'toggleDigitalCompetency',
    innerHTML: '',
    textContent: '',
    value: '',
    dataset: {},
    style: {},
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    children: [],
    setAttribute(name, value) { attrs[name] = String(value); },
    removeAttribute(name) { delete attrs[name]; },
    getAttribute(name) { return Object.prototype.hasOwnProperty.call(attrs, name) ? attrs[name] : null; },
    querySelectorAll() { return []; },
    querySelector() { return null; },
    addEventListener() {},
    appendChild(node) { this._appended = (this._appended || []).concat(node); return node; },
    append(...nodes) { this._appended = (this._appended || []).concat(nodes); },
    remove() {}
  };
  return el;
}

const store = {};
global.localStorage = {
  getItem: key => (key in store ? store[key] : null),
  setItem: (key, value) => { store[key] = String(value); },
  removeItem: key => { delete store[key]; }
};

const elements = {};
[
  'btnStep3Recommend', 'btnStep3PedagogyDigital', 'btnSuggestPedagogyStandards',
  'toggleDigitalCompetency', 'toggleAiCompetency',
  'methodsCatalogPanel', 'techniquesCatalogPanel', 'activitiesCatalogPanel',
  'digitalStandardsPanel', 'aiStandardsPanel',
  'toastContainer', 'selectMyDraft', 'btnImportLegacyDraft',
  'khbdWorkflowStepper', 'step1Badge', 'step2Badge', 'step3Badge', 'step4Badge'
].forEach(id => { elements[id] = fakeEl(id); });
elements.btnStep3Recommend.innerHTML = '⚡ Đề xuất PPDH & NLS';
elements.btnStep3PedagogyDigital.innerHTML = '⚡ ĐỀ XUẤT PPDH, KỸ THUẬT & NĂNG LỰC SỐ (TT 02)';
elements.btnSuggestPedagogyStandards.innerHTML = 'Đề xuất PPDH & Năng lực số';

const created = [];
global.document = {
  getElementById: id => elements[id] || null,
  querySelector() { return fakeEl('q'); },
  querySelectorAll() { return []; },
  createElement(tag) {
    const el = fakeEl(tag);
    created.push(el);
    return el;
  },
  addEventListener() {}
};
global.window = { document: global.document, localStorage: global.localStorage, addEventListener() {} };

let releaseGemini;
const geminiCalls = [];
global.geminiAPI = {
  apiKeys: ['test-key'],
  generateContent: async (prompt) => {
    geminiCalls.push(prompt);
    await new Promise(resolve => { releaseGemini = resolve; });
    return JSON.stringify({
      candidates: [
        { id: '1.1.TC1a', lessonAnchor: 'Tập hợp các số tự nhiên trong SGK', fitRationale: 'Bám bài tập tập hợp', proposedTask: 'HS đối chiếu kết quả trên phiếu.' },
        { id: '1.2.TC1a', lessonAnchor: 'Biểu diễn số trên tia số', fitRationale: 'Bám tia số', proposedTask: 'HS vẽ tia số trên phiếu.' }
      ]
    });
  }
};

const {
  appState,
  triggerStep3PedagogyAndDigitalRecommendations,
  triggerAiCompetencyRecommendations
} = require('../js/khbd-app.js');

const vision = 'Bài 1. Tập hợp các số tự nhiên. Cho tập hợp A = {1; 2; 3}. Học sinh thảo luận, trình bày kết quả vào vở và đối chiếu với bạn. Biểu diễn số tự nhiên trên tia số.';
appState.selectedGrade = '6';
appState.selectedSubject = 'TOAN';
appState.content.vision = vision;
appState.teachingContext = {
  integrations: { digital: true, ai: false },
  ocrReady: true,
  standards: [],
  methods: [],
  phasePedagogy: { A: {}, B: {}, C: {}, D: {} },
  subjectActivities: []
};

console.log('-> 2. Bước 3: loading, 1 toast, cập nhật UI một lần...');
(async () => {
const step3Promise = triggerStep3PedagogyAndDigitalRecommendations();
assert.strictEqual(elements.btnStep3Recommend.disabled, true, 'Nút stepper phải disabled khi đang xử lý');
assert.strictEqual(elements.btnStep3PedagogyDigital.disabled, true, 'Nút card Bước 3 phải disabled');
assert.match(elements.btnStep3Recommend.innerHTML, /Đang phân tích SGK/);
assert.match(elements.digitalStandardsPanel.innerHTML, /Đang phân tích SGK/);
assert.doesNotMatch(elements.digitalStandardsPanel.innerHTML, /standard-choice/, 'Chưa tick NLS tạm trong lúc chờ');
assert.strictEqual(elements.toastContainer._appended, undefined, 'Chưa toast khi AI chưa xong');

assert.ok(typeof releaseGemini === 'function', 'Gemini phải được gọi');
releaseGemini();
const ok = await step3Promise;
  assert.strictEqual(ok, true);
  assert.strictEqual(elements.btnStep3Recommend.disabled, false, 'Nút phải được mở lại sau finally');
  assert.match(elements.btnStep3Recommend.innerHTML, /Đề xuất PPDH/);
  const toasts = elements.toastContainer._appended || [];
  assert.strictEqual(toasts.length, 1, `Chỉ 1 toast hoàn tất, nhận ${toasts.length}`);
  const toastText = toasts.map(t => t.textContent || t.innerHTML || JSON.stringify(t)).join(' ');
  assert.match(String(elements.toastContainer._appended[0].className || '') + toastText, /success|Đã đề xuất PPDH/i);
  assert.ok((appState.teachingContext.methods || []).length > 0, 'PPDH phải được gán kết quả cuối');
  assert.ok(standardsCount('digital') >= 2, 'NLS phải có ít nhất 2 mục khi hoàn tất');
  console.log('  -> Bước 3 atomic: PASS');

  console.log('-> 3. Bước 4 AI: không tick fallback trước, 1 toast, tôn trọng chọn tay...');
  elements.toastContainer._appended = [];
  created.length = 0;
  appState.teachingContext.integrations.ai = true;
  appState.teachingContext.standards = (appState.teachingContext.standards || []).filter(item => item.standardKind !== 'ai' && item.framework !== (global.KHBD_STANDARDS?.ai?.framework));

  let releaseAi;
  global.geminiAPI.generateContent = async () => {
    await new Promise(resolve => { releaseAi = resolve; });
    return JSON.stringify({
      candidates: [
        { id: '6.A1.1', lessonAnchor: 'Tập hợp A = {1; 2; 3}', fitRationale: 'Ngữ cảnh tập hợp', proposedTask: 'HS kiểm chứng kết quả.' },
        { id: '6.A1.2', lessonAnchor: 'Tập hợp các số tự nhiên', fitRationale: 'Vai trò công cụ', proposedTask: 'HS nêu vai trò con người.' }
      ]
    });
  };

  const beforeAiCount = standardsCount('ai');
  const aiPromise = triggerAiCompetencyRecommendations();
  assert.strictEqual(elements.toggleAiCompetency.disabled, true, 'Toggle AI disabled khi đang phân tích');
  assert.match(elements.aiStandardsPanel.innerHTML, /Đang phân tích SGK/);
  assert.strictEqual(standardsCount('ai'), beforeAiCount, 'Không tick fallback AI trước khi Gemini trả lời');
  assert.ok(typeof releaseAi === 'function');
  releaseAi();
  await aiPromise;
  assert.strictEqual(elements.toggleAiCompetency.disabled, false);
  assert.ok(standardsCount('ai') >= 2, 'AI phải có 2–3 mục sau khi xong');
  const aiToasts = elements.toastContainer._appended || [];
  assert.strictEqual(aiToasts.length, 1, `Bật AI chỉ 1 toast, nhận ${aiToasts.length}`);

  const manual = (appState.teachingContext.standards || []).filter(item => item.standardKind === 'ai' || /2422/.test(String(item.framework || '')));
  assert.ok(manual.length, 'Phải có bản ghi AI để gắn autoSuggested=false');
  manual.forEach(item => { item.autoSuggested = false; });
  const kept = manual.map(item => item.catalogId || item.officialCode);
  global.geminiAPI.generateContent = async () => {
    throw new Error('không được gọi Gemini khi giáo viên đã chọn tay');
  };
  elements.toastContainer._appended = [];
  await triggerAiCompetencyRecommendations();
  const afterManual = (appState.teachingContext.standards || [])
    .filter(item => item.standardKind === 'ai' || /2422/.test(String(item.framework || '')))
    .map(item => item.catalogId || item.officialCode);
  assert.deepStrictEqual(afterManual, kept, 'Không ghi đè lựa chọn AI thủ công');
  console.log('  -> Bước 4 AI atomic + preserve: PASS');

  console.log('==================================================');
  console.log('TẤT CẢ TEST LUỒNG ĐỀ XUẤT ĐỀU ĐẠT (PASS)!');
  console.log('==================================================');
})().catch(err => {
  console.error(err);
  process.exit(1);
});

function standardsCount(kind) {
  const list = appState.teachingContext.standards || [];
  if (kind === 'ai') {
    return list.filter(item => item.standardKind === 'ai' || /2422|năng lực AI/i.test(String(item.framework || ''))).length;
  }
  return list.filter(item => item.standardKind === 'digital' || /Thông tư 02|năng lực số/i.test(String(item.framework || ''))).length;
}
