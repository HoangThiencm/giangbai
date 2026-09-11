# PLAN

## Hiện trạng

1. **Vấn đề tâm lý & trải nghiệm của giáo viên khi nộp bài qua liên kết ngoài**:
   - Khi đợt nộp yêu cầu điền vào một đường dẫn bên ngoài (Google Sheets, Google Forms, Drive...), việc nhúng khung `<iframe>` trực tiếp vào trang web thường gây chật chội, khó thao tác trên màn hình nhỏ/điện thoại và dễ gặp lỗi chặn đăng nhập tài khoản Google.
   - Ngược lại, nếu chỉ hiển thị nút mở tab mới và để nút "Nộp bài" riêng biệt ở chân trang: Giáo viên sau khi bấm mở link sang tab mới để điền dữ liệu thì **90% sẽ quên quay lại tab ban đầu để kéo xuống bấm nút "Nộp bài"**.
   - Hậu quả: Dù giáo viên đã điền xong dữ liệu trên Google Sheets, hệ thống quản trị vẫn báo giáo viên đó ở trạng thái "Chưa nộp", người quản lý vẫn phải mất thời gian đi nhắc nhở và kiểm tra thủ công.

2. **Yêu cầu cải tiến từ người dùng**:
   - Đối với trường loại Liên kết (Link), không cần nhúng iframe cồng kềnh.
   - Thiết kế cơ chế **"1 chạm"**: Khi giáo viên nhấn vào nút mở liên kết, hệ thống sẽ **mở trang mới để giáo viên nhập liệu, ĐỒNG THỜI tự động kích hoạt chức năng "Nộp bài"** trên hệ thống ngay lúc đó.

---

## Phạm vi

1. **Cập nhật giao diện nộp bài (`nopbai.html`)**:
   - Đơn giản hóa giao diện trường `link`: Không cần hiển thị khung `<iframe>` to cồng kềnh.
   - Thiết kế nút bấm hành động nổi bật:
     `[ 🚀 Nhấn vào đây để mở liên kết & Nộp bài ]` (kèm icon mở tab mới và biểu tượng xác nhận nộp).
   - Kèm ghi chú chỉ dẫn rõ ràng: *"Hệ thống sẽ tự động ghi nhận bài nộp và mở liên kết nhập liệu trong thẻ mới."*
   - Xử lý sự kiện khi nhấn nút:
     + Mở đường dẫn đích trong tab mới (`window.open(targetUrl, '_blank')`) ngay trong event click của người dùng để tránh bị trình duyệt chặn popup.
     + Tự động gán giá trị xác nhận cho trường liên kết (ví dụ: `"Đã mở và nộp qua liên kết trực tuyến"` nếu người nộp chưa gõ nội dung tùy chỉnh).
     + Tự động kích hoạt hàm gửi bài nộp `submitFiles()` lên máy chủ.
     + Nếu form có các trường bắt buộc khác (`required`): Kiểm tra tính hợp lệ trước khi gửi; nếu đã hợp lệ thì gửi ngay và mở link.
     + Chuyển sang màn hình thông báo nộp bài thành công rõ ràng:
       *"Hệ thống đã ghi nhận thời gian nộp bài của thầy/cô. Thầy/cô vui lòng hoàn thành nội dung trên trang bảng tính vừa mở."*
   - Nút "Nộp bài" ở chân trang vẫn hoạt động bình thường như phương thức nộp dự phòng.

2. **Cập nhật trình quản lý biểu mẫu (`nopbai-quanly.html`)**:
   - Trong dropdown loại trường, giữ nguyên tùy chọn **Liên kết (Link)**.
   - Cho phép quản trị viên nhập Tiêu đề chỉ tiêu và Đường dẫn URL liên kết (Google Sheets, Forms, Drive...).
   - Đơn giản hóa cấu hình: Lược bỏ checkbox nhúng iframe phức tạp, chuẩn hóa theo cơ chế mở link kèm tự động nộp bài tiện lợi.

3. **Backend API (`api/submissions.php`)**:
   - Duy trì hỗ trợ kiểu trường `'link'` trong `$types` và chuẩn hóa lưu trữ `url`.
   - Tiếp nhận dữ liệu nộp tự động từ frontend một cách trơn tru, ghi nhận trạng thái đã nộp vào database.

4. **Kiểm thử tự động (`tests/nopbai-report-link-smoke.js`)**:
   - Cập nhật bài test smoke kiểm tra sự hiện diện của cơ chế mở link và kích hoạt nộp bài tự động.

---

## Ngoài phạm vi

- Không thay đổi cấu trúc bảng cơ sở dữ liệu MySQL.
- Không can thiệp vào các đợt nộp dạng tệp (`submission_type = 'file'`).
- Không can thiệp vào nội dung bảng tính bên trong Google Sheets.
- Tuân thủ quy định `AGENTS.md`: Antigravity chỉ khảo sát và lập kế hoạch, không tự ý sửa source code.

---

## File dự kiến tác động

1. `nopbai.html` (Frontend Người dùng nộp bài: cơ chế 1 chạm mở link + nộp bài tự động)
2. `nopbai-quanly.html` (Frontend Quản lý: cấu hình trường link gọn gàng)
3. `api/submissions.php` (Backend API: đảm bảo nhận dữ liệu nộp trường link)
4. `tests/nopbai-report-link-smoke.js` (Cập nhật bài kiểm thử tự động)

---

## Các bước thực hiện chi tiết

### Bước 1: Cập nhật `nopbai.html` (Cơ chế Mở link & Tự động nộp bài)

1. **Xây dựng hàm `openLinkAndSubmit(fieldKey, targetUrl)`**:
   ```javascript
   function openLinkAndSubmit(fieldKey, targetUrl) {
       if (!targetUrl) return;
       // 1. Mở tab mới ngay lập tức trong event handler để không bị chặn popup
       const win = window.open(targetUrl, '_blank');
       if (!win) {
           // Dự phòng nếu popup bị chặn
           location.href = targetUrl;
           return;
       }

       // 2. Tự động điền giá trị xác nhận nếu ô input chưa có giá trị
       const input = document.querySelector(`[name="report_${fieldKey}"]`);
       if (input && !input.value.trim()) {
           input.value = 'Đã mở và nộp qua liên kết trực tuyến';
       }

       // 3. Kiểm tra tính hợp lệ của form (các trường required khác nếu có)
       const form = document.getElementById('submitForm');
       if (form && !form.checkValidity()) {
           form.reportValidity();
           return;
       }

       // 4. Kích hoạt nộp bài tự động
       const event = new Event('submit', { cancelable: true });
       submitFiles(event);
   }
   ```

2. **Cập nhật hàm `renderReportFields(a)` cho trường `field.type === 'link'`**:
   - Hiển thị card liên kết hiện đại, đẹp mắt:
     ```javascript
     } else if (field.type === 'link') {
         const targetUrl = field.url ? field.url.trim() : '';
         const rawUrl = targetUrl ? (/^https?:\/\//i.test(targetUrl) ? targetUrl : `https://${targetUrl}`) : '';
         input = `
             <div class="rounded-2xl border border-teal-200 bg-gradient-to-br from-teal-50/80 via-emerald-50/50 to-white p-5 shadow-sm">
                 <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                     <div class="min-w-0 flex-1">
                         <div class="flex items-center gap-2 text-sm font-black text-teal-900">
                             <span class="grid h-7 w-7 place-items-center rounded-lg bg-teal-600 text-white text-xs"><i class="fas fa-arrow-up-right-from-square"></i></span>
                             <span>Mở liên kết để nhập thông tin</span>
                         </div>
                         ${rawUrl ? `<p class="mt-1.5 truncate text-xs text-slate-500 font-mono" title="${esc(rawUrl)}">${esc(rawUrl)}</p>` : '<p class="mt-1.5 text-xs text-amber-600">Chưa cấu hình đường dẫn liên kết.</p>'}
                         <p class="mt-1 text-[11px] font-bold text-teal-700"><i class="fas fa-bolt mr-1 text-amber-500"></i>Nhấn nút bên cạnh sẽ mở trang nhập liệu và tự động ghi nhận hoàn thành nộp bài.</p>
                     </div>
                     ${rawUrl ? `
                         <button type="button" onclick="openLinkAndSubmit('${esc(field.key)}', '${esc(rawUrl)}')" class="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-teal-700 px-5 py-3 text-xs font-black text-white shadow-md shadow-teal-700/25 transition hover:bg-teal-800 hover:scale-[1.02] active:scale-95">
                             <i class="fas fa-paper-plane"></i>
                             <span>Nhấn vào đây để nộp & mở link</span>
                         </button>
                     ` : ''}
                 </div>
                 <div class="mt-3.5 pt-3 border-t border-teal-100/80">
                     <label class="block text-xs font-bold text-slate-600 mb-1">Ghi chú xác nhận (tùy chọn):</label>
                     <input class="field text-sm !bg-white" type="text" name="report_${esc(field.key)}" ${field.required ? 'required' : ''} placeholder="Có thể để trống hoặc ghi chú thêm nếu cần...">
                 </div>
             </div>
         `;
     }
     ```

3. **Cập nhật màn hình thông báo thành công (`#successState` trong `nopbai.html`)**:
   - Bổ sung thông điệp nhắc nhở thân thiện:
     *"Hệ thống đã ghi nhận thời gian nộp bài của bạn. Bạn vui lòng tiếp tục hoàn thành nội dung trên trang vừa mở."*

---

### Bước 2: Cập nhật `nopbai-quanly.html`

1. **Đơn giản hóa giao diện cấu hình trường `link` trong `renderReportFields()`**:
   - Giữ lại ô nhập Tiêu đề chỉ tiêu và ô nhập URL liên kết.
   - Bỏ checkbox nhúng iframe phức tạp (đã chuyển sang cơ chế 1 chạm tối ưu).
   - Dropdown thể loại hiển thị: `Liên kết / Bảng tính ngoài (Link)`.

---

### Bước 3: Cập nhật `api/submissions.php`

1. Giữ nguyên `$types` bao gồm `'link'`, chuẩn hóa `url` (tối đa 500 ký tự, chặn mã độc `javascript:`).
2. Khi người nộp gửi bài, dữ liệu trường `link` được lưu nguyên vẹn vào `report_data_json`.

---

### Bước 4: Cập nhật bài kiểm thử `tests/nopbai-report-link-smoke.js`

- Kiểm tra sự hiện diện của hàm `openLinkAndSubmit` trong `nopbai.html`.
- Kiểm tra việc gắn sự kiện click gọi `openLinkAndSubmit` và kích hoạt nộp bài.
- Chạy test tự động với `node tests/nopbai-report-link-smoke.js` để đảm bảo PASS 100%.

---

## Rủi ro & Giải pháp giảm thiểu

1. **Trình duyệt chặn Popup khi mở tab mới (`window.open`)**:
   - *Giải pháp*: Gọi `window.open` ngay dòng đầu tiên của sự kiện click chuột trực tiếp của người dùng. Nếu popup bị chặn, tự động fallback điều hướng bằng `location.href`.
2. **Trường hợp form có các trường bắt buộc khác chưa điền**:
   - *Giải pháp*: Dùng `form.checkValidity()` và `form.reportValidity()`, nếu form chưa hợp lệ thì trỏ đến trường còn thiếu yêu cầu điền trước khi nộp.
3. **Người dùng bấm nhầm**:
   - *Giải pháp*: Người quản lý có thể xem danh sách bài nộp và luôn có sẵn nút "Xóa bài nộp (để cho nộp lại)" nếu cần cấp quyền nộp lại.

---

## Cách kiểm thử

### 1. Kiểm thử tự động
```bash
node tests/nopbai-report-link-smoke.js
```
Kết quả mong muốn: Exit code 0, `nopbai report link smoke: passed`.

### 2. Kiểm thử thủ công
1. Vào `nopbai-quanly.html`, chọn tạo đợt nộp Báo cáo biểu mẫu.
2. Thêm trường loại `Liên kết / Bảng tính ngoài (Link)`, dán link Google Sheets. Bấm **Lưu đợt nộp**.
3. Mở link nộp bài bằng `nopbai.html?code=XYZ&person=P123`.
4. Nhấn nút **"Nhấn vào đây để nộp & mở link"**:
   - Xác nhận tab mới tự động mở ra link Google Sheets.
   - Xác nhận tab nộp bài tự động kích hoạt nộp bài và chuyển sang màn hình xanh **"Nộp bài thành công"**.
5. Quay lại trang Quản lý: Xác nhận người nộp đã được tích xanh trạng thái **"Đã nộp"**.

---

## Tiêu chí nghiệm thu

- [x] Không còn khung nhúng iframe cồng kềnh, giao diện gọn gàng, tương thích 100% trên cả PC và di động.
- [x] Nút bấm hành động duy nhất: vừa mở tab mới dẫn đến link đích, vừa tự động kích hoạt nộp bài.
- [x] Người nộp không cần phải nhớ quay lại bấm nút Nộp bài nữa.
- [x] Hệ thống ghi nhận trạng thái đã nộp tức thì vào cơ sở dữ liệu.
- [x] Toàn bộ test tự động `tests/nopbai-report-link-smoke.js` chạy thành công.
