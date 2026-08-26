const assert = require("assert");
const { getPromptTemplate } = require("../js/khbd-prompts.js");

const stub = {
  subjectName: "Toán",
  topic: "Tập hợp",
  duration: "2 tiết",
  objectives_content: "Mục tiêu",
  yccd_official: "",
  pedagogical_context: "",
  grade: "6",
  competencies: [],
  textbook_content: "Bài 1: Cho tập hợp A = {1,2}"
};

function main() {
  const promptC = getPromptTemplate("GENERATE_ACTIVITY_C", stub);
  assert.ok(promptC.includes("Bài 1: Cho tập hợp"), "GENERATE_ACTIVITY_C phải chứa textbook_content đã thay");
  assert.ok(!/\{textbook_content\}/.test(promptC), "GENERATE_ACTIVITY_C không được để sót {textbook_content}");
  assert.ok(!/Nếu nguồn không có bài luyện tập:\s*ghi/.test(promptC), "C đã nới câu placeholder cứng");
  assert.ok(/CẤM ghi "\[Không có trong tài liệu đã cung cấp\]"/.test(promptC), "C phải cấm placeholder khi nguồn đã có bài");

  const promptD = getPromptTemplate("GENERATE_ACTIVITY_D", stub);
  assert.ok(promptD.includes("Bài 1: Cho tập hợp"), "GENERATE_ACTIVITY_D phải chứa textbook_content đã thay");
  assert.ok(!/\{textbook_content\}/.test(promptD), "GENERATE_ACTIVITY_D không được để sót {textbook_content}");
  assert.ok(/CẤM ghi "\[Không có trong tài liệu đã cung cấp\]"/.test(promptD), "D phải cấm placeholder khi nguồn đã có bài");

  const promptObj = getPromptTemplate("GENERATE_OBJECTIVES", stub);
  assert.ok(!/NLS\/AI chỉ 2.?3/.test(promptObj), "Không còn quota gộp NLS/AI chỉ 2-3");
  assert.ok(!/năng lực số \/ AI: chỉ khi được bật; CHỈ 2/i.test(promptObj), "Không còn quota gộp năng lực số / AI");
  assert.ok(/đủ từng miền đã chọn/.test(promptObj) && /đủ từng mã đã chọn/.test(promptObj), "Phải có ý đủ từng miền/mã đã chọn");

  console.log("khbd-integrations-smoke: OK");
}

main();
