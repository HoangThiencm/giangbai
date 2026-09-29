STATUS: PASS

## Danh sách lệnh đã chạy và kết quả

1. `& "C:\Users\HoangThien\AppData\Local\Temp\node-portable\node-v20.19.0-win-x64\node.exe" tests/vanban-chuyenmon-signature-smoke.js`
   - **Kết quả**: Thành công (Exit code 0)
   - **Output**:
     ```text
     PASS: lĩnh vực Chuyên môn, chuyển/sao chép văn bản, số quyết định và ngày ký số.
     ```

2. `& "C:\Users\HoangThien\AppData\Local\Temp\node-portable\node-v20.19.0-win-x64\node.exe" tests/vanban-display-saved-smoke.js`
   - **Kết quả**: Thành công (Exit code 0)
   - **Output**:
     ```text
     PASS: hiển thị văn bản đã lưu, bộ lọc năm học và truy vấn legacy.
     ```

## Đánh giá chi tiết
- **Frontend (`vanban-app.js`, `vanban-hub.js`)**:
  - `renderYears`: Mặc định giữ `state.selectedYear = ''` ("Tất cả năm học"), bổ sung tùy chọn "Chưa gán năm học" (`__empty__`), không tự ý ép chọn năm đầu tiên.
  - `scopedDocs` & tab thống kê: Giữ lại toàn bộ văn bản khi chọn "Tất cả năm học"; fallback an toàn `direction` rỗng/null về `incoming`.
- **Backend (`api/vanban.php`)**:
  - Schema marker được nâng lên `20260929-v2`.
  - Chuẩn hóa dữ liệu văn bản cũ tự động khi gọi schema.
  - Hỗ trợ admin xem toàn trường và giáo viên xem văn bản của mình cùng văn bản legacy (`owner_id = 0 OR owner_id IS NULL`).
  - Lĩnh vực hành chính hỗ trợ truy vấn các văn bản cũ có `sector` là NULL hoặc rỗng.
- **Cache-busting**: Đã đồng bộ `?v=20260929-showdocs` trên cả 4 file HTML (`quanlyvanban.html`, `quanlyvanban-chuyenmon.html`, `quanlyvanban-hanhchinh.html`, `quanlyvanban-dang.html`).
