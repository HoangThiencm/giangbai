const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'nghiencuubaihoc.html'), 'utf8');
const has = (value, label = value) => assert(html.includes(value), `Missing: ${label}`);

function extractBracketed(source, startToken, openCh, closeCh) {
    const start = source.indexOf(startToken);
    assert(start >= 0, `missing ${startToken}`);
    const openAt = source.indexOf(openCh, start);
    let depth = 0;
    for (let i = openAt; i < source.length; i++) {
        if (source[i] === openCh) depth++;
        else if (source[i] === closeCh) {
            depth--;
            if (depth === 0) return source.slice(start, i + 1);
        }
    }
    throw new Error(`unclosed ${startToken}`);
}

function extractFunction(source, name) {
    const startToken = `function ${name}(`;
    const start = source.indexOf(startToken);
    assert(start >= 0, `missing function ${name}`);
    const openAt = source.indexOf('{', start);
    let depth = 0;
    for (let i = openAt; i < source.length; i++) {
        if (source[i] === '{') depth++;
        else if (source[i] === '}') {
            depth--;
            if (depth === 0) return source.slice(start, i + 1);
        }
    }
    throw new Error(`unclosed function ${name}`);
}

const ctx = {};
vm.createContext(ctx);
vm.runInContext(
    extractBracketed(html, 'const STEPS = [', '[', ']')
        .replace('const STEPS = ', 'STEPS = ') + ';\n' +
    extractBracketed(html, 'const PRODUCTS_13 = [', '[', ']')
        .replace('const PRODUCTS_13 = ', 'PRODUCTS_13 = ') + ';\n' +
    extractBracketed(html, 'const PHASES_4 = [', '[', ']')
        .replace('const PHASES_4 = ', 'PHASES_4 = ') + ';\n' +
    extractFunction(html, 'phaseOfStep') + ';\n' +
    extractFunction(html, 'productsOfPhase') + ';\n' +
    extractFunction(html, 'phaseProgress') + ';\n' +
    extractFunction(html, 'firstOpenStepOfPhase') + ';\n',
    ctx
);

const host = v => JSON.parse(JSON.stringify(v));
assert.strictEqual(ctx.PHASES_4.length, 4, 'exactly 4 official phases');
assert.deepStrictEqual(host(Array.from(ctx.PHASES_4, p => p.id)), [1, 2, 3, 4]);
assert.deepStrictEqual(host(ctx.PHASES_4[0].steps), [1, 2, 3, 4, 5, 6, 7]);
assert.deepStrictEqual(host(ctx.PHASES_4[1].steps), [8]);
assert.deepStrictEqual(host(ctx.PHASES_4[2].steps), [9, 10]);
assert.deepStrictEqual(host(ctx.PHASES_4[3].steps), [11, 12]);

const allSteps = host(Array.from(ctx.PHASES_4, p => p.steps).flat());
assert.deepStrictEqual([...allSteps].sort((a, b) => a - b), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], '12 micro-steps must cover 1..12');
assert.strictEqual(new Set(allSteps).size, 12, 'no duplicated micro-steps across phases');
assert.strictEqual(ctx.STEPS.length, 12);
assert.strictEqual(ctx.PRODUCTS_13.length, 13);

['emerald', 'blue', 'amber', 'purple'].forEach((color, i) => {
    assert.strictEqual(ctx.PHASES_4[i].color, color, `phase ${i + 1} color`);
});
['fa-book-open-reader', 'fa-chalkboard-user', 'fa-comments', 'fa-award'].forEach((icon, i) => {
    assert.strictEqual(ctx.PHASES_4[i].icon, icon, `phase ${i + 1} icon`);
});

assert.strictEqual(ctx.phaseOfStep(1).id, 1);
assert.strictEqual(ctx.phaseOfStep(7).id, 1);
assert.strictEqual(ctx.phaseOfStep(8).id, 2);
assert.strictEqual(ctx.phaseOfStep(9).id, 3);
assert.strictEqual(ctx.phaseOfStep(10).id, 3);
assert.strictEqual(ctx.phaseOfStep(11).id, 4);
assert.strictEqual(ctx.phaseOfStep(12).id, 4);

assert.strictEqual(ctx.productsOfPhase(ctx.PHASES_4[0]).length, 9, 'phase 1 products 1-9');
assert.strictEqual(ctx.productsOfPhase(ctx.PHASES_4[1]).length, 1, 'phase 2 product 10');
assert.strictEqual(ctx.productsOfPhase(ctx.PHASES_4[2]).length, 2, 'phase 3 products 11-12');
assert.strictEqual(ctx.productsOfPhase(ctx.PHASES_4[3]).length, 1, 'phase 4 product 13');

const p1active = ctx.phaseProgress(ctx.PHASES_4[0], 3, [1, 2]);
assert.strictEqual(p1active.kind, 'active');
assert.ok(p1active.badge.includes('Đang thực hiện'));
assert.ok(p1active.badge.includes('2/7') || p1active.done === 2);

const p1done = ctx.phaseProgress(ctx.PHASES_4[0], 8, [1, 2, 3, 4, 5, 6, 7]);
assert.strictEqual(p1done.kind, 'done');
assert.ok(p1done.badge.includes('Hoàn thành'));
assert.ok(p1done.badge.includes('7/7'));

const p2active = ctx.phaseProgress(ctx.PHASES_4[1], 8, []);
assert.strictEqual(p2active.kind, 'active');
assert.strictEqual(p2active.total, 1);

const p3pending = ctx.phaseProgress(ctx.PHASES_4[2], 1, []);
assert.strictEqual(p3pending.kind, 'pending');
assert.strictEqual(p3pending.badge, 'Chưa bắt đầu');

assert.strictEqual(ctx.firstOpenStepOfPhase(ctx.PHASES_4[0], []), 1);
assert.strictEqual(ctx.firstOpenStepOfPhase(ctx.PHASES_4[0], [1, 2, 3]), 4);
assert.strictEqual(ctx.firstOpenStepOfPhase(ctx.PHASES_4[0], [1, 2, 3, 4, 5, 6, 7]), 1);
assert.strictEqual(ctx.firstOpenStepOfPhase(ctx.PHASES_4[1], []), 8);
assert.strictEqual(ctx.firstOpenStepOfPhase(ctx.PHASES_4[3], [11]), 12);

[
    'id="phaseBar"',
    'id="stepperBar"',
    'id="phaseGuideModal"',
    'id="phaseGuideBody"',
    'function goToPhase',
    'function renderPhaseBar',
    'function openPhaseGuide',
    'function closePhaseGuide',
    'function goStep',
    'function renderStepper',
    'function emptyState',
    'Sơ đồ 4 bước chuẩn CV 5555',
    '4 bước chuẩn Bộ GD&amp;ĐT (Công văn 5555)',
    '12 bước số hóa chuyên sâu',
    'Công văn 5555/BGDĐT-GDTrH',
    'onclick="goToPhase(',
    'onclick="openPhaseGuide()"',
    'phase-1',
    'phase-2',
    'phase-3',
    'phase-4',
    'GĐ ${phase.id} · Bước ${s.n}',
    "runAiTask",
    'function saveSession',
    'function loadSessionById',
    'function exportZip',
    'function exportAllDocx'
].forEach(x => has(x));

assert(html.includes("const CAN_CU = ["), 'CAN_CU must remain');
assert(html.includes("completedSteps: []"), 'emptyState.completedSteps must remain');
assert(html.includes('currentStep: 1'), 'emptyState.currentStep must remain');
assert(!html.includes('Chu trình NCBH sư phạm · 12 bước · KHBD 2 lớp</p>'), 'old 12-step-only subtitle must be replaced');

const inlineScripts = html.match(/<script>([\s\S]*?)<\/script>/g) || [];
assert(inlineScripts.length >= 1, 'inline application script missing');
inlineScripts.forEach((block, i) => {
    const inner = block.replace(/^<script>/, '').replace(/<\/script>$/, '');
    assert(!inner.includes('</script>'), `inline script ${i} must not contain nested </script>`);
});

console.log('nghiencuubaihoc-phases-test: 4 phases cover 12 steps uniquely, UI phase bar + CV 5555 modal, progress badges, goToPhase mapping passed');
