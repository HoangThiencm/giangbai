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
const { getPromptTemplate } = require('../js/khbd-prompts.js');

function runText(run) {
  return run.root.map(item => item.rootKey === 'w:t' ? item.root.filter(text => typeof text === 'string').join('') : '').join('');
}

function hasFormatting(run, tag) {
  return run.root.some(item => item.rootKey === 'w:rPr' && item.root.some(prop => prop.rootKey === tag));
}

const generator = new DocxGenerator();

assert.deepStrictEqual(
  generator.markerRunColor('[NLS: 1.1.TC1a - GeoGebra]'),
  { color: '0369A1', shading: 'E0F2FE', bold: true, italics: true },
  'markerRunColor NLS phải bold + italics'
);
assert.deepStrictEqual(
  generator.markerRunColor('[AI: 8.A1.1 - Kiểm chứng phản hồi AI]'),
  { color: '6D28D9', shading: 'F3E8FF', bold: true, italics: true },
  'markerRunColor AI phải bold + italics'
);

const nlsRuns = generator.parseInlineTextToRuns('***[NLS: 1.1.TC1a - GeoGebra]***');
const nlsRun = nlsRuns.find(run => run instanceof docx.TextRun && runText(run).includes('[NLS: 1.1.TC1a - GeoGebra]'));
assert.ok(nlsRun, '***[NLS]*** phải thành TextRun');
assert.ok(hasFormatting(nlsRun, 'w:b'), 'NLS *** phải có w:b');
assert.ok(hasFormatting(nlsRun, 'w:i'), 'NLS *** phải có w:i');
assert.match(JSON.stringify(nlsRun), /0369A1/i, 'NLS *** phải màu 0369A1');
assert.match(JSON.stringify(nlsRun), /E0F2FE/i, 'NLS *** phải shading E0F2FE');

const aiRuns = generator.parseInlineTextToRuns('***[AI: 8.A1.1 - Kiểm chứng phản hồi AI]***');
const aiRun = aiRuns.find(run => run instanceof docx.TextRun && runText(run).includes('[AI: 8.A1.1 - Kiểm chứng phản hồi AI]'));
assert.ok(aiRun, '***[AI]*** phải thành TextRun');
assert.ok(hasFormatting(aiRun, 'w:b'), 'AI *** phải có w:b');
assert.ok(hasFormatting(aiRun, 'w:i'), 'AI *** phải có w:i');
assert.match(JSON.stringify(aiRun), /6D28D9/i, 'AI *** phải màu 6D28D9');
assert.match(JSON.stringify(aiRun), /F3E8FF/i, 'AI *** phải shading F3E8FF');

const headingRuns = generator.parseInlineTextToRuns('***c) Năng lực số***');
assert.ok(
  headingRuns.some(run => run instanceof docx.TextRun && hasFormatting(run, 'w:b') && hasFormatting(run, 'w:i') && runText(run).includes('c) Năng lực số')),
  '***c) Năng lực số*** phải in đậm và in nghiêng'
);

const css = fs.readFileSync(path.join(__dirname, '../css/khbd-styles.css'), 'utf8');
const nlsBadge = css.match(/\.khbd-badge-nls\s*\{[^}]+\}/);
const aiBadge = css.match(/\.khbd-badge-ai\s*\{[^}]+\}/);
const badgeBase = css.match(/\.khbd-badge\s*\{[^}]+\}/);
assert.ok(nlsBadge && /font-style:\s*italic/.test(nlsBadge[0]), 'CSS .khbd-badge-nls phải italic');
assert.ok(aiBadge && /font-style:\s*italic/.test(aiBadge[0]), 'CSS .khbd-badge-ai phải italic');
assert.ok(badgeBase && /font-weight:\s*700/.test(badgeBase[0]), '.khbd-badge phải font-weight 700');
assert.ok(/\.preview-rendered \.khbd-nls[\s\S]{0,180}font-style:\s*italic/.test(css), 'preview .khbd-nls phải italic');
assert.ok(/\.preview-rendered \.khbd-ai[\s\S]{0,180}font-style:\s*italic/.test(css), 'preview .khbd-ai phải italic');

const stub = {
  subjectName: 'Toán',
  topic: 'Tập hợp',
  duration: '2 tiết',
  objectives_content: 'Mục tiêu',
  yccd_official: '',
  pedagogical_context: '',
  grade: '6',
  competencies: [],
  textbook_content: 'Bài 1',
  digitalCompetencyEnabled: true,
  aiCompetencyEnabled: true
};
const promptA = getPromptTemplate('GENERATE_ACTIVITY_A', stub);
assert.ok(promptA.includes('***[NLS: {Miền/Mã} - {Tên phần mềm}]***'), 'Prompt A marker NLS 3 sao');
assert.ok(promptA.includes('***[AI: {Mã} - Kiểm chứng phản hồi AI]***'), 'Prompt A marker AI 3 sao');
assert.ok(
  promptA.includes('BẮT BUỘC: Các vị trí tích hợp NLS và AI phải được in đậm và in nghiêng'),
  'Prompt A có quy tắc in đậm in nghiêng'
);

const promptObj = getPromptTemplate('GENERATE_OBJECTIVES', stub);
assert.ok(
  promptObj.includes('***[Mã NLS đã chọn, ví dụ 1.1.TC1a]:*** *[Mô tả nhiệm vụ số gắn với bài]*'),
  'Objectives NLS dùng ***[Mã]:*** *mô tả*'
);
assert.ok(
  promptObj.includes('***[Mã AI đã chọn]:*** *[Mô tả nhiệm vụ AI gắn với bài]*'),
  'Objectives AI dùng ***[Mã]:*** *mô tả*'
);

const appSrc = fs.readFileSync(path.join(__dirname, '../js/khbd-app.js'), 'utf8');
assert.ok(
  appSrc.includes('- ***${row.item.officialCode}:*** *${row.item.officialLabel}*'),
  'insertObjectivesMissingStandards xuất bullet 3 sao'
);
assert.ok(appSrc.includes('\\*{1,3}\\[?NLS'), 'stripDisabledActivityIntegrations bắt 1-3 sao NLS');
assert.ok(appSrc.includes('\\*{1,3}\\[?AI'), 'stripDisabledActivityIntegrations bắt 1-3 sao AI');

console.log('khbd-nls-ai-bold-italic-smoke: PASS 100%');
