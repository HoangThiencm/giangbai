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
    ['prompt_version format-lock', LI.PROMPT_VERSION.includes('format-lock')],
    ['skills', pkg.skills.length >= 2],
    ['questions', pkg.questions.length >= 5],
    ['questions have skill', pkg.questions.every(q => q.skill)],
    ['drag match+sort (' + pkg.drag_exercises.length + ')', pkg.drag_exercises.length >= 2],
    ['fill', pkg.fill_exercises.length >= 2],
    ['essay', pkg.essay_exercises.length >= 2],
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
} else if (!LI.getInteractiveFormatGuide().includes('CẤM bảng Markdown') && !LI.getInteractiveFormatGuide().includes('CẤM bảng')) {
    console.error('FAIL: format guide missing markdown table ban');
    failed += 1;
} else {
    console.log('OK: interactive format guide');
}

// Junk markdown-table rows must be rejected
const junkTable = `NỐI Ô
Cột A | Cột B
:--- | :---
$2^2 \\cdot 3 + 1$ | 13
$20 - 2 \\cdot 5$ | 10`;
const junkDrag = LI.parseDragExercises(junkTable, { preferMatch: true });
if (junkDrag.some(d => /cột/i.test(d.prompt) || d.prompt.includes(':---'))) {
    console.error('FAIL: junk table headers accepted as drag', junkDrag);
    failed += 1;
} else if (junkDrag.some(d => (d.items || []).length === 1 && (d.mode === 'sort'))) {
    console.error('FAIL: single-cell table rows accepted as sort', junkDrag);
    failed += 1;
} else {
    console.log('OK: markdown table junk filtered from drag');
}

const junkPkg = LI.normalizeLessonImportPackage({
    schema_version: 'lesson-import-v1',
    subject: 'Toán 6',
    title: 'Test junk',
    slug: 'test-junk',
    skills: [{ id: '', name: '---', target: 80 }, { id: 'ok', name: 'Kỹ năng OK', target: 80 }],
    tasks: ['---', 'Đọc lý thuyết'],
    essay_exercises: [{ id: 'e1', prompt: 'Tính 1+1', answer: '2 ---', hint: '' }],
    drag_exercises: [{ id: 'd1', mode: 'sort', prompt: 'Cột A', items: ['Cột B'], answer: ['Cột B'], hint: '' }]
});
if (junkPkg.skills.some(s => !s.id || s.name === '---')) {
    console.error('FAIL: junk skills not filtered', junkPkg.skills);
    failed += 1;
} else if (junkPkg.tasks.some(t => t === '---')) {
    console.error('FAIL: junk tasks not filtered', junkPkg.tasks);
    failed += 1;
} else if (String(junkPkg.essay_exercises[0]?.answer || '').includes('---')) {
    console.error('FAIL: essay --- not stripped', junkPkg.essay_exercises[0]);
    failed += 1;
} else if (junkPkg.drag_exercises.length) {
    console.error('FAIL: weak/junk drag not filtered', junkPkg.drag_exercises);
    failed += 1;
} else {
    console.log('OK: normalize strips --- / weak drag / empty skills');
}

const incompleteValidation = LI.validateLessonImportPackage({
    schema_version: 'lesson-import-v1',
    subject: 'Toán 6',
    title: 'Thiếu tương tác',
    slug: 'thieu-tuong-tac',
    essay_exercises: [],
    fill_exercises: [],
    drag_exercises: [],
    questions: [],
    skills: [{ id: 'a', name: 'A', target: 80 }]
}, { strictStructure: true });
if (!(incompleteValidation.errors || []).some(e => /TRẮC NGHIỆM|trắc nghiệm|KÉO THẢ|NỐI Ô/i.test(e))) {
    console.error('FAIL: strictStructure should error on empty interactive', incompleteValidation.errors);
    failed += 1;
} else {
    console.log('OK: strictStructure blocks empty interactive export');
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

const theoryWithCompareSection = `LÝ THUYẾT
### 3. Số liền trước và số liền sau
- **Số liền trước** của một số ít hơn số đó $1$ đơn vị.

### 4. So sánh
- Trên dãy số, các số được sắp xếp theo thứ tự tăng dần từ trái sang phải.
- Số có nhiều chữ số hơn thì lớn hơn.

**DANH SÁCH HÌNH ẢNH CẦN TẠO**
HINH_01: theory | Bảng | diagram | Prompt`;

const theorySections = LI.parseGeminiLessonSections(theoryWithCompareSection);
if (!/4\.\s*So sánh/i.test(theorySections.theory || '')) {
    console.error('FAIL: theory section 4 lost during parse', theorySections.theory);
    failed += 1;
} else if (!/sắp xếp/i.test(theorySections.theory || '')) {
    console.error('FAIL: theory compare bullet lost during parse', theorySections.theory);
    failed += 1;
} else if (theorySections.dragSort) {
    console.error('FAIL: theory prose misclassified as dragSort', theorySections.dragSort);
    failed += 1;
} else {
    console.log('OK: theory keeps section 4 when bullet contains "sắp xếp"');
}

const theoryMarkdownHeadings = `### MỤC TIÊU BÀI HỌC
Sau bài học này, học sinh nắm phép nhân và chia.

### LÝ THUYẾT
### 1. Phép nhân số tự nhiên
Tích $a \\times b$ là tổng $a$ số hạng bằng $b$.

### 4. So sánh
- Trên dãy số, các số được sắp xếp theo thứ tự tăng dần từ trái sang phải.`;

const markdownTheoryPkg = LI.buildLessonImportPackage({
    rawGeminiText: '',
    theoryGeminiText: theoryMarkdownHeadings,
    restGeminiText: '**VÍ DỤ**\nDẠNG 1: Tính | 2 x 3 = 6',
    metadata: { subject: 'Toán 6', chapter: 'Ch 1', title: 'Bài 5', tool: 'smoke-test' }
});
if (!markdownTheoryPkg.goal_text) {
    console.error('FAIL: markdown ### MỤC TIÊU not parsed to goal_text');
    failed += 1;
} else if (!markdownTheoryPkg.theory.length) {
    console.error('FAIL: markdown ### LÝ THUYẾT not parsed to theory blocks', markdownTheoryPkg.theory);
    failed += 1;
} else if (!/Phép nhân số tự nhiên/i.test(markdownTheoryPkg.theory[0].text || '')) {
    console.error('FAIL: theory block missing subsection content', markdownTheoryPkg.theory[0]);
    failed += 1;
} else if (!/sắp xếp/i.test((markdownTheoryPkg.theory.map(b => b.text).join('\n')))) {
    console.error('FAIL: markdown theory lost section 4 with sap xep');
    failed += 1;
} else {
    console.log('OK: markdown ### MỤC TIÊU / ### LÝ THUYẾT export to JSON');
}

if (failed) process.exit(1);
console.log('\nAll smoke checks passed.');
