'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

function loadDocx() {
  try { return require('docx'); } catch (projectDependencyError) {
    const runtimeModule = path.join(process.env.USERPROFILE || '', '.cache', 'codex-runtimes', 'codex-primary-runtime', 'dependencies', 'node', 'node_modules', 'docx');
    if (fs.existsSync(runtimeModule)) return require(runtimeModule);
    throw projectDependencyError;
  }
}

const docx = loadDocx();
const TINY_PNG = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';

global.appState = { content: { illustrations: [] } };
global.window = { docx, appState: global.appState };

const { DocxGenerator } = require('../js/khbd-docx.js');

function collectText(node, bag = []) {
  if (!node) return bag;
  if (Array.isArray(node)) {
    node.forEach(item => collectText(item, bag));
    return bag;
  }
  if (typeof node === 'string') {
    bag.push(node);
    return bag;
  }
  if (typeof node === 'object') {
    if (node.root) collectText(node.root, bag);
    Object.keys(node).forEach(key => {
      if (key !== 'root' && node[key] && typeof node[key] === 'object') collectText(node[key], bag);
    });
  }
  return bag;
}

console.log('==================================================');
console.log('BẮT ĐẦU KIỂM THỬ FALLBACK HÌNH VẼ TRONG WORD');
console.log('==================================================');

const generator = new DocxGenerator();
const marker = '![Trục số biểu diễn các số nguyên](khbd-ill:img-3.4)';

console.log('-> 1. Chưa có ảnh: chú thích in nghiêng, không rò khbd-ill...');
global.appState.content.illustrations = [];
const fallbackEls = generator.parseMarkdownToDocxElements(marker);
const fallbackText = collectText(fallbackEls).join(' ');
assert.match(fallbackText, /Hình vẽ minh họa:\s*Trục số biểu diễn các số nguyên/);
assert.doesNotMatch(fallbackText, /khbd-ill/);
assert.doesNotMatch(JSON.stringify(fallbackEls), /khbd-ill:img-3\.4/);
assert.ok(
  JSON.stringify(fallbackEls).includes('"w:i"') || JSON.stringify(fallbackEls).includes('w:i'),
  'Chú thích fallback phải in nghiêng'
);
console.log('  -> Fallback body: PASS');

console.log('-> 2. Marker trong ô bảng cũng fallback...');
const tableMd = `| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| Quan sát trục số | ${marker} |`;
const tableEls = generator.parseMarkdownToDocxElements(tableMd);
const tableJson = JSON.stringify(tableEls);
assert.match(tableJson, /Hình vẽ minh họa/);
assert.doesNotMatch(tableJson, /khbd-ill:img-3\.4/);
console.log('  -> Fallback bảng: PASS');

console.log('-> 3. Đã có ảnh: nhúng ImageRun...');
global.appState.content.illustrations = [{
  id: 'img-3.4',
  dataUrl: TINY_PNG,
  caption: 'Trục số biểu diễn các số nguyên'
}];
const embedded = generator.parseMarkdownToDocxElements(marker);
const embeddedJson = JSON.stringify(embedded);
assert.match(embeddedJson, /w:drawing|a:blip|ImageRun|wp:inline/i);
assert.doesNotMatch(embeddedJson, /khbd-ill:img-3\.4/);
assert.ok(embedded.some(el => el instanceof docx.Paragraph));
console.log('  -> Nhúng ảnh: PASS');

console.log('==================================================');
console.log('TẤT CẢ TEST FALLBACK HÌNH VẼ WORD ĐỀU ĐẠT (PASS)!');
console.log('==================================================');
