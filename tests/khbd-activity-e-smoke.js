const assert = require("assert");
const {
  PROMPTS,
  getPromptTemplate,
  calculateActivityTimeBudgets
} = require("../js/khbd-prompts.js");

console.log("==================================================");
console.log("BẮT ĐẦU KIỂM THỬ TÍCH HỢP HOẠT ĐỘNG E (HƯỚNG DẪN VỀ NHÀ)");
console.log("==================================================");

// Mock môi trường tối giản cho các hàm từ khbd-app.js
function sanitizeLessonMarkdown(rawOutput) {
  if (!rawOutput) return "";
  return String(rawOutput).replace(/^\uFEFF/, "").trim();
}

function parseKhbdSections(text, keys) {
  const source = String(text || "");
  const result = {};
  (keys || []).forEach(key => { result[key] = ""; });
  const hits = [];
  const markerRe = /<<<\s*KHBD_([A-Z]+)\s*>>>/gi;
  let match;
  while ((match = markerRe.exec(source))) {
    hits.push({ key: match[1].toUpperCase(), start: match.index + match[0].length, markerAt: match.index });
  }
  if (hits.length) {
    hits.forEach((hit, i) => {
      const end = i + 1 < hits.length ? hits[i + 1].markerAt : source.length;
      if (Object.prototype.hasOwnProperty.call(result, hit.key)) {
        result[hit.key] = sanitizeLessonMarkdown(source.slice(hit.start, end));
      }
    });
    return result;
  }
  const headingMap = {
    I: /(?:^|\n)\s*#{0,3}\s*(?:I[\.\s:]|MỤC TIÊU\b)[^\n]*/i,
    II: /(?:^|\n)\s*#{0,3}\s*(?:II[\.\s:]|THIẾT BỊ\b)[^\n]*/i,
    A: /(?:^|\n)\s*#{1,3}\s*(?:A[\.\s:]|HOẠT ĐỘNG 1\b|MỞ ĐẦU\b|KHỞI ĐỘNG\b)[^\n]*/i,
    B: /(?:^|\n)\s*#{1,3}\s*(?:B[\.\s:]|HOẠT ĐỘNG 2\b|HÌNH THÀNH KIẾN THỨC\b)[^\n]*/i,
    C: /(?:^|\n)\s*#{1,3}\s*(?:C[\.\s:]|HOẠT ĐỘNG 3\b|LUYỆN TẬP\b)[^\n]*/i,
    D: /(?:^|\n)\s*#{1,3}\s*(?:D[\.\s:]|HOẠT ĐỘNG 4\b|VẬN DỤNG\b)[^\n]*/i,
    E: /(?:^|\n)\s*#{1,3}\s*(?:E[\.\s:]|HOẠT ĐỘNG 5\b|HƯỚNG DẪN VỀ NHÀ\b)[^\n]*/i
  };
  const found = [];
  (keys || []).forEach(key => {
    const re = headingMap[key];
    if (!re) return;
    const hit = re.exec(source);
    if (hit) found.push({ key, at: hit.index + (hit[0].startsWith("\n") ? 1 : 0) });
  });
  found.sort((a, b) => a.at - b.at);
  found.forEach((hit, i) => {
    const end = i + 1 < found.length ? found[i + 1].at : source.length;
    result[hit.key] = sanitizeLessonMarkdown(source.slice(hit.at, end));
  });
  return result;
}

function assertPhasePedagogyOutput(phase, output) {
  const text = String(output || "");
  if (phase === "E") {
    const tablePart = text.split(/#{3,4}\s*d\)/i)[1] || text.split("### d)")[1] || text;
    const hasStep1 = /bước\s*1|chuyển giao/i.test(tablePart);
    const hasStep2 = /bước\s*2|thực hiện/i.test(tablePart);
    const hasStep3 = /bước\s*3|báo cáo|thảo luận/i.test(tablePart);
    const hasStep4 = /bước\s*4|kết luận|nhận định/i.test(tablePart);
    if (!hasStep1 || !hasStep2 || !hasStep3 || !hasStep4) {
      throw new Error("Hoạt động E: Bảng tổ chức thực hiện chưa có đủ 4 bước CV 5512 (Bước 1: Chuyển giao -> Bước 2: Thực hiện -> Bước 3: Báo cáo -> Bước 4: Kết luận).");
    }
    const cellData = tablePart.replace(/\|\s*Hoạt động của GV và HS\s*\|\s*Nội dung\s*\|/i, "");
    const hasGv = /(?:\*\*GV\b|\bGV\s*:|giáo viên)/i.test(cellData);
    const hasHs = /(?:\*\*HS\b|\bHS\s*:|học sinh)/i.test(cellData);
    if (!hasGv || !hasHs) {
      throw new Error("Hoạt động E: Bảng tổ chức thực hiện chưa phân định rõ ràng vai trò GV (giao việc, hướng dẫn) và HS (ghi nhận, tự học tại nhà).");
    }
    return;
  }
}

// 1. Kiểm tra Template PROMPTS.GENERATE_ACTIVITY_E
console.log("-> 1. Kiểm tra Prompt Template GENERATE_ACTIVITY_E...");
assert(Boolean(PROMPTS.GENERATE_ACTIVITY_E), "PROMPTS.GENERATE_ACTIVITY_E must exist");
assert(Boolean(PROMPTS.GENERATE_ACTIVITIES_AE), "PROMPTS.GENERATE_ACTIVITIES_AE must exist");
assert.strictEqual(PROMPTS.GENERATE_ACTIVITIES_AD, PROMPTS.GENERATE_ACTIVITIES_AE, "GENERATE_ACTIVITIES_AD should alias GENERATE_ACTIVITIES_AE");

const context = {
  subject: "toan",
  subjectName: "Toán",
  grade: "7",
  topic: "Số vô tỉ. Căn bậc hai số học",
  duration: "02 tiết (90 phút)",
  aiCompetencyEnabled: true
};

const promptE = getPromptTemplate("GENERATE_ACTIVITY_E", context);
assert(promptE.includes("HƯỚNG DẪN VỀ NHÀ") && promptE.includes("E. HOẠT ĐỘNG"), "Must contain Activity E heading");
assert(promptE.includes("Sơ đồ tư duy") || promptE.includes("sơ đồ tư duy"), "Must instruct mindmap");
assert(promptE.includes("SGK") && promptE.includes("SBT"), "Must instruct textbook & workbook exercises");
assert(promptE.includes("mở rộng") || promptE.includes("nâng cao"), "Must instruct advanced exercises");
assert(promptE.includes("Chuẩn bị bài mới") || promptE.includes("chuẩn bị") || promptE.includes("Chuẩn bị bài sau"), "Must instruct next lesson preparation");
assert(promptE.includes("Prompt AI an toàn"), "Must include AI prompt guide when AI enabled");
console.log("  -> Prompt Template Activity E: PASS");

// 2. Kiểm tra Parser 1-Click bóc tách marker <<<KHBD_E>>>
console.log("-> 2. Kiểm tra Parser 1-Click với marker <<<KHBD_E>>>...");
const mock1ClickOutput = `
<<<KHBD_A>>>
# A. HOẠT ĐỘNG MỞ ĐẦU
Nội dung A...

<<<KHBD_B>>>
# B. HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC
Nội dung B...

<<<KHBD_C>>>
# C. HOẠT ĐỘNG LUYỆN TẬP
Nội dung C...

<<<KHBD_D>>>
# D. HOẠT ĐỘNG VẬN DỤNG
Nội dung D...

<<<KHBD_E>>>
# E. HOẠT ĐỘNG HƯỚNG DẪN VỀ NHÀ
#### a) Mục tiêu:
- Học sinh củng cố kiến thức về căn bậc hai số học.
#### b) Nội dung:
1. Ôn tập kiến thức và vẽ sơ đồ tư duy.
2. Làm bài tập 2.1, 2.2 SGK trang 32.
3. Bài tập nâng cao: Tính giá trị biểu thức.
4. Đọc trước bài mới: Số thực.
#### c) Sản phẩm:
- Vở ghi bài tập và sơ đồ tư duy của học sinh.
#### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| **Bước 1: Chuyển giao nhiệm vụ:**<br>- **GV:** Giao nhiệm vụ tự học tại nhà: "Các em hãy hoàn thành bài tập 2.1, 2.2 vào vở và chuẩn bị bài mới nhé!"<br>- **HS:** Lắng nghe và ghi chép nhiệm vụ.<br><br>**Bước 2: Thực hiện nhiệm vụ:**<br>- **HS:** Tự giác làm bài tập ở nhà.<br><br>**Bước 3: Báo cáo, thảo luận:**<br>- **HS:** Nộp vở bài tập vào đầu tiết học sau.<br><br>**Bước 4: Kết luận, nhận định:**<br>- **GV:** Nhận xét, đánh giá kết quả tự học của học sinh. | 1. Ôn tập kiến thức.<br>2. Bài tập SGK & SBT.<br>3. Bài tập nâng cao.<br>4. Chuẩn bị bài sau. |
`;

const parsed = parseKhbdSections(mock1ClickOutput, ["A", "B", "C", "D", "E"]);
assert(parsed.A && parsed.A.includes("HOẠT ĐỘNG MỞ ĐẦU"), "Parsed A ok");
assert(parsed.B && parsed.B.includes("HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC"), "Parsed B ok");
assert(parsed.C && parsed.C.includes("HOẠT ĐỘNG LUYỆN TẬP"), "Parsed C ok");
assert(parsed.D && parsed.D.includes("HOẠT ĐỘNG VẬN DỤNG"), "Parsed D ok");
assert(parsed.E && parsed.E.includes("HOẠT ĐỘNG HƯỚNG DẪN VỀ NHÀ"), "Parsed E ok with marker");
console.log("  -> Parser với marker KHBD_E: PASS");

// 3. Kiểm tra Parser Fallback nhận diện Heading E. HƯỚNG DẪN VỀ NHÀ
console.log("-> 3. Kiểm tra Parser Fallback Heading E...");
const mockFallbackOutput = `
# A. HOẠT ĐỘNG MỞ ĐẦU
Nội dung A

# B. HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC
Nội dung B

# C. HOẠT ĐỘNG LUYỆN TẬP
Nội dung C

# D. HOẠT ĐỘNG VẬN DỤNG
Nội dung D

# E. HƯỚNG DẪN VỀ NHÀ
Nội dung E
`;
const parsedFallback = parseKhbdSections(mockFallbackOutput, ["A", "B", "C", "D", "E"]);
assert(parsedFallback.E && parsedFallback.E.includes("HƯỚNG DẪN VỀ NHÀ"), "Parsed E fallback ok");
console.log("  -> Parser Fallback Heading E: PASS");

// 4. Kiểm tra Validator Sư phạm assertPhasePedagogyOutput cho Pha E
console.log("-> 4. Kiểm tra assertPhasePedagogyOutput cho Pha E...");
// Hợp lệ:
assert.doesNotThrow(() => {
  assertPhasePedagogyOutput("E", parsed.E);
}, "Valid Activity E should pass assertion");

// Không hợp lệ: Thiếu Bước 4
const invalidStep = `
#### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| **Bước 1: Chuyển giao nhiệm vụ:** **GV:** Giao bài tập. **HS:** Ghi bài. | Nội dung... |
`;
assert.throws(() => {
  assertPhasePedagogyOutput("E", invalidStep);
}, /chưa có đủ 4 bước/, "Should throw when missing CV 5512 steps");

// Không hợp lệ: Thiếu vai trò GV/HS
const invalidRole = `
#### d) Tổ chức thực hiện:
| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| **Bước 1: Chuyển giao:** Giao bài tập.<br>**Bước 2: Thực hiện:** Làm bài.<br>**Bước 3: Báo cáo:** Nộp bài.<br>**Bước 4: Kết luận:** Đánh giá. | Nội dung... |
`;
assert.throws(() => {
  assertPhasePedagogyOutput("E", invalidRole);
}, /chưa phân định rõ ràng vai trò/, "Should throw when missing GV/HS roles");
console.log("  -> Validator Sư phạm Pha E: PASS");

console.log("==================================================");
console.log("TẤT CẢ TEST TÍCH HỢP HOẠT ĐỘNG E ĐỀU ĐẠT (PASS)!");
console.log("==================================================");
