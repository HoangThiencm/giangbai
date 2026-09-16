# Báo cáo triển khai: Nạp 13.Đúng / 14.Sai vào câu MC A. Đúng, B. Sai

## Đã thực hiện

- `thitructuyen.html`
  - `applyImportedAnswerToQuestion`: khi câu `mc` nhận đáp án Đúng/Sai (không phải A–D), chọn phương án chứa "Đúng"/"Sai" trong `q.options` (mặc định index 0 / 1).
  - `parseLatexWordQuiz`: nếu khóa đáp án là Đúng/Sai chứ không phải A–D, gán `correct_index` tương ứng (0 = A. Đúng, 1 = B. Sai).
  - MC 4 lựa chọn A–D vẫn map theo chữ cái như cũ.
- `tests/thitructuyen-cv7991-answerkey-smoke.js`: thêm TEST 8 cho câu 2 lựa chọn A. Đúng / B. Sai.

## Kiểm thử

- `node tests/thitructuyen-cv7991-answerkey-smoke.js`: PASS (8/8, gồm 13.Đúng → index 0, 14.Sai → index 1).

Không commit, push hoặc deploy. `docs/handoff/PLAN.md` không bị sửa.
