const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(path.join(__dirname, '../phancongtochuyenmon.html'), 'utf8');
function declaration(name) { const start = html.lastIndexOf(`function ${name}(`); assert(start >= 0, name); const next = html.indexOf('\n        function ', start + 1); return html.slice(start, next < 0 ? html.length : next); }
const source = ['baoGiangDate','baoGiangIso','baoGiangMonthRange','baoGiangMonthTable','renderBaoGiangCalendarByDay','renderBaoGiangWeekGrid'].map(declaration).join('\n');
const context = vm.createContext({Date, String, Number, Array, Map, escapeHtml: value => String(value), baoGiangWeekdayLabel: () => 'Thứ Hai', formatVnDate: value => value});
vm.runInContext(source, context);
assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext("baoGiangMonthRange('2026-02')", context))), {start:'2026-02-01',end:'2026-02-28',month:'2026-02'});
const rows = [{date:'2026-09-07',session:'morning',period:1,class_name:'9A1',subject:'Toán',teacher_id:'gv-a',lesson:{ppct:'1',lesson:'Bài 1',segment:'1/1'}}];
assert.match(vm.runInContext('renderBaoGiangCalendarByDay(' + JSON.stringify(rows) + ')', context), /Buổi sáng/);
assert.match(vm.runInContext('renderBaoGiangWeekGrid(' + JSON.stringify(rows) + ')', context), /9A1/);
assert.match(html, /id="bg-filter-teacher"/);
assert.match(html, /id="bg-filter-month"/);
assert.match(html, /id="bg-view-mode"/);
assert.match(html, /function exportBaoGiangMonth\(/);
console.log('PASS: lọc GV, phạm vi tháng, lịch theo ngày và lưới tuần.');