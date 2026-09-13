const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

const api = fs.readFileSync(path.join(__dirname, '../api/baogiang_mail.php'), 'utf8');
const html = fs.readFileSync(path.join(__dirname, '../phancongtochuyenmon.html'), 'utf8');
const selfOnlyWarning = 'Chế độ hiện tại chỉ gửi về email cá nhân. Để gửi trực tiếp cho giáo viên, đặt BAOGIANG_GMAIL_TO_SELF_ONLY thành false trong api/config.php.';

assert.match(api, /'delivery_mode'\s*=>\s*\$selfOnly \? 'self' : 'direct'/, 'GET trạng thái phải nêu delivery_mode');
assert.match(api, /'direct_delivery'\s*=>\s*!\$selfOnly/, 'GET trạng thái phải nêu direct_delivery');
assert.match(api, /\$to = \$selfOnly \? \(string\) BAOGIANG_GMAIL_FROM : \$delivery\['to'\]/, 'backend vẫn phải giữ chốt chỉ-gửi-cho-bản-thân');
assert(api.includes('Để gửi trực tiếp cho giáo viên, đặt BAOGIANG_GMAIL_TO_SELF_ONLY thành false trong api/config.php.'), 'phản hồi backend phải chỉ rõ cách bật gửi trực tiếp');

assert.match(html, /id="email-mail-status"/, 'tab Email phải có banner trạng thái');
assert.match(html, /function loadBaoGiangMailStatus\(\)/, 'tab Email phải đọc trạng thái gửi từ backend');
assert.match(html, /fetch\('api\/baogiang_mail\.php', \{ credentials: 'include' \}\)/, 'trạng thái phải dùng GET api mail');
assert.match(html, /id="email-bg-send-teachers"/, 'nút gửi trực tiếp phải có định danh để khóa');
assert.match(html, /directButton\.disabled = !directAllowed/, 'nút gửi trực tiếp phải bị khóa khi self-only');
assert(html.includes(selfOnlyWarning), 'cảnh báo self-only phải rõ cách cấu hình');
assert.match(html, /if \(baogiangMailStatus\.loaded && !baogiangMailStatus\.direct_delivery\)/, 'hàm gửi trực tiếp phải chặn trước khi POST');
assert.match(html, /function buildTeacherBaoGiangWeekHtml\(/, 'email LBG giáo viên phải dùng mẫu riêng có cấu trúc');
assert.match(html, /Lịch được gom theo ngày; buổi sáng và buổi chiều được ngăn cách rõ ràng\./, 'mẫu LBG giáo viên phải gom theo ngày và buổi');
assert.match(html, /formatBaoGiangLessonDisplay\(row\)/, 'mẫu LBG giáo viên phải hiển thị PPCT/phân đoạn');

console.log('PASS: trạng thái gửi email, chốt self-only và mẫu LBG giáo viên.');
