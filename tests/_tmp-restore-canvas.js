const fs = require('fs');
const src = fs.readFileSync('xaydungphuluc.html', 'utf8');
const start = src.indexOf('/* Smart SGK index + explicit AI selection.');
const end = src.indexOf('function syncRanges(){if(typeof nlsSelectedLessonIds');
if (start < 0 || end < 0) throw new Error('cannot extract smart sgk block');
const block = src.slice(start, end);
const files = ['canvas_xaydungphuluc.html', 'backupcode viettailieu/canvas_xaydungphuluc.html'];
for (const f of files) {
  let s = fs.readFileSync(f, 'utf8');
  if (s.includes('function nlsCandidates()') && s.includes('const AI_SELECTION_LIMIT=12')) {
    console.log('already restored', f);
    continue;
  }
  const needle = 'function syncRanges(){if(typeof nlsSelectedLessonIds';
  const idx = s.indexOf(needle);
  if (idx < 0) throw new Error('missing syncRanges needle in ' + f);
  s = s.slice(0, idx) + block + s.slice(idx);
  fs.writeFileSync(f, s);
  console.log('restored', f, 'block chars', block.length);
}
