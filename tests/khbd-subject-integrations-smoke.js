'use strict';

const assert = require('assert');

global.window = {
  addEventListener: () => {},
  removeEventListener: () => {},
  document: {},
  lucide: { createIcons: () => {} }
};

const domStore = {};
global.document = {
  addEventListener: () => {},
  createElement(tag) {
    return {
      tagName: String(tag || 'div').toUpperCase(),
      id: '',
      value: '',
      checked: false,
      textContent: '',
      innerHTML: '',
      hidden: false,
      style: {},
      dataset: {},
      classList: { add() {}, remove() {}, contains() { return false; } },
      setAttribute() {},
      getAttribute() { return null; },
      addEventListener() {},
      appendChild() {},
      append() {}
    };
  },
  getElementById(id) {
    if (!domStore[id]) {
      domStore[id] = {
        id,
        value: '',
        checked: false,
        textContent: '',
        innerHTML: '',
        hidden: false,
        style: {},
        dataset: {},
        classList: { add() {}, remove() {}, contains() { return false; } },
        addEventListener() {},
        appendChild() {},
        append() {}
      };
    }
    return domStore[id];
  },
  querySelectorAll: () => []
};

const lsStore = {};
global.localStorage = {
  getItem(k) { return lsStore[k] || null; },
  setItem(k, v) { lsStore[k] = String(v); },
  removeItem(k) { delete lsStore[k]; },
  clear() { Object.keys(lsStore).forEach(k => delete lsStore[k]); }
};

global.showToast = () => {};
global.updateProgress = () => {};
global.hideProgress = () => {};
global.renderMathPreview = () => {};
global.userConfirm = () => true;

try {
  const curr = require('../js/khbd-curriculum.js');
  Object.assign(global, curr);
} catch (e) {}

try {
  const ped = require('../js/khbd-pedagogy-catalog.js');
  Object.assign(global, ped);
} catch (e) {}

try {
  const prm = require('../js/khbd-prompts.js');
  Object.assign(global, prm);
} catch (e) {}

try {
  const { KHBD_STANDARDS } = require('../js/khbd-standards.js');
  global.KHBD_STANDARDS = KHBD_STANDARDS;
} catch (e) {}

const app = require('../js/khbd-app.js');

function idsFor(subjectId) {
  return app.contextIntegrationsForSubject(subjectId).map(item => item.id);
}

console.log('================================================================================');
console.log('KIỂM THỬ TÍCH HỢP BỐI CẢNH THEO MÔN - SMOKE TESTS');
console.log('================================================================================');

console.log('\n[TEST 1] Catalog theo môn...');
assert(Array.isArray(app.SUBJECT_CONTEXT_INTEGRATIONS), 'SUBJECT_CONTEXT_INTEGRATIONS phải là mảng.');
const toanIds = idsFor('toan');
const nguvanIds = idsFor('nguvan');
const lsIds = idsFor('lichsudialy');
const taIds = idsFor('tienganh');
assert.ok(!toanIds.includes('gdqpan'), 'toan không chứa gdqpan');
assert.ok(toanIds.includes('financialEd') && toanIds.includes('stemModeling'), 'toan có GD tài chính và STEM');
assert.ok(nguvanIds.includes('gdqpan'), 'nguvan có gdqpan');
assert.ok(nguvanIds.includes('hcmThought'), 'nguvan có hcmThought');
assert.ok(nguvanIds.includes('humanRights'), 'nguvan có humanRights');
assert.ok(nguvanIds.includes('localEnv'), 'nguvan có localEnv');
assert.ok(lsIds.includes('gdqpan'), 'lichsudialy có gdqpan');
assert.ok(lsIds.includes('climateSdgs'), 'lichsudialy có climateSdgs');
assert.ok(taIds.includes('clil'), 'tienganh có clil');
assert.ok(!taIds.includes('gdqpan'), 'tienganh không có gdqpan');
assert.strictEqual(idsFor('khtn').length, 0, 'khtn không có mục tích hợp bối cảnh');
assert.strictEqual(idsFor('tinhoc').length, 0, 'tinhoc không có mục tích hợp bối cảnh');
console.log('✓ Catalog theo môn khớp Bộ/chuyên môn.');

console.log('\n[TEST 2] normalizeTeachingContext giữ 4 key cũ và thêm key mới = false...');
const normalized = app.normalizeTeachingContext({});
assert.strictEqual(normalized.integrations.digital, false);
assert.strictEqual(normalized.integrations.ai, false);
assert.strictEqual(normalized.integrations.foreignLanguage, false);
assert.strictEqual(normalized.integrations.inclusive, false);
app.SUBJECT_CONTEXT_INTEGRATIONS.forEach(item => {
  assert.strictEqual(normalized.integrations[item.id], false, `${item.id} phải false khi thiếu`);
});
const kept = app.normalizeTeachingContext({
  integrations: { digital: true, gdqpan: true, clil: true }
});
assert.strictEqual(kept.integrations.digital, true);
assert.strictEqual(kept.integrations.gdqpan, true);
assert.strictEqual(kept.integrations.clil, true);
assert.strictEqual(kept.integrations.ai, false);
console.log('✓ normalizeTeachingContext mở rộng đúng.');

console.log('\n[TEST 3] Tick gdqpan + môn Ngữ văn → prompt có TT 08 và [GDQPAN]...');
app.appState.selectedSubject = 'nguvan';
app.appState.teachingContext = app.normalizeTeachingContext({
  integrations: { gdqpan: true }
});
const pedOn = app.buildPedagogicalContext();
assert.ok(pedOn.includes('TÍCH HỢP BỐI CẢNH'), 'Phải có khối TÍCH HỢP BỐI CẢNH');
assert.ok(pedOn.includes('TT 08'), 'Phải nêu TT 08/2024/TT-BGDĐT');
assert.ok(pedOn.includes('[GDQPAN]'), 'Phải có marker [GDQPAN]');
assert.deepStrictEqual(app.enabledContextIntegrations().map(item => item.id), ['gdqpan']);
const genOn = app.getGenerationPromptContext();
assert.deepStrictEqual(genOn.contextIntegrationsEnabled, ['gdqpan']);
console.log('✓ Tick hợp môn được lồng vào prompt.');

console.log('\n[TEST 4] Không tick → CẤM, không bắt buộc lồng GDQPAN...');
app.appState.selectedSubject = 'nguvan';
app.appState.teachingContext = app.normalizeTeachingContext({});
const pedOff = app.buildPedagogicalContext();
assert.ok(pedOff.includes('CẤM'), 'Không tick thì phải có câu CẤM');
assert.ok(!/lồng GDQPAN/.test(pedOff), 'Không được có câu bắt buộc lồng GDQPAN');
assert.ok(!pedOff.includes('**[GDQPAN]**'), 'Không tick thì không đánh dấu bắt buộc [GDQPAN]');
assert.strictEqual(app.enabledContextIntegrations().length, 0);
console.log('✓ Không tick thì cấm bịa, không bắt buộc thực hiện.');

console.log('\n[TEST 5] Đổi môn prune: gdqpan không rò sang Toán...');
app.appState.selectedSubject = 'nguvan';
app.appState.teachingContext = app.normalizeTeachingContext({
  integrations: { gdqpan: true }
});
app.appState.selectedSubject = 'toan';
assert.strictEqual(app.enabledContextIntegrations().length, 0, 'enabled list phải rỗng khi đổi sang toan');
const pedPrune = app.buildPedagogicalContext();
assert.ok(!pedPrune.includes('**[GDQPAN]**'), 'prompt Toán không còn [GDQPAN] như nội dung bắt buộc');
assert.ok(!pedPrune.includes('TT 08/2024/TT-BGDĐT'), 'prompt Toán không bắt buộc TT 08');
app.pruneContextIntegrationsForSubject('toan');
assert.strictEqual(app.appState.teachingContext.integrations.gdqpan, false, 'prune phải zero key không thuộc môn');
console.log('✓ Đổi môn prune không rò 1-click.');

console.log('\n================================================================================');
console.log('TẤT CẢ KIỂM THỬ TÍCH HỢP BỐI CẢNH THEO MÔN ĐỀU ĐẠT.');
console.log('================================================================================');
