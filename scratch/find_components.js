const fs = require('fs');
const content = fs.readFileSync('thitructuyen.html', 'utf8');
const lines = content.split('\n');

lines.forEach((line, idx) => {
  const m = line.match(/const\s+([A-Za-z0-9_]+)\s*=\s*(\([^)]*\)|[A-Za-z0-9_]+)?\s*=>/);
  if (m) {
    console.log(`${idx + 1}: const ${m[1]}`);
  }
});
