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

if (failed) process.exit(1);
console.log('\nAll smoke checks passed.');