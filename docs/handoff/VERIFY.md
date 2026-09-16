# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Khớp 100% yêu cầu trong `PLAN.md`:
  + Cập nhật `getImportedAnswerKey`, `stripImportedAnswerKey` và `parseLatexWordQuiz` trong `thitructuyen.html` để nhận diện bảng đáp án hỗn hợp CV 7991 (Trắc nghiệm A-D, Đúng/Sai, Trả lời ngắn số/chuỗi).
  + Giữ nguyên thuật toán chấm điểm và định dạng đề thi trắc nghiệm cũ.
  + Thêm test tự động `tests/thitructuyen-cv7991-answerkey-smoke.js`.

## Test đã chạy
1. `node tests/thitructuyen-cv7991-answerkey-smoke.js` (PASS 100% 6/6 test cases):
   - [TEST 1] `getImportedAnswerKey` nhận đủ 18 cặp đáp án mẫu (1..12 MC, 13 Đúng, 14 Sai, 15..18 Short Answer: 27, 2000, 100, 30).
   - [TEST 2] `parseLatexWordQuiz` parse 18 câu đề mẫu đầy đủ đáp án 3 phần, bảng đáp án tự động cắt khỏi nội dung đề.
   - [TEST 3] Câu Đúng/Sai nhiều ý phụ (`a.Đúng b.Sai...`, `Đ, S, Đ, S`) ánh xạ chính xác `correct_answers`.
   - [TEST 4] Đề trắc nghiệm thuần và định dạng cũ `1C 2B` không bị xáo trộn.
   - [TEST 5] Số thập phân `3.14` và phân số `-1/2` không bị nhầm thành số thứ tự câu.
   - [TEST 6] `stripImportedAnswerKey` cắt bỏ bảng đáp án hỗn hợp ở cuối văn bản sạch sẽ.
2. `node tests/exam-word-stitch-smoke.js` (PASS 100%).

## Pass / Fail từng tiêu chí
- [PASS] Tự động nhận diện chính xác 100% các câu trắc nghiệm (1..12: B, C, A, B, C, B, A, D, B, C, C, C).
- [PASS] Tự động nhận diện câu Đúng/Sai (13: Đúng, 14: Sai).
- [PASS] Tự động nhận diện các câu Trả lời ngắn (15: 27, 16: 2000, 17: 100, 18: 30).
- [PASS] Không làm xáo trộn các định dạng đề thi cũ (100% trắc nghiệm thuần).

## Bug
Không có.
