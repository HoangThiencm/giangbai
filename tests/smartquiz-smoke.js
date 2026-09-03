'use strict';

const fs = require('fs');
const path = require('path');
const assert = require('assert');

const root = path.join(__dirname, '..');

function load(name) {
    return fs.readFileSync(path.join(root, name), 'utf8').replace(/\r\n/g, '\n');
}

function scriptBodies(html) {
    const bodies = [];
    const openRe = /<script\b[^>]*>/gi;
    let match;
    while ((match = openRe.exec(html))) {
        const start = match.index + match[0].length;
        const close = html.toLowerCase().indexOf('</script>', start);
        assert(close >= 0, 'mỗi thẻ <script> phải có </script> đóng');
        bodies.push(html.slice(start, close));
        openRe.lastIndex = close + 9;
    }
    return bodies;
}

function assertNoNestedScript(html, fileName) {
    const bodies = scriptBodies(html);
    bodies.forEach((body, index) => {
        assert(
            !/<script\b/i.test(body),
            `${fileName}: khối script #${index + 1} không được chứa thẻ <script> lồng`
        );
        assert(
            !/<\/script/i.test(body),
            `${fileName}: khối script #${index + 1} không được chứa chuỗi </script lồng`
        );
    });
}

function assertSingleHeadGuard(html, fileName) {
    const hits = html.match(/js\/security-guard\.js/g) || [];
    assert.strictEqual(hits.length, 1, `${fileName}: security-guard.js chỉ được nằm ở <head> thật, không trong template export`);
    assert.match(
        html.slice(0, 800),
        /<script src="js\/security-guard\.js"><\/script>/,
        `${fileName}: giữ nguyên security-guard.js hợp lệ trên đầu trang`
    );
}

const smartquiz = load('smartquiz.html');
const taobaitap = load('taobaitap.html');
const phancong = load('phancongtochuyenmon.html');

assertSingleHeadGuard(smartquiz, 'smartquiz.html');
assertSingleHeadGuard(taobaitap, 'taobaitap.html');
assertSingleHeadGuard(phancong, 'phancongtochuyenmon.html');

assertNoNestedScript(smartquiz, 'smartquiz.html');
assertNoNestedScript(taobaitap, 'taobaitap.html');
assertNoNestedScript(phancong, 'phancongtochuyenmon.html');

const quizBabelStart = smartquiz.indexOf('<script type="text/babel"');
const quizBabelEnd = smartquiz.indexOf('</script>', quizBabelStart);
assert(quizBabelStart >= 0 && quizBabelEnd > quizBabelStart, 'smartquiz phải có đúng một khối Babel mở-đóng khớp');
const quizBabel = smartquiz.slice(quizBabelStart, quizBabelEnd);
const quizBody = smartquiz.slice(smartquiz.indexOf('>', quizBabelStart) + 1, quizBabelEnd);
assert(quizBabel.includes('const exportWord'), 'smartquiz Babel phải còn hàm exportWord');
assert(quizBabel.includes('root.render(<App />)'), 'smartquiz Babel phải còn root.render — không bị cắt giữa chừng');
assert(quizBody.includes("<meta charset='utf-8'><title>Export</title>"), 'template Word smartquiz giữ meta charset');
assert(!quizBody.includes('security-guard.js'), 'template Word smartquiz không còn security-guard.js');

const taoBabelStart = taobaitap.indexOf('<script type="text/babel"');
const taoBabelEnd = taobaitap.indexOf('</script>', taoBabelStart);
assert(taoBabelStart >= 0 && taoBabelEnd > taoBabelStart, 'taobaitap phải có đúng một khối Babel mở-đóng khớp');
const taoBabel = taobaitap.slice(taoBabelStart, taoBabelEnd);
assert(taoBabel.includes('const exportWord'), 'taobaitap Babel phải còn exportWord');
assert(taoBabel.includes('const exportWordLatex'), 'taobaitap Babel phải còn exportWordLatex');
assert(taoBabel.includes('root.render(<App />)'), 'taobaitap Babel phải còn root.render — không bị cắt giữa chừng');
assert(taoBabel.includes("<meta charset='utf-8'><title>Export</title>"), 'template Word taobaitap giữ meta charset');
assert(taoBabel.includes("<meta charset='utf-8'><title>Export LaTeX</title>"), 'template Word LaTeX taobaitap giữ meta charset');
assert(!taoBabel.includes('security-guard.js'), 'template Word taobaitap không còn security-guard.js');

assert.match(phancong, /function downloadExcelFile/, 'phancongtochuyenmon còn downloadExcelFile');
assert.match(
    phancong,
    /const template = '<html xmlns:o="urn:schemas-microsoft-com:office:office"[^']*<head><meta charset="UTF-8">/,
    'chuỗi template Excel phải nằm trên một dòng, không bị ngắt bởi thẻ script'
);
assert.doesNotMatch(
    phancong.slice(phancong.indexOf('const template')),
    /const template = '[^']*\n/,
    'template Excel không được ngắt dòng trong chuỗi nháy đơn'
);

console.log('smartquiz smoke: nested </script> export templates cleaned; babel scripts stay intact');
