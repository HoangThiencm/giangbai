/**
 * Demo xếp TKB: 16 lớp, ~30 GV (16 * 1.9)
 * Chạy: cscript //nologo agent-tools/tkb-demo-16class.js
 * Port thuật toán từ thoikhoabieu.html (solveByConstraints + precheck)
 */

var state = {
  teachers: [],
  classes: [],
  rooms: [],
  assignments: [],
  rules: {
    morningPeriods: 5,
    afternoonPeriods: 4,
    days: ['T2', 'T3', 'T4', 'T5', 'T6', 'T7'],
    maxSameSubjectDay: 2
  }
};

var _uid = 0;
function uid(prefix) { _uid++; return prefix + '_' + _uid; }
function clean(v) { return String(v == null ? '' : v).replace(/^\s+|\s+$/g, ''); }
function normalizeText(value) {
  var s = clean(value).toLowerCase();
  // simple diacritic strip for common VN chars used in demo
  var map = {
    'à':'a','á':'a','ạ':'a','ả':'a','ã':'a','â':'a','ầ':'a','ấ':'a','ậ':'a','ẩ':'a','ẫ':'a','ă':'a','ằ':'a','ắ':'a','ặ':'a','ẳ':'a','ẵ':'a',
    'è':'e','é':'e','ẹ':'e','ẻ':'e','ẽ':'e','ê':'e','ề':'e','ế':'e','ệ':'e','ể':'e','ễ':'e',
    'ì':'i','í':'i','ị':'i','ỉ':'i','ĩ':'i',
    'ò':'o','ó':'o','ọ':'o','ỏ':'o','õ':'o','ô':'o','ồ':'o','ố':'o','ộ':'o','ổ':'o','ỗ':'o','ơ':'o','ờ':'o','ớ':'o','ợ':'o','ở':'o','ỡ':'o',
    'ù':'u','ú':'u','ụ':'u','ủ':'u','ũ':'u','ư':'u','ừ':'u','ứ':'u','ự':'u','ử':'u','ữ':'u',
    'ỳ':'y','ý':'y','ỵ':'y','ỷ':'y','ỹ':'y','đ':'d'
  };
  var out = '';
  for (var i = 0; i < s.length; i++) out += map[s.charAt(i)] || s.charAt(i);
  return out;
}
function splitList(value) {
  var parts = clean(value).split(/[,\n;]+/);
  var out = [];
  for (var i = 0; i < parts.length; i++) {
    var p = clean(parts[i]);
    if (p) out.push(p);
  }
  return out;
}

function addTeacher(data) {
  state.teachers.push({
    id: data.id || uid('t'),
    name: clean(data.name) || 'GV',
    subject: clean(data.subject),
    maxPeriods: Number(data.maxPeriods || 24),
    unavailable: clean(data.unavailable || ''),
    preferredRooms: clean(data.preferredRooms || '')
  });
  return state.teachers[state.teachers.length - 1];
}
function addClass(data) {
  var name = clean(data.name) || 'Lop';
  state.classes.push({
    id: data.id || uid('c'),
    name: name,
    shift: data.shift || 'morning',
    homeRoom: clean(data.homeRoom) || name
  });
  return state.classes[state.classes.length - 1];
}
function addRoom(data) {
  state.rooms.push({
    id: data.id || uid('r'),
    name: clean(data.name) || 'Phong',
    subjects: clean(data.subjects)
  });
}
function addAssignment(data) {
  state.assignments.push({
    id: data.id || uid('a'),
    classId: data.classId,
    subject: clean(data.subject),
    teacherId: data.teacherId,
    periods: Number(data.periods || 1),
    roomNeed: clean(data.roomNeed || ''),
    note: clean(data.note || '')
  });
}

function parseUnavailable(value) {
  var text = normalizeText(value).replace(/thu\s*/g, 't').replace(/sang/g, 's').replace(/chieu/g, 'c');
  var set = {};
  var parts = text.split(/[,\n;]+/);
  for (var i = 0; i < parts.length; i++) {
    var compact = clean(parts[i]).replace(/\s+/g, '').toUpperCase();
    var match = compact.match(/T?([2-7])([SC])?/);
    if (!match) continue;
    var day = 'T' + match[1];
    var session = match[2];
    if (session) set[day + '-' + (session === 'S' ? 'morning' : 'afternoon')] = true;
    else {
      set[day + '-morning'] = true;
      set[day + '-afternoon'] = true;
    }
  }
  return set;
}

function slotsForClass(classItem) {
  var sessions = classItem.shift === 'both'
    ? ['morning', 'afternoon']
    : [classItem.shift || 'morning'];
  var slots = [];
  for (var d = 0; d < state.rules.days.length; d++) {
    var day = state.rules.days[d];
    for (var s = 0; s < sessions.length; s++) {
      var session = sessions[s];
      var count = session === 'morning' ? state.rules.morningPeriods : state.rules.afternoonPeriods;
      for (var period = 1; period <= count; period++) {
        slots.push({ day: day, session: session, period: period, key: day + '-' + session + '-' + period });
      }
    }
  }
  return slots;
}

function roomMatches(room, needOrSubject) {
  var need = normalizeText(needOrSubject);
  if (!need) return false;
  var list = splitList(room.subjects);
  for (var i = 0; i < list.length; i++) {
    var ns = normalizeText(list[i]);
    if (ns && (need.indexOf(ns) >= 0 || ns.indexOf(need) >= 0)) return true;
  }
  return normalizeText(room.name).indexOf(need) >= 0;
}

function roomOptionsForLesson(lesson, slot) {
  var classItem = null;
  for (var i = 0; i < state.classes.length; i++) if (state.classes[i].id === lesson.classId) classItem = state.classes[i];
  var need = lesson.roomNeed || lesson.subject;
  var specialized = [];
  for (var r = 0; r < state.rooms.length; r++) {
    if (roomMatches(state.rooms[r], need)) specialized.push(state.rooms[r].name);
  }
  var rooms = specialized.length ? specialized : [classItem ? (classItem.homeRoom || classItem.name || '') : ''];
  var seen = {};
  var out = [];
  for (var j = 0; j < rooms.length; j++) {
    if (rooms[j] && !seen[rooms[j]]) {
      seen[rooms[j]] = true;
      out.push({ day: slot.day, session: slot.session, period: slot.period, key: slot.key, room: rooms[j] });
    }
  }
  return out;
}

function buildLessonUnits() {
  var units = [];
  for (var a = 0; a < state.assignments.length; a++) {
    var assignment = state.assignments[a];
    var classItem = null, teacher = null;
    for (var c = 0; c < state.classes.length; c++) if (state.classes[c].id === assignment.classId) classItem = state.classes[c];
    for (var t = 0; t < state.teachers.length; t++) if (state.teachers[t].id === assignment.teacherId) teacher = state.teachers[t];
    var periods = Math.max(0, Number(assignment.periods || 0));
    if (!classItem || !teacher || !assignment.subject || periods <= 0) continue;
    for (var i = 0; i < periods; i++) {
      units.push({
        id: assignment.id,
        classId: assignment.classId,
        subject: assignment.subject,
        teacherId: assignment.teacherId,
        periods: assignment.periods,
        roomNeed: assignment.roomNeed,
        unit: i + 1,
        className: classItem.name,
        teacherName: teacher.name
      });
    }
  }
  // sort by teacher total load desc
  units.sort(function (a, b) {
    function load(tid) {
      var s = 0;
      for (var i = 0; i < state.assignments.length; i++) {
        if (state.assignments[i].teacherId === tid) s += Number(state.assignments[i].periods || 0);
      }
      return s;
    }
    return load(b.teacherId) - load(a.teacherId) || b.periods - a.periods;
  });
  return units;
}

function buildBaseDomains(lessons) {
  var teacherUnavailable = {};
  for (var t = 0; t < state.teachers.length; t++) {
    teacherUnavailable[state.teachers[t].id] = parseUnavailable(state.teachers[t].unavailable);
  }
  var domains = [];
  for (var i = 0; i < lessons.length; i++) {
    var lesson = lessons[i];
    var classItem = null;
    for (var c = 0; c < state.classes.length; c++) if (state.classes[c].id === lesson.classId) classItem = state.classes[c];
    if (!classItem) { domains.push([]); continue; }
    var slots = slotsForClass(classItem);
    var filtered = [];
    for (var s = 0; s < slots.length; s++) {
      var slot = slots[s];
      if (teacherUnavailable[lesson.teacherId] && teacherUnavailable[lesson.teacherId][slot.day + '-' + slot.session]) continue;
      var opts = roomOptionsForLesson(lesson, slot);
      for (var o = 0; o < opts.length; o++) filtered.push(opts[o]);
    }
    domains.push(filtered);
  }
  return domains;
}

function makeIssue(message, type) {
  return { type: type || 'infeasible', message: message };
}

function precheckSchedule(lessons, domains) {
  var issues = [];
  var classLoad = {}, teacherLoad = {};
  for (var i = 0; i < lessons.length; i++) {
    classLoad[lessons[i].classId] = (classLoad[lessons[i].classId] || 0) + 1;
    teacherLoad[lessons[i].teacherId] = (teacherLoad[lessons[i].teacherId] || 0) + 1;
  }
  for (var c = 0; c < state.classes.length; c++) {
    var cl = state.classes[c];
    var capacity = slotsForClass(cl).length;
    if ((classLoad[cl.id] || 0) > capacity) {
      issues.push(makeIssue(cl.name + ' co ' + classLoad[cl.id] + ' tiet can xep nhung chi co ' + capacity + ' o hoc.'));
    }
  }
  for (var t = 0; t < state.teachers.length; t++) {
    var te = state.teachers[t];
    var load = teacherLoad[te.id] || 0;
    if (load > Number(te.maxPeriods || 99)) {
      issues.push(makeIssue(te.name + ' phan cong ' + load + ' tiet, vuot dinh muc ' + te.maxPeriods));
    }
  }
  var classSubjectLoad = {};
  for (var j = 0; j < lessons.length; j++) {
    var key = lessons[j].classId + '|' + normalizeText(lessons[j].subject);
    classSubjectLoad[key] = (classSubjectLoad[key] || 0) + 1;
  }
  for (var k in classSubjectLoad) {
    if (!classSubjectLoad.hasOwnProperty(k)) continue;
    var loadS = classSubjectLoad[k];
    var capacityS = state.rules.days.length * state.rules.maxSameSubjectDay;
    if (loadS > capacityS) {
      issues.push(makeIssue('Mon vuot gioi han tiet/ngay: ' + k + ' = ' + loadS + ' > ' + capacityS));
    }
  }
  for (var n = 0; n < lessons.length; n++) {
    if (!domains[n] || !domains[n].length) {
      issues.push(makeIssue(lessons[n].subject + ' - ' + lessons[n].className + ' (' + lessons[n].teacherName + ') khong co o hop le.'));
    }
  }
  return issues;
}

function gapCount(periods) {
  var unique = {};
  for (var i = 0; i < periods.length; i++) if (periods[i]) unique[periods[i]] = true;
  var list = [];
  for (var p in unique) if (unique.hasOwnProperty(p)) list.push(Number(p));
  list.sort(function (a, b) { return a - b; });
  if (list.length <= 1) return 0;
  var gaps = 0;
  for (var period = list[0]; period <= list[list.length - 1]; period++) {
    if (!unique[period]) gaps++;
  }
  return gaps;
}

function evaluateBeauty(lessons, assignments) {
  var classBuckets = {}, teacherBuckets = {}, subjectDay = {};
  var latePenalty = 0, roomPenalty = 0;
  for (var index = 0; index < assignments.length; index++) {
    var option = assignments[index];
    if (!option) continue;
    var lesson = lessons[index];
    var classKey = lesson.classId + '|' + option.day + '|' + option.session;
    var teacherKey = lesson.teacherId + '|' + option.day + '|' + option.session;
    var subjectKey = lesson.classId + '|' + normalizeText(lesson.subject) + '|' + option.day;
    if (!classBuckets[classKey]) classBuckets[classKey] = [];
    if (!teacherBuckets[teacherKey]) teacherBuckets[teacherKey] = [];
    classBuckets[classKey].push(option.period);
    teacherBuckets[teacherKey].push(option.period);
    subjectDay[subjectKey] = (subjectDay[subjectKey] || 0) + 1;
    latePenalty += option.period * 0.35 + (option.session === 'afternoon' ? 0.4 : 0);
    if (lesson.roomNeed && !roomMatches({ name: option.room, subjects: lesson.roomNeed }, lesson.roomNeed)) roomPenalty += 6;
  }
  var classGaps = 0, teacherGaps = 0, singleLessonTeacherSessions = 0;
  for (var ck in classBuckets) if (classBuckets.hasOwnProperty(ck)) classGaps += gapCount(classBuckets[ck]);
  for (var tk in teacherBuckets) {
    if (!teacherBuckets.hasOwnProperty(tk)) continue;
    teacherGaps += gapCount(teacherBuckets[tk]);
    if (teacherBuckets[tk].length === 1) singleLessonTeacherSessions++;
  }
  var sameSubjectSameDay = 0;
  for (var sk in subjectDay) {
    if (!subjectDay.hasOwnProperty(sk)) continue;
    if (subjectDay[sk] > 1) sameSubjectSameDay += subjectDay[sk] - 1;
  }
  var score = classGaps * 130 + teacherGaps * 90 + sameSubjectSameDay * 38 + singleLessonTeacherSessions * 12 + latePenalty + roomPenalty;
  return {
    score: Math.round(score * 100) / 100,
    classGaps: classGaps,
    teacherGaps: teacherGaps,
    sameSubjectSameDay: sameSubjectSameDay,
    singleLessonTeacherSessions: singleLessonTeacherSessions
  };
}

function solveByConstraints(lessons, domains) {
  var maxDepth = lessons.length > 1000 ? 12 : lessons.length > 700 ? 14 : 22;
  var maxAttempts = lessons.length > 1000 ? 12 : lessons.length > 700 ? 16 : 28;
  var nodeBudget = lessons.length > 1000 ? 520000 : lessons.length > 700 ? 760000 : 1150000;
  var totalNodes = 0;
  var deepest = 0;
  var bestBlocked = null;
  var bestSolution = null;
  var bestBeauty = null;
  var bestPartial = null;
  var bestPartialPlaced = 0;

  function subjectDayKey(lesson, option) {
    return lesson.classId + '|' + normalizeText(lesson.subject) + '|' + option.day;
  }
  function resourceKeys(lesson, option) {
    return {
      classKey: lesson.classId + '|' + option.day + '|' + option.session + '|' + option.period,
      teacherKey: lesson.teacherId + '|' + option.day + '|' + option.session + '|' + option.period,
      roomKey: option.room + '|' + option.day + '|' + option.session + '|' + option.period,
      subjectKey: subjectDayKey(lesson, option)
    };
  }

  var difficultyOrder = [];
  for (var di = 0; di < lessons.length; di++) {
    var load = 0;
    for (var dj = 0; dj < lessons.length; dj++) {
      if (lessons[dj].teacherId === lessons[di].teacherId || lessons[dj].classId === lessons[di].classId) load++;
    }
    difficultyOrder.push({ index: di, size: domains[di].length, load: load });
  }
  difficultyOrder.sort(function (a, b) { return a.size - b.size || b.load - a.load; });
  var difficultyIdx = [];
  for (var dxi = 0; dxi < difficultyOrder.length; dxi++) difficultyIdx.push(difficultyOrder[dxi].index);

  function rememberPartial(assignments, beauty) {
    var placed = 0;
    for (var i = 0; i < assignments.length; i++) if (assignments[i]) placed++;
    if (placed > bestPartialPlaced) {
      bestPartialPlaced = placed;
      bestPartial = assignments.slice();
      if (beauty) {
        bestBeauty = {};
        for (var k in beauty) if (beauty.hasOwnProperty(k)) bestBeauty[k] = beauty[k];
        bestBeauty.placed = placed;
      }
    }
  }

  function makeSolver(attempt) {
    var assignments = new Array(lessons.length);
    for (var i = 0; i < lessons.length; i++) assignments[i] = null;
    var classSlotMap = {};
    var teacherSlotMap = {};
    var roomSlotMap = {};
    var subjectDayMap = {};
    var nodes = 0;

    function snapshot() {
      var subj = {};
      for (var k in subjectDayMap) {
        if (!subjectDayMap.hasOwnProperty(k)) continue;
        var arr = [];
        for (var j = 0; j < subjectDayMap[k].length; j++) arr.push(subjectDayMap[k][j]);
        subj[k] = arr;
      }
      var csm = {}, tsm = {}, rsm = {};
      for (var ck in classSlotMap) if (classSlotMap.hasOwnProperty(ck)) csm[ck] = classSlotMap[ck];
      for (var tk in teacherSlotMap) if (teacherSlotMap.hasOwnProperty(tk)) tsm[tk] = teacherSlotMap[tk];
      for (var rk in roomSlotMap) if (roomSlotMap.hasOwnProperty(rk)) rsm[rk] = roomSlotMap[rk];
      return {
        assignments: assignments.slice(),
        classSlotMap: csm,
        teacherSlotMap: tsm,
        roomSlotMap: rsm,
        subjectDayMap: subj
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
      if (!subjectDayMap[key]) subjectDayMap[key] = [];
      subjectDayMap[key].push(index);
    }

    function place(index, option) {
      var lesson = lessons[index];
      var keys = resourceKeys(lesson, option);
      assignments[index] = option;
      classSlotMap[keys.classKey] = index;
      teacherSlotMap[keys.teacherKey] = index;
      roomSlotMap[keys.roomKey] = index;
      addSubjectDay(keys.subjectKey, index);
    }

    function unplace(index) {
      var option = assignments[index];
      if (!option) return;
      var lesson = lessons[index];
      var keys = resourceKeys(lesson, option);
      assignments[index] = null;
      delete classSlotMap[keys.classKey];
      delete teacherSlotMap[keys.teacherKey];
      delete roomSlotMap[keys.roomKey];
      var subjectSet = subjectDayMap[keys.subjectKey];
      if (subjectSet) {
        var next = [];
        for (var i = 0; i < subjectSet.length; i++) if (subjectSet[i] !== index) next.push(subjectSet[i]);
        if (next.length) subjectDayMap[keys.subjectKey] = next;
        else delete subjectDayMap[keys.subjectKey];
      }
    }

    function conflictsFor(index, option, path) {
      var lesson = lessons[index];
      var keys = resourceKeys(lesson, option);
      var conflicts = {};
      var cands = [classSlotMap[keys.classKey], teacherSlotMap[keys.teacherKey], roomSlotMap[keys.roomKey]];
      for (var i = 0; i < cands.length; i++) {
        if (cands[i] !== undefined && cands[i] !== index) conflicts[cands[i]] = true;
      }
      var subjectSet = subjectDayMap[keys.subjectKey] || [];
      var subjectCount = subjectSet.length;
      if (subjectCount >= state.rules.maxSameSubjectDay) {
        var movable = null;
        var bestDom = -1;
        for (var s = 0; s < subjectSet.length; s++) {
          var conflict = subjectSet[s];
          if (conflict === index || path[conflict]) continue;
          if (domains[conflict].length > bestDom) {
            bestDom = domains[conflict].length;
            movable = conflict;
          }
        }
        if (movable !== null) conflicts[movable] = true;
        else if (subjectSet.length) conflicts[subjectSet[0]] = true;
      }
      var out = [];
      for (var k in conflicts) if (conflicts.hasOwnProperty(k) && Number(k) !== index) out.push(Number(k));
      return out;
    }

    function localSoftCost(index, option) {
      var lesson = lessons[index];
      var classPeriods = [], teacherPeriods = [];
      for (var placedIndex = 0; placedIndex < assignments.length; placedIndex++) {
        var placed = assignments[placedIndex];
        if (!placed || placedIndex === index) continue;
        var other = lessons[placedIndex];
        if (placed.day === option.day && placed.session === option.session && other.classId === lesson.classId) classPeriods.push(placed.period);
        if (placed.day === option.day && placed.session === option.session && other.teacherId === lesson.teacherId) teacherPeriods.push(placed.period);
      }
      var classBefore = gapCount(classPeriods);
      var teacherBefore = gapCount(teacherPeriods);
      var classAfter = gapCount(classPeriods.concat([option.period]));
      var teacherAfter = gapCount(teacherPeriods.concat([option.period]));
      var adjacentClass = false, adjacentTeacher = false;
      for (var i = 0; i < classPeriods.length; i++) if (Math.abs(classPeriods[i] - option.period) === 1) adjacentClass = true;
      for (var j = 0; j < teacherPeriods.length; j++) if (Math.abs(teacherPeriods[j] - option.period) === 1) adjacentTeacher = true;
      var subjectCount = (subjectDayMap[subjectDayKey(lesson, option)] || []).length;
      return (
        (classAfter - classBefore) * 110 +
        (teacherAfter - teacherBefore) * 70 +
        subjectCount * 35 +
        option.period * 0.8 +
        (option.session === 'afternoon' ? 0.6 : 0) -
        (adjacentClass ? 16 : 0) -
        (adjacentTeacher ? 10 : 0) +
        ((attempt * 17 + option.period * 13 + option.day.charCodeAt(1)) % 11) * 0.03
      );
    }

    function orderedOptions(index, path) {
      var list = [];
      for (var i = 0; i < domains[index].length; i++) {
        var option = domains[index][i];
        var conflicts = conflictsFor(index, option, path);
        list.push({ option: option, conflicts: conflicts, cost: conflicts.length * 10000 + localSoftCost(index, option) });
      }
      list.sort(function (a, b) {
        var jitterA = ((attempt + 3) * (a.option.period + 5) * (a.option.day.charCodeAt(1) + 7)) % 17;
        var jitterB = ((attempt + 3) * (b.option.period + 5) * (b.option.day.charCodeAt(1) + 7)) % 17;
        return (a.cost + jitterA * 0.02) - (b.cost + jitterB * 0.02);
      });
      return list;
    }

    function countPlaced() {
      var n = 0;
      for (var i = 0; i < assignments.length; i++) if (assignments[i]) n++;
      return n;
    }

    function recursivePlace(index, depth, path) {
      nodes++;
      totalNodes++;
      deepest = Math.max(deepest, countPlaced());
      if (totalNodes > nodeBudget) {
        rememberPartial(assignments, evaluateBeauty(lessons, assignments));
        return false;
      }
      if (assignments[index]) return true;

      var candidates = orderedOptions(index, path);
      for (var ci = 0; ci < candidates.length; ci++) {
        var candidate = candidates[ci];
        var blockedByPath = false;
        for (var cf = 0; cf < candidate.conflicts.length; cf++) {
          if (path[candidate.conflicts[cf]]) { blockedByPath = true; break; }
        }
        if (blockedByPath) continue;
        if (candidate.conflicts.length && depth <= 0) continue;
        if (candidate.conflicts.length > 4) continue;

        var snap = snapshot();
        for (var u = 0; u < candidate.conflicts.length; u++) unplace(candidate.conflicts[u]);
        place(index, candidate.option);

        var ok = true;
        var nextPath = {};
        for (var pk in path) if (path.hasOwnProperty(pk)) nextPath[pk] = true;
        nextPath[index] = true;

        var displaced = candidate.conflicts.slice().sort(function (a, b) {
          return domains[a].length - domains[b].length;
        });
        for (var di2 = 0; di2 < displaced.length; di2++) {
          if (!recursivePlace(displaced[di2], depth - 1, nextPath)) {
            ok = false;
            bestBlocked = lessons[displaced[di2]];
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

    function improve(maxChecks) {
      var currentBeauty = evaluateBeauty(lessons, assignments);
      var checks = 0;
      var improved = true;
      while (improved && checks < maxChecks) {
        improved = false;
        var order = [];
        for (var i = 0; i < lessons.length; i++) order.push(i);
        order.sort(function (a, b) { return domains[a].length - domains[b].length; });
        for (var oi = 0; oi < order.length; oi++) {
          if (checks >= maxChecks) break;
          var index = order[oi];
          var current = assignments[index];
          if (!current) continue;
          var snap = snapshot();
          unplace(index);
          var cands = [];
          for (var d = 0; d < domains[index].length; d++) {
            var option = domains[index][d];
            if (!conflictsFor(index, option, {}).length) cands.push(option);
          }
          cands.sort(function (a, b) { return localSoftCost(index, a) - localSoftCost(index, b); });
          if (cands.length > 12) cands = cands.slice(0, 12);
          var accepted = false;
          for (var ci = 0; ci < cands.length; ci++) {
            checks++;
            place(index, cands[ci]);
            var beauty = evaluateBeauty(lessons, assignments);
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
      var order;
      if (attempt % 2) {
        order = difficultyIdx.slice().sort(function (a, b) {
          return domains[a].length - domains[b].length || ((a * 31 + attempt) % 7) - ((b * 31 + attempt) % 7);
        });
      } else {
        order = difficultyIdx;
      }
      for (var oi = 0; oi < order.length; oi++) {
        var path = {};
        path[order[oi]] = true;
        if (!recursivePlace(order[oi], maxDepth, path)) {
          var beauty = evaluateBeauty(lessons, assignments);
          rememberPartial(assignments, beauty);
          var placed = countPlaced();
          return { ok: false, assignments: assignments.slice(), nodes: nodes, placed: placed, beauty: beauty };
        }
      }
      var beautyOk = improve(lessons.length > 700 ? 1800 : 3500);
      return { ok: true, assignments: assignments, nodes: nodes, placed: countPlaced(), beauty: beautyOk };
    }

    return { run: run };
  }

  for (var attempt = 0; attempt < maxAttempts && totalNodes <= nodeBudget; attempt++) {
    var result = makeSolver(attempt).run();
    if (result.ok) {
      if (!bestSolution || result.beauty.score < bestBeauty.score) {
        bestSolution = result.assignments.slice();
        bestBeauty = result.beauty;
      }
    } else if (!bestSolution && (!bestBeauty || result.placed > (bestBeauty.placed || 0))) {
      bestBeauty = {};
      for (var bk in result.beauty) if (result.beauty.hasOwnProperty(bk)) bestBeauty[bk] = result.beauty[bk];
      bestBeauty.placed = result.placed;
      rememberPartial(result.assignments, result.beauty);
    }
  }

  // MRV fallback for smaller instances
  function runMrvFallback() {
    if (bestSolution || lessons.length > 420 || totalNodes > nodeBudget) return null;
    var assignments = new Array(lessons.length);
    for (var i = 0; i < lessons.length; i++) assignments[i] = null;
    var classSlotMap = {}, teacherSlotMap = {}, roomSlotMap = {}, subjectDayMap = {};
    var maxFallbackNodes = lessons.length > 240 ? 160000 : 260000;
    var fallbackNodes = 0;

    function keysFor(index, option) { return resourceKeys(lessons[index], option); }
    function canPlace(index, option) {
      var keys = keysFor(index, option);
      if (classSlotMap[keys.classKey] !== undefined || teacherSlotMap[keys.teacherKey] !== undefined || roomSlotMap[keys.roomKey] !== undefined) return false;
      return (subjectDayMap[keys.subjectKey] || []).length < state.rules.maxSameSubjectDay;
    }
    function place(index, option) {
      var keys = keysFor(index, option);
      assignments[index] = option;
      classSlotMap[keys.classKey] = index;
      teacherSlotMap[keys.teacherKey] = index;
      roomSlotMap[keys.roomKey] = index;
      if (!subjectDayMap[keys.subjectKey]) subjectDayMap[keys.subjectKey] = [];
      subjectDayMap[keys.subjectKey].push(index);
    }
    function unplace(index) {
      var option = assignments[index];
      if (!option) return;
      var keys = keysFor(index, option);
      assignments[index] = null;
      delete classSlotMap[keys.classKey];
      delete teacherSlotMap[keys.teacherKey];
      delete roomSlotMap[keys.roomKey];
      var subjectSet = subjectDayMap[keys.subjectKey] || [];
      var next = [];
      for (var i = 0; i < subjectSet.length; i++) if (subjectSet[i] !== index) next.push(subjectSet[i]);
      if (next.length) subjectDayMap[keys.subjectKey] = next;
      else delete subjectDayMap[keys.subjectKey];
    }
    function fallbackCost(index, option) {
      var lesson = lessons[index];
      var classPeriods = [], teacherPeriods = [];
      for (var pi = 0; pi < assignments.length; pi++) {
        var placed = assignments[pi];
        if (!placed) continue;
        var other = lessons[pi];
        if (placed.day === option.day && placed.session === option.session && other.classId === lesson.classId) classPeriods.push(placed.period);
        if (placed.day === option.day && placed.session === option.session && other.teacherId === lesson.teacherId) teacherPeriods.push(placed.period);
      }
      var classAfter = gapCount(classPeriods.concat([option.period]));
      var teacherAfter = gapCount(teacherPeriods.concat([option.period]));
      var sameSubject = (subjectDayMap[subjectDayKey(lesson, option)] || []).length;
      return classAfter * 120 + teacherAfter * 80 + sameSubject * 30 + option.period * 0.5;
    }
    function nextIndex() {
      var best = null;
      for (var index = 0; index < lessons.length; index++) {
        if (assignments[index]) continue;
        var feasible = [];
        for (var d = 0; d < domains[index].length; d++) {
          if (canPlace(index, domains[index][d])) feasible.push(domains[index][d]);
        }
        if (!feasible.length) return { index: index, candidates: [] };
        var item = { index: index, candidates: feasible };
        if (!best || feasible.length < best.candidates.length || (feasible.length === best.candidates.length && domains[index].length < domains[best.index].length)) best = item;
      }
      return best;
    }
    function countPlaced() {
      var n = 0; for (var i = 0; i < assignments.length; i++) if (assignments[i]) n++; return n;
    }
    function search() {
      fallbackNodes++;
      totalNodes++;
      deepest = Math.max(deepest, countPlaced());
      if (fallbackNodes > maxFallbackNodes || totalNodes > nodeBudget) {
        rememberPartial(assignments, evaluateBeauty(lessons, assignments));
        return false;
      }
      var next = nextIndex();
      if (!next) return true;
      if (!next.candidates.length) {
        bestBlocked = lessons[next.index];
        rememberPartial(assignments, evaluateBeauty(lessons, assignments));
        return false;
      }
      var cap = lessons.length > 240 ? 30 : next.candidates.length;
      var candidates = next.candidates.slice().sort(function (a, b) {
        return fallbackCost(next.index, a) - fallbackCost(next.index, b);
      });
      if (candidates.length > cap) candidates = candidates.slice(0, cap);
      for (var i = 0; i < candidates.length; i++) {
        place(next.index, candidates[i]);
        if (search()) return true;
        unplace(next.index);
      }
      bestBlocked = lessons[next.index];
      return false;
    }
    var ok = search();
    var beauty = evaluateBeauty(lessons, assignments);
    rememberPartial(assignments, beauty);
    return { ok: ok, assignments: assignments.slice(), nodes: fallbackNodes, placed: countPlaced(), beauty: beauty };
  }

  var fallback = runMrvFallback();
  if (fallback && fallback.ok) {
    bestSolution = fallback.assignments.slice();
    bestBeauty = fallback.beauty;
  }

  return {
    ok: !!bestSolution,
    assignments: bestSolution || bestPartial || (function () {
      var a = new Array(lessons.length);
      for (var i = 0; i < lessons.length; i++) a[i] = null;
      return a;
    })(),
    nodes: totalNodes,
    deepest: deepest,
    blockedLesson: bestBlocked,
    beauty: bestBeauty
  };
}

// ===================== DEMO DATA: 16 lớp · 30 GV (16 * 1.9) =====================
function buildDemoData() {
  state.teachers = [];
  state.classes = [];
  state.rooms = [];
  state.assignments = [];
  state.rules = {
    morningPeriods: 5,
    afternoonPeriods: 4,
    days: ['T2', 'T3', 'T4', 'T5', 'T6', 'T7'],
    maxSameSubjectDay: 2
  };

  // 16 classes: 4 khối × 4 lớp — half morning, half both for capacity
  var classNames = [
    '6A', '6B', '6C', '6D',
    '7A', '7B', '7C', '7D',
    '8A', '8B', '8C', '8D',
    '9A', '9B', '9C', '9D'
  ];
  for (var i = 0; i < classNames.length; i++) {
    // 1 buổi sáng: capacity 30; 2 buổi: 54 — dùng morning cho tất cả để mô phỏng THCS phổ biến
    // nhưng gán ~28 tiết/lớp nên cần morning only OK
    addClass({ name: classNames[i], shift: 'morning', homeRoom: classNames[i] });
  }

  // 30 teachers = round(16 * 1.9)
  // Phân theo môn thực tế THCS, mỗi GV dạy nhiều lớp
  var teacherDefs = [
    // Toán: 4 GV × 4 lớp × 4 tiết = 16 tiết/GV
    { name: 'GV Toan 1', subject: 'Toan', max: 24, unav: '' },
    { name: 'GV Toan 2', subject: 'Toan', max: 24, unav: 'T7S' },
    { name: 'GV Toan 3', subject: 'Toan', max: 24, unav: '' },
    { name: 'GV Toan 4', subject: 'Toan', max: 24, unav: 'T6S' },
    // Van: 4 GV
    { name: 'GV Van 1', subject: 'Ngu van', max: 24, unav: '' },
    { name: 'GV Van 2', subject: 'Ngu van', max: 24, unav: 'T3S' },
    { name: 'GV Van 3', subject: 'Ngu van', max: 24, unav: '' },
    { name: 'GV Van 4', subject: 'Ngu van', max: 24, unav: '' },
    // Anh: 3 GV
    { name: 'GV Anh 1', subject: 'Tieng Anh', max: 24, unav: '' },
    { name: 'GV Anh 2', subject: 'Tieng Anh', max: 24, unav: 'T5S' },
    { name: 'GV Anh 3', subject: 'Tieng Anh', max: 24, unav: '' },
    // Ly: 2
    { name: 'GV Ly 1', subject: 'Vat ly', max: 22, unav: '', rooms: 'Ly 1' },
    { name: 'GV Ly 2', subject: 'Vat ly', max: 22, unav: 'T2S', rooms: 'Ly 1' },
    // Hoa: 2
    { name: 'GV Hoa 1', subject: 'Hoa hoc', max: 22, unav: '', rooms: 'Hoa 1' },
    { name: 'GV Hoa 2', subject: 'Hoa hoc', max: 22, unav: '', rooms: 'Hoa 1' },
    // Sinh: 2
    { name: 'GV Sinh 1', subject: 'Sinh hoc', max: 22, unav: '', rooms: 'Sinh 1' },
    { name: 'GV Sinh 2', subject: 'Sinh hoc', max: 22, unav: 'T4S', rooms: 'Sinh 1' },
    // Su: 2
    { name: 'GV Su 1', subject: 'Lich su', max: 22, unav: '' },
    { name: 'GV Su 2', subject: 'Lich su', max: 22, unav: '' },
    // Dia: 2
    { name: 'GV Dia 1', subject: 'Dia ly', max: 22, unav: '' },
    { name: 'GV Dia 2', subject: 'Dia ly', max: 22, unav: 'T7S' },
    // GDCD: 1
    { name: 'GV GDCD 1', subject: 'GDCD', max: 22, unav: '' },
    // Tin: 2 (16 lớp × 2 tiết = 32 → 16 tiết/GV)
    { name: 'GV Tin 1', subject: 'Tin hoc', max: 24, unav: '', rooms: 'Tin 1' },
    { name: 'GV Tin 2', subject: 'Tin hoc', max: 24, unav: '', rooms: 'Tin 2' },
    // CN: 1
    { name: 'GV CN 1', subject: 'Cong nghe', max: 22, unav: '', rooms: 'CN 1' },
    // TD: 2
    { name: 'GV TD 1', subject: 'The duc', max: 24, unav: '', rooms: 'San 1' },
    { name: 'GV TD 2', subject: 'The duc', max: 24, unav: '', rooms: 'San 1' },
    // Am nhac: 1
    { name: 'GV AN 1', subject: 'Am nhac', max: 20, unav: '' },
    // My thuat: 1
    { name: 'GV MT 1', subject: 'My thuat', max: 20, unav: '' },
    // Sinh hoat: 1
    { name: 'GV SH 1', subject: 'Sinh hoat', max: 20, unav: '' }
  ];
  // ensure exactly 30
  if (teacherDefs.length !== 30) {
    WScript.Echo('ERROR: expected 30 teachers, got ' + teacherDefs.length);
  }
  for (var t = 0; t < teacherDefs.length; t++) {
    addTeacher({
      name: teacherDefs[t].name,
      subject: teacherDefs[t].subject,
      maxPeriods: teacherDefs[t].max,
      unavailable: teacherDefs[t].unav || '',
      preferredRooms: teacherDefs[t].rooms || ''
    });
  }

  // Phòng BM: mỗi lab ≥ 2 phòng để 16 lớp × 2 tiết (32) ≤ 2×30 ô sáng
  addRoom({ name: 'Tin 1', subjects: 'Tin hoc' });
  addRoom({ name: 'Tin 2', subjects: 'Tin hoc' });
  addRoom({ name: 'Ly 1', subjects: 'Vat ly' });
  addRoom({ name: 'Ly 2', subjects: 'Vat ly' });
  addRoom({ name: 'Hoa 1', subjects: 'Hoa hoc' });
  addRoom({ name: 'Hoa 2', subjects: 'Hoa hoc' });
  addRoom({ name: 'Sinh 1', subjects: 'Sinh hoc' });
  addRoom({ name: 'Sinh 2', subjects: 'Sinh hoc' });
  addRoom({ name: 'CN 1', subjects: 'Cong nghe' });
  addRoom({ name: 'CN 2', subjects: 'Cong nghe' });
  addRoom({ name: 'San 1', subjects: 'The duc' });
  addRoom({ name: 'San 2', subjects: 'The duc' });

  // Curriculum periods per class (~28/class, capacity morning=30)
  // subject -> [periods per class, teacher indices (round-robin by class)]
  function teacherBySubject(subject, classIndex) {
    var idxs = [];
    for (var i = 0; i < state.teachers.length; i++) {
      if (normalizeText(state.teachers[i].subject) === normalizeText(subject)) idxs.push(i);
    }
    if (!idxs.length) return null;
    return state.teachers[idxs[classIndex % idxs.length]];
  }

  var curriculum = [
    { subject: 'Toan', periods: 4, roomNeed: '' },
    { subject: 'Ngu van', periods: 4, roomNeed: '' },
    { subject: 'Tieng Anh', periods: 3, roomNeed: '' },
    { subject: 'Vat ly', periods: 2, roomNeed: 'Vat ly' },
    { subject: 'Hoa hoc', periods: 2, roomNeed: 'Hoa hoc' },
    { subject: 'Sinh hoc', periods: 2, roomNeed: 'Sinh hoc' },
    { subject: 'Lich su', periods: 1, roomNeed: '' },
    { subject: 'Dia ly', periods: 1, roomNeed: '' },
    { subject: 'GDCD', periods: 1, roomNeed: '' },
    { subject: 'Tin hoc', periods: 2, roomNeed: 'Tin hoc' },
    { subject: 'Cong nghe', periods: 1, roomNeed: 'Cong nghe' },
    { subject: 'The duc', periods: 2, roomNeed: 'The duc' },
    { subject: 'Am nhac', periods: 1, roomNeed: '' },
    { subject: 'My thuat', periods: 1, roomNeed: '' },
    { subject: 'Sinh hoat', periods: 1, roomNeed: '' }
  ];
  // total = 4+4+3+2+2+2+1+1+1+2+1+2+1+1+1 = 28 periods/class

  for (var ci = 0; ci < state.classes.length; ci++) {
    var cl = state.classes[ci];
    for (var si = 0; si < curriculum.length; si++) {
      var cur = curriculum[si];
      var teacher = teacherBySubject(cur.subject, ci);
      if (!teacher) {
        // HDTN not in curriculum; skip missing
        WScript.Echo('Missing teacher for ' + cur.subject);
        continue;
      }
      addAssignment({
        classId: cl.id,
        teacherId: teacher.id,
        subject: cur.subject,
        periods: cur.periods,
        roomNeed: cur.roomNeed
      });
    }
  }

  // HDTN teacher unused is fine - ratio still ~1.9
  return {
    classes: state.classes.length,
    teachers: state.teachers.length,
    rooms: state.rooms.length,
    assignments: state.assignments.length,
    ratio: (state.teachers.length / state.classes.length).toFixed(2)
  };
}

function teacherLoadSummary(lessons) {
  var load = {};
  for (var i = 0; i < lessons.length; i++) {
    load[lessons[i].teacherId] = (load[lessons[i].teacherId] || 0) + 1;
  }
  var rows = [];
  for (var t = 0; t < state.teachers.length; t++) {
    var te = state.teachers[t];
    rows.push({ name: te.name, subject: te.subject, load: load[te.id] || 0, max: te.maxPeriods });
  }
  rows.sort(function (a, b) { return b.load - a.load; });
  return rows;
}

function main() {
  var t0 = new Date().getTime();
  var meta = buildDemoData();
  WScript.Echo('=== DEMO TKB 16 lop x 30 GV (16*1.9) ===');
  WScript.Echo('Lop: ' + meta.classes + ' | GV: ' + meta.teachers + ' | Ty le GV/lop: ' + meta.ratio);
  WScript.Echo('Phong BM: ' + meta.rooms + ' | Dong phan cong: ' + meta.assignments);
  WScript.Echo('Cau hinh: ' + state.rules.days.join(',') + ' | Sang ' + state.rules.morningPeriods + ' tiet | Chieu ' + state.rules.afternoonPeriods + ' | max mon/ngay ' + state.rules.maxSameSubjectDay);

  var lessons = buildLessonUnits();
  var domains = buildBaseDomains(lessons);
  WScript.Echo('Tong tiet can xep: ' + lessons.length);
  WScript.Echo('Capacity 1 lop morning: ' + slotsForClass(state.classes[0]).length + ' o');

  var loads = teacherLoadSummary(lessons);
  WScript.Echo('--- Tai GV (top 10) ---');
  for (var i = 0; i < Math.min(10, loads.length); i++) {
    WScript.Echo('  ' + loads[i].name + ' (' + loads[i].subject + '): ' + loads[i].load + '/' + loads[i].max);
  }

  var pre = precheckSchedule(lessons, domains);
  if (pre.length) {
    WScript.Echo('PRECHECK FAIL: ' + pre.length + ' van de');
    for (var p = 0; p < pre.length; p++) WScript.Echo('  - ' + pre[p].message);
    return;
  }
  WScript.Echo('Precheck: OK');

  WScript.Echo('Dang chay solver...');
  var solved = solveByConstraints(lessons, domains);
  var placed = 0;
  for (var j = 0; j < solved.assignments.length; j++) if (solved.assignments[j]) placed++;
  var t1 = new Date().getTime();
  var pct = lessons.length ? Math.round(placed * 10000 / lessons.length) / 100 : 0;

  WScript.Echo('=== KET QUA ===');
  WScript.Echo('OK 100%: ' + (solved.ok ? 'YES' : 'NO'));
  WScript.Echo('Da xep: ' + placed + '/' + lessons.length + ' (' + pct + '%)');
  WScript.Echo('Nodes: ' + solved.nodes + ' | deepest: ' + solved.deepest);
  WScript.Echo('Thoi gian: ' + ((t1 - t0) / 1000) + 's');
  if (solved.beauty) {
    WScript.Echo('Beauty score: ' + solved.beauty.score +
      ' | gap lop: ' + solved.beauty.classGaps +
      ' | gap GV: ' + solved.beauty.teacherGaps +
      ' | mon don: ' + solved.beauty.sameSubjectSameDay);
  }
  if (solved.blockedLesson) {
    WScript.Echo('Diem nghen: ' + solved.blockedLesson.subject + ' - ' +
      solved.blockedLesson.className + ' (' + solved.blockedLesson.teacherName + ')');
  }

  // validate hard constraints on placed cells
  var classMap = {}, teacherMap = {}, roomMap = {}, subjDay = {};
  var violations = 0;
  for (var k = 0; k < solved.assignments.length; k++) {
    var opt = solved.assignments[k];
    if (!opt) continue;
    var les = lessons[k];
    var ck = les.classId + '|' + opt.day + '|' + opt.session + '|' + opt.period;
    var tk = les.teacherId + '|' + opt.day + '|' + opt.session + '|' + opt.period;
    var rk = opt.room + '|' + opt.day + '|' + opt.session + '|' + opt.period;
    var sk = les.classId + '|' + normalizeText(les.subject) + '|' + opt.day;
    if (classMap[ck] || teacherMap[tk] || roomMap[rk]) violations++;
    classMap[ck] = true; teacherMap[tk] = true; roomMap[rk] = true;
    subjDay[sk] = (subjDay[sk] || 0) + 1;
  }
  for (var skey in subjDay) {
    if (subjDay.hasOwnProperty(skey) && subjDay[skey] > state.rules.maxSameSubjectDay) violations++;
  }
  WScript.Echo('Hard-constraint violations tren o da xep: ' + violations);
}

main();
