/**
 * Kiểm tra pack + audit lủng/mồ côi trên demo nhỏ (solver thật từ thoikhoabieu.html)
 */
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'thoikhoabieu.html'), 'utf8');
const start = html.indexOf('<script>');
const end = html.lastIndexOf('</script>');
let src = html.slice(start + 8, end);
if (src.includes('function bindEvents')) src = src.slice(0, src.indexOf('function bindEvents'));

const stubs = `
const document = {
  getElementById(id) {
    if (!this._els) this._els = {};
    if (!this._els[id]) {
      this._els[id] = {
        id, value: '', innerHTML: '', textContent: '', disabled: false, checked: true,
        classList: { add(){}, remove(){}, toggle(){}, contains(){ return false; } },
        style: {}, dataset: {}, addEventListener(){}, querySelectorAll(){ return []; },
        querySelector(){ return null; },
        closest(){ return null; },
        parentElement: null,
      };
    }
    const defaults = {
      morningPeriods: '5', afternoonPeriods: '4', morningFrom: '1', morningTo: '5',
      afternoonFrom: '1', afternoonTo: '4', schoolDays: 'T2,T3,T4,T5,T6,T7',
      maxSameSubjectDay: '2', blockedSlots: '', packFromSessionStart: true,
    };
    if (defaults[id] != null) {
      if (id === 'packFromSessionStart') this._els[id].checked = true;
      else this._els[id].value = defaults[id];
    }
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

const api = new Function('console', stubs + '\n' + src + `
; return {
  state, loadSampleData, solveByConstraints, buildLessonUnits, buildBaseDomains,
  precheckSchedule, auditScheduleQuality, packConstraintAllows, readRulesFromInputs,
  effectiveSessionStart, gapCountInSession
};`)(console);

api.loadSampleData();
api.readRulesFromInputs();
api.state.rules.packFromSessionStart = true;

// Unit: pack + blocked mid
api.state.rules.blockedSlots = 'T2S3';
const lesson = { classId: 'c1' };
const allows = api.packConstraintAllows(
  lesson,
  { day: 'T2', session: 'morning', period: 4 },
  [
    { day: 'T2', session: 'morning', period: 1 },
    { day: 'T2', session: 'morning', period: 2 },
  ],
  [lesson, lesson, lesson]
);
console.log('pack with T2S3 blocked, placing 4 after 1,2:', allows ? 'OK allow' : 'FAIL block');
api.state.rules.blockedSlots = '';

const lessons = api.buildLessonUnits();
const domains = api.buildBaseDomains(lessons);
const pre = api.precheckSchedule(lessons, domains);
console.log('Demo nhỏ: lessons', lessons.length, 'precheck', pre.length);
if (pre.length) pre.forEach(p => console.log(' PRE', p.message));

const t0 = Date.now();
const solved = api.solveByConstraints(lessons, domains);
const ms = Date.now() - t0;
const placed = (solved.assignments || []).filter(Boolean).length;
const audit = api.auditScheduleQuality(lessons, solved.assignments || []);

console.log('--- KẾT QUẢ ---');
console.log('OK solver:', solved.ok, '| placed', placed + '/' + lessons.length);
console.log('time', (ms / 1000).toFixed(2) + 's');
console.log('classHoles', audit.classHoles, '| startLate', audit.startLate);
console.log('teacherOrphans', audit.teacherOrphans, '| teacherGaps', audit.teacherGaps);
console.log('beauty gaps class/teacher', solved.beauty?.classGaps, solved.beauty?.teacherGaps);
if (audit.messages.length) {
  console.log('--- Chi tiết (tối đa 15) ---');
  audit.messages.slice(0, 15).forEach(m => console.log(m.severity, m.message));
}

const failHard = audit.classHoles > 0 || audit.startLate > 0 || !solved.ok || placed < lessons.length;
process.exit(failHard ? 1 : 0);
