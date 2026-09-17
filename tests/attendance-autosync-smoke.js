const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(path.join(__dirname, '../phancongtochuyenmon.html'), 'utf8');
function declaration(name) { const start = html.lastIndexOf(`function ${name}(`); assert(start >= 0, name); const next = html.indexOf('\n        function ', start + 1); return html.slice(start, next < 0 ? html.length : next); }
assert.equal((html.match(/function renderBaoGiangView\(/g) || []).length, 1, 'Chỉ còn một hàm renderBaoGiangView');
assert.match(html, /id="att-db-status"/);
assert.match(html, /onclick="autoSyncSubstitutePeriods\(\)"/);
const syncContext = vm.createContext({
  state: { teachers: [{id:'a'}, {id:'b'}], attendance: { records: {m_9:{}}, substitutes: {m_9:[
    {teacher_id:'a', type:'replacement', period_count:3},
    {teacher_id:'a', type:'makeup', periods_detail:[{},{}]},
    {teacher_id:'b', type:'replacement', period_count:1}
  ]} } },
  getSubPeriodCount: item => Array.isArray(item.periods_detail) && item.periods_detail.length ? item.periods_detail.length : item.period_count || 1,
  getMonthKey: () => 'm_9', saveToLocal: () => {}, scheduleAutoSave: () => {}, renderAttendance: () => {}, showToast: () => {}
});
vm.runInContext(declaration('autoSyncSubstitutePeriods'), syncContext);
vm.runInContext("autoSyncSubstitutePeriods({silent:true,mKey:'m_9',autoSave:false,refresh:false})", syncContext);
assert.equal(syncContext.state.attendance.records.m_9.a.teach_replace, 3);
assert.equal(syncContext.state.attendance.records.m_9.a.makeup_periods, 2);
assert.equal(syncContext.state.attendance.records.m_9.b.teach_replace, 1);
let saved = 0;
const fillContext = vm.createContext({
  state: {teachers:[{id:'a'}], attendance:{records:{m_9:{a:{teach_replace:3,makeup_periods:2}}}, substitutes:{m_9:[]}}},
  getMonthKey: () => 'm_9', autoSyncSubstitutePeriods: () => {}, saveToLocal: () => {}, renderAttendance: () => {}, saveAttendanceToDB: () => {saved++}, showToast: () => {}
});
vm.runInContext(declaration('autoFillAttendance'), fillContext);
vm.runInContext('autoFillAttendance()', fillContext);
assert.equal(fillContext.state.attendance.records.m_9.a.teach_replace, 3);
assert.equal(fillContext.state.attendance.records.m_9.a.makeup_periods, 2);
assert.equal(saved, 1);
console.log('PASS: đồng bộ Chấm công, bảo toàn dạy thay/bù và lưu CSDL.');