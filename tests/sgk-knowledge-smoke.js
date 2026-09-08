const fs = require('fs');
const assert = require('assert');
const vm = require('vm');

console.log('==================================================');
console.log('KIỂM THỬ KHO TRI THỨC SGK DÙNG CHUNG (SMOKE TEST)');
console.log('==================================================');

// 1. Kiểm tra file backend PHP
console.log('-> 1. Kiểm tra mã nguồn API backend api/sgk_knowledge.php...');
const phpContent = fs.readFileSync('api/sgk_knowledge.php', 'utf8');
assert(phpContent.includes('CREATE TABLE IF NOT EXISTS sgk_books'), 'Thiếu lệnh tạo bảng sgk_books');
assert(phpContent.includes('CREATE TABLE IF NOT EXISTS sgk_lessons'), 'Thiếu lệnh tạo bảng sgk_lessons');
assert(phpContent.includes('idx_sgk_books_lookup'), 'Thiếu index lookup bảng sách');
assert(phpContent.includes('idx_sgk_lessons_book'), 'Thiếu index book_id bảng bài học');
assert(phpContent.includes("action === 'check'"), 'Thiếu endpoint check sách tồn tại');
assert(phpContent.includes("action === 'get'"), 'Thiếu endpoint lấy chi tiết sách và bài học');
assert(phpContent.includes("action === 'list'"), 'Thiếu endpoint liệt kê thư viện sách');
assert(phpContent.includes("action === 'save'"), 'Thiếu endpoint lưu bản đồ tri thức');
assert(phpContent.includes("action === 'verify'"), 'Thiếu endpoint kiểm định sách');
assert(phpContent.includes("action === 'delete'"), 'Thiếu endpoint xóa bản đồ tri thức');
assert(phpContent.includes('beginTransaction'), 'Thiếu cơ chế transaction khi lưu');
assert(phpContent.includes('normalize_sgk_book_key'), 'Thiếu hàm chuẩn hóa khóa sách');
console.log('  -> api/sgk_knowledge.php: PASS');

// 2. Kiểm tra giao diện HTML và hooks
console.log('-> 2. Kiểm tra DOM hooks & functions trong xaydungphuluc và canvas...');
const htmlFiles = [
  { path: 'xaydungphuluc.html', isCanvas: false },
  { path: 'canvas_xaydungphuluc.html', isCanvas: true },
  { path: 'backupcode viettailieu/canvas_xaydungphuluc.html', isCanvas: true }
];

const requiredIds = [
  'sharedSgkContainer',
  'sharedSgkTitle',
  'sharedSgkDesc',
  'sharedSgkActions',
  'bookSeries',
  'sgkLibraryModal',
  'sgkLibrarySearch',
  'sgkLibraryList',
  'sgkDetailModal',
  'sgkDetailTitle',
  'sgkDetailSubtitle',
  'sgkDetailContent',
  'btnUseCurBook',
  'sgkJsonFileInput',
  'sgkGradeTabs',
  'btnSeedAllGrade',
  'sgkExtractModal',
  'sgkExtractGrade',
  'sgkExtractSubject',
  'sgkExtractSeries',
  'sgkExtractFileName'
];

const requiredFunctions = [
  'onBookSeriesChange',
  'checkSharedSgkKnowledge',
  'syncSharedSgkToApp',
  'isUnfitDigitalEvidence',
  'recommendLessonDigitalCandidates',
  'buildLessonDigitalEvidence',
  'renderSgkDetailNlsBlock',
  'ensureFullCurriculumLessons',
  'seedStandardSgkKnowledge',
  'extractAndSaveSharedSgk',
  'openSgkLibraryModal',
  'closeSgkLibraryModal',
  'fetchAndRenderSgkLibrary',
  'renderFilteredSgkLibrary',
  'openSgkDetailModal',
  'closeSgkDetailModal',
  'deleteSgkBook',
  'deleteCurrentDetailBook',
  'useCurrentDetailBook',
  'useSharedSgkBook',
  'getSharedSgkLessonKnowledge',
  'exportSgkKnowledgeJson',
  'importSgkKnowledgeJson',
  'switchSgkGradeTab',
  'onSgkSearchInput',
  'renderSgkSubjectMatrix',
  'seedSubjectGradeKnowledge',
  'seedAllSubjectsForGrade',
  'seedAllGradesAllSubjects',
  'applyAndUseSubjectGrade',
  'getSubjectCurriculumKey',
  'getStandardSubjectYccd',
  'getStandardCurriculumCatalog',
  'detectGradeAndSubjectFromFileName',
  'setQuickGrade',
  'updateQuickGradeButtons',
  'openSgkExtractModal',
  'closeSgkExtractModal',
  'confirmAndExecuteSgkExtract'
];

for (const { path, isCanvas } of htmlFiles) {
  const content = fs.readFileSync(path, 'utf8');
  for (const id of requiredIds) {
    assert(content.includes(`id="${id}"`), `File ${path} thiếu DOM element #${id}`);
  }
  for (const fn of requiredFunctions) {
    assert(
      content.includes(`function ${fn}`) || content.includes(`async function ${fn}`),
      `File ${path} thiếu function ${fn}`
    );
  }
  assert(
    content.includes('<option value="Sách giáo khoa dùng chung (từ 2026-2027)" selected>Sách giáo khoa dùng chung (từ 2026-2027)</option>'),
    `File ${path} phải có option "Sách giáo khoa dùng chung (từ 2026-2027)" được selected làm mặc định đầu tiên`
  );
  assert(content.includes('boSach:'), `File ${path} thiếu boSach trong getConfig()`);
  assert(content.includes('SGK_API_ENDPOINT'), `File ${path} thiếu định nghĩa SGK_API_ENDPOINT`);
  if (isCanvas) {
    assert(
      content.includes('https://hoangthiencm.id.vn/api/sgk_knowledge.php'),
      `File ${path} phải trỏ endpoint SGK về hoangthiencm.id.vn`
    );
  } else {
    assert(
      content.includes("api/sgk_knowledge.php"),
      `File ${path} phải dùng endpoint nội bộ api/sgk_knowledge.php`
    );
  }
  console.log(`  -> ${path}: Đầy đủ 100% IDs, hàm JS và option Sách giáo khoa dùng chung: PASS`);
}

// 3. Kiểm tra logic sư phạm tích hợp trong VM Sandbox
console.log('-> 3. Kiểm tra hành vi sư phạm tích hợp trong VM sandbox...');
const sourceCode = fs.readFileSync('xaydungphuluc.html', 'utf8');

// Trích xuất các hàm quan trọng để test
function extractFn(name, code) {
  const match = code.match(new RegExp(`(?:async\\s+)?function\\s+${name}\\s*\\([^{]*\\)\\s*\\{`));
  if (!match) throw new Error(`Missing function ${name}`);
  const start = match.index;
  let depth = 0;
  let inString = null;
  for (let i = start + match[0].length - 1; i < code.length; i++) {
    const ch = code[i];
    if (inString) {
      if (ch === inString && code[i - 1] !== '\\') inString = null;
    } else if (ch === "'" || ch === '"' || ch === '`') {
      inString = ch;
    } else if (ch === '{') {
      depth++;
    } else if (ch === '}') {
      depth--;
      if (depth === 0) {
        return code.slice(start, i + 1);
      }
    }
  }
  throw new Error(`Unclosed function ${name}`);
}

const sandbox = {
  console,
  esc: s => String(s || ''),
  cleanLessonName: s => String(s || '').toLowerCase().replace(/^(bài|chủ đề|tiết)\s*\d+[\s:.-]*/i, '').trim(),
  cleanLessonDescription: s => String(s || '').replace(/^(bài|chủ đề|tiết)\s*\d+[\s:.-]*/i, '').trim(),
  foldText: s => String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd'),
  formatOutcomeLines: s => String(s || '').trim(),
  loadedSharedSgkKnowledge: null,
  lessonsMatch: (t1, t2) => {
    const s1 = String(t1).toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
    const s2 = String(t2).toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
    return s1 && s2 && (s1.includes(s2) || s2.includes(s1));
  },
  lessonOrdinal: s => {
    const m = String(s || '').match(/\bbài\s*(\d+)\b/i);
    return m ? Number(m[1]) : null;
  }
};

vm.createContext(sandbox);

// Load KHBD_YCCD from js/khbd-yccd.js
const yccdCode = fs.readFileSync('js/khbd-yccd.js', 'utf8');
vm.runInContext(yccdCode, sandbox);

// Load KHBD_STANDARDS from js/khbd-standards.js
const standardsCode = fs.readFileSync('js/khbd-standards.js', 'utf8');
vm.runInContext(standardsCode, sandbox);

// Load CURRICULUM_DATA from js/khbd-curriculum.js
const curriculumCode = fs.readFileSync('js/khbd-curriculum.js', 'utf8');
vm.runInContext(curriculumCode, sandbox);

// Load helpers, compactSgkText, lessonOrdinal, ensureFullCurriculumLessons, getSharedSgkLessonKnowledge, lessonAppliedNlsDescription, lessonAppliedAiDescription, appendixOneFallbackOutcome
const codeToRun = [
  extractFn('isUnfitDigitalEvidence', sourceCode),
  extractFn('recommendLessonDigitalCandidates', sourceCode),
  extractFn('buildLessonDigitalEvidence', sourceCode),
  extractFn('renderSgkDetailNlsBlock', sourceCode),
  extractFn('renderSgkDetailAiBlock', sourceCode),
  extractFn('compactSgkText', sourceCode),
  extractFn('lessonOrdinal', sourceCode),
  extractFn('getSubjectCurriculumKey', sourceCode),
  extractFn('getStandardSubjectYccd', sourceCode),
  extractFn('getStandardCurriculumCatalog', sourceCode),
  extractFn('ensureFullCurriculumLessons', sourceCode),
  extractFn('getSharedSgkLessonKnowledge', sourceCode),
  extractFn('lessonAppliedNlsDescription', sourceCode),
  extractFn('lessonAppliedAiDescription', sourceCode),
  extractFn('recommendLessonAiCandidates', sourceCode),
  extractFn('fallbackAiCodes', sourceCode),
  extractFn('fallbackAiCode', sourceCode),
  extractFn('appendixOneFallbackOutcome', sourceCode)
].join('\n\n');

vm.runInContext(codeToRun, sandbox);

// Test 3.1: Khi chưa có tri thức SGK dùng chung
const nlsFallback = vm.runInContext("lessonAppliedNlsDescription('5.3.TC2a', '', 'Bài 1. Khái niệm phương trình')", sandbox);
assert(nlsFallback.includes('máy tính cầm tay') || nlsFallback.includes('GeoGebra'), 'Fallback NLS phải có máy tính hoặc GeoGebra');
console.log('  -> Fallback khi chưa có tri thức dùng chung: PASS');

// Test 3.2: Khi nạp Bản đồ Tri thức SGK dùng chung
sandbox.loadedSharedSgkKnowledge = {
  book: {
    subject: 'Toán học',
    grade: '9',
    series: 'Kết nối tri thức với cuộc sống'
  },
  lessons: [
    {
      lesson_title: 'Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn',
      yccd: '- Nhận biết được phương trình bậc nhất hai ẩn và hệ hai phương trình bậc nhất hai ẩn.\n- Nhận biết nghiệm của hệ hai phương trình bậc nhất hai ẩn.',
      digital_evidence: 'Sử dụng máy tính cầm tay (phím MODE 5 1) để tìm nghiệm và kiểm tra nghiệm của hệ phương trình; sử dụng phần mềm GeoGebra vẽ đồ thị đường thẳng xác định tọa độ giao điểm.',
      ai_pedagogy_hint: 'Sử dụng trợ lý AI tạo tình huống thực tiễn có thể mô hình hóa bằng hệ phương trình bậc nhất hai ẩn; học sinh kiểm chứng nghiệm thực tế.'
    }
  ]
};

// Tra cứu tri thức bài 1
const lookup = vm.runInContext("getSharedSgkLessonKnowledge('Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn')", sandbox);
assert(lookup !== null, 'Phải tìm thấy tri thức bài 1');
assert(lookup.digital_evidence.includes('MODE 5 1'), 'Minh chứng NLS phải khớp với CSDL tri thức');

// Kiểm tra NLS tự động lấy từ tri thức dùng chung
const nlsFromKnowledge = vm.runInContext("lessonAppliedNlsDescription('5.3.TC2a', '', 'Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn')", sandbox);
assert.equal(nlsFromKnowledge, lookup.digital_evidence, 'Mô tả NLS phải lấy trực tiếp từ minh chứng SGK dùng chung');
console.log('  -> NLS tự động lấy từ Bản đồ Tri thức dùng chung: PASS');

// Kiểm tra AI tự động lấy từ tri thức dùng chung
const aiFromKnowledge = vm.runInContext("lessonAppliedAiDescription('9.B2.1', '', 'Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn')", sandbox);
assert.equal(aiFromKnowledge, lookup.ai_pedagogy_hint, 'Mô tả AI phải lấy trực tiếp từ gợi ý sư phạm SGK dùng chung');
console.log('  -> AI tự động lấy từ Bản đồ Tri thức dùng chung: PASS');

// Kiểm tra YCCD Phụ lục 1 tự động lấy từ tri thức dùng chung
const yccdFromKnowledge = vm.runInContext("appendixOneFallbackOutcome('Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn', {lop:'9',monHoc:'Toán học'})", sandbox);
assert(yccdFromKnowledge.includes('Nhận biết được phương trình bậc nhất hai ẩn'), 'YCCD phải lấy chuẩn từ SGK dùng chung');
console.log('  -> YCCD tự động lấy từ Bản đồ Tri thức dùng chung: PASS');

// Test 3.3: Kiểm tra bài Số tự nhiên Toán 6 tuyệt đối không có "kiểm tra nghiệm" hay "vẽ đồ thị"
const nlsArith = vm.runInContext("lessonAppliedNlsDescription('5.3.TC1a', '', 'Bài 3. Thứ tự trong tập hợp các số tự nhiên')", sandbox);
assert(!nlsArith.includes('kiểm tra nghiệm'), 'Bài Toán 6 Số tự nhiên không được chứa "kiểm tra nghiệm"');
assert(!nlsArith.includes('vẽ đồ thị'), 'Bài Toán 6 Số tự nhiên không được chứa "vẽ đồ thị"');
assert(nlsArith.includes('máy tính cầm tay') && (nlsArith.includes('so sánh') || nlsArith.includes('tia số')), 'Bài Toán 6 phải dùng MTCT tính toán/so sánh hoặc tia số');
console.log('  -> NLS Toán 6 chuẩn sư phạm (không nghiệm, không đồ thị): PASS');

// Test 3.4: Khi bài học có 2-3 mã năng lực số, mỗi mã phải có minh chứng tương ứng riêng biệt
const nls11 = vm.runInContext("lessonAppliedNlsDescription('1.1.TC1a', '', 'Bài 3. Thứ tự trong tập hợp các số tự nhiên')", sandbox);
const nls52 = vm.runInContext("lessonAppliedNlsDescription('5.2.TC1a', '', 'Bài 3. Thứ tự trong tập hợp các số tự nhiên')", sandbox);
assert(nls11 !== nlsArith, 'Mã 1.1 phải có mô tả khác mã 5.3');
assert(nls52 !== nlsArith, 'Mã 5.2 phải có mô tả khác mã 5.3');
assert(nls11.includes('học liệu số') || nls11.includes('tia số'), 'Mã 1.1 phải thể hiện khai thác học liệu số');
console.log('  -> Đa mã NLS phân hóa theo từng tiêu chí chuẩn: PASS');

// Test 3.5: Modal chi tiết bài học render đầy đủ các Badge mã NLS và minh chứng cho từng mã
const sampleLessonModal = {
  lesson_title: 'Bài 3. Thứ tự trong tập hợp các số tự nhiên',
  digital_candidates: '5.3.TC1a, 5.2.TC1a, 1.1.TC1a',
  digital_evidence: 'Sử dụng phần mềm vẽ đồ thị (GeoGebra/Desmos) và máy tính cầm tay để minh họa hình học, kiểm tra nghiệm của bài Thứ tự trong tập hợp các số tự nhiên.'
};
sandbox.sampleLessonModal = sampleLessonModal;
const renderedModalHtml = vm.runInContext("renderSgkDetailNlsBlock(sampleLessonModal)", sandbox);
assert(renderedModalHtml.includes('Mã NLS: 5.3.TC1a'), 'Modal phải có badge Mã NLS: 5.3.TC1a');
assert(renderedModalHtml.includes('Mã NLS: 5.2.TC1a'), 'Modal phải có badge Mã NLS: 5.2.TC1a');
assert(renderedModalHtml.includes('Mã NLS: 1.1.TC1a'), 'Modal phải có badge Mã NLS: 1.1.TC1a');
assert(!renderedModalHtml.includes('kiểm tra nghiệm'), 'Modal phải lọc bỏ nội dung không phù hợp "kiểm tra nghiệm"');
console.log('  -> Render khối NLS chi tiết với Badge và phân rã 2-3 mã: PASS');


// 4. Kiểm tra compactSgkText & độ bao phủ SGK
console.log('-> 4. Kiểm tra compactSgkText & độ bao phủ SGK...');
const sampleLines = [];
sampleLines.push('Mục lục');
for (let i = 1; i <= 40; i++) {
  sampleLines.push(`Chương ${Math.ceil(i / 8)}: Chủ đề toán học`);
  sampleLines.push(`Bài ${i}. Tên bài học toán học số ${i}`);
  sampleLines.push(`Mục tiêu bài ${i}: Yêu cầu cần đạt chuẩn`);
  sampleLines.push(`Hoạt động khởi động bài ${i}`);
  sampleLines.push(`Khám phá kiến thức bài ${i}`);
  sampleLines.push(`Luyện tập vận dụng bài ${i} với máy tính cầm tay và GeoGebra`);
  sampleLines.push(`Bài tập cuối chương cho bài ${i}`);
  sampleLines.push(`Trang ${i * 5}`);
}
sandbox.sampleText = sampleLines.join('\n');
const compacted = vm.runInContext("compactSgkText(sampleText)", sandbox);
const compactedLines = compacted.split('\n');
assert(compactedLines.length > 220, `compactSgkText phải giữ được trên 220 dòng khi sách dài (thực tế: ${compactedLines.length} dòng)`);
assert(compacted.includes('Bài 40.'), 'compactSgkText phải giữ được bài cuối cùng (Bài 40)');
console.log(`  -> compactSgkText giữ được ${compactedLines.length} dòng, bao phủ đến bài 40: PASS`);

// 5. Kiểm tra ensureFullCurriculumLessons (Curriculum Assurance bù đủ 100% bài học)
console.log('-> 5. Kiểm tra ensureFullCurriculumLessons (Curriculum Assurance)...');
const sample9Lessons = [
  { lesson_order: 1, lesson_title: 'Bài 1. Tập hợp các số hữu tỉ' },
  { lesson_order: 2, lesson_title: 'Bài 2. Cộng, trừ, nhân, chia số hữu tỉ' },
  { lesson_order: 3, lesson_title: 'Bài 3. Luỹ thừa với số mũ tự nhiên của một số hữu tỉ' },
  { lesson_order: 4, lesson_title: 'Bài 4. Thứ tự thực hiện các phép tính. Quy tắc chuyển vế' },
  { lesson_order: 5, lesson_title: 'Hoạt động thực hành trải nghiệm' },
  { lesson_order: 6, lesson_title: 'Bài tập cuối chương I' },
  { lesson_order: 7, lesson_title: 'Bài 6. Số vô tỉ. Căn bậc hai số học' },
  { lesson_order: 8, lesson_title: 'Bài 7. Tập hợp các số thực' },
  { lesson_order: 9, lesson_title: 'Bài tập cuối chương II' }
];
sandbox.sample9Lessons = sample9Lessons;
const fullToan7 = vm.runInContext("ensureFullCurriculumLessons(sample9Lessons, 'Toán học', '7', 'Sách giáo khoa dùng chung (từ 2026-2027)')", sandbox);
assert(fullToan7.length >= 35, `ensureFullCurriculumLessons phải bù đắp đủ toàn bộ năm học (thực tế: ${fullToan7.length} bài)`);
assert.equal(fullToan7[0].lesson_order, 1, 'Bài đầu tiên phải có order = 1');
assert.equal(fullToan7[fullToan7.length - 1].lesson_order, fullToan7.length, `Bài cuối cùng phải có order = ${fullToan7.length}`);
assert(fullToan7.every(l => l.lesson_order && l.lesson_title && l.digital_evidence && l.ai_pedagogy_hint), 'Mỗi bài học bù đắp phải có đủ STT, tên bài, minh chứng NLS và gợi ý AI');
assert(fullToan7.every(l => !l.digital_evidence.includes('lịch sử ra đời')), 'NLS bù đắp không được chứa chatbot lịch sử');
console.log(`  -> ensureFullCurriculumLessons bù đắp từ 9 bài lên đủ 100% (${fullToan7.length} bài) cho Toán 7: PASS`);

// Kiểm tra seed danh mục chuẩn từ mảng rỗng: BẮT BUỘC ĐỦ 43 BÀI TOÁN 6
const seedToan6 = vm.runInContext("ensureFullCurriculumLessons([], 'Toán học', '6', 'Sách giáo khoa dùng chung (từ 2026-2027)')", sandbox);
assert.equal(seedToan6.length, 43, `Seed Toán 6 phải có ĐÚNG 43 bài (thực tế: ${seedToan6.length} bài)`);
assert.equal(seedToan6[0].lesson_order, 1, 'Bài đầu tiên phải là Bài 1');
assert.equal(seedToan6[2].lesson_order, 3, 'Bài thứ ba phải là Bài 3');
assert(seedToan6[2].lesson_title.includes('Bài 3.'), 'Bài 3 phải là Thứ tự trong tập hợp các số tự nhiên');
assert.equal(seedToan6[42].lesson_order, 43, 'Bài cuối cùng phải là Bài 43');
assert(seedToan6[42].lesson_title.includes('Bài 43.'), 'Bài 43 phải là Xác suất thực nghiệm');
console.log(`  -> Khởi tạo chuẩn 100% bài học Toán 6 (ĐỦ 43/43 bài, có Bài 3 và Bài 43): PASS`);

// Kiểm tra trường hợp AI chỉ nhận diện được 25 bài và nhảy cóc mất Bài 3
const aiTruncated25 = [];
for (let i = 1; i <= 25; i++) {
  if (i === 3) continue; // Giả lập AI bỏ sót Bài 3
  aiTruncated25.push({
    lesson_order: aiTruncated25.length + 1,
    lesson_title: `Bài ${i}. Tên bài ${i} từ SGK`,
    page_start: i * 4,
    page_end: i * 4 + 3,
    yccd: `YCCD chi tiết từ sách cho bài ${i}`
  });
}
sandbox.aiTruncated25 = aiTruncated25;
const compensatedToan6 = vm.runInContext("ensureFullCurriculumLessons(aiTruncated25, 'Toán học', '6', 'Sách giáo khoa dùng chung (từ 2026-2027)')", sandbox);
assert.equal(compensatedToan6.length, 43, `Sau khi bù đắp, Toán 6 phải đủ 43 bài (thực tế: ${compensatedToan6.length} bài)`);
assert(compensatedToan6[2].lesson_title.includes('Bài 3.'), 'Bài 3 bị mất phải được tự động bù đắp vào vị trí thứ 3');
assert.equal(compensatedToan6[2].lesson_order, 3, 'Bài 3 phải có order = 3');
assert.equal(compensatedToan6[0].page_start, 4, 'Trang sách do AI trích xuất của bài 1 phải được giữ nguyên');
assert.equal(compensatedToan6[24].page_start, 100, 'Trang sách do AI trích xuất của bài 25 phải được giữ nguyên');
assert(compensatedToan6[25].lesson_title.includes('Bài 26.'), 'Bài 26 bị thiếu do AI dừng sớm phải được bù đắp chuẩn');
console.log(`  -> Bù đắp an toàn 100% khi AI nhận diện thiếu bài (tự khôi phục Bài 3 và bù đủ 43 bài): PASS`);

// 6. Kiểm tra tính đa dạng của mã NLS theo 6 phân môn (chống template hóa đối phó)
console.log('-> 6. Kiểm tra tính đa dạng sư phạm của mã NLS theo 6 phân môn...');
// 6.1: Nhánh tính toán số học (arith_practice) có mã 5.1.TC1a (sự cố kỹ thuật MTCT)
const candArithPractice = vm.runInContext("recommendLessonDigitalCandidates('Bài 4. Phép cộng và phép trừ số tự nhiên', 6, 'Toán học')", sandbox);
assert(candArithPractice.includes('5.1.TC1a'), `Nhánh tính toán số học phải có mã 5.1.TC1a (thực tế: ${candArithPractice})`);
assert(candArithPractice.includes('5.3.TC1a'), `Nhánh tính toán số học phải có mã 5.3.TC1a (thực tế: ${candArithPractice})`);

// 6.2: Nhánh hình học trực quan (geometry) có mã 3.1 và 1.1 (vẽ hình GeoGebra, mô hình 3D)
const candGeometry = vm.runInContext("recommendLessonDigitalCandidates('Bài 18. Hình tam giác đều. Hình vuông. Hình lục giác đều', 6, 'Toán học')", sandbox);
assert(candGeometry.includes('3.1.TC1a') && candGeometry.includes('1.1.TC1a'), `Nhánh hình học phải có mã 3.1 và 1.1 (thực tế: ${candGeometry})`);

// 6.3: Nhánh thống kê - xác suất (statistics) có mã 3.1 và 1.2 (bảng tính Excel, đánh giá dữ liệu)
const candStat = vm.runInContext("recommendLessonDigitalCandidates('Bài 38. Dữ liệu và thu thập dữ liệu', 6, 'Toán học')", sandbox);
assert(candStat.includes('1.2.TC1a') && (candStat.includes('3.1.TC1a') || candStat.includes('1.1.TC1a')), `Nhánh thống kê phải có mã 1.2 và 3.1 (thực tế: ${candStat})`);

// 6.4: Hoạt động thực hành trải nghiệm (experiential) có mã 2.2 (hợp tác số, chia sẻ dữ liệu)
const candExp = vm.runInContext("recommendLessonDigitalCandidates('Hoạt động thực hành trải nghiệm', 6, 'Toán học')", sandbox);
assert(candExp.includes('2.2.TC1a'), `Hoạt động trải nghiệm phải có mã hợp tác số 2.2.TC1a (thực tế: ${candExp})`);

// 6.5: Nhánh lý thuyết số học trừu tượng (arith_theory) có mã 1.1 và 4.3 (khai thác học liệu số, bảo vệ thị giác)
const candTheory = vm.runInContext("recommendLessonDigitalCandidates('Bài 1. Tập hợp', 6, 'Toán học')", sandbox);
assert(candTheory.includes('1.1.TC1a') && candTheory.includes('4.3.TC1a'), `Nhánh lý thuyết số học phải có 1.1 và 4.3 (thực tế: ${candTheory})`);

// 6.6: Nhánh phương trình/hệ phương trình THCS (equation) có mã bậc 2 (TC2a)
const candEq = vm.runInContext("recommendLessonDigitalCandidates('Bài 1. Phương trình bậc nhất hai ẩn', 9, 'Toán học')", sandbox);
assert(candEq.includes('5.3.TC2a') && candEq.includes('3.1.TC2a'), `Phương trình lớp 9 phải có mã 5.3.TC2a và 3.1.TC2a (thực tế: ${candEq})`);

// 6.7: Kiểm tra nội dung mô tả sư phạm của từng mã phân môn
const desc51 = vm.runInContext("lessonAppliedNlsDescription('5.1.TC1a', '', 'Bài 4. Phép cộng và phép trừ số tự nhiên')", sandbox);
assert(desc51.includes('sự cố') || desc51.includes('Math ERROR') || desc51.includes('máy tính cầm tay'), 'Mã 5.1 phải mô tả giải quyết sự cố kỹ thuật MTCT');

const desc12 = vm.runInContext("lessonAppliedNlsDescription('1.2.TC1a', '', 'Bài 38. Dữ liệu và thu thập dữ liệu')", sandbox);
assert(desc12.includes('đánh giá') || desc12.includes('độ tin cậy') || desc12.includes('dữ liệu'), 'Mã 1.2 phải mô tả đánh giá dữ liệu');

const desc22 = vm.runInContext("lessonAppliedNlsDescription('2.2.TC1a', '', 'Hoạt động thực hành trải nghiệm')", sandbox);
assert(sandbox.foldText(desc22).includes('hop tac') || sandbox.foldText(desc22).includes('chia se') || sandbox.foldText(desc22).includes('hoc tap so'), 'Mã 2.2 phải mô tả hợp tác số');

const desc43 = vm.runInContext("lessonAppliedNlsDescription('4.3.TC1a', '', 'Bài 1. Tập hợp')", sandbox);
assert(desc43.includes('thị giác') || desc43.includes('sức khỏe') || desc43.includes('an toàn'), 'Mã 4.3 phải mô tả bảo vệ thị giác/sức khỏe số');

console.log('  -> Đa dạng hóa 6 phân môn & mô tả sư phạm thực chất: PASS');

// 7. Kiểm tra Hệ thống Tri thức đa môn đa lớp (Toàn bộ 13 môn cấp THCS Lớp 6–9)
console.log('-> 7. Kiểm tra nạp Tri thức chuẩn đa môn, đa lớp (13 môn x 4 khối lớp)...');

// 7.1: Ngữ văn 6
const seedVan6 = vm.runInContext("ensureFullCurriculumLessons([], 'Ngữ văn', '6', 'Sách giáo khoa dùng chung (từ 2026-2027)')", sandbox);
assert(seedVan6.length >= 10, `Ngữ văn 6 phải sinh đủ danh mục bài học (thực tế: ${seedVan6.length} bài)`);
assert(seedVan6.every(l => l.lesson_title && l.yccd && l.digital_evidence && l.ai_pedagogy_hint), 'Bài Ngữ văn 6 phải có đủ YCCĐ, NLS, AI');
assert(seedVan6[0].yccd.includes('văn học') || seedVan6[0].yccd.includes('đọc hiểu') || seedVan6[0].yccd.includes('thể loại'), 'YCCĐ Ngữ văn phải đúng đặc thù bộ môn');

// 7.2: Khoa học tự nhiên 7
const seedKhtn7 = vm.runInContext("ensureFullCurriculumLessons([], 'Khoa học tự nhiên', '7', 'Sách giáo khoa dùng chung (từ 2026-2027)')", sandbox);
assert(seedKhtn7.length >= 40, `KHTN 7 phải sinh đủ danh mục bài học (thực tế: ${seedKhtn7.length} bài)`);
assert(seedKhtn7[0].yccd.includes('khoa học') || seedKhtn7[0].yccd.includes('thí nghiệm') || seedKhtn7[0].yccd.includes('khái niệm'), 'YCCĐ KHTN phải đúng đặc thù bộ môn');

// 7.3: Tin học 8
const seedTin8 = vm.runInContext("ensureFullCurriculumLessons([], 'Tin học', '8', 'Sách giáo khoa dùng chung (từ 2026-2027)')", sandbox);
assert(seedTin8.length >= 15, `Tin học 8 phải sinh đủ danh mục bài học (thực tế: ${seedTin8.length} bài)`);
assert(seedTin8[0].yccd.includes('công nghệ số') || seedTin8[0].yccd.includes('máy tính') || seedTin8[0].yccd.includes('thông tin'), 'YCCĐ Tin học phải đúng đặc thù bộ môn');

// 7.4: Lịch sử và Địa lí 9
const seedSuDia9 = vm.runInContext("ensureFullCurriculumLessons([], 'Lịch sử và Địa lí', '9', 'Sách giáo khoa dùng chung (từ 2026-2027)')", sandbox);
assert(seedSuDia9.length >= 40, `Lịch sử và Địa lí 9 phải sinh đủ danh mục bài học (thực tế: ${seedSuDia9.length} bài)`);
assert(seedSuDia9[0].yccd.includes('lịch sử') || seedSuDia9[0].yccd.includes('địa lí') || seedSuDia9[0].yccd.includes('tư liệu'), 'YCCĐ Sử Địa phải đúng đặc thù bộ môn');

// 7.5: Giáo dục địa phương (GDDP) cả 4 khối lớp
['6', '7', '8', '9'].forEach(g => {
  const seedGddp = vm.runInContext(`ensureFullCurriculumLessons([], 'Giáo dục địa phương', '${g}', 'Sách giáo khoa dùng chung (từ 2026-2027)')`, sandbox);
  assert.equal(seedGddp.length, 8, `GDDP lớp ${g} phải có đủ 8 chủ đề/bài học chuẩn`);
});

console.log('  -> Nạp tri thức chuẩn đa môn, đa khối lớp (Ngữ văn, KHTN, Tin học, Lịch sử - Địa lí, GD địa phương): PASS');

// ==================================================
// 8. KIỂM TRA PHÂN HÓA YCCĐ TOÁN 6, 7, 8, 9 (KHÔNG TRÙNG LẶP)
// ==================================================
console.log('-> 8. Kiểm tra tính phân hóa YCCĐ Toán 6-9 (đặc biệt Toán 9 Bài 1 và Bài 2 không trùng nhau)...');
['6', '7', '8', '9'].forEach(g => {
  const seedToan = vm.runInContext(`ensureFullCurriculumLessons([], 'Toán học', '${g}', 'Sách giáo khoa dùng chung (từ 2026-2027)')`, sandbox);
  assert(seedToan.length >= 30, `Toán ${g} phải có đủ danh mục bài học`);
  const seenYccd = new Set();
  seedToan.forEach((item, idx) => {
    assert(item.yccd && item.yccd.trim().length > 10, `Toán ${g} bài ${idx + 1} phải có YCCĐ`);
    assert(!seenYccd.has(item.yccd), `Toán ${g} bài ${idx + 1} (${item.lesson_title}) bị trùng YCCĐ!`);
    seenYccd.add(item.yccd);
  });
});
const toan9Lessons = vm.runInContext("ensureFullCurriculumLessons([], 'Toán học', '9', 'Sách giáo khoa dùng chung (từ 2026-2027)')", sandbox);
assert.notEqual(toan9Lessons[0].yccd, toan9Lessons[1].yccd, 'Toán 9 Bài 1 và Bài 2 không được có cùng YCCĐ!');
assert.notEqual(toan9Lessons[1].yccd, toan9Lessons[2].yccd, 'Toán 9 Bài 2 và Bài 3 không được có cùng YCCĐ!');
console.log('  -> 100% bài học Toán 6, 7, 8, 9 có YCCĐ riêng biệt, Toán 9 Bài 1 và Bài 2 hoàn toàn khác biệt: PASS');

// ==================================================
// 9. KIỂM TRA PHÂN HÓA NĂNG LỰC SỐ VÀ AI SƯ PHẠM TOÁN 9 (BÀI 1, 2, 3 HOÀN TOÀN KHÁC BIỆT)
// ==================================================
console.log('-> 9. Kiểm tra phân hóa sư phạm NLS và AI theo cấp độ nhận thức từng bài học Toán 9...');
const b1 = toan9Lessons[0];
const b2 = toan9Lessons[1];
const b3 = toan9Lessons[2];

// Mã NLS khác biệt
assert.notEqual(b1.digital_candidates, b2.digital_candidates, 'Bài 1 (Khái niệm) và Bài 2 (Giải hệ) phải có mã NLS khác nhau!');
assert.notEqual(b2.digital_candidates, b3.digital_candidates, 'Bài 2 (Giải hệ) và Bài 3 (Toán thực tế) phải có mã NLS khác nhau!');
assert(b1.digital_candidates.includes('1.1.TC2a') || b1.digital_candidates.includes('3.1.TC2a'), 'Bài 1 phải có mã nhận biết/khai thác học liệu số hoặc sơ đồ tư duy');
assert(b2.digital_candidates.includes('5.1.TC2a') || b2.digital_candidates.includes('5.2.TC2a'), 'Bài 2 phải có mã xử lý sự cố máy tính hoặc lựa chọn công cụ');
assert(b3.digital_candidates.includes('1.2.TC2a') || b3.digital_candidates.includes('3.1.TC2a'), 'Bài 3 phải có mã đánh giá dữ liệu hoặc bảng tính phân tích đại lượng');

// Minh chứng NLS khác biệt và chuẩn sư phạm
assert.notEqual(b1.digital_evidence, b2.digital_evidence, 'Bài 1 và Bài 2 phải có minh chứng NLS khác nhau!');
assert.notEqual(b2.digital_evidence, b3.digital_evidence, 'Bài 2 và Bài 3 phải có minh chứng NLS khác nhau!');
assert(!b1.digital_evidence.includes('các bước giải') && !b1.digital_evidence.includes('SIMULT'), 'Bài 1 mới nhận biết, không được chứa "các bước giải" hay SIMULT giải hệ');
assert(b1.digital_evidence.includes('kiểm tra') || b1.digital_evidence.includes('CALC'), 'Bài 1 phải dùng MTCT kiểm tra cặp số có là nghiệm');
assert(b2.digital_evidence.includes('EQUATION') || b2.digital_evidence.includes('SIMULT') || b2.digital_evidence.includes('giải phương trình') || b2.digital_evidence.includes('giải hệ'), 'Bài 2 phải có chức năng giải hệ trên MTCT');
assert(b3.digital_evidence.includes('bảng tính') || b3.digital_evidence.includes('thực tiễn') || b3.digital_evidence.includes('thực tế'), 'Bài 3 phải có bảng tính phân tích đại lượng hoặc kiểm tra điều kiện thực tiễn');

// Gợi ý AI khác biệt và chuẩn sư phạm
assert.notEqual(b1.ai_pedagogy_hint, b2.ai_pedagogy_hint, 'Bài 1 và Bài 2 phải có gợi ý AI khác biệt!');
assert.notEqual(b2.ai_pedagogy_hint, b3.ai_pedagogy_hint, 'Bài 2 và Bài 3 phải có gợi ý AI khác biệt!');
assert(b1.ai_pedagogy_hint.includes('nghiệm') && !b1.ai_pedagogy_hint.includes('các bước giải bài'), 'AI Bài 1 phải tập trung vào nhận biết nghiệm, không dập khuôn các bước giải');
assert(b2.ai_pedagogy_hint.includes('phương pháp thế') || b2.ai_pedagogy_hint.includes('cộng đại số') || b2.ai_pedagogy_hint.includes('tối ưu'), 'AI Bài 2 phải định hướng chọn phương pháp giải tối ưu');
assert(b3.ai_pedagogy_hint.includes('chọn ẩn') || b3.ai_pedagogy_hint.includes('đại lượng') || b3.ai_pedagogy_hint.includes('phản biện'), 'AI Bài 3 phải phản biện bước chọn ẩn và mô hình hóa đại lượng');

console.log('  -> Toán 9 Bài 1 (Khái niệm), Bài 2 (Giải hệ), Bài 3 (Toán thực tế) phân hóa 100% NLS và AI: PASS');

console.log('-> 10. Kiểm tra hỗ trợ Đa mã Năng lực AI (Multi-Code AI theo QĐ 2422)...');
const aiCandidatesB1 = sandbox.recommendLessonAiCandidates(b1.lesson_title, 9);
const aiCandidatesB2 = sandbox.recommendLessonAiCandidates(b2.lesson_title, 9);
const aiCandidatesB3 = sandbox.recommendLessonAiCandidates(b3.lesson_title, 9);
assert(Array.isArray(aiCandidatesB1) && aiCandidatesB1.length >= 2, 'Bài 1 phải có ít nhất 2 mã AI đề xuất');
assert(Array.isArray(aiCandidatesB2) && aiCandidatesB2.length >= 2, 'Bài 2 phải có ít nhất 2 mã AI đề xuất');
assert(Array.isArray(aiCandidatesB3) && aiCandidatesB3.length >= 2, 'Bài 3 phải có ít nhất 2 mã AI đề xuất');
assert(aiCandidatesB1.includes('9.B2.1') && aiCandidatesB1.includes('9.A3.2'), 'Bài 1 phải kết hợp Miền B (kiểm chứng định nghĩa) và Miền A (tạo ví dụ, tư duy logic)');
assert(aiCandidatesB2.includes('9.B2.1') && aiCandidatesB2.includes('9.A3.1'), 'Bài 2 phải kết hợp Miền B (phương pháp giải tối ưu) và Miền A (phản biện các bước giải)');
assert(aiCandidatesB3.includes('9.B2.1') && aiCandidatesB3.includes('9.D1.1'), 'Bài 3 phải kết hợp Miền B (chọn ẩn số) và Miền D (đánh giá mức độ tin cậy mô hình)');

// Kiểm tra fallbackAiCodes khi chọn mật độ 2-3 mã/bài
const multiAiCodes = sandbox.fallbackAiCodes(0, { lop: '9', ai: { density: '2-3' } }, b2.lesson_title, 2, [1, 2]);
assert.equal(multiAiCodes.length, 2, 'Khi mật độ 2-3 mã/bài, fallbackAiCodes phải sinh đủ 2 mã AI');
assert(multiAiCodes[0].text.includes('9.B2.1') && multiAiCodes[1].text.includes('9.A3.1'), 'Phải sinh đúng 2 mã AI phân hóa');

// Kiểm tra renderSgkDetailAiBlock trong modal chi tiết
const renderedAiHtml = sandbox.renderSgkDetailAiBlock(b1, 9);
assert(renderedAiHtml.includes('Trí tuệ nhân tạo (QĐ 2422):'), 'Phải render khối AI');
assert(renderedAiHtml.includes('Mã AI: 9.B2.1') && renderedAiHtml.includes('Mã AI: 9.A3.2'), 'Phải render cả 2 badge mã AI');
assert(renderedAiHtml.includes('[9.B2.1]') && renderedAiHtml.includes('[9.A3.2]'), 'Phải có mô tả hành động phân rã riêng cho từng mã');

console.log('  -> Hỗ trợ Đa mã AI (Multi-Code AI) theo khung QĐ 2422: PASS');

console.log('==================================================');
console.log('TẤT CẢ TEST KHO TRI THỨC SGK ĐỀU ĐẠT (PASS)!');
console.log('==================================================');


