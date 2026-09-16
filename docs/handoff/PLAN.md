# PLAN

## Hiện trạng & Nguyên nhân gốc rễ (Root Cause)

### 1. Lỗi runtime `ReferenceError: getSystemRole is not defined` khi bấm "Đọc sách giáo khoa"
- **Hiện tượng**: Khi người dùng tải ảnh/PDF SGK và bấm "Đọc sách giáo khoa", console báo lỗi:
  ```
  [CONSOLE_ERROR] OCR SGK: Error: getSystemRole is not defined
  Stack: ReferenceError: getSystemRole is not defined
      at analyzeCanvasTextbookSafely (https://hoangthiencm.id.vn/js/khbd-app.js?v=20260916-textbook-exact-v15:1:443316)
      at async HTMLButtonElement.readTextbookWithMistral (https://hoangthiencm.id.vn/js/khbd-app.js?v=20260916-textbook-exact-v15:1:449777)
  ```
- **Nguyên nhân gốc rễ**:
  1. `getSystemRole` được định nghĩa trong `js/khbd-prompts.js` (dòng 1213) và gán ra toàn cục `window.getSystemRole = getSystemRole` (dòng 1702).
  2. Kiểm tra trực tiếp trên máy chủ bằng `curl -I https://hoangthiencm.id.vn/js/khbd-prompts.js` cho thấy phản hồi HTTP `200 OK` nhưng `Content-Length: 0` (tệp trên hosting đang bị rỗng 0 bytes). Do đó trình duyệt tải về tệp rỗng, hàm `getSystemRole` hoàn toàn không tồn tại trong môi trường Canvas.
  3. Workflow GitHub Actions `.github/workflows/ftp-deploy.yml` chỉ upload các file có thay đổi trong commit diff (`SamKirkland/FTP-Deploy-Action`). Do `js/khbd-prompts.js` không có commit thay đổi gần đây nên action bỏ qua, khiến file 0 bytes bị kẹt trên máy chủ LiteSpeed.
  4. Trong `js/khbd-app.js` (dòng 6846), hàm `analyzeCanvasTextbookSafely` gọi trực tiếp `getSystemRole(appState.selectedSubject, appState.selectedGrade)` mà không có kiểm tra phòng vệ `typeof getSystemRole === "function"`, dẫn đến ném lỗi `ReferenceError` làm dừng toàn bộ tiến trình OCR SGK.

### 2. Lỗi banner "Không tải được danh mục chương trình từ host; đang dùng danh mục dự phòng..."
- **Hiện tượng**: Mở `canvas_soankhbd.html` xuất hiện banner cảnh báo màu đỏ/vàng trên đầu trang.
- **Nguyên nhân gốc rễ**:
  - `https://hoangthiencm.id.vn/js/khbd-curriculum.js` trên hosting cũng đang có `Content-Length: 0` (0 bytes).
  - Tệp rỗng khiến `window.CURRICULUM_DATA` không được khởi tạo, kích hoạt `installCurriculumFallback()`, gán `cfg.moduleFallback.curriculum = true` và làm banner hiển thị cảnh báo lỗi.

### 3. Stepper hiển thị số "1 3 4" thay vì "1 2 3"
- **Hiện tượng**: 3 bước hiển thị trên thanh quy trình Tab 0 có số vòng tròn là 1, 3, 4 trong khi nhãn là Bước 1, Bước 2, Bước 3.
- **Nguyên nhân gốc rễ**:
  - Bước 2 (`data-step="2"`) bị ẩn (`hidden`), khối Bước 3 (`data-step="3"`) mang nhãn `Bước 2` nhưng số hiển thị trong span là `3`, khối Bước 4 (`data-step="4"`) mang nhãn `Bước 3` nhưng số hiển thị trong span là `4`.

---

## Phạm vi thực hiện

1. **Khắc phục lỗi `getSystemRole is not defined` và re-upload `js/khbd-prompts.js`**:
   - Thêm/cập nhật dòng phiên bản deploy ở đầu tệp `js/khbd-prompts.js` (ví dụ `// Deploy version: 20260916-textbook-exact-v15`) để tạo git diff, kích hoạt FTP-Deploy-Action tải toàn bộ 138.942 bytes lên hosting `hoangthiencm.id.vn`.
   - Trong `js/khbd-app.js` (dòng 6846): Bọc kiểm tra phòng vệ an toàn khi gọi `getSystemRole`:
     ```javascript
     typeof getSystemRole === "function" ? getSystemRole(appState.selectedSubject, appState.selectedGrade) : (typeof window !== "undefined" && typeof window.getSystemRole === "function" ? window.getSystemRole(appState.selectedSubject, appState.selectedGrade) : "")
     ```
   - Trong `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`:
     - Tăng query cache-busting cho `khbd-prompts.js` từ `?v=20260916-textbook-exact-v14` lên `?v=20260916-textbook-exact-v15` để trình duyệt và proxy LiteSpeed không giữ file 0-byte trong bộ đệm.
     - Bổ sung fallback stub an toàn trước khi nạp `khbd-app.js`:
       ```javascript
       if (typeof window.getSystemRole === "undefined") {
         window.getSystemRole = function () { return ""; };
       }
       ```

2. **Khắc phục lỗi nạp danh mục chương trình (Curriculum Module)**:
   - File `js/khbd-curriculum.js` (dòng 9) đã đổi `KHBD_CURRICULUM_DEPLOY_VERSION = "canvas-module-v9";` để tạo git diff cho FTP-Deploy-Action tải toàn bộ 173.676 bytes lên host.
   - Cache-busting các module Canvas trong HTML đã được nâng lên `20260916-canvas-module-v9`.

3. **Điều chỉnh số bước Stepper trong `canvas_soankhbd.html` & bản backup**:
   - Xác nhận khối `data-step="3"` hiển thị `<span class="khbd-step-num">2</span>`.
   - Xác nhận khối `data-step="4"` hiển thị `<span class="khbd-step-num">3</span>`.
   - Giữ nguyên các thuộc tính `data-step="3"`, `data-step="4"` và các ID DOM để giữ nguyên vẹn logic của `khbd-app.js`.

---

## Ngoài phạm vi
- Không can thiệp sửa đổi cấu trúc dữ liệu bên trong `js/khbd-curriculum.js` hay logic sinh bài chính của AI.
- Không thay đổi hành vi quy trình 4 bước của trang web chính `soankhbd.html`.

---

## File dự kiến tác động
- `js/khbd-prompts.js` (thêm comment version để kích hoạt FTP deploy)
- `js/khbd-app.js` (thêm kiểm tra phòng vệ `typeof getSystemRole === "function"`)
- `canvas_soankhbd.html` (bump version `khbd-prompts.js` lên v15, thêm fallback stub `getSystemRole`)
- `backupcode viettailieu/canvas_soankhbd.html` (đồng bộ tương tự)
- `js/khbd-curriculum.js` (đã sửa v9 để kích hoạt FTP deploy)

---

## Các bước thực hiện cho Coder
1. **Sửa `js/khbd-prompts.js`**:
   - Ở đầu file (dòng 1-8), thêm chú thích deploy:
     `// Deploy version: 20260916-textbook-exact-v15`
2. **Sửa `js/khbd-app.js`**:
   - Tại dòng 6846, thay `getSystemRole(appState.selectedSubject, appState.selectedGrade)` thành:
     `typeof getSystemRole === "function" ? getSystemRole(appState.selectedSubject, appState.selectedGrade) : (typeof window !== "undefined" && typeof window.getSystemRole === "function" ? window.getSystemRole(appState.selectedSubject, appState.selectedGrade) : "")`
3. **Sửa `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`**:
   - Cập nhật dòng nhúng `khbd-prompts.js` từ `?v=20260916-textbook-exact-v14` thành `?v=20260916-textbook-exact-v15`.
   - Trong khối script fallback trước `khbd-app.js`, bổ sung:
     ```javascript
     if (typeof window.getSystemRole === "undefined") {
       window.getSystemRole = function () { return ""; };
     }
     ```
4. **Kiểm tra smoke test**:
   - Chạy `python C:\Users\HoangThien\.gemini\antigravity\brain\7ddd6240-4311-4b35-b755-f9a3e9f49765\scratch\test_verify.py`.
   - Chạy `node tests/canvas-soankhbd-smoke.js`.
5. **Ghi nhận `docs/handoff/IMPLEMENT.md`**:
   - Ghi lại các thay đổi đã thực hiện và bàn giao cho `/verify`.

---

## Tiêu chí nghiệm thu
1. `analyzeCanvasTextbookSafely` không bao giờ ném lỗi `ReferenceError: getSystemRole is not defined` kể cả khi tệp `khbd-prompts.js` bị trễ mạng hoặc thiếu.
2. `js/khbd-prompts.js` và `js/khbd-curriculum.js` có git diff để CI/CD FTP Deploy tự động tải đầy đủ kích thước (>100KB) lên hosting khi commit & push.
3. Stepper hiển thị chính xác các số `1`, `2`, `3`.
4. Không còn banner cảnh báo lỗi nạp danh mục chương trình.
