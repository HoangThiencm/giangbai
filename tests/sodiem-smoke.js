/* Static smoke checks for the Sổ Điểm & KTTX application. */
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const requireMatch = (text, pattern, message) => { if (!pattern.test(text)) throw new Error(message); };

const page = read('sodiem.html');
const api = read('api/sodiem.php');
['security-guard.js', 'access-control.js', 'xlsx.full.min.js', 'canvas-confetti', 'wheelCanvas', 'spinWheel', 'api/exam.php/student-classes', 'class-students', 'localStorage', 'exportExcel', 'questionInput', 'timer', 'winnerModal'].forEach(token => requireMatch(page, new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')), `Missing ${token} in sodiem.html.`));
['saveStatus','triggerAutoSave','saveBookSilent','beforeunload','keepalive','hasPendingChanges'].forEach(token=>requireMatch(page,new RegExp(token),`Missing auto-save: ${token}.`));
requireMatch(page, /Đã hoàn thành vòng kiểm tra/, 'Wheel must reset after a completed score column.');
requireMatch(page, /scores\[col\]===undefined/, 'Wheel must identify students without a score.');
requireMatch(page, /Array\(s\.scores\[col\]===undefined\?20:1\)\.fill\(s\)/, 'Weighted wheel mode must give scored students 5% of an unscored student weight.');
requireMatch(api, /CREATE TABLE IF NOT EXISTS gradebooks/, 'Gradebook schema is required.');
['load', 'save', 'classes'].forEach(action => requireMatch(api, new RegExp(`action === '${action}'`), `API must provide ${action} action.`));
console.log('sodiem smoke: PASS');
