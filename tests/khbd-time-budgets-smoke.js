const assert = require("assert");
const {
  calculateActivityTimeBudgets,
  getPromptTemplate,
  extractTextbookSubsections
} = require("../js/khbd-prompts.js");

console.log("==================================================");
console.log("BẮT ĐẦU KIỂM THỬ PHÂN BỔ THỜI LƯỢNG THÔNG MINH (TIME BUDGETS)");
console.log("==================================================");

// 1. Kiểm tra các mốc thời gian phổ biến và tính bảo toàn tổng số phút
const testCases = [
  { durationStr: "01 tiết (45 phút)", expectedTotal: 45, subs: 1 },
  { durationStr: "01 tiết (45 phút)", expectedTotal: 45, subs: 2 },
  { durationStr: "02 tiết (90 phút)", expectedTotal: 90, subs: 1 },
  { durationStr: "02 tiết (90 phút)", expectedTotal: 90, subs: 2 },
  { durationStr: "02 tiết (90 phút)", expectedTotal: 90, subs: 3 },
  { durationStr: "02 tiết (90 phút)", expectedTotal: 90, subs: 4 },
  { durationStr: "03 tiết (135 phút)", expectedTotal: 135, subs: 2 },
  { durationStr: "03 tiết (135 phút)", expectedTotal: 135, subs: 3 },
  { durationStr: "03 tiết (135 phút)", expectedTotal: 135, subs: 4 },
  { durationStr: "04 tiết (180 phút)", expectedTotal: 180, subs: 3 },
  { durationStr: "04 tiết (180 phút)", expectedTotal: 180, subs: 4 },
  { durationStr: "1 tiết", expectedTotal: 45, subs: 2 },
  { durationStr: "2 tiết", expectedTotal: 90, subs: 2 },
  { durationStr: "3 tiết", expectedTotal: 135, subs: 3 },
  { durationStr: "4 tiết", expectedTotal: 180, subs: 3 },
  { durationStr: "90p", expectedTotal: 90, subs: 2 },
  { durationStr: "120 phút", expectedTotal: 120, subs: 3 },
  { durationStr: "", expectedTotal: 90, subs: 2 }, // fallback
  { durationStr: "Không rõ", expectedTotal: 90, subs: 2 } // fallback
];

console.log("-> 1. Kiểm tra tổng số phút và phân bổ A, B, C, D, E...");
for (const tc of testCases) {
  const res = calculateActivityTimeBudgets(tc.durationStr, tc.subs, 6);
  
  // Tổng thời gian phân bổ phải đúng bằng expectedTotal
  assert.strictEqual(res.totalMinutes, tc.expectedTotal, `Total minutes mismatch for ${tc.durationStr}`);
  
  // Tổng A + B + C + D + E === totalMinutes
  const sumActivities = res.A + res.B + res.C + res.D + res.E;
  assert.strictEqual(sumActivities, tc.expectedTotal, `Sum of A+B+C+D+E (${sumActivities}) must equal total (${tc.expectedTotal}) for duration "${tc.durationStr}"`);

  // Tổng các tiểu mục B_subsections === B
  const sumBSubs = res.B_subsections.reduce((a, b) => a + b, 0);
  assert.strictEqual(sumBSubs, res.B, `Sum of B_subsections (${sumBSubs}) must equal B (${res.B}) for ${tc.subs} subsections`);
  assert.strictEqual(res.B_subsections.length, tc.subs, `B_subsections length must match subsectionCount ${tc.subs}`);

  // Kiểm tra formatted strings
  assert.strictEqual(res.formatted.A, `${res.A} phút`);
  assert.strictEqual(res.formatted.B, `${res.B} phút`);
  assert.strictEqual(res.formatted.C, `${res.C} phút`);
  assert.strictEqual(res.formatted.D, `${res.D} phút`);
  assert.strictEqual(res.formatted.E, `${res.E} phút`);
  assert.strictEqual(res.formatted.B_subsections.length, tc.subs);
}
console.log("  -> Phân bổ thời lượng và bảo toàn tổng thời gian: PASS (100% khớp)");

// 2. Kiểm tra việc thay thế placeholder trong getPromptTemplate
console.log("-> 2. Kiểm tra placeholder trong getPromptTemplate...");
const context = {
  subject: "toan",
  subjectName: "Toán",
  grade: "6",
  topic: "Tập hợp các số tự nhiên",
  duration: "02 tiết (90 phút)",
  textbook_content: `
I. Số và tập hợp các số tự nhiên
Nội dung 1...
II. Biểu diễn số tự nhiên trên tia số
Nội dung 2...
  `
};

const promptA = getPromptTemplate("GENERATE_ACTIVITY_A", context);
assert(!promptA.includes("{time_budget_A}"), "Placeholder {time_budget_A} must be replaced");
assert(/\(\d+\s*phút\)/.test(promptA), "Prompt Activity A must include time budget");

const promptB = getPromptTemplate("GENERATE_ACTIVITY_B", context);
assert(!promptB.includes("{time_budget_B}"), "Placeholder {time_budget_B} must be replaced");
assert(!promptB.includes("{time_budget_A}"), "All time budget placeholders must be replaced");
assert.match(promptB, /## B\. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI \(45 phút\)/, "Prompt Activity B must show its 45-minute budget");
assert.match(promptB, /Tổng số phút của TẤT CẢ hoạt động nhánh[\s\S]*?đúng bằng 45 phút/, "Prompt Activity B must lock the total of its branches");
assert(promptB.includes("Hoạt động 2.1: Số và tập hợp các số tự nhiên"), "Prompt Activity B must contain branch 1");
assert(promptB.includes("Hoạt động 2.2: Biểu diễn số tự nhiên trên tia số"), "Prompt Activity B must contain branch 2");

const promptE = getPromptTemplate("GENERATE_ACTIVITY_E", context);
assert(!promptE.includes("{time_budget_E}"), "Placeholder {time_budget_E} must be replaced");
assert(promptE.includes("HƯỚNG DẪN VỀ NHÀ"), "Prompt Activity E must contain correct title");

const prompt1Click = getPromptTemplate("GENERATE_ACTIVITIES_AE", context);
assert(prompt1Click.includes("<<<KHBD_A>>>"), "Prompt 1-Click must contain marker A");
assert(prompt1Click.includes("<<<KHBD_B>>>"), "Prompt 1-Click must contain marker B");
assert(prompt1Click.includes("<<<KHBD_C>>>"), "Prompt 1-Click must contain marker C");
assert(prompt1Click.includes("<<<KHBD_D>>>"), "Prompt 1-Click must contain marker D");
assert(prompt1Click.includes("<<<KHBD_E>>>"), "Prompt 1-Click must contain marker E");
assert.match(prompt1Click, /tổng A \+ B \+ C \+ D \+ E BẮT BUỘC đúng bằng toàn bộ thời lượng bài dạy 02 tiết \(90 phút\)/i, "Prompt must lock the full lesson duration");
console.log("  -> getPromptTemplate time budget injection: PASS");

console.log("==================================================");
console.log("TẤT CẢ TEST PHÂN BỔ THỜI LƯỢNG THÔNG MINH ĐỀU ĐẠT (PASS)!");
console.log("==================================================");
