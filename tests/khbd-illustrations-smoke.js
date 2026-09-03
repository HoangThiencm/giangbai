const assert = require("assert");
const fs = require("fs");
const { getPromptTemplate, PROMPTS } = require("../js/khbd-prompts.js");
const {
  parseIllustrationSpecs,
  filterIllustrationSpecs,
  insertIllustrationIntoMarkdown,
  extractSvgCode,
  sanitizeSvg,
  svgToPngDataUrl,
  appState
} = require("../js/khbd-app.js");
const { docxGenerator } = require("../js/khbd-docx.js");

const app = fs.readFileSync("js/khbd-app.js", "utf8");
const gemini = fs.readFileSync("js/khbd-gemini.js", "utf8");
const html = fs.readFileSync("soankhbd.html", "utf8");
const css = fs.readFileSync("css/khbd-styles.css", "utf8");

// 1. Kiểm tra tồn tại các hàm và cấu trúc giao diện
assert.match(app, /function extractSvgCode\(/);
assert.match(app, /function sanitizeSvg\(/);
assert.match(app, /function svgToPngDataUrl\(/);
assert.match(app, /function generateSvgDrawing\(/);
assert.match(app, /function generateLessonIllustrations\(/);
assert.match(app, /setTimeout\(\s*\(\)\s*=>\s*hideProgress\(\),\s*800\s*\)/);
assert.match(app, /btnGenerateIllustrationsAct[\s\S]*finally\s*\{[\s\S]*hideProgress\(\)/);
assert.match(app, /function generateSingleIllustration\(/);
assert.match(app, /function zoomIllustration\(/);
assert.match(app, /function downloadIllustration\(/);
assert.match(html, /id="btnGenerateIllustrations"/);
assert.match(html, /id="illustrationGallery"/);
assert.match(html, /id="zoomSvgContainer"/);
assert.match(css, /\.khbd-svg-container/);
assert.match(css, /\.khbd-illustration-actions/);
assert.match(css, /\.khbd-svg-preview-wrap/);

// 2. Kiểm tra Prompt GENERATE_ILLUSTRATIONS & GENERATE_SVG_DRAWING
const promptIll = getPromptTemplate("GENERATE_ILLUSTRATIONS", {
  subjectName: "Toán",
  topic: "Tam giác vuông",
  grade: "7",
  textbook_content: "Cho tam giác ABC vuông tại A",
  activities_content: "Hoạt động khám phá định lý Pythagore"
});
assert.match(promptIll, /kind "sgk"/);
assert.match(promptIll, /kind "thuc_te"/);
assert.match(promptIll, /CẤM kind=thuc_te|CẤM thuc_te/);
assert.match(promptIll, /CẤM cảnh lớp học|không vẽ lớp học|CẤM cảnh lớp/);
assert.match(promptIll, /Cho tam giác ABC vuông tại A/);

const promptSvg = getPromptTemplate("GENERATE_SVG_DRAWING", {
  subjectName: "Toán",
  grade: "7",
  drawing_prompt: "Tam giác ABC vuông tại A, đường cao AH, nhãn đỉnh Times New Roman",
  drawing_title: "Tam giác vuông và đường cao"
});
assert.match(promptSvg, /viewBox="0 0 500 400"/);
assert.match(promptSvg, /stroke-dasharray="5,4"/);
assert.match(promptSvg, /Times New Roman/);
assert.match(promptSvg, /marker id="arrow"/);
assert.match(promptSvg, /Tam giác ABC vuông tại A/);

// 3. Kiểm tra parseIllustrationSpecs
const specs = parseIllustrationSpecs(`\`\`\`json
{
  "illustrations": [
    {
      "kind": "sgk",
      "title": "Tam giác ABC vuông tại A",
      "caption": "Hình 1. Tam giác ABC vuông tại A và đường cao AH",
      "locus": "B",
      "prompt": "Vẽ tam giác ABC vuông tại A, AH vuông góc với BC tại H"
    },
    {
      "kind": "thuc_te",
      "title": "Đo chiều cao cây",
      "caption": "Hình 2. Ứng dụng giác kế đo bóng cây",
      "locus": "D",
      "prompt": "Học sinh dùng giác kế đo góc nâng tới ngọn cây trên sân trường"
    }
  ]
}
\`\`\``);

assert.strictEqual(specs.length, 2);
assert.strictEqual(specs[0].kind, "sgk");
assert.strictEqual(specs[0].locus, "B");
assert.strictEqual(specs[1].kind, "thuc_te");
assert.strictEqual(specs[1].locus, "D");
assert.deepStrictEqual(parseIllustrationSpecs('{"illustrations":[]}'), []);

const specsWithSub = parseIllustrationSpecs('{"illustrations":[{"kind":"sgk","title":"Trung trực","caption":"Hình 1. Đường trung trực","locus":"B","subsection":"Đường trung trực của đoạn thẳng","prompt":"Vẽ đoạn AB và đường trung trực"}]}');
assert.strictEqual(specsWithSub[0].subsection, "Đường trung trực của đoạn thẳng");

const classroomDropped = filterIllustrationSpecs([
  { id: "ill_thuc_te_1", kind: "thuc_te", title: "Cảnh lớp học", prompt: "Học sinh ngồi trong lớp học thảo luận nhóm", locus: "A" },
  { id: "ill_sgk_1", kind: "sgk", title: "Tam giác ABC", prompt: "Tam giác ABC vuông tại A", locus: "B" }
], { textbook_content: "Cho tam giác ABC vuông tại A. Không có bài toán thực tế." });
assert.strictEqual(classroomDropped.length, 1);
assert.strictEqual(classroomDropped[0].kind, "sgk");

const realKept = filterIllustrationSpecs([
  { id: "ill_thuc_te_1", kind: "thuc_te", title: "Đo cây", prompt: "Đo chiều cao cây bằng bóng trên sân trường", locus: "D" }
], { textbook_content: "Bài toán thực tế: Đo chiều cao cây bằng bóng." });
assert.strictEqual(realKept.length, 1);
assert.strictEqual(realKept[0].kind, "thuc_te");

const activityB = `## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI

### 1. Hoạt động 2.1: Đường trung trực của đoạn thẳng (15 phút)
#### a) Mục tiêu:
- Nhận biết đường trung trực.
#### b) Nội dung:
- Học sinh quan sát hình trong SGK.
#### c) Sản phẩm:
- Định nghĩa đường trung trực.
#### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: ... | **1. Đường trung trực** |

### 2. Hoạt động 2.2: Tính chất đường trung trực (12 phút)
#### a) Mục tiêu:
- Vận dụng tính chất.
#### b) Nội dung:
- Chứng minh tính chất.
`;
const placed = insertIllustrationIntoMarkdown(activityB, {
  id: "ill_sgk_1",
  kind: "sgk",
  title: "Trung trực",
  caption: "Hình 1. Đường trung trực",
  subsection: "Đường trung trực của đoạn thẳng",
  locus: "B"
});
assert.equal(placed.placed, true);
assert.match(placed.markdown, /b\)\s*Nội dung:[\s\S]*khbd-ill:ill_sgk_1[\s\S]*### 2\. Hoạt động 2\.2/);
assert.doesNotMatch(placed.markdown, /Tính chất đường trung trực[\s\S]*khbd-ill:ill_sgk_1/);

// 4. Kiểm tra extractSvgCode
const rawWithMarkdown = "Dưới đây là mã SVG:\n```xml\n<svg viewBox=\"0 0 500 400\"><polygon points=\"100,300 400,300 100,100\" fill=\"none\" stroke=\"#000\"/></svg>\n```\nChúc bạn thành công!";
const extracted = extractSvgCode(rawWithMarkdown);
assert.strictEqual(extracted, '<svg viewBox="0 0 500 400"><polygon points="100,300 400,300 100,100" fill="none" stroke="#000"/></svg>');
assert.strictEqual(extractSvgCode("Không có svg nào ở đây"), "");

// 5. Kiểm tra sanitizeSvg
const maliciousSvg = '<svg viewBox="0 0 500 400" onload="alert(1)"><script>evil()</script><foreignObject><div>bad</div></foreignObject><a href="javascript:attack()"><polygon points="0,0 10,10" onclick="hack()"/></a></svg>';
const sanitized = sanitizeSvg(maliciousSvg);
assert(!sanitized.includes("<script>"), "Phải loại bỏ <script>");
assert(!sanitized.includes("<foreignObject>"), "Phải loại bỏ <foreignObject>");
assert(!sanitized.includes("onload="), "Phải loại bỏ onload");
assert(!sanitized.includes("onclick="), "Phải loại bỏ onclick");
assert(!sanitized.includes("javascript:"), "Phải loại bỏ javascript:");
assert(sanitized.includes('xmlns="http://www.w3.org/2000/svg"'), "Phải có namespace xmlns");
assert(sanitized.includes("khbd-svg-draw"), "Phải có class khbd-svg-draw");

// 6. Kiểm tra svgToPngDataUrl (Node.js fallback)
const cleanSvg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 400"><rect width="500" height="400" fill="#fff"/></svg>';
svgToPngDataUrl(cleanSvg, 2).then(dataUrl => {
  assert(dataUrl && dataUrl.startsWith("data:image/"), "dataUrl phải hợp lệ");
});

// 7. Kiểm tra docxGenerator.createIllustrationParagraphs
global.appState = appState;
global.window = {
  appState: appState,
  docx: {
    Paragraph: function (opts) { this.opts = opts; },
    TextRun: function (opts) { this.opts = opts; },
    ImageRun: function (opts) { this.opts = opts; },
    AlignmentType: { CENTER: "center" },
    ShadingType: { CLEAR: "clear" }
  }
};

appState.content.illustrations = [
  {
    id: "ill_sgk_1",
    kind: "sgk",
    title: "Hình chóp tam giác đều",
    caption: "Hình 1. Hình chóp S.ABC",
    svgContent: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 400"><path d="M 250 50 L 100 350 L 400 350 Z"/></svg>',
    dataUrl: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
  }
];

const docxParagraphs = docxGenerator.createIllustrationParagraphs("Hình chóp tam giác đều S.ABC", "ill_sgk_1");
assert.strictEqual(docxParagraphs.length, 2, "Phải sinh đúng 2 Paragraphs (Image và Caption)");
assert.strictEqual(docxParagraphs[0].opts.alignment, "center");
assert.strictEqual(docxParagraphs[1].opts.alignment, "center");

console.log("✅ khbd illustrations smoke test: ALL PASSED (100%)");
