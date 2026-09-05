# PLAN: Tùy Chỉnh Khung Tiết Buổi Sáng & Chiều + Tích Hợp AI Nhận Diện Thời Khóa Biểu Giáo Viên (phancongtochuyenmon.html)

## Hiện trạng & Nhu cầu người dùng
1. **Khung tiết cứng nhắc**:
   - Hiện tại, khu vực "Phân bổ từng tiết" của Sổ Dạy Thay đang gán cứng 5 tiết: `[1, 2, 3, 4, 5]` cho cả sáng và chiều.
   - Thực tế các trường có khung tiết khác nhau: sáng có nơi học 4 tiết (`1-4`), chiều có nơi học 3 tiết (`7-9` hoặc `6-8`) hoặc 4 tiết (`1-4`, `6-9`).
2. **Nhu cầu quản lý Thời khoá biểu (TKB) và nhận diện AI**:
   - Mỗi giáo viên trong tổ đều có Thời khoá biểu riêng theo tuần (gồm Thứ 2 đến Thứ 7, từng tiết dạy môn gì, lớp nào).
   - Người dùng muốn: Chọn giáo viên $\rightarrow$ Dán ảnh chụp TKB (Ctrl+V) $\rightarrow$ AI nhận diện tự động cấu trúc TKB và lưu lại.
   - **Giá trị cốt lõi**: Khi ghi nhận Sổ Dạy Thay, chọn ngày dạy (ví dụ Thứ 4) và chọn GV được thay (ví dụ Cô Ánh hoặc Thầy Danh) $\rightarrow$ Hệ thống tự động tra TKB của GV đó và tự động điền sẵn các tiết, lớp học và môn học tương ứng, người dùng không cần mở ảnh TKB để tra cứu thủ công từng tiết.

---

## Mục tiêu kỹ thuật

### Phần 1: Tùy chỉnh khung tiết Sáng / Chiều linh hoạt
1. Lưu cấu hình khung tiết vào `state.info`:
   - `morning_periods`: Mặc định `'1-5'` (cho phép người dùng đổi thành `'1-4'`, `'1-5'`...).
   - `afternoon_periods`: Mặc định `'1-4'` (cho phép người dùng đổi thành `'7-9'`, `'6-9'`, `'1-4'`...).
2. Hỗ trợ nhập định dạng dải (VD: `1-4`, `7-9`) hoặc liệt kê cách nhau bởi dấu phẩy (VD: `7, 8, 9`).
3. Cung cấp 2 nơi cấu hình:
   - Nút `⚙️ Khung tiết` ngay tại thanh công cụ của Sổ Dạy Thay (sửa nhanh).
   - Trong Modal "Khai báo tổ" (tab Thông tin tổ).
4. Dropdown Buổi dạy và Lưới Slot Builder:
   - Dropdown Buổi dạy tự động đổi nhãn: `Sáng (tiết 1 - 4)`, `Chiều (tiết 7 - 9)`.
   - Lưới hiển thị đúng các tiết theo buổi: Sáng hiện `Tiết 1 - 4`, Chiều hiện `Tiết 7, 8, 9`.
   - Nút chọn nhanh tự động sinh phù hợp theo dải tiết (`+ Tiết 7-8`, `+ Tiết 8-9`, `+ Cả buổi (7-9)`).
   - Nút `+ Thêm tiết` để chèn thêm tiết bất kỳ đột xuất và nút `✕` để xóa bớt slot tiết.

### Phần 2: Quản lý Thời khoá biểu Giáo viên + AI Gemini Vision nhận diện
1. **Cấu trúc dữ liệu TKB**:
   - Thêm trường `timetable` vào đối tượng mỗi giáo viên trong `state.teachers`:
     ```javascript
     {
       updated_at: '2026-09-07',
       school_year: '2026 - 2027',
       semester: 'Học kỳ 1',
       morning: {
         "2": { "3": { subject: "Toán", class_name: "63" }, "4": { subject: "Toán", class_name: "64" } },
         "3": { "1": { subject: "Toán", class_name: "63" }, "3": { subject: "Toán", class_name: "64" }, "4": { subject: "Toán", class_name: "94" } },
         "4": { "1": { subject: "Toán", class_name: "93" }, "2": { subject: "Toán", class_name: "93" }, "3": { subject: "Toán", class_name: "94" }, "4": { subject: "Toán", class_name: "94" } },
         "5": { "2": { subject: "Toán", class_name: "64" }, "3": { subject: "Toán", class_name: "63" }, "4": { subject: "Toán", class_name: "93" } },
         "6": { "1": { subject: "Toán", class_name: "63" }, "2": { subject: "Toán", class_name: "94" }, "3": { subject: "Toán", class_name: "64" }, "4": { subject: "Toán", class_name: "93" } },
         "7": {}
       },
       afternoon: {
         "2": {}, "3": {}, "4": {}, "5": {}, "6": {}, "7": {}
       }
     }
     ```
2. **Modal Thời khoá biểu Giáo viên (`#teacher-timetable-modal`)**:
   - Mở từ nút `📅 Thời khoá biểu` trên thẻ card của Giáo viên ở View 1 hoặc nút `📅 TKB Giáo viên` tại Tab Sổ Dạy Thay.
   - Vùng dán ảnh thông minh (`#tt-dropzone`): Hỗ trợ **Ctrl + V dán ảnh chụp màn hình**, kéo thả hoặc chọn file ảnh.
   - Nút `✨ AI nhận diện TKB (Gemini Vision)`:
     + Chuyển ảnh sang Base64.
     + Gửi tới proxy backend `api/khbd_gemini.php` (sử dụng model `gemini-2.5-flash` và API key sẵn có của user).
     + AI phân tích ma trận buổi Sáng / Chiều $\times$ Thứ 2 - Thứ 7 $\times$ Tiết $\rightarrow$ Trả về JSON chuẩn.
   - Lưới ma trận Thời khóa biểu tuần trực quan:
     + Hiển thị bảng Sáng & Chiều từ Thứ 2 đến Thứ 7.
     + Các ô có thể click trực tiếp để chỉnh sửa môn và lớp.
     + Nút `Lưu Thời khoá biểu`.
3. **Tính năng Tự động điền tiết thông minh trong Sổ Dạy Thay**:
   - Khi chọn Ngày dạy (VD: 09/09/2026 $\rightarrow$ Thứ Tư), Buổi dạy (Sáng), và chọn "Dạy thay cho giáo viên: Thầy Danh":
     + Hệ thống kiểm tra nếu Thầy Danh đã có TKB:
       - Tự động lấy danh sách tiết của Thầy Danh vào sáng Thứ Tư (Tiết 1: 93, Tiết 2: 93, Tiết 3: 94, Tiết 4: 94).
       - Tự động tick chọn và điền vào các slot tương ứng trong Period Slots Builder!
       - Có nút bấm thủ công: `⚡ Lấy tiết từ TKB giáo viên` để người dùng chủ động nạp lại bất kỳ lúc nào.

---

## Phạm vi thực hiện
1. **Frontend HTML/CSS/JS (`phancongtochuyenmon.html`)**:
   - Thêm HTML Modal Thời khóa biểu giáo viên (`#teacher-timetable-modal`) kèm vùng dán ảnh, nút nhận diện AI và lưới bảng tuần.
   - Thêm nút mở TKB trong thẻ card giáo viên và trong tab Sổ Dạy Thay.
   - Bổ sung cấu hình khung tiết Sáng / Chiều (`morning_periods`, `afternoon_periods`) trong State và giao diện.
   - Xây dựng logic gọi AI Gemini Vision qua `api/khbd_gemini.php` để đọc ảnh TKB.
   - Tích hợp tự động điền slot tiết trong Sổ Dạy Thay dựa theo TKB của GV được thay.
2. **Backend**:
   - Tận dụng `api/khbd_gemini.php` đã có sẵn trong hệ thống (hỗ trợ gọi Gemini với API Key từ session, không cần viết backend mới).

---

## File dự kiến tác động
- `phancongtochuyenmon.html` [SỬA: Cấu hình khung tiết, Modal TKB giáo viên, AI Vision bóc tách TKB, tích hợp tự động điền Sổ Dạy Thay]
- `docs/handoff/PLAN.md` [GHI ĐÈ: Kế hoạch này]
- `docs/handoff/.lock` [GHI: LOCK]

---

## Chi tiết các bước thực hiện cho Coder

### Bước 1: Quản lý Cấu hình Khung tiết Sáng / Chiều
1. Khai báo mặc định trong `defaultState.info`:
   ```javascript
   morning_periods: '1-5',
   afternoon_periods: '1-4',
   ```
2. Viết hàm phân tích dải tiết `parsePeriodsConfig(val, defaultArr)` và `getSessionPeriods(session)`.
3. Cập nhật nhãn `#new-sub-session` thành:
   `Sáng (tiết ${mRange})` và `Chiều (tiết ${aRange})`.
4. Cập nhật `initPeriodSlotsBuilder()`: Lấy danh sách số tiết theo buổi từ `getSessionPeriods(session)` (ví dụ chiều là `[7, 8, 9]`).
5. Thêm nút `⚙️ Khung tiết` trên toolbar Form Sổ Dạy Thay mở modal/dialog nhỏ cho phép sửa nhanh Sáng / Chiều và lưu.

### Bước 2: Xây dựng Modal Thời khóa biểu Giáo viên & Vùng Dán Ảnh
1. Thêm modal `#teacher-timetable-modal`:
   - Header: Chọn giáo viên cần xem/nhập TKB (dropdown danh sách GV).
   - Cột 1 / Phía trên: Vùng Upload & Dán ảnh TKB (`#tt-dropzone`):
     + Lắng nghe sự kiện `paste` trên window hoặc dropzone:
       ```javascript
       window.addEventListener('paste', (e) => {
         const items = e.clipboardData?.items;
         // Kiểm tra nếu có item image, đọc FileReader thành Base64 và hiển thị preview
       });
       ```
     + Nút: `<button id="btn-ai-scan-tt" onclick="scanTimetableWithAI()"><i class="fas fa-wand-magic-sparkles"></i> AI Nhận diện TKB</button>`.
   - Cột 2 / Phía dưới: Bảng Lưới Thời khóa biểu tuần trực quan:
     + Bảng gồm 2 phần: Buổi sáng và Buổi chiều.
     + Cột: Tiết, Thứ 2, Thứ 3, Thứ 4, Thứ 5, Thứ 6, Thứ 7.
     + Mỗi ô cho phép click vào để chỉnh sửa nhanh nội dung (Môn - Lớp).
     + Nút `Lưu Thời khoá biểu`.

### Bước 3: Logic AI Gemini Vision nhận diện Thời khoá biểu
1. Khi bấm `AI Nhận diện TKB`:
   - Lấy chuỗi base64 của ảnh TKB (từ dán ảnh hoặc upload file).
   - Tạo payload gửi đến `api/khbd_gemini.php`:
     ```javascript
     const prompt = `Bạn là trợ lý AI chuyên nhận diện bảng Thời khóa biểu giáo viên THCS tại Việt Nam.
Hãy đọc ảnh Thời khóa biểu đính kèm và trích xuất thành định dạng JSON chuẩn.
Cấu trúc JSON yêu cầu:
{
  "teacher_name": "Tên giáo viên trong ảnh",
  "school": "Tên trường",
  "school_year": "Năm học",
  "semester": "Học kỳ",
  "morning": {
    "2": { "1": "Toán - 63", "2": "...", ... },
    "3": { ... },
    "4": { ... },
    "5": { ... },
    "6": { ... },
    "7": { ... }
  },
  "afternoon": {
    "2": { ... },
    ...
  }
}
Quy tắc:
- Key của các ngày: "2" (Thứ 2), "3" (Thứ 3), "4" (Thứ 4), "5" (Thứ 5), "6" (Thứ 6), "7" (Thứ 7).
- Key của các tiết là số tiết (ví dụ: "1", "2", "3", "4", "5", hoặc "7", "8", "9").
- Giá trị mỗi tiết là chuỗi định dạng "TênMôn - TênLớp" (ví dụ: "Toán - 63", "HĐTN - 64"), nếu tiết trống thì bỏ qua hoặc để rỗng "".
- Chỉ trả về duy nhất khối JSON hợp lệ, không bọc thêm văn bản giải thích.`;
     ```
   - Gọi `fetch('api/khbd_gemini.php', { method: 'POST', body: JSON.stringify({ model: 'gemini-2.5-flash', payload: { contents: [ ... ] } }) })`.
   - Nhận kết quả JSON, bóc tách và tự động điền vào Lưới ma trận TKB trên Modal để người dùng kiểm tra.

### Bước 4: Tích hợp TKB vào Sổ Dạy Thay
1. Trong Tab 2 (Sổ Dạy Thay):
   - Thêm nút `⚡ Lấy tiết từ TKB` cạnh khu vực phân bổ tiết.
   - Khi người dùng thay đổi Ngày dạy (`#new-sub-date`) hoặc Buổi dạy (`#new-sub-session`) hoặc GV được thay (`#new-sub-for-teacher`):
     - Hàm `autoSuggestSlotsFromTimetable()` kiểm tra:
       + Lấy thứ trong tuần từ Ngày dạy (2 đến 7).
       + Lấy giáo viên từ `#new-sub-for-teacher`.
       + Tra trong `teacher.timetable[session][dayOfWeek]`:
       + Nếu có các tiết dạy: Tự động tick chọn các slot tiết tương ứng, điền đúng Lớp học và Môn học!
       + Hiển thị thông báo toast: *"Đã nạp tự động X tiết từ TKB của giáo viên [Tên GV]"*.

---

## Cách kiểm thử
1. **Kiểm tra Cấu hình Khung tiết**:
   - Đổi khung tiết: Sáng `1-4`, Chiều `7-9`.
   - Kiểm tra Tab Sổ Dạy Thay hiển thị đúng các slot: Sáng `1 - 4`, Chiều `7 - 9`.
2. **Kiểm tra Nhập TKB và Dán ảnh (Ctrl+V)**:
   - Mở modal TKB của Thầy Danh.
   - Dán ảnh chụp màn hình TKB (Ctrl+V) $\rightarrow$ Preview ảnh xuất hiện.
   - Bấm `AI Nhận diện TKB` $\rightarrow$ Sau vài giây, bảng ma trận tuần hiển thị đúng các tiết của Thầy Danh (như Thứ 3 tiết 1: Toán 63, Thứ 4 tiết 1-2: Toán 93, tiết 3-4: Toán 94...).
   - Bấm `Lưu Thời khoá biểu`.
3. **Kiểm tra Tự động điền tiết trong Sổ Dạy Thay**:
   - Sang Tab Sổ Dạy Thay.
   - Chọn ngày Thứ Tư, Buổi Sáng, chọn Dạy thay cho: Thầy Danh.
   - Quan sát lưới tiết: Hệ thống tự động tick chọn Tiết 1 (93), Tiết 2 (93), Tiết 3 (94), Tiết 4 (94), tổng số tiết tự tính là 4 tiết!

---

## Tiêu chí nghiệm thu
1. Người dùng tùy chỉnh được khung tiết Sáng / Chiều tự do (ví dụ: Sáng 1-4, Chiều 7-9).
2. Tích hợp giao diện quản lý Thời khóa biểu cá nhân cho từng Giáo viên.
3. Hỗ trợ dán ảnh (Ctrl+V) hoặc upload ảnh TKB và dùng AI Gemini Vision bóc tách tự động chính xác lịch dạy tuần.
4. Sổ Dạy Thay tự động gợi ý / điền nhanh các tiết học cần dạy thay dựa trên TKB của giáo viên được thay.