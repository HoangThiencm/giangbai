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

assert.match(api, /function baogiang_send_gmail\(string \$recipient, string \$subject, string \$body, string \$html = '', string \$ics = ''\)/, 'hàm gửi mail phải nhận tệp ics');
assert.match(api, /'ics' => trim\(\(string\) \(\$item\['ics'\] \?\? ''\)\)/, 'payload deliveries phải nhận trường ics');
assert.match(api, /text\/calendar; charset=UTF-8; method=REQUEST; name=\\"lich_bao_giang\.ics\\"/, 'email có lịch phải đính kèm text/calendar method REQUEST');
assert.match(api, /Content-Disposition: attachment; filename=\\"lich_bao_giang\.ics\\"/, 'tệp lịch phải là attachment lich_bao_giang.ics');
assert.match(api, /if \(\$ics !== ''\)/, 'khi không có ics phải giữ MIME cũ');
assert.match(html, /function buildTeacherBaoGiangIcs\(/, 'trang phải tạo được chuỗi lịch .ics');
assert.match(html, /function exportCurrentBaoGiangIcs\(/, 'trang phải có hàm tải lịch tuần hiện tại');
assert.match(html, /function downloadIcsFile\(/, 'trang phải tải được file .ics trên trình duyệt');
assert.match(html, /TZID:Asia\/Ho_Chi_Minh/, 'lịch phải dùng múi giờ Asia/Ho_Chi_Minh');
assert.match(html, /TRIGGER:-PT15M/, 'mỗi tiết phải nhắc trước 15 phút');
assert.match(html, /Xuất Google Calendar \(\.ics\)/, 'giao diện phải có nút xuất Google Calendar');
assert.match(html, /Tự động đính kèm sự kiện Google Calendar \(\.ics\) trong email/, 'tab gửi email phải nói rõ lịch được đính kèm');
assert.match(html, /ics: buildTeacherBaoGiangIcs\(teacher, range, ordered, baoGiangIcsAllDay\(\)\)/, 'email lịch báo giảng phải kèm chuỗi ics theo định dạng đang chọn');

{
    const vm = require('node:vm');
    const start = html.indexOf('const BAOGIANG_PERIOD_TIMES');
    const end = html.indexOf('function downloadIcsFile');
    assert(start >= 0 && end > start, 'khối tạo .ics phải tách được để kiểm thử');
    const context = vm.createContext({ formatBaoGiangLessonDisplay: row => row.lesson?.lesson || '' });
    vm.runInContext(html.slice(start, end), context);
    const ics = vm.runInContext(`buildTeacherBaoGiangIcs({ id: 'gv1', name: 'Cô An' }, { start: '2026-09-28', end: '2026-10-04' }, [
        { date: '2026-09-28', session: 'morning', period: 1, subject: 'Toán', class_name: '6A1', lesson: { name: 'Số tự nhiên', ppct: '12' } },
        { date: '2026-09-29', session: 'afternoon', period: 8, subject: 'Toán', class_name: '7A1', lesson: { lesson: 'Phân số', ppct: '20' } },
        { date: '2026-09-30', session: 'afternoon', period: 10, subject: 'Toán', class_name: '8A1', lesson: { ppct: '30' } }
    ], false)`, context);
    assert.match(ics, /BEGIN:VCALENDAR/);
    assert.match(ics, /METHOD:REQUEST/);
    assert.match(ics, /TZID:Asia\/Ho_Chi_Minh/);
    assert.match(ics, /DTSTART;TZID=Asia\/Ho_Chi_Minh:20260928T071500/);
    assert.match(ics, /DTEND;TZID=Asia\/Ho_Chi_Minh:20260928T080000/);
    assert.match(ics, /DTSTART;TZID=Asia\/Ho_Chi_Minh:20260929T152000/);
    assert.match(ics, /DTEND;TZID=Asia\/Ho_Chi_Minh:20260929T160500/);
    assert.match(ics, /DTSTART;TZID=Asia\/Ho_Chi_Minh:20260930T170000/);
    assert.match(ics, /DTEND;TZID=Asia\/Ho_Chi_Minh:20260930T174500/);
    assert.match(ics, /SUMMARY:Buổi sáng/);
    assert.match(ics, /SUMMARY:Buổi chiều/);
    assert.match(ics, /BUỔI SÁNG:/);
    assert.match(ics, /- Tiết 1: Toán 6A1 \| Số tự nhiên \(12\)/);
    assert.match(ics, /UID:baogiang-gv1-2026-09-28-morning@giangbai/);
    assert.match(ics, /LOCATION:Lớp 6A1/);
    assert.match(ics, /TRIGGER:-PT15M/);
    assert.match(ics, /Giáo viên: Cô An/);
    assert.equal((ics.match(/BEGIN:VEVENT/g) || []).length, 3);
}

console.log('PASS: trạng thái gửi email, chốt self-only, mẫu LBG giáo viên và tệp lịch .ics.');
