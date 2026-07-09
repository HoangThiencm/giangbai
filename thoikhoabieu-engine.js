/**
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


  const clean = value => String(value ?? '').trim();
  const normalizeText = value => clean(value).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd');
  const splitList = value => clean(value).split(/[,\n;]+/).map(v => v.trim()).filter(Boolean);
  const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));


function parseUnavailable(value) {
      const text = normalizeText(value)
          .replace(/thu\s*/g, 't')
          .replace(/sang/g, 's')
          .replace(/chieu/g, 'c')
          .replace(/tiet/g, '');
      const set = new Set();
      text.split(/[,\n;]+/).forEach(part => {
          const compact = part.replace(/\s+/g, '').toUpperCase();
          if (!compact) return;
          // T2S1-3 | T2S1 | T2S | T2C | T2
          const match = compact.match(/T?([2-7])([SC])?(?:(\d+)(?:-(\d+))?)?/);
          if (!match) return;
          const day = `T${match[1]}`;
          const sessCode = match[2]; // S / C / undefined
          const pFrom = match[3] ? Number(match[3]) : null;
          const pTo = match[4] ? Number(match[4]) : pFrom;

          const sessions = sessCode
              ? [sessCode === 'S' ? 'morning' : 'afternoon']
              : ['morning', 'afternoon'];

          sessions.forEach(session => {
              if (pFrom == null) {
                  set.add(`${day}-${session}`); // cả buổi
                  return;
              }
              const a = Math.min(pFrom, pTo || pFrom);
              const b = Math.max(pFrom, pTo || pFrom);
              for (let p = a; p <= b; p++) set.add(`${day}-${session}-${p}`);
          });
      });
      return set;
  }

  function isSlotBlockedBySet(blockSet, slot) {
      if (!blockSet || !blockSet.size) return false;
      if (blockSet.has(`${slot.day}-${slot.session}`)) return true;
      if (blockSet.has(`${slot.day}-${slot.session}-${slot.period}`)) return true;
      return false;
  }

  function schoolBlockedSet() {
      return parseUnavailable(state.rules.blockedSlots || '');
  }

  function sessionPeriodRange(session) {
      if (session === 'afternoon') {
          const from = Math.max(1, Number(state.rules.afternoonFrom || 1));
          const to = Math.max(from, Number(state.rules.afternoonTo || state.rules.afternoonPeriods || 4));
          return { from, to };
      }
      const from = Math.max(1, Number(state.rules.morningFrom || 1));
      const to = Math.max(from, Number(state.rules.morningTo || state.rules.morningPeriods || 5));
      return { from, to };
  }

  function slotsForClass(classItem) {
      const sessions = classItem.shift === 'both' ? ['morning', 'afternoon'] : [classItem.shift || 'morning'];
      const blocked = schoolBlockedSet();
      const slots = [];
      (state.rules.days || []).forEach(day => {
          sessions.forEach(session => {
              const { from, to } = sessionPeriodRange(session);
              for (let period = from; period <= to; period++) {
                  const slot = { day, session, period, key: `${day}-${session}-${period}` };
                  if (isSlotBlockedBySet(blocked, slot)) continue;
                  slots.push(slot);
              }
          });
      });
      return slots;
  }

  /** Tiết đầu khung buổi sau khi bỏ qua ô ngoại lệ toàn trường (blocked). */
  function effectiveSessionStart(day, session) {
      const { from, to } = sessionPeriodRange(session);
      const blocked = schoolBlockedSet();
      for (let p = from; p <= to; p++) {
          if (!isSlotBlockedBySet(blocked, { day, session, period: p })) return p;
      }
      return from;
  }

  /** Số “lủng” trong dải tiết — bỏ qua ô blocked toàn trường (không tính là lỗ). */
  function gapCountInSession(day, session, periods) {
      const list = uniqueSortedPeriods(periods);
      if (list.length <= 1) return 0;
      const blocked = schoolBlockedSet();
      let gaps = 0;
      for (let p = list[0]; p <= list[list.length - 1]; p++) {
          if (list.includes(p)) continue;
          if (isSlotBlockedBySet(blocked, { day, session, period: p })) continue;
          gaps++;
      }
      return gaps;
  }

  /**
   * Ràng buộc cứng: gói từ tiết đầu buổi, không lủng giữa.
   * Ô ngoại lệ (blockedSlots) được bỏ qua — không bắt phải “lấp” ô đó.
   */
  function packConstraintAllows(lesson, option, assignments, lessonsArr) {
      if (state.rules.packFromSessionStart === false) return true;
      // Chế độ mềm: không chặn domain (chỉ phạt soft) — ưu tiên xếp đủ 100% rồi beautify gói buổi
      if (state._packSoftMode) return true;
      const start = effectiveSessionStart(option.day, option.session);
      const blocked = schoolBlockedSet();
      if (isSlotBlockedBySet(blocked, option)) return false;

      const periods = [];
      (assignments || []).forEach((placed, i) => {
          if (!placed) return;
          const other = lessonsArr[i];
          if (!other || other.classId !== lesson.classId) return;
          if (placed.day === option.day && placed.session === option.session) periods.push(placed.period);
      });
      periods.push(option.period);
      const uniq = Array.from(new Set(periods)).sort((a, b) => a - b);
      const min = uniq[0];
      const max = uniq[uniq.length - 1];
      if (min !== start) return false;
      for (let p = start; p <= max; p++) {
          if (isSlotBlockedBySet(blocked, { day: option.day, session: option.session, period: p })) continue;
          if (!uniq.includes(p)) return false;
      }
      return true;
  }

  /**
   * Rà lịch sau xếp: lủng lớp, trống tiết đầu, tiết mồ côi GV (1 tiết lẻ / gap GV).
   * Trả về { classHoles, teacherOrphans, teacherGaps, startLate, messages }
   */
  function auditScheduleQuality(lessons, assignments) {
      const classBuckets = new Map();
      const teacherBuckets = new Map();
      const messages = [];
      assignments.forEach((option, index) => {
          if (!option) return;
          const lesson = lessons[index];
          const ck = `${lesson.classId}|${lesson.className || ''}|${option.day}|${option.session}`;
          const tk = `${lesson.teacherId}|${lesson.teacherName || ''}|${option.day}|${option.session}`;
          if (!classBuckets.has(ck)) classBuckets.set(ck, []);
          if (!teacherBuckets.has(tk)) teacherBuckets.set(tk, []);
          classBuckets.get(ck).push(option.period);
          teacherBuckets.get(tk).push({ period: option.period, subject: lesson.subject, className: lesson.className });
      });

      let classHoles = 0;
      let startLate = 0;
      classBuckets.forEach((periods, key) => {
          const parts = key.split('|');
          const className = parts[1] || 'Lớp';
          const day = parts[2];
          const session = parts[3];
          const list = uniqueSortedPeriods(periods);
          const holes = gapCountInSession(day, session, list);
          const start = effectiveSessionStart(day, session);
          if (list.length && list[0] > start) {
              startLate++;
              messages.push({
                  type: 'start-late',
                  severity: 'error',
                  message: `${className} · ${day} ${session === 'afternoon' ? 'chiều' : 'sáng'}: trống tiết đầu (bắt đầu từ tiết ${list[0]}, khung từ ${start}).`,
              });
          }
          if (holes > 0) {
              classHoles += holes;
              messages.push({
                  type: 'class-hole',
                  severity: 'error',
                  message: `${className} · ${day} ${session === 'afternoon' ? 'chiều' : 'sáng'}: lủng ${holes} tiết giữa buổi (dải ${list[0]}–${list[list.length - 1]}).`,
              });
          }
      });

      let teacherGaps = 0;
      let teacherOrphans = 0;
      teacherBuckets.forEach((items, key) => {
          const parts = key.split('|');
          const teacherName = parts[1] || 'GV';
          const day = parts[2];
          const session = parts[3];
          const list = uniqueSortedPeriods(items.map(i => i.period));
          const holes = gapCountInSession(day, session, list);
          if (holes > 0) {
              teacherGaps += holes;
              messages.push({
                  type: 'teacher-gap',
                  severity: 'warn',
                  message: `${teacherName} · ${day} ${session === 'afternoon' ? 'chiều' : 'sáng'}: lịch GV lủng ${holes} tiết (dải ${list.join(', ')}).`,
              });
          }
          if (list.length === 1) {
              teacherOrphans++;
              messages.push({
                  type: 'teacher-orphan',
                  severity: 'warn',
                  message: `${teacherName} · ${day} ${session === 'afternoon' ? 'chiều' : 'sáng'}: tiết mồ côi (chỉ 1 tiết ${list[0]} — ${items[0]?.subject || ''} ${items[0]?.className || ''}).`,
              });
          }
      });

      return {
          classHoles,
          startLate,
          teacherGaps,
          teacherOrphans,
          messages,
          ok: classHoles === 0 && startLate === 0,
      };
  }

  /** True nếu mọi buổi lớp đã xếp đều gói từ tiết đầu, không lủng (bỏ qua blocked). */
  function isFullyPackValid(lessons, assignments) {
      if (state.rules.packFromSessionStart === false) return true;
      const buckets = new Map();
      assignments.forEach((opt, i) => {
          if (!opt) return;
          const L = lessons[i];
          const k = `${L.classId}|${opt.day}|${opt.session}`;
          if (!buckets.has(k)) buckets.set(k, []);
          buckets.get(k).push(opt.period);
      });
      for (const [k, periods] of buckets) {
          const parts = k.split('|');
          const day = parts[1];
          const session = parts[2];
          const list = uniqueSortedPeriods(periods);
          const start = effectiveSessionStart(day, session);
          if (list[0] !== start) return false;
          if (gapCountInSession(day, session, list) > 0) return false;
      }
      return true;
  }

  /**
   * Sửa lủng / trống tiết đầu: với mỗi buổi lớp vi phạm, gỡ các tiết “lẻ” không thuộc
   * khối liên tục từ tiết đầu; solver partial có thể để lại trạng thái này khi hết budget.
   */
  function stripPackViolations(lessons, assignments) {
      if (state.rules.packFromSessionStart === false) return assignments;
      const next = assignments.slice();
      const buckets = new Map();
      next.forEach((opt, i) => {
          if (!opt) return;
          const L = lessons[i];
          const k = `${L.classId}|${opt.day}|${opt.session}`;
          if (!buckets.has(k)) buckets.set(k, []);
          buckets.get(k).push(i);
      });
      buckets.forEach((indexes, k) => {
          const parts = k.split('|');
          const day = parts[1];
          const session = parts[2];
          const start = effectiveSessionStart(day, session);
          const blocked = schoolBlockedSet();
          const byPeriod = new Map();
          indexes.forEach(i => {
              const p = next[i].period;
              if (!byPeriod.has(p)) byPeriod.set(p, []);
              byPeriod.get(p).push(i);
          });
          // Giữ chuỗi liên tục start, start+1, ... đến khi gặp lỗ (không blocked)
          const { to } = sessionPeriodRange(session);
          let keepUntil = start - 1;
          for (let p = start; p <= to; p++) {
              if (isSlotBlockedBySet(blocked, { day, session, period: p })) continue;
              if (!byPeriod.has(p)) break;
              keepUntil = p;
          }
          indexes.forEach(i => {
              if (next[i] && next[i].period > keepUntil) next[i] = null;
          });
      });
      return next;
  }

  function roomMatches(room, needOrSubject) {
      const need = normalizeText(needOrSubject);
      if (!need) return false;
      // Đồng nghĩa phòng BM / môn CT 2018
      const aliases = {
          'the duc': ['giao duc the chat', 'gdtc', 'the duc'],
          'giao duc the chat': ['the duc', 'gdtc', 'giao duc the chat'],
          'vat li': ['vat ly', 'ly'],
          'vat ly': ['vat li', 'ly'],
          'khtn': ['khoa hoc tu nhien', 'khtn'],
          'khoa hoc tu nhien': ['khtn', 'khoa hoc tu nhien'],
      };
      const needForms = new Set([need, ...(aliases[need] || [])]);
      return splitList(room.subjects).some(s => {
          const ns = normalizeText(s);
          if (!ns) return false;
          if (needForms.has(ns) || need.includes(ns) || ns.includes(need)) return true;
          return Array.from(needForms).some(f => ns.includes(f) || f.includes(ns));
      }) || Array.from(needForms).some(f => normalizeText(room.name).includes(f));
  }

  function chooseRoom(assignment, slot, roomBusy) {
      const classItem = state.classes.find(c => c.id === assignment.classId);
      const need = assignment.roomNeed || assignment.subject;
      const candidates = state.rooms.filter(room => roomMatches(room, need));
      for (const room of candidates) {
          const key = `${room.name}|${slot.day}|${slot.session}|${slot.period}`;
          if (!roomBusy.has(key)) return room.name;
      }
      return classItem?.homeRoom || classItem?.name || '';
  }

  function buildLessonUnits() {
      const units = [];
      state.assignments.forEach(assignment => {
          const classItem = state.classes.find(c => c.id === assignment.classId);
          const teacher = state.teachers.find(t => t.id === assignment.teacherId);
          const periods = Math.max(0, Number(assignment.periods || 0));
          if (!classItem || !teacher || !assignment.subject || periods <= 0) return;
          for (let i = 0; i < periods; i++) {
              units.push({ ...assignment, unit: i + 1, className: classItem.name, teacherName: teacher.name });
          }
      });
      return units.sort((a, b) => {
          const ta = state.assignments.filter(x => x.teacherId === a.teacherId).reduce((sum, x) => sum + Number(x.periods || 0), 0);
          const tb = state.assignments.filter(x => x.teacherId === b.teacherId).reduce((sum, x) => sum + Number(x.periods || 0), 0);
          return tb - ta || b.periods - a.periods;
      });
  }

  function roomOptionsForLesson(lesson, slot) {
      const classItem = state.classes.find(c => c.id === lesson.classId);
      const need = lesson.roomNeed || lesson.subject;
      const specialized = state.rooms
          .filter(room => roomMatches(room, need))
          .map(room => room.name)
          .filter(Boolean);
      const rooms = specialized.length ? specialized : [classItem?.homeRoom || classItem?.name || ''];
      return Array.from(new Set(rooms.filter(Boolean))).map(room => ({ ...slot, room }));
  }

  function buildBaseDomains(lessons) {
      const teacherUnavailable = Object.fromEntries(state.teachers.map(t => [t.id, parseUnavailable(t.unavailable)]));
      return lessons.map(lesson => {
          const classItem = state.classes.find(c => c.id === lesson.classId);
          if (!classItem) return [];
          const blocked = teacherUnavailable[lesson.teacherId];
          const slots = slotsForClass(classItem).filter(slot => !isSlotBlockedBySet(blocked, slot));
          return slots.flatMap(slot => roomOptionsForLesson(lesson, slot));
      });
  }

  function makeIssue(message, type = 'infeasible') {
      return { type, message };
  }

  function precheckSchedule(lessons, domains) {
      const issues = [];
      const classLoad = {};
      const teacherLoad = {};
      lessons.forEach(lesson => {
          classLoad[lesson.classId] = (classLoad[lesson.classId] || 0) + 1;
          teacherLoad[lesson.teacherId] = (teacherLoad[lesson.teacherId] || 0) + 1;
      });

      state.classes.forEach(c => {
          const capacity = slotsForClass(c).length;
          if ((classLoad[c.id] || 0) > capacity) {
              issues.push(makeIssue(`${c.name} có ${classLoad[c.id]} tiết cần xếp nhưng chỉ có ${capacity} ô học theo cấu hình buổi học.`));
          }
      });

      state.teachers.forEach(t => {
          const load = teacherLoad[t.id] || 0;
          if (load > Number(t.maxPeriods || 99)) {
              issues.push(makeIssue(`${t.name} được phân công ${load} tiết/tuần, vượt định mức ${t.maxPeriods} tiết/tuần.`));
          }
      });

      const classSubjectLoad = {};
      lessons.forEach(lesson => {
          const key = `${lesson.classId}|${normalizeText(lesson.subject)}`;
          classSubjectLoad[key] = (classSubjectLoad[key] || 0) + 1;
      });
      Object.entries(classSubjectLoad).forEach(([key, load]) => {
          const [classId, subjectKey] = key.split('|');
          const classItem = state.classes.find(c => c.id === classId);
          const lesson = lessons.find(item => item.classId === classId && normalizeText(item.subject) === subjectKey);
          const capacity = state.rules.days.length * state.rules.maxSameSubjectDay;
          if (load > capacity) {
              issues.push(makeIssue(`${classItem?.name || 'Lớp'} - ${lesson?.subject || 'môn học'} có ${load} tiết/tuần, vượt giới hạn ${state.rules.maxSameSubjectDay} tiết/môn/ngày trong ${state.rules.days.length} ngày học.`));
          }
      });

      lessons.forEach((lesson, index) => {
          if (!domains[index]?.length) {
              issues.push(makeIssue(`${lesson.subject} - ${lesson.className} (${lesson.teacherName}) không có ô hợp lệ ban đầu. Kiểm tra buổi học của lớp, buổi tránh của giáo viên và phòng bộ môn.`));
          }
      });

      return issues;
  }

  function gapCount(periods) {
      const list = Array.from(new Set(periods.filter(Number))).sort((a, b) => a - b);
      if (list.length <= 1) return 0;
      let gaps = 0;
      for (let period = list[0]; period <= list[list.length - 1]; period++) {
          if (!list.includes(period)) gaps++;
      }
      return gaps;
  }

  function uniqueSortedPeriods(periods) {
      return Array.from(new Set((periods || []).filter(Number))).sort((a, b) => a - b);
  }

  function isCoreSubject(subject) {
      const n = normalizeText(subject);
      return /toan|ngu\s*van|^van$|van hoc|tieng anh|^anh$|ngoai ngu/.test(n);
  }

  function isDoubleFriendlySubject(subject) {
      const n = normalizeText(subject);
      return /toan|ngu\s*van|^van$|tieng anh|^anh$|vat ly|hoa hoc|sinh hoc|tin hoc|ngoai ngu/.test(n);
  }

  /** Điểm thấp = lịch đẹp hơn. Chuẩn thực tế VN / tkb.com.vn: gói buổi, tiết đôi, trống cuối ngày, rải môn. */
  function evaluateBeauty(lessons, assignments) {
      const classBuckets = new Map();
      const teacherBuckets = new Map();
      const subjectDayPeriods = new Map();
      const classDayLoad = new Map();
      let latePenalty = 0;
      let roomPenalty = 0;
      let coreLatePenalty = 0;
      let placed = 0;

      assignments.forEach((option, index) => {
          if (!option) return;
          placed++;
          const lesson = lessons[index];
          const classKey = `${lesson.classId}|${option.day}|${option.session}`;
          const teacherKey = `${lesson.teacherId}|${option.day}|${option.session}`;
          const subjectKey = `${lesson.classId}|${normalizeText(lesson.subject)}|${option.day}|${option.session}`;
          const dayLoadKey = `${lesson.classId}|${option.day}`;
          if (!classBuckets.has(classKey)) classBuckets.set(classKey, []);
          if (!teacherBuckets.has(teacherKey)) teacherBuckets.set(teacherKey, []);
          if (!subjectDayPeriods.has(subjectKey)) subjectDayPeriods.set(subjectKey, []);
          classBuckets.get(classKey).push(option.period);
          teacherBuckets.get(teacherKey).push(option.period);
          subjectDayPeriods.get(subjectKey).push(option.period);
          classDayLoad.set(dayLoadKey, (classDayLoad.get(dayLoadKey) || 0) + 1);
          latePenalty += option.period * 0.22 + (option.session === 'afternoon' ? 0.25 : 0);
          if (isCoreSubject(lesson.subject) && option.period >= 4) coreLatePenalty += (option.period - 3) * 8;
          if (lesson.roomNeed && !roomMatches({ name: option.room, subjects: lesson.roomNeed }, lesson.roomNeed)) roomPenalty += 6;
      });

      let classGaps = 0;
      let teacherGaps = 0;
      let singleLessonTeacherSessions = 0;
      let classStartLate = 0;
      classBuckets.forEach((periods, classKey) => {
          const list = uniqueSortedPeriods(periods);
          const parts = classKey.split('|');
          const day = parts[1];
          const session = parts[2] || 'morning';
          // classKey = classId|day|session
          classGaps += gapCountInSession(day, session, list);
          const start = effectiveSessionStart(day, session);
          if (list.length && list[0] > start) classStartLate += (list[0] - start) * 8 + 20;
      });
      teacherBuckets.forEach((periods, teacherKey) => {
          const list = uniqueSortedPeriods(periods);
          const parts = teacherKey.split('|');
          const day = parts[1];
          const session = parts[2] || 'morning';
          teacherGaps += gapCountInSession(day, session, list);
          if (list.length === 1) singleLessonTeacherSessions++;
      });

      let sameSubjectSameDay = 0;
      let brokenDoubles = 0;
      let goodDoubles = 0;
      subjectDayPeriods.forEach((periods, key) => {
          const list = uniqueSortedPeriods(periods);
          if (list.length > 1) sameSubjectSameDay += list.length - 1;
          if (list.length >= 2) {
              let consecutivePairs = 0;
              for (let i = 1; i < list.length; i++) {
                  if (list[i] === list[i - 1] + 1) consecutivePairs++;
              }
              const needed = list.length - 1;
              goodDoubles += consecutivePairs;
              brokenDoubles += Math.max(0, needed - consecutivePairs);
              // Môn hay dạy tiết đôi mà tách rời → phạt mạnh
              const subject = key.split('|')[1] || '';
              if (isDoubleFriendlySubject(subject) && consecutivePairs < needed) {
                  brokenDoubles += needed - consecutivePairs;
              }
          }
      });

      // Cân tải ngày trong tuần của lớp (tránh ngày 5 tiết, ngày 2 tiết)
      const loadByClass = new Map();
      classDayLoad.forEach((load, key) => {
          const classId = key.split('|')[0];
          if (!loadByClass.has(classId)) loadByClass.set(classId, []);
          loadByClass.get(classId).push(load);
      });
      let dayLoadVariance = 0;
      loadByClass.forEach(loads => {
          if (loads.length <= 1) return;
          const avg = loads.reduce((s, v) => s + v, 0) / loads.length;
          loads.forEach(v => { dayLoadVariance += Math.abs(v - avg); });
      });

      const score =
          classGaps * 280 +
          teacherGaps * 160 +
          brokenDoubles * 95 +
          sameSubjectSameDay * 18 +
          singleLessonTeacherSessions * 55 +
          classStartLate * (state.rules.packFromSessionStart === false ? 40 : 400) +
          dayLoadVariance * 6 +
          coreLatePenalty +
          latePenalty +
          roomPenalty -
          goodDoubles * 28;

      // 0–100: ước lượng chất lượng (càng cao càng đẹp)
      const quality = Math.max(0, Math.min(100, Math.round(100 - score / Math.max(8, placed * 0.55))));

      return {
          score: Math.round(score * 100) / 100,
          quality,
          classGaps,
          teacherGaps,
          sameSubjectSameDay,
          singleLessonTeacherSessions,
          goodDoubles,
          brokenDoubles,
          classStartLate,
          dayLoadVariance: Math.round(dayLoadVariance * 10) / 10,
          placed,
      };
  }

  function solveByConstraints(lessons, domains) {
      // Ưu tiên khả thi 100%: soft-pack khi xếp, hard-pack chỉ khi beautify/audit
      state._packSoftMode = true;
      // Scale budget theo kích thước — large (≈840) cần cắt bớt attempt/beautify
      const n = lessons.length;
      const isLarge = n > 600;
      const isHuge = n > 900;
      // Large: CSP như medium nhưng bỏ improve/beautify nặng + early stop
      const maxDepth = isHuge ? 12 : isLarge ? 14 : n > 400 ? 14 : 20;
      const maxAttempts = isHuge ? 4 : isLarge ? 6 : n > 400 ? 12 : 28;
      const nodeBudget = isHuge ? 400000 : isLarge ? 550000 : n > 400 ? 650000 : 1150000;
      let totalNodes = 0;
      let deepest = 0;
      let bestBlocked = null;
      let bestSolution = null;
      let bestBeauty = null;
      let bestPartial = null;
      let bestPartialPlaced = 0;

      const subjectDayKey = (lesson, option) => `${lesson.classId}|${normalizeText(lesson.subject)}|${option.day}`;
      const resourceKeys = (lesson, option) => ({
          classKey: `${lesson.classId}|${option.day}|${option.session}|${option.period}`,
          teacherKey: `${lesson.teacherId}|${option.day}|${option.session}|${option.period}`,
          roomKey: `${option.room}|${option.day}|${option.session}|${option.period}`,
          subjectKey: subjectDayKey(lesson, option),
      });

      // O(n) thay vì O(n²) khi tính load cho difficulty order
      const teacherLoadMap = Object.create(null);
      const classLoadMap = Object.create(null);
      lessons.forEach(lesson => {
          teacherLoadMap[lesson.teacherId] = (teacherLoadMap[lesson.teacherId] || 0) + 1;
          classLoadMap[lesson.classId] = (classLoadMap[lesson.classId] || 0) + 1;
      });
      const difficultyOrder = lessons.map((lesson, index) => ({
          index,
          size: domains[index].length,
          load: (teacherLoadMap[lesson.teacherId] || 0) + (classLoadMap[lesson.classId] || 0),
      })).sort((a, b) => a.size - b.size || b.load - a.load).map(item => item.index);

      function rememberPartial(assignments, beauty = null) {
          // Không lưu partial đang lủng/trống tiết 1 (trừ khi pack tắt)
          if (state.rules.packFromSessionStart !== false && !isFullyPackValid(lessons, assignments)) {
              // Vẫn cho phép nếu chưa có partial pack-hợp lệ nào và đang sâu hơn
              const cleaned = stripPackViolations(lessons, assignments);
              const placedClean = cleaned.filter(Boolean).length;
              if (placedClean > bestPartialPlaced || (placedClean === bestPartialPlaced && isFullyPackValid(lessons, cleaned))) {
                  bestPartialPlaced = placedClean;
                  bestPartial = cleaned;
                  bestBeauty = beauty ? { ...beauty, placed: placedClean } : bestBeauty;
              }
              return;
          }
          const placed = assignments.filter(Boolean).length;
          if (placed > bestPartialPlaced) {
              bestPartialPlaced = placed;
              bestPartial = assignments.slice();
              bestBeauty = beauty ? { ...beauty, placed } : bestBeauty;
          }
      }

      function makeSolver(attempt) {
          let assignments = new Array(lessons.length).fill(null);
          let classSlotMap = new Map();
          let teacherSlotMap = new Map();
          let roomSlotMap = new Map();
          let subjectDayMap = new Map();
          let nodes = 0;

          function snapshot() {
              return {
                  assignments: assignments.slice(),
                  classSlotMap: new Map(classSlotMap),
                  teacherSlotMap: new Map(teacherSlotMap),
                  roomSlotMap: new Map(roomSlotMap),
                  subjectDayMap: new Map(Array.from(subjectDayMap, ([key, value]) => [key, new Set(value)])),
              };
          }

          function restore(snap) {
              assignments = snap.assignments;
              classSlotMap = snap.classSlotMap;
              teacherSlotMap = snap.teacherSlotMap;
              roomSlotMap = snap.roomSlotMap;
              subjectDayMap = snap.subjectDayMap;
          }

          function addSubjectDay(key, index) {
              if (!subjectDayMap.has(key)) subjectDayMap.set(key, new Set());
              subjectDayMap.get(key).add(index);
          }

          function place(index, option) {
              const lesson = lessons[index];
              const keys = resourceKeys(lesson, option);
              assignments[index] = option;
              classSlotMap.set(keys.classKey, index);
              teacherSlotMap.set(keys.teacherKey, index);
              roomSlotMap.set(keys.roomKey, index);
              addSubjectDay(keys.subjectKey, index);
          }

          function unplace(index) {
              const option = assignments[index];
              if (!option) return;
              const lesson = lessons[index];
              const keys = resourceKeys(lesson, option);
              assignments[index] = null;
              classSlotMap.delete(keys.classKey);
              teacherSlotMap.delete(keys.teacherKey);
              roomSlotMap.delete(keys.roomKey);
              const subjectSet = subjectDayMap.get(keys.subjectKey);
              if (subjectSet) {
                  subjectSet.delete(index);
                  if (!subjectSet.size) subjectDayMap.delete(keys.subjectKey);
              }
          }

          function conflictsFor(index, option, path) {
              const lesson = lessons[index];
              const keys = resourceKeys(lesson, option);
              const conflicts = new Set();
              [classSlotMap.get(keys.classKey), teacherSlotMap.get(keys.teacherKey), roomSlotMap.get(keys.roomKey)]
                  .forEach(conflict => {
                      if (conflict !== undefined && conflict !== index) conflicts.add(conflict);
                  });
              const subjectSet = subjectDayMap.get(keys.subjectKey);
              const subjectCount = subjectSet ? subjectSet.size : 0;
              if (subjectCount >= state.rules.maxSameSubjectDay) {
                  const movable = Array.from(subjectSet || [])
                      .filter(conflict => conflict !== index && !path.has(conflict))
                      .sort((a, b) => domains[b].length - domains[a].length)[0];
                  if (movable !== undefined) conflicts.add(movable);
                  else conflicts.add(Array.from(subjectSet || [])[0]);
              }
              return Array.from(conflicts).filter(conflict => conflict !== undefined && conflict !== index);
          }

          function localSoftCost(index, option) {
              const lesson = lessons[index];
              const classPeriods = [];
              const teacherPeriods = [];
              let adjacentSameSubject = false;
              assignments.forEach((placed, placedIndex) => {
                  if (!placed || placedIndex === index) return;
                  const other = lessons[placedIndex];
                  if (placed.day === option.day && placed.session === option.session && other.classId === lesson.classId) {
                      classPeriods.push(placed.period);
                      if (normalizeText(other.subject) === normalizeText(lesson.subject) && Math.abs(placed.period - option.period) === 1) {
                          adjacentSameSubject = true;
                      }
                  }
                  if (placed.day === option.day && placed.session === option.session && other.teacherId === lesson.teacherId) teacherPeriods.push(placed.period);
              });
              const classBefore = gapCountInSession(option.day, option.session, classPeriods);
              const teacherBefore = gapCountInSession(option.day, option.session, teacherPeriods);
              const classAfter = gapCountInSession(option.day, option.session, [...classPeriods, option.period]);
              const teacherAfter = gapCountInSession(option.day, option.session, [...teacherPeriods, option.period]);
              const adjacentClass = classPeriods.some(period => Math.abs(period - option.period) === 1);
              const adjacentTeacher = teacherPeriods.some(period => Math.abs(period - option.period) === 1);
              const subjectCount = subjectDayMap.get(subjectDayKey(lesson, option))?.size || 0;
              const startP = effectiveSessionStart(option.day, option.session);
              let packFromStart = 0;
              if (!classPeriods.length) {
                  packFromStart = option.period === startP ? -50 : 40 + (option.period - startP) * 22;
              } else {
                  const maxP = Math.max(...classPeriods);
                  const minP = Math.min(...classPeriods);
                  if (option.period > maxP + 1) packFromStart = 45;
                  if (option.period < minP - 1) packFromStart = 45;
                  if (minP > startP) packFromStart += 100;
              }
              if (!packConstraintAllows(lesson, option, assignments, lessons)) packFromStart += 50000;
              // Tránh tiết mồ côi GV: buổi đang 0 tiết thì nhẹ; đã 1 tiết thì mạnh ưu tiên kề
              let orphanTeacher = 0;
              if (teacherPeriods.length === 1 && !adjacentTeacher) orphanTeacher = 35;
              if (teacherPeriods.length === 0) orphanTeacher = 8; // hơi không thích 1 tiết lẻ sau này
              const doubleBonus = adjacentSameSubject && isDoubleFriendlySubject(lesson.subject) ? -42 : (adjacentSameSubject ? -22 : 0);
              const coreLate = isCoreSubject(lesson.subject) && option.period >= startP + 3 ? (option.period - startP - 2) * 6 : 0;
              return (
                  (classAfter - classBefore) * 200 +
                  (teacherAfter - teacherBefore) * 120 +
                  subjectCount * 22 +
                  (option.period - startP) * 0.55 +
                  (option.session === 'afternoon' ? 0.45 : 0) +
                  packFromStart +
                  orphanTeacher +
                  coreLate +
                  doubleBonus -
                  (adjacentClass ? 24 : 0) -
                  (adjacentTeacher ? 28 : 0) +
                  ((attempt * 17 + option.period * 13 + option.day.charCodeAt(1)) % 11) * 0.03
              );
          }

          function orderedOptions(index, path) {
              let pool = domains[index].filter(option => packConstraintAllows(lessons[index], option, assignments, lessons));
              // Large: cắt domain + cost rẻ (tránh O(domain × n) quá nặng)
              if (isLarge || isHuge) {
                  pool = pool.slice().sort((a, b) => a.period - b.period || a.day.localeCompare(b.day)).slice(0, 18);
                  return pool.map(option => {
                      const conflicts = conflictsFor(index, option, path);
                      return {
                          option,
                          conflicts,
                          cost: conflicts.length * 10000 + option.period * 2 + (option.session === 'afternoon' ? 1 : 0),
                      };
                  }).sort((a, b) => a.cost - b.cost);
              }
              return pool.map(option => {
                  const conflicts = conflictsFor(index, option, path);
                  return { option, conflicts, cost: conflicts.length * 10000 + localSoftCost(index, option) };
              }).sort((a, b) => {
                  const jitterA = ((attempt + 3) * (a.option.period + 5) * (a.option.day.charCodeAt(1) + 7)) % 17;
                  const jitterB = ((attempt + 3) * (b.option.period + 5) * (b.option.day.charCodeAt(1) + 7)) % 17;
                  return (a.cost + jitterA * 0.02) - (b.cost + jitterB * 0.02);
              });
          }

          function recursivePlace(index, depth, path) {
              nodes++;
              totalNodes++;
              deepest = Math.max(deepest, assignments.filter(Boolean).length);
              if (totalNodes > nodeBudget) {
                  rememberPartial(assignments, evaluateBeauty(lessons, assignments));
                  return false;
              }
              if (assignments[index]) return true;

              const candidates = orderedOptions(index, path);
              for (const candidate of candidates) {
                  if (candidate.conflicts.some(conflict => path.has(conflict))) continue;
                  if (candidate.conflicts.length && depth <= 0) continue;
                  if (candidate.conflicts.length > 4) continue;

                  const snap = snapshot();
                  candidate.conflicts.forEach(unplace);
                  place(index, candidate.option);

                  let ok = true;
                  const nextPath = new Set(path);
                  nextPath.add(index);
                  // Xếp lại conflict theo tiết sớm trước — tránh re-place tiết 3 trước tiết 1 (gây lủng tạm / fail pack)
                  const displaced = candidate.conflicts.slice().sort((a, b) => {
                      const minA = Math.min(...domains[a].map(o => o.period));
                      const minB = Math.min(...domains[b].map(o => o.period));
                      return minA - minB || domains[a].length - domains[b].length;
                  });
                  for (const conflict of displaced) {
                      if (!recursivePlace(conflict, depth - 1, nextPath)) {
                          ok = false;
                          bestBlocked = lessons[conflict];
                          break;
                      }
                  }
                  if (ok) return true;
                  restore(snap);
              }

              rememberPartial(assignments, evaluateBeauty(lessons, assignments));
              bestBlocked = lessons[index];
              return false;
          }

          function improve(maxChecks = 2500) {
              let currentBeauty = evaluateBeauty(lessons, assignments);
              let checks = 0;
              let improved = true;
              while (improved && checks < maxChecks) {
                  improved = false;
                  const order = lessons.map((_, index) => index).sort((a, b) => {
                      const ba = assignments[a];
                      const bb = assignments[b];
                      // Ưu tiên di chuyển tiết “xấu”: môn tách đôi, gap
                      const badA = ba && isDoubleFriendlySubject(lessons[a].subject) ? 0 : 1;
                      const badB = bb && isDoubleFriendlySubject(lessons[b].subject) ? 0 : 1;
                      return badA - badB || domains[a].length - domains[b].length;
                  });
                  for (const index of order) {
                      if (checks >= maxChecks) break;
                      const current = assignments[index];
                      if (!current) continue;
                      const snap = snapshot();
                      unplace(index);
                      const candidates = domains[index]
                          .filter(option => packConstraintAllows(lessons[index], option, assignments, lessons) && !conflictsFor(index, option, new Set()).length)
                          .sort((a, b) => localSoftCost(index, a) - localSoftCost(index, b))
                          .slice(0, 18);
                      let accepted = false;
                      for (const option of candidates) {
                          checks++;
                          place(index, option);
                          const beauty = evaluateBeauty(lessons, assignments);
                          if (beauty.score + 0.01 < currentBeauty.score) {
                              currentBeauty = beauty;
                              accepted = true;
                              improved = true;
                              break;
                          }
                          unplace(index);
                      }
                      if (!accepted) restore(snap);
                  }
              }
              return currentBeauty;
          }

          function run() {
              const order = attempt % 2
                  ? difficultyOrder.slice().sort((a, b) => domains[a].length - domains[b].length || ((a * 31 + attempt) % 7) - ((b * 31 + attempt) % 7))
                  : difficultyOrder;
              for (const index of order) {
                  if (!recursivePlace(index, maxDepth, new Set([index]))) {
                      const beauty = evaluateBeauty(lessons, assignments);
                      rememberPartial(assignments, beauty);
                      return { ok: false, assignments: assignments.slice(), nodes, placed: assignments.filter(Boolean).length, beauty };
                  }
              }
              // Large: bỏ improve trong attempt (beautify ngoài đã cắt); small/medium cải thiện nhẹ
              let beauty;
              if (isLarge || isHuge) {
                  beauty = evaluateBeauty(lessons, assignments);
              } else {
                  beauty = improve(lessons.length > 400 ? 1200 : 3500);
              }
              return { ok: true, assignments, nodes, placed: assignments.filter(Boolean).length, beauty };
          }

          return { run };
      }

      for (let attempt = 0; attempt < maxAttempts && totalNodes <= nodeBudget; attempt++) {
          const result = makeSolver(attempt).run();
          if (result.ok) {
              if (!bestSolution || result.beauty.score < bestBeauty.score) {
                  bestSolution = result.assignments.slice();
                  bestBeauty = result.beauty;
              }
              // Large: lấy lời giải 100% đầu tiên — không multi-attempt tìm đẹp hơn
              if (isLarge || isHuge) break;
              if (bestSolution && attempt >= Math.min(6, maxAttempts - 1) && bestBeauty.quality >= 72) break;
          } else if (!bestSolution && (!bestBeauty || result.placed > (bestBeauty.placed || 0))) {
              bestBeauty = { ...result.beauty, placed: result.placed };
              rememberPartial(result.assignments, result.beauty);
          }
      }

      /** Phase 2: tối ưu “đẹp” sau khi đã khả thi — relocate + swap (chuẩn thực tế TKB). */
      function beautifySchedule(seedAssignments, budget) {
          if (!seedAssignments?.some(Boolean)) return { assignments: seedAssignments, beauty: evaluateBeauty(lessons, seedAssignments), moves: 0 };

          let assignments = seedAssignments.slice();
          let classSlotMap = new Map();
          let teacherSlotMap = new Map();
          let roomSlotMap = new Map();
          let subjectDayMap = new Map();

          function rebuildMaps() {
              classSlotMap = new Map();
              teacherSlotMap = new Map();
              roomSlotMap = new Map();
              subjectDayMap = new Map();
              assignments.forEach((option, index) => {
                  if (!option) return;
                  const keys = resourceKeys(lessons[index], option);
                  classSlotMap.set(keys.classKey, index);
                  teacherSlotMap.set(keys.teacherKey, index);
                  roomSlotMap.set(keys.roomKey, index);
                  if (!subjectDayMap.has(keys.subjectKey)) subjectDayMap.set(keys.subjectKey, new Set());
                  subjectDayMap.get(keys.subjectKey).add(index);
              });
          }

          function conflictsAt(index, option, ignore = new Set()) {
              const keys = resourceKeys(lessons[index], option);
              const hits = [];
              const classHit = classSlotMap.get(keys.classKey);
              const teacherHit = teacherSlotMap.get(keys.teacherKey);
              const roomHit = roomSlotMap.get(keys.roomKey);
              if (classHit !== undefined && classHit !== index && !ignore.has(classHit)) hits.push(classHit);
              if (teacherHit !== undefined && teacherHit !== index && !ignore.has(teacherHit)) hits.push(teacherHit);
              if (roomHit !== undefined && roomHit !== index && !ignore.has(roomHit)) hits.push(roomHit);
              const subjectSet = subjectDayMap.get(keys.subjectKey);
              if (subjectSet) {
                  const others = Array.from(subjectSet).filter(i => i !== index && !ignore.has(i));
                  if (others.length >= state.rules.maxSameSubjectDay) hits.push(others[0]);
              }
              return Array.from(new Set(hits));
          }

          function unplace(index) {
              const option = assignments[index];
              if (!option) return;
              const keys = resourceKeys(lessons[index], option);
              assignments[index] = null;
              if (classSlotMap.get(keys.classKey) === index) classSlotMap.delete(keys.classKey);
              if (teacherSlotMap.get(keys.teacherKey) === index) teacherSlotMap.delete(keys.teacherKey);
              if (roomSlotMap.get(keys.roomKey) === index) roomSlotMap.delete(keys.roomKey);
              const set = subjectDayMap.get(keys.subjectKey);
              if (set) {
                  set.delete(index);
                  if (!set.size) subjectDayMap.delete(keys.subjectKey);
              }
          }

          function place(index, option) {
              const keys = resourceKeys(lessons[index], option);
              assignments[index] = option;
              classSlotMap.set(keys.classKey, index);
              teacherSlotMap.set(keys.teacherKey, index);
              roomSlotMap.set(keys.roomKey, index);
              if (!subjectDayMap.has(keys.subjectKey)) subjectDayMap.set(keys.subjectKey, new Set());
              subjectDayMap.get(keys.subjectKey).add(index);
          }

          rebuildMaps();
          let beauty = evaluateBeauty(lessons, assignments);
          let moves = 0;
          let checks = 0;
          const maxChecks = budget;

          function optionDoubleBonus(index, opt) {
              const lesson = lessons[index];
              let adj = 0;
              assignments.forEach((p, j) => {
                  if (!p || j === index) return;
                  const o = lessons[j];
                  if (o.classId === lesson.classId && normalizeText(o.subject) === normalizeText(lesson.subject)
                      && p.day === opt.day && p.session === opt.session && Math.abs(p.period - opt.period) === 1) adj += 50;
                  else if (o.classId === lesson.classId && p.day === opt.day && p.session === opt.session && Math.abs(p.period - opt.period) === 1) adj += 8;
                  if (o.teacherId === lesson.teacherId && p.day === opt.day && p.session === opt.session && Math.abs(p.period - opt.period) === 1) adj += 10;
              });
              return adj - opt.period * 0.5 - (isCoreSubject(lesson.subject) && opt.period >= 4 ? 6 : 0);
          }

          function relocatePass(limitPerPass) {
              let improvedLocal = false;
              const order = lessons.map((_, i) => i).sort((a, b) => domains[a].length - domains[b].length);
              for (const index of order) {
                  if (checks >= maxChecks) break;
                  const old = assignments[index];
                  if (!old) continue;
                  unplace(index);
                  const cands = domains[index]
                      .filter(opt => packConstraintAllows(lessons[index], opt, assignments, lessons) && !conflictsAt(index, opt).length)
                      .sort((a, b) => optionDoubleBonus(index, b) - optionDoubleBonus(index, a))
                      .slice(0, 24);
                  let bestOpt = null;
                  let bestScore = beauty.score;
                  for (const opt of cands) {
                      if (checks >= maxChecks || (limitPerPass != null && checks >= limitPerPass)) break;
                      checks++;
                      place(index, opt);
                      const next = evaluateBeauty(lessons, assignments);
                      if (next.score + 0.05 < bestScore) {
                          bestScore = next.score;
                          bestOpt = opt;
                      }
                      unplace(index);
                  }
                  if (bestOpt) {
                      place(index, bestOpt);
                      beauty = evaluateBeauty(lessons, assignments);
                      improvedLocal = true;
                      moves++;
                  } else {
                      place(index, old);
                  }
              }
              return improvedLocal;
          }

          // A) Relocate
          let improved = true;
          let relocateRounds = 0;
          while (improved && checks < maxChecks && relocateRounds < 10) {
              relocateRounds++;
              improved = relocatePass(null);
          }

          // B) Swap cặp tiết (tạo tiết đôi / giảm gap GV)
          improved = true;
          let swapRounds = 0;
          while (improved && checks < maxChecks && swapRounds < 6) {
              improved = false;
              swapRounds++;
              const placedIdx = lessons.map((_, i) => i).filter(i => assignments[i]);
              for (let ai = 0; ai < placedIdx.length && checks < maxChecks; ai++) {
                  const i = placedIdx[ai];
                  const sample = [];
                  for (let bj = ai + 1; bj < placedIdx.length && sample.length < 36; bj++) {
                      const j = placedIdx[bj];
                      const oi = assignments[i];
                      const oj = assignments[j];
                      if (!oi || !oj) continue;
                      if (oi.day === oj.day || lessons[i].teacherId === lessons[j].teacherId || lessons[i].classId === lessons[j].classId) {
                          sample.push(j);
                      }
                  }
                  for (const j of sample) {
                      checks++;
                      const oi = assignments[i];
                      const oj = assignments[j];
                      const slotForI = domains[i].find(d => d.day === oj.day && d.session === oj.session && d.period === oj.period && d.room === oj.room)
                          || domains[i].find(d => d.day === oj.day && d.session === oj.session && d.period === oj.period);
                      const slotForJ = domains[j].find(d => d.day === oi.day && d.session === oi.session && d.period === oi.period && d.room === oi.room)
                          || domains[j].find(d => d.day === oi.day && d.session === oi.session && d.period === oi.period);
                      if (!slotForI || !slotForJ) continue;

                      unplace(i);
                      unplace(j);
                      let applied = false;
                      if (packConstraintAllows(lessons[i], slotForI, assignments, lessons) && !conflictsAt(i, slotForI).length) {
                          place(i, slotForI);
                          if (packConstraintAllows(lessons[j], slotForJ, assignments, lessons) && !conflictsAt(j, slotForJ).length) {
                              place(j, slotForJ);
                              const next = evaluateBeauty(lessons, assignments);
                              if (next.score + 0.05 < beauty.score) {
                                  beauty = next;
                                  improved = true;
                                  moves++;
                                  applied = true;
                              }
                          }
                      }
                      if (!applied) {
                          if (assignments[i]) unplace(i);
                          if (assignments[j]) unplace(j);
                          place(i, oi);
                          place(j, oj);
                      }
                  }
              }
          }

          // C) Relocate tinh chỉnh
          relocateRounds = 0;
          improved = true;
          while (improved && checks < maxChecks && relocateRounds < 6) {
              relocateRounds++;
              improved = relocatePass(null);
          }

          beauty = evaluateBeauty(lessons, assignments);
          return { assignments, beauty, moves, checks };
      }

      function runMrvFallback() {
          if (bestSolution || lessons.length > 420 || totalNodes > nodeBudget) return null;

          let assignments = new Array(lessons.length).fill(null);
          let classSlotMap = new Map();
          let teacherSlotMap = new Map();
          let roomSlotMap = new Map();
          let subjectDayMap = new Map();
          const maxFallbackNodes = lessons.length > 240 ? 160000 : 260000;
          let fallbackNodes = 0;

          function keysFor(index, option) {
              const lesson = lessons[index];
              return resourceKeys(lesson, option);
          }

          function canPlace(index, option) {
              const keys = keysFor(index, option);
              if (classSlotMap.has(keys.classKey) || teacherSlotMap.has(keys.teacherKey) || roomSlotMap.has(keys.roomKey)) return false;
              if ((subjectDayMap.get(keys.subjectKey)?.size || 0) >= state.rules.maxSameSubjectDay) return false;
              if (!packConstraintAllows(lessons[index], option, assignments, lessons)) return false;
              return true;
          }

          function place(index, option) {
              const keys = keysFor(index, option);
              assignments[index] = option;
              classSlotMap.set(keys.classKey, index);
              teacherSlotMap.set(keys.teacherKey, index);
              roomSlotMap.set(keys.roomKey, index);
              if (!subjectDayMap.has(keys.subjectKey)) subjectDayMap.set(keys.subjectKey, new Set());
              subjectDayMap.get(keys.subjectKey).add(index);
          }

          function unplace(index) {
              const option = assignments[index];
              if (!option) return;
              const keys = keysFor(index, option);
              assignments[index] = null;
              classSlotMap.delete(keys.classKey);
              teacherSlotMap.delete(keys.teacherKey);
              roomSlotMap.delete(keys.roomKey);
              const subjectSet = subjectDayMap.get(keys.subjectKey);
              if (subjectSet) {
                  subjectSet.delete(index);
                  if (!subjectSet.size) subjectDayMap.delete(keys.subjectKey);
              }
          }

          function fallbackCost(index, option) {
              const lesson = lessons[index];
              const classPeriods = [];
              const teacherPeriods = [];
              assignments.forEach((placed, placedIndex) => {
                  if (!placed) return;
                  const other = lessons[placedIndex];
                  if (placed.day === option.day && placed.session === option.session && other.classId === lesson.classId) classPeriods.push(placed.period);
                  if (placed.day === option.day && placed.session === option.session && other.teacherId === lesson.teacherId) teacherPeriods.push(placed.period);
              });
              const classAfter = gapCount([...classPeriods, option.period]);
              const teacherAfter = gapCount([...teacherPeriods, option.period]);
              const sameSubject = subjectDayMap.get(subjectDayKey(lesson, option))?.size || 0;
              return classAfter * 120 + teacherAfter * 80 + sameSubject * 30 + option.period * 0.5;
          }

          function nextIndex() {
              let best = null;
              for (let index = 0; index < lessons.length; index++) {
                  if (assignments[index]) continue;
                  const feasible = domains[index].filter(option => canPlace(index, option));
                  if (!feasible.length) return { index, candidates: [] };
                  const item = { index, candidates: feasible };
                  if (!best || feasible.length < best.candidates.length || (feasible.length === best.candidates.length && domains[index].length < domains[best.index].length)) best = item;
              }
              return best;
          }

          function search() {
              fallbackNodes++;
              totalNodes++;
              deepest = Math.max(deepest, assignments.filter(Boolean).length);
              if (fallbackNodes > maxFallbackNodes || totalNodes > nodeBudget) {
                  rememberPartial(assignments, evaluateBeauty(lessons, assignments));
                  return false;
              }

              const next = nextIndex();
              if (!next) return true;
              if (!next.candidates.length) {
                  bestBlocked = lessons[next.index];
                  rememberPartial(assignments, evaluateBeauty(lessons, assignments));
                  return false;
              }

              const cap = lessons.length > 240 ? 30 : next.candidates.length;
              const candidates = next.candidates
                  .sort((a, b) => fallbackCost(next.index, a) - fallbackCost(next.index, b))
                  .slice(0, cap);

              for (const option of candidates) {
                  place(next.index, option);
                  if (search()) return true;
                  unplace(next.index);
              }
              bestBlocked = lessons[next.index];
              return false;
          }

          const ok = search();
          const beauty = evaluateBeauty(lessons, assignments);
          rememberPartial(assignments, beauty);
          return { ok, assignments: assignments.slice(), nodes: fallbackNodes, placed: assignments.filter(Boolean).length, beauty };
      }

      const fallback = runMrvFallback();
      if (fallback?.ok) {
          bestSolution = fallback.assignments.slice();
          bestBeauty = fallback.beauty;
      }

      // Beautify: large chỉ tinh chỉnh nhẹ (tránh 300s+); small/medium beautify đầy đủ hơn
      if (bestSolution) {
          const beautifyBudget = isHuge ? 0 : isLarge ? 0 : n > 400 ? 4000 : n > 200 ? 12000 : 28000;
          if (beautifyBudget > 0) {
              state._packSoftMode = false;
              const polished = beautifySchedule(bestSolution, beautifyBudget);
              bestSolution = polished.assignments;
              if (state.rules.packFromSessionStart !== false && !isFullyPackValid(lessons, bestSolution)) {
                  const stripped = stripPackViolations(lessons, bestSolution);
                  if (stripped.filter(Boolean).length === lessons.length) bestSolution = stripped;
              }
              bestBeauty = { ...evaluateBeauty(lessons, bestSolution), beautifyMoves: polished.moves };
          } else {
              bestBeauty = { ...evaluateBeauty(lessons, bestSolution), beautifyMoves: 0 };
          }
      } else if (bestPartial) {
          bestPartial = stripPackViolations(lessons, bestPartial);
          bestPartialPlaced = bestPartial.filter(Boolean).length;
          bestBeauty = evaluateBeauty(lessons, bestPartial);
      }

      state._packSoftMode = false;
      const finalAssign = bestSolution || bestPartial || new Array(lessons.length).fill(null);
      // 100% = xếp đủ tiết (hard constraints trùng GV/lớp/phòng). Lủng gói buổi = quality audit.
      const finalOk = !!bestSolution && finalAssign.filter(Boolean).length === lessons.length;

      return {
          ok: finalOk,
          assignments: finalAssign,
          nodes: totalNodes,
          deepest,
          blockedLesson: bestBlocked,
          beauty: bestBeauty || evaluateBeauty(lessons, finalAssign),
      };
  }

  function freezeSolveSnapshot(payload) {
      // Deep clone — đóng băng đúng thời điểm bấm Xếp
      return JSON.parse(JSON.stringify({
          teachers: payload.teachers || [],
          classes: payload.classes || [],
          rooms: payload.rooms || [],
          assignments: payload.assignments || [],
          rules: payload.rules || state.rules,
      }));
  }

  function runSolveOnMainThread(payload) {
      // Fallback: xếp đúng snapshot (không đọc state UI lúc sau)
      const snap = freezeSolveSnapshot(payload);
      const bak = {
          teachers: state.teachers,
          classes: state.classes,
          rooms: state.rooms,
          assignments: state.assignments,
          rules: state.rules,
      };
      try {
          state.teachers = snap.teachers;
          state.classes = snap.classes;
          state.rooms = snap.rooms;
          state.assignments = snap.assignments;
          state.rules = normalizeRules(snap.rules || {});
          const lessons = buildLessonUnits();
          const domains = buildBaseDomains(lessons);
          const precheckIssues = precheckSchedule(lessons, domains);
          if (precheckIssues.length) {
              return {
                  ok: false, status: 'infeasible', precheckIssues, lessons,
                  assignments: null, nodes: 0, deepest: 0, beauty: null, audit: null,
                  total: lessons.length, placed: 0, snapshot: snap,
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
              snapshot: snap,
          };
      } finally {
          state.teachers = bak.teachers;
          state.classes = bak.classes;
          state.rooms = bak.rooms;
          state.assignments = bak.assignments;
          state.rules = bak.rules;
      }
  }

  function runSolveInWorker(payload) {
      return new Promise((resolve, reject) => {
          let worker;
          try {
              worker = new Worker('thoikhoabieu-worker.js?v=20260709');
          } catch (e) {
              reject(e);
              return;
          }
          const requestId = 'r_' + Date.now();
          const timer = setTimeout(() => {
              try { worker.terminate(); } catch { /* */ }
              reject(new Error('Solver worker timeout (10 phút).'));
          }, 600000);
          worker.onmessage = (ev) => {
              const msg = ev.data || {};
              if (msg.requestId !== requestId) return;
              clearTimeout(timer);
              worker.terminate();
              if (!msg.ok) {
                  reject(new Error(msg.error || 'Worker lỗi'));
                  return;
              }
              resolve({ ...msg.result, lessons: msg.lessons, snapshot: payload });
          };
          worker.onerror = (err) => {
              clearTimeout(timer);
              try { worker.terminate(); } catch { /* */ }
              reject(err.error || err);
          };
          worker.postMessage({ type: 'solve', requestId, payload });
      });
  }

  function applySolveOutcome(engineResult, snapshot) {
      const snap = snapshot || engineResult.snapshot || {
          teachers: state.teachers,
          classes: state.classes,
          rooms: state.rooms,
          assignments: state.assignments,
      };
      const classes = Array.isArray(snap.classes) ? snap.classes : state.classes;
      const teachers = Array.isArray(snap.teachers) ? snap.teachers : state.teachers;
      const byClass = {};
      classes.forEach(c => { byClass[c.id] = {}; });
      const lessons = engineResult.lessons || [];
      const teacherLoad = Object.fromEntries(teachers.map(t => [t.id, 0]));
      const issues = [];

      if (engineResult.precheckIssues?.length) {
          state.result = {
              byClass,
              issues: engineResult.precheckIssues,
              generatedAt: new Date().toISOString(),
              teacherLoad: {},
              status: 'infeasible',
              solver: { nodes: 0, deepest: 0, total: engineResult.total || lessons.length },
              hard: { ok: false, label: 'Không hợp lệ' },
              soft: { ok: false, label: '—' },
              snapshot: snap,
          };
          state.activeResult = 'issues';
          document.querySelectorAll('#resultTabs .result-tab, #resultTabs .tab-btn').forEach(b => b.classList.toggle('active', b.dataset.result === 'issues'));
          goStep('result');
          renderResultControls();
          renderSchedule();
          showDataNotice(`Precheck hard: ${engineResult.precheckIssues.length} lỗi chặn xếp.`, 'err');
          return;
      }

      const solvedAssign = engineResult.assignments || [];
      if (solvedAssign.some(Boolean)) {
          lessons.forEach((lesson, index) => {
              const option = solvedAssign[index];
              if (!option) return;
              const cell = {
                  ...lesson,
                  day: option.day,
                  session: option.session,
                  period: option.period,
                  slotKey: option.key || `${option.day}-${option.session}-${option.period}`,
                  room: option.room,
              };
              if (!byClass[lesson.classId]) byClass[lesson.classId] = {};
              byClass[lesson.classId][cell.slotKey] = cell;
              teacherLoad[lesson.teacherId] = (teacherLoad[lesson.teacherId] || 0) + 1;
          });
      } else {
          const blocked = engineResult.blockedLesson;
          issues.push(makeIssue(
              blocked
                  ? `Không xếp được. Nghẽn: ${blocked.subject} - ${blocked.className} (${blocked.teacherName}).`
                  : 'Không xếp được với ràng buộc hard hiện tại.'
          ));
      }

      const placed = engineResult.placed ?? solvedAssign.filter(Boolean).length;
      const total = engineResult.total || lessons.length;
      if (!engineResult.ok && !issues.length) {
          issues.push(makeIssue(`Chưa đủ 100% hard: ${placed}/${total} tiết.`));
      }

      const audit = engineResult.audit || { classHoles: 0, startLate: 0, teacherGaps: 0, teacherOrphans: 0, ok: true, messages: [] };
      const qualityIssues = (audit.messages || []).map(m => makeIssue(
          (m.severity === 'error' ? '⛔ [Đẹp] ' : '⚠️ [Đẹp] ') + m.message,
          m.severity === 'error' ? 'quality-error' : 'quality-warn'
      ));
      issues.push(...qualityIssues.filter(i => i.type === 'quality-error').slice(0, 30));
      issues.push(...qualityIssues.filter(i => i.type === 'quality-warn').slice(0, 25));

      const full = !!engineResult.ok && placed === total;
      const softOk = !!audit.ok && !(audit.teacherOrphans > 0) && !(audit.teacherGaps > 0);
      state.result = {
          byClass,
          issues,
          generatedAt: new Date().toISOString(),
          teacherLoad,
          status: full ? 'complete' : (placed > 0 ? 'partial' : 'infeasible'),
          solver: { nodes: engineResult.nodes, deepest: engineResult.deepest, total, ms: engineResult.ms },
          beauty: engineResult.beauty,
          audit,
          snapshot: snap,
          hard: {
              ok: full,
              label: full ? 'Hợp lệ 100%' : (placed > 0 ? `Thiếu ${total - placed} tiết` : 'Không hợp lệ'),
          },
          soft: {
              ok: softOk,
              label: softOk ? 'Đẹp OK' : `Lủng ${audit.classHoles || 0}/đầu ${audit.startLate || 0}/mồ côi ${audit.teacherOrphans || 0}`,
          },
      };
      state.activeResult = full ? (softOk ? 'class' : 'issues') : 'issues';
      document.querySelectorAll('#resultTabs .result-tab, #resultTabs .tab-btn').forEach(b => b.classList.toggle('active', b.dataset.result === state.activeResult));
      renderResultControls();
      // Chọn lớp từ snapshot (đóng băng lúc xếp), map sang state.classes nếu còn
      const firstClassId = classes[0]?.id;
      if ($('viewSelector') && firstClassId && state.activeResult === 'class') {
          const stillThere = state.classes.some(c => c.id === firstClassId);
          $('viewSelector').value = stillThere ? firstClassId : (state.classes[0]?.id || 'all');
      }
      goStep('result');
      renderSchedule();
      updateStats();
      const msTxt = engineResult.ms != null ? ` (${Math.round(engineResult.ms / 1000)}s)` : '';
      showDataNotice(
          full
              ? `✅ Hard: 100% (${placed}/${total})${msTxt}. Soft: ${state.result.soft.label}.`
              : `⛔ Hard: ${placed}/${total}${msTxt}. Soft: ${state.result.soft.label}.`,
          full ? (softOk ? 'ok' : 'warn') : 'err'
      );
  }

  

function curriculumCt2018(grade) {
      const base = [
          { subject: 'Ngữ văn', periods: 4 },
          { subject: 'Toán', periods: 4 },
          { subject: 'Ngoại ngữ 1', periods: 3 },
          { subject: 'Giáo dục công dân', periods: 1 },
          { subject: 'Công nghệ', periods: 1, roomNeed: 'Công nghệ' },
          { subject: 'Tin học', periods: 1, roomNeed: 'Tin học' },
          { subject: 'Giáo dục thể chất', periods: 2, roomNeed: 'Thể dục' },
          { subject: 'Âm nhạc', periods: 1 },
          { subject: 'Mỹ thuật', periods: 1 },
          { subject: 'HĐTN-HN', periods: 2 },
          { subject: 'Sinh hoạt', periods: 1 },
      ];
      if (grade <= 7) {
          return [
              ...base,
              { subject: 'Lịch sử', periods: 1 },
              { subject: 'Địa lí', periods: 2 },
              // KHTN: không ép phòng BM cả 4 tiết (16 lớp×4=64 > 2 phòng×30 ô) — dùng phòng lớp
              { subject: 'Khoa học tự nhiên', periods: 4, roomNeed: '' },
          ];
      }
      return [
          ...base,
          { subject: 'Lịch sử', periods: 2 },
          { subject: 'Địa lí', periods: 1 },
          { subject: 'Vật lí', periods: 1, roomNeed: 'Vật lí' },
          { subject: 'Hóa học', periods: 2, roomNeed: 'Hóa học' },
          { subject: 'Sinh học', periods: 1, roomNeed: 'Sinh học' },
      ];
  }

  function classGrade(name) {
      const m = String(name || '').match(/^(\d+)/);
      return m ? Number(m[1]) : 6;
  }

  

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
