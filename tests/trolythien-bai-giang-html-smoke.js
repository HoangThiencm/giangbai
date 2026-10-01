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
  '10. "10/ Tạo bài giảng HTML (từ PDF)"',
  '11. "11/ Vẽ hình học cực kỳ chính xác (từ đề bài / ảnh)"',
  '12. "12/ Chuẩn hoá văn bản (Hành chính / Đảng)"'
];

mustInclude(workflow, "description: Trợ lý Sư phạm Hoàng Thiên — Menu tương tác 12 tác vụ chính", "workflow");
mustInclude(workflow, "Gọi tool `ask_question` với danh sách 12 lựa chọn:", "workflow");
assert.ok(!workflow.includes("danh sách 9 lựa chọn"), "workflow con dong menu 9 lua chon");
mustInclude(rules, "## 1. Menu Cấp 1 (Tác vụ chính - 12 lựa chọn)", "rules");
mustInclude(rules, "Gọi tool `ask_question` với 12 lựa chọn:", "rules");
assert.ok(!rules.includes("Tác vụ chính - 9 lựa chọn"), "rules con tieu de menu 9 lua chon");

const workflowMenu = workflow.split("### BƯỚC 2")[0];
const workflowMenuCount = (workflowMenu.match(/^\s+\d+\. "/gm) || []).length;
assert.strictEqual(workflowMenuCount, 12, "workflow menu cap 1 phai dung 12 lua chon");

const rulesMenu = rules.split("## 2.")[0];
const rulesMenuCount = (rulesMenu.match(/^\s+\d+\. "/gm) || []).length;
assert.strictEqual(rulesMenuCount, 12, "rules menu cap 1 phai dung 12 lua chon");

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

for (let i = 1; i <= 11; i += 1) {
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

const presenterNeedles = [
  "Vá 23",
  "Vá 24",
  "data-step=\"4\"",
  "PageDown",
  "PageUp",
  "Backspace",
  "blank-screen",
  "mjx-container",
  "Vá 25",
  "toggleLaserMode",
  "togglePenMode",
  "#laserPointer",
  "#drawCanvas",
  "Vá 26",
  "getSweetVietnameseVoice",
  "laser-mode"
];
for (const needle of presenterNeedles) {
  mustInclude(prompt, needle, "master prompt presenter");
  mustInclude(rule, needle, "rule presenter");
}

const lectures = [
  "TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html",
  "TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html"
];
for (const rel of lectures) {
  const lecture = read(rel);
  mustInclude(lecture, "PageDown", rel);
  mustInclude(lecture, "PageUp", rel);
  mustInclude(lecture, "ArrowDown", rel);
  mustInclude(lecture, "ArrowUp", rel);
  mustInclude(lecture, "Backspace", rel);
  mustInclude(lecture, "zoomableFigure", rel);
  mustInclude(lecture, ".image-lightbox-backdrop, svg, img, .figure-box, [data-zoomable]", rel);
  mustInclude(lecture, 'data-step="3"', rel);
  mustInclude(lecture, "badge-role-sol", rel);
  mustInclude(lecture, 'id="laserPointer"', rel);
  mustInclude(lecture, 'id="drawCanvas"', rel);
  mustInclude(lecture, "toggleLaserMode", rel);
  mustInclude(lecture, "togglePenMode", rel);
  mustInclude(lecture, "e.key === 'l' || e.key === 'L'", rel);
  mustInclude(lecture, "e.key === 'p' || e.key === 'P'", rel);
  const slides = lecture.split(/<section class="slide-item\b/).slice(1);
  slides.forEach((slide, i) => {
    const cols = [];
    const reCol = /<div class="col-(?:board|task)"/g;
    const marks = [];
    let cm;
    while ((cm = reCol.exec(slide))) marks.push(cm.index);
    marks.forEach((pos, idx) => {
      const chunk = slide.slice(pos, marks[idx + 1] || slide.length);
      const steps = new Set();
      const re = /<div class="content-block\b[^>]*>/g;
      let m;
      while ((m = re.exec(chunk))) {
        const step = (m[0].match(/data-step="(\d+)"/) || [])[1];
        if (step && step !== "0") steps.add(step);
      }
      cols.push(steps);
    });
    for (let a = 0; a < cols.length; a++) {
      for (let b = a + 1; b < cols.length; b++) {
        for (const step of cols[a]) {
          assert.ok(!cols[b].has(step), rel + " slide " + (i + 1) + " trung data-step=" + step);
        }
      }
    }
  });
}

const bai12 = read("TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html");
function openingStep(src, id) {
  const at = src.indexOf('id="' + id + '"');
  assert.ok(at > 0, "thieu " + id);
  const tag = src.slice(src.lastIndexOf("<div", at), src.indexOf(">", at) + 1);
  return (tag.match(/data-step="(\d+)"/) || [])[1];
}
assert.strictEqual(openingStep(bai12, "s2_t1"), "1", "de bai Hoat dong 1 phai o buoc 1");
assert.strictEqual(openingStep(bai12, "s2_t2"), "1", "Hinh 4.12 phai cung buoc voi de bai");
assert.strictEqual(openingStep(bai12, "s2_b1"), "2", "quy uoc ky hieu phai o buoc 2");
assert.strictEqual(openingStep(bai12, "s2_t3"), "3", "huong dan cau a b phai o buoc 3");
assert.strictEqual(openingStep(bai12, "s2_b2"), "4", "he thuc chot phai o buoc 4");
mustInclude(bai12, "document.body.classList.contains('laser-mode')) return;", "bai12 laser");
mustInclude(bai12, "getSweetVietnameseVoice", "bai12 voice");
mustInclude(bai12, "speakBlockVi", "bai12 speak vi");
mustInclude(bai12, "function playAudioOrSpeech", "bai12 audio");
mustInclude(bai12, "audio/slide-", "bai12 mp3 path");
const edgeBat = read("TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Chay_Bai_12_Bang_Edge.bat");
mustInclude(edgeBat, "msedge", "bat edge");
mustInclude(edgeBat, "Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html", "bat html");
const exporter = read("TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/export_hoaimy_audio.py");
mustInclude(exporter, "edge_tts", "exporter lib");
mustInclude(exporter, "vi-VN-HoaiMyNeural", "exporter voice");
mustInclude(prompt, "playAudioOrSpeech", "prompt audio");
mustInclude(rule, "Chay_Bai_12_Bang_Edge.bat", "rule bat");
mustInclude(bai12, "Hoài My truyền cảm", "bai12 toast edge");
mustInclude(bai12, 'id="blackboardOverlay"', "bai12 bang");
mustInclude(bai12, "function toggleBlackboard", "bai12 toggle bang");
mustInclude(bai12, "function jumpToPeriod", "bai12 nhay tiet");
mustInclude(bai12, "speakBlockAuto", "bai12 loa");
mustInclude(bai12, "e.key === 'w' || e.key === 'W'", "bai12 phim W");
mustInclude(bai12, "overflow: hidden", "bai12 khoa cuon");
assert.ok(!bai12.includes('id="btnHelpCaption"'), "bai12 khong con nut tat phu de");
assert.ok(!bai12.includes('onclick="speakBlockEn('), "bai12 nut loa khong goi cung speakBlockEn");
mustInclude(prompt, 'id="blackboardOverlay"', "prompt bang");
mustInclude(rule, "speakBlockAuto", "rule loa");
mustInclude(prompt, "jumpToPeriod(3)", "prompt tiet 3");
assert.ok((bai12.match(/core-board/g) || []).length >= 9, "bai12 phai bao luu bang cot loi o cac slide vi du");
mustInclude(bai12, "Định lí 1", "bai12 dinh li 1");
mustInclude(bai12, "Định lí 2", "bai12 dinh li 2");
mustInclude(prompt, "Đồng hành Đề bài - Hình vẽ", "prompt hinh ve");
mustInclude(rule, "Phân bước Tuần tự 2 cột", "rule cot");

console.log("trolythien-bai-giang-html-smoke: PASS");
