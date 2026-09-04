'use strict';

const assert = require('assert');

const store = {};
global.localStorage = {
  getItem: (key) => (key in store ? store[key] : null),
  setItem: (key, value) => { store[key] = String(value); },
  removeItem: (key) => { delete store[key]; }
};
global.document = {
  getElementById() { return null; },
  querySelector() { return null; },
  querySelectorAll() { return []; },
  addEventListener() {},
  createElement() { return { style: {}, classList: { add() {}, remove() {}, contains() { return false; } } }; }
};
global.window = global;
global.alert = () => {};
global.prompt = () => '';
global.confirm = () => false;

const { getPromptTemplate } = require('../js/khbd-prompts.js');
const app = require('../js/khbd-app.js');

function setFlags({ digital, ai }) {
  app.appState.teachingContext.integrations.digital = digital;
  app.appState.teachingContext.integrations.ai = ai;
}

const stub = {
  subjectName: 'Toán',
  topic: 'Tập hợp',
  duration: '2 tiết',
  grade: '6',
  textbook_content: 'Bài 1: Tập hợp',
  pedagogical_context: ''
};

setFlags({ digital: true, ai: false });
const constraintOff = app.buildIntegrationActivityConstraint('B');
assert.ok(/CẤM|KHÔNG bật/.test(constraintOff), 'aiOn=false phải có lệnh cấm AI');
assert.ok(!constraintOff.includes('Dạng 1'), 'aiOn=false không được chứa Dạng 1');
assert.ok(!constraintOff.includes('Dạng 2'), 'aiOn=false không được chứa Dạng 2');
assert.ok(constraintOff.includes('[AI]'), 'aiOn=false phải nêu cấm tag [AI]');
assert.ok(constraintOff.includes('[NLS:'), 'digitalOn && !aiOn vẫn cho phép kịch bản NLS');

const dirty = 'HS đối chiếu SGK **[AI: 7.A1.MR1 - Kiểm chứng phản hồi AI]** rồi dùng **[NLS: 1.1.TC1a - GeoGebra]** và [AI].\n- Hướng dẫn Prompt AI an toàn: ...\n- Mẫu Prompt: "Em hãy hỏi AI"';
const cleaned = app.stripDisabledActivityIntegrations(dirty);
assert.ok(!cleaned.includes('**[AI: 7.A1.MR1 - Kiểm chứng phản hồi AI]**'), 'phải xóa marker AI đậm');
assert.ok(!cleaned.includes('[AI]'), 'phải xóa [AI]');
assert.ok(!/Hướng dẫn Prompt AI/.test(cleaned), 'phải xóa dòng hướng dẫn Prompt AI');
assert.ok(!/Mẫu Prompt:/.test(cleaned), 'phải xóa dòng Mẫu Prompt');
assert.ok(cleaned.includes('[NLS: 1.1.TC1a - GeoGebra]') || cleaned.includes('**[NLS: 1.1.TC1a - GeoGebra]**'), 'NLS phải được giữ khi digitalOn');

setFlags({ digital: true, ai: true });
const kept = app.stripDisabledActivityIntegrations('Giữ **[AI: 7.A1.MR1 - Kiểm chứng phản hồi AI]** và [AI]');
assert.ok(kept.includes('**[AI: 7.A1.MR1 - Kiểm chứng phản hồi AI]**'), 'aiOn=true phải giữ marker AI');
assert.ok(kept.includes('[AI]'), 'aiOn=true phải giữ [AI]');

const promptLocked = getPromptTemplate('GENERATE_ACTIVITY_B', { ...stub, aiCompetencyEnabled: false, digitalCompetencyEnabled: true });
assert.ok(promptLocked.includes('QUY TẮC BẮT BUỘC VỀ KHUNG NĂNG LỰC AI'), 'getPromptTemplate phải khóa AI khi không bật');
assert.ok(promptLocked.includes('LỆNH BẮT BUỘC KHÓA NĂNG LỰC AI'), 'getPromptTemplate phải có lệnh khóa AI');
['GENERATE_ACTIVITY_A', 'GENERATE_ACTIVITY_C', 'GENERATE_ACTIVITY_D', 'GENERATE_ACTIVITY_E'].forEach(key => {
  const p = getPromptTemplate(key, { ...stub, aiCompetencyEnabled: false });
  assert.ok(p.includes('TUYỆT ĐỐI CẤM'), `${key} phải có chỉ thị cấm AI khi tắt`);
});

const promptAiOn = getPromptTemplate('GENERATE_ACTIVITY_B', { ...stub, aiCompetencyEnabled: true, digitalCompetencyEnabled: true });
assert.ok(!promptAiOn.includes('LỆNH BẮT BUỘC KHÓA NĂNG LỰC AI'), 'khi bật AI không gắn lệnh khóa AI');

console.log('khbd-ai-integration-gate: passed');
