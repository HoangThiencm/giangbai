# PLAN: Bỏ bắt buộc đăng nhập để xem Quản lý văn bản và Thêm tab Chuyên môn (Cho phép tick chọn lấy văn bản từ Hành chính)

## Hiện trạng
1. **Rào cản đăng nhập khi xem văn bản (`access-control.js`, `api/vanban.php`)**:
   - `access-control.js`: Khai báo các trang `quanlyvanban.html`, `quanlyvanban-hanhchinh.html`, `quanlyvanban-dang.html` nằm trong danh sách kiểm soát `pageKeys`. Khi không có `authToken` trong `localStorage`, script lập tức thực thi `window.location.href = 'login.html'`, ngăn cản hoàn toàn việc truy cập trực tiếp.
   - `api/vanban.php`: Hàm `vbd_current_user($pdo)` được gọi cưỡng bức ở đầu file trước hầu hết các action (kể cả `action=list`, `action=reminder_count`, `action=file`), trả về HTTP `401 Vui lòng đăng nhập lại` nếu thiếu session PHP.
   - Hậu quả: Khi đoàn kiểm tra, ban giám hiệu hoặc cấp trên cần kiểm tra hồ sơ, văn bản chỉ đạo và tệp minh chứng thì không thể xem được nếu không có tài khoản giáo viên/admin đăng nhập, gây bất tiện lớn trong công tác kiểm tra công khai.

2. **Cấu trúc phân loại lĩnh vực (Sectors) hiện hữu**:
   - Hiện hệ thống chỉ hỗ trợ 2 lĩnh vực cứng: **Hành chính** (`hanhchinh`) và **Đảng** (`dang`).
   - Trang Hub tổng quan `quanlyvanban.html` và file xử lý `vanban-hub.js` chỉ có 2 thẻ lĩnh vực và tính toán số liệu cho Hành chính và Đảng.
   - Chỉ có 2 trang chuyên mục: `quanlyvanban-hanhchinh.html` và `quanlyvanban-dang.html`.
   - Chưa có lĩnh vực **Chuyên môn** (`chuyenmon`) để lưu trữ các văn bản chuyên môn, kế hoạch dạy học, công văn chỉ đạo chuyên môn của Sở/Phòng GD&ĐT.
   - Chưa có công cụ cho phép chọn lọc các văn bản nhận từ Hành chính (văn thư tiếp nhận chung) để tick chọn sao chép sang Chuyên môn.

---

## Phạm vi
1. **Bỏ bắt buộc đăng nhập để xem Quản lý văn bản (Chế độ xem công khai / Cấp trên kiểm tra)**:
   - Cho phép khách chưa đăng nhập truy cập xem đầy đủ 4 trang:
     + `quanlyvanban.html` (Hub tổng quan)
     + `quanlyvanban-hanhchinh.html`
     + `quanlyvanban-chuyenmon.html` (Trang mới)
     + `quanlyvanban-dang.html`
   - **Frontend (`access-control.js`)**: Cho phép các trang văn bản bỏ qua bước kiểm tra đăng nhập bắt buộc (`isOpenExamLink || (isPublicVanbanPage && !token)`).
   - **Backend (`api/vanban.php`)**:
     + Các action chỉ đọc (`list`, `file`, `reminder_count`, `drive_check`) không chặn HTTP 401 khi chưa đăng nhập.
     + Khi ở chế độ khách (Guest / Cấp trên kiểm tra): `action=list` trả về danh sách toàn bộ văn bản theo lĩnh vực đang chọn, danh mục năm học, thông tin tệp đính kèm.
     + `action=file`: Cho phép tải hoặc xem trực tiếp các tệp lưu trữ hosting mà không đòi hỏi session giáo viên sở hữu.
     + Các action ghi / sửa đổi dữ liệu (`save`, `delete`, `delete_file`, `update_status`, `upload*`, `create_school_year`, `copy_from_hanhchinh`): Tiếp tục bắt buộc phải đăng nhập tài khoản giáo viên/admin hợp lệ, tuyệt đối không cho phép khách sửa/xóa/thêm văn bản.
   - **Giao diện người dùng (`vanban-app.js`, `vanban-hub.js`)**:
     + Khi ở chế độ xem công khai (chưa đăng nhập):
       * Ẩn các nút thao tác quản trị: "Thêm văn bản", "Tạo năm học", "Lấy từ Hành chính", nút "Sửa", "Xóa", nút cập nhật trạng thái ("Đang xử lý", "Chỉ biết", "Đã báo cáo") trong bảng dữ liệu và modal chi tiết.
       * Cấp trên vẫn tra cứu đầy đủ: Thống kê số lượng, lọc năm học, lọc loại VB, lọc trạng thái, tìm kiếm từ khóa, xem modal chi tiết nội dung/trích yếu, xem trước và tải tệp đính kèm, xuất danh sách ra file Excel.
       * Bổ sung nút/liên kết nhỏ "Đăng nhập giáo viên" trên thanh header để giáo viên phụ trách tiện đăng nhập khi cần quản lý dữ liệu.

2. **Mở tab "Chuyên môn" và tính năng tick chọn lấy văn bản từ Hành chính**:
   - **Lĩnh vực Chuyên môn (`chuyenmon`)**:
     + Khai báo thêm sector `chuyenmon`: Nhãn "Chuyên môn", icon `fa-graduation-cap`, tone màu xanh Indigo (`indigo-700` / `indigo-800`), file liên kết `quanlyvanban-chuyenmon.html`.
     + Cập nhật trang Hub `quanlyvanban.html` và `vanban-hub.js`: Thêm thẻ Chuyên môn vào danh sách lĩnh vực, tính toán số liệu thống kê văn bản đến/đi/cần xử lý/quá hạn của Chuyên môn, hiển thị việc gấp của Chuyên môn trong danh sách nhắc việc.
     + Tạo file trang mới `quanlyvanban-chuyenmon.html` với đầy đủ tính năng: Bộ lọc năm học, loại văn bản, trạng thái báo cáo, bảng danh sách văn bản, modal chi tiết, modal xem tệp đính kèm.
     + Cập nhật thanh điều hướng trên cùng (`vanban-app.js`): Hiển thị đầy đủ liên kết chuyển đổi giữa cả 3 lĩnh vực (Hành chính · Chuyên môn · Đảng) với lĩnh vực đang chọn được làm nổi bật (active).
     + Cập nhật `teacher-lotrinh-nav.js`: Nhận diện thêm `quanlyvanban-chuyenmon.html` là trang thuộc nhóm Quản lý văn bản.
   - **Chức năng tick chọn lấy văn bản từ Hành chính sang Chuyên môn**:
     + Trên trang `quanlyvanban-chuyenmon.html`: Bổ sung nút **"Lấy từ Hành chính"** (icon `fa-file-import` hoặc `fa-clone`, hiển thị khi đã đăng nhập).
     + Khi bấm nút: Mở modal "Lấy văn bản từ Hành chính sang Chuyên môn":
       * Có bộ lọc năm học và ô tìm kiếm nhanh văn bản Hành chính.
       * Danh sách các văn bản từ Hành chính có kèm Checkbox để tick chọn từng văn bản hoặc "Chọn tất cả".
       * Hiển thị rõ: Số/Ký hiệu, Loại VB, Ngày VB, Trích yếu, Số tệp đính kèm, và nhãn nhận biết nếu văn bản đã được sao chép sang Chuyên môn trước đó.
       * Nút xác nhận: "Lấy văn bản đã chọn sang Chuyên môn".
     + **Backend API `api/vanban.php`**:
       * Thêm action `copy_from_hanhchinh`: Nhận mảng `document_ids` từ client.
       * Kiểm tra quyền đăng nhập giáo viên/admin.
       * Duyệt qua từng ID văn bản Hành chính: Sao chép bản ghi vào bảng `office_documents` với `sector = 'chuyenmon'`, sao chép toàn bộ thông tin nghiệp vụ (năm học, số hiệu, ngày, trích yếu, tóm tắt, hạn báo cáo...).
       * Sao chép các bản ghi tệp đính kèm tương ứng trong `office_document_files` sang ID văn bản mới, giữ nguyên mã tệp Google Drive / đường dẫn hosting để Chuyên môn xem được ngay lập tức mà không cần tải lại tệp.
       * Trả về kết quả thành công và số lượng văn bản đã lấy.
     + Sau khi sao chép thành công: Tự động đóng modal, làm mới danh sách văn bản Chuyên môn và hiển thị thông báo toast thành công.

---

## Ngoài phạm vi
- Không thay đổi kiểu dữ liệu cột `sector` trong bảng cơ sở dữ liệu `office_documents` (cột đã có kiểu `VARCHAR(20)`, hoàn toàn tương thích với chuỗi `'chuyenmon'`).
- Không tác động vào phân quyền của các module khác ngoài Quản lý văn bản (ví dụ Soạn KHBD, Thời khóa biểu, Điểm số vẫn giữ nguyên phân quyền hiện tại).
- Không can thiệp vào tài khoản Google Drive hay thay đổi cấu hình Drive đã lưu trong `api/config.php`.

---

## File dự kiến tác động
1. `access-control.js`: Cho phép truy cập các trang văn bản không cần `authToken`.
2. `teacher-lotrinh-nav.js`: Bổ sung `quanlyvanban-chuyenmon.html` vào nhóm trang văn bản.
3. `quanlyvanban.html`: Điều chỉnh lưới lĩnh vực hiển thị 3 cột và cập nhật mô tả.
4. `vanban-hub.js`: Bổ sung sector `chuyenmon` vào danh mục lĩnh vực, thống kê và nhắc việc.
5. `quanlyvanban-hanhchinh.html`: Bổ sung liên kết điều hướng 3 tab.
6. `quanlyvanban-dang.html`: Bổ sung liên kết điều hướng 3 tab.
7. `quanlyvanban-chuyenmon.html`: File giao diện mới cho lĩnh vực Chuyên môn.
8. `vanban-app.js`: Hỗ trợ sector `chuyenmon`, thanh điều hướng 3 tab, chế độ xem khách (ẩn nút sửa/xóa/thêm), giao diện và xử lý modal tick chọn lấy văn bản từ Hành chính.
9. `api/vanban.php`: Cho phép chế độ khách đọc danh mục và xem tệp; hỗ trợ sector `chuyenmon`; bổ sung action `copy_from_hanhchinh`.
10. `docs/handoff/IMPLEMENT.md`
11. `docs/handoff/VERIFY.md`
12. `docs/handoff/.lock`

---

## Các bước thực hiện
1. **Bước 1: Mở khóa handoff**:
   - Coder xóa file `docs/handoff/.lock` trước khi sửa mã nguồn.

2. **Bước 2: Nâng cấp Backend `api/vanban.php`**:
   - Cập nhật hàm `vbd_sector()`: Chấp nhận thêm `'chuyenmon'` (hợp lệ gồm `['hanhchinh', 'dang', 'chuyenmon']`).
   - Cập nhật hàm `vbd_sector_label()`: Bổ sung `'chuyenmon' => 'Chuyên môn'`.
   - Cập nhật hàm lấy thư mục Drive cho Chuyên môn: `'CHUYEN_MON'`.
   - Cập nhật cơ chế xác thực phiên:
     + Tách biệt kiểm tra người dùng bắt buộc (`vbd_current_user`) và lấy người dùng hiện tại tùy chọn (`vbd_optional_user`).
     + Đối với `action=list`: Nếu không có phiên đăng nhập (`$user === null`), truy vấn tất cả văn bản theo `sector` được yêu cầu mà không lọc theo `owner_id`. Trả về `is_guest => true` và `user => null`.
     + Đối với `action=file`: Cho phép khách truy cập xem/tải tệp đính kèm lưu trên hosting nếu tệp tồn tại trong CSDL.
     + Đối với `action=reminder_count`: Cho phép trả về số lượng việc cần xử lý chung mà không báo lỗi 401.
   - Thêm action `copy_from_hanhchinh`:
     + Yêu cầu đăng nhập (`vbd_current_user`).
     + Tiếp nhận mảng `source_ids` từ JSON body.
     + Với mỗi ID: Truy vấn văn bản từ `office_documents` có `id = ? AND sector = 'hanhchinh'`.
     + Tạo bản ghi mới trong `office_documents` với `sector = 'chuyenmon'`, giữ nguyên các trường thông tin khác.
     + Truy vấn tất cả file từ `office_document_files WHERE document_id = ?` của văn bản nguồn và chèn bản ghi mới trỏ đến ID văn bản Chuyên môn vừa tạo.
     + Trả về `{ ok: true, copied_count: $count, message: 'Đã lấy thành công X văn bản sang Chuyên môn.' }`.

3. **Bước 3: Điều chỉnh kiểm soát truy cập `access-control.js` và điều hướng `teacher-lotrinh-nav.js`**:
   - Thêm `'quanlyvanban-chuyenmon.html': 'quanlyvanban'` vào `pageKeys` của `access-control.js`.
   - Khai báo danh sách các trang văn bản công khai:
     ```javascript
     const isPublicVanbanPage = [
         'quanlyvanban.html',
         'quanlyvanban-hanhchinh.html',
         'quanlyvanban-chuyenmon.html',
         'quanlyvanban-dang.html'
     ].includes(fileName);
     ```
   - Nếu `!token && isPublicVanbanPage`: Bỏ qua chuyển hướng `login.html`, cho phép tiếp tục tải trang ở chế độ khách.
   - Bổ sung `quanlyvanban-chuyenmon.html` vào hàm `isVanbanPage()` trong `teacher-lotrinh-nav.js`.

4. **Bước 4: Cập nhật Hub Quản lý văn bản `quanlyvanban.html` và `vanban-hub.js`**:
   - Trong `vanban-hub.js`: Thêm `chuyenmon` vào đối tượng `SECTORS`:
     ```javascript
     chuyenmon: { label: 'Chuyên môn', icon: 'fa-graduation-cap', accent: 'indigo', page: 'quanlyvanban-chuyenmon.html' }
     ```
   - Cập nhật hàm `sectorOf(doc)` để nhận diện đúng `doc.sector === 'chuyenmon'`.
   - Cập nhật hàm `sectorCard` hỗ trợ thêm accent màu `indigo` (border, text, badge, button).
   - Trong `quanlyvanban.html`: Điều chỉnh layout lưới của `#sectorCards` thành `grid-cols-1 md:grid-cols-2 lg:grid-cols-3` để 3 thẻ Hành chính, Chuyên môn, Đảng cân đối đẹp mắt.
   - Thêm nút/liên kết Đăng nhập cho giáo viên ở header khi chưa đăng nhập.

5. **Bước 5: Tạo trang `quanlyvanban-chuyenmon.html` và đồng bộ giao diện 3 trang lĩnh vực**:
   - Tạo file `quanlyvanban-chuyenmon.html` kế thừa bố cục chuẩn của Hành chính và Đảng, thiết lập `window.VANBAN_SECTOR = 'chuyenmon';` và tiêu đề "Quản lý văn bản · Chuyên môn".
   - Đồng bộ cấu trúc modal và các thành phần giao diện.

6. **Bước 6: Nâng cấp `vanban-app.js`**:
   - Bổ sung `chuyenmon` vào `SECTOR_META` với accent `indigo`.
   - Hỗ trợ chế độ khách (Guest mode):
     + Nhận diện `state.isGuest` từ dữ liệu API `list` hoặc kiểm tra `authToken`.
     + Khi `state.isGuest === true`:
       * Ẩn các nút "Thêm văn bản", "Tạo năm học", "Lấy từ Hành chính".
       * Bảng danh sách văn bản: Ẩn các nút Sửa, Xóa, Đổi trạng thái; thay vào đó hiển thị nút "Xem chi tiết" (icon con mắt).
       * Modal chi tiết: Ẩn các nút thao tác Sửa/Đổi trạng thái, chỉ giữ nút Đóng.
       * Tệp đính kèm: Ẩn nút xóa tệp (thùng rác), chỉ hiển thị nút Xem/Tải tệp.
       * Giữ nguyên nút "Xuất Excel" và toàn bộ các bộ lọc, tìm kiếm, xem trước tệp.
   - Nâng cấp thanh điều hướng `renderNav()`:
     + Hiển thị đồng thời cả 3 tab: Hành chính, Chuyên môn, Đảng với trạng thái Active rõ ràng.
     + Nếu ở trang Chuyên môn và đã đăng nhập: Hiển thị thêm nút **"Lấy từ Hành chính"**.
   - Xây dựng Modal "Lấy văn bản từ Hành chính sang Chuyên môn":
     + Gọi API lấy danh sách văn bản Hành chính (`api/vanban.php?action=list&sector=hanhchinh`).
     + Hiển thị bảng chọn có checkbox cho từng văn bản kèm thông tin: Số/Ký hiệu, Ngày, Trích yếu, Tệp đính kèm.
     + Đánh dấu rõ các văn bản đã có ở Chuyên môn.
     + Bắt sự kiện chọn tất cả / bỏ chọn tất cả / chọn từng dòng.
     + Gửi danh sách ID đã chọn tới API `action=copy_from_hanhchinh`.
     + Cập nhật lại danh sách văn bản Chuyên môn ngay sau khi hoàn tất.

7. **Bước 7: Khóa handoff và chuẩn bị kiểm thử**:
   - Ghi lại toàn bộ thay đổi vào `docs/handoff/IMPLEMENT.md`.
   - Coder tạo lại `docs/handoff/.lock` nội dung `LOCK`.

---

## Rủi ro
1. **Bảo mật và an toàn dữ liệu khi mở xem công khai**:
   - *Rủi ro*: Khách chưa đăng nhập có thể lợi dụng để gọi các API chỉnh sửa, xóa văn bản hoặc xóa tệp trên Google Drive.
   - *Biện pháp giảm thiểu*: Tất cả các endpoint ghi/sửa/xóa (`save`, `delete`, `delete_file`, `update_status`, `upload*`, `copy_from_hanhchinh`) bắt buộc kiểm tra chặt chẽ `vbd_current_user`, trả về 401 ngay lập tức nếu chưa đăng nhập. Chỉ duy nhất các endpoint đọc (`list`, `file` đọc nội dung) được mở công khai.
2. **Xóa văn bản sao chép ảnh hưởng đến file trên Google Drive**:
   - *Rủi ro*: Nếu văn bản Chuyên môn dùng chung `drive_file_id` với văn bản Hành chính, khi người dùng xóa văn bản Chuyên môn có thể vô tình xóa file gốc trên Google Drive.
   - *Biện pháp giảm thiểu*: Khi xóa văn bản Chuyên môn, hàm `vbd_delete_document` trong `api/vanban.php` cần kiểm tra xem `drive_file_id` đó có còn được tham chiếu bởi văn bản nào khác (ở Hành chính hoặc Chuyên môn) hay không trước khi gọi lệnh xóa file trên Google Drive; nếu còn tham chiếu thì chỉ xóa liên kết trong CSDL MySQL, không xóa file trên Drive.
3. **Trùng lặp khi tick lấy văn bản từ Hành chính**:
   - *Rủi ro*: Người dùng tick chọn nhiều lần có thể gây nhân bản thừa thãi văn bản vào Chuyên môn.
   - *Biện pháp giảm thiểu*: Giao diện modal chọn văn bản Hành chính sẽ so sánh (theo số ký hiệu / trích yếu / ngày) và hiển thị nhãn "(Đã lấy)" đối với văn bản đã có mặt trong Chuyên môn, giúp người dùng dễ dàng nhận biết.

---

## Cách kiểm thử
1. **Kiểm thử chế độ xem không cần đăng nhập (Khách / Cấp trên kiểm tra)**:
   - Dùng trình duyệt ẩn danh (Incognito) hoặc xóa `authToken` trong `localStorage`:
   - Truy cập `quanlyvanban.html`: Trang mở thành công, hiển thị đầy đủ thẻ thống kê 3 lĩnh vực (Hành chính, Chuyên môn, Đảng).
   - Bấm vào từng lĩnh vực `quanlyvanban-hanhchinh.html`, `quanlyvanban-chuyenmon.html`, `quanlyvanban-dang.html`:
     + Không bị chuyển hướng về `login.html`.
     + Xem được danh sách văn bản, số/ký hiệu, ngày tháng, trích yếu.
     + Các bộ lọc (Năm học, Loại văn bản, Trạng thái) và tìm kiếm hoạt động bình thường.
     + Bấm vào trích yếu mở modal chi tiết văn bản đầy đủ.
     + Bấm "Xem" mở xem trước tệp đính kèm trên Google Drive hoặc tệp tải từ hosting thành công.
     + Xuất Excel hoạt động tốt.
     + Không nhìn thấy các nút: "Thêm văn bản", "Tạo năm học", "Lấy từ Hành chính", "Sửa", "Xóa", đổi trạng thái báo cáo.
   - Thử gửi request API `POST api/vanban.php?action=save` hoặc `action=delete` khi không có session -> Nhận HTTP 401.

2. **Kiểm thử chế độ Quản trị (Giáo viên / Admin đăng nhập)**:
   - Đăng nhập tài khoản giáo viên:
   - Truy cập `quanlyvanban.html`: Hiển thị 3 lĩnh vực và nút quản lý.
   - Mở `quanlyvanban-chuyenmon.html`:
     + Xuất hiện nút "Thêm văn bản", "Tạo năm học" và nút **"Lấy từ Hành chính"**.
     + Thêm mới một văn bản trực tiếp vào Chuyên môn -> Lưu thành công, hiển thị đúng ở tab Chuyên môn.
     + Bấm **"Lấy từ Hành chính"**:
       * Modal hiển thị danh sách văn bản thuộc Hành chính.
       * Tick chọn 2-3 văn bản bất kỳ (có kèm tệp đính kèm).
       * Bấm "Lấy văn bản đã chọn sang Chuyên môn".
       * Xác nhận thông báo thành công.
       * Danh sách Chuyên môn xuất hiện ngay các văn bản vừa lấy, đầy đủ thông tin và tệp đính kèm.
       * Mở xem tệp đính kèm của văn bản vừa lấy -> Xem bình thường.
       * Quay lại tab Hành chính: Các văn bản gốc ở Hành chính vẫn nguyên vẹn.
     + Thử sửa, đổi trạng thái, xóa văn bản ở Chuyên môn -> Hoạt động bình thường.
     + Thử xóa văn bản đã sao chép ở Chuyên môn -> Văn bản gốc ở Hành chính và file đính kèm ở Hành chính không bị ảnh hưởng.

---

## Tiêu chí nghiệm thu
1. Cấp trên / người xem chưa đăng nhập có thể truy cập trực tiếp và xem đầy đủ danh mục văn bản, chi tiết văn bản, tệp đính kèm ở cả 4 trang (`quanlyvanban.html`, `quanlyvanban-hanhchinh.html`, `quanlyvanban-chuyenmon.html`, `quanlyvanban-dang.html`) mà không bị bắt đăng nhập hay chuyển hướng về `login.html`.
2. Khách chưa đăng nhập không thể thực hiện bất kỳ hành động thêm, sửa, xóa hay thay đổi trạng thái văn bản nào (chặn cả ở giao diện và tầng API).
3. Hệ thống có đầy đủ 3 lĩnh vực độc lập: **Hành chính**, **Chuyên môn**, **Đảng** trên Hub tổng quan và thanh điều hướng từng trang.
4. Tab Chuyên môn có nút "Lấy từ Hành chính", mở modal hiển thị danh sách văn bản Hành chính có checkbox để tick chọn và sao chép sang Chuyên môn.
5. Văn bản được lấy sang Chuyên môn giữ nguyên thông tin nghiệp vụ và tệp đính kèm (mở xem được bình thường).
