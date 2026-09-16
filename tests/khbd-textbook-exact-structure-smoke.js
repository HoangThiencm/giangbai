/** Smoke: trích xuất SGK nguyên văn theo schema + khóa đề mục/đề bài Hoạt động B/C/D. Node 18+. */
'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const appSrc = fs.readFileSync(path.join(root, 'js', 'khbd-app.js'), 'utf8');
const {
  canvasTextbookAnalysisPrompt,
  parseCanvasTextbookAnalysis,
  formatCanvasTextbookContext
} = require('../js/khbd-app.js');
const {
  getPromptTemplate,
  extractTextbookSubsections,
  extractTextbookLessonMap
} = require('../js/khbd-prompts.js');

console.log('================================================================================');
console.log('KIỂM THỬ TRÍCH XUẤT SGK NGUYÊN VĂN VÀ KHÓA ĐỀ BÀI HOẠT ĐỘNG B/C/D');
console.log('================================================================================');

console.log('\n[TEST 1] Prompt phân tích SGK dùng schema fact-extraction nguyên văn...');
const prompt = canvasTextbookAnalysisPrompt('PDF SGK, trang 1');
assert.match(prompt, /fact extraction/, 'Phải trích xuất từng trường ngắn');
assert.match(prompt, /không chép nguyên trang/, 'Không chép nguyên trang (tránh RECITATION)');
assert.match(prompt, /nguyên văn 100%/, 'Phải giữ nguyên văn tên đề mục và đề bài');
assert.match(prompt, /"sections"/, 'Schema phải có sections');
assert.match(prompt, /"coreKnowledge"/, 'Schema phải có coreKnowledge');
assert.match(prompt, /"activities"/, 'Schema phải có activities');
assert.match(prompt, /"exercises"/, 'Schema phải có exercises');
assert.match(prompt, /Bài 1\.36/, 'Schema mẫu phải có mã bài tập');
assert.match(prompt, /CẤM diễn đạt lại/, 'Cấm diễn đạt lại đề mục/đề bài');
assert.match(prompt, /TUYỆT ĐỐI KHÔNG ĐƯỢC TỰ Ý ĐÁNH SỐ THÊM/, 'Cấm tự đánh số đề mục khi SGK không có số');
assert.match(prompt, /TUYỆT ĐỐI KHÔNG điền chỗ trống bằng trí nhớ/, 'Cấm điền SGK theo trí nhớ');
assert.doesNotMatch(prompt, /Chỉ diễn đạt lại bằng lời của bạn/, 'Không còn lệnh diễn đạt lại toàn trang');
console.log('✓ Prompt schema sections/exercises, nguyên văn, không chép nguyên trang.');

console.log('\n[TEST 2] parse + format giữ nguyên văn đề mục, HĐ và bài tập...');
const sampleJson = JSON.stringify({
  subject: 'Toán',
  grade: '6',
  topic: 'Tập hợp',
  periodCount: 2,
  sections: [
    {
      index: '1',
      title: 'Khái niệm tập hợp',
      coreKnowledge: 'Tập hợp là một nhóm đối tượng được xác định rõ.',
      activities: [
        { label: 'HĐ 1', task: 'Quan sát các hình và cho biết đâu là tập hợp.' },
        { label: 'Luyện tập 1', task: 'Cho $A = \\{1; 2; 3\\}$. Viết các phần tử của $A$.' },
        { label: 'Vận dụng 1', task: 'Nêu một tập hợp các môn học em đang học.' }
      ]
    },
    {
      index: '2',
      title: 'Phần tử của tập hợp',
      coreKnowledge: 'Nếu $a$ thuộc $A$ thì viết $a \\in A$.',
      activities: [
        { label: 'HĐ 2', task: 'Xác định phần tử thuộc tập hợp đã cho.' }
      ]
    }
  ],
  exercises: [
    { code: 'Bài 1.36', statement: 'Cho $A = \\{0; 1; 2\\}$. Tìm số phần tử của $A$.' },
    { code: 'Bài 1.37', statement: 'Viết tập hợp các số tự nhiên nhỏ hơn 5.' }
  ],
  unknowns: []
});
const parsed = parseCanvasTextbookAnalysis(sampleJson);
assert.strictEqual(parsed.sections.length, 2);
assert.strictEqual(parsed.sections[0].title, 'Khái niệm tập hợp');
assert.strictEqual(parsed.sections[0].activities[0].label, 'HĐ 1');
assert.strictEqual(parsed.sections[0].activities[0].task, 'Quan sát các hình và cho biết đâu là tập hợp.');
assert.strictEqual(parsed.exercises[0].code, 'Bài 1.36');
assert.ok(parsed.exercises[0].statement.includes('A = \\{0; 1; 2\\}'));
assert.ok(parsed.subsections.some(item => item.title === 'Khái niệm tập hợp'), 'Phải suy tiểu mục từ sections');

const formatted = formatCanvasTextbookContext(parsed);
assert.match(formatted, /### Khái niệm tập hợp/);
assert.match(formatted, /### Phần tử của tập hợp/);
assert.match(formatted, /- Đề mục: Khái niệm tập hợp/);
assert.doesNotMatch(formatted, /### 1\. Khái niệm tập hợp/, 'Không tự thêm số vào đề mục không có số');
assert.doesNotMatch(formatted, /Mục 1:/, 'Không chèn nhãn Mục N');
assert.match(formatted, /HĐ 1: Quan sát các hình và cho biết đâu là tập hợp\./);
assert.match(formatted, /Luyện tập 1: Cho \$A =/);
assert.match(formatted, /Bài 1\.36: Cho \$A =/);
assert.match(formatted, /## Luyện tập \/ Bài tập/);
assert.match(formatted, /## Vận dụng/);
assert.match(formatted, /Vận dụng 1: Nêu một tập hợp các môn học em đang học\./);

const subsections = extractTextbookSubsections(formatted);
assert.ok(subsections.some(item => item.title === 'Khái niệm tập hợp'), 'Heading đề mục phải trích được cho Hoạt động B');
assert.ok(subsections.some(item => item.title === 'Phần tử của tập hợp'));
const lessonMap = extractTextbookLessonMap(formatted);
assert.match(lessonMap.practice, /Bài 1\.36/);
assert.match(lessonMap.application, /Vận dụng 1/);
console.log('✓ JSON → ngữ cảnh giữ nguyên văn; extractTextbookSubsections/LessonMap đọc được.');

console.log('\n[TEST 3] GENERATE_ACTIVITY_B/C/D khóa tên đề mục và đề bài nguyên văn...');
const ctx = {
  subjectName: 'Toán',
  grade: '6',
  duration: '02 tiết (90 phút)',
  topic: 'Tập hợp',
  textbook_content: formatted
};
const promptB = getPromptTemplate('GENERATE_ACTIVITY_B', ctx);
assert.match(promptB, /KHÓA TÊN ĐỀ MỤC NGUYÊN VĂN 100%/);
assert.match(promptB, /không diễn đạt lại, không đổi từ, không rút gọn/);
assert.match(promptB, /Hoạt động 2\.1: Khái niệm tập hợp/);
assert.match(promptB, /Hoạt động 2\.2: Phần tử của tập hợp/);

const promptC = getPromptTemplate('GENERATE_ACTIVITY_C', ctx);
assert.match(promptC, /KHÓA ĐỀ BÀI NGUYÊN VĂN 100%/);
assert.match(promptC, /CẤM đổi số liệu/);
assert.match(promptC, /CẤM tự tạo đề bài lạ ngoài sách/);
assert.match(promptC, /Bài 1\.36/);

const promptD = getPromptTemplate('GENERATE_ACTIVITY_D', ctx);
assert.match(promptD, /ƯU TIÊN ĐỀ BÀI VẬN DỤNG NGUYÊN VĂN 100%/);
assert.match(promptD, /Vận dụng 1: Nêu một tập hợp các môn học em đang học\./);
console.log('✓ Prompt B/C/D khóa nguyên văn tên đề mục và đề bài SGK.');

console.log('\n[TEST 4] Cache-bust JS mới trên Canvas/soankhbd...');
assert.match(appSrc, /finishReason=RECITATION/, 'Vẫn hướng dẫn khi RECITATION, không tự gửi lại');
['canvas_soankhbd.html', path.join('backupcode viettailieu', 'canvas_soankhbd.html')].forEach(rel => {
  const html = fs.readFileSync(path.join(root, rel), 'utf8');
  assert.match(html, /textbook-exact-v12/, `${rel} phải cache-bust textbook-exact-v12`);
});
console.log('✓ Cache-bust textbook-exact-v12; RECITATION vẫn được bắt.');

console.log('\n[TEST 5] Giữ đúng chỉ số SGK, không tự đánh số, không lặp số...');
const numbered = parseCanvasTextbookAnalysis(JSON.stringify({
  sections: [
    { title: '1. Lũy thừa với số mũ tự nhiên', coreKnowledge: '', activities: [] },
    { title: 'I. Khái niệm', coreKnowledge: '', activities: [] },
    { title: 'Khái niệm lũy thừa', coreKnowledge: '', activities: [] }
  ],
  exercises: []
}));
assert.strictEqual(numbered.sections[0].title, '1. Lũy thừa với số mũ tự nhiên');
assert.strictEqual(numbered.sections[1].title, 'I. Khái niệm');
assert.strictEqual(numbered.sections[2].title, 'Khái niệm lũy thừa');
assert.ok(!('index' in numbered.sections[0]), 'Không ép index vào section');
const numberedCtx = formatCanvasTextbookContext(numbered);
assert.match(numberedCtx, /### 1\. Lũy thừa với số mũ tự nhiên/);
assert.doesNotMatch(numberedCtx, /1\. 1\. Lũy thừa/, 'Không lặp số đúp 1. 1.');
assert.match(numberedCtx, /### I\. Khái niệm/);
assert.doesNotMatch(numberedCtx, /### 1\. I\. Khái niệm/, 'Không đổi I. thành 1. I.');
assert.match(numberedCtx, /### Khái niệm lũy thừa/);
assert.doesNotMatch(numberedCtx, /### \d+\.\s*Khái niệm lũy thừa/, 'Không tự đánh số đề mục không có số');

const fromNumbered = extractTextbookSubsections(numberedCtx);
assert.ok(fromNumbered.some(item => item.title === '1. Lũy thừa với số mũ tự nhiên'));
assert.ok(fromNumbered.some(item => item.title === 'I. Khái niệm'));
assert.ok(fromNumbered.some(item => item.title === 'Khái niệm lũy thừa'));

const promptNumbered = getPromptTemplate('GENERATE_ACTIVITY_B', {
  subjectName: 'Toán', grade: '6', duration: '02 tiết (90 phút)', topic: 'Lũy thừa',
  textbook_content: numberedCtx
});
assert.match(promptNumbered, /### Hoạt động 2\.1: 1\. Lũy thừa với số mũ tự nhiên/);
assert.doesNotMatch(promptNumbered, /Hoạt động 2\.1: 1\. 1\./);
console.log('✓ 1. / I. giữ nguyên; đề mục không số không bị tự đánh số.');

console.log('\n================================================================================');
console.log('TẤT CẢ KIỂM THỬ TRÍCH XUẤT SGK NGUYÊN VĂN ĐÃ PASS 100%!');
console.log('================================================================================');
