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
const guide = read("TROLYTHIEN/11_VE_HINH/HUONG_DAN_VE_HINH.md");
const option = '11. "11/ Vẽ hình học cực kỳ chính xác (từ đề bài / ảnh)"';

const workflowMenu = workflow.split("### BƯỚC 2")[0];
const rulesMenu = rules.split("## 2.")[0];
assert.strictEqual((workflowMenu.match(/^\s+\d+\. "/gm) || []).length, 12, "workflow menu 12");
assert.strictEqual((rulesMenu.match(/^\s+\d+\. "/gm) || []).length, 12, "rules menu 12");
mustInclude(workflowMenu, option, "workflow menu");
mustInclude(rulesMenu, option, "rules menu");
mustInclude(workflow, '#### Nhánh 11: Khi chọn "11/ Vẽ hình học cực kỳ chính xác (từ đề bài / ảnh)"', "workflow");
mustInclude(rules, "## 4. Quy ước thư mục đầu vào và kết quả", "rules");
mustInclude(rules, "## 6. Quy chuẩn kỹ thuật cho Nhánh 11", "rules");

const paths = [
  "TROLYTHIEN/11_VE_HINH/Dau_vao/",
  "TROLYTHIEN/11_VE_HINH/Ket_qua/",
  "TROLYTHIEN/11_VE_HINH/HUONG_DAN_VE_HINH.md",
  "[Ten_Hinh].png",
  "[Ten_Hinh].svg",
  "[Ten_Hinh]_geogebra.txt",
  "[Ten_Hinh].html"
];
for (const needle of paths) {
  mustInclude(workflow, needle, "workflow nhanh 11");
  mustInclude(rules, needle, "rules nhanh 11");
  mustInclude(guide, needle, "huong dan");
}

for (const needle of ["trực tâm", "trọng tâm", "nét đứt", "Segment", "viewBox", "https://www.hoangthiencm.id.vn/vehinh.html", "file:///c:/Users/HoangThien/Documents/GitHub/giangbai/vehinh.html"]) {
  mustInclude(guide, needle, "huong dan");
  mustInclude(rules, needle, "rules muc 6");
}

const inputDir = path.join(root, "TROLYTHIEN", "11_VE_HINH", "Dau_vao");
const outputDir = path.join(root, "TROLYTHIEN", "11_VE_HINH", "Ket_qua");
assert.ok(fs.existsSync(inputDir) && fs.statSync(inputDir).isDirectory(), "Thieu Dau_vao");
assert.ok(fs.existsSync(outputDir) && fs.statSync(outputDir).isDirectory(), "Thieu Ket_qua");
assert.ok(fs.existsSync(path.join(inputDir, ".gitkeep")), "Thieu Dau_vao/.gitkeep");
assert.ok(fs.existsSync(path.join(outputDir, ".gitkeep")), "Thieu Ket_qua/.gitkeep");

console.log("trolythien-vehinh-smoke: PASS");
