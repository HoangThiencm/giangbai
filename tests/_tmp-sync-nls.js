const fs = require('fs');
if (process.argv[2] === 'probe') {
  const s = fs.readFileSync('canvas_xaydungphuluc.html', 'utf8');
  const n = "let sgkCompactContext='',aiSelectedLessonIds=new Set();";
  const i = s.indexOf('let sgkCompactContext');
  console.log('idx exact', s.indexOf(n));
  console.log('slice', JSON.stringify(s.slice(i, i + 90)));
  process.exit(0);
}
const src = fs.readFileSync('xaydungphuluc.html', 'utf8');
const files = [
  'canvas_xaydungphuluc.html',
  'backupcode viettailieu/canvas_xaydungphuluc.html'
];

function extract(hay, startNeedle, endNeedle) {
  const start = hay.indexOf(startNeedle);
  if (start < 0) throw new Error('src missing ' + startNeedle.slice(0, 80));
  const end = hay.indexOf(endNeedle, start);
  if (end < 0) throw new Error('src missing end ' + endNeedle.slice(0, 80));
  return hay.slice(start, end);
}

function replaceOnce(s, from, to, label, file) {
  if (s.includes(to) && !s.includes(from)) return s;
  const idx = s.indexOf(from);
  if (idx < 0) throw new Error(file + ' missing ' + label + ': ' + String(from).slice(0, 90));
  return s.slice(0, idx) + to + s.slice(idx + from.length);
}

const nlsHelpers = extract(src, 'function nlsCandidates()', 'function aiPeriodCandidates()');
const remapBlock = extract(src, 'function remapAiSelectionsAfterPpctMove(', 'function periodsPerWeekForSubject(');
const selectedBlock = extract(src, 'function selectedIntegration(', 'function enrichNlsCode(');
const separateBlock = extract(src, 'function separateIntegration(', 'function sourcePpctRowsForAppendixOne()');
const pickerInner = extract(src, "  const nlsRate=typeof syncNlsRateFromSelection===", '  if(selected.size>limit)');
const syncRangesBlock = extract(src, 'function syncRanges(){if(typeof nlsSelectedLessonIds', 'function aiPickerRows()');

for (const f of files) {
  let s = fs.readFileSync(f, 'utf8');

  if (!s.includes('function nlsCandidates()')) {
    s = replaceOnce(s, 'function aiPeriodCandidates()', nlsHelpers + 'function aiPeriodCandidates()', 'insert nls helpers', f);
  }

  s = replaceOnce(
    s,
    extract(s, 'function remapAiSelectionsAfterPpctMove(', 'function periodsPerWeekForSubject('),
    remapBlock,
    'remap',
    f
  );
  s = replaceOnce(
    s,
    extract(s, 'function selectedIntegration(', 'function enrichNlsCode('),
    selectedBlock,
    'selectedIntegration',
    f
  );
  s = replaceOnce(
    s,
    extract(s, 'function separateIntegration(', 'function sourcePpctRowsForAppendixOne()'),
    separateBlock,
    'separateIntegration',
    f
  );

  if (s.includes("card.classList.remove('hidden');count.textContent=`🎯 Đã chọn:")) {
    s = replaceOnce(
      s,
      extract(s, "  card.classList.remove('hidden');count.textContent=`🎯 Đã chọn:", '  if(selected.size>limit)'),
      pickerInner,
      'picker inner',
      f
    );
  }

  if (!s.includes('function syncRanges(){if(typeof nlsSelectedLessonIds')) {
    s = replaceOnce(
      s,
      extract(s, 'function syncRanges(){nlsRateOut.value=', 'function aiPickerRows()'),
      syncRangesBlock,
      'syncRanges',
      f
    );
  }

  const simples = [
    ["let sgkCompactContext='',aiSelectedLessonIds=new Set();", "let sgkCompactContext='',aiSelectedLessonIds=new Set(),nlsSelectedLessonIds=new Set();"],
    ["if(typeof aiSelectedLessonIds!=='undefined')aiSelectedLessonIds.clear();if(typeof updateAiPicker==='function')updateAiPicker();", "if(typeof aiSelectedLessonIds!=='undefined')aiSelectedLessonIds.clear();if(typeof nlsSelectedLessonIds!=='undefined')nlsSelectedLessonIds.clear();if(typeof updateAiPicker==='function')updateAiPicker();"],
    ["aiSelectedLessonIds:[...aiSelectedLessonIds],sgkCompactContext", "aiSelectedLessonIds:[...aiSelectedLessonIds],nlsSelectedLessonIds:[...nlsSelectedLessonIds],sgkCompactContext"],
    ["aiSelectedLessonIds=new Set(Array.isArray(draft.aiSelectedLessonIds)?draft.aiSelectedLessonIds:[]);sgkCompactContext", "aiSelectedLessonIds=new Set(Array.isArray(draft.aiSelectedLessonIds)?draft.aiSelectedLessonIds:[]);nlsSelectedLessonIds=new Set(Array.isArray(draft.nlsSelectedLessonIds)?draft.nlsSelectedLessonIds:[]);sgkCompactContext"]
  ];
  for (const [a, b] of simples) {
    if (s.includes(b)) continue;
    if (!s.includes(a)) {
      console.warn('skip simple in', f, a.slice(0, 70));
      continue;
    }
    s = s.replace(a, b);
  }
  if (!s.includes('nlsSelectedLessonIds=new Set()') && !s.includes('nlsSelectedLessonIds = new Set')) {
    s = s.replace("let sgkCompactContext='',aiSelectedLessonIds=new Set();", "let sgkCompactContext='',aiSelectedLessonIds=new Set(),nlsSelectedLessonIds=new Set();");
  }

  if (!s.includes('syncNlsSelectionFromRate();}else{nlsSelectedLessonIds.clear()')) {
    s = replaceOnce(
      s,
      "if(typeof aiEnabled!=='undefined'&&aiEnabled.checked){syncAiSelectionFromRate();}else{aiSelectedLessonIds.clear();updateAiPicker();}",
      "if(typeof aiEnabled!=='undefined'&&aiEnabled.checked){syncAiSelectionFromRate();}else{aiSelectedLessonIds.clear();updateAiPicker();}\n  if(typeof nlsEnabled!=='undefined'&&nlsEnabled.checked){syncNlsSelectionFromRate();}else{nlsSelectedLessonIds.clear();if(typeof updateAiPicker==='function')updateAiPicker();}",
      'loadDefault nls sync',
      f
    );
  }

  const callPairs = [
    ["const selected=selectedPeriodsForLesson(row.id||`ppct:${index}`,row.lesson);const sep=separateIntegration(row.integration,selected,normal,c,row.lesson,row.periods);",
     "const selected=selectedPeriodsForLesson(row.id||`ppct:${index}`,row.lesson);const sep=separateIntegration(row.integration,selected,normal,c,row.lesson,row.periods,row.id||`ppct:${index}`);"],
    ["const {nlsText,aiText}=separateIntegration(matching.integration,selectedPeriodsForLessonId(row.id),normal,c,row.lesson,row.periods);",
     "const {nlsText,aiText}=separateIntegration(matching.integration,selectedPeriodsForLessonId(row.id),normal,c,row.lesson,row.periods,row.id);"],
    ["selectedIntegration(row.integration,selectedPeriodsForLesson(row.id||`ppct:${index}`,row.lesson),index,config,row.lesson,row.periods)",
     "selectedIntegration(row.integration,selectedPeriodsForLesson(row.id||`ppct:${index}`,row.lesson),index,config,row.lesson,row.periods,row.id||`ppct:${index}`)"]
    ,
    ["selectedIntegration(row.integration,selectedPeriodsForLesson(row.id||`ppct:${index}`,row.lesson),index,c,row.lesson,row.periods)",
     "selectedIntegration(row.integration,selectedPeriodsForLesson(row.id||`ppct:${index}`,row.lesson),index,c,row.lesson,row.periods,row.id||`ppct:${index}`)"]
    ,
    ["const integration=appendixOneIntegrationForLesson(lesson)||selectedIntegration(generatedRow.integration,selected,normal,c,lesson,lessonPeriods);",
     "const integration=appendixOneIntegrationForLesson(lesson)||selectedIntegration(generatedRow.integration,selected,normal,c,lesson,lessonPeriods,aiCandidateIdForSourceRow(rowIndex));"]
  ];
  for (const [a, b] of callPairs) {
    if (s.includes(a)) s = s.replace(a, b);
  }

  fs.writeFileSync(f, s);
  console.log('synced', f);
}
