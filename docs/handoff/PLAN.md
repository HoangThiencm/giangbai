# PLAN

## Hiện trạng
- Hệ thống quản lý quyền truy cập và phân phối công cụ hiện tại được cấu hình chặt chẽ qua:
  + `access-control.js`: Lưu trữ bản đồ trang `pageKeys` và `pageUrls`, kiểm tra đăng nhập (`token`), phân quyền (`allowedPages`), tự động nạp các key API của người dùng (`khbd_user_gemini_keys_...`, `global_gemini_keys`).
  + `index.html`: Chứa lưới công cụ `#mainToolsGrid` và danh sách liên kết `TOOL_PAGE_LINKS`. Kiểm tra quyền của giáo viên (`applyTeacherAllowedPagesVisibility`) dựa trên `allowedPages` từ cơ sở dữ liệu.
  + `admin.html`: Danh mục trang `hostingPages`, `teacherOnlyPages`, `teacherFeatureGroups`. Quản trị viên cấp quyền từng trang và nhập Gemini API keys cho từng user thông qua modal chỉnh sửa tài khoản.
  + `api/admin_students.php`: Lưu trữ và cập nhật danh sách `allowed_pages` (cột `allowed_pages_json`) và khóa Gemini API mã hóa AES-256 (cột `gemini_keys`) cho từng user trong bảng `users`.
  + `api/user_gemini_keys.php` & `api/duyetde_ai.php`: Cung cấp cơ chế nạp, mã hóa, giải mã và xoay tua (rotate) các key Gemini của chính người dùng đăng nhập để gọi AI an toàn trên máy chủ.
- Hiện chưa có công cụ `sualoichinhta.html`, chưa có card trên `index.html`, chưa được đăng ký trang trong `access-control.js` và `admin.html`.

## Phạm vi
1. Tạo giao diện trang công cụ `sualoichinhta.html`:
   - Giao diện người dùng chuẩn phong cách hệ thống (Tailwind CSS, Font Awesome, responsive).
   - Tích hợp kiểm tra quyền truy cập qua `access-control.js`.
   - Khu vực quản lý Gemini API Key của chính user (tích hợp với `api/user_gemini_keys.php`, cho phép xem trạng thái key, test key, thêm/xóa key cá nhân).
   - Khu vực nhập liệu văn bản (nhập/dán text trực tiếp, tải file text/docx).
   - Tùy chọn cấu hình kiểm tra: Sửa lỗi chính tả & gõ phím; Sửa lỗi dùng từ sai ngữ cảnh (xán lạn / sáng lạng...); Chuẩn hóa dấu câu và khoảng trắng.
   - Bảng kết quả trực quan: Highlight từ sai, bảng liệt kê chi tiết các lỗi (từ gốc, từ đề xuất, ngữ cảnh, giải thích), các nút thao tác: "Áp dụng từng lỗi", "Áp dụng tất cả", "Sao chép", "Tải file".
2. Tạo backend endpoint gọi AI theo user: `api/sualoichinhta_ai.php`:
   - Tự động lấy các `gemini_keys` đã mã hóa của chính user trong session đăng nhập (bảng `users`).
   - Xoay tua key nếu gặp lỗi quota (429, 403), hỗ trợ fallback model (gemini-2.5-flash / gemini-2.0-flash / gemini-1.5-flash).
   - Ép kiểu output dạng JSON chuẩn (Structured Outputs) để client parse lỗi chính xác.
   - Răn đe AI không được tự ý viết lại văn phong (paraphrasing).
3. Đăng ký trang và phân quyền trong `access-control.js`:
   - Bổ sung `sualoichinhta.html` vào `pageKeys` và `pageUrls`.
4. Tích hợp hiển thị trên trang chủ `index.html`:
   - Thêm `sualoichinhta: 'sualoichinhta.html'` vào `TOOL_PAGE_LINKS`.
   - Thêm thẻ hiển thị công cụ (Tool Tile Card) `sualoichinhta` vào `#mainToolsGrid` với icon, nhãn, mô tả và CSS đồng bộ.
   - Hiển thị theo quyền `allowedPages` của user.
5. Cấp quyền trong `admin.html`:
   - Thêm `sualoichinhta` vào `hostingPages`.
   - Thêm `sualoichinhta` vào `teacherFeatureGroups` (nhóm Công cụ giảng dạy) để admin bật/tắt quyền cho từng tài khoản.

## Ngoài phạm vi
- Không can thiệp vào cơ chế xác thực hoặc đổi schema cơ sở dữ liệu bảng `users` (dùng cấu trúc cột `gemini_keys` và `allowed_pages_json` sẵn có).
- Không sửa đổi mã nguồn các công cụ hiện hữu khác ngoài việc đăng ký quyền.

## File dự kiến tác động
- Tạo mới: `sualoichinhta.html`
- Tạo mới: `api/sualoichinhta_ai.php`
- Chỉnh sửa: `access-control.js`
- Chỉnh sửa: `index.html`
- Chỉnh sửa: `admin.html`

## Các bước thực hiện
1. Bước 1: Viết backend `api/sualoichinhta_ai.php`:
   - Kiểm tra session đăng nhập `$_SESSION['user_id']`.
   - Lấy danh sách `gemini_keys` được mã hóa của user hiện tại bằng hàm trong `api/helpers.php`.
   - Tạo prompt nghiêm ngặt kiểm tra lỗi chính tả tiếng Việt kèm JSON Schema đầu ra (chứa danh sách: `original_text`, `suggested_text`, `error_type`, `explanation`, `context`).
   - Gọi Google Gemini REST API với xoay tua key và trả kết quả JSON về cho frontend.
2. Bước 2: Tạo trang giao diện `sualoichinhta.html`:
   - Nhúng `access-control.js`.
   - Dựng header, thanh trạng thái API Key người dùng (tự load từ `api/user_gemini_keys.php`), form nhập văn bản, các nút chức năng.
   - Xử lý tương tác: chia đoạn văn bản nếu dài, gọi API `api/sualoichinhta_ai.php`, hiển thị giao diện so sánh từ sai/từ đúng, cho phép click để sửa trực tiếp vào văn bản.
3. Bước 3: Cập nhật `access-control.js`:
   - Bổ sung `'sualoichinhta.html': 'sualoichinhta'` vào object `pageKeys`.
   - Bổ sung `sualoichinhta: 'sualoichinhta.html'` vào object `pageUrls`.
4. Bước 4: Cập nhật `index.html`:
   - Thêm `sualoichinhta: 'sualoichinhta.html'` vào `TOOL_PAGE_LINKS`.
   - Thêm CSS class `.tool-tile--sualoichinhta` với gradient và watermark biểu tượng chính tả/bút viết.
   - Thêm khối HTML thẻ công cụ `data-tool="sualoichinhta"` vào `#mainToolsGrid`.
5. Bước 5: Cập nhật `admin.html`:
   - Thêm `sualoichinhta: { title: 'Sửa lỗi chính tả AI', url: 'sualoichinhta.html' }` vào `hostingPages`.
   - Thêm `'sualoichinhta'` vào danh sách `pages` trong `teacherFeatureGroups` (Công cụ giảng dạy).

## Rủi ro
- User chưa cấu hình key Gemini riêng trong tài khoản: Cần hiển thị cảnh báo hướng dẫn người dùng nhập key ngay tại giao diện hoặc nhờ admin cấu hình.
- Văn bản kiểm tra quá dài vượt quá giới hạn token: Cần xử lý cắt đoạn văn bản (chunking theo dòng/đoạn) ở phía client/server trước khi gửi đến Gemini.
- Gemini có thể trả về lỗi parse JSON nếu prompt không được gán chặt `response_mime_type: "application/json"`.

## Cách kiểm thử
1. Mở `admin.html`:
   - Kiểm tra trong danh sách phân quyền giáo viên đã xuất hiện tùy chọn "Sửa lỗi chính tả AI".
   - Cấp quyền cho một tài khoản kiểm thử và cấu hình Gemini API Key cho tài khoản đó.
2. Đăng nhập tài khoản kiểm thử:
   - Truy cập `index.html`, kiểm tra thẻ công cụ "Sửa lỗi chính tả AI" có xuất hiện đúng không.
   - Đăng nhập tài khoản chưa được cấp quyền, xác nhận thẻ bị ẩn và nếu gõ trực tiếp `sualoichinhta.html` thì `access-control.js` chặn chuyển hướng về `index.html`.
3. Kiểm thử trang `sualoichinhta.html`:
   - Xác nhận trạng thái Gemini Key hiển thị đúng số lượng key của tài khoản đó.
   - Nhập một đoạn văn có các lỗi mẫu: "Tương lai rất sáng lạng", "Học xinh giỏi giang", "Làm việc trân chính".
   - Nhấn kiểm tra: Xác nhận AI phát hiện đúng từ sai, đề xuất từ đúng ("xán lạn", "học sinh", "chân chính"), không tự tiện viết lại các câu khác.
   - Thử nghiệm tính năng "Áp dụng sửa" và "Sao chép kết quả".

## Tiêu chí nghiệm thu
- Trang `sualoichinhta.html` hoạt động trơn tru, giao diện chuẩn đẹp, responsive.
- Người dùng nào chỉ dùng đúng API Key đã được gán hoặc lưu của người dùng đó (không dùng chung key hệ thống).
- Phân quyền trong Admin hoạt động chuẩn xác: user có quyền mới thấy trên trang chủ và mới truy cập được.
- Phát hiện và sửa chính xác lỗi chính tả, lỗi dùng từ sai ngữ cảnh tiếng Việt, giữ nguyên vẹn cấu trúc văn bản gốc.
