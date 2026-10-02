"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const root = path.resolve(__dirname, "..");

function read(rel) {
  const full = path.join(root, rel);
  assert.ok(fs.existsSync(full), "Thieu file: " + rel);
  return fs.readFileSync(full, "utf8").replace(/\r\n/g, "\n");
}

function mustInclude(text, needle, label) {
  assert.ok(text.includes(needle), label + " thieu: " + needle);
}

// 1. Kiểm tra cấu hình Menu workflow & rules
const workflow = read(".agents/workflows/thien.md");
const rules = read(".agents/rules/tro-ly-thien.md");
const guide = read("TROLYTHIEN/13_CHUYEN_GHI_AM/HUONG_DAN_CHUYEN_GHI_AM.md");
const prompt = read("TROLYTHIEN/13_CHUYEN_GHI_AM/PROMPT_CHUYEN_GHI_AM.md");
const option = '13. "13/ Chuyển ghi âm thành văn bản (iPhone / MP3)"';

mustInclude(workflow, option, "workflow menu 13");
mustInclude(rules, option, "rules menu 13");
mustInclude(workflow, "Menu tương tác 13 tác vụ chính", "workflow");
mustInclude(workflow, '#### Nhánh 13: Khi chọn "13/ Chuyển ghi âm thành văn bản (iPhone / MP3)"', "workflow");
mustInclude(rules, "## 1. Menu Cấp 1 (Tác vụ chính - 13 lựa chọn)", "rules");
mustInclude(rules, "## 9. Quy chuẩn kỹ thuật cho Nhánh 13", "rules");

// 2. Kiểm tra các đường dẫn và từ khóa cốt lõi
const paths = [
  "TROLYTHIEN/13_CHUYEN_GHI_AM/Dau_vao/",
  "TROLYTHIEN/13_CHUYEN_GHI_AM/Ket_qua/",
  "TROLYTHIEN/13_CHUYEN_GHI_AM/HUONG_DAN_CHUYEN_GHI_AM.md",
  "TROLYTHIEN/13_CHUYEN_GHI_AM/PROMPT_CHUYEN_GHI_AM.md",
  ".m4a",
  ".mp3",
  ".docx",
  ".txt"
];
for (const needle of paths) {
  mustInclude(workflow, needle, "workflow nhanh 13");
  mustInclude(rules, needle, "rules nhanh 13");
  mustInclude(guide, needle, "huong dan nhanh 13");
}

for (const needle of ["90", "95", "iPhone", "Times New Roman", "13pt", "1.27 cm", "nguyên văn", "ngữ cảnh", "chính tả"]) {
  mustInclude(guide, needle, "huong dan");
  mustInclude(prompt, needle, "prompt");
}

// 3. Kiểm tra thư mục đầu vào và kết quả
const inputDir = path.join(root, "TROLYTHIEN", "13_CHUYEN_GHI_AM", "Dau_vao");
const outputDir = path.join(root, "TROLYTHIEN", "13_CHUYEN_GHI_AM", "Ket_qua");
assert.ok(fs.existsSync(inputDir) && fs.statSync(inputDir).isDirectory(), "Thieu Dau_vao");
assert.ok(fs.existsSync(outputDir) && fs.statSync(outputDir).isDirectory(), "Thieu Ket_qua");
assert.ok(fs.existsSync(path.join(inputDir, ".gitkeep")), "Thieu Dau_vao/.gitkeep");
assert.ok(fs.existsSync(path.join(outputDir, ".gitkeep")), "Thieu Ket_qua/.gitkeep");

// 4. Kiểm tra công cụ xuất văn bản tools/chuyen_ghi_am.py
const testAudioName = "test_smoke_recording.m4a";
const sampleText = "Chủ trì: Xin chào toàn thể các thầy cô giáo trong tổ chuyên môn.\nThầy Nam: Tôi hoàn toàn nhất trí với phương án phân công chuyên môn đã đề ra.";
execFileSync("python", ["tools/chuyen_ghi_am.py", testAudioName, sampleText, outputDir]);

const expectedDocx = path.join(outputDir, "test_smoke_recording.docx");
const expectedTxt = path.join(outputDir, "test_smoke_recording.txt");
assert.ok(fs.existsSync(expectedDocx), "Thieu file test_smoke_recording.docx");
assert.ok(fs.existsSync(expectedTxt), "Thieu file test_smoke_recording.txt");

// Dọn dẹp tệp test smoke
fs.unlinkSync(expectedDocx);
fs.unlinkSync(expectedTxt);

console.log("trolythien-chuyen-ghi-am-smoke: PASS");
