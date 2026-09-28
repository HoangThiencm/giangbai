/** Smoke: đề tạo lần 2 phải khác lần 1 nhờ generationConfig và prompt chống trùng. */
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'taobaitap.html'), 'utf8');

assert.match(html, /const generationConfig = options\.generationConfig \|\| \{ temperature: 0\.85, topP: 0\.95 \}/, 'callGeminiParts phải có generationConfig mặc định');
assert.match(html, /bodyPayload\.generationConfig = generationConfig/, 'payload Gemini phải gửi generationConfig');
assert.match(html, /const variantNonce = Math\.random\(\)\.toString\(36\)\.substring\(2, 7\)\.toUpperCase\(\)/, 'generateContent phải có mã biến thể ngẫu nhiên');
assert.match(html, /let antiDuplicationPrompt = ''/, 'generateContent phải dựng antiDuplicationPrompt');
assert.match(html, /CÁC CÂU HỎI ĐÃ TẠO Ở LẦN TRƯỚC \(CẦN TRÁNH TRÙNG LẶP\)/, 'prompt phải liệt kê câu đã tạo');
assert.match(html, /BẮT BUỘC: Bạn PHẢI tạo ra bộ câu hỏi MỚI HOÀN TOÀN/, 'prompt phải cấm lặp bộ câu cũ');
assert.match(html, /QUY TẮC ĐA DẠNG HÓA & ĐỔI MỚI BÀI TẬP \(Mã đề #\$\{variantNonce\}\)/, 'prompt phải có quy tắc đổi mới đề');
assert.match(html, /generationConfig: \{ temperature: 0\.9, topP: 0\.95 \}/, 'generateContent phải gọi API với temperature 0.9');
assert.match(html, /Đã bật chế độ tự động làm mới đề & chống trùng lặp câu hỏi giữa các lần tạo\./, 'giao diện phải báo chế độ chống trùng');

const scriptMatch = html.match(/<script type="text\/babel"[^>]*>([\s\S]*?)<\/script>/);
assert.ok(scriptMatch, 'phải có script Babel của taobaitap');
const babelSource = fs.readFileSync(path.join(root, 'vendor', 'babel.min.js'), 'utf8');
const sandbox = { window: {}, console };
vm.createContext(sandbox);
vm.runInContext(babelSource, sandbox);
assert.ok(sandbox.Babel, 'Babel phải sẵn sàng');
const transformed = sandbox.Babel.transform(scriptMatch[1], { presets: ['react', 'env'] });
assert.ok(transformed.code && transformed.code.length > 0, 'Babel phải biên dịch taobaitap không lỗi cú pháp');

console.log('PASS: generationConfig, prompt chống trùng và cú pháp Babel của taobaitap.');
