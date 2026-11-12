const path = require('path');
const fs = require('fs');
const { loadDocx, sanitizeKhbdMathSource } = require('../../engine/export_khbd_engine');
const docx = loadDocx();

global.window = {
  docx: docx,
  appState: { content: { illustrations: [] }, teachingContext: {} }
};

const khbdDocxPath = path.resolve(__dirname, '../../../js/khbd-docx.js');
const { DocxGenerator } = require(khbdDocxPath);

// Đọc chính xác đoạn sanitize và parse trong createKhbdDocx
const mdPath = path.join(__dirname, '01_Bai07_CanBacHaiVaCanThucBacHai.md');
let markdownContent = sanitizeKhbdMathSource(fs.readFileSync(mdPath, 'utf8'));

// Tìm dòng table có Tích hợp NLS
const lines = markdownContent.split('\n');
const tblLines = [];
let inTbl = false;
for (const line of lines) {
  if (line.trim().startsWith('|') && line.trim().endsWith('|')) {
    tblLines.push(line);
  }
}

console.log("Total tbl lines:", tblLines.length);
const targetLine = tblLines.find(l => l.includes('Tích hợp NLS'));
console.log("Found targetLine:", Boolean(targetLine));
if (targetLine) {
  const cells = targetLine.split('|').filter(c => c.trim());
  console.log("Cell 0 raw:", cells[0]);
}
