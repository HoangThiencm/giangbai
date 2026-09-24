# PLAN: Thêm tùy chỉnh số câu trắc nghiệm CV 7991 và chức năng quay số gọi tên từ danh sách lớp vào taobaitap.html

## Hiện trạng
1. **Về cấu trúc Công văn 7991 trong `taobaitap.html`:**
   - Dropdown `synthForm` hiện tại gồm tùy chọn `cv7991` (mặc định 17 câu: 12 TN + 1 Đ/S + 4 TL ngắn).
   - Phần cấu hình CV 7991 (`cv7991Config`) có preset `custom` nhưng bị giấu sau nút click phụ "Chỉnh sửa số câu từng phần", chưa có tùy chọn độc lập rõ ràng trên menu hình thức để người dùng chủ động chọn "Dạng Công văn 7991 (Tùy chỉnh số câu/mức độ)" bám sát Menu tạo bài tập của trợ lý.
   - Khi người dùng muốn đổi số lượng câu trắc nghiệm (Phần I) tự do (ví dụ: 6, 8, 10, 14, 18 câu...), giao diện cần hiển thị trực quan, tính toán lại tổng điểm và phân bổ điểm số tương ứng.

2. **Về chức năng gọi học sinh kiểm tra:**
   - Trong `sodiem.html` đã có module sổ điểm hoàn chỉnh: danh sách lớp lấy từ API `api/sodiem.php?action=classes`, danh sách học sinh theo lớp, chức năng vòng quay / bốc ngẫu nhiên học sinh, hiển thị câu hỏi, chấm điểm (0–10) và lưu trực tiếp vào CSDL/localStorage của sổ điểm.
   - Trong `taobaitap.html`, chế độ trình chiếu câu hỏi (`QuizPresentationMode` và `EssayPresentationMode`) hiện chỉ phục vụ hiển thị câu hỏi và bấm làm bài, chưa có nút gọi ngẫu nhiên học sinh từ danh sách lớp để kiểm tra miệng/đánh giá thường xuyên trực tiếp trên màn hình chiếu.

---

## Phạm vi thực hiện
1. **Cấu trúc Công văn 7991 tùy chỉnh số câu trắc nghiệm trong `taobaitap.html`:**
   - Bổ sung tùy chọn hình thức rõ ràng: `cv7991-custom`: "⭐ Dạng Công văn 7991 (Tùy chỉnh số câu trắc nghiệm / mức độ)" trong dropdown `synthForm`.
   - Hiển thị trực quan cụm điều khiển số câu cho từng phần:
     + Số câu Phần I (Trắc nghiệm nhiều lựa chọn): cho phép tăng giảm linh hoạt (mặc định gợi ý: 6, 8, 12, 16...).
     + Số câu Phần II (Trắc nghiệm Đúng/Sai 4 ý).
     + Số câu Phần III (Trắc nghiệm Trả lời ngắn).
   - Đảm bảo logic tính toán điểm tự động `allocateCv7991PartScores` và prompt gửi AI `generateSynthesizedFromSource` nhận chính xác số câu trắc nghiệm tùy chỉnh.
   - Bảo toàn tương thích xuất file Word/Text CV 7991 và các bộ test tự động (`tests/cv7991-taobaitap-thitructuyen-sync-smoke.js`).

2. **Chức năng quay số / gọi tên học sinh kiểm tra từ danh sách lớp trong `taobaitap.html`:**
   - Thêm nút "🎲 Gọi học sinh" / "Quay số kiểm tra" trên thanh tiêu đề của `QuizPresentationMode` và `EssayPresentationMode`.
   - Xây dựng component modal gọi học sinh (`CallStudentModal`):
     + Nạp danh sách lớp từ API `api/sodiem.php?action=classes` (kèm fallback đọc cache `localStorage` của `sodiem.html` và cho phép dán danh sách thủ công nếu offline).
     + Chọn lớp cần gọi kiểm tra.
     + Nút "QUAY SỐ" / "BỐC TÊN" với hiệu ứng chạy chữ ngẫu nhiên kèm âm thanh / confetti khi dừng lại.
     + Hiển thị nổi bật tên học sinh được gọi và nội dung câu hỏi hiện tại đang chiếu.
     + Nhập điểm đánh giá (thang điểm 0–10) và chọn cột điểm (KTTX 1, KTTX 2, Điểm miệng...).
     + Nút "Lưu điểm vào sổ điểm": gửi dữ liệu đến `api/sodiem.php?action=save` và đồng bộ `localStorage` của Sổ Điểm để giáo viên mở lại `sodiem.html` là thấy điểm ngay.

---

## Ngoài phạm vi
- Không sửa đổi cấu trúc dữ liệu backend trong CSDL MySQL hay thay đổi định dạng API `api/sodiem.php`.
- Không thay đổi giao diện cốt lõi của các game giáo dục khác hoặc các trang không liên quan.

---

## File dự kiến tác động
- `taobaitap.html` (Mã nguồn giao diện Tạo bài tập & Trình chiếu)
- `docs/handoff/IMPLEMENT.md` (Ghi nhận nhật ký triển khai)

---

## Các bước thực hiện chi tiết cho Coder
1. **Bước 1: Mở khóa file handoff:**
   - Xóa `docs/handoff/.lock` trước khi sửa source.

2. **Bước 2: Cập nhật cấu hình CV 7991 tùy chỉnh số câu trong `taobaitap.html`:**
   - Tìm khối select `synthForm` (khoảng dòng 17115–17137):
     + Bổ sung option:
       `<option value="cv7991-custom">⭐ Dạng Công văn 7991 (Tùy chỉnh số câu trắc nghiệm / các phần)</option>`
     + Khi chọn `cv7991-custom`, kích hoạt ngay chế độ `preset: 'custom'` và hiển thị các ô input nhập số câu Phần I, Phần II, Phần III.
   - Cập nhật hàm xử lý prompt `generateSynthesizedFromSource`:
     + Nhận diện cả `synthForm === 'cv7991'` lẫn `synthForm === 'cv7991-custom'`.
     + Đọc đúng `countPart1` (số câu trắc nghiệm do giáo viên tùy chỉnh) để đưa vào chỉ dẫn prompt sinh đề và bộ chia điểm.
   - Cập nhật các bộ lọc và hàm xuất file (Word, Text, LaTeX, OLM) để nhận diện định dạng CV 7991 khi ở mode `cv7991-custom`.

3. **Bước 3: Tích hợp dữ liệu Sổ Điểm và chức năng gọi học sinh trong Trình chiếu:**
   - Bổ sung helper functions nạp danh sách lớp và học sinh từ Sổ Điểm:
     + `fetchSodiemClasses()`: gọi `api/sodiem.php?action=classes` hoặc duyệt keys `sodiem:*:*:*` trong `localStorage`.
     + `fetchSodiemStudents(className, subject)`: gọi `api/sodiem.php?action=load` hoặc parse từ `localStorage.getItem("sodiem:" + className + ":" + subject + ":2025-2026")`.
     + `saveSodiemStudentScore(className, subject, studentId, column, score)`: gửi `POST` đến `api/sodiem.php?action=save` và cập nhật `localStorage`.
   - Trong component `QuizPresentationMode` (dòng ~14510) và `EssayPresentationMode` (dòng ~14810):
     + Thêm nút bấm icon gọi loa/xúc xắc: `<button onClick={() => setShowStudentPicker(true)} className="bg-amber-500 hover:bg-amber-400 text-slate-900 font-bold px-3 py-1.5 rounded-lg flex items-center gap-1.5 text-sm shadow">🎲 Gọi học sinh</button>`.
   - Xây dựng component giao diện `StudentPickerModal`:
     + Giao diện nổi (modal overlay) với phong cách sư phạm chuyên nghiệp.
     + Bộ chọn lớp học (Select box) và hiển thị sĩ số.
     + Vùng hiển thị tên học sinh với hiệu ứng quay số chạy ngẫu nhiên (animation shuffle ~2-3 giây) kèm âm thanh click/beep.
     + Khi dừng: hiển thị rõ Họ tên, Mã/SBD, câu hỏi đang chiếu.
     + Form chấm điểm: input điểm số (0 - 10), select cột điểm (tự động lấy danh sách cột từ sổ điểm), nút "Lưu vào sổ điểm" và nút "Để sau / Bỏ qua".
     + Thông báo lưu thành công và cập nhật ngay vào dữ liệu sổ điểm.

4. **Bước 4: Chạy kiểm thử tự động:**
   - Chạy `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js` để đảm bảo logic trích xuất CV 7991 không bị ảnh hưởng.
   - Chạy `node tests/taobaitap-presentation-smoke.js` nếu có.

5. **Bước 5: Hoàn tất tài liệu handoff:**
   - Ghi nhật ký vào `docs/handoff/IMPLEMENT.md`.
   - Tạo lại file `docs/handoff/.lock` nội dung `LOCK`.

---

## Rủi ro và biện pháp xử lý
- **Rủi ro 1: Phá vỡ logic đồng bộ với `thitructuyen.html` hoặc xuất file CV 7991:**
  - *Giải pháp:* Tùy chọn `cv7991-custom` sử dụng cùng schema câu hỏi và bộ parser `buildCv7991ExportHtml`, `buildCv7991ExportText`, chỉ thay đổi linh hoạt số lượng phần tử của `part1`, `part2`, `part3`.
- **Rủi ro 2: Mất kết nối API Sổ điểm hoặc chưa đăng nhập CSDL:**
  - *Giải pháp:* Luôn ưu tiên đọc/ghi song song vào `localStorage` của trình duyệt theo đúng format key `sodiem:${class}:${subject}:2025-2026`, đảm bảo hoạt động mượt mà cả offline lẫn online.

---

## Cách kiểm thử
1. **Kiểm tra chức năng CV 7991 tùy chỉnh:**
   - Mở `taobaitap.html`.
   - Chọn hình thức "⭐ Dạng Công văn 7991 (Tùy chỉnh số câu trắc nghiệm / các phần)".
   - Điều chỉnh số câu Phần I (ví dụ: 6 hoặc 8 câu trắc nghiệm), 1 câu Đúng/Sai, 2 câu Trả lời ngắn.
   - Bấm sinh đề và kiểm tra: đề ra đúng số lượng từng phần, điểm số tính toán tự động chuẩn xác, xuất file Word và Text đầy đủ.
2. **Kiểm tra chức năng Gọi học sinh:**
   - Vào mục Trình chiếu bài tập (Presentation).
   - Bấm nút "🎲 Gọi học sinh".
   - Chọn lớp học đã có trong sổ điểm.
   - Bấm "Quay số" -> Tên học sinh quay ngẫu nhiên và dừng lại.
   - Nhập điểm (ví dụ: 9.0), chọn cột "KTTX 1", bấm "Lưu vào sổ điểm".
   - Mở trang `sodiem.html` kiểm tra xem điểm của học sinh đó đã được cập nhật chính xác hay chưa.

---

## Tiêu chí nghiệm thu
- Có tùy chọn Công văn 7991 tùy chỉnh số câu trắc nghiệm một cách rõ ràng, trực quan.
- Chế độ trình chiếu có tính năng quay số gọi tên ngẫu nhiên học sinh từ danh sách lớp của Sổ Điểm.
- Điểm chấm trực tiếp trong lúc gọi học sinh được đồng bộ vào Sổ Điểm (`sodiem.html`).
- Không có lỗi console JavaScript, các bài test hiện có chạy qua PASS 100%.
