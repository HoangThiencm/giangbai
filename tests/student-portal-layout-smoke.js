/* Static contract checks for the responsive student portal section layout. */
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const index = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const fail = message => { throw new Error(message); };
const requireMatch = (text, pattern, message) => {
    if (!pattern.test(text)) fail(message);
};

requireMatch(
    index,
    /<div id="studentSectionsWrap" class="grid grid-cols-1 gap-8 mb-8">[\s\S]*?<div id="studentLotrinhSection"[\s\S]*?<div id="studentActivitiesSection"[\s\S]*?<\/div>\s*<\/div>\s*<!-- Khi chưa được phân quyền/,
    'studentSectionsWrap must contain both student portal sections before the empty state.'
);

requireMatch(
    index,
    /const hasMath = allowedMath\.length > 0;[\s\S]*?const hasTools = allowedTools\.length > 0;[\s\S]*?const sectionsWrap = document\.getElementById\('studentSectionsWrap'\);/,
    'renderStudentPortal must derive visibility state for both section groups.'
);

requireMatch(
    index,
    /if \(hasMath && hasTools\) \{[\s\S]*?sectionsWrap\.className = 'grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8';/,
    'When both groups have content, the wrapper must switch to a two-column large-screen layout.'
);

requireMatch(
    index,
    /lotrinhSection\.className = 'flex flex-col';[\s\S]*?activitiesSection\.className = 'flex flex-col';/,
    'Both visible groups must use flex columns so their cards stretch consistently.'
);

requireMatch(
    index,
    /lotrinhGrid\.className = allowedMath\.length > 1[\s\S]*?'grid grid-cols-1 gap-4 flex-1';/,
    'A single learning-route card must fill its half instead of reserving extra columns.'
);

requireMatch(
    index,
    /activitiesGrid\.className = allowedTools\.length > 1[\s\S]*?'grid grid-cols-1 gap-4 flex-1';/,
    'A single activity card must fill its half instead of reserving extra columns.'
);

requireMatch(
    index,
    /else \{[\s\S]*?sectionsWrap\.className = 'grid grid-cols-1 gap-8 mb-8';[\s\S]*?lotrinhGrid\.className = 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4';[\s\S]*?activitiesGrid\.className = 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4';/,
    'A lone visible group must keep the full-width responsive three-column layout.'
);

console.log('student-portal-layout smoke: PASS');
