# PLAN

## Hiện trạng
- Đã khảo sát mã nguồn `soankhbd.html`, `js/khbd-standards.js`, `js/khbd-gemini.js`, `js/khbd-prompts.js`, `duyetgiaoan.html` và `giaoantichhop.html`.
- Trong `soankhbd.html`:
  + Tích hợp Khung Năng lực Số (TT 02/2025/TT-BGDĐT & CV 3456/BGDĐT-GDPT, 5 miền nền tảng, dải lớp 6–7 và 8–9) và Khung Năng lực AI (QĐ 2422/QĐ-BGDĐT, 4 miền A–D, phân bổ YCCĐ chuẩn xác theo lớp 6, 7, 8, 9).
  + Tích hợp vào 2 cấp độ: (1) Mục I. Mục tiêu: bổ sung c) Năng lực số và d) Năng lực AI, bảo toàn nguyên vẹn năng lực chung và đặc thù; (2) Mục III. Hoạt động cụ thể: tích hợp thực chiến 1–2 điểm then chốt theo 3 dạng kịch bản chuẩn (kiểm chứng phản hồi AI có lỗi sai ngộ nhận, prompting gợi mở bước giải, thao tác công cụ số/phần mềm chuyên dụng như GeoGebra/bảng tính), gắn marker chuẩn `[AI: ...]` và `[NLS: ...]`, kèm Bảng tổng hợp tích hợp cuối bài.
  + Cơ chế gọi AI: Dùng `GeminiAPIManager` với danh sách model, xoay vòng key, cơ chế fallback tự động từ model cao sang model nhẹ hơn (`gemini-2.5-flash`).
  + Tuy nhiên, `soankhbd.html` yêu cầu đăng nhập tài khoản hệ thống (`authToken`, `access-control.js`, `api/user_gemini_keys.php`).
- Trong `giaoantichhop.html` hiện tại:
  + Công cụ cũ phụ thuộc vào việc sao chép prompt ra ngoài chat Gemini thủ công rồi dán ngược về, dẫn đến kết quả trả về không chuẩn xác, thiếu đồng nhất, hay bị mất định dạng.
  + Chưa có tính năng tải tệp giáo án lên (PDF/Word), chưa có gọi API Gemini trực tiếp, chưa có giao diện nhập và quản lý API key cá nhân của giáo viên.
  + Đã có sẵn bộ render KaTeX và xuất Word Equation OMML (`<m:oMath>`, `<m:oMathPara>`) rất chuẩn xác.

## Phạm vi
1. Nâng cấp toàn diện giao diện `giaoantichhop.html` (và cung cấp alias `tichhopgiaoan.html`) theo phong cách hiện đại, chuyên nghiệp, responsive (Tailwind CSS, Lucide icons, Inter font, chuẩn giấy in A4).
2. Chế độ công khai hoàn toàn: Không yêu cầu đăng nhập, không kiểm tra `authToken`, không gọi `access-control.js`.
3. Khu vực quản lý API Key Gemini cá nhân:
   - Thiết kế modal/panel nhập một hoặc nhiều Gemini API key (hỗ trợ xoay vòng key).
   - Nút kiểm tra tính hợp lệ của key (Test API Key).
   - Lưu trữ an toàn cục bộ trong `localStorage` trình duyệt của giáo viên (tuyệt đối không gửi về server trung gian).
   - Hướng dẫn nhanh cách lấy key miễn phí từ Google AI Studio (`aistudio.google.com`).
   - Che mờ dạng password (`••••••••`), có nút xóa key khi cần dọn dẹp trên máy dùng chung.
4. Khu vực tải lên và trích xuất tệp giáo án:
   - Vùng kéo thả (dropzone) trực quan, hỗ trợ các định dạng: `.docx`, `.pdf`, `.txt`, `.md`.
   - Sử dụng thư viện client-side `mammoth.browser.min.js` để đọc file DOCX và `pdf.js` để đọc file PDF.
   - Hiển thị thông tin tệp (tên, dung lượng) và cho phép xem, chỉnh sửa nội dung văn bản giáo án gốc trước khi gửi AI.
5. Khu vực lựa chọn chuẩn NLS & AI:
   - Tận dụng cơ sở dữ liệu và thuật toán từ `js/khbd-standards.js` (đã có sẵn trong repo).
   - Cho phép chọn/nhận diện: Môn học, Khối lớp (6–9), Tên bài dạy, Thời lượng tiết.
   - Bật/tắt Khung NLS (TT 02 / CV 3456) và Khung AI (QĐ 2422) kèm nút "⚡ Gợi ý tự động" thông minh theo môn và khối lớp.
6. Module gọi AI trực tiếp phía Client (Xử lý 100% tự động qua API, loại bỏ luồng copy chat thủ công):
   - Model mặc định/ưu tiên: `gemini-3.8-flash`.
   - Cơ chế Fallback thông minh: Tự động chuyển về `gemini-2.5-flash` khi gặp lỗi quá tải (503), lỗi hạn ngạch (429) hoặc model không khả dụng.
   - Hỗ trợ xoay vòng key tự động nếu người dùng nhập nhiều key.
   - Hiển thị thanh tiến trình (progress bar) và thông báo Toast trạng thái rõ ràng.
7. Tích hợp chuẩn xác vào Kế hoạch bài dạy theo đúng chuẩn `soankhbd`:
   - Tích hợp vào Mục I (Mục tiêu): Bảo toàn a/b, bổ sung c) Năng lực số và d) Năng lực AI với mã chuẩn.
   - Tích hợp vào Mục III (Tiến trình dạy học): Tích hợp thực chiến tại hoạt động thích hợp theo 3 dạng kịch bản chuẩn, gắn marker `[AI: ...]` (màu tím) và `[NLS: ...]` (màu xanh lá).
   - Bổ sung Bảng tổng hợp tích hợp ở cuối bài dạy.
8. Khu vực kết quả & Xuất bản:
   - Xem trước trang in A4 chuẩn thể thức: KaTeX toán học sắc nét, bảng biểu chuẩn CV 5512.
   - Nút xuất file Word `.doc` (hỗ trợ công thức Microsoft Word Equation OMML chỉnh sửa được 100%) và tùy chọn xuất `.docx`.
   - Nút sao chép toàn văn Markdown.

## Ngoài phạm vi
- Loại bỏ hoàn toàn phương thức sao chép prompt ra ngoài chat Gemini thủ công (tập trung 100% xử lý tự động qua Gemini API trực tiếp trong app).
- Tuyệt đối không chỉnh sửa `soankhbd.html`, `js/khbd-app.js`, `js/khbd-prompts.js`, `js/khbd-gemini.js` hay bất kỳ tệp nào của phân hệ soạn bài chính.
- Không tạo backend PHP mới hoặc lưu dữ liệu giáo án/key lên máy chủ (hoạt động 100% phía client).
- Không yêu cầu đăng nhập tài khoản hệ thống (`login.html`).

## File dự kiến tác động
- `giaoantichhop.html`: Mã nguồn chính của công cụ, được tái cấu trúc và bổ sung tính năng hoàn chỉnh.
- `tichhopgiaoan.html`: File alias/đồng bộ với `giaoantichhop.html` để đảm bảo người dùng truy cập theo đường dẫn nào cũng sử dụng đúng phiên bản.

## Các bước thực hiện
### Bước 1: Nạp các thư viện cần thiết trong `giaoantichhop.html`
- Bổ sung CDN `mammoth.browser.min.js` (đọc file Word DOCX).
- Bổ sung CDN `pdf.js` và cấu hình worker (đọc file PDF).
- Giữ vững CDN `katex.min.js`, `auto-render.min.js`, `FileSaver.min.js`, `Tailwind CSS`, `lucide` icons.
- Nhúng `js/khbd-standards.js` để dùng danh mục chuẩn NLS và AI.
- Đảm bảo không nhúng `access-control.js` hoặc bất kỳ script kiểm tra `authToken` nào.

### Bước 2: Thiết kế giao diện chuyên nghiệp và hiện đại
- Header chuyên nghiệp: Logo, tiêu đề "Hệ thống Tích hợp Năng lực Số & AI vào Kế hoạch Bài dạy", nhãn "Công khai · Không cần tài khoản", nút "🔑 Quản lý API Key (N keys)", nút "Nạp giáo án mẫu", nút "Làm mới".
- Modal Quản lý API Key:
  + Textarea nhập danh sách API key (mỗi dòng một key), hỗ trợ hiển thị/ẩn masking bảo mật.
  + Nút "Kiểm tra Key" (test gọi thử prompt ngắn tới API).
  + Nút "Lưu Key" (lưu vào `localStorage`).
  + Nút "Xóa Key" (dọn dẹp dữ liệu khi dùng máy tính công cộng).
  + Nút "Nhập file .txt" để nạp nhanh danh sách key.
  + Hướng dẫn ngắn cách lấy key miễn phí trong 1 phút tại Google AI Studio.
- Cột bên trái: Cấu hình & Nạp dữ liệu
  + Vùng tải tệp thông minh (Dropzone): Kéo thả hoặc duyệt file `.docx`, `.pdf`, `.txt`, `.md`.
  + Trích xuất nội dung văn bản tự động và hiển thị trong textarea (cho phép xem, sửa).
  + Khối thông tin bài dạy: Môn học, Khối lớp (6, 7, 8, 9), Tên bài dạy, Thời lượng (tiết), Giáo viên.
  + Khối tích hợp NLS & AI:
    * Checkbox Năng lực số (TT 02 / CV 3456) + Nút "⚡ Gợi ý tự động" + Danh mục mã NLS theo lớp.
    * Checkbox Năng lực AI (QĐ 2422) + Nút "⚡ Gợi ý tự động" + Danh mục mã AI theo lớp.
  + Nút hành động nổi bật: "⚡ BẮT ĐẦU TÍCH HỢP BẰNG AI (Gemini 3.8)".
  + Thanh tiến trình thời gian thực (Progress bar).
- Cột bên phải: Xem trước & Xuất bản
  + Vùng xem trước chuẩn khổ giấy A4: Times New Roman 13pt, căn đều, công thức toán KaTeX, định dạng màu NLS (xanh lá `#16a34a`) và AI (tím `#9333ea`), bảng biểu rõ ràng.
  + Nút "Xuất file Word (.doc OMML)" và nút "Xuất file Word (.docx)".
  + Nút "Sao chép Markdown".

### Bước 3: Xây dựng Module Client-side Gemini với Fallback 3.8 sang 2.5
- Viết module gọi API `GeminiAPIHandler`:
  + Quản lý danh sách keys từ `localStorage.getItem('tichhop_gemini_keys')`.
  + Hàm `callGemini(promptText, options)`:
    * Thử gọi trước với model `gemini-3.8-flash`.
    * Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}`.
    * Nếu model `gemini-3.8-flash` báo lỗi 404/400/503 hoặc 429 Quota Exceeded, tự động chuyển sang gọi model `gemini-2.5-flash`.
    * Nếu key bị hết hạn ngạch (429), tự động xoay vòng sang key tiếp theo trong danh sách đã lưu.
    * Hiển thị thông báo Toast về trạng thái model đang dùng (vd: "Đang xử lý bằng Gemini 3.8 Flash..." -> nếu fallback: "Đã tự động chuyển sang Gemini 2.5 Flash").

### Bước 4: Xây dựng Prompt Tích hợp NLS & AI chuyên sâu theo chuẩn `soankhbd`
- Viết hàm tạo prompt tích hợp:
  + Yêu cầu AI đóng vai trò chuyên gia sư phạm theo chuẩn CV 5512, TT 02/2025 (CV 3456) và QĐ 2422.
  + Nguyên tắc bất biến: Bảo toàn nguyên vẹn toàn bộ văn bản và cấu trúc bài dạy gốc.
  + Tích hợp Mục I. Mục tiêu:
    * Giữ nguyên a) Năng lực chung và b) Năng lực đặc thù.
    * Thêm c) Năng lực số: `- [Mã NLS đã chọn/gợi ý]: [Mô tả nhiệm vụ cụ thể gắn với bài]`.
    * Thêm d) Năng lực AI: `- [Mã AI đã chọn/gợi ý]: [Mô tả nhiệm vụ cụ thể gắn với bài]`.
  + Tích hợp Mục III. Tiến trình dạy học:
    * Lựa chọn 1–2 hoạt động then chốt nhất (Hình thành kiến thức, Luyện tập, Vận dụng).
    * Áp dụng 3 dạng kịch bản thực chiến: Kiểm chứng phản hồi AI có lỗi sai / Prompting gợi mở bước giải / Thao tác công cụ số, phần mềm chuyên dụng (GeoGebra, bảng tính...).
    * Gắn marker chuẩn `**[AI: {Mã} - {Nhiệm vụ}]**`, `**[NLS: {Miền/Mã} - {Tên công cụ}]**`.
    * Nêu rõ sản phẩm/minh chứng, cách giáo viên quan sát đánh giá và kiểm chứng an toàn.
  + Nối Bảng tổng hợp tích hợp ở cuối bài (Nội dung | Mã NLS | Mã AI | Minh chứng sản phẩm).
  + Định dạng đầu ra: Toàn văn Markdown kèm công thức LaTeX `$ ... $` và `$$ ... $$`.

### Bước 5: Hoàn thiện Xử lý Tệp tải lên và Xuất Word OMML
- Xử lý đọc file kéo thả:
  + File `.docx`: dùng `mammoth.extractRawText` (kèm định dạng bảng cơ bản nếu có).
  + File `.pdf`: dùng `pdfjsLib` trích xuất từng trang.
  + File `.txt` / `.md`: đọc văn bản trực tiếp.
- Giữ vững và tối ưu hàm `convertLatexToOMML` và `exportWordDocument` để tạo file `.doc` chứa công thức Word Equation OMML chỉnh sửa được.
- Đồng bộ file `tichhopgiaoan.html` với `giaoantichhop.html`.

## Rủi ro
1. File giáo án tải lên (PDF/Word) có dung lượng quá lớn hoặc cấu trúc phức tạp:
   - Khắc phục: Cho phép người dùng xem trước và chỉnh sửa văn bản đã trích xuất trong ô textarea trước khi bấm tạo; hiển thị số từ/ký tự.
2. Người dùng chưa có API Key hoặc key hết hạn ngạch (429 Quota Exceeded):
   - Khắc phục: Hỗ trợ lưu nhiều key; tự động xoay vòng key; tự động fallback từ 3.8 sang 2.5; hướng dẫn trực quan cách lấy key miễn phí trong 1 phút.
3. Người dùng nhầm lẫn đường dẫn `giaoantichhop.html` và `tichhopgiaoan.html`:
   - Khắc phục: Tạo đồng bộ cả hai tệp để dù mở đường dẫn nào cũng hoạt động hoàn hảo.

## Cách kiểm thử
1. Kiểm tra quyền truy cập không cần đăng nhập:
   - Mở file trong cửa sổ ẩn danh (không có `authToken`), xác nhận không bị điều hướng sang `login.html`.
2. Kiểm tra quản lý API Key:
   - Mở modal Quản lý Key, nhập API key, bấm "Kiểm tra Key" -> xác nhận kiểm tra thành công.
   - Lưu key, F5 tải lại trang -> xác nhận key vẫn lưu trong `localStorage`.
3. Kiểm tra nạp file giáo án:
   - Tải lên tệp Word `.docx` -> xác nhận trích xuất đúng văn bản giáo án.
   - Tải lên tệp PDF `.pdf` -> xác nhận trích xuất đúng nội dung.
   - Bấm "Nạp giáo án mẫu" -> xác nhận nạp đầy đủ thông tin bài dạy mẫu.
4. Kiểm tra gợi ý chuẩn NLS và AI:
   - Chọn Môn học và Lớp (6-9), bấm "⚡ Gợi ý tự động" -> xác nhận các mã chuẩn theo TT 02 và QĐ 2422 được chọn chính xác.
5. Kiểm tra gọi AI và Fallback:
   - Bấm "Bắt đầu tích hợp bằng AI" -> xác nhận gọi `gemini-3.8-flash`.
   - Giả lập lỗi hoặc model bận -> xác nhận hệ thống tự động fallback sang `gemini-2.5-flash` và thông báo cho người dùng.
6. Kiểm tra cấu trúc kết quả:
   - Xác nhận Mục I có bổ sung c) Năng lực số và d) Năng lực AI theo mã đã chọn.
   - Xác nhận Mục III có tích hợp thực chiến với marker `[NLS: ...]` và `[AI: ...]`.
   - Xác nhận có Bảng tổng hợp tích hợp ở cuối bài.
7. Kiểm tra xuất Word:
   - Bấm xuất Word `.doc` -> mở file trong Microsoft Word -> kiểm tra các công thức toán là Microsoft Word Equation (OMML) chỉnh sửa được, định dạng lề A4 chuẩn, màu sắc NLS xanh lá và AI tím hiển thị rõ ràng.

## Tiêu chí nghiệm thu
- Không sửa đổi bất kỳ file nào thuộc `soankhbd.html` hoặc thư viện của nó.
- Trang `giaoantichhop.html` (và `tichhopgiaoan.html`) hoạt động độc lập 100% phía client, không cần đăng nhập.
- Giao diện hiện đại, chuyên nghiệp, hỗ trợ kéo thả tệp giáo án DOCX/PDF/TXT.
- Quản lý API Key cá nhân tiện lợi, lưu cục bộ an toàn, có nút kiểm tra key và xóa key.
- Tích hợp chuẩn xác khung NLS (TT 02 / CV 3456) và khung AI (QĐ 2422) vào Mục I (Mục tiêu) và Mục III (Hoạt động) như `soankhbd`.
- Tự động gọi trực tiếp qua API: Ưu tiên chạy `gemini-3.8-flash` và tự động fallback sang `gemini-2.5-flash`.
- Xuất file Word chuẩn Microsoft Word Equation OMML.
