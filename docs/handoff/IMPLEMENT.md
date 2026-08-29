# IMPLEMENT

Trạng thái: ĐÃ LÀM — Sửa NLS luôn 2–3 mục + bố cục Tab 0 từ trên xuống, tách AI độc lập

## File đã đổi

- `soankhbd.html`
- `js/khbd-app.js`
- `js/khbd-standards.js`
- `tests/khbd-4steps-workflow-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Nội dung chính

1. **NLS không còn rỗng**: `KHBD_STANDARDS.digital.minSelect = 2`, `maxSelect = 3`. `recommendOfficialStandards` và `catalogFallbackRecords("digital")` luôn trả 2–3 mục TC1a (lớp 6–7) / TC2a (lớp 8–9). `applySuggestedStandardRecords` không ghi mảng rỗng (không xóa tick). Nhóm `<details>` có mục được chọn tự `open`.
2. **Nút đọc dưới dropzone**: `btnAnalyzeVision` / `btnAnalyzePpct` đặt ngay dưới vùng nạp tương ứng.
3. **Tab 0 tuần tự**: Khối 1 học liệu → Khối 2 thông tin bài dạy → Khối 3 PPDH & NLS (TT 02) → Khối 4 card AI (QĐ 2422) độc lập.
4. **AI tách khỏi NLS**: Không còn chung tab tích hợp. AI mặc định tắt; chỉ tick 2–3 mục khi bật.

## Ngoài phạm vi giữ nguyên

- Không đổi danh mục mã TT 02 / QĐ 2422.
- Không đổi xuất Word 5512.

## Test đã chạy

```
node tests/khbd-4steps-workflow-smoke.js
```

Kết quả: **pass** (`khbd-4steps-workflow-smoke.js`, kèm structured-candidates, mistral-ocr, ppct-integration, dynamic-integrations).
