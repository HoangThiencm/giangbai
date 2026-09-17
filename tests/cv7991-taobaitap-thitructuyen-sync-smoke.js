/** Smoke: đồng bộ CV 7991 17 câu giữa taobaitap.html và thitructuyen.html. Node 18+. */
'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.join(__dirname, '..');
const taoHtml = fs.readFileSync(path.join(root, 'taobaitap.html'), 'utf8');
const thiHtml = fs.readFileSync(path.join(root, 'thitructuyen.html'), 'utf8');

function extractAndRun(html, startNeedle, endNeedle, exports) {
    const start = html.indexOf(startNeedle);
    const end = html.indexOf(endNeedle);
    assert.ok(start >= 0 && end > start, `Phải trích được khối từ ${startNeedle.slice(0, 40)}`);
    const src = html.slice(start, end);
    const sandbox = {};
    vm.createContext(sandbox);
    const assign = exports.map((name) => `this.${name} = ${name};`).join('\n');
    vm.runInContext(src + '\n' + assign, sandbox);
    return sandbox;
}

const tao = extractAndRun(
    taoHtml,
    '        const cleanOptionText',
    '        const saveDocxFromHtml',
    [
        'normalizeQuizItems',
        'normalizeShortAnswerValue',
        'isCv7991TrueFalseItem',
        'getCv7991TrueFalseItems',
        'formatQuizAnswer',
        'buildCv7991ExportHtml',
        'buildCv7991ExportText'
    ]
);

const thi = extractAndRun(
    thiHtml,
    '        const normalizeImportedQuizText',
    '        const HybridExamCreator',
    [
        'normalizeImportedQuizText',
        'parseLatexWordQuiz',
        'getImportedAnswerKey',
        'stripImportedAnswerKey'
    ]
);

const {
    normalizeQuizItems,
    normalizeShortAnswerValue,
    isCv7991TrueFalseItem,
    getCv7991TrueFalseItems,
    buildCv7991ExportHtml,
    buildCv7991ExportText
} = tao;

const {
    normalizeImportedQuizText,
    parseLatexWordQuiz,
    getImportedAnswerKey,
    stripImportedAnswerKey
} = thi;

const clone = (value) => JSON.parse(JSON.stringify(value));

function htmlToPlainText(html) {
    return String(html || '')
        .replace(/<br\s*\/?>/gi, '\n')
        .replace(/<\/(p|div|h1|h2|h3|tr|table|li)>/gi, '\n')
        .replace(/<[^>]+>/g, ' ')
        .replace(/&nbsp;/gi, ' ')
        .replace(/&lt;/gi, '<')
        .replace(/&gt;/gi, '>')
        .replace(/&amp;/gi, '&')
        .replace(/[ \t]+\n/g, '\n')
        .replace(/\n{3,}/g, '\n\n')
        .trim();
}

const MC_LETTERS = ['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D'];
const TF_ANSWERS = [true, false, true, false];
const SA_ANSWERS = ['25', '3.5', '100', '-4'];

function buildSampleCv7991Items() {
    const mc = MC_LETTERS.map((letter, idx) => ({
        type: 'multiple-choice',
        question: `Nội dung câu trắc nghiệm ${idx + 1}`,
        options: ['Phương án A', 'Phương án B', 'Phương án C', 'Phương án D'],
        correctAnswerIndex: 'ABCD'.indexOf(letter)
    }));
    const tf = {
        type: 'true-false',
        question: 'Cho hàm số y = 2x + 1. Xét các mệnh đề sau:',
        options: [
            'Hàm số đồng biến trên R',
            'Đồ thị cắt trục tung tại (0; 2)',
            'Hàm số có hệ số góc bằng 2',
            'Hàm số nghịch biến trên R'
        ],
        correct_answers: TF_ANSWERS
    };
    const sa = SA_ANSWERS.map((ans, idx) => ({
        type: 'short-answer',
        question: `Tính kết quả số thứ ${idx + 1}`,
        correctAnswer: ans
    }));
    return [...mc, tf, ...sa];
}

function assertParsedCv7991(parsed, label) {
    assert.strictEqual(parsed.length, 17, `${label}: phải đúng 17 câu`);
    parsed.slice(0, 12).forEach((q, idx) => {
        assert.strictEqual(q.type, 'mc', `${label}: câu ${idx + 1} phải là mc`);
        assert.strictEqual((q.options || []).filter(Boolean).length, 4, `${label}: câu ${idx + 1} đủ 4 phương án`);
        assert.ok(q.options[0], `${label}: câu ${idx + 1} có A`);
        assert.ok(q.options[1], `${label}: câu ${idx + 1} có B`);
        assert.ok(q.options[2], `${label}: câu ${idx + 1} có C`);
        assert.ok(q.options[3], `${label}: câu ${idx + 1} có D`);
        assert.strictEqual(q.correct_index, 'ABCD'.indexOf(MC_LETTERS[idx]), `${label}: câu ${idx + 1} đúng ${MC_LETTERS[idx]}`);
    });
    assert.strictEqual(parsed[12].type, 'tf', `${label}: câu 13 phải là tf`);
    assert.strictEqual((parsed[12].options || []).filter(Boolean).length, 4, `${label}: câu 13 đủ 4 ý`);
    assert.deepStrictEqual(clone(parsed[12].correct_answers), TF_ANSWERS, `${label}: câu 13 đúng mảng 4 boolean`);
    parsed.slice(13, 17).forEach((q, idx) => {
        assert.strictEqual(q.type, 'short_answer', `${label}: câu ${idx + 14} phải là short_answer`);
        assert.strictEqual(String(q.correct_answer), SA_ANSWERS[idx], `${label}: câu ${idx + 14} đáp án ${SA_ANSWERS[idx]}`);
        assert.doesNotMatch(String(q.correct_answer), /[a-zA-Z]/, `${label}: câu ${idx + 14} đáp án chỉ là số`);
    });
    parsed.forEach((q, idx) => {
        assert.doesNotMatch(String(q.question || ''), /bảng\s*đáp\s*án|đáp\s*án\s*:/i, `${label}: câu ${idx + 1} không còn bảng đáp án`);
    });
    assert.strictEqual(parsed.exam_format, 'cv7991', `${label}: tự nhận diện exam_format cv7991`);
}

console.log('================================================================================');
console.log('KIỂM THỬ ĐỒNG BỘ CV 7991 (17 CÂU) TẠO BÀI TẬP ↔ THI TRỰC TUYẾN');
console.log('================================================================================');

console.log('\n[TEST 0] Giao diện & prompt taobaitap.html khóa cấu trúc 17 câu...');
assert.match(taoHtml, /Chuẩn Công văn 7991 \(17 câu - 10đ: 12 TN \+ 1 Đ\/S 4 ý \+ 4 TL ngắn\)/);
assert.match(taoHtml, /setSynthCount\(17\)/);
assert.match(taoHtml, /synthForm === 'cv7991' \? 17/);
assert.match(taoHtml, /ĐÚNG 1 câu trắc nghiệm Đúng\/Sai/);
assert.match(taoHtml, /correct_answers": \[true, false, true, false\]/);
assert.match(taoHtml, /TUYỆT ĐỐI KHÔNG chứa chữ cái hay đơn vị đo/);
assert.match(taoHtml, /BẢNG ĐÁP ÁN/);
assert.match(taoHtml, /<p class="option">A\./);
assert.match(taoHtml, /handleUpdateTfSubItem/);
assert.match(taoHtml, /Đáp án số:/);
assert.ok(thiHtml.includes('\\t([A-Da-d]'), 'normalizeImportedQuizText phải tách tab trước chữ A-D/a-d');
assert.match(thiHtml, /exam_format = "cv7991"/);
console.log('✓ Nhãn 17 câu, prompt 1 TF 4 ý, xuất p.option + bảng đáp án, parser tách tab.');

console.log('\n[TEST 1] normalizeQuizItems: TF 4 ý + short-answer chỉ còn số...');
const dirty = normalizeQuizItems([
    ...MC_LETTERS.map((letter, idx) => ({
        type: 'multiple-choice',
        question: `Câu ${idx + 1}. Hỏi ${idx + 1}`,
        options: ['A. Một', 'B. Hai', 'C. Ba', 'D. Bốn'],
        correctAnswerIndex: 'ABCD'.indexOf(letter)
    })),
    {
        type: 'true-false',
        question: 'Ngữ cảnh bài toán',
        options: ['Mệnh đề a', 'Mệnh đề b', 'Mệnh đề c', 'Mệnh đề d'],
        correct_answers: ['true', false, 'Đúng', 0]
    },
    { type: 'short-answer', question: 'Tính x', correctAnswer: 'x = 25 cm' },
    { type: 'short-answer', question: 'Tính y', correctAnswer: '3,5' },
    { type: 'short-answer', question: 'Tính z', correctAnswer: 'khoảng 100' },
    { type: 'short-answer', question: 'Tính t', correctAnswer: '-4' }
]);
assert.strictEqual(dirty.length, 17);
assert.ok(isCv7991TrueFalseItem(dirty[12]));
assert.deepStrictEqual(clone(dirty[12].correct_answers), TF_ANSWERS);
assert.strictEqual(dirty[12].subItems.length, 4);
assert.strictEqual(normalizeShortAnswerValue('x = 25 cm'), '25');
assert.strictEqual(dirty[13].correctAnswer, '25');
assert.strictEqual(dirty[14].correctAnswer, '3.5');
assert.strictEqual(dirty[15].correctAnswer, '100');
assert.strictEqual(dirty[16].correctAnswer, '-4');
console.log('✓ TF 4 ý đồng bộ subItems/correct_answers; TLN lọc x=, đơn vị, dấu phẩy.');

console.log('\n[TEST 2] Xuất Text CV 7991 rồi nạp vào parser thi trực tuyến...');
const sampleItems = normalizeQuizItems(buildSampleCv7991Items());
const exportedText = buildCv7991ExportText(sampleItems, 'quiz');
assert.match(exportedText, /PHẦN I\. CÂU TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN LỰA CHỌN \(6\.0 điểm\)/);
assert.match(exportedText, /PHẦN II\. CÂU TRẮC NGHIỆM ĐÚNG SAI \(2\.0 điểm\)/);
assert.match(exportedText, /PHẦN III\. CÂU TRẮC NGHIỆM TRẢ LỜI NGẮN \(2\.0 điểm\)/);
assert.match(exportedText, /BẢNG ĐÁP ÁN/);
assert.match(exportedText, /a\) Hàm số đồng biến trên R \[Đúng\]/);
assert.match(exportedText, /b\) Đồ thị cắt trục tung tại \(0; 2\) \[Sai\]/);
assert.match(exportedText, /c\) Hàm số có hệ số góc bằng 2 \[Đúng\]/);
assert.match(exportedText, /d\) Hàm số nghịch biến trên R \[Sai\]/);
assert.match(exportedText, /13\. a\.Đúng b\.Sai c\.Đúng d\.Sai/);
assert.match(exportedText, /14\. 25\s+15\. 3\.5\s+16\. 100\s+17\. -4/);

const parsedText = parseLatexWordQuiz(exportedText);
assertParsedCv7991(parsedText, 'Text export');
const strippedText = stripImportedAnswerKey(normalizeImportedQuizText(exportedText));
assert.doesNotMatch(strippedText, /BẢNG ĐÁP ÁN/);
assert.doesNotMatch(strippedText, /13\. a\.Đúng/);
assert.doesNotMatch(strippedText, /14\. 25\s+15\. 3\.5/);
assert.match(strippedText, /Câu 17/);
console.log('✓ Text 17 câu: 12 MC + 1 TF 4 ý + 4 TLN; bảng đáp án đã cắt.');

console.log('\n[TEST 3] Xuất HTML/Word CV 7991 rồi nạp vào parser...');
const exportedHtml = buildCv7991ExportHtml(sampleItems, 'quiz');
assert.match(exportedHtml, /<p class="option">A\./);
assert.doesNotMatch(exportedHtml, /options-table/);
assert.match(exportedHtml, /<h2>BẢNG ĐÁP ÁN<\/h2>/);
assert.match(exportedHtml, /<div class="tf-item">a\)/);
const parsedHtml = parseLatexWordQuiz(htmlToPlainText(exportedHtml));
assertParsedCv7991(parsedHtml, 'HTML export');
console.log('✓ HTML/Word: phương án từng dòng, 4 ý TF, bảng đáp án parse đủ 17 câu.');

console.log('\n[TEST 4] Tab/khoảng trắng 2 cột không làm rơi phương án B, D...');
const tabbedQuiz = [
    'Câu 1: Giá trị của biểu thức.',
    'A. Phương án 1*\tB. Phương án 2',
    'C. Phương án 3\tD. Phương án 4',
    'Câu 2: Câu hỏi cột ngang.',
    'A. Một*  B. Hai',
    'C. Ba  D. Bốn',
    'Đáp án:',
    '1.A   2.A'
].join('\n');
const normalizedTabs = normalizeImportedQuizText(tabbedQuiz);
assert.match(normalizedTabs, /\nB\. Phương án 2/);
assert.match(normalizedTabs, /\nD\. Phương án 4/);
assert.match(normalizedTabs, /\nB\. Hai/);
assert.match(normalizedTabs, /\nD\. Bốn/);
const parsedTabs = parseLatexWordQuiz(tabbedQuiz);
assert.strictEqual(parsedTabs.length, 2);
assert.strictEqual(parsedTabs[0].type, 'mc');
assert.strictEqual(parsedTabs[0].options[1], 'Phương án 2');
assert.strictEqual(parsedTabs[0].options[3], 'Phương án 4');
assert.strictEqual(parsedTabs[0].correct_index, 0);
assert.strictEqual(parsedTabs[1].options[1], 'Hai');
assert.strictEqual(parsedTabs[1].options[3], 'Bốn');
console.log('✓ Tab và 2 khoảng trắng tách A/B/C/D thành từng dòng; không rơi B, D.');

console.log('\n[TEST 5] Bảng đáp án 17 câu: 12 MC + 1 TF 4 ý + 4 số...');
const keyText = normalizeImportedQuizText([
    'Đáp án:',
    '1.A   2.B   3.C   4.D   5.A   6.B   7.C   8.D   9.A   10.B   11.C   12.D',
    '13. a.Đúng b.Sai c.Đúng d.Sai',
    '14. 25   15. 3.5   16. 100   17. -4'
].join('\n'));
const answerKey = getImportedAnswerKey(keyText);
assert.strictEqual(Object.keys(answerKey).length, 17);
MC_LETTERS.forEach((letter, idx) => {
    assert.strictEqual(answerKey[idx + 1].type, 'mc');
    assert.strictEqual(answerKey[idx + 1].value, letter);
});
assert.strictEqual(answerKey[13].type, 'tf');
assert.deepStrictEqual(clone(answerKey[13].value), TF_ANSWERS);
assert.strictEqual(answerKey[14].value, '25');
assert.strictEqual(answerKey[15].value, '3.5');
assert.strictEqual(answerKey[16].value, '100');
assert.strictEqual(answerKey[17].value, '-4');
console.log('✓ getImportedAnswerKey nhận đủ 17 cặp theo chuẩn mới.');

console.log('\n================================================================================');
console.log('TẤT CẢ KIỂM THỬ ĐỒNG BỘ CV 7991 17 CÂU ĐÃ PASS 100%!');
console.log('================================================================================');
