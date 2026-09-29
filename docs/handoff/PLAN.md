# Kế hoạch xử lý: Giữ nguyên văn bản gốc tại Hành chính khi chuyển sang Chuyên môn

## 1. Mục tiêu
- Sửa lỗi khi người dùng ở phân hệ Hành chính (`quanlyvanban-hanhchinh.html`) bấm nút **"Chuyển sang Chuyên môn"** (hoặc chuyển hàng loạt, hoặc trong modal chi tiết) làm mất văn bản và tệp tại Hành chính.
- Đảm bảo đúng chuẩn nghiệp vụ: **Thư mục Hành chính là gốc** (lưu trữ và sở hữu mọi văn bản, tệp đính kèm gốc); **phân hệ Chuyên môn là tích hợp qua**.
- Khi chuyển sang Chuyên môn:
  1. Bản ghi văn bản và toàn bộ tệp đính kèm tại Hành chính phải được giữ nguyên vẹn 100%, không bị đổi `sector` hay di dời thư mục tệp.
  2. Tạo bản ghi tích hợp sang Chuyên môn (`sector = 'chuyenmon'`) với đầy đủ thông tin (số hiệu, loại, trích yếu, ngày tháng, hạn báo cáo...) và các tệp đính kèm.
  3. Xử lý toàn vẹn tệp đính kèm (File):
     - Với tệp cục bộ (hosting local fallback): sao chép thư mục tệp vật lý sang thư mục của văn bản mới ở Chuyên môn, cập nhật đúng `view_url` và `download_url` với `document_id` mới.
     - Với tệp Google Drive: sao chép thông tin liên kết tệp sang văn bản mới. Khi xóa văn bản ở Chuyên môn, chỉ xóa tệp trên Google Drive nếu không còn bất kỳ văn bản nào khác (đặc biệt là bản gốc Hành chính) đang tham chiếu `drive_file_id`.
  4. Duy trì đầy đủ tính tương thích ngược với các smoke test hiện tại (`transfer_sector`, `copy_sector`, nhãn các nút trên UI).

---

## 2. Danh sách file dự kiến tác động
1. `api/vanban.php`:
   - Sửa logic xử lý `action === 'transfer_sector'` và `action === 'copy_sector'`: Không đổi `sector` của bản ghi gốc ở Hành chính, không gọi `vbd_move_local_storage` làm mất thư mục gốc. Thay vào đó tạo bản ghi tích hợp sang Chuyên môn.
   - Bổ sung hàm `vbd_copy_local_storage` để sao chép thư mục tệp cục bộ vật lý sang văn bản mới khi nhân bản.
   - Cập nhật `vbd_copy_document_files` để tái tạo đúng `view_url`, `download_url` và sao chép tệp vật lý cho văn bản mới.
   - Cập nhật `vbd_delete_document_file_storage` để không xóa tệp trên Google Drive nếu `drive_file_id` còn được tham chiếu bởi văn bản khác.
2. `vanban-app.js`:
   - Cập nhật `moveToChuyenMon`: Cập nhật câu hỏi xác nhận và thông báo kết quả (toast) rõ ràng: Chuyển tích hợp sang Chuyên môn thành công (bản gốc tại Hành chính vẫn được lưu trữ nguyên vẹn).
   - Đảm bảo sau khi chuyển, danh sách Hành chính được reload và vẫn giữ nguyên văn bản.
3. `quanlyvanban-hanhchinh.html`:
   - Giữ nguyên các nút và ID: `transferSelectedBtn`, `copySelectedBtn`, không làm vỡ cấu trúc và hợp đồng giao diện.
4. `tests/vanban-chuyenmon-root-smoke.py` (tạo mới):
   - Kịch bản kiểm thử tự động kiểm tra cú pháp, hợp đồng giao diện, logic không xóa bản gốc ở Hành chính và logic bảo vệ tệp đính kèm.

---

## 3. Các bước thực hiện chi tiết cho Coder

### Bước 1: Sửa logic backend trong `api/vanban.php`
1. **Viết hàm sao chép thư mục tệp cục bộ:**
   ```php
   function vbd_copy_local_storage(int $fromId, array $fromDoc, int $toId, array $toDoc): void
   {
       $fromDir = vbd_local_file_dir($fromId, $fromDoc);
       $toDir = vbd_local_file_dir($toId, $toDoc);
       if (!is_dir($fromDir) || $fromDir === $toDir) return;
       if (!is_dir($toDir) && !@mkdir($toDir, 0755, true) && !is_dir($toDir)) {
           return;
       }
       $items = @scandir($fromDir) ?: [];
       foreach ($items as $item) {
           if ($item === '.' || $item === '..') continue;
           $src = $fromDir . '/' . $item;
           $dst = $toDir . '/' . $item;
           if (is_file($src)) {
               @copy($src, $dst);
           }
       }
   }
   ```
2. **Cập nhật `vbd_copy_document_files`:**
   - Nhận thêm `$fromDoc` và `$toDoc`.
   - Với mỗi tệp: nếu `vbd_is_local_file_id((string)$file['drive_file_id'])`:
     + `view_url` tạo lại theo `$toId`: `vbd_local_file_url($toId, $file['stored_name'], false)`.
     + `download_url` tạo lại theo `$toId`: `vbd_local_file_url($toId, $file['stored_name'], true)`.
   - Gọi `vbd_copy_local_storage($fromId, $fromDoc, $toId, $toDoc)` sau khi sao chép bản ghi.
3. **Cập nhật bảo vệ tệp Google Drive khi xóa trong `vbd_delete_document_file_storage`:**
   - Trước khi gọi `drive_delete_file($fileId)`:
     ```php
     $checkStmt = $pdo->prepare('SELECT COUNT(*) FROM office_document_files WHERE drive_file_id = ? AND document_id != ?');
     $checkStmt->execute([$rawId, $documentId]);
     if ((int)$checkStmt->fetchColumn() > 0) {
         return null; // Tệp còn được dùng ở văn bản khác, không xóa file Drive dùng chung
     }
     ```
4. **Cập nhật xử lý `action === 'transfer_sector' || $action === 'copy_sector'`:**
   - Khi gọi `transfer_sector` từ Hành chính:
     + KHÔNG chạy câu lệnh `UPDATE office_documents SET sector = ?` làm mất văn bản ở Hành chính.
     + KHÔNG gọi `vbd_move_local_storage` di dời thư mục gốc.
     + Thực hiện tạo bản ghi mới tại `$target` (`chuyenmon`) tương tự `copy_sector` để Hành chính vẫn giữ nguyên bản gốc.
     + Thông điệp trả về: `'Đã chuyển ' . count($created) . ' văn bản sang ' . $label . ' (bản gốc tại Hành chính được giữ nguyên).'`.

### Bước 2: Cập nhật giao diện trong `vanban-app.js`
1. Trong hàm `moveToChuyenMon`:
   - Xác nhận:
     + `Chuyển ${unique.length} văn bản sang Chuyên môn (bản gốc tại Hành chính vẫn được lưu trữ)?`
   - Thông báo sau khi gọi API thành công:
     + Hiển thị `data.message` (hoặc thông báo thành công rõ ràng).
   - Tải lại dữ liệu bằng `await load();` để giao diện phản ánh văn bản vẫn có mặt trong danh mục Hành chính.
2. Đảm bảo các nút trên bảng danh mục (`data-action="transfer"`), thanh tác vụ hàng loạt (`#transferSelectedBtn`, `#copySelectedBtn`) và modal chi tiết (`data-detail-action="transfer"`, `data-detail-action="copy"`) giữ nguyên data attribute và ID để tương thích test.

### Bước 3: Đảm bảo tính tương thích và kiểm thử
1. Giữ nguyên cấu trúc HTML của `quanlyvanban-hanhchinh.html`, `quanlyvanban-chuyenmon.html`, `quanlyvanban.html`.
2. Tạo script kiểm thử Python `tests/vanban-chuyenmon-root-smoke.py` kiểm tra:
   - Kiểm tra API `transfer_sector` không update `sector` của bản ghi gốc.
   - Kiểm tra `vbd_copy_document_files` sao chép tệp an toàn.
   - Kiểm tra `vbd_delete_document_file_storage` không xóa tệp Drive dùng chung.
   - Kiểm tra UI contracts trong `vanban-app.js` và `quanlyvanban-hanhchinh.html`.

---

## 4. Rủi ro và giải pháp
| Rủi ro | Giải pháp |
| :--- | :--- |
| Trùng lặp văn bản khi người dùng bấm chuyển nhiều lần | Có thể kiểm tra nếu đã có văn bản tương ứng ở Chuyên môn thì nhắc nhở hoặc cho phép sao chép thêm bản ghi mới rõ ràng. |
| Xóa văn bản ở Chuyên môn làm mất file Drive của Hành chính | Kiểm tra `SELECT COUNT(*) FROM office_document_files WHERE drive_file_id = ? AND document_id != ?` trước khi xóa file trên Drive. |
| Tệp lưu cục bộ (local hosting) bị lỗi 404 khi mở ở Chuyên môn | Sao chép vật lý thư mục tệp sang thư mục ID mới và tạo lại URL xem/tải theo ID mới. |
| Phá vỡ các smoke test hiện có kiểm tra chuỗi regex (`tests/vanban-chuyenmon-signature-smoke.js`) | Giữ nguyên tên action `transfer_sector`, `copy_sector` và các selector nút UI. |

---

## 5. Lệnh máy kiểm thử cụ thể
Chạy lệnh kiểm thử sau bằng PowerShell/Terminal:
```powershell
py tests/vanban-chuyenmon-root-smoke.py
```
Và kiểm tra các chuỗi hợp đồng trong codebase:
```powershell
Select-String -Path "vanban-app.js", "quanlyvanban-hanhchinh.html", "api/vanban.php" -Pattern "transfer_sector|copy_sector"
```
