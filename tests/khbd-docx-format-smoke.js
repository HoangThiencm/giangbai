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
global.window = { docx };
const { DocxGenerator } = require('../js/khbd-docx.js');

function runText(run) {
  return run.root.map(item => item.rootKey === 'w:t' ? item.root.filter(text => typeof text === 'string').join('') : '').join('');
}

function hasFormatting(run, tag) {
  return run.root.some(item => item.rootKey === 'w:rPr' && item.root.some(prop => prop.rootKey === tag));
}

const generator = new DocxGenerator();
const runs = generator.parseInlineTextToRuns('_Trạm 1:_ và __Nội dung__; *nghiêng* và **đậm**; $x_1$');

assert.strictEqual(runs.filter(run => run instanceof docx.TextRun).map(runText).join(''), 'Trạm 1: và Nội dung; nghiêng và đậm; ', 'Bóc đúng marker Markdown');
assert.ok(runs.some(run => !(run instanceof docx.TextRun)), 'Giữ công thức LaTeX thành math run riêng');
assert.ok(hasFormatting(runs[0], 'w:i'), '_italic_ phải xuất italic');
assert.ok(hasFormatting(runs[2], 'w:b'), '__bold__ phải xuất bold');
assert.ok(hasFormatting(runs[4], 'w:i'), '*italic* phải xuất italic');
assert.ok(hasFormatting(runs[6], 'w:b'), '**bold** phải xuất bold');

const elementsAfterArtifact = generator.parseMarkdownToDocxElements('|\nNội dung sau artifact');
assert.match(JSON.stringify(elementsAfterArtifact), /Nội dung sau artifact/, 'Không bỏ qua dòng hợp lệ ngay sau pipe rò rỉ');

console.log('khbd-docx format smoke: passed');
