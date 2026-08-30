'use strict';

const assert = require('assert');
const { calculateActivityTimeBudgets } = require('../js/khbd-prompts.js');

console.log('==================================================');
console.log('BẮT ĐẦU KIỂM THỬ PHÂN BỔ THỜI LƯỢNG ĐỘNG A–D');
console.log('==================================================');

const cases = [
  { duration: '01 tiết (45 phút)', grade: 6, expectedT: 45 },
  { duration: '01 tiết (35 phút)', grade: 4, expectedT: 35 },
  { duration: '02 tiết (90 phút)', grade: 6, expectedT: 90 },
  { duration: '02 tiết (70 phút)', grade: 4, expectedT: 70 },
  { duration: '03 tiết (135 phút)', grade: 8, expectedT: 135 },
  { duration: '03 tiết (105 phút)', grade: 3, expectedT: 105 },
  { duration: '04 tiết (180 phút)', grade: 9, expectedT: 180 },
  { duration: '04 tiết (140 phút)', grade: 5, expectedT: 140 },
  { duration: '120 phút', grade: 6, expectedT: 120 },
  { duration: '150 phút', grade: 7, expectedT: 150 }
];

for (const tc of cases) {
  for (const n of [1, 2, 3, 4]) {
    const res = calculateActivityTimeBudgets(tc.duration, n, tc.grade);
    assert.strictEqual(res.totalMinutes, tc.expectedT, `${tc.duration} T`);
    assert.strictEqual(res.A + res.B + res.C + res.D, tc.expectedT, `${tc.duration} N=${n} A+B+C+D`);
    assert.strictEqual(res.E, 0, `${tc.duration} không tách E`);
    assert.ok(res.A >= 3 && res.A <= 12, `${tc.duration} A in 3–12, got ${res.A}`);
    assert.ok(res.D >= 5 && res.D <= 25, `${tc.duration} D in 5–25, got ${res.D}`);
    assert.ok(res.B >= 5, `${tc.duration} B>=5`);
    assert.ok(res.C >= 3, `${tc.duration} C>=3`);
    assert.strictEqual(res.B_subsections.length, n);
    assert.strictEqual(res.B_subsections.reduce((a, b) => a + b, 0), res.B, `${tc.duration} N=${n} sum B_i = B`);
    assert.ok(res.fourActivities);
  }
}

const two = calculateActivityTimeBudgets('02 tiết (90 phút)', 2, 6);
assert.strictEqual(two.A + two.B + two.C + two.D, 90);
assert.strictEqual(two.B, two.B_subsections[0] + two.B_subsections[1]);

const one = calculateActivityTimeBudgets('01 tiết (45 phút)', 1, 6);
assert.strictEqual(one.A + one.B + one.C + one.D, 45);

const three = calculateActivityTimeBudgets('03 tiết (135 phút)', 3, 6);
assert.strictEqual(three.A + three.B + three.C + three.D, 135);
assert.ok(three.B > three.C, 'N=3 thì B nặng hơn C');

const four = calculateActivityTimeBudgets('04 tiết (180 phút)', 4, 6);
assert.strictEqual(four.A + four.B + four.C + four.D, 180);
assert.ok(four.B > four.C, 'N=4 thì B nặng hơn C');

const legacy = calculateActivityTimeBudgets('02 tiết (90 phút)', 2, 6, { fourActivities: false });
assert.ok(legacy.E > 0);
assert.strictEqual(legacy.A + legacy.B + legacy.C + legacy.D + legacy.E, 90);

console.log('  -> Phân bổ động mọi mốc tiết/tiểu mục: PASS');
console.log('==================================================');
console.log('TẤT CẢ TEST PHÂN BỔ THỜI LƯỢNG ĐỘNG ĐỀU ĐẠT (PASS)!');
console.log('==================================================');
