const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const sourcePath = path.join(root, 'xaydungphuluc.html');
const backupPath = path.join(root, 'backupcode viettailieu', 'canvas_xaydungphuluc.html');
const canvasPath = path.join(root, 'canvas_xaydungphuluc.html');

function extractNamed(src, name) {
  const needle = `function ${name}(`;
  let start = -1, from = 0;
  while (true) {
    const idx = src.indexOf(needle, from);
    if (idx < 0) break;
    start = idx;
    from = idx + needle.length;
  }
  if (start < 0) throw new Error('missing ' + name);
  const nl = src.indexOf('\n', start);
  const line = nl < 0 ? src.slice(start) : src.slice(start, nl);
  if (line.includes('{') && line.trim().endsWith('}')) return line;
  const brace = src.indexOf('{', start);
  let depth = 0;
  for (let i = brace; i < src.length; i++) {
    if (src[i] === '{') depth++;
    else if (src[i] === '}') {
      depth--;
      if (depth === 0) return src.slice(start, i + 1);
    }
  }
  throw new Error('unterminated ' + name);
}

function replaceNamed(target, name, body) {
  const needle = `function ${name}(`;
  let start = -1, from = 0;
  while (true) {
    const idx = target.indexOf(needle, from);
    if (idx < 0) break;
    start = idx;
    from = idx + needle.length;
  }
  if (start < 0) return { text: target, replaced: false };
  const nl = target.indexOf('\n', start);
  const line = nl < 0 ? target.slice(start) : target.slice(start, nl);
  let end = -1;
  if (line.includes('{') && line.trim().endsWith('}')) end = start + line.length;
  else {
    const brace = target.indexOf('{', start);
    let depth = 0;
    for (let i = brace; i < target.length; i++) {
      if (target[i] === '{') depth++;
      else if (target[i] === '}') {
        depth--;
        if (depth === 0) { end = i + 1; break; }
      }
    }
  }
  if (end < 0) throw new Error('unterminated target ' + name);
  return { text: target.slice(0, start) + body + target.slice(end), replaced: true };
}

function insertAfter(target, markerFn, body) {
  if (target.includes(`function ${markerFn.split('(')[0].replace('function ', '')}` ) && target.includes(body.slice(0, 40))) {
    return target;
  }
  const extracted = extractNamed(target.includes('function selectedAiLessons(') ? target : target, 'selectedAiLessons');
  const idx = target.lastIndexOf(extracted);
  if (idx < 0) throw new Error('cannot insert after selectedAiLessons');
  const at = idx + extracted.length;
  if (target.slice(at, at + body.length).includes('function selectedNlsLessons')) return target;
  return target.slice(0, at) + '\n' + body + target.slice(at);
}

const source = fs.readFileSync(sourcePath, 'utf8');
if (!fs.existsSync(canvasPath)) {
  fs.copyFileSync(backupPath, canvasPath);
  console.log('created canvas_xaydungphuluc.html from backup');
}

const names = [
  'isLessonNlsSelected',
  'selectedPeriodsForLesson',
  'selectedNlsLessons',
  'pickAppendixOneRow',
  'cleanLessonName',
  'lessonKeywords',
  'lessonsMatch',
  'appendixThreeTable',
  'appendixOneIntegrationForLesson',
  'syncIntegrationFromAppendixOne',
  'preservedPpctTable',
  'getConfig',
  'appendixPrompt',
  'autoWrapMathInDelimiters',
  'isSinglePeriodLesson',
  'hasAiSelectionForLesson',
  'canUseNlsLesson',
  'chooseNlsLessonsForPeriods',
  'nlsAutoCandidates',
  'syncNlsSelectionFromRate',
  'syncNlsSelectionFromCount',
  'canUseAiPeriod',
  'aiAutoLessons',
  'syncAiSelectionFromRate',
  'syncAiSelectionFromCount',
  'allocationSummary',
  'densityUpperBound',
  'safeParseAiJson',
  'onNlsEnabledChange',
  'onAiEnabledChange',
  'foldSubjectName',
  'currentSubjectName',
  'isInformaticsSubject',
  'subjectPedagogyGroup',
  'nlsSubjectToolkit',
  'lessonAppliedNlsFallback',
  'lessonAppliedAiFallback',
  'calculateComplianceReport'
];

function syncFile(filePath) {
  let text = fs.readFileSync(filePath, 'utf8');
  const report = [];
  for (const name of names) {
    const body = extractNamed(source, name);
    if (text.includes(`function ${name}(`)) {
      const result = replaceNamed(text, name, body);
      text = result.text;
      report.push(result.replaced ? 'replaced ' + name : 'skip ' + name);
    } else if (name === 'selectedNlsLessons') {
      const after = extractNamed(text, 'selectedAiLessons');
      const idx = text.lastIndexOf(after);
      text = text.slice(0, idx + after.length) + '\n' + body + text.slice(idx + after.length);
      report.push('inserted ' + name);
    } else if (name === 'pickAppendixOneRow') {
      const needle = 'function appendixOneIntegrationForLesson(';
      const idx = text.lastIndexOf(needle);
      if (idx < 0) throw new Error('cannot insert pickAppendixOneRow into ' + filePath);
      text = text.slice(0, idx) + body + '\n' + text.slice(idx);
      report.push('inserted ' + name);
    } else {
      const close = text.lastIndexOf('</script>');
      if (close < 0) throw new Error('cannot insert ' + name);
      text = text.slice(0, close) + body + '\n' + text.slice(close);
      report.push('appended ' + name);
    }
  }
  text = text
    .replace('<input class="field" id="school" placeholder="THCS Trần Phú">', '<input class="field" id="school" value="THCS Trần Phú">')
    .replace('<input class="field" id="department" placeholder="Tổ Toán - Tin">', '<input class="field" id="department" value="Tổ Toán - Tin">')
    .replace('<input class="field" id="teacher" placeholder="Nguyễn Văn A">', '<input class="field" id="teacher" value="Hoàng Tấn Thiên">')
    .replace('dạy bài mới', 'PPCT')
    .replace('AI tự đề xuất bài/tiết tích hợp NLS &amp; AI; bạn rà soát và điều chỉnh', 'AI đề xuất bài/tiết tích hợp NLS &amp; AI; bạn rà soát và điều chỉnh');
  if (!text.includes('AI tự đề xuất bài/tiết phù hợp dựa trên PPCT và ngữ cảnh SGK')) {
    text = text.replace(
      'NLS chỉ sinh cho đúng bài được tick theo tỉ trọng CV 3456; mã AI chỉ sinh cho đúng tiết được chọn từ PPCT.',
      'AI tự đề xuất bài/tiết phù hợp dựa trên PPCT và ngữ cảnh SGK. Bạn có thể rà soát, tick hoặc bỏ tick để điều chỉnh.'
    );
  }
  fs.writeFileSync(filePath, text);
  console.log(path.relative(root, filePath) + ': ' + report.join(', '));
}

syncFile(backupPath);
syncFile(canvasPath);
