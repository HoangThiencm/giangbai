'use strict';

const assert = require('assert');
const {
  CURRICULUM_DATA,
  getLessonsForBook,
  getSubjectsForGrade,
  lessonsBySubject
} = require('../js/khbd-curriculum.js');

function countItems(chapters) {
  return (chapters || []).reduce((n, ch) => n + (ch.items || []).length, 0);
}

assert.deepStrictEqual(
  CURRICULUM_DATA.grades.map((g) => g.id),
  ['6', '7', '8', '9'],
  'grades chỉ 6–9'
);

const subjectIds = CURRICULUM_DATA.subjects.map((s) => s.id);
assert.ok(!subjectIds.includes('tiengviet'), 'không còn tiengviet');
assert.ok(!subjectIds.includes('vatly'), 'không còn vatly');
assert.ok(!subjectIds.includes('gdqpan'), 'không còn gdqpan');
assert.ok(subjectIds.includes('toan') && subjectIds.includes('nguvan'));

assert.ok(countItems(getLessonsForBook('toan', 'x', 6)) > 5, 'toan 6');
assert.ok(countItems(getLessonsForBook('nguvan', 'x', 6)) > 5, 'nguvan 6');
assert.ok(countItems(getLessonsForBook('khtn', 'x', 6)) > 10, 'khtn 6');
assert.ok(countItems(getLessonsForBook('tinhoc', 'x', 6)) > 5, 'tinhoc 6');
assert.ok(countItems(getLessonsForBook('lichsudialy', 'x', 6)) > 5, 'lichsudialy 6');
assert.ok(countItems(getLessonsForBook('gdcd', 'x', 6)) > 3, 'gdcd 6');

const bySub = lessonsBySubject || CURRICULUM_DATA.lessonsBySubject;
const labelBlob = JSON.stringify(bySub);
assert.ok(!/kntt|kết nối tri thức/i.test(labelBlob), 'không ghi KNTT trên nhãn mục lục');

assert.ok(countItems(getLessonsForBook('nguvan', 'x', 7)) > 0, 'nguvan 7 không rỗng');
assert.ok(countItems(getLessonsForBook('khtn', 'x', 7)) > 0, 'khtn 7 không rỗng');
assert.ok(countItems(getLessonsForBook('nguvan', 'x', 8)) > 0, 'nguvan 8 không rỗng');
assert.ok(countItems(getLessonsForBook('khtn', 'x', 8)) > 0, 'khtn 8 không rỗng');
assert.ok(countItems(getLessonsForBook('nguvan', 'x', 9)) > 0, 'nguvan 9 không rỗng');

const khtn9 = countItems(getLessonsForBook('khtn', 'x', 9));
const tinhoc9 = countItems(getLessonsForBook('tinhoc', 'x', 9));
if (!khtn9) console.warn('LOG: khtn lớp 9 trống');
if (!tinhoc9) console.warn('LOG: tinhoc lớp 9 trống');

const grade6Subjects = getSubjectsForGrade(6).map((s) => s.id);
assert.ok(grade6Subjects.includes('toan') && grade6Subjects.includes('nguvan'));
assert.ok(!grade6Subjects.includes('vatly'));

console.log('khbd-curriculum-thcs-smoke: OK');
for (const sub of CURRICULUM_DATA.subjects) {
  for (const g of ['6', '7', '8', '9']) {
    const ch = getLessonsForBook(sub.id, 'bo-sach-chung', g);
    console.log(`  ${sub.id} ${g}: ${ch.length} chương, ${countItems(ch)} bài`);
  }
}
