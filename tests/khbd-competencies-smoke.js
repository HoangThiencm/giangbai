'use strict';

const assert = require('assert');
const {
  getGeneralCompetenciesForSubject,
  formatGeneralCompetenciesGuide,
  getPromptTemplate
} = require('../js/khbd-prompts.js');

const toan = getGeneralCompetenciesForSubject('toan');
assert.strictEqual(toan[0].name, 'Giải quyết vấn đề và sáng tạo');

const guideToan = formatGeneralCompetenciesGuide('toan', {});
assert.ok(guideToan.includes('Ưu tiên: **Giải quyết vấn đề và sáng tạo**'));
assert.ok(guideToan.includes('Ưu tiên: **Tự chủ và tự học**'));
assert.ok(guideToan.includes('chỉ chọn nếu bài thực sự thể hiện'));
assert.ok(!/1\. \*\*Giải quyết/.test(guideToan), 'Không đánh số 1. 2. 3. cả ba năng lực');
assert.ok((guideToan.match(/Ưu tiên:/g) || []).length === 2, 'Chỉ inject 2 năng lực ưu tiên');

const talk = formatGeneralCompetenciesGuide('toan', { pedagogical_context: 'Kỹ thuật Think-Pair-Share, thảo luận nhóm' });
assert.ok(talk.startsWith('- Ưu tiên: **Giao tiếp và hợp tác**'), 'Thảo luận đẩy Giao tiếp lên ưu tiên');

const make = formatGeneralCompetenciesGuide('nguvan', { methods: ['dự án', 'thực hành đo đạc'] });
assert.ok(make.startsWith('- Ưu tiên: **Giải quyết vấn đề và sáng tạo**'), 'Dự án/thực hành đẩy GQVĐ lên với môn ngôn ngữ');

const prompt = getPromptTemplate('GENERATE_OBJECTIVES', {
  subject: 'toan',
  subjectName: 'Toán',
  topic: 'Tập hợp',
  duration: '2 tiết',
  textbook_content: '',
  yccd_official: '',
  pedagogical_context: ''
});
assert.ok(prompt.includes('Ưu tiên: **Giải quyết vấn đề và sáng tạo**'));
assert.ok(prompt.includes('CẤM liệt kê cho đủ khung'));

const promptB = getPromptTemplate('GENERATE_ACTIVITY_B', {
  subjectName: 'Toán',
  topic: 'Tập hợp',
  textbook_content: 'Mục 1: Khái niệm',
  objectives_content: ''
});
assert.ok(promptB.includes('lỗi sai điển hình'));
assert.ok(promptB.includes('CẤM lỗi generic'));
assert.ok(!/\* \+ Bước 1: Chuyển giao nhiệm vụ: \.\.\./.test(promptB), 'Không dùng ... làm ví dụ bước');

console.log('khbd-competencies-smoke: passed');
