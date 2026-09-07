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
  'btnUseCurBook'
];

const requiredFunctions = [
  'onBookSeriesChange',
  'checkSharedSgkKnowledge',
  'syncSharedSgkToApp',
  'extractAndSaveSharedSgk',
  'openSgkLibraryModal',
  'closeSgkLibraryModal',
  'fetchAndRenderSgkLibrary',
  'renderFilteredSgkLibrary',
  'openSgkDetailModal',
  'closeSgkDetailModal',
  'useCurrentDetailBook',
  'useSharedSgkBook',
  'getSharedSgkLessonKnowledge'
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
  console.log(`  -> ${path}: Đầy đủ 100% IDs và hàm JS: PASS`);
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
  loadedSharedSgkKnowledge: null
};

vm.createContext(sandbox);

// Load getSharedSgkLessonKnowledge, lessonAppliedNlsDescription, lessonAppliedAiDescription, appendixOneFallbackOutcome
const codeToRun = [
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

console.log('==================================================');
console.log('TẤT CẢ TEST KHO TRI THỨC SGK ĐỀU ĐẠT (PASS)!');
console.log('==================================================');
