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
  const table = generator.createDocxTableFromMarkdown([
    "| Hoạt động | Nội dung |",
    "| --- | --- |",
    String.raw`| Kiểm tra | $\notinA$ |`
  ]);
  const document = new docx.Document({
    sections: [{
      children: [
        new docx.Paragraph({ children: generator.parseInlineTextToRuns(inline) }),
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
  console.log("khbd-docx math smoke: passed");
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
