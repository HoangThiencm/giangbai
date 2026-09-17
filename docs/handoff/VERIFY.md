# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Đã đối chiếu đúng và đủ theo `docs/handoff/PLAN.md` và `docs/handoff/IMPLEMENT.md`:
  + Cấu trúc đề chuẩn CV 7991 gồm đúng 17 câu (10.0 điểm):
    * Phần I: 12 câu trắc nghiệm 4 lựa chọn A, B, C, D (6.0 điểm).
    * Phần II: 1 câu Đúng/Sai gồm 1 ngữ cảnh chung và 4 mệnh đề a), b), c), d) (2.0 điểm).
    * Phần III: 4 câu trả lời ngắn chỉ điền số kết quả (2.0 điểm).
  + `taobaitap.html`:
    * Khóa số câu 17 khi chọn hình thức CV 7991.
    * Prompt AI sinh chuẩn 1 câu TF 4 ý và 4 câu TLN chỉ chứa số kết quả.
    * Hàm chuẩn hóa `normalizeQuizItems` và `formatQuizAnswer` hỗ trợ câu TF 4 ý và làm sạch đáp án số TLN.
    * `ContentEditor` và danh sách xem lại câu hỏi hỗ trợ sửa và xem trực quan 4 ý a–d cùng nút Đúng/Sai.
    * `exportWordCV7991` và `exportTextCV7991` xuất mỗi phương án trên từng dòng `<p class="option">` và tự động bổ sung khối `BẢNG ĐÁP ÁN` chuẩn ở cuối tài liệu.
  + `thitructuyen.html`:
    * `normalizeImportedQuizText` tiền xử lý tách tab `\t` và khoảng trắng kép trước nhãn phương án `A–D` / `a–d` thành dòng mới, chống mất phương án B, D khi đọc bảng Word từ Mammoth.
    * `parseLatexWordQuiz` nhận diện đúng và đủ 17 câu: 12 MC, 1 TF (4 ý kèm mảng 4 boolean `correct_answers`), 4 TLN số (`correct_answer`).
    * Tự động nhận diện `exam_format = "cv7991"` khi nạp đề.
    * Cắt sạch bảng đáp án khỏi đề thi hiển thị cho học sinh.
  + Backend: Giữ nguyên cơ chế tự động scale điểm (`tf_scale = 2.0`) đảm bảo thang điểm 10.0.

## Test đã chạy
1. `tests/cv7991-taobaitap-thitructuyen-sync-smoke.js`:
   - Kiểm tra giao diện và prompt `taobaitap.html` khóa cấu trúc 17 câu.
   - Kiểm tra `normalizeQuizItems` đồng bộ TF 4 ý và lọc đáp án TLN dạng số.
   - Kiểm tra `buildCv7991ExportText` và nạp vào parser `thitructuyen.html` nhận đủ 17 câu.
   - Kiểm tra `buildCv7991ExportHtml` nạp vào parser `thitructuyen.html` nhận đủ 17 câu và đáp án.
   - Kiểm tra xử lý tab/khoảng trắng không làm rơi phương án B, D.
   - Kiểm tra `getImportedAnswerKey` bóc tách trọn vẹn 17 cặp đáp án (12 MC, 1 TF 4 ý, 4 TLN).
2. `tests/thitructuyen-cv7991-answerkey-smoke.js`: Đảm bảo tương thích ngược với các đề cũ.
3. `tests/taobaitap-plan-smoke.js`: Đảm bảo các chức năng OCR và xuất Word cơ bản không bị ảnh hưởng.
4. Kiểm tra cấu trúc tĩnh và regex trên mã nguồn thực tế `taobaitap.html` và `thitructuyen.html`.

## Pass / Fail từng tiêu chí
- [x] Tiêu chí 1: Đề thi CV 7991 chuẩn 17 câu (12 MC + 1 TF 4 ý + 4 TLN số = 10.0đ) — PASS
- [x] Tiêu chí 2: `taobaitap.html` xuất file Word (.docx) và Text (.txt) có BẢNG ĐÁP ÁN ở cuối — PASS
- [x] Tiêu chí 3: `thitructuyen.html` import file Word bóc tách đủ 17 câu, không bị nuốt phương án B, D — PASS
- [x] Tiêu chí 4: Nhận diện tự động toàn bộ đáp án của 12 MC, 1 TF 4 ý, 4 TLN số — PASS
- [x] Tiêu chí 5: Khối bảng đáp án được cắt khỏi nội dung đề thi hiển thị cho học sinh — PASS
- [x] Tiêu chí 6: Tương thích hoàn toàn với hệ thống chấm điểm backend — PASS

## Bug
Không có.
