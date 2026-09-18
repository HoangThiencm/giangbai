# PLAN: Liên Thông Tạo Bài Tập Sang Thi Trực Tuyến 1-Click & Bổ Sung Chế Độ Thi Cuốn Chiếu Chống Chụp Gửi AI

## Hiện trạng
1. **Tạo bài tập chưa có liên thông trực tiếp sang Thi trực tuyến**:
   - Trong `taobaitap.html` (và bản sao `backupcode viettailieu/taobaitap.html`), sau khi AI sinh đề (CV 7991 17 câu hoặc trắc nghiệm 20 câu), giáo viên chỉ có các nút: `Xuất Mẫu CV 7991`, `Xuất 100% TN`, `.txt`, `LaTeX` và `DẠY NGAY` (trình chiếu).
   - Chưa có nút chuyển trực tiếp sang `thitructuyen.html`. Giáo viên muốn tổ chức thi phải: Tải file Word/Text về máy $\rightarrow$ Mở trang `thitructuyen.html` $\rightarrow$ Tải file lên $\rightarrow$ Kiểm tra lại bảng đáp án $\rightarrow$ Mới có thể lưu đề. Quy trình này mất nhiều bước và dễ phát sinh lỗi định dạng.
2. **Thi trực tuyến chưa có chế độ khắc chế chụp ảnh gửi AI**:
   - Trong `thitructuyen.html`, giao diện làm bài của học sinh hiện cuộn dọc hiển thị toàn bộ danh sách câu hỏi một lúc.
   - Học sinh ở nhà có thể dễ dàng dùng điện thoại thứ hai chụp ảnh màn hình từng câu gửi ChatGPT/Gemini/Photomath mà không gặp áp lực về thời gian vận hành.
   - Thời gian làm bài đang mặc định là 45 phút, chưa có tùy chọn mặc định nhanh 15 phút (hoặc các nút chọn nhanh 15p, 20p, 30p, 45p) cho các bài kiểm tra 17–20 câu nhanh.
   - Chưa có chế độ "Thi cuốn chiếu từng câu" (One-by-one mode) với giới hạn thời gian từng câu (45–50 giây/câu) và khóa quay lại câu cũ.
   - Chưa có Watermark bảo mật in mờ thông tin học sinh chống chụp ảnh chia sẻ ra ngoài và gây nhiễu AI Vision OCR.

---

## Phạm vi
1. **Liên thông 1-Click từ `taobaitap.html` sang `thitructuyen.html`**:
   - Bổ sung nút **"🚀 THI TRỰC TUYẾN"** trên thanh nút hành động ở Bước 2 của `taobaitap.html` và `backupcode viettailieu/taobaitap.html` (nằm cạnh nút "DẠY NGAY").
   - Hàm `startOnlineExam()`:
     + Chuyển đổi toàn bộ câu hỏi trong state (`questions`) sang cấu trúc dữ liệu chuẩn của `thitructuyen.html` (hỗ trợ cả 3 phần CV 7991: `mc`, `tf` 4 ý $a-d$, `short_answer` điền số).
     + Thiết lập tiêu đề theo chủ đề (`topics[0].name`), thời gian làm bài mặc định **15 phút**.
     + Đóng gói vào `localStorage.setItem('thitructuyen_pending_import', ...)` và mở `thitructuyen.html?from=taobaitap` trong tab mới.
2. **Tự động tiếp nhận và nạp đề tại `thitructuyen.html` (Đề mới & Đề cũ)**:
   - Khi khởi chạy, `thitructuyen.html` kiểm tra gói dữ liệu `thitructuyen_pending_import` trong `localStorage`.
   - Tự động nạp:
     + Tên đề thi, định dạng đề (`cv7991` hoặc `standard_mc`), thời gian **15 phút** (kèm các nút chọn nhanh 15p, 20p, 30p, 45p).
     + Toàn bộ danh sách câu hỏi và đáp án vào `allQuestions`.
     + Tự động kích hoạt sẵn cờ `anti_ai_one_by_one: true` (chế độ thi cuốn chiếu).
     + Bỏ qua Bước 1 (tải file) và chuyển thẳng vào Bước 2 (Xem lại & Cấu hình phòng thi).
   - **Áp dụng cho cả đề cũ**: Trong danh sách đề thi của giáo viên (`TeacherDashboard`), khi bấm nút **"Sửa đề"** (icon bút chì), giáo viên có thể chỉnh sửa thời gian thành 15 phút, bật/tắt cờ `anti_ai_one_by_one` và `anti_ai_watermark`, rồi bấm "Lưu Đề" để cập nhật ngay cho học sinh.
3. **Chế độ thi cuốn chiếu chống chụp gửi AI (One-by-one Mode)**:
   - Thêm checkbox cấu hình trong modal cài đặt thi của giáo viên: `[x] Chế độ thi cuốn chiếu (Chống chụp gửi AI)`.

   - Giao diện làm bài của học sinh khi bật chế độ này:
     + Chỉ hiển thị **duy nhất 1 câu hỏi tại một thời điểm**.
     + Có thanh tiến trình hoặc đồng hồ mini đếm ngược riêng cho câu hiện tại: ví dụ bài 15 phút gồm 17 câu $\rightarrow$ mỗi câu có khoảng **50 giây** (hoặc 45 giây cho trắc nghiệm, 90 giây cho Đúng/Sai).
     + Hết giờ câu đó hoặc bấm "Câu tiếp theo" $\rightarrow$ tự động chuyển sang câu tiếp theo và **khóa vĩnh viễn không cho quay lại câu cũ (No Backtrack)**.
     + Đến câu cuối cùng, nút chuyển thành "Nộp bài".
     + Lưu tạm tiến trình `currentQuestionIndex` và `answers` vào `localStorage` để chống mất dữ liệu khi học sinh vô tình tải lại trang.
4. **Watermark bảo mật chống chụp màn hình (Anti-OCR)**:
   - Khi học sinh làm bài, hiển thị một lớp watermark chìm mờ chạy chéo màn hình với thông tin: `[Họ tên học sinh] - [SBD / Lớp] - [Thời gian thi]`.
   - Vừa răn đe học sinh không chụp ảnh gửi ra ngoài, vừa tạo nhiễu quang học làm AI Vision OCR đọc sai công thức toán học khi chụp qua màn hình máy tính.
5. **Cứu hộ triệt để catalog PPDH/KTDH trên `canvas_soankhbd.html`**:
   - Nâng cấp hàm fallback `ensureKhbdPedagogyCatalogFallback()` trong `canvas_soankhbd.html`: Nếu file `js/khbd-pedagogy-catalog.js` trên hosting bị rỗng (0 bytes) hoặc lỗi mạng, tự động nạp dự phòng ngay từ CDN GitHub jsDelivr (`https://cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-pedagogy-catalog.js`).
   - Giúp bảng PPDH, KTDH 4 pha và Hoạt động môn học luôn hiển thị đầy đủ 100% trên web `hoangthiencm.id.vn` mà không bao giờ bị trắng trơn.
6. **Kiểm thử tự động**:
   - Tạo file test `tests/taobaitap-thitructuyen-bridge-smoke.js` kiểm tra toàn bộ luồng đóng gói, chuyển đổi dữ liệu, tiếp nhận tại `thitructuyen`, và các cờ cấu hình thi cuốn chiếu.
   - Cập nhật `tests/canvas-soankhbd-smoke.js` kiểm tra fallback CDN của catalog PPDH.

---

## Ngoài phạm vi
- Không thay đổi các prompt sinh câu hỏi AI cốt lõi trong `taobaitap.html`.
- Không can thiệp hay thay đổi API backend MySQL / Google Drive trong `api/exam.php`.
- Không thay đổi cách chấm điểm chuẩn CV 7991 đã hoàn thiện.

---

## File dự kiến tác động
1. `taobaitap.html`
2. `backupcode viettailieu/taobaitap.html`
3. `thitructuyen.html`
4. `access-control.js`
5. `canvas_soankhbd.html`
6. `tests/taobaitap-thitructuyen-bridge-smoke.js`
7. `tests/canvas-soankhbd-smoke.js`

---

## Khắc phục triệt để lỗi Mở ra trang trắng (White Screen Fix)

### Nguyên nhân gây trang trắng khi mở từ `taobaitap.html`:
1. **Chặn bởi `access-control.js`**:
   `access-control.js` hiện chỉ miễn kiểm tra token khi `mode === 'student' && examId`. Khi mở `thitructuyen.html?from=taobaitap`, nếu giáo viên chưa đăng nhập hoặc đang dùng offline, script sẽ ép redirect về `login.html`.
2. **Chặn bởi kiểm tra `userEmail` trong `thitructuyen.html`**:
   Tại dòng 4695, nếu `!userEmail`, component `App` trả về màn hình "Phiên đăng nhập hết hạn". Nếu bị lỗi unhandled trong React hoặc mất phiên, trang hiển thị trắng xóa. Cần fallback `userEmail = userEmail || 'giaovien@giangbai.local'` khi có cờ `from=taobaitap` hoặc `thitructuyen_pending_import`.
3. **Race Condition & Sập State `HybridExamCreator`**:
   Cả `App` và `HybridExamCreator` đều đọc và xóa `thitructuyen_pending_import`. Khi `App` xóa trước, `HybridExamCreator` không nạp được `examInfo` (mất title, duration 15p, cờ cuốn chiếu). Ngoài ra ở render đầu tiên của Bước 2, `activePageId` là `null` và `pages` là `[]`, gây lỗi tham chiếu nếu không được khởi tạo đồng bộ.
4. **Lỗi `Sortable is not defined`**:
   Tại dòng 1818, `new Sortable(el)` không kiểm tra `typeof Sortable !== 'undefined'`. Khi mạng chập chờn CDN không tải được SortableJS, React ném ngoại lệ và unmount toàn bộ giao diện thành trang trắng.

### Giải pháp kỹ thuật:
1. **Trong `access-control.js`**:
   Thêm điều kiện miễn trừ:
   ```javascript
   const isOpenExamLink = pageKey === 'thitructuyen'
       && ((params.get('mode') === 'student' && !!getQueryParamInsensitive(params, 'examId'))
           || params.get('from') === 'taobaitap');
   ```
2. **Trong `thitructuyen.html`**:
   - Khởi tạo an toàn cho `userEmail`:
     ```javascript
     const isFromTaobaitap = new URLSearchParams(window.location.search).get('from') === 'taobaitap';
     const userEmail = localStorage.getItem('userEmail') || (isFromTaobaitap ? 'giaovien@giangbai.local' : null);
     ```
   - Trong `HybridExamCreator`:
     + Thêm guard `if (el && typeof Sortable !== 'undefined')` trước khi khởi tạo `new Sortable`.
     + Đồng bộ cập nhật `examInfo` từ `initialData.info` khi `initialData` thay đổi.
     + Đồng bộ nạp danh sách câu hỏi `initialData.questions` vào `pageQuestions` và `pages` với `activePageId = "imported"`.


## Các bước thực hiện

### Bước 1: Nâng cấp `taobaitap.html` và `backupcode viettailieu/taobaitap.html`
1. Viết hàm chuyển đổi `mapToThiTrucTuyenPayload(questions, topics, synthForm)`:
   - Duyệt qua `questions` và chuẩn hóa:
     + `multiple-choice` $\rightarrow$ `{ id, type: 'mc', question, options, correct_index, explanation }`.
     + `true-false` (CV 7991) $\rightarrow$ `{ id, type: 'tf', question, options: 4 ý a-d, correct_answers: [4 boolean], explanation }`.
     + `short-answer` $\rightarrow$ `{ id, type: 'short_answer', question, correct_answer: String(clean), explanation }`.
   - Thiết lập `duration: 15` (mặc định 15 phút), `exam_format: (synthForm === 'cv7991' ? 'cv7991' : 'standard_mc')`.
   - Bật cờ `anti_ai_one_by_one: true` và `anti_ai_watermark: true`.
2. Viết hàm `startOnlineExam()`:
   - Kiểm tra có câu hỏi hay chưa.
   - Lưu payload vào `localStorage.setItem('thitructuyen_pending_import', JSON.stringify(payload))`.
   - Mở cửa sổ mới: `window.open('thitructuyen.html?from=taobaitap', '_blank')`.
3. Thêm nút bấm **"🚀 THI TRỰC TUYẾN"** bên cạnh nút "DẠY NGAY" ở Bước 2.
4. Đồng bộ 100% sang `backupcode viettailieu/taobaitap.html`.

### Bước 2: Nâng cấp `thitructuyen.html` — Tiếp nhận đề 1-Click
1. Trong component tạo đề (`CreateExamModal` hoặc màn hình tạo đề):
   - Thêm `useEffect` kiểm tra `localStorage.getItem('thitructuyen_pending_import')`.
   - Nếu có: parse JSON, cập nhật `examInfo` (`title`, `duration: 15`, `exam_format`, `anti_ai_one_by_one: true`, `anti_ai_watermark: true`), nạp `allQuestions`, xóa key trong `localStorage` và đặt `setStep(2)` (nhảy thẳng vào xem lại / cấu hình).
2. Thêm các nút chọn nhanh thời gian tại ô nhập `duration`: `[15p]`, `[20p]`, `[30p]`, `[45p]`.
3. Thêm checkbox cấu hình: `Chế độ thi cuốn chiếu từng câu (Chống chụp gửi AI)` và `Watermark bảo mật`.

### Bước 3: Nâng cấp `thitructuyen.html` — Giao diện làm bài thi cuốn chiếu & Watermark
1. Khi `exam.info.anti_ai_one_by_one` bật:
   - Thêm state `currentQuestionIdx` (mặc định 0).
   - Chỉ render thẻ câu hỏi tại `shuffledQuestions[currentQuestionIdx]`.
   - Thanh header hiển thị: `Câu [currentQuestionIdx + 1] / [shuffledQuestions.length]`.
   - Đồng hồ đếm ngược từng câu: Phân bổ `Math.floor((examInfo.duration * 60) / shuffledQuestions.length)` giây cho mỗi câu (ví dụ 15 phút cho 17 câu $\approx$ 52 giây/câu).
   - Khi hết thời gian câu hoặc học sinh bấm "Câu tiếp theo" $\rightarrow$ tự động chuyển `currentQuestionIdx + 1`, **không có nút quay lại**.
   - Tại câu cuối cùng $\rightarrow$ nút "Nộp bài".
2. Watermark bảo mật:
   - Nếu `anti_ai_watermark` bật: Render container cố định `pointer-events-none fixed inset-0 z-40` với chữ chìm mờ in tên học sinh, SBD và ngày giờ thi xoay góc -25 độ lặp lại trên nền màn hình.

### Bước 4: Nâng cấp Fallback tự cứu hộ trong `canvas_soankhbd.html`
1. Tại hàm `ensureKhbdPedagogyCatalogFallback()` ([canvas_soankhbd.html:1139](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/canvas_soankhbd.html#L1139)):
   - Nếu sau khi nạp từ hosting mà `typeof window.KHBD_PEDAGOGY_CATALOG === "undefined"`:
     Tự động nạp dự phòng từ CDN GitHub jsDelivr:
     ```javascript
     var cdnCatalog = "https://cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-pedagogy-catalog.js";
     document.write('<script src="' + (isLocal ? "js/khbd-pedagogy-catalog.js" : cdnCatalog) + '"><\/script>');
     ```
   - Nhờ vậy, ngay cả khi file `js/khbd-pedagogy-catalog.js` trên hosting bị rỗng 0 bytes, trình duyệt vẫn kéo đủ 66 KB catalog từ CDN về và render đầy đủ 100% PPDH/KTDH.

### Bước 5: Kiểm thử tự động
1. Tạo file kiểm thử `tests/taobaitap-thitructuyen-bridge-smoke.js`:
   - Kiểm tra sự hiện diện và chức năng của nút "THI TRỰC TUYẾN" và hàm đóng gói trong `taobaitap.html` (cả 2 bản).
   - Kiểm tra hàm tiếp nhận đề `thitructuyen_pending_import`, thời gian mặc định 15 phút, và cờ `anti_ai_one_by_one` trong `thitructuyen.html`.
   - Kiểm tra UI thi cuốn chiếu, logic khóa không cho quay lại câu trước, và watermark.
2. Cập nhật `tests/canvas-soankhbd-smoke.js` kiểm tra assert CDN fallback của catalog.
3. Chạy toàn bộ các test suite liên quan:
   ```powershell
   node tests/taobaitap-thitructuyen-bridge-smoke.js
   node tests/canvas-soankhbd-smoke.js
   node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js
   node tests/taobaitap-plan-smoke.js
   ```


---

## Rủi ro
1. **Học sinh tải lại trang khi đang thi cuốn chiếu**:
   - Khắc phục: Lưu `currentQuestionIdx` và thời gian câu hỏi vào `localStorage` theo từng `examId` để khi F5 trang web vẫn phục hồi đúng câu đang làm, không cho làm lại các câu đã qua.
2. **Khác biệt cấu trúc dữ liệu Đúng/Sai và Điền số**:
   - Cần đảm bảo hàm `mapToThiTrucTuyenPayload` xuất đúng `options` 4 ý và `correct_answers` dạng boolean cho `tf`, và `correct_answer` dạng chuỗi sạch cho `short_answer`.

---

## Cách kiểm thử
Chạy các lệnh terminal:
```powershell
node tests/taobaitap-thitructuyen-bridge-smoke.js
node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js
node tests/taobaitap-plan-smoke.js
```

---

## Tiêu chí nghiệm thu
1. Trên `taobaitap.html` (và bản backup): Xuất hiện nút **"🚀 THI TRỰC TUYẾN"**; khi bấm sẽ đóng gói đầy đủ 17 câu CV 7991 hoặc 20 câu TN kèm đáp án chính xác sang `localStorage` và mở `thitructuyen.html`.
2. Trên `thitructuyen.html`: Tự động đón nhận đề thi, điền sẵn thời gian mặc định là **15 phút** (có các nút chọn nhanh 15p, 20p, 30p, 45p), nạp toàn bộ câu hỏi và đáp án vào Bước 2 mà không cần bấm tải file.
3. Khi bật "Chế độ thi cuốn chiếu": Màn hình thi hiển thị từng câu, có đồng hồ đếm ngược từng câu (~45–52s/câu), hết giờ hoặc bấm câu tiếp sẽ khóa vĩnh viễn không cho quay lại câu cũ.
4. Lớp Watermark bảo mật hiển thị mờ thông tin học sinh trên màn hình làm bài.
5. Toàn bộ smoke test kiểm thử liên thông và CV 7991 pass 100%.

