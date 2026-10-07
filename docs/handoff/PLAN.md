# PLAN: Khắc phục lỗi xem tệp PDF Google Drive trong Padlet ("Không thể truy cập vào Tài khoản Google của bạn")

## Hiện trạng
1. **Hiện tượng lỗi theo ảnh thực tế của giáo viên:**
   - Trên điện thoại (iPhone/Safari), khi giáo viên mở bảng Padlet ("HỌP TỔ · Bảng chia sẻ", bài đăng "CONG TAC THANG 10.pdf"), khung nhúng xem tệp không hiển thị nội dung PDF mà hiện thông báo lỗi của Google:
     > *"Không thể truy cập vào Tài khoản Google của bạn. Chúng tôi hiện không thể truy cập vào nội dung này. Hãy thử đăng nhập vào Tài khoản Google của bạn hoặc cấp quyền truy cập vào cookie để tiếp tục."*
2. **Nguyên nhân kỹ thuật 1 (Cốt lõi phân quyền Google Drive):**
   - Trong `api/padlet.php` (dòng 675 và 775), khi tải tệp lên chỉ gọi `drive_upload_file(...)`.
   - Trong `api/google_drive.php`, hàm `drive_upload_response()` chỉ cấp quyền xem công khai khi hằng số `GOOGLE_DRIVE_SHARE_MODE === 'anyone'`. Mặc định hosting (hoặc mẫu `config.sample.php`) thường để `'private'`.
   - Kết quả: Tệp trên Google Drive chỉ thuộc quyền sở hữu của Service Account, không được chia sẻ cho công chúng (`anyone` + `reader`). Khi giáo viên mở xem, Google Drive yêu cầu xác thực tài khoản có quyền truy cập.
3. **Nguyên nhân kỹ thuật 2 (Chính sách chặn Cookie bên thứ ba trong iFrame trên di động):**
   - Trong `padlet_ht.html` (dòng 1817), tài liệu được nhúng trực tiếp bằng thẻ:
     `<iframe src="https://drive.google.com/file/d/{id}/preview" ...>`
   - Trên Safari iOS (và Chrome/Firefox di động), cơ chế **Ngăn chặn theo dõi trang web chéo (Prevent Cross-Site Tracking / ITP)** chặn hoàn toàn **Third-Party Cookies** trong thẻ `<iframe>`.
   - Khi iFrame của Google Drive không đọc được Cookie xác thực phiên đăng nhập của người dùng đối với một tệp bị khóa quyền (private), Google lập tức hiển thị màn hình từ chối xác thực như trong ảnh.
   - Ngoài ra, nút mở ngoài hiện tại trên bài viết chỉ là icon nhỏ (`fa-external-link-alt`), modal xem tệp (`#previewModal`) thiếu nút mở ngoài trực tiếp, khiến giáo viên không biết cách mở khi iFrame bị lỗi.

## Phạm vi
1. **Backend (`api/padlet.php`):**
   - Đảm bảo mọi tệp đính kèm khi tải lên Padlet đều được tự động chia sẻ công khai (`anyone` + `reader`) qua hàm `drive_share_file_anyone($fileId)` (tương tự chuẩn đã áp dụng tại `api/lessons.php`).
   - Thêm cơ chế tự động thử cấp quyền `anyone` nếu tệp chưa được chia sẻ khi người dùng gọi API lấy dữ liệu bảng hoặc tệp.
2. **Frontend (`padlet_ht.html`):**
   - Nâng cấp khối nhúng tài liệu `documentEmbedHtml`:
     - Thêm thanh liên kết phụ trợ / nút dự phòng rõ ràng: **"Mở tệp trong tab mới"** ngay dưới hoặc trên khung xem tài liệu.
     - Xử lý chỉ dẫn thân thiện khi xem trên trình duyệt điện thoại chặn cookie.
   - Nâng cấp `#previewModal`:
     - Bổ sung nút bấm **"Mở trong tab mới"** (`fas fa-external-link-alt`) trên thanh tiêu đề modal để giáo viên có thể mở thẳng tệp ra trình duyệt khi iFrame gặp sự cố.
3. **Kiểm thử & Tính tương thích:**
   - Đảm bảo các bộ smoke test hiện tại (`padlet-ownership-smoke.js`, `padlet-ui-smoke.js`, `padlet-comment-ui-smoke.js`) tiếp tục PASS 100%.

## Ngoài phạm vi
- Không đổi dịch vụ lưu trữ (vẫn dùng Google Drive qua Service Account).
- Không can thiệp vào các mô-đun khác ngoài Padlet.
- Không chỉnh sửa trực tiếp mã nguồn trong lượt survey (tuân thủ quy trình Antigravity IDE).

## File dự kiến tác động
1. `api/padlet.php`: Bổ sung `drive_share_file_anyone` khi lưu tệp tải lên (`add-post`, `edit-post`).
2. `padlet_ht.html`: Thêm nút mở tab mới trực quan tại `documentEmbedHtml` và `#previewModal`.
3. `api/config.php` (trên hosting): Khuyến nghị cấu hình `define('GOOGLE_DRIVE_SHARE_MODE', 'anyone');`.
4. `tests/padlet-ui-smoke.js`: Cập nhật/bổ sung kiểm tra nút mở tệp ngoài.

## Các bước thực hiện
1. **Bước 1: Cập nhật Backend `api/padlet.php`**
   - Tại `add-post` (sau dòng 675) và `edit-post` (sau dòng 775):
     ```php
     try {
         drive_share_file_anyone($drive['file_id']);
     } catch (Throwable $e) {
         error_log('Padlet share file error: ' . $e->getMessage());
     }
     ```
   - Thêm cơ chế an toàn: Bọc trong `try/catch` để nếu Drive chặn chia sẻ thì bài viết vẫn được lưu mà không gây lỗi 500.
2. **Bước 2: Cập nhật Frontend `padlet_ht.html`**
   - Trong `documentEmbedHtml(file)`:
     - Làm rõ nút mở ngoài và thêm dòng ghi chú hỗ trợ: *"Nếu không tải được trên điện thoại, bấm Mở tệp ngoài"*.
   - Trong `#previewModal`:
     - Thêm nút `<a id="previewExternalLink" href="#" target="_blank" rel="noopener" class="flex items-center gap-1.5 rounded-xl bg-teal-50 px-3 py-2 text-xs font-bold text-teal-800 hover:bg-teal-100"><i class="fas fa-external-link-alt"></i><span>Mở tab mới</span></a>` cạnh nút đóng modal.
     - Cập nhật hàm `previewFile()` để gán URL mở ngoài vào nút này.
3. **Bước 3: Hướng dẫn cấu hình Server & Xử lý tệp cũ**
   - Hướng dẫn cấu hình hosting `GOOGLE_DRIVE_SHARE_MODE = 'anyone'` trong `api/config.php`.
   - Với các tệp cũ đã tải lên (như file `CONG TAC THANG 10.pdf`), người quản trị vào Google Drive cấp quyền "Bất kỳ ai có đường liên kết đều có thể xem" cho thư mục bảng chia sẻ đó.
4. **Bước 4: Kiểm thử và hoàn tất**
   - Chạy toàn bộ smoke tests của Padlet.
   - Xác nhận giao diện hiển thị đúng trên điện thoại và máy tính.

## Rủi ro
- Một số tổ chức/trường học dùng Google Workspace có chính sách quản trị chặn chia sẻ ra ngoài tên miền đối với Service Account.
  -> **Biện pháp:** Bọc `try/catch` khi gọi `drive_share_file_anyone` và duy trì nút mở trực tiếp bằng link Drive để người dùng đã đăng nhập tài khoản trường vẫn mở được.

## Cách kiểm thử
1. Chạy lệnh:
   `node tests/padlet-ownership-smoke.js`
   `node tests/padlet-ui-smoke.js`
   `node tests/padlet-comment-ui-smoke.js`
2. Kiểm tra thẻ bài viết và modal xem trước tài liệu có hiển thị nút mở tab mới hay không.

## Tiêu chí nghiệm thu
1. Tệp tải lên qua Padlet được tự động kích hoạt quyền chia sẻ công khai (`anyone`).
2. Giao diện bài viết và modal xem tệp có lối tắt "Mở tab mới" rõ ràng, không để giáo viên bị kẹt ở màn hình lỗi cookie iFrame.
3. Không làm hỏng các tính năng bình luận, phê duyệt, xóa/sửa bài đăng hiện có.
