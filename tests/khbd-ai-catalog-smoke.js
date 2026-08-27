const assert = require("assert");
const { KHBD_STANDARDS, recommendOfficialStandards } = require("../js/khbd-standards.js");

const expectedCodes = {
  6: "A1.1 A1.2 A1.3 A3.1 A3.2 A3.3 A3.4 B1.1 B2.1 C1.1 C1.MR1 C1.MR2 C1.2 C1.MR3 C2.1 C2.2 C2.MR1 C3.1 C3.MR1 D1.1 D1.MR1 D2.1 D2.MR1 D2.MR2".split(" "),
  7: "A1.1 A1.2 A1.MR1 A2.1 A2.2 A3.1 A3.MR1 A3.MR2 A3.2 B2.1 B2.2 B3.1 C4.1 C4.MR1 C5.1 C5.2 C5.MR1 D1.1 D1.MR1 D2.1 D2.MR1".split(" "),
  8: "A1.1 A1.2 A2.1 A2.2 A3.1 A3.MR1 A3.2 A3.3 A3.MR2 B1.1 B2.1 B3.1 C1.1 C1.MR1 C5.1 C5.MR1 D1.1 D1.MR1 D2.1 D2.MR1 D2.MR2".split(" "),
  9: "A1.1 A2.1 A2.2 A3.1 A3.2 A3.3 A3.4 B2.1 B2.2 B2.3 B3.1 B3.2 C2.1 C2.MR1 C4.1 C4.MR1 C4.MR2 D1.1 D1.MR1 D2.1 D2.MR1 D2.MR2".split(" ")
};

const entries = KHBD_STANDARDS.ai.entries;
for (const [gradeText, suffixes] of Object.entries(expectedCodes)) {
  const grade = Number(gradeText);
  const actual = entries.filter(entry => entry.grades.length === 1 && entry.grades[0] === grade).map(entry => entry.code);
  assert.deepStrictEqual(actual, suffixes.map(suffix => `${grade}.${suffix}`), `Catalog QĐ 2422 lớp ${grade} phải đủ cả YCCĐ MR`);
}
assert.strictEqual(entries.length, 88, "Catalog AI lớp 6–9 phải có đủ 88 YCCĐ");
assert.ok(entries.every(entry => entry.label && entry.id && entry.code), "Mỗi YCCĐ phải có mã, id và nội dung");

const digital = KHBD_STANDARDS.digital.entries;
const nls67 = digital.filter(entry => entry.grades.includes(6));
const nls89 = digital.filter(entry => entry.grades.includes(8));
assert.strictEqual(nls67.length, 24, "Lớp 6–7 phải hiện đủ 24 năng lực thành phần NLS");
assert.strictEqual(nls89.length, 24, "Lớp 8–9 phải hiện đủ 24 năng lực thành phần NLS");
assert.ok(nls67.every(entry => entry.band.includes("6–7") && entry.descriptor.includes("vấn đề đơn giản")), "Lớp 6 chỉ dùng mô tả Trung cấp 1");
assert.ok(nls89.every(entry => entry.band.includes("8–9") && entry.descriptor.includes("không theo thông lệ")), "Lớp 8 chỉ dùng mô tả Trung cấp 2");
assert.ok(nls67.every(entry => !nls89.some(other => other.id === entry.id)), "Không được dùng chung lựa chọn giữa hai dải NLS");

const baseContext = { vision: "Bài tập về tập hợp", subjectName: "Toán", facilities: { internet: true }, methods: [], activities: [] };
assert.deepStrictEqual(recommendOfficialStandards("ai", { ...baseContext, grade: 6, aiOn: false }), [], "Không tự đề xuất AI khi chưa chọn tích hợp và nội dung không có AI");
for (const grade of [6, 7, 8, 9]) {
  const recommended = recommendOfficialStandards("ai", { ...baseContext, grade, aiOn: true });
  assert.ok(recommended.every(entry => entry.grade === grade && entry.officialCode.startsWith(`${grade}.`)), `Chỉ đề xuất mã AI đúng lớp ${grade}`);
}
console.log("khbd AI catalog smoke: passed");
