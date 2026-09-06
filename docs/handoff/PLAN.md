# PLAN: Tách Thời Khóa Biểu Thành Tab Riêng & Tối Ưu Quy Trình Nhận Diện TKB Hàng Loạt (Lưu Local Liên Tục, Lưu CSDL 1 Lần)

## Hiện trạng
1. **Thời khóa biểu hiện tại đang là Modal popup (`#teacher-timetable-modal`)**:
   - Hiện tại, tính năng TKB của giáo viên mở dưới dạng modal popup khi bấm nút "Thời khoá biểu" trên từng card giáo viên hoặc trong tab Sổ Dạy Thay.
   - Khi làm việc với nhiều giáo viên trong tổ (10 - 20 GV): người dùng phải mở modal cho GV 1, dán ảnh, nhận diện AI, lưu (modal tự đóng), rồi lại tìm thẻ GV 2, mở modal... Quy trình bị ngắt quãng, chật chội và tốn rất nhiều thao tác đóng/mở.
2. **Nhu cầu quy trình nhận diện TKB hàng loạt liên tục**:
   - Người dùng có ảnh chụp TKB của cả tổ (hoặc nhận diện lần lượt từng giáo viên).
   - Nhu cầu thực tế: Chọn GV 1 $\rightarrow$ Dán ảnh $\rightarrow$ AI nhận diện $\rightarrow$ **Tự động lưu ngay vào máy (Local)** $\rightarrow$ Chuyển sang GV 2 tiếp tục $\rightarrow$ Cứ thế làm hết toàn bộ giáo viên trong tổ $\rightarrow$ Nhấn **"Lưu CSDL" 1 lần duy nhất** để đẩy toàn bộ dữ liệu tổ lên server MySQL.
   - Cần một không gian làm việc toàn trang rộng rãi, chuyên nghiệp với danh sách giáo viên bên trái (hiển thị rõ ai đã có TKB, ai chưa có) và lưới TKB bên phải để thao tác nhanh, trực quan.

---

## Phạm vi
1. **Tách tính năng Thời khóa biểu thành Tab riêng trong thanh Workspace Navigation (`#tab-nav-timetable`, `#view-timetable`)**:
   - Thêm Tab mới trên thanh 5 tab hiện tại:
     + `1. Phân công giảng dạy` (`#view-phancong`)
     + `2. Thời khoá biểu GV` (`#view-timetable`)
     + `3. Sổ Dạy Thay - Bù` (`#view-daythay`)
     + `4. Chấm công GV` (`#view-chamcong`)
     + `5. Tăng Giờ` (`#view-tanggio`)
     + `6. Báo cáo & Thống kê` (`#view-baocao`)
   - Cập nhật hàm `switchAppView()` hỗ trợ view `view-timetable` và gọi `renderTimetableView()`.
   - Giữ hàm `openTeacherTimetableModal(teacherId)` như một alias chuyển sang `switchAppView('view-timetable')` và focus chọn đúng giáo viên đó để tương thích 100% với các nút gọi hiện có trên Thẻ GV và Sổ Dạy Thay.

2. **Xây dựng Màn hình Không gian làm việc Thời khóa biểu Toàn trang 2 cột (`#view-timetable`)**:
   - **Cột Trái (Danh sách Giáo viên & Trạng thái TKB)**:
     + Ô tìm kiếm nhanh giáo viên (`#tt-teacher-search`).
     + Bộ lọc: `Tất cả` | `Đã có TKB` | `Chưa có TKB`.
     + Thống kê tiến độ trực quan: `Đã có TKB: X / Y giáo viên`.
     + Danh sách thẻ giáo viên: Mỗi dòng gồm Avatar/Icon, Tên giáo viên, vai trò (GV, TTCM...), badge trạng thái:
       * `✓ Đã có TKB (X tiết)` (màu xanh lá)
       * `⏳ Chưa có TKB` (màu cam/xám)
       * `● Chưa lưu CSDL` (chấm xanh dương nổi bật nếu có thay đổi local chưa đồng bộ lên CSDL).
     + Bấm vào giáo viên nào thì vùng làm việc bên phải lập tức chuyển sang giáo viên đó.
   - **Cột Phải (Không gian làm việc TKB của giáo viên đang chọn)**:
     + Header thông tin: Tên giáo viên (lớn), vai trò, nút chuyển nhanh `< GV trước` và `GV tiếp theo >`.
     + Bộ chọn Năm học (`#tt-school-year`), Học kỳ (`#tt-semester`).
     + Vùng dán ảnh thông minh (`#tt-dropzone`):
       * Lắng nghe Ctrl+V dán ảnh chụp màn hình, kéo thả ảnh hoặc chọn file ảnh.
       * Preview ảnh thu nhỏ gọn gàng, có nút xóa ảnh.
       * Nút **`✨ AI Nhận diện TKB`** với spinner loading mượt mà.
     + Lưới ma trận Thời khóa biểu tuần (Buổi Sáng + Buổi Chiều $\times$ Thứ 2 - Thứ 7):
       * Cho phép click chỉnh sửa nhanh từng ô Môn - Lớp.
     + Thanh công cụ tác vụ:
       * Nút **`Lưu tất cả lên CSDL`** (nổi bật, gọi `saveToDB()`).
       * Nút **`⚡ Dịch sang Phân công`** (`applyCurrentTimetableToAssignments()`).
       * Nút **`GV tiếp theo ➔`** (chuyển sang GV chưa có TKB tiếp theo để làm liên tục).
       * Nút **`🗑️ Xóa TKB GV này`** (xóa trắng TKB của GV hiện tại nếu muốn làm lại).

3. **Cơ chế Tự động Lưu Local khi AI nhận diện & Chuyển tiếp liên tục**:
   - Khi AI Gemini Vision nhận diện xong (hoặc khi người dùng sửa ô TKB):
     + Dữ liệu TKB của giáo viên được cập nhật ngay vào `teacher.timetable`.
     + Tự động gọi `persistTeacherTimetable(teacherId, next)`.
     + Tự động gọi `saveToLocal({ autoSave: false })` để lưu ngay vào `localStorage`.
     + Đánh dấu cờ `hasUnsavedChanges = true`.
     + Badge trạng thái của giáo viên bên cột trái tự động đổi sang `✓ Đã có TKB`.
     + Hiển thị Toast thông báo: *"Đã lưu TKB của [Tên GV] vào máy! Bạn có thể chọn giáo viên tiếp theo."*.
     + Tự động kích hoạt gợi ý chuyển sang giáo viên kế tiếp mà không làm ngắt quãng mạch làm việc của người dùng.

4. **Lưu toàn bộ dữ liệu lên CSDL 1 lần duy nhất**:
   - Khi hoàn thành tất cả giáo viên trong tổ (hoặc bất kỳ lúc nào), người dùng bấm nút **"Lưu tất cả lên CSDL"** trên Tab TKB (hoặc nút "Lưu CSDL" ở Top Header):
     + Gọi `saveToDB()` $\rightarrow$ Đẩy toàn bộ `state` (bao gồm TKB của tất cả giáo viên và phân công các đợt) lên server MySQL qua `api/phancong.php?action=save`.
     + Server phản hồi thành công $\rightarrow$ Cập nhật trạng thái `Đã lưu CSDL`, xóa cờ `hasUnsavedChanges`.

---

## Ngoài phạm vi
- Không thay đổi cấu trúc dữ liệu JSON lưu trong MySQL (`state.teachers[].timetable`).
- Không sửa backend PHP (`api/phancong.php` và `api/khbd_gemini.php` đã hỗ trợ đầy đủ payload).
- Không làm thay đổi logic phân công hoặc chấm công hiện có.

---

## File dự kiến tác động
- `phancongtochuyenmon.html` [SỬA: Thêm tab và view `#view-timetable`, render layout 2 cột, danh sách GV kèm trạng thái TKB, tự động lưu local khi AI nhận diện, nút lưu CSDL toàn tổ]
- `docs/handoff/PLAN.md` [GHI ĐÈ: Kế hoạch này]
- `docs/handoff/.lock` [TẠO: LOCK]

---

## Các bước thực hiện

### Bước 1: Khai báo Tab Navigation & Tạo Khung HTML View TKB
1. Trong `#top-navbar .view-switcher`:
   - Thêm nút tab:
     ```html
     <button class="view-tab-btn" id="tab-nav-timetable" onclick="switchAppView('view-timetable')">
         <i class="fas fa-calendar-days"></i> 2. Thời khoá biểu GV
     </button>
     ```
   - Điều chỉnh lại số thứ tự các tab tiếp theo:
     + 3. Sổ Dạy Thay - Bù (`tab-nav-daythay`)
     + 4. Chấm công GV (`tab-nav-chamcong`)
     + 5. Tăng Giờ (`tab-nav-tanggio`)
     + 6. Báo cáo & Thống kê (`tab-nav-baocao`)
2. Thêm container `#view-timetable` trong thân trang:
   - Layout gồm 2 phần:
     + `#tt-left-panel`: Cột danh sách giáo viên, thanh tìm kiếm, bộ lọc trạng thái và thống kê tiến độ.
     + `#tt-right-panel`: Vùng làm việc TKB giáo viên đang chọn, vùng dán ảnh AI, ma trận tuần và thanh công cụ lưu.
3. Cập nhật CSS cho `#view-timetable`:
   - Phân chia 2 cột rõ ràng, responsive mượt mà trên các độ phân giải màn hình.

### Bước 2: Xây dựng Logic Cột Trái (Danh sách Giáo viên & Trạng thái)
1. Viết hàm `renderTimetableTeacherList()`:
   - Đọc danh sách `state.teachers`.
   - Lọc theo từ khóa tìm kiếm (`#tt-teacher-search`) và bộ lọc trạng thái (`filter: all | has_tt | missing_tt`).
   - Đếm số GV đã có TKB (`timetableHasLessons(t.timetable)`) / Tổng số GV và hiển thị badge tiến độ.
   - Vẽ danh sách các item giáo viên:
     + Highlight GV đang được chọn (`selectedTimetableTeacherId`).
     + Hiển thị badge: `✓ Đã có TKB` hoặc `⏳ Chưa có TKB`.
     + Khi click vào một item: gọi `selectTimetableTeacher(teacherId)`.
2. Hàm `selectTimetableTeacher(teacherId)`:
   - Cập nhật `selectedTimetableTeacherId = teacherId`.
   - Cập nhật lại class active ở danh sách bên trái.
   - Nạp TKB của GV vào `editingTimetable = JSON.parse(JSON.stringify(teacher.timetable || emptyTimetable()))`.
   - Gọi `renderTimetableWorkspace()` để hiển thị thông tin và lưới TKB bên phải.

### Bước 3: Xây dựng Không gian Làm việc TKB Cột Phải
1. Viết hàm `renderTimetableWorkspace()`:
   - Hiển thị tên giáo viên, vai trò, số tiết hiện tại.
   - Nạp giá trị năm học (`#tt-school-year`), học kỳ (`#tt-semester`).
   - Render lưới ma trận Buổi sáng (`#tt-morning-wrap`) và Buổi chiều (`#tt-afternoon-wrap`).
   - Đặt lại vùng dán ảnh preview (nếu có ảnh trước đó).
2. Xử lý nút điều hướng nhanh:
   - `goToPrevTimetableTeacher()`: Chọn giáo viên liền trước trong danh sách.
   - `goToNextTimetableTeacher(onlyMissing = false)`: Chọn giáo viên liền sau; nếu `onlyMissing = true` thì nhảy thẳng đến giáo viên tiếp theo chưa có TKB.

### Bước 4: Tích hợp Tự động Lưu Local & Chuyển Tiếp Sau Khi AI Nhận Diện
1. Cập nhật `applyAiTimetableResult(raw)`:
   - Đọc JSON từ Gemini Vision, cập nhật vào `editingTimetable`.
   - Tự động gọi `persistTeacherTimetable(selectedTimetableTeacherId, editingTimetable)`.
   - Tự động gọi `saveCurrentPhaseSnapshot()`.
   - Tự động gọi `saveToLocal({ autoSave: false })` để ghi ngay vào `localStorage`.
   - Đánh dấu `hasUnsavedChanges = true`.
   - Cập nhật lại danh sách bên trái (`renderTimetableTeacherList()`) để badge GV đó ngay lập tức chuyển sang màu xanh lá `✓ Đã có TKB`.
   - Hiển thị Toast thông báo: *"Đã nhận diện và lưu TKB của GV [Tên GV] vào máy! Bạn có thể chọn GV tiếp theo để tiếp tục."*.
   - Hiển thị nút bấm nhanh: `GV tiếp theo ➔` để người dùng tiếp tục thao tác mà không cần tìm kiếm.
2. Xử lý sửa ô trực tiếp trên lưới:
   - Khi người dùng sửa nội dung ô TKB trên lưới: tự động cập nhật vào `editingTimetable`, tự động lưu local sau 500ms debounce hoặc khi blur.

### Bước 5: Nút Lưu Toàn Bộ CSDL & Tích Hợp Menu
1. Trên thanh công cụ của View TKB:
   - Đặt nút nổi bật:
     `<button class="btn-toolbar btn-db-save" onclick="saveToDB()"><i class="fas fa-cloud-arrow-up"></i> Lưu tất cả lên CSDL</button>`
   - Nút gọi trực tiếp `saveToDB()`, gửi toàn bộ `state` lên MySQL và hiển thị thông báo thành công.
2. Nút "Dịch sang Phân công" trên View TKB:
   - Bấm nút gọi `applyTimetableToAssignments(selectedTimetableTeacherId)` để nạp phân công lớp ngay cho giáo viên đang chọn.
3. Giữ hàm tương thích:
   - `openTeacherTimetableModal(teacherId)`: nếu được gọi từ bất kỳ đâu (như Thẻ GV ở View 1 hay Sổ Dạy Thay ở View 3), hàm sẽ gọi `switchAppView('view-timetable')` và `selectTimetableTeacher(teacherId)`. Đảm bảo các nút bấm cũ hoạt động trơn tru.

---

## Rủi ro
1. **Lắng nghe sự kiện Paste (Ctrl+V)**: Khi chuyển từ modal sang Tab view toàn trang, sự kiện `paste` cần gắn đúng vùng dropzone hoặc chỉ kích hoạt khi tab TKB đang `active` để tránh bắt nhầm khi người dùng đang ở các tab khác.
   - *Biện pháp*: Kiểm tra `document.getElementById('view-timetable')?.classList.contains('active')` trước khi xử lý dán ảnh.
2. **Trùng lặp ID phần tử**: Một số ID trong modal cũ (`#tt-dropzone`, `#tt-morning-wrap`...) nếu tái sử dụng trong view mới cần đảm bảo không bị nhân bản thành 2 ID trùng lặp trong DOM.
   - *Biện pháp*: Chuyển toàn bộ các phần tử từ modal sang view mới hoặc thay thế modal bằng view mới, chạy test kiểm tra 100% ID duy nhất.

---

## Cách kiểm thử
1. **Kiểm tra Thanh Tab Navigation**:
   - Mở trang: Quan sát thấy Tab `2. Thời khoá biểu GV` trên thanh tab.
   - Bấm vào Tab: Chuyển sang `#view-timetable`, hiển thị đầy đủ bố cục 2 cột (Danh sách GV bên trái, Không gian TKB bên phải).
2. **Kiểm tra Danh sách Giáo viên & Trạng thái TKB**:
   - Cột trái hiển thị đầy đủ danh sách giáo viên của tổ.
   - Giáo viên đã có TKB có badge xanh `✓ Đã có TKB`; giáo viên chưa có hiển thị `⏳ Chưa có TKB`.
   - Tìm kiếm tên giáo viên lọc chính xác danh sách.
   - Bấm vào Thầy Danh: Panel bên phải tải đúng TKB của Thầy Danh.
3. **Kiểm tra Quy trình AI Nhận diện & Tự Động Lưu Local**:
   - Chọn một giáo viên chưa có TKB (VD: Cô Ánh).
   - Dán ảnh TKB (Ctrl+V) $\rightarrow$ Preview ảnh xuất hiện.
   - Bấm `AI nhận diện TKB` $\rightarrow$ AI đọc và render lưới TKB.
   - Kiểm tra `localStorage`: TKB của Cô Ánh đã được lưu ngay vào máy mà không cần bấm thêm nút nào!
   - Badge của Cô Ánh bên cột trái lập tức chuyển thành `✓ Đã có TKB`.
   - Bấm nút `GV tiếp theo ➔`: Hệ thống tự động chuyển sang giáo viên kế tiếp chưa có TKB.
4. **Kiểm tra Lưu CSDL 1 lần duy nhất**:
   - Sau khi làm xong các giáo viên, bấm nút **"Lưu tất cả lên CSDL"** trên tab TKB.
   - Kiểm tra request gửi đến `api/phancong.php?action=save`: Toàn bộ TKB của các giáo viên được gửi lên và server phản hồi thành công.
   - Nạp lại trang (F5): Dữ liệu TKB của toàn bộ giáo viên được giữ nguyên vẹn từ CSDL.
5. **Kiểm tra Tương thích Nút bấm từ View khác**:
   - Sang Tab 1 (Phân công): Bấm nút "Thời khoá biểu" trên thẻ của Thầy Danh $\rightarrow$ Tự động nhảy sang Tab TKB và focus đúng Thầy Danh.

---

## Tiêu chí nghiệm thu
1. Thời khóa biểu được tách thành một Tab riêng biệt trong thanh làm việc của Quản lý tổ chuyên môn (`view-timetable`).
2. Giao diện toàn trang 2 cột chuyên nghiệp: Cột trái liệt kê giáo viên kèm trạng thái TKB trực quan, cột phải là bảng làm việc TKB chi tiết.
3. Nhận diện ảnh TKB tự động lưu ngay vào máy (`localStorage`), cho phép người dùng chuyển liên tục qua các giáo viên khác mà không bị đóng/mở ngắt quãng.
4. Cung cấp nút Lưu CSDL rõ ràng để người dùng nhấn lưu 1 lần sau khi đã hoàn tất toàn bộ giáo viên trong tổ.
5. Các nút xem TKB từ Thẻ GV và Sổ Dạy Thay tự động điều hướng mượt mà sang Tab Thời khóa biểu.