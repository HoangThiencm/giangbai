'use strict';
const assert = require('assert');
const { calculateActivityTimeBudgets, normalizeTextbookSubsectionProfiles, getPromptTemplate } = require('../js/khbd-prompts.js');

for (const duration of ['01 tiết (45 phút)', '02 tiết (90 phút)']) {
  const result = calculateActivityTimeBudgets(duration, 3, 6, { fourActivities: true, subsectionWeights: [1, 3, 1] });
  assert.strictEqual(result.B_subsections.reduce((a, b) => a + b, 0), result.B);
  assert.ok(result.B_subsections[1] > result.B_subsections[0]);
  assert.ok(result.B_subsections[1] > result.B_subsections[2]);
  assert.ok(result.B_subsections.every(minutes => minutes >= 3), 'Mỗi nhánh phải có định mức nền khả dụng');
  assert.strictEqual(result.A + result.B + result.C + result.D, result.totalMinutes);
}
const legacy = calculateActivityTimeBudgets('02 tiết (90 phút)', 3, 6, { fourActivities: true, subsectionWeights: [1, 0, NaN] });
assert.deepStrictEqual(legacy.B_subsections, [Math.ceil(legacy.B / 3), Math.floor((legacy.B + 1) / 3), Math.floor(legacy.B / 3)]);
const profiles = normalizeTextbookSubsectionProfiles([{ title: 'Khái niệm', complexity: 2, signals: ['khái niệm mới'] }, { title: 'Vận dụng nhiều bước', complexity: 3, signals: ['nhiều bước', 'thực hành'] }]);
assert.strictEqual(profiles.length, 2);
assert.ok(profiles[1].weight > profiles[0].weight);
const clipped = calculateActivityTimeBudgets('02 tiết (90 phút)', 3, 6, { fourActivities: true, subsectionWeights: [1, 99, 1] });
assert.ok(clipped.B_subsections[1] < clipped.B - 6, 'Trọng số bất thường phải được chặn trước khi phân bổ');
const canvasPrompt = getPromptTemplate('GENERATE_ACTIVITY_B', {
  subjectName: 'Toán', grade: 6, duration: '02 tiết (90 phút)', topic: 'Bài có cấu trúc',
  textbook_content: '## Ngữ cảnh SGK đã phân tích\n- Chủ đề: Bài có cấu trúc',
  subsectionProfiles: [
    { title: 'Khái niệm nền', weight: 1, complexity: 1 },
    { title: 'Quy trình nhiều bước', weight: 3, complexity: 3, signals: ['nhiều bước'] },
    { title: 'Vận dụng', weight: 1, complexity: 1 }
  ]
});
assert.match(canvasPrompt, /Hoạt động 2\.2: Quy trình nhiều bước \(\d+ phút\)/);
assert.match(canvasPrompt, /Hoạt động 2\.1: Khái niệm nền \(\d+ phút\)/);
const branchMinutes = Array.from(canvasPrompt.matchAll(/Hoạt động 2\.\d+:[^\n]*\((\d+) phút\)/g), m => Number(m[1]));
assert.strictEqual(branchMinutes.slice(-3).reduce((a, b) => a + b, 0), calculateActivityTimeBudgets('02 tiết (90 phút)', 3, 6, { fourActivities: true, subsectionWeights: [1, 3, 1] }).B);
assert.ok(branchMinutes[branchMinutes.length - 2] > branchMinutes[branchMinutes.length - 3]);
console.log('khbd weighted duration: PASS');
