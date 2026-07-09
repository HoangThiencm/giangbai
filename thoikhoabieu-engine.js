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

      /**
       * Large: xếp theo Ô (ngày×buổi×tiết) — mọi lớp đồng thời.
       * Ưu tiên gói từ tiết đầu + dồn GV; multi-seed; residual + 1-hop repair.
       * Không rơi CSP sâu 840 biến (quá chậm).
       */
      function solveBySlotScan(seed = 0) {
          const assignments = new Array(lessons.length).fill(null);
          const teacherBusy = new Set();
          const roomBusy = new Set();
          const classBusy = new Set();
          const subjectDay = new Map();
          const remaining = new Set();
          let nodes = 0;

          const byClass = new Map();
          lessons.forEach((l, i) => {
              remaining.add(i);
              if (!byClass.has(l.classId)) byClass.set(l.classId, []);
              byClass.get(l.classId).push(i);
          });
          // Đếm số tiết cùng môn trong lớp (ưu tiên môn nhiều tiết như KHTN/Toán)
          const subjectCountInClass = new Map();
          byClass.forEach((idxs, cid) => {
              idxs.forEach(i => {
                  const k = `${cid}|${normalizeText(lessons[i].subject)}`;
                  subjectCountInClass.set(k, (subjectCountInClass.get(k) || 0) + 1);
              });
              idxs.sort((a, b) => {
                  const ra = lessons[a].roomNeed ? 0 : 1;
                  const rb = lessons[b].roomNeed ? 0 : 1;
                  const sa = subjectCountInClass.get(`${cid}|${normalizeText(lessons[a].subject)}`) || 0;
                  const sb = subjectCountInClass.get(`${cid}|${normalizeText(lessons[b].subject)}`) || 0;
                  return ra - rb || sb - sa || domains[a].length - domains[b].length;
              });
          });

          const days = state.rules.days || ['T2', 'T3', 'T4', 'T5', 'T6', 'T7'];
          const classDayCount = new Map();
          const classTargets = new Map();
          byClass.forEach((idxs, cid) => {
              const n = idxs.length;
              const base = days.map((_, d) => Math.floor(n / days.length) + (d < (n % days.length) ? 1 : 0));
              const rot = seed % days.length;
              const rotated = base.slice(rot).concat(base.slice(0, rot));
              classTargets.set(cid, Object.fromEntries(days.map((d, i) => [d, rotated[i]])));
          });

          // index ô → lesson (để repair O(1))
          const teacherAt = new Map();
          const roomAt = new Map();

          function sessionsFor(cid) {
              const cl = state.classes.find(c => c.id === cid);
              return cl?.shift === 'both' ? ['morning', 'afternoon'] : [cl?.shift || 'morning'];
          }

          function canPlace(index, opt) {
              const L = lessons[index];
              if (teacherBusy.has(`${L.teacherId}|${opt.day}|${opt.session}|${opt.period}`)) return false;
              if (roomBusy.has(`${opt.room}|${opt.day}|${opt.session}|${opt.period}`)) return false;
              if (classBusy.has(`${L.classId}|${opt.day}|${opt.session}|${opt.period}`)) return false;
              const sk = `${L.classId}|${normalizeText(L.subject)}|${opt.day}`;
              if ((subjectDay.get(sk) || 0) >= state.rules.maxSameSubjectDay) return false;
              return true;
          }

          function placeAt(index, opt) {
              const L = lessons[index];
              assignments[index] = opt;
              const tk = `${L.teacherId}|${opt.day}|${opt.session}|${opt.period}`;
              const rk = `${opt.room}|${opt.day}|${opt.session}|${opt.period}`;
              teacherBusy.add(tk);
              roomBusy.add(rk);
              classBusy.add(`${L.classId}|${opt.day}|${opt.session}|${opt.period}`);
              teacherAt.set(tk, index);
              roomAt.set(rk, index);
              const sk = `${L.classId}|${normalizeText(L.subject)}|${opt.day}`;
              subjectDay.set(sk, (subjectDay.get(sk) || 0) + 1);
              classDayCount.set(`${L.classId}|${opt.day}`, (classDayCount.get(`${L.classId}|${opt.day}`) || 0) + 1);
              remaining.delete(index);
              nodes++;
          }

          function unplaceAt(index) {
              const opt = assignments[index];
              if (!opt) return;
              const L = lessons[index];
              const tk = `${L.teacherId}|${opt.day}|${opt.session}|${opt.period}`;
              const rk = `${opt.room}|${opt.day}|${opt.session}|${opt.period}`;
              teacherBusy.delete(tk);
              roomBusy.delete(rk);
              classBusy.delete(`${L.classId}|${opt.day}|${opt.session}|${opt.period}`);
              if (teacherAt.get(tk) === index) teacherAt.delete(tk);
              if (roomAt.get(rk) === index) roomAt.delete(rk);
              const sk = `${L.classId}|${normalizeText(L.subject)}|${opt.day}`;
              const sc = (subjectDay.get(sk) || 1) - 1;
              if (sc <= 0) subjectDay.delete(sk); else subjectDay.set(sk, sc);
              const dk = `${L.classId}|${opt.day}`;
              const dc = (classDayCount.get(dk) || 1) - 1;
              if (dc <= 0) classDayCount.delete(dk); else classDayCount.set(dk, dc);
              assignments[index] = null;
              remaining.add(index);
          }

          function tryReplaceAnywhere(index) {
              let best = null;
              for (const opt of domains[index]) {
                  if (!canPlace(index, opt)) continue;
                  const sc = scoreOption(index, opt);
                  if (!best || sc < best.sc) best = { opt, sc };
              }
              if (best) {
                  placeAt(index, best.opt);
                  return true;
              }
              return false;
          }

          function scoreOption(index, opt) {
              const L = lessons[index];
              let score = opt.period * 1.2 + (opt.session === 'afternoon' ? 4 : 0);
              if (L.roomNeed) score -= 10;
              const subjN = subjectCountInClass.get(`${L.classId}|${normalizeText(L.subject)}`) || 1;
              if (subjN >= 3) score -= 6; // ưu tiên môn nhiều tiết
              let tAdj = false;
              let tCount = 0;
              let cAdj = false;
              let cPeriods = [];
              let sAdj = false;
              for (let j = 0; j < assignments.length; j++) {
                  const o = assignments[j];
                  if (!o) continue;
                  const Lj = lessons[j];
                  if (Lj.teacherId === L.teacherId && o.day === opt.day && o.session === opt.session) {
                      tCount++;
                      if (Math.abs(o.period - opt.period) === 1) tAdj = true;
                  }
                  if (Lj.classId === L.classId && o.day === opt.day && o.session === opt.session) {
                      cPeriods.push(o.period);
                      if (Math.abs(o.period - opt.period) === 1) cAdj = true;
                      if (normalizeText(Lj.subject) === normalizeText(L.subject) && Math.abs(o.period - opt.period) === 1) sAdj = true;
                  }
              }
              if (tCount > 0) score -= 12 + Math.min(4, tCount) * 3;
              if (tAdj) score -= 24;
              if (cAdj) score -= 18;
              if (sAdj) score -= 16;
              // Cân tải ngày môn: tránh 2 tiết xong rồi kẹt maxSameSubjectDay
              const sk = `${L.classId}|${normalizeText(L.subject)}|${opt.day}`;
              const daySub = subjectDay.get(sk) || 0;
              if (daySub === 1 && subjN >= 3) score -= 8; // ghép đôi
              if (daySub === 0 && subjN >= 3) score -= 3;
              const start = effectiveSessionStart(opt.day, opt.session);
              // Pack lớp là ưu tiên soft #1 (tránh holes/startLate lúc hard fill)
              if (!cPeriods.length) {
                  score += opt.period === start ? -80 : 90 + (opt.period - start) * 35;
              } else {
                  const minP = Math.min(...cPeriods);
                  const maxP = Math.max(...cPeriods);
                  if (opt.period === maxP + 1 || opt.period === minP - 1) score -= 55;
                  else if (opt.period > maxP + 1 || opt.period < minP - 1) score += 120;
                  if (minP > start) score += 70;
                  // phạt lỗ nếu chèn giữa không kề
                  if (opt.period > minP && opt.period < maxP && !cPeriods.includes(opt.period - 1) && !cPeriods.includes(opt.period + 1)) {
                      score += 40;
                  }
              }
              // jitter seed
              score += ((seed * 19 + index * 7 + opt.period * 3 + opt.day.charCodeAt(1)) % 9) * 0.15;
              return score;
          }

          // Phase 1: fill theo ô — mọi lớp đồng thời, gói từ tiết đầu (score pack nặng)
          const dayOrder = seed % 2 ? days.slice().reverse() : days.slice();
          for (const day of dayOrder) {
              for (const session of ['morning', 'afternoon']) {
                  const { from, to } = sessionPeriodRange(session);
                  for (let p = from; p <= to; p++) {
                      let classIds = Array.from(byClass.keys()).filter(cid => {
                          if (!sessionsFor(cid).includes(session)) return false;
                          if (classBusy.has(`${cid}|${day}|${session}|${p}`)) return false;
                          if (!byClass.get(cid).some(i => remaining.has(i))) return false;
                          const placedDay = classDayCount.get(`${cid}|${day}`) || 0;
                          const target = classTargets.get(cid)?.[day] ?? 99;
                          return placedDay < target;
                      });
                      classIds.sort((a, b) => {
                          const ra = byClass.get(a).filter(i => remaining.has(i)).length;
                          const rb = byClass.get(b).filter(i => remaining.has(i)).length;
                          const ja = (seed * 13 + a.charCodeAt(0) + p * 3) % 11;
                          const jb = (seed * 17 + b.charCodeAt(0) + p * 5) % 11;
                          return rb - ra || ja - jb;
                      });
                      if (classIds.length) {
                          const off = (seed * 3 + p + day.charCodeAt(1)) % classIds.length;
                          classIds = classIds.slice(off).concat(classIds.slice(0, off));
                      }
                      for (const cid of classIds) {
                          let best = null;
                          for (const idx of byClass.get(cid)) {
                              if (!remaining.has(idx)) continue;
                              for (const opt of domains[idx]) {
                                  if (opt.day !== day || opt.session !== session || opt.period !== p) continue;
                                  if (!canPlace(idx, opt)) continue;
                                  const sc = scoreOption(idx, opt);
                                  if (!best || sc < best.sc) best = { idx, opt, sc };
                              }
                          }
                          if (best) placeAt(best.idx, best.opt);
                      }
                  }
              }
          }

          // Phase 2: residual — ưu tiên ô giữ gói lớp; chỉ nới khi không còn lựa chọn
          function residualPass(packOnly = false) {
              const residual = Array.from(remaining).sort((a, b) => {
                  const sa = subjectCountInClass.get(`${lessons[a].classId}|${normalizeText(lessons[a].subject)}`) || 0;
                  const sb = subjectCountInClass.get(`${lessons[b].classId}|${normalizeText(lessons[b].subject)}`) || 0;
                  return sb - sa || domains[a].length - domains[b].length;
              });
              for (const idx of residual) {
                  const L = lessons[idx];
                  let bestPack = null;
                  let bestAny = null;
                  for (const opt of domains[idx]) {
                      if (!canPlace(idx, opt)) continue;
                      const sc = scoreOption(idx, opt);
                      if (!bestAny || sc < bestAny.sc) bestAny = { opt, sc };
                      // kiểm tra gói sau khi thêm
                      const periods = [];
                      assignments.forEach((o, j) => {
                          if (!o || lessons[j].classId !== L.classId) return;
                          if (o.day === opt.day && o.session === opt.session) periods.push(o.period);
                      });
                      periods.push(opt.period);
                      const list = uniqueSortedPeriods(periods);
                      const start = effectiveSessionStart(opt.day, opt.session);
                      const packOk = list[0] === start && gapCountInSession(opt.day, opt.session, list) === 0;
                      if (packOk && (!bestPack || sc < bestPack.sc)) bestPack = { opt, sc };
                  }
                  const pick = bestPack || (packOnly ? null : bestAny);
                  if (pick) placeAt(idx, pick.opt);
              }
          }
          residualPass(true);  // chỉ gói
          residualPass(false); // nới nếu còn

          // Phase 3: repair — gỡ 1–2 tiết chặn (GV/phòng), xếp lại
          function repairPass(maxHops = 2) {
              for (const idx of Array.from(remaining)) {
                  const pool = domains[idx].slice().sort((a, b) => {
                      const sa = scoreOption(idx, a);
                      const sb = scoreOption(idx, b);
                      return sa - sb;
                  });
                  let done = false;
                  for (const opt of pool) {
                      if (done) break;
                      const L = lessons[idx];
                      if (classBusy.has(`${L.classId}|${opt.day}|${opt.session}|${opt.period}`)) continue;
                      const sk = `${L.classId}|${normalizeText(L.subject)}|${opt.day}`;
                      if ((subjectDay.get(sk) || 0) >= state.rules.maxSameSubjectDay) continue;
                      const tk = `${L.teacherId}|${opt.day}|${opt.session}|${opt.period}`;
                      const rk = `${opt.room}|${opt.day}|${opt.session}|${opt.period}`;
                      if (canPlace(idx, opt)) {
                          placeAt(idx, opt);
                          done = true;
                          break;
                      }
                      const conflicts = [];
                      if (teacherBusy.has(tk)) {
                          const j = teacherAt.get(tk);
                          if (j !== undefined && j !== idx) conflicts.push(j);
                      }
                      if (roomBusy.has(rk)) {
                          const j = roomAt.get(rk);
                          if (j !== undefined && j !== idx && !conflicts.includes(j)) conflicts.push(j);
                      }
                      if (!conflicts.length || conflicts.length > maxHops) continue;

                      const saved = conflicts.map(j => ({ j, opt: assignments[j] }));
                      conflicts.forEach(unplaceAt);
                      if (!canPlace(idx, opt)) {
                          saved.forEach(s => placeAt(s.j, s.opt));
                          continue;
                      }
                      placeAt(idx, opt);
                      let allRe = true;
                      for (const s of saved) {
                          if (!tryReplaceAnywhere(s.j)) {
                              allRe = false;
                              break;
                          }
                      }
                      if (allRe) {
                          done = true;
                      } else {
                          // rollback chain
                          unplaceAt(idx);
                          saved.forEach(s => {
                              if (assignments[s.j]) unplaceAt(s.j);
                          });
                          saved.forEach(s => placeAt(s.j, s.opt));
                      }
                  }
              }
          }
          repairPass(1);
          residualPass();
          repairPass(2);

          // Phase 4: class-slot steal — gỡ tiết “mềm” cùng lớp (môn 1 tiết) để nhường ô cho môn kẹt
          if (remaining.size) {
              for (const idx of Array.from(remaining)) {
                  const L = lessons[idx];
                  const softVictims = [];
                  assignments.forEach((opt, j) => {
                      if (!opt || lessons[j].classId !== L.classId) return;
                      const sn = subjectCountInClass.get(`${L.classId}|${normalizeText(lessons[j].subject)}`) || 1;
                      if (sn <= 2 && !lessons[j].roomNeed) softVictims.push(j);
                  });
                  let placedIdx = false;
                  for (const vj of softVictims) {
                      if (placedIdx) break;
                      const vOpt = assignments[vj];
                      if (!vOpt) continue;
                      const match = domains[idx].find(o =>
                          o.day === vOpt.day && o.session === vOpt.session && o.period === vOpt.period
                      );
                      if (!match) continue;
                      unplaceAt(vj);
                      if (canPlace(idx, match)) {
                          placeAt(idx, match);
                          if (tryReplaceAnywhere(vj)) {
                              placedIdx = true;
                          } else {
                              unplaceAt(idx);
                              placeAt(vj, vOpt);
                          }
                      } else {
                          const tk = `${L.teacherId}|${match.day}|${match.session}|${match.period}`;
                          const rk = `${match.room}|${match.day}|${match.session}|${match.period}`;
                          const conf = [];
                          if (teacherBusy.has(tk) && teacherAt.has(tk)) conf.push(teacherAt.get(tk));
                          if (roomBusy.has(rk) && roomAt.has(rk)) {
                              const rj = roomAt.get(rk);
                              if (!conf.includes(rj)) conf.push(rj);
                          }
                          if (conf.length === 1) {
                              const cj = conf[0];
                              const cOpt = assignments[cj];
                              unplaceAt(cj);
                              if (canPlace(idx, match)) {
                                  placeAt(idx, match);
                                  const okV = tryReplaceAnywhere(vj);
                                  const okC = tryReplaceAnywhere(cj);
                                  if (okV && okC) placedIdx = true;
                                  else {
                                      if (assignments[idx]) unplaceAt(idx);
                                      if (assignments[vj]) unplaceAt(vj);
                                      if (assignments[cj]) unplaceAt(cj);
                                      placeAt(vj, vOpt);
                                      placeAt(cj, cOpt);
                                  }
                              } else {
                                  placeAt(cj, cOpt);
                                  placeAt(vj, vOpt);
                              }
                          } else {
                              placeAt(vj, vOpt);
                          }
                      }
                  }
              }
              residualPass();
              repairPass(2);
          }

          // Phase 5: chain repair đệ quy (độ sâu 3) — đẩy dồn conflict GV/phòng
          if (remaining.size) {
              function tryPlaceChain(index, depth, taboo) {
                  if (assignments[index]) return true;
                  nodes++;
                  const ordered = domains[index].slice().sort((a, b) => a.period - b.period || a.day.localeCompare(b.day));
                  // ưu tiên ô không conflict
                  const freeFirst = [];
                  const needDisplace = [];
                  for (const opt of ordered) {
                      const L = lessons[index];
                      if (classBusy.has(`${L.classId}|${opt.day}|${opt.session}|${opt.period}`)) continue;
                      const sk = `${L.classId}|${normalizeText(L.subject)}|${opt.day}`;
                      if ((subjectDay.get(sk) || 0) >= state.rules.maxSameSubjectDay) continue;
                      if (canPlace(index, opt)) freeFirst.push(opt);
                      else needDisplace.push(opt);
                  }
                  for (const opt of freeFirst) {
                      placeAt(index, opt);
                      return true;
                  }
                  if (depth <= 0) return false;
                  for (const opt of needDisplace) {
                      const L = lessons[index];
                      const tk = `${L.teacherId}|${opt.day}|${opt.session}|${opt.period}`;
                      const rk = `${opt.room}|${opt.day}|${opt.session}|${opt.period}`;
                      const confs = [];
                      if (teacherBusy.has(tk)) {
                          const j = teacherAt.get(tk);
                          if (j !== undefined && j !== index && !taboo.has(j)) confs.push(j);
                      }
                      if (roomBusy.has(rk)) {
                          const j = roomAt.get(rk);
                          if (j !== undefined && j !== index && !taboo.has(j) && !confs.includes(j)) confs.push(j);
                      }
                      if (!confs.length || confs.length > 2) continue;
                      const saved = confs.map(j => ({ j, opt: Object.assign({}, assignments[j]) }));
                      confs.forEach(unplaceAt);
                      if (!canPlace(index, opt)) {
                          saved.forEach(s => placeAt(s.j, s.opt));
                          continue;
                      }
                      placeAt(index, opt);
                      const nextTaboo = new Set(taboo);
                      nextTaboo.add(index);
                      let ok = true;
                      for (const s of saved) {
                          if (!tryPlaceChain(s.j, depth - 1, nextTaboo)) {
                              ok = false;
                              break;
                          }
                      }
                      if (ok) return true;
                      unplaceAt(index);
                      saved.forEach(s => {
                          if (assignments[s.j]) unplaceAt(s.j);
                      });
                      saved.forEach(s => placeAt(s.j, s.opt));
                  }
                  return false;
              }

              for (let round = 0; round < 4 && remaining.size; round++) {
                  for (const idx of Array.from(remaining)) {
                      tryPlaceChain(idx, 3, new Set([idx]));
                  }
                  // nếu còn: gỡ tạm 1 tiết cùng lớp (bất kỳ, ưu tiên môn 1 tiết) rồi chain lại
                  if (remaining.size) {
                      for (const idx of Array.from(remaining)) {
                          const L = lessons[idx];
                          const victims = [];
                          assignments.forEach((opt, j) => {
                              if (!opt || lessons[j].classId !== L.classId) return;
                              const sn = subjectCountInClass.get(`${L.classId}|${normalizeText(lessons[j].subject)}`) || 1;
                              victims.push({ j, sn, room: !!lessons[j].roomNeed });
                          });
                          victims.sort((a, b) => (a.room ? 1 : 0) - (b.room ? 1 : 0) || a.sn - b.sn);
                          let done = false;
                          for (const v of victims.slice(0, 8)) {
                              if (done) break;
                              const vOpt = assignments[v.j];
                              if (!vOpt) continue;
                              unplaceAt(v.j);
                              if (tryPlaceChain(idx, 3, new Set([idx, v.j]))) {
                                  if (tryPlaceChain(v.j, 3, new Set([idx, v.j]))) {
                                      done = true;
                                  } else if (assignments[idx]) {
                                      // idx đã vào, victim chưa — thử residual victim
                                      if (!tryReplaceAnywhere(v.j)) {
                                          unplaceAt(idx);
                                          placeAt(v.j, vOpt);
                                      } else done = true;
                                  } else {
                                      placeAt(v.j, vOpt);
                                  }
                              } else {
                                  placeAt(v.j, vOpt);
                              }
                          }
                      }
                  }
              }
          }

          const placed = lessons.length - remaining.size;
          return {
              ok: remaining.size === 0,
              assignments,
              nodes,
              placed,
              unplaced: Array.from(remaining),
          };
      }

      /**
       * Pass ưu tiên sau hard large: đóng lủng lớp + trống tiết đầu (giữ đủ tiết hard).
       * Chiến lược: recompact buổi → slide lấp lỗ → kéo tiết từ ngày khác → đẩy overflow.
       */
      function repairClassPack(assignments, maxMoves = 12000) {
          if (state.rules.packFromSessionStart === false) {
              return { assignments: assignments.slice(), moves: 0 };
          }
          const arr = assignments.slice();
          let moves = 0;

          function mapsFrom(arr0) {
              const tBusy = new Set();
              const cBusy = new Set();
              const rBusy = new Set();
              const subj = new Map();
              arr0.forEach((opt, i) => {
                  if (!opt) return;
                  const L = lessons[i];
                  tBusy.add(`${L.teacherId}|${opt.day}|${opt.session}|${opt.period}`);
                  cBusy.add(`${L.classId}|${opt.day}|${opt.session}|${opt.period}`);
                  rBusy.add(`${opt.room}|${opt.day}|${opt.session}|${opt.period}`);
                  const sk = `${L.classId}|${normalizeText(L.subject)}|${opt.day}`;
                  subj.set(sk, (subj.get(sk) || 0) + 1);
              });
              return { tBusy, cBusy, rBusy, subj };
          }

          function unplaceMaps(i, maps) {
              const opt = arr[i];
              if (!opt) return;
              const L = lessons[i];
              maps.tBusy.delete(`${L.teacherId}|${opt.day}|${opt.session}|${opt.period}`);
              maps.cBusy.delete(`${L.classId}|${opt.day}|${opt.session}|${opt.period}`);
              maps.rBusy.delete(`${opt.room}|${opt.day}|${opt.session}|${opt.period}`);
              const sk = `${L.classId}|${normalizeText(L.subject)}|${opt.day}`;
              const sc = (maps.subj.get(sk) || 1) - 1;
              if (sc <= 0) maps.subj.delete(sk); else maps.subj.set(sk, sc);
              arr[i] = null;
          }

          function placeMaps(i, opt, maps) {
              const L = lessons[i];
              arr[i] = opt;
              maps.tBusy.add(`${L.teacherId}|${opt.day}|${opt.session}|${opt.period}`);
              maps.cBusy.add(`${L.classId}|${opt.day}|${opt.session}|${opt.period}`);
              maps.rBusy.add(`${opt.room}|${opt.day}|${opt.session}|${opt.period}`);
              const sk = `${L.classId}|${normalizeText(L.subject)}|${opt.day}`;
              maps.subj.set(sk, (maps.subj.get(sk) || 0) + 1);
          }

          function canHard(i, opt, maps) {
              const L = lessons[i];
              if (maps.tBusy.has(`${L.teacherId}|${opt.day}|${opt.session}|${opt.period}`)) return false;
              if (maps.cBusy.has(`${L.classId}|${opt.day}|${opt.session}|${opt.period}`)) return false;
              if (maps.rBusy.has(`${opt.room}|${opt.day}|${opt.session}|${opt.period}`)) return false;
              const sk = `${L.classId}|${normalizeText(L.subject)}|${opt.day}`;
              if ((maps.subj.get(sk) || 0) >= state.rules.maxSameSubjectDay) return false;
              return true;
          }

          function sessionIdxs(classId, day, session) {
              const idxs = [];
              arr.forEach((opt, i) => {
                  if (opt && lessons[i].classId === classId && opt.day === day && opt.session === session) idxs.push(i);
              });
              return idxs;
          }

          function sessionPacked(classId, day, session) {
              const idxs = sessionIdxs(classId, day, session);
              if (!idxs.length) return true;
              const list = uniqueSortedPeriods(idxs.map(i => arr[i].period));
              const start = effectiveSessionStart(day, session);
              return list[0] === start && gapCountInSession(day, session, list) === 0;
          }

          function classSessionPackOk(arr0, classId, day, session) {
              const periods = [];
              arr0.forEach((opt, j) => {
                  if (!opt || lessons[j].classId !== classId) return;
                  if (opt.day === day && opt.session === session) periods.push(opt.period);
              });
              if (!periods.length) return true;
              const list = uniqueSortedPeriods(periods);
              const start = effectiveSessionStart(day, session);
              return list[0] === start && gapCountInSession(day, session, list) === 0;
          }

          function findTeacherAt(maps, teacherId, day, session, period) {
              const key = `${teacherId}|${day}|${session}|${period}`;
              if (!maps.tBusy.has(key)) return -1;
              for (let j = 0; j < arr.length; j++) {
                  if (!arr[j] || lessons[j].teacherId !== teacherId) continue;
                  if (arr[j].day === day && arr[j].session === session && arr[j].period === period) return j;
              }
              return -1;
          }

          function findRoomAt(maps, room, day, session, period) {
              const key = `${room}|${day}|${session}|${period}`;
              if (!maps.rBusy.has(key)) return -1;
              for (let j = 0; j < arr.length; j++) {
                  if (!arr[j] || arr[j].room !== room) continue;
                  if (arr[j].day === day && arr[j].session === session && arr[j].period === period) return j;
              }
              return -1;
          }

          /**
           * Thử đặt i tại opt; nếu kẹt GV/phòng thì gỡ 1 conflict và xếp lại.
           * loose=false: re-place conflict phải giữ pack lớp conflict.
           * loose=true: chấp nhận re-place free bất kỳ (lớp conflict có thể lủng tạm — vòng sau sửa).
           */
          function placeWithDisplace(i, opt, maps, taboo, loose = false) {
              if (canHard(i, opt, maps)) {
                  placeMaps(i, opt, maps);
                  return true;
              }
              const L = lessons[i];
              if (maps.cBusy.has(`${L.classId}|${opt.day}|${opt.session}|${opt.period}`)) return false;
              const sk = `${L.classId}|${normalizeText(L.subject)}|${opt.day}`;
              if ((maps.subj.get(sk) || 0) >= state.rules.maxSameSubjectDay) return false;

              const confs = [];
              const tj = findTeacherAt(maps, L.teacherId, opt.day, opt.session, opt.period);
              if (tj >= 0 && tj !== i && !taboo.has(tj)) confs.push(tj);
              const rj = findRoomAt(maps, opt.room, opt.day, opt.session, opt.period);
              if (rj >= 0 && rj !== i && !taboo.has(rj) && !confs.includes(rj)) confs.push(rj);
              if (confs.length !== 1) return false;

              const cj = confs[0];
              const cSaved = { ...arr[cj] };
              unplaceMaps(cj, maps);
              if (!canHard(i, opt, maps)) {
                  placeMaps(cj, cSaved, maps);
                  return false;
              }
              placeMaps(i, opt, maps);
              let bestStrict = null;
              let bestLoose = null;
              for (const o2 of domains[cj]) {
                  if (!canHard(cj, o2, maps)) continue;
                  placeMaps(cj, o2, maps);
                  const packNew = classSessionPackOk(arr, lessons[cj].classId, o2.day, o2.session);
                  const packOld = (o2.day === cSaved.day && o2.session === cSaved.session)
                      || classSessionPackOk(arr, lessons[cj].classId, cSaved.day, cSaved.session);
                  unplaceMaps(cj, maps);
                  const sc = o2.period
                      + (o2.day === cSaved.day && o2.session === cSaved.session ? -5 : 0);
                  if (packNew && packOld) {
                      if (!bestStrict || sc < bestStrict.sc) bestStrict = { opt: o2, sc };
                  } else if (loose) {
                      if (!bestLoose || sc < bestLoose.sc) bestLoose = { opt: o2, sc };
                  }
              }
              const bestRe = bestStrict || (loose ? bestLoose : null);
              if (bestRe) {
                  placeMaps(cj, bestRe.opt, maps);
                  return true;
              }
              unplaceMaps(i, maps);
              placeMaps(cj, cSaved, maps);
              return false;
          }

          /** Recompact: gỡ cả buổi lớp, lấp liên tục từ tiết đầu (+1-hop displace). */
          function recompactSession(classId, day, session) {
              const idxs = sessionIdxs(classId, day, session);
              if (idxs.length <= 1) {
                  if (idxs.length === 1) {
                      const start = effectiveSessionStart(day, session);
                      if (arr[idxs[0]].period === start) return true;
                      const maps = mapsFrom(arr);
                      const i = idxs[0];
                      const old = arr[i];
                      unplaceMaps(i, maps);
                      let ok = false;
                      for (const cand of domains[i]) {
                          if (cand.day !== day || cand.session !== session || cand.period !== start) continue;
                          if (placeWithDisplace(i, cand, maps, new Set([i]))) {
                              moves++;
                              ok = true;
                              break;
                          }
                      }
                      if (!ok) placeMaps(i, old, maps);
                      return ok;
                  }
                  return true;
              }
              if (sessionPacked(classId, day, session)) return true;

              const snapAll = arr.map(o => (o ? { ...o } : null));
              const movesBefore = moves;
              const maps = mapsFrom(arr);
              const saved = idxs.map(i => ({ i, opt: { ...arr[i] } }));
              idxs.forEach(i => unplaceMaps(i, maps));

              const start = effectiveSessionStart(day, session);
              const { to } = sessionPeriodRange(session);
              const blocked = schoolBlockedSet();
              const rem = new Set(idxs);
              const taboo = new Set(idxs);
              let localMoves = 0;

              for (let p = start; p <= to && rem.size; p++) {
                  if (isSlotBlockedBySet(blocked, { day, session, period: p })) continue;
                  let placed = false;
                  let best = null;
                  for (const i of rem) {
                      for (const cand of domains[i]) {
                          if (cand.day !== day || cand.session !== session || cand.period !== p) continue;
                          if (!canHard(i, cand, maps)) continue;
                          const prev = saved.find(s => s.i === i);
                          let sc = 0;
                          if (prev && prev.opt.room === cand.room) sc -= 3;
                          if (prev && prev.opt.period === p) sc -= 5;
                          if (!best || sc < best.sc) best = { i, cand, sc };
                      }
                  }
                  if (best) {
                      placeMaps(best.i, best.cand, maps);
                      rem.delete(best.i);
                      localMoves++;
                      placed = true;
                  } else {
                      for (const i of Array.from(rem)) {
                          if (placed) break;
                          for (const cand of domains[i]) {
                              if (cand.day !== day || cand.session !== session || cand.period !== p) continue;
                              if (placeWithDisplace(i, cand, maps, taboo, false)) {
                                  rem.delete(i);
                                  localMoves++;
                                  placed = true;
                                  break;
                              }
                          }
                      }
                  }
                  if (!placed) break;
              }

              if (rem.size === 0 && sessionPacked(classId, day, session)) {
                  moves += localMoves;
                  return true;
              }
              for (let k = 0; k < arr.length; k++) arr[k] = snapAll[k] ? { ...snapAll[k] } : null;
              moves = movesBefore;
              return false;
          }

          /** Lấp 1 lỗ bằng cách kéo tiết muộn hơn trong cùng buổi xuống (+displace). */
          function slideFill(classId, day, session) {
              const idxs = sessionIdxs(classId, day, session);
              if (idxs.length < 2) return false;
              const start = effectiveSessionStart(day, session);
              const list = uniqueSortedPeriods(idxs.map(i => arr[i].period));
              const blocked = schoolBlockedSet();
              const holes = [];
              const maxP = list[list.length - 1];
              for (let p = start; p <= maxP; p++) {
                  if (isSlotBlockedBySet(blocked, { day, session, period: p })) continue;
                  if (!list.includes(p)) holes.push(p);
              }
              if (!holes.length && list[0] === start) return false;

              const targets = holes.length ? holes : (list[0] > start ? [start] : []);
              const holes1 = gapCountInSession(day, session, list) + (list[0] > start ? 1 : 0);

              for (const hole of targets) {
                  const candidates = idxs
                      .filter(i => arr[i] && arr[i].period > hole)
                      .sort((a, b) => arr[b].period - arr[a].period);
                  for (const i of candidates) {
                      const snap = arr.map(o => (o ? { ...o } : null));
                      const movesBefore = moves;
                      const maps = mapsFrom(arr);
                      const old = arr[i];
                      unplaceMaps(i, maps);
                      for (const cand of domains[i]) {
                          if (cand.day !== day || cand.session !== session || cand.period !== hole) continue;
                          if (placeWithDisplace(i, cand, maps, new Set([i]))) {
                              const list2 = uniqueSortedPeriods(sessionIdxs(classId, day, session).map(x => arr[x].period));
                              const holes2 = gapCountInSession(day, session, list2) + (list2[0] > start ? 1 : 0);
                              if (holes2 < holes1 || sessionPacked(classId, day, session)) {
                                  moves++;
                                  return true;
                              }
                          }
                          // restore and try next cand
                          for (let k = 0; k < arr.length; k++) arr[k] = snap[k] ? { ...snap[k] } : null;
                          moves = movesBefore;
                          // re-unplace i for next cand
                          const maps2 = mapsFrom(arr);
                          unplaceMaps(i, maps2);
                          Object.assign(maps, maps2);
                      }
                      for (let k = 0; k < arr.length; k++) arr[k] = snap[k] ? { ...snap[k] } : null;
                      moves = movesBefore;
                  }
              }
              return false;
          }

          /** Kéo 1 tiết cùng lớp từ ngày khác vào lỗ / tiết đầu. */
          function pullFromOtherDay(classId, day, session) {
              const idxs = sessionIdxs(classId, day, session);
              const start = effectiveSessionStart(day, session);
              const list = uniqueSortedPeriods(idxs.map(i => arr[i].period));
              const blocked = schoolBlockedSet();
              const needPeriods = [];
              if (!idxs.length) return false;
              if (list[0] > start) needPeriods.push(start);
              const maxP = list[list.length - 1];
              for (let p = list[0]; p <= maxP; p++) {
                  if (isSlotBlockedBySet(blocked, { day, session, period: p })) continue;
                  if (!list.includes(p)) needPeriods.push(p);
              }
              if (!needPeriods.length) return false;

              const donors = [];
              arr.forEach((opt, i) => {
                  if (!opt || lessons[i].classId !== classId) return;
                  if (opt.day === day && opt.session === session) return;
                  donors.push(i);
              });
              // ưu tiên donor từ buổi nhiều tiết / môn 1 tiết
              donors.sort((a, b) => {
                  const sa = sessionIdxs(classId, arr[a].day, arr[a].session).length;
                  const sb = sessionIdxs(classId, arr[b].day, arr[b].session).length;
                  return sb - sa;
              });

              const maps = mapsFrom(arr);
              for (const hole of needPeriods) {
                  for (const i of donors) {
                      const old = arr[i];
                      if (!old) continue;
                      const oldDay = old.day;
                      const oldSession = old.session;
                      for (const cand of domains[i]) {
                          if (cand.day !== day || cand.session !== session || cand.period !== hole) continue;
                          unplaceMaps(i, maps);
                          if (!canHard(i, cand, maps)) {
                              placeMaps(i, old, maps);
                              continue;
                          }
                          placeMaps(i, cand, maps);
                          const okNew = classSessionPackOk(arr, classId, day, session);
                          const okOld = classSessionPackOk(arr, classId, oldDay, oldSession);
                          // ngày cũ: sau khi bớt 1 tiết vẫn gói được, hoặc recompact
                          if (okNew && okOld) {
                              moves++;
                              return true;
                          }
                          // thử recompact ngày cũ
                          if (okNew) {
                              if (recompactSession(classId, oldDay, oldSession)) {
                                  moves++;
                                  return true;
                              }
                          }
                          unplaceMaps(i, maps);
                          placeMaps(i, old, maps);
                      }
                  }
              }
              return false;
          }

          /** Đẩy tiết muộn ra ngày khác rồi recompact buổi. */
          function pushAndRecompact(classId, day, session) {
              const idxs = sessionIdxs(classId, day, session);
              if (idxs.length < 2) return false;
              const byLate = idxs.slice().sort((a, b) => arr[b].period - arr[a].period);

              for (const i of byLate.slice(0, 5)) {
                  const old = arr[i];
                  if (!old) continue;
                  const snap = arr.map(o => (o ? { ...o } : null));
                  const movesBefore = moves;
                  const maps = mapsFrom(arr);
                  unplaceMaps(i, maps);
                  const pool = domains[i].slice().sort((a, b) => a.period - b.period || a.day.localeCompare(b.day));
                  for (const cand of pool) {
                      if (cand.day === day && cand.session === session) continue;
                      // rebuild maps from current arr (after unplace)
                      const maps2 = mapsFrom(arr);
                      if (!canHard(i, cand, maps2)) continue;
                      placeMaps(i, cand, maps2);
                      if (!classSessionPackOk(arr, classId, cand.day, cand.session)) {
                          if (!recompactSession(classId, cand.day, cand.session)) {
                              // restore i only if still on cand
                              if (arr[i]) {
                                  const m3 = mapsFrom(arr);
                                  unplaceMaps(i, m3);
                              }
                              continue;
                          }
                      }
                      if (recompactSession(classId, day, session)) {
                          moves++;
                          return true;
                      }
                      // rollback full
                      for (let k = 0; k < arr.length; k++) arr[k] = snap[k] ? { ...snap[k] } : null;
                      moves = movesBefore;
                  }
                  // ensure restored
                  for (let k = 0; k < arr.length; k++) arr[k] = snap[k] ? { ...snap[k] } : null;
                  moves = movesBefore;
              }
              return false;
          }

          function listViolations() {
              const buckets = new Map();
              arr.forEach((opt, i) => {
                  if (!opt) return;
                  const L = lessons[i];
                  const k = `${L.classId}|${opt.day}|${opt.session}`;
                  if (!buckets.has(k)) buckets.set(k, []);
                  buckets.get(k).push(opt.period);
              });
              const viol = [];
              buckets.forEach((periods, k) => {
                  const [classId, day, session] = k.split('|');
                  const list = uniqueSortedPeriods(periods);
                  const start = effectiveSessionStart(day, session);
                  const holes = gapCountInSession(day, session, list);
                  const late = list.length && list[0] > start ? 1 : 0;
                  if (holes > 0 || late) viol.push({ classId, day, session, holes, late, n: list.length });
              });
              // ưu tiên nhiều lỗ / startLate
              viol.sort((a, b) => (b.holes + b.late * 3) - (a.holes + a.late * 3) || b.n - a.n);
              return viol;
          }

          /** Ép gói: gán n tiết buổi vào n tiết liên tục từ start (greedy + displace). */
          function forcePackSession(classId, day, session, loose = false) {
              const idxs = sessionIdxs(classId, day, session);
              if (!idxs.length || sessionPacked(classId, day, session)) return false;
              const start = effectiveSessionStart(day, session);
              const { to } = sessionPeriodRange(session);
              const blocked = schoolBlockedSet();
              const ideal = [];
              for (let p = start; p <= to && ideal.length < idxs.length; p++) {
                  if (!isSlotBlockedBySet(blocked, { day, session, period: p })) ideal.push(p);
              }
              if (ideal.length < idxs.length) return false;

              const snapAll = arr.map(o => (o ? { ...o } : null));
              const movesBefore = moves;
              const maps = mapsFrom(arr);
              idxs.forEach(i => unplaceMaps(i, maps));
              const rem = idxs.slice();
              const taboo = new Set(idxs);

              for (const p of ideal) {
                  let done = false;
                  let best = null;
                  for (const i of rem) {
                      for (const cand of domains[i]) {
                          if (cand.day !== day || cand.session !== session || cand.period !== p) continue;
                          if (!canHard(i, cand, maps)) continue;
                          if (!best) best = { i, cand };
                      }
                  }
                  if (best) {
                      placeMaps(best.i, best.cand, maps);
                      rem.splice(rem.indexOf(best.i), 1);
                      done = true;
                  } else {
                      for (const i of rem.slice()) {
                          if (done) break;
                          for (const cand of domains[i]) {
                              if (cand.day !== day || cand.session !== session || cand.period !== p) continue;
                              if (placeWithDisplace(i, cand, maps, taboo, loose)) {
                                  rem.splice(rem.indexOf(i), 1);
                                  done = true;
                                  break;
                              }
                          }
                      }
                  }
                  if (!done) {
                      for (let k = 0; k < arr.length; k++) arr[k] = snapAll[k] ? { ...snapAll[k] } : null;
                      moves = movesBefore;
                      return false;
                  }
              }
              if (rem.length === 0 && sessionPacked(classId, day, session)) {
                  moves += idxs.length;
                  return true;
              }
              for (let k = 0; k < arr.length; k++) arr[k] = snapAll[k] ? { ...snapAll[k] } : null;
              moves = movesBefore;
              return false;
          }

          let guard = 0;
          const auditStart = auditScheduleQuality(lessons, arr);
          while (moves < maxMoves && guard < 100) {
              guard++;
              const audit0 = auditScheduleQuality(lessons, arr);
              if ((audit0.classHoles || 0) === 0 && (audit0.startLate || 0) === 0) break;

              const viol = listViolations();
              if (!viol.length) break;
              let progressed = false;

              for (const v of viol) {
                  if (sessionPacked(v.classId, v.day, v.session)) continue;
                  if (forcePackSession(v.classId, v.day, v.session)) {
                      progressed = true;
                      break;
                  }
              }
              if (progressed) continue;

              for (const v of viol) {
                  if (sessionPacked(v.classId, v.day, v.session)) continue;
                  if (recompactSession(v.classId, v.day, v.session)) {
                      progressed = true;
                      break;
                  }
              }
              if (progressed) continue;

              for (const v of viol) {
                  if (slideFill(v.classId, v.day, v.session)) {
                      progressed = true;
                      break;
                  }
              }
              if (progressed) continue;

              for (const v of viol) {
                  if (pullFromOtherDay(v.classId, v.day, v.session)) {
                      progressed = true;
                      break;
                  }
              }
              if (progressed) continue;

              for (const v of viol) {
                  if (pushAndRecompact(v.classId, v.day, v.session)) {
                      progressed = true;
                      break;
                  }
              }
              if (!progressed) break;
          }

          /**
           * Buổi cứng đầu: đẩy 1–2 tiết ra ngày khác, forcePack cả nguồn và đích.
           */
          function ejectAndPack(classId, day, session) {
              const idxs = sessionIdxs(classId, day, session);
              if (!idxs.length || sessionPacked(classId, day, session)) return false;
              const ordered = idxs.slice().sort((a, b) => arr[b].period - arr[a].period);

              function restore(snap, movesBefore) {
                  for (let k = 0; k < arr.length; k++) arr[k] = snap[k] ? { ...snap[k] } : null;
                  moves = movesBefore;
              }

              function tryEjectOnes(ejectList) {
                  const snap0 = arr.map(o => (o ? { ...o } : null));
                  const moves0 = moves;
                  // DFS-ish: gán lần lượt từng eject
                  function rec(level, destKeys) {
                      if (level >= ejectList.length) {
                          // pack nguồn
                          if (!(forcePackSession(classId, day, session)
                              || sessionPacked(classId, day, session)
                              || sessionIdxs(classId, day, session).length === 0)) {
                              return false;
                          }
                          // pack mọi đích
                          for (const dk of destKeys) {
                              const [d, s] = dk.split('|');
                              if (!classSessionPackOk(arr, classId, d, s)) {
                                  if (!forcePackSession(classId, d, s) && !sessionPacked(classId, d, s)) return false;
                              }
                          }
                          if (!sessionPacked(classId, day, session) && sessionIdxs(classId, day, session).length > 0) return false;
                          for (const dk of destKeys) {
                              const [d, s] = dk.split('|');
                              if (!sessionPacked(classId, d, s) && sessionIdxs(classId, d, s).length > 0) return false;
                          }
                          moves += 5 + ejectList.length;
                          return true;
                      }
                      const ei = ejectList[level];
                      if (!arr[ei]) return false;
                      const pool = domains[ei].slice().sort((a, b) => a.period - b.period || a.day.localeCompare(b.day));
                      const snapL = arr.map(o => (o ? { ...o } : null));
                      const movesL = moves;
                      for (const cand of pool) {
                          if (cand.day === day && cand.session === session) continue;
                          restore(snapL, movesL);
                          const maps = mapsFrom(arr);
                          unplaceMaps(ei, maps);
                          if (!canHard(ei, cand, maps)) continue;
                          placeMaps(ei, cand, maps);
                          const dk = `${cand.day}|${cand.session}`;
                          if (rec(level + 1, destKeys.concat([dk]))) return true;
                      }
                      restore(snapL, movesL);
                      return false;
                  }
                  const ok = rec(0, []);
                  if (!ok) restore(snap0, moves0);
                  return ok;
              }

              for (const ei of ordered) {
                  if (tryEjectOnes([ei])) return true;
              }
              if (ordered.length >= 3) {
                  if (tryEjectOnes(ordered.slice(0, 2))) return true;
              }
              return false;
          }

          /**
           * Swap chéo lớp: tiết muộn lớp A ↔ tiết GV đang chặn lỗ lớp A (cùng GV, khác lớp).
           * Hay gặp khi 2 lớp tranh GV ở tiết giữa.
           */
          function crossClassSwapFill(classId, day, session) {
              const idxs = sessionIdxs(classId, day, session);
              if (idxs.length < 2) return false;
              const start = effectiveSessionStart(day, session);
              const list = uniqueSortedPeriods(idxs.map(i => arr[i].period));
              const holes = [];
              const blocked = schoolBlockedSet();
              for (let p = start; p <= list[list.length - 1]; p++) {
                  if (isSlotBlockedBySet(blocked, { day, session, period: p })) continue;
                  if (!list.includes(p)) holes.push(p);
              }
              if (!holes.length) return false;

              for (const hole of holes) {
                  const lates = idxs.filter(i => arr[i] && arr[i].period > hole)
                      .sort((a, b) => arr[b].period - arr[a].period);
                  for (const i of lates) {
                      const Li = lessons[i];
                      const oldI = arr[i];
                      // ai đang giữ GV của i tại hole?
                      const maps = mapsFrom(arr);
                      const tj = findTeacherAt(maps, Li.teacherId, day, session, hole);
                      if (tj < 0 || lessons[tj].classId === classId) {
                          // không phải tranh lớp khác — thử move thường
                          continue;
                      }
                      const Lj = lessons[tj];
                      const oldJ = arr[tj];
                      // i → hole, j → oldI.period (đổi tiết)
                      const optI = domains[i].find(o =>
                          o.day === day && o.session === session && o.period === hole
                      );
                      const optJ = domains[tj].find(o =>
                          o.day === oldI.day && o.session === oldI.session && o.period === oldI.period
                      );
                      if (!optI || !optJ) continue;

                      const snap = arr.map(o => (o ? { ...o } : null));
                      const movesBefore = moves;
                      unplaceMaps(i, maps);
                      unplaceMaps(tj, maps);
                      // class slots: i frees oldI, j frees hole - both free for swap
                      if (!canHard(i, optI, maps)) {
                          placeMaps(i, oldI, maps);
                          placeMaps(tj, oldJ, maps);
                          continue;
                      }
                      placeMaps(i, optI, maps);
                      if (!canHard(tj, optJ, maps)) {
                          for (let k = 0; k < arr.length; k++) arr[k] = snap[k] ? { ...snap[k] } : null;
                          moves = movesBefore;
                          continue;
                      }
                      placeMaps(tj, optJ, maps);

                      const okA = classSessionPackOk(arr, classId, day, session);
                      const okB = classSessionPackOk(arr, Lj.classId, oldJ.day, oldJ.session);
                      // chấp nhận nếu A hết lỗ (hoặc giảm) và B không xấu hơn
                      const listA = uniqueSortedPeriods(sessionIdxs(classId, day, session).map(x => arr[x].period));
                      const holesA = gapCountInSession(day, session, listA) + (listA[0] > start ? 1 : 0);
                      const holesA0 = gapCountInSession(day, session, list) + (list[0] > start ? 1 : 0);

                      const listB0 = [];
                      // B before was packed? measure after
                      if (holesA < holesA0 && (okB || forcePackSession(Lj.classId, oldJ.day, oldJ.session))) {
                          // forcePack B if needed
                          if (!sessionPacked(Lj.classId, oldJ.day, oldJ.session)) {
                              if (!forcePackSession(Lj.classId, oldJ.day, oldJ.session)
                                  && !classSessionPackOk(arr, Lj.classId, oldJ.day, oldJ.session)) {
                                  for (let k = 0; k < arr.length; k++) arr[k] = snap[k] ? { ...snap[k] } : null;
                                  moves = movesBefore;
                                  continue;
                              }
                          }
                          if (forcePackSession(classId, day, session) || sessionPacked(classId, day, session) || holesA < holesA0) {
                              moves++;
                              return true;
                          }
                      }
                      for (let k = 0; k < arr.length; k++) arr[k] = snap[k] ? { ...snap[k] } : null;
                      moves = movesBefore;
                  }
              }
              return false;
          }

          // Vòng stubborn: swap chéo → eject + pack
          for (let round = 0; round < 8 && moves < maxMoves; round++) {
              const viol = listViolations();
              if (!viol.length) break;
              let progressed = false;
              for (const v of viol) {
                  if (crossClassSwapFill(v.classId, v.day, v.session)) {
                      progressed = true;
                      break;
                  }
              }
              if (progressed) continue;
              for (const v of viol) {
                  if (ejectAndPack(v.classId, v.day, v.session)) {
                      progressed = true;
                      break;
                  }
              }
              if (!progressed) break;
          }

          // forcePack lặp strict
          for (let fin = 0; fin < 8 && moves < maxMoves; fin++) {
              const viol = listViolations();
              if (!viol.length) break;
              let any = false;
              for (const v of viol) {
                  if (forcePackSession(v.classId, v.day, v.session, false)) any = true;
                  else if (ejectAndPack(v.classId, v.day, v.session)) any = true;
              }
              if (!any) break;
          }

          // Last-ditch: loose + replan cả lớp (gỡ hết tiết lớp, xếp lại gói từ đầu tuần)
          {
              const mid = auditScheduleQuality(lessons, arr);
              if ((mid.classHoles || 0) > 0 && (mid.classHoles || 0) <= 12) {
                  for (let fin = 0; fin < 8 && moves < maxMoves; fin++) {
                      const viol = listViolations();
                      if (!viol.length) break;
                      let any = false;
                      for (const v of viol) {
                          if (forcePackSession(v.classId, v.day, v.session, true)) {
                              any = true;
                              for (const v2 of listViolations()) {
                                  forcePackSession(v2.classId, v2.day, v2.session, false);
                              }
                          }
                      }
                      if (!any) {
                          for (const v of viol) {
                              if (crossClassSwapFill(v.classId, v.day, v.session)) any = true;
                          }
                      }
                      if (!any) break;
                      const now = auditScheduleQuality(lessons, arr);
                      if ((now.classHoles || 0) === 0 && (now.startLate || 0) === 0) break;
                  }
              }

              function replanClass(classId) {
                  const allIdx = [];
                  arr.forEach((opt, i) => {
                      if (opt && lessons[i].classId === classId) allIdx.push(i);
                  });
                  if (!allIdx.length) return false;
                  const snapAll = arr.map(o => (o ? { ...o } : null));
                  const movesBefore = moves;
                  const maps = mapsFrom(arr);
                  allIdx.forEach(i => unplaceMaps(i, maps));
                  const rem = allIdx.slice().sort((a, b) => {
                      const ra = lessons[a].roomNeed ? 0 : 1;
                      const rb = lessons[b].roomNeed ? 0 : 1;
                      return ra - rb || domains[a].length - domains[b].length;
                  });
                  const days = state.rules.days || ['T2', 'T3', 'T4', 'T5', 'T6', 'T7'];
                  const cl = state.classes.find(c => c.id === classId);
                  const sessions = cl?.shift === 'both' ? ['morning', 'afternoon'] : [cl?.shift || 'morning'];

                  for (const day of days) {
                      for (const session of sessions) {
                          const start = effectiveSessionStart(day, session);
                          const { to } = sessionPeriodRange(session);
                          for (let p = start; p <= to && rem.length; p++) {
                              if (isSlotBlockedBySet(schoolBlockedSet(), { day, session, period: p })) continue;
                              let best = null;
                              for (const i of rem) {
                                  for (const cand of domains[i]) {
                                      if (cand.day !== day || cand.session !== session || cand.period !== p) continue;
                                      if (!canHard(i, cand, maps)) continue;
                                      if (!best) best = { i, cand };
                                  }
                              }
                              if (best) {
                                  placeMaps(best.i, best.cand, maps);
                                  rem.splice(rem.indexOf(best.i), 1);
                              } else {
                                  let placedLoose = false;
                                  const taboo = new Set(rem);
                                  for (const i of rem.slice()) {
                                      if (placedLoose) break;
                                      for (const cand of domains[i]) {
                                          if (cand.day !== day || cand.session !== session || cand.period !== p) continue;
                                          if (placeWithDisplace(i, cand, maps, taboo, true)) {
                                              rem.splice(rem.indexOf(i), 1);
                                              placedLoose = true;
                                              break;
                                          }
                                      }
                                  }
                                  if (!placedLoose) break; // dừng buổi — giữ gói
                              }
                          }
                      }
                  }
                  // phần còn: residual pack-prefer
                  for (const i of rem.slice()) {
                      let bestPack = null;
                      let bestAny = null;
                      for (const cand of domains[i]) {
                          if (!canHard(i, cand, maps)) continue;
                          placeMaps(i, cand, maps);
                          const ok = classSessionPackOk(arr, classId, cand.day, cand.session);
                          unplaceMaps(i, maps);
                          if (ok) {
                              if (!bestPack) bestPack = cand;
                          } else if (!bestAny) bestAny = cand;
                      }
                      const pick = bestPack || bestAny;
                      if (pick) {
                          placeMaps(i, pick, maps);
                          rem.splice(rem.indexOf(i), 1);
                      }
                  }
                  if (rem.length === 0) {
                      // force pack mọi buổi lớp
                      const days2 = state.rules.days || ['T2', 'T3', 'T4', 'T5', 'T6', 'T7'];
                      for (const day of days2) {
                          for (const session of sessions) {
                              if (!sessionPacked(classId, day, session) && sessionIdxs(classId, day, session).length) {
                                  forcePackSession(classId, day, session, true);
                              }
                          }
                      }
                      let okAll = true;
                      for (const day of days2) {
                          for (const session of sessions) {
                              if (sessionIdxs(classId, day, session).length
                                  && !sessionPacked(classId, day, session)) okAll = false;
                          }
                      }
                      if (okAll) {
                          moves += allIdx.length;
                          return true;
                      }
                  }
                  for (let k = 0; k < arr.length; k++) arr[k] = snapAll[k] ? { ...snapAll[k] } : null;
                  moves = movesBefore;
                  return false;
              }

              // replan 2 vòng các lớp còn vi phạm
              for (let rp = 0; rp < 3 && moves < maxMoves; rp++) {
                  const brokenClasses = Array.from(new Set(listViolations().map(v => v.classId)));
                  if (!brokenClasses.length) break;
                  let any = false;
                  for (const cid of brokenClasses) {
                      if (replanClass(cid)) any = true;
                  }
                  for (const v of listViolations()) {
                      if (forcePackSession(v.classId, v.day, v.session, true)) any = true;
                      else if (crossClassSwapFill(v.classId, v.day, v.session)) any = true;
                      else if (ejectAndPack(v.classId, v.day, v.session)) any = true;
                  }
                  if (!any) break;
              }
          }

          if (typeof process !== 'undefined' && process.env && process.env.TKB_DEBUG) {
              const auditEnd = auditScheduleQuality(lessons, arr);
              console.log('[repairClassPack]', 'holes', auditStart.classHoles, '→', auditEnd.classHoles,
                  'late', auditStart.startLate, '→', auditEnd.startLate, 'moves', moves);
          }

          return { assignments: arr, moves };
      }

      /**
       * Pass mềm: giảm tiết mồ côi GV — dồn sang ngày đã có tiết + ghép 2 orphan.
       * Chỉ chạy sau khi pack lớp đã ổn (hoặc chấp nhận soft); mọi move giữ pack lớp.
       */
      function reduceTeacherOrphans(assignments, maxMoves = 4000) {
          let moves = 0;
          let improved = true;
          const arr = assignments.slice();

          function mapsFrom(arr0) {
              const tBusy = new Set();
              const cBusy = new Set();
              const rBusy = new Set();
              const subj = new Map();
              arr0.forEach((opt, i) => {
                  if (!opt) return;
                  const L = lessons[i];
                  tBusy.add(`${L.teacherId}|${opt.day}|${opt.session}|${opt.period}`);
                  cBusy.add(`${L.classId}|${opt.day}|${opt.session}|${opt.period}`);
                  rBusy.add(`${opt.room}|${opt.day}|${opt.session}|${opt.period}`);
                  const sk = `${L.classId}|${normalizeText(L.subject)}|${opt.day}`;
                  subj.set(sk, (subj.get(sk) || 0) + 1);
              });
              return { tBusy, cBusy, rBusy, subj };
          }

          function classSessionPackOk(arr0, classId, day, session, ignoreIndex) {
              if (state.rules.packFromSessionStart === false) return true;
              const periods = [];
              arr0.forEach((opt, j) => {
                  if (!opt || j === ignoreIndex) return;
                  if (lessons[j].classId !== classId) return;
                  if (opt.day === day && opt.session === session) periods.push(opt.period);
              });
              if (!periods.length) return true;
              const list = uniqueSortedPeriods(periods);
              const start = effectiveSessionStart(day, session);
              if (list[0] > start) return false;
              return gapCountInSession(day, session, list) === 0;
          }

          function tryMove(i, day, session, maps) {
              const { tBusy, cBusy, rBusy, subj } = maps;
              const L = lessons[i];
              const old = arr[i];
              const { from, to } = sessionPeriodRange(session);
              let best = null;
              for (let p = from; p <= to; p++) {
                  for (const cand of domains[i]) {
                      if (cand.day !== day || cand.session !== session || cand.period !== p) continue;
                      const tk = `${L.teacherId}|${day}|${session}|${p}`;
                      const ck = `${L.classId}|${day}|${session}|${p}`;
                      const rk = `${cand.room}|${day}|${session}|${p}`;
                      const sk = `${L.classId}|${normalizeText(L.subject)}|${day}`;
                      if (tBusy.has(tk) || cBusy.has(ck) || rBusy.has(rk)) continue;
                      if ((subj.get(sk) || 0) >= state.rules.maxSameSubjectDay) continue;
                      // thử tạm — không phá gói lớp (tiết 1 / lủng)
                      arr[i] = cand;
                      const okNew = classSessionPackOk(arr, L.classId, day, session, -1);
                      const okOld = !old || (old.day === day && old.session === session)
                          || classSessionPackOk(arr, L.classId, old.day, old.session, -1);
                      arr[i] = old;
                      if (!okNew || !okOld) continue;
                      // ưu tiên kề tiết GV đã có
                      let adj = 0;
                      arr.forEach((o, j) => {
                          if (!o || j === i || lessons[j].teacherId !== L.teacherId) return;
                          if (o.day === day && o.session === session && Math.abs(o.period - p) === 1) adj = 1;
                      });
                      const sc = p - adj * 20;
                      if (!best || sc < best.sc) best = { cand, sc };
                  }
              }
              return best?.cand || null;
          }

          while (improved && moves < maxMoves) {
              improved = false;
              const audit0 = auditScheduleQuality(lessons, arr);
              if ((audit0.teacherOrphans || 0) === 0) break;

              const buckets = new Map();
              arr.forEach((opt, i) => {
                  if (!opt) return;
                  const L = lessons[i];
                  const k = `${L.teacherId}|${opt.day}|${opt.session}`;
                  if (!buckets.has(k)) buckets.set(k, []);
                  buckets.get(k).push(i);
              });

              // 1) Dồn orphan → ngày GV đã có ≥2 tiết (ưu tiên), rồi ≥1
              for (const [, idxs] of buckets) {
                  if (idxs.length !== 1 || moves >= maxMoves) continue;
                  const i = idxs[0];
                  const opt = arr[i];
                  if (!opt) continue;
                  const L = lessons[i];
                  const teacherDays = new Map();
                  arr.forEach((o, j) => {
                      if (!o || lessons[j].teacherId !== L.teacherId) return;
                      const dk = `${o.day}|${o.session}`;
                      teacherDays.set(dk, (teacherDays.get(dk) || 0) + 1);
                  });
                  const targets = [];
                  teacherDays.forEach((cnt, dk) => {
                      if (cnt >= 1 && dk !== `${opt.day}|${opt.session}`) targets.push({ dk, cnt });
                  });
                  targets.sort((a, b) => b.cnt - a.cnt);
                  if (!targets.length) continue;

                  const maps = mapsFrom(arr);
                  maps.tBusy.delete(`${L.teacherId}|${opt.day}|${opt.session}|${opt.period}`);
                  maps.cBusy.delete(`${L.classId}|${opt.day}|${opt.session}|${opt.period}`);
                  maps.rBusy.delete(`${opt.room}|${opt.day}|${opt.session}|${opt.period}`);
                  const sk0 = `${L.classId}|${normalizeText(L.subject)}|${opt.day}`;
                  maps.subj.set(sk0, (maps.subj.get(sk0) || 1) - 1);

                  let moved = false;
                  for (const { dk } of targets) {
                      const [day, session] = dk.split('|');
                      const cand = tryMove(i, day, session, maps);
                      if (cand) {
                          arr[i] = cand;
                          moves++;
                          improved = true;
                          moved = true;
                          break;
                      }
                  }
                  if (!moved) arr[i] = opt;
              }

              // 2) Ghép 2 orphan cùng GV vào cùng một ngày trống chung
              if (moves < maxMoves) {
                  const orphanByTeacher = new Map();
                  buckets.forEach((idxs, k) => {
                      if (idxs.length !== 1) return;
                      const tid = k.split('|')[0];
                      if (!orphanByTeacher.has(tid)) orphanByTeacher.set(tid, []);
                      orphanByTeacher.get(tid).push(idxs[0]);
                  });
                  for (const [, oidxs] of orphanByTeacher) {
                      if (oidxs.length < 2 || moves >= maxMoves) continue;
                      for (let a = 0; a < oidxs.length && moves < maxMoves; a++) {
                          for (let b = a + 1; b < oidxs.length && moves < maxMoves; b++) {
                              const i = oidxs[a];
                              const j = oidxs[b];
                              if (!arr[i] || !arr[j]) continue;
                              if (arr[i].day === arr[j].day && arr[i].session === arr[j].session) continue;
                              const L = lessons[i];
                              const maps = mapsFrom(arr);
                              maps.tBusy.delete(`${lessons[j].teacherId}|${arr[j].day}|${arr[j].session}|${arr[j].period}`);
                              maps.cBusy.delete(`${lessons[j].classId}|${arr[j].day}|${arr[j].session}|${arr[j].period}`);
                              maps.rBusy.delete(`${arr[j].room}|${arr[j].day}|${arr[j].session}|${arr[j].period}`);
                              const skj = `${lessons[j].classId}|${normalizeText(lessons[j].subject)}|${arr[j].day}`;
                              maps.subj.set(skj, (maps.subj.get(skj) || 1) - 1);
                              const cand = tryMove(j, arr[i].day, arr[i].session, maps);
                              if (cand) {
                                  arr[j] = cand;
                                  moves++;
                                  improved = true;
                              } else {
                                  const maps2 = mapsFrom(arr);
                                  maps2.tBusy.delete(`${L.teacherId}|${arr[i].day}|${arr[i].session}|${arr[i].period}`);
                                  maps2.cBusy.delete(`${L.classId}|${arr[i].day}|${arr[i].session}|${arr[i].period}`);
                                  maps2.rBusy.delete(`${arr[i].room}|${arr[i].day}|${arr[i].session}|${arr[i].period}`);
                                  const ski = `${L.classId}|${normalizeText(L.subject)}|${arr[i].day}`;
                                  maps2.subj.set(ski, (maps2.subj.get(ski) || 1) - 1);
                                  const cand2 = tryMove(i, arr[j].day, arr[j].session, maps2);
                                  if (cand2) {
                                      arr[i] = cand2;
                                      moves++;
                                      improved = true;
                                  }
                              }
                          }
                      }
                  }
              }

              // 3) Swap cùng lớp: orphan ↔ tiết khác lớp (giữ gói) để dồn GV
              if (moves < maxMoves) {
                  const orphanIdxs = [];
                  buckets.forEach((idxs) => {
                      if (idxs.length === 1) orphanIdxs.push(idxs[0]);
                  });
                  for (const i of orphanIdxs) {
                      if (moves >= maxMoves) break;
                      const oi = arr[i];
                      if (!oi) continue;
                      const Li = lessons[i];
                      // ngày GV đã có ≥1 tiết khác
                      const denseDays = new Set();
                      arr.forEach((o, j) => {
                          if (!o || j === i || lessons[j].teacherId !== Li.teacherId) return;
                          denseDays.add(`${o.day}|${o.session}`);
                      });
                      if (!denseDays.size) continue;

                      for (let j = 0; j < arr.length; j++) {
                          if (moves >= maxMoves) break;
                          if (j === i || !arr[j]) continue;
                          const Lj = lessons[j];
                          if (Lj.classId !== Li.classId) continue;
                          const oj = arr[j];
                          if (oi.day === oj.day && oi.session === oj.session) continue;
                          // muốn đưa i sang slot của j nếu j nằm ngày dense của GV i
                          if (!denseDays.has(`${oj.day}|${oj.session}`)) continue;

                          // tìm option domain: i tại slot j, j tại slot i (đổi chỗ thời gian, phòng theo domain)
                          const optI = domains[i].find(o =>
                              o.day === oj.day && o.session === oj.session && o.period === oj.period
                          );
                          const optJ = domains[j].find(o =>
                              o.day === oi.day && o.session === oi.session && o.period === oi.period
                          );
                          if (!optI || !optJ) continue;

                          // hard: GV/phòng free sau khi gỡ cả 2
                          const maps = mapsFrom(arr);
                          maps.tBusy.delete(`${Li.teacherId}|${oi.day}|${oi.session}|${oi.period}`);
                          maps.tBusy.delete(`${Lj.teacherId}|${oj.day}|${oj.session}|${oj.period}`);
                          maps.cBusy.delete(`${Li.classId}|${oi.day}|${oi.session}|${oi.period}`);
                          maps.cBusy.delete(`${Lj.classId}|${oj.day}|${oj.session}|${oj.period}`);
                          maps.rBusy.delete(`${oi.room}|${oi.day}|${oi.session}|${oi.period}`);
                          maps.rBusy.delete(`${oj.room}|${oj.day}|${oj.session}|${oj.period}`);
                          // subject counts: gỡ cũ
                          const ski0 = `${Li.classId}|${normalizeText(Li.subject)}|${oi.day}`;
                          const skj0 = `${Lj.classId}|${normalizeText(Lj.subject)}|${oj.day}`;
                          maps.subj.set(ski0, (maps.subj.get(ski0) || 1) - 1);
                          maps.subj.set(skj0, (maps.subj.get(skj0) || 1) - 1);

                          const tki = `${Li.teacherId}|${optI.day}|${optI.session}|${optI.period}`;
                          const tkj = `${Lj.teacherId}|${optJ.day}|${optJ.session}|${optJ.period}`;
                          const rki = `${optI.room}|${optI.day}|${optI.session}|${optI.period}`;
                          const rkj = `${optJ.room}|${optJ.day}|${optJ.session}|${optJ.period}`;
                          // class keys swap same class same periods exchanged — class slots free each other
                          if (maps.tBusy.has(tki) || maps.tBusy.has(tkj)) continue;
                          if (maps.rBusy.has(rki) || maps.rBusy.has(rkj)) continue;
                          // same teacher can't occupy both if same slot (impossible across days usually)
                          if (tki === tkj) continue;
                          if (rki === rkj && optI.room === optJ.room) continue;
                          const ski = `${Li.classId}|${normalizeText(Li.subject)}|${optI.day}`;
                          const skj = `${Lj.classId}|${normalizeText(Lj.subject)}|${optJ.day}`;
                          if ((maps.subj.get(ski) || 0) >= state.rules.maxSameSubjectDay) continue;
                          if ((maps.subj.get(skj) || 0) >= state.rules.maxSameSubjectDay) continue;

                          const prevI = arr[i];
                          const prevJ = arr[j];
                          arr[i] = optI;
                          arr[j] = optJ;
                          const packOk =
                              classSessionPackOk(arr, Li.classId, optI.day, optI.session, -1)
                              && classSessionPackOk(arr, Li.classId, optJ.day, optJ.session, -1);
                          // swap cùng lớp cùng số tiết/buổi — gói thường giữ; vẫn check
                          if (!packOk) {
                              arr[i] = prevI;
                              arr[j] = prevJ;
                              continue;
                          }
                          // chỉ nhận nếu orphan giảm
                          const before = 1; // i was orphan
                          const afterBuckets = new Map();
                          [i, j].forEach(idx => {
                              const o = arr[idx];
                              const Lx = lessons[idx];
                              // count teacher sessions
                              let cnt = 0;
                              arr.forEach((oo, jj) => {
                                  if (!oo || lessons[jj].teacherId !== Lx.teacherId) return;
                                  if (oo.day === o.day && oo.session === o.session) cnt++;
                              });
                              afterBuckets.set(idx, cnt);
                          });
                          // accept if i no longer alone OR total teacher orphans for Li improved
                          let orphanLiBefore = 0;
                          let orphanLiAfter = 0;
                          const sessCount = (useArr, tid) => {
                              const m = new Map();
                              useArr.forEach((o, jj) => {
                                  if (!o || lessons[jj].teacherId !== tid) return;
                                  const k = `${o.day}|${o.session}`;
                                  m.set(k, (m.get(k) || 0) + 1);
                              });
                              let o = 0;
                              m.forEach(c => { if (c === 1) o++; });
                              return o;
                          };
                          // rollback to measure before
                          arr[i] = prevI;
                          arr[j] = prevJ;
                          orphanLiBefore = sessCount(arr, Li.teacherId);
                          arr[i] = optI;
                          arr[j] = optJ;
                          orphanLiAfter = sessCount(arr, Li.teacherId);
                          const orphanLjBefore = sessCount(
                              (() => { const t = arr.slice(); t[i] = prevI; t[j] = prevJ; return t; })(),
                              Lj.teacherId
                          );
                          const orphanLjAfter = sessCount(arr, Lj.teacherId);
                          if (orphanLiAfter + orphanLjAfter < orphanLiBefore + orphanLjBefore) {
                              moves++;
                              improved = true;
                              break;
                          }
                          arr[i] = prevI;
                          arr[j] = prevJ;
                      }
                  }
              }
          }
          return { assignments: arr, moves };
      }

      if (isLarge || isHuge) {
          const seedCount = isHuge ? 12 : 16;
          let best = null;
          let bestPacked = null; // hard 100% + pack lớp tốt nhất
          let totalWaveNodes = 0;

          function packScore(audit) {
              return (audit.classHoles || 0) * 100 + (audit.startLate || 0) * 200
                  + (audit.teacherOrphans || 0) * 0.5 + (audit.teacherGaps || 0) * 0.05;
          }

          function applyPack(seedAssign) {
              const packed = repairClassPack(seedAssign, isHuge ? 14000 : 22000);
              let assign = packed.assignments;
              let softMoves = packed.moves || 0;
              let audit = auditScheduleQuality(lessons, assign);
              // vòng 2 nếu còn lủng
              if ((audit.classHoles || 0) > 0 || (audit.startLate || 0) > 0) {
                  const packed2 = repairClassPack(assign, isHuge ? 10000 : 16000);
                  assign = packed2.assignments;
                  softMoves += packed2.moves || 0;
                  audit = auditScheduleQuality(lessons, assign);
              }
              return { assign, softMoves, audit };
          }

          function applyOrphanIfPacked(item) {
              if ((item.audit.classHoles || 0) !== 0 || (item.audit.startLate || 0) !== 0) return item;
              const repaired = reduceTeacherOrphans(item.assign, isHuge ? 4000 : 7000);
              let assign = repaired.assignments;
              let softMoves = item.softMoves + (repaired.moves || 0);
              const packed3 = repairClassPack(assign, 5000);
              assign = packed3.assignments;
              softMoves += packed3.moves || 0;
              const audit = auditScheduleQuality(lessons, assign);
              return { assign, softMoves, audit };
          }

          let fullTried = 0;
          for (let s = 0; s < seedCount; s++) {
              const wave = solveBySlotScan(s);
              totalWaveNodes += wave.nodes || 0;
              if (!best || wave.placed > best.placed || (wave.placed === best.placed && wave.ok && !best.ok)) {
                  best = wave;
              }
              if (!wave.ok) continue;
              fullTried++;

              const packed = applyPack(wave.assignments);
              if (!bestPacked || packScore(packed.audit) < packScore(bestPacked.audit)) {
                  bestPacked = packed;
              }
              // pack hoàn hảo → orphan 1 lần rồi chốt
              if ((packed.audit.classHoles || 0) === 0 && (packed.audit.startLate || 0) === 0) {
                  const final = applyOrphanIfPacked(packed);
                  state._packSoftMode = false;
                  totalNodes += totalWaveNodes;
                  deepest = lessons.length;
                  return {
                      ok: true,
                      assignments: final.assign,
                      nodes: totalNodes,
                      deepest: lessons.length,
                      blockedLesson: null,
                      beauty: { ...evaluateBeauty(lessons, final.assign), beautifyMoves: final.softMoves },
                  };
              }
              // đã có pack gần tốt (holes≤4, startLate=0) và thử ≥6 seed → chốt (giữ <15s)
              if (fullTried >= 6 && bestPacked
                  && (bestPacked.audit.classHoles || 0) <= 4
                  && (bestPacked.audit.startLate || 0) === 0) {
                  break;
              }
          }
          totalNodes += totalWaveNodes;
          if (bestPacked) {
              const final = applyOrphanIfPacked(bestPacked);
              state._packSoftMode = false;
              deepest = lessons.length;
              return {
                  ok: true,
                  assignments: final.assign,
                  nodes: totalNodes,
                  deepest: lessons.length,
                  blockedLesson: null,
                  beauty: { ...evaluateBeauty(lessons, final.assign), beautifyMoves: final.softMoves },
              };
          }
          if (best) {
              deepest = Math.max(deepest, best.placed || 0);
              rememberPartial(best.assignments, evaluateBeauty(lessons, best.assignments));
              state._packSoftMode = false;
              const blockedIdx = (best.unplaced && best.unplaced[0])
                  ?? best.assignments.findIndex(a => !a);
              return {
                  ok: false,
                  assignments: best.assignments,
                  nodes: totalNodes,
                  deepest: best.placed || 0,
                  blockedLesson: blockedIdx >= 0 ? lessons[blockedIdx] : null,
                  beauty: evaluateBeauty(lessons, best.assignments),
              };
          }
      }

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
          let beautyMoves = 0;
          if (beautifyBudget > 0) {
              state._packSoftMode = false;
              const polished = beautifySchedule(bestSolution, beautifyBudget);
              bestSolution = polished.assignments;
              beautyMoves += polished.moves || 0;
              if (state.rules.packFromSessionStart !== false && !isFullyPackValid(lessons, bestSolution)) {
                  const stripped = stripPackViolations(lessons, bestSolution);
                  if (stripped.filter(Boolean).length === lessons.length) bestSolution = stripped;
              }
          }
          // Medium/small: pack lớp (nếu lủng) → dồn mồ côi GV (pack-safe)
          if (!isLarge && !isHuge) {
              const packed = repairClassPack(bestSolution, n > 400 ? 8000 : 5000);
              bestSolution = packed.assignments;
              beautyMoves += packed.moves || 0;
              const orphanBudget = n > 400 ? 8000 : n > 200 ? 6000 : 3500;
              const repaired = reduceTeacherOrphans(bestSolution, orphanBudget);
              bestSolution = repaired.assignments;
              beautyMoves += repaired.moves || 0;
              const packed2 = repairClassPack(bestSolution, 3000);
              bestSolution = packed2.assignments;
              beautyMoves += packed2.moves || 0;
          }
          bestBeauty = { ...evaluateBeauty(lessons, bestSolution), beautifyMoves: beautyMoves };
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
