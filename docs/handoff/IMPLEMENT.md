# IMPLEMENT: Sửa nhận diện câu 13 Đúng/Sai (CV 7991) giữa Tạo Bài Tập và Thi Trực Tuyến

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

### `thitructuyen.html` — `parseLatexWordQuiz`
- Xóa triệt để tiêu đề/hướng dẫn phần ở cuối block: từ `PHẦN I|II|III` hoặc `Thí sinh trả lời...` đến hết block (không chỉ 1 dòng tiêu đề).
- Khi cắt từng ý TF, ý cuối (d) cũng được strip lần nữa nếu còn sót hướng dẫn phần.
- `isTF` đa tầng: `importedAnswerKeyTfList(answerKey[n])` + cụm `Xét tính đúng/sai` / đáp án đúng-sai.
- Nếu nhận diện Đúng/Sai nhưng file Word dùng nhãn A–D: ánh xạ A–D → a–d rồi parse như TF 4 ý.

### `taobaitap.html` — `exportWord` / `exportWordLatex`
- Khi `synthForm === 'cv7991'` hoặc đề có `isCv7991TrueFalseItem`: chuyển sang `buildCv7991ExportHtml` (đủ 4 ý `a)…d)`, không còn bảng A/B 2 cột).
- Nhánh generic vẫn in đủ 4 ý nếu gặp TF CV 7991.

### `backupcode viettailieu/taobaitap.html`
- Sửa tối thiểu nhánh `true-false` trong `exportWord` / `exportWordLatex`: khi đủ 4 ý (options ≥ 3 / subItems / correct_answers) in `a)…d)`.

### `tests/cv7991-taobaitap-thitructuyen-sync-smoke.js`
- TEST 6: ý d câu 13 không dính hướng dẫn Phần III.
- TEST 7: nhãn A–D + “Xét tính đúng/sai” → type `tf` a–d.
- TEST 8: nguồn `exportWord`/`exportWordLatex` (+ backup) đồng bộ CV 7991.

## Test đã chạy

- `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js` — PASS
- `node tests/taobaitap-plan-smoke.js` — PASS
- `node tests/smartquiz-smoke.js` — PASS
- `node tests/thitructuyen-cv7991-answerkey-smoke.js` — PASS (hồi quy parser)

Không mở rộng scope ngoài PLAN. Cần `/verify` trên Antigravity.
