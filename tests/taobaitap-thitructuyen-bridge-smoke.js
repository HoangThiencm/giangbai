/** Smoke: liên thông 1-Click Tạo bài tập → Thi trực tuyến + cờ cuốn chiếu/watermark. Node 18+. */
'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.join(__dirname, '..');
const taoHtml = fs.readFileSync(path.join(root, 'taobaitap.html'), 'utf8');
const backupTaoHtml = fs.readFileSync(path.join(root, 'backupcode viettailieu', 'taobaitap.html'), 'utf8');
const thiHtml = fs.readFileSync(path.join(root, 'thitructuyen.html'), 'utf8');

function extractFn(html, startNeedle, endNeedle) {
    const start = html.indexOf(startNeedle);
    const end = html.indexOf(endNeedle, start + 1);
    assert.ok(start >= 0 && end > start, `Phải trích được khối từ ${startNeedle.slice(0, 40)}`);
    return html.slice(start, end);
}

console.log('================================================================================');
console.log('KIỂM THỬ LIÊN THÔNG TẠO BÀI TẬP ↔ THI TRỰC TUYẾN + CUỐN CHIẾU');
console.log('================================================================================');

console.log('\n[TEST 1] Nút THI TRỰC TUYẾN + hàm đóng gói trên taobaitap (root + backup)...');
for (const [label, html] of [['root', taoHtml], ['backup', backupTaoHtml]]) {
    assert.match(html, /🚀 THI TRỰC TUYẾN/, `${label}: phải có nút THI TRỰC TUYẾN`);
    assert.match(html, /const mapToThiTrucTuyenPayload/, `${label}: phải có mapToThiTrucTuyenPayload`);
    assert.match(html, /const startOnlineExam/, `${label}: phải có startOnlineExam`);
    assert.match(html, /thitructuyen_pending_import/, `${label}: phải ghi localStorage pending import`);
    assert.match(html, /thitructuyen\.html\?from=taobaitap/, `${label}: phải mở thitructuyen?from=taobaitap`);
    assert.match(html, /anti_ai_one_by_one:\s*true/, `${label}: payload bật cuốn chiếu`);
    assert.match(html, /anti_ai_watermark:\s*true/, `${label}: payload bật watermark`);
    assert.match(html, /duration:\s*15/, `${label}: mặc định 15 phút`);
}
console.log('✓ Cả 2 bản taobaitap có nút + đóng gói 1-Click.');

console.log('\n[TEST 2] mapToThiTrucTuyenPayload chuyển đúng mc/tf/short_answer...');
const mapperSrc = extractFn(
    taoHtml,
    '            const mapToThiTrucTuyenPayload = (quizItems, topicList, form) => {',
    '            const startOnlineExam = () => {'
);
const sandbox = {
    isCv7991TrueFalseItem: (q) => Array.isArray(q?.correct_answers) && q.correct_answers.length >= 2
        || Array.isArray(q?.subItems) && q.subItems.length >= 2
        || (Array.isArray(q?.options) && q.options.length >= 3),
    getCv7991TrueFalseItems: (q) => {
        const opts = Array.isArray(q.options) ? q.options : [];
        const answers = Array.isArray(q.correct_answers) ? q.correct_answers : [];
        return [0, 1, 2, 3].map((i) => ({ text: opts[i] || '', isCorrect: !!answers[i] }));
    },
    cleanOptionText: (t) => String(t || '').replace(/^[A-Da-d][\.\)\-:]\s*/, '').trim(),
    normalizeShortAnswerValue: (raw) => String(raw || '').replace(/[^\d.\-]/g, '') || String(raw || '').trim()
};
vm.createContext(sandbox);
vm.runInContext(mapperSrc + '\nthis.mapToThiTrucTuyenPayload = mapToThiTrucTuyenPayload;', sandbox);
const payload = sandbox.mapToThiTrucTuyenPayload([
    { type: 'multiple-choice', question: 'MC1', options: ['A1', 'B1', 'C1', 'D1'], correctAnswerIndex: 2 },
    {
        type: 'true-false',
        question: 'TF1',
        options: ['ý a', 'ý b', 'ý c', 'ý d'],
        correct_answers: [true, false, true, false]
    },
    { type: 'short-answer', question: 'SA1', correctAnswer: 'x = 25 cm' }
], [{ name: 'Hàm số bậc nhất' }], 'cv7991');

assert.strictEqual(payload.duration, 15);
assert.strictEqual(payload.exam_format, 'cv7991');
assert.strictEqual(payload.anti_ai_one_by_one, true);
assert.strictEqual(payload.anti_ai_watermark, true);
assert.match(payload.title, /Hàm số bậc nhất/);
assert.strictEqual(payload.questions.length, 3);
assert.strictEqual(payload.questions[0].type, 'mc');
assert.strictEqual(payload.questions[0].correct_index, 2);
assert.strictEqual(payload.questions[1].type, 'tf');
assert.deepStrictEqual(payload.questions[1].correct_answers, [true, false, true, false]);
assert.strictEqual(payload.questions[1].options.length, 4);
assert.strictEqual(payload.questions[2].type, 'short_answer');
assert.strictEqual(String(payload.questions[2].correct_answer), '25');
console.log('✓ Payload 3 loại câu đúng chuẩn thitructuyen.');

console.log('\n[TEST 3] thitructuyen tiếp nhận pending_import + preset thời gian + checkbox...');
assert.match(thiHtml, /thitructuyen_pending_import/, 'phải đọc pending import');
assert.match(thiHtml, /setStep\(2\)/, 'phải nhảy Bước 2');
assert.match(thiHtml, /anti_ai_one_by_one/, 'phải có cờ cuốn chiếu');
assert.match(thiHtml, /anti_ai_watermark/, 'phải có cờ watermark');
assert.match(thiHtml, /\[15,\s*20,\s*30,\s*45\]/, 'phải có nút chọn nhanh 15/20/30/45');
assert.match(thiHtml, /Chế độ thi cuốn chiếu từng câu/, 'checkbox cuốn chiếu');
assert.match(thiHtml, /Watermark bảo mật/, 'checkbox watermark');
assert.match(thiHtml, /matrixConfig/, 'lưu cờ qua matrixConfig khi save');
assert.match(thiHtml, /handleEdit = async \(id\)/, 'phải có Sửa đề (handleEdit)');
assert.match(thiHtml, /anti_ai_one_by_one: !!\(info\.anti_ai_one_by_one \?\? matrix\.anti_ai_one_by_one\)/, 'Sửa đề cũ phải khôi phục cờ cuốn chiếu từ matrixConfig');
assert.match(thiHtml, /anti_ai_watermark: !!\(info\.anti_ai_watermark \?\? matrix\.anti_ai_watermark\)/, 'Sửa đề cũ phải khôi phục cờ watermark từ matrixConfig');
assert.match(thiHtml, /giaovien@giangbai\.local/, 'from=taobaitap phải có fallback userEmail tránh trang trắng');
assert.match(thiHtml, /typeof Sortable !== ["']undefined["']/, 'Sortable phải được guard trước khi new Sortable');
assert.match(thiHtml, /from'\) === 'taobaitap'|from"\) === "taobaitap"/, 'phải nhận diện query from=taobaitap');
assert.match(thiHtml, /access-control\.js\?v=20260919-taobaitap-bridge/, 'cache-buster access-control phải là 20260919-taobaitap-bridge');
assert.match(thiHtml, /class ErrorBoundary extends React\.Component/, 'phải có ErrorBoundary chống trắng màn hình');
assert.match(thiHtml, /root\.render\(<ErrorBoundary><App \/><\/ErrorBoundary>\)/, 'App phải được bọc ErrorBoundary');
assert.match(thiHtml, /const str = String\(text \?\? ""\)\.trim\(\);\s*\n\s*if \(!str\) return "";\s*\n\s*return str\.replace\(\/\^\(\[A-Da-d0-9\]\+\)/, 'cleanOptionText phải ép String trước replace');
assert.match(thiHtml, /const raw = String\(text \?\? ''\);/, 'MathText phải ép String(text) trước khi render');
assert.match(thiHtml, /String\(processedText\)\.split/, 'MathText phải ép String trước split');
assert.match(thiHtml, /const \[editingData, setEditingData\] = useState\(\(\) => \{/, 'App phải khởi tạo editingData đồng bộ từ pending_import');
assert.match(thiHtml, /const \[view, setView\] = useState\(\(\) => \(editingData \|\| isFromTaobaitap\) \? "create" : "dashboard"\)/, 'App phải khởi tạo view=create đồng bộ khi from=taobaitap');
assert.match(thiHtml, /return \[\{ id: "imported"/, 'HybridExamCreator phải khởi tạo pages đồng bộ khi có initialData.questions');

const accessJs = fs.readFileSync(path.join(root, 'access-control.js'), 'utf8');
assert.match(accessJs, /params\.get\(['"]from['"]\) === ['"]taobaitap['"]/, 'access-control phải miễn check token khi from=taobaitap');

// Runtime: số trong options không được làm sập cleanOptionText / cleanQuestionPrefix
const helperSrc = extractFn(
    thiHtml,
    '        const cleanOptionText = (text) => {',
    '        const MathText = ({ text, cleanPrefix = false }) => {'
);
const helperSandbox = {};
vm.createContext(helperSandbox);
vm.runInContext(helperSrc + '\nthis.cleanOptionText = cleanOptionText;\nthis.cleanQuestionPrefix = cleanQuestionPrefix;', helperSandbox);
assert.strictEqual(helperSandbox.cleanOptionText(1), '1');
assert.strictEqual(helperSandbox.cleanOptionText(0), '0');
assert.strictEqual(helperSandbox.cleanOptionText(null), '');
assert.strictEqual(helperSandbox.cleanQuestionPrefix(1), '1');
assert.doesNotThrow(() => helperSandbox.cleanOptionText(10));
assert.doesNotThrow(() => helperSandbox.cleanQuestionPrefix(10));
console.log('✓ Tiếp nhận đề + cấu hình giáo viên đủ (kể cả đề cũ) + chống trang trắng.');

console.log('\n[TEST 4] UI thi cuốn chiếu + no-backtrack + watermark...');
assert.match(thiHtml, /currentQuestionIdx/, 'state câu hiện tại');
assert.match(thiHtml, /questionTimeLeft/, 'đồng hồ từng câu');
assert.match(thiHtml, /goToNextQuestion/, 'chuyển câu tiếp');
assert.match(thiHtml, /Câu tiếp theo/, 'nút câu tiếp theo');
assert.match(thiHtml, /exam_one_by_one_progress_/, 'lưu tiến trình localStorage');
assert.match(thiHtml, /pointer-events-none fixed inset-0 z-40/, 'lớp watermark cố định');
assert.match(thiHtml, /rotate-\[-25deg\]/, 'watermark xoay -25 độ');
assert.ok(!/goToPrevQuestion|Câu trước|quay lại câu/.test(thiHtml.slice(thiHtml.indexOf('goToNextQuestion'), thiHtml.indexOf('goToNextQuestion') + 2500)), 'không có nút quay lại câu trong luồng cuốn chiếu');
assert.match(thiHtml, /visibleQuestions/, 'chỉ render câu hiện tại khi cuốn chiếu');
console.log('✓ Cuốn chiếu + watermark + khóa quay lại.');

console.log('\n================================================================================');
console.log('TẤT CẢ KIỂM THỬ LIÊN THÔNG / CUỐN CHIẾU ĐÃ PASS 100%!');
console.log('================================================================================');
