# PLAN: Khắc phục Triệt để Lỗi Gán ghép Năng lực số Gượng ép và Lỗi Cụt Mô tả Khung Năng lực AI trong Phụ lục 1 & 3

## Hiện trạng
Khảo sát trực tiếp từ hình ảnh thực tế người dùng cung cấp (Bài 1: Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn, 2 tiết, môn Toán lớp 9) và đối chiếu toàn bộ luồng xử lý mã nguồn tại `xaydungphuluc.html`, `canvas_xaydungphuluc.html` và `js/khbd-standards.js`:

1. **Vấn đề 1: Năng lực số (NLS - CV 3456) bị gán ghép tào lao, phi sư phạm, xa rời mục tiêu bài dạy**:
   - *Biểu hiện thực tế*:
     Cột Năng lực số xuất hiện câu: `6.1.TC2a - Sử dụng chatbot AI để tìm hiểu lịch sử ra đời của hệ phương trình bậc nhất.;`
   - *Nguyên nhân gốc rễ trong mã nguồn*:
     + Trong `js/khbd-standards.js` (dòng 216-220), hàm `scoreOfficialStandard` quy định: nếu bài học có bật AI (`ctx.aiOn = true`), miền `Ứng dụng trí tuệ nhân tạo` (gồm các mã 6.1, 6.2, 6.3 trong Khung NLS CV 3456) tự động được cộng thêm điểm ưu tiên (`score += 5`).
     + Dẫn tới thuật toán tự động đề xuất mã `6.1.TC2a` ("Hiểu biết về hệ thống trí tuệ nhân tạo") vào danh mục NLS của bài học Toán lý thuyết.
     + Trong `xaydungphuluc.html` (dòng 316), câu prompt hướng dẫn lại lấy ví dụ mẫu là mã `6.2.TC2a`, khiến Gemini AI học theo mẫu này và sinh ra mô tả khiên cưỡng: học sinh giải hệ phương trình lại đi "dùng chatbot AI tìm hiểu lịch sử ra đời"!
   - *Sai phạm về mặt sư phạm*:
     + Môn Toán THCS có các năng lực số đặc thù gắn liền với công cụ học toán: **Máy tính cầm tay (Casio/Vinacal)** để kiểm tra nghiệm/bấm máy; **Phần mềm đồ thị và hình học động (GeoGebra, Desmos)** để vẽ 2 đường thẳng và quan sát giao điểm nghiệm; **Bảng tính (Excel/Sheets)** để lập bảng giá trị.
     + Các mã NLS môn Toán chuẩn theo CV 3456 phải thuộc **Miền 5** (5.3 Sử dụng sáng tạo công nghệ số, 5.2 Giải pháp công nghệ), **Miền 1** (1.1, 1.2 Khai thác dữ liệu/thông tin), **Miền 3** (3.1 Biểu diễn mô hình số), chứ KHÔNG ĐƯỢC ép mã 6.1 của Tin học/AI vào bài học Toán để sinh ra hoạt động đối phó, vô bổ.
     + Khi bài học ĐÃ CÓ cột riêng cho Trí tuệ nhân tạo (QĐ 2422), cột NLS bắt buộc phải tập trung vào các công cụ số toán học cốt lõi, không được nhét chatbot vào cột NLS.

2. **Vấn đề 2: Cột Trí tuệ nhân tạo (AI - QĐ 2422) bị cụt lủn, chỉ có mã trần, thiếu hoàn toàn mô tả**:
   - *Biểu hiện thực tế*:
     Cột AI xuất ra đúng một dòng cụt: `9.B2.1 - (Áp dụng: tiết 1, 2).` (sau dấu gạch ngang bị rỗng hoàn toàn, không có mô tả hành động).
   - *Nguyên nhân gốc rễ trong mã nguồn*:
     + Tại `cleanAiColumnText` (`xaydungphuluc.html` dòng 335 và `canvas_xaydungphuluc.html` dòng 350): Khi AI trả về chỉ có mã và phạm vi tiết (ví dụ: `[AI: 9.B2.1 (Áp dụng: tiết 1, 2)]`), hàm bóc tách phần `after` (chuỗi sau mã).
     + Do không có chữ mô tả nào trước phạm vi tiết, biến `after` sau khi loại bỏ scope trở thành chuỗi rỗng `""`.
     + Logic hiện tại: `if (isGeneric) { ... }` chỉ kích hoạt khi `after` tồn tại và khớp với nhãn chung. Nhưng khi `after` rỗng, điều kiện `isGeneric` không chạy!
     + Hàm `cleanAiColumnText` không có cơ chế bù đắp mô tả (enrichment fallback) khi thiếu mô tả, dẫn tới giữ nguyên chuỗi cụt: `9.B2.1 - (Áp dụng: tiết 1, 2).`!
     + Ngược lại, hàm NLS (`enrichNlsCode`) có cơ chế tự động bù đắp mô tả sư phạm theo bài học `lessonAppliedNlsDescription`, trong khi AI thì bị bỏ quên hoàn toàn.

---

## Phạm vi
1. Chuẩn hóa thuật toán chấm điểm và đề xuất Năng lực số cho môn Toán và các môn học trong `js/khbd-standards.js`:
   - Môn Toán: Ưu tiên tuyệt đối các mã NLS công cụ số học tập (Máy tính cầm tay, phần mềm hình học động GeoGebra, Desmos, Bảng tính số liệu). Cấm gán mã 6.1 (tìm hiểu hệ thống AI) vào bài học toán lý thuyết.
2. Hoàn thiện cơ chế hậu xử lý và làm sạch cột Trí tuệ nhân tạo (`cleanAiColumnText` & `lessonAppliedAiDescription`):
   - Khi mã AI thiếu mô tả (hoặc chỉ có mã trần kèm phạm vi tiết), hệ thống tự động bù đắp câu mô tả sư phạm chuẩn xác gắn liền với bài học theo đúng 4 nhóm khung A, B, C, D của Quyết định 2422/QĐ-BGDĐT.
   - Đảm bảo 100% các ô AI luôn có cấu trúc hoàn chỉnh: `Mã AI - Mô tả hành động sư phạm gắn với bài học cụ thể (Áp dụng: tiết X, Y).`
3. Cải tiến chỉ thị Prompt (`appendixPrompt`):
   - Nêu rõ các ví dụ chuẩn sư phạm môn Toán cho NLS (dùng máy tính cầm tay, GeoGebra/Desmos vẽ đồ thị nghiệm, bảng tính số liệu); cấm AI sinh các câu gượng ép "hỏi chatbot về lịch sử".
   - Khóa chặt hợp đồng đầu ra cho cột AI: bắt buộc phải có mô tả hành động trước phạm vi tiết.
4. Áp dụng đồng bộ trên cả 3 tệp:
   - `xaydungphuluc.html`
   - `canvas_xaydungphuluc.html`
   - `backupcode viettailieu/canvas_xaydungphuluc.html`
   - `js/khbd-standards.js`

---

## Ngoài phạm vi
- Không thay đổi bảng Phân phối chương trình hay cấu trúc Yêu cầu cần đạt chuẩn CTGDPT 2018.
- Không thay đổi các tiêu chí thẩm định 100% của `calculateComplianceReport`.

---

## File dự kiến tác động
- `js/khbd-standards.js`: Tinh chỉnh luật chấm điểm NLS môn Toán (ưu tiên 5.3, 5.2, 3.1, 1.1; loại bỏ điểm cộng 6.1 cho Toán).
- `xaydungphuluc.html`: Xây dựng `lessonAppliedAiDescription()`, hoàn thiện `cleanAiColumnText()` tự động bù mô tả khi rỗng, tinh chỉnh prompt.
- `canvas_xaydungphuluc.html` & `backupcode viettailieu/canvas_xaydungphuluc.html`: Đồng bộ 1-1 các nâng cấp trên.
- `tests/xaydungphuluc-smoke.js`: Bổ sung test case chống mã AI cụt và chống NLS gượng ép.

---

## Các bước thực hiện

### Bước 1: Xây dựng hàm tạo mô tả AI chuẩn sư phạm theo bài học (`lessonAppliedAiDescription`)
1. Phân loại theo 4 miền năng lực AI của QĐ 2422:
   - **Miền A (Hiểu biết & Định hướng con người làm chủ)**:
     `Sử dụng trợ lý AI gợi mở phương pháp/ý tưởng thực hành bài [Tên bài], học sinh chủ động đối chiếu với SGK và giữ quyền quyết định cuối cùng`
   - **Miền B (Trách nhiệm & Đạo đức AI)**:
     `Ứng dụng AI hỗ trợ phân tích/đối chiếu bước giải bài [Tên bài], tuân thủ tính trung thực học thuật và kiểm chứng dữ liệu độc lập`
   - **Miền C (Hiểu biết kỹ thuật & Khám phá AI)**:
     `Khám phá nguyên lý thu thập và xử lý dữ liệu qua bài toán/mô hình thực nghiệm của bài [Tên bài]`
   - **Miền D (Sáng tạo & Đánh giá ứng dụng AI)**:
     `Đánh giá mức độ chính xác và tính an toàn của công cụ AI khi hỗ trợ giải quyết nhiệm vụ học tập bài [Tên bài]`
2. Tích hợp vào `cleanAiColumnText`:
   - Khi bóc tách mã AI: Nếu `!after` (mô tả rỗng) hoặc `isGeneric` (chỉ là tên chuẩn lý thuyết chung chung), hệ thống lập tức tự động điền mô tả từ `lessonAppliedAiDescription(code, entry?.label, lesson)`.
   - Bảo đảm chuỗi xuất ra luôn có dạng: `${code} - ${description}. (Áp dụng: tiết ...)`. Triệt tiêu hoàn toàn lỗi cụt `${code} - (Áp dụng: tiết ...)`.

### Bước 2: Tái định hướng Năng lực số môn Toán trong `js/khbd-standards.js`
1. Sửa hàm `scoreOfficialStandard`:
   - Với môn Toán: Giảm điểm miền 6 ("Ứng dụng trí tuệ nhân tạo" của NLS) về 0 khi đã có cột AI riêng; ưu tiên vượt trội cho:
     * Mã `5.3.TC1a / 5.3.TC2a`: "Sử dụng sáng tạo công nghệ số" (Sử dụng máy tính cầm tay, GeoGebra).
     * Mã `3.1.TC1a / 3.1.TC2a`: "Sáng tạo nội dung số" (Vẽ hình động, vẽ đồ thị hàm số minh họa nghiệm).
     * Mã `1.1.TC1a / 1.1.TC2a`: "Khai thác dữ liệu và thông tin số" (Tra cứu dữ liệu, bảng số liệu thống kê).
2. Nâng cấp hàm `lessonAppliedNlsDescription`:
   - Với các bài học Toán (Đại số, Hình học, Phương trình, Hệ phương trình):
     * Ưu tiên sinh câu hành động thiết thực:
       - *"Sử dụng máy tính cầm tay để thực hiện tính toán, kiểm tra và đối chiếu nghiệm của bài [Tên bài]."*
       - *"Sử dụng phần mềm vẽ hình học động (GeoGebra) hoặc đồ thị để trực quan hóa và minh họa kiến thức bài [Tên bài]."*
       - *"Sử dụng bảng tính điện tử để lập bảng giá trị, xử lý số liệu và phân tích kết quả trong bài [Tên bài]."*
     * Tuyệt đối không sinh câu "hỏi chatbot về lịch sử ra đời".

### Bước 3: Tinh chỉnh Prompt Chỉ thị AI trong `appendixPrompt`
1. Thay đổi câu chỉ thị mẫu trong `appendixPrompt('1')`:
   - Đổi ví dụ mẫu từ `6.2.TC2a` sang:
     `[NLS: 5.3.TC2a - Sử dụng phần mềm vẽ đồ thị (GeoGebra) và máy tính cầm tay để minh họa hình học và kiểm tra nghiệm của hệ hai phương trình bậc nhất hai ẩn.]`
   - Bổ sung lệnh cấm: *CẤM TUYỆT ĐỐI gán các hoạt động ngoài lề như "dùng chatbot tìm hiểu lịch sử ra đời" vào bài học Toán; mọi hoạt động NLS phải phục vụ trực tiếp việc hình thành kiến thức, luyện tập, kiểm tra kết quả bài toán.*
   - Khóa chặt định dạng AI: *Mã AI bắt buộc phải có mô tả hành động học sinh dùng AI làm gì trong bài học đó trước phần phạm vi tiết; cấm chỉ ghi mã kèm phạm vi tiết mà bỏ trống mô tả.*

### Bước 4: Đồng bộ 1-1 và Kiểm thử Toàn diện
1. Cập nhật đồng bộ sang `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.
2. Kiểm tra bằng smoke test:
   - Kiểm tra ca fixture: Bài toán lớp 9 có mã `9.B2.1` không có mô tả -> tự động sinh đủ mô tả sư phạm chuẩn QĐ 2422.
   - Kiểm tra ca fixture: NLS bài phương trình / hệ phương trình -> nhận mã 5.3 / 3.1 / 1.1 với công cụ GeoGebra / máy tính cầm tay, không còn chatbot lịch sử.
3. Chạy toàn bộ 58 test suite trong `tests/run-all-tests.js` đạt 100% PASS.

---

## Rủi ro
- *Rủi ro*: Một số bài test cũ kiểm tra chuỗi literal hoặc regex NLS.
- *Xử lý*: Giữ nguyên các hợp đồng định dạng `[NLS: mã - mô tả]`, `[AI: mã - mô tả (Áp dụng: tiết ...)]`, đảm bảo tương thích ngược 100% với các test suite hiện hành.

---

## Cách kiểm thử
1. Chạy test riêng: `node tests/xaydungphuluc-smoke.js` và `node tests/canvas-xaydungphuluc-smoke.js`.
2. Kiểm tra đầu ra trực tiếp của `cleanAiColumnText('9.B2.1 - (Áp dụng: tiết 1, 2).', 'Bài 1. Khái niệm phương trình...')`:
   - Khẳng định chuỗi trả về có đầy đủ mô tả hành động sư phạm, không bị cụt.
3. Kiểm tra đầu ra của `cleanNlsColumnText` đối với bài hệ phương trình:
   - Khẳng định mô tả gắn liền với máy tính cầm tay hoặc GeoGebra/đồ thị, không có "lịch sử ra đời".
4. Chạy toàn bộ hệ thống: `node tests/run-all-tests.js` đạt 100% PASS.

---

## Tiêu chí nghiệm thu
1. Cột Năng lực số (CV 3456) môn Toán gắn liền với các công cụ học tập số thực tế (máy tính cầm tay, GeoGebra, Desmos, bảng tính), chấm dứt hoàn toàn tình trạng gán ghép vô nghĩa "dùng chatbot tìm hiểu lịch sử".
2. Cột Trí tuệ nhân tạo (QĐ 2422) luôn có đầy đủ cả mã chuẩn, mô tả ứng dụng sư phạm cụ thể gắn với bài học, và phạm vi tiết (không bao giờ bị cụt chỉ có mã).
3. Bản xuất Word và Preview hiển thị chuẩn xác, chuyên nghiệp, đúng tinh thần đổi mới giáo dục.
4. Toàn bộ test suites đạt 100% PASS.

---

# PLAN: Triển khai Kho Tri thức Sách Giáo Khoa (SGK) Dùng Chung Trên Toàn Hệ Thống

## Hiện trạng & Mục tiêu
- **Hiện trạng**: Mỗi lần xây dựng Phụ lục, người dùng phải tải file SGK nặng lên để AI quét tóm tắt cục bộ, tốn tài nguyên và thời gian chờ, không chia sẻ được cho các giáo viên khác cùng môn/khối.
- **Mục tiêu**:
  1. Xây dựng CSDL dùng chung (MySQL) lưu trữ Bản đồ Tri thức SGK (`sgk_books` & `sgk_lessons`).
  2. Cung cấp API backend `api/sgk_knowledge.php` đầy đủ các thao tác `check`, `get`, `list`, `save`, `verify`.
  3. Cập nhật giao diện `xaydungphuluc.html`, `canvas_xaydungphuluc.html` và mirror `backupcode viettailieu/canvas_xaydungphuluc.html` với trường chọn Bộ sách (`bookSeries`), tự động kiểm tra kho tri thức dùng chung; nếu đã có thì nạp tức thì (< 0.5s); nếu chưa có thì trích xuất 1 lần bằng AI và lưu vào CSDL cho cả hệ thống cùng dùng.
   4. Viết hướng dẫn chi tiết cách thức vận hành và sử dụng.
   5. Đảm bảo toàn bộ test suites đạt PASS 100%.

## Kiến trúc Kỹ thuật
1. **Backend Database (`api/sgk_knowledge.php`)**:
   - Tự động tạo bảng `sgk_books` và `sgk_lessons` (nếu chưa tồn tại).
   - `sgk_books`: `id, book_key, subject, grade, series, semester, publisher, total_lessons, is_verified, created_by, updated_at`.
   - `sgk_lessons`: `id, book_id, lesson_order, chapter, lesson_code, lesson_title, page_start, page_end, yccd, activities_json, digital_candidates, digital_evidence, ai_pedagogy_hint`.
   - Các action API:
     + `GET ?action=check&subject=...&grade=...&series=...&semester=...`
     + `GET ?action=get&book_id=...` hoặc qua thông tin sách
     + `GET ?action=list` (thư viện sách đã số hóa)
     + `POST ?action=save` (lưu sách + mảng bài học)
     + `POST ?action=verify` (đánh dấu sách đã kiểm định chuẩn)
2. **Frontend UI/UX**:
   - Thêm dropdown chọn Bộ sách: `Kết nối tri thức với cuộc sống`, `Cánh diều`, `Chân trời sáng tạo`, `Khác`.
   - Badge trạng thái trực quan:
     + Xanh lá: `✓ Đã có Bản đồ Tri thức SGK dùng chung (N bài học) · Tự động nạp sẵn sàng`.
     + Vàng/Xanh dương: `ℹ Chưa có tri thức SGK dùng chung cho bộ sách này · Tải SGK để trích xuất & lưu vào kho`.
   - Nút `🚀 Trích xuất & Lưu vào Kho Tri thức Dùng chung` và nút `📚 Xem Thư viện SGK đã có`.
   - Khi có tri thức: tự động điền Yêu cầu cần đạt chuẩn SGK, minh chứng NLS thực tế và gợi ý AI chuẩn QĐ 2422.
3. **Đồng bộ mã nguồn**:
   - Đồng bộ 100% giữa `xaydungphuluc.html`, `canvas_xaydungphuluc.html`, và `backupcode viettailieu/canvas_xaydungphuluc.html`.
4. **Kiểm thử**:
   - Test suite `tests/sgk-knowledge-smoke.js` kiểm tra toàn bộ luồng: schema DB, API helpers, UI component hooks, format dữ liệu bản đồ tri thức.

---

# PLAN: Nâng cấp "Sách giáo khoa dùng chung (từ 2026-2027)" & Bảo đảm Bao phủ 100% Tất cả Bài học

## Hiện trạng & Vấn đề Cần Khắc Phục
1. **Bộ sách**:
   - Theo chỉ đạo giáo dục mới, bắt đầu từ năm học 2026-2027, sử dụng **"Sách giáo khoa dùng chung (từ 2026-2027)"** cho toàn quốc.
   - Hiện tại hệ thống đang mặc định "Kết nối tri thức với cuộc sống", chưa có tùy chọn sách dùng chung này.
2. **Độ bao phủ tri thức (100% bài học)**:
   - Khi trích xuất từ file PDF, `compactSgkText` cắt ngắn ở `slice(0, 220)` dòng, dẫn tới hết Chương I là bị cắt, chỉ ra được 9 bài.
   - Prompt gửi AI cắt ở `slice(0, 35000)` và thiếu chỉ thị ràng buộc độ bao phủ 100%.
   - Năng lực số (CV 3456) áp dụng 100% số bài học; Trí tuệ nhân tạo (QĐ 2422) năm nay là 12 tiết nhưng về sau sẽ tích hợp rộng rãi hơn. Tất cả các bài học đều phải có sẵn YCCD chuẩn, NLS thực tế và gợi ý AI trong CSDL.

## Giải pháp Triển khai
1. **Cập nhật dropdown `#bookSeries` & Cấu hình mặc định**:
   - Đặt `<option value="Sách giáo khoa dùng chung (từ 2026-2027)" selected>Sách giáo khoa dùng chung (từ 2026-2027)</option>` ở vị trí đầu tiên và là mặc định.
   - Áp dụng trên `xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`.
2. **Mở rộng `compactSgkText` & Tối ưu Trích xuất**:
   - Bắt thêm mục lục (TOC), tất cả các chương, bài, hoạt động trải nghiệm.
   - Nâng giới hạn trích xuất lên tới 2.000 dòng và 120.000 ký tự.
3. **Cải tiến Prompt `extractAndSaveSharedSgk`**:
   - Chỉ thị bắt buộc AI quét toàn bộ mục lục và tất cả các chương, trích xuất ĐỦ 100% TẤT CẢ CÁC BÀI HỌC (20-45 bài).
   - Mọi bài học đều có đủ: YCCD, 3 hoạt động, mã NLS + minh chứng công cụ số thực tế (máy tính Casio, GeoGebra, Excel), gợi ý AI theo QĐ 2422.
   - Sửa lỗi runtime ReferenceError của biến `payload`.
4. **Cơ chế Tự động Bù đắp & Bảo đảm 100% Bài học (Curriculum Assurance)**:
   - Xây dựng hàm `ensureFullCurriculumLessons`: Nếu tệp PDF tải lên chỉ có Tập 1 hoặc scan thiếu trang, hệ thống tự động đối chiếu danh mục chuẩn trong `KHBD_YCCD` / PPCT chuẩn để bổ sung đủ 100% các bài còn thiếu kèm YCCD, NLS thực tế và gợi ý AI.
5. **Nạp sẵn dữ liệu chuẩn cho "Sách giáo khoa dùng chung (từ 2026-2027)"**:
   - Seed sẵn toàn bộ 100% bài học môn Toán các lớp 6 (43 bài), 7 (37 bài), 8 (39 bài), 9 (32 bài) vào kho tri thức để sẵn sàng sử dụng tức thì.
6. **Kiểm thử**:
   - Nâng cấp `tests/sgk-knowledge-smoke.js` và đảm bảo toàn bộ 59 test suites đạt 100% PASS.

---

# PLAN: Tối ưu Hóa Luồng Giao diện Người dùng (UI Flow) - Đưa Cấu hình Sư phạm & Tri thức lên Đầu Trang

## Hiện trạng & Bất tiện Người dùng Phản hồi
- Mục 4 (Thông tin & cấu hình sư phạm) nằm dưới Mục 3 (Bảng chọn tiết AI dài 40+ hàng).
- Giáo viên muốn chọn Khối lớp, Môn học, Bộ sách, cấu hình NLS/AI phải cuộn chuột dài xuống dưới, rồi lại cuộn ngược lên trên để bấm Nhận diện hoặc xem Kho Tri thức.

## Giải pháp Triển khai
1. Đưa Khối **Thông tin & cấu hình sư phạm** lên làm **Mục 1** ngay đầu trang.
2. Đặt Khối **Tài liệu nguồn & Kho Tri thức SGK dùng chung** làm **Mục 2** ngay liền kề, giúp phản ánh trạng thái tri thức theo đúng Môn/Lớp/Bộ sách vừa chọn.
3. Chuyển Khối **Chọn loại phụ lục** thành **Mục 3**.
4. Chuyển Bảng dài **Chọn chính xác tiết tích hợp AI** xuống **Mục 4**.
5. Đồng bộ 100% trên `xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`.
6. Giữ nguyên vẹn toàn bộ ID, class, logic JS và bảo đảm 59 test suites PASS 100%.

---

# PLAN: Xóa Tri thức Sai & Bảo đảm Nhận diện Đủ 100% Bài học (Toán 6 đủ 43 bài)

## Vấn đề Cần Giải Quyết
1. **Thiếu bài trong nhận diện & nhảy cóc bài (Toán 6 chỉ ra 25 bài, thiếu Bài 3)**:
   - Khi người dùng trích xuất từ PDF SGK, do giới hạn độ dài phản hồi một lần của mô hình AI nên danh sách bị dừng ở bài 25.
   - Hàm `lessonsMatch` trước đây có thể match nhầm số thứ tự khiến Bài 3 bị bỏ qua.
   - Script ngoài `https://hoangthiencm.id.vn/js/khbd-yccd.js` bị obfuscate dạng IIFE không xuất biến ra `window`, dẫn đến `KHBD_YCCD` bị undefined trong trình duyệt, khiến hàm bù đắp bài học không chạy được.
2. **Không xóa được bản đồ tri thức nhận diện sai**:
   - Trong Thư viện SGK dùng chung (`sgkLibraryModal`) và Modal chi tiết (`sgkDetailModal`) chưa có nút Xóa bộ sách nhận diện sai hoặc bị thiếu bài.

## Giải pháp Triển khai
1. **Backend (`api/sgk_knowledge.php`)**:
   - Bổ sung endpoint `action=delete` (hỗ trợ cả POST và GET, nhận `book_id` hoặc `book_key`), sử dụng transaction an toàn xóa sạch `sgk_lessons` trước rồi xóa `sgk_books`.
2. **Frontend UI - Thao tác Xóa An Toàn**:
   - Thêm nút `🗑 Xóa` bên cạnh mỗi bộ sách trong Thư viện SGK (`sgkLibraryModal`).
   - Thêm nút `🗑 Xóa bộ sách này` trong chân Modal chi tiết bài học (`sgkDetailModal`).
   - Cài đặt hàm `deleteSgkBook(bookId, bookTitle)` và `deleteCurrentDetailBook()`:
     + Hiển thị hộp thoại xác nhận `canvasConfirm` cảnh báo hành động không thể hoàn tác.
     + Gọi API `?action=delete`.
     + Tự động dọn dẹp cache `localStorage` nếu bộ sách đang được nạp.
     + Làm mới danh sách và cập nhật trạng thái kho tri thức tức thì.
3. **Bảo đảm 100% Đủ 43 Bài Học Môn Toán 6 (Chậm nhưng chắc)**:
   - Nhúng trực tiếp từ điển chuẩn `DEFAULT_MATH_CATALOG` (Toán 6 đủ 43 bài, Toán 7 đủ 37 bài, Toán 8 đủ 39 bài, Toán 9 đủ 32 bài) ngay trong mã nguồn, giải phóng hoàn toàn sự phụ thuộc vào script mạng ngoài.
   - Sửa hàm `ensureFullCurriculumLessons`:
     + Đối chiếu từng bài từ 1 đến 43 theo số thứ tự và tên bài.
     + Bài nào AI trích xuất được từ PDF: giữ nguyên số trang, hoạt động chi tiết, YCCD riêng của bài.
     + Bài nào bị AI bỏ sót (như Bài 3) hoặc bị dừng giữa chừng (bài 26-43): tự động bù đắp chuẩn xác theo CTGDPT 2018, trang bị đầy đủ minh chứng NLS thực tế (Casio/GeoGebra) và gợi ý AI (QĐ 2422).
     + Đảm bảo kết quả luôn ĐỦ 43 bài môn Toán 6, không nhảy cóc, sắp xếp đúng thứ tự 1..43.
4. **Đồng bộ và Kiểm thử**:
   - Đồng bộ 100% giữa `canvas_xaydungphuluc.html`, `xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.
   - Cập nhật `tests/sgk-knowledge-smoke.js` kiểm tra chặt chẽ 43 bài và tính năng xóa.
   - Bảo đảm 59 test suites chạy PASS 100%.

---

# PLAN: Khắc phục Lỗi Sư phạm "Kiểm tra nghiệm" ở Bài Số học & Hoàn thiện Cơ chế Tích hợp 2–3 Mã Năng lực số (CV 3456)

## Hiện trạng & Phản ánh của Người dùng
1. **Lỗi sư phạm phi lý trong bài học Số học (Toán 6 Bài 3 - Thứ tự trong tập hợp các số tự nhiên)**:
   - Minh chứng NLS hiển thị: *"Sử dụng phần mềm vẽ đồ thị (GeoGebra/Desmos) và máy tính cầm tay để minh họa hình học, kiểm tra nghiệm của bài..."*.
   - Đây là lỗi sư phạm: Bài 3 Toán 6 học về thứ tự số tự nhiên (so sánh $a < b$, biểu diễn trên tia số), hoàn toàn không có "phương trình", không có "nghiệm", và không dùng "đồ thị GeoGebra/Desmos".
   - *Nguyên nhân*: Regex phân loại môn Toán trước đây gom chung các bài vào nhóm đại số/phương trình nếu không khớp hình học/thống kê, dẫn đến gán nhầm cụm từ "kiểm tra nghiệm".
2. **Thắc mắc về cơ chế tích hợp 2–3 mã Năng lực số (CV 3456)**:
   - Người dùng hỏi: *"Rồi có 2-3 mã năng lực thì sao?"*.
   - Cần thể hiện rõ ràng: Một bài học khi tích hợp 2–3 mã NLS thì giao diện hiển thị các mã đó như thế nào (từng badge riêng biệt) và minh chứng hành động sư phạm của từng mã ra sao thay vì chỉ ghi chung chung một câu.

## Giải pháp Triển khai
1. **Phân loại sư phạm chính xác tuyệt đối theo phân môn**:
   - `isArith`: Bài Số học (Số tự nhiên, thứ tự, số nguyên, phân số, số thập phân, ước, bội, chia hết...).
     -> Hành động NLS: Sử dụng máy tính cầm tay thực hiện các phép tính số học, kiểm tra kết quả tính toán, so sánh thứ tự hai số; khai thác phần mềm hoặc công cụ trực quan tia số/trục số. (Tuyệt đối KHÔNG có chữ "nghiệm" hay "đồ thị").
   - `isGeo`: Hình học (hình trực quan, góc, tam giác, tứ giác...).
     -> Hành động NLS: Sử dụng phần mềm hình học động (GeoGebra) hoặc công cụ đo vẽ trực quan hóa hình vẽ.
   - `isStat`: Thống kê & Xác suất.
     -> Hành động NLS: Sử dụng bảng tính (Excel/Sheets) hoặc công cụ số để thu thập, lập bảng số liệu và vẽ biểu đồ.
   - `isEquation`: Phương trình & Hệ phương trình.
     -> Hành động NLS: Sử dụng MTCT và phần mềm đồ thị kiểm tra nghiệm và đối chiếu kết quả.
   - `isFunction`: Hàm số & Đồ thị.
     -> Hành động NLS: Sử dụng phần mềm vẽ đồ thị (GeoGebra/Desmos) khảo sát hàm số.
2. **Thanh lọc dữ liệu cũ và CSDL Backend**:
   - Hàm `isUnfitDigitalEvidence(ev, lesson)`: Phát hiện tức thì các câu chứa "nghiệm", "đồ thị" ở bài Số học.
   - `api/sgk_knowledge.php`: Tự động làm sạch các minh chứng unfit trong `action=get` và `action=save`.
   - `enrichNlsCode`: Tự động thay thế bằng mô tả số học chuẩn xác.
3. **Cơ chế Phân rã & Thể hiện 2–3 Mã NLS (CV 3456)**:
   - Hàm `recommendLessonDigitalCandidates(lessonTitle, grade, subject, yccd)`: Tự động đề xuất danh sách 2–3 mã NLS chuẩn:
     + Lớp 6–7: `5.3.TC1a, 5.2.TC1a, 1.1.TC1a`.
     + Lớp 8–9: `5.3.TC2a, 5.2.TC2a, 1.1.TC2a`.
   - Hàm `buildLessonDigitalEvidence(candidatesStr, lessonTitle)`: Xây dựng minh chứng sư phạm riêng cho từng mã:
     + Mã 5.3: Thực hành tính toán trên máy tính cầm tay, kiểm tra so sánh và công cụ tia số/trục số.
     + Mã 5.2: Lựa chọn và sử dụng công cụ tính toán số phù hợp với bài học.
     + Mã 1.1: Khai thác học liệu số, mô phỏng trực quan tia số/trục số để tìm hiểu bài học.
   - Giao diện Modal Chi tiết SGK (`renderSgkDetailNlsBlock`):
     + Hiển thị hàng badge trực quan: `[Mã NLS: 5.3.TC1a] [Mã NLS: 5.2.TC1a] [Mã NLS: 1.1.TC1a]`.
     + Kèm danh sách các hành động sư phạm riêng biệt ứng với từng mã.
   - Trong Phụ lục 1 & 3: Tự động phân bổ 1–3 mã theo cấu hình mật độ NLS, giữ cấu trúc `Mã - Mô tả`.
4. **Đồng bộ và Kiểm thử Toàn diện**:
   - Đồng bộ trên cả 3 tệp HTML: `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`, `xaydungphuluc.html`.
   - Smoke tests: `tests/sgk-knowledge-smoke.js`, `tests/canvas-xaydungphuluc-smoke.js`.
   - Chạy toàn bộ 59/59 test suites PASS 100%.

---

# PLAN: Đa dạng hóa & Chuẩn hóa Thực chất Năng lực số (CV 3456) & Năng lực AI (QĐ 2422)

## Vấn đề Cần Giải Quyết
- Tránh tình trạng "Template hóa" lặp đi lặp lại bộ mã `5.3, 5.2, 1.1` trên toàn bộ các bài học trong năm.
- Cần đa dạng hóa các mã NLS bám sát thực chất hoạt động học tập của từng bài:
  + Bài tính toán số học: bổ sung `5.1.TC1a` (nhận biết & xử lý lỗi kỹ thuật MTCT: Math ERROR, Syntax ERROR).
  + Bài hình học & đối xứng: bổ sung `3.1.TC1a` (dựng hình GeoGebra, vẽ trục/tâm đối xứng) và `1.1.TC1a`.
  + Bài thống kê & xác suất: bổ sung `1.2.TC1a` (đánh giá độ tin cậy dữ liệu số) và `3.1.TC1a` (bảng tính Excel/Sheets).
  + Bài thực hành trải nghiệm & dự án: bổ sung `2.2.TC1a` (chia sẻ sản phẩm nhóm trên môi trường số).
  + Bài lý thuyết khái niệm trừu tượng: bổ sung `1.1.TC1a`, `5.2.TC1a`, `4.3.TC1a` (an toàn mắt & tư thế).
- Tinh chỉnh mô tả hành động sư phạm của từng mã rõ ràng, thực tiễn, có công cụ thực tế (MTCT Casio fx-580, GeoGebra, Excel, bảng số liệu...).

## Các Bước Triển Khai
1. **Nâng cấp `recommendLessonDigitalCandidates`**:
   - Nhận diện 6 nhóm bài học đặc thù qua tiêu đề và YCCD.
   - Đề xuất bộ 2–3 mã NLS riêng biệt cho từng nhóm, giải phóng hoàn toàn sự lặp lại đơn điệu.
2. **Nâng cấp `lessonAppliedNlsDescription`**:
   - Bổ sung mô tả hành động cụ thể cho các mã mới: `5.1` (sự cố kỹ thuật MTCT), `3.1` (sản phẩm số/dựng hình/bảng tính), `2.2` (hợp tác số), `1.2` (đánh giá dữ liệu số), `4.3` (an toàn sức khỏe số).
   - Giữ hàm ở định dạng 1 dòng đơn (`single-line`) để tương thích với `sliceNamedFunction` của bộ test smoke Canvas.
3. **Đồng bộ 1-1**:
   - Áp dụng trên `canvas_xaydungphuluc.html`, `xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`.
4. **Kiểm thử**:
   - Viết test case trong `tests/sgk-knowledge-smoke.js` xác nhận tính đa dạng: kiểm tra các bài Toán 6 thuộc các phân môn khác nhau nhận các mã khác nhau (`5.1`, `3.1`, `1.2`, `2.2`...), không bài nào bị trùng lặp máy móc.
   - Chạy toàn bộ 59 test suites PASS 100%.

---

# PLAN: Hệ thống Nạp Tri thức Toàn diện cho Từng Môn ở Mỗi Lớp (Lớp 6–9)

## 1. Hiện trạng & Yêu cầu Người dùng
- Người dùng phản ánh: *"xaydungphuluc và canvas_xaydungphuluc tôi nạp tri thức được mỗi toán 6 còn lại không có chỗ để nạp. Đúng ra sẽ có nút nạp cho từng môn ở mỗi lớp"*.
- *Nguyên nhân*:
  + `onchange` của thẻ `<select id="grade">` không gọi `checkSharedSgkKnowledge(true)`, khiến khung tri thức bị giữ nguyên trạng thái cũ khi đổi lớp.
  + Hàm `ensureFullCurriculumLessons` chỉ hỗ trợ môn Toán (`isMath = /toán/i.test(subject)`). Khi chọn các môn khác (Ngữ văn, KHTN, Lịch sử - Địa lí, Tin học, Công nghệ, GDCD, Tiếng Anh, v.v.), hệ thống báo lỗi không có danh mục chuẩn.
  + Modal Thư viện sách (`#sgkLibraryModal`) chỉ hiển thị các sách đã lưu trong CSDL, không có danh mục ma trận các môn theo từng khối lớp và không có nút nạp riêng cho từng môn.

## 2. Giải pháp Thực hiện
1. **Mở rộng Kho Tri thức Chuẩn cho Tất cả 12 Môn THCS (Lớp 6, 7, 8, 9)**:
   - Khai thác danh mục bài học từ `js/khbd-curriculum.js` (`CURRICULUM_DATA.lessonsBySubject`) cho toàn bộ 12 môn THCS.
   - Tích hợp hàm `getStandardCurriculumLessons(subject, grade)` tự động cung cấp danh mục 100% bài học chuẩn cho bất kỳ môn học nào.
   - Nâng cấp `ensureFullCurriculumLessons`: hỗ trợ trọn vẹn 100% các môn và các khối lớp 6, 7, 8, 9.
2. **Cập nhật Giao diện Ngoài Trang Chính (`#sharedSgkContainer`)**:
   - Thêm `checkSharedSgkKnowledge(true)` vào sự kiện `onchange` của `#grade`.
   - Khi chọn bất kỳ môn và lớp nào, khung hiển thị ngay trạng thái của môn/lớp đó kèm nút `⚡ Nạp Tri thức chuẩn môn [Môn] Lớp [Lớp] (100% bài)`.
3. **Xây dựng Trung tâm Quản lý & Nạp Tri thức Toàn bộ Môn học (`#sgkLibraryModal`)**:
   - Bổ sung Tab chọn Khối lớp: `[ Lớp 6 ]` · `[ Lớp 7 ]` · `[ Lớp 8 ]` · `[ Lớp 9 ]` · `[ Sách đã lưu trong CSDL ]`.
   - Bổ sung các nút tác vụ hàng loạt: `⚡ Nạp tất cả môn Khối Lớp X` và `⚡ Nạp trọn bộ tất cả các môn (Lớp 6–9)`.
   - Lưới danh sách môn học: Mỗi môn có tên, số tiết, số bài học chuẩn, trạng thái CSDL và **Nút Nạp Tri thức riêng cho môn đó**.
4. **Đồng bộ 100%**:
   - Áp dụng trên `xaydungphuluc.html`, `canvas_xaydungphuluc.html` và mirror `backupcode viettailieu/canvas_xaydungphuluc.html`.
5. **Kiểm thử Toàn diện**:
   - `tests/sgk-knowledge-smoke.js`, `tests/canvas-xaydungphuluc-smoke.js` và `tests/run-all-tests.js` (59/59 suites PASS 100%).

---

## Kế hoạch Triển khai: Bắt buộc Chuyển Đổi 100% Công Thức Toán Học thành Equation (Office Math OMML) trong Phụ Lục

### 1. Mục tiêu
- Yêu cầu User: *"các công thức được sinh ra trong phụ lục không được chuyển thành equation nha, tất cả các công thức đều được đặt trong equation hết, bắt buộc"*.
- Mọi công thức toán học trong Phụ lục (Bài học, YCCĐ, NLS, AI, Hoạt động) bắt buộc xuất ra Word dưới dạng đối tượng Equation (OMML `<m:oMath>`), không được để dạng text thô.
- Giao diện web hiển thị công thức toán qua KaTeX.

### 2. Các bước triển khai
1. Nạp `js/khbd-docx.js` và KaTeX vào `<head>` của cả 3 tệp HTML (`xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`).
2. Xây dựng bộ nhận diện công thức toán `autoWrapMathInDelimiters`.
3. Xây dựng `parseDocxMathRuns` tạo đối tượng `docx.Math` (`<m:oMath>`).
4. Tích hợp `renderMathHtml` với KaTeX cho giao diện Preview.
5. Cập nhật `exportDocx` (`para`, `outcomeCell`, `cell`, `integrationCell`).
6. Cập nhật prompt AI trong `standards()` yêu cầu bọc công thức trong `$ ... $`.
7. Viết smoke test `tests/xaydungphuluc-math-smoke.js` và kiểm thử toàn bộ 60/60 test suites.

---

## Kế hoạch Triển khai: Rà soát Sư phạm & Phân rã YCCĐ Riêng biệt Từng Bài học Toán 7, 8, 9 (Xóa bỏ Trùng lặp)

### 1. Mục tiêu
- Phản hồi User: *"ở kho tri thức tôi thấy toán 9 bài 1 và bài 2 mục tiêu yêu cầu cần đạt giống nhau. Vậy rà soát lại xem"*
- Xóa bỏ 100% tình trạng trùng lặp YCCĐ giữa các bài học liên tiếp trong cùng một chương ở môn Toán (Toán 9, Toán 8, Toán 7).
- Đảm bảo mỗi bài học có mục tiêu YCCĐ riêng biệt, chính xác theo chuẩn CTGDPT 2018 (Thông tư 32/2018/TT-BGDĐT) và bám sát nội dung từng bài trong SGK.

### 2. Các bước triển khai
1. Rà soát toàn bộ 32 bài học Toán 9, 39 bài học Toán 8, 37 bài học Toán 7.
2. Biên soạn danh mục YCCĐ phân rã chi tiết, riêng biệt cho từng bài học.
3. Cập nhật `DEFAULT_MATH_CATALOG` trong `xaydungphuluc.html`, `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.
4. Cập nhật `KHBD_YCCD.toan` trong `js/khbd-yccd.js`.
5. Bổ sung Section 8 vào `tests/sgk-knowledge-smoke.js` kiểm tra tính duy nhất (distinctness) của YCCĐ Toán 6–9.
6. Chạy kiểm thử toàn diện `node tests/run-all-tests.js` (60/60 suites pass 100%).

