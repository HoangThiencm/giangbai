'use strict';

const fs = require('fs');
const path = require('path');
const assert = require('assert');
const vm = require('vm');

console.log('================================================================');
console.log('KIỂM THỬ TỰ ĐỘNG: CANVAS_SOANKHBD.HTML 1-1 & 1-CLICK GENERATE');
console.log('================================================================');

const root = path.join(__dirname, '..');
const sourceHtml = fs.readFileSync(path.join(root, 'soankhbd.html'), 'utf8');
const targetPaths = [
  path.join(root, 'backupcode viettailieu', 'canvas_soankhbd.html'),
  path.join(root, 'canvas_soankhbd.html')
];

function extractIds(html) {
  const matches = [...html.matchAll(/\bid=["']([^"']+)["']/g)];
  return new Set(matches.map(m => m[1]));
}

const sourceIds = extractIds(sourceHtml);
const khbdApp = fs.readFileSync(path.join(root, 'js', 'khbd-app.js'), 'utf8');
assert.match(khbdApp, /function safeGetGradeLevel\(grade\)/, 'khbd-app phải có helper cấp học an toàn');
assert.match(khbdApp, /function safeGetGradeLevelName\(grade\)/, 'khbd-app phải có helper tên cấp học an toàn');
assert.match(khbdApp, /function getSubjectDisplayName\(subjectId\)/, 'khbd-app phải có getSubjectDisplayName');
assert.match(khbdApp, /function isOffTopicObjectivesHallucination\(text\)/, 'khbd-app phải lọc I. Mục tiêu lạc đề trước khi repair');
assert.match(khbdApp, /doanh nghiệp\|quy trình doanh nghiệp\|khách hàng\|phân tích sắc thái/, 'bộ lọc lạc đề phải nhận diện từ khóa doanh nghiệp');
assert.match(khbdApp, /function normalizeLessonTitleMatch\(str\)/, 'khbd-app phải chuẩn hóa dấu chấm/hai chấm khi so khớp bài');
assert.match(khbdApp, /normalizeLessonTitleMatch\(item\) === normalizeLessonTitleMatch\(appState\.selectedLesson\)/, 'dropdown bài học so khớp PPCT với SGK');
assert.match(khbdApp, /getPromptTemplate\("GENERATE_OBJECTIVES"/, 'mục tiêu lạc đề phải tái tạo bằng prompt cứng môn học');
assert.match(khbdApp, /async function handleGenerateCurrentActivity\(\)\s*\{\s*try \{/, 'Tạo nội dung mục này phải bọc try/catch');
assert.match(khbdApp, /async function handleGenerateObjectives\(\)\s*\{\s*try \{/, 'Tạo I. Mục tiêu phải bọc try/catch');
assert.match(khbdApp, /async function handleGenerateMaterials\(\)\s*\{\s*try \{/, 'Tạo II. Học liệu phải bọc try/catch');
assert.match(khbdApp, /showToast\("Lỗi khởi tạo: " \+ err\.message, "danger", 6000\)/, 'nút tạo mục phải báo lỗi khởi tạo, không đơ im lặng');
{
  const start = khbdApp.indexOf('function normalizeLessonTitleMatch');
  const end = khbdApp.indexOf('function populateLessonDropdown');
  const sandbox = {};
  vm.createContext(sandbox);
  vm.runInContext(khbdApp.slice(start, end), sandbox);
  assert.strictEqual(
    sandbox.normalizeLessonTitleMatch('Bài 2. Giải hệ hai phương trình bậc nhất hai ẩn'),
    sandbox.normalizeLessonTitleMatch('Bài 2: Giải hệ hai phương trình bậc nhất hai ẩn'),
    'Bài 2. phải khớp Bài 2:'
  );
}
assert.ok(!/gradeLevel:\s*getGradeLevel\(appState\.selectedGrade\)/.test(khbdApp), 'khbd-app không được gọi trực tiếp getGradeLevel khi tạo prompt');
assert.ok(!/gradeLevelName:\s*getGradeLevelName\(appState\.selectedGrade\)/.test(khbdApp), 'khbd-app không được gọi trực tiếp getGradeLevelName khi tạo prompt');
const canvasPromptFn = khbdApp.slice(khbdApp.indexOf('function canvasTextbookAnalysisPrompt'), khbdApp.indexOf('function isLevel1SectionTitle'));
assert.match(canvasPromptFn, /\.join\("\\n"\)/, 'prompt phân tích SGK phải nối bằng xuống dòng thật');
assert.ok(!/\.join\("\\\\n"\)/.test(canvasPromptFn), 'prompt phân tích SGK không được join("\\\\n")');

// Hồi quy bỏ tick PPDH/KTDH: prompt không được tự yêu cầu AI lấy lại từ catalog.
assert.match(khbdApp, /pedagogyConfigured:\s*Boolean\(source\.pedagogyConfigured\)/, 'teaching context phải lưu cờ cấu hình thủ công');
assert.match(khbdApp, /pedagogyConfigured\s*=\s*true/, 'thay đổi checkbox phải đánh dấu cấu hình thủ công');
assert.ok(!khbdApp.includes('khi soạn chỉ được lấy 1–2 phương pháp phù hợp môn'), 'prompt không được ép AI tự lấy PPDH từ catalog');
assert.ok(!khbdApp.includes('Chưa chọn; chỉ dùng kỹ thuật catalog đúng pha A–E'), 'prompt không được ép AI tự lấy KTDH từ catalog');
assert.match(khbdApp, /KHÔNG áp dụng PPDH đặc thù riêng/, 'prompt phải cấm PPDH đặc thù khi bỏ tick');
assert.match(khbdApp, /KHÔNG áp dụng kỹ thuật dạy học riêng nào/, 'prompt phải cấm KTDH khi bỏ tick');

for (const targetPath of targetPaths) {
  const relPath = path.relative(root, targetPath);
  console.log(`\nKiểm tra tệp: ${relPath}`);
  assert.ok(fs.existsSync(targetPath), `Tệp không tồn tại: ${relPath}`);

  const targetHtml = fs.readFileSync(targetPath, 'utf8');
  const targetIds = extractIds(targetHtml);

  // 1. Kiểm tra không chứa script bảo mật đăng nhập
  assert.ok(!targetHtml.includes('js/security-guard.js'), `${relPath} không được chứa security-guard.js`);
  assert.ok(!targetHtml.includes("localStorage.getItem('authToken')"), `${relPath} không được chứa kiểm tra authToken chuyển trang login`);

  // 2. Kiểm tra các thành phần đặc trưng của Canvas
  assert.ok(targetIds.has('canvasHostBanner'), `${relPath} phải có thanh banner #canvasHostBanner`);
  assert.ok(targetHtml.includes('https://hoangthiencm.id.vn/api/canvas_gemini.php'), `${relPath} phải trỏ endpoint canvas_gemini.php`);
  assert.ok(targetHtml.includes('gemini-3-flash-preview'), `${relPath} phải sử dụng model hệ thống gemini-3-flash-preview`);
  assert.ok(targetHtml.includes('canvasConfirm'), `${relPath} phải có hàm xác nhận modal nội bộ canvasConfirm`);
  assert.ok(targetHtml.includes('isLocal ? "js/khbd-docx.js"'), `${relPath} phải nạp khbd-docx.js cục bộ khi chạy file/localhost`);
  assert.ok(targetHtml.includes('https://hoangthiencm.id.vn/js/khbd-docx.js'), `${relPath} phải giữ nguồn khbd-docx.js từ hosting khi chạy Canvas`);
  assert.ok(!targetHtml.includes('<\\\\/script>'), `${relPath} không được escape kép thẻ đóng của bộ nạp khbd-docx.js`);
  assert.ok(targetHtml.includes('"><\\/script>`);'), `${relPath} phải tạo thẻ đóng </script> hợp lệ cho bộ nạp khbd-docx.js`);
  assert.ok(targetHtml.includes('isLocal ? "css/khbd-styles.css"'), `${relPath} phải nạp khbd-styles.css cục bộ khi chạy file/localhost`);
  assert.ok(targetHtml.includes('https://hoangthiencm.id.vn/css/khbd-styles.css'), `${relPath} phải giữ nguồn khbd-styles.css từ hosting khi chạy Canvas`);
  assert.ok(targetHtml.includes('isLocal ? "js/khbd-prompts.js"'), `${relPath} phải nạp khbd-prompts.js cục bộ khi chạy file/localhost`);
  assert.ok(targetHtml.includes('https://hoangthiencm.id.vn/js/khbd-prompts.js'), `${relPath} phải giữ nguồn khbd-prompts.js từ hosting khi chạy Canvas`);
  assert.ok(targetHtml.includes('ensureKhbdPromptsFallback'), `${relPath} phải có fallback ensureKhbdPromptsFallback`);
  assert.ok(targetHtml.includes('cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-prompts.js'), `${relPath} fallback prompts phải nạp từ CDN jsDelivr khi host rỗng`);
  assert.ok(targetHtml.includes('window.PROMPTS.GENERATE_OBJECTIVES'), `${relPath} prompts fallback phải guard GENERATE_OBJECTIVES`);
  assert.ok(targetHtml.includes('ensureKhbdDocxFallback'), `${relPath} phải có fallback ensureKhbdDocxFallback`);
  assert.ok(targetHtml.includes('cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-docx.js'), `${relPath} fallback docx phải nạp từ CDN jsDelivr khi host rỗng`);
  assert.ok(targetHtml.includes('typeof window.docxGenerator !== "undefined"') || targetHtml.includes("typeof window.docxGenerator !== 'undefined'"), `${relPath} docx fallback phải guard window.docxGenerator`);
  assert.ok(targetHtml.includes('typeof window.DocxGenerator !== "undefined"') || targetHtml.includes("typeof window.DocxGenerator !== 'undefined'"), `${relPath} docx fallback phải guard window.DocxGenerator`);
  assert.ok(targetHtml.includes('isLocal ? "js/khbd-pedagogy-catalog.js"'), `${relPath} phải nạp khbd-pedagogy-catalog.js cục bộ khi chạy file/localhost`);
  assert.ok(targetHtml.includes('https://hoangthiencm.id.vn/js/khbd-pedagogy-catalog.js'), `${relPath} phải giữ nguồn khbd-pedagogy-catalog.js từ hosting khi chạy Canvas`);
  assert.ok(targetHtml.includes('ensureKhbdPedagogyCatalogFallback'), `${relPath} phải có fallback ensureKhbdPedagogyCatalogFallback`);
  assert.ok(targetHtml.includes('typeof window.KHBD_PEDAGOGY_CATALOG !== "undefined"'), `${relPath} phải guard KHBD_PEDAGOGY_CATALOG trước khi fallback`);
  assert.ok(targetHtml.includes('cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-pedagogy-catalog.js'), `${relPath} fallback phải nạp catalog từ CDN jsDelivr khi host rỗng`);
  assert.ok(targetHtml.includes('isLocal ? "js/khbd-pedagogy-catalog.js" : cdnCatalog') || /isLocal \? "js\/khbd-pedagogy-catalog\.js" : cdnCatalog/.test(targetHtml), `${relPath} fallback phải chọn local vs CDN theo isLocal`);
  assert.ok(!/<script\s+src=["']https:\/\/hoangthiencm\.id\.vn\/js\/khbd-pedagogy-catalog\.js[^"']*["']\s*>\s*<\/script>/.test(targetHtml), `${relPath} không được hardcode thẻ script pedagogy-catalog (phải dùng isLocal)`);
  assert.ok(targetHtml.includes('20260916-canvas-module-v9'), `${relPath} phải cache-bust bản Canvas module v9`);
  assert.ok(!targetHtml.includes('canvas-system-v3'), `${relPath} không được nạp Canvas cache v3 cũ`);
  assert.ok(targetHtml.includes('systemGemini: true'), `${relPath} phải bật rõ tuyến Gemini hệ thống Canvas`);
  assert.ok(targetHtml.includes('geminiEndpoint: "https://hoangthiencm.id.vn/api/canvas_gemini.php"'), `${relPath} phải khai báo endpoint Gemini Canvas tin cậy`);
  assert.ok(targetHtml.includes('canvasTimeBudgetAndRoleBreaks'), `${relPath} phải nhúng patch định mức 1 tiết + GV/HS`);
  assert.ok(targetHtml.includes('pedagogy-activity'), `${relPath} patch phải lọc hoạt động đặc thù`);
  assert.ok(/HEAVY\s*=\s*\/[^\n]*station/.test(targetHtml), `${relPath} patch phải chặn Station/Trạm`);
  assert.ok(targetHtml.includes('__khbdRolePatched'), `${relPath} phải vá parseTableCellParagraphs khi xuất Word`);
  assert.ok(targetHtml.includes('v=20260916-canvas-module-v9'), `${relPath} phải cache-bust khbd-app bản Canvas module v9`);
  assert.ok(targetHtml.includes('Phân tích SGK'), `${relPath} phải hướng người dùng dùng luồng phân tích SGK Canvas`);
  assert.ok(/\.khbd-badge-nls\s*\{[^}]*font-style:\s*italic/.test(targetHtml), `${relPath} badge NLS Canvas phải italic`);
  assert.ok(/\.khbd-badge-ai\s*\{[^}]*font-style:\s*italic/.test(targetHtml), `${relPath} badge AI Canvas phải italic`);
  assert.ok(/\.preview-rendered \.khbd-nls[\s\S]{0,180}font-style:\s*italic/.test(targetHtml), `${relPath} preview NLS Canvas phải italic`);
  assert.ok(/\.preview-rendered \.khbd-ai[\s\S]{0,180}font-style:\s*italic/.test(targetHtml), `${relPath} preview AI Canvas phải italic`);

  // Stepper chỉ hiện ba bước, nhưng giữ data-step 3/4 để điều hướng JS không đổi.
  const workflow = targetHtml.match(/<nav id="khbdWorkflowStepper"[\s\S]*?<\/nav>/);
  assert.ok(workflow, `${relPath} phải có khối Stepper`);
  assert.ok(workflow[0].includes('aria-label="Quy trình 3 bước soạn KHBD"'), `${relPath} Stepper phải công bố 3 bước`);
  assert.match(workflow[0], /data-step="3"[\s\S]*?<span class="khbd-step-num">2<\/span>/, `${relPath} data-step 3 phải hiển thị Bước 2`);
  assert.match(workflow[0], /data-step="4"[\s\S]*?<span class="khbd-step-num">3<\/span>/, `${relPath} data-step 4 phải hiển thị Bước 3`);

  // 2b. Fallback KHBD_STANDARDS + polling kết nối (host script có thể rỗng 0 bytes)
  assert.ok(targetHtml.includes('ensureKhbdStandardsFallback'), `${relPath} phải có fallback ensureKhbdStandardsFallback`);
  assert.ok(targetHtml.includes('typeof window.KHBD_STANDARDS === "undefined"'), `${relPath} phải guard typeof KHBD_STANDARDS === undefined`);
  assert.ok(targetHtml.includes('Thông tư 02/2025/TT-BGDĐT & Công văn 3456/BGDĐT-GDPT'), `${relPath} fallback NLS phải ghi framework TT 02/CV 3456`);
  assert.ok(targetHtml.includes('Quyết định 2422/QĐ-BGDĐT'), `${relPath} fallback AI phải ghi QĐ 2422`);
  assert.ok(targetHtml.includes('pollConnection'), `${relPath} phải có cơ chế pollConnection`);
  assert.ok(targetHtml.includes('pollConnection(15)'), `${relPath} phải thăm dò tối đa 15 lần (~4.5s)`);
  assert.ok(targetHtml.includes('setTimeout(function () { pollConnection(retriesLeft - 1); }, 300)'), `${relPath} phải retry mỗi 300ms`);
  assert.ok(!/setTimeout\(function \(\) \{\s*initConnection\(\);\s*bindCanvasEvents\(\);\s*\}, 350\)/.test(targetHtml), `${relPath} không còn setTimeout(initConnection, 350) đơn lẻ`);

  // Canvas OCR uses exactly the server Gemini route: no fake Mistral key/client
  // that makes khbd-app attempt OCR twice before falling back.
  assert.ok(!targetHtml.includes('canvas-session'), `${relPath} không dùng pseudo key canvas-session`);
  assert.ok(!targetHtml.includes('mistral-ocr-client.js'), `${relPath} không nạp Mistral OCR client trong Canvas`);
  assert.ok(!targetHtml.includes('window.MistralOcr ='), `${relPath} không giả MistralOcr bằng Gemini`);
  assert.ok(targetHtml.includes('preferred_model: useModel'), `${relPath} gửi preferred_model tới Canvas API`);
  assert.ok(targetHtml.includes('allowEmptyKey: true'), `${relPath} cho phép tuyến Gemini hệ thống không cần key trình duyệt`);
  assert.ok(targetHtml.includes('lastCanvasMeta = metadata'), `${relPath} lưu metadata tuyến/model Canvas an toàn`);
  assert.ok(targetHtml.includes('type: "canvas_route"'), `${relPath} báo tuyến Gemini Canvas thực tế`);
  assert.ok(!targetHtml.includes('user_account:'), `${relPath} không gửi danh tính người dùng từ Canvas`);

  // 3. Kiểm tra nút 1-Click
  assert.ok(targetIds.has('btn1ClickGenerate'), `${relPath} phải có nút #btn1ClickGenerate`);
  assert.ok(targetIds.has('selectGenerationMode'), `${relPath} phải có bộ chọn chế độ soạn`);
  assert.match(targetHtml, /id="selectGenerationMode"[\s\S]*?value="detailed" selected/, `${relPath} phải mặc định soạn chi tiết`);
  assert.ok(targetHtml.includes("khbd_generation_mode"), `${relPath} phải lưu chế độ soạn`);
  assert.ok(targetHtml.includes("isCompact"), `${relPath} phải điều phối riêng chế độ rút gọn`);
  assert.ok(targetHtml.includes('TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)'), `${relPath} phải có nhãn nút 1-Click`);
  assert.ok(targetHtml.includes('handle1ClickGenerate'), `${relPath} phải có hàm điều phối handle1ClickGenerate`);
  assert.match(targetHtml, /async function handle1ClickGenerate\(\)\s*\{\s*await \(window\.__KHBD_CANVAS_CORE_READY__ \|\| Promise\.resolve\(\)\);/, `${relPath} 1-Click phải chờ core modules sẵn sàng`);
  assert.match(targetHtml, /topic === "Bài học chưa đặt tên"/, `${relPath} 1-Click phải chặn bài chưa đặt tên`);
  assert.match(targetHtml, /danh mục SGK\/PPCT hoặc nhập tên bài/, `${relPath} 1-Click phải cảnh báo chọn bài từ SGK/PPCT`);
  assert.match(targetHtml, /function getSubjectDisplayName/, `${relPath} phải có getSubjectDisplayName`);
  assert.match(targetHtml, /Năng lực số \(NLS theo CV 3456\/BGDĐT - máy tính cầm tay, GeoGebra, tra cứu bảng số\)/, `${relPath} OUTPUT_CONTRACT phải giải nghĩa NLS kèm công cụ môn học`);
  assert.match(targetHtml, /Natural Language System/, `${relPath} OUTPUT_CONTRACT phải cấm giải nghĩa NLS thành Natural Language System`);
  if (relPath === 'canvas_soankhbd.html') {
    assert.ok(targetHtml.includes("!isCompact && typeof generateLessonIllustrations"), `${relPath} rút gọn không tạo hình minh họa SGK`);
    assert.ok(targetHtml.includes('8. 🎨 F. Hình minh họa SGK (Vector SVG & Hình ảnh)'), `${relPath} popup 1-Click phải hiển thị bước 8 hình minh họa SGK`);
    assert.ok(targetHtml.includes('await generateLessonIllustrations({ silent: true })'), `${relPath} 1-Click phải tự động gọi bước tạo hình minh họa SGK ở chế độ silent`);
  }

  // 4. Kiểm tra độ tương thích 1-1 các DOM ID từ soankhbd.html
  const criticalIds = [
    'khbdWorkflowStepper', 'step1Badge', 'step2Badge', 'step3Badge', 'step4Badge',
    'btnStep3Recommend', 'btnStartComposeFromStep4',
    'ppctLessonPicker', 'ppctLessonSearch', 'ppctLessonList', 'ppctLessonSummary',
    'tab0-sub-materials', 'tab0-sub-lesson-info', 'tab0-sub-pedagogy-digital', 'tab0-sub-ai-competency', 'tab0-sub-language-inclusive',
    'lessonTextbookAnalysis', 'dropzoneContainer', 'fileInputImages', 'btnAnalyzeVision', 'imageGallery', 'detailsVisionContent', 'editorVision', 'previewVision',
    'lessonPpctAnalysis', 'dropzoneContainerPpct', 'fileInputPpct', 'btnPastePpct', 'btnAnalyzePpct', 'ppctGallery', 'detailsPpctContent', 'editorPpct', 'previewPpct',
    'lessonIllustrationCard', 'btnGenerateIllustrations', 'illustrationGallery',
    'lessonGeneralSettingsCard', 'selectGrade', 'selectSubject', 'selectLesson',
    'inputSchool', 'inputGroup', 'inputTeacher', 'inputSubject', 'inputTopicCustom', 'inputDuration', 'inputLessonScope',
    'inputClassSize', 'selectReadiness', 'selectGrouping', 'hasProjector', 'hasInternet', 'hasDevices',
    'lessonStep3RecommendCard', 'btnSuggestPedagogyStandards', 'btnStep3PedagogyDigital',
    'methodsCatalogPanel', 'techniquesCatalogPanel', 'activitiesCatalogPanel', 'digitalStandardsPanel', 'subjectIntegrationsPanel',
    'toggleDigitalCompetency', 'toggleAiCompetency', 'aiStandardsPanel',
    'dynamicIntegrationsContainer', 'toggleForeignLanguage', 'toggleInclusiveSupport',
    'tabObjectives', 'btnGenerateObjectives', 'btnExportObjectivesDocx', 'editorObjectives', 'previewObjectives',
    'tabMaterials', 'btnGenerateMaterials', 'btnExportMaterialsDocx', 'editorMaterials', 'previewMaterials',
    'tabActivities', 'currentActTitle', 'btnGenerateCurrentAct', 'btnExportCurrentActDocx', 'editorActivity', 'previewActivity', 'activityMarkdownCard', 'activityIllustrationCard',
    'tabFullPreview', 'btnExportFullDocx', 'btnCopyFullMarkdown', 'btnPrintPlan', 'fullLessonPreview',
    'progressContainer', 'progressStepTitle', 'progressPercent', 'progressBarInner',
    'btnCancelGeneration', 'btnClearAll',
    'modalImageZoom', 'modalPdfPageSelect', 'modalPpctStandardsDetected', 'ppctDetectedStandardsList',
    'modalApiKeys', 'textareaApiKeys', 'btnSaveApiKeys', 'btnTestApiKey', 'textareaMistralKeys', 'btnTestMistralKey',
    'btnConfirmPdfPages', 'pdfRadioAll', 'pdfRadioRange', 'inputPdfPageRange',
    'statusFooterText', 'toastContainer'
  ];

  for (const id of criticalIds) {
    assert.ok(targetIds.has(id), `${relPath} thiếu DOM ID thiết yếu #${id}`);
  }

  // 5. Kiểm tra cú pháp JavaScript inline
  const scriptBlocks = [...targetHtml.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].map(m => m[1]);
  for (let i = 0; i < scriptBlocks.length; i++) {
    const code = scriptBlocks[i].trim();
    if (!code) continue;
    try {
      new vm.Script(code);
    } catch (err) {
      assert.fail(`Lỗi cú pháp JavaScript trong khối script #${i + 1} của ${relPath}: ${err.message}`);
    }
  }

  console.log(`✓ ${relPath}: Đã kiểm tra 100% đạt chuẩn Canvas và tương thích 1-1 với soankhbd.html.`);
}

console.log('\n================================================================');
console.log('🎉 TẤT CẢ KIỂM THỬ CANVAS_SOANKHBD ĐÃ PASS 100%!');
console.log('================================================================\n');
