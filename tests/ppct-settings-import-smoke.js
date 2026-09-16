const fs = require('fs');
const assert = require('assert');
const html = fs.readFileSync('soankhbd.html', 'utf8');
const app = fs.readFileSync('js/khbd-app.js', 'utf8');
const api = fs.readFileSync('api/khbd_ppct_catalog.php', 'utf8');

assert.match(html, /modalPpctCatalogSettings/);
assert.match(html, /id="step2PpctLessonSelect"/, 'Vẫn giữ select PPCT ẩn để tương thích CSDL');
assert.match(html, /id="ppctLessonPicker"/, 'Chọn bài PPCT nằm ở thông tin bài học');
assert.match(html, /tab0-sub-lesson-info[\s\S]*ppctLessonPicker/, 'Picker PPCT phải ở tab thông tin bài & lớp');
assert.match(html, /id="lessonPpctAnalysis" style="display:none"/, 'Khối PPCT trùng lặp ở tab học liệu phải được ẩn');
assert.match(html, /Gửi file &amp; Đọc SGK<\/button>/, 'Tab học liệu chính chỉ còn luồng SGK');
assert.match(html, /ppctCatalogGrade/);
assert.match(html, /ppctCatalogSubject/);
assert.match(html, /ppctCatalogYear/);
assert.match(html, /btnSavePpctCatalogSettings/);
assert.match(app, /function analyzePpctImport/);
assert.match(app, /PPCT tái tạo từ JSON/);
assert.match(app, /Chương\/Chủ đề/);
assert.match(app, /Bài học\/Hoạt động/);
assert.match(app, /Ghi chú \/ NLS \/ AI/);
assert.match(app, /Cần kiểm tra/);
assert.match(app, /uncertain_fields/);
assert.match(html, /ppctJsonInput/);
assert.match(html, /btnImportPpctJson/);
assert.match(html, /ppctJsonFileInput/);
assert.match(html, /btnCopyPpctJson/);
assert.match(html, /btnExportPpctJson/);
assert.match(html, /Sao chép Prompt PPCT → JSON/);
assert.match(app, /function buildPpctJsonConversionPrompt/);
assert.match(app, /function importPortablePpctJson/);
assert.match(app, /function ppctCatalogToPortableJson/);
assert.match(app, /schema_version:\"ppct-v1\"/);
assert.match(app, /KHONG DOC RO/);
assert.match(app, /Không tóm tắt, không diễn giải, không sửa tên bài/);
assert.match(app, /academic_year/);
assert.match(app, /ppctCatalogCount/, 'Workflow phải dùng số dòng ppctCatalog làm trạng thái Bước 2');
assert.match(app, /Đã có \$\{ppctCatalogCount\} dòng PPCT/, 'Badge Bước 2 phải báo số dòng PPCT đã lưu');
assert.match(app, /step2PpctLessonSelect/, 'Danh mục PPCT phải được đổ vào dropdown Bước 2');
assert.match(api, /ORDER BY updated_at DESC,id DESC LIMIT 1/, 'API phải lấy PPCT mới nhất khi chưa có năm học');
assert.match(app, /cleanPpctCatalogSource/);
assert.match(app, /Danh mục PPCT cho khối, môn và năm học này đã có/);
assert.match(app, /data-kind="nls"/);
assert.match(app, /data-kind="ai"/);
assert.doesNotMatch(app.match(/function cleanPpctCatalogSource[^\n]+/)?.[0] || '', /dataUrl|rawText|OCR/i);
assert.match(api, /\$_SESSION\['user_id'\]/);
assert.match(api, /academic_year/);
assert.match(html, /mã NLS\/AI và mô tả PPCT được khóa đúng nguồn, không tự tick thêm/);
assert.match(app, /function extractPpctDetailedEntries/);
assert.match(app, /fromPpct: true/);
assert.match(app, /lockedFromPpct: true/);
assert.match(app, /function skipAutoSuggestStandards/);
assert.match(app, /function applyPpctVerbatimObjectives/);

const elements = {};
function element(id) {
  return elements[id] ||= {
    id, value: '', checked: false, textContent: '', innerHTML: '', hidden: false, style: {}, children: [],
    classList: { active: false, add(name) { if (name === 'active') this.active = true; }, remove(name) { if (name === 'active') this.active = false; } },
    dataset: {}, addEventListener() {}, appendChild(child) { this.children.push(child); return child; },
    querySelector() { return null; }, querySelectorAll() { return []; }, scrollIntoView() {}
  };
}
global.window = { addEventListener() {}, lucide: { createIcons() {} } };
global.document = {
  addEventListener() {}, getElementById: element, querySelector() { return null; }, querySelectorAll() { return []; },
  createElement() {
    let text = '';
    return { get textContent() { return text; }, set textContent(value) { text = String(value); }, get innerHTML() { return text; }, appendChild() {}, setAttribute() {} };
  }
};
const storage = {};
global.localStorage = { getItem: key => storage[key] || null, setItem: (key, value) => { storage[key] = String(value); }, removeItem: key => delete storage[key] };
global.showToast = () => {};
global.renderMathPreview = () => {};
global.updateWorkflowStepper = () => {};

Object.assign(global, require('../js/khbd-standards.js'));
const khbd = require('../js/khbd-app.js');
const { getPromptTemplate } = require('../js/khbd-prompts.js');

const nlsDesc = 'Sử dụng máy tính cầm tay (phím CALC) để kiểm tra cặp số (x; y) có là nghiệm của hệ phương trình hay không.';
const aiDesc = 'Sử dụng trợ lý AI tạo các ví dụ ngẫu nhiên về phương trình để luyện tập nhận biết khái niệm và chịu trách nhiệm kiểm chứng kết quả (Áp dụng: tiết 1, 2).';
const extracted = khbd.extractPpctDetailedEntries(
  `5.3.TC2a : ${nlsDesc}\n9.B2.1 : ${aiDesc}`
);
assert.deepStrictEqual(extracted.map(item => item.code), ['5.3.TC2a', '9.B2.1']);
assert.strictEqual(extracted.find(item => item.code === '5.3.TC2a').description, nlsDesc);
assert.ok(extracted.find(item => item.code === '9.B2.1').description.includes('Sử dụng trợ lý AI tạo các ví dụ ngẫu nhiên'));

khbd.appState.selectedGrade = '9';
khbd.appState.selectedSubject = 'toan';
khbd.appState.teachingContext = khbd.normalizeTeachingContext({ integrations: { digital: true, ai: false }, standards: [] });
khbd.appState.ppctCatalog = {
  rows: [{
    id: 'bai1',
    title: 'Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn',
    tietCt: '1, 2',
    periods: 2,
    week: '1',
    nls: { enabled: true, codes: ['5.3.TC2a'], evidence: `5.3.TC2a : ${nlsDesc}` },
    ai: { enabled: true, codes: ['9.B2.1'], evidence: `9.B2.1 : ${aiDesc}` },
    digital_competency: [{ code: '5.3.TC2a', description: nlsDesc }],
    ai_competency: [{ code: '9.B2.1', description: aiDesc }]
  }],
  selectedRowId: '',
  source: {},
  serverId: null
};
khbd.applyPpctCatalogRow('bai1');
const codes = khbd.appState.teachingContext.standards.map(item => item.officialCode).sort();
assert.deepStrictEqual(codes, ['5.3.TC2a', '9.B2.1'], 'Chỉ tick đúng 2 mã PPCT');
assert.ok(!codes.includes('1.1.TC2a') && !codes.includes('5.2.TC2a'), 'Không tự tick thêm 1.1.TC2a hay 5.2.TC2a');
assert.ok(khbd.appState.teachingContext.standards.every(item => item.fromPpct || item.lockedFromPpct), 'Mã PPCT phải khóa fromPpct');
assert.strictEqual(khbd.appState.teachingContext.standards.find(item => item.officialCode === '5.3.TC2a').proposedTask, nlsDesc);
assert.ok(khbd.appState.teachingContext.standards.find(item => item.officialCode === '9.B2.1').proposedTask.includes('Sử dụng trợ lý AI tạo các ví dụ ngẫu nhiên'));

khbd.appState.content.vision = 'Bài 1. Khái niệm phương trình. Cho hệ phương trình bậc nhất hai ẩn. Học sinh kiểm tra cặp số (x; y). '.repeat(4);
khbd.appState.teachingContext.ocrReady = true;
Promise.resolve(khbd.requestStructuredIntegrationCandidates('digital', { silent: true, force: true })).then(async digitalResult => {
  assert.strictEqual(digitalResult, false, 'Không tự đề xuất thêm NLS khi đã khóa PPCT');
  const afterDigital = khbd.appState.teachingContext.standards.map(item => item.officialCode).sort();
  assert.deepStrictEqual(afterDigital, ['5.3.TC2a', '9.B2.1']);
  const aiResult = await khbd.requestStructuredIntegrationCandidates('ai', { silent: true, force: true });
  assert.strictEqual(aiResult, false, 'Không tự đề xuất thêm AI khi đã khóa PPCT');
  assert.deepStrictEqual(khbd.appState.teachingContext.standards.map(item => item.officialCode).sort(), ['5.3.TC2a', '9.B2.1']);

  const ctx = khbd.getGenerationPromptContext();
  assert.ok(ctx.ppct_objectives_verbatim, 'Prompt mục tiêu phải khóa mô tả PPCT');
  assert.match(ctx.digital_objectives_section, /5\.3\.TC2a/);
  assert.ok(ctx.digital_objectives_section.includes(nlsDesc), 'Prompt NLS phải chứa nguyên văn mô tả PPCT');
  assert.ok(ctx.ai_objectives_section.includes(aiDesc) || ctx.ai_objectives_section.includes('Sử dụng trợ lý AI tạo các ví dụ ngẫu nhiên'), 'Prompt AI phải chứa nguyên văn mô tả PPCT');
  const promptObj = getPromptTemplate('GENERATE_OBJECTIVES', ctx);
  assert.ok(promptObj.includes(`### c) Năng lực số: ***[5.3.TC2a]:*** ${nlsDesc}`), 'GENERATE_OBJECTIVES phải chép nguyên văn NLS PPCT');
  assert.ok(promptObj.includes('### d) Năng lực AI: ***[9.B2.1]:***'), 'GENERATE_OBJECTIVES phải chép nguyên văn AI PPCT');
  assert.ok(promptObj.includes('CẤM diễn đạt lại') || promptObj.includes('KHÓA MÔ TẢ NLS/AI THEO PPCT'), 'Prompt phải cấm bịa lại mô tả PPCT');

  const objectives = khbd.applyPpctVerbatimObjectives('# I. MỤC TIÊU\n## 2. Về năng lực\n### c) Năng lực số\n- bịa\n### d) Năng lực AI\n- bịa\n## 3. Về phẩm chất\n- Trung thực');
  assert.ok(objectives.includes(`### c) Năng lực số: ***[5.3.TC2a]:*** ${nlsDesc}`), 'Phần I phải giữ nguyên văn mô tả NLS từ PPCT');
  assert.ok(objectives.includes('### d) Năng lực AI: ***[9.B2.1]:***') && objectives.includes('Sử dụng trợ lý AI tạo các ví dụ ngẫu nhiên'), 'Phần I phải giữ nguyên văn mô tả AI từ PPCT');
  assert.ok(!objectives.includes('1.1.TC2a') && !objectives.includes('5.2.TC2a'), 'Phần I không được thêm mã ngoài PPCT');
  console.log('PASS ppct settings import smoke');
}).catch(error => {
  console.error(error);
  process.exit(1);
});
