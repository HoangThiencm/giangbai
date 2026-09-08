# KẾ HOẠCH BÀN GIAO TRIỂN KHAI (HANDOFF PLAN)
## Khắc phục lỗi: Cấp quyền 1 chức năng nhưng giáo viên đăng nhập lại nhận Full chức năng

---

## 1. Hiện trạng & Phản ánh từ Người dùng
- **Phản ánh từ User**:
  > *"hiện tại khi tôi mở admin phân quyền cho 1 user đăng ký, tôi cấp 1 năm sử dụng và tôi mở chức năng vẽ hình AI hoặc bất kỳ 1 chức năng khác cho họ xài thì khi họ đăng nhập lại sử dụng toàn bộ các chức năng (full)."*

---

## 2. Khảo sát Gốc rễ Mã nguồn (Root Cause Analysis)

Qua rà soát toàn bộ chu trình Đăng ký -> Duyệt/Cấp quyền Admin -> Đăng nhập -> Kiểm soát quyền truy cập, phát hiện **5 gốc rễ** dẫn đến hiện tượng bị mở Full tính năng:

### Gốc rễ 1: Cơ chế tự động "nâng cấp ngầm" (Auto-upgrade) tự ý bung full 20 công cụ
- **Vị trí 1 - `api/helpers.php` (`maybe_upgrade_teacher_allowed_pages`, dòng 306–314)**:
  ```php
  // GV đã có lộ trình + tab quản lý nhưng DB thiếu mã công cụ (Thi Online, Ma trận…)
  if ($hasLotrinh && $hasTeacherHub && !$hasTools) {
      $fromFeatures = teacher_tool_pages_from_user_features((string)($user['username'] ?? ''));
      $upgraded = normalize_pages(array_merge(
          $upgraded,
          $fromFeatures ?: $toolPages
      ));
  }
  ```
  Khi tài khoản có lộ trình (vốn bị ép mặc định là Toán 6) VÀ có 1 tính năng quản trị (`quanlyvanban`, `theodoiai`, `thongketientrinh`), hệ thống coi là "thiếu công cụ" và tự động nhét toàn bộ 20 công cụ của `teacher_workspace_page_ids()` vào `allowed_pages_json` rồi ghi đè thẳng vào MySQL database!
- **Vị trí 2 - `admin.html` (`ensureTeacherToolPages`, dòng 2676–2688)**:
  ```javascript
  function ensureTeacherToolPages(allowedPages) {
      ...
      if (!hasLotrinh || !hasHub || hasTool) return pages;
      CLIENT_FEATURE_CHECKS.forEach(id => {
          if (!pages.includes(id)) pages.push(id);
      });
      return pages;
  }
  ```
  Nếu Admin cấp quyền quản lý (như Quản lý văn bản) mà chưa chọn công cụ giảng dạy nào, hàm này tự động nhồi toàn bộ danh sách `CLIENT_FEATURE_CHECKS` (20 công cụ) vào payload lưu lên server!
- **Vị trí 3 - `index.html` (`applyTeacherAllowedPagesVisibility`, dòng 994–997)**:
  ```javascript
  const grantWorkspaceTools = teacherHasWorkspaceHub(allowedSet) && !teacherHasAnyToolPage(allowedSet);
  Object.entries(TOOL_PAGE_LINKS).forEach(([tool]) => {
      const allowed = allowedSet.has(tool) || grantWorkspaceTools;
      ...
  ```
  Giao diện phía client tự động coi tất cả các công cụ là được phép nếu giáo viên có lộ trình và hub quản lý.

### Gốc rễ 2: Ép mặc định `lotrinhtoan6` cho mảng quyền rỗng `[]`
- **Vị trí 1 - `api/helpers.php` (`normalize_pages`, dòng 180)**:
  ```php
  return array_values(array_unique($clean)) ?: ['lotrinhtoan6'];
  ```
  Khi user mới đăng ký, `allowed_pages_json` trong DB là `[]`. Hàm `normalize_pages` tự động đổi mảng rỗng thành `['lotrinhtoan6']`.
- **Vị trí 2 - `admin.html` (`openStudentConfig`, dòng 3116)**:
  ```javascript
  renderPageChecks('editAllowedPages', editingStudent.allowed_pages || ['lotrinhtoan6'], editingStudent.role || 'student');
  ```
  Ô "Lộ trình tự học Toán 6" bị **tự động tick sẵn (CHECKED)** ngay khi Admin mở form. Admin không hề muốn cấp lộ trình nhưng hệ thống đã coi là có lộ trình, kết hợp với Gốc rễ 1 kích hoạt chuỗi tự động bung full công cụ.

### Gốc rễ 3: Xung đột và đồng bộ thất bại giữa 2 kho quyền (`MySQL users.allowed_pages_json` vs `global_config.json: user_features`)
- **Vị trí 1 - `admin.html` (`syncTeacherUserFeaturesFromPages`, dòng 2660–2664)**:
  Cố ghi quyền vào `global_config.json` qua `api/global_config.php`. Nếu hosting phân quyền không cho ghi file, khối `try...catch` nuốt chửng lỗi (`console.warn`).
- **Vị trí 2 - `index.html` (`mergeAccountFeatures`, dòng 914–919)**:
  Do `global_config.json` không lưu được tài khoản mới, `config.user_features[account]` rỗng. Hàm lấy fallback từ `config.features` toàn cục (vốn đặt tất cả là `true`!).
- **Vị trí 3 - `api/helpers.php` (`teacher_allowed_pages_resolved`, dòng 162–165)**:
  Tự ý `array_merge` quyền từ `user_features` vào `allowed_pages` từ database, gây xung đột và làm mất tính độc lập của bảng MySQL `users`.
- **Giải pháp**: MySQL `users.allowed_pages_json` là **nguồn sự thật duy nhất (Single Source of Truth)** cho phân quyền tài khoản trên Hosting. Không để `global_config.json` can thiệp hay tự động cấp thêm quyền.

### Gốc rễ 4: `access-control.js` thiếu hàng loạt công cụ giáo viên mới trong danh sách chặn
- **Vị trí - `access-control.js` (dòng 20–38 & dòng 276–283)**:
  ```javascript
  const teacherWorkspaceTools = ['gslides', 'vehinh', 'smartquiz', 'matrande', 'tronde', 'thitructuyen', 'kttx', 'nopbai', 'padlet', 'vietbaocao', 'thoikhoabieu'];
  ```
  - Danh sách hoàn toàn **thiếu 7 công cụ**: `soankhbd`, `taovideo`, `xaydungphuluc`, `duyetgiaoan`, `duyetde`, `nghiencuubaihoc`, `thanhtich`.
  - Thậm chí `soankhbd.html` còn không được khai báo trong `pageKeys`.
  - Hậu quả: Dù Admin không cấp quyền các công cụ này, giáo viên mở trực tiếp link (hoặc click từ menu) vẫn vào được 100%, không hề bị chặn hay cảnh báo!

### Gốc rễ 5: Giao diện `index.html` hiển thị toàn bộ thẻ công cụ ở HTML tĩnh trước khi lọc
- **Vị trí - `index.html` (dòng 1185–1405 & dòng 1013–1017)**:
  Các thẻ trong `#mainToolsGrid` ban đầu không có class `hidden`. Nếu tài khoản giáo viên có `allowedSet` rỗng hoặc xử lý lọc gặp lỗi, `resetMainToolsGridVisibility()` xóa class `hidden` và không ẩn các thẻ chưa được cấp, khiến người dùng nhìn thấy và bấm được toàn bộ công cụ.

---

## 3. Phạm vi Triển khai (Scope)
- **Thuộc phạm vi (In Scope)**:
  1. `api/helpers.php`:
     - Sửa `normalize_pages`: Cho phép trả về mảng rỗng `[]` khi đầu vào rỗng (không tự ép `['lotrinhtoan6']` cho giáo viên).
     - Xóa bỏ hoàn toàn logic auto-grant full công cụ trong `maybe_upgrade_teacher_allowed_pages`.
     - `teacher_allowed_pages_resolved`: Lấy chuẩn 100% từ `users.allowed_pages_json` trong MySQL.
  2. `admin.html`:
     - Sửa `ensureTeacherToolPages`: Không tự động nhét toàn bộ `CLIENT_FEATURE_CHECKS` vào quyền của giáo viên. Giữ đúng những gì Admin đã tick chọn.
     - Sửa `openStudentConfig` & `renderTeacherPageToggles`: Không tự động tick sẵn `lotrinhtoan6` nếu tài khoản đang có `allowed_pages` rỗng.
     - Đảm bảo Admin cấp đúng chức năng nào thì lưu chính xác chức năng đó.
  3. `access-control.js`:
     - Bổ sung `'soankhbd.html': 'soankhbd'` vào `pageKeys` và `pageUrls`.
     - Cập nhật `teacherWorkspaceTools` đầy đủ tất cả các công cụ giáo viên (bao gồm `soankhbd`, `xaydungphuluc`, `duyetgiaoan`, `duyetde`, `nghiencuubaihoc`, `thanhtich`, `taovideo`).
     - Đảm bảo bất kỳ trang nào không có trong `allowedPages` đều bị chặn và redirect về `index.html`.
  4. `index.html`:
     - Xóa bỏ cờ `grantWorkspaceTools` trong `applyTeacherAllowedPagesVisibility`.
     - Công cụ chỉ hiển thị nếu `allowedSet.has(tool)` là TRUE.
     - Đảm bảo tài khoản giáo viên chỉ nhìn thấy đúng những công cụ được Admin bật.
  5. Viết bộ kiểm thử tự động (Smoke Test) để thẩm định chu trình phân quyền giáo viên.
- **Ngoài phạm vi (Out of Scope)**:
  - Không thay đổi cơ chế phân quyền của học sinh (`role === 'student'`).
  - Không thay đổi cấu trúc bảng CSDL `users` (dùng nguyên cột `allowed_pages_json`).

---

## 4. Danh sách File Tác động (Target Files)
1. `api/helpers.php`
2. `admin.html`
3. `access-control.js`
4. `index.html`
5. `tests/teacher-permissions-smoke.js` (Tạo mới để kiểm thử)

---

## 5. Kế hoạch Triển khai Chi tiết cho ChatGPT (Step-by-step Implementation Plan)

### Bước 1: Chuẩn hóa logic cấp quyền tại Backend (`api/helpers.php`)
1. **Sửa hàm `normalize_pages`**:
   - Hiện tại:
     ```php
     function normalize_pages($pages): array
     {
         $catalog = page_catalog();
         $aliases = ['lotrinh' => 'lotrinhtoan6'];
         if (!is_array($pages)) return ['lotrinhtoan6'];
         $clean = [];
         foreach ($pages as $page) {
             $page = $aliases[$page] ?? $page;
             if (isset($catalog[$page])) $clean[] = $page;
         }
         return array_values(array_unique($clean)) ?: ['lotrinhtoan6'];
     }
     ```
   - Chuyển thành: Thêm tham số `$defaultToLotrinh6 = false` (hoặc khi mảng rỗng thì trả về `[]`, chỉ học sinh hoặc khi gọi chỉ định mới fallback `lotrinhtoan6`). Cụ thể:
     ```php
     function normalize_pages($pages, bool $allowEmpty = true): array
     {
         $catalog = page_catalog();
         $aliases = ['lotrinh' => 'lotrinhtoan6'];
         if (!is_array($pages)) return $allowEmpty ? [] : ['lotrinhtoan6'];
         $clean = [];
         foreach ($pages as $page) {
             $page = $aliases[$page] ?? $page;
             if (isset($catalog[$page])) $clean[] = $page;
         }
         $unique = array_values(array_unique($clean));
         if (empty($unique) && !$allowEmpty) {
             return ['lotrinhtoan6'];
         }
         return $unique;
     }
     ```
2. **Sửa hàm `teacher_allowed_pages_resolved`**:
   - Nguồn sự thật cho phân quyền giáo viên là trường `allowed_pages_json` trong MySQL.
   - Không tự ý lấy cờ từ `global_config.json` để ghi đè hay merge thêm quyền công cụ nếu Admin đã cấu hình trong DB:
     ```php
     function teacher_allowed_pages_resolved(array $user): array
     {
         $raw = json_decode($user['allowed_pages_json'] ?? '[]', true);
         $pages = normalize_pages(is_array($raw) ? $raw : [], true);
         return $pages;
     }
     ```
3. **Sửa hàm `maybe_upgrade_teacher_allowed_pages`**:
   - Loại bỏ hoàn toàn khối tự động cấp full công cụ:
     ```php
     // XÓA BỎ HOẶC VÔ HIỆU HÓA KHỐI:
     // if ($hasLotrinh && $hasTeacherHub && !$hasTools) { ... $upgraded = normalize_pages(array_merge($upgraded, $toolPages)); }
     ```
   - Chỉ giữ việc chuẩn hóa mảng và đảm bảo cấu trúc hợp lệ, không tự động thêm bất kỳ trang nào ngoài những gì Admin đã lưu.

---

### Bước 2: Chuẩn hóa trang Quản trị viên (`admin.html`)
1. **Sửa hàm `ensureTeacherToolPages` (dòng 2676–2688)**:
   - Hiện tại hàm này tự động inject tất cả `CLIENT_FEATURE_CHECKS` nếu giáo viên có `hasLotrinh && hasHub && !hasTool`.
   - Cần sửa để trả về đúng `allowedPages` mà Admin chọn, tuyệt đối không tự chèn thêm công cụ:
     ```javascript
     function ensureTeacherToolPages(allowedPages) {
         return Array.isArray(allowedPages) ? [...allowedPages] : [];
     }
     ```
2. **Sửa hàm `openStudentConfig` và `renderPageChecks`**:
   - Tại dòng 3116:
     ```javascript
     // Trước:
     renderPageChecks('editAllowedPages', editingStudent.allowed_pages || ['lotrinhtoan6'], editingStudent.role || 'student');
     // Sau: Nếu role là teacher, giữ nguyên mảng allowed_pages (kể cả rỗng []), không fallback về ['lotrinhtoan6']
     const initialPages = editingStudent.role === 'teacher'
         ? (Array.isArray(editingStudent.allowed_pages) ? editingStudent.allowed_pages : [])
         : (editingStudent.allowed_pages || ['lotrinhtoan6']);
     renderPageChecks('editAllowedPages', initialPages, editingStudent.role || 'student');
     ```
3. **Sửa `renderTeacherPageToggles` (dòng 2574–2575)**:
   - Không ép `selectedPages || ['lotrinhtoan6']`:
     ```javascript
     const normalizedPages = (Array.isArray(selectedPages) ? selectedPages : []).map(page => page === 'lotrinh' ? 'lotrinhtoan6' : page);
     const selected = new Set(normalizedPages);
     ```
4. **Kiểm tra lưu cấu hình (`saveUserConfig`)**:
   - Khi Admin chỉ chọn `vehinh` (Vẽ hình học AI), `allowedPages` gửi lên `api/admin_students.php` chỉ chứa đúng `['vehinh']`.

---

### Bước 3: Hoàn thiện lá chắn bảo vệ Route (`access-control.js`)
1. **Bổ sung `soankhbd.html` vào `pageKeys` và `pageUrls`**:
   ```javascript
   // Trong pageKeys:
   'soankhbd.html': 'soankhbd',
   // Trong pageUrls:
   soankhbd: 'soankhbd.html',
   ```
2. **Cập nhật đầy đủ mảng `teacherWorkspaceTools` (dòng 276)**:
   ```javascript
   const teacherWorkspaceTools = [
       'gslides', 'vehinh', 'smartquiz', 'matrande', 'tronde',
       'thitructuyen', 'kttx', 'nopbai', 'padlet', 'vietbaocao',
       'thoikhoabieu', 'phancongtochuyenmon', 'rutgon', 'thanhtich',
       'soankhbd', 'taovideo', 'xaydungphuluc', 'duyetgiaoan', 'duyetde', 'nghiencuubaihoc'
   ];
   ```
3. Đảm bảo nếu `role === 'teacher'` mà truy cập vào bất kỳ trang nào trong `teacherWorkspaceTools` mà không có trong `allowedPages`, lập tức bị chặn:
   ```javascript
   if (role === 'teacher' && teacherWorkspaceTools.includes(pageKey)) {
       if (!canOpenPage(pageKey, allowedPages)) {
           alert('Tài khoản chưa được admin cấp quyền mở công cụ này.');
           window.location.href = 'index.html';
           return;
       }
       return;
   }
   ```

---

### Bước 4: Chuẩn hóa hiển thị giao diện Portal (`index.html`)
1. **Xóa bỏ cơ chế `grantWorkspaceTools` (dòng 994)**:
   ```javascript
   function applyTeacherAllowedPagesVisibility(allowedSet, features) {
       if (localStorage.getItem('userRole') !== 'teacher') return;
       Object.entries(TOOL_PAGE_LINKS).forEach(([tool]) => {
           // Quyền công cụ chỉ được bật khi allowedSet THỰC SỰ có mã công cụ đó
           const allowed = allowedSet.has(tool);
           const visible = allowed && features[tool] !== false;
           setToolCardsVisible(`#mainToolsGrid > [data-tool="${tool}"]`, visible);
       });
       const hasLotrinh = LOTRINH_PAGE_KEYS.some(key => allowedSet.has(key));
       setToolCardsVisible('[data-tool="teacher-lotrinh-design"]', hasLotrinh && features.teacher_design !== false);
       setToolCardsVisible('[data-tool="teacher-documents"]', allowedSet.has('quanlyvanban'));
       setToolCardsVisible(
           'a[href="thongketientrinh.html"]',
           allowedSet.has('thongketientrinh') && features.teacher_progress_stats !== false
       );
       setToolCardsVisible(
           'a[href="theodoi-ai.html"]',
           allowedSet.has('theodoiai') && features.teacher_ai_stats !== false
       );
   }
   ```
2. **Sửa `applyTeacherHubVisibility` khi `allowedSet` rỗng**:
   - Nếu giáo viên chưa được cấp quyền nào (`allowedSet.size === 0`), ẩn toàn bộ thẻ công cụ và hiển thị thông báo "Chưa mở công cụ giảng dạy — liên hệ Admin để cấp quyền".
3. **Sửa `augmentTeacherAllowedSet` (dòng 942–957)**:
   - Không tự ý thêm tool vào `set` từ `global_config.json` nếu DB không có. Quyền từ DB MySQL (`allowedPages`) là quyết định cao nhất.

---

### Bước 5: Kiểm thử và Thẩm định Tự động
Tạo file kiểm thử `tests/teacher-permissions-smoke.js` dùng Node.js để kiểm tra tính toàn vẹn:
1. `access-control.js` chứa đầy đủ 20 công cụ trong `teacherWorkspaceTools` và có `soankhbd.html` trong `pageKeys`.
2. `admin.html` không chứa logic tự động nhồi full tool `CLIENT_FEATURE_CHECKS` trong `ensureTeacherToolPages`.
3. `api/helpers.php` không tự động gộp `$toolPages` trong `maybe_upgrade_teacher_allowed_pages`.
4. `index.html` không sử dụng cờ `grantWorkspaceTools` để ép mở thẻ.
5. Chạy `node tests/teacher-permissions-smoke.js` để xác nhận PASS 100%.

---

## 6. Kế hoạch Kiểm thử & Xác minh (Verification Plan)
1. **Kiểm tra tĩnh**: Chạy file test `tests/teacher-permissions-smoke.js`.
2. **Kiểm tra hành vi**:
   - Giả lập tài khoản giáo viên mới được cấp `['vehinh']`:
     * Truy cập `index.html`: Chỉ duy nhất thẻ "Vẽ hình học AI" hiển thị trong danh sách công cụ. Các thẻ khác (Soạn KHBD, Thi trực tuyến, Trình chiếu slides...) đều có class `hidden`.
     * Truy cập trực tiếp `soankhbd.html` hoặc `gslides.html`: Bị `access-control.js` chặn lại, bật alert thông báo chưa cấp quyền và chuyển về `index.html`.
     * Truy cập `vehinh.html`: Vào sử dụng bình thường.
