# VERIFY

## Kết luận
FAIL

## Đối chiếu scope
- Việc nạp đáp án tự động từ file Word (`parseLatexWordQuiz`) đã nhận diện được, NHƯNG tính năng **Nạp Đáp Án Nhanh** qua Modal trên giao diện (`AnswerImportModal` & `handleBulkAnswer`) vẫn dùng logic cũ:
  1. `handleManualImport` chỉ dùng regex `/(\d+)[\.\-\:\s]*([A-D])/g` để lọc chữ cái A-D.
  2. `handleBulkAnswer` chỉ ánh xạ `correct_index` (A-D) mà không gán `correct_answers` cho câu Đúng/Sai (`tf`) và `correct_answer` cho câu Trả lời ngắn (`short_answer`).

## Test đã chạy
- Kiểm tra luồng UI Modal "Nạp Đáp Án":
  + Khi dán chuỗi: `1.B ... 12.C 13.Đúng 14.Sai 15.27 16.2000 17.100 18.30` vào ô Nhập tay của Modal "Nạp Đáp Án", `handleManualImport` chỉ lọc ra 12 câu trắc nghiệm (1..12).
  + Câu 13, 14 (Đúng/Sai) và câu 15, 16, 17, 18 (Trả lời ngắn) bị bỏ qua hoàn toàn, không được đẩy vào câu hỏi.

## Pass / Fail từng tiêu chí
- [PASS] Nhận diện bảng đáp án trong file Word LaTeX (`parseLatexWordQuiz`).
- [FAIL] Nạp đáp án thủ công qua Modal "Nạp Đáp Án Nhanh" (`AnswerImportModal` -> `handleManualImport` -> `handleBulkAnswer`).

## Bug
- Lỗi: Modal "Nạp Đáp Án Nhanh" (`AnswerImportModal`) chỉ nhận 12 câu trắc nghiệm A-D, không nhận diện và không đẩy đáp án vào các câu Đúng/Sai và Trả lời ngắn.
- Tái hiện:
  1. Vào trang `thitructuyen.html`, tạo hoặc mở đề có đủ 18 câu theo cấu trúc CV 7991 (12 câu MC, 2 câu TF, 4 câu Trả lời ngắn).
  2. Bấm nút **"Nạp Đáp Án"** ở thanh công cụ góc trên.
  3. Dán chuỗi đáp án mẫu vào ô Nhập tay:
     ```text
     1.B   2.C   3.A   4.B   5.C   6.B   7.A   8.D   9.B   10.C   11.C   12.C   
     13.Đúng   14.Sai   
     15.27	16.2000   17.100   18.30
     ```
  4. Bấm "Lưu Đáp Án" -> Chỉ 12 câu trắc nghiệm có đáp án, câu 13, 14, 15, 16, 17, 18 vẫn trống.
- File liên quan:
  + `thitructuyen.html` (tại `AnswerImportModal` dòng ~1012 và `handleBulkAnswer` dòng ~2006).
