const fs=require('fs'),assert=require('assert');

const files=[
  'backupcode viettailieu/canvas_soankhbd.html',
  'backupcode viettailieu/soanbaigemini.html',
  'backupcode viettailieu/taobaitap.html',
  'backupcode viettailieu/taobaocao.html',
  'backupcode viettailieu/sangkien.html',
  'backupcode viettailieu/chuyenpdf.html'
];

for(const file of files){
  const html=fs.readFileSync(file,'utf8');
  assert(/<html\b/i.test(html)&&/<body\b/i.test(html)&&/<\/body>/i.test(html),`${file}: HTML document must remain complete`);
  assert(html.includes('canvasHostBanner'),`${file}: missing Gemini Canvas status banner`);
  assert(html.includes('MutationObserver'),`${file}: missing anti-FOUC visibility observer`);
  assert(/html\s*,\s*body\s*\{\s*display:\s*block\s*!important/i.test(html),`${file}: missing force-visible first-paint style`);
  assert(html.includes('max-w-[98%]')||html.includes('max-width: 98%')||html.includes('max-width:98%'),`${file}: missing expanded Canvas layout`);
  assert(html.includes('toggleCompactMode'),`${file}: missing compact-mode control`);
  assert(html.includes('getCanvasStorage')&&html.includes('memoryStorage'),`${file}: missing sandbox-safe in-memory storage fallback`);
  assert(html.includes('canvasConfirm'),`${file}: missing Canvas DOM confirmation API`);
}

const quiz=fs.readFileSync('backupcode viettailieu/taobaitap.html','utf8');
assert(quiz.includes('await window.canvasConfirm(`Bạn có chắc chắn muốn xóa'), 'taobaitap must use Canvas confirmation rather than browser confirm');
assert(!quiz.includes('if (confirm(`Bạn có chắc chắn muốn xóa'), 'taobaitap must not call browser confirm for deletion');
const report=fs.readFileSync('backupcode viettailieu/taobaocao.html','utf8');
assert(report.includes('await canvasConfirm("Bạn có chắc muốn xóa phụ lục này không?")'), 'taobaocao must use the Canvas confirmation modal for appendix deletion');
const protectedBackup='backupcode viettailieu/soanbaigemini_bakcup_khong đụng tới.html';
assert(fs.existsSync(protectedBackup),'the protected original backup must remain present');
console.log('backupcode-canvas-smoke: PASS');
