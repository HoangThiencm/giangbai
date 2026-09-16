# Báo cáo triển khai: Bảng đáp án hỗn hợp CV 7991 khi nhập Word/văn bản

## Đã thực hiện

- `thitructuyen.html`
  - Nâng cấp `getImportedAnswerKey` để nhận diện 3 loại đáp án trong block `Đáp án:`:
    1. Trắc nghiệm nhiều lựa chọn `A-D` (kể cả dạng cũ `1C 2B` không có dấu chấm).
    2. Đúng/Sai: `Đúng`, `Sai`, `Đ`, `S`, `True`, `False`, `T`, `F`; nhiều ý phụ `13. a.Đúng b.Sai c.Đúng d.Sai` hoặc `13: Đ, S, Đ, S`.
    3. Trả lời ngắn: số nguyên, số thực, phân số, chuỗi ngắn (`27`, `2000`, `3.14`, `-1/2`).
  - Token được duyệt trái sang phải nên `15. 3.14` không bị hiểu thành câu 3.
  - `stripImportedAnswerKey` cắt bảng đáp án khi `getImportedAnswerKey` nhận được ít nhất 1 cặp.
  - `parseLatexWordQuiz` gán `correct_answers` cho câu `tf` từ `answerKey` nếu chưa có đáp án inline; gán `correct_answer` cho câu `short_answer` từ `answerKey` (chữ `Đúng`/`Sai` nếu khóa là tf đơn).
- `tests/thitructuyen-cv7991-answerkey-smoke.js`: test mới theo chuỗi đáp án mẫu trong PLAN.

## Ngoài phạm vi (không đụng)

- Không đổi thuật toán chấm điểm / trọng số CV 7991 trong `backend/thitructuyen.py` và `api/exam.php`.
- Không đổi giao diện làm bài của học sinh.
- Không sửa `docs/handoff/PLAN.md`.

## Kiểm thử

- `node tests/thitructuyen-cv7991-answerkey-smoke.js`: PASS (18 câu mẫu, TF nhiều ý, MC thuần, số thập phân, strip bảng đáp án).
- `node tests/exam-word-stitch-smoke.js`: PASS.
- `git diff --check`: không chạy được vì `git` không có trong PATH.

Không commit, push hoặc deploy. `docs/handoff/PLAN.md` không bị sửa.
