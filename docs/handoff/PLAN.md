# PLAN: Tối Ưu Hiệu Năng Nhập Liệu PPCT (Chống Lag) & Bổ Sung Tính Năng Lưu / Khôi Phục Tiến Trình Lên CSDL Người Dùng

## Hiện trạng
1. **Hiện tượng lag nặng khi nhập dữ liệu trong bảng PPCT (Mục 3)**:
   - Trong `xaydungphuluc.html`, hàm `updatePpctField` gọi `refreshPpctDependents()`, hàm này liên tục kích hoạt `updateAiPicker()` và gán lại `list.innerHTML`. Toàn bộ 60–100 dòng cùng hàng trăm ô input/checkbox bị xóa và vẽ lại trên từng thao tác sửa ô, gây mất focus, layout reflow toàn trang và độ trễ lớn khi gõ phím.
   - Vòng lặp `updateAiPicker` chứa thuật toán $O(N^2)$ lồng nhau khi gọi `aiPeriodCandidates()` trong mỗi dòng duyệt.
   - Quá trình chuẩn hóa phụ lục (`normalizeAppendix`) và render preview chạy đồng bộ liên tục mà không có bộ đệm (Debounce).
2. **Chưa có tính năng Lưu tiến trình làm dở lên Cơ sở dữ liệu (CSDL) của tài khoản người dùng**:
   - Hiện tại, toàn bộ dữ liệu đang làm việc (Cấu hình sư phạm, bảng PPCT đã nạp/sửa, các tiết AI đã tick chọn, ngữ cảnh SGK, kết quả sinh Phụ lục 1, 2, 3) chỉ tồn tại tạm thời trong bộ nhớ trình duyệt (RAM).
   - Khi giáo viên đang làm nửa chừng nhưng phải đổi máy tính, tải lại trang (F5) hoặc đóng trình duyệt, toàn bộ dữ liệu bị mất và phải làm lại từ đầu.
   - Người dùng có nhu cầu lưu trữ trực tiếp lên CSDL máy chủ gắn với tài khoản đang đăng nhập (`user_id`), không chỉ lưu tạm ở local máy cá nhân.

## Phạm vi
1. **Triệt tiêu lag nhập liệu bảng PPCT (Mục 3)**:
   - Cập nhật in-place vào dữ liệu bộ nhớ khi sửa ô (`lesson`, `tietCT`, `week`, `devices`, `location`), không xóa vẽ lại cây DOM của Mục 3.
   - Giảm độ phức tạp `updateAiPicker` từ $O(N^2)$ xuống $O(N)$ bằng `Map` gom nhóm tiết AI.
   - Áp dụng Debounce cho việc đồng bộ và render lại bảng xem trước ở Mục 7.
2. **Xây dựng tính năng Lưu / Tải bản nháp tiến trình lên CSDL máy chủ (`api/user_phuluc_draft.php`)**:
   - Tạo endpoint API chuẩn trên máy chủ PHP/MySQL:
     * `GET api/user_phuluc_draft.php`: Tải bản nháp mới nhất của tài khoản người dùng (xác thực qua session `$_SESSION['user_id']`).
     * `POST api/user_phuluc_draft.php`: Lưu gói dữ liệu tiến trình (payload JSON) lên CSDL gắn theo `user_id`.
   - Bảng CSDL `user_phuluc_drafts`:
     * Các trường: `id`, `user_id`, `mon_hoc`, `lop`, `nam_hoc`, `draft_data` (LONGTEXT JSON), `created_at`, `updated_at`.
   - Dữ liệu lưu trữ bao gồm:
     * Cấu hình sư phạm (Môn học, Khối lớp, Năm học, Trường, Tổ, Giáo viên, Tỉ lệ NLS/AI, Chỉ đạo riêng...).
     * Bảng PPCT nguồn (`sourcePpctRows`, `sourcePpctTable`).
     * Danh sách tiết AI đã chọn (`aiSelectedLessonIds`).
     * Ngữ cảnh SGK tinh gọn (`sgkCompactContext`, `sgkKnowledgeBase`).
     * Kết quả 3 Phụ lục (`results['1']`, `results['2']`, `results['3']`).
3. **Giao diện thao tác Lưu / Tải trên `xaydungphuluc.html`**:
   - Thêm nút `💾 Lưu lên CSDL` và `📂 Tải từ CSDL` trên thanh điều hướng/đầu trang và khu vực tiến trình.
   - Thông báo rõ ràng thời gian đã lưu gần nhất (ví dụ: `Đã lưu lên CSDL lúc 19:45`).
   - Tự động kiểm tra và gợi ý nạp bản nháp đã lưu khi người dùng đăng nhập mở trang.

## Ngoài phạm vi
- Không can thiệp các module khác không liên quan đến Phụ lục 5512.
- Không thay đổi nghiệp vụ sư phạm hay định dạng xuất Word đã chuẩn hóa.

## File dự kiến tác động
- `api/user_phuluc_draft.php` [TẠO MỚI: API LƯU VÀ TẢI BẢN NHÁP TIẾN TRÌNH THEO USER SESSION]
- `xaydungphuluc.html` [TỐI ƯU HIỆU NĂNG NHẬP LIỆU PPCT, BỔ SUNG GIAO DIỆN & HÀM LƯU/TẢI DRAFT TỪ CSDL MÁY CHỦ]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG TEST CASE HIỆU NĂNG VÀ ĐỒNG BỘ DRAFT CSDL]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Xây dựng backend API `api/user_phuluc_draft.php`**:
   - Tự động khởi tạo bảng `user_phuluc_drafts` (nếu chưa có) bằng PDO.
   - Xử lý xác thực người dùng qua `$_SESSION['user_id']`.
   - `GET`: Trả về `draft_data` kèm thông tin thời gian cập nhật.
   - `POST`: Nhận payload JSON, lưu/cập nhật `draft_data` theo `user_id`.
2. **Bước 2: Triệt tiêu hiện tượng lag khi nhập liệu trong `xaydungphuluc.html`**:
   - Viết lại `updatePpctField`: Cập nhật trực tiếp giá trị vào mảng dữ liệu mà không gọi `updateAiPicker()`.
   - Tối ưu `updateAiPicker`: Gom nhóm `aiPeriodCandidates` thành `Map` trước khi duyệt hàng để đạt độ phức tạp $O(N)$.
   - Áp dụng Debounce cho `renderPreview` khi cập nhật dữ liệu.
3. **Bước 3: Tích hợp hàm `saveDraftToServer()` và `loadDraftFromServer()` vào `xaydungphuluc.html`**:
   - Hàm `saveDraftToServer()`: Thu thập toàn bộ form, PPCT, AI selection, SGK context và results -> gửi POST lên `api/user_phuluc_draft.php` -> hiển thị thông báo thành công.
   - Hàm `loadDraftFromServer()`: Gửi GET lấy dữ liệu -> khôi phục form, nạp lại bảng PPCT Mục 3, khôi phục tick chọn AI, nạp lại preview Mục 7.
   - Thêm nút bấm trực quan `💾 Lưu lên CSDL` và `📂 Tải từ CSDL` trên giao diện.
4. **Bước 4: Cập nhật kiểm thử tự động `tests/xaydungphuluc-smoke.js`**:
   - Kiểm tra các hàm in-place update không gây lỗi giao diện.
   - Kiểm tra cấu trúc payload bản nháp lưu CSDL đầy đủ các trường cần thiết.
5. **Bước 5: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

## Rủi ro
1. **Rủi ro người dùng chưa đăng nhập khi bấm Lưu lên CSDL**:
   - *Giải pháp*: API trả về HTTP 401; giao diện hiển thị thông báo yêu cầu đăng nhập và hướng dẫn chuyển tới trang đăng nhập mà không làm mất dữ liệu hiện hành.
2. **Rủi ro dung lượng bản nháp quá lớn**:
   - *Giải pháp*: Dùng trường kiểu `LONGTEXT` trong MySQL; chỉ đóng gói dữ liệu JSON cần thiết (tối đa vài trăm KB), đảm bảo tốc độ lưu/tải dưới 200ms.

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh: `node tests/xaydungphuluc-smoke.js`
   - Chạy lệnh: `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html`:
     * Nhập liệu, sửa ô PPCT: Đảm bảo phản hồi mượt mà tức thì, không giật lag.
     * Bấm `💾 Lưu lên CSDL` -> Kiểm tra thông báo lưu thành công kèm thời gian.
     * Đặt lại form (Refresh / Reset) -> Bấm `📂 Tải từ CSDL` -> Kiểm tra toàn bộ cấu hình, bảng PPCT, các tiết AI đã chọn và kết quả xem trước được khôi phục chính xác 100%.

## Tiêu chí nghiệm thu
- [x] Nhập liệu trong bảng PPCT Mục 3 phản hồi tức thì, không còn hiện tượng full re-render hay giật lag.
- [x] Có API `api/user_phuluc_draft.php` lưu và tải bản nháp tiến trình theo tài khoản `user_id` trên CSDL máy chủ.
- [x] Giao diện có đầy đủ nút `💾 Lưu lên CSDL` và `📂 Tải từ CSDL`, hiển thị trạng thái lưu rõ ràng.
- [x] Khôi phục toàn diện: Cấu hình sư phạm, bảng PPCT nguồn, tiết AI đã chọn, ngữ cảnh SGK và kết quả Phụ lục 1, 2, 3.
- [x] 100% các bài kiểm thử tự động chạy đạt PASS.
