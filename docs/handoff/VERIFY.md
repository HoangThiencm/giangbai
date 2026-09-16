# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Đã sửa triệt để lỗi Modal **Nạp Đáp Án Nhanh** theo đúng `PLAN.md`:
  1. `handleManualImport` trong `AnswerImportModal`: dùng `parseManualImportedAnswers(textInput)` thông qua parser chuẩn hóa `getImportedAnswerKey`, trích xuất đầy đủ 18 câu (MC, TF, Short Answer).
  2. `handleBulkAnswer`: gọi `applyImportedAnswerToQuestion` để gán chính xác `correct_index` cho câu `mc`, `correct_answers` cho câu `tf`, và `correct_answer` cho câu `short_answer`.
  3. Giữ tương thích hoàn toàn cho luồng nạp đáp án từ ảnh qua AI (`{ index, answer }`).

## Test đã chạy
1. `node tests/thitructuyen-cv7991-answerkey-smoke.js` (PASS 100% 7/7 test cases):
   - [TEST 1] `getImportedAnswerKey` nhận đủ 18 cặp đáp án mẫu (1..12 MC, 13 Đúng, 14 Sai, 15..18 Short Answer).
   - [TEST 2] `parseLatexWordQuiz` parse 18 câu đề mẫu đầy đủ đáp án 3 phần.
   - [TEST 3] Câu Đúng/Sai nhiều ý phụ (`a.Đúng b.Sai...`, `Đ, S, Đ, S`) lấy đúng `correct_answers`.
   - [TEST 4] Đề trắc nghiệm thuần và định dạng cũ `1C 2B` giữ nguyên tính tương thích.
   - [TEST 5] Số thập phân `3.14` và phân số `-1/2` không bị nhầm số thứ tự câu.
   - [TEST 6] `stripImportedAnswerKey` cắt bỏ bảng đáp án hỗn hợp sạch sẽ.
   - [TEST 7] Modal Nạp Đáp Án: `handleManualImport` + `handleBulkAnswer` nạp đủ 18 câu (12 MC, 2 TF, 4 TLN) và đẩy dữ liệu đáp án vào toàn bộ danh sách câu hỏi.
2. `node tests/exam-word-stitch-smoke.js` (PASS 100%).

## Pass / Fail từng tiêu chí
- [PASS] Nhập qua Modal "Nạp Đáp Án" nhận diện và gán đủ 12 câu trắc nghiệm A-D (`correct_index`).
- [PASS] Nhập qua Modal "Nạp Đáp Án" nhận diện và gán đủ 2 câu Đúng/Sai (`correct_answers`).
- [PASS] Nhập qua Modal "Nạp Đáp Án" nhận diện và gán đủ 4 câu Trả lời ngắn (`correct_answer`).
- [PASS] Nhập qua file Word LaTeX tự động nhận diện cả 3 phần CV 7991.

## Bug
Không có.
