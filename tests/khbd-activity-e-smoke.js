const assert = require("assert");
const {
  PROMPTS,
  getPromptTemplate
} = require("../js/khbd-prompts.js");

console.log("==================================================");
console.log("BẮT ĐẦU KIỂM THỬ TÍCH HỢP HOẠT ĐỘNG E (HƯỚNG DẪN VỀ NHÀ)");
console.log("==================================================");

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
    const hasOnTap = /ôn\s*tập/i.test(text);
    const hasBaiTap = /làm\s*bài\s*tập|bài\s*tập/i.test(text);
    const hasChuanBi = /chuẩn\s*bị\s*bài/i.test(text);
    const hasMoRong = /tìm\s*tòi|mở\s*rộng/i.test(text);
    if (!hasOnTap || !hasBaiTap || !hasChuanBi || !hasMoRong) {
      throw new Error("Hoạt động E: Chưa đủ 4 mục (Ôn tập kiến thức, Làm bài tập, Chuẩn bị bài mới, Nhiệm vụ tìm tòi/mở rộng).");
    }
    return;
  }
}

function assertCompactListItems(text) {
  assert.match(text, /1\.\s*Ôn tập kiến thức/i, "Must have item 1 Ôn tập kiến thức");
  assert.match(text, /2\.\s*Làm bài tập/i, "Must have item 2 Làm bài tập");
  assert.match(text, /3\.\s*Chuẩn bị bài mới/i, "Must have item 3 Chuẩn bị bài mới");
  assert.match(text, /4\.\s*Nhiệm vụ tìm tòi, mở rộng/i, "Must have item 4 Tìm tòi, mở rộng");
}

function assertGeneratedCompactE(text) {
  assertCompactListItems(text);
  const sample = String(text).split(/#{1,3}\s*E\./i)[1] || text;
  assert.doesNotMatch(sample, /#{2,4}\s*a\)\s*Mục tiêu/i, "Sample E must not use a) Mục tiêu");
  assert.doesNotMatch(sample, /#{2,4}\s*d\)\s*Tổ chức thực hiện/i, "Sample E must not use d) Tổ chức thực hiện");
  assert.doesNotMatch(sample, /\|\s*Hoạt động của GV và HS\s*\|/i, "Sample E must not use 2-column table");
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
assertGeneratedCompactE(promptE);
assert(promptE.includes("SGK") && promptE.includes("SBT"), "Must instruct textbook & workbook exercises");
assert(promptE.includes("CẤM TUYỆT ĐỐI bảng Markdown 2 cột") || promptE.includes("CẤM TUYỆT ĐỐI bảng Markdown"), "Must forbid 2-column table");
assert(promptE.includes("Prompt AI an toàn"), "Must include AI prompt guide when AI enabled");
assert.match(promptE, /Mẫu Prompt:/, "Must include sample AI prompt");

const promptAE = getPromptTemplate("GENERATE_ACTIVITIES_AE", context);
assert.match(promptAE, /PHA E — HƯỚNG DẪN VỀ NHÀ/);
assert.match(promptAE, /CẤM TUYỆT ĐỐI mục a\) Mục tiêu/);
assert.match(promptAE, /1\.\s*Ôn tập kiến thức/);
assert.match(promptAE, /danh sách 4 mục/);
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
## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ (3 phút)
1. Ôn tập kiến thức: Ôn lại các định nghĩa, quy tắc, công thức trọng tâm đã học trong bài.
2. Làm bài tập: Hoàn thành các bài tập còn lại trong SGK (chưa làm/chữa ở Hoạt động C và D) và SBT.
3. Chuẩn bị bài mới: Đọc trước nội dung bài học tiếp theo trong SGK.
4. Nhiệm vụ tìm tòi, mở rộng: Tìm hiểu ứng dụng thực tế của căn bậc hai.
- Hướng dẫn Prompt AI an toàn:
+ Mẫu Prompt: "Em là học sinh lớp 7, em đang tự học bài Số vô tỉ và gặp khó khăn ở [nêu bài tập]. Bạn hãy đóng vai gia sư gợi mở..."
`;

const parsed = parseKhbdSections(mock1ClickOutput, ["A", "B", "C", "D", "E"]);
assert(parsed.A && parsed.A.includes("HOẠT ĐỘNG MỞ ĐẦU"), "Parsed A ok");
assert(parsed.B && parsed.B.includes("HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC"), "Parsed B ok");
assert(parsed.C && parsed.C.includes("HOẠT ĐỘNG LUYỆN TẬP"), "Parsed C ok");
assert(parsed.D && parsed.D.includes("HOẠT ĐỘNG VẬN DỤNG"), "Parsed D ok");
assert(parsed.E && parsed.E.includes("HƯỚNG DẪN VỀ NHÀ"), "Parsed E ok with marker");
assertGeneratedCompactE(parsed.E);
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
1. Ôn tập kiến thức: Ôn lại kiến thức trọng tâm.
2. Làm bài tập: Hoàn thành bài tập còn lại SGK và SBT.
3. Chuẩn bị bài mới: Đọc trước bài mới.
4. Nhiệm vụ tìm tòi, mở rộng: Tìm hiểu ứng dụng thực tế.
`;
const parsedFallback = parseKhbdSections(mockFallbackOutput, ["A", "B", "C", "D", "E"]);
assert(parsedFallback.E && parsedFallback.E.includes("HƯỚNG DẪN VỀ NHÀ"), "Parsed E fallback ok");
assertGeneratedCompactE(parsedFallback.E);
console.log("  -> Parser Fallback Heading E: PASS");

// 4. Kiểm tra Validator Sư phạm assertPhasePedagogyOutput cho Pha E
console.log("-> 4. Kiểm tra assertPhasePedagogyOutput cho Pha E...");
assert.doesNotThrow(() => {
  assertPhasePedagogyOutput("E", parsed.E);
}, "Valid compact Activity E should pass assertion");

const invalidMissing = `
## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ (3 phút)
1. Ôn tập kiến thức: Ôn lại định nghĩa.
2. Làm bài tập: Làm bài 2.1 SGK.
`;
assert.throws(() => {
  assertPhasePedagogyOutput("E", invalidMissing);
}, /Chưa đủ 4 mục/, "Should throw when missing compact E items");
console.log("  -> Validator Sư phạm Pha E: PASS");

console.log("==================================================");
console.log("TẤT CẢ TEST TÍCH HỢP HOẠT ĐỘNG E ĐỀU ĐẠT (PASS)!");
console.log("==================================================");
