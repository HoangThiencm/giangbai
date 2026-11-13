const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('../../engine/export_khbd_engine.js');

const testMd = path.resolve(__dirname, 'test_table_img.md');
const testDocx = path.resolve(__dirname, 'test_table_img.docx');

fs.writeFileSync(testMd, `# I. TEST
| Cot 1 | Cot 2 |
| :--- | :--- |
| Text 1<br>![Test Alt](khbd-ill:test_img) | Text 2 |
`);

const imgPath = path.resolve(__dirname, '../../1_SOAN_KHBD/Dau_vao/03.11/NCBH_DINH_LY_THALES_TOAN_8/images/hinh_1_tam_giac_thales_luoi.png');
const b64 = fs.readFileSync(imgPath).toString('base64');

createKhbdDocx({
  mdFilePath: testMd,
  outputDocxPath: testDocx,
  lessonInfo: { subject: 'Toan', grade: '8', lessonScope: 'Tiet 16', lessonTitle: 'Test' },
  illustrations: [{ id: 'test_img', dataUrl: 'data:image/png;base64,' + b64, width: 220, height: 180 }]
}).then(() => console.log('TABLE CELL IMAGE TEST PASSED!')).catch(e => console.error(e));
