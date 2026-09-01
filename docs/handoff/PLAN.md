# PLAN: Sửa Lỗi Bảng Chọn Tiết AI Bị Bó Hẹp 50% Chiều Rộng Và Khắc Phục Nút "Sinh Trọn Bộ Phụ Lục" Không Sinh Đủ 3 Phụ Lục Trong xaydungphuluc.html

## Hiện trạng
1. **Nguyên nhân bảng Mục 3 ("3. Chọn chính xác tiết tích hợp AI") bị co cụm dù đã mở rộng main**:
   - Trong thẻ `<section id="aiLessonPickerCard">`, phần tử chứa bảng có class cố định: `<div id="aiLessonPicker" class="grid md:grid-cols-2 gap-2 mt-3"></div>`.
   - Thuộc tính `grid md:grid-cols-2` ép toàn bộ bảng 8 cột (`.ai-picker-table`) chui vào 1 nửa (50% bề rộng màn hình), để trống hoàn toàn nửa bên phải.
   - Do bị ép vào khung 50%, các cột "Bài học", "Thiết bị", "Địa điểm", "Tích hợp AI" bị co nghẹt lại và ngắt dòng vụn vặt như trong ảnh người dùng gửi (`media_1788232765119.png`).
2. **Nguyên nhân nút "⚡ Sinh trọn bộ Phụ lục" chỉ sinh mỗi Phụ lục 3**:
   - Thẻ button ở Mục 6 đang gán `onclick="generateSelected()"` (không truyền tham số).
   - Hàm `generateSelected(force)` lấy `let selection = force || document.querySelector('[name=appendix]:checked').value`.
   - Nếu người dùng trước đó đã bấm chọn radio "Phụ lục 3" ở Mục 1 (hoặc radio Phụ lục 3 được chọn), khi bấm nút "⚡ Sinh trọn bộ Phụ lục", hệ thống lấy giá trị `'3'` thay vì `'all'`, dẫn đến mảng `list = ['3']` và chỉ sinh duy nhất Phụ lục 3.
   - Ngoài ra, khi sinh trọn bộ (`'all'`), nếu một phụ lục gặp lỗi hoặc thời gian chờ lâu, cần đảm bảo từng phụ lục (`results['1']`, `results['2']`, `results['3']`) được xử lý tuần tự, hiển thị log/tiến trình rõ ràng và chuyển tab xem trước linh hoạt.

---

## Phạm vi
1. **Khắc phục triệt để lỗi bề rộng Bảng chọn tiết AI (Mục 3)**:
   - Xóa bỏ class `grid md:grid-cols-2 gap-2` tại `#aiLessonPicker`, đổi thành `<div id="aiLessonPicker" class="w-full mt-3 overflow-x-auto"></div>`.
   - Bảng `.ai-picker-table` chiếm trọn vẹn 100% bề rộng màn hình (Full width container), các cột dữ liệu trải rộng thông thoáng, không còn hiện tượng chia đôi màn hình vô lý.
2. **Khắc phục nút "⚡ Sinh trọn bộ Phụ lục"**:
   - Gán rõ ràng `onclick="generateSelected('all')"` cho nút `generateAll` ở Mục 6 và đồng bộ với radio "⚡ Trọn bộ 1–2–3" ở Mục 1.
   - Đảm bảo khi bấm "⚡ Sinh trọn bộ Phụ lục", hệ thống chắc chắn chạy vòng lặp cho đủ cả 3 phụ lục: `list = ['1', '2', '3']`.
   - Cập nhật dữ liệu đầy đủ vào `results['1']`, `results['2']`, `results['3']`, cập nhật tiến trình từng bước `① Phân tích -> ② Phụ lục 1 -> ③ Phụ lục 2 -> ④ Phụ lục 3 -> Hoàn tất`.
   - Sau khi hoàn thành trọn bộ, mặc định hiển thị Tab Phụ lục 1 và bật sáng tab để người dùng có thể nhấp xem ngay cả 3 tab Phụ lục 1, 2, 3 ở Mục 7.
3. **Kiểm thử**:
   - Cập nhật test `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` xác thực:
     * `#aiLessonPicker` không còn chứa `grid md:grid-cols-2`.
     * Nút `generateAll` gọi `generateSelected('all')`.
     * `generateSelected('all')` sinh và lưu trữ đầy đủ `results['1']`, `results['2']`, `results['3']`.

---

## Ngoài phạm vi
- Không thay đổi các quy chuẩn sư phạm (CV 5512, TT 38/2021, TT 14/2020, NLS CV 3456 / TT 02, Khung AI QĐ 2422).
- Không can thiệp vào các trang khác (`soankhbd.html`, `admin.html`).

---

## File dự kiến tác động
- `xaydungphuluc.html` [XÓA BỎ GRID MD:GRID-COLS-2 TẠI #aiLessonPicker, GÁN ONCLICK='generateSelected(\"all\")' CHO NÚT SINH TRỌN BỘ]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG TEST CHO GIAO DIỆN FULL-WIDTH MỤC 3 VÀ SINH ĐỦ TRỌN BỘ 3 PHỤ LỤC]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi hoàn thành triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

---

## Các bước thực hiện
1. **Bước 1: Sửa HTML `#aiLessonPicker` trong `xaydungphuluc.html`**:
   - Tìm thẻ `<div id="aiLessonPicker" class="grid md:grid-cols-2 gap-2 mt-3"></div>`.
   - Sửa thành `<div id="aiLessonPicker" class="w-full mt-3 overflow-x-auto"></div>`.
   - Đảm bảo thẻ cha `<section id="aiLessonPickerCard">` có class `card p-5 w-full`.
2. **Bước 2: Sửa nút hành động Mục 6 & Logic `generateSelected`**:
   - Trong Mục 6:
     * Đổi `<button id="generateAll" class="btn primary" onclick="generateSelected()">⚡ Sinh trọn bộ Phụ lục</button>` thành `<button id="generateAll" class="btn primary" onclick="generateSelected('all')">⚡ Sinh trọn bộ Phụ lục</button>`.
   - Trong hàm `generateSelected(force)`:
     * Đảm bảo `const selection = force || (document.querySelector('[name=appendix]:checked') ? document.querySelector('[name=appendix]:checked').value : 'all');`
     * `const list = (selection === 'all' || !selection) ? ['1', '2', '3'] : [selection];`
     * Nếu `selection === 'all'`, tự động check radio `input[value="all"]` ở Mục 1 để giao diện đồng bộ.
     * Chạy tuần tự cho từng phụ lục trong `list`, lưu kết quả vào `results[no]`, cập nhật log chi tiết `✓ Hoàn thành Phụ lục ${no}`.
     * Khi hoàn thành, gọi `showTab('1')` (hoặc `showTab(list[0])`), kích hoạt sẵn sàng cả 3 tab xem trước và xuất Word ở Mục 7.
3. **Bước 3: Cập nhật kiểm thử tự động `tests/xaydungphuluc-smoke.js`**:
   - Bổ sung assertion:
     * `assert(!html.includes('id="aiLessonPicker" class="grid md:grid-cols-2'), '#aiLessonPicker must not be split into 2-column grid');`
     * `assert(html.includes("onclick=\"generateSelected('all')\""), 'generateAll button must explicitly trigger all 3 appendices');`
     * Mô phỏng chạy `generateSelected('all')` kiểm tra `results['1']`, `results['2']`, `results['3']` đều có dữ liệu.
4. **Bước 4: Chạy test và khóa handoff**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`.
   - Ghi `LOCK` vào `docs/handoff/.lock`.

---

## Rủi ro & Giải pháp
1. **Rủi ro người dùng bấm radio Mục 1 sau đó bấm nút Mục 6**:
   - *Giải pháp*: Nút "⚡ Sinh trọn bộ Phụ lục" truyền tường minh `'all'`, luôn sinh đủ cả 3 phụ lục bất kể radio nào đang chọn; các nút "Sinh PL 1", "Sinh PL 2", "Sinh PL 3" truyền tương ứng `'1'`, `'2'`, `'3'`.
2. **Rủi ro bảng quá rộng trên thiết bị di động**:
   - *Giải pháp*: Container bọc `overflow-x-auto` cho phép cuộn ngang mượt mà trên màn hình nhỏ mà vẫn hiển thị 100% full width trên màn hình máy tính.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - `node tests/xaydungphuluc-smoke.js`
   - `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html`:
     * Kiểm tra Mục 3: Bảng chọn tiết AI mở rộng 100% toàn bộ chiều rộng thẻ, không còn bị ép vào cột 50% bên trái.
     * Bấm nút "⚡ Sinh trọn bộ Phụ lục":
       - Quan sát tiến trình chạy đủ qua 3 phụ lục: PL 1 -> PL 2 -> PL 3.
       - Log hiển thị hoàn thành đủ cả 3 phụ lục.
       - Chuyển qua các tab Phụ lục 1, Phụ lục 2, Phụ lục 3 ở Mục 7 đều có nội dung đầy đủ.
       - Bấm nút "📦 Tải trọn bộ (.zip)" tải về file zip chứa đủ `Phu-luc-1.docx`, `Phu-luc-2.docx`, `Phu-luc-3.docx`.

---

## Tiêu chí nghiệm thu
- [x] Bảng chọn tiết AI ở Mục 3 mở rộng 100% toàn màn hình, xóa bỏ hoàn toàn class `grid md:grid-cols-2` gây bó hẹp 50%.
- [x] Nút "⚡ Sinh trọn bộ Phụ lục" luôn sinh đầy đủ cả 3 Phụ lục (1, 2, 3), lưu kết quả vào `results['1']`, `results['2']`, `results['3']`.
- [x] Người dùng xem trước được đầy đủ cả 3 tab Phụ lục ở Mục 7 và xuất được trọn bộ file zip chứa đủ 3 file Word.
- [x] Bộ test `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` đạt PASS 100%.