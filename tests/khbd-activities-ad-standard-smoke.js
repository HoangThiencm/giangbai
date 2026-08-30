'use strict';

const assert = require('assert');
const {
  calculateActivityTimeBudgets,
  getPromptTemplate,
  PROMPTS
} = require('../js/khbd-prompts.js');
const {
  appState,
  getFullLessonPlanMarkdown,
  activityKeysForFullPlan
} = require('../js/khbd-app.js');

console.log('==================================================');
console.log('BẮT ĐẦU KIỂM THỬ 4 HOẠT ĐỘNG A–D CHUẨN CV 5512');
console.log('==================================================');

console.log('-> 1. Phân bổ 4 hoạt động A+B+C+D = 90 phút...');
const four = calculateActivityTimeBudgets('02 tiết (90 phút)', 2, 6, { fourActivities: true });
assert.strictEqual(four.totalMinutes, 90);
assert.strictEqual(four.E, 0, 'Chế độ 4 hoạt động không tách pha E');
assert.strictEqual(four.A + four.B + four.C + four.D, 90, 'A+B+C+D phải đúng 90');
assert.strictEqual(four.A, 8, 'A ~ 8 phút');
assert.strictEqual(four.B, 45, 'B ~ 45 phút');
assert.strictEqual(four.C, 25, 'C ~ 25 phút');
assert.strictEqual(four.D, 12, 'D ~ 12 phút');
assert.strictEqual(four.B_subsections.reduce((a, b) => a + b, 0), 45);

const five = calculateActivityTimeBudgets('02 tiết (90 phút)', 2, 6);
assert.strictEqual(five.E, 0, 'Mặc định chuẩn 4 hoạt động không tách pha E');
assert.strictEqual(five.A + five.B + five.C + five.D, 90);
console.log('  -> Time budget 4 hoạt động: PASS');

console.log('-> 2. Prompt GENERATE_ACTIVITIES_AD / GENERATE_ACTIVITY_D...');
const context = {
  subjectName: 'Toán',
  topic: 'Tập hợp các số tự nhiên',
  duration: '02 tiết (90 phút)',
  grade: '6',
  textbook_content: `
I. Số và tập hợp các số tự nhiên
Nội dung 1
II. Biểu diễn số tự nhiên trên tia số
Nội dung 2
  `,
  objectives_content: ''
};

const promptAd = getPromptTemplate('GENERATE_ACTIVITIES_AD', context);
assert.match(promptAd, /<<<KHBD_A>>>/);
assert.match(promptAd, /<<<KHBD_B>>>/);
assert.match(promptAd, /<<<KHBD_C>>>/);
assert.match(promptAd, /<<<KHBD_D>>>/);
assert.doesNotMatch(promptAd, /^<<<KHBD_E>>>/m);
assert.match(promptAd, /CẤM xuất <<<KHBD_E>>>/);
assert.match(promptAd, /## D\. HOẠT ĐỘNG 4: VẬN DỤNG & HƯỚNG DẪN TỰ HỌC \(12 phút\)/);
assert.match(promptAd, /Tổng A \+ B \+ C \+ D BẮT BUỘC đúng bằng toàn bộ thời lượng bài dạy 02 tiết \(90 phút\)/);
assert.match(promptAd, /Ôn tập/);
assert.match(promptAd, /Làm bài tập/);
assert.match(promptAd, /Chuẩn bị bài mới/);
assert.match(promptAd, /tìm tòi mở rộng/i);
assert.match(promptAd, /CẤM viết mục E/);
assert.notStrictEqual(PROMPTS.GENERATE_ACTIVITIES_AD, PROMPTS.GENERATE_ACTIVITIES_AE);

const promptD = getPromptTemplate('GENERATE_ACTIVITY_D', context);
assert.match(promptD, /## D\. HOẠT ĐỘNG 4: VẬN DỤNG & HƯỚNG DẪN TỰ HỌC \(12 phút\)/);
assert.match(promptD, /CẤM viết mục E/);
assert.match(promptD, /4 nhiệm vụ tự học/);
assert.match(promptD, /Nhiệm vụ tự học/);
console.log('  -> Prompt AD / D: PASS');

console.log('-> 3. getFullLessonPlanMarkdown ưu tiên A–D khi D đã có tự học...');
appState.content.activities.A = '## A. HOẠT ĐỘNG 1: MỞ ĐẦU (8 phút)\nMở đầu';
appState.content.activities.B = '## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (45 phút)\nHình thành';
appState.content.activities.C = '## C. HOẠT ĐỘNG 3: LUYỆN TẬP (25 phút)\nLuyện tập';
appState.content.activities.D = `## D. HOẠT ĐỘNG 4: VẬN DỤNG & HƯỚNG DẪN TỰ HỌC (12 phút)
### a) Mục tiêu:
- Vận dụng và tự học.
### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| Bước 4: Giao 4 nhiệm vụ tự học | **Nhiệm vụ tự học**<br>1. Ôn tập kiến thức<br>2. Làm bài tập còn lại SGK/SBT<br>3. Chuẩn bị bài mới<br>4. Vận dụng, tìm tòi mở rộng |`;
appState.content.activities.E = `## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ (4 phút)
1. Ôn tập kiến thức: trùng lặp.`;

assert.deepStrictEqual(activityKeysForFullPlan(appState.content), ['A', 'B', 'C', 'D']);
const full = getFullLessonPlanMarkdown({ includeHeader: false });
assert.match(full, /VẬN DỤNG & HƯỚNG DẪN TỰ HỌC/);
assert.match(full, /Ôn tập kiến thức/);
assert.doesNotMatch(full, /HOẠT ĐỘNG 5/);
assert.match(full, /III\.A - D|TIẾN TRÌNH DẠY HỌC/);
console.log('  -> Ghép giáo án A–D: PASS');

console.log('==================================================');
console.log('TẤT CẢ TEST 4 HOẠT ĐỘNG A–D ĐỀU ĐẠT (PASS)!');
console.log('==================================================');
