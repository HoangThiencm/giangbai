# QUY CHUẨN BẮT BUỘC KHI SOẠN KẾ HOẠCH BÀI DẠY (SOẠN KHBD)

Quy tắc này áp dụng vĩnh viễn cho mọi yêu cầu "soạn khbd" trong Antigravity. Tuyệt đối không được vi phạm ở bất kỳ bài nào tiếp theo.

## 1. Nguồn dữ liệu đầu vào
- Tự động đọc dữ liệu trong thư mục `TROLYTHIEN/1_SOAN_KHBD/Dau_vao/`:
  + Tệp PDF nội dung bài học SGK.
  + Tệp Phân phối chương trình (PPCT) dưới dạng Word, Excel, PDF hoặc ảnh.
  + Tệp chỉ dẫn chuẩn: `TROLYTHIEN/1_SOAN_KHBD/Dau_vao/PROMPT_SOAN_GIAO_AN.md`.

## 2. Tiêu đề Mục III và Thời lượng hoạt động
- **Tiêu đề Mục III chỉ ghi duy nhất:** `# III. TIẾN TRÌNH DẠY HỌC`
  - **CẤM TUYỆT ĐỐI:** Không ghi `(01 TIẾT — 45 PHÚT)` hay `(X TIẾT — Y PHÚT)` ở tiêu đề này.
- **Thời lượng:** Phân bổ cụ thể vào các hoạt động sao cho **tổng thời lượng khớp chính xác** thời gian của bài (ví dụ bài 1 tiết: 5p + 32p + 8p = 45 phút; bài 2 tiết: 8p + 45p + 25p + 12p = 90 phút).

## 3. Thể hiện Năng lực số và AI
- Cột Ghi chú PPCT là căn cứ duy nhất. Có mã thì trích đúng mã vào Mục I.2.c và I.2.d. Cột Ghi chú để trống thì **cấm** tạo mục NLS/AI ở Mục I và **cấm** chèn dòng tích hợp ở Mục III.
- Tiêu đề mục con trong Phần I (chỉ khi PPCT có mã) ghi đúng chuẩn:
  - `### c) Năng lực số (NLS)`
  - `### d) Năng lực Trí tuệ Nhân tạo (AI)`
- **CẤM TUYỆT ĐỐI:** Không chèn chữ `-- Theo PPCT` vào tiêu đề các mục này. Không bịa mã khi PPCT không chỉ định.
- **BẮT BUỘC IN ĐẬM, IN NGHIÊNG TRONG CÁC HOẠT ĐỘNG DẠY HỌC:**
  + Trong tiến trình dạy học (các hoạt động A, B, C, D), ở bất kỳ hoạt động/bước nào có triển khai Năng lực số hoặc Năng lực AI, **toàn bộ nội dung tích hợp (mã chỉ báo và mô tả hành động GV/HS)** bắt buộc phải được **in đậm, in nghiêng** (ví dụ: `***(Tích hợp NLS 1.1.TC1a: Khai thác học liệu số mô phỏng...)***` hoặc `***(Tích hợp AI 6.B2.1: Sử dụng trợ lý AI...)***`).
  + Quy định này đồng bộ 100% với tiêu chuẩn kiểm tra/duyệt giáo án của trường THCS Trần Phú (chưa in đậm nghiêng -> Trả hồ sơ).

## 4. Hình vẽ, sơ đồ tư duy
- **Bài Số học:** Không chèn sơ đồ quy trình dạng ảnh lặp lại lý thuyết. Nhưng nếu bài học/bài tập có các đối tượng toán học trực quan (tia số, trục số, biểu đồ Ven, mô hình khối lập phương, bài toán thực tế lát nền/chia mảnh đất) thì **bắt buộc phải vẽ và nhúng hình đầy đủ**. Trình bày lý thuyết đại số bằng ngôn ngữ toán, bảng và công thức.
- **BẮT BUỘC CÓ SƠ ĐỒ TƯ DUY (MINDMAP) TRONG TIẾT ÔN TẬP / LUYỆN TẬP:**
  + Trong các tiết Luyện tập chung, Ôn tập chương, Ôn tập học kỳ: tại **Hoạt động 2.1 (Hệ thống hoá kiến thức)**, **BẮT BUỘC PHẢI TẠO VÀ NHÚNG HÌNH ẢNH SƠ ĐỒ TƯ DUY (Mindmap)**.
  + Sơ đồ tư duy phải trực quan, phân nhánh mạch lạc (Chủ đề trung tâm $\rightarrow$ Các nhánh khái niệm, định nghĩa $\rightarrow$ Tính chất, dấu hiệu $\rightarrow$ Quy tắc tính / phương pháp giải).
  + **VỊ TRÍ ĐẶT SƠ ĐỒ TƯ DUY:** Đặt độc lập tại **mục b) Nội dung** của Hoạt động 2.1 (bên ngoài bảng), căn giữa tài liệu để ảnh hiển thị rộng rãi, chuẩn tỷ lệ và rõ nét nguyên khổ A4. **TUYỆT ĐỐI KHÔNG** nhúng ảnh sơ đồ tư duy vào trong ô bảng của mục d) Tổ chức thực hiện vì bề rộng cột hẹp (chỉ ~8-9 cm) sẽ làm ảnh bị ép méo, che lấp chữ hoặc tràn lề bảng.
  + Sơ đồ được render dạng ảnh PNG nét cao, nền trắng, nhúng vào văn bản qua thẻ: `![Hình Sơ đồ tư duy](khbd-ill:hinh-so-do-tu-duy)` và truyền dữ liệu base64 trong mảng `illustrations`.
  + **TUYỆT ĐỐI CẤM** chỉ viết các gạch đầu dòng chữ suông mà thiếu sơ đồ tư duy trong các tiết này.

- **BẮT BUỘC CÓ HÌNH VẼ TRONG BÀI HÌNH HỌC:**
  + Mọi bài học thuộc phân môn Hình học (đoạn thẳng, góc, tam giác, tứ giác, hình không gian...) **BẮT BUỘC PHẢI CÓ HÌNH VẼ MINH HỌA TOÁN HỌC**.
  + Hình vẽ tạo bằng SVG và render ra PNG 300 DPI độ nét cao, nền trắng (#ffffff), nét vẽ mực đen (#111827), nhãn điểm Times New Roman in hoa nghiêng.
  + Nhúng vào Word qua thẻ: `![Tên hình](khbd-ill:id-hinh)` kèm dữ liệu trong `illustrations`.
  + **Quy tắc hình học vector giải tích chuẩn xác:**
    * Các cung đo góc (angle arc) phải được tính tọa độ toán học chính xác từ 2 vector cạnh: cung bắt đầu đúng trên cạnh thứ nhất và kết thúc đúng trên cạnh thứ hai, nằm **hoàn toàn bên trong góc**, không bao giờ bị đâm lòi ra ngoài cạnh.
    * Vạch đánh dấu góc bằng nhau (tick mark) phải nằm dọc theo phương bán kính (vuông góc với tiếp tuyến của cung) tại đúng trung điểm của cung, cắt ngang cung đối xứng và ngay ngắn; cấm vẽ nét tự do lem nhem hoặc giống mũi tên.
    * Vạch đánh dấu đoạn thẳng bằng nhau phải nằm vuông góc với đoạn thẳng tại trung điểm đoạn thẳng.

## 5. Chuẩn hóa Công thức Toán học (Chống sót ký hiệu)
- **Ký hiệu Chia hết và Không chia hết:**
  + Dấu chia hết: dùng `$a \vdots b$` hoặc `a ⋮ b`. Cấm khoảng trắng thoát `\ \vdots \`.
  + Dấu không chia hết: dùng `$a \not\vdots b$`, `$a \nmid b$` hoặc `a ∤ b`.
  + Phân số `\frac{a}{b}` không được lọt ký tự form feed. Tập hợp dùng `\mathbb{N}`, `\in`, `\subset`, `\cap`, `\cup`.
  + Engine phải khôi phục `\vdots` khi `\v` bị thành Vertical Tab và `\frac` khi `\f` bị thành Form Feed, rồi xuất Equation `m:oMath` với ký tự `⋮` (U+22EE). Cấm chữ `dots` in nghiêng.
- Các ký hiệu khác: phân số `\frac`, căn `\sqrt`, góc `\widehat`, vector `\overrightarrow`, quan hệ tập hợp $\in, \notin, \subset, \cup, \cap$, dấu tương đương $\Leftrightarrow$, suy ra $\Rightarrow$ phải hiển thị đúng chuẩn Equation Word (OMML).

## 6. Bảng biểu trong Word và Chống lỗi "Mất bảng"
- **Lề trái và phải trong ô đều là 0pt:**
  + `TableCell margins: { top: 60, bottom: 60, left: 0, right: 0 }`
  + `Paragraph indent: { left: 0, right: 0 }`
- **Chống lỗi gãy bảng ("Mất bảng"):**
  + Mỗi hàng trong bảng Markdown bắt buộc phải nằm trên 1 dòng duy nhất bắt đầu và kết thúc bằng `|`.
  + Khi xuất Word bằng script Node.js, luôn đọc nội dung Markdown từ file `.md` bằng `fs.readFileSync(path, 'utf8')`. Tuyệt đối không nhúng chuỗi Markdown trực tiếp vào JS template literal (dấu backticks \`...\`) vì các ký hiệu LaTeX toán học như `\ne`, `\rightarrow`, `\text` sẽ bị JS biến thành ký tự ngắt dòng `\n`, làm gãy hàng bảng thành văn bản thuần.

## 7. Dung lượng và Cấu trúc bài dạy
- **Tiết luyện tập chung / Ôn tập (1 tiết = 45 phút):** 3 - 4 trang Word; chỉ 3 hoạt động (A. Khởi động -> B. Luyện tập: HĐ 2.1 Hệ thống hóa bằng Sơ đồ tư duy Mindmap + HĐ 2.2 Giải quyết bài tập trọng tâm -> C. Vận dụng).
- **Tiết hình thành kiến thức mới (2 tiết = 90 phút):** 6 - 7 trang Word; đủ 4 hoạt động A, B (chia theo đề mục SGK), C, D.
- Tự động lưu file thành phẩm `.docx` tại `TROLYTHIEN/1_SOAN_KHBD/Ket_qua/`.

## 8. Lịch sử Phản biện Thực chiến & Các Bản vá Hệ thống (Battle-Tested Patches)
Mỗi phản biện của giáo viên là một "bản vá đỏ" bắt buộc hệ thống phải ghi nhớ vĩnh viễn và không bao giờ tái phạm:

1. **Bản vá 1 — Phản biện Tích hợp NLS & AI:**
   - *Phản biện:* Không phải tiết nào cũng tích hợp NLS và AI. Phải nhìn PPCT tháng 9 và 10.
   - *Quy chuẩn vá:* Căn cứ pháp lý duy nhất là cột Ghi chú của PPCT. Chỉ tích hợp khi có mã chỉ định (ví dụ Bài 8, 9, 12). Cột Ghi chú để trống $\rightarrow$ TUYỆT ĐỐI CẤM bịa mã hoặc tự chèn mục NLS/AI. Khi có tích hợp, bắt buộc **in đậm, in nghiêng** `***(...)***` trong bảng phân vai GV-HS.

2. **Bản vá 2 — Phản biện Hình minh họa trong môn Số học:**
   - *Phản biện:* Số học bài nào cũng vẽ sơ đồ hộp/sơ đồ quy trình làm loãng giáo án, chỉ vẽ khi thực sự cần thiết. Nếu bài số học có hình vẽ thực sự cần thiết thì có chèn không?
   - *Quy chuẩn vá (Phân định rạch ròi):*
     + **CẤM:** Vẽ các sơ đồ hộp chữ nhật / lưu đồ quy trình giả tạo chỉ lặp lại bằng chữ các định lý, quy tắc (ví dụ: vẽ hình chữ nhật ghi chữ "Tính chất chia hết", "Quy trình 3 bước tìm BCNN"...). Những nội dung này trình bày bằng bảng 2 cột và công thức toán học là chuẩn mực và trang trọng nhất.
     + **BẮT BUỘC CHÈN KHI CÓ YÊU CẦU TOÁN HỌC TRỰC QUAN:** Trong môn Số học, nếu bài học hoặc bài tập SGK có các đối tượng toán học trực quan sau đây thì **BẮT BUỘC PHẢI VẼ VÀ NHÚNG ĐẦY ĐỦ**:
       * **Tia số / Trục số:** Biểu diễn số tự nhiên, điểm biểu diễn số nguyên âm/dương, bước nhảy bội số trên tia số.
       * **Biểu đồ Ven:** Minh họa tập hợp, phần tử thuộc/không thuộc, tập hợp con, giao của hai tập hợp.
       * **Mô hình toán học của bài toán thực tế:** Mô hình khối lập phương ghép (bài Lũy thừa, Thứ tự phép tính), mô hình lưới ô vuông chia kẹo/chia tổ, hình vẽ mảnh đất/nền nhà lát gạch trong bài toán thực tế, mô hình cân đĩa thăng bằng.
       * **Hình ảnh tư liệu từ đề bài SGK.**
     + **Tiết Luyện tập chung / Ôn tập:** Đúng 01 Sơ đồ tư duy (Mindmap) tại mục b) Nội dung của Hoạt động 2.1 (ngoài bảng).
     + **Phân môn Hình học:** 100% hình vẽ vector Oxy giải tích cực kỳ chính xác.

3. **Bản vá 3 — Phản biện Vị trí đặt Sơ đồ tư duy (Mindmap):**
   - *Phản biện:* "Đặt ảnh ở đây nó không phù hợp, vì cột nhỏ lắm. Ảnh sơ đồ tư duy có thể đặt ở mục b, Nội dung là được."
   - *Quy chuẩn vá:* TUYỆT ĐỐI CẤM nhúng ảnh Mindmap vào cột "Nội dung" trong ô bảng của mục d) Tổ chức thực hiện (vì cột chỉ rộng ~8-9 cm sẽ làm ảnh bị ép hẹp, méo, tràn lề và đè chữ). BẮT BUỘC đặt ảnh độc lập tại **mục b) Nội dung của Hoạt động 2.1 (bên ngoài bảng)**, căn giữa, rộng 480pt (16.9 cm) chiếm trọn khổ ngang A4 sắc nét.

4. **Bản vá 4 — Phản biện Lỗi công thức Toán học (`\vdots` & `\frac`):**
   - *Phản biện:* Công thức bị lỗi biến dạng thành `dots x`, `vv⋮x` và `rac24108`, `rac29`.
   - *Quy chuẩn vá:*
     + Lỗi `\vdots`: Ngăn chặn escape `\v` biến thành `\x0b`; cấm dùng regex `\\?dots` vì nuốt chữ `v` của `\vdots` biến thành `vv⋮`. Xuất đúng thẻ `<m:oMath>` chứa ký tự ba chấm dọc `⋮` (U+22EE).
     + Lỗi `\frac`: Ngăn chặn escape `\f` biến thành Form Feed `\x0c` làm rụng chữ `\f` thành `rac`. Bộ lọc 2 tầng tự động khôi phục `(?:frac|rac){` thành `\frac{` và xuất thẻ phân số Word `<m:f>` với `<m:num>` và `<m:den>`.

5. **Bản vá 5 — Phản biện Công cụ Rà soát Tự động trước khi xuất Word:**
   - *Phản biện:* Cần viết thêm chức năng rà soát giáo án coi có bị lỗi gì không để tránh sai sót không đáng có.
   - *Quy chuẩn vá:* Xây dựng và duy trì công cụ thẩm định tự động `tools/ra_soat_khbd.py` (kèm file chạy nhanh 1-click `tools/Kiem_Tra_KHBD.bat`) quét 4 nhóm lỗi cốt lõi (Công thức toán, PPCT NLS/AI, Vị trí Mindmap/Hình vẽ, Cấu trúc CV 5512). Giáo án phải đạt 100% PASS trước khi bàn giao.

6. **Bản vá 6 — Phản biện Lỗi rụng gạch chéo LaTeX (`eginarray`, `ext{`) & Thẩm định Kép Word DOCX XML:**
   - *Phản biện:* File `KHBD_05_Toan6_Bai10_SoNguyenTo_Tiet18-19.docx` bị hiển thị text rác `eginarrayrl60&2 30&2 15&...` trong Word mà công cụ phản biện không phát hiện ra.
   - *Nguyên nhân cốt lõi:*
     1. Ký tự escape `\b` (Backspace) trong chuỗi Python/JS bị nuốt mất gạch chéo, biến `\begin` thành `egin`. Word OMML không hiểu và in thẳng chuỗi thô.
     2. Công cụ rà soát cũ chỉ đọc file `.md`, hoàn toàn KHÔNG mở file `.docx` thành phẩm để kiểm tra, dẫn đến việc người dùng thấy lỗi trong Word nhưng công cụ rà soát vẫn báo PASS!
   - *Quy chuẩn vá vĩnh viễn:*
     1. **Cấm dùng `\begin{array}` cho sơ đồ cột Số học trong Word:** Sơ đồ cột phân tích thừa số nguyên tố phải trình bày bằng các bước chia liên tiếp rõ ràng hoặc bảng 2 cột mini căn giữa.
     2. **Engine khôi phục toàn diện ký tự điều khiển:** Tự động sửa `\u0008egin` -> `\begin`, `\u0009ext` -> `\text`, `\u0009imes` -> `\times`, `(?<![\\f])rac{` -> `\frac{` trước khi xuất Word.
     3. **Nâng cấp công cụ rà soát lên V3.0 (Bảo vệ kép Dual-Layer):** Rà soát bắt buộc phải giải nén và quét trực tiếp file `word/document.xml` của file `.docx` thành phẩm. Bắt buộc kiểm tra cả thẻ `<m:t>` và `<w:t>`. Bất kỳ chuỗi rác nào (`egin`, `array`, `rac`, `\\vdots`, `&`, `\\`) xuất hiện trong file Word đều bị đánh FAIL ngay lập tức.

