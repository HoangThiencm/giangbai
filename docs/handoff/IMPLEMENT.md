# IMPLEMENT

Trạng thái: ĐÃ LÀM — Tinh gọn Hoạt động E thành danh sách 4 mục, không bảng 4 bước

## File đã đổi

- `js/khbd-prompts.js`
- `js/khbd-app.js`
- `tests/khbd-activity-e-smoke.js`
- `tests/khbd-activity-e-dedupe-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Nội dung chính

1. **Prompt (`js/khbd-prompts.js`)**
   - `GENERATE_ACTIVITY_E`: bỏ `ACTIVITY_TABLE_CONTRACT`, a) b) c) d) và bảng 2 cột. Mẫu xuất:
     `## E. HOẠT ĐỘNG 5: HƯỚNG DẪN VỀ NHÀ ({time_budget_E})` rồi `1.` Ôn tập kiến thức, `2.` Làm bài tập, `3.` Chuẩn bị bài mới, `4.` Nhiệm vụ tìm tòi, mở rộng.
   - `{ai_homework_prompt_note}` chỉ khi bật AI: `- Hướng dẫn Prompt AI an toàn:` + `+ Mẫu Prompt: "..."`.
   - `GENERATE_ACTIVITIES_AE` / `GENERATE_ACTIVITIES_AD`: bảng 2 cột chỉ áp dụng A–D; Pha E cùng định dạng danh sách 4 mục, cấm a/b/c/d và bảng.

2. **Logic (`js/khbd-app.js`)**
   - `buildPhasePedagogyContext("E")`: yêu cầu danh sách 4 mục, cấm bảng/4 bước.
   - `assertPhasePedagogyOutput("E")`: bắt đủ 4 nội dung (ôn tập, làm bài tập, chuẩn bị bài mới, tìm tòi/mở rộng); không bắt bảng hay GV/HS.
   - `scoreKhbdActivityBlock(block, actKey)`: khối E cộng điểm 4 mục + danh sách `1. 2. 3. 4.`; không cộng điểm a/b/c/d; trừ nhẹ nếu còn bảng/a-b-c-d.
   - `getFullLessonPlanMarkdown` / `renderMathPreview` giữ nguyên: markdown `1. 2. 3. 4.` render danh sách.

3. **Test**
   - `tests/khbd-activity-e-smoke.js`: assert 4 mục, cấm bảng 2 cột, validator thiếu mục thì fail.
   - `tests/khbd-activity-e-dedupe-smoke.js`: khi trùng tiêu đề E, giữ khối danh sách 4 mục.

## Ngoài phạm vi (không đụng)

- Bảng 2 cột 4 bước của Hoạt động A, B, C, D.
- Cấu trúc xuất Word chung (`DocxGenerator`).

## Test đã chạy

```
node tests/khbd-activity-e-smoke.js
node tests/khbd-activity-e-dedupe-smoke.js
node tests/khbd-4steps-workflow-smoke.js
node tests/khbd-docx-layout-smoke.js
node tests/khbd-time-budgets-smoke.js
node tests/khbd-pedagogy-script-smoke.js
```

Kết quả: **pass**.

Không mở được trình duyệt để bấm "Tạo Hoạt động E" trên `soankhbd.html` hay xuất file .docx thật. Cần `/verify` trên giao diện.
