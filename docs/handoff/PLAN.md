# PLAN: Nạp Phân Công TKB Toàn Tổ & Tạo Ảnh Thông Báo Dạy Thay Thông Minh Bằng AI

## Hiện trạng & Nhu cầu
1. **Phân công từ Thời khóa biểu (TKB)**:
   - Đã nhận diện TKB cho cả tổ (11/11 giáo viên), nhưng các lớp chưa tự động phiên sang phân công giảng dạy (`state.teachers[].assignments`).
   - Người dùng phải bấm thủ công trên từng giáo viên ("phải nạp thụ động từng người"), thiếu nút nổi bật để nạp một lượt cho toàn bộ giáo viên trong tổ.
2. **Thông báo Sổ Dạy Thay - Bù**:
   - Sau khi ghi nhận các lượt dạy thay / dạy bù trong tổ (GV nghỉ phép, đi công tác, GV khác dạy thay tiết nào, lớp nào), Tổ trưởng cần gửi thông báo đến các giáo viên liên quan hoặc gửi vào nhóm Zalo trường/tổ.
   - Hiện tại chỉ có xuất Excel hoặc xem bảng trên web, chưa có tính năng **tạo ảnh thông báo đẹp mắt chuẩn sư phạm** và **chưa có AI hỗ trợ soạn thông báo Zalo / dặn dò** để gửi nhanh cho giáo viên.

---

## Phạm vi thực hiện

### PHẦN 1: Nạp Phân Công Từ TKB Toàn Tổ & Tự Động Phiên Lớp Sau Nhận Diện
1. **Bổ sung Nút Nổi Bật Nạp Phân Công Toàn Tổ (1-Click Sync)**:
   - **Tab 1 (`#view-phancong`)**: Thêm nút `⚡ Nạp phân công từ TKB toàn tổ` (`btn-small-primary`) ngay trên thanh thống kê tiến độ `.live-stats-banner` (cạnh nút "Xem Ma trận Đợt này").
   - **Tab 2 (`#view-timetable`)**:
     + Thêm nút `⚡ Dịch TKB toàn tổ sang Phân công` (`btn-small-primary`) trên thanh công cụ tác vụ (`#tt-right-panel`, cạnh nút "Lưu tất cả lên CSDL").
     + Đổi nhãn nút đơn lẻ thành `Dịch GV này sang Phân công`.
     + Cột trái (`#tt-left-panel`): thêm nút nhanh `⚡ Nạp phân công toàn tổ` ngay dưới dòng tiến độ `Đã có TKB: X / Y giáo viên`.
2. **Tự Động Phiên Lớp Khi AI Nhận Diện Xong**:
   - Đặt checkbox `#tt-auto-apply-assign` ("Tự động cập nhật phân công khi lưu TKB") thành mặc định **`checked`** trong HTML.
   - Trong `applyAiTimetableResult(raw)`: nếu `#tt-auto-apply-assign` được tích, tự động gọi ngay `applyTimetableToAssignments(selectedTimetableTeacherId, { silent: true, skipRender: true })`.
   - Thông báo Toast hiển thị rõ: *"Đã nhận diện, lưu TKB và tự động phiên X lớp sang phân công cho GV [Tên GV]!"*.
3. **Nâng Cấp Hàm `syncAllAssignmentsFromTimetables()`**:
   - Xác nhận thân thiện: *"Bạn có muốn nạp phân công từ Thời khoá biểu của X giáo viên vào [Tên đợt] không?"*.
   - Đếm tổng số giáo viên và tổng số lượt lớp được gán; dọn sạch kho lớp chưa gán (`state.unassigned`), bổ sung lớp mới vào `state.classes`.
   - Lưu snapshot đợt (`saveCurrentPhaseSnapshot()`) và lưu máy (`saveToLocal()`), gọi `render()`.
   - Toast kết quả: *"✅ Đã nạp phân công thành công cho X giáo viên (tổng cộng Y lượt lớp) từ Thời khoá biểu vào [Tên đợt]!"*.
4. **Cải Tiến Bóc Tách Ô & Khớp Môn**:
   - Hỗ trợ tách lớp khi ô TKB không có dấu gạch ngang (VD: `Toán 95`, `Toán 9A1`, `Toán/95`).
   - Bổ sung alias khớp môn trong `matchSubjectFromTimetableLabel`: `tin` -> `Tin học`, `toan` -> `Toán`, `hdtn` -> `HĐTN`, `shl` / `sinh hoạt lớp` -> `Chủ nhiệm` (nếu có lớp kèm theo).

---

### PHẦN 2: Tính Năng Tạo Ảnh Thông Báo Dạy Thay Thông Minh Bằng AI & Canvas
1. **Nút "Tạo ảnh thông báo (AI)" trên Sổ Dạy Thay (`view-daythay`)**:
   - Thêm nút **`✨ Tạo ảnh thông báo (AI)`** (`btn-small-primary`) trên thanh công cụ của Sổ Dạy Thay (cạnh nút "Xuất Excel Sổ Dạy Thay").
2. **Tích Hợp Thư Viện `html2canvas`**:
   - Thêm script `html2canvas` (`https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js`) vào `<head>` của `phancongtochuyenmon.html` (đồng bộ với `vehinh.html`).
3. **Modal "Thông báo Phân công Dạy thay" (`#substitute-announcement-modal`)**:
   - **Bộ điều khiển & Tuỳ biến**:
     + Chọn ngày cần thông báo (Date picker, mặc định là ngày có lượt dạy thay gần nhất hoặc ngày được chọn).
     + Tiêu đề thông báo (mặc định: `THÔNG BÁO PHÂN CÔNG DẠY THAY NGÀY DD/MM/YYYY`).
     + Ghi chú / Dặn dò của Tổ chuyên môn (cho phép nhập thủ công hoặc AI sinh tự động).
     + Nút **`✨ AI Soạn thông báo Zalo`**: Gửi danh sách các tiết dạy thay của ngày được chọn sang `api/khbd_gemini.php` (Gemini 2.5 Flash) để tự động soạn lời dặn dò trang trọng, lịch sự, chuẩn văn phong nhà trường và tóm tắt gửi Zalo.
   - **Khung Preview Card Thông Báo Thiết Kế Chuẩn Sư Phạm (`#dt-announcement-card`)**:
     + Thiết kế card đồ họa chuyên nghiệp, trang nhã:
       * Header: Tên đơn vị / Trường THCS (`state.info.school`), Tổ chuyên môn (`state.info.title`).
       * Tiêu đề chính nổi bật: `BẢNG PHÂN CÔNG DẠY THAY` kèm Ngày, Thứ.
       * Bảng phân công chi tiết, rõ ràng:
         | Buổi | Tiết | Lớp | Môn | Giáo viên vắng & Lý do | Giáo viên dạy thay | Ghi chú |
       * Footer: Lời dặn dò của tổ, ngày giờ lập thông báo, chữ ký đại diện Tổ trưởng chuyên môn (`TTCM`).
   - **Thanh Tác Vụ Xuất Bản (1-Click Export)**:
     + **`📋 Sao chép ảnh (Copy Image)`**: Dùng `html2canvas` kết hợp `navigator.clipboard.write([new ClipboardItem({'image/png': blob})])` để copy trực tiếp ảnh vào bộ nhớ tạm -> Người dùng chỉ cần ấn `Ctrl+V` vào Zalo/Messenger là gửi được ngay ảnh thông báo!
     + **`💾 Tải ảnh PNG (Download Image)`**: Xuất ảnh PNG độ nét cao (2x retina) lưu về máy tính.
     + **`📝 Sao chép tin nhắn Zalo (Copy Text)`**: Copy văn bản thông báo có emoji gọn gàng để dán kèm caption tin nhắn khi gửi ảnh trên Zalo.

---

## Ngoài phạm vi
- Không thay đổi cấu trúc dữ liệu JSON lưu trong CSDL (`state.attendance.substitutes`, `state.teachers[].assignments`, `state.teachers[].timetable`).
- Không sửa backend PHP (`api/phancong.php`, `api/khbd_gemini.php`). Proxy Gemini hiện tại đã hỗ trợ đầy đủ `generateContent`.
- Không ảnh hưởng đến dữ liệu chấm công, tăng giờ.

---

## File dự kiến tác động
- `phancongtochuyenmon.html` [SỬA:
  + Thêm thư viện `html2canvas` ở `<head>`.
  + Thêm nút nạp TKB toàn tổ ở Tab 1 và Tab 2; kích hoạt tự động phiên lớp sau khi AI nhận diện TKB.
  + Thêm nút `Tạo ảnh thông báo (AI)` trên toolbar Sổ Dạy Thay.
  + Thêm Modal `#substitute-announcement-modal` kèm Card thông báo `#dt-announcement-card`.
  + Viết các hàm JS: `openDayThayAnnouncementModal()`, `closeDayThayAnnouncementModal()`, `renderAnnouncementCard()`, `generateDayThayAnnouncementAI()`, `copyAnnouncementImage()`, `downloadAnnouncementImage()`, `copyAnnouncementZaloText()`.
]
- `docs/handoff/PLAN.md` [GHI ĐÈ: Kế hoạch này]
- `docs/handoff/.lock` [TẠO/GIỮ: LOCK]

---

## Các bước thực hiện chi tiết

### Bước 1: Nút Nạp Phân Công Toàn Tổ & Tự Động Phiên Lớp TKB (Phần 1)
1. **Tab 1 (`#view-phancong`)**:
   - Thêm nút `<button class="btn-small btn-small-primary" onclick="syncAllAssignmentsFromTimetables()"><i class="fas fa-bolt"></i> Nạp phân công từ TKB toàn tổ</button>` vào `.live-stats-banner`.
2. **Tab 2 (`#view-timetable`)**:
   - Thêm nút `<button type="button" class="btn-small btn-small-primary" onclick="syncAllAssignmentsFromTimetables()"><i class="fas fa-bolt"></i> Dịch TKB toàn tổ sang Phân công</button>` cạnh nút Lưu CSDL.
   - Thêm nút nhanh `⚡ Nạp phân công TKB toàn tổ` ở cột trái dưới `#tt-progress`.
   - Đặt checkbox `#tt-auto-apply-assign` mặc định `checked`.
3. **Trong `applyAiTimetableResult(raw)`**:
   - Sau khi lưu TKB giáo viên, nếu `#tt-auto-apply-assign` bật thì tự động gọi `applyTimetableToAssignments(selectedTimetableTeacherId, { silent: true, skipRender: true })`.
4. **Tối ưu `syncAllAssignmentsFromTimetables()`**:
   - Thêm xác nhận `confirm()`, đếm số GV và số lớp được phiên, dọn sạch kho lớp unassigned và render cập nhật Tab 1.

### Bước 2: Tích Hợp Thư Viện html2canvas & Giao Diện Nút Sổ Dạy Thay (Phần 2)
1. Trong `<head>` của `phancongtochuyenmon.html`:
   - Thêm `<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>`.
2. Trong thanh công cụ của Sổ Dạy Thay (`view-daythay`):
   - Thêm nút:
     ```html
     <button type="button" class="btn-small btn-small-primary" onclick="openDayThayAnnouncementModal()">
         <i class="fas fa-wand-magic-sparkles"></i> Tạo ảnh thông báo (AI)
     </button>
     ```

### Bước 3: Xây Dựng Modal & Card Thông Báo Dạy Thay Chuẩn Sư Phạm
1. Tạo modal `#substitute-announcement-modal` gồm:
   - Header modal: Tiêu đề "Tạo ảnh thông báo phân công dạy thay", nút đóng.
   - Cột trái: Bộ điều khiển (Chọn ngày dạy thay, Tiêu đề thông báo, Lời dặn dò, Nút "✨ AI Soạn thông báo Zalo").
   - Cột phải: Khung xem trước trực quan `#dt-announcement-card`:
     + Phong cách thiết kế: Giấy khen / Văn bản sư phạm hiện đại, nền gradient nhẹ hoặc viền bo trang trọng, logo biểu tượng giáo dục.
     + Tiêu đề trường & tổ chuyên môn.
     + Bảng liệt kê: Buổi, Tiết, Lớp, Môn, GV vắng (Lý do), GV dạy thay.
     + Lời dặn dò của TTCM.
     + Chữ ký / Đại diện Tổ chuyên môn.
   - Footer modal:
     + Nút `📋 Sao chép ảnh` (`copyAnnouncementImage()`).
     + Nút `💾 Tải ảnh PNG` (`downloadAnnouncementImage()`).
     + Nút `📝 Sao chép tin Zalo` (`copyAnnouncementZaloText()`).

### Bước 4: Viết Logic JS Cho Tính Năng Tạo Ảnh & AI Soạn Tin
1. Hàm `openDayThayAnnouncementModal(targetDate)`:
   - Mở modal, xác định ngày cần thông báo (ưu tiên ngày truyền vào hoặc ngày có lượt dạy thay gần nhất).
   - Nạp các bản ghi dạy thay của ngày đó từ `state.attendance.substitutes`.
   - Render preview card thông báo.
2. Hàm `generateDayThayAnnouncementAI()`:
   - Thu thập danh sách lượt dạy thay trong ngày (GV vắng, lý do, GV dạy thay, tiết, lớp).
   - Gửi prompt yêu cầu Gemini soạn lời dặn dò ngắn gọn, lịch sự, ân cần và chuyên nghiệp.
   - Điền kết quả vào ô "Lời dặn dò" và cập nhật trực tiếp lên card xem trước.
3. Hàm `copyAnnouncementImage()` & `downloadAnnouncementImage()`:
   - Gọi `html2canvas(document.getElementById('dt-announcement-card'), { scale: 2, useCORS: true })`.
   - `copyAnnouncementImage`: chuyển canvas thành blob `image/png`, ghi vào `navigator.clipboard.write([new ClipboardItem({'image/png': blob})])`, hiển thị Toast "Đã sao chép ảnh vào bộ nhớ tạm! Bạn có thể dán (Ctrl+V) ngay vào Zalo.".
   - `downloadAnnouncementImage`: tạo thẻ `<a>` tải file `Thong_Bao_Day_Thay_YYYYMMDD.png`.
4. Hàm `copyAnnouncementZaloText()`:
   - Định dạng văn bản tóm tắt có icon đẹp mắt, copy vào clipboard.

---

## Rủi ro & Biện pháp giảm thiểu
1. **Quyền ghi Clipboard Image**: Một số trình duyệt cũ hoặc trang không chạy qua HTTPS/localhost có thể chặn `navigator.clipboard.write([ClipboardItem])`.
   - *Biện pháp*: Bọc trong `try...catch`; nếu clipboard image không khả dụng, tự động fallback sang tải ảnh về máy (`downloadAnnouncementImage()`) kèm thông báo rõ ràng cho người dùng.
2. **Kích thước Card thông báo khi có nhiều tiết**: Nếu một ngày có nhiều lượt dạy thay, bảng có thể dài.
   - *Biện pháp*: Thiết kế card có padding hợp lý, font chữ co giãn linh hoạt (auto scale) và bảng table responsive để ảnh chụp luôn rõ ràng, sắc nét.

---

## Cách kiểm thử
1. **Kiểm tra Nạp TKB Toàn Tổ**:
   - Tab 1: Thấy nút `⚡ Nạp phân công từ TKB toàn tổ`. Bấm vào -> Xác nhận -> 11/11 GV được nạp đủ lớp từ TKB.
   - Tab 2: Thấy nút `⚡ Dịch TKB toàn tổ sang Phân công` và nút nhanh bên cột trái.
2. **Kiểm tra Tạo Ảnh Thông Báo Dạy Thay**:
   - Mở Tab 3 (Sổ Dạy Thay): Ghi nhận 1-2 lượt dạy thay cho ngày mai.
   - Bấm nút `✨ Tạo ảnh thông báo (AI)` -> Modal xuất hiện với bảng xem trước đẹp mắt chứa đúng các lượt dạy thay của ngày đó.
   - Bấm `✨ AI Soạn thông báo Zalo` -> AI Gemini trả về lời dặn dò phù hợp, tự động điền vào bảng và caption.
   - Bấm `📋 Sao chép ảnh` -> Dán Ctrl+V vào khung chat Zalo / Word kiểm tra ảnh nét, chuẩn định dạng.
   - Bấm `💾 Tải ảnh PNG` -> File ảnh được tải về máy thành công.
   - Bấm `📝 Sao chép tin Zalo` -> Văn bản tóm tắt được sao chép chuẩn emoji.

---

## Tiêu chí nghiệm thu
1. Có nút **`⚡ Nạp phân công từ TKB toàn tổ`** nổi bật ở Tab 1 và Tab 2, 1 click phân công cho tất cả giáo viên.
2. Khi AI nhận diện TKB của giáo viên mới, các lớp tự động được phiên ngay sang phân công.
3. Có nút **`✨ Tạo ảnh thông báo (AI)`** trên thanh công cụ của Sổ Dạy Thay.
4. Xuất được ảnh thông báo dạy thay thiết kế chuẩn sư phạm, sắc nét (PNG), cho phép copy trực tiếp vào clipboard để paste Zalo và tải về máy.
5. AI Gemini hỗ trợ soạn nội dung thông báo / lời dặn dò văn phong nhà trường và văn bản gửi Zalo tiện lợi.
