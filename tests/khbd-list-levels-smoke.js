const assert = require("assert");
const fs = require("fs");
const path = require("path");
const zlib = require("zlib");

function loadDocx() {
  try {
    return require("docx");
  } catch (projectDependencyError) {
    const runtimeModule = path.join(
      process.env.USERPROFILE || "",
      ".cache", "codex-runtimes", "codex-primary-runtime",
      "dependencies", "node", "node_modules", "docx"
    );
    if (fs.existsSync(runtimeModule)) return require(runtimeModule);
    throw projectDependencyError;
  }
}

function readZipEntry(buffer, entryName) {
  let endOffset = -1;
  for (let offset = buffer.length - 22; offset >= Math.max(0, buffer.length - 65557); offset--) {
    if (buffer.readUInt32LE(offset) === 0x06054b50) { endOffset = offset; break; }
  }
  assert.notStrictEqual(endOffset, -1, "DOCX phải là ZIP hợp lệ");
  const entryCount = buffer.readUInt16LE(endOffset + 10);
  let offset = buffer.readUInt32LE(endOffset + 16);
  for (let index = 0; index < entryCount; index++) {
    const compressedSize = buffer.readUInt32LE(offset + 20);
    const nameLength = buffer.readUInt16LE(offset + 28);
    const extraLength = buffer.readUInt16LE(offset + 30);
    const commentLength = buffer.readUInt16LE(offset + 32);
    const localOffset = buffer.readUInt32LE(offset + 42);
    const name = buffer.subarray(offset + 46, offset + 46 + nameLength).toString("utf8");
    if (name === entryName) {
      const compression = buffer.readUInt16LE(offset + 10);
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
  const docx = loadDocx();
  global.window = { docx };
  const { DocxGenerator } = require("../js/khbd-docx.js");
  const generator = new DocxGenerator();
  const content = "- Thiết bị dạy học\n  + Máy chiếu\n    • Dùng khi trình chiếu hình minh họa";
  const document = new docx.Document({
    sections: [{ children: generator.parseMarkdownToDocxElements(content) }]
  });
  const xml = readZipEntry(await docx.Packer.toBuffer(document), "word/document.xml").toString("utf8");

  assert.match(xml, /<w:t xml:space="preserve">- Thiết bị dạy học<\/w:t>/);
  assert.match(xml, /<w:t xml:space="preserve">\+ Máy chiếu<\/w:t>/);
  assert.match(xml, /<w:t xml:space="preserve">• Dùng khi trình chiếu hình minh họa<\/w:t>/);
  assert.match(xml, /<w:ind w:left="360"\/>/, "Cấp + phải thụt 360 dxa");
  assert.match(xml, /<w:ind w:left="720"\/>/, "Cấp • phải thụt 720 dxa");
  console.log("khbd list levels smoke: passed");
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
