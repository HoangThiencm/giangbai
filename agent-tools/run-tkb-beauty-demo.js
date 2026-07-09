/**
 * Chạy solver thật từ thoikhoabieu.html trên demo 16 lớp,
 * đo % xếp + chỉ số đẹp (gap, tiết đôi, quality).
 */
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'thoikhoabieu.html'), 'utf8');
const start = html.indexOf('<script>');
const end = html.lastIndexOf('</script>');
let src = html.slice(start + 8, end);

// Cắt phần bind DOM / init trang — giữ logic + loadSampleData16
src = src
  .replace(/async function initTimetablePage[\s\S]*?\n\s*initTimetablePage\(\);\s*/, '')
  .replace(/function bindEvents\(\)[\s\S]*?\n\s*\}\n\n\s*async function initTimetablePage/, 'async function initTimetablePage')
  .replace(/async function initTimetablePage[\s\S]*$/, '');

// Bỏ các handler còn sót nếu regex không khớp hoàn hảo
if (src.includes('initTimetablePage')) {
  src = src.replace(/async function initTimetablePage[\s\S]*$/, '');
}
if (src.includes('function bindEvents')) {
  const i = src.indexOf('function bindEvents');
  src = src.slice(0, i);
}

const stubs = `
const document = {
  getElementById(id) {
    if (!this._els) this._els = {};
    if (!this._els[id]) {
      this._els[id] = {
        id,
        value: '',
        innerHTML: '',
        textContent: '',
        disabled: false,
        classList: { add(){}, remove(){}, toggle(){}, contains(){ return false; } },
        style: {},
        dataset: {},
        addEventListener(){},
        querySelectorAll(){ return []; },
        closest(){ return null; },
      };
    }
    // defaults for rule inputs
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

const sandbox = { console, setTimeout, clearTimeout, Date, Math, JSON, Array, Object, Map, Set, Number, String, Boolean, Error, parseInt, parseFloat, isNaN, Infinity };
const fn = new Function('console', stubs + '\n' + src + '\n; return { state, loadSampleData16, generateSchedule, buildLessonUnits, buildBaseDomains, precheckSchedule, solveByConstraints, evaluateBeauty, readRulesFromInputs };');
const api = fn(console);

const t0 = Date.now();
api.loadSampleData16();
api.readRulesFromInputs();
const lessons = api.buildLessonUnits();
const domains = api.buildBaseDomains(lessons);
const pre = api.precheckSchedule(lessons, domains);
console.log('=== DEMO 16 lớp beauty ===');
console.log('Lớp', api.state.classes.length, '| GV', api.state.teachers.length, '| PC', api.state.assignments.length);
console.log('Tiết', lessons.length, '| Precheck issues', pre.length);
if (pre.length) {
  pre.forEach(p => console.log(' -', p.message));
  process.exit(2);
}

const solved = api.solveByConstraints(lessons, domains);
const placed = solved.assignments.filter(Boolean).length;
const beauty = solved.beauty || api.evaluateBeauty(lessons, solved.assignments);
const ms = Date.now() - t0;

// validate hard
let violations = 0;
const classMap = {}, teacherMap = {}, roomMap = {}, subj = {};
solved.assignments.forEach((opt, i) => {
  if (!opt) return;
  const les = lessons[i];
  const ck = `${les.classId}|${opt.day}|${opt.session}|${opt.period}`;
  const tk = `${les.teacherId}|${opt.day}|${opt.session}|${opt.period}`;
  const rk = `${opt.room}|${opt.day}|${opt.session}|${opt.period}`;
  const sk = `${les.classId}|${les.subject}|${opt.day}`;
  if (classMap[ck] || teacherMap[tk] || roomMap[rk]) violations++;
  classMap[ck] = teacherMap[tk] = roomMap[rk] = true;
  subj[sk] = (subj[sk] || 0) + 1;
});
Object.values(subj).forEach(c => { if (c > 2) violations++; });

console.log('OK 100%:', solved.ok ? 'YES' : 'NO');
console.log('Đã xếp:', placed + '/' + lessons.length, `(${(placed * 100 / lessons.length).toFixed(1)}%)`);
console.log('Nodes:', solved.nodes, '| deepest:', solved.deepest);
console.log('Hard violations:', violations);
console.log('Beauty score:', beauty.score);
console.log('Quality:', beauty.quality);
console.log('Gap lớp:', beauty.classGaps, '| Gap GV:', beauty.teacherGaps);
console.log('Tiết đôi tốt:', beauty.goodDoubles, '| Tách đôi:', beauty.brokenDoubles);
console.log('Beautify moves:', beauty.beautifyMoves);
console.log('Thời gian:', (ms / 1000).toFixed(2) + 's');
process.exit(solved.ok && violations === 0 ? 0 : 1);
