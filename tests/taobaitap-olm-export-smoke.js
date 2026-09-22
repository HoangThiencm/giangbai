'use strict';

const fs = require('fs');
const path = require('path');
const assert = require('assert');

console.log('================================================================');
console.log('KIỂM THỬ: XUẤT CẢ 2 HƯỚNG OLM.VN TRONG TAOBAITAP.HTML');
console.log('================================================================');

const root = path.join(__dirname, '..');
const filePath = path.join(root, 'taobaitap.html');
assert.ok(fs.existsSync(filePath), 'taobaitap.html phải tồn tại');

const content = fs.readFileSync(filePath, 'utf8');

// 1. Kiểm tra Hướng 1: Đề thi thông minh
assert.ok(content.includes('const exportWordOLM ='), 'taobaitap.html phải có exportWordOLM');
assert.ok(content.includes('De_Thi_OLM.docx'), 'exportWordOLM phải xuất file De_Thi_OLM.docx');
assert.ok(content.includes('onClick={exportWordOLM}'), 'taobaitap.html phải có nút gọi exportWordOLM');

// 2. Kiểm tra Hướng 2: Bộ đôi Đề bài + Hướng dẫn giải (cho dạng Đề thi PDF)
assert.ok(content.includes('const exportOlmPdfPair ='), 'taobaitap.html phải có exportOlmPdfPair');
assert.ok(content.includes('De_Bai_OLM_PDF.docx'), 'phải xuất file De_Bai_OLM_PDF.docx');
assert.ok(content.includes('Huong_Dan_Giai_OLM_PDF.docx'), 'phải xuất file Huong_Dan_Giai_OLM_PDF.docx');
assert.ok(content.includes('onClick={exportOlmPdfPair}'), 'taobaitap.html phải có nút gọi exportOlmPdfPair');
assert.ok(content.includes('Bộ đôi OLM (Đề & Giải PDF)'), 'nút phải có nhãn Bộ đôi OLM (Đề & Giải PDF)');

console.log('✓ taobaitap.html: Đã tích hợp trọn vẹn cả 2 hướng OLM.vn (Đề thông minh + Bộ đôi PDF)!');
console.log('================================================================\n');
