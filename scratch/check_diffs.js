const fs = require('fs');
const orig = fs.readFileSync('canvas_soankhbd.html', 'utf8');
const curr = fs.readFileSync('canvas_soanbaigiang.html', 'utf8');

// Compare script tags and their content
const getScriptBlocks = (html) => {
  return [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].map(m => m[1]);
};

const origScripts = getScriptBlocks(orig);
const currScripts = getScriptBlocks(curr);

console.log(`Orig scripts: ${origScripts.length}, Curr scripts: ${currScripts.length}`);
for (let i = 0; i < Math.min(origScripts.length, currScripts.length); i++) {
  if (origScripts[i].trim() !== currScripts[i].trim()) {
    console.log(`Script block #${i+1} differs!`);
    console.log(`  Orig length: ${origScripts[i].length}, Curr length: ${currScripts[i].length}`);
    // find first difference
    for (let j = 0; j < Math.min(origScripts[i].length, currScripts[i].length); j++) {
      if (origScripts[i][j] !== currScripts[i][j]) {
        console.log(`  First diff at char ${j}:`);
        console.log(`  Orig snippet:`, origScripts[i].slice(Math.max(0, j-30), j+50));
        console.log(`  Curr snippet:`, currScripts[i].slice(Math.max(0, j-30), j+50));
        break;
      }
    }
  }
}
