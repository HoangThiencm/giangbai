# IMPLEMENT

Trạng thái: ĐÃ LÀM — Tái cấu trúc Tab 0 thành 5 tab con

## File đã đổi

- `soankhbd.html`
- `js/khbd-app.js`
- `tests/khbd-4steps-workflow-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Nội dung chính

1. **HTML Tab 0**: thanh `.tab0-subtabs-nav` với 5 nút, bọc nội dung sẵn có vào 5 pane:
   - `tab0-sub-materials`: SGK, PPCT, card hình minh họa
   - `tab0-sub-lesson-info`: trường/GV/môn/bài, thời lượng, bối cảnh lớp, đề xuất thông tin + bản nháp
   - `tab0-sub-pedagogy-digital`: PPDH 4 pha, NLS TT 02, tích hợp môn
   - `tab0-sub-ai-competency`: Năng lực AI QĐ 2422 độc lập
   - `tab0-sub-language-inclusive`: Ngoại ngữ, Hòa nhập, Hỗ trợ chức năng
2. **JS**: `switchTab0Subtab(subtabKey)` đổi class `active` trên nút và pane. Stepper 4 bước gọi `revealTab0WorkflowStep` (bước 1–2 → gửi file, bước 3 → PPDH/NLS, bước 4 → AI). Ctrl+V / nạp PDF mở tab con gửi file. ID input/select/checkbox và localStorage không đổi.
3. **Smoke**: `tests/khbd-4steps-workflow-smoke.js` kiểm 5 pane, mapping stepper, và hàm chuyển tab.

## Ngoài phạm vi (không đụng)

- Tab 1 Mục tiêu, Tab 2 Thiết bị, Tab 3 Tiến trình A–F.
- Đổi tên ID form.

## Test đã chạy

```
node tests/khbd-4steps-workflow-smoke.js
```

Kết quả: **pass** (5 pane Tab 0, mapping stepper, switchTab0Subtab).
