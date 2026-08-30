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

const {
  collapseDottedLines,
  stripExcessiveDottedLines,
  sanitizeLessonMarkdown
} = require('../js/khbd-app.js');
const { DocxGenerator } = require('../js/khbd-docx.js');
const { getPromptTemplate } = require('../js/khbd-prompts.js');

console.log('==================================================');
console.log('BẮT ĐẦU KIỂM THỬ RÚT GỌN DÒNG CHẤM PHỤ LỤC F');
console.log('==================================================');

const dottedRe = /^\s*[.\-_…\s]{10,}\s*$/;
const fiftyDots = Array(50).fill('........................................').join('\n');

console.log('-> 1. collapseDottedLines rút 50 dòng chấm về 1 dòng...');
const collapsed = collapseDottedLines(fiftyDots);
const collapsedCount = collapsed.split(/\r?\n/).filter(line => dottedRe.test(line)).length;
assert.strictEqual(collapsedCount, 1, '50 dòng chấm phải rút gọn còn 1 dòng');
assert.strictEqual(stripExcessiveDottedLines(fiftyDots).split(/\r?\n/).filter(line => dottedRe.test(line)).length, 1);
console.log('  -> collapseDottedLines: PASS');

console.log('-> 2. Bộ lọc Word không phình thành nhiều đoạn văn...');
const generator = new DocxGenerator();
assert.strictEqual(typeof generator.collapseDottedLines, 'function');
const wordCollapsed = generator.collapseDottedLines(fiftyDots);
assert.strictEqual(wordCollapsed.split(/\r?\n/).filter(line => dottedRe.test(line)).length, 1, 'Word collapseDottedLines phải giữ 1 dòng');
const elements = generator.parseMarkdownToDocxElements(fiftyDots);
assert.ok(elements.length <= 2, `50 dòng chấm không được nở thành nhiều Paragraph (got ${elements.length})`);
console.log('  -> parseMarkdownToDocxElements: PASS');

console.log('-> 3. Không lọc nhầm dòng điền Họ và tên hoặc ô bảng...');
const labeled = `**HỌ VÀ TÊN: .....................................................................................**
**LỚP: .............. NHÓM: ..............................**

| Nhiệm vụ | Nội dung câu hỏi / Bài tập | Chỗ HS điền kết quả |
| :--- | :--- | :--- |
| **Nhiệm vụ 1** | Câu hỏi bám SGK | ................................ |
| **Nhiệm vụ 2** | Câu hỏi bám SGK | ................................ |

........................................
........................................
........................................
........................................`;
const labeledOut = sanitizeLessonMarkdown(labeled);
assert.ok(labeledOut.includes('HỌ VÀ TÊN:'), 'Giữ dòng Họ và tên');
assert.ok(labeledOut.includes('| **Nhiệm vụ 1** |'), 'Giữ hàng bảng');
assert.ok((labeledOut.match(/Chỗ HS điền kết quả/g) || []).length === 1, 'Không nuốt bảng');
const leftoverDots = labeledOut.split(/\r?\n/).filter(line => dottedRe.test(line.trim()));
assert.strictEqual(leftoverDots.length, 1, 'Khối 4 dòng chấm ngoài bảng phải còn 1 dòng');
const twoDots = '....................\n....................';
assert.strictEqual(collapseDottedLines(twoDots).split(/\r?\n/).length, 2, '2 dòng chấm không bị rút (cần từ 3 dòng)');
console.log('  -> Không lọc nhầm mẫu in ngắn: PASS');

console.log('-> 4. Prompt Phụ lục F cấm khối dòng chấm rác...');
const promptF = getPromptTemplate('GENERATE_PORTFOLIO_WORKSHEETS', {
  subjectName: 'Toán',
  topic: 'Tập hợp',
  duration: '02 tiết (90 phút)',
  objectives_content: '',
  activities_content: '',
  textbook_content: ''
});
assert.match(promptF, /CẤM DÒNG CHẤM RÁC/i);
assert.match(promptF, /1–2 trang in Word/i);
assert.match(promptF, /nằm gọn trong ô của BẢNG/i);
console.log('  -> GENERATE_PORTFOLIO_WORKSHEETS: PASS');

console.log('==================================================');
console.log('TẤT CẢ TEST DÒNG CHẤM ĐỀU ĐẠT (PASS)!');
console.log('==================================================');
