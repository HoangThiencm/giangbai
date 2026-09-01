# PLAN: Tối Ưu Định Dạng Xuống Dòng YCCĐ & NLS, Khắc Phục Lỗi Hiển Thị Mã NLS + AI, Chuẩn Hóa Cột Tiết CT / Tuần (Phụ Lục 3) Và Quy Chuẩn Xuất File Word 13pt Dãn Dòng 1.3 Khổ Ngang

## Hiện trạng
1. **Lỗi không xuống dòng các ý trong cột "Yêu cầu cần đạt" và cột "Mã NLS & AI" (Ảnh 1)**:
   - Trong `exportDocx` và hiển thị bảng, toàn bộ các gạch đầu dòng YCCĐ bị nối liền thành một khối văn bản duy nhất (`.,- Nhận biết... ,- So sánh...`) do hàm `cell()` chỉ tạo 1 `Paragraph` đơn và `TextRun` không bóc tách từng dòng `\n`.
   - Các mã NLS trong cột tích hợp bị viết dính liền ngang hàng (`[NLS: 6.1.TC1a ...] [NLS: 6.2.TC1a ...]`), chưa được tách dòng riêng biệt cho từng mã.
2. **Lỗi lặp cụm "Áp dụng: tiết..." và thiếu mã NLS khi chọn AI (Ảnh 2)**:
   - Hàm `selectedIntegration` trong `xaydungphuluc.html` xử lý chuỗi regex chưa sạch, dẫn đến việc cụm `"Áp dụng: tiết 1, 2"` bị lặp lại ở cả đầu và cuối chuỗi mã (`Áp dụng: tiết 1, 2 [AI: ...] Áp dụng: tiết 1, 2.`).
   - Một số bài khi tick chọn AI lại bị mất các mã NLS chuẩn của bài. Theo nguyên tắc sư phạm: Mọi bài đều có mã NLS (theo mật độ 1–2 hoặc 2–3 mã); nếu bài/tiết đó được tick chọn AI thì phải hiển thị **cả Mã NLS VÀ Mã AI**; nếu không tick chọn AI thì **chỉ hiển thị Mã NLS**.
3. **Lỗi hiển thị cột Tiết CT và cột Tuần trong Phụ lục 3 (Ảnh 3)**:
   - Cột "Tiết CT" khi bài học có từ 2 tiết trở lên đang bị viết dính liền cách nhau bởi dấu cách (`8 9`). Cần xuống dòng rõ ràng (dạng `8\n9` hoặc `8, 9`).
   - Cột "Tuần" bị lặp lại giá trị của từng tiết (`3 3`). Cần gộp gọn thành `3` (hoặc `Tuần 3`) khi các tiết trong cùng một tuần, chỉ hiển thị nhiều tuần khi bài dạy vắt qua tuần khác (vd: `3\n4` hoặc `3, 4`).
4. **Quy chuẩn định dạng xuất file Word (.docx) chưa đạt chuẩn hành chính giáo dục**:
   - Cần cấu hình chuẩn xác:
     * Khổ giấy: A4 nằm ngang (`PageOrientation.LANDSCAPE`, `width: 16838, height: 11906`).
     * Font chữ: `Times New Roman` toàn bộ văn bản và bảng biểu.
     * Cỡ chữ chuẩn: `13pt` (tương đương `size: 26` half-points trong thư viện docx).
     * Dãn dòng (Line Spacing): `Multiple 1.3` (tương đương `spacing: { line: 312, lineRule: LineRuleType.AUTO }`).
     * Bảng biểu: Auto-fit Window (`width: { size: 100, type: WidthType.PERCENTAGE }`) với tỷ lệ phân bổ các cột cân đối, thoáng đãng, trình bày đẹp mắt.

---

## Phạm vi
1. **Chuẩn hóa xuống dòng đa đoạn (Multi-paragraph) cho ô bảng trong Word & HTML**:
   - Nâng cấp hàm `cell(text, opts)` trong `exportDocx`: Bóc tách chuỗi `text` theo các dòng `\n` hoặc từng gạch đầu dòng `- `, tạo thành các `Paragraph` độc lập với cỡ chữ 13pt và dãn dòng 1.3.
   - Nâng cấp `integrationCell(value, opts)`: Xuất mỗi mã `[NLS: ...]` và `[AI: ...]` trên một dòng riêng biệt, có màu phân biệt (NLS: xanh dương `#0070C0`, AI: tím `#7030A0`).
2. **Khắc phục triệt để hàm `selectedIntegration`**:
   - Luôn đảm bảo giữ đầy đủ mã NLS của bài theo cấu hình mật độ.
   - Khi tiết có AI: Ghép mã AI vào danh sách kèm đúng phạm vi `(Áp dụng: tiết ...)`, loại bỏ hoàn toàn các chuỗi lặp thừa.
   - Khi tiết không có AI: Chỉ trả về danh sách mã NLS sạch.
3. **Chuẩn hóa hiển thị cột "Tiết CT" và cột "Tuần" (Phụ lục 3)**:
   - Hàm chuẩn hóa `formatTietCT(val)`: Định dạng tiết đôi/tiết ba xuống dòng ngăn cách rõ ràng (`8\n9`).
   - Hàm chuẩn hóa `formatWeek(val)`: Khử trùng lặp số tuần (`3 3` -> `3`).
4. **Cập nhật toàn diện cấu hình xuất Word (.docx)**:
   - Áp dụng khổ ngang A4, font `Times New Roman`, size `13pt` (size 26), line spacing `1.3` (`line: 312`), table 100% width auto-fit cho toàn bộ Phụ lục 1, 2, 3.

---

## Ngoài phạm vi
- Không thay đổi danh mục mã năng lực số chuẩn (CV 3456) và chuẩn AI (QĐ 2422).
- Không can thiệp sang các trang khác như `soankhbd.html`.

---

## File dự kiến tác động
- `xaydungphuluc.html` [NÂNG CẤP cell(), integrationCell(), selectedIntegration(), formatTietCT(), formatWeek(), CẤU HÌNH DOCX 13PT LINE 1.3 LANDSCAPE]
- `js/khbd-yccd.js` [ĐẢM BẢO getCleanOfficialYccd TRẢ CHUỖI XUỐNG DÒNG CHUẨN ĐẦU VÀO]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG KIỂM THỬ XUỐNG DÒNG, GỘP TUẦN, MÃ NLS+AI VÀ ĐỊNH DẠNG WORD 13PT]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi hoàn thành triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

---

## Các bước thực hiện
1. **Bước 1: Nâng cấp hàm xử lý văn bản YCCĐ và ô bảng trong `xaydungphuluc.html`**:
   - Viết hàm chuẩn hóa `formatOutcomeLines(text)`: Tách các câu dạng `.,- `, `.- `, `; - ` thành từng dòng `- ...`.
   - Trong `exportDocx`: Nâng cấp hàm `cell(text, opts)` để tạo danh sách các `Paragraph` riêng biệt cho mỗi dòng text, áp dụng `font: 'Times New Roman', size: 26` (13pt) và `spacing: { line: 312 }` (multiple 1.3).
2. **Bước 2: Sửa lỗi `selectedIntegration` & tối ưu hiển thị NLS + AI**:
   - Viết lại hàm `selectedIntegration(value, selectedPeriods, index, c)`:
     * Trích xuất các mã NLS từ dữ liệu gốc hoặc từ `getStandardCompetenciesForLesson`.
     * Nếu có tiết AI được chọn: Lấy mã AI chuẩn của bài/lớp, gắn đúng đuôi `(Áp dụng: tiết 1, 2)`.
     * Trả về kết quả sạch, không bị lặp từ khóa `Áp dụng`.
   - Cập nhật `integrationCell`: Mỗi mã NLS / AI nằm trên 1 dòng riêng (`Paragraph` riêng).
3. **Bước 3: Chuẩn hóa hiển thị Tiết CT và Tuần trong Phụ lục 3**:
   - Hàm xử lý `cleanTietCT(val)`: Nếu chuỗi dạng `8 9` hoặc `8-9`, tách và định dạng xuống dòng `8\n9` (trong Word thành 2 dòng của 1 ô).
   - Hàm xử lý `cleanWeek(val)`: Tách các số tuần, lọc `[...new Set(weeks)]`, nối lại dạng `3` hoặc `3\n4` nếu khác tuần.
4. **Bước 4: Chuẩn hóa toàn bộ tham số xuất Word trong `exportDocx`**:
   - Cài đặt mặc định cho document:
     * Font: `Times New Roman`
     * Size văn bản thông thường và bảng biểu: `13pt` (`size: 26`)
     * Tiêu đề lớn: `14pt` in đậm (`size: 28`)
     * Khoảng cách dòng: `spacing: { line: 312, lineRule: LineRuleType.AUTO }`
     * Khổ giấy: A4 Landscape (`width: 16838, height: 11906`)
     * Căn lề: 1.5cm - 2cm (`top: 1134, bottom: 1134, left: 1134, right: 1134`)
     * Bảng: `width: { size: 100, type: WidthType.PERCENTAGE }`
5. **Bước 5: Cập nhật kiểm thử tự động `tests/xaydungphuluc-smoke.js`**:
   - Kiểm tra `cell()` sinh nhiều paragraphs khi text có xuống dòng.
   - Kiểm tra `cleanWeek('3 3')` trả về `'3'`.
   - Kiểm tra `cleanTietCT('8 9')` trả về `'8\n9'`.
   - Kiểm tra `selectedIntegration` chứa cả NLS và AI khi được tick, không bị lặp từ khóa.
   - Kiểm tra cấu hình Word có font size 26 (13pt) và line spacing 312.
6. **Bước 6: Khóa trạng thái giao việc**:
   - Ghi `LOCK` vào `docs/handoff/.lock`.

---

## Rủi ro & Giải pháp
1. **Rủi ro ô bảng có quá nhiều gạch đầu dòng làm tăng độ dài trang**:
   - *Giải pháp*: Đặt `spacing: { line: 312, before: 40, after: 40 }` vừa vặn, không để khoảng cách đoạn quá lớn giữa các gạch đầu dòng trong cùng một ô.
2. **Rủi ro cột Tuần có dữ liệu phức tạp (vd: "Tuần 3, 4" hoặc "3-4")**:
   - *Giải pháp*: Dùng regex bóc tách số thông minh để khử trùng lặp chính xác mà không làm mất thông tin tuần thực tế.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - `node tests/xaydungphuluc-smoke.js`
   - `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html`:
     * Kiểm tra Phụ lục 1: Cột "Yêu cầu cần đạt" xuống dòng rõ ràng từng ý gạch đầu dòng (không bị dính liền `.,- `).
     * Kiểm tra cột "Mã NLS & AI": Mỗi mã nằm trên 1 dòng riêng; bài có chọn AI hiển thị cả mã NLS và mã AI kèm `(Áp dụng: tiết 1, 2)` sạch sẽ, không bị lặp.
     * Kiểm tra Phụ lục 3: Cột Tiết CT xuống dòng `8\n9`, cột Tuần không bị lặp `3 3`.
     * Xuất file Word (.docx): Mở file Word kiểm tra đúng khổ ngang A4, font Times New Roman 13pt, dãn dòng 1.3, bảng tự động căn tràn lề đẹp mắt.

---

## Tiêu chí nghiệm thu
- [x] Cột "Yêu cầu cần đạt" ở Phụ lục 1 xuống dòng chuẩn từng ý gạch đầu dòng trong cả bản xem trước HTML và file Word (.docx).
- [x] Mỗi mã NLS và AI được hiển thị trên 1 dòng riêng; bài có tick AI hiển thị đầy đủ cả NLS + AI không bị lặp chuỗi "Áp dụng: tiết...".
- [x] Cột "Tiết CT" trong Phụ lục 3 xuống dòng ngăn cách giữa các tiết đôi/ba; cột "Tuần" tự động khử trùng lặp (không còn hiện tượng `3 3`).
- [x] File Word (.docx) xuất ra đạt 100% chuẩn: Khổ A4 Landscape, font Times New Roman, cỡ chữ 13pt, dãn dòng 1.3, bảng auto-fit 100% width.
- [x] 100% bộ test `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` đạt PASS.
