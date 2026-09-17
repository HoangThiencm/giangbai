'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

console.log('================================================================');
console.log('KIỂM THỬ: soankhbd.html — 2 chế độ soạn + nút 1-CLICK');
console.log('================================================================');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'soankhbd.html'), 'utf8');
const appSrc = fs.readFileSync(path.join(root, 'js', 'khbd-app.js'), 'utf8');
const promptsSrc = fs.readFileSync(path.join(root, 'js', 'khbd-prompts.js'), 'utf8');

// 1. HTML: nút 1-Click và dropdown chế độ soạn
assert.ok(html.includes('id="btn1ClickGenerate"'), 'soankhbd.html phải có #btn1ClickGenerate');
assert.ok(html.includes('TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)'), 'soankhbd.html phải có nhãn nút 1-Click');
assert.ok(html.includes('id="selectGenerationMode"'), 'soankhbd.html phải có #selectGenerationMode');
assert.match(html, /id="selectGenerationMode"[\s\S]*?value="detailed" selected/, 'Mặc định phải là detailed');
assert.match(html, /id="selectGenerationMode"[\s\S]*?value="compact"/, 'Phải có tùy chọn compact');
assert.ok(
  html.indexOf('id="btn1ClickGenerate"') < html.indexOf('id="btnCancelGeneration"'),
  'Nút 1-Click phải đứng trước btnCancelGeneration trong header-actions'
);
assert.ok(
  html.indexOf('id="selectSubject"') < html.indexOf('id="selectGenerationMode"')
    && html.indexOf('id="selectGenerationMode"') < html.indexOf('id="selectLesson"'),
  'selectGenerationMode phải nằm giữa Môn học và Danh mục bài học'
);
console.log('✓ HTML: #btn1ClickGenerate + #selectGenerationMode đúng vị trí');

// 2. khbd-app.js: state, localStorage, 1-Click handler
assert.match(appSrc, /generationMode:\s*\(typeof localStorage/, 'appState phải khởi tạo generationMode từ localStorage');
assert.match(appSrc, /khbd_generation_mode/, 'phải dùng key localStorage khbd_generation_mode');
assert.match(appSrc, /function getGenerationMode\s*\(/, 'phải có getGenerationMode');
assert.match(appSrc, /function setGenerationMode\s*\(/, 'phải có setGenerationMode');
assert.match(appSrc, /function resolveGenerationMode\s*\(/, 'phải có resolveGenerationMode');
assert.match(appSrc, /async function handle1ClickGenerate\s*\(/, 'phải có handle1ClickGenerate');
assert.match(appSrc, /btn1ClickGenerate[\s\S]*?addEventListener\("click",\s*handle1ClickGenerate\)/, 'phải gắn click #btn1ClickGenerate');
assert.match(appSrc, /selectGenerationMode[\s\S]*?addEventListener\("change"/, 'phải lắng nghe change #selectGenerationMode');
assert.match(appSrc, /getGenerationPromptContext\(\{\s*generationMode:\s*generationMode\s*\}\)/, '1-Click phải truyền generationMode vào prompt context');
assert.match(appSrc, /isCompact/, '1-Click phải phân nhánh chế độ rút gọn');
assert.match(appSrc, /!isCompact[\s\S]*GENERATE_PORTFOLIO_WORKSHEETS/, 'chi tiết mới chạy III.E');
assert.match(appSrc, /!isCompact[\s\S]*generateLessonIllustrations\(\{\s*silent:\s*true\s*\}\)/, 'chi tiết mới tạo hình minh họa SGK');
assert.match(appSrc, /switchMainTab\("tabFullPreview"\)/, '1-Click phải chuyển Tab Toàn bộ Giáo án');
assert.match(appSrc, /handle1ClickGenerate,/, 'handle1ClickGenerate phải được export');
console.log('✓ khbd-app.js: generationMode + handle1ClickGenerate');

// 3. Prompt compact trong khbd-prompts.js
assert.match(promptsSrc, /context\.generationMode\s*===\s*['"]compact['"]/, 'prompts phải xử lý generationMode compact');
assert.match(promptsSrc, /ACTIVITY_TABLE_CONTRACT_COMPACT/, 'prompts compact phải dùng ACTIVITY_TABLE_CONTRACT_COMPACT');
assert.match(promptsSrc, /RÀNG BUỘC CHẾ ĐỘ SOẠN RÚT GỌN/, 'prompts materials phải có ràng buộc rút gọn');

const sandbox = {
  console,
  module: { exports: {} },
  exports: {},
  require,
  CURRICULUM_DATA: {},
  SUBJECT_COMPETENCIES: {},
  KHBD_STANDARDS: {},
  getGradeLevel: () => 'thcs',
  getGradeLevelName: () => 'THCS',
  getSubjectDisplayName: () => 'Toán',
  getSubjectCompetencies: () => []
};
vm.createContext(sandbox);
vm.runInContext(promptsSrc, sandbox);
const getPromptTemplate = sandbox.getPromptTemplate || sandbox.module.exports.getPromptTemplate;
assert.equal(typeof getPromptTemplate, 'function', 'getPromptTemplate phải export được');

const baseCtx = {
  subject: 'toan',
  subjectName: 'Toán',
  grade: '6',
  gradeLevel: 'thcs',
  gradeLevelName: 'THCS',
  topic: 'Bài 1. Số tự nhiên',
  duration: '02 tiết (90 phút)',
  textbook_content: 'Nội dung SGK mẫu',
  objectives_content: '',
  activities_content: '',
  methods: [],
  techniques: [],
  digitalCompetencyEnabled: false,
  aiCompetencyEnabled: false,
  competencies: []
};

const detailed = getPromptTemplate('GENERATE_MATERIALS', { ...baseCtx, generationMode: 'detailed' });
const compact = getPromptTemplate('GENERATE_MATERIALS', { ...baseCtx, generationMode: 'compact' });
assert.ok(compact.includes('RÀNG BUỘC CHẾ ĐỘ SOẠN RÚT GỌN'), 'compact materials phải có ràng buộc rút gọn');
assert.ok(!detailed.includes('RÀNG BUỘC CHẾ ĐỘ SOẠN RÚT GỌN'), 'detailed materials không thêm ràng buộc rút gọn');

const compactAct = getPromptTemplate('GENERATE_ACTIVITY_A', { ...baseCtx, generationMode: 'compact' });
const detailedAct = getPromptTemplate('GENERATE_ACTIVITY_A', { ...baseCtx, generationMode: 'detailed' });
assert.ok(compactAct.length > 100, 'compact activity prompt không rỗng');
assert.ok(detailedAct.length > 100, 'detailed activity prompt không rỗng');
assert.notStrictEqual(compactAct, detailedAct, 'compact và detailed activity prompt phải khác nhau (bảng rút gọn)');
console.log('✓ khbd-prompts.js: generationMode compact trả nội dung rút gọn');

console.log('\n================================================================');
console.log('🎉 soankhbd-generation-mode-smoke PASS');
console.log('================================================================\n');
