# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Khớp 100% yêu cầu trong `PLAN.md`:
  + Nâng cấp `applyImportedAnswerToQuestion` và `parseLatexWordQuiz` trong `thitructuyen.html` để nhận diện đáp án Đúng/Sai (`13.Đúng`, `14.Sai`) cho các câu hỏi trắc nghiệm (`type: "mc"`) có 2 lựa chọn A. Đúng / B. Sai.
  + Tự động chọn phương án **A. Đúng** (`correct_index = 0`) khi đáp án là "Đúng", và **B. Sai** (`correct_index = 1`) khi đáp án là "Sai".
  + Đảm bảo các câu trắc nghiệm 4 lựa chọn A-D và câu Đúng/Sai 4 ý (a, b, c, d) không bị ảnh hưởng.

## Test đã chạy
1. `node tests/thitructuyen-cv7991-answerkey-smoke.js` (PASS 100% 8/8 test cases):
   - [TEST 1] `getImportedAnswerKey` nhận đủ 18 cặp đáp án mẫu.
   - [TEST 2] `parseLatexWordQuiz` parse 18 câu đề mẫu đầy đủ đáp án 3 phần.
   - [TEST 3] Câu Đúng/Sai 4 ý phụ (`a.Đúng b.Sai...`, `Đ, S, Đ, S`) lấy đúng `correct_answers`.
   - [TEST 4] Đề trắc nghiệm thuần và định dạng cũ `1C 2B` giữ nguyên tính tương thích.
   - [TEST 5] Số thập phân `3.14` và phân số `-1/2` không bị nhầm số thứ tự câu.
   - [TEST 6] `stripImportedAnswerKey` cắt bỏ bảng đáp án hỗn hợp sạch sẽ.
   - [TEST 7] Modal Nạp Đáp Án: `handleManualImport` + `handleBulkAnswer` nạp đủ 18 câu (12 MC, 2 TF, 4 TLN).
   - [TEST 8] Câu trắc nghiệm 2 lựa chọn A. Đúng / B. Sai nhận chính xác `13.Đúng` -> chọn A (index 0), `14.Sai` -> chọn B (index 1).
2. `node tests/exam-word-stitch-smoke.js` (PASS 100%).

## Pass / Fail từng tiêu chí
- [PASS] Nhập qua Modal "Nạp Đáp Án" nhận diện và gán đủ 12 câu trắc nghiệm A-D.
- [PASS] Nhập qua Modal "Nạp Đáp Án" tự động chọn A. Đúng cho `13.Đúng` và B. Sai cho `14.Sai` ở câu trắc nghiệm 2 phương án Đúng/Sai.
- [PASS] Nhập qua Modal "Nạp Đáp Án" nhận diện và gán đủ 4 câu Trả lời ngắn.
- [PASS] Nhập qua file Word LaTeX tự động nhận diện cả 3 phần.

## Bug
Không có.
