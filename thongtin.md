# Thông tin dự án

## Cấu trúc hiện tại của dự án
Dự án được xây dựng dựa trên stack: HTML, CSS (Tailwind), JS thuần ở phía Frontend và PHP (PDO) + MySQL ở phía Backend.

### Các file và chức năng chính
1. **Giao diện bài học (`lotrinhtoan6.html`, `lotrinhtoan7.html`, `lotrinhtoan8.html`, `lotrinhtoan9.html`)**
   - Chứa cấu trúc HTML cho lộ trình học môn Toán các lớp; mỗi trang đặt `window.LOTRINH_SUBJECT` và `window.LOTRINH_PAGE_TITLE` (UTF-8 đúng).
   - Layout học sinh: cột trái (tiến độ + danh sách/bản đồ bài), cột giữa (nội dung bài), cột phải (kế hoạch tự học, động lực, kỹ năng, nhiệm vụ).
   - Định dạng CSS nội bộ (`<style>`) giúp render MathJax SVG và bong bóng chat AI giải thích.
   - Đã thêm style `.ai-chat-bubble` đồng bộ cho cả Toán 6, 7, 8, 9; bong bóng có nút `x`, mũi nhọn chat, và không bị cắt nội dung.
   - Cache script gần nhất: `access-control.js?v=20260619-teacher-scope1`, `lotrinh.js?v=20260619-drag-fill1`, `admin-lesson-manager.js?v=20260619-teacher-scope1`, `admin-progress.js?v=20260619-teacher-class1` (trên `lotrinhtoan6–9.html` và `index.html`).

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
   - **Bài tập kéo vào ô trống** (`renderFillExercises`): HS kéo chip từ pool vào ô trống trong đề; chấm sau khi nộp luyện tập. Soạn bài qua textarea *Điền khuyết* trong panel GV (`parseFillExercises` / `formatFillExercises`).
   - **Bài tập nối ô** (`renderDragExercises`, `mode: match`): bấm mục trái rồi phải để ghép cặp; có chế độ sắp xếp thứ tự (`mode: sort`). Parser GV: `câu hỏi | trái > … | phải > … | 0-1,1-0` (cặp chỉ số).

3. **Soạn bài giáo viên (`admin-lesson-manager.js`)**
   - Mount `#lessonDesignerMount` khi `userRole === 'teacher'`.
   - Chỉ hiển thị/soạn môn nằm trong `allowedPages` (tick **Lộ trình được phép soạn** khi admin tạo/sửa GV). Request API dùng `credentials: 'include'` (session PHP).
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
   - GV chỉ xem HS thuộc **lớp phụ trách** (`userClassName` từ `login.html`); dropdown lớp khóa khi chỉ có một lớp. API `admin_progress.php` cũng lọc theo lớp/môn được cấp.
   - Gọi `api/admin_progress.php`; nhóm bảng theo lớp khi xem "Tất cả lớp" (mỗi cột `<td>` thẳng header).
   - Trên trang lộ trình: lọc dropdown bài học theo `LOTRINH_SUBJECT`.
   - Trang `thongketientrinh.html` có nút **Xuất Excel** theo lớp/bài/môn đang lọc; file gồm sheet bài hiện tại và sheet tổng hợp lớp theo các bài.
   - Giáo viên tự đặt **ngưỡng điểm yếu** (0–100) và mốc **chưa vào học** (3/7/14/30 ngày). Hai điều kiện trở thành bộ lọc bảng và xuất hiện trong khối **Việc cần xử lý hôm nay** cùng học sinh chưa bắt đầu bài.
   - Mỗi dòng báo cáo và file Excel hiển thị lần vào học gần nhất, số ngày chưa vào học, điểm, tiến trình và nội dung cần lưu ý.

5. **Backend API (`api/`)**
   - `lessons.php`: Lấy danh sách bài học; **lưu tiến độ** HS (`save_progress`, `reset_progress`); **soạn bài** GV (`save_content` theo `id`/slug, `delete_lesson`, `duplicate_lesson`, `rename_chapter`) — server chặn nếu GV không có quyền môn (`require_lesson_manager`). Auto-migrate schema (`ensure_lesson_schema`, `ensure_progress_schema`) dùng try-catch riêng từng cột.
   - `admin_progress.php`: Trả dữ liệu theo dõi tiến độ học sinh theo `lesson_id`. GV chỉ nhận bài thuộc môn được cấp và HS thuộc lớp phụ trách; thiếu lớp phụ trách → lỗi 403. Mỗi row gồm `class_name` (từ `users.class_name`); response thêm mảng `classes`. Cho phép session giáo viên đang hoạt động.
   - `admin_students.php`: Tạo/sửa/xóa HS/GV kèm `class_name`, `allowed_pages`, `expires_at`, `expires_option`. GV bắt buộc có lớp phụ trách. Action `import_batch`: import hàng loạt từ Excel.
   - `login.php`: Chặn đăng nhập nếu `expires_at` đã qua.
   - `global_config.php`: Lưu/đọc cấu hình hệ thống trên hosting (`global_config.json`) — Gemini keys, ShopAIKey, GitHub PAT, v.v.
   - `ai_explain.php`: Ưu tiên **Cloudflare Workers AI** qua Worker stateless (`cloudflare-worker/worker.js`): PHP xác thực request và gửi ngữ cảnh bài học, Worker tạo system prompt rồi gọi Workers AI. Worker lỗi/quá quota thì PHP fallback Gemini, rồi ShopAIKey (`https://api.shopaikey.com/v1/chat/completions`, mặc định model `deepseek-v4-flash`). Worker URL và secret chỉ đặt trong `api/config.php` trên hosting, không lưu vào `global_config.json` hay JavaScript. **Mỗi lượt gọi** (thành công/lỗi/fallback) được ghi log qua `ai_usage_log.php` → `data/ai_usage.json`.
   - `ai_usage_log.php`: Ghi/đọc log sử dụng AI lộ trình — provider, mode (`explain`/`chat`), model, token, USD ước tính (ShopAIKey), lịch sử 90 ngày + 120 lượt gần nhất.
   - `ai_stats.php`: API thống kê cho admin (`require_admin_key`). Tổng hợp log nội bộ; gọi ShopAIKey `/v1/dashboard/billing/subscription` + `/usage` (Đã dùng $ / Còn lại $); tùy chọn Cloudflare GraphQL `workersInvocationsAdaptive` khi có `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_WORKER_SCRIPT_NAME` trong `api/config.php`.
   - `helpers.php`: Tiện ích chung (`respond()`, `column_exists()`, `lotrinh_page_subjects()`, `teacher_allowed_subjects()`, `teacher_managed_classes()`, `require_lesson_manager()`, `resolve_account_expiry()`, `ensure_users_expires_option_column()`).

6. **Quản trị tài khoản (`admin.html`)**
   - Đăng nhập bằng **Admin Key** (ô che ký tự bằng CSS, `autocomplete="off"` — tránh trình duyệt hỏi lưu mật khẩu); quản lý tài khoản HS/GV trên MySQL (`api/admin_students.php`). Sau `loadUsers` hosting tự gọi `loadGlobalConfig()`.
   - **Tab admin**: Tạo tài khoản · THCS Trần Phú · **Theo dõi AI** · Cài đặt hệ thống.
   - **Tab Theo dõi AI**: đọc `api/ai_stats.php` — hiển thị lượt AI lộ trình hôm nay/14 ngày, Cloudflare (Worker/ngày từ GraphQL + log nội bộ), Gemini fallback (log), ShopAIKey (USD đã dùng/còn lại từ API + lượt fallback từ log); bảng lượt gọi gần đây; link dashboard CF / AI Studio / ShopAIKey.
   - **Phân quyền giáo viên**: vai trò **Giáo viên** + tick **Lộ trình được phép soạn** (`lotrinhtoan6–9`) + **Lớp phụ trách** (bắt buộc). Không có checkbox riêng “được soạn bài” — quyền soạn = `role=teacher` + lộ trình được tick.
   - **Lớp phụ trách**: dropdown từ danh sách lớp HS đã có (`studentClassCatalog()`); tùy chọn *+ Nhập lớp mới…*. Hỗ trợ nhiều lớp qua dấu phẩy (vd. `6A,6B`). Tên lớp phải trùng `Lớp/Nhóm` của HS.
   - **Thời hạn tài khoản**: gói Không giới hạn / 1 tháng / 3 tháng / 9 tháng / 1 năm (`expires_option` + `expires_at`); cột bảng hiển thị ngày hết hạn.
   - **Cấu hình AI**: Cloudflare Worker URL và `APP_SHARED_SECRET` nằm trong `api/config.php` server-side. Tùy chọn thêm `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_WORKER_SCRIPT_NAME` để tab **Theo dõi AI** lấy lượt Worker/ngày từ Cloudflare GraphQL (badge **GraphQL OK**). Admin chọn nhanh hoặc tự nhập model cho Cloudflare Workers AI (`@cf/...`), Gemini và DeepSeek/ShopAIKey; PHP gửi model Cloudflare đã chọn cho Worker, Worker chỉ chấp nhận model ID hợp lệ dạng `@cf/...`. Gemini và DeepSeek/ShopAIKey có công tắc độc lập; khi tắt provider, key vẫn được giữ trong `global_config.json` nhưng backend bỏ qua provider đó — dùng để kiểm thử Worker độc lập.
   - **Tạo từng tài khoản**: form Cấp tài khoản (vai trò, tài khoản, mật khẩu, họ tên, lớp/lớp phụ trách, trang/lộ trình được mở, thời hạn).
   - **Import Excel hàng loạt** (panel *Import danh sách học sinh từ Excel*):
     - File mẫu: `templates/DanhSachHocSinh_Mau.xlsx` (tải từ repo hoặc nút **Tạo file mẫu mới** trên trang).
     - Cột Excel: `STT | Tài khoản | Mật khẩu | Họ và tên | Lớp/Nhóm` — **bắt buộc** Tài khoản + Họ và tên.
     - Mật khẩu/Lớp để trống → dùng **mật khẩu mặc định** / **lớp mặc định** trên màn hình import.
     - Chọn trang mở (checkbox giống form tạo tài khoản); tài khoản trùng → **cập nhật** thông tin.
     - Frontend đọc `.xlsx/.xls/.csv` bằng SheetJS; gửi `action: import_batch` lên API.
   - **Lên lớp hàng loạt**: chuyển HS từ lộ trình Toán 6→7, 7→8, 8→9 (cập nhật `allowed_pages` + `class_name`).

7. **Thi trực tuyến (`thitructuyen.html`)**
   - Frontend React (CDN). **Dữ liệu đề thi & kết quả** lưu MySQL trên hosting qua `api/exam.php` (`EXAM_API` tự trỏ cùng domain). **AI soạn đề** (quét PDF, nhận diện câu hỏi) vẫn gọi HuggingFace: `AI_API` mặc định `https://hoangthiencm-giangbai.hf.space` (ghi đè `localStorage.omr_backend_url`).
   - **Giáo viên**: soạn đề (PDF/Word + AI), lưu kho đề, xem QR/link chia sẻ, xem kết quả, xuất Excel.
   - **Chế độ thí sinh** (GV chọn khi lưu đề, lưu trong `variants_json` meta):
     - **Thí sinh tự do** (`student_mode: free`): HS tự nhập Họ tên, SBD, Lớp — mặc định; đề cũ không có meta cũng dùng chế độ này.
     - **Danh sách từ lớp** (`student_mode: class`): GV chọn lớp từ `users.class_name` (cùng nguồn admin/import Excel) → API `student-classes` / `class-students` lấy roster; snapshot `roster` lưu khi Lưu đề (SBD = `username`). Kho đề hiển thị cột **Thí sinh** (vd. `Lớp 6A (32 HS)`).
     - Khi nộp bài chế độ lớp: server kiểm tra tên+SBD có trong `roster` của đề.
   - **Học sinh**: mở link `?mode=student&examId=...` (không cần đăng nhập — `access-control.js` bỏ qua khi có `examId`). Chế độ lớp: ô tìm tên/SBD + dropdown chọn đúng tên trong danh sách; SBD và lớp tự điền.
   - **Trộn đề**: khi HS làm bài, thứ tự câu và đáp án trộn trên UI; đáp án nộp lên server dùng `originalIdx` / `originalOptIdx` (theo **đề gốc**). Chấm điểm và `details_json` (câu sai) cũng theo đề gốc.
   - **Nộp bài mobile/Zalo** (`StudentView`):
     - `isMobileExamClient()` nhận diện điện thoại / Zalo / in-app browser → **tắt** chống gian lận toàn màn hình và khóa màn hình.
     - `persistInfo()` + `sessionStorage` key `exam_student_info_{examId}` — giữ Họ tên/SBD khi nộp (fix mất tên do bàn phím tiếng Việt).
     - `formatApiError()` — không còn alert `[object Object]`; luôn gửi `student_class` (có thể rỗng).
     - Modal xác nhận nộp trên mobile; `ref` cho đáp án/tên khi hết giờ tự nộp.
   - **Kết quả GV** (`ResultDetail`): bảng chi tiết + khối **Học sinh thi nhiều lần** (gom theo SBD+tên); **Xuất Excel** một sheet: `STT | Họ và tên | Số báo danh | Lớp học | Điểm | Kết quả | Các câu đúng (đề gốc) | Các câu sai (đề gốc)` — đối chiếu `details_json` với `api/exam/get/{id}` để ra số câu đề gốc.
   - **Xóa kết quả HS** (`ResultDetail`): cột **Thao tác** — nút thùng rác xóa từng lượt thi (có xác nhận); nút **Xóa N bản ghi test** (SBD bắt đầu `TEST` hoặc tên `Test...`). API hosting: `api/exam.php?route=result/{id}` (DELETE), `route=results/delete-batch` (POST).
   - **Bảng MySQL**: `exams`, `exam_submissions` (trong `database_schema.sql`; `api/exam.php` tự tạo bảng nếu chưa có).
   - **QRModal**: hiển thị mã QR + ô link + nút **Copy** (clipboard / fallback) để GV gửi Zalo.

## Vấn đề cần lưu ý (Notes)
- **MathJax & Tailwind:** Tailwind CSS mặc định thiết lập `svg { display: block; }`, điều này làm vỡ các công thức inline của MathJax. Dự án khắc phục bằng cách thiết lập cẩn thận thuộc tính `display: inline !important` cho `mjx-container svg`.
- **Database Schema:** Chức năng lưu tiến độ học phụ thuộc vào bảng `student_lesson_progress`. Việc tự động thêm cột (`ALTER TABLE`) có thể gặp rủi ro nếu quyền Database không đủ. Đã bọc `try-catch` độc lập cho từng cột để tránh làm sập luồng.
- **AI Explain:** Luồng trả lời là **Cloudflare Workers AI → Gemini → ShopAIKey**. Worker không lưu lịch sử/D1/KV/RAG; ngữ cảnh bài hiện tại và vài lượt chat gần nhất được gửi theo request rồi bỏ đi. Đầu ra từ AI cần được loại bỏ markdown thô trước khi hiển thị. Frontend gọi `typesetMath()` sau khi chèn text vào bong bóng chat để đảm bảo công thức toán học được render đúng chuẩn. Bong bóng được gắn theo ngữ cảnh nút vừa bấm và người dùng có thể đóng bằng nút `x`.
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
- **Thi trực tuyến — danh sách lớp:** Lớp phải có HS hoạt động trong admin (`class_name` không rỗng). Đổi danh sách HS sau khi lưu đề **không** tự cập nhật đề đã lưu — GV cần mở sửa đề, chọn lại lớp và Lưu nếu muốn đồng bộ roster mới.
- **Phân quyền GV soạn bài:** Admin tick lộ trình Toán 6/7/8/9 trong form tài khoản GV. `access-control.js` chặn GV mở lộ trình chưa được cấp. `api/lessons.php` enforce môn khi lưu/xóa/nhân bản/đổi tên chương. GV báo “không có quyền” thường do session hết hạn hoặc chưa tick lộ trình — cần **đăng xuất → đăng nhập lại** sau khi admin lưu.
- **Lớp phụ trách GV:** Trường `class_name` của GV = lớp phụ trách (vd. `6A`). Nhiều lớp: `6A,6B`. Panel tiến độ và API chỉ trả HS thuộc lớp đó. Chưa có HS xếp lớp → dropdown trống; cần import/tạo HS trước hoặc chọn *Nhập lớp mới*.
- **Thời hạn tài khoản:** `expires_at` + `expires_option`; `login.php` chặn tài khoản hết hạn. Đổi gói thời hạn khi sửa sẽ tính lại từ hôm nay (trừ khi giữ nguyên gói đang dùng).
- **Cấu hình AI trên hosting:** Key Gemini/ShopAIKey lưu trong `global_config.json` trên server. File trong repo có thể **không có** `gemini_keys` — form admin trống là đúng nếu chưa lưu trên hosting. Banner admin cho biết trạng thái tải/lưu.
- **Theo dõi lượt sử dụng AI (đã cấu hình):** Tab **Theo dõi AI** trên `admin.html` đọc `api/ai_stats.php` thành công khi hosting có quyền ghi `data/ai_usage.json` và key ShopAIKey hợp lệ. **ShopAIKey**: API billing trả **Đã dùng $** / **Còn lại $** (khớp dashboard shopaikey.com). **Cloudflare**: nếu đã điền token GraphQL → hiện lượt Worker hôm nay (**GraphQL OK**); luôn có thêm cột **Lộ trình hôm nay (log)** từ `ai_explain.php`. **Gemini**: chỉ thống kê lượt **fallback** qua server (không có API quota còn lại theo ngày). **Phạm vi log:** chỉ `api/ai_explain.php` (AI lộ trình); vẽ hình, smartquiz, game… gọi Gemini trực tiếp từ trình duyệt **không** vào `data/ai_usage.json`.
- **Quy trình admin cấp GV:** (1) Vai trò Giáo viên → (2) Tick lộ trình được phép soạn → (3) Chọn lớp phụ trách → (4) Chọn thời hạn → (5) GV đăng xuất/đăng nhập lại → (6) Vào `lotrinhtoan6.html` (hoặc lộ trình tương ứng).
- **Bảo mật:** `global_config.json` trong repo có thể chứa GitHub PAT plaintext — nên rotate token, không commit secret.

---
*Cập nhật lần cuối: 2026-06-21. File này đồng bộ trạng thái dự án khi chuyển môi trường làm việc.*
