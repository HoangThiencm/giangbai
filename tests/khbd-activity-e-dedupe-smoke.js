const assert = require("assert");
const { clipKhbdActivityMarkdown } = require("../js/khbd-app.js");
const { getPromptTemplate } = require("../js/khbd-prompts.js");

const leakedD = `## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)
### a) Mục tiêu:
- Vận dụng tập hợp vào tình huống thực tế.
### b) Nội dung:
- Bài toán thực tế trong SGK.
## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ (3 phút)
- Ôn tập lại 2 cách mô tả tập hợp.
- Hoàn thành các bài tập còn lại trong SGK: 1.1, 1.2.`;
const clippedD = clipKhbdActivityMarkdown("D", leakedD);
assert.match(clippedD, /VẬN DỤNG/);
assert.doesNotMatch(clippedD, /HƯỚNG DẪN VỀ NHÀ/);

const dupE = `## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ (3 phút)
- Ôn tập lại 2 cách mô tả tập hợp.
- Ghi nhớ kí hiệu ∈, ∉, ℕ, ℕ*.
- [NLS: 1.3] Tìm hiểu nhà toán học Cantor.

## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ (4 phút)
1. Ôn tập kiến thức: Ôn lại định nghĩa tập hợp.
2. Làm bài tập: Hoàn thành các bài tập còn lại trong SGK.
3. Chuẩn bị bài mới: Đọc bài số tự nhiên.
4. Nhiệm vụ tìm tòi, mở rộng: Tìm hiểu nhà toán học Cantor.`;
const clippedE = clipKhbdActivityMarkdown("E", dupE);
assert.match(clippedE, /1\. Ôn tập kiến thức:/);
assert.match(clippedE, /\(4 phút\)/);
assert.doesNotMatch(clippedE, /\(3 phút\)/);
assert.doesNotMatch(clippedE, /### a\) Mục tiêu:/);
assert.equal((clippedE.match(/HOẠT ĐỘNG 5/g) || []).length, 1);

const promptE = getPromptTemplate("GENERATE_ACTIVITY_E", {
  subjectName: "Toán",
  topic: "Tập hợp",
  duration: "2 tiết",
  objectives_content: "",
  activities_content: ""
});
assert.match(promptE, /CHỈ xuất ĐÚNG MỘT khối/);
const promptD = getPromptTemplate("GENERATE_ACTIVITY_D", {
  subjectName: "Toán",
  topic: "Tập hợp",
  duration: "2 tiết",
  objectives_content: "",
  textbook_content: "Vận dụng\nBài toán thực tế"
});
assert.match(promptD, /CẤM viết mục E/);

console.log("khbd activity E dedupe smoke: passed");
