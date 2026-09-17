# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Đã kiểm tra `js/khbd-app.js`:
  + Khai báo các hàm phòng vệ `safeGetGradeLevel` và `safeGetGradeLevelName`, thay thế toàn bộ các vị trí gọi `getGradeLevel(...)` và `getGradeLevelName(...)` trực tiếp trên global scope.
  + Thêm hàm `normalizeLessonTitleMatch(str)` chuẩn hóa dấu câu (`Bài 2.` tương đương `Bài 2:`), giúp `populateLessonDropdown()` nhận diện chính xác bài học chọn từ danh mục PPCT và không bị nhảy về `-- Chọn bài học từ SGK --`.
  + Bọc khối `try/catch` tại `handleGenerateCurrentActivity`, `handleGenerateObjectives`, `handleGenerateMaterials` để đảm bảo luôn gọi `hideProgress()` và hiển thị `showToast("Lỗi khởi tạo: " + err.message, "danger", 6000)` khi có lỗi ngoại lệ phát sinh, triệt tiêu tình trạng click vào nút bấm bị "đơ" im lặng.
  + Sửa lỗi nối chuỗi prompt phân tích SGK tại dòng 7002 từ `.join("\\n")` thành `.join("\n")`.
  + Cập nhật `applyObjectivesOutput`: tự động phát hiện và hủy bỏ toàn bộ nội dung rác doanh nghiệp (`doanh nghiệp`, `quy trình doanh nghiệp`, `khách hàng`, `phân tích sắc thái`) trước khi xử lý, loại bỏ lệnh ép Gemini giữ nguyên dòng rác, tái tạo mục tiêu bài dạy đúng chuẩn môn học THCS/THPT.
- Đã kiểm tra `js/khbd-prompts.js`, `canvas_soankhbd.html`, `canvas_soanbaigiang.html` và các file backup:
  + `OUTPUT_CONTRACT`: Quy định rõ ràng NLS là Năng lực số (CV 3456/BGDĐT — máy tính cầm tay, GeoGebra, bảng số), AI là Năng lực AI (QĐ 2422/BGDĐT); nghiêm cấm tuyệt đối suy diễn thành "Natural Language System" hoặc sinh nội dung quản trị kinh doanh/doanh nghiệp.
  + Khối `RÀNG BUỘC MÔN HỌC BẮT BUỘC` (Subject & Pedagogical Discipline Guard) trong `GENERATE_OBJECTIVES` và `buildPedagogicalPrompt` khóa chặt môn học phổ thông theo CT GDPT 2018.
  + Chuẩn hóa `currentSubjectId` / `appState.selectedSubject` lowercase và hàm `getSubjectDisplayName` trả về đúng tên môn học, không bị rơi về `"Môn học"`.
- Đã kiểm tra `js/khbd-curriculum.js` & `installCurriculumFallback`:
  + Export đầy đủ `window.getGradeLevel`, `window.getGradeLevelName`, `window.getSubjectCompetencies`.
  + Khai báo dự phòng đầy đủ trong `installCurriculumFallback` ở các file HTML canvas.

## Test đã chạy
- `node tests/canvas-soankhbd-smoke.js` — PASS 100%
- `node tests/canvas-module-fallback-smoke.js` — PASS 100%
- `node tests/khbd-nls-ai-bold-italic-smoke.js` — PASS 100%
- `node tests/canvas-prompts-integrity-smoke.js` — PASS 100%
- `node tests/khbd-1click-chain-smoke.js` — PASS 100%
- `node tests/khbd-autofill-metadata-smoke.js` — PASS 100%
- `node tests/khbd-4steps-workflow-smoke.js` — PASS 100%
- `node tests/canvas-soanbaigiang-smoke.js` — PASS 100%
- `node tests/ppct-settings-import-smoke.js` — PASS 100%

## Pass / Fail từng tiêu chí
- [x] Tiêu chí 1: Chọn bài học từ PPCT thì Dropdown DANH MỤC BÀI HỌC ở thanh trên cùng tự động đồng bộ và giữ nguyên tên bài, không bị nhảy về `-- Chọn bài học từ SGK --` -> PASS.
- [x] Tiêu chí 2: Khóa chặt môn học, triệt tiêu hoàn toàn ảo giác NLS thành Natural Language System / tối ưu hóa quy trình doanh nghiệp -> PASS.
- [x] Tiêu chí 3: Nút "Tạo nội dung mục này" ở từng hoạt động được bảo vệ bằng try/catch + toast thông báo, không còn hiện tượng click bị đơ im lặng -> PASS.
- [x] Tiêu chí 4: `safeGetGradeLevel` và fallback hoạt động chuẩn xác, loại bỏ hoàn toàn `ReferenceError: getGradeLevel is not defined` -> PASS.
- [x] Tiêu chí 5: Toàn bộ test suites kiểm thử tự động đạt 100% PASS -> PASS.

## Bug
Không có.
