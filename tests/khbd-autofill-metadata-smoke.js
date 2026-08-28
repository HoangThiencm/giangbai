'use strict';

const assert = require('assert');

// 1. Mock DOM and localStorage
const lsStore = {};
global.localStorage = {
  getItem(k) { return lsStore[k] || null; },
  setItem(k, v) { lsStore[k] = String(v); },
  removeItem(k) { delete lsStore[k]; },
  clear() { Object.keys(lsStore).forEach(k => delete lsStore[k]); }
};

const domElements = {
  inputTopicCustom: { value: '' },
  inputLessonScope: { value: '' },
  inputDuration: { value: '' },
  toggleAiCompetency: { checked: false },
  selectMyDraft: { innerHTML: '', value: '' },
  selectGrade: { value: '6' }
};

global.window = {
  addEventListener: () => {},
  document: {}
};

global.document = {
  addEventListener: () => {},
  getElementById: (id) => domElements[id] || null,
  querySelectorAll: () => []
};

global.showToast = () => {};

const {
  appState,
  extractLessonTitleFromOcr,
  autoDetectAndFillLessonMetadata,
  parsePpctLessonDetails
} = require('../js/khbd-app.js');

console.log('==================================================');
console.log('BẮT ĐẦU KIỂM THỬ AI TỰ ĐỘNG ĐIỀN THÔNG TIN BÀI DẠY (AUTOFILL METADATA)');
console.log('==================================================');

// 1. Kiểm tra trích xuất tiêu đề bài học từ OCR SGK: extractLessonTitleFromOcr
console.log('-> 1. Kiểm tra extractLessonTitleFromOcr...');

const ocrText1 = `
# BÀI 1: TẬP HỢP CÁC SỐ TỰ NHIÊN
1. Khái niệm tập hợp
Tập hợp các số tự nhiên được kí hiệu là N...
`;
assert.strictEqual(extractLessonTitleFromOcr(ocrText1), 'Bài 1: TẬP HỢP CÁC SỐ TỰ NHIÊN');

const ocrText2 = `
**BÀI 15: BIỂU THỨC ĐẠI SỐ** (2 tiết)
Nội dung bài học gồm có hai phần...
`;
assert.strictEqual(extractLessonTitleFromOcr(ocrText2), 'Bài 15: BIỂU THỨC ĐẠI SỐ');

const ocrText3 = `
### CHỦ ĐỀ 3: HÌNH HỌC TRỰC QUAN
Các hình khối trong thực tiễn
`;
assert.strictEqual(extractLessonTitleFromOcr(ocrText3), 'Bài 3: HÌNH HỌC TRỰC QUAN');

const ocrText4 = `
# Phương trình bậc nhất một ẩn
Khái niệm về phương trình bậc nhất...
`;
assert.strictEqual(extractLessonTitleFromOcr(ocrText4), 'Phương trình bậc nhất một ẩn');

console.log('  -> extractLessonTitleFromOcr: PASS');

// 2. Kiểm tra trích xuất chi tiết từ bảng PPCT: parsePpctLessonDetails
console.log('-> 2. Kiểm tra parsePpctLessonDetails...');

const ppctTableSample = `
| TT | Tên bài học | Tiết PPCT | Số tiết | Ghi chú |
|---|---|---|---|---|
| 1 | Bài 1: Tập hợp các số tự nhiên | Tiết 1, 2 | 2 | Tích hợp GD Năng lực AI |
| 2 | Bài 2: Phép cộng và phép trừ số tự nhiên | Tiết 3, 4, 5 | 3 | Dùng GeoGebra |
`;

const details1 = parsePpctLessonDetails(ppctTableSample, 'Bài 1: Tập hợp các số tự nhiên');
assert.strictEqual(details1.lessonScopeSuggestion, 'Tiết 1, 2', 'Phạm vi tiết phải là "Tiết 1, 2"');
assert.strictEqual(details1.durationSuggestion, '2', 'Số tiết phải là 2');
assert.strictEqual(details1.hasAiIntegration, true, 'Phải phát hiện ghi chú AI');

const details2 = parsePpctLessonDetails(ppctTableSample, 'Phép cộng và phép trừ số tự nhiên');
assert.strictEqual(details2.lessonScopeSuggestion, 'Tiết 3, 4, 5', 'Phạm vi tiết phải là "Tiết 3, 4, 5"');
assert.strictEqual(details2.durationSuggestion, '3', 'Số tiết phải là 3');

console.log('  -> parsePpctLessonDetails: PASS');

// 3. Kiểm tra toàn luồng autoDetectAndFillLessonMetadata
console.log('-> 3. Kiểm tra autoDetectAndFillLessonMetadata...');

appState.selectedGrade = '6';
appState.selectedLesson = '';
appState.customTopic = '';
appState.duration = '';
appState.teachingContext.lessonScope = '';
appState.teachingContext.integrations.ai = false;

const result = autoDetectAndFillLessonMetadata({
  ocrText: ocrText1,
  ppctText: ppctTableSample,
  silent: true
});

assert.strictEqual(result.topic, 'Bài 1: TẬP HỢP CÁC SỐ TỰ NHIÊN', 'Topic phải tự động nhận diện từ OCR');
assert.strictEqual(result.lessonScope, 'Tiết 1, 2', 'LessonScope phải nhận diện từ PPCT');
assert.strictEqual(result.duration, '02 tiết (90 phút)', 'Thời lượng lớp 6 (2 tiết) phải là 90 phút');
assert.strictEqual(result.hasAiIntegration, true, 'Năng lực AI phải được phát hiện');

assert.strictEqual(appState.customTopic, 'Bài 1: TẬP HỢP CÁC SỐ TỰ NHIÊN');
assert.strictEqual(appState.teachingContext.lessonScope, 'Tiết 1, 2');
assert.strictEqual(appState.duration, '02 tiết (90 phút)');
assert.strictEqual(appState.teachingContext.integrations.ai, true);

console.log('  -> autoDetectAndFillLessonMetadata: PASS');

console.log('==================================================');
console.log('TẤT CẢ KIỂM THỬ AUTOFILL METADATA ĐỀU ĐẠT 100% (PASS)!');
console.log('==================================================');
