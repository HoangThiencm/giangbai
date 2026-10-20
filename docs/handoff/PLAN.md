# PLAN: Nâng cấp Phân hệ Duyệt đề (duyetde.html) theo 4 Trụ cột Chuyên môn Cốt lõi

## Hiện trạng
- Hệ thống hiện có trang `duyetde.html` ("Rà soát & Hiệu chỉnh Đề Kiểm Tra / Duyệt đề AI"), được hỗ trợ bởi 2 backend: `api/duyetde_ai.php` (xử lý AI gateway, xoay tua Gemini API key mã hóa) và `api/duyetde.php` (lưu trữ phiên làm việc `duyetde_sessions` trong MySQL).
- Giao diện hiện tại được xây dựng theo quy trình 5 bước phẳng, nhưng chưa làm nổi bật và tách bạch 4 nhu cầu cốt lõi của Tổ trưởng chuyên môn khi duyệt đề:
  1. **Kiểm tra Ma trận & Đặc tả:** Hiện chỉ bóc tách chỉ mục (`extract_matrix_index`) thô sơ, chưa có module kiểm toán tự động phát hiện lỗi ma trận (như tổng điểm lệch 10.0, sai tỉ lệ 40-30-20-10, các ô bị bỏ trống điểm/câu, ghép câu lai tạp số học - hình học) và chưa đối soát định lượng 1-1 giữa Khung Ma trận và Bản đặc tả.
  2. **Kiểm tra Đề GV nộp vs Ma trận & Tính chính xác nội dung:** Hiện bước `evaluate_exam` đánh giá chung chung, chưa phân tách rõ 2 tầng: Tầng 1 (Đối soát khớp ma trận từng câu theo `spec_id`) và Tầng 2 (Kiểm toán tính chính xác khoa học toán học: bài toán vô nghiệm, hình vẽ vi phạm hình học Euclid, vượt chuẩn GDPT 2018, bẫy thực tế gây hiểu nhầm).
  3. **Tạo đề kiểm tra mới theo Ma trận đã cho:** Hiện tại `duyetde.html` hoàn toàn chưa có tính năng sinh đề kiểm tra mới từ ma trận đã thẩm định (người dùng phải mở trang khác như `matrande.html` hoặc chạy script rời).
  4. **Xuất biên bản phản biện:** Hàm `exportMinutesDocx()` hiện tại chỉ xuất vài đoạn văn bản thô, chưa có bảng đối soát định lượng, chưa phân loại lỗi theo cấp độ sư phạm, chưa đạt chuẩn thể thức văn bản hành chính theo Nghị định 30/2020/NĐ-CP và mẫu phản biện thực tế của trường THCS Trần Phú (như trong `TROLYTHIEN/4_DUYET_DE/Ket_qua/Bien_Ban_Tham_Dinh_Ma_Tran_Toan_6_Giua_HKI_2026_2027.docx` và `Phan_Bien_De_Cuong_Toan_6.docx`).

## Phạm vi
Triển khai toàn diện 4 trụ cột nghiệp vụ trực tiếp trong Phân hệ Duyệt đề (`duyetde.html` & `api/duyetde_ai.php` & `api/duyetde.php`):

1. **Trụ cột 1: Kiểm tra Ma trận đã chính xác chưa? Bản đặc tả đã khớp với Ma trận hay chưa?**
   - Hỗ trợ nạp tệp Ma trận & Bản đặc tả (PDF, Word DOCX hoặc văn bản dán trực tiếp).
   - Tự động bóc tách và phân tích cấu trúc 2 bảng (`Khung Ma trận` và `Bản đặc tả`).
   - Tự động kiểm toán định lượng Ma trận:
     + Tổng điểm: Kiểm tra chính xác thang điểm 10.0 (phát hiện lệch điểm như ca mẫu 10.25đ hoặc 9.5đ).
     + Tỉ lệ 4 mức độ nhận thức: Nhận biết (40%), Thông hiểu (30%), Vận dụng (20%), Vận dụng cao (10%) (hoặc tỉ lệ do tổ cấu hình).
     + Cảnh báo các ô bị bỏ quên điểm, ô thiếu số lượng câu hỏi, ô ghép lai tạp (như câu VDC đặt trước câu NB).
   - Tự động đối soát 1-1 giữa Khung Ma trận và Bản đặc tả:
     + So khớp số câu hỏi từng mức độ nhận thức giữa 2 bảng.
     + So khớp điểm số từng chủ đề / đơn vị kiến thức giữa 2 bảng.
     + So khớp mô tả Yêu cầu cần đạt (YCCĐ) với phân bổ mức độ nhận thức.
   - Hiển thị trực quan: Bảng đối soát định lượng Ma trận & Đặc tả, danh sách Cảnh báo đỏ (Lỗi nghiêm trọng), Cảnh báo vàng (Bất cập sư phạm).

2. **Trụ cột 2: Kiểm tra Đề GV nộp có khớp với Ma trận hay không? Nội dung chính xác chưa?**
   - Nạp tệp Đề thi của giáo viên (kèm file Đáp án / Hướng dẫn chấm nếu có).
   - Kiểm tra đa tầng độc lập:
     + **Tầng 2.1 - Khớp Ma trận (Alignment):** Định vị từng câu hỏi vào đúng chỉ mục `spec_id`/slot ma trận; kiểm tra đúng chủ đề, đúng mức độ nhận thức (NB/TH/VD/VDC), đúng dạng câu (TNKQ 4 lựa chọn, Đúng/Sai có 4 ý a-b-c-d, Trả lời ngắn, Tự luận), đúng thang điểm quy định.
     + **Tầng 2.2 - Kiểm toán Tính chính xác Nội dung & Khoa học (Deep Content & Math Audit):**
       * Kiểm tra tính đúng đắn toán học: Phương trình/bài toán có nghiệm hay vô nghiệm (như bài BCNN trong khoảng hẹp), đa nghiệm; điều kiện xác định ($x \in \mathbb{N}^*$, mẫu số $\ne 0$); số đo hình học có tồn tại trên mặt phẳng Euclid (bộ ba số Pythagore, bất đẳng thức tam giác); tính toán đáp án độc lập.
       * Kiểm tra chuẩn chương trình GDPT 2018: Phát hiện kiến thức vượt cấp (ví dụ lớp 6 không dùng kiến thức lớp 7/8; không dùng ký hiệu chưa học $\Leftrightarrow$ hay tập nghiệm $S$).
       * Kiểm tra tính sư phạm & thời lượng: Trật tự câu hỏi (không để câu khó trước câu dễ gây ức chế tâm lý); bài toán thực tế có logic thực tế và không tạo bẫy giá tiền hòa vốn gây bối rối cho học sinh; ước lượng độ dài phù hợp với thời gian thi (ví dụ 60 phút / 90 phút).
   - Giao diện rà soát câu hỏi: Bảng phân loại trực quan (Đạt - Cần chỉnh sửa - Không đạt), hiển thị song song Câu gốc vs Câu đề xuất sửa, cho phép giáo viên chỉnh sửa trực tiếp và bấm "Kiểm tra lại câu sửa (Recheck)" độc lập từng câu tiết kiệm token.

3. **Trụ cột 3: Tạo đề kiểm tra theo Ma trận đã cho**
   - Tích hợp tính năng tạo đề thi mới trực tiếp từ Bảng chỉ mục Ma trận & Đặc tả đã thẩm định.
   - AI Engine sinh trọn bộ đề thi chuẩn mực bám sát 100% ma trận:
     + Sinh đúng 100% YCCĐ, đúng dạng thức câu và đúng số điểm từng câu.
     + Sinh đồng bộ: (1) Đề kiểm tra chuẩn A4; (2) Ma trận đối chiếu và Bảng đáp án; (3) Hướng dẫn chấm chi tiết kèm thang điểm từng bước (Rubric).
   - Cho phép xem trước trực quan với KaTeX công thức toán học sắc nét.
   - Hỗ trợ đổi câu hỏi đơn lẻ (Regenerate single question theo đúng `spec_id`) khi người dùng muốn đổi câu khác.
   - Xuất file Word `.docx` Đề thi hoàn chỉnh sẵn sàng in ấn.

4. **Trụ cột 4: Xuất biên bản phản biện chuyên môn**
   - Tổng hợp toàn diện kết quả thẩm định từ Trụ cột 1 (Ma trận/Đặc tả) và Trụ cột 2 (Đề thi GV nộp).
   - Tích hợp ý kiến kết luận, phân loại quyết định chính thức của Tổ trưởng chuyên môn (Có thể sử dụng / Cần chỉnh sửa / Không sử dụng).
   - Xuất file Word `.docx` Biên bản phản biện theo đúng thể thức văn bản hành chính (Nghị định 30/2020/NĐ-CP, font Times New Roman, dãn dòng 1.2, bảng biểu đóng khung kín 4 cạnh, chữ ký 3 bên: GV ra đề, Tổ trưởng chuyên môn, Ban Giám hiệu).
   - Nội dung biên bản gồm 5 phần chuẩn chuyên môn:
     + Phần I: Thông tin đợt thẩm định & Hồ sơ nộp.
     + Phần II: Kết quả đối soát định lượng Ma trận & Bản đặc tả (Bảng đối soát số câu, điểm, tỉ lệ % NB-TH-VD-VDC).
     + Phần III: Phân tích chi tiết các lỗi & bất cập chuyên môn (Lỗi logic/khoa học toán học, lỗi lệch ma trận, bất cập sư phạm, tính khả thi thời lượng).
     + Phần IV: Bảng tổng hợp đối chiếu Câu gốc vs Phương án chuẩn hóa đề xuất.
     + Phần V: Kết luận & Kiến nghị thẩm duyệt của Tổ trưởng chuyên môn (kèm chữ ký phê duyệt).
   - Cung cấp nút xem trước / sao chép văn bản Markdown `.md` biên bản phản biện.

## Ngoài phạm vi
- Không can thiệp vào các trang ứng dụng khác ngoài phân hệ duyệt đề (`soankhbd.html`, `canvas_soanbaigiang.html`, v.v.).
- Không tạo bảng CSDL mới trong MySQL; tiếp tục sử dụng bảng `duyetde_sessions` hiện tại với trường `session_data LONGTEXT` để lưu trữ đồng bộ trạng thái của 4 trụ cột.
- Không thay thế thao tác thẩm định con người; AI đóng vai trò Trợ lý chuyên môn phát hiện lỗi và đề xuất phương án chuẩn hóa.

## File dự kiến tác động
- `duyetde.html`: Tái cấu trúc thanh điều hướng và giao diện thành 4 Tab/Trụ cột nghiệp vụ rõ ràng, tích hợp quy trình thao tác mượt mà.
- `api/duyetde_ai.php`: Bổ sung action `audit_matrix_and_spec`, action `generate_exam_from_matrix`, tối ưu hóa prompt kiểm toán khoa học/sư phạm cho `evaluate_exam` và `recheck_question`.
- `api/duyetde.php`: Đảm bảo lưu và phục hồi đầy đủ dữ liệu 4 trụ cột trong `duyetde_sessions`.
- `tests/duyetde-4pillars-smoke.js`: Tạo kịch bản kiểm thử tự động toàn diện cho 4 trụ cột chức năng.

## Các bước thực hiện
1. **Bước 1 (Chuẩn bị Cấu trúc Dữ liệu & Backend AI):**
   - Cập nhật `api/duyetde_ai.php`:
     + Xây dựng action `audit_matrix_and_spec`: Nhận tệp ma trận & đặc tả, trả về bảng đối soát định lượng (số câu, số điểm, tỉ lệ thực tế vs quy định), phát hiện lỗi lệch tổng điểm, ô trống, lỗi lệch khớp giữa ma trận và đặc tả.
     + Tối ưu action `evaluate_exam`: Bổ sung kiểm toán chuyên sâu về toán học (bài toán vô nghiệm/đa nghiệm, số đo hình học vi phạm Euclid, công thức vượt chuẩn GDPT 2018, bẫy ngữ cảnh thực tế).
     + Xây dựng action `generate_exam_from_matrix`: Nhận bảng chỉ mục ma trận đã duyệt, sinh bộ đề mới 1-1 kèm bảng đáp án và hướng dẫn chấm chi tiết.
     + Cập nhật action `generate_single_question_by_spec`: Hỗ trợ đổi câu đơn lẻ theo chỉ mục `spec_id`.
2. **Bước 2 (Nâng cấp CSDL & Session Storage):**
   - Đảm bảo `api/duyetde.php` lưu trữ và khôi phục đầy đủ trạng thái của cả 4 trụ cột: `matrix_audit`, `exam_evaluation`, `generated_exam`, `review_minutes`, `final_decision`.
3. **Bước 3 (Thiết kế lại Giao diện người dùng trong `duyetde.html`):**
   - Thiết kế Header & Tab Navigation 4 Trụ cột rõ ràng:
     + **Tab 1: Thẩm định Ma trận & Bản đặc tả** (Nạp tệp -> Bóc tách -> Bảng đối soát định lượng & Cảnh báo đỏ/vàng).
     + **Tab 2: Thẩm định Đề thi GV nộp** (Nạp đề & đáp án -> Đối soát khớp ma trận -> Kiểm toán nội dung khoa học/sư phạm -> Duyệt & sửa từng câu).
     + **Tab 3: Tạo đề mới theo Ma trận** (Sinh bộ đề chuẩn 100% ma trận -> Xem trước KaTeX -> Đổi câu / Sửa câu -> Tải đề Word).
     + **Tab 4: Biên bản phản biện & Xuất báo cáo** (Tổng hợp toàn diện -> Kết luận Tổ trưởng -> Xuất file Word `.docx` chuẩn NĐ 30 & bản Markdown).
   - Giữ nguyên cơ chế bảo mật quản lý Gemini API Key xoay tua trên server.
4. **Bước 4 (Nâng cấp Bộ sinh File Word Biên bản phản biện):**
   - Viết lại hàm `exportMinutesDocx()` sử dụng thư viện `docx.js` trên client:
     + Chuẩn thể thức văn bản hành chính theo Nghị định 30/2020/NĐ-CP (Font Times New Roman 13pt/14pt, lề chuẩn, dãn dòng 1.2).
     + Bảng đối soát định lượng đóng khung kín 4 cạnh (`single border`, cell padding chuẩn).
     + Bảng tổng hợp câu hỏi: Câu gốc vs Câu đề xuất sửa, căn cứ ma trận, nhận xét chuyên môn.
     + Khung ký duyệt 3 bên trang trọng (Giáo viên ra đề, Tổ trưởng chuyên môn, Ban Giám hiệu).
5. **Bước 5 (Viết kịch bản Kiểm thử Tự động):**
   - Tạo file `tests/duyetde-4pillars-smoke.js` kiểm tra:
     + Bóc tách và kiểm toán ma trận phát hiện lỗi tổng điểm/tỉ lệ.
     + Kiểm toán đề thi phát hiện lỗi khoa học toán học và lỗi lệch ma trận.
     + Kiểm tra endpoint sinh đề theo ma trận.
     + Kiểm tra xuất biên bản phản biện có đầy đủ cấu trúc bảng và trường dữ liệu.
6. **Bước 6 (Kiểm định và Hoàn tất Tài liệu Handoff):**
   - Chạy toàn bộ test suite đảm bảo không phát sinh lỗi hồi quy.
   - Ghi nhận kết quả vào `docs/handoff/IMPLEMENT.md` và chuẩn bị cho bước `/verify`.

## Rủi ro
- *Rủi ro cấu trúc bảng phức tạp trong file PDF Ma trận/Đặc tả:* Xử lý bằng cách gửi song song văn bản trích xuất và bản PDF gốc nguyên dạng (inline data base64) cho Gemini Vision để nhận diện chuẩn xác các ô gộp (`rowspan`/`colspan`).
- *Rủi ro vượt ngưỡng thời gian (Timeout 180s) khi AI giải và kiểm toán đề dài:* Tách quy trình thành từng chặng độc lập (Chặng 1: Bóc tách & kiểm toán ma trận; Chặng 2: Giải đề; Chặng 3: Thẩm định đề; Chặng 4: Sinh đề mới), mỗi chặng có thanh tiến trình (Progress bar) rõ ràng.
- *Rủi ro Gemini API Rate Limit / Quota:* Tiếp tục tận dụng hệ thống xoay tua đa key (`call_gemini_with_rotation`) tự động chuyển sang key kế tiếp khi gặp mã lỗi 429 hoặc Resource Exhausted.
- *Rủi ro công thức toán học bị biến dạng khi xuất file Word:* Sử dụng KaTeX rendering trên giao diện và chuẩn hóa text/omml trong tệp Word xuất ra để đảm bảo công thức hiển thị sắc nét, không bị lỗi font.

## Cách kiểm thử
1. **Kiểm thử tự động bằng script:**
   ```bash
   node tests/duyetde-4pillars-smoke.js
   ```
2. **Kiểm thử tính năng trên giao diện (`duyetde.html`):**
   - **Tab 1:** Nạp tệp `TROLYTHIEN/4_DUYET_DE/Dau_vao/Ma_Tran__Giua_HKI_Toan_6_2026_2027.pdf`. Kiểm tra xem hệ thống có phát hiện ra:
     + Cột Thông hiểu bị bỏ trống điểm.
     + Điểm VDC ghi sai thành 1.0 làm tổng điểm đội lên 10.25đ.
     + Bảng đối soát định lượng tỉ lệ % có khớp với quy định không.
   - **Tab 2:** Nạp đề thi có câu BCNN vô nghiệm (khoảng 400 - 550) và bài toán hình học có câu khó đặt trước câu dễ. Kiểm tra xem AI có phát hiện đúng lỗi toán học vô nghiệm và cảnh báo sắp xếp sư phạm không.
   - **Tab 3:** Bấm "Tạo đề mới theo Ma trận". Kiểm tra đề sinh ra có đúng 100% số câu, điểm số và dạng thức của ma trận không. Thử bấm "Đổi câu hỏi" cho một câu cụ thể.
   - **Tab 4:** Chọn kết luận "Cần chỉnh sửa", nhập ý kiến chỉ đạo của Tổ trưởng, bấm "Xuất biên bản phản biện .docx". Mở tệp Word kiểm tra font Times New Roman, cấu trúc bảng 4 cạnh, các bảng đối soát và chữ ký phê duyệt.

## Tiêu chí nghiệm thu
- Giao diện `duyetde.html` có thanh điều hướng 4 Tab rõ ràng, trực quan, chuyên nghiệp.
- **Trụ cột 1:** Nhận diện được ma trận/đặc tả, tính toán và hiển thị bảng đối soát định lượng (số câu, số điểm, tỉ lệ %), chỉ ra các lỗi sai lệch tổng điểm, ô trống và lệch khớp giữa 2 bảng.
- **Trụ cột 2:** Thẩm định đề thi chỉ ra được câu lệch ma trận, câu sai toán học (vô nghiệm/vi phạm hình học/vượt chuẩn GDPT 2018), hiển thị câu gốc song song câu đề xuất sửa, tính năng Recheck 1 câu hoạt động chính xác.
- **Trụ cột 3:** Sinh được bộ đề kiểm tra mới hoàn chỉnh (đề thi + ma trận đối chiếu + hướng dẫn chấm chi tiết) bám sát 100% chỉ mục ma trận.
- **Trụ cột 4:** Xuất được file Word Biên bản phản biện chuyên môn `.docx` chuẩn thể thức Nghị định 30/2020/NĐ-CP với đầy đủ các bảng đối soát định lượng và ý kiến phê duyệt của Tổ trưởng chuyên môn.
- Script kiểm thử tự động `tests/duyetde-4pillars-smoke.js` chạy thành công (PASS 100%).
