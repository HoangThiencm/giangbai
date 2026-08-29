/** Static smoke test for the self-contained 5512 lesson-plan tab. Node 18+. */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'backupcode viettailieu', 'soanbaigemini.html'), 'utf8');
const checks = [
    ['named plan tab', /id="lesson-tab-plan"[^>]*[\s\S]*?Soạn giáo án/.test(html)],
    ['image and PDF input', /accept="image\/\*,application\/pdf,\.pdf"/.test(html)],
    ['PDF file picker button', /Chọn ảnh hoặc PDF từ máy/.test(html)],
    ['PDF preview in soạn bài', /function addLessonInputPreview[\s\S]*?application\/pdf[\s\S]*?PDF đã nhận/.test(html)],
    ['PDF sent with lesson Gemini call', html.includes('application\\/pdf));base64')],
    ['PDF clipboard branch', /items\[i\]\.type === 'application\/pdf'[\s\S]*?addLessonPlanFiles\(\[pdfFile\]\)/.test(html)],
    ['source caps', /LESSON_PLAN_MAX_FILES\s*=\s*12/.test(html) && /LESSON_PLAN_MAX_TOTAL_BYTES/.test(html)],
    ['single requested model', /const LESSON_PLAN_MODEL = 'gemini-3-flash-preview'/.test(html)],
    ['no plan fallback', /async function callLessonPlanGemini[\s\S]*?postCanvasGeminiGenerate\(LESSON_PLAN_MODEL/.test(html)],
    ['configuration and direct text input', /lesson-plan-teacher/.test(html) && /lesson-plan-school/.test(html) && /lesson-plan-book/.test(html) && /lesson-plan-material-text/.test(html)],
    ['optional integrations', /plan-opt-digital/.test(html) && /plan-opt-ai/.test(html) && /plan-opt-active/.test(html) && /plan-opt-game/.test(html) && /plan-opt-defense/.test(html) && /plan-opt-disability/.test(html) && /plan-opt-questions/.test(html) && /plan-opt-stem/.test(html)],
    ['5512 validator', /function validateLessonPlan/.test(html) && /LESSON_PLAN_STEP_NAMES/.test(html)],
    ['UNESCO groups and levels', /UNESCO_AI_GROUPS/.test(html) && /\['Hiểu', 'Vận dụng', 'Tạo'\]/.test(html)],
    ['two-column Word export', /Hoạt động của giáo viên/.test(html) && /Hoạt động của học sinh/.test(html)],
    ['sandbox message', /Gemini Canvas chặn tải file Word/.test(html)],
    ['ví dụ quét toàn diện SGK', /function buildRemainingSectionsPrompt[\s\S]*QUÉT TOÀN DIỆN SGK[\s\S]*3–5 dạng đặc trưng/.test(html)],
    ['ví dụ 3 thành phần dạng toán', /function buildRemainingSectionsPrompt[\s\S]*PHƯƠNG PHÁP GIẢI[\s\S]*VÍ DỤ MẪU/.test(html)],
    ['tự luận 5 câu phân hóa trong prompt', /function buildRemainingSectionsPrompt[\s\S]*Câu 1 Nhận biết[\s\S]*Câu 5 Vận dụng thực tế/.test(html)],
    ['hợp đồng format khóa 5 câu tự luận', /BÀI TẬP TỰ LUẬN NGẮN:[\s\S]*ĐÚNG 5 DÒNG[\s\S]*Câu 1: Nhận biết/.test(html)],
    ['gợi ý sư phạm không đối phó', /CẤM gợi ý đối phó[\s\S]*Tính cẩn thận/.test(html)],
    ['bài tập bám kỹ năng cần đạt', /tương ứng trực tiếp với 1 kỹ năng trong KỸ NĂNG CẦN ĐẠT/.test(html)],
    ['validator chặn tự luận dưới 5 câu', /essayList\.length < 5[\s\S]*phải đủ đúng 5 câu phân hóa/.test(html)],
    ['repair bổ sung đủ 5 câu tự luận', /function buildFormatRepairPrompt[\s\S]*Nếu TỰ LUẬN dưới 5 câu[\s\S]*Câu 5 Vận dụng thực tế/.test(html)],
    ['giữ lọc đáp án số tự luận', /isLotrinhEssayNumericAnswer/.test(html)],
    ['Bước 1 khóa HINH_01 HINH_02', /function buildTheoryPhasePrompt[\s\S]*KHÓA MÃ HÌNH BƯỚC 1[\s\S]*HINH_01[\s\S]*HINH_02/.test(html)],
    ['Bước 2 tiếp nối HINH_03', /function buildRemainingSectionsPrompt[\s\S]*KHÓA MÃ HÌNH BƯỚC 2[\s\S]*HINH_03/.test(html)],
    ['inventory tự tạo prompt khi thiếu danh sách hình', /function buildLessonImageInventory[\s\S]*buildFallbackPromptFromContext[\s\S]*autoFilled/.test(html)],
    ['card tạo ảnh prompt tùy chọn', /id="custom-image-tool-card"/.test(html) && /Tạo ảnh từ Prompt \/ Mô tả tùy chọn/.test(html)],
    ['nút tạo ảnh ngay', /id="custom-image-generate-btn"[\s\S]*Tạo ảnh ngay/.test(html)],
    ['chèn HINH_CUSTOM vào bài', /HINH_CUSTOM_/.test(html) && /function insertCustomImageIntoLesson/.test(html)],
    ['tải PNG và copy data URL', /id="custom-image-download-btn"/.test(html) && /id="custom-image-copy-btn"/.test(html)]
];

let failed = 0;
for (const [name, ok] of checks) {
    console[ok ? 'log' : 'error']((ok ? 'OK: ' : 'FAIL: ') + name);
    if (!ok) failed += 1;
}

// Compile every inline script without executing browser-dependent code.
const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(match => match[1]);
try {
    scripts.forEach((script, index) => new vm.Script(script, { filename: `soanbaigemini-inline-${index}.js` }));
    console.log('OK: inline JavaScript syntax');
} catch (error) {
    console.error('FAIL: inline JavaScript syntax', error.message);
    failed += 1;
}
process.exitCode = failed ? 1 : 0;
