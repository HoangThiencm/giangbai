const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(require('node:path').join(__dirname, '../phancongtochuyenmon.html'), 'utf8');
const scripts = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map(match => match[1]);
scripts.forEach(source => new vm.Script(source));
function declaration(name) {
    const start = html.lastIndexOf(`function ${name}(`);
    assert(start >= 0, name);
    const prefix = html.slice(start - 6, start) === 'async ' ? start - 6 : start;
    const end = html.indexOf('\n        }', start) + '\n        }'.length;
    return html.slice(prefix, end);
}
const names = ['baoGiangPdfPageText', 'requestBaoGiangRecognition', 'baoGiangRecognizedLines', 'scanBaoGiangPpct', 'parseBaoGiangPpctAiJson'];
const source = names.map(declaration).join('\n');
const lesson = 'Luyện tập “chung” }, { nguyên văn';
const valid = JSON.stringify({ curriculum: [{week: 1, period_no: '3', strand: 'Đại số', lesson, periods: 1}, {week: 2, period_no: '4-5', strand: 'Đại số', lesson, periods: 2}] });
const gemini = (text, finishReason = 'STOP') => ({ok: true, body: { candidates: [{finishReason, content: {parts: [{text}]}}] }});
async function run(responses, expectedCalls, success = false, input = 'PPCT') {
    let calls = 0, saved = 0;
    const elements = {
        'bg-ppct-file': { files: [{}] }, 'bg-scan-ppct': {}, 'bg-ppct-status': {},
        'bg-ppct-grade': {value: '9'}, 'bg-ppct-subject': {value: 'Toán'}, 'bg-curriculum': {value: 'existing'}
    };
    const context = vm.createContext({
        AbortController, setTimeout, clearTimeout,
        document: {getElementById: id => elements[id]}, state: {bao_giang: {curriculum_text: 'existing'}},
        extractBaoGiangPpctText: async () => input, mergeBaoGiangCurriculumLines: lines => 'existing-other\n' + lines.join('\n'),
        saveToLocal: () => saved++, renderBaoGiangView() {}, showToast() {}, setBaoGiangPpctNotice() {},
        fetch: async () => {
            const data = responses[calls++];
            if (data === 'abort') { const error = new Error(); error.name = 'AbortError'; throw error; }
            return {ok: !data.http, status: data.http || 200, text: async () => data.raw ?? JSON.stringify(data)};
        }
    });
    vm.runInContext(source, context);
    await vm.runInContext('scanBaoGiangPpct()', context);
    assert.equal(calls, expectedCalls);
    assert.equal(elements['bg-scan-ppct'].disabled, false);
    assert.equal(saved, success ? 1 : 0);
    if (!success) {
        assert.equal(context.state.bao_giang.curriculum_text, 'existing');
        assert.equal(elements['bg-curriculum'].value, 'existing');
        assert(elements['bg-ppct-status'].textContent.length > 0);
    } else {
        assert(context.state.bao_giang.curriculum_text.includes(lesson));
        assert(context.state.bao_giang.curriculum_text.includes('9 | Toán | 2 | 4-5'));
    }
    return context;
}
(async () => {
    const context = await run([gemini(valid)], 1, true);
    await run([gemini('{broken'), gemini(valid)], 2, true);
    await run([gemini('{broken'), gemini('{broken')], 2);
    await run([gemini(valid, 'MAX_TOKENS')], 1);
    await run([{ok: true, body: {promptFeedback: {blockReason: 'SAFETY'}}}], 1);
    await run([{http: 401, raw: '<html>login</html>'}], 1);
    await run([{http: 502, raw: '<html>gateway timeout</html>'}], 1);
    await run(['abort'], 1);
    await run([gemini('{"curriculum":[{"week":1,"lesson":"bad"}]}')], 1);
    await run([], 0, false, 'x'.repeat(70001));
    const page = vm.runInContext('baoGiangPdfPageText([{str:"Bài 2",transform:[1,0,0,1,0,50],width:30},{str:"3",transform:[1,0,0,1,100,50],width:5,hasEOL:true},{str:"Tuần 2",transform:[1,0,0,1,0,30],width:30}])', context);
    assert.equal(page, 'Bài 2\t3\nTuần 2');
    const legacy = vm.runInContext('baoGiangRecognizedLines({curriculum:[{week:null,lesson:"Bài cũ",periods:2}]},"6","Tin")', context);
    assert.equal(legacy[0], '6 | Tin | Bài cũ | 2');
    assert.match(html, /function baoGiangWeekdayLabel\(/);
    assert.match(html, /<b>\$\{escapeHtml\(baoGiangWeekdayLabel\(row\.date\)\)\}<\/b><br><small style="color:#64748b;">\$\{escapeHtml\(formatVnDate\(row\.date\)\)\}<\/small>/);
    assert.match(html, /\$\{escapeHtml\(baoGiangWeekdayLabel\(date\)\)\}, ngày \$\{escapeHtml\(formatVnDate\(date\)\)\}/);
    function nextDeclaration(name) {
        const start = html.lastIndexOf(`function ${name}(`);
        assert(start >= 0, name);
        const next = html.indexOf('\n        function ', start + 1);
        return html.slice(start, next < 0 ? html.length : next);
    }
    const parseSource = ['baoGiangDate', 'baoGiangWeekdayLabel', 'baoGiangSubjectKey', 'baoGiangKey', 'parseBaoGiangCurriculumEntries', 'baoGiangExpandPeriodNumbers', 'parseBaoGiangCurriculum', 'normalizeBaoGiangLessonTitle'].map(nextDeclaration).join('\n');
    const parseContext = vm.createContext({
        Map, Date, String, Number, Array,
        foldText: value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toUpperCase().replace(/\s+/g, ' ').trim()
    });
    vm.runInContext(parseSource, parseContext);
    const plan = vm.runInContext(`parseBaoGiangCurriculum([
        '9 | Toán | 1 | 1 | Hình học | Bài 11. Tỉ số lượng giác của góc nhọn | 1',
        '9 | Toán | 2 | 2-3 | Hình học | Bài 11. Tỉ số lượng giác của góc nhọn (tiếp theo) | 2'
    ].join('\\n')).get(baoGiangKey('9', 'Toán')).all`, parseContext);
    assert.deepEqual(JSON.parse(JSON.stringify(plan.map(item => [item.ppct, item.segment]))), [['1', '1/3'], ['2', '2/3'], ['3', '3/3']]);
    assert.equal(vm.runInContext("baoGiangWeekdayLabel('2026-09-09')", parseContext), 'Thứ Tư');
    console.log('PASS: scripts compile; PPCT success/retry, transport/blocked/truncation preservation, strict rows, legacy and PDF rows.');
})().catch(error => { console.error(error); process.exitCode = 1; });
