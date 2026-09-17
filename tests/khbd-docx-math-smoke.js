const assert = require("assert");
const fs = require("fs");
const path = require("path");
const zlib = require("zlib");

function loadDocx() {
  try {
    return require("docx");
  } catch (projectDependencyError) {
    // Ứng dụng dùng docx từ CDN; trong Codex, dùng bản runtime đi kèm thay vì cài thêm package.
    const runtimeModule = path.join(
      process.env.USERPROFILE || "",
      ".cache", "codex-runtimes", "codex-primary-runtime",
      "dependencies", "node", "node_modules", "docx"
    );
    if (fs.existsSync(runtimeModule)) return require(runtimeModule);
    throw projectDependencyError;
  }
}

const docx = loadDocx();

global.window = { docx };
const { DocxGenerator } = require("../js/khbd-docx.js");

function readZipEntry(buffer, entryName) {
  // DOCX là ZIP; chỉ cần đọc một entry deflate/store nên không cần thêm dependency test.
  const endSignature = 0x06054b50;
  let endOffset = -1;
  for (let offset = buffer.length - 22; offset >= Math.max(0, buffer.length - 65557); offset--) {
    if (buffer.readUInt32LE(offset) === endSignature) {
      endOffset = offset;
      break;
    }
  }
  assert.notStrictEqual(endOffset, -1, "DOCX phải là gói ZIP hợp lệ");

  const entryCount = buffer.readUInt16LE(endOffset + 10);
  let offset = buffer.readUInt32LE(endOffset + 16);
  for (let index = 0; index < entryCount; index++) {
    assert.strictEqual(buffer.readUInt32LE(offset), 0x02014b50, "Central directory ZIP không hợp lệ");
    const compression = buffer.readUInt16LE(offset + 10);
    const compressedSize = buffer.readUInt32LE(offset + 20);
    const nameLength = buffer.readUInt16LE(offset + 28);
    const extraLength = buffer.readUInt16LE(offset + 30);
    const commentLength = buffer.readUInt16LE(offset + 32);
    const localOffset = buffer.readUInt32LE(offset + 42);
    const name = buffer.subarray(offset + 46, offset + 46 + nameLength).toString("utf8");
    if (name === entryName) {
      assert.strictEqual(buffer.readUInt32LE(localOffset), 0x04034b50, "Local ZIP header không hợp lệ");
      const localNameLength = buffer.readUInt16LE(localOffset + 26);
      const localExtraLength = buffer.readUInt16LE(localOffset + 28);
      const payloadOffset = localOffset + 30 + localNameLength + localExtraLength;
      const payload = buffer.subarray(payloadOffset, payloadOffset + compressedSize);
      return compression === 0 ? payload : zlib.inflateRawSync(payload);
    }
    offset += 46 + nameLength + extraLength + commentLength;
  }
  throw new Error(`Không tìm thấy ${entryName} trong DOCX`);
}

async function main() {
  const generator = new DocxGenerator();
  const newlineMath = "a\\\\\nb";
  assert.strictEqual(generator.normalizeLatexForMath(newlineMath), newlineMath, "Không được đổi lệnh xuống dòng LaTex");
  const optionalNewlineMath = String.raw`a\\[4pt]b`;
  assert.strictEqual(generator.normalizeLatexForMath(optionalNewlineMath), optionalNewlineMath, "Không được đổi lệnh xuống dòng có tham số");
  assert.strictEqual(generator.normalizeLatexForMath(String.raw`$\\notin A$`), String.raw`$\notin A$`);
  assert.strictEqual(generator.normalizeLatexForMath(String.raw`$\notinA$`), String.raw`$\notin A$`);

  const inline = String.raw`$\notin A$; $\\notin A$; $\notinA$; $\frac{a}{b}$; $\sqrt{x}$; $x^2$`;
  const cases = String.raw`$\begin{cases}x + y = 17\;(1) \\ 10x + 3y = 100\;(2)\end{cases}$`;
  const aligned = String.raw`$\begin{aligned}x &= 2 \\ y &= 3\end{aligned}$`;
  const leftBrace = String.raw`$\left\{x+y=5 \\ x-y=1\right.$`;
  const prefixedCases = String.raw`$\Leftrightarrow \begin{cases} -3x+8y=-30 \\ 2x-4y=40 \end{cases}$`;
  assert.ok(!/begin(?:cases|aligned)|end(?:cases|aligned)/i.test(generator.latexToUnicodeMath(cases)), "Fallback Unicode phải bỏ begin/end");
  const prefixedLatex = String.raw`\Leftrightarrow \begin{cases} -3x+8y=-30 \\ 2x-4y=40 \end{cases}`;
  const prefixedUnicode = generator.latexToUnicodeMath(prefixedLatex);
  assert.match(prefixedUnicode, /\{/, "Fallback Unicode phải giữ ngoặc nhọn hệ phương trình");
  assert.ok(!/begincases|endcases/i.test(prefixedUnicode), "Fallback Unicode không được lộ begincases");
  const table = generator.createDocxTableFromMarkdown([
    "| Hoạt động | Nội dung |",
    "| --- | --- |",
    String.raw`| Kiểm tra | $\notinA$ |`
  ]);
  const document = new docx.Document({
    sections: [{
      children: [
        new docx.Paragraph({ children: generator.parseInlineTextToRuns(inline) }),
        new docx.Paragraph({ children: generator.parseInlineTextToRuns(cases) }),
        new docx.Paragraph({ children: generator.parseInlineTextToRuns(aligned) }),
        new docx.Paragraph({ children: generator.parseInlineTextToRuns(leftBrace) }),
        new docx.Paragraph({ children: generator.parseInlineTextToRuns(prefixedCases) }),
        table
      ]
    }]
  });
  const buffer = await docx.Packer.toBuffer(document);
  const xml = readZipEntry(buffer, "word/document.xml").toString("utf8");

  assert.match(xml, /<m:oMath>/, "Word export phải có OMML thực");
  assert.ok((xml.match(/<m:t>∉<\/m:t>/g) || []).length >= 4, "Các biến thể notin phải tạo ký hiệu ∉");
  assert.match(xml, /<w:tbl>[\s\S]*?<m:t>∉<\/m:t>/, "Ô bảng Markdown phải giữ Equation OMML");
  assert.match(xml, /<m:f>/, "frac phải tạo OMML fraction");
  assert.match(xml, /<m:rad>/, "sqrt phải tạo OMML radical");
  assert.match(xml, /<m:sSup>/, "superscript phải tạo OMML superscript");
  assert.match(xml, /<m:dPr><m:begChr m:val="\{"\/><m:endChr m:val=""\/><\/m:dPr>/, "Hệ phương trình phải có dấu ngoặc nhọn mở OMML");
  assert.ok((xml.match(/<m:eqArr>/g) || []).length >= 3, "cases, aligned và left brace phải tạo Equation Array");
  assert.match(xml, /x \+ y = 17.*\(1\)/, "Giữ dòng và số thứ tự phương trình thứ nhất");
  assert.match(xml, /10x \+ 3y = 100.*\(2\)/, "Giữ dòng và số thứ tự phương trình thứ hai");
  assert.ok(!/begincases|endcases|beginaligned|endaligned/i.test(xml), "XML DOCX không được chứa token LaTeX rác");
  assert.match(xml, /-3x\s*\+\s*8y\s*=\s*-30/, "Hệ có tiền tố phải giữ phương trình thứ nhất");
  assert.match(xml, /2x\s*-\s*4y\s*=\s*40/, "Hệ có tiền tố phải giữ phương trình thứ hai");
  assert.ok((xml.match(/<m:dPr><m:begChr m:val="\{"\/><m:endChr m:val=""\/><\/m:dPr>/g) || []).length >= 2, "Hệ có tiền tố \\Leftrightarrow vẫn tạo delimiter {");

  const { getPromptTemplate } = require("../js/khbd-prompts.js");
  const thcsPrompt = getPromptTemplate("GENERATE_ACTIVITY_C", {
    subject: "toan",
    subjectName: "Toán",
    grade: "9",
    topic: "Giải hệ hai phương trình bậc nhất hai ẩn",
    duration: "02 tiết (90 phút)",
    textbook_content: "Bài 2",
    digitalCompetencyEnabled: false,
    aiCompetencyEnabled: false
  });
  assert.match(thcsPrompt, /TUYỆT ĐỐI CẤM DÙNG DẤU TƯƠNG ĐƯƠNG/, "Prompt Toán 9 cấm \\Leftrightarrow");
  assert.match(thcsPrompt, /Phương pháp thế/, "Prompt Toán bắt buộc phương pháp thế");
  assert.match(thcsPrompt, /QUY TẮC CỘT BẢNG TUYỆT ĐỐI/, "Prompt cấm dấu | trong ô bảng");
  console.log("khbd-docx math smoke: passed");
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
