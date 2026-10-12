# PLAN: Bổ sung tính năng tạo đề thi từ Ma trận và Bản đặc tả trong mục Tạo bài tập (TROLYTHIEN/2_TAO_BAI_TAP)

## Hiện trạng
1. **Quy trình tương tác hiện tại của Trợ lý Hoàng Thiên (`/thien`):**
   - Menu Cấp 1 có mục "3/ Tạo bài tập" tương ứng với thư mục nghiệp vụ `TROLYTHIEN/2_TAO_BAI_TAP/`.
   - Khi chọn mục này, hệ thống hiển thị Menu Cấp 2 với 10 định dạng bài tập (CV 7991, 100% trắc nghiệm, game, OLM/Azota, đề 15 phút, tự luận, bài dạy HTML, cắt PDF SGK).
   - Chưa có lựa chọn chuyên biệt cho phép giáo viên tạo đề thi tự động bám sát file Ma trận & Bản đặc tả.
2. **Học liệu thực tế giáo viên cung cấp:**
   - Tại `TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/12.10/`, giáo viên đã tải lên 2 file mẫu chuẩn:
     + `MA TRẬN - BẢN ĐẶC TẢ - GIỮA KÌ 1 - TOÁN 8 - 2026-2027.docx` (Khung ma trận + Bản đặc tả môn Toán 8 kết hợp TN + TL).
     + `MH (26-27)-MA TRẬN GIỮA HK1-Toan-9.docx` (Khung ma trận + Bản đặc tả môn Toán 9 theo định dạng CV 7991).
   - **Yêu cầu bổ sung của giáo viên:**
     + Hỗ trợ linh hoạt đường dẫn đầu vào (chỉ định thư mục/file bất kỳ hoặc quét mặc định trong `Dau_vao/`).
     + Làm rõ về cấu trúc đề: Hệ thống tự động nhận diện cả 3 dạng cấu trúc chuẩn (CV 7991, TN + TL kết hợp, 100% TL) trực tiếp từ ma trận, đồng thời tiếp nhận file cấu trúc/đề mẫu riêng của trường nếu giáo viên cung cấp thêm.
3. **Thiếu hụt tài liệu quy chuẩn và công cụ trích xuất:**
   - Trong `TROLYTHIEN/2_TAO_BAI_TAP/`, hiện có `QUY_CHUAN_TRON_DE.md`, `HUONG_DAN_CAT_PDF_SGK.md`, nhưng chưa có Master Prompt và Hướng dẫn nghiệp vụ chuyên sâu về quy trình đọc ma trận, trích xuất Yêu cầu cần đạt từ bản đặc tả, và sinh đề thi chuẩn 3 phần (Đề, Đáp án, Hướng dẫn chấm) bằng Word Equation OMML.
   - Chưa có script engine tự động phân tích và trích xuất bảng biểu ma trận từ các file Word `.docx` đầu vào.

## Phạm vi
1. **Cập nhật Menu & Quy tắc Sư phạm Trợ lý Thiên:**
   - Bổ sung lựa chọn số 11 vào Menu Cấp 2 của "Tạo bài tập" trong `.agents/workflows/thien.md` và `.agents/rules/tro-ly-thien.md`:
     `11. 📋 Tạo đề thi từ Ma trận & Bản đặc tả (Tự động đọc .docx trong Dau_vao hoặc thư mục chỉ định)`
   - Bổ sung quy định chi tiết về nghiệp vụ tạo đề từ ma trận & bản đặc tả vào cả 2 file quy tắc trên, bao gồm cơ chế tiếp nhận đường dẫn thư mục tùy biến từ người dùng.
2. **Biên soạn Quy chuẩn Master Prompt chuyên sâu:**
   - Tạo file `TROLYTHIEN/2_TAO_BAI_TAP/HUONG_DAN_TAO_DE_THI_TU_MA_TRAN.md` đóng vai trò Master Prompt chuẩn mực cho việc sinh đề thi từ Ma trận và Bản đặc tả:
     + **Cơ chế nạp file linh hoạt:** Hỗ trợ quét thư mục mặc định `TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/` (bao gồm đệ quy thư mục con) HOẶC đọc trực tiếp từ bất kỳ thư mục/đường dẫn cụ thể nào do giáo viên chỉ định trong chat.
     + **Tự động nhận diện cấu trúc đề (Không bắt buộc giáo viên đưa đề mẫu):**
       * *Dạng 1 (Theo Công văn 7991):* Đủ 3 phần: Phần I (Trắc nghiệm nhiều lựa chọn A, B, C, D); Phần II (Trắc nghiệm Đúng/Sai, barem 0.1 - 0.25 - 0.5 - 1.0đ); Phần III (Trắc nghiệm trả lời ngắn).
       * *Dạng 2 (Kết hợp TN 4 lựa chọn + Tự luận):* Trắc nghiệm khách quan chuẩn và Tự luận có thang điểm từng câu theo ma trận (như mẫu Toán 8 thực tế).
       * *Dạng 3 (100% Tự luận):* Bám sát các đơn vị kiến thức và Yêu cầu cần đạt của ma trận, có hướng dẫn chấm chi tiết từng bước.
       * *Khi có đề mẫu riêng của trường:* Hệ thống ưu tiên kế thừa tiêu đề, header, định dạng bảng điểm từ đề mẫu của trường.
     + Nguyên tắc sinh câu hỏi bám sát 100% Yêu cầu cần đạt, tuân thủ giới hạn kiến thức cấp học GDPT 2018 (không dùng $\Leftrightarrow$, không dùng tập nghiệm $S$, chuẩn hóa công thức LaTeX).
     + Kỹ thuật xuất Word Equation OMML (`m:oMath`) qua engine `latex_to_omml`, tuyệt đối không để trần ký hiệu `$x^2$` hay dán ảnh công thức.
     + Đầu ra hoàn chỉnh gồm 3 phần độc lập trong file Word `.docx`: (1) Đề kiểm tra chuẩn A4 trang trọng THCS Trần Phú; (2) Ma trận đối chiếu và bảng đáp án; (3) Hướng dẫn chấm & Thang điểm chi tiết từng bước.
3. **Xây dựng Script Engine phân tích Ma trận & Bản đặc tả:**
   - Tạo script `TROLYTHIEN/engine/doc_ma_tran_dac_ta.py` sử dụng `python-docx`:
     + Hỗ trợ tham số đường dẫn thư mục hoặc tệp chỉ định (CLI argument hoặc gọi qua hàm).
     + Tự động bóc tách các bảng trong file `.docx` đầu vào thành cấu trúc dữ liệu JSON/Dict có cấu trúc (chủ đề, đơn vị kiến thức, mức độ, yêu cầu cần đạt, dạng câu, số điểm).
4. **Đồng bộ ứng dụng Desktop (`app_trolythien`):**
   - Bổ sung ánh xạ trong `BUNDLE_MAP` (`app_trolythien/core/prompt_builder.py`) nếu cần đồng bộ tri thức đóng gói.
5. **Kiểm thử tự động:**
   - Tạo bộ test `tests/trolythien-tao-de-ma-tran-smoke.py` kiểm thử khả năng đọc và bóc tách chính xác từ cả thư mục mặc định và thư mục tùy biến (như `Dau_vao/12.10/`).
   - Đảm bảo toàn bộ test hiện có (`test_verify_dekiemtra.py`) tiếp tục PASS 100%.

## Ngoài phạm vi
- Không chỉnh sửa các định dạng bài tập từ 1 đến 10 hiện có.
- Không can thiệp vào các mô-đun khác ngoài phân hệ Tạo bài tập / Đề kiểm tra.
- Không sửa mã nguồn trong lượt khảo sát này (Antigravity IDE chỉ lập PLAN và khóa LOCK).

## File dự kiến tác động
1. `.agents/workflows/thien.md`: Bổ sung lựa chọn 11 vào menu cấp 2 và kịch bản thực thi linh hoạt đường dẫn.
2. `.agents/rules/tro-ly-thien.md`: Cập nhật menu cấp 2 và quy chuẩn nghiệp vụ cho lựa chọn 11.
3. `TROLYTHIEN/2_TAO_BAI_TAP/HUONG_DAN_TAO_DE_THI_TU_MA_TRAN.md`: Master Prompt và quy chuẩn kỹ thuật sinh đề thi từ ma trận & bản đặc tả (tự động nhận diện cấu trúc đề, hỗ trợ thư mục tùy định).
4. `TROLYTHIEN/engine/doc_ma_tran_dac_ta.py`: Script bóc tách bảng ma trận và bản đặc tả từ file `.docx` theo đường dẫn chỉ định hoặc mặc định.
5. `app_trolythien/core/prompt_builder.py`: Cập nhật `BUNDLE_MAP` ánh xạ tri thức mới.
6. `tests/trolythien-tao-de-ma-tran-smoke.py`: Bộ kiểm thử tự động cho tính năng mới.

## Các bước thực hiện
1. **Bước 1: Cập nhật Menu Cấp 2 và Quy chuẩn Sư phạm Trợ lý Thiên**
   - Trong `.agents/workflows/thien.md`:
     + Thêm `11. 📋 Tạo đề thi từ Ma trận & Bản đặc tả (Tự động đọc .docx trong Dau_vao hoặc thư mục chỉ định)` vào `ask_question` của Nhánh 3.
     + Thêm hướng dẫn quy trình kích hoạt khi chọn mục 11: cho phép giáo viên dán đường dẫn thư mục tùy chọn hoặc dùng mặc định.
   - Trong `.agents/rules/tro-ly-thien.md`:
     + Cập nhật danh sách 11 lựa chọn tại mục 3 (Menu Cấp 2 khi chọn Tạo bài tập).
     + Thêm mục quy chuẩn nghiệp vụ chi tiết cho tính năng Tạo đề thi từ Ma trận & Bản đặc tả (hỗ trợ đọc thư mục do người dùng chỉ định).
2. **Bước 2: Xây dựng Master Prompt `HUONG_DAN_TAO_DE_THI_TU_MA_TRAN.md`**
   - Tạo file trong `TROLYTHIEN/2_TAO_BAI_TAP/` quy định đầy đủ:
     + Cơ chế nhận diện dữ liệu đầu vào: Ưu tiên đường dẫn thư mục giáo viên chỉ định trong câu lệnh/chat; nếu không chỉ định thì quét đệ quy `TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/` (bao gồm các thư mục con theo ngày như `12.10/`).
     + Tự động nhận diện dạng đề từ chính file ma trận (CV 7991, TN + TL, 100% TL). Nếu giáo viên đưa thêm file đề mẫu của trường, kế thừa header và mẫu trình bày.
     + Bóc tách Bản đặc tả: Ghép nối 1-1 từng câu hỏi với Yêu cầu cần đạt.
     + Quy tắc biên soạn đề thi GDPT 2018: Độ khó phân tầng chuẩn mực, không dùng kiến thức cấp trên, chuẩn hóa toàn bộ công thức toán LaTeX.
     + Quy cách xuất file Word: Dùng `latex_to_omml` chèn công thức Word Equation (`m:oMath`), bố cục bảng điểm, khung thông tin học sinh trang trọng, bảng đáp án và thang điểm chi tiết.
     + Vị trí lưu kết quả: Mặc định lưu tại `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/De_Kiem_Tra_[Mon]_[Lop]_[KyThi].docx` (hoặc thư mục kết quả tương ứng nếu người dùng chỉ định).
3. **Bước 3: Xây dựng Script Engine `doc_ma_tran_dac_ta.py`**
   - Tạo `TROLYTHIEN/engine/doc_ma_tran_dac_ta.py`:
     + Hỗ trợ nhận tham số đường dẫn thư mục/file từ dòng lệnh `--input-dir` hoặc `--file`.
     + Hàm `quet_file_dau_vao(input_path=None)`: Tìm kiếm thông minh các file `.docx` ma trận trong thư mục chỉ định hoặc thư mục mặc định.
     + Hàm `phan_tich_ma_tran_dac_ta(docx_path)`: Đọc qua các `table` trong `.docx`, nhận diện bảng ma trận và bảng đặc tả bằng heuristic (từ khóa: chủ đề, nội dung, yêu cầu cần đạt, nhận biết, thông hiểu, vận dụng, câu hỏi, điểm).
     + Trả về cấu trúc JSON sạch chứa đầy đủ thông tin để phục vụ sinh đề.
4. **Bước 4: Cập nhật `BUNDLE_MAP` trong `app_trolythien/core/prompt_builder.py`**
   - Bổ sung cặp ánh xạ tài liệu quy chuẩn mới vào `BUNDLE_MAP` và `REQUIRED_PROMPTS` nếu cần đồng bộ cho ứng dụng Desktop.
5. **Bước 5: Viết bộ kiểm thử tự động và xác minh**
   - Tạo `tests/trolythien-tao-de-ma-tran-smoke.py`:
     + Kiểm thử đọc và parse thành công với đường dẫn chỉ định cụ thể (`TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/12.10/`).
     + Kiểm thử đọc với đường dẫn mặc định (`TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/`).
     + Kiểm chứng cấu trúc JSON trích xuất có đủ số câu, mức độ và yêu cầu cần đạt.
   - Chạy test xác nhận PASS toàn bộ.

## Rủi ro
- **Rủi ro 1:** Đường dẫn người dùng chỉ định chứa khoảng trắng, ký tự tiếng Việt hoặc đường dẫn tương đối không tồn tại.
  -> **Giải pháp:** Engine xử lý chuẩn hóa đường dẫn bằng `pathlib.Path().resolve()`, kiểm tra `is_dir()` / `is_file()` an toàn và thông báo rõ ràng nếu đường dẫn không hợp lệ.
- **Rủi ro 2:** Định dạng bảng Ma trận và Bản đặc tả có sự khác biệt giữa các trường hoặc các năm học (cấu trúc gộp ô, tên cột khác biệt nhẹ).
  -> **Giải pháp:** Engine phân tích áp dụng cơ chế nhận diện từ khóa mềm đa năng (fuzzy matching / heuristic regex), kết hợp trích xuất dòng dữ liệu an toàn.

## Cách kiểm thử
1. Chạy lệnh kiểm thử bộ phân tích ma trận (bao gồm cả test đường dẫn chỉ định):
   `python tests/trolythien-tao-de-ma-tran-smoke.py`
2. Chạy lệnh kiểm thử bộ đề kiểm tra hiện tại:
   `python tests/test_verify_dekiemtra.py`
3. Kiểm tra tính khớp 100% giữa danh sách menu trong `.agents/workflows/thien.md` và `.agents/rules/tro-ly-thien.md`.

## Tiêu chí nghiệm thu
1. Menu Cấp 2 của Tạo bài tập trong `/thien` có đúng 11 lựa chọn, gồm lựa chọn "11. 📋 Tạo đề thi từ Ma trận & Bản đặc tả (Tự động đọc .docx trong Dau_vao hoặc thư mục chỉ định)".
2. Master Prompt và Engine hỗ trợ trơn tru cả 2 chế độ: tự động quét thư mục mặc định `Dau_vao/` VÀ tiếp nhận đường dẫn thư mục do người dùng chỉ định.
3. Engine tự động nhận diện chính xác 3 dạng cấu trúc đề (CV 7991, TN + TL, 100% TL) từ ma trận và bản đặc tả mà không bắt buộc người dùng nạp đề mẫu. Nếu có đề mẫu riêng của trường, kế thừa chuẩn xác.
4. Engine `doc_ma_tran_dac_ta.py` đọc và trích xuất chính xác cấu trúc từ các file `.docx` thực tế trong `Dau_vao/12.10/`.
5. Toàn bộ smoke test liên quan PASS 100%, không gây xung đột với các tính năng khác.
