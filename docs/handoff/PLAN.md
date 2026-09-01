# PLAN: Chuẩn Hóa Yêu Cầu Cần Đạt Sư Phạm, Khớp Chính Xác Bài Học & Tri Thức SGK, Đa Dạng Mã NLS Theo Mật Độ Và Xuất File Word Khổ Nằm Ngang (Landscape)

## Hiện trạng
1. **Lỗi tràn văn bản quy chuẩn / prompt vào cột "Yêu cầu cần đạt" (Phụ lục 1)**:
   - Hàm `getOfficialYccd` trong `js/khbd-yccd.js` sinh ra khối văn bản tiền đề cho prompt (`"Nguồn bắt buộc: Yêu cầu cần đạt môn Toán 6–12... Căn cứ pháp lý: Thông tư 32/2018... Bài SGK:... Nội dung CTGDPT 2018 tham chiếu:..."`).
   - Khi `appendixOneFallbackOutcome` sử dụng kết quả này hoặc khi AI trả về nguyên văn prompt tham chiếu, toàn bộ văn bản quy chuẩn này bị đưa thẳng vào ô "Yêu cầu cần đạt" trong bảng hiển thị và file Word (`media_1788237703203.png`).
2. **Lỗi so khớp bài học sai lệch kiến thức (Bài cộng trừ số nguyên lại gán YCCĐ và mã của Ước chung lớn nhất)**:
   - Thuật toán `scoreYccdRow` và tìm kiếm bài học chấm điểm theo từ khóa đơn giản trong chuỗi, dẫn đến các bài số nguyên (như Bài 14: Phép cộng và phép trừ số nguyên) bị gán nhầm sang bài Bài 11 (Ước chung. Ước chung lớn nhất).
   - Chưa bóc tách chính xác số thứ tự bài ("Bài 14", "Bài 4"...) và tên bài chuẩn hóa để map trực tiếp 1-1 với kho YCCĐ.
3. **Mã Năng lực số (NLS) chỉ hiển thị 1 mã duy nhất, chưa bám sát tri thức SGK và mật độ cấu hình**:
   - Hàm fallback `integrationText` đang cố định `standard.digital.slice(0, 1)` (chỉ lấy đúng 1 mã).
   - Chưa tích hợp linh hoạt mật độ NLS (`nlsDensity`: `1-2`, `2-3`, `3-4` mã/bài) và chưa liên kết sâu với từ khóa hoạt động thực tế từ SGK đã đọc.
4. **File Word xuất ra (.docx) đang để khổ dọc (Portrait) gây chật chội bảng**:
   - Trong hàm `exportDocx`, cấu hình trang đang là `width: 11906, height: 16838` (khổ dọc A4), khiến bảng 7–8 cột bị co hẹp lề, chữ trong các ô bị ngắt dòng nhiều. Người dùng yêu cầu chuyển file Word sang khổ **nằm ngang (Landscape)**.

---

## Phạm vi
1. **Chuẩn hóa hàm trích xuất Yêu cầu cần đạt sạch (`getCleanYccdForLesson`)**:
   - Xây dựng hàm trích xuất YCCĐ tinh gọn, chỉ lấy nội dung các gạch đầu dòng hành vi chuẩn của học sinh từ `KHBD_YCCD.toan[grade]` hoặc từ SGK/AI:
     * Loại bỏ 100% các câu hành chính, metadata ("Nguồn bắt buộc...", "Căn cứ pháp lý...", "Bài SGK:", "Nội dung CTGDPT 2018 tham chiếu:").
     * Định dạng kết quả sạch: các gạch đầu dòng rõ ràng, chuẩn ngữ pháp sư phạm.
2. **Nâng cấp thuật toán so khớp bài học chuẩn xác 1-1**:
   - Chuẩn hóa tách số hiệu bài học (vd: "Bài 14.", "Bài 4.", "Bài 11.") và so khớp chính xác tên bài học với `KHBD_YCCD.toan[grade]` và mục lục SGK.
   - Đảm bảo bài nào thì sinh đúng YCCĐ và mã NLS/AI của bài đó: Bài Số nguyên / Phép tính số nguyên chỉ sinh kiến thức về số nguyên và quy tắc dấu ngoặc, tuyệt đối không gán sang Ước chung lớn nhất.
3. **Sinh đa dạng mã NLS theo đúng cấu hình mật độ và tri thức SGK**:
   - Nâng cấp `integrationText` và prompt AI để sinh đúng số lượng mã NLS theo `nlsDensity` (`1–2`, `2–3`, `3–4` mã/bài).
   - Phối hợp các nhóm năng lực số phù hợp (tìm kiếm dữ liệu `1.1.TC1a`, giải quyết vấn đề số `5.3.TC1a`, giao tiếp số `2.1.TC1a`, sáng tạo nội dung số `3.1.TC1a`...).
4. **Chuyển đổi toàn bộ xuất file Word (.docx) sang khổ nằm ngang (Landscape)**:
   - Cập nhật cấu hình phần `sections` trong `docx.Document` thành khổ ngang A4:
     `size: { width: 16838, height: 11906, orientation: docx.PageOrientation.LANDSCAPE }` (hoặc `orientation: 'landscape'`), margin cân đối 1.5cm–2cm (`top: 1134, bottom: 1134, left: 1134, right: 1134`).
   - Giúp bảng Phụ lục 1 (5 cột) và Phụ lục 3 (7 cột) hiển thị thoáng đãng, chuyên nghiệp, đúng quy cách hồ sơ chuyên môn THCS.

---

## Ngoài phạm vi
- Không can thiệp vào các trang khác như `soankhbd.html`, `admin.html`.
- Không thay đổi các quy định bảo mật API key.

---

## File dự kiến tác động
- `xaydungphuluc.html` [HÀM getCleanYccdForLesson SẠCH METADATA, SO KHỚP CHÍNH XÁC BÀI HỌC, NLS THEO MẬT ĐỘ, WORD KHỔ NẰM NGANG LANDSCAPE]
- `js/khbd-yccd.js` [TỐI ƯU HÓA HÀM TRÍCH XUẤT YCCĐ VÀ MATCHING ĐẢM BẢO KHÔNG BỊ LỆCH BÀI]
- `tests/xaydungphuluc-smoke.js` [KIỂM TRA YCCĐ SẠCH KHÔNG CHỨA METADATA, WORD KHỔ NGANG LANDSCAPE, MẬT ĐỘ NLS]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi hoàn thành triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

---

## Các bước thực hiện
1. **Bước 1: Nâng cấp `getCleanYccdForLesson` trong `xaydungphuluc.html` và `js/khbd-yccd.js`**:
   - Viết hàm `getCleanYccdForLesson(lessonName, grade, subject)`:
     * Bóc tách số bài học (vd: `Bài 14`, `Bài 4`) và từ khóa chính (vd: `phép cộng và phép trừ số nguyên`).
     * Tra cứu trực tiếp trong `KHBD_YCCD.toan[grade]`:
       + Tìm kiếm ưu tiên 1: Cùng số hiệu bài (ví dụ `Bài 14`).
       + Tìm kiếm ưu tiên 2: Khớp tên bài học sau khi chuẩn hóa không dấu.
     * Khi tìm thấy: Lấy mảng `row.items`, lọc các câu trùng lặp, nối thành danh sách gạch đầu dòng: `row.items.map(item => '- ' + item.trim()).join('\n')`.
     * Tuyệt đối không thêm bất kỳ dòng nào chứa `"Nguồn bắt buộc"`, `"Căn cứ pháp lý"`, `"Bài SGK"`, `"Nội dung CTGDPT 2018 tham chiếu"`.
2. **Bước 2: Chuẩn hóa cột "Yêu cầu cần đạt" trong Phụ lục 1 (`appendixOneTable` và `appendixPrompt`)**:
   - Trong `appendixOneTable`: Nếu kết quả do AI sinh ra có chứa các cụm từ boilerplate (`Nguồn bắt buộc`, `Căn cứ pháp lý`, `tham chiếu`), tự động làm sạch hoặc thay thế bằng `getCleanYccdForLesson`.
   - Trong `appendixPrompt('1')`: Ràng buộc AI: "Chỉ viết ngắn gọn các mục tiêu hành vi học sinh đạt được (bắt đầu bằng động từ: Nhận biết, Thực hiện, Vận dụng, Giải quyết...). Cấm đưa các câu dẫn văn bản, căn cứ pháp lý, hay tiêu đề mục vào ô yêu cầu cần đạt."
3. **Bước 3: Tối ưu hóa gợi ý Mã NLS theo mật độ và tri thức SGK**:
   - Trong hàm `integrationText(i, c, lesson)`:
     * Đọc `c.nls.density` để xác định số lượng mã NLS cần lấy (ví dụ `1-2` -> lấy 1-2 mã; `2-3` -> lấy 2-3 mã; `3-4` -> lấy 3-4 mã).
     * Phân bổ các mã NLS chuẩn từ `KHBD_STANDARDS.digital` phù hợp với nội dung bài (Toán số học dùng `1.1.TC1a`, `5.3.TC1a`; Hình học dùng `3.1.TC1a`, `5.2.TC1a`; Thống kê dùng `1.2.TC1a`, `1.3.TC1a`...).
     * Nếu có ngữ cảnh SGK (`sgkCompactContext`), ưu tiên các mã NLS tương ứng với các hoạt động số/khám phá của bài trong SGK.
4. **Bước 4: Cập nhật cấu hình xuất Word DOCX sang khổ nằm ngang (Landscape)**:
   - Trong `exportDocx(n, save)`:
     * Cập nhật section properties:
       ```js
       properties: {
         page: {
           size: {
             width: 16838, // Chiều rộng khổ A4 ngang (twips)
             height: 11906, // Chiều cao khổ A4 ngang (twips)
             orientation: docx.PageOrientation.LANDSCAPE
           },
           margin: {
             top: 1134,   // 2 cm
             bottom: 1134,
             left: 1134,
             right: 1134
           }
         }
       }
       ```
5. **Bước 5: Cập nhật kiểm thử tự động `tests/xaydungphuluc-smoke.js`**:
   - Kiểm tra `getCleanYccdForLesson('Bài 14. Phép cộng và phép trừ số nguyên', '6', 'Toán học')` phải trả về đúng YCCĐ của số nguyên, không được trả về Ước chung lớn nhất.
   - Kiểm tra `appendixOneTable` không chứa bất kỳ từ khóa nào như `"Nguồn bắt buộc"`, `"Căn cứ pháp lý"`.
   - Kiểm tra cấu hình DOCX có `width: 16838`, `height: 11906`, `LANDSCAPE`.
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js` đạt 100% PASS.
6. **Bước 6: Khóa trạng thái giao việc**:
   - Ghi `LOCK` vào `docs/handoff/.lock`.

---

## Rủi ro & Giải pháp
1. **Rủi ro người dùng tải lên bài học viết tắt hoặc tên khác SGK mẫu**:
   - *Giải pháp*: Kết hợp trích xuất số thứ tự bài kết hợp so khớp ngữ nghĩa từ khóa chính và ngữ cảnh SGK đã nạp ở Bước 2.
2. **Rủi ro khổ ngang làm bảng phụ mục I, III bị giãn quá rộng**:
   - *Giải pháp*: Định dạng tỷ lệ phần trăm các cột trong bảng phụ hợp lý (STT: 5%, Thiết bị/Phòng: 30%, Số lượng: 15%, Phạm vi: 35%, Ghi chú: 15%) để trang văn bản cân đối, đẹp mắt.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - `node tests/xaydungphuluc-smoke.js`
   - `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html`:
     * Kiểm tra Phụ lục 1: Cột "Yêu cầu cần đạt" hiển thị danh sách mục tiêu sư phạm sạch sẽ, chuẩn xác cho từng bài (Bài 14 số nguyên có YCCĐ về phép cộng trừ số nguyên, quy tắc dấu ngoặc; không có Ước chung lớn nhất; không có chữ "Nguồn bắt buộc...").
     * Kiểm tra cột "Mã NLS & AI": Hiển thị đủ 2-3 mã NLS theo mật độ cấu hình, kết hợp đúng mã AI cho các tiết đã chọn.
     * Bấm "📥 Xuất phụ lục đang xem (.docx)": Mở file Word và kiểm tra toàn bộ trang văn bản nằm ngang (Landscape), bảng rộng rãi, trình bày đẹp mắt.

---

## Tiêu chí nghiệm thu
- [x] Cột "Yêu cầu cần đạt" ở Phụ lục 1 hiển thị các mục tiêu hành vi sư phạm sạch, hoàn toàn không chứa văn bản quy chuẩn/boilerplate ("Nguồn bắt buộc...", "Căn cứ pháp lý...").
- [x] Bài học nào thì khớp chính xác 100% YCCĐ của bài học đó (Bài số nguyên không gán nhầm sang Ước chung lớn nhất).
- [x] Mã NLS được sinh đa dạng theo đúng mật độ `nlsDensity` cấu hình (1–2, 2–3, hoặc 3–4 mã/bài) và liên kết với tri thức SGK.
- [x] Toàn bộ file Word (.docx) của Phụ lục 1, Phụ lục 2, Phụ lục 3 được xuất theo khổ **nằm ngang (Landscape)**.
- [x] Bộ test `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` đạt PASS 100%.