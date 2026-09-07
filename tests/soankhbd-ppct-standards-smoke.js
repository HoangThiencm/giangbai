'use strict';

const assert = require('assert');
const elements = {};
function element(id) {
  return elements[id] ||= {
    id, value: '', checked: false, textContent: '', innerHTML: '', hidden: false, style: {},
    classList: { active: false, add(name) { if (name === 'active') this.active = true; }, remove(name) { if (name === 'active') this.active = false; } },
    addEventListener() {}, querySelectorAll() { return []; }, scrollIntoView() {}
  };
}
global.window = { addEventListener() {}, lucide: { createIcons() {} } };
global.document = {
  addEventListener() {}, getElementById: element, querySelector() { return null; }, querySelectorAll() { return []; },
  createElement() {
    let text = '';
    return { get textContent() { return text; }, set textContent(value) { text = String(value); }, get innerHTML() { return text; } };
  }
};
const storage = {};
global.localStorage = { getItem: key => storage[key] || null, setItem: (key, value) => { storage[key] = String(value); }, removeItem: key => delete storage[key] };
global.showToast = () => {};
global.renderMathPreview = () => {};
global.updateWorkflowStepper = () => {};

Object.assign(global, require('../js/khbd-standards.js'));
const app = require('../js/khbd-app.js');

app.appState.selectedGrade = '6';
app.appState.selectedLesson = 'Bài 1. Tập hợp';
app.appState.customTopic = '';
app.appState.teachingContext = app.normalizeTeachingContext({ integrations: { digital: false, ai: false }, standards: [] });
const ppct = [
  '| Bài học | Ghi chú / Tích hợp |',
  '| Bài 1. Tập hợp | [NLS: 1.1.TC1a] [NLS: 5.3.TC1a] [AI: 6.A1.1] |',
  '| Bài 2. Số nguyên | [NLS: 2.1.TC1a] [AI: 6.A1.2] |'
].join('\n');
const detected = app.extractStandardsFromPpctText(ppct, app.appState.selectedLesson, '6');
assert.deepStrictEqual(detected.digital.map(entry => entry.code), ['1.1.TC1a', '5.3.TC1a']);
assert.deepStrictEqual(detected.ai.map(entry => entry.code), ['6.A1.1']);
assert.strictEqual(detected.matchedLines.length, 1, 'must prefer the PPCT row matching the chosen lesson');

assert.strictEqual(app.applyPpctDetectedStandards(detected), true);
assert.strictEqual(element('toggleDigitalCompetency').checked, true);
assert.strictEqual(element('toggleAiCompetency').checked, true);
assert.strictEqual(app.appState.teachingContext.integrations.digital, true);
assert.strictEqual(app.appState.teachingContext.integrations.ai, true);
assert.deepStrictEqual(app.appState.teachingContext.standards.filter(item => item.standardKind === 'digital').map(item => item.officialCode), ['1.1.TC1a', '5.3.TC1a']);
assert.deepStrictEqual(app.appState.teachingContext.standards.filter(item => item.standardKind === 'ai').map(item => item.officialCode), ['6.A1.1']);
assert.strictEqual(element('modalPpctStandardsDetected').classList.active, true);
assert.match(element('ppctDetectedStandardsList').innerHTML, /1\.1\.TC1a/);
assert.match(element('ppctDetectedStandardsList').innerHTML, /6\.A1\.1/);
app.closePpctStandardsModal();
assert.strictEqual(element('modalPpctStandardsDetected').classList.active, false);

const wrongBand = app.extractStandardsFromPpctText('[NLS: 1.1.TC2a] [AI: 8.A1.1]', '', '6');
assert.deepStrictEqual(wrongBand.digital, []);
assert.deepStrictEqual(wrongBand.ai, []);
console.log('PASS soankhbd PPCT standards smoke');
