# PLAN: Nâng cấp độ chính xác nhận diện Thời khóa biểu (TKB) AI trong Quản lý Tổ chuyên môn

## 1. Hiện trạng & Phân tích nguyên nhân gốc rễ

Người dùng phản ánh:
> *"phần nhận diện thời khoá biểu ở quản lý tổ chuyên môn nó không chính xác lắm. Rất dễ bị nhận nhầm tiết, nhầm lớp. Biểu mẫu gốc của thời khoá biểu nhà trường gửi như ảnh"*

### Phân tích biểu mẫu gốc từ ảnh thực tế (`Giáo viên Danh`, THCS Trần Phú):
1. **Cấu trúc bảng TKB:**
   - Gồm 2 bảng: **Buổi sáng** và **Buổi chiều**.
   - Cột: Gồm 6 cột thứ: `THỨ 2 | THỨ 3 | THỨ 4 | THỨ 5 | THỨ 6 | THỨ 7`.
   - **Đặc điểm mấu chốt:** Bảng **HOÀN TOÀN KHÔNG CÓ CỘT IN SỐ TIẾT** (cột 1, 2, 3, 4, 5 ở ngoài cùng bên trái bị lược bỏ).
   - Buổi sáng có đúng **5 hàng kẻ ngang vật lý (rows)** tương ứng với 5 tiết (Tiết 1, 2, 3, 4, 5).
   - Buổi chiều có 5 hàng kẻ ngang vật lý.

2. **Dữ liệu phân bố và các ô trống đặc thù:**
   - **Thứ 2:** Hàng 1 để TRỐNG. Hàng 2: `Toán - 93`, Hàng 3: `Toán - 64`, Hàng 4: `Toán - 63`, Hàng 5: `Toán - 94`.
   - **Thứ 3:** Hàng 1: `Toán - 93`, Hàng 2: `Toán - 64`, Hàng 3: `Toán - 64`, Hàng 4: `Toán - 63`, Hàng 5 để TRỐNG.
   - **Thứ 4:** Hàng 1: `Toán - 93`, Hàng 2: `Toán - 93`, Hàng 3: `Toán - 94`, Hàng 4: `Toán - 94`, Hàng 5 để TRỐNG.
   - **Thứ 5:** Cả 5 hàng đều để TRỐNG.
   - **Thứ 6:** Hàng 1: `Toán - 94`, Hàng 2: `Toán - 63`, Hàng 3: `Toán - 63`, Hàng 4 để TRỐNG, Hàng 5: `Toán - 64`.
   - **Thứ 7:** Cả 5 hàng đều để TRỐNG.

---

### Các nguyên nhân gốc rễ (Root Causes):

#### Nguyên nhân 1: Nhận nhầm tiết do hiện tượng trôi hàng (Row Slip) khi có ô trống
- Vì bảng không in cột số tiết, khi thị giác máy (Vision AI) đọc cột **Thứ 2**:
  - Hàng 1 trống, môn đầu tiên xuất hiện là `Toán - 93` ở Hàng 2.
  - Nếu AI duyệt dọc theo cột hoặc không neo chặt tọa độ hàng ngang 2D, AI sẽ coi môn đầu tiên tìm thấy là Tiết 1 $\rightarrow$ **Gán sai `Toán - 93` vào Tiết 1 thay vì Tiết 2!**
- Tương tự ở cột **Thứ 6**:
  - Hàng 4 trống, Hàng 5 có môn `Toán - 64`.
  - AI đọc thấy 4 môn ở Thứ 6 sẽ tự động dồn vào Tiết 1, 2, 3, 4 và để Tiết 5 trống $\rightarrow$ **Gán sai `Toán - 64` vào Tiết 4 thay vì Tiết 5!**
- Lời nhắc (Prompt) hiện tại trong `scanTimetableWithAI()` tuy có nhắc đếm hàng nhưng:
  - Chưa hướng dẫn AI quét theo ma trận 2D ngang qua toàn bộ bảng (Row Matrix Sweep).
  - Chưa nhấn mạnh nguyên tắc bất di bất dịch về **Bảo toàn ô trống (Blank Cell Preservation)**: Tuyệt đối không được dồn tiết lên khi hàng trên trống.
  - Chứa câu lệnh cứng nhắc gây nhiễu/ảo giác (ví dụ dòng 7337: *"Nếu Thứ 3 có môn ở Hàng 3 và Hàng 4 thì BẮT BUỘC là Tiết 8 và Tiết 9!"*).

#### Nguyên nhân 2: Nhận nhầm lớp do định dạng viết tắt và thiếu so khớp thông minh (Class Alias Mismatch)
- Trong các phần mềm xếp TKB trường học (SmartSchool, TKB, FET, Viettel, vnEdu...), mã lớp thường viết tắt 2 chữ số:
  - `93` = Lớp 9/3 (hoặc 9A3, 9C)
  - `64` = Lớp 6/4 (hoặc 6A4, 6D)
  - `63` = Lớp 6/3 (hoặc 6A3, 6C)
  - `94` = Lớp 9/4 (hoặc 9A4, 9D)
- Trong khi đó, trong cơ sở dữ liệu Tổ chuyên môn (`state.classes`), người dùng thường khai báo lớp có dấu gạch chéo (`6/3, 6/4, 9/3, 9/4`) hoặc có chữ cái (`6A3, 6A4, 9A3, 9A4`).
- Hiện tại trong `phancongtochuyenmon.html`:
  - Hàm `normalizeClassNameFromTimetable` chỉ xử lý thô:
    ```javascript
    function normalizeClassNameFromTimetable(name) {
        return String(name || '').replace(/\s+/g, '').replace(/\//g, '').trim();
    }
    ```
    Hàm này xóa sạch dấu gạch chéo (`/`), làm mất định dạng chuẩn của trường.
  - Hệ thống **hoàn toàn không có hàm so khớp lớp thông minh** (`matchClassFromTimetable`) đối chiếu với `state.classes`.
  - Kết quả: Khi đọc ra `93`, hệ thống kiểm tra `!state.classes.includes('93')` thấy không có, liền tự tiện tạo thêm một lớp mới tên `'93'` làm rác danh sách lớp và không liên kết được với lớp `'9/3'` đã có trong phân công!
  - Ngoài ra, hai chữ số `6` và `9` đối xứng nhau, `3` và `4` trong font chữ in bảng biểu dễ bị nhầm lẫn nếu không có context danh sách lớp hiện có của trường để neo chặn (constrain).

#### Nguyên nhân 3: Nén ảnh JPEG làm mờ và gây nhiễu hạt ký tự số
- Trong hàm `compressTimetableImage()`:
  ```javascript
  resolve(canvas.toDataURL('image/jpeg', 0.85));
  ```
  Ảnh người dùng tải lên có kích thước 862x595 (rất nhẹ, chỉ khoảng 40KB). Việc vẽ lên canvas rồi nén sang JPEG 0.85 sinh ra hiện tượng nhiễu khối (ringing artifacts) xung quanh các con số nhỏ nét mảnh như `93, 63, 64, 94`, khiến mô hình Vision nhận diện nhầm số 9 thành số 6 hoặc ngược lại.
  Với ảnh chụp bảng biểu TKB có dung lượng vừa phải (< 3MB), việc giữ nguyên chất lượng cao lossless (PNG) hoặc JPEG 0.95+ giúp độ sắc nét của chữ số đạt tối đa.

#### Nguyên nhân 4: Cơ chế dịch tiết cứng nhắc trong `alignSessionPeriods()`
- Đoạn code `vnEduPlusOne` (dòng 7383–7395) can thiệp dịch lùi/tiến tiết dựa trên các giả định cứng, đôi khi làm dịch chuyển sai lệch cả những tiết mà AI đã nhận diện đúng.

---

## 2. Mục tiêu kỹ thuật

1. **Giữ nguyên độ sắc nét ảnh khi đưa vào AI:**
   - Điều chỉnh `compressTimetableImage()`: Nếu ảnh dưới 2MB và kích thước chiều rộng/dài <= 2048px, không ép nén JPEG 0.85 gây vỡ chữ số; giữ nguyên PNG hoặc JPEG chất lượng cao (0.95).

2. **Nâng cấp Prompt AI nhận diện TKB với đầy đủ ngữ cảnh & thuật toán ma trận 2D:**
   - **Bơm ngữ cảnh thực tế của tổ chuyên môn vào prompt:**
     + Truyền danh sách lớp của trường (`state.classes`): ví dụ `[6/1, 6/2, 6/3, 6/4, 9/1, 9/2, 9/3, 9/4]`.
     + Truyền danh sách môn học (`state.subjects`).
     + Truyền tên giáo viên đang chọn (`teacher.name`).
   - **Quy tắc ma trận 2D (Matrix Grid Sweep) chống dồn hàng / lệch tiết:**
     + Bảng buổi sáng có đúng 5 hàng vật lý (Row 1..5) ứng với Tiết 1..5. Bảng buổi chiều ứng với khung tiết buổi chiều.
     + Nguyên tắc bảo toàn ô trống: Đọc theo từng hàng ngang từ trái sang phải qua các cột Thứ. Nếu ô Hàng 1 Thứ 2 trống $\rightarrow$ Tiết 1 là rỗng, cấm dồn môn ở Hàng 2 lên Tiết 1. Nếu ô Hàng 4 Thứ 6 trống $\rightarrow$ Tiết 4 là rỗng, Hàng 5 là Tiết 5.
   - **Quy tắc giải mã mã lớp viết tắt:**
     + Giải thích rõ quy ước 2 chữ số (`93` là 9/3 hoặc 9A3, `64` là 6/4 hoặc 6A4...). Yêu cầu AI đối chiếu với danh sách lớp được cung cấp để trả về đúng tên lớp chuẩn.
   - Loại bỏ các câu lệnh hardcode gây nhiễu ("Nếu Thứ 3 có môn...").

3. **Xây dựng hàm so khớp lớp thông minh (`matchClassFromTimetable`):**
   - Ánh xạ tự động và 2 chiều giữa các định dạng tên lớp phổ biến tại Việt Nam:
     + Dạng 2 số: `93` $\leftrightarrow$ `9/3` $\leftrightarrow$ `9.3` $\leftrightarrow$ `9-3` $\leftrightarrow$ `9A3`.
     + Dạng lớp chữ cái: `64` $\leftrightarrow$ `6/4` $\leftrightarrow$ `6D` (với A=1, B=2, C=3, D=4).
   - Nếu tìm thấy lớp tương ứng trong `state.classes`, luôn ưu tiên sử dụng tên lớp chuẩn đã có trong hệ thống, không tạo thêm lớp trùng lặp rác.

4. **Tinh chỉnh `alignSessionPeriods()` và giao diện hiển thị:**
   - Đảm bảo các tiết sáng (1..5) giữ nguyên đúng vị trí hàng.
   - Hiển thị badge thống kê rõ ràng sau khi AI đọc xong (Số tiết sáng, Số tiết chiều, Danh sách lớp đã nhận diện).

---

## 3. Kế hoạch sửa đổi chi tiết từng file

### File 1: `phancongtochuyenmon.html`

#### 1. Cải tiến `compressTimetableImage(dataUrl)` (khoảng dòng 7157):
- Kiểm tra kích thước và định dạng ảnh gốc:
  - Nếu ảnh là PNG hoặc JPEG có kích thước width <= 2048px và height <= 2048px, không downscale quá mức.
  - Xuất canvas dạng PNG (đối với ảnh chụp sắc nét) hoặc JPEG với quality 0.95 thay vì 0.85 để giữ nguyên nét mảnh của chữ số 6, 9, 3, 4.

#### 2. Xây dựng hàm `matchClassFromTimetable(rawClass, existingClasses)` và nâng cấp `normalizeClassNameFromTimetable`:
- Viết hàm `matchClassFromTimetable(rawClass, existingClasses)`:
  1. Chuẩn hóa chuỗi thô: bỏ khoảng trắng thừa.
  2. Tìm kiếm chính xác (exact match): Nếu `existingClasses` có chứa `rawClass` $\rightarrow$ trả về ngay.
  3. Tìm kiếm theo quy tắc viết tắt 2 chữ số (Khối + Lớp):
     - Biểu thức chính quy: `^([6-9])(\d)$` (ví dụ `93` $\rightarrow$ Khối 9, Lớp 3).
     - Thử tìm trong `existingClasses` các dạng:
       - `${grade}/${section}` (ví dụ `9/3`)
       - `${grade}.${section}` (ví dụ `9.3`)
       - `${grade}-${section}` (ví dụ `9-3`)
       - `${grade}A${section}` (ví dụ `9A3`)
       - `${grade}${char}` (với section 1='A', 2='B', 3='C', 4='D', 5='E'... ví dụ 93 $\rightarrow$ 9C).
  4. Tìm kiếm ngược lại (từ `9/3` sang `93` hoặc `9A3`):
     - Biểu thức chính quy: `^([6-9])[\/.-](\d)$` $\rightarrow$ thử tìm `93` hoặc `9A3`.
  5. Nếu không khớp với lớp nào trong `existingClasses`, trả về chuỗi đã chuẩn hóa (giữ nguyên nếu có dấu `/`).

#### 3. Nâng cấp `scanTimetableWithAI()` (khoảng dòng 7275–7350):
- Lấy thông tin ngữ cảnh hiện tại:
  ```javascript
  const teacher = (state.teachers || []).find(t => String(t.id) === String(selectedTimetableTeacherId));
  const currentClasses = (state.classes || []).slice();
  const currentSubjects = (state.subjects || []).map(s => s.name);
  ```
- Cập nhật Prompt gửi tới Gemini:
  - Nêu rõ tên giáo viên cần quét: `teacher?.name || ''`.
  - Cung cấp danh sách lớp học hiện có của trường: `JSON.stringify(currentClasses)`.
  - Cung cấp danh sách môn học: `currentSubjects.join(', ')`.
  - Mô tả quy tắc ma trận 2D và nguyên tắc bảo toàn ô trống:
    ```
    - BẢNG THỜI KHÓA BIỂU KHÔNG IN CỘT SỐ TIẾT:
      + Buổi sáng có đúng 5 hàng kẻ ngang vật lý từ trên xuống dưới, tương ứng chính xác:
        Hàng 1 -> Tiết 1, Hàng 2 -> Tiết 2, Hàng 3 -> Tiết 3, Hàng 4 -> Tiết 4, Hàng 5 -> Tiết 5.
      + NGUYÊN TẮC BẢO TOÀN Ô TRỐNG (CỰC KỲ QUAN TRỌNG):
        * Đọc quét theo từng hàng ngang từ trái qua phải qua tất cả các cột Thứ (Thứ 2 đến Thứ 7).
        * TUYỆT ĐỐI KHÔNG được dồn môn ở hàng dưới lên hàng trên nếu hàng trên để trống!
        * Ví dụ thực tế: Ở cột Thứ 2, Hàng 1 để trống, Hàng 2 có môn "Toán - 93" -> Tiết 1 là rỗng "", Tiết 2 là "Toán - 93".
        * Ví dụ thực tế: Ở cột Thứ 6, Hàng 4 để trống, Hàng 5 có môn "Toán - 64" -> Tiết 4 là rỗng "", Tiết 5 là "Toán - 64".
      + QUY ƯỚC TÊN LỚP VIẾT TẮT 2 CHỮ SỐ:
        * Trong ảnh, tên lớp thường viết tắt 2 chữ số: 93 (lớp 9/3 hoặc 9A3), 64 (lớp 6/4 hoặc 6A4), 63 (lớp 6/3 hoặc 6A3), 94 (lớp 9/4 hoặc 9A4).
        * Hãy đối chiếu với Danh sách lớp hiện có của trường được cung cấp ở trên để điền đúng tên lớp chuẩn.
    ```
  - Giữ lại các yêu cầu token bắt buộc theo test suite (`tuyệt đối không bỏ sót bất kỳ tiết nào có phân công dạy`).

#### 4. Cập nhật `applyAiTimetableResult(raw)` và `extractAssignmentsFromTimetable`:
- Áp dụng `matchClassFromTimetable(parsed.class_name, state.classes)` khi lưu vào `editingTimetable` và khi phiên sang phân công chuyên môn.
- Tránh tạo lớp mới nếu lớp đó đã có dạng tương đương trong `state.classes`.

---

### File 2: `tests/timetable-render-smoke.js`

- Bổ sung khối test chuyên sâu kiểm thử các tính năng mới:
  1. **Test `matchClassFromTimetable`:**
     - Khớp `93` với `9/3` trong `state.classes`.
     - Khớp `64` với `6/4` trong `state.classes`.
     - Khớp `63` với `6A3` trong `state.classes`.
     - Khớp `71` với `71` khi danh sách lớp dùng định dạng 2 số.
  2. **Test bảo toàn ô trống ma trận 2D:**
     - Giả lập JSON kết quả từ ảnh thật của giáo viên Danh:
       + Thứ 2: Tiết 1 rỗng, Tiết 2 là `Toán - 93`, Tiết 3 là `Toán - 64`, Tiết 4 là `Toán - 63`, Tiết 5 là `Toán - 94`.
       + Thứ 6: Tiết 1 là `Toán - 94`, Tiết 2 là `Toán - 63`, Tiết 3 là `Toán - 63`, Tiết 4 rỗng, Tiết 5 là `Toán - 64`.
     - Xác nhận `applyAiTimetableResult` đưa chính xác vào các tiết tương ứng, không bị trôi hàng.
  3. **Đảm bảo tất cả các test case cũ vẫn PASS 100%.**

---

## 4. Kế hoạch kiểm thử & Verify

1. Chạy suite kiểm thử bằng lệnh:
   ```bash
   node tests/timetable-render-smoke.js
   ```
   Xác nhận PASS toàn bộ, không có lỗi regression.
2. Kiểm tra tính hợp lệ cú pháp của `phancongtochuyenmon.html` thông qua `vm.Script`.
3. Ghi chép kết quả nghiệm thu vào `docs/handoff/VERIFY.md`.
