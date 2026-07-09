const fs = require('fs');
const html = fs.readFileSync('thoikhoabieu.html', 'utf8');
const need = [
  'evaluateBeauty',
  'beautifySchedule',
  'loadSampleData16',
  'goodDoubles',
  'qualityBoard',
  'optionDoubleBonus',
  'isCoreSubject',
  'isDoubleFriendlySubject',
];
for (const n of need) {
  console.log(html.includes(n) ? 'OK' : 'MISSING', n);
}
const start = html.indexOf('<script>');
const end = html.lastIndexOf('</script>');
const s = html.slice(start + 8, end);
let bal = 0;
let min = 0;
for (const ch of s) {
  if (ch === '{') bal++;
  if (ch === '}') bal--;
  if (bal < min) min = bal;
}
console.log('brace balance', bal, 'min', min, 'len', s.length);

// Extract pure functions into a runnable demo by eval-ing a patched subset is hard.
// Instead: dynamic extract loadSampleData16 + solver by wrapping state.
try {
  // Quick parse check via Function constructor (syntax only)
  // strip browser-only bits
  let code = s
    .replace(/document\.[^;]+;/g, ';')
    .replace(/window\./g, '')
    .replace(/\$\(/g, '(__missing$(');
  // Just syntax-check the original script body with stubs
  const stubs = `
    const document = { getElementById: () => ({
      addEventListener(){}, querySelectorAll(){return []}, classList:{toggle(){},add(){},remove(){}},
      value:'', innerHTML:'', textContent:'', disabled:false, style:{}, dataset:{}
    }), querySelectorAll: () => [], querySelector: () => null};
    const window = { setTimeout: (fn) => fn(), print(){}, XLSX: null };
    const localStorage = { getItem: () => null, setItem(){} };
    const alert = () => {};
    const fetch = async () => ({ ok:false, json: async () => ({}) });
    const URL = { createObjectURL: () => '', revokeObjectURL(){} };
    const Blob = function(){};
  `;
  // Don't run full page - only syntax
  new Function(stubs + s.replace(/initTimetablePage\(\);/, ''));
  console.log('Function() syntax: OK');
} catch (e) {
  console.log('Function() syntax FAIL:', e.message);
}
