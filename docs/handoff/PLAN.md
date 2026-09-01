# PLAN: Tối Ưu Định Dạng Xuống Dòng YCCĐ & NLS, Khắc Phục Lỗi Hiển Thị NLS+AI, Bổ Sung Thêm/Xóa/Di Chuyển Dòng PPCT Kèm Tự Động Tính Lại Tiết CT & Tuần, Và Xuất Word 13pt Dãn Dòng 1.3 Khổ Ngang

## Hiện trạng
1. **Chưa có tính năng Thêm dòng mới hoặc Xóa dòng tại vị trí bất kỳ trong Bảng PPCT (Mục 3)**:
   - Hiện tại bảng PPCT ở Mục 3 sau khi nhận diện từ file PDF/Word/Excel chỉ hiển thị các dòng cố định và cho phép sửa số tiết.
   - Khi giáo viên muốn chèn thêm một bài học mới, thêm tiết ôn tập/kiểm tra tại một vị trí bất kỳ (ví dụ chèn sau Bài 5 hoặc giữa Học kì I), hoặc muốn xóa bỏ một dòng không cần thiết thì chưa có nút thao tác trực tiếp trên bảng.
2. **Nhu cầu tự động cập nhật lại Tiết CT và Số tuần khi Thêm, Xóa hoặc Kéo thả / Đổi thứ tự bài học trong PPCT**:
   - Khi người dùng thêm dòng, xóa dòng, hoặc di chuyển bài học (ví dụ: chuyển phần Ôn tập kiểm tra từ tuần 9 sang tuần 10 ở tiết 29):
   - Hệ thống cần **tự động tính toán lại Tiết CT luỹ kế (từ 1 đến N)** và **tính lại Số tuần phân bổ** dựa trên số tiết của từng bài học để giáo viên không phải sửa thủ công từng bài, đồng thời **vẫn cho phép chỉnh tay linh hoạt** khi cần.
3. **Lỗi không xuống dòng các ý trong cột "Yêu cầu cần đạt" và cột "Mã NLS & AI" (Ảnh 1)**:
   - Trong `exportDocx` và hiển thị bảng, các gạch đầu dòng YCCĐ bị nối liền thành một khối văn bản duy nhất (`.,- Nhận biết... ,- So sánh...`) do hàm `cell()` chỉ tạo 1 `Paragraph` đơn và `TextRun` không bóc tách từng dòng `\n`.
   - Các mã NLS trong cột tích hợp bị viết dính liền ngang hàng (`[NLS: 6.1.TC1a ...] [NLS: 6.2.TC1a ...]`), chưa được tách dòng riêng biệt cho từng mã.
4. **Lỗi lặp cụm "Áp dụng: tiết..." và thiếu mã NLS khi chọn AI (Ảnh 2)**:
   - Hàm `selectedIntegration` trong `xaydungphuluc.html` xử lý chuỗi regex chưa sạch, dẫn đến việc cụm `"Áp dụng: tiết 1, 2"` bị lặp lại ở cả đầu và cuối chuỗi mã (`Áp dụng: tiết 1, 2 [AI: ...] Áp dụng: tiết 1, 2.`).
   - Một số bài khi tick chọn AI lại bị mất các mã NLS chuẩn của bài. Theo nguyên tắc sư phạm: Mọi bài đều có mã NLS (theo mật độ 1–2 hoặc 2–3 mã); nếu bài/tiết đó được tick chọn AI thì phải hiển thị **cả Mã NLS VÀ Mã AI**; nếu không tick chọn AI thì **chỉ hiển thị Mã NLS**.
5. **Lỗi hiển thị cột Tiết CT và cột Tuần trong Phụ lục 3 (Ảnh 3)**:
   - Cột "Tiết CT" khi bài học có từ 2 tiết trở lên đang bị viết dính liền cách nhau bởi dấu cách (`8 9`). Cần xuống dòng rõ ràng (dạng `8\n9` hoặc `8, 9`).
   - Cột "Tuần" bị lặp lại giá trị của từng tiết (`3 3`). Cần gộp gọn thành `3` (hoặc `Tuần 3`) khi các tiết trong cùng một tuần.
6. **Quy chuẩn định dạng xuất file Word (.docx)**:
   - Khổ giấy: A4 nằm ngang (`PageOrientation.LANDSCAPE`, `width: 16838, height: 11906`).
   - Font chữ: `Times New Roman` toàn bộ văn bản và bảng biểu.
   - Cỡ chữ chuẩn: `13pt` (`size: 26` half-points trong thư viện docx).
   - Dãn dòng (Line Spacing): `Multiple 1.3` (`spacing: { line: 312, lineRule: LineRuleType.AUTO }`).
   - Bảng biểu: Auto-fit Window (`width: { size: 100, type: WidthType.PERCENTAGE }`).

---

## Phạm vi
1. **Bổ sung đầy đủ bộ công cụ quản lý dòng PPCT tại Mục 3 (Bảng phân phối chương trình & AI)**:
   - **Thêm dòng mới (Insert Row)**:
     * Nút `➕ Thêm dòng mới` ở đầu / cuối bảng.
     * Nút `➕` (Chèn dòng dưới) trực tiếp tại từng hàng trong bảng để chèn bài học mới tại đúng vị trí mong muốn.
     * Hỗ trợ chọn loại dòng: Dòng bài học bình thường hoặc Dòng tiêu đề phân cấp (HỌC KÌ / CHƯƠNG / CHỦ ĐỀ).
   - **Xóa dòng (Delete Row)**:
     * Nút `🗑️` (Xóa) tại từng hàng để xóa bỏ nhanh bài học thừa.
   - **Di chuyển vị trí (Move & Drag-Drop)**:
     * Nút `▲` (Lên), `▼` (Xuống) và Kéo thả chuột (HTML5 Drag & Drop).
2. **Cơ chế tự động tính lại Tiết CT & Tuần luỹ kế (`recalculatePpctSequences`)**:
   - Khi Thêm dòng, Xóa dòng, hoặc Di chuyển thứ tự:
     * Quét toàn bộ danh sách bài học theo thứ tự từ trên xuống dưới.
     * Tính luỹ kế Tiết CT liên tục từ 1 đến N dựa trên `Số tiết` của từng bài (vd: `1-2`, `3-4`, `5`, `6-7`...).
     * Phân bổ lại Số tuần dựa trên định mức tiết/tuần của môn học (vd: 4 tiết/tuần).
     * Cho phép chỉnh tay trực tiếp bất kỳ ô nào (Inline Edit).
     * Nút tiện ích `🔄 Tính lại Tiết CT & Tuần tự động` để kích hoạt bất cứ lúc nào.
3. **Chuẩn hóa xuống dòng đa đoạn (Multi-paragraph) cho ô bảng trong Word & HTML**:
   - Nâng cấp hàm `cell(text, opts)` trong `exportDocx`: Bóc tách chuỗi `text` theo các dòng `\n` hoặc từng gạch đầu dòng `- `, tạo thành các `Paragraph` độc lập với cỡ chữ 13pt và dãn dòng 1.3.
   - Nâng cấp `integrationCell(value, opts)`: Xuất mỗi mã `[NLS: ...]` và `[AI: ...]` trên một dòng riêng biệt, có màu phân biệt (NLS: xanh dương `#0070C0`, AI: tím `#7030A0`).
4. **Khắc phục triệt để hàm `selectedIntegration`**:
   - Luôn đảm bảo giữ đầy đủ mã NLS của bài theo cấu hình mật độ.
   - Khi tiết có AI: Ghép mã AI vào danh sách kèm đúng phạm vi `(Áp dụng: tiết ...)`, loại bỏ hoàn toàn các chuỗi lặp thừa.
   - Khi tiết không có AI: Chỉ trả về danh sách mã NLS sạch.
5. **Chuẩn hóa hiển thị Tiết CT và Tuần (Phụ lục 3)**:
   - Hàm `formatTietCT(val)`: Định dạng tiết đôi/tiết ba xuống dòng ngăn cách rõ ràng (`8\n9`).
   - Hàm `formatWeek(val)`: Khử trùng lặp số tuần (`3 3` -> `3`).
6. **Cập nhật toàn diện cấu hình xuất Word (.docx)**:
   - Áp dụng khổ ngang A4, font `Times New Roman`, size `13pt` (size 26), line spacing `1.3` (`line: 312`), table 100% width auto-fit cho toàn bộ Phụ lục 1, 2, 3.

---

## Ngoài phạm vi
- Không can thiệp vào các trang khác như `soankhbd.html`.
- Không thay đổi danh mục mã năng lực số chuẩn (CV 3456) và chuẩn AI (QĐ 2422).

---

## File dự kiến tác động
- `xaydungphuluc.html` [BỔ SUNG THÊM/XÓA/CHÈN DÒNG PPCT, TỰ ĐỘNG TÍNH LẠI TIẾT CT & TUẦN, KÉO THẢ, NÂNG CẤP cell(), integrationCell(), selectedIntegration(), CẤU HÌNH DOCX 13PT LINE 1.3 LANDSCAPE]
- `js/khbd-yccd.js` [ĐẢM BẢO getCleanOfficialYccd TRẢ CHUỖI XUỐNG DÒNG CHUẨN]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG KIỂM THỬ THÊM/XÓA DÒNG, TỰ ĐỘNG TÍNH LẠI TIẾT CT & TUẦN, XUỐNG DÒNG VÀ ĐỊNH DẠNG WORD 13PT]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi hoàn thành triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

---

## Các bước thực hiện
1. **Bước 1: Xây dựng các hàm Thêm, Xóa, Chèn và Tính lại dòng PPCT trong `xaydungphuluc.html`**:
   - Viết hàm `insertPpctRowAt(index, isHeader=false)`: Chèn một dòng mới ngay sau vị trí `index`.
   - Viết hàm `deletePpctRowAt(index)`: Xóa dòng tại vị trí `index`.
   - Viết hàm `recalculatePpctSequences()`: Tự động đánh lại Tiết CT luỹ kế và Số tuần liên tục cho toàn bộ danh sách.
   - Đồng bộ ngay lập tức sang `sourcePpctTable`, `sourcePpctRows`, `results['1']`, `results['3']`, `updateAiPicker()`, `renderPreview()`.
2. **Bước 2: Nâng cấp giao diện Bảng PPCT tại Mục 3 (`updateAiPicker`)**:
   - Thêm cột Thao tác trên mỗi dòng chứa các nút:
     * `▲` / `▼` (Di chuyển lên / xuống).
     * `➕` (Chèn bài mới ngay bên dưới).
     * `🗑️` (Xóa bài này).
     * Cần kéo thả (Drag Handle).
   - Thêm nút `➕ Thêm bài học mới` và `🔄 Tính lại Tiết CT & Tuần tự động` ở đầu bảng.
3. **Bước 3: Nâng cấp hàm xử lý văn bản YCCĐ và ô bảng trong `xaydungphuluc.html`**:
   - Viết hàm chuẩn hóa `formatOutcomeLines(text)`: Tách các câu dạng `.,- `, `.- `, `; - ` thành từng dòng `- ...`.
   - Trong `exportDocx`: Nâng cấp hàm `cell(text, opts)` để tạo danh sách các `Paragraph` riêng biệt cho mỗi dòng text, áp dụng `font: 'Times New Roman', size: 26` (13pt) và `spacing: { line: 312 }` (multiple 1.3).
4. **Bước 4: Sửa lỗi `selectedIntegration` & tối ưu hiển thị NLS + AI**:
   - Viết lại hàm `selectedIntegration(value, selectedPeriods, index, c)`: Luôn giữ mã NLS; nếu có chọn AI thì nối thêm mã AI sạch sẽ không lặp từ khóa.
   - Cập nhật `integrationCell`: Mỗi mã NLS / AI nằm trên 1 dòng riêng (`Paragraph` riêng).
5. **Bước 5: Chuẩn hóa hiển thị Tiết CT và Tuần trong Phụ lục 3**:
   - Hàm `cleanTietCT(val)`: Xuống dòng giữa các tiết đôi/ba (`8\n9`).
   - Hàm `cleanWeek(val)`: Khử trùng lặp (`3 3` -> `3`).
6. **Bước 6: Chuẩn hóa toàn bộ tham số xuất Word trong `exportDocx`**:
   - Font: `Times New Roman`, Size: `13pt` (`size: 26`), Dãn dòng: `1.3` (`spacing: { line: 312 }`), Khổ ngang A4 (`16838 x 11906`), Bảng: `100% width`.
7. **Bước 7: Cập nhật kiểm thử tự động `tests/xaydungphuluc-smoke.js`**:
   - Kiểm tra `insertPpctRowAt`, `deletePpctRowAt`, `recalculatePpctSequences` hoạt động chuẩn xác.
   - Kiểm tra các tiêu chí xuống dòng, khử lặp tuần, mã NLS+AI và định dạng Word 13pt.
8. **Bước 8: Khóa trạng thái giao việc**:
   - Ghi `LOCK` vào `docs/handoff/.lock`.

---

## Rủi ro & Giải pháp
1. **Rủi ro người dùng vô tình bấm xóa mất bài quan trọng**:
   - *Giải pháp*: Hiển thị hộp thoại xác nhận nhanh (confirm) hoặc nút hoàn tác trước khi xóa dòng.
2. **Rủi ro khi chèn dòng mới chưa có tên bài làm lỗi tính năng AI**:
   - *Giải pháp*: Gán tên mặc định "Bài học mới", số tiết là 1 và tự động gán Tiết CT / Tuần tiếp nối theo chuỗi.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - `node tests/xaydungphuluc-smoke.js`
   - `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html`:
     * Bấm nút `➕` trên một dòng bất kỳ -> Dòng mới được chèn ngay bên dưới, Tiết CT và Tuần của toàn bộ bảng tự động cập nhật lại luỹ kế.
     * Bấm nút `🗑️` trên một dòng -> Dòng đó bị xóa, Tiết CT và Tuần tự động co lại liên tục, không bị đứt quãng.
     * Thử kéo thả, đổi tuần, chỉnh sửa nội dung -> Xem trước và xuất Word chuẩn xác.

---

## Tiêu chí nghiệm thu
- [x] Bảng PPCT ở Mục 3 có đầy đủ chức năng: **Thêm dòng mới**, **Chèn dòng tại vị trí bất kỳ (➕)**, **Xóa dòng (🗑️)**, **Di chuyển Lên/Xuống (▲/▼)** và **Kéo thả (Drag & Drop)**.
- [x] Hệ thống tự động tính toán lại **Tiết CT luỹ kế và Số tuần phân bổ** ngay khi thêm, xóa hoặc di chuyển dòng.
- [x] Cột "Yêu cầu cần đạt" ở Phụ lục 1 xuống dòng chuẩn từng ý gạch đầu dòng trong cả bản xem trước HTML và file Word (.docx).
- [x] Mỗi mã NLS và AI được hiển thị trên 1 dòng riêng; bài có tick AI hiển thị đầy đủ cả NLS + AI không bị lặp chuỗi "Áp dụng: tiết...".
- [x] Cột "Tiết CT" trong Phụ lục 3 xuống dòng ngăn cách giữa các tiết đôi/ba; cột "Tuần" tự động khử trùng lặp (không còn hiện tượng `3 3`).
- [x] File Word (.docx) xuất ra đạt 100% chuẩn: Khổ A4 Landscape, font Times New Roman, cỡ chữ 13pt, dãn dòng 1.3, bảng auto-fit 100% width.
- [x] 100% bộ test `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` đạt PASS.
