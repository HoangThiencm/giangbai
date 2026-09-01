# PLAN: Tối Ưu Định Dạng Xuống Dòng YCCĐ & NLS, Khắc Phục Lỗi Hiển Thị NLS+AI, Tự Động Tính Lại Tiết CT & Tuần Khi Kéo Thả PPCT, Và Xuất Word 13pt Dãn Dòng 1.3 Khổ Ngang

## Hiện trạng
1. **Lỗi không xuống dòng các ý trong cột "Yêu cầu cần đạt" và cột "Mã NLS & AI" (Ảnh 1)**:
   - Trong `exportDocx` và hiển thị bảng, các gạch đầu dòng YCCĐ bị nối liền thành một khối văn bản duy nhất (`.,- Nhận biết... ,- So sánh...`) do hàm `cell()` chỉ tạo 1 `Paragraph` đơn và `TextRun` không bóc tách từng dòng `\n`.
   - Các mã NLS trong cột tích hợp bị viết dính liền ngang hàng (`[NLS: 6.1.TC1a ...] [NLS: 6.2.TC1a ...]`), chưa được tách dòng riêng biệt cho từng mã.
2. **Lỗi lặp cụm "Áp dụng: tiết..." và thiếu mã NLS khi chọn AI (Ảnh 2)**:
   - Hàm `selectedIntegration` trong `xaydungphuluc.html` xử lý chuỗi regex chưa sạch, dẫn đến việc cụm `"Áp dụng: tiết 1, 2"` bị lặp lại ở cả đầu và cuối chuỗi mã (`Áp dụng: tiết 1, 2 [AI: ...] Áp dụng: tiết 1, 2.`).
   - Một số bài khi tick chọn AI lại bị mất các mã NLS chuẩn của bài. Theo nguyên tắc sư phạm: Mọi bài đều có mã NLS (theo mật độ 1–2 hoặc 2–3 mã); nếu bài/tiết đó được tick chọn AI thì phải hiển thị **cả Mã NLS VÀ Mã AI**; nếu không tick chọn AI thì **chỉ hiển thị Mã NLS**.
3. **Nhu cầu tự động cập nhật lại Tiết CT và Số tuần khi kéo thả / đổi thứ tự bài học trong PPCT**:
   - Khi người dùng kéo thả hoặc di chuyển một bài học (ví dụ: chuyển phần Ôn tập kiểm tra từ tuần 9 sang tuần 10 ở tiết 29), các bài học khác được đẩy lên.
   - Hệ thống cần **tự động tính toán lại Tiết CT luỹ kế (từ 1 đến N)** và **tính lại Số tuần phân bổ** dựa trên số tiết của từng bài học để giáo viên không phải sửa thủ công từng bài, đồng thời **vẫn cho phép chỉnh tay linh hoạt** khi cần.
4. **Lỗi hiển thị cột Tiết CT và cột Tuần trong Phụ lục 3 (Ảnh 3)**:
   - Cột "Tiết CT" khi bài học có từ 2 tiết trở lên đang bị viết dính liền cách nhau bởi dấu cách (`8 9`). Cần xuống dòng rõ ràng (dạng `8\n9` hoặc `8, 9`).
   - Cột "Tuần" bị lặp lại giá trị của từng tiết (`3 3`). Cần gộp gọn thành `3` (hoặc `Tuần 3`) khi các tiết trong cùng một tuần.
5. **Quy chuẩn định dạng xuất file Word (.docx)**:
   - Khổ giấy: A4 nằm ngang (`PageOrientation.LANDSCAPE`, `width: 16838, height: 11906`).
   - Font chữ: `Times New Roman` toàn bộ văn bản và bảng biểu.
   - Cỡ chữ chuẩn: `13pt` (`size: 26` half-points trong thư viện docx).
   - Dãn dòng (Line Spacing): `Multiple 1.3` (`spacing: { line: 312, lineRule: LineRuleType.AUTO }`).
   - Bảng biểu: Auto-fit Window (`width: { size: 100, type: WidthType.PERCENTAGE }`).

---

## Phạm vi
1. **Chuẩn hóa xuống dòng đa đoạn (Multi-paragraph) cho ô bảng trong Word & HTML**:
   - Nâng cấp hàm `cell(text, opts)` trong `exportDocx`: Bóc tách chuỗi `text` theo các dòng `\n` hoặc từng gạch đầu dòng `- `, tạo thành các `Paragraph` độc lập với cỡ chữ 13pt và dãn dòng 1.3.
   - Nâng cấp `integrationCell(value, opts)`: Xuất mỗi mã `[NLS: ...]` và `[AI: ...]` trên một dòng riêng biệt, có màu phân biệt (NLS: xanh dương `#0070C0`, AI: tím `#7030A0`).
2. **Khắc phục triệt để hàm `selectedIntegration`**:
   - Luôn đảm bảo giữ đầy đủ mã NLS của bài theo cấu hình mật độ.
   - Khi tiết có AI: Ghép mã AI vào danh sách kèm đúng phạm vi `(Áp dụng: tiết ...)`, loại bỏ hoàn toàn các chuỗi lặp thừa.
   - Khi tiết không có AI: Chỉ trả về danh sách mã NLS sạch.
3. **Cơ chế tự động tính lại Tiết CT & Tuần luỹ kế khi kéo thả / đổi thứ tự dòng PPCT**:
   - Xây dựng thuật toán `recalculatePpctSequences()`:
     * Quét toàn bộ danh sách bài học theo thứ tự từ trên xuống dưới.
     * Tính luỹ kế Tiết CT: Bài thứ $k$ có số tiết $p_k$, Tiết CT bắt đầu từ $(\text{tiết trước} + 1)$ đến $(\text{tiết trước} + p_k)$ (ví dụ: `1-2`, `3-4`, `5`, `6-7`... hoặc `1\n2`, `3\n4`).
     * Tính Số tuần tương ứng dựa trên định mức tiết/tuần của môn học (ví dụ Toán: 4 tiết/tuần -> Tiết 1-4 là Tuần 1, Tiết 5-8 là Tuần 2...).
     * Tự động chạy lại khi người dùng kéo thả (drag & drop) hoặc bấm di chuyển `▲`/`▼`.
     * Cho phép chỉnh tay trực tiếp bất kỳ ô nào nếu có tuần đặc thù.
4. **Chuẩn hóa hiển thị Tiết CT và Tuần (Phụ lục 3)**:
   - Hàm `formatTietCT(val)`: Định dạng tiết đôi/tiết ba xuống dòng ngăn cách rõ ràng (`8\n9`).
   - Hàm `formatWeek(val)`: Khử trùng lặp số tuần (`3 3` -> `3`).
5. **Cập nhật toàn diện cấu hình xuất Word (.docx)**:
   - Áp dụng khổ ngang A4, font `Times New Roman`, size `13pt` (size 26), line spacing `1.3` (`line: 312`), table 100% width auto-fit cho toàn bộ Phụ lục 1, 2, 3.

---

## Ngoài phạm vi
- Không can thiệp vào các trang khác như `soankhbd.html`.
- Không thay đổi danh mục mã năng lực số chuẩn (CV 3456) và chuẩn AI (QĐ 2422).

---

## File dự kiến tác động
- `xaydungphuluc.html` [TÍNH NĂNG TỰ ĐỘNG TÍNH LẠI TIẾT CT & TUẦN, KÉO THẢ, NÂNG CẤP cell(), integrationCell(), selectedIntegration(), CẤU HÌNH DOCX 13PT LINE 1.3 LANDSCAPE]
- `js/khbd-yccd.js` [ĐẢM BẢO getCleanOfficialYccd TRẢ CHUỖI XUỐNG DÒNG CHUẨN]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG KIỂM THỬ TỰ ĐỘNG TÍNH LẠI TIẾT CT & TUẦN, XUỐNG DÒNG VÀ ĐỊNH DẠNG WORD 13PT]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi hoàn thành triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

---

## Các bước thực hiện
1. **Bước 1: Xây dựng hàm `recalculatePpctSequences()` trong `xaydungphuluc.html`**:
   - Duyệt qua mảng `rows` (bỏ qua header):
     * Tính tổng số tiết luỹ kế `currentPeriod`.
     * Gán `tietCT`: nếu $p=1$ thì gán `String(currentPeriod)`, nếu $p>1$ thì gán `${currentPeriod - p + 1}-${currentPeriod}` (hoặc danh sách các tiết).
     * Gán `week`: `Tuần ${Math.ceil(currentPeriod / periodsPerWeek)}`.
   - Gọi tự động hàm này sau mỗi thao tác kéo thả (`reorderPpctRow`) hoặc bấm di chuyển (`movePpctRow`).
   - Thêm nút tiện ích `🔄 Tính lại Tiết CT & Tuần tự động` trên bảng Mục 3 để người dùng có thể bấm chạy lại bất cứ lúc nào.
2. **Bước 2: Nâng cấp hàm xử lý văn bản YCCĐ và ô bảng trong `xaydungphuluc.html`**:
   - Viết hàm chuẩn hóa `formatOutcomeLines(text)`: Tách các câu dạng `.,- `, `.- `, `; - ` thành từng dòng `- ...`.
   - Trong `exportDocx`: Nâng cấp hàm `cell(text, opts)` để tạo danh sách các `Paragraph` riêng biệt cho mỗi dòng text, áp dụng `font: 'Times New Roman', size: 26` (13pt) và `spacing: { line: 312 }` (multiple 1.3).
3. **Bước 3: Sửa lỗi `selectedIntegration` & tối ưu hiển thị NLS + AI**:
   - Viết lại hàm `selectedIntegration(value, selectedPeriods, index, c)`:
     * Luôn giữ mã NLS chuẩn của bài.
     * Khi có tiết AI được chọn: Nối thêm mã AI chuẩn kèm phạm vi `(Áp dụng: tiết 1, 2)`.
     * Khi không có tiết AI: Chỉ hiển thị mã NLS.
   - Cập nhật `integrationCell`: Mỗi mã NLS / AI nằm trên 1 dòng riêng (`Paragraph` riêng).
4. **Bước 4: Chuẩn hóa hiển thị Tiết CT và Tuần trong Phụ lục 3**:
   - Hàm `cleanTietCT(val)`: Xuống dòng giữa các tiết đôi/ba (`8\n9`).
   - Hàm `cleanWeek(val)`: Khử trùng lặp (`3 3` -> `3`).
5. **Bước 5: Chuẩn hóa toàn bộ tham số xuất Word trong `exportDocx`**:
   - Font: `Times New Roman`, Size: `13pt` (`size: 26`), Dãn dòng: `1.3` (`spacing: { line: 312 }`), Khổ ngang A4 (`16838 x 11906`), Bảng: `100% width`.
6. **Bước 6: Cập nhật kiểm thử tự động `tests/xaydungphuluc-smoke.js`**:
   - Kiểm tra `recalculatePpctSequences()` tính đúng luỹ kế Tiết CT và Tuần khi đổi vị trí dòng.
   - Kiểm tra các tiêu chí xuống dòng, khử lặp tuần, mã NLS+AI và định dạng Word 13pt.
7. **Bước 7: Khóa trạng thái giao việc**:
   - Ghi `LOCK` vào `docs/handoff/.lock`.

---

## Rủi ro & Giải pháp
1. **Rủi ro người dùng đã chỉnh tay số tuần nhưng khi kéo thả bị tính đè lại**:
   - *Giải pháp*: Cho phép người dùng bật/tắt chế độ tự động tính lại (Auto-recalculate checkbox/nút bấm) hoặc cho phép chỉnh tay ghi đè trực tiếp bất kỳ ô nào.
2. **Rủi ro các môn có số tiết/tuần khác nhau (Toán: 4 tiết, KHTN: 4 tiết, Ngữ văn: 4 tiết, GDĐP: 1 tiết)**:
   - *Giải pháp*: Tự động nhận diện định mức số tiết/tuần dựa trên môn học và tổng số tiết/35 tuần để phân bổ số tuần chính xác nhất.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - `node tests/xaydungphuluc-smoke.js`
   - `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html`:
     * Kéo một bài học (ví dụ bài Ôn tập kiểm tra) từ tuần 9 xuống vị trí tuần sau (tiết 29) -> Kiểm tra Tiết CT và Tuần của toàn bộ bảng tự động cập nhật lại luỹ kế liên tục, chính xác.
     * Thử chỉnh tay trực tiếp vào ô Tuần / Tiết CT -> Giá trị cập nhật ngay lập tức.
     * Xuất Word (.docx) -> Kiểm tra file Word đẹp, chuẩn 13pt, dãn dòng 1.3, khổ ngang, xuống dòng rõ ràng.

---

## Tiêu chí nghiệm thu
- [x] Khi kéo thả hoặc di chuyển thứ tự bài học trong PPCT, hệ thống hỗ trợ **tự động tính toán lại Tiết CT luỹ kế và Số tuần phân bổ liên tục**, đồng thời **vẫn cho phép chỉnh tay linh hoạt**.
- [x] Cột "Yêu cầu cần đạt" ở Phụ lục 1 xuống dòng chuẩn từng ý gạch đầu dòng trong cả bản xem trước HTML và file Word (.docx).
- [x] Mỗi mã NLS và AI được hiển thị trên 1 dòng riêng; bài có tick AI hiển thị đầy đủ cả NLS + AI không bị lặp chuỗi "Áp dụng: tiết...".
- [x] Cột "Tiết CT" trong Phụ lục 3 xuống dòng ngăn cách giữa các tiết đôi/ba; cột "Tuần" tự động khử trùng lặp (không còn hiện tượng `3 3`).
- [x] File Word (.docx) xuất ra đạt 100% chuẩn: Khổ A4 Landscape, font Times New Roman, cỡ chữ 13pt, dãn dòng 1.3, bảng auto-fit 100% width.
- [x] 100% bộ test `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` đạt PASS.
