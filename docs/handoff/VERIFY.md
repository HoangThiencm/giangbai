# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `js/khbd-docx.js`: `markerRunColor` trả về `bold: true, italics: true` cho NLS và AI. `pushMarkerWithMath` chuyển tiếp `italics`. `parseInlineTextToRuns` bóc tách `***...***` và `___...___` thành TextRun in đậm + in nghiêng. Heading 3 NLS/AI xuất Word in đậm + in nghiêng. Khớp 100% PLAN.
- `css/khbd-styles.css`: `.khbd-badge-nls` và `.khbd-badge-ai` bổ sung `font-style: italic`. Khối `.preview-rendered .khbd-nls` và `.khbd-ai` cùng heading tương ứng có `font-weight: 700; font-style: italic`. Khớp 100% PLAN.
- `js/khbd-prompts.js`: Marker mẫu pha A–D và hợp đồng đầu ra chuyển sang `***[NLS: ...]***` / `***[AI: ...]***`. Mục tiêu NLS / AI dùng `- ***[Mã]:*** *[Mô tả]*`. Khớp 100% PLAN.
- `js/khbd-app.js`: `insertObjectivesMissingStandards` xuất định dạng `- ***${code}:*** *${label}*`. Bộ làm sạch `stripDisabledActivityIntegrations` và kiểm định tích hợp hỗ trợ cú pháp `\*{1,3}`. Khớp 100% PLAN.
- Không sửa ngoài scope của PLAN.md. Không đổi cấu trúc ngoài plan.

## Test đã chạy
- `node tests/khbd-nls-ai-bold-italic-smoke.js`: PASS 100%
- `node tests/khbd-integrations-smoke.js`: PASS
- `node tests/khbd-dynamic-integrations-smoke.js`: PASS
- `node tests/khbd-docx-format-smoke.js`: PASS
- `node tests/khbd-ai-integration-gate.test.js`: PASS

## Pass / Fail từng tiêu chí
- Tiêu chí 1 (Word DOCX TextRun w:b + w:i cho marker NLS & AI): PASS
- Tiêu chí 2 (Web Preview Badge NLS & AI có font-weight 700 và font-style italic): PASS
- Tiêu chí 3 (Parse Markdown inline `***...***` sang bold + italic trong DOCX): PASS
- Tiêu chí 4 (Prompt mẫu và cấu trúc Mục I NLS/AI chuẩn hóa bold + italic): PASS
- Tiêu chí 5 (Bộ làm sạch / gate khi tắt NLS/AI dọn sạch cả marker 3 sao): PASS

## Bug
Không có.
