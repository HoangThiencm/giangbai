# PLAN: Tối ưu tải tệp Quản lý văn bản — Bộ đệm Staging trên hosting, đẩy sang Google Drive và tự động xóa để bảo vệ dung lượng 3GB

## 1. Hiện trạng & Vấn đề
1. **Dung lượng hosting có hạn (chỉ 3 GB):** Không thể lưu trữ văn bản vĩnh viễn trên hosting. Bắt buộc kho lưu trữ chính phải là Google Drive (Shared Drive của nhà trường qua Service Account).
2. **Nút thắt tốc độ hiện tại:**
   - Dù hosting đã nâng `upload_max_filesize` và `post_max_size` lên 64 MB, và cấu hình `VANBAN_UPLOAD_CHUNK_MB = 25`, nhưng frontend `vanban-app.js` khi `state.driveReady = true` vẫn chạy luồng `uploadFileViaChunks` tuần tự.
   - Mỗi văn bản mới phải chạy qua `upload_init` gọi `vbd_drive_folder()` dò tìm/tạo 5 cấp thư mục trên Drive (`04_QUAN_LY_VAN_BAN` -> Lĩnh vực -> Năm học -> Đến/Đi -> Tên văn bản) tốn 5–8 giây mạng quốc tế trước khi gửi byte đầu tiên.
   - Băng thông quốc tế (outbound) của shared hosting từ Việt Nam sang Google API (`googleapis.com`) bị bóp hẹp (thường chỉ 1–2 MB/s). Người dùng phải ngồi chờ thanh phần trăm chạy tuần tự 20–40 giây cho mỗi tệp lớn.

## 2. Mục tiêu kiến trúc (Staging Buffer -> Google Drive -> Auto-Delete)
1. **Trải nghiệm người dùng tức thì (1–2 giây):**
   - Người dùng bấm Lưu văn bản -> Trình duyệt đẩy tệp thẳng lên trạm trung chuyển (Staging) trên hosting trong nước qua 1 request duy nhất -> Giao diện báo thành công ngay lập tức (1–2 giây), đóng modal, cho phép thầy/cô tiếp tục công việc mà không phải chờ đợi.
2. **Bảo vệ tuyệt đối ổ cứng 3 GB của hosting:**
   - Tệp trên staging chỉ tồn tại tạm thời trong lúc chuyển tiếp.
   - Ngay sau khi Google Drive xác nhận đã nhận trọn vẹn tệp -> PHP gọi `unlink()` **xóa sạch tệp đệm trên hosting ngay lập tức**.
   - Dung lượng lưu trữ lâu dài trên hosting cho tệp văn bản luôn là **0 MB**.
3. **Độ tin cậy & Tính liên tục:**
   - Trong vài chục giây tệp đang ở staging chờ đẩy sang Drive, nếu người dùng bấm "Xem" hoặc "Tải về", hệ thống vẫn phục vụ xem trơn tru từ tệp đệm cục bộ.
   - Có cơ chế dọn dẹp quét rác (Garbage Collection) tự động dọn sạch các tệp staging mồ côi nếu có sự cố mạng.

---

## 3. Thiết kế chi tiết

### A. Phía Backend (`api/vanban.php`)

1. **Thư mục lưu đệm Staging:**
   - Đường dẫn: `storage/vanban/staging/{document_id}/` (tạo thư mục tự động nếu chưa có, bảo vệ bằng `.htaccess` chặn truy cập trực tiếp nếu cần).
2. **Endpoint lưu văn bản & nạp vào Staging (`action=save_upload_stage` hoặc nâng cấp `action=save_upload`):**
   - Nhận thông tin văn bản + danh sách tệp đính kèm (`files[]`) qua multipart POST.
   - Lưu hoặc cập nhật văn bản vào bảng `office_documents`.
   - Di chuyển các tệp tải lên vào thư mục staging: `storage/vanban/staging/{doc_id}/{stored_name}`.
   - Thêm bản ghi vào bảng `office_document_files`:
     - `drive_file_id`: `staging:{doc_id}:{stored_name}` (đánh dấu tệp đang ở trạm trung chuyển).
     - `original_name`: tên gốc của tệp.
     - `stored_name`: tên chuẩn hóa.
     - `mime_type`: MIME detect được.
     - `size_bytes`: kích thước tệp.
     - `view_url` & `download_url`: trỏ về endpoint xem cục bộ `api/vanban.php?action=file&document_id=...&name=...`.
   - Phản hồi ngay cho frontend: `{ ok: true, document: ..., staged_files: [...] }` trong vòng 1–2 giây.
3. **Endpoint đồng bộ sang Google Drive & Xóa đệm (`action=sync_drive_file`):**
   - Nhận `file_id` (ID dòng trong `office_document_files`) hoặc `document_id`.
   - Kiểm tra quyền sở hữu văn bản.
   - Tìm file trên đĩa tại `storage/vanban/staging/...`.
   - Tối ưu tìm/tạo thư mục Drive:
     - Tận dụng `drive_folder_id` đã lưu trong `office_documents`.
     - Nếu chưa có: gọi `vbd_drive_folder($document)` và cập nhật ngay vào `office_documents.drive_folder_id` để các tệp sau không phải dò lại 5 cấp thư mục.
   - Gọi `drive_upload_file($folderId, $storedName, $mime, $stagingPath)` đẩy tệp sang Google Drive.
   - Nhận phản hồi từ Drive: lấy `file_id` thật, `webViewLink`, `webContentLink`.
   - Cập nhật dòng trong `office_document_files`:
     - `drive_file_id = $drive['file_id']`
     - `view_url = $drive['view_url']`
     - `download_url = $drive['download_url']`
   - **XÓA ĐỆM:** Gọi `@unlink($stagingPath)`. Nếu thư mục con `storage/vanban/staging/{doc_id}/` rỗng thì `@rmdir()` xóa luôn.
   - Phản hồi `{ ok: true, synced: true, file: ... }`.
4. **Cơ chế phục vụ tệp xem trước (`action=file`):**
   - Nếu `drive_file_id` bắt đầu bằng `staging:`, đọc và xuất tệp trực tiếp từ `storage/vanban/staging/...`.
   - Đảm bảo người dùng xem được tệp ngay cả khi tệp vừa tải xong 1 giây trước và chưa kịp sang Drive.
5. **Cơ chế tự dọn dẹp (Garbage Collection):**
   - Khi gọi `action=list` hoặc `action=save`, nếu phát hiện tệp staging nào đã được đồng bộ (đã có Google Drive file ID) hoặc tệp mồ côi quá 24h, tự động xóa để bảo vệ tuyệt đối hạn mức 3 GB.

### B. Phía Frontend (`vanban-app.js`)

1. **Điều chỉnh hàm `saveDocument`:**
   - Khi có tệp đính kèm (`pendingUploadFiles.length > 0`):
     - Gửi toàn bộ dữ liệu form + tệp qua `save_upload_stage` bằng một request `fetch` duy nhất (với `FormData`).
     - Thanh tiến trình tải lên chuyển sang trạng thái "Đang lưu văn bản và tệp..." và hoàn tất ngay khi nhận được phản hồi (1–2 giây).
     - Đóng modal chỉnh sửa, cập nhật danh sách văn bản hiển thị trên bảng.
2. **Kích hoạt đồng bộ ngầm (Background Sync):**
   - Sau khi form đã đóng thành công, frontend tự động kích hoạt tiến trình đồng bộ ngầm cho các tệp vừa lưu:
     - Gửi yêu cầu `action=sync_drive_file` cho từng tệp vừa đưa vào staging.
     - Hiển thị badge nhỏ hoặc toast nhẹ ở góc dưới: "Đang đồng bộ [Tên file] lên Google Drive...".
     - Khi đồng bộ xong: cập nhật lại trạng thái tệp sang biểu tượng Google Drive.
   - Nếu người dùng chuyển trang hoặc tắt tab: Lần sau khi vào trang hoặc qua cơ chế dọn dẹp, hệ thống vẫn duy trì kiểm tra và đồng bộ nốt.

---

## 4. Phạm vi tác động & Danh sách file

1. `api/vanban.php`:
   - Bổ sung logic xử lý staging và xóa tự động sau khi upload Drive thành công.
   - Bổ sung action `sync_drive_file`.
   - Cập nhật action `file` để hỗ trợ đọc tệp staging.
   - Thêm hàm dọn dẹp rác định kỳ cho staging.
2. `vanban-app.js`:
   - Cập nhật luồng `saveDocument` ưu tiên đẩy nhanh vào staging.
   - Thêm bộ điều phối đồng bộ ngầm sau khi lưu văn bản.
   - Cập nhật hiển thị trạng thái tệp (đang đồng bộ Drive / đã trên Drive).
3. `tests/vanban-staging-sync-smoke.js`:
   - Bộ kiểm thử tự động kiểm tra:
     + Lưu văn bản kèm tệp vào staging thành công.
     + File tạm tồn tại trong staging.
     + Kích hoạt sync sang Google Drive.
     + Kiểm tra file tạm trong staging đã bị `unlink` hoàn toàn (kích thước thư mục staging = 0).
     + Bản ghi MySQL cập nhật đúng ID Google Drive.

---

## 5. Ngoài phạm vi
- Không thay đổi cấu trúc bảng cơ sở dữ liệu `office_documents` và `office_school_years`.
- Không thay đổi cấu hình xác thực Google Drive Service Account đã có.
- Không sửa đổi các chức năng khác (OCR, phân công, lịch, sổ điểm).

---

## 6. Rủi ro & Giải pháp

| Rủi ro | Giải pháp |
| :--- | :--- |
| Mạng từ hosting sang Google bị ngắt giữa chừng khi sync | Tệp vẫn an toàn ở thư mục staging; lần sau hoặc khi giáo viên bấm vào xem, hệ thống thử đồng bộ lại. Không mất dữ liệu. |
| Người dùng tải nhiều tệp cùng lúc vượt 64MB | Frontend kiểm tra tổng dung lượng trước khi gửi; nếu vượt quá 50MB thì tự động chia làm 2 đợt hoặc cảnh báo trước. |
| Hosting hết ổ cứng nếu tệp bị kẹt không xóa được | Cơ chế dọn rác tự động (Garbage Collection) quét thư mục staging khi tải danh sách văn bản, xóa mọi tệp tạm cũ > 24h. |

---

## 7. Các bước thực hiện chi tiết cho Coder

1. **Bước 1: Cập nhật `api/vanban.php`**
   - Định nghĩa thư mục `vbd_staging_dir()` tại `storage/vanban/staging/`.
   - Viết hàm `vbd_store_staging_upload()` lưu tệp tạm và tạo bản ghi đệm.
   - Thêm action `save_upload_stage` (hoặc tích hợp vào `save_upload`).
   - Thêm action `sync_drive_file` thực hiện: đọc file staging -> `drive_upload_file` -> cập nhật DB -> `unlink()` xóa file đệm.
   - Cập nhật action `file` hỗ trợ tải tệp từ staging nếu `drive_file_id` dạng `staging:...`.
   - Viết hàm `vbd_clean_orphan_staging()` quét dọn file thừa.

2. **Bước 2: Cập nhật `vanban-app.js`**
   - Điều chỉnh hàm `saveDocument`: gom toàn bộ tệp đính kèm vào `FormData` gửi lên endpoint staging.
   - Nhận phản hồi thành công ngay lập tức, hiển thị thông báo "Đã lưu văn bản", đóng modal.
   - Tạo hàm chạy nền `syncPendingStagedFiles()` gửi request `sync_drive_file` từng tệp lên server.
   - Hiển thị trạng thái đồng bộ nhẹ nhàng trên giao diện.

3. **Bước 3: Viết và chạy Smoke Test**
   - Tạo file test `tests/vanban-staging-sync-smoke.js`.
   - Kiểm thử quy trình: Upload staging -> Verify file exists on disk -> Trigger sync -> Verify file deleted from disk -> Verify Drive link valid.
   - Chạy test xác nhận PASS 100%.
