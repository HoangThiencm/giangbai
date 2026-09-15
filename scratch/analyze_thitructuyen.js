const fs = require('fs');
const content = fs.readFileSync('thitructuyen.html', 'utf8');
const lines = content.split('\n');

console.log('Total lines:', lines.length);

const found = [];
lines.forEach((line, idx) => {
  const trimmed = line.trim();
  if (
    trimmed.startsWith('function ') ||
    trimmed.startsWith('const ') && trimmed.includes('= () =>') ||
    trimmed.startsWith('const ') && trimmed.includes('= function') ||
    trimmed.includes('type="text/babel"') ||
    trimmed.includes('view ===') ||
    trimmed.includes('setExamData') ||
    trimmed.includes('questions:') ||
    trimmed.includes('questions.map') ||
    trimmed.includes('options.map') ||
    trimmed.includes('type: "') ||
    trimmed.includes("type: '") ||
    trimmed.includes('correctAnswer') ||
    trimmed.includes('correct_answer')
  ) {
    if (trimmed.length < 120) {
      found.push(`${idx + 1}: ${trimmed}`);
    }
  }
});

console.log('Found ' + found.length + ' points:');
found.forEach(f => console.log(f));
