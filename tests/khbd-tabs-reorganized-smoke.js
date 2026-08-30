'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'soankhbd.html'), 'utf8');
const appSrc = fs.readFileSync(path.join(__dirname, '..', 'js', 'khbd-app.js'), 'utf8');

const ls = {};
global.localStorage = {
  getItem: k => (k in ls ? ls[k] : null),
  setItem: (k, v) => { ls[k] = String(v); },
  removeItem: k => { delete ls[k]; }
};
function fakeEl() {
  return {
    hidden: false, disabled: false, checked: false, value: '', textContent: '', innerHTML: '',
    style: {}, dataset: {}, children: [],
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    getAttribute() { return null; }, setAttribute() {}, removeAttribute() {},
    addEventListener() {}, querySelectorAll() { return []; }, querySelector() { return null; },
    replaceChildren() {}, appendChild() {}
  };
}
global.document = {
  getElementById() { return fakeEl(); },
  querySelector() { return fakeEl(); },
  querySelectorAll() { return []; },
  createElement() { return fakeEl(); },
  addEventListener() {}
};
global.window = { document: global.document, localStorage: global.localStorage, addEventListener() {} };

console.log('==================================================');
console.log('BẮT ĐẦU KIỂM THỬ TÁI CẤU TRÚC SUBTAB A–F');
console.log('==================================================');

console.log('-> 1. HTML Tab 4...');
assert.match(html, /data-act="A">A\. Mở đầu/);
assert.match(html, /data-act="B">B\. Hình thành Kiến thức/);
assert.match(html, /data-act="C">C\. Luyện tập/);
assert.match(html, /data-act="D">D\. Vận dụng &amp; Hướng dẫn tự học/);
assert.match(html, /data-act="E">E\. Hồ sơ học tập/);
assert.match(html, /data-act="F">🎨 F\. Hình minh họa SGK/);
assert.doesNotMatch(html, /data-act="E">E\. Hướng dẫn về nhà/);
assert.match(html, /id="activityIllustrationCard"/);
assert.match(html, /id="illustrationGalleryAct"/);
assert.match(html, /id="activityMarkdownCard"/);
console.log('  -> HTML: PASS');

console.log('-> 2. ACTIVITY_TITLES + migrate + ghép giáo án...');
const {
  ACTIVITY_TITLES,
  appState,
  migrateLegacyActivitiesPortfolio,
  activityKeysForFullPlan,
  getFullLessonPlanMarkdown,
  switchActivitySubtab
} = require('../js/khbd-app.js');

assert.strictEqual(ACTIVITY_TITLES.D.short, 'D. Vận dụng & Hướng dẫn tự học');
assert.match(ACTIVITY_TITLES.E.full, /Hồ sơ học tập/);
assert.match(ACTIVITY_TITLES.F.full, /Hình minh họa SGK/);
assert.doesNotMatch(ACTIVITY_TITLES.E.full, /HƯỚNG DẪN VỀ NHÀ/);

const migrated = migrateLegacyActivitiesPortfolio({
  A: 'a',
  E: '',
  F: '# F. HỒ SƠ DẠY HỌC\n## 1. PHIẾU HỌC TẬP SỐ 1'
});
assert.match(migrated.E, /PHIẾU HỌC TẬP/);
assert.strictEqual(migrated.F, '');

const clearedHomework = migrateLegacyActivitiesPortfolio({
  E: '## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ (4 phút)\n1. Ôn tập kiến thức: ...',
  F: '## 1. PHIẾU HỌC TẬP SỐ 1\nNội dung phiếu'
});
assert.match(clearedHomework.E, /PHIẾU HỌC TẬP/);
assert.doesNotMatch(clearedHomework.E, /HƯỚNG DẪN VỀ NHÀ/);

assert.deepStrictEqual(activityKeysForFullPlan(appState.content), ['A', 'B', 'C', 'D']);

appState.content.activities.A = '## A. HOẠT ĐỘNG 1: MỞ ĐẦU (8 phút)\nMở đầu';
appState.content.activities.B = '## B. HOẠT ĐỘNG 2 (45 phút)\nB';
appState.content.activities.C = '## C. HOẠT ĐỘNG 3 (25 phút)\nC';
appState.content.activities.D = '## D. HOẠT ĐỘNG 4: VẬN DỤNG & HƯỚNG DẪN TỰ HỌC (12 phút)\nD';
appState.content.activities.E = '# E. HỒ SƠ DẠY HỌC & PHIẾU HỌC TẬP (PHỤ LỤC)\nPhiếu 1';
const full = getFullLessonPlanMarkdown({ includeHeader: false });
assert.match(full, /III\. TIẾN TRÌNH DẠY HỌC/);
assert.match(full, /VẬN DỤNG & HƯỚNG DẪN TỰ HỌC/);
assert.match(full, /IV\. PHỤ LỤC/);
assert.match(full, /Phiếu 1/);
assert.doesNotMatch(full, /HOẠT ĐỘNG 5/);
console.log('  -> Titles / migrate / markdown: PASS');

console.log('-> 3. switchActivitySubtab ẩn/hiện panel F...');
const store = {};
['activityMarkdownCard', 'activityIllustrationCard', 'currentActTitle', 'editorActLabel', 'editorActivity', 'previewActivity', 'btnGenerateCurrentAct'].forEach(id => {
  store[id] = {
    id,
    hidden: id === 'activityIllustrationCard',
    classList: { add() {}, remove() {}, contains() { return false; } },
    textContent: '',
    innerHTML: '',
    value: '',
    children: [],
    replaceChildren() {},
    appendChild() {},
    getAttribute() { return null; }
  };
});
const actBtns = ['A', 'B', 'C', 'D', 'E', 'F'].map(k => ({
  getAttribute: () => k,
  classList: { add() {}, remove() {}, contains() { return false; } }
}));
global.document.querySelectorAll = (sel) => (sel === '.act-tab-btn' ? actBtns : []);
const prevGet = global.document.getElementById;
global.document.getElementById = (id) => store[id] || (typeof prevGet === 'function' ? prevGet(id) : { classList: { add() {}, remove() {} }, textContent: '', innerHTML: '', value: '' });

switchActivitySubtab('F');
assert.strictEqual(appState.activeActSubtab, 'F');
assert.strictEqual(store.activityMarkdownCard.hidden, true);
assert.strictEqual(store.activityIllustrationCard.hidden, false);
assert.match(store.currentActTitle.textContent, /Hình minh họa/);

switchActivitySubtab('E');
assert.strictEqual(store.activityMarkdownCard.hidden, false);
assert.strictEqual(store.activityIllustrationCard.hidden, true);
assert.match(store.currentActTitle.textContent, /Hồ sơ học tập/);
console.log('  -> switchActivitySubtab: PASS');

assert.match(appSrc, /GENERATE_PORTFOLIO_WORKSHEETS/);
assert.match(appSrc, /actKey === "E" \? "GENERATE_PORTFOLIO_WORKSHEETS"/);
assert.match(appSrc, /migrateLegacyActivitiesPortfolio/);

console.log('==================================================');
console.log('TẤT CẢ TEST TÁI CẤU TRÚC TAB ĐỀU ĐẠT (PASS)!');
console.log('==================================================');
