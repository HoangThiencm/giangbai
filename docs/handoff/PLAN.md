# PLAN: TỔNG HỢP NÂNG CẤP TOÀN DIỆN BÀI GIẢNG SƯ PHẠM, BẢNG VIẾT NHÁP, NHẢY NHANH TIẾT DẠY VÀ TINH GỌN THANH CÔNG CỤ

## Hiện trạng & Yêu cầu sư phạm cốt lõi
1. **Bố cục Cột Ghi bảng và Tên đề mục:**
   - Bảng chính (Cột trái) của giáo viên phải súc tích, ngắn gọn, đặt tiêu đề đề mục ngay đầu cột và **CỐ ĐỊNH công thức cốt lõi** trong suốt đề mục đó (chỉ đổi khi sang đề mục mới). Không đưa bài tập/ví dụ vào cột ghi bảng.
   - Cột phải (Hoạt động) chuyên trách diễn biến toàn bộ bài học (đề bài, hình vẽ, gợi ý, lời giải, trắc nghiệm).
2. **Nút loa 🔊 phải thông minh song ngữ:**
   - Nút loa 🔊 trên từng khối đang bị gán cứng `speakBlockEn` và tự ý lật giao diện sang tiếng Anh khi đang ở tiếng Việt.
   - Yêu cầu: Giao diện tiếng Việt bấm loa phải đọc tiếng Việt (ưu tiên audio MP3 Hoài My); giao diện tiếng Anh bấm loa đọc tiếng Anh. Tuyệt đối không tự ý đảo ngôn ngữ của người dùng.
3. **Lỗi lệch nét khi cuộn trang trong lúc vẽ bút:**
   - Canvas vẽ bị trôi khi cuộn chuột khiến nét vẽ không ăn khớp với nội dung bài học. Slide trình chiếu cần cô đọng vừa vặn khung 16:9 và khóa cuộn khi bật bút vẽ.
4. **Thanh công cụ quá tải & Thiếu Bảng viết nháp giảng dạy:**
   - Thanh điều khiển quá nhiều nút, nút `[💬 Tắt phụ đề]` gây vướng víu.
   - Giáo viên thiếu công cụ Bảng viết nháp (Blackboard / Whiteboard) để mở ra vẽ hình phụ hoặc giải thích chi tiết khi học sinh cần.
5. **Nhu cầu điều hướng theo phân phối chương trình khi dạy nhiều lớp:**
   - Một giáo viên dạy 3–4 lớp cùng khối với tốc độ tiếp thu khác nhau, việc tự động lưu tiến độ duy nhất trên máy sẽ gây nhảy nhầm bài giữa các lớp.
   - Cần cụm nút **Nhảy nhanh theo Tiết học (`[Tiết 1]`, `[Tiết 2]`, `[Tiết 3]`)** để giáo viên bước vào bất kỳ lớp nào cũng mở đúng bài học chỉ trong 1 giây.

## Phạm vi
1. **Chuẩn hóa Cột Ghi bảng và Cột Hoạt động:**
   - Đặt tiêu đề bài học và tên đề mục lớn (`1. HỆ THỨC GIỮA CẠNH HUYỀN VÀ CẠNH GÓC VUÔNG`) ở đầu Cột Ghi bảng bên trái (`data-step="0"`).
   - Nội dung ghi bảng súc tích: Chỉ ghi định nghĩa, định lí, công thức trọng tâm. Giữ nguyên không đổi xuyên suốt toàn bộ các slide thuộc mục đó.
   - Cột phải hiển thị toàn bộ hoạt động học tập.
2. **Nút âm thanh thông minh đa ngữ (`speakBlockAuto`) & Bộ audio Hoài My:**
   - Tạo hàm `speakBlockAuto(blockEl)`: ở giao diện tiếng Việt đọc tiếng Việt Hoài My (không đổi sang tiếng Anh), ở giao diện tiếng Anh đọc tiếng Anh.
   - Thay thế toàn bộ `onclick="speakBlockEn..."` trên các nút loa 🔊 thành `onclick="speakBlockAuto..."`.
   - Bỏ lệnh tự đảo ngôn ngữ trong `speakBlockEn`.
   - Sinh 26 file MP3 giọng Hoài My vào `audio/` bằng `export_hoaimy_audio.py` để chạy mượt mà trên Chrome, Cốc Cốc, Edge, Offline.
3. **Khắc phục lỗi cuộn trang khi vẽ bút:**
   - Tối ưu kích thước slide 16:9 vừa vặn màn hình trình chiếu.
   - Khi bật Bút vẽ (`body.pen-mode`), tự động khóa cuộn trang (`overflow: hidden`).
4. **Tinh giản Thanh công cụ `#controlBar`:**
   - Bỏ hoàn toàn nút `[💬 Tắt phụ đề]`.
   - Bố trí thanh công cụ tinh gọn, trực quan, phân chia rõ ràng các nhóm nút.
5. **Tích hợp BẢNG VIẾT DẠY HỌC (`#blackboardOverlay` / Phím tắt `W` hoặc `B`):**
   - Thêm nút `[📋 Bảng viết]` trên thanh điều khiển.
   - Khi bấm (hoặc nhấn phím `W` / `B`): Bảng xanh ô ly truyền thống phủ toàn màn hình.
   - Hỗ trợ viết phấn trắng, phấn vàng, xóa bảng, và **giữ phím `Shift` để vẽ đường thẳng tắp** phục vụ môn Hình học.
   - Nhấn `Escape` hoặc nút đóng để quay lại đúng slide đang giảng dạy mà không làm mất bài học.
6. **Cụm nút nhảy nhanh theo Tiết học (`[Tiết 1]`, `[Tiết 2]`, `[Tiết 3]`):**
   - Bố trí cụm nút chuyển nhanh theo tiết cạnh số trang slide hoặc trên thanh điều khiển:
     + `[Tiết 1]` $\rightarrow$ Nhảy đến Slide 1
     + `[Tiết 2]` $\rightarrow$ Nhảy đến Slide 9
     + `[Tiết 3]` $\rightarrow$ Nhảy đến Slide 16
7. **Chuẩn hóa triệt để Mục 5 trong Prompt & Rules:**
   - Thay thế skeleton cũ ở Mục 5 của `PROMPT_TAO_BAI_GIANG_HTML.md` và `.agents/rules/tao-bai-giang-html.md` bằng bộ khung chuẩn có sẵn Laser, Bút vẽ, Bảng viết nháp, nút nhảy tiết và loa song ngữ.

## Ngoài phạm vi
- Không thay đổi nội dung chuẩn kiến thức SGK Toán 9.

## File dự kiến tác động
1. `TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html`
2. `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html`
3. `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/audio/` (chứa các file `slide-*.mp3`)
4. `TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md`
5. `.agents/rules/tao-bai-giang-html.md`
6. `tests/trolythien-template-smoke.js`
7. `tests/trolythien-bai-giang-html-smoke.js`

## Các bước thực hiện
1. **Bước 1: Thiết kế BẢNG VIẾT DẠY HỌC (`#blackboardOverlay`)**
   - Thêm HTML `#blackboardOverlay` (bảng xanh ô ly) và `#blackboardCanvas`.
   - Thêm CSS bảng xanh sư phạm và thanh công cụ viết phấn trắng/vàng, xóa bảng.
   - Viết JS: `toggleBlackboard()`, `clearBlackboard()`, phím `W` / `B`, giữ `Shift` vẽ đường thẳng.
2. **Bước 2: Tinh giản thanh công cụ `#controlBar` & Thêm nút Nhảy Tiết học**
   - Xóa bỏ nút `[💬 Tắt phụ đề]`.
   - Bố trí nút `[📋 Bảng viết]`.
   - Thêm cụm nút `[Tiết 1]`, `[Tiết 2]`, `[Tiết 3]` nhảy nhanh đến Slide 1, 9, 16.
3. **Bước 3: Khắc phục lỗi cuộn trang khi vẽ bút**
   - Khi bật bút (`pen-mode`), khóa cuộn `overflow: hidden`.
4. **Bước 4: Nút loa thông minh `speakBlockAuto` & Xuất bộ audio MP3 Hoài My**
   - Khai báo hàm `speakBlockAuto(blockEl)` tự động chọn ngôn ngữ.
   - Thay thế toàn bộ `onclick="speakBlockEn..."` trên các nút loa 🔊 thành `onclick="speakBlockAuto..."`.
   - Bỏ lệnh tự đảo ngôn ngữ trong `speakBlockEn`.
   - Chạy `export_hoaimy_audio.py` xuất 26 file MP3 giọng Hoài My vào thư mục `audio/`.
5. **Bước 5: Chuẩn hóa Cột Ghi bảng Bài 12 súc tích & cố định**
   - Đặt tiêu đề mục cố định ở đầu Cột Ghi bảng (`data-step="0"`).
   - Giữ nguyên công thức cốt lõi suốt các slide trong cùng một mục.
   - Toàn bộ đề bài, hình vẽ, lời giải đưa về Cột Hoạt động (cột phải).
6. **Bước 6: Đồng bộ Mục 5 Skeleton trong Prompt & Rules**
   - Thay thế skeleton cũ bằng bộ khung HTML chuẩn có sẵn đầy đủ các công cụ trên.
7. **Bước 7: Cập nhật và chạy kiểm thử tự động**
   - Cập nhật assertions trong `tests/trolythien-template-smoke.js` và `tests/trolythien-bai-giang-html-smoke.js`.
   - Chạy test đảm bảo 100% PASS.

## Cách kiểm thử
1. Mở `Bai_12...html` trên Google Chrome:
   - Bấm nút `[Tiết 1]`, `[Tiết 2]`, `[Tiết 3]`: Nhảy chính xác đến các slide mốc.
   - Bấm nút `[📋 Bảng viết]` (hoặc phím `W`): Bảng xanh ô ly hiện ra, giữ Shift vẽ đường thẳng chuẩn xác. Bấm Escape để đóng.
   - Bật bút vẽ trên slide: không bị lệch hay trôi nét khi rê chuột.
   - Đang ở giao diện tiếng Việt: bấm loa đọc tiếng Việt (giọng Hoài My), không nhảy sang tiếng Anh.
   - Thanh công cụ không còn nút tắt phụ đề, thoáng đãng.
   - Cột ghi bảng bên trái súc tích và cố định công thức cốt lõi.
2. Chạy smoke tests:
   - `node tests/trolythien-template-smoke.js`
   - `node tests/trolythien-bai-giang-html-smoke.js`

## Tiêu chí nghiệm thu
- Có Bảng viết dạy học (`#blackboardOverlay`, phím `W`), viết phấn và vẽ đường thẳng bằng Shift.
- Có cụm nút nhảy nhanh theo tiết học (`[Tiết 1]`, `[Tiết 2]`, `[Tiết 3]`).
- Bật bút vẽ trên slide không bị trôi lệch.
- Thanh công cụ tinh gọn, bỏ nút tắt phụ đề.
- Nút loa 🔊 thông minh: giao diện nào đọc tiếng đó.
- Cột Ghi bảng ngắn gọn, chứa tiêu đề mục và cố định định lí cốt lõi.
- Bộ kiểm thử tự động đạt 100% PASS.
