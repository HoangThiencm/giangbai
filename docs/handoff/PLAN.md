# PLAN

## Hiện trạng & Nguyên nhân gốc rễ (Root Cause)

### 1. Lỗi banner "Không tải được danh mục chương trình từ host; đang dùng danh mục dự phòng để chọn môn và bài học."
- **Hiện tượng**: Khi mở `canvas_soankhbd.html` trên Gemini Canvas, xuất hiện banner cảnh báo lỗi màu đỏ/vàng trên đầu trang.
- **Nguyên nhân gốc rễ**:
  - Khi khởi động, hàm `bootstrapCanvasCoreModules()` tải file `https://hoangthiencm.id.vn/js/khbd-curriculum.js?v=20260916-canvas-module-v8`.
  - Kiểm tra thực tế bằng lệnh mạng (`curl -I`): Máy chủ `hoangthiencm.id.vn` trả về `HTTP 200 OK` nhưng `Content-Length: 0` (file trên máy chủ đang bị rỗng 0 bytes, do quá trình upload FTP trước đó bị ngắt hoặc lỗi).
  - Do file rỗng 0 bytes, `window.CURRICULUM_DATA` không được định nghĩa, hàm kiểm tra `hasCurriculum()` trả về `false`.
  - Trình duyệt kích hoạt hàm `installCurriculumFallback()`, gán cờ `cfg.moduleFallback.curriculum = true`.
  - Hàm `initConnection()` phát hiện cờ này và hiển thị thông báo lỗi trên banner: *"Không tải được danh mục chương trình từ host; đang dùng danh mục dự phòng để chọn môn và bài học."*

### 2. Stepper hiển thị số "1 3 4" thay vì "1 2 3"
- **Hiện tượng**: Trên thanh quy trình Stepper đầu trang Tab 0, 3 bước hiển thị có số vòng tròn là 1, 3, 4 trong khi nhãn là Bước 1, Bước 2, Bước 3.
- **Nguyên nhân gốc rễ**:
  - Trong `canvas_soankhbd.html` (dòng 343–376):
    - Bước 1 (`data-step="1"`): Số `<span class="khbd-step-num">1</span>`, tiêu đề `Bước 1: Nạp & Đọc SGK`.
    - Bước 2 (`data-step="2"`): `Bước 2: PPCT đã lưu` bị ẩn (`hidden style="display:none"`).
    - Bước 3 (`data-step="3"`): Nhãn text là `Bước 2: Kế hoạch PPDH & Tích hợp NLS/AI (Ưu tiên từ PPCT)`, nhưng số vòng tròn hiển thị vẫn còn là `<span class="khbd-step-num">3</span>`.
    - Bước 4 (`data-step="4"`): Nhãn text là `Bước 3: Tích hợp AI & Soạn bài`, nhưng số vòng tròn hiển thị vẫn còn là `<span class="khbd-step-num">4</span>`.
  - Do đó người dùng thấy 3 vòng tròn nối tiếp nhau mang số `1`, `3`, `4`.

---

## Phạm vi thực hiện

1. **Điều chỉnh số bước Stepper trong `canvas_soankhbd.html`**:
   - Đổi số hiển thị của bước thứ 2 (khối `data-step="3"`) từ `<span class="khbd-step-num">3</span>` thành `<span class="khbd-step-num">2</span>`.
   - Đổi số hiển thị của bước thứ 3 (khối `data-step="4"`) từ `<span class="khbd-step-num">4</span>` thành `<span class="khbd-step-num">3</span>`.
   - Giữ nguyên các thuộc tính `data-step="3"` và `data-step="4"`, cùng toàn bộ ID phần tử (`step3Badge`, `step4Badge`, `btnStep3Recommend`, `btnStartComposeFromStep4`) để giữ nguyên vẹn logic cập nhật trạng thái `is-done`/`is-active` và điều hướng click của `js/khbd-app.js`.
   - Cập nhật `aria-label` của `#khbdWorkflowStepper` thành `"Quy trình 3 bước soạn KHBD"`.
   - Đồng bộ tương tự cho `backupcode viettailieu/canvas_soankhbd.html`.

2. **Khắc phục lỗi nạp danh mục chương trình (Curriculum Module)**:
   - Re-upload file `js/khbd-curriculum.js` đầy đủ (173.6 KB trong repo) lên hosting `https://hoangthiencm.id.vn/js/khbd-curriculum.js`.
   - Tăng chuỗi phiên bản cache-busting trong `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html` từ `20260916-canvas-module-v8` lên `20260916-canvas-module-v9` (hoặc `v10`) để trình duyệt và proxy LiteSpeed không giữ bản 0-byte trong bộ nhớ cache.

---

## Ngoài phạm vi
- Không can thiệp sửa đổi cấu trúc dữ liệu bên trong `js/khbd-curriculum.js` hoặc logic sinh bài của AI.
- Không thay đổi hành vi quy trình 4 bước của trang web chính `soankhbd.html`.

---

## File dự kiến tác động
- `canvas_soankhbd.html`
- `backupcode viettailieu/canvas_soankhbd.html`
- `tests/canvas-module-fallback-smoke.js`
- `tests/canvas-soankhbd-smoke.js`
- Hosting: `https://hoangthiencm.id.vn/js/khbd-curriculum.js` (re-upload file 173 KB).

---

## Các bước thực hiện
1. Sửa file `canvas_soankhbd.html`:
   - Đổi `<span class="khbd-step-num">3</span>` thành `<span class="khbd-step-num">2</span>` ở khối `data-step="3"`.
   - Đổi `<span class="khbd-step-num">4</span>` thành `<span class="khbd-step-num">3</span>` ở khối `data-step="4"`.
   - Cập nhật `aria-label="Quy trình 3 bước soạn KHBD"`.
   - Tăng version query string của các module Canvas lên `20260916-canvas-module-v9`.
2. Đồng bộ các thay đổi trên vào `backupcode viettailieu/canvas_soankhbd.html`.
3. Re-upload `js/khbd-curriculum.js` lên hosting `hoangthiencm.id.vn`.
4. Cập nhật test smoke tests và chạy kiểm thử tự động.

---

## Rủi ro & Cách phòng tránh
- **Rủi ro vỡ điều hướng JS**: Nếu đổi `data-step="3"` thành `data-step="2"`, hàm `revealTab0WorkflowStep()` sẽ chuyển nhầm subtab (vào vật liệu học thay vì bảng PPDH/NLS).
  - *Phòng tránh*: Chỉ sửa nội dung text hiển thị trong `<span class="khbd-step-num">`, giữ nguyên giá trị thuộc tính `data-step`.
- **Rủi ro cache 0-byte**: Trình duyệt có thể lưu cache phản hồi HTTP 200 (0 bytes) của file `khbd-curriculum.js`.
  - *Phòng tránh*: Tăng query version `?v=20260916-canvas-module-v9`.

---

## Cách kiểm thử
1. **Kiểm tra giao diện Stepper**:
   - Mở `canvas_soankhbd.html`: 3 vòng tròn bước hiển thị theo thứ tự `1` -> `2` -> `3`.
   - Nhãn tương ứng: `Bước 1: Nạp & Đọc SGK`, `Bước 2: Kế hoạch PPDH & Tích hợp NLS/AI (Ưu tiên từ PPCT)`, `Bước 3: Tích hợp AI & Soạn bài`.
2. **Kiểm tra tương tác Stepper**:
   - Bấm vào vòng tròn 2 / Bước 2: Tự động cuộn đến card đề xuất PPDH & NLS (`lessonStep3RecommendCard`).
   - Bấm vào nút `⚡ Đề xuất PPDH & NLS`: Hoạt động bình thường.
   - Bấm vào vòng tròn 3 / Bước 3: Chuyển đến phần AI.
3. **Kiểm tra kết nối host**:
   - `curl -I "https://hoangthiencm.id.vn/js/khbd-curriculum.js?v=20260916-canvas-module-v9"` trả về `Content-Length > 150000`.
   - Banner màu xanh hiện lên: `Đã kết nối host hoangthiencm.id.vn — dùng Gemini Canvas (gemini-3-flash-preview)...`.

---

## Tiêu chí nghiệm thu
1. Các vòng tròn trên thanh Stepper hiển thị chính xác chuỗi số `1`, `2`, `3`.
2. Không còn lệch số (1 - 3 - 4).
3. Khi file `js/khbd-curriculum.js` được re-upload lên hosting, banner báo lỗi biến mất và hiển thị thông báo kết nối thành công.
