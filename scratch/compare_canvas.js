const fs = require('fs');
const orig = fs.readFileSync('canvas_soankhbd.html', 'utf8');
const curr = fs.readFileSync('canvas_soanbaigiang.html', 'utf8');

function getIds(html) {
  const matches = [...html.matchAll(/\bid=["']([^"']+)["']/g)];
  return new Set(matches.map(m => m[1]));
}

const origIds = getIds(orig);
const currIds = getIds(curr);

const missingInCurr = [...origIds].filter(id => !currIds.has(id));
console.log('Missing in curr:', missingInCurr);
const missingInOrig = [...currIds].filter(id => !origIds.has(id));
console.log('New in curr:', missingInOrig);

// Check scripts
const origScripts = [...orig.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].map(m => m[1]);
const currScripts = [...curr.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].map(m => m[1]);
console.log('Orig inline scripts:', origScripts.length, 'Curr inline scripts:', currScripts.length);
