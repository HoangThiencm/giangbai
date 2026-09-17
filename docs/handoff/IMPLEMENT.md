# IMPLEMENT: getGradeLevel, dropdown PPCT, ảo giác NLS/doanh nghiệp

Đã triển khai đúng `docs/handoff/PLAN.md`.

## A. Khóa môn học, dropdown PPCT, triệt ảo giác NLS

- `OUTPUT_CONTRACT` (Canvas KHBD, Canvas bài giảng, backup, `js/khbd-prompts.js`): NLS = Năng lực số (CV 3456/BGDĐT — máy tính cầm tay, GeoGebra, tra cứu bảng số); AI = Năng lực AI (QĐ 2422/BGDĐT). Cấm Natural Language System, văn bản doanh nghiệp, quy trình kinh doanh.
- `getPromptTemplate('GENERATE_OBJECTIVES')` và `buildPedagogicalPrompt`: khối `RÀNG BUỘC MÔN HỌC BẮT BUỘC`.
- `currentSubjectId` / `appState.selectedSubject` lowercase. `getSystemRole`, `getSubjectCompetencies`, `latexSubjects.includes` so khớp `toan`. `getSubjectDisplayName` không rơi về `"Môn học"`.
- `normalizeLessonTitleMatch`: `Bài 2.` ≡ `Bài 2:`. `populateLessonDropdown` dùng hàm này nên chọn PPCT không làm dropdown nhảy về `-- Chọn bài học từ SGK --`.
- `canvasTextbookAnalysisPrompt`: `.join("\n")`.
- `applyObjectivesOutput`: hủy văn bản lạc đề; không `repairWithGemini` kiểu “giữ nguyên dòng đã có”; tái tạo bằng `GENERATE_OBJECTIVES` + khóa môn học.

## B. `getGradeLevel` & nút tạo từng mục không đơ

- `safeGetGradeLevel` / `safeGetGradeLevelName`; prompt dùng helper; export `window`.
- `installCurriculumFallback` đủ `getGradeLevel` / `getGradeLevelName` (1–5 tiểu học, 6–9 THCS, 10–12 THPT).
- 1-Click `await window.__KHBD_CANVAS_CORE_READY__`.
- `js/khbd-curriculum.js` gán `window.getGradeLevel`, `window.getGradeLevelName`, `window.getSubjectCompetencies`.
- `handleGenerateCurrentActivity`, `handleGenerateObjectives`, `handleGenerateMaterials`: `try/catch` → `hideProgress()` + `showToast("Lỗi khởi tạo: " + err.message)`.

Kiểm thử:

- `node tests/canvas-soankhbd-smoke.js` — PASS (`Bài 2.` ≡ `Bài 2:`, try/catch nút tạo mục)
- `node tests/canvas-module-fallback-smoke.js` — PASS
- `node tests/khbd-nls-ai-bold-italic-smoke.js` — PASS
- `node tests/canvas-prompts-integrity-smoke.js` — PASS
- `node tests/canvas-soanbaigiang-smoke.js` — PASS
- `node tests/khbd-4steps-workflow-smoke.js` — PASS
- `node tests/ppct-settings-import-smoke.js` — PASS

Không thêm chức năng ngoài plan. Cần `/verify` trên Antigravity: chọn bài từ PPCT (dấu chấm), 1-Click Toán 9 Bài 2, và bấm “Tạo nội dung mục này”.
