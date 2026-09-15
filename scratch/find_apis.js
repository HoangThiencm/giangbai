const fs = require('fs');
const content = fs.readFileSync('thitructuyen.html', 'utf8');
const lines = content.split('\n');

const apiCalls = [];
lines.forEach((line, idx) => {
  if (/axios|\bfetch\b|\/api\/|api_keys|supabase/i.test(line)) {
    if (line.trim().length < 150) {
      apiCalls.push(`${idx + 1}: ${line.trim()}`);
    }
  }
});
console.log('Found ' + apiCalls.length + ' lines:');
apiCalls.slice(0, 40).forEach(l => console.log(l));
