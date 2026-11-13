const path = require('path');
const fs = require('fs');

const { loadDocx } = require('../../engine/export_khbd_engine');
const docx = loadDocx();

global.window = {
  docx: docx,
  appState: { content: { illustrations: [] }, teachingContext: {} }
};

const khbdDocxPath = path.resolve(__dirname, '../../../js/khbd-docx.js');
const { DocxGenerator } = require(khbdDocxPath);
const gen = new DocxGenerator();

const sample1 = '- ***(Tích hợp NLS 5.2.TC2b: HS sử dụng máy tính cầm tay bấm phím căn bậc hai $\\sqrt{\\phantom{x}}$ để thấy máy tính báo lỗi Math ERROR, giải thích vì sao dưới dấu căn bậc hai không thể là số âm).***';

console.log("=== TEST SAMPLE 1 ===");
const runs1 = gen.parseInlineTextToRuns(sample1, null);
console.log("Total runs:", runs1.length);
runs1.forEach((r, idx) => {
  console.log(`Run ${idx}:`, JSON.stringify(r));
});
