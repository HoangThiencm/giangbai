const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'game-treasure.html'), 'utf8');

// 1. MathText & KaTeX
assert.match(html, /MathText/, 'game-treasure.html phải có component MathText');
assert.match(html, /vendor\/katex\.min\.js/, 'game-treasure.html phải nạp thư viện katex');

// 2. Question section above the river
const qSectionIdx = html.indexOf('📝 Câu hỏi');
const riverSectionIdx = html.indexOf('<River');
assert.ok(qSectionIdx > 0, 'Phải có phần hiển thị Câu hỏi');
assert.ok(riverSectionIdx > 0, 'Phải có canvas River');
assert.ok(qSectionIdx < riverSectionIdx, 'Bảng câu hỏi phải nằm phía TRÊN canvas River');

// 3. Short sprint & Fast start (No 3-2-1 countdown)
assert.ok(!html.includes('setCount('), 'Đã loại bỏ hoàn toàn đếm ngược 3-2-1');
assert.match(html, /whistle/, 'Có âm thanh còi xuất phát whistle');
assert.match(html, /GO!/, 'Có hiệu ứng còi GO!');
assert.match(html, /option value="3"/, 'Có tùy chọn 3 giây Siêu tốc');
assert.match(html, /option value="5"/, 'Có tùy chọn 5 giây Tiêu chuẩn');

// 4. River physics & Roles: Pack capped, only winnerId reaches finish line
assert.match(html, /winnerId/, 'Có cơ chế phân định winnerId');
assert.match(html, /topIds/, 'Có cơ chế phân định topIds');
assert.match(html, /roleOf/, 'Có hàm phân vai roleOf');
assert.match(html, /q\.cap/, 'Đàn vịt thường bị giới hạn bởi cap');
assert.match(html, /OBSTACLES/, 'Có danh sách chướng ngại vật OBSTACLES');
assert.match(html, /🍞|bread/, 'Có bánh mì');
assert.match(html, /🌀|whirl/, 'Có xoáy nước');
assert.match(html, /🚀|nitro/, 'Có nitro');
assert.match(html, /🐢|turtle/, 'Có rùa thần');

// 5. Zero-click transition & No intermediate congratulation modal blocking question
assert.ok(!html.includes('Hiện câu hỏi kiểm tra'), 'Đã bỏ nút trung gian Hiện câu hỏi kiểm tra');
assert.match(html, /XIN MỜI TRẢ LỜI/i, 'Có banner vinh danh Xin mời trả lời');

// 6. Teacher controls & Scoring
assert.match(html, /Đúng \(\+Điểm\)/, 'Có nút Đúng (+Điểm)');
assert.match(html, /Tiếp tục/, 'Có nút Tiếp tục');
assert.match(html, /Enter · Mở đáp án/, 'Có nút Mở đáp án');
assert.match(html, /Loại bạn vừa gọi/, 'Có tùy chọn Loại bạn vừa gọi');
assert.match(html, /Vịt cứu trợ \(H\)/, 'Có nút Vịt cứu trợ (phím H)');

// 7. Hotkeys
assert.match(html, /e\.code === "Space"/, 'Hỗ trợ phím Space');
assert.ok(html.includes('/^[1-4]$/.test(e.key)'), 'Hỗ trợ phím 1-4');
assert.ok(html.includes('/^[a-dA-D]$/.test(e.key)'), 'Hỗ trợ phím A-D');
assert.match(html, /e\.key === "Enter"/, 'Hỗ trợ phím Enter');
assert.match(html, /e\.key === "h" \|\| e\.key === "H"/, 'Hỗ trợ phím H');

// 8. Babel syntax compilation check
const scriptMatch = html.match(/<script type="text\/babel"[^>]*>([\s\S]*?)<\/script>/);
assert.ok(scriptMatch, 'Phải tìm thấy thẻ script type="text/babel"');
const babelSource = fs.readFileSync(path.join(root, 'vendor', 'babel.min.js'), 'utf8');
const vm = require('vm');
const sandbox = { window: {}, console: console };
vm.createContext(sandbox);
vm.runInContext(babelSource, sandbox);
assert.ok(sandbox.Babel, 'Babel phải sẵn sàng trong sandbox');
const transformed = sandbox.Babel.transform(scriptMatch[1], { presets: ['react', 'env'] });
assert.ok(transformed.code && transformed.code.length > 0, 'Babel phải biên dịch thành công không lỗi cú pháp');
console.log('Babel syntax compile check: SUCCESS (compiled ' + transformed.code.length + ' chars)');

console.log('duck-race smoke test: ALL PASS');

