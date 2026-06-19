# Thông tin dự án

## Cấu trúc hiện tại của dự án
Dự án được xây dựng dựa trên stack: HTML, CSS (Tailwind), JS thuần ở phía Frontend và PHP (PDO) + MySQL ở phía Backend.

### Các file và chức năng chính
1. **Giao diện bài học (`lotrinhtoan6.html`, `lotrinhtoan7.html`, `lotrinhtoan8.html`, `lotrinhtoan9.html`)**
   - Chứa cấu trúc HTML cho lộ trình học môn Toán các lớp; mỗi trang đặt `window.LOTRINH_SUBJECT` và `window.LOTRINH_PAGE_TITLE` (UTF-8 đúng).
   - Layout học sinh: cột trái (tiến độ + danh sách/bản đồ bài), cột giữa (nội dung bài), cột phải (kế hoạch tự học, động lực, kỹ năng, nhiệm vụ).
   - Định dạng CSS nội bộ (`<style>`) giúp render MathJax SVG và bong bóng chat AI giải thích.
   - Đã thêm style `.ai-chat-bubble` đồng bộ cho cả Toán 6, 7, 8, 9; bong bóng có nút `x`, mũi nhọn chat, và không bị cắt nội dung.
   - Cache script gần nhất: `lotrinh.js?v=20260620-motivation-fix1`, `admin-lesson-manager.js?v=20260620-lesson-crud1`, `admin-progress.js?v=20260620-group-align1` (trên `lotrinhtoan6–9.html` và `index.html`). Trang `index.html` vẫn dùng `admin-progress.js?v=20260619-class-filter1` — nên đồng bộ khi cập nhật panel tiến độ.

2. **Logic Frontend (`lotrinh.js`)**
   - Quản lý trạng thái học tập của học sinh.
   - Gửi yêu cầu lưu tiến độ lên Server (`syncLessonState`) và cập nhật `state.progress` tại client ngay sau khi lưu thành công.
   - Xử lý các tương tác AI: `bindAiExplainButtons`, `showAiModal`; hiện tại `showAiModal` thực chất render bong bóng chat gần nút vừa bấm thay vì modal phủ toàn màn hình.
   - Kết xuất giao diện dựa trên dữ liệu (tiến độ, nội dung lý thuyết, bài tập).
   - Bài luyện tập trắc nghiệm hiển thị dấu đúng/sai ngay sau khi học sinh chọn đáp án; đáp án được chuẩn hóa kiểu dữ liệu để `1` và `"1"` đều chấm đúng.
   - Nút làm lại bài luyện chỉ reset phần luyện tập, giữ tiến trình học lý thuyết/ví dụ và cập nhật lại giao diện ngay.
   - Tiến trình bài hiện tại được tính theo các mốc: lý thuyết 30%, ví dụ 20%, luyện tập 50% theo tỷ lệ số câu đã làm. Giá trị này hiển thị ở sidebar và header bài học.
   - Tiến độ chương được tính bằng trung bình phần trăm hoàn thành của các bài trong lộ trình, không chỉ dựa vào số bài `mastered`; vì vậy đánh dấu đã học từng phần sẽ làm thanh tiến trình chương thay đổi.
   - Bảng kỹ năng không còn hiển thị `--` khi học sinh vào luyện tập; mặc định hiển thị `0%`, lấy tiến độ hoàn thành bài làm mức tối thiểu, và cập nhật theo thao tác đánh dấu/nộp bài.
   - Khi bài đã học xong (`mastered`), nút trên header bài học đổi thành "Học lại"; bấm nút này sẽ reset tiến trình bài hiện tại để học sinh làm lại.
   - Giao diện giáo viên (`lessonDesignerMount`) có panel soạn bài (`admin-lesson-manager.js`, chỉ khi `userRole === 'teacher'`) và panel theo dõi tiến độ (`admin-progress.js`). Trang `admin.html` không mount hai panel này — admin chỉ quản lý tài khoản và cài đặt hệ thống.
   - Marker `[AI]` / `[[AI]]` trong nội dung lý thuyết quyết định vị trí nút **AI giải thích**; không tự gắn theo ngắt đoạn.
   - `lessonRichText()` render định dạng soạn bài: xuống dòng, đoạn, đậm/nghiêng/gạch chân, ảnh.
   - `renderNextAction()` gợi ý bước tiếp theo theo tab (lý thuyết / ví dụ / luyện tập) và tiến độ hiện tại.
   - **Danh sách bài** (`renderLessonList`): khung cuộn, tìm kiếm, lọc chương, dòng compact; khi gõ tìm/lọc chương chỉ render lại danh sách (`updateToolbar: false`) để giữ focus ô tìm. Tab **Bản đồ chương** (`renderChapterMap`) với `chapterAggregateStatus()` — Chưa học / Đang học / Cần luyện / Đã xong; bấm chương → lọc danh sách. View lưu `localStorage` key `lotrinh_lesson_nav_view_{môn}`.
   - **Kế hoạch tự học** (`renderStudyPlanner`, mount cột phải): khối **Ôn tập thông minh** + **Lộ trình hôm nay**; chọn 15–60 phút (`buildStudyPlan` ưu tiên smart review trước).
   - **Ôn tập thông minh** (`buildSmartReviewSuggestions`, `smartReviewReason`, `staleMasteredDays`): ưu tiên `needs_practice`, điểm dưới 80%; với `mastered` chỉ gợi ý ôn khi có `completedAt` hợp lệ và ≥ 7 ngày (`REVIEW_STALE_DAYS`). Bấm đề xuất → chuyển bài + tab luyện tập.
   - **Động lực học** (`renderMotivationPanel`, cột phải dưới kế hoạch): streak theo `todayKey()` **ngày local**; huy hiệu `streak_3`, `mastered_5`, `perfect_100`. Badge 100% chỉ khi `score >= 100` sau nộp luyện tập (`markPerfectLesson`), không từ nút **Đã học** thủ công. Lưu `localStorage` `lotrinh_motivation_{môn}_{user}`.

3. **Soạn bài giáo viên (`admin-lesson-manager.js`)**
   - Mount `#lessonDesignerMount` khi `userRole === 'teacher'`.
   - Trên trang `lotrinhtoan6–9`: khóa theo `LOTRINH_SUBJECT` — không chuyển sang môn khác.
   - Mục tiêu bài: textarea `#lessonGoalInput` (không trùng `#lessonGoal` hiển thị HS); lưu field `goal_text`.
   - **Mở cho học sinh** (`is_published`): mặc định **tắt** khi tạo bài mới / nhân bản; giáo viên chủ động bật khi muốn lộ trình tới bài đó. Học sinh chỉ nhận bài `is_published` từ API.
   - **Quản lý bài & chương** (panel soạn bài):
     - **Thêm**: nút *Tạo bài mới* → điền nội dung → *Lưu bài học* (`save_content`).
     - **Sửa**: chọn bài trong dropdown → chỉnh mọi trường (chương, tên, slug, nội dung…) → Lưu. Lưu theo `id` — đổi slug không tạo bài trùng.
     - **Xóa**: nút *Xóa bài đang chọn* → xác nhận → `delete_lesson` (xóa cả `student_lesson_progress` của bài đó).
     - **Nhân bản**: nút *Nhân bản bài đang chọn* → `duplicate_lesson` (tiêu đề thêm `(bản sao)`, slug mới, `is_published` tắt).
     - **Chương**: không có bảng chương riêng — mỗi bài có trường `chapter` (text). Ô Chương có `datalist` gợi ý chương đã có; nút *Đổi tên chương cho tất cả bài trong chương này* gọi `rename_chapter` (cập nhật hàng loạt theo môn). Dropdown bài hiển thị `Chương · Tên bài`.

4. **Theo dõi tiến độ giáo viên (`admin-progress.js`)**
   - Mount vào `#lessonDesignerMount` khi đăng nhập vai trò `teacher`.
   - Dropdown bài học, **lớp**, trạng thái, ô tìm kiếm; thẻ thống kê và bảng HS.
   - Gọi `api/admin_progress.php`; nhóm bảng theo lớp khi xem "Tất cả lớp" (mỗi cột `<td>` thẳng header).
   - Trên trang lộ trình: lọc dropdown bài học theo `LOTRINH_SUBJECT`.

5. **Backend API (`api/`)**
   - `lessons.php`: Lấy danh sách bài học; **lưu tiến độ** HS (`save_progress`, `reset_progress`); **soạn bài** GV (`save_content` theo `id`/slug, `delete_lesson`, `duplicate_lesson`, `rename_chapter`). Auto-migrate schema (`ensure_lesson_schema`, `ensure_progress_schema`) dùng try-catch riêng từng cột.
   - `admin_progress.php`: Trả dữ liệu theo dõi tiến độ học sinh theo `lesson_id`. Mỗi row gồm `class_name` (từ `users.class_name`); response thêm mảng `classes` (danh sách lớp distinct, đã sort). Cho phép session giáo viên đang hoạt động; admin key vẫn dùng được ở API nhưng UI admin không hiển thị panel tiến độ.
   - `admin_students.php`: Tạo/sửa học sinh kèm trường `class_name` — dùng để nhóm và lọc tiến độ theo lớp (vd. `6A`, `6B`, `6C` hoặc `Toán 6 tối T3`).
   - `ai_explain.php`: Gọi Gemini trước; nếu hết quota hoặc lỗi thì fallback ShopAIKey (`https://api.shopaikey.com/v1/chat/completions`, mặc định model `deepseek-v4-flash`). Cấu hình key/model trong `admin.html` → `global_config.json`. Trả JSON súc tích; đã tăng giới hạn token và nối tiếp khi câu trả lời bị ngắt.
   - `helpers.php`: Gồm các hàm tiện ích chung (`respond()`, `column_exists()`, `mysql_datetime_or_null()`).

6. **Thi trực tuyến (`thitructuyen.html`)**
   - Frontend React (CDN); backend đề thi/nộp bài/chấm điểm trên HuggingFace: `API_BASE` mặc định `https://hoangthiencm-giangbai.hf.space` (có thể ghi đè qua `localStorage.omr_backend_url`).
   - **Giáo viên**: soạn đề (PDF/Word + AI), lưu kho đề, xem QR/link chia sẻ, xem kết quả, xuất Excel.
   - **Học sinh**: mở link `?mode=student&examId=...` (không cần đăng nhập — `access-control.js` bỏ qua khi có `examId`).
   - **Trộn đề**: khi HS làm bài, thứ tự câu và đáp án trộn trên UI; đáp án nộp lên server dùng `originalIdx` / `originalOptIdx` (theo **đề gốc**). Chấm điểm và `details_json` (câu sai) cũng theo đề gốc.
   - **Nộp bài mobile/Zalo** (`StudentView`):
     - `isMobileExamClient()` nhận diện điện thoại / Zalo / in-app browser → **tắt** chống gian lận toàn màn hình và khóa màn hình.
     - `persistInfo()` + `sessionStorage` key `exam_student_info_{examId}` — giữ Họ tên/SBD khi nộp (fix mất tên do bàn phím tiếng Việt).
     - `formatApiError()` — không còn alert `[object Object]`; luôn gửi `student_class` (có thể rỗng).
     - Modal xác nhận nộp trên mobile; `ref` cho đáp án/tên khi hết giờ tự nộp.
   - **Kết quả GV** (`ResultDetail`): bảng chi tiết + khối **Học sinh thi nhiều lần** (gom theo SBD+tên); **Xuất Excel** một sheet: `STT | Họ và tên | Số báo danh | Lớp học | Điểm | Kết quả | Các câu đúng (đề gốc) | Các câu sai (đề gốc)` — đối chiếu `details_json` với `api/exam/get/{id}` để ra số câu đề gốc.
   - **QRModal**: hiển thị mã QR + ô link + nút **Copy** (clipboard / fallback) để GV gửi Zalo.

## Vấn đề cần lưu ý (Notes)
- **MathJax & Tailwind:** Tailwind CSS mặc định thiết lập `svg { display: block; }`, điều này làm vỡ các công thức inline của MathJax. Dự án khắc phục bằng cách thiết lập cẩn thận thuộc tính `display: inline !important` cho `mjx-container svg`.
- **Database Schema:** Chức năng lưu tiến độ học phụ thuộc vào bảng `student_lesson_progress`. Việc tự động thêm cột (`ALTER TABLE`) có thể gặp rủi ro nếu quyền Database không đủ. Đã bọc `try-catch` độc lập cho từng cột để tránh làm sập luồng.
- **AI Explain:** Đầu ra từ AI cần được loại bỏ markdown thô trước khi hiển thị. Frontend gọi `typesetMath()` sau khi chèn text vào bong bóng chat để đảm bảo công thức toán học được render đúng chuẩn. Bong bóng được gắn theo ngữ cảnh nút vừa bấm và người dùng có thể đóng bằng nút `x`.
- **AI Explain - điểm cần kiểm tra:** Nếu bong bóng vẫn hiện câu bị cụt, cần phân biệt hai nguyên nhân: CSS che mất nội dung hay Gemini trả response bị ngắt. Hiện frontend đã cho thân bong bóng cuộn dọc, backend đã thêm cơ chế nối tiếp khi câu trả lời chưa kết thúc bằng dấu câu.
- **Trạng thái lưu trữ:** Lỗi "Unknown column 'state_json'" (Error 500) đã được khắc phục hoàn toàn bằng bản vá auto-migrate an toàn.
- **Tiến trình học:** `syncLessonState` hiện cập nhật lại `state.progress` ở frontend sau khi API lưu thành công. Nhờ vậy thanh tiến trình, trạng thái bài, nhiệm vụ hằng ngày và bảng kỹ năng phản hồi ngay, không phụ thuộc hoàn toàn vào lần reload dữ liệu tiếp theo.
- **Tiến trình bài hiện tại:** Không dùng `score` làm đại diện duy nhất cho tiến trình học nữa. Frontend có `lessonCompletionPercent()` để tính tiến trình học theo hoạt động đã hoàn thành và `practiceProgress()` để tính tỷ lệ câu luyện tập đã làm.
- **Tiến độ chương:** `renderOverallProgress()` hiện lấy trung bình `lessonCompletionPercent()` của các bài đang hiển thị. Dòng phụ vẫn cho biết số bài đã học xong trên tổng số bài.
- **Trạng thái hoàn tất:** Trạng thái `mastered` trên UI được hiển thị là "Đã học xong" để phản hồi đúng hành động bấm nút "Đã học".
- **Kỹ năng của bài:** `renderSkills()` hiện hiển thị tối thiểu bằng `lessonCompletionPercent()`, nên học sinh đánh dấu đã học lý thuyết/ví dụ/toàn bài sẽ thấy thanh kỹ năng của bài thay đổi ngay, không đứng yên 0%.
- **Học lại:** Khi bài ở trạng thái `mastered`, nút hành động chuyển thành "Học lại". Nút này gọi `resetLesson()`, xóa tiến trình bài đó và đánh dấu lại trạng thái bắt đầu để học sinh học lại.
- **Theo dõi tiến độ cho giáo viên:** `admin-progress.js` chỉ mount vào `lessonDesignerMount` khi `localStorage.userRole === 'teacher'`; không mount vào admin dashboard. Nếu không có admin key, request API vẫn chạy bằng session giáo viên.
- **Theo dõi tiến độ theo lớp:** Tiến độ lưu theo từng học sinh trong `student_lesson_progress`; UI nhóm/lọc qua `users.class_name`. Panel có dropdown **Lớp** (`#progressClassFilter`), lọc trạng thái, tìm kiếm; thống kê tính theo phạm vi lớp đang chọn. Chọn "Tất cả lớp" → dòng tóm tắt mỗi lớp căn đúng cột bảng. Lựa chọn lớp lưu `localStorage.progress_class_filter`.
- **Phát hành bài cho học sinh:** API `lessons.php` chỉ trả bài `is_published` cho role `student`. Giáo viên soạn xong cần tick **Mở bài này cho học sinh** rồi Lưu; HS tải lại trang lộ trình mới thấy chương/bài mới.
- **Xóa / nhân bản bài:** Xóa bài là không hoàn tác — tiến độ HS của bài đó cũng bị xóa. Nhân bản tạo bài mới chưa mở cho HS; giáo viên chỉnh nội dung rồi bật phát hành khi sẵn sàng.
- **Chương học:** Tên chương lưu trên từng bài (`lessons.chapter`). Đổi tên hàng loạt qua `rename_chapter`; sửa một bài chỉ đổi chương của bài đó. Bản đồ chương phía HS nhóm theo giá trị `chapter` đang có.
- **Ôn tập & kế hoạch:** Ôn tập thông minh và kế hoạch tự học dùng chung tiến độ `state.progress`. Gợi ý ôn bài học xong lâu phụ thuộc `completedAt` trong progress — bài `mastered` thiếu ngày hoàn thành sẽ không vào danh sách ôn.
- **Streak/huy hiệu:** Chỉ lưu phía client (`localStorage`); chưa đồng bộ server — đổi máy/trình duyệt sẽ mất streak cũ. Streak tính theo ngày local máy người dùng (không UTC). `perfect_100` = điểm luyện tập 100, khác với hoàn thành bài bằng nút **Đã học**.
- **Kiến trúc UI học sinh (3 cột):** Trái = tiến độ + danh sách/bản đồ bài; giữa = nội dung bài; phải = kế hoạch tự học + động lực + kỹ năng + nhiệm vụ. Ba tính năng ôn tập thông minh, bản đồ chương, động lực học bổ sung cho kế hoạch tự học và điều hướng lộ trình dài.
- **Quy trình quản lý nhiều lớp (vd. Toán 6 có 3 lớp):** (1) Gắn `class_name` khi tạo/sửa HS trong admin; (2) Mở trang lộ trình tương ứng; (3) Chọn bài học + lớp; (4) Lọc "Cần luyện thêm" để xem HS cần hỗ trợ trong lớp đó.
- **Render công thức trong theo dõi tiến độ:** `admin-progress.js` có hàm `mathText()` và gọi `MathJax.typesetPromise()` sau khi render bảng. `index.html` và các trang lộ trình Toán nạp MathJax để công thức trong dữ liệu kỹ năng/cần lưu ý hiển thị đúng.
- **Bài luyện tập:** Trắc nghiệm đã có phản hồi đúng/sai sau khi chọn đáp án; thao tác nộp bài cập nhật điểm, kỹ năng và trạng thái (`in_progress`, `needs_practice`, `mastered`). Nút "Làm lại bài luyện" reset đáp án/điểm luyện tập về trạng thái đang học để học sinh có thể làm lại.
- **Cần phản biện sau sửa:** Xem checklist trong `plan.md` (mục *Cần người dùng phản biện lại trên giao diện*), gồm AI giải thích, tiến trình luyện tập, panel giáo viên theo lớp, ôn tập/bản đồ/động lực, tìm bài, phát hành bài mới, CRUD bài/chương, và **thi trực tuyến mobile/Zalo**.
- **Thi trực tuyến — đề trộn vs đề gốc:** HS chỉ thấy số câu 1…N theo thứ tự đã trộn; báo cáo GV/Excel luôn dùng số câu **đề gốc**. Không lưu `display_order` trên server — Excel quy đổi bằng đối chiếu nội dung câu trong `details_json`.
- **Thi trực tuyến — dữ liệu cũ:** Các lượt thi trước khi sửa có thể thiếu `student_name` (nộp từ Zalo); không khôi phục tự động — cần HS thi lại sau khi deploy bản mới.
- **Thi trực tuyến — khuyến nghị HS:** Nếu Zalo lỗi, mở link bằng Chrome/Safari (menu *Mở bằng trình duyệt*).

---
*Cập nhật lần cuối: 2026-06-20. File này đồng bộ trạng thái dự án khi chuyển môi trường làm việc.*
