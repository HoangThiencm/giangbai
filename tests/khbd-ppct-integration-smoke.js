/**
 * tests/khbd-ppct-integration-smoke.js
 * Kiểm thử tích hợp đính kèm & phân tích Phân phối chương trình (PPCT / Phụ lục 3 CV 5512) tại Bước 0.
 */

'use strict';

const assert = require('assert');
const path = require('path');

// Mock browser environment for khbd-app
global.window = {
  addEventListener: () => {},
  removeEventListener: () => {},
  document: {},
  lucide: { createIcons: () => {} }
};

const domStore = {};
global.document = {
  addEventListener: () => {},
  getElementById: (id) => {
    if (!domStore[id]) {
      domStore[id] = {
        id,
        value: '',
        checked: false,
        textContent: '',
        innerHTML: '',
        style: {},
        classList: { add: () => {}, remove: () => {}, contains: () => false },
        addEventListener: () => {},
        appendChild: () => {},
        append: () => {}
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

// Mock helpers
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

// Load app
const app = require('../js/khbd-app.js');

console.log('================================================================================');
console.log('KIỂM THỬ TÍCH HỢP PPCT (PHỤ LỤC 3 CÔNG VĂN 5512) - SMOKE TESTS');
console.log('================================================================================');

// 1. Kiểm tra Prompt ANALYZE_PPCT
console.log('\n[TEST 1] Kiểm tra PROMPTS.ANALYZE_PPCT, cấu trúc Ma trận 7 Cột và Lệnh cấm...');
assert(typeof global.PROMPTS.ANALYZE_PPCT === 'string', 'PROMPTS.ANALYZE_PPCT phải là một string.');
assert(global.PROMPTS.ANALYZE_PPCT.includes('Phụ lục 3'), 'Prompt phải nhắc đến Phụ lục 3.');
assert(global.PROMPTS.ANALYZE_PPCT.includes('5512'), 'Prompt phải nhắc đến Công văn 5512.');
assert(global.PROMPTS.ANALYZE_PPCT.includes('Tiết CT'), 'Prompt phải có cột Tiết CT.');
assert(global.PROMPTS.ANALYZE_PPCT.includes('Bài học / Chủ đề') || global.PROMPTS.ANALYZE_PPCT.includes('Bài học'), 'Prompt phải có cột Bài học / Chủ đề.');
assert(global.PROMPTS.ANALYZE_PPCT.includes('Số tiết'), 'Prompt phải có cột Số tiết.');
assert(global.PROMPTS.ANALYZE_PPCT.includes('Tuần'), 'Prompt phải có cột Tuần.');
assert(global.PROMPTS.ANALYZE_PPCT.includes('Thiết bị dạy học'), 'Prompt phải có cột Thiết bị dạy học.');
assert(global.PROMPTS.ANALYZE_PPCT.includes('Địa điểm dạy học'), 'Prompt phải có cột Địa điểm dạy học.');
assert(global.PROMPTS.ANALYZE_PPCT.includes('Ghi chú / Tích hợp') || global.PROMPTS.ANALYZE_PPCT.includes('Ghi chú'), 'Prompt phải có cột Ghi chú / Tích hợp.');
assert(global.PROMPTS.ANALYZE_PPCT.includes('TUYỆT ĐỐI CẤM sinh Kế hoạch bài dạy'), 'Prompt phải có chỉ thị cấm sinh KHBD.');
assert(global.PROMPTS.ANALYZE_PPCT.includes('CẤM viết tiến trình dạy học'), 'Prompt phải có chỉ thị cấm viết tiến trình dạy học.');
assert(global.PROMPTS.ANALYZE_PPCT.includes('Gợi ý phạm vi tiết dạy (Lesson Scope)'), 'Prompt phải có mục Gợi ý phạm vi tiết dạy.');
console.log('✓ PROMPTS.ANALYZE_PPCT hợp lệ chuẩn Ma trận 7 Cột Phụ lục 3 CV 5512 và lệnh cấm nghiêm ngặt.');

// 2. Kiểm tra getPromptTemplate với ANALYZE_PPCT
console.log("\n[TEST 2] Kiểm tra getPromptTemplate('ANALYZE_PPCT', ...)...");
const ppctPrompt = global.getPromptTemplate('ANALYZE_PPCT', {
  subject: 'toan',
  subjectName: 'Toán',
  gradeLevelName: 'THCS',
  grade: '6',
  topic: 'Tập hợp các số tự nhiên',
  duration: '02 tiết (90 phút)'
});
assert(ppctPrompt.includes('Toán'), 'Prompt template phải chứa tên môn Toán.');
assert(ppctPrompt.includes('Tập hợp các số tự nhiên'), 'Prompt template phải chứa tên bài dạy.');
console.log("✓ getPromptTemplate('ANALYZE_PPCT') hoạt động chính xác.");

// 3. Kiểm tra getPromptTemplate với lesson_scope và ppct_content
console.log('\n[TEST 3] Kiểm tra chèn {lesson_scope} và {ppct_content} vào các prompt soạn bài...');
const mockContext = {
  subject: 'toan',
  subjectName: 'Toán',
  gradeLevelName: 'THCS',
  grade: '7',
  topic: 'Số vô tỉ. Căn bậc hai số học',
  duration: '02 tiết (90 phút)',
  lesson_scope: 'Tiết 1: Số vô tỉ và Căn bậc hai số học (Mục 1 + 2)',
  ppct_content: '| Tiết CT | Bài học / Chủ đề | Số tiết | Tuần | Thiết bị dạy học | Địa điểm dạy học | Ghi chú / Tích hợp |\n| 1 | Số vô tỉ. Căn bậc hai số học | 1 | Tuần 5 | Thước kẻ, máy tính Casio | Lớp học | Tích hợp AI |',
  textbook_content: 'I. Số vô tỉ\nII. Căn bậc hai số học\nLuyện tập 1\nBài tập 2.1',
  objectives_content: '1. Về kiến thức: Nhận biết số vô tỉ và căn bậc hai số học.',
  activities_content: ''
};

const objPrompt = global.getPromptTemplate('GENERATE_OBJECTIVES', mockContext);
assert(objPrompt.includes('Tiết 1: Số vô tỉ'), 'Prompt GENERATE_OBJECTIVES phải chứa lesson_scope.');
assert(objPrompt.includes('ĐỊNH HƯỚNG PHÂN PHỐI CHƯƠNG TRÌNH & PHẠM VI TIẾT HỌC'), 'Prompt phải chứa khối ràng buộc PPCT.');
assert(objPrompt.includes('Thước kẻ, máy tính Casio'), 'Prompt phải chứa ppct_content.');

const corePrompt = global.getPromptTemplate('GENERATE_CORE_LESSON', mockContext);
assert(corePrompt.includes('Tiết 1: Số vô tỉ'), 'Prompt GENERATE_CORE_LESSON phải chứa lesson_scope.');
assert(corePrompt.includes('Thước kẻ, máy tính Casio'), 'Prompt GENERATE_CORE_LESSON phải chứa ppct_content.');

const actBPrompt = global.getPromptTemplate('GENERATE_ACTIVITY_B', mockContext);
assert(actBPrompt.includes('Tiết 1: Số vô tỉ'), 'Prompt GENERATE_ACTIVITY_B phải chứa lesson_scope.');

const actAEPrompt = global.getPromptTemplate('GENERATE_ACTIVITIES_AE', mockContext);
assert(actAEPrompt.includes('Tiết 1: Số vô tỉ'), 'Prompt GENERATE_ACTIVITIES_AE phải chứa lesson_scope.');
console.log('✓ Các prompt sư phạm đã thay thế và ràng buộc PPCT / phạm vi tiết dạy thành công.');

// 4. Kiểm tra appState và các trường PPCT & Mặc định NLS = true
console.log('\n[TEST 4] Kiểm tra appState, normalizeTeachingContext và Năng lực số mặc định...');
assert(Array.isArray(app.appState.ppctImages), 'appState.ppctImages phải là một mảng.');
assert(Array.isArray(app.appState.ppctPdfAttachments), 'appState.ppctPdfAttachments phải là một mảng.');
assert(typeof app.appState.content.ppctAnalysis === 'string', 'appState.content.ppctAnalysis phải là một chuỗi.');
assert.strictEqual(app.appState.teachingContext.integrations.digital, true, 'appState NLS phải mặc định true.');

const normalizedCtx = app.normalizeTeachingContext({
  lessonScope: 'Tiết 15-16',
  specialRequirements: 'Tập trung phân hóa'
});
assert.strictEqual(normalizedCtx.lessonScope, 'Tiết 15-16', 'normalizeTeachingContext phải giữ nguyên lessonScope.');
assert.strictEqual(normalizedCtx.integrations.digital, true, 'normalizeTeachingContext phải mặc định digital = true.');
console.log('✓ appState và normalizeTeachingContext xử lý PPCT / lessonScope & NLS mặc định chính xác.');

// 5. Kiểm tra buildPedagogicalContext & getGenerationPromptContext
console.log('\n[TEST 5] Kiểm tra buildPedagogicalContext & getGenerationPromptContext...');
app.appState.teachingContext.lessonScope = 'Tiết 10 (Mục 1)';
app.appState.content.ppctAnalysis = 'Bảng PPCT mẫu tuần 3';

const pedCtx = app.buildPedagogicalContext();
assert(pedCtx.includes('Tiết 10 (Mục 1)'), 'buildPedagogicalContext phải chứa thông tin lessonScope.');
assert(pedCtx.includes('Phân phối chương trình (PPCT / Phụ lục 3 CV 5512)'), 'buildPedagogicalContext phải chứa thông tin PPCT.');

const genCtx = app.getGenerationPromptContext();
assert.strictEqual(genCtx.lesson_scope, 'Tiết 10 (Mục 1)', 'getGenerationPromptContext.lesson_scope phải khớp appState.');
assert.strictEqual(genCtx.ppct_content, 'Bảng PPCT mẫu tuần 3', 'getGenerationPromptContext.ppct_content phải khớp appState.');
console.log('✓ buildPedagogicalContext & getGenerationPromptContext đồng bộ thông tin PPCT chuẩn xác.');

// 6. Kiểm tra emptyDraftForTarget và handleClearAllContent
console.log('\n[TEST 6] Kiểm tra reset trạng thái PPCT khi emptyDraft hoặc clearAll...');
app.appState.ppctImages = [{ id: 'test_ppct_1', name: 'ppct.png' }];
app.appState.ppctPdfAttachments = [{ id: 'pdf_1', name: 'ppct.pdf' }];

app.emptyDraftForTarget({ grade: '8', lesson: 'Bài 1', topic: 'Đơn thức' });
assert.strictEqual(app.appState.content.ppctAnalysis, '', 'emptyDraftForTarget phải reset ppctAnalysis.');
assert.strictEqual(app.appState.ppctImages.length, 0, 'emptyDraftForTarget phải reset ppctImages.');
assert.strictEqual(app.appState.ppctPdfAttachments.length, 0, 'emptyDraftForTarget phải reset ppctPdfAttachments.');
assert.strictEqual(app.appState.teachingContext.lessonScope, '', 'emptyDraftForTarget phải reset lessonScope.');
console.log('✓ Đã reset sạch sẽ state PPCT khi tạo draft mới.');

// 7. Kiểm tra parsePpctLessonDetails và tự động bóc tách Lesson Scope & AI
console.log('\n[TEST 7] Kiểm tra helper parsePpctLessonDetails...');
const samplePpctOutput = `
# PHÂN PHỐI CHƯƠNG TRÌNH MÔN TOÁN LỚP 6

1. **Bảng Khung Ma trận Phân phối chương trình (Chuẩn Phụ lục 3 Công văn 5512 - 7 Cột):**
| Tiết CT | Bài học / Chủ đề | Số tiết | Tuần | Thiết bị dạy học | Địa điểm dạy học | Ghi chú / Tích hợp |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Tập hợp các số tự nhiên | 1 | Tuần 1 | Máy chiếu, phiếu học tập | Lớp học | Tích hợp AI (QĐ 2422) |
| 2 | Các phép tính với số tự nhiên | 2 | Tuần 1, 2 | Bảng phụ | Lớp học | Không |

2. **Bóc tách thông tin trọng tâm cho bài học "Tập hợp các số tự nhiên":**
- **Tiết CT:** 1
- **Tuần:** Tuần 1
- **Thời lượng:** 01 tiết (45 phút)
- **Thiết bị dạy học:** Máy chiếu, phiếu học tập
- **Địa điểm dạy học:** Lớp học
- **Ghi chú / Tích hợp:** Tích hợp AI (QĐ 2422)
- **Gợi ý phạm vi tiết dạy (Lesson Scope):** Tiết 1 (Tuần 1) - Thời lượng: 01 tiết (45 phút)
`;

const parsed1 = app.parsePpctLessonDetails(samplePpctOutput, "Tập hợp các số tự nhiên");
assert.strictEqual(parsed1.lessonScopeSuggestion, 'Tiết 1 (Tuần 1) - Thời lượng: 01 tiết (45 phút)', 'Bóc tách lessonScopeSuggestion phải chính xác.');
assert.strictEqual(parsed1.hasAiIntegration, true, 'hasAiIntegration phải là true khi có ghi chú Tích hợp AI.');
assert.strictEqual(parsed1.durationSuggestion, '01 tiết (45 phút)', 'durationSuggestion phải khớp.');
assert.strictEqual(parsed1.details.tietCt, '1', 'Tiết CT phải là 1.');
assert.strictEqual(parsed1.details.tuan, 'Tuần 1', 'Tuần phải là Tuần 1.');

const sampleNoAiOutput = `
2. **Bóc tách thông tin trọng tâm cho bài học "Đoạn thẳng":**
- **Tiết CT:** 18, 19
- **Tuần:** Tuần 9, 10
- **Thời lượng:** 02 tiết (90 phút)
- **Thiết bị dạy học:** Thước thẳng có vạch chia
- **Địa điểm dạy học:** Lớp học
- **Ghi chú / Tích hợp:** Không
`;

const parsed2 = app.parsePpctLessonDetails(sampleNoAiOutput, "Đoạn thẳng");
assert.strictEqual(parsed2.hasAiIntegration, false, 'hasAiIntegration phải là false khi không có ghi chú AI.');
assert.strictEqual(parsed2.lessonScopeSuggestion, 'Tiết 18, 19 (Tuần 9, 10) - Thời lượng: 02 tiết (90 phút)', 'Tự động tổng hợp lessonScopeSuggestion khi không có dòng gợi ý tường minh.');
console.log('✓ parsePpctLessonDetails bóc tách và nhận diện AI & Lesson Scope chính xác 100%.');

console.log('\n================================================================================');
console.log('🎉 TẤT CẢ CÁC BÀI KIỂM THỬ PPCT SMOKE ĐÃ VƯỢT QUA 100% THÀNH CÔNG!');
console.log('================================================================================');
