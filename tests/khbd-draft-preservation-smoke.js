'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

global.window = {
  addEventListener: () => {},
  removeEventListener: () => {},
  document: {},
  lucide: { createIcons: () => {} }
};

function createEl() {
  const el = {
    value: '',
    checked: false,
    textContent: '',
    innerHTML: '',
    children: [],
    style: {},
    classList: { add() {}, remove() {}, contains() { return false; }, toggle() {} },
    dataset: {},
    options: [],
    addEventListener() {},
    appendChild(child) { el.children.push(child); return child; },
    append(...items) { items.forEach(item => el.appendChild(item)); },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    replaceChildren(...items) { el.innerHTML = ''; el.children = []; items.forEach(item => el.appendChild(item)); }
  };
  return el;
}

const domStore = {};
global.document = {
  addEventListener() {},
  createElement() { return createEl(); },
  getElementById(id) {
    if (!domStore[id]) domStore[id] = createEl();
    return domStore[id];
  },
  querySelector() { return null; },
  querySelectorAll() { return []; }
};

const lsStore = {};
global.localStorage = {
  getItem(k) { return Object.prototype.hasOwnProperty.call(lsStore, k) ? lsStore[k] : null; },
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
  Object.assign(global, require('../js/khbd-curriculum.js'));
} catch (e) {}
try {
  Object.assign(global, require('../js/khbd-pedagogy-catalog.js'));
} catch (e) {}
try {
  Object.assign(global, require('../js/khbd-prompts.js'));
} catch (e) {}
try {
  const { KHBD_STANDARDS } = require('../js/khbd-standards.js');
  global.KHBD_STANDARDS = KHBD_STANDARDS;
} catch (e) {}

const app = require('../js/khbd-app.js');
const src = fs.readFileSync(path.join(__dirname, '..', 'js', 'khbd-app.js'), 'utf8');

function seedSourceMaterials() {
  app.appState.content.vision = 'SGK OCR: Bài 1 Tập hợp các số tự nhiên. Tập hợp N...';
  app.appState.content.ppctAnalysis = 'PPCT tuần 1: Tập hợp';
  app.appState.teachingContext.ocrReady = true;
  app.appState.images = [{ id: 'img1', name: 'trang-1.png', dataUrl: 'data:image/png;base64,aaa' }];
  app.appState.pdfAttachments = [{ id: 'pdf1', name: 'sgk.pdf', dataUrl: 'data:application/pdf;base64,bbb' }];
  app.appState.ppctImages = [{ id: 'ppct1', name: 'ppct.png' }];
  app.appState.ppctPdfAttachments = [{ id: 'ppctpdf1', name: 'ppct.pdf' }];
}

function assertSourceKept(label) {
  assert.ok(String(app.appState.content.vision).includes('SGK OCR'), `${label}: vision phải được giữ`);
  assert.strictEqual(app.appState.images.length, 1, `${label}: images phải được giữ`);
  assert.strictEqual(app.appState.pdfAttachments.length, 1, `${label}: pdfAttachments phải được giữ`);
  assert.ok(String(app.appState.content.ppctAnalysis).includes('PPCT'), `${label}: ppctAnalysis phải được giữ`);
  assert.strictEqual(app.appState.ppctImages.length, 1, `${label}: ppctImages phải được giữ`);
  assert.strictEqual(app.appState.ppctPdfAttachments.length, 1, `${label}: ppctPdfAttachments phải được giữ`);
}

console.log('==================================================');
console.log('KIỂM THỬ BẢO TOÀN HỌC LIỆU SGK/PPCT KHI ĐỔI TÊN / CHUYỂN BÀI');
console.log('==================================================');

assert.match(src, /preserveSource = false/, 'emptyDraftForTarget phải có preserveSource mặc định false');
assert.match(src, /preserveSource = true/, 'switchDraft/applyDraftData phải mặc định preserveSource true');
assert.match(src, /function commitCustomTopicName\(topic\)/, 'phải tách commitCustomTopicName để đổi tên không xóa SGK');
assert.match(src, /autoDetectAndFillLessonMetadata\(\{ ocrText, silent: true \}\)/, 'OCR Mistral phải autofill metadata');
assert.match(src, /Đã xóa toàn bộ học liệu SGK/, 'nút xóa SGK phải xóa cả vision');

console.log('\n[CASE 1] Đổi tên bài (blur) sau OCR không được xóa vision/attachments...');
localStorage.clear();
app.emptyDraftForTarget({ grade: '6', lesson: '', topic: '' });
app.appState.selectedGrade = '6';
app.appState.selectedLesson = '';
app.appState.customTopic = '';
seedSourceMaterials();
app.commitCustomTopicName('Bài 1: Tập hợp');
assert.strictEqual(app.appState.customTopic, 'Bài 1: Tập hợp', 'Case 1: phải lưu tên bài mới');
assertSourceKept('Case 1');
console.log('✓ Case 1: đổi tên bài giữ nguyên học liệu.');

console.log('\n[CASE 2] Chọn bài mới chưa có draft từ dropdown phải kế thừa SGK...');
localStorage.clear();
app.emptyDraftForTarget({ grade: '6', lesson: '', topic: '' });
app.appState.selectedGrade = '6';
app.appState.customTopic = 'Bài tạm';
seedSourceMaterials();
app.switchDraft({ grade: '6', lesson: 'Bài 2: Số tự nhiên', topic: 'Bài 2: Số tự nhiên' });
assert.strictEqual(app.appState.customTopic, 'Bài 2: Số tự nhiên', 'Case 2: phải chuyển sang bài mới');
assertSourceKept('Case 2');
console.log('✓ Case 2: switchDraft bài mới kế thừa 100% học liệu.');

console.log('\n[CASE 3] Draft cũ không có vision không được đè OCR phiên hiện tại...');
localStorage.clear();
app.emptyDraftForTarget({ grade: '6', lesson: '', topic: '' });
seedSourceMaterials();
app.applyDraftData({
  selectedGrade: '6',
  selectedSubject: 'TOAN',
  selectedLesson: 'Bài cũ',
  customTopic: 'Bài cũ',
  teachingContext: {},
  content: {
    vision: '',
    ppctAnalysis: '',
    objectives: 'Mục tiêu cũ',
    materials: '',
    activities: {},
    illustrations: []
  }
}, { preserveSource: true });
assert.ok(String(app.appState.content.vision).includes('SGK OCR'), 'Case 3: vision phiên hiện tại phải được giữ');
assert.strictEqual(app.appState.content.objectives, 'Mục tiêu cũ', 'Case 3: nội dung soạn của draft cũ vẫn nạp');
assert.strictEqual(app.appState.images.length, 1, 'Case 3: ảnh RAM không bị xóa');
console.log('✓ Case 3: applyDraftData không đè vision rỗng lên OCR đang có.');

console.log('\n[CASE 4] emptyDraftForTarget mặc định vẫn reset sạch...');
app.appState.content.vision = 'SGK OCR còn lại';
app.appState.content.ppctAnalysis = 'PPCT còn lại';
app.appState.images = [{ id: 'keep' }];
app.appState.pdfAttachments = [{ id: 'keep-pdf' }];
app.appState.ppctImages = [{ id: 'keep-ppct' }];
app.appState.ppctPdfAttachments = [{ id: 'keep-ppct-pdf' }];
app.emptyDraftForTarget({ grade: '8', lesson: 'Bài 1', topic: 'Đơn thức' });
assert.strictEqual(app.appState.content.vision, '', 'Case 4: mặc định phải xóa vision');
assert.strictEqual(app.appState.content.ppctAnalysis, '', 'Case 4: mặc định phải xóa ppctAnalysis');
assert.strictEqual(app.appState.images.length, 0, 'Case 4: mặc định phải xóa images');
assert.strictEqual(app.appState.pdfAttachments.length, 0, 'Case 4: mặc định phải xóa pdfAttachments');
assert.strictEqual(app.appState.ppctImages.length, 0, 'Case 4: mặc định phải xóa ppctImages');
assert.strictEqual(app.appState.ppctPdfAttachments.length, 0, 'Case 4: mặc định phải xóa ppctPdfAttachments');
console.log('✓ Case 4: emptyDraftForTarget() không tham số vẫn reset sạch.');

console.log('\n[CASE 5] Autofill tên bài sau OCR...');
app.emptyDraftForTarget({ grade: '6', lesson: '', topic: '' });
app.appState.selectedGrade = '6';
app.appState.customTopic = '';
app.appState.selectedLesson = '';
const ocrText = `
# BÀI 1: TẬP HỢP CÁC SỐ TỰ NHIÊN
1. Khái niệm tập hợp
Tập hợp các số tự nhiên được kí hiệu là N...
`;
const detected = app.autoDetectAndFillLessonMetadata({ ocrText, silent: true });
assert.strictEqual(detected.topic, 'Bài 1: Tập hợp', 'Case 5: phải trích đúng tên bài từ OCR');
assert.strictEqual(app.appState.customTopic, 'Bài 1: Tập hợp', 'Case 5: appState.customTopic phải được điền');
assert.match(src, /await applyTextbookOcrResult\(ocrText[\s\S]{0,400}autoDetectAndFillLessonMetadata/, 'Case 5: readTextbookWithMistral phải gọi autofill ngay sau OCR');
console.log('✓ Case 5: autofill metadata sau OCR.');

console.log('\n==================================================');
console.log('khbd draft preservation smoke: passed');
console.log('==================================================');
