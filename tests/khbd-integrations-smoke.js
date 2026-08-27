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
  const promptA = getPromptTemplate("GENERATE_ACTIVITY_A", stub);
  assert.ok(promptA.includes("KỊCH BẢN TÍCH HỢP NĂNG LỰC SỐ (NLS) VÀ NĂNG LỰC AI"), "Prompt A phải chứa contract kịch bản NLS/AI");
  assert.ok(promptA.includes("[NLS:"), "Prompt A phải chứa hướng dẫn marker [NLS:");
  assert.ok(promptA.includes("[AI:"), "Prompt A phải chứa hướng dẫn marker [AI:");

  const promptB = getPromptTemplate("GENERATE_ACTIVITY_B", stub);
  assert.ok(promptB.includes("KỊCH BẢN TÍCH HỢP NĂNG LỰC SỐ (NLS) VÀ NĂNG LỰC AI"), "Prompt B phải chứa contract kịch bản NLS/AI");

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

  // Kiểm tra DocxGenerator styling cho NLS và AI
  const { DocxGenerator } = require("../js/khbd-docx.js");
  const generator = new DocxGenerator();
  
  const nlsBadge = generator.markerRunColor("[NLS: Miền 1 - Khai thác GeoGebra]");
  assert.deepStrictEqual(nlsBadge, { color: "0369A1", shading: "E0F2FE", bold: true }, "NLS badge phải có màu chữ 0369A1 và nền E0F2FE");

  const aiBadge = generator.markerRunColor("[AI: 1.A1.1 - Kiểm chứng kết quả]");
  assert.deepStrictEqual(aiBadge, { color: "6D28D9", shading: "F3E8FF", bold: true }, "AI badge phải có màu chữ 6D28D9 và nền F3E8FF");

  assert.strictEqual(generator.headingIntegrationColor("### c) Năng lực số"), "0369A1", "Heading NLS phải có màu 0369A1");
  assert.strictEqual(generator.headingIntegrationColor("### d) Năng lực AI"), "6D28D9", "Heading AI phải có màu 6D28D9");

  // Kiểm tra parseInlineTextToRuns với mock TextRun
  global.window = {
    docx: {
      TextRun: class MockTextRun {
        constructor(props) { Object.assign(this, props); }
      },
      ShadingType: { CLEAR: "clear" }
    }
  };

  const runs = generator.parseInlineTextToRuns("GV hướng dẫn **[NLS: Miền 1 - GeoGebra]** và **[AI: 1.A1.1 - Prompt]**");
  assert.ok(runs.some(r => r.text === "[NLS: Miền 1 - GeoGebra]" && r.color === "0369A1" && r.shading?.fill === "E0F2FE"), "TextRun NLS phải có đúng màu và shading");
  assert.ok(runs.some(r => r.text === "[AI: 1.A1.1 - Prompt]" && r.color === "6D28D9" && r.shading?.fill === "F3E8FF"), "TextRun AI phải có đúng màu và shading");

  console.log("khbd-integrations-smoke: OK");
}

main();
