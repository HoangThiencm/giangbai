/**
 * Tách pure solver từ thoikhoabieu.html → thoikhoabieu-engine.js + worker
 */
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'thoikhoabieu.html'), 'utf8');
const a = html.indexOf('<script>') + 8;
const b = html.lastIndexOf('</script>');
const src = html.slice(a, b);

function sliceFn(src, startMarker, endMarker) {
  const i = src.indexOf(startMarker);
  const j = src.indexOf(endMarker);
  if (i < 0 || j < 0 || j <= i) throw new Error('slice fail ' + startMarker);
  return src.slice(i, j);
}

// Helpers thuần
const helpers = `
  const clean = value => String(value ?? '').trim();
  const normalizeText = value => clean(value).toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').replace(/đ/g, 'd');
  const splitList = value => clean(value).split(/[,\\n;]+/).map(v => v.trim()).filter(Boolean);
  const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
`;

// Core pure: parseUnavailable → marker TKB_ENGINE_END (trước freeze/Worker/DOM)
const endMarker = '// === TKB_ENGINE_END ===';
let core;
if (src.includes(endMarker)) {
  core = sliceFn(src, 'function parseUnavailable', endMarker);
} else {
  // fallback: cắt trước generateSchedule (cũ) — tránh nếu quên marker
  console.warn('WARN: missing TKB_ENGINE_END marker, fallback to generateSchedule');
  core = sliceFn(src, 'function parseUnavailable', 'async function generateSchedule');
}

// curriculum helpers (đặt sau ENGINE_END trong HTML)
let curriculum = '';
const cStart = src.indexOf('function curriculumCt2018');
const cEnd = src.indexOf('function loadSampleData');
if (cStart > 0 && cEnd > cStart) {
  curriculum = src.slice(cStart, cEnd);
}

// Dedent common 8 spaces from HTML indent
function dedent(code) {
  return code.replace(/^[ ]{8}/gm, '  ');
}

const engine = `/**
 * thoikhoabieu-engine.js — pure solver (no DOM)
 * Sinh bởi agent-tools/extract-tkb-engine.js — chạy lại khi sửa solver trong HTML.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.TkbEngine = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const state = {
    teachers: [],
    classes: [],
    rooms: [],
    assignments: [],
    rules: {
      morningPeriods: 5, afternoonPeriods: 4,
      morningFrom: 1, morningTo: 5, afternoonFrom: 1, afternoonTo: 4,
      packFromSessionStart: true, blockedSlots: '',
      days: ['T2', 'T3', 'T4', 'T5', 'T6', 'T7'], maxSameSubjectDay: 2,
    },
    _packSoftMode: true,
  };

  function normalizeRules(rules) {
    rules = rules || {};
    const morningFrom = Math.max(1, Number(rules.morningFrom ?? 1));
    const morningTo = Math.max(morningFrom, Number(rules.morningTo ?? rules.morningPeriods ?? 5));
    const afternoonFrom = Math.max(1, Number(rules.afternoonFrom ?? 1));
    const afternoonTo = Math.max(afternoonFrom, Number(rules.afternoonTo ?? rules.afternoonPeriods ?? 4));
    return {
      morningFrom, morningTo, afternoonFrom, afternoonTo,
      morningPeriods: morningTo - morningFrom + 1,
      afternoonPeriods: afternoonTo - afternoonFrom + 1,
      packFromSessionStart: rules.packFromSessionStart !== false && rules.packFromSessionStart !== 0 && rules.packFromSessionStart !== '0',
      blockedSlots: String(rules.blockedSlots ?? '').trim(),
      days: Array.isArray(rules.days) ? rules.days : ['T2', 'T3', 'T4', 'T5', 'T6', 'T7'],
      maxSameSubjectDay: Math.max(1, Number(rules.maxSameSubjectDay ?? 2)),
    };
  }

  function setSnapshot(snap) {
    state.teachers = Array.isArray(snap.teachers) ? snap.teachers : [];
    state.classes = Array.isArray(snap.classes) ? snap.classes : [];
    state.rooms = Array.isArray(snap.rooms) ? snap.rooms : [];
    state.assignments = Array.isArray(snap.assignments) ? snap.assignments : [];
    state.rules = normalizeRules(snap.rules || state.rules);
    state._packSoftMode = true;
  }

${helpers}

${dedent(core)}

${dedent(curriculum)}

  function solveSnapshot(snap) {
    setSnapshot(snap);
    const lessons = buildLessonUnits();
    const domains = buildBaseDomains(lessons);
    const precheckIssues = precheckSchedule(lessons, domains);
    if (precheckIssues.length) {
      return {
        ok: false, status: 'infeasible', precheckIssues, lessons,
        assignments: null, nodes: 0, deepest: 0, beauty: null, audit: null,
        total: lessons.length, placed: 0,
      };
    }
    const solved = solveByConstraints(lessons, domains);
    const placed = (solved.assignments || []).filter(Boolean).length;
    const audit = auditScheduleQuality(lessons, solved.assignments || []);
    const full = !!solved.ok && placed === lessons.length;
    return {
      ok: full,
      status: full ? 'complete' : (placed > 0 ? 'partial' : 'infeasible'),
      precheckIssues: [],
      lessons,
      assignments: solved.assignments,
      nodes: solved.nodes,
      deepest: solved.deepest,
      blockedLesson: solved.blockedLesson || null,
      beauty: solved.beauty,
      audit,
      total: lessons.length,
      placed,
    };
  }

  return {
    state, setSnapshot, normalizeRules, solveSnapshot,
    buildLessonUnits, buildBaseDomains, precheckSchedule, solveByConstraints,
    auditScheduleQuality, evaluateBeauty, curriculumCt2018, classGrade,
  };
});
`;

const outEngine = path.join(root, 'thoikhoabieu-engine.js');
fs.writeFileSync(outEngine, engine, 'utf8');
console.log('Wrote', outEngine, engine.length);

try {
  // syntax
  require('vm').runInNewContext(engine, { module: { exports: {} }, exports: {}, console }, { timeout: 1000 });
  console.log('engine load OK');
} catch (err) {
  console.error('engine FAIL', err.message);
  // still write for inspection
}

const worker = `/** Web Worker — xếp TKB ngoài main thread */
importScripts('./thoikhoabieu-engine.js');
self.onmessage = function (ev) {
  var msg = ev.data || {};
  if (msg.type !== 'solve') return;
  try {
    var t0 = Date.now();
    var result = self.TkbEngine.solveSnapshot(msg.payload || {});
    self.postMessage({
      type: 'solve-done',
      requestId: msg.requestId,
      ok: true,
      result: {
        ok: result.ok,
        status: result.status,
        precheckIssues: result.precheckIssues,
        assignments: result.assignments,
        nodes: result.nodes,
        deepest: result.deepest,
        blockedLesson: result.blockedLesson,
        beauty: result.beauty,
        audit: result.audit,
        total: result.total,
        placed: result.placed,
        ms: Date.now() - t0
      },
      lessons: (result.lessons || []).map(function (L) {
        return {
          id: L.id, classId: L.classId, teacherId: L.teacherId,
          subject: L.subject, className: L.className, teacherName: L.teacherName,
          roomNeed: L.roomNeed || '', unit: L.unit
        };
      })
    });
  } catch (err) {
    self.postMessage({
      type: 'solve-done', requestId: msg.requestId, ok: false,
      error: String(err && err.message ? err.message : err)
    });
  }
};
`;
fs.writeFileSync(path.join(root, 'thoikhoabieu-worker.js'), worker, 'utf8');
console.log('Wrote worker');
