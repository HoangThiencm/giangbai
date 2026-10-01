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

for (const needle of ["Times New Roman", "13pt", "1,27", "cantSplit", "tblHeader", "Nghị định 30/2020/NĐ-CP", "399-QĐ/TW", "05-HD/VPTW", "chính quyền 2 cấp", "1. Kết luận nhận diện", "5. Cảnh báo pháp lý/thẩm quyền"]) {
  mustInclude(workflow, needle, "workflow");
  mustInclude(rules, needle, "rules");
  mustInclude(guide, needle, "huong dan");
  mustInclude(prompt, needle, "prompt");
}

for (const heading of [
  "## A. Cơ sở áp dụng",
  "## B. Nguyên tắc xử lý tuyệt đối",
  "## C. Nhận diện văn bản",
  "## D. Xử lý văn bản hành chính NĐ 30",
  "## E. Xử lý văn bản Đảng QĐ 399",
  "## F. Kiểm tra chất lượng nội dung",
  "## G. Quy tắc về căn cứ pháp lý",
  "## H. Cấu trúc trả lời 5 phần",
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

console.log("trolythien-chuan-hoa-van-ban-smoke: PASS");
