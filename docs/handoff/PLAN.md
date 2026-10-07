# PLAN: THÊM NÚT "THÊM BÌNH LUẬN" VÀ CHUẨN HÓA ĐỊNH DANH NGƯỜI BÌNH LUẬN TRONG PADLET

## Hiện trạng
1. **Thanh thao tác trên thẻ bài viết (`postCard` trong `padlet_ht.html`):**
   - Hiện tại, cụm nút hành động (`actions`) dưới chân bài viết chỉ hiển thị khi `state.canManage || p.can_delete` (gồm: Duyệt, Từ chối, Ghim/Bỏ ghim, Sửa, Xóa).
   - Nút xem/mở bình luận chỉ là một nút đếm nhỏ `💬 [số]` nằm ở khối tương tác `social` (chung với nút cảm xúc) phía trên dòng thông tin tác giả, chưa có nút chữ rõ ràng "Thêm bình luận" ở hàng thao tác Ghim/Sửa/Xóa.
   - Người xem thông thường (học sinh, phụ huynh, khách vãng lai qua liên kết bảng chia sẻ) nếu không có quyền quản lý hay xóa bài thì không thấy thanh thao tác, khó nhận biết cách bình luận.
2. **Khâu định danh người bình luận (`commentModal` trong `padlet_ht.html`):**
   - Ô nhập Họ tên người bình luận `<input id="commentAuthor">` chưa có thuộc tính `required` ở client-side form HTML, chưa có nhãn hướng dẫn rõ ràng.
   - Hệ thống chưa lưu nhớ thông tin khách bình luận vào `localStorage`, khiến mỗi lần bình luận bài viết khác nhau người dùng đều phải gõ lại từ đầu.
   - Khi người dùng đăng nhập tài khoản hệ thống (`state.user`), modal chưa có khối thông báo trực quan "Bình luận với tư cách: [Họ tên]".
   - Danh sách bình luận hiển thị thông tin tác giả bình luận còn sơ sài, chưa nổi bật danh tính (tên, vai trò/lớp) để giáo viên và người xem nhận biết ngay là ai.

---

## Mục tiêu & Phạm vi
1. **Bổ sung nút "Thêm bình luận" vào hàng thao tác thẻ bài viết:**
   - Trong `postCard(p)`: Khi bảng cho phép bình luận (`b.comments_enabled`), hiển thị nút **"Thêm bình luận"** (kèm icon `far fa-comment-dots`) tại thanh nút hành động cùng hàng với Ghim, Sửa, Xóa.
   - Bất kỳ ai xem bảng (kể cả khách vãng lai, học sinh chưa đăng nhập) đều nhìn thấy nút "Thêm bình luận" nếu bảng đang bật tính năng bình luận (`b.comments_enabled`).
   - Khi bấm "Thêm bình luận", kích hoạt hàm `openComments(p.id)`.
   - Giữ nguyên toàn bộ logic phân quyền an toàn cho Duyệt, Từ chối, Ghim, Sửa, Xóa (đảm bảo 100% qua `padlet-ownership-smoke.js`).
2. **Định danh bắt buộc và tối ưu trải nghiệm nhập thông tin người bình luận ("để biết là ai"):**
   - Đối với tài khoản đã đăng nhập: Hiển thị rõ danh tính đang đăng nhập trong modal bình luận.
   - Đối với khách vãng lai / học sinh chưa đăng nhập:
     - Bắt buộc nhập Họ và tên (thêm `required`, placeholder rõ nghĩa "Họ và tên của bạn * (bắt buộc)").
     - Bổ sung ô nhập "Vai trò / Lớp" (placeholder "Lớp / Đơn vị / Vai trò (VD: Lớp 6A, Phụ huynh...)").
     - Tự động nhớ danh tính vào `localStorage` (`padlet_guest_name`, `padlet_guest_role`) và tự động điền sẵn (pre-fill) khi mở modal bình luận.
     - Đồng bộ với tên khách đăng bài (nếu đã từng nhập khi đăng bài).
     - Kiểm tra client-side trước khi submit: nếu để trống họ tên thì chặn gửi, cảnh báo toast và tự động focus vào ô nhập họ tên.
3. **Nâng cấp hiển thị danh sách bình luận (`commentsList`):**
   - Hiển thị rõ ràng tên người bình luận (chữ đậm nổi bật), badge vai trò/lớp, avatar ký tự đầu, và thời gian bình luận.
4. **Smoke test:**
   - Đảm bảo các test hiện hữu `tests/padlet-ownership-smoke.js` và `tests/padlet-ui-smoke.js` đều PASS.
   - Bổ sung kiểm tra smoke test cho tính năng nút "Thêm bình luận" và định danh bình luận.

---

## File tác động
1. `padlet_ht.html`:
   - Hàm `postCard(p)`: Bổ sung nút "Thêm bình luận" vào khối `actions`, hiển thị khi `b.comments_enabled`.
   - Modal `#commentModal`: Cải tiến giao diện form nhập thông tin, thêm badge người dùng đăng nhập, nhãn định danh.
   - Hàm `openComments(id)`: Nạp danh sách kèm giao diện định danh rõ ràng, autofill thông tin từ `localStorage`.
   - Hàm `submitComment(e)`: Kiểm tra họ tên bắt buộc, lưu `localStorage` khi gửi thành công.
2. `tests/padlet-comment-ui-smoke.js` (hoặc cập nhật `tests/padlet-ui-smoke.js`):
   - Bổ sung smoke test kiểm tra sự hiện diện của nút "Thêm bình luận", kiểm tra validation họ tên và lưu nhớ `localStorage`.

---

## Các bước thực hiện chi tiết cho Coder

### Bước 1: Cập nhật hàm `postCard(p)` trong `padlet_ht.html`
1. Xác định điều kiện hiển thị thanh hành động dưới chân thẻ bài:
   - Thanh hành động hiển thị khi: `state.canManage || p.can_delete || b.comments_enabled`.
2. Tạo nút "Thêm bình luận":
   ```javascript
   const commentBtn = b.comments_enabled ? `
       <button type="button" onclick="openComments(${p.id})" class="rounded-lg bg-teal-50 px-3 py-2 font-bold text-teal-800 hover:bg-teal-100">
           <i class="far fa-comment-dots mr-1"></i>Thêm bình luận
       </button>` : '';
   ```
3. Đặt `commentBtn` vào thanh `post-action` cùng với các nút Ghim, Sửa, Xóa:
   - Lưu ý giữ nguyên cấu trúc điều kiện của Ghim: `${state.canManage ? `<button type="button" onclick="moderate(${p.id},'pin')"...` : ''}`
   - Giữ nguyên cấu trúc của Sửa và Xóa: bọc trong điều kiện `(state.canManage || p.can_delete)` để người xem bình thường chỉ thấy nút "Thêm bình luận" mà không can thiệp vào sửa/xóa/ghim.
   - Đảm bảo regex trong `tests/padlet-ownership-smoke.js` (`state.canManage || p.can_delete`) luôn khớp.

### Bước 2: Nâng cấp Form Bình luận trong `#commentModal` (`padlet_ht.html`)
1. Cập nhật phần thông tin người bình luận trong form:
   - Thêm badge danh tính khi đã đăng nhập (`#commentUserBadge`):
     ```html
     <div id="commentUserBadge" class="mb-3 hidden rounded-xl bg-teal-50 px-3.5 py-2 text-xs font-bold text-teal-800">
         <i class="fas fa-user-check mr-1.5"></i>Bình luận với tên: <span id="commentUserName" class="font-black"></span>
     </div>
     ```
   - Nâng cấp khối nhập thông tin khách (`#commentGuest`):
     ```html
     <div id="commentGuest" class="mb-3 space-y-2">
         <p class="text-xs font-bold text-slate-500">Thông tin người bình luận:</p>
         <div class="grid gap-2 sm:grid-cols-2">
             <input id="commentAuthor" class="field" placeholder="Họ và tên của bạn * (Bắt buộc)" maxlength="100">
             <input id="commentRole" class="field" placeholder="Lớp / Vai trò (VD: Lớp 6A, GV...)" maxlength="50">
         </div>
     </div>
     ```

### Bước 3: Hoàn thiện logic JS cho `openComments` và `submitComment`
1. Trong hàm `openComments(id)`:
   - Nếu đã đăng nhập (`state.user`):
     - Hiển thị `#commentUserBadge`, gán text tên người dùng.
     - Ẩn `#commentGuest`.
   - Nếu chưa đăng nhập:
     - Ẩn `#commentUserBadge`.
     - Hiển thị `#commentGuest`.
     - Điền sẵn họ tên và vai trò từ `localStorage` (`padlet_guest_name`, `padlet_guest_role` hoặc trường bài đăng `postAuthorName`).
   - Cải tiến giao diện hiển thị từng bình luận trong `commentsList`:
     - Hiển thị avatar tròn mang chữ cái đầu của tên.
     - Tên in đậm rõ ràng, tag vai trò nếu có.
     - Thời gian bình luận chi tiết.
2. Trong hàm `submitComment(e)`:
   - Lấy họ tên: nếu đã đăng nhập dùng `state.user.full_name`, nếu khách lấy từ `document.getElementById('commentAuthor').value.trim()`.
   - Nếu là khách và họ tên trống:
     - `toast('Vui lòng nhập họ và tên để gửi bình luận.');`
     - Focus vào ô `commentAuthor`.
     - Trả về (ngăn submit).
   - Khi gửi thành công:
     - Lưu họ tên và vai trò vào `localStorage.setItem('padlet_guest_name', ...)` và `localStorage.setItem('padlet_guest_role', ...)`.
     - Xóa ô nội dung bình luận `commentBody`.
     - Tải lại bảng (`loadBoard()`) và hiển thị toast thành công.

### Bước 4: Kiểm thử và xác minh (Verification)
1. Chạy lại toàn bộ test hiện hành:
   - `node tests/padlet-ownership-smoke.js` (Phải PASS).
   - `node tests/padlet-ui-smoke.js` (Phải PASS).
2. Tạo test `tests/padlet-comment-ui-smoke.js` kiểm tra:
   - Tồn tại nút "Thêm bình luận" gọi `openComments(...)` trong thẻ bài viết.
   - Modal chứa trường họ tên người bình luận và logic kiểm tra bắt buộc họ tên.
   - Cơ chế lưu trữ thông tin danh tính `localStorage`.
   - Chạy test đảm bảo PASS 100%.
