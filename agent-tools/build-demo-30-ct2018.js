/**
 * Sinh dữ liệu demo 30 lớp CT GDPT 2018 + chạy kiểm tra.
 * Ghi: data/tkb-demo-30lop-ct2018.json
 * Chạy: node agent-tools/build-demo-30-ct2018.js
 */
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'thoikhoabieu.html'), 'utf8');
const start = html.indexOf('<script>');
const end = html.lastIndexOf('</script>');
let src = html.slice(start + 8, end);
if (src.includes('function bindEvents')) {
  src = src.slice(0, src.indexOf('function bindEvents'));
}

const stubs = `
const document = {
  getElementById(id) {
    if (!this._els) this._els = {};
    if (!this._els[id]) {
      this._els[id] = {
        id, value: '', innerHTML: '', textContent: '', disabled: false,
        classList: { add(){}, remove(){}, toggle(){}, contains(){ return false; } },
        style: {}, dataset: {}, addEventListener(){}, querySelectorAll(){ return []; },
      };
    }
    if (id === 'morningPeriods') this._els[id].value = '5';
    if (id === 'afternoonPeriods') this._els[id].value = '4';
    if (id === 'schoolDays') this._els[id].value = 'T2,T3,T4,T5,T6,T7';
    if (id === 'maxSameSubjectDay') this._els[id].value = '2';
    return this._els[id];
  },
  querySelectorAll() { return []; },
  querySelector() { return null; },
};
const window = { setTimeout(fn) { return fn(); }, print(){}, XLSX: null };
const localStorage = { getItem() { return null; }, setItem(){} };
const alert = () => {};
const fetch = async () => ({ ok: false, json: async () => ({}) });
const URL = { createObjectURL() { return ''; }, revokeObjectURL(){} };
const Blob = function(){};
`;

const fn = new Function('console', stubs + '\n' + src + '\n; return { state, loadSampleData30, buildDiagnosticsReport, curriculumCt2018, classGrade, slotsForClass, projectPayload, readRulesFromInputs };');
const api = fn(console);

api.loadSampleData30();
api.readRulesFromInputs();
const report = api.buildDiagnosticsReport();

const teacherLoad = {};
api.state.assignments.forEach(a => {
  teacherLoad[a.teacherId] = (teacherLoad[a.teacherId] || 0) + Number(a.periods || 0);
});
const classLoad = {};
api.state.assignments.forEach(a => {
  classLoad[a.classId] = (classLoad[a.classId] || 0) + Number(a.periods || 0);
});

const payload = {
  meta: {
    title: 'Demo TKB 30 lớp THCS — CT GDPT 2018',
    curriculum: 'CT GDPT 2018 (THCS), tiết/tuần ≈ tiết/năm ÷ 35',
    notes: [
      'Tin học: 35 tiết/năm ≈ 1 tiết/tuần',
      'Lịch sử và Địa lí: 105 tiết/năm ≈ 3 tiết/tuần (tách Sử + Địa theo khối)',
      'KHTN: 140 tiết/năm ≈ 4 tiết/tuần (lớp 6–7 gộp; 8–9 tách Vật lí / Hóa / Sinh)',
      'Ngữ văn 4, Toán 4, Ngoại ngữ 1: 3, GDCD 1, CN 1, GDTC 2, Nghệ thuật 2 (AN+MT), HĐTN-HN 2, SH 1',
      '30 lớp = 8(K6)+8(K7)+7(K8)+7(K9); 57 GV = 30×1,9',
      'Tổng ~28 tiết/lớp/tuần (gần khung 29–29,5; chưa môn tự chọn)',
    ],
    generatedAt: new Date().toISOString(),
    diagnostics: {
      errors: report.errors.length,
      warnings: report.warnings.length,
      ok: report.summary.ok,
      errorMessages: report.errors.map(e => e.message),
      warningMessages: report.warnings.map(w => w.message),
    },
    counts: report.summary,
  },
  rules: api.state.rules,
  curriculumByGrade: {
    6: api.curriculumCt2018(6),
    7: api.curriculumCt2018(7),
    8: api.curriculumCt2018(8),
    9: api.curriculumCt2018(9),
  },
  teachers: api.state.teachers.map(t => ({
    id: t.id,
    name: t.name,
    subject: t.subject,
    maxPeriods: t.maxPeriods,
    unavailable: t.unavailable,
    assignedPeriods: teacherLoad[t.id] || 0,
  })),
  classes: api.state.classes.map(c => ({
    id: c.id,
    name: c.name,
    grade: api.classGrade(c.name),
    shift: c.shift,
    homeRoom: c.homeRoom,
    assignedPeriods: classLoad[c.id] || 0,
    capacity: api.slotsForClass(c).length,
  })),
  rooms: api.state.rooms.map(r => ({ id: r.id, name: r.name, subjects: r.subjects })),
  assignments: api.state.assignments.map(a => {
    const cl = api.state.classes.find(c => c.id === a.classId);
    const te = api.state.teachers.find(t => t.id === a.teacherId);
    return {
      className: cl?.name,
      grade: api.classGrade(cl?.name),
      subject: a.subject,
      periods: a.periods,
      teacherName: te?.name,
      roomNeed: a.roomNeed || '',
      note: a.note || '',
    };
  }),
  teacherLoadTable: report.teacherRows,
  classLoadTable: report.classRows,
  periodsBySubject: report.bySubject,
};

const outDir = path.join(__dirname, '..', 'data');
fs.mkdirSync(outDir, { recursive: true });
const outFile = path.join(outDir, 'tkb-demo-30lop-ct2018.json');
fs.writeFileSync(outFile, JSON.stringify(payload, null, 2), 'utf8');

console.log('=== DEMO 30 LỚP CT2018 ===');
console.log('Lớp', payload.meta.counts.classes, '| GV', payload.meta.counts.teachers, '| Tỷ lệ', payload.meta.counts.ratio);
console.log('Phòng', payload.meta.counts.rooms, '| PC', payload.meta.counts.assignments, '| Tiết', payload.meta.counts.totalPeriods);
console.log('Lỗi', report.errors.length, '| Cảnh báo', report.warnings.length, '| OK', report.summary.ok);
if (report.errors.length) report.errors.slice(0, 15).forEach(e => console.log(' E:', e.message));
if (report.warnings.length) report.warnings.slice(0, 15).forEach(w => console.log(' W:', w.message));
console.log('Curriculum K6 periods', payload.curriculumByGrade[6].reduce((s, x) => s + x.periods, 0));
console.log('Curriculum K8 periods', payload.curriculumByGrade[8].reduce((s, x) => s + x.periods, 0));
console.log('Tin học periods total', payload.periodsBySubject['Tin học'] || 0, '(expect 30 = 30 lớp × 1)');
console.log('Wrote', outFile);
process.exit(report.summary.ok ? 0 : 1);
