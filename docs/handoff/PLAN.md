# PLAN: Thêm tính năng xóa học sinh và tự động lưu khi chỉnh sửa thông tin trong Sổ Điểm & KTTX

## Hiện trạng
1. **Thiếu nút và hàm Xóa học sinh (`sodiem.html`)**:
   - Trong bảng sổ điểm ([`sodiem.html#L39`](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/sodiem.html#L39)), ở cột thao tác cuối mỗi dòng hiện chỉ có duy nhất nút "Gọi kiểm tra" (biểu tượng `<i class="fa fa-bullhorn"></i>`, hàm `quickCall(index)`).
   - Hoàn toàn chưa có nút hay chức năng Xóa học sinh (`deleteStudent`). Khi giáo viên bấm nút "Thêm học sinh", dán danh sách hoặc nhập Excel bị thừa, trùng hoặc sai tên, không thể xóa bỏ học sinh đó khỏi sổ điểm.
2. **Chỉnh sửa thông tin học sinh chưa kích hoạt tự động lưu CSDL**:
   - Khi sửa Mã/SBD, Họ và tên hoặc Nhận xét trên các ô input ([`sodiem.html#L39`](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/sodiem.html#L39)), sự kiện `onchange` mới chỉ gọi `persist()` (lưu tạm localStorage) mà không gọi `triggerAutoSave()`.
   - Nếu giáo viên sửa lại tên bị nhập sai mà không bấm nút "Lưu" thủ công (hoặc không nhập điểm), dữ liệu không được đồng bộ lên CSDL MySQL và có thể bị hoàn tác khi mở lại hoặc nạp lại lớp.
3. **Cơ chế nạp lớp (`mergeStudents`)**:
   - Hàm `mergeStudents()` ([`sodiem.html#L34`](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/sodiem.html#L34)) tự động hợp nhất học sinh từ CSDL, cache localStorage và roster từ hệ thống. Nếu không lưu danh sách các học sinh đã xóa (`deletedKeys`), học sinh từ roster có thể bị tự động nạp lại khi giáo viên chọn lại lớp.

---

## Phạm vi
1. **Bổ sung tính năng Xóa học sinh trong `sodiem.html`**:
   - Thêm nút Xóa (icon thùng rác `<i class="fa fa-trash"></i>`, màu đỏ `text-rose-600 hover:text-rose-800`) vào cột thao tác bên cạnh nút Gọi kiểm tra trên từng dòng của bảng sổ điểm.
   - Thêm hàm `deleteStudent(index)`:
     + Hiển thị hộp thoại xác nhận rõ ràng: "Bạn có chắc chắn muốn xóa học sinh [Tên HS] (Mã: [SBD]) khỏi sổ điểm? Điểm số của học sinh này sẽ bị xóa."
     + Khi người dùng bấm OK: Xóa học sinh khỏi mảng `students` (`students.splice(index, 1)`).
     + Lưu khóa nhận diện của học sinh đã xóa vào danh sách loại trừ (`deletedStudentKeys` lưu trong localStorage và đồng bộ theo sổ điểm) để hàm `mergeStudents()` không tự động nạp lại từ roster khi tải lại lớp.
     + Gọi `persist()`, `triggerAutoSave()` để cập nhật tức thì lên localStorage và máy chủ/CSDL MySQL.
     + Cập nhật lại giao diện qua `renderAll()`.
2. **Kích hoạt tự động lưu CSDL khi thêm hoặc sửa thông tin học sinh**:
   - Cập nhật hàm `addStudent()`: Gọi thêm `triggerAutoSave()` sau khi push học sinh mới để lưu ngay bản ghi lên CSDL.
   - Cập nhật sự kiện `onchange` của các ô input: Mã/SBD (`sbd`), Họ và tên (`name`), và Nhận xét (`comment`): Gọi thêm `triggerAutoSave()` để đồng bộ ngay thay đổi lên CSDL MySQL.
3. **Cập nhật bài test tự động `tests/sodiem-smoke.js`**:
   - Bổ sung assertion kiểm tra sự tồn tại của hàm `deleteStudent`, nút xóa với icon thùng rác, xác nhận confirm, loại bỏ phần tử khỏi `students`, và cơ chế `triggerAutoSave` khi chỉnh sửa thông tin học sinh.

---

## Ngoài phạm vi
- Không thay đổi cấu trúc bảng cơ sở dữ liệu `gradebooks` trong MySQL (trường `students_data_json` dạng `LONGTEXT` đã hỗ trợ đầy đủ mảng học sinh cập nhật).
- Không ảnh hưởng tới logic tính điểm trung bình thường xuyên (ĐTBtx), vòng quay kiểm tra hay ngân hàng câu hỏi.

---

## File dự kiến tác động
- `sodiem.html`
- `tests/sodiem-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

---

## Các bước thực hiện
1. **Bước 1: Mở khóa handoff**:
   - Coder xóa `docs/handoff/.lock` trước khi sửa source code.
2. **Bước 2: Nâng cấp `sodiem.html`**:
   - Bổ sung mảng theo dõi học sinh bị xóa `deletedStudentKeys` theo từng lớp/môn.
   - Cập nhật hàm `mergeStudents`: Bỏ qua các học sinh có khóa nằm trong `deletedStudentKeys`.
   - Cập nhật hàm `renderGrades()`:
     + Trong cột thao tác `td.no-print`, thêm nút `<button onclick="deleteStudent(${index})" class="text-rose-600 hover:text-rose-800 p-1 ml-1" title="Xóa học sinh"><i class="fa fa-trash"></i></button>`.
     + Cập nhật các input `sbd`, `name`, `comment`: Thêm `triggerAutoSave()` vào `onchange`.
   - Viết hàm `deleteStudent(index)`:
     + Xác nhận `confirm(...)`.
     + Lưu key vào `deletedStudentKeys`.
     + `students.splice(index, 1)`.
     + Gọi `persist()`, `triggerAutoSave()`, `renderAll()`.
   - Cập nhật `addStudent()` và `pasteStudents()`: Kích hoạt `triggerAutoSave()`.
3. **Bước 3: Cập nhật bài test `tests/sodiem-smoke.js`**:
   - Kiểm tra các mẫu regex cho `deleteStudent`, nút xóa `fa-trash`, xác nhận confirm, và auto-save khi sửa tên/sbd.
   - Chạy `agy-node tests/sodiem-smoke.js` đạt PASS 100%.
4. **Bước 4: Ghi nhật ký vào `docs/handoff/IMPLEMENT.md` và tạo lại `docs/handoff/.lock` nội dung `LOCK`**.

---

## Rủi ro
- **Xóa nhầm học sinh đang có nhiều cột điểm**: Có thể mất dữ liệu điểm nếu bấm nhầm.
  -> Biện pháp: Đặt hộp thoại `confirm()` hiển thị rõ họ tên, mã học sinh và cảnh báo điểm sẽ bị xóa trước khi thực hiện.
- **Học sinh bị xóa xuất hiện lại khi chuyển lớp rồi quay lại**: Do `roster` trả về từ server.
  -> Biện pháp: Lưu danh sách `deletedStudentKeys` trong cấu hình lưu trữ của sổ điểm và lọc bỏ ngay trong `mergeStudents()`.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh: `agy-node tests/sodiem-smoke.js` -> PASS 100%.
2. **Kiểm thử thủ công trên trình duyệt**:
   - Mở trang `sodiem.html`, chọn lớp và môn học.
   - Bấm "Thêm học sinh" -> Xuất hiện dòng học sinh mới.
   - Sửa Họ và tên, Mã/SBD -> Trạng thái lưu trên thanh tiêu đề đổi sang "Đang lưu CSDL..." rồi "Đã lưu CSDL".
   - Bấm nút Xóa (thùng rác màu đỏ) tại một học sinh nhập sai:
     + Xuất hiện hộp thoại hỏi xác nhận.
     + Bấm Hủy -> Học sinh vẫn còn nguyên.
     + Bấm OK -> Học sinh biến mất khỏi bảng, danh sách cập nhật ngay, ĐTB và báo cáo được tính lại.
   - Bấm nút "Nạp lớp" hoặc tải lại trang F5 -> Học sinh đã xóa không bị xuất hiện lại.

---

## Tiêu chí nghiệm thu
- Có nút thùng rác màu đỏ để xóa từng học sinh nhập sai trên mỗi dòng của bảng sổ điểm.
- Có thông báo xác nhận an toàn trước khi xóa.
- Khi xóa, học sinh và điểm số liên quan được xóa bỏ sạch sẽ khỏi mảng dữ liệu, giao diện và CSDL.
- Khi sửa Họ tên, Mã/SBD, Nhận xét thì hệ thống tự động lưu lên CSDL MySQL.
- Học sinh đã xóa không bị tự động xuất hiện lại khi nạp lại lớp.
- Smoke test chạy thành công 100%.
