# PLAN: Chuẩn hóa Quy chuẩn Sư phạm Toán học & Hình học Việt Nam (Ký hiệu Hình học, Bảng 2 Cột & Cấu trúc 4 Phần CV 5512)

## Hiện trạng & Phân tích nguyên nhân gốc rễ

### 1. Dấu đồng dạng trong Toán học Việt Nam khác biệt hoàn toàn với Equation quốc tế
- **Quy chuẩn Toán học Việt Nam (SGK GDPT 2018 - Cánh diều, Kết nối tri thức, Chân trời sáng tạo)**:
  - Ký hiệu hai tam giác đồng dạng ở Việt Nam là **chữ S nằm ngang**: `∽` (Unicode `U+223D` - REVERSED TILDE).
  - Ví dụ chuẩn SGK: $\triangle ABC \backsim \triangle A'B'C'$ (đọc là: tam giác ABC đồng dạng với tam giác A'B'C').
- **Sai lệch trong hệ thống hiện tại**:
  - Trong Word Equation và LaTeX quốc tế, lệnh `\sim` mặc định sinh ra **dấu ngã sóng nằm ngang** `∼` (Unicode `U+223C` - TILDE OPERATOR). Ký hiệu này trong giáo dục Việt Nam bị coi là sai quy chuẩn hình học.
  - Trong `js/khbd-docx.js` (dòng 279), `commandMap` đang map `sim: "∼"` $\rightarrow$ render ra dấu ngã `∼` (sai chuẩn Việt Nam).
  - `commandMap` và `mathDict` hoàn toàn thiếu lệnh `\backsim` (lệnh chuẩn tạo chữ S nằm ngang `∽` trong LaTeX).

---

### 2. Ký hiệu góc (`\widehat` / `\hat`) bị bộ render Word gọt mất mũ góc
- **Hiện trạng**:
  - Khi giáo viên hoặc AI viết góc $\widehat{ABC}$ hoặc $\widehat{A}$:
  - Tại dòng 449–450 file `js/khbd-docx.js`:
    ```javascript
    } else if (command === "overline" || command === "hat" || command === "widehat" || command === "vec" || command === "overrightarrow" || command === "underline") {
      nodes = readGroup();
    ```
  - Trình phân tích `createNativeMath` của Word **vứt bỏ hoàn toàn ký hiệu mũ góc** (`readGroup()`)!
  - Kết quả trong Word: $\widehat{ABC}$ biến thành chữ `ABC` trần trụi (từ góc biến thành tên mặt phẳng hoặc tích các cạnh, mất hoàn toàn bản chất toán học).
  - Vectơ `\vec{AB}` hoặc `\overrightarrow{AB}` cũng bị vứt bỏ mũi tên, biến thành đoạn thẳng `AB`.

---

### 3. Lỗi bảng 2 cột mục d): Cột 2 ("Nội dung") bị bỏ trống hoặc chỉ ghi `---`, dồn hết vào Cột 1
- **Hiện trạng từ thực tế (Ảnh 1 người dùng gửi)**:
  - Ở Hoạt động 2.2: Bảng gồm 2 cột `Hoạt động của GV và HS` và `Nội dung`. Cột 1 dồn toàn bộ kịch bản 4 bước và ở Bước 4 dồn luôn toàn bộ nội dung ghi bảng:
    `- HS: Ghi nội dung cốt lõi. / 2. PHƯƠNG PHÁP CỘNG ĐẠI SỐ \n Quy tắc giải: ... \n Ví dụ 4: ... \n Lời giải: ...`
    Trong khi đó Cột 2 ("Nội dung") hoàn toàn **RỖNG KHÔNG**!
  - Ở Hoạt động 2.3 (Thực hành máy tính cầm tay): Cột 1 ghi các bước hướng dẫn bấm máy, Cột 2 chỉ ghi đúng ba dấu gạch ngang `---`!
- **Nguyên nhân gốc rễ**:
  1. **Prompt**: AI hiểu nhầm chỉ thị Bước 4 "- HS ghi chép nội dung cốt lõi..." nên chép luôn nội dung định nghĩa, quy tắc và ví dụ giải chi tiết vào lời thoại của HS trong Cột 1, để Cột 2 rỗng hoặc `---`.
  2. **`semanticSplitActivityRow` trong `js/khbd-app.js` và `js/khbd-docx.js`**:
     ```javascript
     if (list.length === 2) return [list[0], list[1]];
     ```
     Khi AI xuất `| Cột 1 đầy đủ kiến thức ghi bảng | |` hoặc `| Cột 1 | --- |`, hàm thấy có 2 phần tử nên trả về nguyên trạng, không phát hiện Cột 2 đang rỗng và Cột 1 đang ôm đồm toàn bộ nội dung ghi bảng.
  3. **Bộ kiểm thử & Assertion (`assertPhasePedagogyOutput`)**:
     Chỉ kiểm tra Cột 1 có Bước 1..4 và GV/HS hay không, không kiểm tra Cột 2 có bị rỗng hoặc `---` hay không.

---

### 4. Lỗi thiếu 4 phần chuẩn CV 5512 ở Hoạt động 4 (Vận dụng) (Ảnh 2 người dùng gửi)
- **Hiện trạng từ thực tế (Ảnh 2)**:
  - Sau tiêu đề `D. HOẠT ĐỘNG 4: VẬN DỤNG & HƯỚNG DẪN TỰ HỌC (18 phút)`, văn bản chỉ có:
    `- Mục tiêu: Vận dụng giải quyết bài toán...`
    và nhảy cóc ngay lập tức vào bảng `| Hoạt động của GV và HS | Nội dung |`!
  - Bị mất hoàn toàn 3 mục bắt buộc của CV 5512:
    + `### b) Nội dung:`
    + `### c) Sản phẩm:`
    + `### d) Tổ chức thực hiện:`
- **Nguyên nhân gốc rễ**:
  1. Trong `GENERATE_ACTIVITIES_AD` và `GENERATE_ACTIVITIES_AE` (`js/khbd-prompts.js`), chỉ thị cho Hoạt động A và B nêu rõ yêu cầu đủ a) b) c) d), nhưng mục Hoạt động D lại không nhắc lại ràng buộc "BẮT BUỘC ĐỦ 4 MỤC: ### a) Mục tiêu, ### b) Nội dung, ### c) Sản phẩm, ### d) Tổ chức thực hiện". AI đã lược bỏ b) và c) và bỏ luôn tiêu đề d).
  2. Trong `js/khbd-app.js`, không có bộ lọc tự động kiểm tra và phục hồi (Auto-Repair) cấu trúc 4 phần nếu AI sinh thiếu `b)` và `c)`.

---

### 5. Cấm dùng dấu ngoặc vuông `[` khi giải phương trình tích ở cấp THCS
- **Quy chuẩn sư phạm CT GDPT 2018 (SGK Toán 8, 9)**:
  - Ở cấp THCS (lớp 6, 7, 8, 9): **TUYỆT ĐỐI CẤM DÙNG DẤU NGOẶC VUÔNG `[` KHI GIẢI PHƯƠNG TRÌNH TÍCH**.
  - Ký hiệu ngoặc vuông `[` (tuyển mệnh đề) chỉ được dạy ở Toán lớp 10 (THPT).
  - Trong SGK Toán 8, 9 hiện hành, khi giải phương trình tích $(ax+b)(cx+d)=0$, SGK 100% sử dụng từ ngữ tiếng Việt **"hoặc"** hoặc chia **Trường hợp 1 / Trường hợp 2**.

---

### 6. Quy chuẩn trình bày Số thập phân & Dấu phân cách tọa độ / Cặp nghiệm
- **Dấu số thập phân**: Số thập phân ở Việt Nam BẮT BUỘC DÙNG DẤU PHẨY `,` (ví dụ $3,5$; $0,2$; $666,67$), TUYỆT ĐỐI KHÔNG dùng dấu chấm `.` kiểu phương Tây ($3.5$).
- **Dấu phân cách tọa độ / Cặp nghiệm**: BẮT BUỘC dùng dấu chấm phẩy `;` (ví dụ $A(2; 3)$, $(x; y) = (1; -2)$), không dùng dấu phẩy `,` để tránh nhầm lẫn với số thập phân.

---

### 7. Ký hiệu Hàm lượng giác, Tam giác, Cung tròn, Quan hệ hình học
- **Lượng giác**: Chuẩn hóa $\tan, \cot$ (CẤM $\text{tg}, \text{cotg}$).
- **Cung tròn**: Chuẩn mực THCS là viết bằng lời *"cung $AB$"*, *"sđ cung $AB$"*. Renderer Word hỗ trợ $\wideparen{AB} \rightarrow \⌒AB$.
- **Thứ tự đỉnh tương ứng**: Hai tam giác đồng dạng $\triangle ABC \backsim \triangle A'B'C'$ BẮT BUỘC viết đúng thứ tự các đỉnh tương ứng, từ đó suy ra đúng các cặp cạnh tỉ lệ và góc tương ứng.
- **Tên trường hợp**: Dùng tiếng Việt `(c.c.c)`, `(c.g.c)`, `(g.g)`, CẤM dùng tiếng Anh `(SSS)`, `(SAS)`, `(AA)`.
- **Độ dài đoạn thẳng**: Viết $AB$, CẤM gạch ngang trên đầu $\overline{AB}$ (dấu gạch ngang chỉ dùng cho cấu tạo số $\overline{ab}$).
- **Chia hết**: Viết lời văn *"$a$ chia hết cho $b$"*, cấm ký hiệu $b \mid a$.

---

## Kế hoạch triển khai chi tiết

### Module 1: Chuẩn hóa Ký hiệu Đồng dạng & Mũ Góc trong Word OMML (`js/khbd-docx.js`)
1. **Dấu đồng dạng `∽` (U+223D)**:
   - Thêm vào `commandMap`: `backsim: "∽", sim: "∽", backsimeq: "⋍"`.
   - Thêm vào `mathDict`: `"\\backsim": "∽", "\\sim": "∽", "\\backsimeq": "⋍"`.
   - Thêm `backsim` vào `supportedCommands` của `normalizeLatexForMath`.
2. **Ký hiệu Mũ Góc (`\widehat`, `\hat`), Vectơ (`\vec`), Gạch đầu (`\overline`)**:
   - Xây dựng `buildAccentMath(children, charValue, mathApi)` tạo thẻ XML OMML `<m:acc>` với `<m:accPr><m:chr m:val="..."/></m:accPr>`.
   - Giữ nguyên ký hiệu mũ góc `̂` (`\u0302`) cho `\widehat` và `\hat`, mũi tên `→` (`\u2192`) cho `\vec`, gạch đầu `¯` cho `\overline`.
   - Fallback `latexToUnicodeMath`: `\widehat{ABC}` chuyển đổi thành `∠ABC` hoặc `ABĈ`, không để chữ cái trơn.
3. **Ký hiệu delimiter ngoặc vuông**:
   - Hỗ trợ delimiter ngoặc vuông `[` trong `createCasesMath` / `buildCasesDelimiter` cho cấp THPT.

---

### Module 2: Khắc phục Triệt để Lỗi Bảng 2 Cột Mục d) (Cột 2 Rỗng / `---`)
1. **Cập nhật Prompt Contract (`js/khbd-prompts.js`)**:
   - Trong `ACTIVITY_TABLE_CONTRACT`, `ACTIVITY_TABLE_CONTRACT_COMPACT` và các prompt Hoạt động B, C, D:
     * **Cột PHẢI ("Nội dung") BẮT BUỘC PHẢI CÓ DỮ LIỆU**: Trình bày toàn bộ kiến thức chốt bảng: Tên mục kiến thức, định nghĩa, định lý, quy tắc giải, công thức LaTeX, ví dụ mẫu kèm đề bài và lời giải chi tiết (hoặc quy trình thao tác máy tính/kết quả thực hành).
     * **TUYỆT ĐỐI CẤM**: Để trống Cột 2, cấm ghi `---` hoặc `...`.
     * **TUYỆT ĐỐI CẤM**: Chép kiến thức ghi bảng (Quy tắc, Ví dụ, Lời giải) vào Cột Trái dưới Bước 4 `- HS: Ghi bài...`. Cột Trái Bước 4 chỉ ghi hướng dẫn sư phạm: `- GV: Nhận xét, chốt kiến thức... - HS: Ghi nhớ quy tắc và ghi chép nội dung chuẩn vào vở.` Toàn bộ nội dung cụ thể phải đưa sang Cột Phải!
2. **Cải tiến `semanticSplitActivityRow` & `mergeSplitActivityTables` (`js/khbd-app.js`, `js/khbd-docx.js`)**:
   - Khi `list.length >= 1`: Kiểm tra xem Cột 2 có bị rỗng, toàn khoảng trắng, hoặc là các placeholder vô nghĩa (`---`, `--`, `...`, `None`, `N/A`) hay không.
   - Nếu Cột 2 rỗng/placeholder nhưng Cột 1 chứa các khối nội dung ghi bảng (nhận diện bằng regex: `(?:(?:\d+\.\s*)?[A-ZÀ-Ỵ\s]{4,}|Quy tắc(?: giải)?|Định nghĩa|Định lý|Tính chất|Ví dụ \d+|Lời giải(?: Ví dụ)?):?`):
     $\rightarrow$ Tự động bóc tách (extract) phần kiến thức ghi bảng khỏi Cột 1 và chuyển sang Cột 2!
   - Nếu Cột 2 rỗng và Cột 1 không chứa khối bóc tách:
     $\rightarrow$ Tự động trích xuất từ `c) Sản phẩm` của hoạt động tương ứng để điền vào Cột 2, đảm bảo Cột 2 không bao giờ bị rỗng hoặc chỉ có `---`.
3. **Cập nhật hàm kiểm tra `assertPhasePedagogyOutput`**:
   - Kiểm tra Cột 2 của bảng: nếu Cột 2 rỗng hoặc chỉ chứa `---` / `...`, báo lỗi để kích hoạt sửa tự động (repair).

---

### Module 3: Chuẩn hóa & Khôi phục Cấu trúc 4 Phần CV 5512 (Khắc phục lỗi Hoạt động 4)
1. **Cập nhật Prompt Contract (`js/khbd-prompts.js`)**:
   - Bổ sung chỉ thị nghiêm ngặt cho `GENERATE_ACTIVITY_C`, `GENERATE_ACTIVITY_D`, `GENERATE_ACTIVITIES_AD`, `GENERATE_ACTIVITIES_AE`:
     `BẮT BUỘC ĐỦ 4 MỤC THEO ĐÚNG CÔNG VĂN 5512 (TUYỆT ĐỐI CẤM NHẢY CÓC TỪ MỤC TIÊU VÀO BẢNG TIẾN TRÌNH):`
     `### a) Mục tiêu:`
     `### b) Nội dung:`
     `### c) Sản phẩm:`
     `### d) Tổ chức thực hiện:`
     `| Hoạt động của GV và HS | Nội dung |`
   - Hướng dẫn chi tiết nội dung từng mục cho Hoạt động 4 (Vận dụng):
     + `a) Mục tiêu`: Nêu rõ mục tiêu giải quyết vấn đề thực tiễn và phát triển năng lực tự học.
     + `b) Nội dung`: Nêu rõ đề bài tình huống vận dụng thực tế trong SGK và 4 nhiệm vụ tự học ở nhà.
     + `c) Sản phẩm`: Lời giải mô hình hóa thực tế và kế hoạch tự học ghi vào vở.
     + `d) Tổ chức thực hiện`: Bảng 2 cột 4 bước.
2. **Cơ chế Tự động Bổ sung & Chuẩn hóa Cấu trúc (Auto-Repair) trong `js/khbd-app.js`**:
   - Xây dựng hàm `ensureActivityFourPartStructure(activityText, actKey, subject, topic)`:
     * Chuẩn hóa heading mục tiêu: nếu là `- Mục tiêu:` hoặc `Mục tiêu:` $\rightarrow$ đổi thành `### a) Mục tiêu:`.
     * Nếu phát hiện thiếu `b) Nội dung:` hoặc `c) Sản phẩm:` hoặc `d) Tổ chức thực hiện:` trước bảng:
       Tự động tạo các mục bị thiếu dựa trên thông tin bảng bên dưới (trích xuất nhiệm vụ/đề bài từ Bước 1 làm `b) Nội dung`, trích xuất kết quả/nghiệm từ Bước 3 làm `c) Sản phẩm`, chèn `### d) Tổ chức thực hiện:` ngay trước bảng).
     * Áp dụng trong `clipKhbdActivityMarkdown`, `finalizeParsedKhbdSection` và `applyActivityOutput`.
3. **Cập nhật kiểm thử `assertPhasePedagogyOutput`**:
   - Kiểm tra sự hiện diện của cả 4 phần `a)`, `b)`, `c)`, `d)` cho tất cả các hoạt động A, B (từng nhánh), C, D.

---

### Module 4: Chuẩn hóa Quy chuẩn Sư phạm Toán học Toàn diện
1. **Prompt Sư phạm (`js/khbd-prompts.js`, `js/khbd-app.js`)**:
   - **Phương trình tích THCS**: Cấm ngoặc vuông `[`, dùng từ "hoặc" hoặc chia "Trường hợp 1 / 2".
   - **Số thập phân & Tọa độ**: Số thập phân dùng dấu phẩy `,` ($3,5$), tọa độ và cặp nghiệm dùng dấu chấm phẩy `;` ($A(2; 3)$).
   - **Lượng giác**: Dùng $\tan, \cot$.
   - **Hình học**: Hai tam giác đồng dạng $\triangle ABC \backsim \triangle A'B'C'$ viết đúng thứ tự đỉnh tương ứng; suy ra các cặp cạnh tỉ lệ và góc tương ứng chuẩn xác. Ký hiệu chữ S nằm ngang `\backsim` hoặc `∽`.
   - **ĐKXĐ & Đối chiếu nghiệm**: Luôn có bước đối chiếu ĐKXĐ và kết luận nghiệm.

---

## File tác động
1. `js/khbd-prompts.js`:
   - Bổ sung ràng buộc bảng 2 cột: Cột 2 bắt buộc có dữ liệu, cấm rỗng/`---`, kiến thức ghi bảng phải nằm ở Cột 2.
   - Bổ sung cấu trúc 4 phần bắt buộc `### a) b) c) d)` cho Hoạt động C, Hoạt động D trong các mẫu prompt `GENERATE_ACTIVITIES_AD`, `GENERATE_ACTIVITIES_AE`, `GENERATE_ACTIVITY_D`.
   - Bổ sung quy chuẩn ký hiệu hình học (`\backsim`, `∽`, đỉnh tương ứng, `\widehat`) và toán học (không dùng `[` ở THCS, số thập phân phẩy, tọa độ chấm phẩy).
2. `js/khbd-app.js`:
   - Cải tiến `semanticSplitActivityRow` và `mergeSplitActivityTables`: bóc tách khối kiến thức chốt bảng từ Cột 1 sang Cột 2 khi Cột 2 rỗng/`---`.
   - Bổ sung hàm `ensureActivityFourPartStructure`: tự động phục hồi `### a) Mục tiêu`, `### b) Nội dung`, `### c) Sản phẩm`, `### d) Tổ chức thực hiện` nếu AI sinh thiếu.
   - Cập nhật `assertPhasePedagogyOutput`: kiểm tra 4 phần CV 5512 và kiểm tra Cột 2 không rỗng.
3. `js/khbd-docx.js`:
   - Thêm `backsim: "∽"`, `sim: "∽"`, `wideparen: "⌒"` vào `commandMap` và `mathDict`.
   - Thêm `buildAccentMath` tạo OMML `<m:acc>` cho `\widehat`, `\hat`, `\vec`, `\overline`.
   - Cập nhật `semanticSplitActivityRow` đồng bộ với `khbd-app.js` để Word DOCX không bao giờ render Cột 2 rỗng khi có kiến thức ghi bảng.
4. `tests/`:
   - Bổ sung test kiểm thử:
     * Cột 2 rỗng được tự động cứu hộ, bóc tách nội dung ghi bảng từ Cột 1 sang Cột 2.
     * Hoạt động D bị thiếu `b) Nội dung`, `c) Sản phẩm`, `d) Tổ chức thực hiện` được tự động chuẩn hóa và khôi phục đủ 4 phần.
     * Ký hiệu `\backsim` và `\sim` render ra chữ S nằm ngang `∽` (U+223D).
     * Góc `\widehat{ABC}` tạo OMML `<m:acc>`.

---

## Tiêu chí nghiệm thu (Acceptance Criteria)
1. **Cấu trúc 4 phần CV 5512**: Mọi hoạt động (A, B các nhánh, C, D) đều đảm bảo có đầy đủ 4 mục rõ ràng: `### a) Mục tiêu:`, `### b) Nội dung:`, `### c) Sản phẩm:`, `### d) Tổ chức thực hiện:`. Tuyệt đối không còn tình trạng Hoạt động 4 (Vận dụng) chỉ có Mục tiêu rồi nhảy cóc vào bảng.
2. **Bảng 2 cột cân đối & Cột 2 đầy đủ kiến thức**: Cột 2 ("Nội dung") của tất cả các hoạt động không bao giờ bị rỗng hoặc chỉ có `---`. Toàn bộ kiến thức chốt bảng (Tên mục, Định nghĩa, Quy tắc, Ví dụ mẫu & Lời giải chi tiết) nằm ở Cột 2. Nếu AI dồn nhầm vào Cột 1, hệ thống tự động bóc tách sang Cột 2.
3. **Ký hiệu Đồng dạng**: Render ra đúng chữ S nằm ngang `∽` (Unicode `U+223D`), không bị biến thành dấu ngã sóng `∼` hay dấu trừ.
4. **Ký hiệu Góc trong Word**: Công thức góc $\widehat{ABC}$ khi xuất ra Word giữ nguyên ký hiệu mũ trên đỉnh chữ thông qua thẻ OMML `<m:acc>`, không bị gọt cụt thành `ABC`.
5. **Kỷ luật Sư phạm Toán học**: Phương trình tích ở cấp THCS dùng chữ "hoặc" (không dùng `[`), số thập phân dùng dấu phẩy `,`, tọa độ dùng dấu chấm phẩy `;`, hàm lượng giác dùng $\tan, \cot$.
6. **Bộ test**: Tất cả các kịch bản kiểm thử trong `tests/` chạy `node tests/...` đều đạt kết quả PASS 100%.
