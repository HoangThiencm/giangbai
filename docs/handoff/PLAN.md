# PLAN: Tổ chức Quản lý Lưu & Tải Bản Kế hoạch Phụ lục Theo Môn học, Khối lớp, Năm học trên CSDL

## Hiện trạng
1. **Lưu đè đơn nhất (Single Draft Per User)**:
   - Trong `api/user_phuluc_draft.php`, bảng `user_phuluc_drafts` có ràng buộc `UNIQUE KEY uniq_user_phuluc_draft_user (user_id)`.
   - Mỗi người dùng chỉ lưu được **duy nhất 1 bản ghi** trên toàn bộ hệ thống. Khi giáo viên soạn nhiều môn (Toán 6, Toán 7, Tin học...) hoặc nhiều khối lớp/kỳ học khác nhau, việc bấm "Lưu lên CSDL" sẽ lập tức ghi đè và làm mất bản kế hoạch của môn/lớp trước đó.
2. **Không phân loại Môn học, Lớp, Năm học và Thiếu Tên bản lưu**:
   - Nút "Lưu lên CSDL" trên thanh header và section 6 chỉ gửi dữ liệu ngầm lên API mà không hiển thị thông tin xác nhận: đang lưu cho Môn gì, Lớp mấy, Năm học nào, Tiêu đề bản lưu là gì.
   - Nút "Tải từ CSDL" chỉ tải về 1 bản ghi duy nhất mà không cho người dùng biết bản nháp đó thuộc Môn nào, Lớp mấy, lưu vào thời gian nào trước khi quyết định nạp đè vào trình soạn thảo.
3. **Thiếu giao diện Quản lý Danh sách Bản lưu (Draft Manager Modal)**:
   - Chưa có modal danh sách các bản kế hoạch đã lưu để giáo viên tìm kiếm, lọc theo Môn học/Khối lớp/Năm học, xem ngày cập nhật, số lượng bài học/tiết AI đã thiết lập.
   - Chưa có chức năng Xóa bản lưu cũ hoặc chọn Lưu thành bản mới (Save as new) vs Lưu đè bản hiện tại (Update existing).

## Phạm vi
1. **Nâng cấp CSDL & API Backend (`api/user_phuluc_draft.php`)**:
   - Xóa bỏ ràng buộc `UNIQUE KEY uniq_user_phuluc_draft_user (user_id)` để mỗi giáo viên có thể quản lý nhiều bản kế hoạch độc lập.
   - Bổ sung/chuẩn hóa các trường metadata: `title` (Tiêu đề bản kế hoạch), `mon_hoc` (Môn học), `lop` (Khối lớp), `nam_hoc` (Năm học), `appendix_type` (Loại phụ lục), `summary` (Tóm tắt thông tin: số bài, số tiết AI, tiến trình).
   - Thêm các API actions:
     * `GET api/user_phuluc_draft.php?action=list` (hoặc lọc `mon_hoc`, `lop`, `nam_hoc`): Trả về danh sách bản lưu gồm `id`, `title`, `mon_hoc`, `lop`, `nam_hoc`, `appendix_type`, `summary`, `created_at`, `updated_at`.
     * `GET api/user_phuluc_draft.php?id={id}`: Trả về chi tiết `draft_data` và cấu hình của bản lưu được chỉ định.
     * `POST api/user_phuluc_draft.php`: Hỗ trợ lưu bản mới (`save_mode: 'new'`) hoặc cập nhật bản hiện tại (`id` xác định).
     * `POST api/user_phuluc_draft.php?action=delete` (hoặc DELETE method với `id`): Xóa bản lưu theo `id` của đúng `user_id` sở hữu.
2. **Xây dựng Giao diện & Modal Tổ chức Lưu / Tải trên Client (`xaydungphuluc.html`)**:
   - **Modal "Lưu bản kế hoạch lên CSDL" (`#saveDraftModal`)**:
     * Hiển thị rõ ràng: Môn học, Khối lớp, Năm học, Tên trường, Tổ chuyên môn.
     * Cho phép nhập/chỉnh sửa Tên bản kế hoạch (Gợi ý tự động: `Kế hoạch [Môn] [Lớp] - Năm học [Năm]`).
     * Hiển thị thống kê nhanh: Số lượng bài học PPCT, số tiết AI đã tick chọn, trạng thái các phụ lục 1, 2, 3 đã sinh.
     * Tùy chọn thao tác rõ ràng: "Lưu thành bản mới" hoặc "Cập nhật bản đang mở".
   - **Modal "Quản lý & Tải bản kế hoạch từ CSDL" (`#loadDraftModal`)**:
     * Bộ lọc nhanh theo Môn học, Khối lớp, Năm học và ô tìm kiếm theo tên.
     * Danh sách bảng/thẻ trực quan: Tên kế hoạch, Môn học - Lớp, Năm học, Thống kê, Thời gian lưu/cập nhật cuối cùng.
     * Nút "Mở / Tải" để nạp vào giao diện (tự động cập nhật `grade`, `subject`, `schoolYear`, bảng PPCT, danh sách tiết AI, kết quả xem trước).
     * Nút "Xóa" kèm hộp thoại xác nhận an toàn.
   - **Quản lý ngữ cảnh bản nháp hiện tại (Active Draft Context)**:
     * Lưu trữ `currentDraftId` và `currentDraftTitle`.
     * Cập nhật thông báo thanh trạng thái (`#draftStatus`): `Đang làm việc: [Tên kế hoạch] (Môn [Môn], Lớp [Lớp]) · Đã lưu CSDL lúc HH:mm - DD/MM/YYYY`.
3. **Cập nhật Bộ Kiểm thử Tự động (`tests/xaydungphuluc-smoke.js`)**:
   - Bổ sung kiểm thử cho các hàm quản lý bản lưu nhiều mục (`openSaveDraftModal`, `openLoadDraftModal`, `fetchDraftList`, `saveDraftToServer`, `loadDraftById`, `deleteDraftFromServer`).
   - Kiểm tra cấu trúc CSDL và các action API mới không làm gãy tương thích ngược.

## Ngoài phạm vi
- Không thay đổi thuật toán sinh nội dung YCCĐ và đối chiếu chuẩn NLS (CV 3456) / AI (QĐ 2422).
- Không thay đổi định dạng xuất tệp DOCX / ZIP.

## File dự kiến tác động
- `api/user_phuluc_draft.php` [NÂNG CẤP SCHEMA BỎ UNIQUE USER_ID, THÊM CÁC ENDPOINT LIST, GET BY ID, CREATE/UPDATE, DELETE]
- `xaydungphuluc.html` [THÊM MODAL LƯU CSDL VỚI TÊN/MÔN/LỚP, MODAL QUẢN LÝ TẢI BẢN LƯU CÓ LỌC, CẬP NHẬT TRẠNG THÁI ACTIVE DRAFT]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG TEST CASE CHO ĐA BẢN LƯU, MODAL QUẢN LÝ VÀ API ACTIONS]
- `docs/handoff/PLAN.md` [GHI ĐÈ KẾ HOẠCH THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Nâng cấp Backend `api/user_phuluc_draft.php`**:
   - Viết hàm migration tự động:
     * Kiểm tra và `DROP INDEX uniq_user_phuluc_draft_user` nếu còn tồn tại.
     * Thêm cột `title VARCHAR(255)`, `appendix_type VARCHAR(30)`, `summary VARCHAR(255)` nếu chưa có.
     * Thêm index `idx_user_phuluc_drafts_user (user_id)`, `idx_user_phuluc_drafts_mon_lop (user_id, mon_hoc, lop)`.
   - Xử lý các request method & action:
     * `GET ?action=list`: Trả về mảng các bản lưu rút gọn của `user_id` hiện tại (sắp xếp `updated_at DESC`).
     * `GET ?id={id}`: Lấy bản ghi chi tiết theo ID.
     * `GET` (không tham số): Nếu có bản ghi mới nhất thì trả về kèm danh sách hoặc bản gần nhất (đảm bảo tương thích ngược).
     * `POST`: Nhận payload `{ id, title, save_mode, draft }`, trích xuất `mon_hoc`, `lop`, `nam_hoc` từ `draft.config`, sinh tóm tắt `summary`, thực hiện INSERT bản mới hoặc UPDATE theo `id`.
     * `POST ?action=delete` hoặc `DELETE`: Xóa bản ghi theo `id` thuộc `user_id`.
2. **Bước 2: Xây dựng Modal & Giao diện trên `xaydungphuluc.html`**:
   - Thêm HTML cho Modal Lưu `#saveDraftModal`:
     * Hiển thị thông tin Môn học, Khối lớp, Năm học hiện tại.
     * Trường nhập tiêu đề bản lưu `#draftTitleInput` (tự động điền theo cấu hình hiện hành).
     * Bảng tóm tắt nội dung (số bài học PPCT, số tiết AI, các phụ lục đã tạo).
     * Nút "Lưu bản mới" và nút "Lưu đè bản hiện tại" (nếu đang mở từ một bản lưu có `currentDraftId`).
   - Thêm HTML cho Modal Tải `#loadDraftModal`:
     * Thanh công cụ lọc: Lọc theo Môn học, Khối lớp, Năm học, ô tìm kiếm nhanh.
     * Vùng danh sách bản lưu `#draftListContainer` hiển thị thẻ/bảng gồm: Tiêu đề, Môn - Lớp, Năm học, Tóm tắt, Ngày lưu, Nút "Mở", Nút "Xóa".
   - Viết các hàm JS điều khiển:
     * `openSaveDraftModal()`, `closeSaveDraftModal()`, `submitSaveDraft(mode)`.
     * `openLoadDraftModal()`, `closeLoadDraftModal()`, `fetchAndRenderDraftList()`, `loadDraftById(id)`, `deleteDraftFromServer(id)`.
     * Cập nhật `saveDraftToServer()` và `loadDraftFromServer()` để mở các modal trực quan tương ứng thay vì lưu ngầm thiếu thông tin.
     * Cập nhật `setDraftStatus(draftInfo)` hiển thị chi tiết tên bản kế hoạch, môn, lớp và thời gian lưu.
3. **Bước 3: Cập nhật Kiểm thử Tự động `tests/xaydungphuluc-smoke.js`**:
   - Bổ sung assertions kiểm tra các phần tử modal lưu/tải mới (`#saveDraftModal`, `#loadDraftModal`, `#draftTitleInput`, `#draftListContainer`).
   - Kiểm tra các hàm JS đa bản lưu (`openSaveDraftModal`, `openLoadDraftModal`, `buildDraftSummary`, `loadDraftById`, `deleteDraftFromServer`).
   - Kiểm tra tính tương thích của API `user_phuluc_draft.php` với cấu trúc đa bản lưu.
4. **Bước 4: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

## Rủi ro
1. **Rủi ro mất dữ liệu bản nháp cũ của người dùng trong quá trình migrate CSDL**:
   - *Giải pháp*: Script migrate chỉ drop UNIQUE index và bổ sung các cột mới với giá trị mặc định (`DEFAULT ''`), giữ nguyên toàn bộ dữ liệu `draft_data` hiện có trong bảng.
2. **Rủi ro người dùng vô tình ghi đè bản kế hoạch khác khi lưu**:
   - *Giải pháp*: Modal lưu luôn hiển thị rõ Môn học - Lớp - Năm học và phân tách rõ ràng 2 nút "Lưu thành bản mới" và "Cập nhật bản hiện tại".

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh: `node tests/xaydungphuluc-smoke.js`
   - Chạy lệnh: `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html`:
     * Chọn Môn: Toán học, Lớp: 6, Năm học: 2026-2027 $\to$ Bấm "Lưu lên CSDL" $\to$ Modal mở ra hiển thị đúng "Toán học - Lớp 6 (2026-2027)", nhập tên "Kế hoạch Toán 6 HK1" $\to$ Lưu thành công.
     * Đổi sang Môn: Tin học, Lớp: 7, Năm học: 2026-2027 $\to$ Bấm "Lưu lên CSDL" $\to$ Lưu thành bản mới "Kế hoạch Tin học 7".
     * Bấm "Tải từ CSDL" $\to$ Modal hiển thị danh sách cả 2 bản lưu với đầy đủ thông tin Môn, Lớp, Năm học, ngày giờ tạo.
     * Bấm lọc theo môn "Toán học" $\to$ Chỉ hiện bản lưu Toán 6.
     * Bấm "Mở" bản lưu Toán 6 $\to$ Giao diện nạp lại đầy đủ Môn Toán học, Lớp 6, các bài PPCT và tiết AI của Toán 6.
     * Thử bấm "Xóa" một bản lưu $\to$ Xác nhận xóa $\to$ Danh sách cập nhật và bản ghi được xóa khỏi CSDL.

## Tiêu chí nghiệm thu
- [ ] Bảng `user_phuluc_drafts` cho phép mỗi tài khoản lưu nhiều bản kế hoạch độc lập, có đầy đủ metadata Môn học, Lớp, Năm học, Tiêu đề, Tóm tắt.
- [ ] Bấm "Lưu lên CSDL" mở modal xác nhận đầy đủ Môn, Lớp, Năm học, cho phép đặt tên và chọn Lưu mới / Cập nhật.
- [ ] Bấm "Tải từ CSDL" mở modal danh sách các bản lưu có bộ lọc theo Môn, Lớp, Năm học, hiển thị ngày giờ, cho phép Mở và Xóa.
- [ ] Thanh trạng thái hiển thị rõ ràng bản kế hoạch đang làm việc và thời gian đồng bộ CSDL.
- [ ] 100% kiểm thử tự động `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` chạy đạt PASS.
