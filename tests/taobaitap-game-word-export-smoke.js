/** Smoke test: Game-compatible Word export structure. Node 18+. */
'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const importer = require('../js/game-quiz-importer.js');

function buildGameText() {
    return [
        'Câu 1: Giải phương trình \\(... x^2 = 4 \\).', 'A. 2', 'B. 3', 'C. 4', 'D. 5', 'Đáp án: A', '',
        'Câu 2: Mệnh đề đúng?', 'A. Đúng', 'B. Sai', 'Đáp án: A', '',
        'Câu 3: Đề CV - Mệnh đề a: 1 + 1 = 2', 'A. Đúng', 'B. Sai', 'Đáp án: A', '',
        'Câu 4: Điền kết quả: 2 + 2 = ?', 'A. 4', 'B. Đáp án khác', 'Đáp án: A', '',
        'Khái niệm A - Định nghĩa A', '',
        'BẢNG ĐÁP ÁN:', '1.A   2.A   3.A   4.A'
    ].join('\n');
}

const text = buildGameText();
const quiz = importer.parseQuizQuestions(text);
const pairs = importer.parseMatchingPairs('Khái niệm A - Định nghĩa A');
assert.ok(quiz.length >= 4, 'must parse multiple choice, true/false, CV7991 item, and fill blank');
assert.equal(quiz[0].choices[quiz[0].answer], '2');
assert.ok(quiz[0].prompt.includes('\\(... x^2 = 4 \\)'), 'must preserve LaTex');
assert.equal(quiz[1].choices[quiz[1].answer], 'Đúng');
assert.equal(quiz[2].choices[quiz[2].answer], 'Đúng');
assert.deepEqual(pairs[0] && [pairs[0].left, pairs[0].right], ['Khái niệm A', 'Định nghĩa A']);

const root = path.join(__dirname, '..');
for (const relativeFile of ['taobaitap.html', path.join('backupcode viettailieu', 'taobaitap.html'), 'smartquiz.html']) {
    const html = fs.readFileSync(path.join(root, relativeFile), 'utf8');
    assert.ok(html.includes('const exportWordForGame = () =>'), `${relativeFile}: export function`);
    assert.ok(html.includes('De_Thi_Game_Giao_Duc.docx'), `${relativeFile}: game DOCX filename`);
    assert.ok(html.includes('BẢNG ĐÁP ÁN:'), `${relativeFile}: answer key`);
    assert.ok(html.includes('Xuất Word cho Game'), `${relativeFile}: export button`);
    const start = html.indexOf('const exportWordForGame = () =>');
    const end = html.indexOf(relativeFile === 'smartquiz.html' ? 'const startPresentation' : 'const exportWordLatex', start);
    assert.ok(!html.slice(start, end).includes('convertToMathML'), `${relativeFile}: does not convert LaTex to MathML`);
}

console.log('ALL taobaitap game-word-export smoke checks passed.');
