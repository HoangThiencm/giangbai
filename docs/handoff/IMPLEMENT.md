# IMPLEMENT

Trạng thái: ĐÃ LÀM — Sub-tab F Hồ sơ & Phiếu học tập + phụ lục Word IV

## File đã đổi

- `soankhbd.html`
- `js/khbd-app.js`
- `js/khbd-prompts.js`
- `js/khbd-docx.js` (file xuất Word thực tế của project; không tạo `khbd-docx-export.js` mới)
- `tests/khbd-pedagogy-script-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Nội dung chính

1. **Tab F**: `activities-nav` thêm `F. Hồ sơ học tập`. `ACTIVITY_TITLES.F` = Hồ sơ dạy học & phiếu học tập (phụ lục).
2. **Sinh AI**: Tab F gọi `GENERATE_PORTFOLIO_WORKSHEETS` (alias `PROMPTS.ACTIVITY_F`). Đọc A–D, thiết kế PHT số 1/2, phiếu Trạm 1–3 nếu có station, Rubric/Bảng kiểm, hướng dẫn chấm, khung in trường/lớp/họ tên.
3. **Word**: `getFullLessonPlanMarkdown` thêm `# IV. PHỤ LỤC: HỒ SƠ DẠY HỌC...` ở cuối. `khbd-docx.js` ngắt trang trước tiêu đề IV phụ lục.
4. **A–E không đổi** cấu trúc I, II, III.

## Test đã chạy

```
node tests/khbd-pedagogy-script-smoke.js
```

Kết quả: **pass**.
