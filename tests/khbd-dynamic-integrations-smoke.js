'use strict';

const assert = require('assert');

// Giả lập môi trường DOM
global.window = {
  addEventListener: () => {},
  removeEventListener: () => {},
  document: {},
  lucide: { createIcons: () => {} }
};

const domStore = {};
global.document = {
  addEventListener: () => {},
  createElement(tag) {
    return {
      tagName: String(tag || 'div').toUpperCase(),
      id: '',
      value: '',
      checked: false,
      textContent: '',
      innerHTML: '',
      hidden: false,
      style: {},
      dataset: {},
      classList: { add() {}, remove() {}, contains() { return false; } },
      setAttribute() {},
      getAttribute() { return null; },
      addEventListener() {},
      appendChild() {},
      append() {}
    };
  },
  getElementById(id) {
    if (!domStore[id]) {
      domStore[id] = {
        id,
        value: '',
        checked: false,
        textContent: '',
        innerHTML: '',
        hidden: false,
        style: {},
        dataset: {},
        classList: { add() {}, remove() {}, contains() { return false; } },
        addEventListener() {},
        appendChild() {},
        append() {}
      };
    }
    return domStore[id];
  },
  querySelectorAll: () => []
};

const lsStore = {};
global.localStorage = {
  getItem(k) { return lsStore[k] || null; },
  setItem(k, v) { lsStore[k] = String(v); },
  removeItem(k) { delete lsStore[k]; },
  clear() { Object.keys(lsStore).forEach(k => delete lsStore[k]); }
};

global.showToast = () => {};
global.updateProgress = () => {};
global.hideProgress = () => {};
global.renderMathPreview = () => {};
global.userConfirm = () => true;

try {
  const curr = require('../js/khbd-curriculum.js');
  Object.assign(global, curr);
} catch (e) {}

try {
  const ped = require('../js/khbd-pedagogy-catalog.js');
  Object.assign(global, ped);
} catch (e) {}

try {
  const prm = require('../js/khbd-prompts.js');
  Object.assign(global, prm);
} catch (e) {}

try {
  const { KHBD_STANDARDS } = require('../js/khbd-standards.js');
  global.KHBD_STANDARDS = KHBD_STANDARDS;
} catch (e) {}

const app = require('../js/khbd-app.js');
const { DocxGenerator, docxGenerator } = require('../js/khbd-docx.js');

function idsFor(subjectId) {
  return app.contextIntegrationsForSubject(subjectId).map(item => item.id);
}

console.log('================================================================================');
console.log('KIỂM THỬ HỆ THỐNG BỘ LỌC TÍCH HỢP ĐỘNG THEO MÔN (DYNAMIC SUBJECT INTEGRATIONS)');
console.log('================================================================================');

// -----------------------------------------------------------------------------
// TEST 1: CATALOG MÔN HỌC & CĂN CỨ PHÁP LÝ
// -----------------------------------------------------------------------------
console.log('\n[TEST 1] Kiểm tra Catalog 14 mục tích hợp và phân môn...');
assert(Array.isArray(app.SUBJECT_CONTEXT_INTEGRATIONS), 'SUBJECT_CONTEXT_INTEGRATIONS phải là mảng.');
assert.ok(app.SUBJECT_CONTEXT_INTEGRATIONS.length >= 12, 'Phải có ít nhất 12 loại tích hợp.');

// Môn Toán
const toanIds = idsFor('toan');
assert.ok(toanIds.includes('financialEd'), 'Toán phải có Giáo dục tài chính (QĐ 149/QĐ-TTg)');
assert.ok(toanIds.includes('stemModeling'), 'Toán phải có STEM & Mô hình hóa (CV 3089)');
assert.ok(toanIds.includes('virtualLab'), 'Toán phải có Thí nghiệm ảo / GeoGebra');
assert.ok(!toanIds.includes('gdqpan'), 'Toán không lồng GDQPAN');
assert.ok(!toanIds.includes('clil'), 'Toán không có CLIL ngoại ngữ');

// Môn Ngữ văn
const nguvanIds = idsFor('nguvan');
assert.ok(nguvanIds.includes('gdqpan'), 'Ngữ văn có GDQPAN (TT 08/2024)');
assert.ok(nguvanIds.includes('hcmThought'), 'Ngữ văn có Tư tưởng Hồ Chí Minh (CT 05-CT/TW)');
assert.ok(nguvanIds.includes('humanRights'), 'Ngữ văn có Quyền con người (QĐ 1309)');
assert.ok(nguvanIds.includes('greenEnergyEnv'), 'Ngữ văn có Môi trường & Năng lượng xanh');
assert.ok(nguvanIds.includes('localEnv'), 'Ngữ văn có GD địa phương & môi trường');

// Môn KHTN
const khtnIds = idsFor('khtn');
assert.ok(khtnIds.includes('stemModeling'), 'KHTN có STEM');
assert.ok(khtnIds.includes('virtualLab'), 'KHTN có Thí nghiệm ảo PhET/GeoGebra');
assert.ok(khtnIds.includes('greenEnergyEnv'), 'KHTN có Năng lượng xanh & MT');
assert.ok(!khtnIds.includes('clil'), 'KHTN không có CLIL');

// Môn Lịch sử - Địa lí
const lsIds = idsFor('lichsudialy');
assert.ok(lsIds.includes('gdqpan'), 'Lịch sử - Địa lí có GDQPAN');
assert.ok(lsIds.includes('hcmThought'), 'Lịch sử - Địa lí có Bác Hồ');
assert.ok(lsIds.includes('humanRights'), 'Lịch sử - Địa lí có Quyền con người');
assert.ok(lsIds.includes('climateSdgs'), 'Lịch sử - Địa lí có BĐKH & SDGs');
assert.ok(lsIds.includes('localHeritage'), 'Lịch sử - Địa lí có Di sản ĐP');
assert.ok(lsIds.includes('greenEnergyEnv'), 'Lịch sử - Địa lí có Môi trường & Năng lượng xanh');

// Môn Tiếng Anh
const taIds = idsFor('tienganh');
assert.ok(taIds.includes('clil'), 'Tiếng Anh có CLIL');
assert.ok(taIds.includes('speechAiRoleplay'), 'Tiếng Anh có Speech AI');
assert.ok(taIds.includes('vnIdentity'), 'Tiếng Anh có Bản sắc VN');
assert.ok(taIds.includes('globalCitizen'), 'Tiếng Anh có Công dân toàn cầu');
assert.ok(!taIds.includes('gdqpan'), 'Tiếng Anh không có GDQPAN');

// Môn GDCD
const gdcdIds = idsFor('gdcd');
assert.ok(gdcdIds.includes('gdqpan'), 'GDCD có GDQPAN');
assert.ok(gdcdIds.includes('hcmThought'), 'GDCD có Tư tưởng Bác Hồ');
assert.ok(gdcdIds.includes('humanRights'), 'GDCD có Quyền con người');
assert.ok(gdcdIds.includes('financialEd'), 'GDCD có Giáo dục tài chính');

// Môn Tin học & Công nghệ
const tinhocIds = idsFor('tinhoc');
assert.ok(tinhocIds.includes('stemModeling') && tinhocIds.includes('virtualLab'), 'Tin học có STEM & Thí nghiệm ảo');
const cnIds = idsFor('congnghe');
assert.ok(cnIds.includes('stemModeling') && cnIds.includes('virtualLab') && cnIds.includes('greenEnergyEnv'), 'Công nghệ có STEM, Thí nghiệm ảo, Năng lượng xanh');

console.log('✓ Phân loại tích hợp theo môn học chuẩn 100% văn bản pháp quy.');

// -----------------------------------------------------------------------------
// TEST 2: STATE NORMALIZATION & PRUNING KHI ĐỔI MÔN
// -----------------------------------------------------------------------------
console.log('\n[TEST 2] Kiểm tra normalizeTeachingContext và tự động prune khi chuyển môn...');
const emptyCtx = app.normalizeTeachingContext({});
assert.strictEqual(emptyCtx.integrations.digital, true);
assert.strictEqual(emptyCtx.integrations.ai, false);
assert.strictEqual(emptyCtx.integrations.gdqpan, false);
assert.strictEqual(emptyCtx.integrations.stemModeling, false);
assert.strictEqual(emptyCtx.integrations.virtualLab, false);
assert.strictEqual(emptyCtx.integrations.financialEd, false);

// Giả lập giáo viên chọn Ngữ văn và tick GDQPAN + HCM
app.appState.selectedSubject = 'nguvan';
app.appState.teachingContext = app.normalizeTeachingContext({
  integrations: { gdqpan: true, hcmThought: true, clil: false }
});
assert.strictEqual(app.appState.teachingContext.integrations.gdqpan, true);
assert.strictEqual(app.appState.teachingContext.integrations.hcmThought, true);

// Chuyển sang môn Toán: pruneContextIntegrationsForSubject phải tắt GDQPAN và HCM
const changed = app.pruneContextIntegrationsForSubject('toan');
assert.strictEqual(changed, true, 'Phải có thay đổi khi prune các mục không thuộc môn Toán');
assert.strictEqual(app.appState.teachingContext.integrations.gdqpan, false, 'GDQPAN phải bị tắt khi chuyển sang Toán');
assert.strictEqual(app.appState.teachingContext.integrations.hcmThought, false, 'HCM phải bị tắt khi chuyển sang Toán');

console.log('✓ Chuẩn hóa và prune state khi đổi môn hoạt động an toàn.');

// -----------------------------------------------------------------------------
// TEST 3: PROMPT CONSTRAINTS VÀ MARKER GẮN MÔN
// -----------------------------------------------------------------------------
console.log('\n[TEST 3] Kiểm tra Prompt Engineering tích hợp bối cảnh...');
// Môn KHTN tick STEM và Virtual Lab
app.appState.selectedSubject = 'khtn';
app.appState.teachingContext = app.normalizeTeachingContext({
  integrations: { stemModeling: true, virtualLab: true }
});
const khtnPrompt = app.buildPedagogicalContext();
assert.ok(khtnPrompt.includes('TÍCH HỢP BỐI CẢNH'), 'Phải có khối TÍCH HỢP BỐI CẢNH');
assert.ok(khtnPrompt.includes('CV 3089'), 'Phải có căn cứ pháp lý STEM CV 3089');
assert.ok(khtnPrompt.includes('[STEM]'), 'Phải có marker [STEM]');
assert.ok(khtnPrompt.includes('[TN-AO]'), 'Phải có marker [TN-AO]');
assert.ok(khtnPrompt.includes('CÁC MỤC KHÔNG TICK'), 'Phải có danh sách cấm các mục không tick');

// Môn Toán tick GD tài chính
app.appState.selectedSubject = 'toan';
app.appState.teachingContext = app.normalizeTeachingContext({
  integrations: { financialEd: true }
});
const toanPrompt = app.buildPedagogicalContext();
assert.ok(toanPrompt.includes('QĐ 149/QĐ-TTg'), 'Toán phải có QĐ 149 về GD tài chính');
assert.ok(toanPrompt.includes('[GDTC]'), 'Toán phải có marker [GDTC]');

// Môn Tiếng Anh tick CLIL
app.appState.selectedSubject = 'tienganh';
app.appState.teachingContext = app.normalizeTeachingContext({
  integrations: { clil: true }
});
const taPrompt = app.buildPedagogicalContext();
assert.ok(taPrompt.includes('[CLIL]'), 'Tiếng Anh phải có marker [CLIL]');

console.log('✓ Prompt Constraints và Marker sinh chuẩn xác.');

// -----------------------------------------------------------------------------
// TEST 4: PREVIEW BADGE CLASS RESOLUTION
// -----------------------------------------------------------------------------
console.log('\n[TEST 4] Kiểm tra Badge Class Resolution trong KaTeX/Preview...');
assert.strictEqual(app.getIntegrationBadgeClass('[NLS: 1.1 - GeoGebra]'), 'khbd-badge khbd-badge-nls');
assert.strictEqual(app.getIntegrationBadgeClass('[AI: 2.1 - Prompting]'), 'khbd-badge khbd-badge-ai');
assert.strictEqual(app.getIntegrationBadgeClass('[GDQPAN: Chủ quyền biển đảo]'), 'khbd-badge khbd-badge-gdqpan');
assert.strictEqual(app.getIntegrationBadgeClass('[HCM: Tinh thần tự học]'), 'khbd-badge khbd-badge-hcm');
assert.strictEqual(app.getIntegrationBadgeClass('[QCN: Bình đẳng giới]'), 'khbd-badge khbd-badge-qcn');
assert.strictEqual(app.getIntegrationBadgeClass('[CLIL: Science terms]'), 'khbd-badge khbd-badge-clil');
assert.strictEqual(app.getIntegrationBadgeClass('[GDTC: Tiết kiệm ngân sách]'), 'khbd-badge khbd-badge-taichinh');
assert.strictEqual(app.getIntegrationBadgeClass('[TAICHINH]'), 'khbd-badge khbd-badge-taichinh');
assert.strictEqual(app.getIntegrationBadgeClass('[STEM: Thiết kế mô hình]'), 'khbd-badge khbd-badge-stem');
assert.strictEqual(app.getIntegrationBadgeClass('[TN-AO: Mô phỏng PhET]'), 'khbd-badge khbd-badge-tnao');
assert.strictEqual(app.getIntegrationBadgeClass('[MT-NLX: Năng lượng sạch]'), 'khbd-badge khbd-badge-green');
assert.strictEqual(app.getIntegrationBadgeClass('[GDĐP-MT]'), 'khbd-badge khbd-badge-gddp-mt');
assert.strictEqual(app.getIntegrationBadgeClass('[BĐKH-SDG]'), 'khbd-badge khbd-badge-bdkh-sdg');
assert.strictEqual(app.getIntegrationBadgeClass('[Di sản ĐP]'), 'khbd-badge khbd-badge-heritage');
assert.strictEqual(app.getIntegrationBadgeClass('[Speech AI]'), 'khbd-badge khbd-badge-speechai');
assert.strictEqual(app.getIntegrationBadgeClass('[Bản sắc VN]'), 'khbd-badge khbd-badge-vnidentity');
assert.strictEqual(app.getIntegrationBadgeClass('[CDTG]'), 'khbd-badge khbd-badge-globalcitizen');
assert.strictEqual(app.getIntegrationBadgeClass('[Generic]'), '');

console.log('✓ 100% Badge classes được ánh xạ chính xác.');

// -----------------------------------------------------------------------------
// TEST 5: WORD DOCX EXPORT MARKER RUN COLOR
// -----------------------------------------------------------------------------
console.log('\n[TEST 5] Kiểm tra Word DOCX Export Marker Color & Shading...');
const gen = new DocxGenerator();
assert.deepStrictEqual(gen.markerRunColor('[GDQPAN]'), { color: 'B91C1C', shading: 'FEE2E2', bold: true });
assert.deepStrictEqual(gen.markerRunColor('[HCM: Đạo đức Hồ Chí Minh]'), { color: 'B45309', shading: 'FEF3C7', bold: true });
assert.deepStrictEqual(gen.markerRunColor('[QCN: Quyền con người]'), { color: '047857', shading: 'D1FAE5', bold: true });
assert.deepStrictEqual(gen.markerRunColor('[CLIL: English Integration]'), { color: '4338CA', shading: 'E0E7FF', bold: true });
assert.deepStrictEqual(gen.markerRunColor('[GDTC: Quản lý tài chính]'), { color: '15803D', shading: 'DCFCE7', bold: true });
assert.deepStrictEqual(gen.markerRunColor('[STEM: Mô hình hóa]'), { color: '0E7490', shading: 'CFFAFE', bold: true });
assert.deepStrictEqual(gen.markerRunColor('[TN-AO: PhET Simulation]'), { color: '0284C7', shading: 'E0F2FE', bold: true });
assert.deepStrictEqual(gen.markerRunColor('[MT-NLX: Năng lượng xanh]'), { color: '4D7C0F', shading: 'ECFCCB', bold: true });
assert.deepStrictEqual(gen.markerRunColor('[NLS: 1.1]'), { color: '0369A1', shading: 'E0F2FE', bold: true });
assert.deepStrictEqual(gen.markerRunColor('[AI: 2.1]'), { color: '6D28D9', shading: 'F3E8FF', bold: true });
assert.strictEqual(gen.markerRunColor('[RandomText]'), null);

console.log('✓ DOCX Generator gán đúng màu chữ, shading và in đậm cho mọi marker.');

console.log('\n================================================================================');
console.log('🎉 TẤT CẢ 5 BỘ KIỂM THỬ DYNAMIC INTEGRATIONS ĐÃ VƯỢT QUA 100% THÀNH CÔNG!');
console.log('================================================================================\n');
