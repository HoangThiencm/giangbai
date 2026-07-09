/**
 * Benchmark chuẩn solver hiện tại (thoikhoabieu-engine.js)
 *   node agent-tools/benchmark-tkb.js
 *   node agent-tools/benchmark-tkb.js --size small|medium|large
 */
const path = require('path');
const engine = require(path.join(__dirname, '..', 'thoikhoabieu-engine.js'));

function uid(p) { return p + '_' + Math.random().toString(36).slice(2, 9); }
function clean(v) { return String(v ?? '').trim(); }

function buildSmall() {
  const teachers = [
    { id: 't1', name: 'GV Toán', subject: 'Toán', maxPeriods: 32, unavailable: '', preferredRooms: '' },
    { id: 't2', name: 'GV Văn', subject: 'Ngữ văn', maxPeriods: 32, unavailable: '', preferredRooms: '' },
    { id: 't3', name: 'GV Anh', subject: 'Ngoại ngữ 1', maxPeriods: 28, unavailable: '', preferredRooms: '' },
    { id: 't4', name: 'GV KHTN', subject: 'Khoa học tự nhiên', maxPeriods: 28, unavailable: '', preferredRooms: '' },
    { id: 't5', name: 'GV TD', subject: 'Giáo dục thể chất', maxPeriods: 24, unavailable: '', preferredRooms: '' },
    { id: 't6', name: 'GV Tin', subject: 'Tin học', maxPeriods: 20, unavailable: '', preferredRooms: '' },
  ];
  const classes = ['6A', '6B', '7A', '7B'].map(name => ({ id: uid('c'), name, shift: 'morning', homeRoom: name }));
  const rooms = [
    { id: 'r1', name: 'Tin 1', subjects: 'Tin học' },
    { id: 'r2', name: 'KHTN 1', subjects: 'Khoa học tự nhiên' },
    { id: 'r3', name: 'Sân 1', subjects: 'Giáo dục thể chất, Thể dục' },
  ];
  const cur = engine.curriculumCt2018(6);
  const bySub = {};
  teachers.forEach(t => {
    const k = t.subject.toLowerCase();
    if (!bySub[k]) bySub[k] = [];
    bySub[k].push(t);
  });
  const assignments = [];
  classes.forEach((cl, ci) => {
    cur.forEach(row => {
      const pool = bySub[row.subject.toLowerCase()] || teachers;
      const te = pool[ci % pool.length];
      assignments.push({
        id: uid('a'), classId: cl.id, teacherId: te.id,
        subject: row.subject, periods: row.periods, roomNeed: row.roomNeed || '', note: '',
      });
    });
  });
  return {
    label: 'small-4class-ct2018',
    teachers, classes, rooms, assignments,
    rules: engine.normalizeRules({ packFromSessionStart: true }),
  };
}

function buildLarge(nClass) {
  // 16 or 30 classes, ratio ~1.9 teachers
  const grades = [];
  if (nClass === 16) {
    for (const g of [6, 7, 8, 9]) for (let i = 0; i < 4; i++) grades.push({ g, name: `${g}${String.fromCharCode(65 + i)}` });
  } else {
    for (const g of [6, 7]) for (let i = 0; i < 8; i++) grades.push({ g, name: `${g}${String.fromCharCode(65 + i)}` });
    for (const g of [8, 9]) for (let i = 0; i < 7; i++) grades.push({ g, name: `${g}${String.fromCharCode(65 + i)}` });
  }
  // Đủ GV để 1,9–2,2 GV/lớp + dư địa concurrent (tránh nghẽn tổ môn)
  const teacherPlan = [
    ['Toán', Math.max(6, Math.ceil(nClass / 4)), 24],
    ['Ngữ văn', Math.max(6, Math.ceil(nClass / 4)), 24],
    ['Ngoại ngữ 1', Math.max(5, Math.ceil(nClass / 5)), 24],
    ['Giáo dục công dân', Math.max(2, Math.ceil(nClass / 12)), 22],
    ['Lịch sử', Math.max(3, Math.ceil(nClass / 8)), 22],
    ['Địa lí', Math.max(3, Math.ceil(nClass / 8)), 22],
    ['Khoa học tự nhiên', Math.max(5, Math.ceil(nClass / 5)), 24],
    ['Vật lí', Math.max(3, Math.ceil(nClass / 10)), 22],
    ['Hóa học', Math.max(3, Math.ceil(nClass / 10)), 22],
    ['Sinh học', Math.max(3, Math.ceil(nClass / 10)), 22],
    ['Công nghệ', Math.max(2, Math.ceil(nClass / 12)), 22],
    ['Tin học', Math.max(3, Math.ceil(nClass / 10)), 22],
    ['Giáo dục thể chất', Math.max(5, Math.ceil(nClass / 5)), 24],
    ['Âm nhạc', Math.max(2, Math.ceil(nClass / 12)), 20],
    ['Mỹ thuật', Math.max(2, Math.ceil(nClass / 12)), 20],
    ['HĐTN-HN', Math.max(3, Math.ceil(nClass / 8)), 24],
    ['Sinh hoạt', Math.max(4, Math.ceil(nClass / 6)), 22],
  ];
  const teachers = [];
  teacherPlan.forEach(([subject, count, max]) => {
    for (let i = 1; i <= count; i++) {
      teachers.push({ id: uid('t'), name: `GV ${subject} ${i}`, subject, maxPeriods: max, unavailable: '', preferredRooms: '' });
    }
  });
  const classes = grades.map(({ name }) => ({ id: uid('c'), name, shift: 'morning', homeRoom: name }));
  const rooms = [
    ['Tin 1', 'Tin học'], ['Tin 2', 'Tin học'],
    ['KHTN 1', 'Khoa học tự nhiên, Vật lí, Hóa học, Sinh học'],
    ['KHTN 2', 'Khoa học tự nhiên, Vật lí, Hóa học, Sinh học'],
    ['KHTN 3', 'Khoa học tự nhiên'],
    ['Lý 1', 'Vật lí'], ['Lý 2', 'Vật lí'],
    ['Hóa 1', 'Hóa học'], ['Hóa 2', 'Hóa học'],
    ['Sinh 1', 'Sinh học'], ['Sinh 2', 'Sinh học'],
    ['CN 1', 'Công nghệ'], ['CN 2', 'Công nghệ'],
    ['Sân 1', 'Giáo dục thể chất, Thể dục'], ['Sân 2', 'Giáo dục thể chất, Thể dục'], ['Sân 3', 'Giáo dục thể chất, Thể dục'],
  ].map(([name, subjects]) => ({ id: uid('r'), name, subjects }));

  const bySub = {};
  teachers.forEach(t => {
    const k = t.subject.toLowerCase();
    if (!bySub[k]) bySub[k] = [];
    bySub[k].push(t);
  });
  const assignments = [];
  classes.forEach((cl, ci) => {
    const g = engine.classGrade(cl.name);
    engine.curriculumCt2018(g).forEach(row => {
      const pool = bySub[row.subject.toLowerCase()] || [];
      if (!pool.length) return;
      // pick least load
      let best = pool[0];
      let bestL = Infinity;
      pool.forEach(t => {
        const load = assignments.filter(a => a.teacherId === t.id).reduce((s, a) => s + a.periods, 0);
        if (load < bestL) { bestL = load; best = t; }
      });
      assignments.push({
        id: uid('a'), classId: cl.id, teacherId: best.id,
        subject: row.subject, periods: row.periods, roomNeed: row.roomNeed || '', note: '',
      });
    });
  });
  return {
    label: `ct2018-${nClass}class-${teachers.length}gv`,
    teachers, classes, rooms, assignments,
    rules: engine.normalizeRules({ packFromSessionStart: true }),
  };
}

function runOne(snap) {
  const t0 = Date.now();
  const periods = snap.assignments.reduce((s, a) => s + a.periods, 0);
  console.log(`\n=== ${snap.label} ===`);
  console.log(`GV ${snap.teachers.length} | Lớp ${snap.classes.length} | PC ${snap.assignments.length} | Tiết ${periods}`);
  const r = engine.solveSnapshot(snap);
  const ms = Date.now() - t0;
  console.log(`Hard: ${r.ok ? 'PASS 100%' : 'FAIL'} ${r.placed}/${r.total} | status=${r.status}`);
  if (r.precheckIssues?.length) {
    console.log('Precheck:', r.precheckIssues.length);
    r.precheckIssues.slice(0, 5).forEach(i => console.log(' -', i.message));
  }
  if (r.audit) {
    console.log(`Soft: holes=${r.audit.classHoles} startLate=${r.audit.startLate} orphans=${r.audit.teacherOrphans} tGaps=${r.audit.teacherGaps}`);
  }
  console.log(`nodes=${r.nodes} beauty=${r.beauty?.score} time=${(ms / 1000).toFixed(2)}s`);
  return { ...r, ms, label: snap.label };
}

const arg = process.argv.find(a => a.startsWith('--size='))?.split('=')[1]
  || (process.argv.includes('--size') ? process.argv[process.argv.indexOf('--size') + 1] : 'small');

const results = [];
if (arg === 'small' || arg === 'all') results.push(runOne(buildSmall()));
if (arg === 'medium' || arg === 'all') results.push(runOne(buildLarge(16)));
if (arg === 'large' || arg === 'all') results.push(runOne(buildLarge(30)));
if (!['small', 'medium', 'large', 'all'].includes(arg)) {
  console.log('Usage: node agent-tools/benchmark-tkb.js --size small|medium|large|all');
  process.exit(2);
}

console.log('\n=== SUMMARY ===');
results.forEach(r => {
  console.log(`${r.label}: hard=${r.ok ? 'OK' : 'NO'} ${r.placed}/${r.total} softHoles=${r.audit?.classHoles ?? '-'} ${(r.ms / 1000).toFixed(1)}s`);
});
process.exit(results.every(r => r.ok) ? 0 : 1);
