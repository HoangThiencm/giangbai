# PLAN: Nâng cấp Quản lý Ngày nghỉ (Toàn trường & Cá nhân), Hỗ trợ Nhiều ngày nghỉ trong tuần và Chuẩn hóa Gửi TKB/LBG cho Giáo viên

**Ngày lập:** 2026-11-22  
**Mục tiêu:**
1. **Sửa lỗi gửi TKB cho giáo viên vẫn còn lịch vào ngày nghỉ:** Khi đã thêm ngày nghỉ (ví dụ nghỉ lễ toàn trường hoặc ngày nghỉ cá nhân), bảng Thời khóa biểu gửi qua email (cho cá nhân, gửi tổng hợp, hoặc gửi riêng từng GV) phải nhận diện chính xác ngày nghỉ trong tuần được chọn; các ô tiết học của ngày nghỉ phải được thay thế bằng trạng thái nghỉ rõ ràng (`NGHỈ LỄ: [Lý do]` / `NGHỈ PHÉP`), tuyệt đối không hiển thị lịch học bình thường.
2. **Chuẩn hóa phân loại ngày nghỉ Toàn trường & Cá nhân:** Cung cấp giao diện quản lý ngày nghỉ trực quan, dễ tiếp cận từ cả 3 khu vực: Tab Thời khóa biểu GV, Tab Gửi email, và Tab Lịch báo giảng. Phân định rành mạch 2 nhóm đối tượng:
   - **Nghỉ Toàn trường:** Áp dụng cho mọi giáo viên và học sinh toàn trường (nghỉ lễ 2/9, 20/11, 30/4 - 1/5, Giỗ Tổ, nghỉ đột xuất...).
   - **Nghỉ Cá nhân:** Áp dụng cho từng giáo viên cụ thể (chọn từ danh sách GV tổ chuyên môn) hoặc bản thân người đăng nhập (nghỉ ốm, việc riêng, công tác, thai sản...).
3. **Bổ sung tính năng Thêm ngày nghỉ linh hoạt theo Tuần (chọn 2 hay nhiều ngày nghỉ ngắt quãng trong tuần):**
   - Giải quyết triệt để vấn đề: "trong tuần có 2 ngày nghỉ thì lại không có chức năng thêm ngày nghỉ".
   - Cho phép chọn 1 Tuần học cụ thể, hệ thống hiển thị 6 ô chọn từ Thứ 2 đến Thứ 7 kèm ngày tháng dương lịch cụ thể (ví dụ: `Thứ Hai (23/11)`, `Thứ Năm (26/11)`). Người dùng có thể tick chọn cùng lúc 2 ngày (hoặc nhiều ngày bất kỳ), nhập lý do, chọn đối tượng (Toàn trường / Cá nhân), và lưu một chạm tạo đồng loạt các ngày nghỉ trong tuần đó.
4. **Hiển thị thông tin ngày nghỉ rõ ràng trong Lịch Báo Giảng (LBG) gửi email:** Ngày nghỉ toàn trường hoặc ngày nghỉ cá nhân trong tuần gửi LBG phải xuất hiện thành khối thông báo trang trọng, không bị biến mất âm thầm khiến giáo viên nghi ngờ dữ liệu.

---

## 1. Khảo sát hiện trạng & Nguyên nhân gốc rễ

### 1.1. Vấn đề gửi TKB qua email vẫn còn lịch dù đã thêm ngày nghỉ
- Trong `phancongtochuyenmon.html`, hàm dựng bảng TKB email `timetableEmailSessionTable(teacher, session)` (dòng ~7204) chỉ duyệt tĩnh qua 6 thứ: `TT_DAYS = ['2', '3', '4', '5', '6', '7']` dựa vào ma trận gốc `teacher.timetable`.
- Hàm này **không nhận tham số tuần/khoảng ngày**, do đó không hề đối chiếu với mảng ngoại lệ ngày nghỉ `state.bao_giang.exceptions`.
- Dù người dùng đã thêm "Nghỉ lễ toàn trường" hay "Giáo viên nghỉ" vào hệ thống, email TKB gửi đi vẫn hiển thị đầy đủ các tiết học của ngày đó như một tuần bình thường.
- Ở Tab Gửi email (`#view-email`), hai nút `sendMyTimetableEmail()` và `sendSelectedTeachersTimetableEmail()` không cho chọn tuần áp dụng TKB, chỉ gửi mẫu thời khóa biểu tĩnh không có ngày tháng cụ thể.

### 1.2. Vấn đề chức năng thêm ngày nghỉ bị phân tán và thiếu thân thiện
- Chức năng thêm ngày nghỉ hiện tại nằm sâu trong modal "Cài đặt PPCT & Lịch nghỉ" (`#baogiang-config-modal`, dòng ~2958) của Tab Lịch báo giảng. Người dùng ở Tab "Thời khóa biểu GV" hay Tab "Gửi email" không thấy nút quản lý ngày nghỉ.
- Menu phạm vi nghỉ (`#bg-ex-scope`) gồm 6 tùy chọn kỹ thuật rối rắm: `all`, `teacher`, `class`, `self`, `self_lesson`, `subject`. Người dùng phổ thông chỉ cần phân biệt nhanh: **Toàn trường** hay **Cá nhân giáo viên**.

### 1.3. Vấn đề trong tuần có 2 ngày nghỉ không liên tiếp
- Giao diện hiện tại chỉ có 2 ô `Từ ngày` và `Đến ngày`. Nếu tuần đó nghỉ Thứ Hai (Giỗ Tổ) và Thứ Sáu (hoạt động trải nghiệm):
  * Nếu chọn từ Thứ Hai đến Thứ Sáu: Hệ thống hiểu là nghỉ cả tuần (từ Thứ 2 đến Thứ 6 đều nghỉ)!
  * Nếu muốn thêm 2 ngày rời nhau: Người dùng phải tự tra lịch ngày tháng, nhập ngày thứ nhất, bấm thêm, rồi lại phải gõ lại ngày thứ hai. Form không reset, không có giao diện trực quan theo tuần, khiến người dùng kết luận "trong tuần có 2 ngày nghỉ thì lại không có chức năng thêm ngày nghỉ".

---

## 2. Kiến trúc giải pháp (Architecture & Solution Design)

### 2.1. Thiết kế Modal "Quản lý Ngày nghỉ & Ngoại lệ" (`#modal-manage-holidays`)
Modal chuyên dụng, hiện đại, có thể mở từ bất kỳ đâu qua nút `openHolidaysManagerModal()`:
1. **Nút mở modal:**
   - Tab "Thời khóa biểu GV" (`#view-timetable`): Thêm nút `<button type="button" class="btn-small" onclick="openHolidaysManagerModal()"><i class="fas fa-calendar-xmark text-rose-600"></i> Quản lý Ngày nghỉ</button>` vào toolbar.
   - Tab "Gửi email" (`#view-email`): Thêm nút mở modal ngày nghỉ tại phần đầu giao diện.
   - Tab "Lịch báo giảng" (`#view-baogiang`): Giữ liên kết mở nhanh trong modal cài đặt hoặc cạnh nút Cài đặt PPCT.
2. **Giao diện Modal gồm 2 Chế độ thêm ngày nghỉ:**
   - **Chế độ A: Thêm nhanh theo tuần (Weekly Multi-Days Selector):**
     * Chọn tuần áp dụng: `<input type="week" id="hl-week-input" onchange="renderWeeklyHolidayCheckboxes()">` (mặc định tuần hiện tại hoặc tuần kế tiếp).
     * Lưới 6 checkbox tương ứng Thứ 2, Thứ 3, Thứ 4, Thứ 5, Thứ 6, Thứ 7 kèm ngày tháng cụ thể (ví dụ: `[ ] Thứ 2 (23/11)`, `[ ] Thứ 3 (24/11)`...).
     * Người dùng dễ dàng tick chọn 1 ngày, 2 ngày bất kỳ (ví dụ: tick Thứ 2 và Thứ 5) hoặc tick cả tuần.
     * Đối tượng áp dụng:
       + Radio: `🔘 Toàn trường (Tất cả GV & học sinh)`
       + Radio: `⚪ Giáo viên cá nhân` -> Hiện danh sách chọn 1 hoặc nhiều GV trong tổ (có checkbox "Chọn tất cả" hoặc chọn GV riêng).
     * Buổi nghỉ: `Cả ngày` / `Buổi sáng` / `Buổi chiều`.
     * Lý do nghỉ: Ô nhập text kèm datalist gợi ý: `Nghỉ lễ`, `Nghỉ Giỗ Tổ Hùng Vương`, `Nghỉ 30/4 - 1/5`, `Nghỉ Tết`, `Công tác`, `Tập huấn`, `Nghỉ phép`, `Hội nghị`...
     * Nút: `<button class="btn-small btn-small-primary" onclick="saveWeeklyHolidayBatch()"><i class="fas fa-plus"></i> Lưu các ngày nghỉ đã chọn</button>`.
   - **Chế độ B: Thêm theo khoảng ngày dài (Date Range Picker):**
     * Dành cho đợt nghỉ dài nhiều ngày liên tiếp (Nghỉ Tết Nguyên Đán, nghỉ hè, nghỉ thai sản...).
     * Chọn `Từ ngày` -> `Đến ngày`, Đối tượng (Toàn trường / Giáo viên), Buổi, Lý do.
3. **Danh sách ngày nghỉ đã lưu (Holidays Table):**
   - Hiển thị bảng/danh sách các ngày nghỉ đã thiết lập trong học kỳ/năm học.
   - Cột: Ngày/Khoảng ngày | Thứ | Buổi | Đối tượng (`Toàn trường` / `Tên GV`) | Lý do | Thao tác (Xóa).
   - Tự động đồng bộ với `state.bao_giang.exceptions` để không làm gián đoạn bất kỳ luồng dữ liệu cũ nào.

### 2.2. Nâng cấp Bảng TKB gửi Email (`timetableEmailSessionTable`)
1. **Bổ sung tham số `weekRange` (hoặc `weekValue`) cho hàm dựng TKB email:**
   - `timetableEmailSessionTable(teacher, session, weekRange = null)`
   - Khi có `weekRange` (tính từ `baoGiangWeekRange(weekValue)` gồm `{ start, end }` từ Thứ 2 đến Chủ nhật):
     * Xác định ngày cụ thể ứng với từng thứ trong tuần (`TT_DAYS`: 2 -> Thứ 2, 3 -> Thứ 3...).
     * Kiểm tra xem ngày đó đối với giáo viên `teacher` có rơi vào ngày nghỉ hay không:
       ```javascript
       function isTeacherDayOff(teacher, dateStr, session) {
           return (state.bao_giang.exceptions || []).find(ex => {
               if (ex.type !== 'off') return false;
               const from = ex.start_date || ex.date, to = ex.end_date || from;
               if (dateStr < from || dateStr > to) return false;
               const exSession = ex.session || 'all_day';
               if (exSession !== 'all_day' && exSession !== session) return false;
               return baoGiangMatchesException(ex, { date: dateStr, session, teacher_id: teacher.id, teacher_name: teacher.name });
           });
       }
       ```
     * **Xử lý hiển thị trên bảng TKB:**
       - Nếu cả thứ đó là ngày nghỉ (Toàn trường hoặc GV nghỉ cả ngày/buổi): Thay vì render các tiết học bình thường, ô tiết của ngày đó hiển thị khối nền xám/nổi bật:
         `NGHỈ LỄ` hoặc `NGHỈ PHÉP` kèm lý do:
         `<div style="padding:6px; background:#f1f5f9; border-radius:6px; color:#475569; font-weight:700; font-size:12px;">NGHỈ LỄ<br><span style="font-weight:normal; font-size:11px; color:#64748b;">${escapeHtml(dayOff.reason || 'Nghỉ theo quy định')}</span></div>`
       - Tiêu đề cột các thứ: Bổ sung ngày tháng cụ thể (ví dụ: `Thứ 2<br><small>23/11</small>`). Nếu là ngày nghỉ toàn trường, tiêu đề thứ có huy hiệu `(Nghỉ)`.
2. **Cập nhật giao diện Tab Gửi email (`#view-email`):**
   - Thêm ô chọn **Tuần áp dụng TKB cần gửi** (`#email-tt-week`) tại cả Tab 1 ("TKB của tôi") và Tab 2 ("TKB tất cả GV → email tôi").
   - Nhãn hiển thị trực quan: `Tuần 12 (Từ 23/11 đến 29/11/2026) — 2 ngày nghỉ (Thứ 2, Thứ 5)`.
   - Bổ sung nút bấm gọi `sendSelectedTeachersIndividualTimetableEmail()` trong Tab Email: "Gửi riêng TKB tuần này cho từng GV đã chọn" (đảm bảo mỗi GV nhận đúng TKB tuần của mình có đánh dấu ngày nghỉ).

### 2.3. Nâng cấp Lịch Báo Giảng (LBG) tuần gửi Email
- Trong `buildTeacherBaoGiangWeekHtml(teacher, range, ordered, webcalUrl, pageUrl)`:
  * Khi lặp qua các ngày trong tuần từ Thứ 2 đến Thứ 7:
  * Nếu ngày đó có tiết dạy: Hiển thị bảng tiết như bình thường.
  * Nếu ngày đó **không có tiết do rơi vào ngày nghỉ** (toàn trường hoặc cá nhân):
    Hiển thị khối thông báo ngày nghỉ rõ ràng:
    `<div style="margin:0 0 16px; padding:12px 14px; background:#fef2f2; border:1px solid #fecaca; border-radius:10px; color:#991b1b;"><b style="font-size:14px;"><i class="fas fa-calendar-xmark"></i> ${escapeHtml(baoGiangWeekdayLabel(date))}, ngày ${escapeHtml(formatVnDate(date))}</b>: NGHỈ TOÀN TRƯỜNG (${escapeHtml(holidayReason)})</div>`
  * Nhờ vậy, giáo viên nhận email nhìn vào tuần sẽ thấy rõ ràng ngày nào nghỉ lễ và ngày nào dạy, không bị hoang mang khi thấy thiếu ngày.

---

## 3. Các tệp cần sửa đổi & Kế hoạch triển khai chi tiết

### 3.1. `phancongtochuyenmon.html`
1. **Giao diện HTML:**
   - Bổ sung Modal Quản lý Ngày nghỉ `#modal-manage-holidays` (Chế độ theo tuần có checkbox 6 ngày, chế độ khoảng ngày, danh sách ngày nghỉ).
   - Thêm nút "Quản lý Ngày nghỉ" vào toolbar của `#view-timetable` và `#view-email`.
   - Thêm bộ chọn Tuần gửi TKB `#email-tt-week` và nhãn thông tin ngày nghỉ trong `#view-email`.
   - Thêm nút "Gửi riêng TKB tuần cho từng GV" vào Tab 2 của `#view-email`.
2. **Hàm JavaScript mới & cập nhật:**
   - `openHolidaysManagerModal()`: Mở modal quản lý ngày nghỉ, đồng bộ tuần hiện tại và nạp danh sách ngày nghỉ.
   - `closeHolidaysManagerModal()`: Đóng modal.
   - `renderWeeklyHolidayCheckboxes()`: Tính toán ngày cụ thể (YYYY-MM-DD) cho từng thứ từ Thứ 2 đến Thứ 7 của tuần đang chọn, hiển thị 6 checkbox tương ứng.
   - `saveWeeklyHolidayBatch()`: Đọc các checkbox thứ được chọn trong tuần, tạo các bản ghi ngoại lệ tương ứng (dùng `state.bao_giang.exceptions`), lưu vào localStorage & đồng bộ CSDL (`saveToDB()` / `saveToLocal()`), hiển thị toast thành công.
   - `renderHolidaysList()`: Hiển thị bảng tổng hợp toàn bộ các ngày nghỉ đã có trong hệ thống, phân loại rõ Toàn trường vs Cá nhân, kèm nút xóa.
   - `deleteHolidayException(id)`: Xóa một ngày nghỉ và làm mới giao diện.
   - `isTeacherDayOff(teacher, dateStr, session)`: Hàm phụ trợ kiểm tra ngày nghỉ cho một giáo viên tại một ngày/buổi cụ thể.
   - Cập nhật `timetableEmailSessionTable(teacher, session, weekRange)`: Render ô ngày nghỉ thay vì tiết học khi rơi vào ngày nghỉ.
   - Cập nhật `buildTeacherIndividualTimetableEmail(teacher, recipient, requireRecipient, webcalUrl, weekValue)`: Nhận thêm `weekValue`, chuyển đổi thành `weekRange` và truyền vào `timetableEmailSessionTable`.
   - Cập nhật `buildSelectedTeachersTimetableEmail(teacherIds, weekValue)`: Nhận `weekValue` và truyền vào các bảng giáo viên.
   - Cập nhật `buildTeacherBaoGiangWeekHtml(teacher, range, ordered, ...)`: Bổ sung khối render thông báo ngày nghỉ cho những ngày nghỉ trong tuần.
   - Cập nhật `syncBaoGiangEmailWeek` và thêm `syncTimetableEmailWeek` để cập nhật nhãn số ngày nghỉ trong tuần được chọn.

### 3.2. `tests/timetable-render-smoke.js`
- Bổ sung các case kiểm thử tự động (Smoke test):
  1. Kiểm tra cấu trúc Modal Quản lý Ngày nghỉ `#modal-manage-holidays` và các hàm xử lý batch ngày nghỉ trong tuần.
  2. Kiểm tra hàm `timetableEmailSessionTable` khi có ngày nghỉ toàn trường: xác nhận cột ngày nghỉ hiển thị nội dung `NGHỈ LỄ` (hoặc lý do nghỉ) và KHÔNG còn môn học cũ.
  3. Kiểm tra trường hợp trong tuần có 2 ngày nghỉ không liên tiếp (ví dụ Thứ 2 và Thứ 5): xác nhận cả hai ngày Thứ 2 và Thứ 5 đều hiển thị trạng thái nghỉ, các ngày Thứ 3, 4, 6, 7 vẫn giữ nguyên lịch dạy.
  4. Kiểm tra ngày nghỉ cá nhân (giáo viên A nghỉ, giáo viên B không nghỉ): xác nhận chỉ email của giáo viên A hiển thị ngày nghỉ, email của giáo viên B vẫn có tiết học bình thường.

### 3.3. `tests/baogiang-mail-smoke.js`
- Bổ sung kiểm thử:
  1. Bảng LBG gửi qua email (`buildTeacherBaoGiangWeekHtml`) hiển thị khối thông báo ngày nghỉ rõ ràng khi có ngày nghỉ toàn trường trong tuần.

---

## 4. Kịch bản xác minh (Verification Scenarios)

1. **Kịch bản 1 — Khai báo 2 ngày nghỉ trong tuần:**
   - Mở Modal Quản lý Ngày nghỉ.
   - Chọn tuần (ví dụ: Tuần 12 từ 23/11/2026 đến 29/11/2026).
   - Tick chọn 2 ngày: Thứ Hai (23/11) và Thứ Năm (26/11).
   - Chọn đối tượng "Toàn trường", lý do: "Nghỉ lễ & Hoạt động ngoại khóa".
   - Bấm "Lưu các ngày nghỉ đã chọn".
   - Kết quả: Danh sách ngày nghỉ hiển thị 2 bản ghi mới tương ứng ngày 23/11 và 26/11 với nhãn Toàn trường.

2. **Kịch bản 2 — Gửi TKB cho Giáo viên phản ánh chính xác ngày nghỉ:**
   - Vào Tab Gửi email (`#view-email`), chọn Tuần 12.
   - Nhãn thông báo hiển thị: "Tuần 12 (Từ 23/11 đến 29/11/2026) — 2 ngày nghỉ (Thứ 2, Thứ 5)".
   - Xem nội dung TKB được tạo bởi `buildTeacherIndividualTimetableEmail`:
     * Cột Thứ Hai và cột Thứ Năm: Các ô tiết học được thay bằng nhãn `NGHỈ LỄ: Nghỉ lễ & Hoạt động ngoại khóa`.
     * Cột Thứ Ba, Thứ Tư, Thứ Sáu, Thứ Bảy: Vẫn giữ nguyên phân bổ tiết học bình thường.

3. **Kịch bản 3 — Khai báo Ngày nghỉ cá nhân cho một giáo viên:**
   - Thêm ngày nghỉ cá nhân cho Thầy Tùng vào Thứ Ba (24/11).
   - Tạo TKB cho Thầy Tùng: Thứ Ba hiển thị `NGHỈ PHÉP` / `Cá nhân nghỉ`.
   - Tạo TKB cho Cô Thảo: Thứ Ba vẫn có tiết dạy bình thường.

4. **Kịch bản 4 — Chạy toàn bộ Smoke Tests:**
   - Chạy `node tests/timetable-render-smoke.js` -> PASS.
   - Chạy `node tests/baogiang-mail-smoke.js` -> PASS.
