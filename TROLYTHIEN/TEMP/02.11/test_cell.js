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

const content = fs.readFileSync(path.join(__dirname, '01_Bai07_CanBacHaiVaCanThucBacHai.md'), 'utf8');
const lines = content.split('\n');
const tableLine = lines.find(l => l.includes('Tích hợp NLS'));
const cells = tableLine.split('|').filter(c => c.trim());

const cell0 = cells[0];
console.log("Original cell0 excerpt:", cell0.substring(0, 200));

// Giờ hãy chạy formatKhbdRoleLineBreaks và parseTableCellParagraphs
const { formatKhbdRoleLineBreaks } = require('../../engine/export_khbd_engine');
// Xem export_khbd_engine có export formatKhbdRoleLineBreaks không hoặc copy hàm đó vào test
