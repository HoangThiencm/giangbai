# PLAN: Thiết kế lại Đề thi Chuẩn Công văn 7991/BGDĐT & Đồng bộ Tuyệt đối giữa "Tạo bài tập" và "Thi trực tuyến"

## I. Hiện trạng & Phân tích Nguyên nhân Lệch pha

### 1. Hiện trạng cấu trúc đề thi CV 7991 trong hệ thống
- **Hiện trạng cũ trong `taobaitap.html`**:
  - Giao diện và prompt đang định nghĩa CV 7991 gồm 18 câu: 12 câu trắc nghiệm 4 lựa chọn (6đ) + **2 câu Đúng/Sai** (2đ) + 4 câu trả lời ngắn (2đ).
  - Phần II (Đúng/Sai) trong prompt cũ chỉ yêu cầu: `{"question":"...","options":["Đúng","Sai"],"correctAnswerIndex":0,"type":"true-false"}`. AI sinh ra câu hỏi đơn chỉ có 2 lựa chọn Đúng hoặc Sai, **không có 4 ý con $a, b, c, d$** bám vào một chủ đề chung.
  - Khi xuất Word (`exportWordCV7991`), vì không có `subItems`, hệ thống xuất fallback ra: `a) Mệnh đề trên là [Đúng]`, chỉ có duy nhất 1 ý $a$, mất hoàn toàn bản chất dạng câu hỏi Đúng/Sai theo chuẩn GDPT 2018 của Bộ GD&ĐT.
- **Yêu cầu mới chuẩn hóa theo chỉ đạo người dùng**:
  - **Phần I**: **12 câu trắc nghiệm nhiều phương án lựa chọn** (6.0 điểm, mỗi câu 0.5 điểm) — Thí sinh chọn 1 trong 4 phương án $A, B, C, D$.
  - **Phần II**: **ĐÚNG 1 CÂU TRẮC NGHIỆM ĐÚNG SAI** (2.0 điểm) — Gồm **1 chủ đề/ngữ cảnh/bài toán dẫn chung và 4 ý/mệnh đề** $a), b), c), d)$ dựa trên ngữ cảnh đó.
  - **Phần III**: **4 câu trắc nghiệm trả lời ngắn** (2.0 điểm, mỗi câu 0.5 điểm) — Câu hỏi định hướng tính toán, **chỉ điền số kết quả** (số nguyên, số thập phân hoặc phân số ngắn gọn dạng số), không chứa chữ.
  - **Tổng số câu toàn đề**: $12 + 1 + 4 = 17$ câu hỏi (tổng điểm 10.0).

---

### 2. Nguyên nhân "Thi trực tuyến" không nhận diện trọn vẹn đáp án từ file Word của "Tạo bài tập"
1. **Thiếu Bảng Đáp Án ở cuối file Word xuất ra (`exportWordCV7991`)**:
   - `exportWord100TN` có tạo bảng đáp án ở cuối, nhưng `exportWordCV7991` trong `taobaitap.html` hoàn toàn **KHÔNG sinh khối `BẢNG ĐÁP ÁN`** ở cuối file `.docx`.
   - Mặc dù đề có đánh dấu `*` ở trắc nghiệm và tag `[Đúng]`/`[Sai]` ở đúng sai, nhưng nếu thiếu bảng đáp án chuẩn ở cuối file, `getImportedAnswerKey` trong `thitructuyen.html` không có dữ liệu nguồn đối soát, dễ gây thiếu sót hoặc phải dựa đơn độc vào inline regex.
2. **Lỗi ngắt dòng khi Mammoth đọc bảng phương án ($A, B, C, D$)**:
   - Trong `exportWordCV7991`, 4 phương án trắc nghiệm được bọc trong thẻ HTML `<table><tr><td>A...</td><td>B...</td></tr><tr><td>C...</td><td>D...</td></tr></table>`.
   - Khi Mammoth bóc tách text từ file Word, các ô cùng hàng thường được phân tách bằng tab `\t`.
   - Trong `thitructuyen.html`, hàm `normalizeImportedQuizText` thay thế `\t` thành khoảng trắng ` ` đơn thuần: `.replace(/\t/g, " ")`.
   - Hậu quả: `A. Phương án 1* B. Phương án 2` nằm trên cùng 1 dòng. Regex `optionRegexMC = /(?:^|\n)\s*([A-D])\s*[\.\):：-]\s*/g` chỉ bắt được phương án $A$ và $C$ (vì đứng đầu dòng), làm **rơi mất hoàn toàn phương án $B$ và $D$**!
3. **Lỗi nhận diện câu Đúng/Sai 4 ý**:
   - Do `taobaitap.html` chỉ sinh 1 ý `a)` thay vì đủ 4 ý $a), b), c), d)$, bộ parser `thitructuyen.html` kiểm tra `tfMatches.length >= 2` bị `false`, dẫn tới việc nhận diện sai loại câu (bị biến thành `short_answer`).
4. **Chuẩn hóa dữ liệu trả lời ngắn**:
   - AI đôi khi sinh câu trả lời ngắn kèm chữ hoặc đơn vị (ví dụ: `x = 25`, `25 cm`, `khoảng 12`). Cần ép buộc chặt chẽ trong Prompt và hàm Normalizer để đáp án chỉ là số thuần túy (`25`, `3.5`, `1/2`, `-4`).

---

## II. Kế hoạch Triển khai Chi tiết

### Module 1: Tái cấu trúc Đề thi CV 7991 trong `taobaitap.html`
1. **Cập nhật Thiết lập & Giao diện lựa chọn (`taobaitap.html`)**:
   - Thay đổi nhãn lựa chọn `synthForm`:
     `⭐ Chuẩn Công văn 7991 (17 câu - 10đ: 12 TN + 1 Đ/S 4 ý + 4 TL ngắn)`
   - Khi chọn `cv7991`, tự động đặt `synthCount = 17`. Khóa hoặc gán cứng cấu trúc 17 câu khi xuất hình thức này.
2. **Cập nhật Prompt AI (`generateSynthesizedFromSource` & `generateContent`)**:
   - Xây dựng chỉ thị cụ thể cho `synthForm === 'cv7991'`:
     ```text
     Hình thức: ĐỀ THI CHUẨN CÔNG VĂN 7991 / BGDĐT (17 câu - 10.0 điểm) gồm ĐÚNG 03 phần:
     - Phần I (Câu 1 đến Câu 12): 12 câu trắc nghiệm 4 lựa chọn A, B, C, D (type: "multiple-choice", mỗi câu 0.5đ = 6.0đ). Chỉ 1 đáp án đúng.
     - Phần II (Câu 13): ĐÚNG 1 câu trắc nghiệm Đúng/Sai (type: "true-false", tổng 2.0đ) dựa trên 1 chủ đề/ngữ cảnh/bài toán thực tế chung sâu sắc. Gồm 4 mệnh đề a, b, c, d. Cấu trúc JSON bắt buộc:
       {"question": "[Ngữ cảnh/chủ đề bài toán dẫn chung]...", "options": ["Nội dung mệnh đề a", "Nội dung mệnh đề b", "Nội dung mệnh đề c", "Nội dung mệnh đề d"], "correct_answers": [true, false, true, false], "type": "true-false"}
     - Phần III (Câu 14 đến Câu 17): ĐÚNG 4 câu trắc nghiệm trả lời ngắn (type: "short-answer", mỗi câu 0.5đ = 2.0đ). Câu hỏi yêu cầu tính toán ra kết quả số cụ thể. Trường "correctAnswer" CHỈ CHỨA SỐ (số nguyên, số thập phân hoặc phân số ngắn gọn, ví dụ "25", "3.5", "-4", "1/2"), TUYỆT ĐỐI KHÔNG chứa chữ cái hay đơn vị đo.
     Tổng cộng toàn đề đúng 17 câu = 10.0 điểm.
     ```
3. **Chuẩn hóa dữ liệu `normalizeQuizItems`**:
   - Hỗ trợ câu `true-false` chuẩn CV 7991:
     + Nhận diện `options` có 4 mệnh đề $a, b, c, d$ và `correct_answers` là mảng 4 boolean `[bool, bool, bool, bool]`.
     + Đồng bộ cả `subItems: [{ text: opt, isCorrect: correct_answers[i] }]` và `correct_answers` để tương thích mọi component.
   - Chuẩn hóa `short-answer`:
     + Tự động làm sạch `correctAnswer`: lọc bỏ tiền tố thừa như `x = `, đơn vị `cm, m, kg`, chuyển dấu phẩy số thập phân `3,5` hoặc giữ `3.5`.
4. **Cập nhật Giao diện Hiển thị & Chỉnh sửa (`ContentEditor` & Step 2 Card)**:
   - Trong `ContentEditor`: Khi sửa câu `true-false` 4 ý, hiển thị 4 ô nhập nội dung $a, b, c, d$ kèm nút bấm chuyển đổi `[ĐÚNG]` / `[SAI]` (xanh lá / đỏ) trực quan.
   - Trong danh sách câu hỏi Step 2: Hiển thị câu Đúng/Sai với 4 dòng $a), b), c), d)$ rõ ràng; hiển thị câu trả lời ngắn kèm ô đáp án số nổi bật.

---

### Module 2: Đồng bộ Định dạng Xuất Word (`exportWordCV7991`) & Xuất Text (`exportTextCV7991`)
1. **Quy chuẩn xuất DOCX trong `exportWordCV7991`**:
   - **Phần I (Câu 1 - 12)**:
     + Tiêu đề: `PHẦN I. CÂU TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN LỰA CHỌN (6.0 điểm)`
     + Hướng dẫn: `Thí sinh trả lời từ câu 1 đến câu 12. Mỗi câu hỏi thí sinh chỉ chọn một phương án. Mỗi câu đúng được 0.5 điểm.`
     + Trình bày từng phương án trên từng dòng `<p class="option">A. ...*</p>` hoặc trong bảng với mỗi ô chứa thẻ `<p>`, đánh dấu `*` ở phương án đúng.
   - **Phần II (Câu 13)**:
     + Tiêu đề: `PHẦN II. CÂU TRẮC NGHIỆM ĐÚNG SAI (2.0 điểm)`
     + Hướng dẫn: `Thí sinh trả lời câu 13. Trong mỗi ý a), b), c), d), thí sinh chọn Đúng hoặc Sai. Điểm tối đa là 2.0 điểm (Đúng 1 ý: 0.2đ; 2 ý: 0.5đ; 3 ý: 1.0đ; 4 ý: 2.0đ).`
     + Trình bày:
       ```html
       <div class="question-block">
           <b>Câu 13:</b> [Nội dung ngữ cảnh bài toán chung]<br>
           <div class="tf-item">a) [Mệnh đề a] [Đúng]</div>
           <div class="tf-item">b) [Mệnh đề b] [Sai]</div>
           <div class="tf-item">c) [Mệnh đề c] [Đúng]</div>
           <div class="tf-item">d) [Mệnh đề d] [Sai]</div>
       </div>
       ```
   - **Phần III (Câu 14 - 17)**:
     + Tiêu đề: `PHẦN III. CÂU TRẮC NGHIỆM TRẢ LỜI NGẮN (2.0 điểm)`
     + Hướng dẫn: `Thí sinh trả lời từ câu 14 đến câu 17. Thí sinh chỉ điền số kết quả vào ô trả lời. Mỗi câu đúng được 0.5 điểm.`
     + Trình bày:
       ```html
       <div class="question-block">
           <b>Câu 14:</b> [Nội dung bài toán]<br>
           <div class="answer-line">Đáp án: 25</div>
       </div>
       ```
   - **BẢNG ĐÁP ÁN ĐỒNG BỘ Ở CUỐI TÀI LIỆU**:
     + Xuất khối bảng đáp án chuẩn mực:
       ```html
       <div class="answer-key">
           <h2>BẢNG ĐÁP ÁN</h2>
           <p>Đáp án:</p>
           <p>1.A   2.B   3.C   4.D   5.A   6.B   7.C   8.D   9.A   10.B   11.C   12.D</p>
           <p>13. a.Đúng b.Sai c.Đúng d.Sai</p>
           <p>14. 25   15. 3.5   16. 100   17. -4</p>
       </div>
       ```
2. **Quy chuẩn xuất Text trong `exportTextCV7991`**:
   - Định dạng text thuần đồng bộ 100% với file Word, chứa đủ 3 phần và Bảng Đáp Án ở cuối để giáo viên có thể copy-paste trực tiếp vào ô "Nạp đáp án" hoặc "Nhập văn bản đề thi".

---

### Module 3: Nâng cấp Trình Đọc & Nhận diện Đề Word trong `thitructuyen.html`
1. **Gia cố `normalizeImportedQuizText`**:
   - Xử lý các ký tự phân tách giữa các phương án trước khi gộp tab:
     Tự động chuyển `\t([A-Da-d][\.\):：-])` và `(?<=\S)\s{2,}([A-Da-d][\.\):：-])` thành `\n$1`.
     Đảm bảo dù file Word thiết kế bảng hay 2 cột ngang, các phương án $A, B, C, D$ và các ý $a, b, c, d$ luôn được tách dòng độc lập, không bao giờ bị dính chùm.
2. **Nâng cấp `parseLatexWordQuiz`**:
   - Nhận diện câu Đúng/Sai 4 ý:
     Khi phát hiện $a), b), c), d)$ trong một câu hỏi:
     + Trích xuất nội dung 4 ý vào `options`.
     + Đọc đáp án Đúng/Sai từ inline tag `[Đúng]`/`[Sai]` hoặc từ `answerKey` (`13. a.Đúng b.Sai...` hoặc `13: Đ, S, Đ, S`).
     + Gán `type: "tf"`, `correct_answers: [bool, bool, bool, bool]`.
   - Nhận diện câu Trả lời ngắn kết quả số:
     + Gán `type: "short_answer"`, trích xuất số từ `Đáp án: [số]` hoặc từ `answerKey[14..17]`.
     + Chuẩn hóa khoảng trắng, lưu trữ đúng giá trị số.
   - Nhận diện câu Trắc nghiệm 4 lựa chọn:
     + Gán `type: "mc"`, nhận diện đủ 4 phương án $A, B, C, D$, xác định `correct_index` từ dấu `*` hoặc `answerKey`.
   - Tự động nhận diện cấu trúc đề:
     Nếu đề có 17 câu (12 MC + 1 TF + 4 Short Answer), tự động kích hoạt cờ `exam_format: "cv7991"`.

---

### Module 4: Đồng bộ Thang điểm & Chấm thi Backend
1. **Kiểm tra tính tương thích của Backend (`backend/thitructuyen.py` và `api/exam.php`)**:
   - Backend hiện tại đã có cơ chế tự động:
     + `mc_weight = 6.0 / mc_count` (với 12 câu MC $\rightarrow 0.5$đ/câu).
     + `short_weight = 2.0 / short_count` (với 4 câu TLN $\rightarrow 0.5$đ/câu).
     + `tf_scale = 2.0 / (tf_count * 1.0)` (với 1 câu Đúng/Sai $\rightarrow \text{tf\_scale} = 2.0 / 1.0 = 2.0$).
     + Điểm câu Đúng/Sai khi nhân hệ số scale 2.0:
       * Đúng 1 ý: $0.1 \times 2.0 = 0.2$ điểm.
       * Đúng 2 ý: $0.25 \times 2.0 = 0.5$ điểm.
       * Đúng 3 ý: $0.5 \times 2.0 = 1.0$ điểm.
       * Đúng 4 ý: $1.0 \times 2.0 = 2.0$ điểm.
     + Tổng điểm: $6.0 + 2.0 + 2.0 = 10.0$ điểm tối đa!
   - Cả hai file `backend/thitructuyen.py` và `api/exam.php` đã hỗ trợ công thức này chuẩn xác, hoạt động hoàn hảo khi đề có đúng 1 câu Đúng/Sai (2.0 điểm).

---

### Module 5: Kiểm thử Tự động (Smoke Test)
1. **Tạo kịch bản kiểm thử tích hợp (`tests/cv7991-taobaitap-thitructuyen-sync-smoke.js`)**:
   - Sinh mô phỏng dữ liệu đề thi CV 7991 chuẩn (12 MC + 1 TF 4 ý + 4 TLN số).
   - Chạy hàm xuất HTML/Word từ `taobaitap.html`.
   - Nạp chuỗi xuất ra vào hàm parser của `thitructuyen.html`.
   - Kiểm tra xác nhận 100%:
     + Đúng 17 câu hỏi được tạo ra.
     + 12 câu đầu: `type === 'mc'`, có đủ 4 phương án $A, B, C, D$, nhận đúng `correct_index`.
     + Câu 13: `type === 'tf'`, có đủ 4 ý $a, b, c, d$, nhận đúng mảng 4 giá trị `correct_answers` `[true/false, ...]`.
     + Câu 14..17: `type === 'short_answer'`, nhận đúng `correct_answer` dạng số thuần túy.
     + Bảng đáp án được cắt sạch khỏi đề bài, không bị sót vào nội dung câu hỏi cuối cùng.

---

## File tác động
1. `taobaitap.html`:
   - Cập nhật định nghĩa CV 7991 (17 câu: 12 MC + 1 TF 4 ý + 4 TLN).
   - Cập nhật prompt sinh bài tập từ file & từ chủ đề.
   - Cập nhật `normalizeQuizItems`, `formatQuizAnswer`, `ContentEditor` và Step 2 Card.
   - Nâng cấp `exportWordCV7991` và `exportTextCV7991` tạo cấu trúc chuẩn và Bảng Đáp Án ở cuối.
2. `thitructuyen.html`:
   - Tăng cường `normalizeImportedQuizText` xử lý phân tách tab/khoảng trắng giữa các phương án.
   - Tinh chỉnh `parseLatexWordQuiz` đảm bảo nhận diện chính xác 100% cả 3 phần và Bảng Đáp Án từ file Word.
3. `tests/cv7991-taobaitap-thitructuyen-sync-smoke.js`:
   - Kịch bản kiểm thử tự động xác thực sự đồng bộ hai chiều giữa `taobaitap.html` và `thitructuyen.html`.

---

## Tiêu chí Nghiệm thu (Acceptance Criteria)
1. **Đề thi CV 7991 chuẩn 17 câu**:
   - Gồm Phần I (12 câu MC - 6đ), Phần II (1 câu TF có ngữ cảnh chung và 4 ý $a, b, c, d$ - 2đ), Phần III (4 câu TLN số - 2đ). Tổng 10 điểm.
2. **Xuất Word & Text đồng bộ**:
   - File Word và Text xuất từ `taobaitap.html` có đầy đủ tiêu đề 3 phần, nội dung các câu hỏi và BẢNG ĐÁP ÁN ở cuối.
3. **Nạp đề vào Thi trực tuyến tự động nhận diện 100%**:
   - Giáo viên tải file Word từ "Tạo bài tập" rồi bấm nạp vào "Thi trực tuyến" $\rightarrow$ Hệ thống tự động nhận diện đúng 17 câu:
     + 12 câu trắc nghiệm nhận đủ 4 phương án và đáp án đúng $A, B, C, D$.
     + 1 câu Đúng/Sai nhận đủ ngữ cảnh bài toán, 4 mệnh đề $a, b, c, d$ và tick sẵn Đúng/Sai cho từng ý.
     + 4 câu Trả lời ngắn nhận đúng kết quả số vào ô đáp án.
   - Không bị mất phương án $B, D$ do lỗi tab/khoảng trắng.
4. **Kiểm thử**:
   - Chạy test kiểm thử tự động đạt kết quả PASS 100%.
