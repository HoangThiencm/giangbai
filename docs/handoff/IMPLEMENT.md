# Báo cáo triển khai: Nạp đáp án hỗn hợp CV 7991 qua Modal

## Sửa theo VERIFY.md (FAIL)

- Lỗi: Modal **Nạp Đáp Án Nhanh** chỉ nhận 12 câu A–D, bỏ qua Đúng/Sai và Trả lời ngắn.
- `thitructuyen.html`
  - `handleManualImport` không còn regex `/(\d+)[\.\-\:\s]*([A-D])/g`.
  - Dùng `parseManualImportedAnswers(textInput)` → `getImportedAnswerKey("Đáp án:\n" + textInput)` để lấy MC, TF, trả lời ngắn.
  - `handleBulkAnswer` gọi `applyImportedAnswerToQuestion`:
    - `mc`: gán `correct_index` theo A–D.
    - `tf`: gán `correct_answers` từ `tfList` hoặc parse `Đúng`/`Sai` / `Đ, S, Đ, S`.
    - `short_answer`: gán `correct_answer`.
  - Giữ tương thích AI `{ index, answer }`.
- `tests/thitructuyen-cv7991-answerkey-smoke.js`: thêm TEST 7 mô phỏng `handleManualImport` + `handleBulkAnswer` với 18 câu mẫu.

## Kiểm thử

- `node tests/thitructuyen-cv7991-answerkey-smoke.js`: PASS (gồm TEST 7: 12 MC, 2 TF, 4 TLN).

Không commit, push hoặc deploy. `docs/handoff/PLAN.md` không bị sửa.
