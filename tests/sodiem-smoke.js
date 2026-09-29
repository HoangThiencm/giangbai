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
requireMatch(page, /function deleteStudent\(index\)/, 'Missing deleteStudent.');
requireMatch(page, /<button onclick="deleteStudent\(\$\{index\}\)" class="text-rose-600 hover:text-rose-800 p-1 ml-1" title="Xóa học sinh"><i class="fa fa-trash"><\/i><\/button>/, 'Each grade row needs a rose trash button.');
requireMatch(page, /Bạn có chắc chắn muốn xóa học sinh \$\{student\.name\} \(Mã: \$\{student\.sbd\}\) khỏi sổ điểm\? Điểm số của học sinh này sẽ bị xóa\./, 'deleteStudent must confirm name, code, and score loss.');
requireMatch(page, /students\.splice\(index,1\)/, 'deleteStudent must remove the student from the list.');
requireMatch(page, /deletedStudentKeys\.includes\(key\)/, 'mergeStudents must skip deleted student keys.');
requireMatch(page, /rememberDeletedKeys\(studentKeys\(student\)\)/, 'deleteStudent must record the deleted student key.');
requireMatch(page, /onchange="students\[\$\{index\}\]\.sbd=this\.value;persist\(\);triggerAutoSave\(\)"/, 'SBD edits must auto-save.');
requireMatch(page, /onchange="students\[\$\{index\}\]\.name=this\.value;persist\(\);triggerAutoSave\(\)"/, 'Name edits must auto-save.');
requireMatch(page, /onchange="students\[\$\{index\}\]\.comment=this\.value;persist\(\);triggerAutoSave\(\)"/, 'Comment edits must auto-save.');
requireMatch(page, /function addStudent\(\)\{students\.push\(normalizeStudent\(\{\},students\.length\)\);renderAll\(\);persist\(\);triggerAutoSave\(\)\}/, 'Adding a student must auto-save.');
requireMatch(page, /function pasteStudents\(\)\{[\s\S]*renderAll\(\);persist\(\);triggerAutoSave\(\)\}/, 'Pasting students must auto-save.');
requireMatch(api, /CREATE TABLE IF NOT EXISTS gradebooks/, 'Gradebook schema is required.');
['load', 'save', 'classes'].forEach(action => requireMatch(api, new RegExp(`action === '${action}'`), `API must provide ${action} action.`));
console.log('sodiem smoke: PASS');
