# IMPLEMENT

Trạng thái: ĐÃ LÀM — Lọc đề theo lớp + giữ nguyên 20 câu Word ở Tổng hợp

## File đã đổi

- `thitructuyen.html`
- `exam-stitch-client.js`
- `tests/exam-word-stitch-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Nội dung chính

1. **Lọc theo lớp**: `TeacherDashboard` có dropdown `classFilter` (Tất cả các lớp / Thí sinh tự do / từng lớp). Danh sách lớp gộp từ đề đã tạo và `api/student-classes`. `matchesClassFilter` lọc `filteredExams`.
2. **Không nuốt câu Word**: `isDuplicate` so sánh cả nội dung câu hỏi và 4 đáp án, ngưỡng > 98% (Dice bigram), bỏ so sánh index 0.85. `flattenStitchedQuestions` không dedupe khi chỉ có 1 trang (nhập Word).

## Ngoài phạm vi giữ nguyên

- Không đổi schema lưu đề.
- Không đổi StudentView.

## Test đã chạy

```
node tests/exam-word-stitch-smoke.js
```

Kết quả: **pass**.
