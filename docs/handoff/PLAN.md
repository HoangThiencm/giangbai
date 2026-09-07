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


