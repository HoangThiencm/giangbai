'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

console.log('================================================================');
console.log('KIỂM THỬ: Nhận diện bài Luyện tập / Ôn tập + xóa prompt leak YCCĐ');
console.log('================================================================');

const root = path.join(__dirname, '..');
const promptsSrc = fs.readFileSync(path.join(root, 'js', 'khbd-prompts.js'), 'utf8');
const appSrc = fs.readFileSync(path.join(root, 'js', 'khbd-app.js'), 'utf8');

// --- 1. isReviewOrPracticeLesson nhận diện đúng ---
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

const {
  isReviewOrPracticeLesson,
  isPracticeOrReviewLesson,
  getPromptTemplate,
  PROMPTS
} = sandbox.module.exports;

assert.equal(typeof isReviewOrPracticeLesson, 'function', 'phải export isReviewOrPracticeLesson');
assert.equal(typeof isPracticeOrReviewLesson, 'function', 'phải giữ alias isPracticeOrReviewLesson');

assert.strictEqual(isReviewOrPracticeLesson('Bài tập cuối chương I'), true);
assert.strictEqual(isReviewOrPracticeLesson('Luyện tập chung trang 21'), true);
assert.strictEqual(isReviewOrPracticeLesson('Ôn tập chương 2'), true);
assert.strictEqual(isReviewOrPracticeLesson('Ôn tập học kỳ I'), true);
assert.strictEqual(isReviewOrPracticeLesson('Thực hành tổng hợp'), true);
assert.strictEqual(isReviewOrPracticeLesson('Bài 1. Phương trình bậc nhất'), false);
assert.strictEqual(isReviewOrPracticeLesson('Tập hợp các số tự nhiên'), false);
assert.strictEqual(isPracticeOrReviewLesson('Luyện tập chung'), true, 'alias phải khớp');
console.log('✓ isReviewOrPracticeLesson nhận diện đúng các dạng bài ôn/luyện tập');

// --- 2. GENERATE_ACTIVITY_B / C đổi tiêu đề khi là bài ôn tập ---
const reviewCtx = {
  subject: 'toan',
  subjectName: 'Toán',
  grade: '6',
  gradeLevelName: 'THCS',
  topic: 'Ôn tập chương 2',
  duration: '02 tiết (90 phút)',
  textbook_content: 'Bài 1. Tính...\nBài 2. Giải...'
};
const promptB = getPromptTemplate('GENERATE_ACTIVITY_B', reviewCtx);
assert.match(promptB, /LUYỆN TẬP \(HỆ THỐNG HÓA KIẾN THỨC VÀ CHỮA CÁC BÀI TẬP TRỌNG TÂM TRONG SGK\)/, 'Mục B phải đổi tiêu đề LUYỆN TẬP khi ôn tập');
assert.match(promptB, /ĐÂY LÀ TIẾT LUYỆN TẬP \/ ÔN TẬP/, 'Mục B phải có chỉ dẫn tiết luyện tập/ôn tập');
assert.match(promptB, /Chữa Bài tập/, 'Mục B phải hướng dẫn chia nhánh theo bài tập SGK');
assert.doesNotMatch(promptB, /## B\. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI/, 'Mục B ôn tập không còn tiêu đề hình thành kiến thức mới');

const promptC = getPromptTemplate('GENERATE_ACTIVITY_C', reviewCtx);
assert.match(
  promptC,
  /LUYỆN TẬP NÂNG CAO VÀ VẬN DỤNG CÁC BÀI TẬP CÒN LẠI TRONG SGK/,
  'Mục C phải đổi tiêu đề nâng cao khi ôn tập'
);

const theoryCtx = { ...reviewCtx, topic: 'Bài 1. Phương trình bậc nhất' };
const promptBTheory = getPromptTemplate('GENERATE_ACTIVITY_B', theoryCtx);
assert.match(promptBTheory, /HÌNH THÀNH KIẾN THỨC MỚI/, 'Bài lý thuyết giữ tiêu đề hình thành kiến thức mới');
assert.doesNotMatch(promptBTheory, /ĐÂY LÀ TIẾT LUYỆN TẬP \/ ÔN TẬP \/ BÀI TẬP CUỐI CHƯƠNG/, 'Bài lý thuyết không gắn chỉ dẫn ôn tập');
console.log('✓ GENERATE_ACTIVITY_B/C đổi tiêu đề đúng theo thể loại bài');

// --- 3. Prompt leak YCCĐ không còn trong template + sanitize gọt sạch ---
assert.doesNotMatch(
  PROMPTS.GENERATE_OBJECTIVES,
  /\(Các YCCĐ của bài học theo CT GDPT 2018; mỗi ý một gạch đầu dòng, giữ động từ hành vi\.\)/,
  'Template GENERATE_OBJECTIVES phải xóa dòng prompt leak YCCĐ'
);

const promptObjReview = getPromptTemplate('GENERATE_OBJECTIVES', reviewCtx);
assert.match(promptObjReview, /ĐÂY LÀ BÀI LUYỆN TẬP \/ ÔN TẬP/, 'Mục tiêu bài ôn tập phải có chỉ dẫn củng cố/hệ thống hóa');
assert.doesNotMatch(promptObjReview, /\(Các YCCĐ của bài học theo CT GDPT 2018/, 'Prompt mục tiêu không còn leak YCCĐ');

assert.match(appSrc, /Các YCCĐ\|mỗi ý một gạch đầu dòng/, 'sanitizeLessonMarkdown phải có regex lọc prompt leak YCCĐ');
assert.match(appSrc, /function isReviewOrPracticeLesson\s*\(/, 'khbd-app.js phải có isReviewOrPracticeLesson');
assert.match(appSrc, /B\. Luyện tập & Chữa bài tập SGK/, 'khbd-app.js phải đổi nhãn tab B khi bài ôn tập');
assert.match(appSrc, /syncActivityBTabLabels/, 'khbd-app.js phải sync nhãn tab B');
assert.match(
  appSrc,
  /!hasAnalyzedLessonContent\(\)\s*&&\s*hasTextbookMedia\(\)[\s\S]*?handleAnalyzeSourceMaterials\(\{\s*internal:\s*true\s*\}\)/,
  '1-Click phải tự đọc SGK khi có media chưa OCR (internal: true)'
);

const store = {};
global.localStorage = {
  getItem: (key) => (key in store ? store[key] : null),
  setItem: (key, value) => { store[key] = String(value); },
  removeItem: (key) => { delete store[key]; }
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

const { sanitizeLessonMarkdown, isReviewOrPracticeLesson: appIsReview } = require('../js/khbd-app.js');
assert.equal(typeof sanitizeLessonMarkdown, 'function');
assert.strictEqual(appIsReview('Ôn tập chương 2'), true);

const leaked = `# I. MỤC TIÊU

## 1. Về kiến thức
(Các YCCĐ của bài học theo CT GDPT 2018; mỗi ý một gạch đầu dòng, giữ động từ hành vi.)
- Hệ thống hoá kiến thức chương 2.

## 2. Về năng lực
- Giải quyết vấn đề: vận dụng công thức đã học.`;
const cleaned = sanitizeLessonMarkdown(leaked);
assert.doesNotMatch(cleaned, /Các YCCĐ của bài học theo CT GDPT 2018/, 'sanitize phải gọt sạch dòng leak YCCĐ');
assert.ok(cleaned.includes('Hệ thống hoá kiến thức chương 2.'), 'sanitize giữ nội dung mục tiêu thật');
console.log('✓ Prompt leak YCCĐ đã xóa khỏi template và được sanitize gọt sạch');

console.log('================================================================');
console.log('PASS 100%: khbd-review-practice-lesson-smoke.js');
console.log('================================================================');
