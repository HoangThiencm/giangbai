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

// Đọc logic export_khbd_engine
const engineCode = fs.readFileSync(path.resolve(__dirname, '../../engine/export_khbd_engine.js'), 'utf8');

// Chạy test trực tiếp createKhbdDocx trên 01_Bai07 và in ra các TextRun của bảng
const { createKhbdDocx } = require('../../engine/export_khbd_engine');

async function testOne() {
  const mdPath = path.join(__dirname, '01_Bai07_CanBacHaiVaCanThucBacHai.md');
  const outPath = path.join(__dirname, 'test_out.docx');
  await createKhbdDocx({
    mdFilePath: mdPath,
    outputDocxPath: outPath,
    lessonInfo: {
      topic: "BÀI 7",
      ppct: "Tiết 23",
      lessonScope: "Tiết 23",
      duration: "02 tiết"
    }
  });

  // Đọc lại xml
  const AdmZip = require('adm-zip'); // nếu có adm-zip hoặc dùng python
}
testOne().catch(console.error);
