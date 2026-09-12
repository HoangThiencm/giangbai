# PLAN

## Hiện trạng

### 1. Vấn đề 1: Cảnh báo lệch tiết TKB và PPCT ("Tuần 1 – Toán lớp 71: TKB có 8 tiết, PPCT xác định 4 tiết...")
- **Bản chất**: Hệ thống đối chiếu số tiết giữa Thời khóa biểu (TKB) và Phân phối chương trình (PPCT). TKB xếp 8 tiết trong khi PPCT tuần 1 chỉ có 4 tiết, dẫn đến chênh lệch 4 tiết không có bài dạy ghép vào.
- **Nguyên nhân cốt lõi**:
  1. Có trường hợp 2 giáo viên cùng có TKB dạy môn Toán cho lớp 71 (Thầy A dạy 4 tiết, Cô B dạy 4 tiết). Hiện tại hệ thống gom chung tất cả GV vào một giỏ của lớp mà chưa kiểm tra/cảnh báo hiện tượng 2 GV cùng dạy.
  2. Lớp học cả sáng và chiều (4 tiết sáng + 4 tiết chiều).
  3. Hàm `baoGiangRows(until)` luôn duyệt từ ngày đầu năm học `start_date` đến ngày xem, khiến cảnh báo của các tuần đã qua trong quá khứ (như Tuần 1) liên tục bị tính lại và treo cảnh báo trên màn hình cũng như chặn gửi email.
  4. Hàm `buildBaoGiangSelfEmail` dùng chung `warningDetails` của toàn trường để chặn giáo viên (`throw new Error`).

### 2. Vấn đề 2: Thể hiện bài dạy đa tuần (Bài 11 học ở 3 tuần: Tuần 4, 5, 6)
- **Yêu cầu**: Khi một bài học (ví dụ: *Bài 11. Tỉ số lượng giác của góc nhọn*) dạy kéo dài qua 3 tuần (mỗi tuần 1 tiết), phải thể hiện rõ ràng và đầy đủ:
  - Tuần 4: `Tuần 4  Bài 11. Tỉ số lượng giác của góc nhọn (tiết ppct: ví dụ tiết 6) 1/3`
  - Tuần 5: `Tuần 5  Bài 11. Tỉ số lượng giác của góc nhọn (tiết ppct ví dụ tiết 7) 2/3`
  - Tuần 6: `Tuần 6  Bài 11. Tỉ số lượng giác của góc nhọn (tiết ppct ví dụ tiết 8) 3/3`
- **Tồn tại**: Thuật toán `parseBaoGiangCurriculum()` hiện phụ thuộc vào khối liền kề của Mạch (`strand`). Nếu không có Mạch hoặc giữa các tuần có bài khác xen vào thì bài học bị cắt nhỏ thành các khối độc lập `1/1, 1/1, 1/1`.

### 3. Vấn đề 3: Gửi Thời khóa biểu các giáo viên được tick chọn qua email cá nhân
- **Yêu cầu**:
  - Trong tab "2. Thời khoá biểu GV", cho phép tick chọn (checkbox) các giáo viên cần xem (có tùy chọn chọn tất cả / bỏ chọn).
  - Có nút bấm gửi TKB của **toàn bộ các giáo viên được tick chọn** về email cá nhân (tài khoản đang đăng nhập).
  - Phân tách rõ ràng từng giáo viên (mỗi giáo viên là một bảng TKB trực quan độc lập gồm Buổi sáng, Buổi chiều, Thứ 2 đến Thứ 7, Tiết, Môn, Lớp).
  - **Chỉ chứa Thời khóa biểu, hoàn toàn không có lịch báo giảng hay PPCT**.
- **Tồn tại**: Chưa có checkbox trong danh sách giáo viên, chưa có hàm dựng mẫu email HTML TKB đa giáo viên và nút gửi email TKB.

### 4. Vấn đề 4: Tự động reload lại toàn bộ trên web mỗi lần đẩy lên GitHub (Toàn hệ thống hoangthiencm.id.vn)
- **Hiện tượng**: Khi đẩy code mới lên GitHub, người dùng mở trang web trên trình duyệt nhưng trang web không nhận phiên bản mới (vẫn chạy mã nguồn cũ, giao diện cũ).
- **Nguyên nhân cốt lõi**:
  1. **Bộ nhớ đệm trình duyệt (Browser Cache)**: Các trình duyệt (Chrome, Safari, Edge, Cốc Cốc) tự động cache các file HTML, JS, CSS vào bộ nhớ đệm máy khách. Khi người dùng mở trang, trình duyệt đọc lại bản cache cũ thay vì tải bản mới từ hosting.
  2. **Chưa có cấu hình cấm cache HTML trên máy chủ hosting**: Chưa có file `.htaccess` để chỉ định `Cache-Control: no-cache, no-store, must-revalidate` cho các file HTML và JSON.
  3. **Chưa có cơ chế Version Manifest và Auto-reload**: Mỗi lần GitHub Actions build & deploy lên hosting qua FTP, hệ thống chưa tự tạo file nhận diện phiên bản (`version.json`), và máy khách chưa có cơ chế định kỳ kiểm tra phiên bản mới để tự động xóa cache và reload trang.

---

## Phạm vi

1. **Xử lý cảnh báo lệch tiết và phát hiện 1 lớp 2 người dạy**:
   - Bỏ qua tuần đã qua: Chỉ tính và cảnh báo cho tuần đang xem / tuần hiện tại trở đi.
   - Phát hiện và cảnh báo "1 lớp 2 người cùng dạy": Nêu rõ tên các GV cùng dạy và số tiết.
   - Bỏ chặn cứng trong gửi email cá nhân: chuyển thành thông báo xác nhận gửi.
2. **Cải tiến thuật toán phân đoạn PPCT đa tuần liên tục**:
   - Bài 11 học ở Tuần 4, 5, 6 (mỗi tuần 1 tiết) -> phân đoạn lũy kế chuẩn xác `1/3, 2/3, 3/3`.
   - Chuẩn hóa định dạng hiển thị: `Tuần [X]  [Tên bài dạy] (tiết ppct: [Y]) [A/B]`.
3. **Tick chọn nhiều giáo viên và gửi TKB qua email cá nhân**:
   - Checkbox từng GV, nút chọn tất cả / bỏ chọn trong tab Thời khóa biểu.
   - Nút gửi TKB các GV đã chọn về email cá nhân dạng bảng TKB trực quan, phân tách từng GV, không có lịch báo giảng.
4. **Cơ chế tự động reload toàn bộ web mỗi lần đẩy lên GitHub cho toàn hệ thống `hoangthiencm.id.vn`**:
   - **Tự động sinh `version.json` trong GitHub Actions**: Mỗi lần push lên GitHub, workflow `.github/workflows/ftp-deploy.yml` tự tạo file `version.json` chứa commit SHA và timestamp mới nhất rồi đồng bộ lên hosting.
   - **Cấu hình `.htaccess` chống cache HTML/JSON**: Đặt ở thư mục gốc hosting, yêu cầu mọi trình duyệt luôn kiểm tra phiên bản mới nhất của file `.html` và `version.json`.
   - **Tích hợp module Auto-Reload vào `js/security-guard.js`**:
     + Vì `js/security-guard.js` đã được nạp sẵn ở đầu `<head>` của toàn bộ các file HTML trong hệ thống (60+ trang), việc tích hợp tại đây bảo đảm **100% mọi trang web trên `hoangthiencm.id.vn` đều tự động hưởng cơ chế auto-reload** mà không cần sửa từng trang HTML riêng lẻ.
     + Script tự động fetch `/version.json?_t=${Date.now()}`. Nếu phát hiện phiên bản trên server mới hơn phiên bản đang chạy ở máy khách: tự động xóa cache và reload ngay lập tức (`window.location.reload(true)`).
     + Khi người dùng đang mở tab: Tự động kiểm tra lại khi chuyển tab quay lại (`visibilitychange`, `focus`) hoặc định kỳ mỗi 60 giây.

---

## Ngoài phạm vi

- Không thay đổi cấu trúc LocalStorage cốt lõi.
- Không can thiệp vào các module Phân công chuyên môn, Quản lý chấm công, Dạy thay.

---

## File dự kiến tác động

1. `.github/workflows/ftp-deploy.yml`:
   - Bổ sung bước tự động tạo file `version.json` trước khi sync FTP lên hosting.
2. `.htaccess`:
   - Tạo file `.htaccess` tại thư mục gốc với cấu hình `Cache-Control: no-cache, no-store, must-revalidate` cho `.html` và `.json`.
3. `js/security-guard.js`:
   - Bổ sung logic kiểm tra phiên bản tự động (`checkAppVersionUpdate()`), lưu phiên bản hiện tại vào `localStorage`, và tự động reload trang khi phát hiện bản deploy mới từ GitHub.
4. `phancongtochuyenmon.html`:
   - Hoàn thiện tính năng checkbox chọn nhiều giáo viên và hàm `sendSelectedTeachersTimetableEmail()` / `buildSelectedTeachersTimetableEmail()`.
5. `tests/baogiang-weekday-segment-smoke.js`:
   - Đảm bảo test phân đoạn đa tuần, lọc tuần cũ và cảnh báo 2 GV đạt PASS.
6. `tests/timetable-render-smoke.js`:
   - Bổ sung test case kiểm tra tính năng tick chọn nhiều giáo viên và hàm sinh mã HTML email TKB đa giáo viên.
7. `tests/auto-reload-smoke.js`:
   - Tạo test tự động kiểm tra cơ chế so khớp `version.json` và logic phát hiện bản cập nhật mới.

---

## Các bước thực hiện

### Bước 1: Triển khai tính năng tự động reload toàn bộ web khi push GitHub
1. Cập nhật `.github/workflows/ftp-deploy.yml`:
   - Thêm bước sinh `version.json`:
     ```yaml
     - name: Generate version manifest
       run: node -e "require('fs').writeFileSync('version.json', JSON.stringify({ version: process.env.GITHUB_SHA || String(Date.now()), deployed_at: new Date().toISOString() }, null, 2))"
     ```
2. Tạo file `.htaccess` tại root:
   - Cấu hình chỉ thị chống cache cho file HTML và JSON:
     ```apache
     <FilesMatch "\.(html|htm|json)$">
         Header set Cache-Control "no-cache, no-store, must-revalidate, max-age=0"
         Header set Pragma "no-cache"
         Header set Expires "0"
     </FilesMatch>
     ```
3. Bổ sung cơ chế auto-reload vào `js/security-guard.js`:
   - Hàm `initAutoUpdateChecker()`:
     + Tải `version.json?_t=${Date.now()}`.
     + So sánh `serverVersion` với `localStorage.getItem('__system_app_version__')`.
     + Nếu khác nhau và đã có phiên bản trước đó: Cập nhật version mới và gọi `window.location.reload(true)`.
     + Nếu là lần đầu mở: Ghi nhận version.
     + Lắng nghe `document.addEventListener('visibilitychange')` và kiểm tra định kỳ mỗi 60 giây.

### Bước 2: Hoàn thiện tính năng tick chọn GV và gửi TKB qua email trong `phancongtochuyenmon.html`
1. Thêm `selectedTimetableTeacherIds = new Set()` và ô checkbox cho từng GV trong `renderTimetableTeacherList()`.
2. Thêm nút "Chọn tất cả GV có TKB", "Bỏ chọn" và nút "Gửi TKB các GV đã chọn qua email".
3. Xây dựng hàm `buildSelectedTeachersTimetableEmail(teacherIds)` tạo mẫu HTML bảng TKB riêng biệt cho từng giáo viên (không có lịch báo giảng).
4. Xây dựng hàm `sendSelectedTeachersTimetableEmail()` gửi payload tới `api/baogiang_mail.php`.

### Bước 3: Đảm bảo các chức năng Báo giảng và cảnh báo TKB
- Giữ vững thuật toán PPCT đa tuần 3 tuần liên tiếp (Bài 11: `1/3, 2/3, 3/3`).
- Giữ vững logic bỏ tuần cũ và cảnh báo 1 lớp 2 giáo viên cùng dạy.

### Bước 4: Viết test tự động và nghiệm thu
- Chạy toàn bộ test suites: `baogiang-weekday-segment-smoke.js`, `timetable-render-smoke.js` và `auto-reload-smoke.js`.

---

## Rủi ro

- **Vòng lặp reload vô tận (Reload loop)**: Nếu `version.json` không lưu được vào `localStorage` hoặc bị lỗi mạng.
  - *Kiểm soát*: Chỉ reload khi `serverVersion` hợp lệ, khác với `currentVersion`, và có debounce tối thiểu 10 giây giữa 2 lần reload.
- **Trình duyệt chặn request ngầm**:
  - *Kiểm soát*: Dùng `fetch` với cache `no-store` và bọc trong `try...catch`, không làm gián đoạn trải nghiệm người dùng nếu mất mạng.

---

## Cách kiểm thử

1. **Kiểm thử tự động bằng script**:
   - `node tests/baogiang-weekday-segment-smoke.js` -> PASS.
   - `node tests/timetable-render-smoke.js` -> PASS.
   - `node tests/auto-reload-smoke.js` -> PASS.
2. **Kiểm thử thực tế**:
   - Kiểm tra file `version.json` sinh ra hợp lệ.
   - Kiểm tra cơ chế reload: Khi đổi giá trị version trong mock, script phát hiện và kích hoạt reload.
   - Kiểm tra giao diện TKB: Tick chọn 2 giáo viên và bấm gửi email -> Nhận email bảng TKB phân tách rõ ràng từng GV.

---

## Tiêu chí nghiệm thu

1. **Tự động reload toàn bộ web khi push GitHub**:
   - File `version.json` tự động sinh ra mỗi lần push lên GitHub.
   - File `.htaccess` cấu hình chống cache cho HTML và JSON trên hosting `hoangthiencm.id.vn`.
   - `js/security-guard.js` tự động phát hiện phiên bản mới và reload trang, áp dụng cho toàn bộ các trang web trong hệ thống.
2. **Gửi TKB các GV được tick chọn qua email**:
   - Có ô checkbox chọn từng GV, chọn tất cả, bỏ chọn.
   - Gửi TKB của các GV được tick chọn qua email cá nhân thành công, hiển thị trực quan bảng TKB riêng biệt từng GV, không có lịch báo giảng.
3. **PPCT đa tuần và cảnh báo TKB**:
   - Bài 11 học tuần 4, 5, 6 hiển thị đúng `1/3, 2/3, 3/3`.
   - Tuần đã qua không bị cảnh báo; phát hiện và cảnh báo 1 lớp 2 người cùng dạy.
4. **Bộ test tự động**: Đạt **PASS 100%**.
