# VERIFY: Tách Riêng Các Môn Lịch Sử, Địa Lí, Vật Lí, Hoá Học, Sinh Học & Bỏ Qua Ràng Buộc Tổng Số Tiết

## Kết luận
PASS

## Đối chiếu Scope & Tính năng
- [x] **Tách toàn bộ các môn Lịch sử, Địa lí, Vật lí, Hoá học, Sinh học:**
  - `canvas_xaydungphuluc.html` & `xaydungphuluc.html` hiển thị đầy đủ trên thanh chọn môn học:
    - **Lịch sử**: 52 tiết/năm, icon 🏛
    - **Địa lí**: 53 tiết/năm, icon 🌍
    - **Vật lí**: 47 tiết/năm, icon ⚡
    - **Hoá học**: 43 tiết/năm, icon 🧪
    - **Sinh học**: 50 tiết/năm, icon 🌱
    - **Khoa học tự nhiên**: 140 tiết/năm, icon 🔬
    - **Lịch sử và Địa lí**: 105 tiết/năm, icon 🌏
- [x] **Nạp mục lục chuẩn SGK Thống nhất:**
  - Đã nạp đầy đủ 100% mục lục bài học chuẩn xác, phân chia chương mục rõ ràng cho cả 4 khối (6, 7, 8, 9) vào `js/khbd-curriculum.js` và `agent-tools/thcs-toc.json`.
- [x] **Nút tick Bỏ qua ràng buộc tổng số tiết:**
  - Xuất hiện ở cả Mục 1 và Mục 3, mặc định tick chọn.
  - Báo cáo thẩm định tự động đạt chuẩn 100% khi thời lượng linh hoạt theo phân phối nhà trường.
  - Tích hợp NLS và AI hoạt động trơn tru theo số tiết thực tế của bảng PPCT.
- [x] **Ô nhập số tiết/năm tùy chỉnh:**
  - Cho phép giáo viên nhập số tiết riêng của trường mình (ví dụ 48, 50, 52, 54 tiết) nếu cần.
- [x] **Kho Tri thức SGK dùng chung & Xử lý sự cố môn Địa lí 8**:
  - Đã rà soát toàn diện máy chủ `https://hoangthiencm.id.vn/api/sgk_knowledge.php`.
  - Xóa bỏ Book ID 65 (Địa lí 8 nạp nhầm bài Toán) và các Book ID 27, 39, 51, 63 (GDDP nạp nhầm bài Toán).
  - Khởi tạo Book ID 66: Địa lí 8 chuẩn xác 100% gồm đúng 14 bài của CTGDPT 2018 (Bài 1: Vị trí địa lí và phạm vi lãnh thổ Việt Nam,...).
  - Nạp đầy đủ SGK chuẩn cho toàn bộ 5 phân môn mới (Lịch sử, Địa lí, Vật lí, Hoá học, Sinh học) và Giáo dục địa phương ở cả 4 khối (6, 7, 8, 9).
  - Sửa hàm gập ký tự `Đ`/`đ` trong `foldText` và regex nhận diện môn trong `canvas_xaydungphuluc.html` và `xaydungphuluc.html`.
  - Cơ chế Auto-purge Cache tự động kích hoạt nếu phát hiện cache cũ lưu nhầm bài Toán.
- [x] **Cổng học tập học sinh & Phân quyền giao diện User**:
  - `login.html`: `landingPageFor` điều hướng tài khoản `student` về đúng `index.html` (Cổng học sinh), không ép nhảy thẳng vào một trang lộ trình cố định.
  - `index.html`:
    + Bỏ đoạn mã ép đá học sinh sang lộ trình ở đầu trang.
    + Thêm container `#studentPortalDeck` với giao diện người học: Lời chào, tên học sinh, lớp học.
    + Lọc hiển thị đúng các khối lớp Toán được phân quyền (`lotrinhtoan4` đến `lotrinhtoan9`).
    + Lọc hiển thị đúng các hoạt động/tiện ích được cấp quyền (`thitructuyen`, `nopbai`, `padlet`, `smartquiz`, `gslides`, `vehinh`).
    + Ẩn toàn bộ công cụ giáo viên, bảng điều khiển giáo viên, nút Cài đặt AI & Key, hướng dẫn nhanh.
    + Bảo lưu 100% không gian làm việc và bộ công cụ cho role `teacher`.
  - `access-control.js`: Chặn toàn bộ 18 trang công cụ giáo viên đối với học sinh và điều hướng về `index.html`.
- [x] **Không đề cập tên bộ sách trong hệ thống:**
  - Regex phủ định `!/kntt|kết nối tri thức/i` pass trên toàn bộ cấu hình, tên môn, nhãn và danh mục.
- [x] **Đường dẫn tài nguyên ổn định:**
  - Chuyển toàn bộ CDN/remote scripts sang relative paths (`js/khbd-curriculum.js`, `css/khbd-styles.css`,...).

## Test đã chạy
1. `python verify_patch.py`:
   - `test_curriculum_js`: PASSED
   - `test_thcs_toc`: PASSED (tất cả các môn cho 4 khối 6, 7, 8, 9)
   - `test_canvas_html`: PASSED
   - `test_xaydungphuluc_html`: PASSED
   - `test_regex_logic`: PASSED
   - Kết quả: **ALL TESTS PASSED WITH 100% SUCCESS!**
2. `python verify_period_bypass.py`:
   - Kiểm tra UI `#ignoreTotalPeriods`, `#ignoreTotalPeriodsSection3`, `#customAnnualPeriods`
   - Kiểm tra logic đồng bộ `syncIgnoreTotalPeriods`
   - Kiểm tra `getConfig`, `applyDraftConfig`, `calculateComplianceReport`, `defaultPpctRows`
   - Kết quả: **ALL CHECKS PASSED!**
3. `python verify_all_subjects_catalog.py`:
   - Kiểm tra live API `Địa lí 8`: Trả về chuẩn 14 bài học, bài đầu tiên "Bài 1: Vị trí địa lí và phạm vi lãnh thổ Việt Nam".
   - Kiểm tra 32 unit test phân tách chuỗi tên môn trong Javascript (`Địa lí`, `ĐỊA LÍ 8`, `Lịch sử 8`, `Vật lí 8`, `Hoá học 8`, `Sinh học 8`...): 32/32 PASSED.
4. `python audit_server_books.py`:
   - Quét toàn bộ sách trên cơ sở dữ liệu server live: Phát hiện **0 sách bị nhiễm bẩn** (`Total contaminated books found: 0`).
5. `python test_smoke_contracts.py`:
   - Kiểm tra hợp đồng Least-Privilege cho role Giáo viên trên `index.html`: PASSED.
6. `python test_student_portal.py`:
   - `test_login_landing_page`: PASSED
   - `test_access_control_guards`: PASSED
   - `test_index_student_portal`: PASSED
   - Kết quả: **ALL STUDENT PORTAL TESTS PASSED (100%)!**

## Bug
Không có.

