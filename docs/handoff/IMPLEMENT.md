# Báo cáo triển khai: Chuẩn hóa in đậm & in nghiêng cho NLS và Năng lực AI

## Phạm vi đã thực hiện

- `js/khbd-docx.js`: Marker NLS/AI trong `markerRunColor()` nhận `bold: true` và `italics: true`. `pushMarkerWithMath()` chuyển tiếp `italics`. `parseInlineTextToRuns()` bắt khối `***...***` / `___...___` trước `**` / `__`. Heading 3 NLS/AI (`### c) Năng lực số`, `### d) Năng lực AI`) xuất Word với in đậm và in nghiêng.
- `css/khbd-styles.css`: `.khbd-badge-nls` và `.khbd-badge-ai` thêm `font-style: italic` (giữ `font-weight: 700` từ `.khbd-badge`). `.preview-rendered .khbd-nls` / `.khbd-ai` và heading tương ứng thêm `font-weight: 700; font-style: italic`.
- `js/khbd-prompts.js`: Marker mẫu pha A–D và hợp đồng đầu ra chuyển sang `***[NLS: ...]***` / `***[AI: ...]***`. `digitalObjectivesSection` / `aiObjectivesSection` dùng `- ***[Mã]:*** *[Mô tả]*`. Bổ sung quy tắc bắt buộc in đậm + in nghiêng bằng Markdown `***...***`.
- `js/khbd-app.js`: `insertObjectivesMissingStandards()` xuất `- ***${code}:*** *${label}*`. `stripDisabledActivityIntegrations()` và `assertActivityIntegrations()` (dùng bởi `activityOutputProblem`) bắt `\*{1,3}` cho marker NLS/AI. Prompt ràng buộc pha dùng marker 3 sao.
- `tests/khbd-integrations-smoke.js` và `tests/khbd-dynamic-integrations-smoke.js`: assertion `markerRunColor` NLS/AI khớp `{ ..., bold: true, italics: true }`.
- `tests/khbd-nls-ai-bold-italic-smoke.js`: kiểm tra parse `***`, TextRun `w:b` + `w:i` + màu/shading, CSS badge/preview, và prompt contract.

## Kiểm thử

- `node tests/khbd-nls-ai-bold-italic-smoke.js`: PASS 100%.
- `node tests/khbd-integrations-smoke.js`: PASS.
- `node tests/khbd-dynamic-integrations-smoke.js`: PASS.
- `node tests/khbd-docx-format-smoke.js`: PASS.
- `node tests/khbd-ai-integration-gate.test.js`: PASS.

Không chạy được `git diff --check` trên máy này vì `git` không có trong PATH.

## Bảo toàn

`docs/handoff/PLAN.md` không bị sửa. Không commit/push.
