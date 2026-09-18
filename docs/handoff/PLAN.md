# PLAN: Nâng Cấp Giao Diện Padlet — Tùy Chọn Màu Chữ Tiêu Đề Và Cho Phép Tác Giả Chỉnh Sửa Bài Đăng, Hiển Thị Nhiều Ảnh

## Hiện trạng
1. **Tiêu đề bảng bị điệp màu trên nền tối / màu nền tùy biến**:
   - Hiện tại, class `body.board-light .board-title-input` ([padlet_ht.html:161](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/padlet_ht.html#L161)) mặc định gán màu chữ `#0f172a` (xanh đen tối).
   - Khi bảng sử dụng nền có tông màu sẫm (như đỏ rượu `board-bg-rose`, tím đậm `board-bg-violet`, xanh đậm `board-bg-blue`...), chữ tiêu đề `TOÁN LỚP 9/1` màu đen/xanh đen bị chìm hoàn toàn vào màu nền (bị điệp màu, không nhìn rõ như ảnh minh họa của người dùng).
   - Trong giao diện bảng và modal cài đặt ([padlet_ht.html:512](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/padlet_ht.html#L512)), tác giả chỉ có thể chọn `color_mode` là "Sáng" hoặc "Tối", chưa có bảng màu/bộ chọn màu sắc (color picker / palette) để chủ động chọn màu chữ tiêu đề theo ý muốn (trắng, vàng, xanh sáng, hồng, đỏ...).

2. **Bài đăng thiếu nút "Sửa" và chỉ hiển thị tối đa 1 hình ảnh**:
   - Khung nút hành động của bài đăng ([padlet_ht.html:1727-1741](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/padlet_ht.html#L1727-L1741)) hiện chỉ có các nút: `Duyệt`/`Từ chối` (nếu chờ duyệt), `Ghim`/`Bỏ ghim` (giáo viên), và `Xóa` (`moderate(p.id, 'delete')`).
   - Hoàn toàn **chưa có nút "Sửa"** cho tác giả bài viết hoặc giáo viên quản lý chỉnh sửa lại nội dung bài đăng sau khi đã tạo.
   - Hàm `attachmentHero` ([padlet_ht.html:1702-1708](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/padlet_ht.html#L1702-L1708)) hiện dùng `(p.files || []).find(isImageFile)`: chỉ lấy đúng **1 hình ảnh đầu tiên** để hiển thị dạng ảnh bìa/ảnh lớn. Nếu tác giả đính kèm thêm 2, 3, 4 ảnh thì các ảnh sau bị đẩy xuống mục tệp đính kèm phụ dưới dạng nút text có tên file (`otherFiles`), không hiển thị được trực quan hình ảnh trên bài đăng.
   - Phía backend ([api/padlet.php](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/api/padlet.php)) chưa có API cho thao tác chỉnh sửa bài viết (`action === 'edit-post'`).

---

## Phạm vi
1. **Tùy biến màu chữ tiêu đề bảng**:
   - Thêm cột `title_color` (VARCHAR(30) DEFAULT NULL) vào bảng `padlet_boards` thông qua `padlet_migrate` trong [api/padlet.php](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/api/padlet.php).
   - Cho phép chọn màu chữ tiêu đề trực tiếp từ giao diện:
     + Trong modal cài đặt bảng (Tab Giao diện / Bảng màu): Thêm bảng màu chọn nhanh (Trắng, Đen, Vàng, Xanh dương, Xanh lá, Hồng, Cam...) kèm ô chọn màu tùy ý (`<input type="color">`).
     + Nút chọn màu nhanh dạng icon bảng màu (palette) cạnh ô nhập tiêu đề trên thanh header khi tác giả/giáo viên đang xem bảng.
   - Hiển thị màu chữ tiêu đề bảng theo giá trị `title_color` được lưu (áp dụng inline style hoặc class, ưu tiên cao hơn màu mặc định để không bị điệp màu trên bất kỳ nền nào).

2. **Chức năng Chỉnh sửa bài đăng (Edit Post)**:
   - Thêm nút **`Sửa`** (`<button onclick="openEditPostModal(...)">`) trên mỗi thẻ bài đăng cho người có quyền (`state.canManage || p.can_delete`).
   - Modal chỉnh sửa bài viết: Cho phép sửa nội dung chữ (`body`), liên kết (`link_url`), màu thẻ (`card_color`), quản lý danh sách ảnh/tệp hiện có (có nút xóa tệp cũ), và tải thêm hình ảnh/tệp mới.
   - Thêm endpoint `action === 'edit-post'` trong [api/padlet.php](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/api/padlet.php): Xác thực quyền tác giả (`$isAuthor`) hoặc chủ bảng (`$isOwner`), cập nhật dữ liệu và lưu tệp bổ sung vào `padlet_post_files`.

3. **Hiển thị thư viện ảnh (Image Gallery / Grid) trên bài đăng**:
   - Nâng cấp hàm render ảnh trong [padlet_ht.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/padlet_ht.html):
     + Lọc toàn bộ các tệp là ảnh (`(p.files || []).filter(isImageFile)`).
     + Nếu có 1 ảnh: hiển thị 1 ảnh full width.
     + Nếu có từ 2 ảnh trở lên: hiển thị dạng lưới ảnh (grid 2 cột hoặc 3 cột với tỉ lệ khung hình đồng đều, bo góc đẹp mắt), bấm vào bất kỳ ảnh nào đều mở xem kích thước lớn (preview modal).

4. **Kiểm thử**:
   - Cập nhật và bổ sung test cases trong `tests/padlet-ownership-smoke.js` và `tests/padlet-ui-smoke.js`.

---

## Ngoài phạm vi
- Không thay đổi các quyền phân quyền cơ bản (học sinh chỉ sửa/xóa bài của chính mình, giáo viên quản lý toàn bộ).
- Không sửa đổi các template cấu trúc bảng khác (Mindmap, KWL, Venn...) ngoài việc đồng bộ hiển thị ảnh và nút sửa.

---

## File dự kiến tác động
1. `padlet_ht.html`
2. `api/padlet.php`
3. `tests/padlet-ui-smoke.js`
4. `tests/padlet-ownership-smoke.js`

---

## Các bước thực hiện

### Bước 1: Backend [api/padlet.php](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/api/padlet.php)
1. Thêm migration trong `padlet_migrate`:
   ```php
   if (!padlet_column_exists($pdo, 'padlet_boards', 'title_color')) {
       $pdo->exec("ALTER TABLE padlet_boards ADD COLUMN title_color VARCHAR(30) DEFAULT NULL AFTER color_mode");
   }
   ```
2. Cập nhật `action === 'save-board'`: Lưu và validate trường `title_color` (chuỗi mã màu hex hoặc tên màu hợp lệ, tối đa 30 ký tự).
3. Thêm `action === 'edit-post'`:
   - Nhận `post_id`, `body`, `link_url`, `card_color`, `deleted_file_ids` (mảng id tệp muốn xóa), và các tệp upload mới `padlet_file_input()`.
   - Kiểm tra quyền: `$isOwner || $isAuthor`.
   - Cập nhật thông tin bài đăng, xóa tệp cũ theo `deleted_file_ids`, lưu tệp tải lên mới vào Google Drive/DB.

### Bước 2: Frontend [padlet_ht.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/padlet_ht.html) — Màu chữ tiêu đề
1. Thêm `title_color` vào state, render tiêu đề bảng:
   ```html
   style="${b.title_color ? `color: ${esc(b.title_color)} !important; caret-color: ${esc(b.title_color)};` : ''}"
   ```
2. Thêm bộ chọn màu tiêu đề trong `settingsAppearance`: Bảng màu các màu tương phản cao (Trắng `#ffffff`, Đen `#0f172a`, Vàng `#facc15`, Xanh cyan `#38bdf8`, Xanh lá `#4ade80`, Hồng `#f472b6`, Cam `#fb923c`...) + ô `input type="color"`.
3. Bổ sung nút đổi màu nhanh dạng icon bảng màu (palette) cạnh ô tiêu đề trên header khi có quyền quản trị để thao tác 1 chạm.

### Bước 3: Frontend [padlet_ht.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/padlet_ht.html) — Sửa bài và hiển thị nhiều ảnh
1. Cải tiến `attachmentHero` / hiển thị ảnh trên bài đăng:
   - Gom tất cả `const imageFiles = (p.files || []).filter(isImageFile);`.
   - Nếu `imageFiles.length === 1`: hiển thị 1 ảnh như cũ.
   - Nếu `imageFiles.length > 1`: hiển thị lưới ảnh `grid grid-cols-2 gap-1.5 rounded-t-2xl overflow-hidden mb-3`, mỗi ảnh click mở preview.
2. Thêm nút **`Sửa`** vào `postCard`:
   - Nút nằm cạnh nút `Xóa` khi `state.canManage || p.can_delete`.
3. Thêm modal `editPostModal` và hàm `openEditPostModal(postId)`:
   - Điền sẵn nội dung, màu thẻ, danh sách tệp đính kèm (cho phép bấm xóa từng tệp).
   - Thêm input đính kèm file/ảnh mới (hỗ trợ chọn nhiều ảnh hoặc paste từ clipboard).
   - Gửi yêu cầu tới `API` với `action=edit-post`.

### Bước 4: Kiểm thử và xác nhận
1. Chạy các bài test:
   ```powershell
   node tests/padlet-ui-smoke.js
   node tests/padlet-ownership-smoke.js
   ```
2. Đảm bảo toàn bộ tiêu chí kiểm thử pass 100%.

---

## Rủi ro
1. **Bảo mật quyền sửa bài**: Phải kiểm tra chặt chẽ `isOwner || isAuthor` trên server PHP theo user ID, không tin tưởng dữ liệu client gửi lên.
2. **Xóa tệp Google Drive**: Khi tác giả xóa ảnh cũ trong lúc sửa bài, cần xóa an toàn trong `padlet_post_files` và dọn dẹp Drive tương tự như xóa bài.

---

## Cách kiểm thử
Chạy các lệnh terminal:
```powershell
node tests/padlet-ui-smoke.js
node tests/padlet-ownership-smoke.js
```

---

## Tiêu chí nghiệm thu
1. Tác giả có thể chọn bất kỳ màu sắc nào cho tiêu đề `TOÁN LỚP 9/1` (bằng bảng màu hoặc color picker), tiêu đề hiển thị rõ ràng, không bị điệp màu trên nền đỏ hay bất kỳ nền nào.
2. Trên thẻ bài đăng có nút **`Sửa`** cho tác giả/giáo viên.
3. Khi sửa bài, tác giả cập nhật được nội dung và chèn thêm được hình ảnh/tệp mới.
4. Khi bài đăng có nhiều hình ảnh, tất cả các hình ảnh đều được hiển thị trực quan dạng lưới ảnh trên thẻ bài thay vì chỉ hiện 1 ảnh.
5. Kiểm thử `padlet-ui-smoke.js` và `padlet-ownership-smoke.js` pass 100%.
