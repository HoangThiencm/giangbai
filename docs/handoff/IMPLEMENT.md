# Báo cáo triển khai: Danh sách nhân sự mặc định cho báo cáo

## Phạm vi đã thực hiện

- Cập nhật duy nhất `DEFAULT_ACCOUNT_PROFILE_SEED` trong `backupcode viettailieu/taobaocao.html`.
- Danh sách Ban giám hiệu mặc định theo đúng thứ tự: Bùi Ngọc Nam (Hiệu trưởng), Đinh Văn Đông (Hiệu phó), Nguyễn Ngọc Nam (Hiệu phó).
- Danh sách mặc định gồm 6 tổ theo đúng thứ tự và nhân sự đã được cung cấp: Tổ Anh văn - TV - TB, Tổ GDTC - NT, Tổ KHTN - CN, Tổ Toán - Tin, Tổ Văn - GDCD - Sử - Địa và Tổ Văn phòng.
- Không thay đổi cơ chế nạp/lưu hồ sơ: dữ liệu này chỉ được dùng khi khởi tạo mặc định, không ghi đè hồ sơ hoặc cài đặt đã lưu của người dùng.
- Thêm `tests/taobaocao-default-staff-seed-smoke.js` để kiểm tra đầy đủ BGH, 6 tổ, thứ tự và danh sách nhân sự mặc định.

## Kiểm thử

- `node tests/taobaocao-default-staff-seed-smoke.js`: PASS.
- `node tests/taobaocao-account-sync-smoke.js`: PASS.
- `git diff --check`: PASS (chỉ có cảnh báo CRLF từ Git, không có lỗi định dạng diff).

## Bảo toàn

- Không sửa `docs/handoff/PLAN.md`.
- Không commit hoặc push.
- Giữ nguyên các thay đổi ngoài phạm vi.

---

# Báo cáo trước đó: Chuẩn hóa in đậm & in nghiêng cho NLS và Năng lực AI

## Phạm vi đã thực hiện

- `js/khbd-docx.js`: Marker NLS/AI trong `markerRunColor()` nhận `bold: true` và `italics: true`. `pushMarkerWithMath()` chuyển tiếp `italics`. `parseInlineTextToRuns()` bắt khối `***...***` / `___...___` trước `**` / `__`. Heading 3 NLS/AI (`### c) Năng lực số`, `### d) Năng lực AI`) xuất Word với in đậm và in nghiêng.
- `css/khbd-styles.css`: `.khbd-badge-nls` và `.khbd-badge-ai` thêm `font-style: italic` (giữ `font-weight: 700` từ `.khbd-badge`). `.preview-rendered .khbd-nls` / `.khbd-ai` và heading tương ứng thêm `font-weight: 700; font-style: italic`.
- `js/khbd-prompts.js`: Marker mẫu pha A–D và hợp đồng đầu ra chuyển sang `***[NLS: ...]***` / `***[AI: ...]***`. `digitalObjectivesSection` / `aiObjectivesSection` dùng `- ***[Mã]:*** *[Mô tả]*`. Bổ sung quy tắc bắt buộc in đậm + in nghiêng bằng Markdown `***...***`.
- `js/khbd-app.js`: `insertObjectivesMissingStandards()` xuất `- ***${code}:*** *${label}*`. `stripDisabledActivityIntegrations()` và `assertActivityIntegrations()` (dùng bởi `activityOutputProblem`) bắt `\*{1,3}` cho marker NLS/AI. Prompt ràng buộc pha dùng marker 3 sao.
- `tests/khbd-integrations-smoke.js` và `tests/khbd-dynamic-integrations-smoke.js`: assertion `markerRunColor` NLS/AI khớp `{ ..., bold: true, italics: true }`.
- `tests/khbd-nls-ai-bold-italic-smoke.js`: kiểm tra parse `***`, TextRun `w:b` + `w:i` + màu/shading, CSS badge/preview, và prompt contract.
- `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`: nạp `css/khbd-styles.css`, `js/khbd-prompts.js`, `js/khbd-docx.js`, `js/khbd-app.js` local khi `file:`/`localhost`; hosting kèm `?v=20260915-nls-ai-bi`. CSS inline badge/preview NLS–AI in đậm + in nghiêng để Canvas sandbox không phụ thuộc CSS hosting cũ.

## Kiểm thử

- `node tests/khbd-nls-ai-bold-italic-smoke.js`: PASS 100%.
- `node tests/khbd-integrations-smoke.js`: PASS.
- `node tests/khbd-dynamic-integrations-smoke.js`: PASS.
- `node tests/khbd-docx-format-smoke.js`: PASS.
- `node tests/khbd-ai-integration-gate.test.js`: PASS.
- `node tests/canvas-soankhbd-smoke.js`: PASS.
- `node tests/backupcode-canvas-smoke.js`: PASS.

Không chạy được `git diff --check` trên máy này vì `git` không có trong PATH.

## Bảo toàn

`docs/handoff/PLAN.md` không bị sửa. Không commit/push.
