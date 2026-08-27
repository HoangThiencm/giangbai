const assert = require("assert");
const fs = require("fs");
const { getPromptTemplate } = require("../js/khbd-prompts.js");

const docx = fs.readFileSync("js/khbd-docx.js", "utf8");
assert.match(docx, /fontSizeBody = 26/);
assert.match(docx, /lineSpacing = 276/);
assert.match(docx, /lineRule = "auto"/);
assert.match(docx, /top: 850/);
assert.match(docx, /bottom: 850/);
assert.match(docx, /left: 1417/);
assert.match(docx, /right: 850/);
assert.match(docx, /width: 11906/);
assert.match(docx, /height: 16838/);

const prompt = getPromptTemplate("GENERATE_ACTIVITY_B", {
  subjectName: "Toán",
  topic: "Tập hợp",
  duration: "2 tiết",
  textbook_content: "Mục 1: Khái niệm tập hợp",
  objectives_content: ""
});
assert.match(prompt, /8–10 trang|8–12 trang|~10 trang/);
assert.match(prompt, /súc tích|cô đọng|GIỚI HẠN DUNG LƯỢNG|YÊU CẦU ĐỘ DÀI/);

console.log("khbd docx layout smoke: passed");
