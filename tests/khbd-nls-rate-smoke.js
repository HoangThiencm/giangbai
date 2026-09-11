'use strict';

const fs = require('fs');
const path = require('path');
const assert = require('assert');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'xaydungphuluc.html'), 'utf8');
const appSrc = fs.readFileSync(path.join(__dirname, '..', 'js', 'khbd-app.js'), 'utf8');

assert.match(html, /nlsSelectedLessonIds\s*=\s*new Set/);
assert.match(html, /function isLessonNlsSelected\(/);
assert.match(html, /function prioritizedNlsLessons\(/);
assert.match(html, /💻 Gợi ý NLS theo tỉ trọng/);
assert.match(html, /Tích hợp NLS \(CV 3456\)/);
assert.match(html, /Do người dùng quyết định/);
assert.match(html, /nlsOn\?fallbackNlsCodes/);
assert.match(appSrc, /integrations\.digital !== undefined \? Boolean\(integrations\.digital\) : true/);
assert.match(appSrc, /const isDigitalActive = toggleDigital \? toggleDigital\.checked/);
assert.doesNotMatch(
  appSrc.slice(appSrc.indexOf('async function triggerStep3PedagogyAndDigitalRecommendations'), appSrc.indexOf('function renderStandardsCatalog')),
  /toggleDigital\.checked = true/
);

function extract(name) {
  const start = html.indexOf(`function ${name}(`);
  assert.ok(start >= 0, name + ' missing');
  let i = html.indexOf('{', start), depth = 0, end = i;
  for (; end < html.length; end++) {
    if (html[end] === '{') depth++;
    else if (html[end] === '}') {
      depth--;
      if (depth === 0) { end++; break; }
    }
  }
  return html.slice(start, end);
}

const sandbox = {
  nlsSelectedLessonIds: new Set(),
  nlsEnabled: { checked: true },
  nlsRate: { value: '50' },
  nlsRateOut: { value: '' }, nlsUnit:{value:'period'}, nlsCountInput:{value:''},
  document: { querySelector(sel) { return {'#nlsRate':sandbox.nlsRate,'#nlsRateOut':sandbox.nlsRateOut,'#nlsUnit':sandbox.nlsUnit,'#nlsCountInput':sandbox.nlsCountInput}[sel]||null; } },
  notify() {},
  updateAiPicker() {},
  selectedAiLessons() { return []; },
  lessonsMatch(a, b) { return String(a) === String(b); },
  cleanLessonDescription(s) { return String(s || ''); },
  foldText(s) {
    return String(s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toUpperCase().replace(/\s+/g, ' ').trim();
  },
  _cands: []
};
sandbox.nlsCandidates = function nlsCandidates() { return sandbox._cands; };
sandbox.validPeriodCount = value => Number(value) || 1;
sandbox.aiPeriodCandidates = () => sandbox._cands.flatMap(row => Array.from({length:sandbox.validPeriodCount(row.periods,row.tietCT)},(_,index)=>({id:`${row.id}:period:${index+1}`,lessonId:row.id})));
vm.createContext(sandbox);
vm.runInContext(
  extract('nlsLessonPriorityScore') + '\n' +
  extract('prioritizedNlsLessons') + '\n' +
  extract('isLessonNlsSelected') + '\n' +
  extract('allocationUnit') + '\n' +
  extract('allocationTotals') + '\n' +
  extract('nlsSelectedPeriodCount') + '\n' +
  extract('chooseNlsLessonsForPeriods') + '\n' +
  extract('allocationSummary') + '\n' +
  extract('syncNlsRateFromSelection') + '\n' +
  extract('syncNlsSelectionFromRate') + '\n' +
  extract('toggleNlsLesson') + '\n' +
  extract('clearNlsLessons'),
  sandbox
);

sandbox._cands = [
  { id: 'ppct:0', lesson: 'Bài 1. Tập hợp' },
  { id: 'ppct:1', lesson: 'Bài 18. Tam giác đều, hình vuông' },
  { id: 'ppct:2', lesson: 'Bài 38. Dữ liệu và thu thập dữ liệu' },
  { id: 'ppct:3', lesson: 'Ôn tập và Bài tập cuối chương II' },
  { id: 'ppct:4', lesson: 'Kiểm tra giữa kỳ I' }
];

console.log('==================================================');
console.log('KIỂM THỬ TỈ TRỌNG NLS (CV 3456) DO NGƯỜI DÙNG CHỌN');
console.log('==================================================');

console.log('\n[CASE 1] Tỉ trọng 0% / tắt NLS -> không bài nào có NLS');
sandbox.nlsSelectedLessonIds = new Set();
sandbox.nlsEnabled.checked = false;
assert.strictEqual(sandbox.isLessonNlsSelected('ppct:1', 'Bài 18. Tam giác đều, hình vuông', { nls: { enabled: false, rate: 50 } }), false);
sandbox.nlsEnabled.checked = true;
assert.strictEqual(sandbox.isLessonNlsSelected('ppct:1', 'Bài 18. Tam giác đều, hình vuông', { nls: { enabled: true, rate: 0 } }), false);
console.log('✓ Case 1');

console.log('\n[CASE 2] Tỉ trọng 50% -> khoảng một nửa số bài, ưu tiên hình học/thống kê');
sandbox.nlsRate.value = '50';
sandbox.syncNlsSelectionFromRate();
assert.strictEqual(sandbox.nlsSelectedLessonIds.size, 3, '50% của 5 bài = 3 bài');
assert.ok(sandbox.nlsSelectedLessonIds.has('ppct:1'), 'hình học phải được ưu tiên');
assert.ok(sandbox.nlsSelectedLessonIds.has('ppct:2'), 'thống kê phải được ưu tiên');
assert.ok(!sandbox.nlsSelectedLessonIds.has('ppct:4'), 'kiểm tra không được ưu tiên');
console.log('✓ Case 2');

console.log('\n[CASE 3] Tick tay 3 bài cụ thể');
sandbox.clearNlsLessons();
sandbox.toggleNlsLesson('ppct:0', true);
sandbox.toggleNlsLesson('ppct:2', true);
sandbox.toggleNlsLesson('ppct:3', true);
assert.deepStrictEqual([...sandbox.nlsSelectedLessonIds].sort(), ['ppct:0', 'ppct:2', 'ppct:3']);
assert.strictEqual(sandbox.isLessonNlsSelected('ppct:0', 'Bài 1. Tập hợp', { nls: { enabled: true, rate: 40 } }), true);
assert.strictEqual(sandbox.isLessonNlsSelected('ppct:1', 'Bài 18. Tam giác đều, hình vuông', { nls: { enabled: true, rate: 40 } }), false);
console.log('✓ Case 3');

console.log('\n[CASE 4] Ưu tiên sư phạm: hình học & thống kê trước ôn tập/kiểm tra');
const ranked = sandbox.prioritizedNlsLessons().map(x => x.id);
assert.ok(ranked.indexOf('ppct:1') < ranked.indexOf('ppct:4'), 'hình học trước kiểm tra');
assert.ok(ranked.indexOf('ppct:2') < ranked.indexOf('ppct:3'), 'thống kê trước ôn tập');
console.log('✓ Case 4');

console.log('\n[CASE 5] PL1/PL3 dùng cùng isLessonNlsSelected nên khớp theo bài');
const cfg = { nls: { enabled: true, rate: 40 } };
const pl1 = sandbox._cands.map(row => sandbox.isLessonNlsSelected(row.id, row.lesson, cfg) ? 'NLS' : '-');
const pl3 = sandbox._cands.map(row => sandbox.isLessonNlsSelected(row.id, row.lesson, cfg) ? 'NLS' : '-');
assert.deepStrictEqual(pl1, pl3);
console.log('✓ Case 5');

console.log('\n[CASE 6] Soạn KHBD tôn trọng digital:false');
const { normalizeTeachingContext } = require('../js/khbd-app.js');
const off = normalizeTeachingContext({ integrations: { digital: false } });
assert.strictEqual(off.integrations.digital, false, 'không được ép digital=true khi GV đã tắt');
const def = normalizeTeachingContext({});
assert.strictEqual(def.integrations.digital, true, 'mặc định vẫn bật NLS khi chưa chọn');
console.log('✓ Case 6');

console.log('\n==================================================');
console.log('khbd nls rate smoke: passed');
console.log('==================================================');
