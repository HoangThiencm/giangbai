'use strict';

const assert = require('assert');
const { getPeriodMinutesByGrade, parsePeriodsFromInput, formatSmartDuration } = require('../js/khbd-app.js');
const { calculateActivityTimeBudgets } = require('../js/khbd-prompts.js');

console.log('==================================================');
console.log('BẮT ĐẦU KIỂM THỬ THỜI LƯỢNG THÔNG MINH (35P/45P)');
console.log('==================================================');

// 1. Kiểm tra số phút chuẩn theo khối lớp: getPeriodMinutesByGrade
console.log('-> 1. Kiểm tra getPeriodMinutesByGrade...');
assert.strictEqual(getPeriodMinutesByGrade(1), 35, 'Lớp 1 phải là 35 phút/tiết');
assert.strictEqual(getPeriodMinutesByGrade(2), 35, 'Lớp 2 phải là 35 phút/tiết');
assert.strictEqual(getPeriodMinutesByGrade(3), 35, 'Lớp 3 phải là 35 phút/tiết');
assert.strictEqual(getPeriodMinutesByGrade(4), 35, 'Lớp 4 phải là 35 phút/tiết');
assert.strictEqual(getPeriodMinutesByGrade(5), 35, 'Lớp 5 phải là 35 phút/tiết');
assert.strictEqual(getPeriodMinutesByGrade('5'), 35, 'Lớp "5" (string) phải là 35 phút/tiết');

assert.strictEqual(getPeriodMinutesByGrade(6), 45, 'Lớp 6 phải là 45 phút/tiết');
assert.strictEqual(getPeriodMinutesByGrade(7), 45, 'Lớp 7 phải là 45 phút/tiết');
assert.strictEqual(getPeriodMinutesByGrade(8), 45, 'Lớp 8 phải là 45 phút/tiết');
assert.strictEqual(getPeriodMinutesByGrade(9), 45, 'Lớp 9 phải là 45 phút/tiết');
assert.strictEqual(getPeriodMinutesByGrade(10), 45, 'Lớp 10 phải là 45 phút/tiết');
assert.strictEqual(getPeriodMinutesByGrade(11), 45, 'Lớp 11 phải là 45 phút/tiết');
assert.strictEqual(getPeriodMinutesByGrade(12), 45, 'Lớp 12 phải là 45 phút/tiết');
assert.strictEqual(getPeriodMinutesByGrade('9'), 45, 'Lớp "9" (string) phải là 45 phút/tiết');
assert.strictEqual(getPeriodMinutesByGrade(), 45, 'Mặc định (undefined) phải là 45 phút/tiết');
console.log('  -> getPeriodMinutesByGrade: PASS');

// 2. Kiểm tra trích xuất số tiết: parsePeriodsFromInput
console.log('-> 2. Kiểm tra parsePeriodsFromInput...');
assert.strictEqual(parsePeriodsFromInput('01 tiết (35 phút)', 3), 1);
assert.strictEqual(parsePeriodsFromInput('2 tiết', 6), 2);
assert.strictEqual(parsePeriodsFromInput('3 tiết (135 phút)', 6), 3);
assert.strictEqual(parsePeriodsFromInput('70 phút', 4), 2, '70 phút ở lớp 4 (35p/tiết) = 2 tiết');
assert.strictEqual(parsePeriodsFromInput('90 phút', 7), 2, '90 phút ở lớp 7 (45p/tiết) = 2 tiết');
assert.strictEqual(parsePeriodsFromInput('35p', 5), 1, '35p ở lớp 5 = 1 tiết');
assert.strictEqual(parsePeriodsFromInput('45 min', 8), 1, '45 min ở lớp 8 = 1 tiết');
assert.strictEqual(parsePeriodsFromInput('2', 6), 2, 'Nhập số "2" = 2 tiết');
assert.strictEqual(parsePeriodsFromInput('90', 6), 2, 'Nhập "90" (phút) ở lớp 6 = 2 tiết');
assert.strictEqual(parsePeriodsFromInput('70', 3), 2, 'Nhập "70" (phút) ở lớp 3 = 2 tiết');
console.log('  -> parsePeriodsFromInput: PASS');

// 3. Kiểm tra định dạng thời lượng: formatSmartDuration
console.log('-> 3. Kiểm tra formatSmartDuration...');
assert.strictEqual(formatSmartDuration('1', 3), '01 tiết (35 phút)', 'Lớp 3: 1 tiết = 35 phút');
assert.strictEqual(formatSmartDuration('2', 4), '02 tiết (70 phút)', 'Lớp 4: 2 tiết = 70 phút');
assert.strictEqual(formatSmartDuration('3', 5), '03 tiết (105 phút)', 'Lớp 5: 3 tiết = 105 phút');

assert.strictEqual(formatSmartDuration('1', 6), '01 tiết (45 phút)', 'Lớp 6: 1 tiết = 45 phút');
assert.strictEqual(formatSmartDuration('2', 7), '02 tiết (90 phút)', 'Lớp 7: 2 tiết = 90 phút');
assert.strictEqual(formatSmartDuration('3', 8), '03 tiết (135 phút)', 'Lớp 8: 3 tiết = 135 phút');
assert.strictEqual(formatSmartDuration('4', 9), '04 tiết (180 phút)', 'Lớp 9: 4 tiết = 180 phút');
console.log('  -> formatSmartDuration: PASS');

// 4. Kiểm tra phân bổ thời lượng hoạt động: calculateActivityTimeBudgets
console.log('-> 4. Kiểm tra calculateActivityTimeBudgets...');
const budgetsGrade4 = calculateActivityTimeBudgets('02 tiết (70 phút)', 2, 4);
assert.strictEqual(budgetsGrade4.totalMinutes, 70, 'Tổng phút lớp 4 (2 tiết) phải là 70');
assert.ok(budgetsGrade4.A > 0, 'Pha A > 0');
assert.ok(budgetsGrade4.B > 0, 'Pha B > 0');
assert.ok(budgetsGrade4.C > 0, 'Pha C > 0');
assert.ok(budgetsGrade4.D > 0, 'Pha D > 0');
assert.ok(budgetsGrade4.E > 0, 'Pha E > 0');
assert.strictEqual(budgetsGrade4.A + budgetsGrade4.B + budgetsGrade4.C + budgetsGrade4.D + budgetsGrade4.E, 70, 'Tổng các pha phải bằng đúng 70 phút');

const budgetsGrade8 = calculateActivityTimeBudgets('02 tiết (90 phút)', 2, 8);
assert.strictEqual(budgetsGrade8.totalMinutes, 90, 'Tổng phút lớp 8 (2 tiết) phải là 90');
assert.strictEqual(budgetsGrade8.A + budgetsGrade8.B + budgetsGrade8.C + budgetsGrade8.D + budgetsGrade8.E, 90, 'Tổng các pha phải bằng đúng 90 phút');

console.log('  -> calculateActivityTimeBudgets: PASS');

console.log('==================================================');
console.log('TẤT CẢ KIỂM THỬ THỜI LƯỢNG THÔNG MINH ĐỀU ĐẠT 100%!');
console.log('==================================================');
