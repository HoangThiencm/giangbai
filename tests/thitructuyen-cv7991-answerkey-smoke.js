/** Smoke: nhận diện bảng đáp án hỗn hợp CV 7991 (MC + Đúng/Sai + trả lời ngắn). Node 18+. */
'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'thitructuyen.html'), 'utf8');

const start = html.indexOf('        const normalizeImportedQuizText');
const end = html.indexOf('        const HybridExamCreator');
assert.ok(start >= 0 && end > start, 'Phải trích được khối parse đề Word từ thitructuyen.html');
const parserSrc = html.slice(start, end);
assert.match(parserSrc, /classifyImportedAnswerValue/, 'Phải có classifyImportedAnswerValue');
assert.match(parserSrc, /importedAnswerKeyTfList/, 'Phải gán đáp án tf từ answerKey');
assert.ok(!parserSrc.includes('pairRegex = /(\\d{1,3})\\s*[\\.\\)\\-:]?\\s*([A-D])/gi'), 'Không còn regex chỉ bắt A-D');

const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(
    parserSrc + `
this.normalizeImportedQuizText = normalizeImportedQuizText;
this.getImportedAnswerKey = getImportedAnswerKey;
this.stripImportedAnswerKey = stripImportedAnswerKey;
this.parseLatexWordQuiz = parseLatexWordQuiz;
`,
    sandbox
);

const {
    normalizeImportedQuizText,
    getImportedAnswerKey,
    stripImportedAnswerKey,
    parseLatexWordQuiz
} = sandbox;

assert.strictEqual(typeof getImportedAnswerKey, 'function');
assert.strictEqual(typeof stripImportedAnswerKey, 'function');
assert.strictEqual(typeof parseLatexWordQuiz, 'function');

const clone = (value) => JSON.parse(JSON.stringify(value));

const USER_ANSWER_TABLE = [
    'Đáp án:',
    '1.B   2.C   3.A   4.B   5.C   6.B   7.A   8.D   9.B   10.C   11.C   12.C   ',
    '13.Đúng   14.Sai   ',
    '15.27\t16.2000   17.100   18.30'
].join('\n');

const MC_LETTERS = ['B', 'C', 'A', 'B', 'C', 'B', 'A', 'D', 'B', 'C', 'C', 'C'];
const MC_INDEXES = MC_LETTERS.map((letter) => 'ABCD'.indexOf(letter));

function buildMcQuestions(count) {
    return Array.from({ length: count }, (_, i) => [
        `Câu ${i + 1}. Nội dung câu trắc nghiệm ${i + 1}.`,
        'A. Phương án A',
        'B. Phương án B',
        'C. Phương án C',
        'D. Phương án D'
    ].join('\n')).join('\n\n');
}

console.log('================================================================================');
console.log('KIỂM THỬ BẢNG ĐÁP ÁN HỖN HỢP CV 7991');
console.log('================================================================================');

console.log('\n[TEST 1] getImportedAnswerKey nhận đủ 18 cặp đáp án mẫu...');
const keyText = normalizeImportedQuizText(USER_ANSWER_TABLE);
const answerKey = getImportedAnswerKey(keyText);
assert.strictEqual(Object.keys(answerKey).length, 18, 'Phải nhận đúng 18 cặp đáp án');
MC_LETTERS.forEach((letter, idx) => {
    const entry = answerKey[idx + 1];
    assert.ok(entry, `Thiếu đáp án câu ${idx + 1}`);
    assert.strictEqual(entry.type, 'mc', `Câu ${idx + 1} phải là mc`);
    assert.strictEqual(entry.value, letter, `Câu ${idx + 1} phải là ${letter}`);
});
assert.strictEqual(answerKey[13].type, 'tf');
assert.strictEqual(answerKey[13].value, true);
assert.strictEqual(answerKey[14].type, 'tf');
assert.strictEqual(answerKey[14].value, false);
assert.strictEqual(answerKey[15].type, 'short_answer');
assert.strictEqual(answerKey[15].value, '27');
assert.strictEqual(answerKey[16].value, '2000');
assert.strictEqual(answerKey[17].value, '100');
assert.strictEqual(answerKey[18].value, '30');
console.log('✓ 1..12 MC, 13 Đúng, 14 Sai, 15..18 trả lời ngắn.');

console.log('\n[TEST 2] parse 18 câu đề mẫu với bảng đáp án người dùng...');
const sample18 = [
    'PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn. Thí sinh trả lời từ câu 1 đến câu 12.',
    buildMcQuestions(12),
    'PHẦN II. Câu trắc nghiệm đúng sai. Thí sinh trả lời từ câu 13 đến câu 14.',
    'Câu 13. Mệnh đề số 13 là mệnh đề đúng.',
    'Câu 14. Mệnh đề số 14 là mệnh đề sai.',
    'PHẦN III. Câu trắc nghiệm trả lời ngắn. Thí sinh trả lời từ câu 15 đến câu 18.',
    'Câu 15. Kết quả phép tính thứ nhất.',
    'Câu 16. Kết quả phép tính thứ hai.',
    'Câu 17. Kết quả phép tính thứ ba.',
    'Câu 18. Kết quả phép tính thứ tư.',
    USER_ANSWER_TABLE
].join('\n\n');

const parsed18 = parseLatexWordQuiz(sample18);
assert.strictEqual(parsed18.length, 18, 'Phải parse đúng 18 câu');
parsed18.slice(0, 12).forEach((q, idx) => {
    assert.strictEqual(q.type, 'mc', `Câu ${idx + 1} phải là mc`);
    assert.strictEqual(q.correct_index, MC_INDEXES[idx], `Câu ${idx + 1} đúng ${MC_LETTERS[idx]}`);
});
assert.strictEqual(parsed18[12].type, 'short_answer');
assert.strictEqual(parsed18[12].correct_answer, 'Đúng');
assert.strictEqual(parsed18[13].type, 'short_answer');
assert.strictEqual(parsed18[13].correct_answer, 'Sai');
assert.strictEqual(parsed18[14].correct_answer, '27');
assert.strictEqual(parsed18[15].correct_answer, '2000');
assert.strictEqual(parsed18[16].correct_answer, '100');
assert.strictEqual(parsed18[17].correct_answer, '30');
parsed18.forEach((q, idx) => {
    assert.ok(!/đáp\s*án/i.test(q.question), `Câu ${idx + 1} không được còn bảng đáp án trong đề`);
});
console.log('✓ 18 câu có đủ đáp án 3 phần, bảng đáp án đã được cắt khỏi đề.');

console.log('\n[TEST 3] Câu Đúng/Sai nhiều ý phụ lấy correct_answers từ answerKey...');
const sampleTfMulti = [
    'Câu 1. Cho các mệnh đề sau:',
    'a) Ý a.',
    'b) Ý b.',
    'c) Ý c.',
    'd) Ý d.',
    'Câu 2. Cho các mệnh đề khác:',
    'a) Ý a.',
    'b) Ý b.',
    'c) Ý c.',
    'd) Ý d.',
    'Đáp án:',
    '1. a.Đúng b.Sai c.Đúng d.Sai',
    '2: Đ, S, Đ, S'
].join('\n');
const parsedTf = parseLatexWordQuiz(sampleTfMulti);
assert.strictEqual(parsedTf.length, 2);
assert.strictEqual(parsedTf[0].type, 'tf');
assert.deepStrictEqual(clone(parsedTf[0].correct_answers), [true, false, true, false]);
assert.strictEqual(parsedTf[1].type, 'tf');
assert.deepStrictEqual(clone(parsedTf[1].correct_answers), [true, false, true, false]);
console.log('✓ 1. a.Đúng b.Sai c.Đúng d.Sai và 2: Đ, S, Đ, S.');

console.log('\n[TEST 4] Đề trắc nghiệm thuần (định dạng cũ) không bị xáo trộn...');
const sampleMcOnly = [
    'Câu 1. Số nguyên tố là:',
    'A. 4',
    'B. 6',
    'C. 7',
    'D. 9',
    'Câu 2. Tập hợp các ước của 6 là:',
    'A. {1; 2; 3; 6}',
    'B. {1; 2; 3}',
    'C. {2; 3; 6}',
    'D. {1; 6}',
    'Đáp án: 1.C 2.A'
].join('\n');
const parsedMc = parseLatexWordQuiz(sampleMcOnly);
assert.strictEqual(parsedMc.length, 2);
assert.strictEqual(parsedMc[0].type, 'mc');
assert.strictEqual(parsedMc[0].correct_index, 2);
assert.strictEqual(parsedMc[1].type, 'mc');
assert.strictEqual(parsedMc[1].correct_index, 0);

const sampleMcCompact = [
    'Câu 1. Hỏi A',
    'A. 1',
    'B. 2',
    'C. 3',
    'D. 4',
    'Câu 2. Hỏi B',
    'A. 1',
    'B. 2',
    'C. 3',
    'D. 4',
    'Đáp án: 1C 2B'
].join('\n');
const parsedCompact = parseLatexWordQuiz(sampleMcCompact);
assert.strictEqual(parsedCompact.length, 2);
assert.strictEqual(parsedCompact[0].correct_index, 2);
assert.strictEqual(parsedCompact[1].correct_index, 1);
console.log('✓ 1.C 2.A và dạng cũ 1C 2B vẫn đúng.');

console.log('\n[TEST 5] Số thập phân 3.14 không bị nhầm thành số thứ tự câu...');
const sampleDecimal = [
    'Câu 1. Tính pi xấp xỉ.',
    'Câu 2. Tính phân số.',
    'Đáp án:',
    '1. 3.14',
    '2. -1/2'
].join('\n');
const parsedDecimal = parseLatexWordQuiz(sampleDecimal);
assert.strictEqual(parsedDecimal.length, 2);
assert.strictEqual(parsedDecimal[0].type, 'short_answer');
assert.strictEqual(parsedDecimal[0].correct_answer, '3.14');
assert.strictEqual(parsedDecimal[1].correct_answer, '-1/2');
const decimalKey = getImportedAnswerKey(normalizeImportedQuizText('Đáp án:\n15. 3.14   16.2000'));
assert.strictEqual(decimalKey[15].value, '3.14');
assert.strictEqual(decimalKey[16].value, '2000');
assert.ok(!decimalKey[3], '3.14 không được hiểu thành câu 3');
console.log('✓ 15. 3.14 và -1/2 được giữ nguyên.');

console.log('\n[TEST 6] stripImportedAnswerKey cắt bảng đáp án hỗn hợp...');
const stripped = stripImportedAnswerKey(normalizeImportedQuizText(sample18));
assert.doesNotMatch(stripped, /13\.Đúng/);
assert.doesNotMatch(stripped, /15\.27/);
assert.match(stripped, /Câu 18/);
console.log('✓ Bảng đáp án hỗn hợp đã được cắt, câu hỏi vẫn còn.');

console.log('\n================================================================================');
console.log('TẤT CẢ KIỂM THỬ BẢNG ĐÁP ÁN CV 7991 ĐÃ PASS 100%!');
console.log('================================================================================');
