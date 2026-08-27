const assert = require("assert");
const { getPromptTemplate, getSystemRole, PROMPTS } = require("../js/khbd-prompts.js");

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
  // 1. Kiểm tra Contract tích hợp NLS & AI thực chiến
  const promptA = getPromptTemplate("GENERATE_ACTIVITY_A", stub);
  assert.ok(promptA.includes("KỊCH BẢN TÍCH HỢP NĂNG LỰC SỐ (NLS) VÀ NĂNG LỰC AI THỰC CHIẾN GẮN MÔN HỌC"), "Prompt A phải chứa contract kịch bản NLS/AI thực chiến");
  assert.ok(promptA.includes("Dạng 1 (Kiểm chứng & Phản biện lỗi sai của AI)"), "Phải có Dạng 1: Kiểm chứng lỗi sai AI");
  assert.ok(promptA.includes("Dạng 2 (Prompting tư duy môn học)"), "Phải có Dạng 2: Prompting tư duy môn học");
  assert.ok(promptA.includes("Dạng 3 (Phần mềm chuyên dụng NLS)"), "Phải có Dạng 3: Phần mềm chuyên dụng NLS");
  assert.ok(promptA.includes("Kiểm chứng phản hồi AI"), "Phải có marker kiểm chứng phản hồi AI");
  assert.ok(promptA.includes("Prompting gợi mở & Tự giải"), "Phải có marker prompting gợi mở");
  assert.ok(promptA.includes("TUYỆT ĐỐI CẤM giáo viên hỏi miệng chung chung về định nghĩa hay lý thuyết AI"), "Phải có điều khoản cấm hỏi lý thuyết AI suông");
  assert.ok(promptA.includes("TUYỆT ĐỐI CẤM rải tag dồn dập"), "Phải cấm rải tag dồn dập");
  assert.ok(promptA.includes("CHỈ tích hợp tại 1 đến 2 vị trí then chốt"), "Phải chỉ định 1-2 vị trí then chốt");

  const promptB = getPromptTemplate("GENERATE_ACTIVITY_B", stub);
  assert.ok(promptB.includes("KỊCH BẢN TÍCH HỢP NĂNG LỰC SỐ (NLS) VÀ NĂNG LỰC AI THỰC CHIẾN"), "Prompt B phải chứa contract kịch bản NLS/AI thực chiến");
  assert.ok(promptB.includes("CẤM hỏi lý thuyết AI suông"), "Prompt B phải cấm hỏi lý thuyết AI suông");

  const promptC = getPromptTemplate("GENERATE_ACTIVITY_C", stub);
  assert.ok(promptC.includes("Bài 1: Cho tập hợp"), "GENERATE_ACTIVITY_C phải chứa textbook_content đã thay");
  assert.ok(!/\{textbook_content\}/.test(promptC), "GENERATE_ACTIVITY_C không được để sót {textbook_content}");
  assert.ok(!/Nếu nguồn không có bài luyện tập:\s*ghi/.test(promptC), "C đã nới câu placeholder cứng");
  assert.ok(/CẤM ghi "\[Không có trong tài liệu đã cung cấp\]"/.test(promptC), "C phải cấm placeholder khi nguồn đã có bài");
  assert.ok(promptC.includes("CẤM hỏi lý thuyết AI suông"), "Prompt C phải cấm hỏi lý thuyết AI suông");

  const promptD = getPromptTemplate("GENERATE_ACTIVITY_D", stub);
  assert.ok(promptD.includes("Bài 1: Cho tập hợp"), "GENERATE_ACTIVITY_D phải chứa textbook_content đã thay");
  assert.ok(!/\{textbook_content\}/.test(promptD), "GENERATE_ACTIVITY_D không được để sót {textbook_content}");
  assert.ok(/CẤM ghi "\[Không có trong tài liệu đã cung cấp\]"/.test(promptD), "D phải cấm placeholder khi nguồn đã có bài");
  assert.ok(promptD.includes("CẤM hỏi lý thuyết AI suông"), "Prompt D phải cấm hỏi lý thuyết AI suông");

  // 2. Kiểm tra SYSTEM_ROLE và getSystemRole
  assert.ok(PROMPTS.SYSTEM_ROLE.includes("công cụ thực hành của môn học"), "PROMPTS.SYSTEM_ROLE phải có nguyên tắc NLS/AI là công cụ thực hành");
  const sysRole = getSystemRole("toan", "6");
  assert.ok(sysRole.includes("công cụ thực hành của môn học"), "getSystemRole phải có nguyên tắc NLS/AI là công cụ thực hành");
  assert.ok(sysRole.includes("TUYỆT ĐỐI KHÔNG dạy lý thuyết Tin học/AI hay hỏi lý thuyết AI suông"), "getSystemRole phải cấm lý thuyết AI suông");

  const promptObj = getPromptTemplate("GENERATE_OBJECTIVES", stub);
  assert.ok(!/NLS\/AI chỉ 2.?3/.test(promptObj), "Không còn quota gộp NLS/AI chỉ 2-3");
  assert.ok(!/năng lực số \/ AI: chỉ khi được bật; CHỈ 2/i.test(promptObj), "Không còn quota gộp năng lực số / AI");
  assert.ok(/đủ từng miền đã chọn/.test(promptObj) && /đủ từng mã đã chọn/.test(promptObj), "Phải có ý đủ từng miền/mã đã chọn");

  // 3. Kiểm tra DocxGenerator styling cho NLS và AI với các marker chuẩn mới
  const { DocxGenerator } = require("../js/khbd-docx.js");
  const generator = new DocxGenerator();
  
  const nlsBadge = generator.markerRunColor("[NLS: Miền 1 - GeoGebra]");
  assert.deepStrictEqual(nlsBadge, { color: "0369A1", shading: "E0F2FE", bold: true }, "NLS badge phải có màu chữ 0369A1 và nền E0F2FE");

  const aiBadge1 = generator.markerRunColor("[AI: 1.A1.1 - Kiểm chứng phản hồi AI]");
  assert.deepStrictEqual(aiBadge1, { color: "6D28D9", shading: "F3E8FF", bold: true }, "AI badge 1 phải có màu chữ 6D28D9 và nền F3E8FF");

  const aiBadge2 = generator.markerRunColor("[AI: 1.A1.2 - Prompting gợi mở & Tự giải]");
  assert.deepStrictEqual(aiBadge2, { color: "6D28D9", shading: "F3E8FF", bold: true }, "AI badge 2 phải có màu chữ 6D28D9 và nền F3E8FF");

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

  const runs = generator.parseInlineTextToRuns("GV giao **[NLS: Miền 1 - GeoGebra]**, chiếu lời giải **[AI: 1.A1.1 - Kiểm chứng phản hồi AI]** và **[AI: 1.A1.2 - Prompting gợi mở & Tự giải]**");
  assert.ok(runs.some(r => r.text === "[NLS: Miền 1 - GeoGebra]" && r.color === "0369A1" && r.shading?.fill === "E0F2FE"), "TextRun NLS phải có đúng màu và shading");
  assert.ok(runs.some(r => r.text === "[AI: 1.A1.1 - Kiểm chứng phản hồi AI]" && r.color === "6D28D9" && r.shading?.fill === "F3E8FF"), "TextRun AI 1 phải có đúng màu và shading");
  assert.ok(runs.some(r => r.text === "[AI: 1.A1.2 - Prompting gợi mở & Tự giải]" && r.color === "6D28D9" && r.shading?.fill === "F3E8FF"), "TextRun AI 2 phải có đúng màu và shading");

  console.log("khbd-integrations-smoke: OK");
}

main();

