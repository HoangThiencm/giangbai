# PLAN: Chức năng nhập Thời khóa biểu từ Word (.docx), Đối chiếu Giáo viên & Nạp TKB Tổ chuyên môn

**Ngày lập:** 2026-11-17  
**Mục tiêu:** 
1. Giải quyết triệt để vấn đề nhận diện sai tiết học và nhầm lẫn giáo viên (đặc biệt các tên gần giống nhau như `Thiên` vs `Thiện`) khi nhập thời khóa biểu trong `phancongtochuyenmon.html`.
2. Hỗ trợ import trực tiếp file Word (.docx) chứa TKB toàn trường (hoặc nhiều giáo viên).
3. Hệ thống hóa quy trình:
   - **Bước 1:** Bóc tách dữ liệu bảng từ file Word (tận dụng thư viện `mammoth.js` sẵn có).
   - **Bước 2:** Đối chiếu danh sách giáo viên trong Word với CSDL giáo viên của tổ chuyên môn (phân biệt tuyệt đối dấu tiếng Việt, hỗ trợ lưu bí danh `alias`).
   - **Bước 3:** Cho phép tổ trưởng tick chọn các giáo viên thuộc tổ của mình để xử lý.
   - **Bước 4 (Chế độ kép - Dual Engine):**
     + *Chế độ 1 (Khuyên dùng - Nạp trực tiếp 100% chuẩn):* Thuật toán Client-side bóc tách trực tiếp từ cấu trúc hàng/cột của Word sang JSON TKB. Không lo trượt hàng, không tốn token AI, xử lý tức thì.
     + *Chế độ 2 (Xuất Prompt AI + Nạp JSON):* Sinh prompt chuẩn hóa kèm dữ liệu bảng rút gọn để người dùng dán vào ChatGPT / Gemini Web (hoặc bấm gọi Gemini API), sau đó có ô dán JSON kết quả để hệ thống nạp lại.
   - **Bước 5:** Kiểm tra quy tắc & xung đột (tiết vượt dải, trùng tiết, lớp không tồn tại) trước khi lưu vào CSDL.

---

## 1. Khảo sát hiện trạng & Phân tích cấu trúc dữ liệu

### 1.1. Hiện trạng trong `phancongtochuyenmon.html`
- Thẻ `<details class="tt-import-card" id="tt-import-details">` (dòng ~1999) hiện chỉ có khu vực kéo thả ảnh (`#tt-dropzone`) và nút gọi Gemini Vision `scanTimetableWithAI()` (dòng ~7426).
- Nhược điểm của nhận diện qua ảnh:
  + Các bảng TKB không in số thứ tự tiết ở mép trái khiến AI dễ đếm nhầm hàng, dồn môn ở hàng dưới lên hàng trên bị trống.
  + Ảnh chụp mờ hoặc vỡ nét làm sai lệch tên lớp (nhầm `63` thành `68`, `94` thành `91`...).
  + Nhận diện từng ảnh giáo viên đơn lẻ gây mất thời gian khi tổ có 8–15 giáo viên.
- Thư viện sẵn có:
  + `mammoth.browser.min.js` (dòng 19) đã được nhúng sẵn trong trang.
- Schema lưu trữ TKB trong hệ thống:
  ```json
  {
    "school_year": "2026 - 2027",
    "semester": "Học kỳ 1",
    "morning": {
      "2": { "1": { "subject": "Toán", "class_name": "64" }, "2": null },
      "3": { ... },
      "4": { ... },
      "5": { ... },
      "6": { ... },
      "7": { ... }
    },
    "afternoon": {
      "2": { "1": null, "2": { "subject": "Toán", "class_name": "74" } },
      ...
    }
  }
  ```

### 1.2. Phân tích cấu trúc bảng Word thực tế (THCS Trần Phú - TKB Số 11)
Từ dữ liệu mẫu Thầy/Cô cung cấp:
- Mỗi giáo viên là một bảng riêng biệt (`<table>`).
- Phần Header bảng:
  + Chứa tiêu đề trường, năm học, học kỳ, số hiệu TKB (`Số 11`).
  + Tên giáo viên xuất hiện ở dòng 2: `Giáo viên Danh`, `Giáo viên Ánh`, `Giáo viên Thiên`, `Giáo viên Thiện`...
  + Ngày áp dụng: `(Thực hiện từ ngày 16 tháng 11 năm 2026)`.
- Khối `Buổi sáng`:
  + Dòng tiêu đề các thứ: `THỨ 2`, `THỨ 3`, `THỨ 4`, `THỨ 5`, `THỨ 6`, `THỨ 7` (mỗi thứ có thể gồm 1 hoặc 2 cột do colspan gộp ô).
  + Kế tiếp là đúng **5 hàng kẻ ngang vật lý**, tương ứng chính xác:
    * Hàng 1 -> Tiết 1
    * Hàng 2 -> Tiết 2
    * Hàng 3 -> Tiết 3
    * Hàng 4 -> Tiết 4
    * Hàng 5 -> Tiết 5
- Khối `Buổi chiều`:
  + Dòng tiêu đề các thứ: `THỨ 2`, `THỨ 3`, `THỨ 4`, `THỨ 5`, `THỨ 6`, `THỨ 7`.
  + Kế tiếp là đúng **5 hàng kẻ ngang vật lý**, tương ứng:
    * Hàng 1 -> Tiết 1 chiều (hoặc Tiết 6 theo cấu hình trường)
    * Hàng 2 -> Tiết 2 chiều (hoặc Tiết 7)
    * Hàng 3 -> Tiết 3 chiều (hoặc Tiết 8)
    * Hàng 4 -> Tiết 4 chiều (hoặc Tiết 9)
    * Hàng 5 -> Tiết 5 chiều (hoặc Tiết 10)
- Tọa độ hàng vật lý trong Word là **bất biến**, do đó bóc tách bằng DOM / code xác định 100% đúng tiết, loại bỏ hoàn toàn rủi ro AI bị hallucination trượt tiết.

---

## 2. Kiến trúc giải pháp (Architecture Design)

```
[ File Word .docx TKB ]
         │
         ▼
[ mammoth.js Client Parser ] ─── Bóc tách HTML Tables
         │
         ▼
[ Extract Teacher Tables ] ───── Thu thập danh sách giáo viên & ma trận các ô (Thứ, Tiết)
         │
         ▼
[ Teacher Matching Engine ] ──── Đối chiếu với state.teachers (Bảo toàn dấu TV: Thiên ≠ Thiện)
         │                       + Kiểm tra Aliases (Bí danh đã lưu trong localStorage)
         │
         ▼
[ Giao diện Modal Đối chiếu & Chọn Giáo viên ]
   ├── Bảng danh sách: Tên Word | Gợi ý CSDL | Trạng thái (Khớp / Chọn / Thêm mới) | Checkbox
   ├── Bộ lọc nhanh: [Chọn GV trong tổ] [Chọn tất cả] [Bỏ chọn]
   ├── Nút: [Lưu bí danh]
   ├── TÙY CHỌN 1: [⚡ Nạp TKB trực tiếp vào hệ thống (Chính xác 100%)]
   └── TÙY CHỌN 2: [🤖 Xuất Prompt cho ChatGPT/Gemini] ──► [Ô dán JSON kết quả & Nạp lại]
         │
         ▼
[ Conflict & Rule Validator ] ── Kiểm tra dải tiết, trùng lặp phân công, tên lớp chuẩn
         │
         ▼
[ Apply to state.teachers ] ──── Cập nhật TKB, đồng bộ phân công môn, lưu DB (saveToDB)
```

---

## 3. Chi tiết thực hiện (Implementation Specs)

### 3.1. Giao diện người dùng trong `phancongtochuyenmon.html`
1. **Thêm Card nhập Word trong `#tt-import-details`:**
   - Đặt tab chuyển đổi hoặc hiển thị song song 2 lựa chọn:
     + Tab 1: `Nhập ảnh TKB (JPG/PNG)` (giữ nguyên luồng cũ).
     + Tab 2: `Nhập file Word TKB (.docx)` (chức năng mới).
   - Vùng kéo thả file Word: `#tt-word-dropzone`, chấp nhận `.docx`.
2. **Modal đối chiếu & duyệt TKB Word (`#modal-word-tkb`):**
   - Tiêu đề: *Nhận diện Thời khóa biểu từ Word - Đối chiếu Giáo viên*.
   - Thanh công cụ phía trên:
     + Hiển thị: Tổng số GV tìm thấy trong file Word (VD: 50 GV), số GV đã khớp với tổ (VD: 8 GV).
     + Nút: `Chỉ chọn GV thuộc tổ`, `Chọn tất cả`, `Bỏ chọn`.
     + Tuần áp dụng TKB (dropdown kế thừa từ giao diện chính).
   - Bảng danh sách đối chiếu:
     | Chọn | Tên trong Word | Giáo viên trong CSDL | Trạng thái | Thao tác / Bí danh |
     |:---:|:---|:---|:---:|:---|
     | [x] | Giáo viên Thiên | Hoàng Tấn Thiên | Khớp chính xác | [Đã nhớ bí danh] |
     | [ ] | Giáo viên Thiện | Nguyễn Văn Thiện | Không thuộc tổ | Dropdown chọn lại |
     | [x] | Giáo viên Ánh | Trần Ngọc Ánh | Khớp chính xác | - |
   - Nút hành động ở chân modal:
     + Nút 1 (Chính): `⚡ Nạp trực tiếp TKB các GV đã chọn` (màu xanh lá/indigo nổi bật).
     + Nút 2: `🤖 Xuất Prompt cho ChatGPT / Gemini`.
     + Nút 3: `📋 Nạp từ mã JSON AI` (mở ô dán JSON).

### 3.2. Thuật toán phân tích bảng Word (`parseWordTimetableTables`)
1. Dùng `mammoth.convertToHtml({ arrayBuffer })` để lấy chuỗi HTML.
2. Dùng DOMParser phân tích các thẻ `<table>`:
   - Lấy tên giáo viên: Quét 3 hàng đầu của table, regex `/(?:Giáo viên|GV|Thầy|Cô)\s+([^\n\r<–—]+)/i`.
   - Tìm chỉ số cột cho từng Thứ:
     + Quét hàng chứa `THỨ 2`, `THỨ 3`... Đếm colspan để xác định chỉ số cột bắt đầu của mỗi thứ (Thứ 2 = colIdx2, Thứ 3 = colIdx3...).
   - Quét khối `Buổi sáng`:
     + Xác định hàng bắt đầu sau chữ `Buổi sáng`.
     + Duyệt 5 hàng kế tiếp: Hàng `r = 0..4` tương ứng Tiết `p = r + 1` (Tiết 1..5).
     + Lấy nội dung ô tại cột của từng Thứ, chuẩn hóa chuỗi `Môn - Lớp`.
   - Quét khối `Buổi chiều`:
     + Xác định hàng bắt đầu sau chữ `Buổi chiều`.
     + Duyệt 5 hàng kế tiếp: Hàng `r = 0..4` tương ứng Tiết `p = r + 1` (hoặc `r + 6` nếu cấu hình trường đánh số 6..10).
3. Đóng gói thành cấu trúc trung gian `rawExtractedTeachers`:
   ```js
   {
     rawName: "Thiên",
     rawLabel: "Giáo viên Thiên",
     tableIndex: 30,
     morning: { "2": {}, "3": {}, "4": { "1": "Toán - 92", "2": "Tin - 61", "3": "Toán - 61", "4": "Toán - 61" }, ... },
     afternoon: { "3": { "2": "Toán - 92", "3": "Toán - 61", "4": "Toán - 91" }, ... }
   }
   ```

### 3.3. Thuật toán đối chiếu Giáo viên & Quản lý Bí danh (`matchWordTeachersWithDb`)
1. **Quy tắc phân biệt nghiêm ngặt:**
   - **Tuyệt đối không bỏ dấu tiếng Việt khi so khớp tên**: `Thiên` KHÁC `Thiện`, `Hải` KHÁC `Hà`, `Sanh` KHÁC `Sáng`.
   - Chuẩn hóa: Cắt bỏ tiền tố `Giáo viên`, `GV`, `Thầy`, `Cô`, khoảng trắng thừa, chuyển về chữ thường có dấu (`thiên`, `thiện`).
2. **Nguồn tra cứu bí danh (`aliasMap`):**
   - Đọc từ `localStorage.getItem('tkb_word_aliases')` (object dạng `{ "thiên": "gv_thien_id", "gv ánh": "gv_anh_id" }`).
   - Nếu nhãn Word có trong `aliasMap`, lập tức ánh xạ vào đúng `teacher.id` tương ứng.
3. **So khớp với `state.teachers`:**
   - Nếu tên họ chuẩn trong CSDL có từ cuối trùng với tên trong Word (ví dụ `Hoàng Tấn Thiên` -> từ cuối là `Thiên`):
     * Nếu trong danh sách `state.teachers` chỉ có DUY NHẤT 1 người có tên này -> Đánh dấu `exact_match`.
     * Nếu có nhiều người trùng tên (ví dụ 2 người tên `Hương`): Yêu cầu người dùng chọn từ dropdown.
   - Nếu trong `state.teachers` không tìm thấy: Đánh dấu `not_found` (mặc định bỏ tick).
4. **Lưu bí danh:**
   - Khi người dùng chọn giáo viên từ dropdown và bấm `Lưu bí danh`, hệ thống lưu cặp `(nhãn Word -> teacher.id)` vào `localStorage` để các lần nhập sau tự động nhận diện chính xác 100%.

### 3.4. Chế độ 1: Nạp trực tiếp từ dữ liệu Word (Engine A - Direct)
- Khi bấm `⚡ Nạp trực tiếp TKB các GV đã chọn`:
  1. Duyệt qua các giáo viên được tick chọn.
  2. Map dữ liệu `morning` và `afternoon` sang schema `state.teachers[id].timetable` (hoặc `timetable_by_week[week]`).
  3. Gọi hàm `parseTimetableCell()` và `matchClassFromTimetable()` sẵn có để khớp chuẩn mã lớp (`92` -> `9/2` hoặc `9A2` tùy danh sách lớp của trường).
  4. Thực hiện validate quy tắc (xem mục 3.6).
  5. Cập nhật vào `state.teachers`, tự động đồng bộ phân công môn dạy (`applyTimetableToAssignments`) nếu có tùy chọn, và gọi `persistAndSaveTimetableLocal()`.
  6. Hiển thị thông báo tổng kết: `Đã nạp thành công TKB cho X giáo viên, tổng cộng Y tiết học.`

### 3.5. Chế độ 2: Xuất Prompt cho AI & Nạp JSON (Engine B - AI Assistant)
- Khi Thầy/Cô muốn dùng ChatGPT/Gemini web hoặc file Word có định dạng đặc thù:
  1. Hệ thống xuất prompt có cấu trúc:
     ```markdown
     Bạn là bộ nhận diện Thời khóa biểu chuyên nghiệp.
     Đọc dữ liệu bảng thời khóa biểu đính kèm. CHỈ trích xuất thời khóa biểu cho danh sách giáo viên sau:
     - Teacher ID: [ID_1], Họ tên: [Hoàng Tấn Thiên], Tên trong bảng: [Giáo viên Thiên]
     - Teacher ID: [ID_2], Họ tên: [Trần Ngọc Ánh], Tên trong bảng: [Giáo viên Ánh]

     QUY TẮC BẮT BUỘC:
     - Không nhận diện giáo viên ngoài danh sách trên.
     - Phân biệt tuyệt đối chữ có dấu: "Thiên" khác "Thiện".
     - Giữ nguyên ô trống, không dồn tiết.
     - Trả về DUY NHẤT chuỗi JSON hợp lệ theo định dạng:
     [
       {
         "teacher_id": "...",
         "teacher_name": "...",
         "morning": {
           "2": { "1": "Toán - 64", "2": null },
           ...
         },
         "afternoon": { ... }
       }
     ]

     DỮ LIỆU BẢNG TKB NGUỒN CỦA CÁC GIÁO VIÊN TRÊN:
     [Dữ liệu text rút gọn của từng bảng GV đã chọn]
     ```
  2. Nút `Sao chép Prompt` để người dùng copy 1 chạm dán vào ChatGPT / Gemini.
  3. Ô nhập `Dán JSON phản hồi từ AI vào đây` + Nút `Nạp JSON vào hệ thống`.
  4. Parser kiểm tra JSON schema, map ngược vào `state.teachers` tương tự Engine A.

### 3.6. Bộ kiểm tra quy tắc & Xung đột (Validator)
- **Kiểm tra tiết:** Cảnh báo nếu số tiết nằm ngoài khung giờ quy định của trường (ví dụ sáng có tiết 6 hoặc chiều có tiết 11).
- **Kiểm tra trùng lịch:** Cảnh báo nếu cùng 1 thứ, 1 tiết, có 2 giáo viên cùng dạy 1 lớp.
- **Kiểm tra lớp học:** Cảnh báo nếu tên lớp không tìm thấy trong danh mục `state.classes`.
- Danh sách cảnh báo hiển thị rõ ràng trên màn hình kết quả để tổ trưởng duyệt.

---

## 4. Danh sách tệp cần chỉnh sửa
- **`phancongtochuyenmon.html`:**
  1. Thêm HTML cho nút/khu vực tải Word `.docx` trong `#tt-import-details`.
  2. Thêm HTML Modal `#modal-word-tkb` (gồm bảng đối chiếu giáo viên, nút nạp trực tiếp, nút xuất prompt, ô dán JSON).
  3. Thêm CSS chuyên biệt cho modal đối chiếu, badge trạng thái, bảng preview TKB Word.
  4. Thêm JavaScript:
     - `handleTimetableWordFile(file)`
     - `parseWordTimetableHtml(html)`
     - `matchWordTeachersWithDb(extracted)`
     - `renderWordTeacherMatchModal()`
     - `saveWordTeacherAliases()`
     - `applyWordTimetableDirectly()`
     - `generateWordTimetablePrompt()`
     - `importTimetableFromJson(jsonText)`
     - `validateTimetableRules(entries)`

---

## 5. Kịch bản kiểm thử (Test Cases)

1. **Test Case 1: Tải file Word mẫu của trường THCS Trần Phú**
   - File chứa 50 giáo viên.
   - Xác nhận `mammoth.js` đọc được 50 bảng mà không bị crash trình duyệt.
2. **Test Case 2: Độ chính xác phân biệt tên có dấu**
   - Kiểm tra `Giáo viên Thiên` (dạy Toán - Tin) và `Giáo viên Thiện` (dạy Thể dục).
   - Xác nhận hệ thống phân tách thành 2 bản ghi riêng biệt, không gộp và không gán nhầm TKB môn Thể dục cho Thầy Thiên.
3. **Test Case 3: Nạp trực tiếp TKB cho Tổ Toán - Tin**
   - Tick chọn: Thiên, Danh, Ánh, Bình, Hải, Tùng, Sáng, Thảo.
   - Bấm `⚡ Nạp trực tiếp TKB các GV đã chọn`.
   - Xác nhận Thầy Thiên có đúng:
     * Thứ 4 sáng: Tiết 1 (Toán 92), Tiết 2 (Tin 61), Tiết 3 (Toán 61), Tiết 4 (Toán 61).
     * Thứ 5 sáng: Tiết 3 (Toán 91), Tiết 4 (Toán 92).
     * Thứ 6 sáng: Tiết 1 (Toán 91), Tiết 2 (Toán 91), Tiết 3 (Toán 92), Tiết 4 (Toán 61).
     * Thứ 3 chiều: Tiết 2 (Toán 92), Tiết 3 (Toán 61), Tiết 4 (Toán 91).
   - Kiểm tra các tiết trống (như Thứ 2 sáng) không bị dồn tiết.
4. **Test Case 4: Nhớ bí danh (Alias persistence)**
   - Gán `Giáo viên Thiên` -> `Hoàng Tấn Thiên` và bấm lưu.
   - F5 tải lại trang, nạp lại file Word -> Tự động khớp xanh và tick chọn Thầy Thiên ngay lập tức.
5. **Test Case 5: Xuất Prompt & Nạp JSON AI**
   - Bấm `Xuất Prompt`, copy prompt sinh ra.
   - Dán chuỗi JSON mẫu vào ô nạp JSON -> Xác nhận hệ thống nạp đúng và hiển thị số tiết tương ứng.
