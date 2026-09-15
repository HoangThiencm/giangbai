'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

console.log('================================================================');
console.log('KIỂM THỬ: ĐỊNH MỨC PPDH/KTDH THEO SỐ TIẾT & XUỐNG DÒNG GV/HS');
console.log('================================================================');

const root = path.join(__dirname, '..');
const app = require(path.join(root, 'js/khbd-app.js'));
const appCode = fs.readFileSync(path.join(root, 'js/khbd-app.js'), 'utf8');
const docxCode = fs.readFileSync(path.join(root, 'js/khbd-docx.js'), 'utf8');
const promptsCode = fs.readFileSync(path.join(root, 'js/khbd-prompts.js'), 'utf8');

// --- 1. Time-budget gate: 1 tiết ---
console.log('\n[1] Bài 1 tiết: tối đa 1 PPDH, 1–2 KTDH nhẹ, không kỹ thuật nặng');
app.appState.duration = '01 tiết (45 phút)';
app.appState.selectedGrade = '6';
const gated1 = app.applyTimeBudgetGateToPedagogy({
  methods: ['pbl', 'cooperative', 'inquiry'],
  techniques: {
    A: ['kwl-tech', 'jigsaw'],
    B: ['jigsaw-tech', 'tablecloth', 'tps-tech', 'station'],
    C: ['station', 'gallery-tech'],
    D: ['mini-project', 'pbl']
  }
}, 1);
assert.ok(gated1.methods.length <= 1, `1 tiết: PPDH <= 1, nhận ${gated1.methods.length}`);
assert.ok(!gated1.methods.includes('pbl'), '1 tiết: không PPDH dự án');
assert.strictEqual(gated1.techniques.B.length, 1, '1 tiết: pha B đúng 1 kỹ thuật');
assert.ok(['tps-tech', 'tablecloth', '5w1h'].includes(gated1.techniques.B[0]), '1 tiết: pha B phải kỹ thuật nhẹ');
const total1 = ['A', 'B', 'C', 'D'].reduce((n, p) => n + (gated1.techniques[p] || []).length, 0);
assert.ok(total1 <= 2, `1 tiết: tổng KTDH <= 2, nhận ${total1}`);
assert.ok(!(gated1.techniques.C || []).some(id => /jigsaw|station|gallery|mini-project|pbl|steam/.test(String(id))), '1 tiết: không kỹ thuật nặng pha C');
assert.deepStrictEqual(gated1.techniques.A, [], '1 tiết: pha A không đề xuất KTDH (dùng vấn đáp tự nhiên)');
assert.deepStrictEqual(gated1.techniques.C, [], '1 tiết: pha C không đề xuất KTDH nặng/thêm');
assert.deepStrictEqual(gated1.techniques.D, [], '1 tiết: pha D không đề xuất KTDH nặng/thêm');
const gatedAct = app.applyTimeBudgetGateToPedagogy({
  methods: ['cooperative'],
  techniques: { A: ['5w1h'], B: ['tps-tech'], C: ['station'], D: [] },
  activities: ['station-act', 'station', 'experiment', 'product']
}, 1);
assert.ok(!(gatedAct.activities || []).includes('station'), '1 tiết: không Station trong HĐ đặc thù');
assert.ok(!(gatedAct.activities || []).includes('station-act'), '1 tiết: không Trạm xoay vòng (station-act)');
assert.ok(!(gatedAct.activities || []).includes('product'), '1 tiết: không sản phẩm/dự án mini');
assert.ok((gatedAct.activities || []).length <= 1, '1 tiết: tối đa 1 HĐ đặc thù');
assert.deepStrictEqual(gatedAct.techniques.A, [], '1 tiết: không giữ 5W1H ở pha A cùng TPS pha B');
assert.deepStrictEqual(gatedAct.techniques.C, [], '1 tiết: không giữ Station ở pha C');
assert.ok(!(gatedAct.activities || []).some(id => /station|product/.test(String(id))), '1 tiết: HĐ đặc thù phải lọc hết kỹ thuật nặng');
console.log('✓ Gate 1 tiết đạt.');

// --- 2. Time-budget gate: 2 tiết ---
console.log('\n[2] Bài 2 tiết: tối đa 2 PPDH, 2–3 KTDH');
const gated2 = app.applyTimeBudgetGateToPedagogy({
  methods: ['inquiry', 'cooperative', 'pbl', 'steam'],
  techniques: {
    A: ['kwl-tech', 'mindmap'],
    B: ['tablecloth', 'jigsaw'],
    C: ['station'],
    D: ['exit-ticket', 'mini-project']
  }
}, 2);
assert.ok(gated2.methods.length <= 2, `2 tiết: PPDH <= 2, nhận ${gated2.methods.length}`);
const total2 = ['A', 'B', 'C', 'D'].reduce((n, p) => n + (gated2.techniques[p] || []).length, 0);
assert.ok(total2 <= 3, `2 tiết: tổng KTDH <= 3, nhận ${total2}`);
console.log('✓ Gate 2 tiết đạt.');

// --- 3. formatKhbdRoleLineBreaks ---
console.log('\n[3] Xuống dòng phân vai GV/HS');
assert.ok(typeof app.formatKhbdRoleLineBreaks === 'function', 'Phải export formatKhbdRoleLineBreaks');
const sticky = '+ Bước 1: Chuyển giao nhiệm vụ: (Kỹ thuật TPS) GV: "Mở SGK trang 12." HS: Quan sát hình và ghi chú.';
const fixed = app.formatKhbdRoleLineBreaks(sticky);
assert.ok(fixed.includes('<br>- **GV:**'), 'Phải chèn <br>- **GV:**');
assert.ok(fixed.includes('<br>- **HS:**'), 'Phải chèn <br>- **HS:**');
assert.ok(!/GV:\s*[^*"][\s\S]{0,40}HS:/.test(fixed.replace(/<br>/g, '\n')) || fixed.includes('<br>- **HS:**'), 'GV và HS không còn dính liền');
const already = '+ Bước 2:<br>- **GV:** "Quan sát."<br>- **HS:** Thảo luận.';
const stable = app.formatKhbdRoleLineBreaks(already);
assert.ok(stable.includes('- **GV:**') && stable.includes('- **HS:**'), 'Giữ format đã chuẩn');
assert.strictEqual(app.formatKhbdRoleLineBreaks(stable), stable, 'Format đã chuẩn phải idempotent, không nhân đôi <br>');
const piped = '+ Bước 1 (Chuyển giao): GV: "Mở SGK." | HS: Quan sát hình.';
const pipedFixed = app.formatKhbdRoleLineBreaks(piped);
assert.ok(pipedFixed.includes('<br>- **GV:**'), 'Tách GV sau dấu |');
assert.ok(pipedFixed.includes('<br>- **HS:**'), 'Tách HS sau dấu |');
const tableRow = '| + Bước 1: Giao việc GV: "Mở SGK trang 12." HS: Quan sát hình. | Định nghĩa tập hợp |';
const tableFixed = app.formatKhbdRoleLineBreaks(tableRow);
assert.ok(tableFixed.includes('<br>- **GV:**'), 'Trong ô bảng phải tách GV');
assert.ok(tableFixed.includes('<br>- **HS:**'), 'Trong ô bảng phải tách HS');
assert.ok(tableFixed.startsWith('|'), 'Không phá hàng bảng Markdown');
const tableLines = tableFixed.replace(/<br>/g, '\n').split('\n');
assert.ok(tableLines.some(line => /\*\*GV:\*\*/.test(line) && !/\*\*HS:\*\*/.test(line)), 'GV phải tách riêng dòng trong bảng');
assert.ok(tableLines.some(line => /\*\*HS:\*\*/.test(line) && !/\*\*GV:\*\*/.test(line)), 'HS phải tách riêng dòng trong bảng');
console.log('✓ formatKhbdRoleLineBreaks đạt.');

// --- 4. applyActivityOutput pipeline gọi formatKhbdRoleLineBreaks ---
console.log('\n[4] Pipeline applyActivityOutput');
assert.match(appCode, /finalResult = formatKhbdRoleLineBreaks\(finalResult\)/, 'applyActivityOutput phải gọi formatKhbdRoleLineBreaks');
assert.match(appCode, /function formatKhbdRoleLineBreaks/, 'Phải định nghĩa formatKhbdRoleLineBreaks');
assert.match(appCode, /periodsCount/, 'applyTimeBudgetGateToPedagogy phải nhận periodsCount');
console.log('✓ Pipeline đạt.');

// --- 5. DOCX parseTableCellParagraphs ---
console.log('\n[5] DOCX tách đoạn GV/HS');
assert.match(docxCode, /\*\*GV:\*\*/, 'docx phải chuẩn hóa **GV:**');
assert.match(docxCode, /\*\*HS:\*\*/, 'docx phải chuẩn hóa **HS:**');
assert.match(docxCode, /isRoleLine|roleMatch/, 'docx phải nhận diện dòng vai trò');
console.log('✓ DOCX đạt.');

// --- 6. Prompt contract ---
console.log('\n[6] Prompt Cột TRÁI + TIME-BUDGET');
assert.match(promptsCode, /TUYỆT ĐỐI CẤM viết dính liền GV và HS/, 'Prompt cấm dính liền GV/HS');
assert.match(promptsCode, /<br>- \*\*GV:\*\*/, 'Prompt yêu cầu <br>- **GV:**');
assert.match(promptsCode, /<br>- \*\*HS:\*\*/, 'Prompt yêu cầu <br>- **HS:**');
assert.match(promptsCode, /TIME-BUDGET GATE/, 'Prompt có TIME-BUDGET GATE');
assert.match(promptsCode, /Bài 1 tiết/, 'Prompt có quy tắc bài 1 tiết');
console.log('✓ Prompt đạt.');

console.log('\n================================================================');
console.log('🎉 TẤT CẢ KIỂM THỬ PEDAGOGY-RATE ĐÃ PASS 100%!');
console.log('================================================================\n');
