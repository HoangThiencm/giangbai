const fs = require('fs');
const path = require('path');
const assert = require('assert');

const html = fs.readFileSync(path.join(__dirname, '..', 'kttx.html'), 'utf8');
const babelStart = html.indexOf('<script type="text/babel"');
const babelEnd = html.indexOf('</script>', babelStart);
assert(babelStart >= 0 && babelEnd > babelStart, 'KTTX must contain one complete Babel application script');
const babel = html.slice(babelStart, babelEnd);

['exportWord', 'exportMatrixToWord', 'renderSpecHtml'].forEach(name => {
  const start = babel.indexOf(`const ${name}`);
  assert(start >= 0, `${name} must exist`);
  const next = babel.indexOf('\n            const ', start + 1);
  const block = babel.slice(start, next >= 0 ? next : babel.length);
  assert(!/<script\b/i.test(block) && !/<\/script>/i.test(block), `${name} Word template must not contain script tags`);
  assert(block.includes("<meta charset='utf-8'>"), `${name} Word template must declare UTF-8`);
});
assert(!babel.includes("phút</p></div><hr/>"), 'exam Word template must not contain an orphan closing div');
assert(babel.includes("fetch('api/user_gemini_keys.php', { credentials: 'include', cache: 'no-store' })"), 'must fetch account Gemini keys with the session credentials');
assert(babel.includes('const syncUserKeysFromServer = async'), 'must define key synchronization');
assert(babel.includes("localStorage.setItem('global_gemini_keys'"), 'must cache synchronized Gemini keys');
assert(babel.includes('readCachedGeminiKeys') && babel.includes("source: 'cache'"), 'must safely fall back to cached keys');
assert(babel.includes('useEffect(() => {\n                let active = true;\n                syncUserKeysFromServer()'), 'must synchronize keys when React mounts');
assert(babel.includes('Đã nạp ${keys.length} Gemini API Key'), 'must show the number of account keys loaded');

console.log('kttx smoke: Word templates and account Gemini key synchronization passed');
