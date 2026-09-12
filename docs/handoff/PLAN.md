# PLAN: Sửa lỗi nhận diện nhầm giáo viên Hoàng Xuân Ánh sang Hồ Đăng Danh, Gỡ bỏ Auto-Reload, và Cấu hình Phụ lục

## Hiện trạng

### 1. Vấn đề 1: Dán Thời khóa biểu thầy "Hoàng Xuân Ánh" bị nhận diện nhầm thành thầy "Hồ Đăng Danh"
- **Hiện tượng**:
  - Khi dán hoặc nhận diện ảnh TKB của thầy Hoàng Xuân Ánh, hệ thống luôn tự động gán vào thầy Hồ Đăng Danh; trong khi các giáo viên khác đều nhận diện đúng.
- **Nguyên nhân cốt lõi**:
  - Trong hàm `applyAiTimetableResult()` (dòng 6110–6118 của `phancongtochuyenmon.html`):
    ```javascript
    const foldedName = foldText(name);
    const match = (state.teachers || []).find(t => {
        const folded = foldText(t.name);
        return folded === foldedName || folded.includes(foldedName) || foldedName.includes(folded);
    });
    ```
  - Trong ảnh TKB, tên giáo viên ghi là "Ánh" (hoặc "Giáo viên: Ánh") -> `foldedName = "ANH"`.
  - Tên thầy Hồ Đăng Danh được chuẩn hóa thành `folded = "HO DANG DANH"`.
  - Do dùng lệnh kiểm tra chuỗi con `.includes("ANH")`, chữ **D-A-N-H** chứa chuỗi con **A-N-H** nên `"HO DANG DANH".includes("ANH")` trả về **`true`**!
  - Vì thầy Hồ Đăng Danh đứng trước thầy Hoàng Xuân Ánh trong danh sách giáo viên, hàm `.find()` dừng ngay tại thầy Hồ Đăng Danh và gán TKB cho thầy Danh, không bao giờ duyệt tới thầy Ánh!

### 2. Vấn đề 2: Hệ thống bị tự động refresh / reload liên tục
- **Hiện tượng**: Toàn bộ hệ thống hoangthiencm.id.vn tự động reload liên tục do cơ chế `initAutoUpdateChecker()` trong `js/security-guard.js`.
- **Yêu cầu**: Gỡ bỏ hoàn toàn cơ chế auto-reload, trả về nguyên trạng như cũ, không bao giờ tự động reload trang.

### 3. Vấn đề 3: Đưa bộ chọn tích hợp theo "Tổng số tiết" và "Tỉ lệ %" vào Mục 1 Xây dựng Phụ lục
- **Hiện tượng**: Trên `canvas_xaydungphuluc.html`, các ô nhập số tiết `#nlsCountInput`, `#aiCountInput` bị đặt nhầm xuống tận cuối trang sau Mục 7.
- **Yêu cầu**: Đưa cụm chọn đơn vị và nhập số tiết vào trực tiếp trong thẻ NLS & AI tại Mục 1, đồng bộ 2 chiều với thanh trượt %.

---

## Mục tiêu & Giải pháp thiết kế

### 1. Xây dựng thuật toán so khớp tên giáo viên chuẩn xác (`matchTeacherByName`)
1. **Khớp trọn từ (Word Token Matching)**:
   - Tách tên thành các từ riêng biệt bằng khoảng trắng `split(/\s+/)`.
   - Tuyệt đối không dùng `.includes()` trên cả chuỗi họ tên để tránh các từ như `DANH`, `THANH`, `MANH`, `HANH` bị nhận nhầm thành `ANH`.
2. **Quy tắc ưu tiên**:
   - **Ưu tiên 1**: Nếu trên màn hình người dùng đang chọn sẵn một giáo viên (`currentTeacherId`), và tên trong ảnh khớp hoàn toàn hoặc từ cuối (tên chính) trùng khớp với giáo viên đang chọn -> Giữ nguyên giáo viên đang chọn, không nhảy sang người khác.
   - **Ưu tiên 2**: Khớp chính xác 100% cả họ và tên (`folded === target`).
   - **Ưu tiên 3**: Bắt buộc từ cuối cùng (Tên chính) phải trùng khớp nhau (`tLastWord === targetLastWord`). Ví dụ: Tên ảnh là "ANH" thì từ cuối của GV bắt buộc phải là "ANH" (loại trừ ngay "DANH").
   - **Ưu tiên 4**: Nếu có nhiều người trùng tên chính (ví dụ "Hoàng Xuân Ánh" và "Nguyễn Thị Ánh"), so khớp các từ họ đệm để chọn người có độ trùng khớp cao nhất.

### 2. Gỡ bỏ hoàn toàn Auto-Reload trong `js/security-guard.js`
- Xóa bỏ các hàm và biến liên quan đến `initAutoUpdateChecker`, `checkAppVersionUpdate`, `version.json`, và `window.location.reload()`.

### 3. Bố trí bộ chọn số tiết & tỉ lệ % vào Mục 1 Xây dựng Phụ lục
- Đưa `#nlsUnit`, `#nlsCountInput`, `#aiUnit`, `#aiCountInput` vào bên trong thẻ NLS và AI ở Mục 1 `canvas_xaydungphuluc.html` và xóa thẻ thừa dòng 73.

---

## Phạm vi thực hiện

1. `phancongtochuyenmon.html`:
   - Thêm hàm `matchTeacherByName(rawName, teachers, currentTeacherId)`.
   - Trong `applyAiTimetableResult()`: Gọi `matchTeacherByName(name, state.teachers, selectedTimetableTeacherId)` thay cho đoạn so khớp thô cũ.
2. `js/security-guard.js`:
   - Gỡ bỏ hoàn toàn module auto-reload (dòng 34–105).
3. `canvas_xaydungphuluc.html`:
   - Chuyển `#nlsUnit`, `#nlsCountInput`, `#aiUnit`, `#aiCountInput` vào Mục 1, xóa thẻ thừa dòng 73.
4. `tests/timetable-render-smoke.js`:
   - Bổ sung test case xác nhận: Tên "Ánh" trong ảnh phải khớp với "Hoàng Xuân Ánh", không được khớp với "Hồ Đăng Danh".
5. `tests/auto-reload-smoke.js`:
   - Cập nhật test xác nhận `security-guard.js` không còn chứa lệnh auto-reload.

---

## Ngoài phạm vi

- Không sửa đổi thuật toán AI trích xuất tiết học.
- Không sửa đổi cấu trúc dữ liệu lưu CSDL.

---

## File dự kiến tác động

1. `phancongtochuyenmon.html`
2. `js/security-guard.js`
3. `canvas_xaydungphuluc.html`
4. `tests/timetable-render-smoke.js`
5. `tests/auto-reload-smoke.js`

---

## Các bước thực hiện

### Bước 1: Sửa thuật toán so khớp tên trong `phancongtochuyenmon.html`
- Định nghĩa hàm `matchTeacherByName(rawName, teachers, currentTeacherId)` với cơ chế khớp từ ranh giới từ và ưu tiên tên chính.
- Trong `applyAiTimetableResult`:
  ```javascript
  const matchedTeacher = matchTeacherByName(name, state.teachers || [], selectedTimetableTeacherId);
  if (matchedTeacher) selectedTimetableTeacherId = matchedTeacher.id;
  ```

### Bước 2: Gỡ bỏ auto-reload trong `js/security-guard.js`
- Xóa dòng 34 đến 105 trong `js/security-guard.js`.

### Bước 3: Cập nhật giao diện Mục 1 trong `canvas_xaydungphuluc.html`
- Đặt `#nlsUnit`, `#nlsCountInput` vào thẻ NLS, `#aiUnit`, `#aiCountInput` vào thẻ AI; xóa thẻ thừa ở dòng 73.

### Bước 4: Chạy toàn bộ các bài kiểm thử
- `node tests/baogiang-weekday-segment-smoke.js`
- `node tests/timetable-render-smoke.js`
- `node tests/auto-reload-smoke.js`
- `git diff --check`

---

## Tiêu chí nghiệm thu

1. Khi dán hoặc nhận diện ảnh TKB có tên "Ánh" hoặc "Hoàng Xuân Ánh", hệ thống chọn chính xác thầy **Hoàng Xuân Ánh**, tuyệt đối không bị nhảy sang thầy **Hồ Đăng Danh**.
2. Hệ thống hoàn toàn không còn tự reload trang bất thường.
3. Mục 1 Xây dựng Phụ lục có đầy đủ ô chọn/nhập theo Tổng số tiết và kéo theo Tỉ lệ %.
4. Tất cả các test suites đạt **PASS 100%**.
