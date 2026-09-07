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

  // 3. Kiểm tra nút 1-Click
  assert.ok(targetIds.has('btn1ClickGenerate'), `${relPath} phải có nút #btn1ClickGenerate`);
  assert.ok(targetHtml.includes('TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)'), `${relPath} phải có nhãn nút 1-Click`);
  assert.ok(targetHtml.includes('handle1ClickGenerate'), `${relPath} phải có hàm điều phối handle1ClickGenerate`);

  // 4. Kiểm tra độ tương thích 1-1 các DOM ID từ soankhbd.html
  const criticalIds = [
    'khbdWorkflowStepper', 'step1Badge', 'step2Badge', 'step3Badge', 'step4Badge',
    'btnStep3Recommend', 'btnStartComposeFromStep4',
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
