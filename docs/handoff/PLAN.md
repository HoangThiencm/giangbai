# Kế hoạch Triển khai: Chức năng Sổ Điểm & Kiểm Tra Thường Xuyên (sodiem.html)

## Hiện trạng & Phân tích Kiến trúc
- Hệ thống đã có các phân hệ phục vụ giảng dạy và kiểm tra:
  + `kttx.html`: Soạn đề kiểm tra thường xuyên từ ảnh SGK/PDF, lưu đề vào `saved_exams` (localStorage/GitHub).
  + `thitructuyen.html` & `api/exam.php`: Đã có sẵn API phân cấp lấy danh sách lớp học (`api/exam.php/student-classes`) và danh sách học sinh theo lớp (`api/exam.php/class-students?class_name=...`) từ bảng `users` (`role = 'student'`).
  + Hệ thống phân quyền giáo viên (`access-control.js`, `api/helpers.php`, `admin.html`, `index.html`) kiểm soát chặt chẽ các module công cụ theo cơ chế Least Privilege, được kiểm định qua smoke test `tests/teacher-permissions-smoke.js`.
- Yêu cầu mới từ người dùng:
  + Mở trang mới: `sodiem.html` để phục vụ Sổ điểm Kiểm tra thường xuyên (KTTX).
  + Lấy danh sách học sinh theo từng lớp từ hệ thống (kèm hỗ trợ nạp Excel/dán danh sách linh hoạt).
  + Tab quay số chiếc nón kỳ diệu (Lucky Wheel) để bốc thăm học sinh gọi lên bảng kiểm tra miệng / KTTX.
  + Cơ chế quay thông minh: Hạn chế tối đa hoặc loại trừ những học sinh đã có điểm ở cột hiện tại; khi toàn bộ lớp đã đủ điểm cột đó thì tự động kích hoạt vòng mới.
  + Mở rộng tiện ích sư phạm: Tích hợp ngân hàng đề/câu hỏi trực quan (kèm đồng hồ đếm ngược) khi gọi học sinh lên bảng, tính điểm trung bình KTTX, xuất Excel chuẩn mẫu.

## Phạm vi
1. **Trang giao diện ứng dụng `sodiem.html`:**
   - Xây dựng giao diện Responsive, chuẩn thiết kế hệ thống (Tailwind CSS, FontAwesome 6, Google Fonts, bảo vệ bằng `security-guard.js` và `access-control.js`).
   - Tích hợp 4 Tab chức năng mượt mà:
     - **Tab 1 - Sổ điểm điện tử:** Quản lý danh sách lớp, các cột điểm KTTX (KTTX 1, KTTX 2, KTTX 3, KTTX 4, điểm miệng, 15 phút...), tính ĐTBtx, nhận xét, nhập điểm inline bằng bàn phím (hỗ trợ phím mũi tên / Enter).
     - **Tab 2 - Chiếc nón kỳ diệu (Vòng quay may mắn):** Vẽ Canvas HTML5 bánh xe quay động, hiệu ứng âm thanh AudioContext, pháo hoa confetti, thuật toán ưu tiên học sinh chưa có điểm, tự động sang vòng mới khi đủ 1 cột, popup nhập điểm ngay khi quay trúng.
     - **Tab 3 - Đề kiểm tra & Câu hỏi vấn đáp:** Hiển thị câu hỏi to rõ cho học sinh trả lời, hỗ trợ công thức Toán KaTeX, đồng hồ bấm giờ đếm ngược (30s, 60s, 120s...), liên kết đề đã lưu từ `kttx.html` hoặc ngân hàng câu hỏi nhanh.
     - **Tab 4 - Thống kê & Xuất dữ liệu:** Biểu đồ phổ điểm, tỷ lệ hoàn thành cột điểm, xuất bảng điểm ra Excel (`.xlsx`) bằng SheetJS, in ấn.
2. **Nguồn dữ liệu học sinh & Lưu trữ:**
   - Gọi API có sẵn `api/exam.php/student-classes` và `api/exam.php/class-students` để nạp danh sách lớp và học sinh thực tế.
   - Hỗ trợ nhập file Excel danh sách học sinh (kéo thả `.xlsx`, `.xls`, `.csv`).
   - Lưu trữ tự động tại `localStorage` theo từng lớp, môn, năm học; hỗ trợ xuất/nhập tệp sao lưu JSON.
   - Xây dựng API `api/sodiem.php` (hoặc tích hợp backend) để lưu trữ đồng bộ bảng điểm lên cơ sở dữ liệu khi có kết nối mạng.
3. **Cấu hình phân quyền & Điều hướng toàn hệ thống:**
   - Cập nhật `access-control.js`: Khai báo route `sodiem.html` <-> `sodiem`, thêm vào `teacherWorkspacePageKeys`.
   - Cập nhật `api/helpers.php`: Thêm `sodiem` vào `page_catalog()`, `teacher_workspace_page_ids()`, `teacher_feature_keys_for_pages()`.
   - Cập nhật `admin.html`: Thêm checkbox cấp quyền "Sổ Điểm & KTTX" (`cfg_sodiem`) cho tài khoản giáo viên.
   - Cập nhật `index.html`: Thêm thẻ công cụ "Sổ Điểm & KTTX" vào Bento Grid trên trang chủ.
   - Cập nhật `tests/teacher-permissions-smoke.js` và tạo test mới `tests/sodiem-smoke.js`.

## Ngoài phạm vi
- Không can thiệp vào các trang công cụ khác (`kttx.html`, `thitructuyen.html`, `matrande.html`, `soankhbd.html`).
- Không sửa đổi cấu trúc bảng `users` trong cơ sở dữ liệu.

## File dự kiến tác động
1. **Tạo mới:** `sodiem.html` — Ứng dụng Sổ điểm & Chiếc nón kỳ diệu gọi học sinh lấy điểm KTTX.
2. **Tạo mới:** `api/sodiem.php` — API backend quản lý lưu trữ và đồng bộ dữ liệu sổ điểm theo giáo viên và lớp.
3. **Cập nhật:** `access-control.js` — Đăng ký route guard cho `sodiem.html`.
4. **Cập nhật:** `api/helpers.php` — Đăng ký page catalog và workspace permission cho `sodiem`.
5. **Cập nhật:** `admin.html` — Đăng ký quyền công cụ trong bảng quản trị admin.
6. **Cập nhật:** `index.html` — Thêm thẻ mở Sổ Điểm KTTX trên trang chủ giáo viên.
7. **Cập nhật:** `tests/teacher-permissions-smoke.js` — Bổ sung `sodiem` vào static contract tests.
8. **Tạo mới:** `tests/sodiem-smoke.js` — Smoke test tự động kiểm tra cú pháp, cấu trúc tab, Canvas wheel và tính toàn vẹn của `sodiem.html`.

## Các bước thực hiện chi tiết

### Bước 1: Khai báo hạ tầng phân quyền và liên kết hệ thống
- Trong `api/helpers.php`:
  + Thêm phần tử `'sodiem' => ['title' => 'Sổ điểm & KTTX', 'url' => 'sodiem.html']` vào hàm `page_catalog()`.
  + Thêm `'sodiem'` vào danh sách `teacher_workspace_page_ids()`.
  + Thêm `'sodiem' => 'sodiem'` vào `teacher_feature_keys_for_pages()`.
- Trong `access-control.js`:
  + Thêm `'sodiem.html': 'sodiem'` vào `pageKeys`.
  + Thêm `'sodiem': 'sodiem.html'` vào `pageUrls`.
  + Thêm `'sodiem'` vào mảng danh sách các trang workspace giáo viên.
- Trong `admin.html`:
  + Thêm checkbox `cfg_sodiem` vào phần cấu hình quyền công cụ giáo viên.
  + Bổ sung `'sodiem'` vào mảng `CLIENT_FEATURE_CHECKS` và các bảng mã trang giáo viên.
- Trong `index.html`:
  + Thêm khối thẻ `tool-tile` cho `data-tool="sodiem"`, liên kết tới `sodiem.html` với biểu tượng sổ điểm và mô tả tính năng.
- Chạy cập nhật `tests/teacher-permissions-smoke.js` để xác nhận hợp đồng phân quyền đạt PASS.

### Bước 2: Xây dựng Backend API `api/sodiem.php`
- Kiểm tra phiên bản schema tự động (`gradebooks` table):
  ```sql
  CREATE TABLE IF NOT EXISTS gradebooks (
      id INT AUTO_INCREMENT PRIMARY KEY,
      teacher_id INT NOT NULL,
      class_name VARCHAR(80) NOT NULL,
      subject VARCHAR(80) NOT NULL,
      academic_year VARCHAR(30) NOT NULL DEFAULT '2025-2026',
      columns_config_json TEXT DEFAULT NULL,
      students_data_json LONGTEXT DEFAULT NULL,
      history_log_json LONGTEXT DEFAULT NULL,
      updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      UNIQUE KEY uniq_teacher_class_sub (teacher_id, class_name, subject, academic_year),
      INDEX idx_gradebooks_class (class_name)
  ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```
- Cung cấp các hành động (Actions):
  + `GET ?action=load&class_name=...&subject=...`: Tải sổ điểm đã lưu của giáo viên.
  + `POST ?action=save`: Lưu/cập nhật toàn bộ sổ điểm (cấu hình cột, điểm số học sinh, lịch sử quay).
  + `GET ?action=classes`: Trả về danh sách lớp học và sĩ số.

### Bước 3: Phát triển giao diện và logic hoàn chỉnh cho `sodiem.html`
- **Head & Thư viện:**
  + Tích hợp `security-guard.js`, `access-control.js`.
  + Nạp Tailwind CSS CDN, FontAwesome 6, KaTeX (để hiển thị công thức toán đề bài), SheetJS `xlsx.full.min.js` (nhập/xuất Excel), Canvas Confetti (`canvas-confetti`).
- **Thanh tác vụ & Chọn lớp:**
  + Bộ chọn lớp: Nạp danh sách lớp từ `api/exam.php/student-classes` hoặc `api/sodiem.php`.
  + Khi chuyển lớp: Nạp danh sách học sinh từ API `class-students`, tự động map vào bảng điểm.
  + Nút chức năng: Thêm học sinh, Nhập Excel danh sách, Xuất Excel bảng điểm, Lưu dữ liệu, Cài đặt vòng quay.
- **Tab 1 - Sổ điểm điện tử:**
  + Render bảng danh sách học sinh: STT, Mã định danh/SBD, Họ và tên, các cột điểm KTTX 1, KTTX 2, KTTX 3, KTTX 4 (có nút thêm cột tùy chọn), ĐTBtx, Nhận xét nhanh.
  + Hỗ trợ chỉnh sửa điểm trực tiếp (inline edit): Giới hạn 0 - 10, tự động bôi màu theo thang điểm.
  + Điều hướng bàn phím: Enter xuống dòng, Tab sang cột kế tiếp, mũi tên điều hướng ô nhập.
  + Nút icon gọi nhanh học sinh đó sang tab vòng quay / kiểm tra miệng.
- **Tab 2 - Vòng quay may mắn (Chiếc nón kỳ diệu):**
  + Canvas bánh xe quay mượt mà 60fps với các múi màu sinh động và tên học sinh.
  + Bộ chọn: "Đang kiểm tra cột điểm nào?" (mặc định KTTX 1 hoặc cột giáo viên chọn).
  + Logic lọc thông minh:
    * Đếm số học sinh đã có điểm / chưa có điểm ở cột đang chọn.
    * Tùy chọn lọc: **Chỉ quay HS chưa có điểm** (ưu tiên 100%) hoặc **Hạn chế HS đã có điểm** (trọng số giảm còn 5%).
    * **Kiểm tra hoàn thành vòng:** Nếu tất cả học sinh đều đã có điểm ở cột này (100%), hiển thị thông báo "Đã hoàn thành vòng kiểm tra [Tên cột]!" và tự động kích hoạt vòng mới (cho phép quay lại từ đầu hoặc chuyển sang cột KTTX tiếp theo).
  + Hiệu ứng âm thanh bằng Web Audio API: Tiếng gõ kim tạch tạch theo gia tốc quay của bánh xe và tiếng chuông reo vui tai khi dừng.
  + Popup/Modal vinh danh học sinh: Hiện tên học sinh trúng số, kèm đề bài gợi ý, ô nhập điểm tại chỗ (0 - 10) và nút lưu ngay vào sổ điểm mà không cần chuyển tab.
- **Tab 3 - Ngân hàng đề & Câu hỏi vấn đáp:**
  + Bộ câu hỏi kiểm tra nhanh theo khối (Toán 6, 7, 8, 9) hoặc lấy từ các đề `saved_exams` của `kttx.html`.
  + Cho phép giáo viên dán danh sách câu hỏi nhanh của riêng mình.
  + Giao diện trình chiếu câu hỏi chữ lớn, rõ ràng cho máy chiếu lớp học.
  + Đồng hồ bấm giờ đếm ngược (Countdown Timer) 15s, 30s, 60s, 2 phút kèm âm báo khi hết giờ.
  + Nút bốc thăm câu hỏi ngẫu nhiên không trùng lặp cho mỗi lượt gọi học sinh.
- **Tab 4 - Báo cáo & Thống kê:**
  + Thống kê tiến độ lấy điểm theo từng cột (Bao nhiêu % đã có điểm).
  + Phổ điểm trực quan, tỷ lệ Giỏi, Khá, Đạt, Chưa đạt.
  + Xuất file Excel bảng điểm chuẩn form.

### Bước 4: Kiểm thử và hoàn thiện
- Chạy kiểm tra tĩnh và hợp đồng phân quyền: `node tests/teacher-permissions-smoke.js`.
- Tạo và chạy test: `node tests/sodiem-smoke.js` kiểm tra sự tồn tại của các thành phần bắt buộc trong `sodiem.html`.

## Rủi ro & Giải pháp
1. **Rủi ro:** Khi lớp học chưa có danh sách trong database, giáo viên không dùng được vòng quay.
   - **Giải pháp:** Tích hợp nút nạp file Excel hoặc dán danh sách thủ công trực tiếp trên giao diện, lưu vào `localStorage`, giáo viên dùng được ngay cả khi không có kết nối cơ sở dữ liệu.
2. **Rủi ro:** Lớp đông (40 - 45 học sinh), các nan quạt trên bánh xe bị quá hẹp chữ.
   - **Giải pháp:** Khi danh sách trên 30 học sinh, Canvas tự động hiển thị số thứ tự (STT) hoặc tên ngắn gọn trên nan quạt kèm bảng chỉ số bên cạnh, hoặc chỉ nạp vào bánh xe danh sách những học sinh chưa có điểm (thường từ 10 - 20 em mỗi đợt quay), giúp bánh xe luôn thông thoáng, chữ to rõ.
3. **Rủi ro:** Trình duyệt chặn âm thanh tự động (Autoplay Policy).
   - **Giải pháp:** Khởi tạo `AudioContext` sau cú click chuột đầu tiên của người dùng (khi bấm nút QUAY), đảm bảo âm thanh phát mượt mà trên mọi trình duyệt.

## Tiêu chí nghiệm thu
1. Truy cập `sodiem.html` có route guard chuẩn phân quyền giáo viên, liên kết từ `index.html` và hiển thị trong `admin.html`.
2. Lấy được danh sách lớp học và học sinh từ API `exam.php` hoặc tải từ file Excel.
3. Vòng quay chiếc nón kỳ diệu hoạt động mượt mà, có âm thanh quay và pháo hoa chúc mừng.
4. Thuật toán hạn chế/loại trừ học sinh đã có điểm hoạt động chính xác; khi 100% học sinh đã có điểm ở một cột thì bắt đầu vòng mới theo đúng yêu cầu.
5. Nhập điểm trực tiếp trên sổ điểm hoặc ngay trên popup sau khi quay, dữ liệu được bảo lưu an toàn.
6. Có tính năng hiển thị câu hỏi/đề kiểm tra kèm đồng hồ đếm ngược.
7. Toàn bộ smoke test (`teacher-permissions-smoke.js`, `sodiem-smoke.js`) đạt PASS.
