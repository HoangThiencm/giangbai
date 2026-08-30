'use strict';

const assert = require('assert');
const {
  clipKhbdActivityMarkdown,
  parseKhbdSections,
  normalizeActivityTimeHeadings
} = require('../js/khbd-app.js');
const {
  calculateActivityTimeBudgets,
  getPromptTemplate
} = require('../js/khbd-prompts.js');

console.log('==================================================');
console.log('BẮT ĐẦU KIỂM THỬ DEDUPE HOẠT ĐỘNG D VÀ KHÓA 90 PHÚT');
console.log('==================================================');

const dupD = `## D. HOẠT ĐỘNG 4: VẬN DỤNG (11 phút)
### a) Mục tiêu:
- Vận dụng tập hợp vào tình huống thực tế.
### b) Nội dung:
- Bài toán thực tế trong SGK.
### c) Sản phẩm:
- Kết quả mô hình hóa.
### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| Bước 1 | Vận dụng |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (11 phút)
### a) Mục tiêu:
- Lặp lại hoạt động vận dụng.
### b) Nội dung:
- Bản sao thứ hai.
`;

console.log('-> 1. clipKhbdActivityMarkdown giữ đúng 1 khối D...');
const clippedD = clipKhbdActivityMarkdown('D', dupD);
assert.match(clippedD, /VẬN DỤNG/);
assert.equal((clippedD.match(/##\s*D\.\s*HOẠT ĐỘNG 4/gi) || []).length, 1, 'Chỉ còn 1 tiêu đề D');
assert.doesNotMatch(clippedD, /Bản sao thứ hai/);
console.log('  -> clip D: PASS');

console.log('-> 2. parseKhbdSections dedupe marker và heading D...');
const marked = `<<<KHBD_A>>>
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (7 phút)
Mở đầu
<<<KHBD_B>>>
## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (75 phút)
### 1. Hoạt động 2.1: Tập hợp (45 phút)
Nội dung 2.1
### 2. Hoạt động 2.2: Tia số (30 phút)
Nội dung 2.2
<<<KHBD_C>>>
## C. HOẠT ĐỘNG 3: LUYỆN TẬP (23 phút)
Luyện tập
<<<KHBD_D>>>
## D. HOẠT ĐỘNG 4: VẬN DỤNG (11 phút)
### a) Mục tiêu:
- Vận dụng lần 1.
### b) Nội dung:
- Nội dung 1.
### c) Sản phẩm:
- Sản phẩm 1.
### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| Bước 1 | Nội dung |
<<<KHBD_D>>>
## D. HOẠT ĐỘNG 4: VẬN DỤNG (11 phút)
Bản D thứ hai thiếu 4 phần.
<<<KHBD_E>>>
## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ (4 phút)
1. Ôn tập kiến thức: Ôn lại định nghĩa.
2. Làm bài tập: Bài còn lại SGK.
3. Chuẩn bị bài mới: Đọc bài mới.
4. Nhiệm vụ tìm tòi, mở rộng: Ứng dụng thực tế.
`;
const parsed = parseKhbdSections(marked, ['A', 'B', 'C', 'D', 'E']);
assert.equal((parsed.D.match(/##\s*D\.\s*HOẠT ĐỘNG 4/gi) || []).length, 1, 'parse marker: 1 khối D');
assert.match(parsed.D, /Vận dụng lần 1/);
assert.doesNotMatch(parsed.D, /Bản D thứ hai/);

const headingDup = `## A. HOẠT ĐỘNG 1: MỞ ĐẦU (7 phút)
Mở đầu
## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (45 phút)
Hình thành
## C. HOẠT ĐỘNG 3: LUYỆN TẬP (23 phút)
Luyện tập
## D. HOẠT ĐỘNG 4: VẬN DỤNG (11 phút)
### a) Mục tiêu:
- Vận dụng chuẩn.
### b) Nội dung:
- Nội dung chuẩn.
### c) Sản phẩm:
- Sản phẩm chuẩn.
### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| Bước 1 | Nội dung |
## D. HOẠT ĐỘNG 4: VẬN DỤNG (11 phút)
Bản D lặp.
## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ (4 phút)
1. Ôn tập kiến thức: Ôn lại.
2. Làm bài tập: Bài còn lại.
3. Chuẩn bị bài mới: Đọc bài mới.
4. Nhiệm vụ tìm tòi, mở rộng: Thực tế.
`;
const parsedHeading = parseKhbdSections(headingDup, ['A', 'B', 'C', 'D', 'E']);
assert.equal((parsedHeading.D.match(/##\s*D\.\s*HOẠT ĐỘNG 4/gi) || []).length, 1, 'parse heading: 1 khối D');
assert.match(parsedHeading.D, /Vận dụng chuẩn/);
assert.doesNotMatch(parsedHeading.D, /Bản D lặp/);
console.log('  -> parseKhbdSections: PASS');

console.log('-> 3. Chuẩn hóa tổng thời lượng 5 hoạt động đúng 90 phút...');
const inflated = `## A. HOẠT ĐỘNG 1: MỞ ĐẦU (10 phút)
Mở đầu
## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (75 phút)
### 1. Hoạt động 2.1: Tập hợp (45 phút)
Nội dung 2.1
### 2. Hoạt động 2.2: Tia số (30 phút)
Nội dung 2.2
## C. HOẠT ĐỘNG 3: LUYỆN TẬP (20 phút)
Luyện tập
## D. HOẠT ĐỘNG 4: VẬN DỤNG (11 phút)
Vận dụng
## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ (5 phút)
Về nhà`;
const normalized = normalizeActivityTimeHeadings(inflated, {
  duration: '02 tiết (90 phút)',
  grade: 6,
  subsectionCount: 2
});
const budgets = calculateActivityTimeBudgets('02 tiết (90 phút)', 2, 6);
assert.strictEqual(budgets.totalMinutes, 90);
assert.strictEqual(budgets.B, 45);
assert.strictEqual(budgets.B_subsections.reduce((a, b) => a + b, 0), 45);
assert.match(normalized, new RegExp(`## A\\. HOẠT ĐỘNG 1: MỞ ĐẦU \\(${budgets.A} phút\\)`));
assert.match(normalized, new RegExp(`## B\\. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI \\(${budgets.B} phút\\)`));
assert.match(normalized, new RegExp(`Hoạt động 2\\.1: Tập hợp \\(${budgets.B_subsections[0]} phút\\)`));
assert.match(normalized, new RegExp(`Hoạt động 2\\.2: Tia số \\(${budgets.B_subsections[1]} phút\\)`));
assert.match(normalized, new RegExp(`## C\\. HOẠT ĐỘNG 3: LUYỆN TẬP \\(${budgets.C} phút\\)`));
assert.match(normalized, new RegExp(`## D\\. HOẠT ĐỘNG 4: VẬN DỤNG \\(${budgets.D} phút\\)`));
assert.match(normalized, new RegExp(`## E\\. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ \\(${budgets.E} phút\\)`));
const headingMinutes = [...normalized.matchAll(/\((\d+)\s*phút\)/g)].map(m => Number(m[1]));
const mainAndBranch = headingMinutes.slice(0, 7);
assert.strictEqual(mainAndBranch[0] + mainAndBranch[1] + mainAndBranch[4] + mainAndBranch[5] + mainAndBranch[6], 90, 'A+B+C+D+E phải bằng 90');
assert.strictEqual(mainAndBranch[2] + mainAndBranch[3], 45, 'Nhánh 2.1 + 2.2 phải bằng 45');
assert.doesNotMatch(normalized, /\(75 phút\)/);
assert.doesNotMatch(normalized, /Hoạt động 2\.2:[^\n]*\(30 phút\)/);
console.log('  -> normalizeActivityTimeHeadings 90 phút: PASS');

console.log('-> 4. Prompt khóa thời lượng B và cấm lặp D...');
const promptAE = getPromptTemplate('GENERATE_ACTIVITIES_AE', {
  subjectName: 'Toán',
  topic: 'Tập hợp',
  duration: '02 tiết (90 phút)',
  textbook_content: `
I. Số và tập hợp các số tự nhiên
Nội dung 1
II. Biểu diễn số tự nhiên trên tia số
Nội dung 2
  `,
  objectives_content: ''
});
assert.match(promptAE, /KHÓA ĐÚNG 5 MARKER DUY NHẤT/);
assert.match(promptAE, /CẤM xuất thêm tiêu đề hoặc khối ## D\. HOẠT ĐỘNG 4/);
assert.match(promptAE, /TUYỆT ĐỐI CẤM gán 45 phút \+ 30 phút = 75 phút/);
assert.match(promptAE, /tổng A \+ B \+ C \+ D \+ E BẮT BUỘC đúng bằng toàn bộ thời lượng bài dạy 02 tiết \(90 phút\)/i);
assert.match(promptAE, /## B\. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI \(45 phút\)/);

const promptB = getPromptTemplate('GENERATE_ACTIVITY_B', {
  subjectName: 'Toán',
  topic: 'Tập hợp',
  duration: '02 tiết (90 phút)',
  textbook_content: `
I. Số và tập hợp các số tự nhiên
Nội dung 1
II. Biểu diễn số tự nhiên trên tia số
Nội dung 2
  `,
  objectives_content: ''
});
assert.match(promptB, /Tổng số phút của TẤT CẢ hoạt động nhánh[\s\S]*?đúng bằng 45 phút/);
assert.match(promptB, /TUYỆT ĐỐI CẤM gán 45 phút \+ 30 phút = 75 phút/);
console.log('  -> Prompt AE / B: PASS');

console.log('==================================================');
console.log('TẤT CẢ TEST DEDUPE D VÀ 90 PHÚT ĐỀU ĐẠT (PASS)!');
console.log('==================================================');
