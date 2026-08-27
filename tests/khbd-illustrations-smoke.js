const assert = require("assert");
const fs = require("fs");
const { getPromptTemplate } = require("../js/khbd-prompts.js");

const app = fs.readFileSync("js/khbd-app.js", "utf8");
const gemini = fs.readFileSync("js/khbd-gemini.js", "utf8");
const html = fs.readFileSync("soankhbd.html", "utf8");

assert.match(app, /function parseIllustrationSpecs\(/);
assert.match(app, /function generateLessonIllustrations\(/);
assert.match(app, /kind === "thuc_te"/);
assert.match(app, /khbd-ill:/);
assert.match(gemini, /async generateImage\(/);
assert.match(gemini, /responseModalities:\s*\["TEXT", "IMAGE"\]/);
assert.match(html, /id="btnGenerateIllustrations"/);
assert.match(html, /id="illustrationGallery"/);

const prompt = getPromptTemplate("GENERATE_ILLUSTRATIONS", {
  subjectName: "Toán",
  topic: "Tam giác",
  grade: "6",
  textbook_content: "Tam giác ABC vuông tại A",
  activities_content: "Hoạt động B hình thành kiến thức"
});
assert.match(prompt, /kind "sgk"/);
assert.match(prompt, /kind "thuc_te"/);
assert.match(prompt, /Tam giác ABC vuông tại A/);

const { parseIllustrationSpecs } = require("../js/khbd-app.js");
const specs = parseIllustrationSpecs(`Kết quả:
{"illustrations":[
  {"kind":"sgk","title":"Tam giác ABC","caption":"Hình 1. Tam giác ABC vuông tại A","locus":"B","prompt":"Tam giác ABC vuông tại A, AB = 3cm, AC = 4cm"},
  {"kind":"thuc_te","title":"Đo sân trường","caption":"Hình 2. Học sinh đo góc sân","locus":"D","prompt":"Học sinh dùng thước đo góc trên sân trường"}
]}`);
assert.strictEqual(specs.length, 2);
assert.strictEqual(specs[0].kind, "sgk");
assert.strictEqual(specs[1].kind, "thuc_te");
assert.strictEqual(specs[1].locus, "D");
assert.deepStrictEqual(parseIllustrationSpecs('{"illustrations":[]}'), []);

console.log("khbd illustrations smoke: passed");
