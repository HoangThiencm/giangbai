# PLAN: Xây Dựng Hệ Thống Nghiên Cứu Bài Học (NCBH) Có Hỗ Trợ AI

## Hiện trạng
1. **Kiến trúc hệ thống hiện tại**:
   - Hệ thống web trợ lý giáo viên hiện có các phân hệ chuyên môn: `soankhbd.html` (soạn KHBD CV 5512), `xaydungphuluc.html` (Phụ lục 1, 2, 3), `duyetgiaoan.html` (thẩm định giáo án), `duyetde.html` (rà soát ma trận đề), `thitructuyen.html` (thi & chấm tự động).
   - Hệ thống quản lý API key cá nhân và Model tập trung tại `api/user_gemini_keys.php` (lưu CSDL bảng `users` các cột `gemini_keys`, `mistral_keys`), đồng bộ qua `localStorage` (`global_gemini_keys`, `global_mistral_keys`, `default_gemini_module`, `khbd_gemini_model`).
   - `index.html` có thanh điều hướng, khu vực công cụ `#mainToolsGrid` với các thẻ `tool-tile`, và hệ thống phân quyền giáo viên theo `allowed_pages` từ `api/me.php` và `global_config.json`.
   - Đã có sẵn các thư viện và chuẩn dữ liệu: `js/security-guard.js`, `access-control.js`, `js/khbd-standards.js` (Khung AI QĐ 2422, NLS CV 3456 & 2345), `js/khbd-yccd.js` (YCCĐ môn Toán THCS), `mistral-ocr-client.js` (quét PDF OCR bằng Mistral), PDF.js, Mammoth.js (đọc DOCX), docx.js + FileSaver (xuất Word).
2. **Vấn đề cần giải quyết**:
   - Hiện chưa có module chuyên sâu hỗ trợ tổ/nhóm chuyên môn thực hiện đầy đủ quy trình **Nghiên cứu bài học (NCBH)**.
   - Cần một phân hệ chuyên biệt `nghiencuubaihoc.html` hiện thực hóa triết lý: *Văn bản hướng dẫn → Yêu cầu chuyên môn → GV cần làm gì → HS cần làm gì → Cần quan sát gì → Minh chứng nào cần thu thập → Sản phẩm/hồ sơ nào cần hoàn thành*.
   - Hệ thống cần tách biệt 12 tác vụ AI chuyên sâu thay vì một prompt lớn, thiết kế KHBD 2 lớp (Lớp 1: KHBD chuẩn CV 5512, Lớp 2: Thông tin NCBH), lưu trữ nhật ký phát triển bài học từ Phiên bản 1 sang Phiên bản 2 dựa trên minh chứng thực tế, và cho phép xuất trọn bộ 13 sản phẩm hồ sơ NCBH.

## Phạm vi
1. **Mở tab / thẻ công cụ "Nghiên cứu bài học" trong `index.html`**:
   - Cập nhật biến `TOOL_PAGE_LINKS` bổ sung: `nghiencuubaihoc: 'nghiencuubaihoc.html'`.
   - Thêm khối thẻ `tool-tile--nghiencuubaihoc` vào `#mainToolsGrid` với nhãn *"Chu trình NCBH sư phạm"*, tiêu đề *"Nghiên cứu bài học AI"*, mô tả *"12 bước NCBH có hỗ trợ AI · KHBD 2 lớp · Phân tích minh chứng · Cải tiến bài học"*.
   - Cập nhật danh mục phân quyền trong `admin.html` để quản trị viên có thể bật/tắt quyền truy cập cho giáo viên.
2. **Xây dựng trang giao diện chuyên biệt `nghiencuubaihoc.html`**:
   - Giao diện hiện đại sử dụng TailwindCSS, FontAwesome 6, Google Fonts Plus Jakarta Sans, bảo mật với `js/security-guard.js` và `access-control.js`.
   - **Cấu trúc đồng bộ 6 khu vực cho mỗi bước**:
     1. Căn cứ (Văn bản pháp lý, hướng dẫn chuyên môn liên quan).
     2. AI phân tích (Nhận định dữ liệu từ SGK, giáo án, minh chứng).
     3. GV cần làm (Thao tác nghiệp vụ sư phạm cụ thể).
     4. HS dự kiến làm (Hành vi, tư duy, hoạt động học tập).
     5. Cần quan sát / thu thập (Tiêu chí và minh chứng cụ thể).
     6. Sản phẩm của bước (Dữ liệu ghi vào hồ sơ NCBH).
   - **Hiện thực hóa 12 bước quy trình**:
     - *Bước 1: Khởi tạo hồ sơ*: Khai báo thông tin (môn, lớp, bài, bộ SGK, số tiết, GV dạy minh họa, thành viên tổ NCBH, lớp thực nghiệm); nạp tệp SGK (bắt buộc PDF), giáo án hiện có (DOCX/PDF tùy chọn), phiếu học tập, tài liệu GV; AI kiểm tra tính đầy đủ của dữ liệu.
     - *Bước 2: Nghiên cứu văn bản và phân tích bài học*: Đọc văn bản trong Kho căn cứ + SGK + YCCĐ CTGDPT 2018. Phân tích YCCĐ, trọng tâm, kiến thức tiền đề, chuỗi nhiệm vụ SGK, sản phẩm học tập, điểm khó, lỗi HS có thể gặp, cơ hội năng lực phẩm chất, tích hợp NLS (CV 3456) & Khung AI (QĐ 2422). Đính kèm câu hỏi căn cứ: “Đề xuất này dựa trên căn cứ hoặc yêu cầu chuyên môn nào?”. Sản phẩm: *Phiếu phân tích bài học*.
     - *Bước 3: Đánh giá giáo án hiện có (nếu có giáo án)*: Đánh giá 8 khía cạnh chuyên môn, phân loại 4 mức: [Giữ nguyên], [Giữ nhưng bổ sung], [Cần điều chỉnh], [Nên thiết kế lại]. Chỉ rõ vấn đề, nguyên nhân, căn cứ và hướng sửa. Sản phẩm: *Báo cáo phân tích giáo án ban đầu*.
     - *Bước 4: Xác định vấn đề nghiên cứu*: AI gợi ý các câu hỏi nghiên cứu cụ thể, tập trung vào việc học của HS (tránh chung chung hình thức). GV chọn/chỉnh sửa hoặc tự nhập câu hỏi nghiên cứu. Đây là trục xuyên suốt toàn bộ quy trình. Sản phẩm: *Vấn đề/câu hỏi nghiên cứu chính thức*.
     - *Bước 5: Dự kiến quá trình học của HS*: Dự kiến chi tiết từng hoạt động: HS bắt đầu ra sao, các hướng suy nghĩ, phương án đúng/chưa hoàn chỉnh, sai lầm, bế tắc, sản phẩm dự kiến, dấu hiệu hiểu/chưa hiểu; gợi ý câu hỏi gợi mở, thời điểm can thiệp/không can thiệp, cách xử lý sai lầm. Sản phẩm: *Bảng dự kiến hoạt động và phản ứng của HS*.
     - *Bước 6: Xây dựng bài dạy minh họa (KHBD Phiên bản 1)*: Thiết kế 2 lớp cho mỗi hoạt động:
       + Lớp 1 (KHBD chính thức): Mục tiêu, Nội dung, Sản phẩm, Tổ chức thực hiện (Hoạt động GV - Hoạt động HS), Kiểm tra đánh giá.
       + Lớp 2 (Thông tin NCBH): Điều cần quan sát, Phản ứng HS dự kiến, Lỗi sai dự kiến, Câu hỏi gợi mở, Tình huống dự phòng, HS/nhóm cần chú ý, Minh chứng cần thu thập, Thời điểm GV can thiệp / không can thiệp.
       Lưu lại mọi quyết định duyệt/sửa/từ chối của GV. Sản phẩm: *KHBD minh họa - phiên bản 1*.
     - *Bước 7: Xây dựng kế hoạch quan sát và hồ sơ trước giờ dạy*: Tạo Phiếu quan sát HS (trọng tâm là "HS học như thế nào", không đánh giá GV dạy hay/dở), Phiếu dự giờ NCBH, Tiêu chí quan sát gắn liền với vấn đề nghiên cứu ở Bước 4, Phân công người quan sát, Nội dung họp chuẩn bị, Biên bản xây dựng bài học. Sản phẩm: *Bộ hồ sơ trước giờ dạy minh họa*.
     - *Bước 8: Dạy minh họa và thu thập minh chứng*: Giao diện nhập ghi chú quan sát thời gian thực trong giờ dạy (thời điểm, tình huống, phát biểu của HS, lỗi sai, hỗ trợ của GV, kết quả); upload ảnh chụp bài làm, sản phẩm HS, phiếu học tập. Gắn minh chứng với hoạt động, đối tượng HS và tiêu chí quan sát. Sản phẩm: *Kho minh chứng tiết dạy*.
     - *Bước 9: AI phân tích sau giờ dạy*: Đối chiếu **Dự kiến trước giờ dạy ↔ Thực tế xảy ra**: dự đoán nào đúng, điều gì ngoài dự đoán, HS bế tắc ở đâu, nguyên nhân, câu hỏi nào hiệu quả, can thiệp lúc nào sớm/muộn, phân biệt rõ ý kiến nhận xét cảm tính và minh chứng thực tế. Sản phẩm: *Báo cáo phân tích tiết dạy*.
     - *Bước 10: Thảo luận và xây dựng biên bản sau tiết dạy*: AI hỗ trợ nhóm ý kiến trùng lặp, chỉ ra ý kiến trái chiều, đối chiếu ý kiến với minh chứng thực tế, gợi ý nội dung thảo luận sâu, lập biên bản sinh hoạt chuyên môn trung thực dựa trên dữ liệu thực tế (không tự sinh nội dung hình thức "thống nhất cao" nếu thiếu dữ liệu). Sản phẩm: *Biên bản phân tích bài học sau tiết dạy*.
     - *Bước 11: Điều chỉnh bài học (KHBD Phiên bản 2)*: Cải tiến KHBD theo công thức: **Trước → Vấn đề → Minh chứng → Đề xuất sửa → Lý do sửa**. Sản phẩm: *KHBD minh họa - phiên bản 2*.
     - *Bước 12: Hoàn thiện hồ sơ NCBH*: Tổng hợp và cho phép xuất toàn bộ 13 sản phẩm/biểu mẫu, xuất file Word (.docx) từng biểu mẫu hoặc nén ZIP toàn bộ hồ sơ.
   - **Tách riêng 12 tác vụ AI**:
     1. Document Analyzer (đọc văn bản, SGK)
     2. Lesson Analyzer (phân tích bài học)
     3. Lesson Plan Reviewer (đánh giá giáo án)
     4. Research Question Advisor (gợi ý vấn đề nghiên cứu)
     5. Student Thinking Predictor (dự đoán suy nghĩ, lỗi sai HS)
     6. Lesson Adaptation Advisor (điều chỉnh KHBD 2 lớp)
     7. Observation Designer (xây công cụ quan sát)
     8. Evidence Analyzer (phân tích minh chứng)
     9. Discussion Assistant (hỗ trợ thảo luận)
     10. Minutes Generator (xây biên bản)
     11. Lesson Reviser (hoàn thiện bài dạy v2)
     12. Report Generator (tổng hợp hồ sơ)
   - **Nguyên tắc bắt buộc tuân thủ**:
     + Không tự suy diễn quy định; căn cứ minh bạch.
     + Phân biệt rõ: yêu cầu văn bản, khuyến nghị chuyên môn, đề xuất AI, quyết định GV.
     + AI chỉ đề xuất, GV quyết định; lưu nhật ký quyết định.
     + Không tạo biên bản giả mạo.
     + Không xếp loại giáo viên.
3. **Quản lý AI Keys & Models từ CSDL**:
   - Tự động đồng bộ khóa từ `api/user_gemini_keys.php` (lấy cả `keys` của Gemini và `mistral_keys` của Mistral AI).
   - Đọc model Gemini mặc định từ cấu hình người dùng (`localStorage.getItem('khbd_gemini_model')` hoặc `localStorage.getItem('default_gemini_module')`, fallback `gemini-2.5-flash`).
   - Tích hợp Mistral OCR thông qua `mistral-ocr-client.js` để đọc PDF SGK scan và Mistral Chat Completion dự phòng khi Gemini quá tải.
   - Có cơ chế xoay vòng key tự động, xử lý lỗi 429/503/Timeout.
4. **Kho căn cứ chuyên môn có sẵn**:
   - Tích hợp văn bản cốt lõi: Công văn 5512/BGDĐT-GDTrH, Thông tư 32/2018/TT-BGDĐT, Hướng dẫn sinh hoạt chuyên môn theo NCBH của Bộ GDĐT, Quyết định 2422/QĐ-BGDĐT (Khung năng lực AI), Công văn 3456/BGDĐT-CNTT & Công văn 2345/BGDĐT-GDTH (Khung năng lực số), Thông tư 38/2021 & TT 14/2020 (thiết bị & phòng bộ môn).
5. **Backend lưu trữ phiên làm việc `api/nghiencuubaihoc.php`**:
   - Tự động tạo bảng `nghien_cuu_bai_hoc_sessions` trên MySQL.
   - Cung cấp các action: `list`, `get by id`, `save` (create/update), `delete`.
   - Cơ chế tự động lưu (auto-save) và lưu cục bộ song song vào `localStorage` chống mất dữ liệu khi mất kết nối mạng.
6. **Bộ kiểm thử tự động `tests/nghiencuubaihoc-smoke.js`**:
   - Kiểm tra tích hợp trong `index.html` và `admin.html`.
   - Kiểm tra cấu trúc `nghiencuubaihoc.html` có đầy đủ 12 bước, 6 khu vực, 12 tác vụ AI, logic nạp key từ `api/user_gemini_keys.php`.
   - Kiểm tra tính hợp lệ của `api/nghiencuubaihoc.php`.

## Ngoài phạm vi
- Không can thiệp hoặc sửa đổi logic của các công cụ hiện có (`soankhbd.html`, `xaydungphuluc.html`, `duyetgiaoan.html`, `duyetde.html`).
- Không sửa đổi cấu hình Google Drive hoặc Cloudflare Workers đã hoạt động ổn định.
- Không tự động thay đổi cấu trúc bảng `users`.

## File dự kiến tác động
- `index.html` [SỬA: Thêm công cụ Nghiên cứu bài học vào `TOOL_PAGE_LINKS` và `#mainToolsGrid`]
- `admin.html` [SỬA: Bổ sung quyền trang `nghiencuubaihoc` vào danh mục công cụ]
- `api/nghiencuubaihoc.php` [TẠO MỚI: API quản lý dữ liệu phiên hồ sơ NCBH trên CSDL MySQL]
- `nghiencuubaihoc.html` [TẠO MỚI: Toàn bộ giao diện và logic 12 bước Nghiên cứu bài học có hỗ trợ AI]
- `tests/nghiencuubaihoc-smoke.js` [TẠO MỚI: Bộ kiểm thử smoke test tự động]
- `docs/handoff/PLAN.md` [GHI ĐÈ: Kế hoạch bàn giao cho Coder]
- `docs/handoff/.lock` [GHI MỚI: Đặt cờ khóa LOCK]

## Các bước thực hiện
1. **Bước 1: Tạo Backend API `api/nghiencuubaihoc.php`**:
   - Kiểm tra xác thực phiên người dùng (`$_SESSION['user_id']`).
   - Khởi tạo bảng MySQL `nghien_cuu_bai_hoc_sessions` (nếu chưa có):
     `id, user_id, mon_hoc, lop, bai_hoc, bo_sgk, gv_day, session_title, current_step, session_data (LONGTEXT), created_at, updated_at`.
   - Viết các handler:
     + `GET ?action=list`: Trả về danh sách hồ sơ của user.
     + `GET ?id=...`: Trả về toàn bộ chi tiết dữ liệu hồ sơ.
     + `POST`: Tạo mới hoặc cập nhật hồ sơ.
     + `POST ?action=delete`: Xóa hồ sơ.
2. **Bước 2: Cập nhật `index.html` và `admin.html`**:
   - Trong `index.html`:
     + Dòng 896: Thêm `nghiencuubaihoc: 'nghiencuubaihoc.html'` vào `TOOL_PAGE_LINKS`.
     + Thêm card công cụ Nghiên cứu bài học vào `#mainToolsGrid` ngay sau khối Duyệt giáo án / Xây dựng phụ lục:
       Icon `fa-users-rectangle`, tiêu đề *Nghiên cứu bài học*, mô tả chuẩn mực.
   - Trong `admin.html`:
     + Thêm `nghiencuubaihoc` vào danh mục quyền giảng dạy và cấu hình hiển thị công cụ.
3. **Bước 3: Xây dựng giao diện và logic `nghiencuubaihoc.html`**:
   - Tích hợp các thư viện: Tailwind CSS, FontAwesome 6, PDF.js, Mammoth.js, docx.js, FileSaver.js, `js/security-guard.js`, `access-control.js`, `mistral-ocr-client.js`.
   - Thiết kế thanh tiến trình 12 bước trực quan (Stepper Bar) cho phép chuyển bước mượt mà và lưu lại trạng thái đã hoàn thành.
   - Xây dựng 6 khu vực thống nhất trong từng bước: (1) Căn cứ chuyên môn; (2) AI phân tích; (3) GV cần làm; (4) HS dự kiến làm; (5) Cần quan sát/thu thập; (6) Sản phẩm của bước.
   - Triển khai 12 module AI chuyên biệt với các prompt được thiết kế riêng:
     + Module 1: Document Analyzer (Đọc văn bản, bóc tách SGK, đối chiếu YCCĐ).
     + Module 2: Lesson Analyzer (Phân tích trọng tâm, điểm khó, lỗi sai, cơ hội NLS/AI).
     + Module 3: Lesson Plan Reviewer (Đánh giá giáo án theo 4 mức độ: Giữ nguyên / Giữ nhưng bổ sung / Cần điều chỉnh / Nên thiết kế lại).
     + Module 4: Research Question Advisor (Đề xuất các câu hỏi nghiên cứu sư phạm sắc bén).
     + Module 5: Student Thinking Predictor (Dự đoán hành vi, phản ứng, khó khăn, câu hỏi gợi mở, thời điểm can thiệp).
     + Module 6: Lesson Adaptation Advisor (Sinh KHBD 2 lớp: Lớp 1 chuẩn CV 5512, Lớp 2 thông tin NCBH; quản lý quyết định của GV).
     + Module 7: Observation Designer (Thiết kế phiếu quan sát HS, phiếu dự giờ, tiêu chí tập trung vào việc học của HS).
     + Module 8: Evidence Analyzer (Ghi nhận biên bản thực địa, gắn ảnh/sản phẩm với tiêu chí và câu hỏi nghiên cứu).
     + Module 9: Discussion Assistant (Phân tích sau giờ dạy, đối chiếu Dự kiến ↔ Thực tế, nhận diện câu hỏi hiệu quả và thời điểm can thiệp).
     + Module 10: Minutes Generator (Tổng hợp ý kiến thảo luận, nhận diện đồng thuận/bất đồng, tạo biên bản sinh hoạt trung thực).
     + Module 11: Lesson Reviser (Đề xuất KHBD Phiên bản 2 theo cấu trúc: Trước → Vấn đề → Minh chứng → Đề xuất sửa → Lý do).
     + Module 12: Report Generator (Tổng hợp và xuất trọn bộ 13 sản phẩm hồ sơ NCBH).
   - Tích hợp gọi API Gemini & Mistral:
     + Đồng bộ API Key từ `api/user_gemini_keys.php` (Gemini & Mistral).
     + Đọc model từ khai báo của người dùng (`default_gemini_module` / `khbd_gemini_model`).
     + Mistral OCR đọc trực tiếp PDF SGK dạng scan khi cần.
     + Quay vòng key tự động, xử lý retry khi gặp lỗi 429 hoặc quá tải.
   - Triển khai tính năng Xuất Word (.docx):
     + Xuất lẻ từng sản phẩm trong 13 sản phẩm.
     + Xuất trọn bộ hồ sơ NCBH (tổng hợp đầy đủ minh chứng và biên bản).
4. **Bước 4: Xây dựng bài kiểm thử tự động `tests/nghiencuubaihoc-smoke.js`**:
   - Kiểm tra tích hợp trong `index.html` và `admin.html`.
   - Kiểm tra cấu trúc `nghiencuubaihoc.html` có đầy đủ 12 bước, 6 khu vực, 12 tác vụ AI, logic nạp key từ `api/user_gemini_keys.php`.
   - Kiểm tra tính hợp lệ của `api/nghiencuubaihoc.php`.
5. **Bước 5: Chạy toàn bộ kiểm thử**:
   - Chạy `node tests/nghiencuubaihoc-smoke.js`.
   - Chạy `node tests/run-all-tests.js` đảm bảo không phát sinh bất kỳ regression nào.

## Rủi ro
1. **Dữ liệu PDF SGK lớn làm tràn context của AI**:
   - *Giải pháp*: Tích hợp đọc tách trang theo nội dung bài học cụ thể, trích xuất văn bản tinh gọn (compact context) hoặc dùng Mistral OCR quét các trang trọng tâm của bài.
2. **Mất dữ liệu trong quá trình thực hiện 12 bước**:
   - *Giải pháp*: Triển khai cơ chế lưu kép: tự động lưu lên CSDL MySQL thông qua `api/nghiencuubaihoc.php` sau mỗi thao tác quan trọng, đồng thời lưu đệm vào `localStorage` của trình duyệt.
3. **Lỗi hạn ngạch (429 Rate Limit) hoặc mạng chập chờn khi gọi AI**:
   - *Giải pháp*: Tự động quay vòng toàn bộ danh sách Gemini API Key đã lưu trong CSDL của người dùng; fallback linh hoạt sang model phụ (`gemini-2.5-flash`) hoặc Mistral AI.

## Cách kiểm thử
1. **Kiểm thử tự động (Automated Smoke Test)**:
   ```powershell
   node tests/nghiencuubaihoc-smoke.js
   node tests/run-all-tests.js
   ```
2. **Kiểm thử thủ công (Manual Verification)**:
   - Mở `index.html`: Xác nhận xuất hiện thẻ "Nghiên cứu bài học" trong danh mục công cụ giảng dạy, click mở chuyển đúng sang `nghiencuubaihoc.html`.
   - Trên `nghiencuubaihoc.html`:
     + Kiểm tra trạng thái nạp API key từ CSDL hiển thị đúng số lượng Gemini & Mistral Key.
     + Điền thông tin Bước 1 (Toán 6, bài học cụ thể), nạp tệp SGK/giáo án mẫu.
     + Chạy thử phân tích bài học (Bước 2), đánh giá giáo án (Bước 3), đề xuất câu hỏi nghiên cứu (Bước 4).
     + Kiểm tra giao diện 2 lớp của KHBD (Bước 6) và bảng dự kiến học sinh (Bước 5).
     + Nhập ghi chú và thử tải ảnh minh chứng ở Bước 8.
     + Xem phân tích đối chiếu ở Bước 9, thảo luận ở Bước 10 và phiên bản KHBD 2 ở Bước 11.
     + Bấm nút xuất Word (.docx) ở Bước 12 để kiểm tra tệp đầu ra.
     + Bấm "Lưu CSDL" và "Mở hồ sơ cũ" để kiểm tra tải lại toàn bộ tiến trình.

## Tiêu chí nghiệm thu
1. `index.html` có thẻ công cụ "Nghiên cứu bài học" trỏ đến `nghiencuubaihoc.html` và hiển thị đồng bộ với hệ thống.
2. `admin.html` có tùy chọn cấp quyền và hiển thị trang `nghiencuubaihoc`.
3. `api/nghiencuubaihoc.php` hoạt động trơn tru: tự tạo bảng `nghien_cuu_bai_hoc_sessions`, lưu và khôi phục toàn vẹn dữ liệu hồ sơ.
4. `nghiencuubaihoc.html` hiện thực hóa đầy đủ 12 bước NCBH, cấu trúc 6 khu vực thống nhất, 12 tác vụ AI chuyên biệt, mô hình KHBD 2 lớp, lưu trữ nhật ký phát triển bài học.
5. Tích hợp đọc API key (Gemini & Mistral) từ CSDL qua `api/user_gemini_keys.php` và đọc model được người dùng chọn.
6. Hỗ trợ xuất file Word (.docx) chuẩn thể thức cho các sản phẩm hồ sơ NCBH.
7. File kiểm thử `tests/nghiencuubaihoc-smoke.js` chạy PASS 100%.
8. File handoff `docs/handoff/PLAN.md` và `docs/handoff/.lock` được ghi nhận đầy đủ.