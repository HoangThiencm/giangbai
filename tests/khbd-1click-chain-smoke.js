'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

console.log('================================================================');
console.log('KIỂM THỬ: XÁC NHẬN ĐÃ GỠ BỎ 1-CLICK & HỖ TRỢ SOẠN THEO TAB ĐỘC LẬP');
console.log('================================================================');

// 1. Kiểm tra trong soankhbd.html
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'soankhbd.html'), 'utf8');

assert.ok(!html.includes('id="btn1ClickGenerate"'), 'Nút btn1ClickGenerate phải được xóa khỏi soankhbd.html');
assert.ok(!html.includes('TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)'), 'Không còn chuỗi 1-CLICK trong HTML');
assert.ok(html.includes('Chuyển sang các <b>Tab 2, 3, 4</b> để tạo từng phần giáo án'), 'Hướng dẫn Bước 4 phải hướng dẫn sang Tab 2, 3, 4');
assert.ok(html.includes('Chưa có nội dung giáo án. Hãy tạo nội dung ở các Tab 2, 3, 4!'), 'Preview giáo án rỗng phải hướng dẫn tạo ở Tab 2, 3, 4');
assert.ok(html.includes('id="btnCancelGeneration"'), 'Nút btnCancelGeneration vẫn được giữ nguyên');

console.log('✓ HTML đã được làm sạch và cập nhật hướng dẫn đúng chuẩn.');

// 2. Kiểm tra trong js/khbd-app.js
const appExports = require('../js/khbd-app.js');

assert.strictEqual(appExports.handle1ClickGenerate, undefined, 'handle1ClickGenerate không còn export');
assert.strictEqual(appExports.generateOneClickContent, undefined, 'generateOneClickContent không còn export');

console.log('✓ Module exports đã loại bỏ sạch các hàm 1-click.');

console.log('\n================================================================');
console.log('🎉 KIỂM THỬ GỠ BỎ 1-CLICK ĐÃ PASS 100%!');
console.log('================================================================\n');
