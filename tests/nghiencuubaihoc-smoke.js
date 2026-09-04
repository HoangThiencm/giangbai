const fs = require('fs');
const assert = require('assert');
const path = require('path');

const root = path.join(__dirname, '..');
const read = (...parts) => fs.readFileSync(path.join(root, ...parts), 'utf8');
const html = read('nghiencuubaihoc.html');
const api = read('api', 'nghiencuubaihoc.php');
const index = read('index.html');
const admin = read('admin.html');
const has = (source, value, label = value) => assert(source.includes(value), `Missing: ${label}`);

has(index, "nghiencuubaihoc: 'nghiencuubaihoc.html'");
has(index, 'data-tool="nghiencuubaihoc"');
has(index, 'href="nghiencuubaihoc.html"');
has(index, 'tool-tile--nghiencuubaihoc');
has(index, 'fa-users-rectangle');
has(index, 'Chu trình NCBH sư phạm');
has(index, 'Nghiên cứu bài học AI');
has(index, '12 bước NCBH có hỗ trợ AI · KHBD 2 lớp · Phân tích minh chứng · Cải tiến bài học');

has(admin, 'id="cfg_nghiencuubaihoc"');
has(admin, "'nghiencuubaihoc'");
has(admin, "nghiencuubaihoc: { title: 'Nghiên cứu bài học AI', url: 'nghiencuubaihoc.html' }");
assert(/const CLIENT_FEATURE_CHECKS = \[[\s\S]*?'nghiencuubaihoc'/.test(admin), 'CLIENT_FEATURE_CHECKS includes nghiencuubaihoc');
assert(/const USER_FEATURE_GROUPS = \[[\s\S]*?ids: \[[^\]]*'nghiencuubaihoc'/.test(admin), 'USER_FEATURE_GROUPS includes nghiencuubaihoc');
assert(/const teacherFeatureGroups = \[[\s\S]*?pages: \[[^\]]*'nghiencuubaihoc'/.test(admin), 'teacherFeatureGroups includes nghiencuubaihoc');

['js/security-guard.js', 'access-control.js', 'mistral-ocr-client.js', 'js/khbd-yccd.js', 'js/khbd-standards.js', 'tailwindcss', 'font-awesome/6', 'Plus Jakarta Sans', 'pdf.js', 'mammoth', 'docx@8.5.0', 'FileSaver', 'jszip'].forEach(x => has(html, x));

const stepTitles = ['Khởi tạo hồ sơ', 'Nghiên cứu văn bản và phân tích bài học', 'Đánh giá giáo án hiện có', 'Xác định vấn đề nghiên cứu', 'Dự kiến quá trình học của HS', 'Xây dựng bài dạy minh họa (KHBD Phiên bản 1)', 'Xây dựng kế hoạch quan sát và hồ sơ trước giờ dạy', 'Dạy minh họa và thu thập minh chứng', 'AI phân tích sau giờ dạy', 'Thảo luận và xây dựng biên bản sau tiết dạy', 'Điều chỉnh bài học (KHBD Phiên bản 2)', 'Hoàn thiện hồ sơ NCBH'];
stepTitles.forEach(x => has(html, x));
assert.strictEqual(stepTitles.length, 12, '12 NCBH steps');

['Căn cứ', 'AI phân tích', 'GV cần làm', 'HS dự kiến làm', 'Cần quan sát / thu thập', 'Sản phẩm của bước'].forEach(x => has(html, x));

['Document Analyzer', 'Lesson Analyzer', 'Lesson Plan Reviewer', 'Research Question Advisor', 'Student Thinking Predictor', 'Lesson Adaptation Advisor', 'Observation Designer', 'Evidence Analyzer', 'Discussion Assistant', 'Minutes Generator', 'Lesson Reviser', 'Report Generator'].forEach(x => has(html, x));

['syncUserKeysFromServer', 'api/user_gemini_keys.php', "credentials: 'include'", "cache: 'no-store'", 'mistral_keys', 'global_gemini_keys', 'global_mistral_keys', "localStorage.getItem('khbd_gemini_model')", "localStorage.getItem('default_gemini_module')", 'gemini-2.5-flash', '429', '503', 'Timeout', 'callGemini', 'callMistral', 'MistralOcr'].forEach(x => has(html, x));

['Lớp 1', 'Lớp 2', 'Giữ nguyên', 'Giữ nhưng bổ sung', 'Cần điều chỉnh', 'Nên thiết kế lại', 'Trước → Vấn đề → Minh chứng → Đề xuất sửa → Lý do sửa', 'AI chỉ đề xuất, GV quyết định', 'Không tạo biên bản giả mạo', 'không xếp loại giáo viên', 'saveSession', 'loadSessions', 'loadSessionById', 'deleteSession', 'session_data', 'currentSessionId', 'ncbh_autosave', 'exportOneDocx', 'exportAllDocx', 'exportZip', 'Lưu CSDL', 'Mở hồ sơ cũ'].forEach(x => has(html, x));

PRODUCTS_13_TITLES().forEach(x => has(html, x));

['$_SESSION[\'user_id\']', 'nghien_cuu_bai_hoc_sessions', 'LONGTEXT', 'mon_hoc', 'lop', 'bai_hoc', 'bo_sgk', 'gv_day', 'session_title', 'current_step', 'session_data', "action === 'list'", "action === 'delete'", 'user_id'].forEach(x => assert(api.includes(x), `API missing ${x}`));

const inlineScripts = html.match(/<script>([\s\S]*?)<\/script>/g) || [];
assert(inlineScripts.length >= 1, 'inline application script missing');
inlineScripts.forEach((block, i) => {
    const inner = block.replace(/^<script>/, '').replace(/<\/script>$/, '');
    assert(!inner.includes('</script>'), `inline script ${i} must not contain nested </script>`);
});

has(read('access-control.js'), "'nghiencuubaihoc.html': 'nghiencuubaihoc'");
has(read('api', 'helpers.php'), "'nghiencuubaihoc'");
has(read('global_config.json'), '"nghiencuubaihoc": true');

['marked/marked.min.js', 'marked.parse', 'fallbackMarkdown', 'renderMarkdown', 'showAi', 'setAiProgress', 'aiProgressBar', 'aiProgressWrap', 'aiProgressContainer', 'aiProgressStatus', 'aiProgressLabel', 'aiProgressPercent', 'prose prose-sm max-w-none text-slate-800'].forEach(x => has(html, x));
has(html, 'Chuẩn bị dữ liệu và trích xuất ngữ cảnh');
has(html, 'Kết nối và gửi prompt tới mô hình AI Gemini / Mistral');
has(html, 'Phân tích sư phạm chuyên sâu và nhận phản hồi');
has(html, 'Hoàn tất xử lý và hiển thị kết quả');
has(html, 'function documentAnalyzerContext');
has(html, 'ĐÃ ĐỦ ĐIỀU KIỆN TIẾN HÀNH NGHIÊN CỨU BÀI HỌC');
has(html, '✓ HỒ SƠ ĐÃ ĐỦ ĐIỀU KIỆN ĐỂ TIẾP TỤC');
has(html, 'showReadyBadge');
has(html, 'CẤM đòi hỏi Câu hỏi nghiên cứu');
has(html, 'CẤM đòi hỏi YCCĐ');
has(html, 'Tùy chọn');
assert(html.includes("runAiTask('Document Analyzer'") && html.includes('documentAnalyzerContext'), 'Document Analyzer uses dedicated step-1 context');
assert(!/runDocumentAnalyzer[\s\S]{0,800}lessonContext\(\)/.test(html), 'Document Analyzer must not send full lessonContext');

has(html, '<select id="fMon"');
has(html, '<select id="fLop"');
has(html, '<select id="fSgk"');
assert(!html.includes('<input id="fMon"'), 'fMon must not remain a text input');
assert(!html.includes('<input id="fLop"'), 'fLop must not remain a text input');
assert(!html.includes('<input id="fSgk"'), 'fSgk must not remain a text input');
['SUBJECT_OPTIONS', 'GRADE_OPTIONS', 'SGK_OPTIONS', 'normalizeSubject', 'normalizeGrade', 'optionList'].forEach(x => has(html, x));
['Toán học', 'Tin học', 'Khoa học tự nhiên', 'Ngữ văn', 'Tiếng Anh', 'Lịch sử và Địa lí', 'Giáo dục công dân', 'Công nghệ', 'Hoạt động trải nghiệm, hướng nghiệp'].forEach(x => has(html, x));
['Lớp 6', 'Lớp 7', 'Lớp 8', 'Lớp 9', 'Lớp 4', 'Lớp 5', 'Lớp 10', 'Lớp 11', 'Lớp 12'].forEach(x => has(html, x));
['Kết nối tri thức với cuộc sống', 'Chân trời sáng tạo', 'Cánh diều', 'Cùng khám phá', 'SGK hiện hành khác'].forEach(x => has(html, x));
has(html, 'Kết nối tri thức');
has(html, "compact === 'toán'");

console.log('nghiencuubaihoc smoke: index/admin integration, 12 steps, 6 zones, 12 AI tasks, key sync, progress bar, markdown, step-1 readiness, subject/grade/sgk selects passed');

function PRODUCTS_13_TITLES() {
    return [
        'Hồ sơ khởi tạo NCBH',
        'Phiếu phân tích bài học',
        'Báo cáo phân tích giáo án ban đầu',
        'Vấn đề/câu hỏi nghiên cứu chính thức',
        'Bảng dự kiến hoạt động và phản ứng của HS',
        'KHBD minh họa - phiên bản 1',
        'Phiếu quan sát học sinh',
        'Phiếu dự giờ NCBH',
        'Biên bản xây dựng bài học',
        'Kho minh chứng tiết dạy',
        'Báo cáo phân tích tiết dạy',
        'Biên bản phân tích bài học sau tiết dạy',
        'KHBD minh họa - phiên bản 2'
    ];
}
