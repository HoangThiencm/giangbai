# PLAN: Đưa Giao Diện Theo Dõi / Hero Vào Modal Setting & Thêm 3 Tab Canvas (Phân Quyền Admin)

## User Review Required
> [!IMPORTANT]
> 1. **Giao diện Hero / Theo dõi giáo viên** (Xin chào, Lớp phụ trách, Tiến độ nộp bài, Theo dõi AI, Thống kê AI hôm nay - như trong ảnh) sẽ được chuyển vào bên trong **Modal Setting** (`UserAiSettings.openModal()`):
>    - Trang chủ `index.html` sẽ gọn gàng, bộ thẻ công cụ bento hiển thị ngay phía trên, không bị đẩy xuống dưới bởi panel lớn.
>    - Trong modal Setting, bổ sung tab navigation:
>      - **Tab 1: Tổng quan & Theo dõi**: Hiển thị trọn vẹn toàn bộ giao diện như ảnh chụp (panel gradient xanh teal, thông tin lớp phụ trách, nút trạng thái API Key, 2 thẻ hành động Lộ trình/Tiến độ và khối nhúng thống kê AI hôm nay).
>      - **Tab 2: Cài đặt AI & API Key**: Hiển thị cấu hình model Gemini mặc định/dự phòng, nhập key Gemini & Mistral, upload file .txt, kiểm tra/lưu/xóa key.
>      - Nút `#heroKeyStatus` ("API Key sẵn sàng...") ở Tab 1 khi bấm sẽ tự động chuyển sang Tab 2 để tiện chỉnh sửa.
> 2. **Bổ sung 3 tab Canvas với phân quyền Admin**:
>    - **Tab 1: `CANVAS_SOANKHBD`** → `https://gemini.google.com/app/74fb6bf46c11076a?hl=vi` (key: `canvas_soankhbd`)
>    - **Tab 2: `CANVAS_SOẠN LỘ TRÌNH`** → `https://gemini.google.com/app/0fdb1756f609d61f?hl=vi` (key: `canvas_soanlotrinh`)
>    - **Tab 3: `CANVAS_SÁNG KIẾN`** (`CANVAS_SANGS KIẾN`) → `https://gemini.google.com/app/e6bf41201af60de3?hl=vi` (key: `canvas_sangkien`)
>    - Cả 3 tab này được tích hợp đầy đủ vào hệ thống phân quyền: Admin có thể bật/tắt toàn cục (global features) hoặc cấp quyền riêng cho từng giáo viên (allowed_pages). Nếu giáo viên chưa được cấp quyền, thẻ sẽ bị ẩn hoàn toàn trên trang chủ.

---

## I. Thiết Kế Kỹ Thuật Chi Tiết

### Module 1: Đưa Hero Panel vào Modal Setting (`js/user-ai-settings.js` & `index.html`)

1. **Cấu trúc lại Modal Setting trong `js/user-ai-settings.js`**:
   - Mở rộng kích thước modal từ `max-w-2xl` thành `max-w-5xl` (responsive, tối ưu hiển thị 2 cột và bảng thống kê AI).
   - Thiết kế thanh chuyển Tab (Tab bar) phía trên nội dung modal:
     - Nút Tab 1: `<button type="button" id="tabBtnOverview" class="tab-btn active"><i class="fas fa-chart-pie mr-2"></i>Tổng quan &amp; Theo dõi</button>`
     - Nút Tab 2: `<button type="button" id="tabBtnKeys" class="tab-btn"><i class="fas fa-key mr-2"></i>Cài đặt AI &amp; API Key</button>`
   - Khung chứa Tab 1 (`#userAiTabOverview`):
     - Chứa container `<div id="teacherLotrinhPanel" class="teacher-lotrinh-panel"></div>` (di chuyển từ body `index.html` vào trong modal, hoặc mount vào đây).
   - Khung chứa Tab 2 (`#userAiTabKeys`):
     - Chứa toàn bộ form cài đặt model Gemini, fallback model, textarea Gemini keys, Mistral keys, test results, và các nút Lưu/Kiểm tra/Xóa.
   - Thêm phương thức `UserAiSettings.switchTab(tabName)`:
     - Chuyển đổi giữa `'overview'` và `'keys'`.
     - Cho phép gọi `UserAiSettings.openModal('overview')` hoặc `UserAiSettings.openModal('keys')`.
     - Nếu mở từ `#heroKeyStatus`, chuyển trực tiếp sang tab `'keys'`.

2. **Cập nhật `index.html`**:
   - Khối `#teacherLotrinhHub` trên trang chủ không còn chiếm diện tích trên trang chính:
     - Giữ thẻ `<section id="teacherLotrinhHub" class="hidden"></section>` hoặc tích hợp trực tiếp vào modal.
     - Khi `setupTeacherLotrinhHub()` chạy:
       - Gọi `UserAiSettings.ensureModal()` trước để DOM `#teacherLotrinhPanel` sẵn sàng trong modal.
       - Render template hero (Xin chào, Lớp phụ trách, Lộ trình actions, Theo dõi AI hôm nay) vào `#teacherLotrinhPanel` bên trong modal.
       - Kích hoạt nạp thống kê AI `window.loadAiStats?.(true, ...)` gắn vào `#teacherAiStatsMount` bên trong panel trong modal.
     - Trên trang chủ:
       - Thanh công cụ `#toolsDeck` và header công cụ giảng dạy sẽ hiển thị nổi bật ngay trên màn hình.
       - Nút navbar `#btnOpenUserAiSettings` ("Cài đặt AI & Key") mở modal setting với đầy đủ giao diện theo dõi và cấu hình.
       - Giữ nguyên `id="heroKeyStatus"` và `id="btnOpenUserAiSettings"` để vượt qua 100% các assertion trong `tests/user-ai-settings-smoke.js`.

---

### Module 2: Tích Hợp 3 Tab Canvas Mới & Phân Quyền Admin

1. **Khai báo trong Backend PHP (`api/helpers.php`)**:
   - Bổ sung vào `page_catalog()`:
     ```php
     'canvas_soankhbd' => ['title' => 'CANVAS_SOANKHBD', 'url' => 'https://gemini.google.com/app/74fb6bf46c11076a?hl=vi'],
     'canvas_soanlotrinh' => ['title' => 'CANVAS_SOẠN LỘ TRÌNH', 'url' => 'https://gemini.google.com/app/0fdb1756f609d61f?hl=vi'],
     'canvas_sangkien' => ['title' => 'CANVAS_SÁNG KIẾN', 'url' => 'https://gemini.google.com/app/e6bf41201af60de3?hl=vi'],
     ```
   - Bổ sung vào `teacher_workspace_page_ids()`:
     - Thêm `'canvas_soankhbd'`, `'canvas_soanlotrinh'`, `'canvas_sangkien'`.
   - Bổ sung vào `teacher_feature_keys_for_pages()`:
     ```php
     'canvas_soankhbd' => 'canvas_soankhbd',
     'canvas_soanlotrinh' => 'canvas_soanlotrinh',
     'canvas_sangkien' => 'canvas_sangkien',
     ```

2. **Cập nhật Cấu hình Toàn Cục (`global_config.json`)**:
   - Thêm vào object `"features"`:
     ```json
     "canvas_soankhbd": true,
     "canvas_soanlotrinh": true,
     "canvas_sangkien": true
     ```

3. **Cập nhật Quản Trị Phân Quyền (`admin.html`)**:
   - Bổ sung vào `CLIENT_FEATURE_CHECKS`:
     - Thêm `'canvas_soankhbd'`, `'canvas_soanlotrinh'`, `'canvas_sangkien'`.
   - Bổ sung vào `FEATURE_NAMES`:
     ```javascript
     canvas_soankhbd: "CANVAS_SOANKHBD",
     canvas_soanlotrinh: "CANVAS_SOẠN LỘ TRÌNH",
     canvas_sangkien: "CANVAS_SÁNG KIẾN",
     ```
   - Bổ sung vào `USER_FEATURE_GROUPS`:
     - Thêm 3 key vào danh sách ids của `'Công cụ AI trên hub giáo viên'`.
   - Bổ sung vào `hostingPages`:
     ```javascript
     canvas_soankhbd: { title: 'CANVAS_SOANKHBD', url: 'https://gemini.google.com/app/74fb6bf46c11076a?hl=vi' },
     canvas_soanlotrinh: { title: 'CANVAS_SOẠN LỘ TRÌNH', url: 'https://gemini.google.com/app/0fdb1756f609d61f?hl=vi' },
     canvas_sangkien: { title: 'CANVAS_SÁNG KIẾN', url: 'https://gemini.google.com/app/e6bf41201af60de3?hl=vi' },
     ```
   - Bổ sung vào `teacherFeatureGroups`:
     - Thêm 3 key vào mảng `pages` của `'Công cụ giảng dạy'`.
   - Thêm các thẻ bật/tắt toàn cục trong phần HTML config features của `admin.html`:
     - `<input type="checkbox" id="cfg_canvas_soankhbd" ...>`
     - `<input type="checkbox" id="cfg_canvas_soanlotrinh" ...>`
     - `<input type="checkbox" id="cfg_canvas_sangkien" ...>`

4. **Hiển Thị Trên Trang Chủ (`index.html`)**:
   - Bổ sung vào `TOOL_PAGE_LINKS`:
     ```javascript
     canvas_soankhbd: 'https://gemini.google.com/app/74fb6bf46c11076a?hl=vi',
     canvas_soanlotrinh: 'https://gemini.google.com/app/0fdb1756f609d61f?hl=vi',
     canvas_sangkien: 'https://gemini.google.com/app/e6bf41201af60de3?hl=vi',
     ```
   - Bổ sung 3 thẻ bento tile vào `#mainToolsGrid`:
     - **Thẻ 1**:
       ```html
       <a href="https://gemini.google.com/app/74fb6bf46c11076a?hl=vi" target="_blank" rel="noopener noreferrer" data-tool="canvas_soankhbd" class="tool-tile tool-tile--colored tool-tile--canvas-soankhbd">
           <span class="tool-tile-glow"></span>
           <span class="tool-tile-watermark"><i class="fas fa-book-bookmark"></i></span>
           <div class="tool-tile-content">
               <span class="tool-tile-eyebrow">Gemini Canvas</span>
               <h3 class="tool-tile-title">CANVAS_SOANKHBD</h3>
               <p class="tool-tile-desc">Soạn kế hoạch bài dạy AI môn Toán chuẩn CV 5512 trên môi trường Canvas.</p>
           </div>
           <span class="tool-tile-go"><i class="fas fa-arrow-up-right-from-square"></i></span>
       </a>
       ```
     - **Thẻ 2**:
       ```html
       <a href="https://gemini.google.com/app/0fdb1756f609d61f?hl=vi" target="_blank" rel="noopener noreferrer" data-tool="canvas_soanlotrinh" class="tool-tile tool-tile--colored tool-tile--canvas-lotrinh">
           <span class="tool-tile-glow"></span>
           <span class="tool-tile-watermark"><i class="fas fa-route"></i></span>
           <div class="tool-tile-content">
               <span class="tool-tile-eyebrow">Gemini Canvas</span>
               <h3 class="tool-tile-title">CANVAS_SOẠN LỘ TRÌNH</h3>
               <p class="tool-tile-desc">Soạn lộ trình bài giảng và học tập theo chuẩn SGK trên môi trường Canvas.</p>
           </div>
           <span class="tool-tile-go"><i class="fas fa-arrow-up-right-from-square"></i></span>
       </a>
       ```
     - **Thẻ 3**:
       ```html
       <a href="https://gemini.google.com/app/e6bf41201af60de3?hl=vi" target="_blank" rel="noopener noreferrer" data-tool="canvas_sangkien" class="tool-tile tool-tile--colored tool-tile--canvas-sangkien">
           <span class="tool-tile-glow"></span>
           <span class="tool-tile-watermark"><i class="fas fa-lightbulb"></i></span>
           <div class="tool-tile-content">
               <span class="tool-tile-eyebrow">Gemini Canvas</span>
               <h3 class="tool-tile-title">CANVAS_SÁNG KIẾN</h3>
               <p class="tool-tile-desc">Sử dụng AI để viết sáng kiến kinh nghiệm giáo dục trên môi trường Canvas.</p>
           </div>
           <span class="tool-tile-go"><i class="fas fa-arrow-up-right-from-square"></i></span>
       </a>
       ```
     - Thay thế/loại bỏ thẻ cũ `vietsangkien` không được quản trị quyền trước đó.
   - Thêm CSS classes định dạng gradient sắc nét, bóng bẩy cho 3 thẻ Canvas mới:
     - `.tool-tile--canvas-soankhbd`: Indigo / Violet gradient
     - `.tool-tile--canvas-lotrinh`: Teal / Emerald gradient
     - `.tool-tile--canvas-sangkien`: Pink / Rose gradient

---

## II. Danh Sách Tệp Cần Chỉnh Sửa

| Tệp tin | Vị trí | Mục đích thay đổi |
| :--- | :--- | :--- |
| `js/user-ai-settings.js` | Toàn bộ file | Thiết kế lại modal thành giao diện 2 tab (Tổng quan & Theo dõi chứa hero panel; Cài đặt AI & Key), mở rộng `max-w-5xl`, hỗ trợ chuyển tab |
| `index.html` | Header, main, script | Chuyển `#teacherLotrinhPanel` vào modal setting, thêm 3 thẻ Canvas mới vào `#mainToolsGrid` và `TOOL_PAGE_LINKS`, bổ sung CSS class |
| `admin.html` | Cấu hình & phân quyền | Thêm 3 quyền `canvas_soankhbd`, `canvas_soanlotrinh`, `canvas_sangkien` vào `CLIENT_FEATURE_CHECKS`, `FEATURE_NAMES`, `hostingPages`, `teacherFeatureGroups`, UI toggles |
| `api/helpers.php` | Page catalog | Khai báo 3 trang Canvas mới trong `page_catalog()`, `teacher_workspace_page_ids()`, `teacher_feature_keys_for_pages()` |
| `global_config.json` | `features` | Bật mặc định `canvas_soankhbd: true`, `canvas_soanlotrinh: true`, `canvas_sangkien: true` |
| `tests/canvas-tabs-permissions-smoke.js` | Tệp mới | Smoke test kiểm tra đăng ký đầy đủ 3 tab trên admin/index/api/config, và kiểm tra cơ chế modal setting |

---

## III. Kế Hoạch Kiểm Thử (Verification Plan)

### 1. Kiểm thử tự động
- Chạy smoke test mới:
  ```powershell
  node tests/canvas-tabs-permissions-smoke.js
  ```
- Chạy lại các smoke test hiện hành để bảo đảm không có regression:
  ```powershell
  node tests/teacher-permissions-smoke.js
  node tests/user-ai-settings-smoke.js
  node tests/duyetgiaoan-integration-smoke.js
  ```

### 2. Kiểm thử hợp đồng phân quyền
- Giáo viên KHÔNG có quyền `canvas_soankhbd`: Thẻ `[data-tool="canvas_soankhbd"]` có class `.hidden` trên `index.html`.
- Giáo viên ĐƯỢC cấp quyền `canvas_soankhbd`: Thẻ hiển thị bình thường và link đúng tới `https://gemini.google.com/app/74fb6bf46c11076a?hl=vi` (`target="_blank"`).
- Tương tự cho `canvas_soanlotrinh` và `canvas_sangkien`.
- Nút "Cài đặt AI & Key" mở modal setting với 2 tab; tab Tổng quan hiển thị đầy đủ thông tin giáo viên, lớp phụ trách và nhúng thống kê AI hôm nay.
