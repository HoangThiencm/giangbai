const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const crosswordHtml = fs.readFileSync(path.join(root, 'game-crossword.html'), 'utf8');
const racingHtml = fs.readFileSync(path.join(root, 'game-racing.html'), 'utf8');
const bellHtml = fs.readFileSync(path.join(root, 'game-bell.html'), 'utf8');
const trochoiJs = fs.readFileSync(path.join(root, 'trochoi.compiled.js'), 'utf8');
const accessJs = fs.readFileSync(path.join(root, 'access-control.js'), 'utf8');

assert.match(crosswordHtml, /MathText/, 'game-crossword.html phải có component MathText để render công thức');
assert.match(crosswordHtml, /entries\.slice\(0,\s*10\)|slice\(0,\s*Math\.min\(10/, 'game-crossword.html phải giới hạn số hàng ngang tối đa 10');
assert.match(crosswordHtml, /kw-col/, 'game-crossword.html có highlight cột từ khóa');
assert.match(racingHtml, /numTeams|setNumTeams|teams/, 'game-racing.html có cấu hình số tổ đua');
assert.match(racingHtml, /Tổ 5|t5|DEFAULT_TEAMS/, 'game-racing.html hỗ trợ linh hoạt các tổ (ít nhất đến tổ 5/6)');
assert.match(bellHtml, /Rung Chuông Vàng/i, 'game-bell.html có tiêu đề Rung Chuông Vàng');
assert.match(bellHtml, /MathText/, 'game-bell.html hỗ trợ MathText KaTeX');
assert.match(bellHtml, /cứu trợ|cuuTro|revive/i, 'game-bell.html có cơ chế cứu trợ thí sinh');
assert.match(bellHtml, /confetti|canvas-confetti/i, 'game-bell.html có pháo hoa chúc mừng rung chuông');
assert.match(trochoiJs, /id:\s*'bell'/, 'trochoi.compiled.js đã đăng ký game bell');
assert.ok(!trochoiJs.includes('Quay lại SmartQuiz'), 'trochoi.compiled.js đã xóa hoàn toàn Quay lại SmartQuiz');
assert.match(accessJs, /'game-bell\.html':\s*'smartquiz'/, 'access-control.js bảo vệ route game-bell.html');
console.log('game-suite smoke: PASS');
