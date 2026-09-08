# PLAN: Phân hóa Triệt để Năng lực số (NLS) và Trợ lý AI Sư phạm theo Cấp độ Nhận thức từng Bài học trong Kho Tri thức SGK

## Hiện trạng & Phản ánh của Người dùng
- **Phản ánh từ User**:
  > *"nhưng mà năng lực số của cả các bài này giống nhau đều được hả? bài 1 mới nhận biết thôi mà. Bài 2 mới giải hệ pt, bài 3 thì lại liên quan giải bài toán bằng cách lập pt. Đây là tôi ví dụ. Mỗi bài đều có năng lực số, AI khác nhau chứ. Cho dù là nạp từ SGK hay nạp từ tri thức. Chỗ này bị nhầm lẫn nè"*

- **Khảo sát gốc rễ mã nguồn**:
  1. **Trong `js/khbd-standards.js`**:
     - Hàm `scoreOfficialStandard` khi chấm điểm nhánh `algebra`:
       Gom chung toàn bộ bài học có chữ "phuong trinh" vào một rổ, luôn cộng điểm tối đa cho `5.3`, `3.1`, `5.2`.
       Không phân biệt bài **Khái niệm / Nhận biết** (Bài 1) với bài **Rèn kỹ năng giải** (Bài 2) với bài **Mô hình hóa thực tế** (Bài 3).
  2. **Trong `recommendLessonDigitalCandidates` (`xaydungphuluc.html` & Canvas)**:
     - Dùng regex gộp trả về cùng bộ mã `5.3.TC2a, 3.1.TC2a, 5.2.TC2a` cho cả 3 bài.
  3. **Trong `lessonAppliedNlsDescription` (`xaydungphuluc.html` & Canvas)**:
     - Khi kiểm tra `isEquation`, sinh ra đúng một mẫu văn bản dập khuôn:
       * 5.3: *"Sử dụng máy tính cầm tay để tìm nghiệm, kiểm tra nghiệm và phần mềm GeoGebra/Desmos vẽ đồ thị minh họa nghiệm hình học..."*
       * 3.1: *"Sử dụng công cụ số (GeoGebra/trình chiếu) để mô hình hóa và trình bày các bước giải..."*
     - Hậu quả sư phạm: Bài 1 mới học "Khái niệm phương trình" (chưa học cách giải) nhưng bị gán "trình bày các bước giải" và "vẽ đồ thị minh họa nghiệm hình học"!
  4. **Trong `lessonAppliedAiDescription` (`xaydungphuluc.html` & Canvas)**:
     - Nhánh domain B luôn trả về câu cố định:
       *"Ứng dụng công cụ AI hỗ trợ gợi ý các bước giải bài ${clean}, học sinh đối chiếu kết quả với SGK..."*
     - Cả Bài 1, Bài 2, Bài 3 đều có chung một câu gợi ý giải bài tập, làm mất tính sư phạm phân hóa.
  5. **Dữ liệu CSDL máy chủ hosting (`hoangthiencm.id.vn`)**:
     - Kho tri thức Toán 9 đang lưu 32 bài học, trong đó Bài 1, Bài 2, Bài 3 đang chứa cùng các đoạn minh chứng NLS và gợi ý AI dập khuôn do được sinh từ engine cũ.

---

## Mục tiêu Cần đạt
1. **Phân hóa rõ rệt 3 cấp độ nhận thức sư phạm cho chủ đề Phương trình & Hệ phương trình (điển hình Toán 9 Bài 1, 2, 3)**:
   - **Bài 1 (Khái niệm, Nhận biết)**:
     * NLS: `1.1.TC2a, 5.3.TC2a, 3.1.TC2a`
     * Minh chứng: Khai thác video/học liệu số nhận diện dạng ax+by=c; Dùng máy tính cầm tay (CALC / tính giá trị biểu thức) kiểm tra cặp số (x0; y0) có là nghiệm không; Phần mềm sơ đồ tư duy hệ thống hóa cấu trúc tổng quát và tập nghiệm.
     * AI: Trợ lý AI tạo ví dụ ngẫu nhiên cặp số và phương trình/hệ phương trình để học sinh luyện tập kiểm tra nghiệm, phân tích nguyên nhân thỏa mãn hoặc không thỏa mãn định nghĩa.
   - **Bài 2 (Kỹ năng giải, Thuật toán giải)**:
     * NLS: `5.3.TC2a, 5.1.TC2a, 5.2.TC2a`
     * Minh chứng: Sử dụng chức năng giải hệ (EQUATION/SIMULT) trên máy tính cầm tay kiểm tra kết quả giải bằng phương pháp thế hoặc cộng đại số; Xử lý thông báo vô số nghiệm (Infinite Solutions) / vô nghiệm (No Solution) hoặc lỗi cú pháp; GeoGebra minh họa giao điểm 2 đường thẳng biểu diễn số nghiệm.
     * AI: Trợ lý AI phân tích hệ số đề xuất lựa chọn phương pháp giải tối ưu (phương pháp thế hay cộng đại số); học sinh tự biến đổi và kiểm chứng kết quả.
   - **Bài 3 (Giải bài toán thực tế / Mô hình hóa toán học)**:
     * NLS: `3.1.TC2a, 5.3.TC2a, 1.2.TC2a`
     * Minh chứng: Bảng tính Excel/Sheets lập bảng phân tích đại lượng (vận tốc, thời gian, quãng đường; năng suất...); Máy tính cầm tay giải hệ và kiểm tra đối chiếu điều kiện thực tế của ẩn (nghiệm nguyên, dương, nằm trong khoảng cho phép); Đánh giá tính hợp lý và độ tin cậy của kết quả số so với đời sống.
     * AI: Trợ lý AI phản biện bước chọn ẩn số, đặt điều kiện thực tế và gợi mở mối liên hệ ràng buộc giữa các đại lượng; học sinh tự xây dựng hệ phương trình, giải và chịu trách nhiệm.

2. **Mở rộng phân hóa sư phạm cho toàn bộ các dạng bài học Toán và các môn học**:
   - Khái niệm / Mở đầu vs Thuật toán / Biến đổi / Phép tính vs Bài toán thực tế / Mô hình hóa.
   - Hàm số & Đồ thị: Khái niệm (bảng giá trị TABLE) vs Vẽ đồ thị (GeoGebra khảo sát đỉnh/hướng) vs Bài toán thực tế.
   - Hình học: Khái niệm mở đầu vs Định lý/Tính toán (tỉ số lượng giác, hệ thức lượng) vs Hình học không gian 3D.
   - Thống kê: Bảng số liệu & Tần số vs Bảng tần số tương đối/ghép nhóm vs Phép thử & Xác suất thực nghiệm.

3. **Đồng bộ mã nguồn & CSDL**:
   - Cập nhật engine đề xuất trong `js/khbd-standards.js`.
   - Cập nhật các hàm sinh NLS & AI trong `xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`.
   - Cập nhật danh mục `DEFAULT_MATH_CATALOG` (Toán 6, 7, 8, 9).
   - Đẩy dữ liệu chuẩn hóa lên CSDL máy chủ hosting `hoangthiencm.id.vn` qua API `action=save`.
   - Bổ sung bộ kiểm thử tự động trong `tests/sgk-knowledge-smoke.js` và đảm bảo 100% test suites PASS.

---

## Kế hoạch: Hỗ trợ Đa mã Năng lực AI (Multi-Code AI) theo Khung QĐ 2422

### 1. Hiện trạng & Phản ánh của Người dùng
- **Phản ánh từ User**:
  > *"ủa bài nào cũng chỉ có 1 mã năng lực AI à, nhiều khi sẽ có hơn thì sao?"*
- **Khảo sát gốc rễ mã nguồn**:
  + Trong Kho Tri thức SGK (`sgk_lessons`), trường `ai_pedagogy_hint` trước đây chỉ lưu 1 câu mô tả đơn lẻ, không có mảng `ai_candidates` như `digital_candidates` của NLS.
  + Trong Modal Chi tiết SGK (`openSgkDetailModal`), NLS được hiển thị đẹp mắt với Badge đa mã `[Mã NLS: 5.3.TC2a] [Mã NLS: 5.1.TC2a] [Mã NLS: 5.2.TC2a]` và danh sách hành động phân rã, trong khi AI chỉ hiển thị đúng 1 dòng văn bản thô.
  + Hàm `fallbackAiCode` chỉ trả về 1 mã duy nhất (`[AI: ${code} - ${desc}]`).
  + Dù giao diện đã có dropdown `#aiDensity` với các lựa chọn `1–2 mã/bài`, `2–3 mã/bài`, `3–4 mã/bài`, luồng fallback và nạp tri thức vẫn bị gò bó vào 1 mã đơn lẻ.

### 2. Mục tiêu Sư phạm & Kỹ thuật
1. **Cặp đôi mã AI chuẩn mực theo QĐ 2422**:
   - Kết hợp giữa **Làm chủ kỹ thuật / Ra lệnh / Khai thác (Miền A)** và **Đạo đức, Trách nhiệm & Đối chiếu kiểm chứng (Miền B)** hoặc **Đánh giá phản biện (Miền D)**:
     * *Bài 1 (Khái niệm)*: `9.B2.1` (kiểm chứng định nghĩa, chịu trách nhiệm) + `9.A3.2` (dùng AI tạo ví dụ ngẫu nhiên, rèn luyện tư duy logic).
     * *Bài 2 (Giải hệ)*: `9.B2.1` (định hướng phương pháp giải tối ưu, đối chiếu SGK) + `9.A3.1` (phản biện các bước giải, đối chiếu nhiều cách giải khác nhau).
     * *Bài 3 (Toán thực tế)*: `9.B2.1` (phản biện bước chọn ẩn số, ràng buộc đại lượng) + `9.D1.1` (đánh giá mức độ tin cậy và tính khả thi của mô hình thực tế).
2. **Xây dựng hàm `recommendLessonAiCandidates(lessonTitle, grade, subject)`**:
   - Trả về bộ 1–2 mã AI phân hóa theo từng dạng bài và khối lớp (Toán 6, 7, 8, 9).
3. **Xây dựng `renderSgkDetailAiBlock(l, grade)` trong Modal Chi tiết SGK**:
   - Hiển thị các Badge màu tím `[Mã AI: 9.B2.1] [Mã AI: 9.A3.1]` nổi bật.
   - Danh sách hành động sư phạm riêng cho từng mã AI, có viền `border-purple-400` tương xứng và đồng bộ 100% với khối Năng lực số.
4. **Nâng cấp `fallbackAiCodes(index, c, lesson, lessonPeriods, selectedAiPeriods)`**:
   - Tự động cấp **2 mã AI** khi giáo viên chọn mật độ `2–3 mã/bài` hoặc khi bài học có từ 2 tiết AI trở lên (`selectedAiPeriods.length >= 2`).
   - Cả 2 mã đều được bọc trong cấu trúc chuẩn và nhận đúng phạm vi tiết `(Áp dụng: tiết ...)`.
5. **Đồng bộ 1-1 và Kiểm thử Toàn diện**:
   - Đồng bộ `xaydungphuluc.html`, `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html` (đạt 100% byte-identical cho Canvas).
   - Chạy `tests/run-all-tests.js` bảo đảm ALL 60 test suites PASS 100%.

---

## Kế hoạch: Xử lý Triệt để Equation Word (PL3), Rà soát PL2 và Đồng bộ 100% NLS & AI (PL1–PL3)

### 1. Hiện trạng & Phản ánh của Người dùng
- **Phản ánh từ User**:
  > *"trong phụ lục 3 xuất word còn mã latex $..$ chứ đã chuyển nó sang equation đâu?, rồi rà soát lại PL 2 đảm bảo chưa? PL1 và PL 3 có giống nhau mã NLS và AI không"*

- **Khảo sát gốc rễ mã nguồn**:
  1. **Về lỗi sót `$..$` trong Phụ lục 3**:
     - Trong `js/khbd-docx.js`: Regex `parseInlineTextToRuns` có nhánh `\[(?:NLS|AI|...)(?::\s*[^\]\r\n]+)?\]` bắt trọn toàn bộ khối `[NLS: ...]` và `[AI: ...]`. Khi một khối chứa công thức `$ax + by = c$` hoặc `$\begin{cases}...\end{cases}$`, nhánh này đẩy thẳng toàn bộ chuỗi vào `this.coloredTextRun(token, ...)`, bỏ qua hoàn toàn việc convert công thức toán bên trong thành `createNativeMath`! Vì vậy, các mã NLS/AI ở Phụ lục 3 (cột 7) và Phụ lục 1 xuất Word bị lộ nguyên ký tự `$`.
     - Trong `autoWrapMathInDelimiters`:
       * Các số mũ/chỉ số dưới dạng Unicode (`²`, `³`, `₀`, `₁`) không được nhận diện trong `eqRegex`, khiến phương trình dạng `y = ax² (a ≠ 0)` bị đóng dấu `$` sai vị trí (`$y = ax$² $(a \ne 0)$`).
       * Phân số có biểu thức lồng nhau như `\frac{-b \pm \sqrt{\Delta}}{2a}` bị dừng sớm do regex `\{[^{}]*\}` không hỗ trợ ngoặc nhọn lồng nhau.
  2. **Về rà soát Phụ lục 2**:
     - Phụ lục 2 là "Khung kế hoạch tổ chức các hoạt động giáo dục của tổ chuyên môn" theo CV 5512.
     - Yêu cầu chuẩn: 10 cột dữ liệu (STT, Chủ đề (1), Yêu cầu cần đạt (2), Số tiết (3), Thời điểm (4), Địa điểm (5), Chủ trì (6), Phối hợp (7), Điều kiện thực hiện (8), Mã NLS & AI). Số lượng từ 4 đến 6 hoạt động STEM / trải nghiệm, rải đều học kỳ I và II.
  3. **Về sự đồng bộ NLS và AI giữa Phụ lục 1 và Phụ lục 3**:
     - Về nguyên tắc sư phạm của CV 5512: Phụ lục 3 (Kế hoạch giáo dục của giáo viên) phải kế thừa và thống nhất 100% với Phụ lục 1 (Kế hoạch dạy học của Tổ chuyên môn).
     - Trong hàm `lessonsMatch`: Có lỗi so khớp substring (`source.includes(generated)`) chạy trước kiểm tra thứ tự bài (`sourceNumber === generatedNumber`). Khi Bài 1 có tên "Bài 1. Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn" chứa cụm "hệ hai phương trình bậc nhất hai ẩn", nó khiến Bài 2 ("Bài 2. Giải hệ hai phương trình bậc nhất hai ẩn") bị nhận nhầm thành Bài 1, dẫn đến việc lấy sai mã NLS/AI của Bài 1 cho Bài 2!

### 2. Giải pháp Thực hiện
1. **Xử lý triệt để Equation Word trong `js/khbd-docx.js`**:
   - Thêm `pushMarkerWithMath` trong `parseInlineTextToRuns`: Tách nội dung bên trong badge `[NLS: ...]` và `[AI: ...]`, chuyển 100% công thức toán thành `createNativeMath` (`<m:oMath>`), đồng thời giữ nguyên màu sắc, shading và bold cho văn bản bao quanh.
   - Nâng cấp `autoWrapMathInDelimiters`: Tiền chuẩn hóa số mũ Unicode (`⁰`...`⁹`, `ⁿ`, `ˣ`), ký hiệu Hy Lạp (`Δ`, `π`, `α`...), hỗ trợ ngoặc lồng nhau `\{(?:[^{}]|\{[^{}]*\})*\}` cho `\frac` và `\sqrt`.
2. **Sửa dứt điểm hàm `lessonsMatch`**:
   - Ưu tiên kiểm tra `lessonOrdinal` trước: Nếu cả 2 bài đều có số thứ tự bài (Bài 1 vs Bài 2) thì bắt buộc `sourceNumber === generatedNumber`. Không bao giờ để Bài 2 bị nhầm sang Bài 1.
3. **Kiểm tra và xác nhận Phụ lục 2**:
   - Đảm bảo đầy đủ 10 cột theo CV 5512, 4–6 hoạt động STEM/trải nghiệm và tích hợp NLS/AI.
4. **Kiểm tra và xác nhận đồng bộ Phụ lục 1 và Phụ lục 3**:
   - Kiểm tra `syncIntegrationFromAppendixOne` để bảo đảm 100% mã NLS và AI từ PL1 được kế thừa chuẩn xác sang cột 7 của PL3.

