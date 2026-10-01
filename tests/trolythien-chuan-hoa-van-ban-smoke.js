"use strict";

const assert = require("assert");
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
const guide = read("TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/HUONG_DAN_CHUAN_HOA_VAN_BAN.md");
const prompt = read("TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/PROMPT_CHUAN_HOA_VAN_BAN.md");
const option = '12. "12/ Chuẩn hoá văn bản (Hành chính / Đảng)"';

const workflowMenu = workflow.split("### BƯỚC 2")[0];
const rulesMenu = rules.split("## 2.")[0];
assert.strictEqual((workflowMenu.match(/^\s+\d+\. "/gm) || []).length, 12, "workflow menu 12");
assert.strictEqual((rulesMenu.match(/^\s+\d+\. "/gm) || []).length, 12, "rules menu 12");
mustInclude(workflowMenu, option, "workflow menu");
mustInclude(rulesMenu, option, "rules menu");
mustInclude(workflow, "Menu tương tác 12 tác vụ chính", "workflow");
mustInclude(workflow, '#### Nhánh 12: Khi chọn "12/ Chuẩn hoá văn bản (Hành chính / Đảng)"', "workflow");
mustInclude(rules, "## 1. Menu Cấp 1 (Tác vụ chính - 12 lựa chọn)", "rules");
mustInclude(rules, "## 7. Quy chuẩn kỹ thuật cho Nhánh 12", "rules");

const paths = [
  "TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/Dau_vao/",
  "TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/Ket_qua/",
  "TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/HUONG_DAN_CHUAN_HOA_VAN_BAN.md",
  "TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/PROMPT_CHUAN_HOA_VAN_BAN.md",
  "[Ten_File]_Chuan_Hoa.docx",
  ".docx"
];
for (const needle of paths) {
  mustInclude(workflow, needle, "workflow nhanh 12");
  mustInclude(rules, needle, "rules nhanh 12");
  mustInclude(guide, needle, "huong dan");
}

for (const needle of ["Times New Roman", "13pt", "1,27", "cantSplit", "tblHeader", "Nghị định 30/2020/NĐ-CP", "399-QĐ/TW", "05-HD/VPTW", "chính quyền 2 cấp"]) {
  mustInclude(workflow, needle, "workflow");
  mustInclude(rules, needle, "rules");
  mustInclude(guide, needle, "huong dan");
  mustInclude(prompt, needle, "prompt");
}

for (const needle of ["65 mm", "100 mm", "v:line", "0.75pt", "11,5pt", "không xuất báo cáo 5 phần"]) {
  mustInclude(workflow, needle, "workflow the thuc");
  mustInclude(rules, needle, "rules the thuc");
  mustInclude(prompt, needle, "prompt the thuc");
}
mustInclude(guide, "v:line", "huong dan");
mustInclude(guide, "2–3 dòng", "huong dan chat");
mustInclude(prompt, "## H. Phản hồi chat ngắn", "prompt");
assert.ok(!prompt.includes("## H. Cấu trúc trả lời 5 phần"), "prompt con yeu cau bao cao 5 phan");

for (const heading of [
  "## A. Cơ sở áp dụng",
  "## B. Nguyên tắc xử lý tuyệt đối",
  "## C. Nhận diện văn bản",
  "## D. Xử lý văn bản hành chính NĐ 30",
  "## E. Xử lý văn bản Đảng QĐ 399",
  "## F. Kiểm tra chất lượng nội dung",
  "## G. Quy tắc về căn cứ pháp lý",
  "## H. Phản hồi chat ngắn",
  "## I. Yêu cầu cuối cùng"
]) {
  mustInclude(prompt, heading, "prompt");
}

const inputDir = path.join(root, "TROLYTHIEN", "12_CHUAN_HOA_VAN_BAN", "Dau_vao");
const outputDir = path.join(root, "TROLYTHIEN", "12_CHUAN_HOA_VAN_BAN", "Ket_qua");
assert.ok(fs.existsSync(inputDir) && fs.statSync(inputDir).isDirectory(), "Thieu Dau_vao");
assert.ok(fs.existsSync(outputDir) && fs.statSync(outputDir).isDirectory(), "Thieu Ket_qua");
assert.ok(fs.existsSync(path.join(inputDir, ".gitkeep")), "Thieu Dau_vao/.gitkeep");
assert.ok(fs.existsSync(path.join(outputDir, ".gitkeep")), "Thieu Ket_qua/.gitkeep");

const script = read("tools/standardize_kh_dayhoc.py");
mustInclude(script, "Mm(65)", "script");
mustInclude(script, "Mm(100)", "script");
mustInclude(script, "v:line", "script");
mustInclude(script, "0.75pt", "script");
mustInclude(script, "size_pt=11.5", "script");
assert.ok(!script.includes("p_sp2"), "script con doan trong p_sp2");
assert.ok(!script.includes("────────"), "script con ky tu gach ngang");

const docxPath = path.join(outputDir, "KH_TO_CHUC_DAY_HOC_TRUC_TUYEN_2026_2027_TRANPHU_Chuan_Hoa.docx");
assert.ok(fs.existsSync(docxPath), "Thieu file ket qua docx");
const { execFileSync } = require("child_process");
const xml = execFileSync("python", ["-c", "import zipfile,sys; z=zipfile.ZipFile(sys.argv[1]); sys.stdout.buffer.write(z.read('word/document.xml'))", docxPath]).toString("utf8");
mustInclude(xml, "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "docx");
mustInclude(xml, "ỦY BAN NHÂN DÂN XÃ XUÂN ĐÔNG", "docx");
mustInclude(xml, "v:line", "docx");
mustInclude(xml, "0.75pt", "docx");
mustInclude(xml, "w:cantSplit", "docx");
mustInclude(xml, "w:tblHeader", "docx");
assert.ok(!xml.includes("────────"), "docx con ky tu gach ngang");
assert.ok(!xml.includes("w:u "), "docx con gach chan underline");
const quocHieu = xml.split("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM").length - 1;
assert.strictEqual(quocHieu, 1, "quoc hieu phai nam trong mot run");

console.log("trolythien-chuan-hoa-van-ban-smoke: PASS");
