# PLAN: Tối ưu hóa hiển thị Lịch (Calendar) và Xây dựng trang xem Lịch báo giảng cá nhân chuẩn di động (Đúng biểu mẫu trực quan như ảnh chụp)

## Hiện trạng
1. **Lược bỏ Mistral AI**:
   - Thống nhất theo kết quả khảo sát: Không đưa Mistral vào nhận diện TKB vì `mistral-ocr-latest` không hỗ trợ phân tách cấu trúc bảng JSON theo khung tiết THCS, còn Pixtral không tối ưu bằng Gemini 2.5 Flash trên biểu mẫu tiếng Việt THCS. Hệ thống giữ nguyên Gemini 2.5 Flash làm engine nhận diện chính.

2. **Người dùng cung cấp ảnh mẫu mong muốn (Ảnh thực tế trong ứng dụng)**:
   - Biểu mẫu trực quan yêu cầu:
     * Khung ngày: Header nền xanh bo góc `Thứ Ba, ngày 29/09/2026`.
     * Tiêu đề các cột: `Tiết` | `Lớp` | `Môn` | `Bài dạy` | `PPCT`.
     * Phân tách rõ ràng:
       + Dải `Buổi sáng` (nền cam nhạt, chữ nâu cam).
       + Dải `Buổi chiều` (nền xanh nhạt, chữ xanh dương).
     * Từng dòng tiết học:
       + `Tiết 2` | Lớp `92` (xanh đậm) | Môn `Toán` (badge bo tròn) | Tên bài dạy đầy đủ (ví dụ: *Tuần 4 Bài tập cuối chương I...*) | `11 · 2/2` (xanh lá).
   - **Thực tế kỹ thuật của ứng dụng Calendar**:
     + Các ứng dụng Lịch (Apple Calendar, Google Calendar) **không thể vẽ bảng HTML biểu mẫu nhiều cột** (Tiết, Lớp, Môn, Bài dạy, PPCT) lên màn hình lưới lịch tháng/tuần. Chúng chỉ hiển thị các khối màu sự kiện đơn giản.
     + Do đó, nếu ép người dùng xem trên app Calendar, giao diện sẽ không bao giờ đẹp và trực quan được như biểu mẫu trên.
   - **Giải pháp toàn diện đáp ứng 100% mong muốn của giáo viên**:
     1. **Giải pháp 1 (Hoàn hảo nhất): Trang Web-App Lịch cá nhân trên iPhone**:
        - Cung cấp trang xem nhanh dành riêng cho giáo viên trên di động: Hiển thị **chính xác 100% giao diện bảng biểu y như ảnh thầy/cô vừa gửi**.
        - Hỗ trợ lưu ra Màn hình chính của iPhone (*Add to Home Screen*): Giáo viên chỉ cần bấm 1 lần, ngoài màn hình iPhone sẽ có biểu tượng ứng dụng riêng. Mỗi ngày chạm vào 1 cái là mở ngay biểu mẫu đẹp chuẩn chỉnh này mà không cần đăng nhập lại.
     2. **Giải pháp 2: Định dạng sự kiện Lịch (nếu dùng Calendar)**:
        - Gom sự kiện theo Buổi sáng / Buổi chiều.
        - Trong phần Chi tiết (Description) của sự kiện, trình bày danh sách từng tiết, lớp, môn, bài dạy, PPCT thẳng hàng, ngăn nắp mô phỏng biểu mẫu trên.

---

## Phạm vi
1. **Xây dựng trang xem Lịch báo giảng cá nhân chuẩn Mobile (`view-baogiang-mobile` hoặc `baogiang_me.html`)**:
   - Giao diện chuẩn 100% theo mẫu ảnh chụp:
     + Card ngày bo góc có header Thứ, Ngày.
     + Bảng 5 cột: Tiết, Lớp, Môn (badge), Bài dạy, PPCT.
     + Phân đoạn rõ nét Buổi sáng / Buổi chiều.
   - Hỗ trợ PWA / Add to Home Screen: Có icon ứng dụng, manifest, mở toàn màn hình không có thanh địa chỉ trên iPhone.
2. **Cập nhật mẫu Email gửi về iPhone**:
   - Giữ nguyên cấu trúc bảng đẹp y như ảnh chụp (đã có trong `buildTeacherBaoGiangWeekHtml`).
   - Thêm nút: **[📱 Mở xem Sổ Báo Giảng trên iPhone]** dẫn trực tiếp vào trang xem cá nhân.
   - Thêm nút: **[📅 Đồng bộ vào Lịch iPhone / Google Calendar]** cho ai thích dùng chuông báo trước 15 phút của Calendar.
3. **Cải tiến định dạng mô tả trong file Lịch (.ics / Webcal Feed)**:
   - Trình bày chi tiết từng tiết gọn gàng, liệt kê đầy đủ Tên bài và PPCT theo buổi sáng/chiều.

---

## Ngoài phạm vi
- Không can thiệp vào AI nhận diện TKB (giữ nguyên Gemini Flash).
- Không can thiệp sang các mô-đun Soạn KHBD, Đề thi, Sổ điểm.

---

## File dự kiến tác động
- `phancongtochuyenmon.html` (Cập nhật giao diện xem mobile cá nhân chuẩn biểu mẫu, cập nhật nút trong email và định dạng .ics).
- `api/calendar_feed.php` (Tạo mới: Cung cấp feed iCal cho ai cần đồng bộ báo thức/nhắc nhở).
- `tests/timetable-render-smoke.js` (Bổ sung kiểm thử).
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

---

## Các bước thực hiện chi tiết cho Coder
1. **Bước 1: Mở khóa handoff**:
   - Xóa `docs/handoff/.lock` trước khi sửa source code.

2. **Bước 2: Hoàn thiện giao diện xem Lịch báo giảng cá nhân trên di động**:
   - Đảm bảo thẻ ngày và bảng tiết học rendered đúng chuẩn CSS như trong ảnh:
     * Header ngày: background `#dbeafe`, color `#1e3a8a`, font-weight 700.
     * Dải Buổi sáng: background `#fff7ed`, color `#9a3412`.
     * Dải Buổi chiều: background `#eff6ff`, color `#1d4ed8`.
     * Cột Tiết, Lớp (bold `#1e3a8a`), Môn (badge xanh bo tròn `#e0f2fe`), Bài dạy, PPCT (`#047857` bold).
   - Thêm meta tags hỗ trợ iPhone Web App:
     ```html
     <meta name="apple-mobile-web-app-capable" content="yes">
     <meta name="apple-mobile-web-app-status-bar-style" content="default">
     <meta name="apple-mobile-web-app-title" content="Báo Giảng">
     ```

3. **Bước 3: Tối ưu nội dung Email gửi giáo viên**:
   - Đặt bảng biểu mẫu lên vị trí trang trọng nhất trong email (y như ảnh).
   - Thêm nút ghim ra màn hình chính iPhone và link xem trực tuyến.

4. **Bước 4: Định dạng mô tả sự kiện Lịch (.ics / Webcal)**:
   - Định dạng phần Description của từng buổi:
     ```
     BUỔI SÁNG:
     - Tiết 2: Toán 92 | Tuần 4 Bài tập cuối chương I (11 · 2/2)
     - Tiết 3: Toán 91 | Tuần 4 Bài tập cuối chương I (10 · 1/2)
     - Tiết 4: Toán 91 | Tuần 4 Bài tập cuối chương I (11 · 2/2)
     ```

5. **Bước 5: Kiểm thử và cập nhật nhật ký**:
   - Chạy `node tests/timetable-render-smoke.js`.
   - Ghi nhật ký vào `docs/handoff/IMPLEMENT.md`.
   - Tạo lại `docs/handoff/.lock` nội dung `LOCK`.

---

## Rủi ro
- Một số giáo viên không rành thao tác "Thêm vào Màn hình chính" trên iPhone. Cần hiển thị hướng dẫn ngắn kèm hình minh họa trực quan.

---

## Cách kiểm thử
1. **Kiểm thử tự động**: Chạy `node tests/timetable-render-smoke.js` -> 100% PASS.
2. **Kiểm thử thủ công**:
   - Mở giao diện trên Safari iPhone: Bảng hiển thị sắc nét, chuẩn 5 cột y hệt ảnh người dùng gửi.
   - Thao tác "Thêm vào màn hình chính": Biểu tượng hiển thị đẹp ngoài màn hình iPhone, bấm vào mở toàn màn hình.

---

## Tiêu chí nghiệm thu
- Giao diện trên iPhone hiển thị chính xác theo biểu mẫu trong ảnh: Header xanh, phân cách Buổi sáng/Buổi chiều, đầy đủ 5 cột (Tiết, Lớp, Môn, Bài dạy, PPCT).
- Có thể lưu thành ứng dụng ngoài Màn hình chính của iPhone xem hàng ngày bằng 1 chạm.
