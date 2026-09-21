/** Smoke test: guards and option shuffling in QuizPresentationMode. Node 18+. */
'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const files = [
    path.join(root, 'taobaitap.html'),
    path.join(root, 'backupcode viettailieu', 'taobaitap.html'),
    path.join(root, 'smartquiz.html')
];

function shuffleQuestions(questions, settings) {
    const safeSettings = settings || {};
    const shuffleOptions = !!safeSettings.shuffleOptions;
    const safeQuestions = Array.isArray(questions) ? questions : [];
    return safeQuestions.map(q => {
        if (!q || !shuffleOptions || q.type !== 'multiple-choice' || !Array.isArray(q.options) || q.options.length < 2) return q;
        const options = [...q.options];
        const validIdx = (Number.isInteger(q.correctAnswerIndex) && q.correctAnswerIndex >= 0 && q.correctAnswerIndex < options.length) ? q.correctAnswerIndex : 0;
        const correctAnswer = options[validIdx];
        const indices = options.map((_, i) => i).sort(() => Math.random() - 0.5);
        const newOptions = indices.map(i => options[i]);
        const newCorrectIndex = newOptions.indexOf(correctAnswer);
        return { ...q, options: newOptions, correctAnswerIndex: newCorrectIndex >= 0 ? newCorrectIndex : validIdx };
    });
}

const mixedQuestions = [
    { type: 'multiple-choice', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 2 },
    { type: 'true-false', options: ['Đúng', 'Sai'], correctAnswerIndex: 0 },
    { type: 'true-false', subItems: ['a', 'b', 'c', 'd'], correct_answers: [true, false, true, false] },
    { type: 'short-answer', correctAnswer: '42' },
    { type: 'fill-blank', correctAnswer: 'Hà Nội' },
    { type: 'matching', columnA: ['A1'], columnB: ['B1'], correctMatches: [0] },
    null,
    undefined
];

for (const settings of [undefined, {}, { shuffleOptions: false }, { shuffleOptions: true }]) {
    assert.doesNotThrow(() => shuffleQuestions(mixedQuestions, settings));
}
const shuffled = shuffleQuestions(mixedQuestions, { shuffleOptions: true });
assert.equal(shuffled[0].options[shuffled[0].correctAnswerIndex], 'C');
for (const index of [1, 2, 3, 4, 5, 6, 7]) assert.strictEqual(shuffled[index], mixedQuestions[index]);
assert.deepEqual(shuffleQuestions(mixedQuestions, { shuffleOptions: false }), mixedQuestions);

let failures = 0;
for (const file of files) {
    const html = fs.readFileSync(file, 'utf8');
    const label = path.relative(root, file);
    const checks = [
        ['safe settings', html.includes('const safeSettings = settings || {};')],
        ['safe questions', html.includes('const safeQuestions = Array.isArray(questions) ? questions : [];')],
        ['multiple-choice-only shuffle', html.includes("q.type !== 'multiple-choice'")],
        ['options array guard', html.includes('!Array.isArray(q.options) || q.options.length < 2')],
        ['valid correct index', html.includes('const validIdx = (Number.isInteger(q.correctAnswerIndex)')],
        ['missing question fallback UI', html.includes('Không tìm thấy câu hỏi')],
        ['multiple-choice safe map', html.includes('(Array.isArray(q.options) ? q.options : []).map')],
        ['true-false fixed fallback', html.includes("q.options : ['Đúng', 'Sai']")],
        ['matching safe arrays', html.includes('(Array.isArray(q.columnA) ? q.columnA : []).map') && html.includes('(Array.isArray(q.columnB) ? q.columnB : []).map') && html.includes('(Array.isArray(q.correctMatches) ? q.correctMatches : []).map')],
        ['matching comparisons use safe array', html.includes('const safeCorrectMatches = Array.isArray(q.correctMatches) ? q.correctMatches : [];')],
        ['safe fill blank answer', html.includes('const target = String(q.correctAnswer || "").trim().toLowerCase();')]
    ];
    for (const [name, ok] of checks) {
        console[ok ? 'log' : 'error'](`${ok ? 'OK' : 'FAIL'}: ${label}: ${name}`);
        if (!ok) failures += 1;
    }
}

if (failures) process.exit(1);
console.log('ALL taobaitap presentation smoke checks passed.');
