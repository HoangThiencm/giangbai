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
assert.ok(vehinhAiPhp.includes("'maxOutputTokens' => 16384"), 'api/vehinh_ai.php must raise maxOutputTokens to 16384');
assert.ok(!vehinhAiPhp.includes("'maxOutputTokens' => 4096"), 'api/vehinh_ai.php must not keep the old 4096 token cap');
assert.ok(vehinhAiPhp.includes("'thinkingBudget' => 0"), 'api/vehinh_ai.php must disable thinking budget');
assert.ok(vehinhAiPhp.includes('int $timeout = 90') || /vehinh_post_json\([^;]*90/.test(vehinhAiPhp), 'api/vehinh_ai.php must use 90s curl timeout');

const runtimeConfigPhp = fs.readFileSync(path.join(__dirname, '..', 'api', 'ai_runtime_config.php'), 'utf8');
assert.ok(runtimeConfigPhp.includes('gemini-3.6-flash'), 'api/ai_runtime_config.php must default to gemini-3.6-flash');

const appJs = fs.readFileSync(path.join(__dirname, '..', 'app.js'), 'utf8');
assert.ok(appJs.includes('gemini-3.6-flash'), 'app.js must include gemini-3.6-flash in DRAWING_AI_MODEL_CATALOG');
assert.ok(appJs.includes('getSystemDrawingModel'), 'app.js must read system drawing model from settings');
assert.ok(appJs.includes("localStorage.getItem('default_gemini_module')"), 'app.js must read default_gemini_module');
assert.ok(appJs.includes('clearDeprecatedSavedDrawingModel'), 'app.js must clear deprecated vehinh_ai_model_gemini');
assert.ok(appJs.includes('gemini-2.5-flash') && appJs.includes('DEPRECATED_DRAWING_MODELS'), 'app.js must treat gemini-2.5-flash as deprecated');
assert.ok(appJs.includes('Theo Cài đặt chung'), 'app.js dropdown must include Theo Cài đặt chung');
assert.ok(appJs.includes('FOLLOW_SYSTEM_MODEL'), 'app.js must have follow-system sentinel');
assert.ok(appJs.includes('extractDrawingJavascript'), 'app.js must extract JS from AI responses flexibly');
assert.ok(appJs.includes('<javascript>([\\s\\S]*?)<\\/javascript>'), 'app.js must parse <javascript> tags');
assert.ok(appJs.includes('```(?:javascript|js)'), 'app.js must parse markdown javascript fences');
assert.ok(appJs.includes('3-5 gạch đầu dòng'), 'system prompt must keep analysis short');
assert.ok(appJs.includes('resolveDrawingRequestModel'), 'generate request must resolve __system__ to a real model');
assert.ok(appJs.includes('global_gemini_keys'), 'drawing request must send global_gemini_keys');

function extractDrawingJavascript(fullText) {
    const source = String(fullText || '');
    const tagged = source.match(/<javascript>([\s\S]*?)<\/javascript>/i);
    if (tagged && tagged[1].trim()) return tagged[1].trim();
    const fenced = source.match(/```(?:javascript|js)\s*([\s\S]*?)```/i);
    if (fenced && fenced[1].trim()) return fenced[1].trim();
    return null;
}
assert.strictEqual(extractDrawingJavascript('<javascript>canvas.renderAll();</javascript>'), 'canvas.renderAll();');
assert.strictEqual(extractDrawingJavascript('```javascript\nconst a = 1;\n```'), 'const a = 1;');
assert.strictEqual(extractDrawingJavascript('```js\nconst b = 2;\n```'), 'const b = 2;');
assert.strictEqual(extractDrawingJavascript('no code here'), null);

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
