# Kế hoạch kỹ thuật: Sửa lỗi không hiển thị văn bản đã lưu trong Quản lý văn bản

## 1. Mục tiêu
Khắc phục triệt để lỗi không hiển thị các văn bản đã lưu trước đó trong toàn bộ hệ thống Quản lý văn bản (`quanlyvanban.html`, `quanlyvanban-hanhchinh.html`, `quanlyvanban-chuyenmon.html`, `quanlyvanban-dang.html`), bảo đảm:
- Hiển thị đầy đủ tất cả văn bản đã lưu (kể cả văn bản cũ chưa có `academic_year`, `sector` đang là NULL hoặc rỗng, hoặc văn bản đi/đến có `direction` trống).
- Bộ lọc năm học mặc định là "Tất cả năm học" (`value=""`), không tự ý ép chọn năm đầu tiên khiến văn bản cũ bị ẩn. Thêm tùy chọn "Chưa gán năm học" (`value="__empty__"`).
- Khi tính toán số lượng thống kê và chuyển tab đến/đi, các văn bản có `direction` trống/NULL được tự động fallback thành `incoming` để không biến mất khỏi giao diện.
- Backend `api/vanban.php`:
  + Tăng version marker schema lên `20260929-v2` để kích hoạt migration cập nhật chuẩn hóa dữ liệu cũ trên database (`sector = 'hanhchinh'`, `direction = 'incoming'`).
  + Khi query danh sách (`action=list`):
    * Lĩnh vực Hành chính: truy vấn `(sector = 'hanhchinh' OR sector IS NULL OR sector = '')` để không sót bất kỳ văn bản legacy nào.
    * Quyền truy cập: tài khoản `admin` / `superadmin` xem được toàn bộ văn bản của trường; tài khoản giáo viên xem văn bản của mình cùng các văn bản legacy (`owner_id = 0 OR owner_id IS NULL`).
- Đồng bộ cache-busting version query string trên cả 4 file HTML.

## 2. Danh sách file dự kiến tác động
1. `vanban-app.js` (Sửa logic lọc năm học, fallback direction, scopedDocs, renderYears, renderDirectionTabs, renderSummary)
2. `vanban-hub.js` (Bổ sung fallback direction khi tính thống kê cho hub)
3. `api/vanban.php` (Nâng schema version `20260929-v2`, chuẩn hóa dữ liệu cũ, mở rộng query list cho sector hành chính và phân quyền admin/legacy)
4. `quanlyvanban.html` (Đồng bộ cache-busting query string `?v=20260929-showdocs`)
5. `quanlyvanban-chuyenmon.html` (Đồng bộ cache-busting query string `?v=20260929-showdocs`)
6. `quanlyvanban-hanhchinh.html` (Đồng bộ cache-busting query string `?v=20260929-showdocs`)
7. `quanlyvanban-dang.html` (Đồng bộ cache-busting query string `?v=20260929-showdocs`)
8. `tests/vanban-display-saved-smoke.js` (Test tự động xác minh hiển thị văn bản đã lưu và tính toàn vẹn bộ lọc)

## 3. Các bước thực hiện chi tiết cho Coder

### Bước 1: Sửa backend `api/vanban.php`
1. Tại `vbd_maybe_ensure_schema`:
   - Đổi version kiểm tra từ `'20260624-v1'` thành `'20260929-v2'`.
2. Tại `vbd_ensure_schema`:
   - Bổ sung lệnh chuẩn hóa dữ liệu cho các dòng đã tồn tại:
     * `UPDATE office_documents SET sector = 'hanhchinh' WHERE sector IS NULL OR TRIM(sector) = ''`
     * `UPDATE office_documents SET direction = 'incoming' WHERE direction IS NULL OR TRIM(direction) = ''`
     * `UPDATE office_documents SET academic_year = '' WHERE academic_year IS NULL`
3. Tại khối `if ($action === 'list')`:
   - Xác định vai trò: `$userRole = (string)($user['role'] ?? ''); $isAdmin = in_array($userRole, ['admin', 'superadmin'], true);`
   - Điều kiện truy vấn owner:
     * Nếu `$isAdmin`: không hạn chế `owner_id` (xem toàn bộ văn bản của trường).
     * Nếu giáo viên: `WHERE (owner_id = ? OR owner_id = 0 OR owner_id IS NULL)`.
   - Điều kiện truy vấn sector:
     * Nếu `$sectorFilter === 'hanhchinh'`: dùng `(sector = 'hanhchinh' OR sector IS NULL OR sector = '')`.
     * Nếu là sector khác (`dang`, `chuyenmon`): dùng `sector = ?`.
4. Tại `vbd_document` và `vbd_owned_documents`:
   - Cho phép giáo viên truy cập văn bản có `owner_id = 0 OR owner_id IS NULL`, hoặc nếu là admin thì cho phép truy cập theo `id`. Lưu ý giữ chuỗi regex `owner_id = \? AND id IN` trong code để tương thích với test `vanban-chuyenmon-signature-smoke.js`.

### Bước 2: Sửa frontend `vanban-app.js`
1. Tại `renderYears`:
   - Loại bỏ đoạn ép buộc `state.selectedYear = years[0]`. Nếu `state.selectedYear` rỗng, giữ nguyên `''` ("Tất cả năm học").
   - Nếu `state.selectedYear` khác `''`, khác `'__empty__'` và không thuộc mảng `years`, reset về `''`.
   - Trong dropdown `#academicYearFilter`:
     * Thêm tùy chọn đầu tiên: `<option value="">Tất cả năm học</option>`
     * Thêm tùy chọn thứ hai: `<option value="__empty__">Chưa gán năm học</option>`
     * Thêm danh sách các năm học trong `years`.
     * Gán `$('academicYearFilter').value = state.selectedYear`.
   - Trong dropdown `#academicYear` (form tạo/sửa văn bản trong modal): nếu chưa chọn năm và có `years.length > 0`, đặt mặc định là `years[0]` (năm mới nhất) để văn bản mới có năm học.
2. Tại `yearScopedDocs`:
   - Lấy `const year = $('academicYearFilter')?.value || '';`
   - Nếu `!year`: trả về toàn bộ `state.documents`.
   - Nếu `year === '__empty__'`: trả về `state.documents.filter(doc => !doc.academic_year)`.
   - Ngược lại: trả về `state.documents.filter(doc => doc.academic_year === year)`.
3. Tại `scopedDocs`:
   - Lọc năm học:
     * Nếu `year === '__empty__'`: `if (doc.academic_year) return false;`
     * Nếu `year && doc.academic_year !== year`: `return false;`
   - Lọc hướng (`direction`):
     * Fallback: `const docDir = doc.direction || 'incoming';`
     * `if (state.activeDirection && docDir !== state.activeDirection) return false;`
4. Tại `renderDirectionTabs`:
   - Khi đếm `incoming`: `const incoming = docs.filter(d => (d.direction || 'incoming') === 'incoming').length;`
   - Khi đếm `outgoing`: `const outgoing = docs.filter(d => d.direction === 'outgoing').length;`
5. Tại `renderSummary`:
   - Dùng cùng fallback `(d.direction || 'incoming') === 'incoming'` khi đếm số lượng văn bản đến.

### Bước 3: Sửa `vanban-hub.js`
1. Tại `statsFor`:
   - Chuẩn hóa: `const incoming = docs.filter(d => (d.direction || 'incoming') === 'incoming').length;`
   - `const outgoing = docs.filter(d => d.direction === 'outgoing').length;`

### Bước 4: Đồng bộ cache-busting query string trong HTML
1. `quanlyvanban.html`: cập nhật `vanban-hub.js?v=20260929-showdocs`
2. `quanlyvanban-chuyenmon.html`: cập nhật `vanban-app.js?v=20260929-showdocs`
3. `quanlyvanban-hanhchinh.html`: cập nhật `vanban-app.js?v=20260929-showdocs`
4. `quanlyvanban-dang.html`: cập nhật `vanban-app.js?v=20260929-showdocs`, `access-control.js?v=20260929-showdocs`

### Bước 5: Tạo test tự động `tests/vanban-display-saved-smoke.js`
Tạo test Node.js kiểm tra:
1. `renderYears` giữ `state.selectedYear = ''` khi chưa chọn, không ép buộc sang `years[0]`.
2. `scopedDocs` trả về đầy đủ văn bản khi `selectedYear = ''`, bao gồm văn bản không có `academic_year` hoặc thuộc năm học khác.
3. `scopedDocs` giữ lại văn bản có `direction` rỗng/null trên tab `incoming`.
4. `scopedDocs` lọc chính xác văn bản không có năm học khi chọn `__empty__`.
5. `api/vanban.php` chứa version marker `'20260929-v2'`.
6. `api/vanban.php` chứa truy vấn `(sector = 'hanhchinh' OR sector IS NULL OR sector = '')`.
7. `api/vanban.php` hỗ trợ xem văn bản cho admin và văn bản legacy (`owner_id = 0 OR owner_id IS NULL`).

## 4. Rủi ro và giải pháp
- **Rủi ro 1**: Cơ sở dữ liệu đang có văn bản cũ không có trường `sector` hoặc `direction` hoặc `academic_year`.
  -> **Giải pháp**: Tăng version marker schema lên `20260929-v2` để PHP tự chạy lệnh UPDATE chuẩn hóa ngay khi API chạy, đồng thời câu truy vấn SQL và mã lọc frontend đều có fallback phòng thủ.
- **Rủi ro 2**: Người dùng vào trang bị ẩn văn bản cũ do filter tự gán năm học mới.
  -> **Giải pháp**: Mặc định bộ lọc luôn là "Tất cả năm học" (`''`). Bổ sung mục "Chưa gán năm học" để phân loại rõ ràng.
- **Rủi ro 3**: Làm ảnh hưởng các chức năng ký số và chuyên môn vừa cập nhật.
  -> **Giải pháp**: Giữ nguyên toàn bộ logic nhận diện ký số và chạy kiểm thử `tests/vanban-chuyenmon-signature-smoke.js` để bảo đảm PASS.
- **Rủi ro 4**: Trình duyệt người dùng dùng bản JS cũ trong cache.
  -> **Giải pháp**: Cập nhật query version `?v=20260929-showdocs` trên toàn bộ 4 file HTML.

## 5. Lệnh kiểm thử cụ thể
```powershell
& "C:\Users\HoangThien\AppData\Local\Temp\node-portable\node-v20.19.0-win-x64\node.exe" tests/vanban-chuyenmon-signature-smoke.js
& "C:\Users\HoangThien\AppData\Local\Temp\node-portable\node-v20.19.0-win-x64\node.exe" tests/vanban-display-saved-smoke.js
```
