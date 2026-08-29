const assert = require("assert");
const fs = require("fs");
const path = require("path");
const zlib = require("zlib");

const {
  KHBD_PEDAGOGY_CATALOG,
  getPedagogyExecutionScript,
  buildDetailedPedagogyGuide
} = require("../js/khbd-pedagogy-catalog.js");

const {
  PROMPTS,
  getPromptTemplate
} = require("../js/khbd-prompts.js");

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
    return null;
  }
}

function readZipEntry(buffer, entryName) {
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
    const compression = buffer.readUInt16LE(offset + 10);
    const compressedSize = buffer.readUInt32LE(offset + 20);
    const nameLength = buffer.readUInt16LE(offset + 28);
    const extraLength = buffer.readUInt16LE(offset + 30);
    const commentLength = buffer.readUInt16LE(offset + 32);
    const localOffset = buffer.readUInt32LE(offset + 42);
    const name = buffer.subarray(offset + 46, offset + 46 + nameLength).toString("utf8");
    if (name === entryName) {
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

async function xmlFromMarkdown(generator, docx, markdown) {
  const document = new docx.Document({
    sections: [{ children: generator.parseMarkdownToDocxElements(markdown) }]
  });
  return readZipEntry(await docx.Packer.toBuffer(document), "word/document.xml").toString("utf8");
}

function testCatalog() {
  console.log("-> Kiểm tra Pedagogy Catalog & Execution Scripts...");
  
  // 1. Kiểm tra methods có executionScript đầy đủ
  assert.ok(Array.isArray(KHBD_PEDAGOGY_CATALOG.methods) && KHBD_PEDAGOGY_CATALOG.methods.length > 0, "Catalog methods phải tồn tại");
  KHBD_PEDAGOGY_CATALOG.methods.forEach(m => {
    assert.ok(m.executionScript, `Method ${m.id} (${m.label}) phải có executionScript`);
    const s = m.executionScript;
    assert.ok(s.step1 && s.step1.gv && s.step1.hs, `Method ${m.id} step 1 phải có gv và hs`);
    assert.ok(s.step2 && s.step2.gv && s.step2.hs, `Method ${m.id} step 2 phải có gv và hs`);
    assert.ok(s.step3 && s.step3.gv && s.step3.hs, `Method ${m.id} step 3 phải có gv và hs`);
    assert.ok(s.step4 && s.step4.gv && s.step4.hs, `Method ${m.id} step 4 phải có gv và hs`);
  });

  // 2. Kiểm tra techniques có executionScript đầy đủ
  assert.ok(Array.isArray(KHBD_PEDAGOGY_CATALOG.techniques) && KHBD_PEDAGOGY_CATALOG.techniques.length > 0, "Catalog techniques phải tồn tại");
  KHBD_PEDAGOGY_CATALOG.techniques.forEach(t => {
    assert.ok(t.executionScript, `Technique ${t.id} (${t.label}) phải có executionScript`);
    const s = t.executionScript;
    assert.ok(s.step1 && s.step1.gv && s.step1.hs, `Technique ${t.id} step 1 phải có gv và hs`);
    assert.ok(s.step2 && s.step2.gv && s.step2.hs, `Technique ${t.id} step 2 phải có gv và hs`);
    assert.ok(s.step3 && s.step3.gv && s.step3.hs, `Technique ${t.id} step 3 phải có gv và hs`);
    assert.ok(s.step4 && s.step4.gv && s.step4.hs, `Technique ${t.id} step 4 phải có gv và hs`);
  });

  // 3. Kiểm tra helper getPedagogyExecutionScript
  const tpsScript = getPedagogyExecutionScript("techniques", "tps-tech");
  assert.ok(tpsScript, "getPedagogyExecutionScript cho tps-tech phải trả về script");
  assert.ok(tpsScript.step1.gv.includes('"'), "Step 1 GV của tps-tech phải có câu nói trong ngoặc kép");
  assert.ok(tpsScript.step2.hs.includes("nháp"), "Step 2 HS của tps-tech phải có thao tác nháp/cặp");

  const tableclothScript = getPedagogyExecutionScript("techniques", "tablecloth");
  assert.ok(tableclothScript && tableclothScript.step2.gv.includes("lỗi sai"), "Khăn trải bàn phải có lưu ý phát hiện lỗi sai");

  // 4. Kiểm tra helper buildDetailedPedagogyGuide
  const guideB = buildDetailedPedagogyGuide("B", {
    phasePedagogy: { B: { techniques: ["tps-tech", "tablecloth"] } },
    methods: ["cooperative"]
  });
  assert.ok(guideB.includes("KỊCH BẢN THỰC CHIẾN KỸ THUẬT DẠY HỌC (Pha B)"), "Guide B phải có tiêu đề kịch bản kỹ thuật");
  assert.ok(guideB.includes("Think-Pair-Share"), "Guide B phải chứa kỹ thuật Think-Pair-Share");
  assert.ok(guideB.includes("Khăn trải bàn"), "Guide B phải chứa kỹ thuật Khăn trải bàn");
  assert.ok(guideB.includes("Dạy học hợp tác"), "Guide B phải chứa phương pháp hợp tác");
  assert.ok(guideB.includes("Bước 1 (Chuyển giao)"), "Guide B phải có Bước 1");
  assert.ok(guideB.includes("Bước 2 (Thực hiện)"), "Guide B phải có Bước 2");

  console.log("  -> Catalog & Scripts: PASS");
}

function testPrompts() {
  console.log("-> Kiểm tra Prompts & Activity Table Contract...");

  const stubContext = {
    subjectName: "Toán",
    gradeLevelName: "THCS",
    topic: "Tập hợp các số tự nhiên",
    duration: "1 tiết",
    objectives_content: "I. Mục tiêu bài học",
    textbook_content: "Bài 1: Khái niệm tập hợp. Cho A = {1, 2, 3}",
    pedagogical_context: "Phương pháp: Dạy học hợp tác. Kỹ thuật: Think-Pair-Share"
  };

  // 1. Kiểm tra GENERATE_ACTIVITY_A
  const promptA = getPromptTemplate("GENERATE_ACTIVITY_A", stubContext);
  assert.ok(promptA.includes("KỊCH BẢN SƯ PHẠM THỰC CHIẾN"), "Prompt A phải có contract kịch bản thực chiến");
  assert.ok(promptA.includes("**GV:**"), "Prompt A phải có hướng dẫn phân vai **GV:**");
  assert.ok(promptA.includes("**HS:**"), "Prompt A phải có hướng dẫn phân vai **HS:**");
  assert.ok(promptA.includes("Tập hợp các số tự nhiên"), "Prompt A phải thay topic đúng");

  // 2. Kiểm tra GENERATE_ACTIVITY_B
  const promptB = getPromptTemplate("GENERATE_ACTIVITY_B", stubContext);
  assert.ok(promptB.includes("KỊCH BẢN SƯ PHẠM THỰC CHIẾN"), "Prompt B phải có contract kịch bản thực chiến");
  assert.ok(promptB.includes("lỗi sai điển hình"), "Prompt B phải có yêu cầu phát hiện lỗi sai điển hình");
  assert.ok(promptB.includes("hỗ trợ phân hóa"), "Prompt B phải có yêu cầu can thiệp hỗ trợ phân hóa");
  assert.ok(promptB.includes("sản phẩm trung gian"), "Prompt B phải có sản phẩm trung gian");

  // 3. Kiểm tra GENERATE_ACTIVITY_C
  const promptC = getPromptTemplate("GENERATE_ACTIVITY_C", stubContext);
  assert.ok(promptC.includes("KỊCH BẢN SƯ PHẠM THỰC CHIẾN"), "Prompt C phải có contract kịch bản thực chiến");
  assert.ok(promptC.includes("Bài 1: Khái niệm tập hợp"), "Prompt C phải thay textbook_content đúng");

  // 4. Kiểm tra GENERATE_ACTIVITY_D
  const promptD = getPromptTemplate("GENERATE_ACTIVITY_D", stubContext);
  assert.ok(promptD.includes("KỊCH BẢN SƯ PHẠM THỰC CHIẾN"), "Prompt D phải có contract kịch bản thực chiến");
  assert.ok(promptD.includes("mô hình hóa"), "Prompt D phải có yêu cầu mô hình hóa");

  assert.ok(promptB.includes("TIME-BUDGET GATE"), "Prompt B phải có Time-Budget Gate");
  assert.ok(promptB.includes("FACILITY GATE"), "Prompt B phải có Facility Gate");
  assert.ok(promptB.includes("điện thoại"), "Prompt B phải cấm hoạt động điện thoại khi không có thiết bị");
  const promptObj = getPromptTemplate("GENERATE_OBJECTIVES", stubContext);
  const promptMat = getPromptTemplate("GENERATE_MATERIALS", stubContext);
  assert.ok(promptObj.includes("CẤM KHIÊN CƯỠNG"), "Prompt Mục tiêu phải có chống khiên cưỡng");
  assert.ok(promptMat.includes("Canva"), "Prompt Thiết bị phải cấm Canva khi không có thiết bị");

  console.log("  -> Prompts: PASS");
}

function testAssertions() {
  console.log("-> Kiểm tra Assertion logic...");

  function checkPhaseOutput(output, requiredTechnique = null) {
    const text = String(output || "");
    const tablePart = text.split("### d)")[1] || text;

    if (requiredTechnique) {
      const fold = v => String(v || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, " ").trim();
      const hay = fold(tablePart);
      if (!hay.includes(fold(requiredTechnique))) {
        throw new Error(`Nội dung chưa triển khai đúng kỹ thuật dạy học: ${requiredTechnique}`);
      }
    }

    const hasStep1 = /bước\s*1|chuyển giao/i.test(tablePart);
    const hasStep2 = /bước\s*2|thực hiện/i.test(tablePart);
    const hasStep3 = /bước\s*3|báo cáo|thảo luận/i.test(tablePart);
    const hasStep4 = /bước\s*4|kết luận|nhận định/i.test(tablePart);
    if (!hasStep1 || !hasStep2 || !hasStep3 || !hasStep4) {
      throw new Error("Bảng tổ chức thực hiện chưa có đủ 4 bước");
    }

    const hasGv = /(?:\bGV\b|giáo viên)/i.test(tablePart);
    const hasHs = /(?:\bHS\b|học sinh)/i.test(tablePart);
    if (!hasGv || !hasHs) {
      throw new Error("Bảng tổ chức thực hiện chưa phân định rõ ràng vai trò GV và HS");
    }
  }

  const validOutput = `
### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ: Kỹ thuật Think-Pair-Share. **GV:** Phát phiếu học tập và nói: "Các em có 2 phút suy nghĩ cá nhân, 3 phút thảo luận cặp...". **HS:** Nhận phiếu học tập.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Làm việc cá nhân vào nháp (2 phút) -> Thảo luận cặp (3 phút) thống nhất câu trả lời. **GV:** Quan sát, phát hiện lỗi sai điển hình: ..., hỗ trợ phân hóa.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Đại diện cặp báo cáo. **GV:** Đặt câu hỏi phản biện: "Vì sao chọn cách này?".<br>+ Bước 4: Kết luận, nhận định: **GV:** Nhận xét và chốt kiến thức chuẩn. **HS:** Sửa bài vào vở. | **1. Định nghĩa**<br>- Khái niệm: $A = \\{1; 2\\}$. |
`;

  // 1. Output chuẩn: không ném lỗi
  assert.doesNotThrow(() => checkPhaseOutput(validOutput, "Think-Pair-Share"), "Valid output phải pass");

  // 2. Output thiếu Bước 4: ném lỗi
  const missingStep4 = validOutput.replace("+ Bước 4: Kết luận, nhận định", "");
  assert.throws(() => checkPhaseOutput(missingStep4), /chưa có đủ 4 bước/, "Thiếu bước 4 phải throw");

  // 3. Output thiếu vai trò HS: ném lỗi
  const missingHs = validOutput.replace(/\bHS\b/gi, "").replace(/học sinh/gi, "");
  assert.throws(() => checkPhaseOutput(missingHs), /chưa phân định rõ ràng vai trò GV và HS/, "Thiếu vai trò HS phải throw");

  // 4. Output thiếu kỹ thuật bắt buộc: ném lỗi
  assert.throws(() => checkPhaseOutput(validOutput, "Khăn trải bàn"), /chưa triển khai đúng kỹ thuật dạy học/, "Sai kỹ thuật phải throw");

  console.log("  -> Assertion logic: PASS");
}

async function testDocxCompatibility() {
  console.log("-> Kiểm tra Tính tương thích DOCX (Bảng 2 cột kịch bản thực chiến + Math LaTeX)...");

  const docx = loadDocx();
  if (!docx) {
    console.log("  -> DOCX Compatibility: BỎ QUA (Môi trường Node CLI chưa có docx module; docx chạy qua CDN UMD trên trình duyệt)");
    return;
  }
  global.window = { docx };
  const { DocxGenerator } = require("../js/khbd-docx.js");
  const generator = new DocxGenerator();

  const fullLessonMarkdown = [
    "## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI",
    "",
    "### 1. Hoạt động 2.1: Khái niệm tập hợp",
    "#### a) Mục tiêu:",
    "- Nhận biết được khái niệm tập hợp và các phần tử của tập hợp.",
    "#### b) Nội dung:",
    "- Học sinh làm việc cá nhân và theo cặp thực hiện hoạt động khám phá 1 trong SGK.",
    "#### c) Sản phẩm:",
    "- Lời giải hoạt động khám phá 1:",
    "  + Tập hợp $A = \\{x \\in \\mathbb{N} \\mid x < 5\\}$ gồm các số $0, 1, 2, 3, 4$.",
    "#### d) Tổ chức thực hiện:",
    "| Hoạt động của GV và HS | Nội dung |",
    "| :--- | :--- |",
    "| + Bước 1: Chuyển giao nhiệm vụ: Kỹ thuật Think-Pair-Share. **GV:** Phát Phiếu học tập số 1 và giao việc: \"Các em có 2 phút suy nghĩ cá nhân, 3 phút thảo luận cặp hoàn thành HĐ 1...\". **HS:** Nhận phiếu, chuẩn bị nháp.<br>+ Bước 2: Thực hiện nhiệm vụ: **HS:** Làm việc cá nhân (2 phút) ghi nháp -> Thảo luận cặp (3 phút) thống nhất sản phẩm trung gian trên phiếu. **GV:** Bao quát, phát hiện lỗi sai điển hình: nhầm lẫn dấu $\\in$ và $\\subset$, can thiệp hỗ trợ phân hóa cho HS chậm.<br>+ Bước 3: Báo cáo, thảo luận: **HS:** Đại diện một cặp lên bảng trình bày; các cặp khác nhận xét, phản biện. **GV:** Điều hành và đặt câu hỏi mở rộng: \"Phần tử 5 có thuộc tập A không? Vì sao?\".<br>+ Bước 4: Kết luận, nhận định: **GV:** Chuẩn hóa kiến thức và hướng dẫn ghi bảng. **HS:** Sửa bài vào vở. | **1. Khái niệm tập hợp**<br>- Tập hợp là khái niệm cơ bản trong toán học.<br>- Ký hiệu: $x \\in A$ (x thuộc A); $y \\notin A$ (y không thuộc A).<br>+ Chú ý:<br>• Mỗi phần tử chỉ được liệt kê một lần.<br>• Thứ tự các phần tử không quan trọng.<br>- Ví dụ 1: Cho $A = \\{1; 2; 3\\}$, ta có $1 \\in A$ và $4 \\notin A$. |"
  ].join("\n");

  const xml = await xmlFromMarkdown(generator, docx, fullLessonMarkdown);

  // 1. Kiểm tra bảng được tạo với cấu trúc hợp lệ
  assert.ok(xml.includes("<w:tbl>"), "DOCX phải chứa phần tử bảng <w:tbl>");
  assert.ok(xml.includes("<w:tblGrid>"), "Bảng phải có lưới cột <w:tblGrid>");

  // 2. Kiểm tra tỷ lệ 50-50 chuẩn A4 (4819 / 4820 dxa)
  assert.ok(xml.includes('w:w="4819"') || xml.includes('w:w="4820"'), "Cột bảng phải có độ rộng 4819/4820 dxa (chuẩn A4 50-50)");

  // 3. Kiểm tra math formulas được chuyển thành OMML
  assert.ok(xml.includes("<m:oMath>"), "Công thức LaTeX phải được render thành OMML <m:oMath>");
  assert.ok(xml.includes("∈") || xml.includes("∉") || xml.includes("mathbb"), "Ký hiệu toán học phải được chuyển đổi chuẩn xác");

  // 4. Kiểm tra các cấp danh sách và ngắt dòng <br>
  assert.ok(xml.includes("Khái niệm tập hợp"), "Cột phải phải chứa tiêu đề mục kiến thức");
  assert.ok(xml.includes("Bước 1: Chuyển giao"), "Cột trái phải chứa Bước 1");
  assert.ok(xml.includes("Bước 4: Kết luận"), "Cột trái phải chứa Bước 4");
  assert.ok(xml.includes("Think-Pair-Share"), "Cột trái phải chứa tên kỹ thuật");

  console.log("  -> DOCX Compatibility: PASS");
}

async function main() {
  console.log("==================================================");
  console.log("BẮT ĐẦU KIỂM THỬ KỊCH BẢN SƯ PHẠM THỰC CHIẾN (SMOKE TEST)");
  console.log("==================================================");

  testCatalog();
  testPrompts();
  testAssertions();
  await testDocxCompatibility();

  console.log("==================================================");
  console.log("TẤT CẢ CÁC BÀI TEST KỊCH BẢN SƯ PHẠM ĐỀU ĐẠT (PASS)!");
  console.log("==================================================");
}

main().catch(err => {
  console.error("TEST FAILED:", err);
  process.exitCode = 1;
});