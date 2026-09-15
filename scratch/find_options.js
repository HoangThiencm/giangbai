const fs = require('fs');
const content = fs.readFileSync('thitructuyen.html', 'utf8');
const lines = content.split('\n');

lines.forEach((line, idx) => {
  if (line.includes('.options')) {
    console.log(`${idx + 1}: ${line.trim()}`);
  }
});
