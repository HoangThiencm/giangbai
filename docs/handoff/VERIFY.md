# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `js/khbd-prompts.js`: Đã loại bỏ hoàn toàn mẫu `- [Tên năng lực]:` và `[Tên năng lực chung 1...]`, thêm chỉ thị cấm ngoặc vuông `[ ]` trong `GENERATE_OBJECTIVES`, `GENERATE_CORE_LESSON` và `getPromptTemplate`. Giữ nguyên vẹn định dạng mã NLS/AI (`***[Mã]:***`). Đúng scope.
- `js/khbd-app.js`: Thêm hàm `stripSquareBracketsFromCompetencies(markdown)` loại bỏ dấu ngoặc vuông ở tên năng lực chung, năng lực đặc thù và phẩm chất; tích hợp vào `applyObjectivesOutput` và export. Đúng scope.
- `tests/khbd-competency-brackets-smoke.js`: File test mới kiểm tra tính toàn vẹn của prompt, hàm hậu xử lý và pipeline. Đúng scope.
- Không sửa source ngoài scope, không xóa `docs/handoff/.lock`.

## Test đã chạy
1. `node tests/khbd-competency-brackets-smoke.js` -> PASS
2. `node tests/canvas-soankhbd-smoke.js` -> PASS
3. `node tests/canvas-prompts-integrity-smoke.js` -> PASS
4. `node tests/khbd-competencies-smoke.js` -> PASS
5. `node tests/khbd-nls-ai-bold-italic-smoke.js` -> PASS
6. `node tests/ppct-settings-import-smoke.js` -> PASS
7. `node tests/khbd-4steps-workflow-smoke.js` -> PASS
8. `node tests/khbd-docx-math-smoke.js` -> PASS
9. `node tests/khbd-sanitize-smoke.js` -> PASS

## Pass / Fail từng tiêu chí
- [PASS] Bỏ dấu ngoặc vuông `[ ]` quanh tên năng lực chung, năng lực đặc thù và phẩm chất.
- [PASS] Bảo lưu nguyên vẹn dấu ngoặc vuông ở mã NLS/AI (ví dụ: `***[5.3.TC2a]:***`, `***[9.B2.1]:***`).
- [PASS] Prompt hướng dẫn mô hình không sinh ngoặc vuông.
- [PASS] Hậu xử lý loại bỏ triệt để ngoặc vuông nếu mô hình vẫn sinh ra.
- [PASS] Không gây hồi quy các tính năng khác của `canvas_soankhbd`.

## Bug
Không có
