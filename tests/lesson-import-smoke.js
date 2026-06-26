/**
 * Smoke test lesson-import.js (chạy: node tests/lesson-import-smoke.js)
 * Cần Node 18+
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.join(__dirname, '..');
const code = fs.readFileSync(path.join(root, 'lesson-import.js'), 'utf8');
const sandbox = { window: {}, console };
vm.runInNewContext(code, sandbox);
const LI = sandbox.window.LessonImport;

if (!LI) {
    console.error('FAIL: LessonImport không export');
    process.exit(1);
}

const raw = fs.readFileSync(path.join(__dirname, 'fixtures', 'gemini-raw-sample.txt'), 'utf8');
const pkg = LI.buildLessonImportPackage({
    rawGeminiText: raw,
    metadata: { subject: 'Toán 6', chapter: 'Chương 1', title: 'Bài 1: Tập hợp', tool: 'smoke-test' }
});

const validation = LI.validateLessonImportPackage(pkg, { pageSubject: 'Toán 6' });
const errors = validation.errors || [];

const checks = [
    ['schema', pkg.schema_version === 'lesson-import-v1'],
    ['skills', pkg.skills.length >= 2],
    ['questions', pkg.questions.length >= 2],
    ['questions have skill', pkg.questions.every(q => q.skill)],
    ['drag match+sort (' + pkg.drag_exercises.length + ')', pkg.drag_exercises.length >= 2],
    ['fill', pkg.fill_exercises.length >= 1],
    ['essay', pkg.essay_exercises.length >= 1],
    ['self practice', pkg.self_practice.length >= 1],
    ['image manifest', pkg.image_manifest.length >= 1],
    ['is_published false', pkg.is_published === false],
    ['no validate errors', errors.length === 0]
];

let failed = 0;
checks.forEach(([name, ok]) => {
    if (!ok) { console.error('FAIL:', name); failed += 1; }
    else console.log('OK:', name);
});

// Idempotency: drag round-trip
const dragText = 'Nối | A » B | 1 » 2 | 0-0,1-1 | gợi';
const parsed = LI.parseDragExercises(dragText, { preferMatch: true });
const items = parsed.map(item => ({
    de: item.prompt,
    trai: LI.joinPoolText(item.left || item.items),
    phai: LI.joinPoolText(item.right || item.answer),
    map: item.pair_spec || '',
    goi: item.hint || ''
}));
const rebuilt = LI.buildDragExercisesFromItems(items);
if (rebuilt[0]?.mode !== 'match' || rebuilt[0]?.pairs?.length !== 2) {
    console.error('FAIL: drag idempotency');
    failed += 1;
} else {
    console.log('OK: drag idempotency');
}

const messyMatchLine = '- Đề: Nối số với cách đọc tương ứng | Trái » 60 006, 66 000 | Phải » Sáu mươi nghìn không trăm linh sáu, Sáu mươi sáu nghìn | Nối » 0-0, 1-1 | gợi ý: Đọc kỹ các chữ số ở hàng nghìn và hàng đơn vị.';
const messyParsed = LI.parseDragExercises(messyMatchLine, { preferMatch: true });
if (messyParsed.length !== 1 || messyParsed[0].mode !== 'match') {
    console.error('FAIL: messy match line parse');
    failed += 1;
} else if (messyParsed[0].left.join('|') !== '60 006|66 000') {
    console.error('FAIL: messy match left', messyParsed[0].left);
    failed += 1;
} else if (messyParsed[0].pairs.length !== 2) {
    console.error('FAIL: messy match pairs', messyParsed[0].pairs);
    failed += 1;
} else {
    console.log('OK: messy match line canonicalized');
}

const messySortLine = 'Sắp xếp từ bé đến lớn: 12 500; 9 800; 12 050; 12 505 | 12 500 » 9 800 » 12 050 » 12 505 | 9 800 » 12 050 » 12 500 » 12 505 | So sánh hàng nghìn';
const messySortParsed = LI.parseDragExercises(messySortLine);
const sortItem = messySortParsed[0];
const sortSig = arr => [...arr].map(x => String(x).trim()).sort().join('|');
if (!sortItem || sortItem.mode !== 'sort' || sortSig(sortItem.items) !== sortSig(sortItem.answer)) {
    console.error('FAIL: messy sort line', sortItem);
    failed += 1;
} else {
    console.log('OK: messy sort line canonicalized');
}

if (typeof LI.getInteractiveFormatGuide === 'function' && !LI.getInteractiveFormatGuide().includes('lesson-import-v1')) {
    console.error('FAIL: interactive format guide');
    failed += 1;
} else {
    console.log('OK: interactive format guide');
}

const messyEssay = `BÀI TẬP TỰ LUẬN NGẮN
- **Câu 1:** Viết số gồm 4 chục nghìn, 5 nghìn, 6 trăm và 2 đơn vị
**Đáp án:** 45 602
**Gợi ý:** Đọc từng hàng
Viết số 66 006 | 66006 | Đếm hàng`;

const messyEssayParsed = LI.parseEssayExercises(messyEssay);
if (messyEssayParsed.length < 2) {
    console.error('FAIL: messy essay parse count', messyEssayParsed.length);
    failed += 1;
} else if (!String(messyEssayParsed[0].answer || '').replace(/\s/g, '').includes('45602')) {
    console.error('FAIL: messy essay answer merge', messyEssayParsed[0]);
    failed += 1;
} else if (!messyEssayParsed[0].hint) {
    console.error('FAIL: messy essay hint', messyEssayParsed[0]);
    failed += 1;
} else {
    console.log('OK: messy essay markdown canonicalized');
}

const messySortCau = '**Câu 1:** 45 006 | 12 500 » 9 800 » 12 050 | 9 800 » 12 050 » 12 500 | So sánh hàng nghìn';
const messySortCauParsed = LI.parseDragExercises(messySortCau);
if (!messySortCauParsed[0] || !/45\s*006/.test(messySortCauParsed[0].prompt)) {
    console.error('FAIL: sort cau prefix strip', messySortCauParsed[0]);
    failed += 1;
} else {
    console.log('OK: sort cau prefix stripped');
}

if (failed) process.exit(1);
console.log('\nAll smoke checks passed.');