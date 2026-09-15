const fs = require('fs');
const assert = require('assert');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const navChipRule = html.match(/\.nav-chip\s*\{[\s\S]*?\n\s*\}/);

assert.ok(navChipRule, '.nav-chip rule must exist.');
assert.doesNotMatch(navChipRule[0], /color:\s*#e2e8f0/i, '.nav-chip must not use the low-contrast legacy color.');
assert.match(navChipRule[0], /display:\s*inline-flex;/, '.nav-chip must align its icon and label.');
assert.match(navChipRule[0], /align-items:\s*center;/, '.nav-chip must vertically align its contents.');
assert.match(navChipRule[0], /background:\s*#f1f5f9;/i, '.nav-chip must use a light slate background.');
assert.match(navChipRule[0], /border:\s*1px solid #e2e8f0;/i, '.nav-chip must use the matching slate border.');
assert.match(navChipRule[0], /color:\s*#334155;/i, '.nav-chip must use high-contrast slate text.');

assert.match(html, /navBadge\.className = 'nav-chip[^']*font-bold[^']*bg-emerald-50[^']*text-emerald-800[^']*border-emerald-200[^']*';/, 'Student badge must use bold emerald-800 text on emerald-50.');
assert.match(html, /navBadge\.style\.color = '#065f46';/, 'Student badge must set an explicit contrast-safe emerald color.');
assert.match(html, /fa-graduation-cap mr-1\.5 text-emerald-600/, 'Student badge icon must use emerald-600.');

assert.match(html, /<span class="nav-chip[^\"]*px-3 py-1\.5[^\"]*bg-slate-100[^\"]*text-slate-700[^\"]*border-slate-200[^\"]*">\s*<i class="fas fa-sparkles mr-1\.5 text-indigo-500"><\/i> Cập nhật đồng bộ/s, 'Teacher chip must use readable slate text and indigo icon on a light background.');

console.log('nav-chip contrast smoke: PASS');
