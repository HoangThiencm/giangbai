const fs = require('fs');
const { execSync } = require('child_process');

const files = fs.readdirSync(__dirname).filter(f => f.endsWith('.js') && f !== 'run-all-tests.js');
let passed = 0;

for (const f of files) {
  console.log(`Running ${f}...`);
  try {
    execSync(`node "${__dirname}/${f}"`, { stdio: 'inherit' });
    passed++;
  } catch (e) {
    console.error(`FAILED: ${f}`);
    process.exit(1);
  }
}

console.log(`\n========================================\nALL ${passed} TEST SUITES PASSED 100%!\n========================================`);
