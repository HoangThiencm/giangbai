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

// Đọc dòng từ 01_Bai07
const content = fs.readFileSync(path.join(__dirname, '01_Bai07_CanBacHaiVaCanThucBacHai.md'), 'utf8');
const lines = content.split('\n');
const tableLines = lines.filter(l => l.includes('Tích hợp NLS'));

console.log("Found table lines:", tableLines.length);
tableLines.forEach(l => {
  console.log("Raw line excerpt:", l.substring(0, 100));
});
