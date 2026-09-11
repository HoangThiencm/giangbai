const assert = require('assert');
const fs = require('fs');
const path = require('path');

console.log('--- TESTING GAME QUIZ IMPORTER AND AI DRAWING ---');

// 1. Require GameQuizImporter
const importerPath = path.join(__dirname, '..', 'js', 'game-quiz-importer.js');
assert.ok(fs.existsSync(importerPath), 'js/game-quiz-importer.js must exist');
const GameQuizImporter = require(importerPath);
assert.ok(GameQuizImporter, 'GameQuizImporter module must be loadable');

// 2. Test MCQ parsing with inline answers and LaTeX formulas
const sampleMcqText = `
Câu 1: Cho hàm số \\(y = f(x)\\) có đồ thị như hình vẽ. Điểm cực tiểu của hàm số là:
A. \\(x = 1\\)
B. \\(x = -2\\)
C. \\(x = 0\\)
D. \\(x = 3\\)
Đáp án: A
Lời giải: Dựa vào bảng biến thiên, hàm số đạt cực tiểu tại điểm \\(x = 1\\).

Câu 2: Nghiệm của phương trình \\(\\log_2(x - 1) = 3\\) là:
A. \\(x = 7\\)
B. \\(x = 8\\)
C. \\(x = 9\\)
D. \\(x = 10\\)
Đáp án: C

Câu 3: Tính tích phân \\(I = \\int_0^1 (2x + 1) dx\\):
A. 1
B. 2
C. 3
D. 4
Đáp án: B
`;

const questions = GameQuizImporter.parseQuizQuestions(sampleMcqText);
assert.strictEqual(questions.length, 3, 'Should parse exactly 3 questions');

// Check question 1
assert.ok(questions[0].prompt.includes('y = f(x)'), 'Question 1 should preserve LaTeX math formula');
assert.strictEqual(questions[0].choices.length, 4, 'Question 1 should have 4 choices');
assert.ok(questions[0].choices[0].includes('x = 1'), 'Choice A should preserve LaTeX math formula');
assert.strictEqual(questions[0].answer, 0, 'Question 1 answer should be 0 (A)');
assert.ok(questions[0].explanation.includes('Dựa vào bảng biến thiên'), 'Question 1 should preserve explanation');

// Check question 2
assert.ok(questions[1].prompt.includes('log_2(x - 1) = 3'), 'Question 2 should preserve LaTeX log formula');
assert.strictEqual(questions[1].answer, 2, 'Question 2 answer should be 2 (C)');

// Check question 3
assert.ok(questions[2].prompt.includes('int_0^1'), 'Question 3 should preserve LaTeX integral');
assert.strictEqual(questions[2].answer, 1, 'Question 3 answer should be 1 (B)');

console.log('-> 1. Parse MCQ with LaTeX and inline answers: PASS');

// 3. Test MCQ parsing with answer key table at bottom
const sampleWithTable = `
Câu 1: Phương trình bậc hai \\(x^2 - 4x + 3 = 0\\) có tích hai nghiệm bằng:
A. 3
B. -3
C. 4
D. -4

Câu 2: Đạo hàm của hàm số \\(y = e^{2x}\\) là:
A. \\(2e^{2x}\\)
B. \\(e^{2x}\\)
C. \\(\\frac{1}{2}e^{2x}\\)
D. \\(4e^{2x}\\)

BẢNG ĐÁP ÁN:
1.A  2.A
`;

const tableQuestions = GameQuizImporter.parseQuizQuestions(sampleWithTable);
assert.strictEqual(tableQuestions.length, 2, 'Should parse 2 questions with answer table');
assert.strictEqual(tableQuestions[0].answer, 0, 'Question 1 should match answer table (A -> 0)');
assert.strictEqual(tableQuestions[1].answer, 0, 'Question 2 should match answer table (A -> 0)');
assert.ok(tableQuestions[0].prompt.includes('x^2 - 4x + 3 = 0'), 'Question 1 should keep LaTeX formula');

console.log('-> 2. Parse MCQ with bottom answer key table: PASS');

// 4. Test Matching pairs parsing
const sampleMatching = `
f'(x) > 0, \\forall x \\in (a, b) - Hàm số đồng biến trên (a, b)
f'(x) < 0, \\forall x \\in (a, b) - Hàm số nghịch biến trên (a, b)
\\int x^\\alpha dx - \\frac{x^{\\alpha+1}}{\\alpha+1} + C (\\alpha \\ne -1)
\\lim_{x \\to 0} \\frac{\\sin x}{x} - 1
\\vec{a} \\cdot \\vec{b} = 0 - Hai vectơ vuông góc
`;

const pairs = GameQuizImporter.parseMatchingPairs(sampleMatching);
assert.strictEqual(pairs.length, 5, 'Should parse 5 matching pairs');
assert.ok(pairs[0].left.includes("f'(x) > 0"), 'Pair 1 left should preserve math text');
assert.ok(pairs[0].right.includes('đồng biến'), 'Pair 1 right should match');

console.log('-> 3. Parse Matching pairs with LaTeX: PASS');

// 5. Test formatForGame schemas for all 8 educational games
const gameTypes = ['elimination', 'speedscore', 'tower', 'unlock', 'teambattle', 'matching', 'treasure', 'escape'];
for (const gt of gameTypes) {
    const formatted = GameQuizImporter.formatForGame(questions, gt, {
        topic: 'Ôn tập Toán 12',
        rawPairs: pairs
    });
    assert.ok(formatted, `Formatted result for game ${gt} must not be null`);
    if (gt === 'matching') {
        assert.ok(Array.isArray(formatted.pairs), 'Matching format must have pairs array');
        assert.ok(formatted.pairs.length >= 3, 'Matching format must contain pairs');
    } else if (gt === 'unlock') {
        assert.ok(Array.isArray(formatted.questions), 'Unlock format must have questions array');
        assert.ok(formatted.codeWord, 'Unlock format must have codeWord');
        assert.ok(formatted.knowledgeCard, 'Unlock format must have knowledgeCard');
    } else if (gt === 'tower') {
        assert.ok(Array.isArray(formatted.questions), 'Tower format must have questions array');
        assert.ok(formatted.questions[0].difficulty, 'Tower questions must have difficulty');
    } else if (gt === 'teambattle') {
        assert.ok(Array.isArray(formatted.questions), 'TeamBattle format must have questions array');
        assert.strictEqual(typeof formatted.questions[0].individual, 'boolean', 'TeamBattle questions must have individual flag');
    } else {
        assert.ok(Array.isArray(formatted.questions), `${gt} format must have questions array`);
        assert.strictEqual(formatted.questions.length, 3, `${gt} questions array length should match input`);
    }
}

console.log('-> 4. Format schema for all 8 educational games: PASS');

// 6. Test AI Drawing model updates & resolution
const vehinhAiPhp = fs.readFileSync(path.join(__dirname, '..', 'api', 'vehinh_ai.php'), 'utf8');
assert.ok(vehinhAiPhp.includes('gemini-3.6-flash'), 'api/vehinh_ai.php must include gemini-3.6-flash in catalog');
assert.ok(vehinhAiPhp.includes('no longer available') || vehinhAiPhp.includes('404'), 'api/vehinh_ai.php must support fallback retry logic');
assert.ok(vehinhAiPhp.includes("'maxOutputTokens' => 8192"), 'api/vehinh_ai.php must use 8192 maxOutputTokens for faster drawing');
assert.ok(!vehinhAiPhp.includes("'maxOutputTokens' => 16384"), 'api/vehinh_ai.php must not keep the slow 16384 token cap');
assert.ok(vehinhAiPhp.includes("'thinkingBudget' => 0"), 'api/vehinh_ai.php must disable thinking budget');
assert.ok(vehinhAiPhp.includes('int $timeout = 30'), 'api/vehinh_ai.php must use 30s curl timeout');
assert.ok(!/int \$timeout = 90/.test(vehinhAiPhp) && !/vehinh_post_json\([^;]*90/.test(vehinhAiPhp), 'api/vehinh_ai.php must not keep 90s timeout');
assert.ok(vehinhAiPhp.includes("$safeFallback = 'gemini-3.6-flash'"), 'candidate list must cap with one safe fallback');
assert.ok(!vehinhAiPhp.includes('foreach (vehinh_provider_models()[\'gemini\'] as $fb)'), 'must not iterate the full 7-model catalog as candidates');
assert.ok(vehinhAiPhp.includes('$status === 400') && vehinhAiPhp.includes('not supported'), 'fast-fail on 400/unsupported model errors');

const runtimeConfigPhp = fs.readFileSync(path.join(__dirname, '..', 'api', 'ai_runtime_config.php'), 'utf8');
assert.ok(runtimeConfigPhp.includes('gemini-3.6-flash'), 'api/ai_runtime_config.php must default to gemini-3.6-flash');

assert.ok(vehinhAiPhp.includes("fallback_model"), 'api/vehinh_ai.php must accept fallback_model from client');
assert.ok(vehinhAiPhp.includes('$requestedFallback'), 'api/vehinh_ai.php must read requested fallback');
assert.ok(vehinhAiPhp.includes("vehinh_provider_models()['gemini']"), 'api/vehinh_ai.php must append catalog after user fallback');
assert.ok(!vehinhAiPhp.includes("$fallbackList = ['gemini-3.6-flash', 'gemini-3.7-flash'"), 'api/vehinh_ai.php must not hardcode a static fallback list');

const appJs = fs.readFileSync(path.join(__dirname, '..', 'app.js'), 'utf8');
assert.ok(appJs.includes('gemini-3.6-flash'), 'app.js must include gemini-3.6-flash in DRAWING_AI_MODEL_CATALOG');
assert.ok(appJs.includes('getSystemDrawingModel'), 'app.js must read system drawing model from settings');
assert.ok(appJs.includes('getSystemDrawingFallbackModel'), 'app.js must read system fallback model');
assert.ok(appJs.includes("localStorage.getItem('khbd_gemini_model')"), 'app.js must prefer khbd_gemini_model');
assert.ok(appJs.includes("localStorage.getItem('default_gemini_module')"), 'app.js must read default_gemini_module');
assert.ok(appJs.includes("localStorage.getItem('khbd_gemini_fallback_model')"), 'app.js must read khbd_gemini_fallback_model');
assert.ok(appJs.includes("localStorage.getItem('default_gemini_fallback')"), 'app.js must read default_gemini_fallback');
assert.ok(appJs.includes('clearDeprecatedSavedDrawingModel'), 'app.js must clear deprecated vehinh_ai_model_gemini');
assert.ok(/DEPRECATED_DRAWING_MODELS\s*=\s*\[[^\]]*gemini-1\.5-flash/.test(appJs), 'deprecated list must only cover retired 1.x models');
assert.ok(!/DEPRECATED_DRAWING_MODELS\s*=\s*\[[^\]]*gemini-2\.5-flash/.test(appJs), 'gemini-2.5-flash must not be treated as deprecated');
assert.ok(appJs.includes('Theo Cài đặt chung'), 'app.js dropdown must include Theo Cài đặt chung');
assert.ok(appJs.includes('DP:'), 'dropdown must show fallback model');
assert.ok(appJs.includes('FOLLOW_SYSTEM_MODEL'), 'app.js must have follow-system sentinel');
assert.ok(appJs.includes('extractDrawingJavascript'), 'app.js must extract JS from AI responses flexibly');
assert.ok(appJs.includes('<javascript>([\\s\\S]*?)<\\/javascript>'), 'app.js must parse <javascript> tags');
assert.ok(appJs.includes('```(?:javascript|js)'), 'app.js must parse markdown javascript fences');
assert.ok(appJs.includes('stripJavascriptFences'), 'app.js must strip nested markdown fences');
assert.ok(appJs.includes('3-5 gạch đầu dòng'), 'system prompt must keep analysis short');
assert.ok(appJs.includes('PHƯƠNG PHÁP TỌA ĐỘ HÓA'), 'system prompt must require coordinate geometry');
assert.ok(appJs.includes('NGHIÊM CẤM markdown backtick'), 'system prompt must forbid markdown fences in javascript tag');
assert.ok(appJs.includes('<geogebra>'), 'system prompt must request GeoGebra block');
assert.ok(appJs.includes('fallback_model: selectedFallbackModel'), 'generate request must send fallback_model');
assert.ok(appJs.includes('resolveDrawingRequestModel'), 'generate request must resolve __system__ to a real model');
assert.match(extractNamed(appJs, 'resolveDrawingRequestModel'), /if \(raw && raw !== FOLLOW_SYSTEM_MODEL\) return raw;/, 'explicit dropdown selection must win');
assert.match(extractNamed(appJs, 'waitForAiThrottle'), /minMs = 1000/, 'throttle must wait at most the remaining 1s gap');
assert.match(appJs, /AI đang phân tích bằng Gemini · \$\{selectedModel\}/, 'status must show the selected model');
assert.match(appJs, /isCustomSelection \? ''/, 'custom model status must omit fallback DP line');
assert.ok(appJs.includes('global_gemini_keys'), 'drawing request must send global_gemini_keys');
assert.ok(appJs.includes('autoCenterAndFitDrawing'), 'app.js must auto-center AI drawings');
assert.ok(appJs.includes("'addPoint', 'addText', 'drawLine'"), 'executeAiCode must inject addPoint/addText/drawLine');

function extractNamed(source, name) {
    const needles = [`async function ${name}(`, `function ${name}(`];
    let start = -1;
    for (const needle of needles) {
        start = source.indexOf(needle);
        if (start >= 0) break;
    }
    assert(start >= 0, `missing function ${name}`);
    const paren = source.indexOf('(', start);
    let parenDepth = 0, afterParams = -1;
    for (let i = paren; i < source.length; i++) {
        if (source[i] === '(') parenDepth += 1;
        else if (source[i] === ')') {
            parenDepth -= 1;
            if (parenDepth === 0) { afterParams = i; break; }
        }
    }
    const brace = source.indexOf('{', afterParams);
    let depth = 0;
    for (let i = brace; i < source.length; i++) {
        if (source[i] === '{') depth += 1;
        else if (source[i] === '}') {
            depth -= 1;
            if (depth === 0) return source.slice(start, i + 1);
        }
    }
    throw new Error(`unterminated function ${name}`);
}

const vm = require('vm');
assert.ok(appJs.includes('sanitizeAiDrawingCode'), 'app.js must sanitize AI drawing code');
assert.ok(appJs.includes('startProgressIndicator'), 'app.js must start live progress');
assert.ok(appJs.includes('animateDrawingSteps'), 'app.js must animate construction steps');
assert.ok(appJs.includes("TUYỆT ĐỐI KHÔNG viết const canvas"), 'system prompt must forbid redeclaring canvas');

const extractSrc = [
    extractNamed(appJs, 'stripJavascriptFences'),
    extractNamed(appJs, 'extractDrawingJavascript'),
    extractNamed(appJs, 'extractGeoGebraContent'),
    extractNamed(appJs, 'splitGeoGebraBlocks'),
    extractNamed(appJs, 'getSystemDrawingModel'),
    extractNamed(appJs, 'getSystemDrawingFallbackModel'),
    extractNamed(appJs, 'sanitizeAiDrawingCode'),
    extractNamed(appJs, 'formatGeoGebraExecuteCommand'),
].join('\n');
const store = {};
const sandbox = {
    localStorage: {
        getItem(key) { return Object.prototype.hasOwnProperty.call(store, key) ? store[key] : null; },
        setItem(key, value) { store[key] = String(value); }
    }
};
vm.createContext(sandbox);
vm.runInContext(extractSrc, sandbox);

assert.strictEqual(sandbox.extractDrawingJavascript('<javascript>canvas.renderAll();</javascript>'), 'canvas.renderAll();');
assert.strictEqual(sandbox.extractDrawingJavascript('```javascript\nconst a = 1;\n```'), 'const a = 1;');
assert.strictEqual(sandbox.extractDrawingJavascript('```js\nconst b = 2;\n```'), 'const b = 2;');
assert.strictEqual(sandbox.extractDrawingJavascript('<javascript>```javascript\ncanvas.renderAll();\n```</javascript>'), 'canvas.renderAll();');
assert.strictEqual(sandbox.extractDrawingJavascript('no code here'), null);
assert.ok(!sandbox.extractDrawingJavascript('<javascript>```javascript foo() ```</javascript>').includes('```'), 'nested fences must be stripped');

const ggb = sandbox.extractGeoGebraContent('<geogebra>\nBước 1: Đặt A.\nA=(0,0)\nB=(6,0)\nPolygon(A,B,C)\n</geogebra>');
assert.ok(ggb.includes('A=(0,0)'), 'extractGeoGebraContent must keep commands');
const parts = sandbox.splitGeoGebraBlocks(ggb);
assert.ok(parts.commands.includes('Polygon(A,B,C)'), 'GeoGebra commands must be split out');
assert.ok(parts.steps.includes('Bước 1'), 'GeoGebra steps must be split out');

const commentedGgb = sandbox.splitGeoGebraBlocks([
    'O=(0,0)',
    'R=3 // radius',
    'Tangent(M, Circle(O, R)) // This will create two tangents',
    '# ignore this line',
    'Segment(A, B)',
].join('\n'));
assert.ok(!commentedGgb.commands.includes('//'), 'GeoGebra commands must strip // comments');
assert.ok(!commentedGgb.commands.includes('#'), 'GeoGebra commands must strip # comments');
assert.ok(commentedGgb.commandsArray.includes('R=3'), 'assignment after comment strip must remain');
assert.ok(commentedGgb.commandsArray.some((cmd) => cmd.startsWith('Tangent(')), 'command after trailing comment must remain');
const executeLine = sandbox.formatGeoGebraExecuteCommand(['O=(0,0)', 'R=3', 'Segment(A, B)']);
assert.strictEqual(executeLine, 'Execute({"O=(0,0)", "R=3", "Segment(A, B)"})', 'must wrap commands as one-line Execute({...})');
assert.ok(!executeLine.includes('\n'), 'Execute payload must be a single line');

store.khbd_gemini_model = 'gemini-3.7-flash';
store.default_gemini_module = 'gemini-3.6-flash';
assert.strictEqual(sandbox.getSystemDrawingModel(), 'gemini-3.7-flash', 'primary must prefer khbd_gemini_model');
store.khbd_gemini_fallback_model = 'gemini-2.5-flash';
assert.strictEqual(sandbox.getSystemDrawingFallbackModel(), 'gemini-2.5-flash', 'fallback must prefer khbd_gemini_fallback_model');

const dirtySamples = [
    'const canvas = new fabric.Canvas("geometry-canvas");\ncanvas.add(item);',
    'let canvas = document.getElementById("geometry-canvas");\ncanvas.add(item);',
    'var canvas = window.canvas || canvas;\ncanvas.add(item);',
    'const fabric = window.fabric;\ncanvas.add(item);',
];
for (const dirty of dirtySamples) {
    const clean = sandbox.sanitizeAiDrawingCode(dirty);
    assert.doesNotMatch(clean, /(?:const|let|var)\s+canvas\b/, 'must strip canvas redeclare: ' + dirty.split('\n')[0]);
    assert.doesNotMatch(clean, /(?:const|let|var)\s+fabric\b/, 'must strip fabric redeclare');
    assert.doesNotThrow(() => new Function('canvas', 'fabric', clean), 'sanitized code must compile: ' + dirty.split('\n')[0]);
}
const keepWidth = sandbox.sanitizeAiDrawingCode('const canvasWidth = 400;\ncanvas.add(item);');
assert.match(keepWidth, /const canvasWidth = 400/, 'must not rewrite canvasWidth');
assert.doesNotThrow(() => new Function('canvas', 'fabric', keepWidth));

const resolveSandbox = {
    FOLLOW_SYSTEM_MODEL: '__system__',
    allDOMElements: { aiModelSelect: { value: 'gemini-2.5-flash' } },
    getCurrentDrawingModel() { return 'gemini-3.7-flash'; }
};
vm.createContext(resolveSandbox);
vm.runInContext(extractNamed(appJs, 'resolveDrawingRequestModel'), resolveSandbox);
assert.strictEqual(resolveSandbox.resolveDrawingRequestModel('gemini'), 'gemini-2.5-flash', 'direct 2.5-flash selection must not be overwritten');
resolveSandbox.allDOMElements.aiModelSelect.value = '__system__';
assert.strictEqual(resolveSandbox.resolveDrawingRequestModel('gemini'), 'gemini-3.7-flash', 'follow-system sentinel still uses current model');

const vehinhHtml = fs.readFileSync(path.join(__dirname, '..', 'vehinh.html'), 'utf8');
const promptIdx = vehinhHtml.indexOf('id="prompt-input"');
const uploadIdx = vehinhHtml.indexOf('id="image-upload"');
const drawIdx = vehinhHtml.indexOf('id="draw-action-buttons"');
const generateIdx = vehinhHtml.indexOf('id="generate-btn"');
const analysisIdx = vehinhHtml.indexOf('id="analysis-output"');
assert.ok(promptIdx > 0 && uploadIdx > promptIdx, 'image upload follows prompt');
assert.ok(drawIdx > uploadIdx, 'draw buttons must follow question/image inputs');
assert.ok(generateIdx > drawIdx, 'generate button lives in relocated action cluster');
assert.ok(analysisIdx > generateIdx, 'analysis panel stays below draw buttons');
assert.ok(vehinhHtml.includes('id="geogebra-construction-panel"'), 'GeoGebra construction panel');
assert.ok(vehinhHtml.includes('📋 Sao chép lệnh (Dán 1 lần vào GeoGebra)'), 'copy GeoGebra as one-line Execute');
assert.ok(vehinhHtml.includes('id="inject-geogebra-btn"'), 'inject GeoGebra button');
assert.ok(vehinhHtml.includes('⚡ Nạp trực tiếp vào GeoGebra'), 'inject GeoGebra label');
assert.ok(vehinhHtml.includes('🚀 Mở khung GeoGebra'), 'open GeoGebra button');
assert.ok(appJs.includes('formatGeoGebraExecuteCommand'), 'app.js must format Execute({...})');
assert.ok(appJs.includes('injectCommandsToGeoGebra'), 'app.js must inject commands into GeoGebra');
assert.ok(appJs.includes('TUYỆT ĐỐI KHÔNG viết chú thích // hoặc #'), 'prompt must forbid GeoGebra comments');
assert.ok(vehinhHtml.includes('id="ai-progress-widget"'), 'live progress widget');
assert.ok(vehinhHtml.includes('id="ai-progress-timer"'), 'live timer');
assert.ok(vehinhHtml.includes('id="ai-progress-bar"'), 'progress bar');
assert.ok(vehinhHtml.includes('id="ai-progress-status"'), 'multi-stage status');
assert.ok(vehinhHtml.includes('id="replay-construction-btn"'), 'replay construction button');
assert.ok(vehinhHtml.includes('Tái hiện từng bước vẽ'), 'replay button label');
assert.ok(vehinhHtml.includes('https://www.geogebra.org/apps/deployggb.js'), 'vehinh.html must embed deployggb.js');
assert.ok(!vehinhHtml.includes('src="https://www.geogebra.org/classic"'), 'vehinh.html must not use a cross-origin GeoGebra iframe');
assert.ok(appJs.includes('runCommandsOnGeoGebra'), 'app.js must run GeoGebra commands via evalCommand');
assert.ok(appJs.includes('evalCommand'), 'app.js must call ggbApplet.evalCommand');
assert.ok(appJs.includes('ensureGeoGebraAppletLoaded'), 'app.js must lazy-load the GeoGebra applet');
assert.ok(appJs.includes('QUY TẮC BẮT BUỘC: ĐẶT TÊN VÀ CHẤM ĐIỂM'), 'system prompt must require point labels');
assert.ok(appJs.includes("addPoint(O, 'O')"), 'system prompt must show addPoint(pt, name) samples');
assert.ok(appJs.includes('recoverMissingAiPointLabels'), 'executeAiCode must auto-recover missing point labels');
assert.match(extractNamed(appJs, 'wrapAddPoint'), /smartAddPoint\(canvas/, 'wrapAddPoint must delegate to smartAddPoint');
assert.match(extractNamed(appJs, 'wrapAddText'), /smartAddText\(canvas/, 'wrapAddText must delegate to smartAddText');

const pointSrc = [
    extractNamed(appJs, 'looksLikeCanvas'),
    extractNamed(appJs, 'isPointLike'),
    extractNamed(appJs, 'isColorToken'),
    extractNamed(appJs, 'isLabelToken'),
    extractNamed(appJs, 'parseSmartPointArgs'),
    extractNamed(appJs, 'parseSmartTextArgs'),
    extractNamed(appJs, 'smartAddPoint'),
    extractNamed(appJs, 'smartAddText'),
    extractNamed(appJs, 'extractUppercasePointNames'),
    extractNamed(appJs, 'buildAiPointDumpTail'),
    extractNamed(appJs, 'isGeometryPointLabel'),
    extractNamed(appJs, 'recoverMissingAiPointLabels'),
].join('\n');
const addedPointObjs = [];
const mockDrawCanvas = {
    add(obj) { addedPointObjs.push(obj); },
    getObjects() { return addedPointObjs.slice(); },
    renderAll() {}
};
const pointSandbox = {
    pointLabelCounter: 0,
    defaultProps: { originX: 'center', originY: 'center' },
    fabric: {
        Circle: function (opts) {
            Object.assign(this, opts);
            this.type = 'circle';
        },
        IText: function (text, opts) {
            Object.assign(this, opts || {});
            this.text = text;
            if (!this.type) this.type = 'i-text';
        }
    }
};
vm.createContext(pointSandbox);
vm.runInContext(pointSrc, pointSandbox);

const parsedPt = pointSandbox.parseSmartPointArgs([{ x: 100, y: 200 }, 'O']);
assert.strictEqual(parsedPt.x, 100, 'parseSmartPointArgs(pt, name) must read pt.x');
assert.strictEqual(parsedPt.y, 200, 'parseSmartPointArgs(pt, name) must read pt.y');
assert.strictEqual(parsedPt.label, 'O', 'parseSmartPointArgs(pt, name) must keep label O');
assert.ok(Number.isFinite(parsedPt.x) && Number.isFinite(parsedPt.y), 'object point must not become NaN');

const parsedXY = pointSandbox.parseSmartPointArgs([50, 60, 'A']);
assert.strictEqual(parsedXY.x, 50);
assert.strictEqual(parsedXY.y, 60);
assert.strictEqual(parsedXY.label, 'A');

const parsedNamePt = pointSandbox.parseSmartPointArgs(['B', { x: 1, y: 2 }]);
assert.strictEqual(parsedNamePt.label, 'B');
assert.strictEqual(parsedNamePt.x, 1);

const parsedNameXY = pointSandbox.parseSmartPointArgs(['C', 3, 4, '#ff0000']);
assert.strictEqual(parsedNameXY.label, 'C');
assert.strictEqual(parsedNameXY.x, 3);
assert.strictEqual(parsedNameXY.color, '#ff0000');

const parsedCanvasFirst = pointSandbox.parseSmartPointArgs([mockDrawCanvas, { x: 8, y: 9 }, 'M']);
assert.strictEqual(parsedCanvasFirst.label, 'M');
assert.strictEqual(parsedCanvasFirst.x, 8);

const parsedTextXY = pointSandbox.parseSmartTextArgs([10, 20, 'O']);
assert.strictEqual(parsedTextXY.text, 'O');
assert.strictEqual(parsedTextXY.x, 10);
const parsedTextNameFirst = pointSandbox.parseSmartTextArgs(['H', 11, 22]);
assert.strictEqual(parsedTextNameFirst.text, 'H');
assert.strictEqual(parsedTextNameFirst.y, 22);
const parsedTextPt = pointSandbox.parseSmartTextArgs([{ x: 5, y: 6 }, 'F']);
assert.strictEqual(parsedTextPt.text, 'F');
assert.ok(Number.isFinite(parsedTextPt.x), 'addText(pt, text) must not yield NaN');

addedPointObjs.length = 0;
const skippedNaN = pointSandbox.smartAddPoint(mockDrawCanvas, { not: 'a point' }, 'O');
assert.ok(Array.isArray(skippedNaN) && skippedNaN.length === 0, 'invalid point object must not be drawn');
assert.strictEqual(addedPointObjs.length, 0);

const drawn = pointSandbox.smartAddPoint(mockDrawCanvas, { x: 100, y: 200 }, 'O');
assert.strictEqual(drawn.length, 2, 'smartAddPoint must add a dot and a label');
assert.strictEqual(addedPointObjs.length, 2);
assert.strictEqual(addedPointObjs[0].left, 100);
assert.strictEqual(addedPointObjs[0].top, 200);
assert.strictEqual(addedPointObjs[0].radius, 3.5);
assert.ok(!Number.isNaN(addedPointObjs[0].left) && !Number.isNaN(addedPointObjs[0].top), 'circle coords must not be NaN');
assert.strictEqual(addedPointObjs[0].source, 'ai_primitive');
assert.strictEqual(addedPointObjs[1].text, 'O');
assert.strictEqual(addedPointObjs[1].left, 108);
assert.strictEqual(addedPointObjs[1].top, 182);
assert.strictEqual(addedPointObjs[1].fontWeight, 'bold');
assert.strictEqual(addedPointObjs[1].fontSize, 16);
assert.strictEqual(addedPointObjs[1].source, 'ai_primitive');
assert.ok(!Number.isNaN(addedPointObjs[1].left) && !Number.isNaN(addedPointObjs[1].top), 'label coords must not be NaN');

addedPointObjs.length = 0;
pointSandbox.smartAddPoint(mockDrawCanvas, 15, 25, 'A');
assert.strictEqual(addedPointObjs[0].left, 15);
assert.strictEqual(addedPointObjs[1].text, 'A');

addedPointObjs.length = 0;
const textObj = pointSandbox.smartAddText(mockDrawCanvas, { x: 7, y: 9 }, 'H');
assert.ok(textObj);
assert.strictEqual(textObj.text, 'H');
assert.strictEqual(textObj.left, 7);
assert.ok(!Number.isNaN(textObj.left));

const extractedNames = pointSandbox.extractUppercasePointNames('const O = toScreen(0,0);\nconst A = {x:1,y:2};\nconst scale = 10;\nconst toScreen = () => {};');
assert.strictEqual(extractedNames.join(','), 'O,A', 'extractUppercasePointNames must keep O and A only');
assert.match(pointSandbox.buildAiPointDumpTail('const O = toScreen(0,0);'), /__aiPointDump/);

addedPointObjs.length = 0;
addedPointObjs.push({ type: 'line' });
const recovered = pointSandbox.recoverMissingAiPointLabels(mockDrawCanvas, { O: { x: 10, y: 20 }, A: { x: 30, y: 40 } });
assert.ok(recovered.length >= 4, 'auto-recovery must add dots and labels for dumped points');
assert.ok(addedPointObjs.some((o) => o.text === 'O'));
assert.ok(addedPointObjs.some((o) => o.text === 'A'));

const alreadyLabeled = pointSandbox.recoverMissingAiPointLabels(mockDrawCanvas, { B: { x: 1, y: 2 } });
assert.strictEqual(alreadyLabeled.length, 0, 'auto-recovery must not duplicate when labels already exist');

const aiDesignConfigJs = fs.readFileSync(path.join(__dirname, '..', 'ai-design-config.js'), 'utf8');
assert.ok(aiDesignConfigJs.includes('gemini-3.6-flash'), 'ai-design-config.js must support gemini-3.6-flash');

console.log('-> 5. AI Drawing modern model catalog and fallback: PASS');

// 7. Test Educational Games hook presence
const trochoiCompiledJs = fs.readFileSync(path.join(__dirname, '..', 'trochoi.compiled.js'), 'utf8');
assert.ok(trochoiCompiledJs.includes('inputMethod'), 'trochoi.compiled.js must support inputMethod state');
assert.ok(trochoiCompiledJs.includes('word_latex'), 'trochoi.compiled.js must support word_latex tab');
assert.ok(trochoiCompiledJs.includes('gemini-3.6-flash'), 'trochoi.compiled.js must default to gemini-3.6-flash');

const eliminationHtml = fs.readFileSync(path.join(__dirname, '..', 'game-elimination.html'), 'utf8');
assert.ok(eliminationHtml.includes('gameData'), 'game-elimination.html must check gameData');
assert.ok(eliminationHtml.includes('game-quiz-importer.js'), 'game-elimination.html must include game-quiz-importer.js');
assert.ok(eliminationHtml.includes('gemini-3.6-flash'), 'game-elimination.html must default to gemini-3.6-flash');

const speedscoreHtml = fs.readFileSync(path.join(__dirname, '..', 'game-speedscore.html'), 'utf8');
assert.ok(speedscoreHtml.includes('gameData'), 'game-speedscore.html must check gameData');
assert.ok(speedscoreHtml.includes('game-quiz-importer.js'), 'game-speedscore.html must include game-quiz-importer.js');
assert.ok(speedscoreHtml.includes('gemini-3.6-flash'), 'game-speedscore.html must default to gemini-3.6-flash');

const towerHtml = fs.readFileSync(path.join(__dirname, '..', 'game-tower.html'), 'utf8');
assert.ok(towerHtml.includes('gameData'), 'game-tower.html must check gameData');
assert.ok(towerHtml.includes('game-quiz-importer.js'), 'game-tower.html must include game-quiz-importer.js');
assert.ok(towerHtml.includes('gemini-3.6-flash'), 'game-tower.html must default to gemini-3.6-flash');

const unlockHtml = fs.readFileSync(path.join(__dirname, '..', 'game-unlock.html'), 'utf8');
assert.ok(unlockHtml.includes('gameData'), 'game-unlock.html must check gameData');
assert.ok(unlockHtml.includes('game-quiz-importer.js'), 'game-unlock.html must include game-quiz-importer.js');
assert.ok(unlockHtml.includes('gemini-3.6-flash'), 'game-unlock.html must default to gemini-3.6-flash');

const teambattleHtml = fs.readFileSync(path.join(__dirname, '..', 'game-teambattle.html'), 'utf8');
assert.ok(teambattleHtml.includes('gameData'), 'game-teambattle.html must check gameData');
assert.ok(teambattleHtml.includes('game-quiz-importer.js'), 'game-teambattle.html must include game-quiz-importer.js');
assert.ok(teambattleHtml.includes('gemini-3.6-flash'), 'game-teambattle.html must default to gemini-3.6-flash');

console.log('-> 6. Educational game files integration and hooks: PASS');
console.log('==================================================');
console.log('ALL GAME QUIZ IMPORTER AND AI DRAWING TESTS PASSED!');
console.log('==================================================');
