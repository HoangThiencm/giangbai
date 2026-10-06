# PLAN: CHUẨN HÓA TOÀN DIỆN VÀ ỔN ĐỊNH HỆ THỐNG SOẠN KẾ HOẠCH BÀI DẠY (KHBD V2.0)

## Hiện trạng
1. **Sự không ổn định trong các lần chạy tự động:**
   - Mỗi lần thực thi soạn KHBD lại phát sinh sai sót cục bộ (nhận diện nhầm bài tích hợp NLS/AI, chèn hình vẽ tràn lan vào các bài số học không cần thiết, lỗi ký tự công thức toán học biến dạng như `36 dots x`).
   - Thiếu một "Bộ ma trận tiêu chí phân loại cố định" dẫn đến việc AI tự suy diễn cảm tính ở mỗi phiên chat.
2. **Khảo sát lỗi công thức toán học (`dots x`, `\vdots`, `\frac`):**
   - Ký hiệu toán học LaTeX khi lưu chuyển qua môi trường script (JS/Python) bị ảnh hưởng bởi ký tự thoát (escape sequences):
     + `\v` bị biến thành Vertical Tab (mã ASCII `\x0b`), làm mất tiền tố lệnh `\`, bộ phân tích toán học chỉ còn lại chữ `dots`, dẫn đến việc MathRun trong Word in ra chữ nghiêng *dots* thay vì ba chấm dọc `⋮`.
     + `\f` bị biến thành Form Feed (`\x0c`), làm lệnh `\frac` biến thành `\x0crac`.
     + Các khoảng trắng escape như `\ ` xung quanh `\vdots` (`\ \vdots \`) gây đứt gãy token trong regex tách công thức.
3. **Khảo sát vấn đề hình vẽ và sơ đồ tư duy:**
   - Hệ thống đang có xu hướng ép buộc sinh hình ảnh minh họa cho mọi bài học (Bài 8 sơ đồ tính chất chia hết, Bài 9 bảng dấu hiệu, Bài 10 sàng số, Bài 11 quy trình ƯCLN, Bài 12 quy trình BCNN).
   - Trong phân môn Số học THCS, các bài lý thuyết mang tính trừu tượng logic đại số, việc chèn hình vẽ sơ đồ hộp gượng ép làm loãng giáo án, mất tính trang trọng và không đúng thực tế giảng dạy.
   - Sơ đồ tư duy (Mindmap) chưa được định vị rõ ràng về mặt quy chuẩn: chỉ phù hợp và thực sự có giá trị sư phạm ở các tiết **Luyện tập chung** hoặc **Ôn tập chương**, và vị trí đặt chuẩn duy nhất là tại **Hoạt động 2.1 (Hệ thống hoá kiến thức)**.
4. **Khảo sát vấn đề tích hợp Năng lực số (NLS) và Trí tuệ nhân tạo (AI):**
   - Hiện đang bị gán tự động vào mọi bài nếu không có cơ chế chặn chặt chẽ.
   - Nguyên tắc thẩm định chuyên môn: Cột "Ghi chú" của Phân phối chương trình (PPCT) là căn cứ pháp lý duy nhất. Nếu bài học trong PPCT để trống cột Ghi chú thì **tuyệt đối không được tích hợp NLS/AI**. Chỉ tích hợp đúng mã chỉ báo và hành động cụ thể ở các bài có chỉ định rõ ràng.

---

## Phạm vi
1. **Thiết lập Bộ Ma trận Tiêu chuẩn Sư phạm cố định (Pedagogical Standards Matrix):**
   - **Quy tắc Tích hợp NLS & AI:** Khóa cơ chế ánh xạ 1-1 theo PPCT (chỉ tích hợp khi có mã trong PPCT; in đậm, in nghiêng trong bảng; cấm tự bịa bài không có).
   - **Quy tắc Phân loại Hình vẽ & Sơ đồ:** Xác định rõ bài nào cần hình vẽ (Hình học, bài toán thực tế có mô hình không gian), bài nào cấm chèn hình (Số học lý thuyết), bài nào cần Sơ đồ tư duy (tiết Luyện tập chung / Ôn tập chương tại Hoạt động 2.1).
   - **Quy tắc Chuẩn hóa Công thức Toán:** Khóa cứng chuẩn Equation Word, chống tuyệt đối các lỗi escape (`\x0b`, `\x0c`), chuyển đổi triệt để `\vdots` thành ba chấm dọc `⋮`, `\not\vdots` thành `∤`.
2. **Cập nhật và đồng bộ toàn bộ tài liệu hướng dẫn và engine xuất bản:**
   - Đồng bộ Rule hệ thống: `.agents/rules/soankhbd.md` và `.agents/rules/tro-ly-thien.md`.
   - Cập nhật Master Prompt: `TROLYTHIEN/1_SOAN_KHBD/Dau_vao/PROMPT_SOAN_GIAO_AN.md`.
   - Cập nhật Quy trình 2 pha: `TROLYTHIEN/1_SOAN_KHBD/Dau_vao/HUONG_DAN_SOAN_KHBD_HANG_LOAT.md`.
   - Gia cố lớp bảo vệ chống lỗi công thức trong lõi engine: `TROLYTHIEN/engine/export_khbd_engine.js` và `js/khbd-docx.js`.
   - Chuẩn hóa script xuất hàng loạt: `tools/export_all_8_khbd.js`.
3. **Chuẩn hóa lại toàn bộ 8 bài KHBD mẫu Toán 6 hiện tại:**
   - Đảm bảo 8 bài mẫu tại `TROLYTHIEN/1_SOAN_KHBD/Ket_qua/` đạt độ chuẩn xác 100% làm mẫu đối sánh vĩnh viễn cho hệ thống.

---

## Ngoài phạm vi
- Không can thiệp vào các phân hệ khác ngoài KHBD (như Tạo bài tập, Duyệt đề, Tạo báo cáo, Vẽ hình học giải tích riêng lẻ).
- Không sửa đổi cấu trúc 4 bước của CV 5512 đã ổn định.

---

## File dự kiến tác động
1. `.agents/rules/soankhbd.md` (Cập nhật quy chuẩn cốt lõi vĩnh viễn)
2. `TROLYTHIEN/1_SOAN_KHBD/Dau_vao/PROMPT_SOAN_GIAO_AN.md` (Master Prompt chuẩn hóa)
3. `TROLYTHIEN/1_SOAN_KHBD/Dau_vao/HUONG_DAN_SOAN_KHBD_HANG_LOAT.md` (Bổ sung checklist kiểm soát lỗi)
4. `TROLYTHIEN/engine/export_khbd_engine.js` (Lọc ký tự rác ASCII và chuẩn hóa toán học ở tầng engine)
5. `js/khbd-docx.js` (Gia cố bộ chuyển đổi MathRun / Equation Word)
6. `tools/export_all_8_khbd.js` (Cập nhật cấu hình xuất chuẩn xác)
7. `TROLYTHIEN/1_SOAN_KHBD/Ket_qua/` (8 file `.md` và 8 file `.docx` mẫu chuẩn)

---

## Các bước thực hiện

### Bước 1: Xây dựng Bộ Tiêu chí Chuẩn định Phân loại Bài học (Core Rules)
- **Tiêu chí 1: Nhận diện Tích hợp NLS và AI (Đồng bộ PPCT 100%)**
  + Trước khi soạn, quét cột Ghi chú của bài học trong PPCT.
  + Nếu có mã NLS / AI: Trích đúng mã và mô tả vào Mục I.2.c và I.2.d; trong Mục III (Tiến trình dạy học) bắt buộc **in đậm, in nghiêng** toàn bộ lời thoại và hoạt động GV-HS: `***(Tích hợp NLS [Mã]: ...)***`, `***(Tích hợp AI [Mã]: ...)***`.
  + Nếu không có mã (cột Ghi chú để trống): **TUYỆT ĐỐI CẤM** tạo mục NLS/AI ở Mục I và cấm chèn dòng tích hợp vào Mục III.
- **Tiêu chí 2: Quy chuẩn Hình vẽ Minh họa & Sơ đồ Tư duy**
  + *Bài Số học lý thuyết:* Tuyệt đối KHÔNG vẽ hình minh họa, KHÔNG vẽ sơ đồ quy trình dạng ảnh chiếm chỗ. Trình bày bằng ngôn ngữ toán học, bảng biểu và công thức đại số chuẩn mực.
  + *Tiết Luyện tập chung / Ôn tập chương:* BẮT BUỘC có 01 ảnh Sơ đồ tư duy (Mindmap) tại **Hoạt động 2.1 (Hệ thống hoá kiến thức)**. Không đặt ở hoạt động khởi động hay vận dụng.
  + *Bài Hình học:* BẮT BUỘC 100% có hình vẽ vector giải tích chuẩn xác (PNG 300 DPI, nền trắng tinh, nét mực đen, nhãn điểm Times New Roman nghiêng, cung góc chuẩn, vạch đánh dấu vuông góc/bằng nhau).
- **Tiêu chí 3: Quy chuẩn Công thức Toán học (Chống lỗi `dots`, lỗi chia hết)**
  + Ký hiệu chia hết: Dùng `$a \vdots b$` hoặc `a ⋮ b`. Cấm tuyệt đối chèn khoảng trắng thoát chuỗi gây rách lệnh (`\ \vdots \`).
  + Ký hiệu không chia hết: Dùng `$a \not\vdots b$` hoặc `$a \nmid b$` hoặc `a ∤ b`.
  + Ký hiệu phân số: `\frac{a}{b}`, tuyệt đối không để lọt ký tự điều khiển form feed `\x0c`.
  + Ký hiệu tập hợp: $\mathbb{N}, \mathbb{N}^*$, phần tử $\in, \notin$, tập con $\subset, \subseteq$, giao $\cap$, hợp $\cup$.

### Bước 2: Gia cố Engine Xuất Word (`export_khbd_engine.js` & `khbd-docx.js`)
- Bổ sung bộ lọc tiền xử lý (Pre-sanitizer) ngay khi đọc Markdown:
  1. Loại bỏ toàn bộ ký tự điều khiển ASCII không in được: `[\x00-\x08\x0b\x0c\x0e-\x1f]`.
  2. Tự động nhận diện và chuyển đổi mọi mẫu `\dots` hoặc `dots` nằm giữa hai toán hạng số/biến thành `\vdots` (`⋮`).
  3. Rút gọn các chuỗi thoát rác `\ \vdots \ ` thành `\vdots`.
- Đảm bảo MathRun của docx sinh ra đúng thẻ Equation `m:oMath` hiển thị ký tự ba chấm dọc `⋮` (U+22EE), không bao giờ lọt chữ text `dots` in nghiêng ra bản Word.

### Bước 3: Cập nhật Master Prompt và Quy tắc Hệ thống
- Biên tập lại file `.agents/rules/soankhbd.md` đưa 3 tiêu chí cốt lõi vào làm điều khoản bắt buộc.
- Cập nhật `PROMPT_SOAN_GIAO_AN.md` bổ sung bảng checklist kiểm soát chất lượng trước khi xuất bài:
  + [ ] Đã đối chiếu cột Ghi chú PPCT chưa? (Có -> tích hợp in đậm nghiêng; Không -> để trống).
  + [ ] Có chèn hình vẽ tùy tiện vào bài số học lý thuyết không? (Cấm).
  + [ ] Tiết luyện tập chung/ôn tập đã có Mindmap ở Hoạt động 2.1 chưa?
  + [ ] Đã quét sạch các lỗi `dots x`, `\vdots`, `\frac` chưa?

### Bước 4: Chuẩn hóa 8 File KHBD Mẫu và Xuất Thành Phẩm
- Kiểm tra lại toàn bộ 8 file Markdown trong `TROLYTHIEN/1_SOAN_KHBD/Ket_qua/`:
  + `KHBD_01`: Giữ Mindmap 01 tại Hoạt động 2.1, không có NLS/AI.
  + `KHBD_02`: Giữ Mindmap 02 tại Hoạt động 2.1, không có NLS/AI.
  + `KHBD_03`: Tích hợp NLS 1.1.TC1a & AI 6.B2.1 (in đậm nghiêng), không chèn hình thừa.
  + `KHBD_04`: Tích hợp NLS 5.3.TC1a & AI 6.D1.1 (in đậm nghiêng), không chèn hình thừa.
  + `KHBD_05`: Không có NLS/AI, không chèn hình thừa.
  + `KHBD_06`: Giữ Mindmap 06 tại Hoạt động 2.1, không có NLS/AI.
  + `KHBD_07`: Không có NLS/AI, công thức `$36 \vdots x$` chuẩn xác, không chèn hình thừa.
  + `KHBD_08`: Tích hợp NLS 5.3.TC1a & AI 6.C1.1 (in đậm nghiêng), không chèn hình thừa.
- Chạy `tools/export_all_8_khbd.js` xuất 8 file Word hoàn chỉnh, sạch sẽ.

---

## Rủi ro
1. **Rủi ro hồi quy (Regression):** Khi sửa regex toán học có thể ảnh hưởng đến các lệnh LaTeX khác như hệ phương trình hay dấu ngoặc ma trận.
   - *Biện pháp:* Viết test script kiểm thử riêng cho các trường hợp toán học đặc thù trước khi áp dụng.
2. **Khóa file do người dùng mở Word (EBUSY):** Người dùng đang mở file Word thì script không ghi đè được.
   - *Biện pháp:* Engine đã có cơ chế tự động ghi ra `_Moi.docx` khi bị khóa; thêm cảnh báo rõ ràng yêu cầu đóng file Word.

---

## Cách kiểm thử
1. **Kiểm thử tự động (Unit Test):**
   - Viết test script nạp các chuỗi công thức: `$36 \vdots x$`, `$48 \dots x$`, `100 - x \dots 4`, `a \not\vdots b`, `\frac{24}{108}`.
   - Giải nén file `.docx` kiểm tra file `word/document.xml`, đảm bảo xuất hiện đúng thẻ `m:oMath` chứa ký tự `⋮` (U+22EE), không có chữ `dots`.
2. **Kiểm thử đối chiếu PPCT:**
   - Quét kiểm tra 8 file: Chỉ đúng 3 file (03, 04, 08) có chứa chuỗi `***(Tích hợp NLS` và `***(Tích hợp AI`; 5 file còn lại hoàn toàn không có.
3. **Kiểm thử hình ảnh & Mindmap:**
   - Quét cấu trúc: Chỉ đúng 3 file (01, 02, 06) có chứa thẻ Mindmap tại Hoạt động 2.1; các bài số học khác (03, 04, 05, 07, 08) không chứa bất kỳ thẻ hình ảnh nào.
4. **Kiểm thử mở thực tế trên Microsoft Word:**
   - Mở cả 8 file `.docx`, kiểm tra hiển thị công thức, bảng 2 cột lề 0pt, không tràn lề, không gãy dòng.

---

## Tiêu chí nghiệm thu
1. Cả 8 file Word KHBD mở trên Microsoft Word hiển thị công thức toán học sắc nét, đúng chuẩn `36 ⋮ x`, không còn bất kỳ lỗi `dots x` nào.
2. Tích hợp NLS/AI khớp 100% với ảnh PPCT: Bài có thì in đậm nghiêng đầy đủ, bài không có thì sạch sẽ hoàn toàn.
3. Hình vẽ được dùng đúng mực: Các bài số học lý thuyết không bị chèn hình thừa; 3 tiết ôn tập/luyện tập có Mindmap đúng vị trí Hoạt động 2.1.
4. Tài liệu chỉ dẫn và engine được đóng băng quy chuẩn, đảm bảo các lần chạy tiếp theo luôn ổn định, không tái diễn lỗi.
