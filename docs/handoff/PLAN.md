# PLAN: Nâng Cấp Giao Diện Toàn Màn Hình, Chuẩn Hóa 1 Cột Tích Hợp, Quy Trình 4 Bước Đọc SGK & Sinh Mã Năng Lực Số/AI Chuẩn Xác Theo soankhbd

## Hiện trạng
1. **Giao diện bảng bị co cụm (Screenshot phản ánh từ người dùng)**:
   - Thẻ `<main class="max-w-7xl">` giới hạn chiều rộng container trong khi bảng PPCT có tới 7–8 cột dữ liệu lớn.
   - CSS `table.ppct-table { table-layout: fixed; width: 100%; word-break: break-word }` cùng các tỷ lệ phần trăm cột chưa cân đối khiến các cột như "Bài học", "Yêu cầu cần đạt", "Thiết bị", "Mã NLS & AI" bị bóp nghẹt, chữ bị ngắt dòng sau mỗi 1–2 từ (ví dụ: "Tập / hợp", "Cách / ghi số / tự / nhiên").
2. **Lỗi lặp 2 cột "Mã NLS & AI (CV 3456 & QĐ 2422)" trong bảng kết quả & file xuất Word**:
   - Khi bảng nguồn đã có sẵn cột tích hợp hoặc khi gán bảng qua hàm `preservedPpctTable`, code tự động thêm `[...sourcePpctTable.columns, 'Mã NLS & AI (CV 3456 & QĐ 2422)']` mà không kiểm tra trùng lặp, dẫn đến bảng đầu ra xuất hiện 2 cột tích hợp giống hệt nhau.
3. **Quy trình đọc tài liệu và tích hợp chưa tối ưu theo 4 bước sư phạm**:
   - Hiện tại việc upload file và parse diễn ra tự động gộp chung, thiếu các nút hành động độc lập ("Nhận diện PPCT", "Đọc SGK").
   - Chưa có luồng gửi file SGK lên AI để AI đọc hiểu toàn bộ cấu trúc bài học, mục tiêu, nội dung nhằm chuẩn hóa ngữ cảnh sư phạm trước khi sinh phụ lục.
   - Chưa hiển thị thông báo trạng thái rõ ràng: **"Đã hiểu thông tin SGK"** sau khi AI phân tích SGK xong.
4. **Mã Năng lực Số (NLS) và Khung AI chưa chuẩn xác theo quy ước `soankhbd`**:
   - Mã NLS đang sinh giả định (`[1.1.6a]...`) chưa theo đúng khung Thông tư 02/2025/TT-BGDĐT & CV 3456/BGDĐT-GDPT (`1.1.TC1a` cho Lớp 6–7, `1.1.TC2a` cho Lớp 8–9).
   - Mã Khung AI (QĐ 2422) chưa gắn đúng danh mục chuẩn theo từng lớp (`6.A1.1`, `7.A1.1`, `8.A1.1`, `9.A3.1`...).
   - Hiện tượng sinh sai lệch nội dung (ví dụ: bài cộng trừ số tự nhiên nhưng sinh mã ƯCLN/BCNN hoặc mã không liên quan) do prompt chưa liên kết chặt chẽ giữa tên bài học, YCCĐ môn học (`KHBD_YCCD`) và tri thức từ SGK.
   - Phụ lục 1 chưa tận dụng kho Yêu cầu cần đạt chính xác đã có sẵn trong `js/khbd-yccd.js`.

---

## Phạm vi
1. **Mở rộng giao diện hiển thị toàn màn hình (Full-width / Fluid Layout)**:
   - Chuyển `main` sang container siêu rộng (`max-w-[98%] 2xl:max-w-[1750px] mx-auto`) để bảng PPCT và Bảng chọn tiết AI lấp đầy màn hình, hiển thị thoáng đãng.
   - Cân đối lại tỷ lệ bề rộng các cột (STT: 4%, Bài học: 28%, Số tiết: 6%, Tiết CT: 7%, Tuần: 6%, Thiết bị: 14%, Địa điểm: 10%, Mã NLS & AI: 25%) và cho phép tự động co giãn thông minh, hạn chế ngắt dòng vụn vặt.
2. **Khắc phục triệt để lỗi 2 cột tích hợp (Duy nhất 1 cột NLS & AI)**:
   - Chuẩn hóa mọi hàm xử lý bảng (`preservedPpctTable`, `ppctTableFromRows`, `appendixOneTable`, `dynamicPpctTable`, `exportDocx`): Kiểm tra nếu cột NLS & AI đã tồn tại thì cập nhật nội dung vào đúng cột đó; nếu chưa có mới thêm duy nhất 1 cột ở cuối bảng.
3. **Thiết kế quy trình 4 bước chuẩn hóa**:
   - **Bước 1**: Upload file PPCT / Phụ lục (PDF, DOCX, XLSX) -> Bấm nút **"🔍 Nhận diện PPCT"** -> Bóc tách và xuất ngay bảng PPCT trực quan ra màn hình ở Mục 3 và Mục 7.
   - **Bước 2**: Upload file SGK (PDF, DOCX) -> Bấm nút **"📖 Đọc SGK"** -> Đẩy lên AI để phân tích toàn bộ cấu trúc SGK -> Xuất thông báo nổi bật: **"✓ Đã hiểu thông tin SGK"**.
   - **Bước 3**: Người dùng tick chọn các bài/tiết tích hợp Khung năng lực AI (tối đa 12 tiết chuẩn) trên bảng mở rộng.
   - **Bước 4**: Bấm nút sinh phụ lục (Trọn bộ 1–2–3 hoặc từng phụ lục):
     * Đọc toàn bộ danh mục mã NLS (CV 3456 / TT 02) và Khung AI (QĐ 2422) từ `js/khbd-standards.js`.
     * Ghép nối ngữ cảnh SGK (Bước 2) + YCCĐ từ `js/khbd-yccd.js` để AI sinh đúng mã, đúng động từ, đúng hành vi sư phạm phù hợp với từng bài học cụ thể (tuyệt đối không gán nhầm kiến thức).
     * Phụ lục 1 tự động điền Yêu cầu cần đạt chuẩn CT GDPT 2018 từ kho dữ liệu đã cung cấp.
4. **Tích hợp thư viện chuẩn & Kiểm thử**:
   - Nhúng `<script src="js/khbd-standards.js"></script>` vào `xaydungphuluc.html`.
   - Cập nhật test `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` đảm bảo pass 100%.

---

## Ngoài phạm vi
- Không can thiệp vào các trang khác như `soankhbd.html`, `admin.html`, `index.html`.
- Không thay đổi các quy định bảo mật API key (không lưu vào LocalStorage).

---

## File dự kiến tác động
- `xaydungphuluc.html` [MỞ RỘNG LAYOUT TOÀN MÀN HÌNH, NÚT NHẬN DIỆN PPCT & ĐỌC SGK ĐỘC LẬP, SỬA LỖI 2 CỘT TÍCH HỢP, TÍCH HỢP KHBD_STANDARDS & KHBD_YCCD]
- `tests/xaydungphuluc-smoke.js` [CẬP NHẬT TEST CHO 4 BƯỚC, KHBD_STANDARDS, 1 CỘT TÍCH HỢP DUY NHẤT VÀ THÔNG BÁO "ĐÃ HIỂU THÔNG TIN SGK"]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi hoàn thành triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

---

## Các bước thực hiện
1. **Bước 1: Tinh chỉnh Giao diện Mở rộng Toàn màn hình & Tỷ lệ Cột Bảng**:
   - Trong `xaydungphuluc.html`:
     * Đổi `<main class="max-w-7xl mx-auto p-4 space-y-4">` thành `<main class="w-full max-w-[98%] 2xl:max-w-[1750px] mx-auto p-4 space-y-4">`.
     * Tinh chỉnh CSS `.ppct-table`: Loại bỏ `word-break: break-word` cưỡng bức gây ngắt chữ vụn, thêm `min-width: 900px`, `overflow-x: auto`, padding ô hợp lý (`padding: 0.6rem 0.75rem`).
     * Định nghĩa lại `PPCT_COLUMN_WIDTHS`: `{ lesson: 28, periods: 6, tietCT: 7, week: 6, devices: 14, location: 10, integration: 25 }` (hoặc phân bổ linh hoạt theo nội dung).
2. **Bước 2: Cập nhật Mục 2 thành Luồng Thao tác 2 Nút Độc lập (Bước 1 & Bước 2)**:
   - Thiết kế lại thẻ Mục 2:
     * Khu vực PPCT: Input chọn file + Nút **"🔍 Nhận diện PPCT"** (nút nổi bật) + Nút "Nạp cấu trúc mẫu". Khi bấm "Nhận diện PPCT" (hoặc chọn file), bóc tách và xuất ngay bảng ra Mục 3 và Mục 7.
     * Khu vực SGK: Input chọn file SGK + Nút **"📖 Đọc SGK"** (nút nổi bật).
     * Khi bấm "Đọc SGK": Gửi nội dung/mục lục/hoạt động SGK lên AI phân tích, lưu vào `sgkKnowledgeBase`, hiển thị thông báo xanh: **"✓ Đã hiểu thông tin SGK ([Tên file] — [X] bài học/hoạt động)"**.
3. **Bước 3: Khắc phục triệt để lỗi Nhân đôi Cột Tích hợp NLS & AI**:
   - Trong `preservedPpctTable(generated, c)`:
     * Tìm vị trí cột tích hợp hiện có trong `sourcePpctTable.columns` qua regex `/Mã NLS|NLS\s*&\s*AI|Tích hợp/i`.
     * Nếu đã có cột tích hợp -> thay thế giá trị tại đúng cột đó trong mỗi dòng `row.cells[integrationIdx] = ...`.
     * Nếu chưa có cột tích hợp -> thêm đúng 1 cột `'Mã NLS & AI (CV 3456 & QĐ 2422)'` vào cuối mảng `columns`.
   - Áp dụng kiểm tra tương tự trong `ppctTableFromRows`, `appendixOneTable`, `dynamicPpctTable`, `exportDocx`.
4. **Bước 4: Nhúng `js/khbd-standards.js` và Chuẩn hóa Hệ thống Mã Sư phạm**:
   - Thêm `<script src="js/khbd-standards.js"></script>` vào `<head>` của `xaydungphuluc.html`.
   - Xây dựng hàm `getStandardCompetenciesForLesson(lessonName, grade, subject, sgkContext)`:
     * Đối chiếu với `KHBD_STANDARDS.digital` (mã `1.1.TC1a`..`5.4.TC1a` cho khối 6-7, `1.1.TC2a`..`5.4.TC2a` cho khối 8-9).
     * Đối chiếu với `KHBD_STANDARDS.ai` (mã `6.A1.1`..`6.D2.2` cho lớp 6, `7.A1.1`..`7.D2.1` cho lớp 7, `8.A1.1`..`8.D2.2` cho lớp 8, `9.A1.1`..`9.D2.1` cho lớp 9).
     * Lấy Yêu cầu cần đạt chuẩn từ `KHBD_YCCD` cho môn Toán (hoặc tri thức SGK đã đọc cho các môn khác).
   - Nâng cấp `appendixPrompt`:
     * Truyền danh mục mã chuẩn và yêu cầu AI: "Mỗi bài học CHỈ ĐƯỢC sinh mã NLS và mã AI đúng trọng tâm kiến thức của bài đó. Ví dụ: bài Số tự nhiên thì dùng mã NLS về thu thập dữ liệu số/tính toán số học, bài Hình học dùng mã vẽ hình/mô phỏng, bài Thống kê dùng mã biểu đồ. Tuyệt đối KHÔNG gán mã sai lệch như Ước chung lớn nhất cho bài cộng trừ cơ bản."
     * Yêu cầu AI chỉ xuất mã `[AI: ...]` cho các bài/tiết nằm trong danh sách đã chọn ở Bước 3.
     * Với Phụ lục 1: Tự động trích xuất hoặc hoàn thiện cột "Yêu cầu cần đạt" bám sát CT GDPT 2018.
5. **Bước 5: Cập nhật `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js`**:
   - Bổ sung kiểm tra:
     * Sự có mặt của `js/khbd-standards.js` và `KHBD_STANDARDS`.
     * Sự tồn tại của nút "Nhận diện PPCT" và nút "Đọc SGK", thông báo "Đã hiểu thông tin SGK".
     * Kiểm tra cấu trúc bảng xuất ra chỉ có đúng 1 cột "Mã NLS & AI (CV 3456 & QĐ 2422)", không bị lặp cột.
     * Kiểm tra định dạng mã NLS chuẩn (`.TC1a` / `.TC2a`) và mã AI chuẩn (`6.A1.1`, `7.A1.1`...).
   - Chạy test đảm bảo pass 100%.
6. **Bước 6: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

---

## Rủi ro & Giải pháp
1. **Rủi ro bảng rộng bị tràn trên màn hình nhỏ**:
   - *Giải pháp*: Bọc bảng trong container `<div class="overflow-x-auto">` với thanh cuộn ngang mượt mà, đồng thời ưu tiên giãn rộng tối đa trên màn hình máy tính để không bị co cụm chữ.
2. **Rủi ro AI sinh mã NLS/AI ngẫu nhiên không đúng bài**:
   - *Giải pháp*: Cung cấp catalog quy chuẩn từ `KHBD_STANDARDS` và tri thức SGK đã phân tích trực tiếp vào prompt, kèm ràng buộc logic sư phạm nghiêm ngặt.
3. **Rủi ro tệp SGK dung lượng lớn làm vượt quá token**:
   - *Giải pháp*: Sử dụng cơ chế tinh gọn `compactSgkText` kết hợp tóm lược mục tiêu bài học trước khi gửi AI.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - `node tests/xaydungphuluc-smoke.js`
   - `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html` trên trình duyệt:
     * Bước 1: Upload file PPCT -> Bấm "Nhận diện PPCT" -> Kiểm tra bảng hiển thị toàn màn hình, không bị co cụm chữ.
     * Bước 2: Upload file SGK -> Bấm "Đọc SGK" -> Kiểm tra thông báo "Đã hiểu thông tin SGK".
     * Bước 3: Tick chọn 2-3 tiết AI ở Mục 3.
     * Bước 4: Bấm "Sinh trọn bộ Phụ lục" -> Kiểm tra:
       + Phụ lục 1: Cột Yêu cầu cần đạt có nội dung chuẩn xác; Cột NLS & AI chỉ có duy nhất 1 cột.
       + Phụ lục 3: Bảng 7 cột chuẩn CV 5512, chỉ có duy nhất 1 cột NLS & AI, mã NLS & AI khớp đúng nội dung từng bài.
       + Xuất file Word (.docx) và mở kiểm tra không có cột trùng lặp.

---

## Tiêu chí nghiệm thu
- [x] Giao diện Bảng chọn tiết AI và Xem trước được mở rộng toàn màn hình (`max-w-[98%]`), không còn hiện tượng co cụm bóp nghẹt chữ.
- [x] Bảng kết quả Phụ lục 1, Phụ lục 3 trên giao diện và trong file Word (.docx) xuất ra chỉ có duy nhất 1 cột "Mã NLS & AI (CV 3456 & QĐ 2422)".
- [x] Giao diện có đầy đủ nút "Nhận diện PPCT" (Bước 1) và nút "Đọc SGK" (Bước 2), xuất thông báo "Đã hiểu thông tin SGK" sau khi AI đọc xong SGK.
- [x] Tích hợp `js/khbd-standards.js`, mã NLS và mã AI được sinh chuẩn xác theo quy ước sư phạm, khớp đúng nội dung từng bài (không gán nhầm kiến thức).
- [x] Cột "Yêu cầu cần đạt" trong Phụ lục 1 được lấy từ `KHBD_YCCD` / CT GDPT 2018 chuẩn xác.
- [x] Bộ test `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` chạy đạt 100%.