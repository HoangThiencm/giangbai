# VERIFY: Khắc Phục Lỗi Nhận Diện Câu 13 Đúng/Sai (CV 7991) Giữa Tạo Bài Tập và Thi Trực Tuyến

## Kết luận
PASS

## Đối chiếu scope
- [x] `thitructuyen.html`: Loại bỏ triệt để tiêu đề và hướng dẫn phần Phần III (`Thí sinh trả lời từ câu 14 đến câu 17...`) ở cuối block và ở ý d của câu 13.
- [x] `thitructuyen.html`: Nhận diện Đúng/Sai đa tầng (`importedAnswerKeyTfList`, cụm `Xét tính đúng/sai`, nhãn a–d / A–D). Tự động ánh xạ nhãn A–D sang a–d nếu câu là Đúng/Sai.
- [x] `taobaitap.html` & `backupcode viettailieu/taobaitap.html`: Nút `LaTeX` (`exportWordLatex`) và `Xuất Word` (`exportWord`) xuất đủ 4 ý `a)`, `b)`, `c)`, `d)` cho câu hỏi Đúng/Sai CV 7991; không bị rụng ý c, d và không còn bảng 2 cột A, B.
- [x] Không mở rộng scope ngoài PLAN. Không sửa logic chấm điểm hay giao diện học sinh.

## Test đã chạy
1. `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js` — PASS 100% (cả 9/9 test: TEST 0 đến TEST 8)
2. `node tests/taobaitap-plan-smoke.js` — PASS 100%
3. `node tests/smartquiz-smoke.js` — PASS 100%
4. `node tests/thitructuyen-cv7991-answerkey-smoke.js` — PASS 100% (cả 8/8 test)

## Pass / Fail từng tiêu chí
1. **Tiêu chí 1 (Xuất Word giữ đủ 4 ý)**: PASS. `exportWordLatex` và `exportWord` xuất trọn vẹn 4 ý `a) ... d)` cho câu Đúng/Sai CV 7991.
2. **Tiêu chí 2 (Ý d sạch sẽ, không dính hướng dẫn Phần III)**: PASS. Dòng `Thí sinh trả lời từ câu 14 đến câu 17...` bị cắt sạch khỏi ý d câu 13.
3. **Tiêu chí 3 (Ánh xạ nhãn A-D sang Đúng/Sai)**: PASS. File Word cũ dùng nhãn A-D kèm cụm "Xét tính đúng/sai" hoặc bảng đáp án Đúng/Sai được nhận diện chuẩn thành `type: "tf"` 4 ý a-d.
4. **Tiêu chí 4 (Nhận diện exam_format = cv7991)**: PASS. Đề 17 câu (12 MC + 1 TF 4 ý + 4 TLN) tự động nhận diện chuẩn `cv7991`.
5. **Tiêu chí 5 (Toàn bộ test suite pass)**: PASS 100%.

## Bug
Không phát hiện bug mới.
