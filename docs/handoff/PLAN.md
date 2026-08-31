# PLAN: Khớp 100% Biểu Mẫu PPCT Chuẩn (Bài học, Số tiết, Tiết CT, Tuần, Thiết bị, Địa điểm, chỉ thêm Cột NLS & AI) và Sửa Triệt Để Lỗi Thanh Tiến Trình 100% Không Tự Ẩn

## Hiện trạng
1. **Khớp Chuẩn Biểu Mẫu PPCT Thực Tế của Người Dùng**:
   - Biểu mẫu kế hoạch dạy học thực tế của giáo viên gồm 6 cột gốc:
     + Cột 1: **Bài học** (chứa các dòng phân cấp gộp ô: `HỌC KÌ I`, `1. SỐ HỌC 6`, `CHƯƠNG I. TẬP HỢP SỐ TỰ NHIÊN (13 tiết)`, `HỌC KÌ II`,...)
     + Cột 2: **Số tiết**
     + Cột 3: **Tiết CT** (Tiết phân phối chương trình: 1, 2, 3, 4, 5, 6,...)
     + Cột 4: **Tuần** (1, 2, 3,..., 35)
     + Cột 5: **Thiết bị dạy học (*)**
     + Cột 6: **Địa điểm dạy học (**)**
   - **Cam kết hợp đồng & yêu cầu cốt lõi**: Giữ nguyên 100% cấu trúc biểu mẫu của người dùng, giữ nguyên các dòng tiêu đề chương và phân phối tiết CT; **chỉ bổ sung thêm 01 cột duy nhất ở cuối bảng**:
     + Cột 7: **Mã NLS & AI (CV 3456 & QĐ 2422)**.
2. **Lỗi Thanh Tiến Trình 100% Không Dừng / Không Ẩn (như ảnh chụp thực tế)**:
   - Khi chạy xong 100%, hàm `setProgress(100, 'Đã hoàn tất. Có thể xem trước và xuất Word.')` trong [xaydungphuluc.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/xaydungphuluc.html) chỉ gán text thông báo nhưng:
     + Thẻ spinner `<span class="spinner"></span>` vẫn xoay liên tục tạo cảm giác hệ thống chưa xong.
     + Thanh tiến trình không có cơ chế tự động ẩn (`setTimeout hide`) và không có nút đóng `✕`, dẫn đến thanh progress bar nổi cố định ở đáy màn hình che khuất bảng xem trước và các dòng dữ liệu của người dùng.

## Phạm vi
1. **Sửa Triệt Để Lỗi Thanh Tiến Trình (% Floating Bar)**:
   - **Dừng Spinner khi Đạt 100%**: Khi hoàn tất (`percent >= 100`), thay thế spinner xoay bằng biểu tượng tích xanh `✓` hoặc `✦` ("Đã hoàn tất").
   - **Tự động Ẩn Mượt Mà**: Sau 1.5 giây kể từ khi đạt 100%, tự động kích hoạt hiệu ứng fade-out và ẩn thanh tiến trình (`container.classList.add('hidden')`).
   - **Bổ sung Nút Đóng `✕` Thủ công**: Thêm nút `✕` trên thanh tiến trình để người dùng có thể chủ động tắt ngay bất cứ lúc nào.
   - **Xử lý khi Hủy / Lỗi**: Khi người dùng bấm Hủy tác vụ hoặc gặp lỗi, hiển thị thông báo lỗi ngắn và tự ẩn sau 2 giây.
2. **Khớp Tuyệt Đối Biểu Mẫu PPCT 7 Cột Chuẩn**:
   - Cấu trúc 7 cột chuẩn trên Web Preview và file xuất Word `.docx`:
     1. `Bài học`
     2. `Số tiết`
     3. `Tiết CT`
     4. `Tuần`
     5. `Thiết bị dạy học (*)`
     6. `Địa điểm dạy học (**)`
     7. `Mã NLS & AI (CV 3456 & QĐ 2422)` (Cột bổ sung duy nhất)
   - Giữ nguyên các dòng tiêu đề phân cấp gộp cột (`HỌC KÌ I`, `1. SỐ HỌC 6`, `CHƯƠNG I. ...`, `HỌC KÌ II`...).
   - AI chỉ điền nội dung vào cột số 7 (`Mã NLS & AI`) theo tỷ lệ NLS (%), tỷ lệ AI (%) và dải mật độ mã (`1-2`, `2-3`, `3-4 mã/bài`) đã cấu hình.
3. **Đầy đủ Ghi chú & Bảng Chữ ký Phê duyệt**:
   - Chú thích chân bảng:
     + `(*) Tên thiết bị/học liệu số theo Thông tư 38/2021/TT-BGDĐT`
     + `(**) Lớp học/Phòng học bộ môn theo Thông tư 14/2020/TT-BGDĐT`
   - Bảng chữ ký 2 bên chuẩn hành chính (Giáo viên / Tổ trưởng phê duyệt cho Phụ lục 3; Tổ trưởng / Hiệu trưởng cho Phụ lục 1, 2).
4. **Nâng cấp Bộ Kiểm thử Tự động ([tests/xaydungphuluc-smoke.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/tests/xaydungphuluc-smoke.js))**:
   - Kiểm tra các tiêu đề cột `Tiết CT`, `Thiết bị dạy học (*)`, `Địa điểm dạy học (**)`.
   - Kiểm tra cơ chế tự ẩn của progress bar (`hideProgress` / `setTimeout` / nút đóng `✕`).

## Ngoài phạm vi
- Không can thiệp các file ngoài `xaydungphuluc.html` và file test liên quan.

## File dự kiến tác động
- `xaydungphuluc.html` [SỬA PROGRESS BAR TỰ ẨN KHI 100%, DỪNG SPINNER, THÊM NÚT ĐÓNG ✕, KHỚP CHUẨN BIỂU MẪU PPCT 7 CỘT]
- `tests/xaydungphuluc-smoke.js` [CẬP NHẬT SMOKE TEST]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Sửa Hàm Điều Khiển Tiến Trình `setProgress` & `hideProgress` trong `xaydungphuluc.html`**:
   - Thêm nút đóng `✕` (`<button class="text-xs opacity-75 hover:opacity-100 ml-2" onclick="hideProgress()">✕</button>`) vào thanh `#progressContainer`.
   - Nâng cấp `setProgress(percent, message, visible)`:
     + Nếu `percent >= 100`: Hiển thị icon `✓ Đã hoàn tất`, dừng spinner và đặt `setTimeout(() => hideProgress(), 1500)`.
     + Nếu `percent < 100` và `visible`: Hiển thị spinner xoay và xóa timer ẩn trước đó (nếu có).
2. **Bước 2: Chuẩn Hóa 7 Cột Biểu Mẫu PPCT**:
   - Định nghĩa danh sách cột chuẩn:
     `[['lesson','Bài học'],['periods','Số tiết'],['periodOrder','Tiết CT'],['week','Tuần'],['devices','Thiết bị dạy học (*)'],['location','Địa điểm dạy học (**)'],['integration','Mã NLS & AI (CV 3456 & QĐ 2422)']]`.
   - Parser nhận diện và bảo toàn `periodOrder` (Tiết CT), `week` (Tuần), `devices`, `location` từ file tải lên.
   - Siêu Prompt Gemini chỉ điền duy nhất vào cột `integration`.
3. **Bước 3: Nâng Cấp Bảng Xem Trước Inline và Hàm Xuất Word `exportDocx`**:
   - Render bảng xem trước và xuất Word `.docx` chuẩn 7 cột theo đúng bố cục trong ảnh của người dùng.
   - Thêm chú thích `(*)` và `(**)` dưới bảng và chữ ký phê duyệt 2 bên.
4. **Bước 4: Cập nhật và chạy kiểm thử tự động**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`, xác nhận PASS 100%.

## Rủi ro
- **Rủi ro**: Timer tự ẩn thanh progress bar bị đè khi người dùng bấm sinh liên tiếp nhiều lần.
  - *Giải pháp*: Lưu `progressTimerId` vào biến toàn cục và `clearTimeout(progressTimerId)` mỗi khi bắt đầu tiến trình mới hoặc khi người dùng hủy tác vụ.

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`:
     + Xác nhận hàm `setProgress` có cơ chế dừng spinner và tự ẩn sau 1.5s khi 100%.
     + Xác nhận thanh progress bar có nút đóng `✕`.
     + Xác nhận bảng PPCT có đầy đủ các cột: `Bài học`, `Số tiết`, `Tiết CT`, `Tuần`, `Thiết bị dạy học (*)`, `Địa điểm dạy học (**)`, `Mã NLS & AI`.
2. **Kiểm thử thủ công trên trình duyệt**:
   - Mở `xaydungphuluc.html` trên trình duyệt.
   - Bấm nút **⚡ Sinh trọn bộ Phụ lục**:
     + Thanh tiến trình nổi lên với spinner xoay và % tăng dần.
     + Khi đạt 100%: Spinner dừng, icon chuyển sang `✓`, hiển thị thông báo hoàn tất và **tự động ẩn mượt mà sau 1.5 giây** (không còn bị treo che khuất bảng như trong ảnh).
     + Người dùng cũng có thể bấm nút `✕` để đóng thanh tiến trình ngay lập tức.
   - Kiểm tra bảng xem trước và xuất file Word: Khớp 100% biểu mẫu chuẩn 7 cột gồm `Tiết CT`, `Tuần`, `Thiết bị`, `Địa điểm` và `Mã NLS & AI`.

## Tiêu chí nghiệm thu
1. Khi chạy sinh AI đạt 100%, thanh tiến trình dừng spinner, hiển thị tích xanh `✓` và tự động ẩn mượt mà sau 1.5 giây; có nút đóng `✕` để tắt chủ động.
2. Cấu trúc bảng PPCT và file Word xuất ra khớp 100% biểu mẫu người dùng cung cấp (gồm đúng các cột: `Bài học`, `Số tiết`, `Tiết CT`, `Tuần`, `Thiết bị dạy học (*)`, `Địa điểm dạy học (**)`, và chỉ bổ sung cột `Mã NLS & AI (CV 3456 & QĐ 2422)`).
3. Toàn bộ smoke test tự động đều PASS 100%.
