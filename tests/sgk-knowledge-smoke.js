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
  'sgkJsonFileInput'
];

const requiredFunctions = [
  'onBookSeriesChange',
  'checkSharedSgkKnowledge',
  'syncSharedSgkToApp',
  'ensureFullCurriculumLessons',
  'seedStandardSgkKnowledge',
  'extractAndSaveSharedSgk',
  'openSgkLibraryModal',
  'closeSgkLibraryModal',
  'fetchAndRenderSgkLibrary',
  'renderFilteredSgkLibrary',
  'openSgkDetailModal',
  'closeSgkDetailModal',
  'useCurrentDetailBook',
  'useSharedSgkBook',
  'getSharedSgkLessonKnowledge',
  'exportSgkKnowledgeJson',
  'importSgkKnowledgeJson'
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
  }
};

vm.createContext(sandbox);

// Load KHBD_YCCD from js/khbd-yccd.js
const yccdCode = fs.readFileSync('js/khbd-yccd.js', 'utf8');
vm.runInContext(yccdCode, sandbox);

// Load compactSgkText, ensureFullCurriculumLessons, getSharedSgkLessonKnowledge, lessonAppliedNlsDescription, lessonAppliedAiDescription, appendixOneFallbackOutcome
const codeToRun = [
  extractFn('compactSgkText', sourceCode),
  extractFn('ensureFullCurriculumLessons', sourceCode),
  extractFn('getSharedSgkLessonKnowledge', sourceCode),
  extractFn('lessonAppliedNlsDescription', sourceCode),
  extractFn('lessonAppliedAiDescription', sourceCode),
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

// Kiểm tra seed danh mục chuẩn từ mảng rỗng
const seedToan6 = vm.runInContext("ensureFullCurriculumLessons([], 'Toán học', '6', 'Sách giáo khoa dùng chung (từ 2026-2027)')", sandbox);
assert(seedToan6.length >= 40, `Seed Toán 6 phải có ít nhất 40 bài (thực tế: ${seedToan6.length} bài)`);
console.log(`  -> Khởi tạo chuẩn 100% bài học Toán 6 (${seedToan6.length} bài): PASS`);

console.log('==================================================');
console.log('TẤT CẢ TEST KHO TRI THỨC SGK ĐỀU ĐẠT (PASS)!');
console.log('==================================================');
