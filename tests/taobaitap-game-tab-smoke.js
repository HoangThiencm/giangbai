/** Static smoke test: educational-game tab in quiz setup. Node 18+. */
'use strict';

const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const gameUrl = 'https://www.hoangthiencm.id.vn/trochoi.html';
const fullTabFiles = [
    path.join(root, 'taobaitap.html'),
    path.join(root, 'backupcode viettailieu', 'taobaitap.html')
];
const smartQuizFile = path.join(root, 'smartquiz.html');
let failures = 0;

function check(label, ok) {
    console[ok ? 'log' : 'error'](`${ok ? 'OK' : 'FAIL'}: ${label}`);
    if (!ok) failures += 1;
}

for (const file of fullTabFiles) {
    const html = fs.readFileSync(file, 'utf8');
    const label = path.relative(root, file);
    check(`${label}: three-column mode selector`, html.includes('grid grid-cols-3 gap-2 md:gap-4'));
    check(`${label}: Game Giáo dục label`, html.includes('Game Giáo dục'));
    check(`${label}: game URL`, html.includes(`href="${gameUrl}"`));
    check(`${label}: safe new tab`, html.includes('target="_blank" rel="noopener noreferrer"'));
    check(`${label}: game icon`, html.includes('fas fa-gamepad'));
}

const smartQuiz = fs.readFileSync(smartQuizFile, 'utf8');
check('smartquiz.html: game URL', smartQuiz.includes(`href="${gameUrl}"`));
check('smartquiz.html: opens game in new tab', smartQuiz.includes('target="_blank" rel="noopener noreferrer"'));

if (failures) process.exit(1);
console.log('ALL taobaitap game-tab smoke checks passed.');
