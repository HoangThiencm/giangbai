'use strict';

const fs = require('fs');
const path = require('path');
const assert = require('assert');

console.log('================================================================');
console.log('KIỂM THỬ: TAB CHUYÊN BIỆT HỌC LIỆU OLM.VN TRONG TAOBAITAP.HTML');
console.log('================================================================');

const root = path.join(__dirname, '..');
const filePath = path.join(root, 'taobaitap.html');
assert.ok(fs.existsSync(filePath), 'taobaitap.html phải tồn tại');

const content = fs.readFileSync(filePath, 'utf8');

// 1. Kiểm tra hàm xuất và cú pháp OLM chính thức
assert.ok(content.includes('const exportWordOLM ='), 'taobaitap.html phải có exportWordOLM');
assert.ok(content.includes('Phần 1. Trắc nghiệm nhiều lựa chọn.'), 'Phải có tiêu đề Phần 1 chuẩn OLM');
assert.ok(content.includes('Phần 2. Trắc nghiệm đúng/sai.'), 'Phải có tiêu đề Phần 2 chuẩn OLM');
assert.ok(content.includes('#${item.text}'), 'Phần Đúng/Sai phải dùng ký hiệu # trước từng mệnh đề chuẩn OLM');
assert.ok(content.includes('<u>${label})</u>'), 'Mệnh đề đúng phải gạch chân nhãn a), b), ...');
assert.ok(content.includes('Câu ${num}.'), 'Số câu OLM phải dùng dấu chấm sau số thứ tự');
assert.ok(content.includes('[HDG]'), 'Phải có thẻ [HDG] cho lời giải OLM');
assert.ok(content.includes('De_Thi_OLM.docx'), 'Phải xuất file De_Thi_OLM.docx');

// 2. Kiểm tra bộ đôi OLM PDF
assert.ok(content.includes('const exportOlmPdfPair ='), 'taobaitap.html phải có exportOlmPdfPair');
assert.ok(content.includes('De_Bai_OLM_PDF.docx'), 'Phải xuất file De_Bai_OLM_PDF.docx');
assert.ok(content.includes('Huong_Dan_Giai_OLM_PDF.docx'), 'Phải xuất file Huong_Dan_Giai_OLM_PDF.docx');

// 3. Kiểm tra Modal / Tab chuyên biệt OLM
assert.ok(content.includes('showOlmModal'), 'Phải có state showOlmModal');
assert.ok(content.includes('Học liệu OLM'), 'Toolbar phải có nút Học liệu OLM');
assert.ok(content.includes('setShowOlmModal(true)'), 'Nút toolbar phải mở modal OLM');
assert.ok(content.includes('Tải file Word thông minh (OLM)'), 'Modal phải có hướng xuất đề thông minh');
assert.ok(content.includes('Tải bộ đôi Đề &amp; Giải PDF'), 'Modal phải có hướng xuất bộ đôi đề và giải');
assert.ok(content.includes('Xem trước cấu trúc Word OLM'), 'Modal phải có xem trước cú pháp OLM');

console.log('✓ taobaitap.html: Đã tích hợp Tab chuyên biệt và chuẩn hóa 100% cú pháp OLM.vn!');
console.log('================================================================\n');
