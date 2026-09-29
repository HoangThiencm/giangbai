STATUS: PASS

## Danh sách lệnh đã chạy và kết quả

### 1. `py tests/vanban-chuyenmon-root-smoke.py`
- **Kết quả:** PASS (Exit code: 0, 27/27 assertions đạt)
- **Log đầu ra:**
```
PASS  khối transfer_sector/copy_sector còn tồn tại
PASS  transfer_sector không UPDATE sector của bản ghi gốc
PASS  transfer_sector tạo bản ghi tích hợp
PASS  thông điệp chuyển giữ bản gốc Hành chính
PASS  copy_sector vẫn còn thông điệp sao chép
PASS  action name transfer_sector và copy_sector giữ nguyên
PASS  có hàm vbd_copy_local_storage
PASS  sao chép tệp vật lý bằng copy()
PASS  không di chuyển thư mục gốc khi sao chép
PASS  vbd_copy_document_files nhận fromDoc và toDoc
PASS  tệp cục bộ được tạo lại view_url và download_url theo document_id mới
PASS  sau khi sao chép bản ghi thì sao chép thư mục tệp cục bộ
PASS  có câu truy vấn đếm tệp Drive dùng chung
PASS  không xóa tệp Drive dùng chung trước khi đếm tham chiếu
PASS  xác nhận chuyển nói rõ bản gốc Hành chính vẫn được lưu trữ
PASS  sau khi chuyển hiển thị data.message
PASS  sau khi chuyển tải lại danh sách Hành chính
PASS  UI vẫn gọi transfer_sector và copy_sector
PASS  nút dòng vẫn là data-action="transfer"
PASS  modal vẫn có data-detail-action transfer và copy
PASS  nhãn nút Chuyển sang Chuyên môn còn nguyên
PASS  nhãn nút Sao chép sang Chuyên môn còn nguyên
PASS  giữ id transferSelectedBtn
PASS  giữ id copySelectedBtn
PASS  nhãn chuyển hàng loạt còn nguyên
PASS  nhãn sao chép hàng loạt còn nguyên
PASS  cú pháp api/vanban.php

PASS: giữ bản gốc Hành chính khi chuyển sang Chuyên môn.
```

### 2. `Select-String -Path "vanban-app.js", "quanlyvanban-hanhchinh.html", "api/vanban.php" -Pattern "transfer_sector|copy_sector"`
- **Kết quả:** PASS (Exit code: 0)
- **Log đầu ra:**
```
vanban-app.js:850:            const data = await api(copying ? 'copy_sector' : 'transfer_sector', {
api\vanban.php:1506:if ($action === 'transfer_sector' || $action === 'copy_sector') {
api\vanban.php:1549:        $message = $action === 'transfer_sector'
```
