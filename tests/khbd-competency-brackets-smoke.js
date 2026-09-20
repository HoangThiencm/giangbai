'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const { getPromptTemplate, PROMPTS } = require('../js/khbd-prompts.js');

const store = {};
global.localStorage = {
  getItem: key => (key in store ? store[key] : null),
  setItem: (key, value) => { store[key] = String(value); },
  removeItem: key => { delete store[key]; }
};
function fakeEl() {
  return {
    addEventListener() {},
    value: '',
    checked: false,
    textContent: '',
    innerHTML: '',
    style: {},
    classList: { add() {}, remove() {}, contains() { return false; } },
    querySelectorAll() { return []; },
    appendChild() {},
    append() {},
    replaceChildren() {},
    disabled: false,
    hidden: false,
    dataset: {},
    children: [],
    setAttribute() {},
    getAttribute() { return null; }
  };
}
const documentMock = {
  addEventListener() {},
  getElementById() { return fakeEl(); },
  querySelectorAll() { return []; },
  querySelector() { return fakeEl(); },
  createElement() { return fakeEl(); }
};
global.document = documentMock;
global.window = {
  addEventListener() {},
  localStorage,
  document: documentMock,
  confirm: () => true,
  lucide: { createIcons() {} }
};
global.geminiAPI = { apiKeys: [], onKeyRotatedCallback: null, onStatusCallback: null, syncKeysFromServer: async () => [] };

const { stripSquareBracketsFromCompetencies } = require('../js/khbd-app.js');

const generateObjectives = String(PROMPTS.GENERATE_OBJECTIVES || '');
assert.ok(
  !generateObjectives.includes('- [Tên năng lực chung 1') && !generateObjectives.includes('- [Tên năng lực]:'),
  'GENERATE_OBJECTIVES không được dùng mẫu - [Tên năng lực...'
);
assert.ok(
  generateObjectives.includes('TUYỆT ĐỐI CẤM dùng dấu ngoặc vuông [ ]'),
  'GENERATE_OBJECTIVES phải có chỉ thị cấm ngoặc vuông'
);

const runtimePrompt = getPromptTemplate('GENERATE_OBJECTIVES', {
  subject: 'toan',
  subjectName: 'Toán',
  topic: 'Đơn thức',
  duration: '1 tiết',
  textbook_content: '',
  yccd_official: '',
  pedagogical_context: ''
});
assert.ok(
  !runtimePrompt.includes('- [Tên năng lực]:'),
  "getPromptTemplate('GENERATE_OBJECTIVES') không được chứa - [Tên năng lực]:"
);
assert.ok(
  runtimePrompt.includes('TUYỆT ĐỐI CẤM dùng dấu ngoặc vuông [ ]'),
  'getPromptTemplate phải inject chỉ thị cấm ngoặc vuông'
);

const sample = `## 2. Về năng lực
### a) Năng lực chung
- [Tự chủ và tự học]: Học sinh tự lực thực hiện các nhiệm vụ cá nhân.
- [Giải quyết vấn đề và sáng tạo]: Học sinh phát hiện quy luật.
### b) Năng lực đặc thù môn học
- [Tư duy và lập luận toán học]: Học sinh thực hiện thao tác so sánh.
- [Mô hình hóa toán học]: Học sinh sử dụng đơn thức.
### c) Năng lực số
- ***[5.3.TC2a]:*** Mô tả nhiệm vụ số
### d) Năng lực AI
- ***[9.B2.1]:*** Mô tả nhiệm vụ AI
## 3. Về phẩm chất
- [Chăm chỉ]: Tích cực phát biểu xây dựng bài.`;

const cleaned = stripSquareBracketsFromCompetencies(sample);
assert.ok(cleaned.includes('- Tự chủ và tự học: Học sinh tự lực'), 'phải bỏ [] ở năng lực chung');
assert.ok(cleaned.includes('- Giải quyết vấn đề và sáng tạo: Học sinh phát hiện'), 'phải bỏ [] ở GQVĐ');
assert.ok(cleaned.includes('- Tư duy và lập luận toán học: Học sinh thực hiện'), 'phải bỏ [] ở NL đặc thù');
assert.ok(cleaned.includes('- Mô hình hóa toán học: Học sinh sử dụng'), 'phải bỏ [] ở mô hình hóa');
assert.ok(cleaned.includes('- Chăm chỉ: Tích cực phát biểu'), 'phải bỏ [] ở phẩm chất');
assert.ok(!cleaned.includes('[Tự chủ') && !cleaned.includes('[Tư duy'), 'không còn [Tự chủ / [Tư duy');
assert.ok(cleaned.includes('***[5.3.TC2a]:***'), 'phải giữ nguyên mã NLS');
assert.ok(cleaned.includes('***[9.B2.1]:***'), 'phải giữ nguyên mã AI');

const appSrc = fs.readFileSync(path.join(__dirname, '../js/khbd-app.js'), 'utf8');
assert.ok(
  /finalResult\s*=\s*stripSquareBracketsFromCompetencies\(finalResult\)/.test(appSrc),
  'applyObjectivesOutput phải gọi stripSquareBracketsFromCompetencies'
);
assert.ok(
  /window\.stripSquareBracketsFromCompetencies\s*=\s*stripSquareBracketsFromCompetencies/.test(appSrc),
  'phải export window.stripSquareBracketsFromCompetencies'
);

console.log('khbd-competency-brackets-smoke: passed');
