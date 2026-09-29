"use strict";

const assert = require("assert");
const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");

function read(rel) {
  const full = path.join(root, rel);
  assert.ok(fs.existsSync(full), "Thieu file: " + rel);
  return fs.readFileSync(full, "utf8").replace(/\r\n/g, "\n");
}

function mustInclude(text, needle, label) {
  assert.ok(text.includes(needle), label + " thieu: " + needle);
}

const workflow = read(".agents/workflows/thien.md");
const rules = read(".agents/rules/tro-ly-thien.md");
const promptPath = "TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md";
const prompt = read(promptPath);

const menuOptions = [
  '1. "1/ Duyệt giáo án"',
  '2. "2/ Soạn Giáo án (KHBD)"',
  '3. "3/ Tạo bài tập"',
  '4. "4/ Duyệt đề"',
  '5. "5/ Game giáo dục"',
  '6. "6/ Sổ điểm"',
  '7. "7/ Quản lý tổ chuyên môn"',
  '8. "8/ Tạo báo cáo"',
  '9. "9/ Viết sáng kiến"',
  '10. "10/ Tạo bài giảng HTML (từ PDF)"'
];

mustInclude(workflow, "description: Trợ lý Sư phạm Hoàng Thiên — Menu tương tác 10 tác vụ chính", "workflow");
mustInclude(workflow, "Gọi tool `ask_question` với danh sách 10 lựa chọn:", "workflow");
assert.ok(!workflow.includes("danh sách 9 lựa chọn"), "workflow con dong menu 9 lua chon");
mustInclude(rules, "## 1. Menu Cấp 1 (Tác vụ chính - 10 lựa chọn)", "rules");
mustInclude(rules, "Gọi tool `ask_question` với 10 lựa chọn:", "rules");
assert.ok(!rules.includes("Tác vụ chính - 9 lựa chọn"), "rules con tieu de menu 9 lua chon");

const workflowMenu = workflow.split("### BƯỚC 2")[0];
const workflowMenuCount = (workflowMenu.match(/^\s+\d+\. "/gm) || []).length;
assert.strictEqual(workflowMenuCount, 10, "workflow menu cap 1 phai dung 10 lua chon");

const rulesMenu = rules.split("## 2.")[0];
const rulesMenuCount = (rulesMenu.match(/^\s+\d+\. "/gm) || []).length;
assert.strictEqual(rulesMenuCount, 10, "rules menu cap 1 phai dung 10 lua chon");

for (const option of menuOptions) {
  mustInclude(workflowMenu, option, "workflow menu");
  mustInclude(rulesMenu, option, "rules menu");
}

const preservedBranches = [
  '#### Nhánh 1: Khi chọn "1/ Duyệt giáo án"\nHướng dẫn nạp file giáo án cần thẩm định vào `TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/`, xuất kết quả biên bản ra `TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/`.',
  '#### Nhánh 2: Khi chọn "2/ Soạn Giáo án (KHBD)"\nTự động kích hoạt quy trình soạn KHBD chuẩn V2.0:\n- File đầu vào (SGK, PPCT): đọc từ `TROLYTHIEN/1_SOAN_KHBD/Dau_vao/`\n- File kết quả: tự động xuất Word ra `TROLYTHIEN/1_SOAN_KHBD/Ket_qua/`',
  '#### Nhánh 3: Khi chọn "3/ Tạo bài tập"\nGọi tiếp tool `ask_question` với đúng 8 định dạng chuẩn (file đầu vào tại `TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/`, kết quả tại `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/`):',
  '1. "1. ⭐ Dạng Công văn 7991 (17 câu)"',
  '8. "8. ⭐ Bài tập tự luận"',
  '#### Nhánh 4: Khi chọn "4/ Duyệt đề"\nHướng dẫn nạp file đề thi và ma trận vào `TROLYTHIEN/4_DUYET_DE/Dau_vao/`, xuất kết quả thẩm định ra `TROLYTHIEN/4_DUYET_DE/Ket_qua/`.',
  '#### Nhánh 5: Khi chọn "5/ Game giáo dục"',
  "https://www.hoangthiencm.id.vn/trochoi.html",
  '#### Nhánh 6: Khi chọn "6/ Sổ điểm"',
  "https://www.hoangthiencm.id.vn/sodiem.html",
  '#### Nhánh 7: Khi chọn "7/ Quản lý tổ chuyên môn"',
  "https://www.hoangthiencm.id.vn/phancongtochuyenmon.html",
  '#### Nhánh 8: Khi chọn "8/ Tạo báo cáo"',
  "TROLYTHIEN/8_TAO_BAO_CAO/Dau_vao/",
  ".agents/rules/taobaocao.md",
  '#### Nhánh 9: Khi chọn "9/ Viết sáng kiến"',
  "TROLYTHIEN/9_VIET_SANG_KIEN/Ket_qua/",
  ".agents/rules/vietsangkien.md"
];
for (const snippet of preservedBranches) {
  mustInclude(workflow, snippet, "workflow nhanh 1-9");
}

for (let i = 1; i <= 10; i += 1) {
  mustInclude(workflow, "#### Nhánh " + i + ":", "workflow");
}

const branch10 = [
  '#### Nhánh 10: Khi chọn "10/ Tạo bài giảng HTML (từ PDF)"',
  "Môn gì?",
  "Lớp mấy?",
  "Mấy tiết (thời lượng)?",
  "TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/",
  "TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/[Tên_Bài].html",
  "TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md",
  "- Tuân thủ quy chuẩn riêng tại: .agents/rules/tao-bai-giang-html.md",
  "Single-file HTML standalone",
  "16:9",
  "CV 5512",
  "GDPT 2018",
  "MathJax 3",
  "$..$",
  "$$..$$"
];
for (const needle of branch10) {
  mustInclude(workflow, needle, "workflow nhanh 10");
}

const preservedRules = [
  "## 2. Xử lý đường dẫn web trực tiếp:",
  "https://www.hoangthiencm.id.vn/trochoi.html",
  "## 3. Menu Cấp 2 khi chọn \"3/ Tạo bài tập\" (8 định dạng đánh số)",
  "1. \"1. ⭐ Dạng Công văn 7991 (17 câu)\"",
  "8. \"8. ⭐ Bài tập tự luận\"",
  "## 4. Quy ước thư mục đầu vào và kết quả (Bắt buộc không lưu lung tung)",
  "**1/ Soạn Giáo án (KHBD):**",
  "TROLYTHIEN/1_SOAN_KHBD/Dau_vao/",
  "**2/ Tạo bài tập:**",
  "TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/",
  "**3/ Duyệt giáo án:**",
  "TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/",
  "**4/ Duyệt đề:**",
  "TROLYTHIEN/4_DUYET_DE/Ket_qua/",
  "**8/ Tạo báo cáo:**",
  ".agents/rules/taobaocao.md",
  "**9/ Viết sáng kiến:**",
  ".agents/rules/vietsangkien.md"
];
for (const needle of preservedRules) {
  mustInclude(rules, needle, "rules muc cu");
}

const rulesBranch10 = [
  "**10/ Tạo bài giảng HTML (từ PDF):**",
  "Bắt buộc hỏi đúng 3 thông tin: Môn gì? Lớp mấy? Mấy tiết (thời lượng)?",
  "TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/",
  "TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/[Tên_Bài].html",
  "TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md",
  ".agents/rules/tao-bai-giang-html.md",
  "## 5. Quy tắc bổ sung cho Nhánh 10",
  "Single-file standalone",
  "Chế độ Thiết kế",
  "Chế độ Trình chiếu 16:9",
  "CV 5512",
  "GDPT 2018",
  "Hoạt động của Giáo viên",
  "Hoạt động của Học sinh",
  "MathJax 3",
  "MathJax.typesetPromise()",
  "mjx-container svg { display: inline !important; }"
];
for (const needle of rulesBranch10) {
  mustInclude(rules, needle, "rules nhanh 10");
}

const inputDir = path.join(root, "TROLYTHIEN", "10_BAI_GIANG_HTML", "Dau_vao");
const outputDir = path.join(root, "TROLYTHIEN", "10_BAI_GIANG_HTML", "Ket_qua");
assert.ok(fs.existsSync(inputDir) && fs.statSync(inputDir).isDirectory(), "Thieu thu muc Dau_vao");
assert.ok(fs.existsSync(outputDir) && fs.statSync(outputDir).isDirectory(), "Thieu thu muc Ket_qua");
assert.ok(fs.existsSync(path.join(inputDir, ".gitkeep")), "Thieu Dau_vao/.gitkeep");
assert.ok(fs.existsSync(path.join(outputDir, ".gitkeep")), "Thieu Ket_qua/.gitkeep");

const promptNeedles = [
  "Môn gì?",
  "Lớp mấy?",
  "Mấy tiết",
  "TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/",
  "TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/[Tên_Bài].html",
  "Single-file",
  "standalone",
  "file:///",
  "Thiết kế",
  "Trình chiếu",
  "16:9",
  "Hoạt động của Giáo viên",
  "Hoạt động của Học sinh",
  "CV 5512",
  "GDPT 2018",
  "Chuyển giao nhiệm vụ",
  "Thực hiện nhiệm vụ",
  "Báo cáo, thảo luận",
  "Kết luận, nhận định",
  "MathJax",
  "tex-svg.js",
  "inlineMath",
  "displayMath",
  "mjx-container svg { display: inline !important; }",
  "MathJax.typesetPromise()",
  "toggleAnswer",
  "đếm ngược",
  "PDF",
  "không bịa",
  "45 phút",
  "90 phút",
  "Tiết 1",
  "Tiết 2",
  "<!DOCTYPE html>",
  "</html>"
];
for (const needle of promptNeedles) {
  mustInclude(prompt, needle, "master prompt");
}

assert.match(prompt, /8[\u2013-]12/, "master prompt thieu 8-12 slides");
assert.match(prompt, /16[\u2013-]22/, "master prompt thieu 16-22 slides");
assert.match(prompt, /\$\.\.\$/, "master prompt thieu cu phap inline $..$");
assert.match(prompt, /\$\$\.\.\$\$/, "master prompt thieu cu phap block $$..$$");

const rulePath = ".agents/rules/tao-bai-giang-html.md";
const rule = read(rulePath);
mustInclude(rule, "# QUY CHUẨN SOẠN BÀI GIẢNG HTML TRÌNH CHIẾU TƯƠNG TÁC (NHÁNH 10)", "rule nhanh 10");
for (const needle of promptNeedles) {
  mustInclude(rule, needle, "rule nhanh 10");
}
assert.match(rule, /8[\u2013-]12/, "rule nhanh 10 thieu 8-12 slides");
assert.match(rule, /16[\u2013-]22/, "rule nhanh 10 thieu 16-22 slides");
assert.match(rule, /\$\.\.\$/, "rule nhanh 10 thieu cu phap inline $..$");
assert.match(rule, /\$\$\.\.\$\$/, "rule nhanh 10 thieu cu phap block $$..$$");

const gitignore = read(".gitignore");
assert.ok(!/^TROLYTHIEN\/\s*$/m.test(gitignore), "gitignore van chan ca thu muc TROLYTHIEN/");
const gitkeepRules = [
  "TROLYTHIEN/**/Dau_vao/*",
  "!TROLYTHIEN/**/Dau_vao/.gitkeep",
  "!TROLYTHIEN/**/Dau_vao/*.md",
  "TROLYTHIEN/**/Ket_qua/*",
  "!TROLYTHIEN/**/Ket_qua/.gitkeep",
  "!TROLYTHIEN/**/*.md",
  "!TROLYTHIEN/**/*.js"
];
for (const needle of gitkeepRules) {
  mustInclude(gitignore, needle, "gitignore");
}

function gitCheckIgnore(rel) {
  try {
    execFileSync("git", ["check-ignore", "-q", "--no-index", "--", rel], {
      cwd: root,
      stdio: "ignore"
    });
    return true;
  } catch (error) {
    if (error && error.status === 1) return false;
    throw error;
  }
}

assert.strictEqual(gitCheckIgnore("TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/gia-lap.pdf"), true, "pdf trong Dau_vao phai bi gitignore");
assert.strictEqual(gitCheckIgnore("TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/gia-lap.html"), true, "html ket qua phai bi gitignore");
assert.strictEqual(gitCheckIgnore(promptPath), false, "master prompt phai duoc git theo doi");
assert.strictEqual(gitCheckIgnore("TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/.gitkeep"), false, "Dau_vao/.gitkeep phai duoc git theo doi");
assert.strictEqual(gitCheckIgnore("TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/.gitkeep"), false, "Ket_qua/.gitkeep phai duoc git theo doi");
assert.strictEqual(gitCheckIgnore(rulePath), false, "rule agents phai duoc git theo doi");

console.log("trolythien-bai-giang-html-smoke: PASS");
