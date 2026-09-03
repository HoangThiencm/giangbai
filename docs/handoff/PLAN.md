# PLAN: Tích Hợp Hệ Thống Rà Soát & Hiệu Chỉnh Đề Kiểm Tra Theo Ma Trận – Bảng Đặc Tả (duyetde.html)

## Hiện trạng
1. **Mã nguồn thẩm định hiện tại**:
   - Hệ thống đã có các mô-đun thẩm định giáo án theo chuẩn CV 5512 (`duyetgiaoan.html`, `api/duyetgiaoan.php`), tạo đề từ ma trận (`matrande.html`), xây dựng phụ lục (`xaydungphuluc.html`), phân công chuyên môn (`phancongtochuyenmon.html`), quản lý phân quyền người dùng (`admin.html`, `access-control.js`, `api/helpers.php`).
   - Chưa có mô-đun chuyên biệt `duyetde.html` để rà soát, thẩm định và hiệu chỉnh đề kiểm tra theo ma trận và bảng đặc tả.
2. **Cơ chế lưu trữ và sử dụng API Key hiện tại**:
   - `api/user_gemini_keys.php` hiện đang lưu API key dạng chuỗi JSON nguyên bản (plain-text) trong cột `gemini_keys` của bảng `users` và trả toàn bộ raw key về phía trình duyệt (client) qua API GET.
   - Trình duyệt sau đó dùng trực tiếp API key để gọi Google Generative Language API. Điều này chưa đáp ứng tối đa khuyến cáo bảo mật của Google AI Studio (nguy cơ lộ key qua Network inspection, DevTools, tiện ích mở rộng hoặc client-side scripts).
3. **Kịch bản Google Apps Script của người dùng**:
   - Đã xây dựng hoàn chỉnh luồng nghiệp vụ 2 bước:
     * Bước 1: `generateSolution` (Chuyên gia giải toán) giải chi tiết toàn bộ đề thi để làm căn cứ thẩm định.
     * Bước 2: `evaluateWithSolution` (Chuyên gia giáo dục) đối chiếu Đề thi, Ma trận đề và Lời giải tham khảo; xuất nhận xét chi tiết từng câu và khối JSON tóm tắt máy đọc (`tong_so_cau`, `so_cau_dat`, `so_cau_can_chinh_sua`, `so_cau_khong_dat`, `ket_luan`).
     * Có thuật toán `callGeminiWithRotation_` tự động xoay vòng danh sách API keys khi gặp lỗi hạn ngạch (429, Quota, Resource Exhausted, 403).
   - Tuy nhiên, kịch bản trên chạy độc lập trên Google Apps Script, chưa kết nối với CSDL MySQL/Hosting của web app, chưa có cơ chế gợi ý sửa câu sai thành bản đề xuất độc lập, chưa có quản lý phiên bản đề (versioning) khi giáo viên hiệu chỉnh, và chưa có giao diện phê duyệt cho Tổ trưởng chuyên môn.

## Phạm vi
1. **Xây dựng module mới `duyetde.html`** ("Hệ thống rà soát và hiệu chỉnh đề kiểm tra theo Ma trận – Đặc tả"):
   - Giao diện web hoàn chỉnh, hiện đại (Tailwind CSS, KaTeX hiển thị công thức toán học, font chữ sắc nét, responsive trên PC và máy tính bảng).
   - **Khai báo hồ sơ đợt duyệt đề**: Tổ chuyên môn, môn học, khối lớp, năm học, học kỳ, loại bài kiểm tra (Thường xuyên, Giữa kỳ, Cuối kỳ), giáo viên ra đề, người thẩm duyệt.
   - **Nạp tài liệu thẩm định đa định dạng (PDF & DOCX)**:
     * Hỗ trợ nạp tệp Đề thi, Ma trận đề, Bảng đặc tả (và Hướng dẫn chấm/đáp án gốc nếu có).
     * Tích hợp bộ đọc tài liệu trực tiếp từ trình duyệt (`pdf.js` và `mammoth.js`) kết hợp gửi tệp đính kèm sang AI backend.
   - **Bộ máy AI Rà soát & Thẩm định 2 pha (chạy qua Backend Proxy)**:
     * *Pha 1 (Solution Engine)*: Trích xuất nội dung và sinh lời giải chi tiết từng bước cho toàn bộ câu hỏi trong đề.
     * *Pha 2 (Evaluation Engine)*: Đối chiếu đề thi, lời giải với ma trận và bảng đặc tả. Đánh giá dứt khoát theo 3 khía cạnh: Ma trận (chuẩn kiến thức, mức độ tư duy, số điểm), Hình thức (câu từ, chính tả, trình bày), Nội dung (tính chính xác khoa học).
   - **Máy trạng thái kết luận nội bộ (State Machine thống nhất)**:
     * `Đạt`: Câu hỏi, mức độ nhận thức, đơn vị kiến thức, số điểm đều khớp hoàn toàn với ma trận và bảng đặc tả.
     * `Cần chỉnh sửa`: Lỗi chính tả, diễn đạt, hình vẽ chưa rõ ràng hoặc gợi ý tinh chỉnh câu chữ nhỏ.
     * `Không đạt`: Sai mạch kiến thức, sai mức độ tư duy (ví dụ đặc tả yêu cầu mức Vận dụng nhưng câu hỏi thực tế chỉ ở mức Thông hiểu), sai số điểm hoặc không có trong ma trận/đặc tả.
     * `Chưa đủ dữ liệu để kết luận`: Ma trận/đặc tả bị mờ, thiếu dữ liệu hoặc câu hỏi không rõ ngữ cảnh.
   - **Chức năng "Gợi ý sửa đề" & Quản lý Phiên bản (Versioning Engine)**:
     * Không ghi đè trực tiếp lên đề gốc mà tạo thành bản đề xuất hiệu chỉnh (Revision Proposal).
     * Cấu trúc thẻ hiệu chỉnh từng câu:
       + Nhận xét sai lệch chi tiết.
       + Căn cứ cụ thể (Dòng ma trận, tên bài học/chủ đề, mức độ nhận thức, điểm số quy định).
       + Câu hỏi gốc nguyên văn.
       + Câu hỏi đề xuất mới do AI viết lại cho đúng mức độ và chuẩn kiến thức.
       + Đáp án và hướng dẫn chấm mới tương ứng.
     * Hành động của giáo viên: Chấp nhận (Accept) / Chỉnh sửa thêm (Edit inline) / Bỏ qua (Keep original).
     * Khi giáo viên sửa bất kỳ câu nào: Hệ thống tự động tạo phiên bản đề mới (v1 -> v2...), lưu lịch sử thay đổi (diff) và tự động yêu cầu **Kiểm tra lại (Re-verify)** riêng câu đó, đồng thời hủy bỏ trạng thái "Đạt" của đề cũ cho đến khi bản mới được đối chiếu đạt chuẩn.
   - **Quy trình Phê duyệt của Tổ trưởng chuyên môn**:
     * Tổ trưởng xem tổng quan hồ sơ, kết quả đối chiếu từng câu, lịch sử các phiên bản hiệu chỉnh.
     * Đưa ra kết luận chính thức: "Có thể sử dụng" | "Cần chỉnh sửa" | "Không sử dụng" kèm ý kiến chỉ đạo.
     * Xuất biên bản rà soát đề và Đề thi hiệu chỉnh hoàn chỉnh ra định dạng Word (`.docx`).
2. **Nâng cấp bảo mật API Key trong Backend (`api/user_gemini_keys.php`, `api/helpers.php`)**:
   - Lưu trữ mã hóa: Sử dụng thuật toán mã hóa đối xứng AES-256-CBC với Server Secret Key để mã hóa API keys trước khi lưu vào CSDL.
   - Phân quyền theo tài khoản: Mỗi giáo viên chỉ được phép quản lý và sử dụng API keys thuộc tài khoản của mình.
   - Bảo vệ phía Client: API GET tuyệt đối không trả lại raw API keys. Chỉ trả về: số lượng key đã lưu, danh sách key đã che ký tự (ví dụ: `AIzaSy...****`) và thời gian cập nhật.
   - Người dùng có thể tự thêm key mới, xóa danh sách key hoặc cập nhật key từ giao diện.
3. **Xây dựng Backend AI Proxy & Round-Robin Rotation (`api/duyetde_ai.php`)**:
   - Backend đóng vai trò Gateway an toàn kết nối tới Google Gemini API (`https://generativelanguage.googleapis.com/v1beta/models/...`).
   - Tự động lấy danh sách API keys đã giải mã của chính user từ phiên đăng nhập (session).
   - Triển khai cơ chế xoay vòng key (Round-Robin with Auto-Retry) khi gặp mã lỗi 429 (Too Many Requests), 403 (Permission Denied/Quota Exceeded) hoặc lỗi quá tải.
   - Cung cấp các hành động:
     * `generate_solution`: Giải chi tiết đề thi.
     * `evaluate_exam`: Rà soát đối chiếu toàn diện đề thi với ma trận và bảng đặc tả.
     * `recheck_single_question`: Đối chiếu lại riêng 1 câu hỏi vừa được hiệu chỉnh.
4. **Xây dựng API Lưu Trữ Hồ Sơ Duyệt Đề (`api/duyetde.php`)**:
   - Tự động khởi tạo bảng CSDL `duyetde_sessions` nếu chưa tồn tại.
   - Quản lý phiên bản đề thi, lưu trữ dữ liệu JSON chi tiết (câu gốc, nhận xét, gợi ý sửa, các bản hiệu chỉnh, trạng thái duyệt của tổ trưởng).
   - Cung cấp các endpoint: danh sách đợt duyệt, chi tiết đợt duyệt, lưu đợt duyệt mới/cập nhật, xóa đợt duyệt.
5. **Khai báo và kích hoạt trong `admin.html`, `access-control.js`, `api/helpers.php`, `index.html`**:
   - Khai báo tính năng `duyetde` trong `admin.html` (danh mục cấu hình chung, quản lý tính năng theo tài khoản giáo viên).
   - Cập nhật danh mục phân quyền trong `access-control.js` và `api/helpers.php`.
   - Bổ sung thẻ công cụ `duyetde` trực quan trên trang chủ `index.html` cho giáo viên.

## Ngoài phạm vi
- Không can thiệp hoặc thay đổi cấu trúc dữ liệu của các công cụ khác (`matrande.html`, `soankhbd.html`, `duyetgiaoan.html`).
- Không tác động vào hệ thống thi trực tuyến của học sinh (`thitructuyen.html`).

## File dự kiến tác động
- `duyetde.html` [TẠO MỚI: Giao diện hoàn chỉnh Hệ thống rà soát và hiệu chỉnh đề kiểm tra theo Ma trận – Đặc tả]
- `api/duyetde.php` [TẠO MỚI: API lưu trữ hồ sơ thẩm định đề, quản lý đa phiên bản đề, CRUD đợt duyệt]
- `api/duyetde_ai.php` [TẠO MỚI: Backend AI Proxy gọi Gemini, xoay vòng API key, mã hóa bảo mật, giải đề, đối chiếu ma trận, kiểm tra câu sửa]
- `api/user_gemini_keys.php` [NÂNG CẤP: Mã hóa AES-256 lưu trữ key, bảo vệ không trả raw key về client, chỉ trả masked key info]
- `api/helpers.php` [CẬP NHẬN: Bổ sung hàm mã hóa/giải mã AES-256 an toàn, khai báo catalog, workspace page ids, default extra pages cho `duyetde`]
- `access-control.js` [CẬP NHẬN: Khai báo route bảo vệ `duyetde.html` và page key `duyetde`]
- `admin.html` [CẬP NHẬN: Thêm cấu hình bật/tắt `cfg_duyetde`, phân quyền giáo viên theo tài khoản trong danh mục tính năng]
- `index.html` [CẬP NHẬN: Thêm card công cụ "Rà soát & Hiệu chỉnh Đề Kiểm Tra" (Duyệt đề AI) trong Hub giáo viên]
- `docs/handoff/PLAN.md` [GHI ĐÈ KẾ HOẠCH]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]

## Các bước thực hiện
1. **Bước 1: Nâng cấp bảo mật API Key trong `api/helpers.php` và `api/user_gemini_keys.php`**:
   - Xây dựng 2 hàm mã hóa đối xứng trong `api/helpers.php`: `encrypt_user_api_key($rawKey)` và `decrypt_user_api_key($encryptedKey)` sử dụng `openssl_encrypt`/`openssl_decrypt` với thuật toán `AES-256-CBC` và secret salt định nghĩa trên server.
   - Cập nhật `api/user_gemini_keys.php`:
     * Khi nhận key từ người dùng (POST): Mã hóa từng key trước khi lưu vào cột `gemini_keys` trong bảng `users`. Hỗ trợ tự động nhận diện nếu key cũ chưa mã hóa thì tự động nâng cấp sang chuỗi mã hóa.
     * Khi trả về cho trình duyệt (GET): Chỉ trả về metadata an toàn gồm: `count` (số lượng key đang hoạt động), `masked_keys` (dạng `AIzaSy...****`), tuyệt đối không gửi raw key về client.
     * Bổ sung cơ chế test key hợp lệ từ backend mà không lộ key ra ngoài.
2. **Bước 2: Xây dựng Backend AI Gateway `api/duyetde_ai.php`**:
   - Tiếp nhận request từ `duyetde.html` kèm session của người dùng hiện tại.
   - Đọc danh sách keys từ bảng `users`, giải mã bằng hàm nội bộ server.
   - Triển khai logic gọi Gemini với xoay vòng key tự động (`call_gemini_with_rotation`): nếu gặp mã lỗi 429 hoặc lỗi quota/permission, tự động chuyển sang key tiếp theo trong danh sách.
   - Hỗ trợ 3 endpoint con:
     * `action=generate_solution`: Nhận đề thi (PDF base64 hoặc văn bản trích xuất), gửi prompt chuyên gia giải toán để sinh bài giải mẫu chi tiết.
     * `action=evaluate_exam`: Nhận đề thi, ma trận, bảng đặc tả và bài giải tham khảo; yêu cầu Gemini phân tích từng câu theo 3 tiêu chí (Ma trận, Hình thức, Nội dung) và trả về JSON chuẩn hóa (kèm câu hỏi đề xuất viết lại, đáp án gợi ý và căn cứ dòng/cột ma trận cho các câu sai/lệch).
     * `action=recheck_question`: Nhận thông tin ma trận, đặc tả và 1 câu hỏi cụ thể đã được giáo viên sửa để thẩm định lại xem câu đó đã chuyển sang trạng thái "Đạt" hay chưa.
3. **Bước 3: Xây dựng API Lưu Trữ & Quản Lý Phiên Bản `api/duyetde.php`**:
   - Hàm `ensure_duyetde_sessions($pdo)` tự động tạo bảng `duyetde_sessions`:
     ```sql
     CREATE TABLE IF NOT EXISTS duyetde_sessions (
         id INT AUTO_INCREMENT PRIMARY KEY,
         user_id INT NOT NULL,
         title VARCHAR(255) NOT NULL DEFAULT '',
         to_chuyen_mon VARCHAR(150) NOT NULL DEFAULT '',
         mon_hoc VARCHAR(80) NOT NULL DEFAULT '',
         khoi_lop VARCHAR(30) NOT NULL DEFAULT '',
         loai_de VARCHAR(50) NOT NULL DEFAULT '',
         nam_hoc VARCHAR(30) NOT NULL DEFAULT '',
         current_version INT NOT NULL DEFAULT 1,
         status VARCHAR(50) NOT NULL DEFAULT 'draft',
         final_decision VARCHAR(50) NOT NULL DEFAULT '',
         leader_feedback TEXT DEFAULT NULL,
         session_data LONGTEXT NOT NULL,
         created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
         updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
         INDEX idx_duyetde_user (user_id),
         INDEX idx_duyetde_status (status),
         INDEX idx_duyetde_updated (updated_at)
     ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
     ```
   - Cung cấp các thao tác: danh sách đợt duyệt theo user, tải chi tiết theo ID, lưu/cập nhật đợt duyệt kèm lịch sử các phiên bản đề, xóa đợt duyệt, nộp duyệt lên tổ trưởng, lưu quyết định thẩm duyệt của tổ trưởng.
4. **Bước 4: Xây dựng Giao diện Ứng Dụng `duyetde.html`**:
   - Thiết kế giao diện chuyên nghiệp chia thành các phân khu chức năng mạch lạc:
     * *Phân khu 1: Thông tin đợt thẩm định*: Khai báo Tổ chuyên môn, môn giảng dạy, khối lớp, loại bài kiểm tra, năm học. Tích hợp quản lý API Key bảo mật (nhập key cá nhân, xem trạng thái key an toàn, xóa key).
     * *Phân khu 2: Nạp hồ sơ đề thi*: Nạp 3 thành phần bắt buộc (Đề thi, Ma trận đề, Bảng đặc tả) và 1 thành phần tùy chọn (Đáp án/Hướng dẫn chấm). Hỗ trợ xem trước và trích xuất nội dung văn bản qua `pdf.js` và `mammoth.js`.
     * *Phân khu 3: Rà soát & Thẩm định AI*:
       - Thanh tiến trình trực quan từng pha (Đang giải đề -> Đang đối chiếu ma trận -> Hoàn tất).
       - Thống kê tổng quan: Tổng số câu, Số câu Đạt, Cần chỉnh sửa, Không đạt, Chưa đủ dữ liệu.
       - Bảng đối chiếu từng câu chi tiết: Hiển thị trạng thái màu sắc theo State Machine, căn cứ dòng/cột ma trận, nhận xét chi tiết.
     * *Phân khu 4: Bảng đề xuất hiệu chỉnh (Gợi ý sửa đề) & Đa phiên bản (Versioning)*:
       - Hiển thị so sánh song song giữa câu hỏi gốc và câu hỏi do AI đề xuất viết lại kèm đáp án/gợi ý chấm mới.
       - Giáo viên có 3 nút hành động: "Chấp nhận câu đề xuất", "Tự chỉnh sửa thêm", "Bỏ qua (giữ câu gốc)".
       - Cơ chế Versioning: Tự động tạo phiên bản đề mới (v1 -> v2...), lưu diff và gắn cờ câu cần kiểm tra lại. Nút "Kiểm tra lại câu sửa" gọi API recheck để cập nhật trạng thái đạt chuẩn.
     * *Phân khu 5: Thẩm định của Tổ trưởng & Xuất báo cáo*:
       - Quyết định phê duyệt: Có thể sử dụng / Cần chỉnh sửa / Không sử dụng.
       - Nhập ý kiến chỉ đạo chuyên môn của tổ trưởng.
       - Nút "Xuất biên bản thẩm định .docx" và "Xuất đề thi hoàn chỉnh .docx" bằng thư viện `docx.js`.
5. **Bước 5: Đăng ký và kích hoạt quyền trong toàn hệ thống**:
   - Cập nhật `admin.html`:
     * Thêm checkbox cấu hình hệ thống `cfg_duyetde` tại nhóm công cụ chuyên môn.
     * Thêm `duyetde` vào `CLIENT_FEATURE_CHECKS`.
     * Bổ sung tên hiển thị vào `FEATURE_NAMES`: `duyetde: "Rà soát & Hiệu chỉnh Đề Kiểm Tra (Duyệt đề AI)"`.
     * Thêm vào danh mục `USER_FEATURE_GROUPS` (nhóm công cụ giáo viên).
     * Thêm vào `hostingPages` và `teacherFeatureGroups` để cấp quyền mở cho từng tài khoản.
   - Cập nhật `access-control.js`:
     * Thêm mapping `'duyetde.html': 'duyetde'` và `duyetde: 'duyetde.html'`.
   - Cập nhật `api/helpers.php`:
     * Khai báo trong `page_catalog()`, `teacher_workspace_page_ids()`, `teacher_feature_keys_for_pages()`, `teacher_default_workspace_extras()`.
   - Cập nhật `index.html`:
     * Thêm thẻ công cụ "Rà soát & Hiệu chỉnh Đề Kiểm Tra" (Duyệt đề AI) với biểu tượng `fa-file-shield` và nhãn CV chuẩn vào danh sách công cụ giáo viên.
6. **Bước 6: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.


### Giải pháp đặc trị cho Ma trận & Bảng đặc tả dài (8–9 trang PDF)
1. **Thách thức**:
   - Bảng đặc tả đề kiểm tra theo CTGDPT 2018 thường dài từ 6–10 trang PDF, cấu trúc bảng nhiều cột gộp (merged cells), phân cấp phức tạp (Chủ đề -> Đơn vị kiến thức -> YCCĐ -> Mức độ tư duy -> Mã câu/hình thức trắc nghiệm).
   - Nếu ném toàn bộ 8–9 trang PDF cùng lúc với Đề thi vào 1 prompt duy nhất, LLM dễ bị hiện tượng "Lost in the middle", đọc sót dòng hoặc nhầm lẫn giữa các mức độ (Nhận biết vs Thông hiểu).
   - Bóc tách thô bằng `pdf.js` dạng plain text thường làm vỡ cấu trúc cột bảng biểu.
2. **Kiến trúc giải pháp 3 chặng (Pipeline)**:
   - **Chặng 1 - Structural Indexing (Trích xuất & Cấu trúc hóa Ma trận - Đặc tả)**:
     * Gửi trực tiếp PDF nguyên bản (dạng `inline_data` base64) vào Gemini Multimodal để tận dụng khả năng nhận diện bố cục thị giác (Visual Table Understanding).
     * Nhiệm vụ chuyên biệt của Chặng 1: Quét 8–9 trang bảng đặc tả và chuyển đổi thành **"Specification Matrix Index" (Bảng chỉ mục JSON phẳng)**.
     * Mỗi mục trong JSON đại diện cho 1 chỉ tiêu câu hỏi: `{ vi_tri_cau, chu_de, don_vi_kien_thuc, muc_do, yccd_yeu_cau_can_dat, so_diem, dang_cau }`.
     * Tự động tổng hợp bảng kiểm tra chéo (Cross-check): Tổng số câu Nhận biết / Thông hiểu / Vận dụng / Vận dụng cao và tổng điểm (10 điểm).
   - **Chặng 2 - Map & Match (Ánh xạ từng câu đối chiếu)**:
     * Dùng Specification Matrix Index ở Chặng 1 làm chuẩn căn cứ để đối chiếu với từng câu trong đề thi và bài giải.
     * Có thể chạy đối chiếu theo từng phần (Phần I: TN nhiều lựa chọn; Phần II: Đúng/Sai; Phần III: Trả lời ngắn; Tự luận) giúp AI tập trung tuyệt đối, không bao giờ bị tràn ngữ cảnh hay nhầm dòng.
   - **Chặng 3 - Caching & Reusable**:
     * Lưu Specification Matrix Index vào hồ sơ đợt duyệt. Khi giáo viên sửa 1 câu và bấm "Kiểm tra lại câu sửa", hệ thống chỉ cần lấy đúng dòng chỉ mục của câu đó ra để đối chiếu, không cần đọc lại 8–9 trang PDF ma trận từ đầu, tiết kiệm token và tăng tốc độ phản hồi tức thì (< 3 giây).



### Chi tiết Kỹ thuật: Bóc tách Bảng Ma trận & Bảng Đặc tả (Specification Matrix Schema)
Để giải quyết bài toán ma trận dài 8–9 trang và tránh các bẫy nghiệp vụ thực tế, cấu trúc bóc tách bắt buộc phải tuân theo 2 tầng dữ liệu:

1. **Schema JSON chuẩn hóa (`SpecificationMatrixIndex`)**:
```json
{
  "tong_quan": {
    "mon": "Toán",
    "lop": 9,
    "thoi_gian_phut": 90,
    "tong_diem": 10.0,
    "ti_le_phan_tram": {
      "nhan_biet": 40,
      "thong_hieu": 30,
      "van_dung": 20,
      "van_dung_cao": 10
    }
  },
  "danh_sach_chi_tieu": [
    {
      "id": "SPEC_01",
      "chu_de": "Hàm số bậc nhất",
      "don_vi_kien_thuc": "Hàm số y = ax + b",
      "phan_thi": "Phần I",
      "dang_cau": "TNKQ_4_lua_chon",
      "vi_tri_du_kien": "Câu 1",
      "muc_do": "nhan_biet",
      "yccd": "Nhận biết được tính đồng biến, nghịch biến của hàm số y = ax + b qua hệ số a",
      "so_diem": 0.25,
      "yeu_cau_ngu_lieu": "Toán thuần túy"
    },
    {
      "id": "SPEC_02",
      "chu_de": "Hàm số bậc nhất",
      "don_vi_kien_thuc": "Ứng dụng thực tế",
      "phan_thi": "Phần II",
      "dang_cau": "TNKQ_dung_sai",
      "vi_tri_du_kien": "Câu 1",
      "cac_y_con": [
        { "y": "a", "muc_do": "nhan_biet", "diem": 0.1, "yccd": "Nhận biết điểm thuộc đồ thị" },
        { "y": "b", "muc_do": "thong_hieu", "diem": 0.15, "yccd": "Tìm toạ độ giao điểm" },
        { "y": "c", "muc_do": "van_dung", "diem": 0.25, "yccd": "Tính quãng đường chuyển động thực tế", "yeu_cau_ngu_lieu": "Bài toán thực tế" },
        { "y": "d", "muc_do": "van_dung_cao", "diem": 0.5, "yccd": "Tối ưu hóa chi phí taxi theo đồ thị", "yeu_cau_ngu_lieu": "Bài toán thực tế" }
      ]
    }
  ]
}
```

2. **Thuật toán Khớp chỉ tiêu (Slot Matching)**:
- Đối với ma trận có mã câu (`vi_tri_du_kien`): Ánh xạ trực tiếp với câu tương ứng trong đề thi.
- Đối với ma trận không có mã câu (chỉ có số lượng): AI duyệt các câu hỏi trong đề thuộc cùng chủ đề/phần thi, tính độ tương đồng ngữ nghĩa giữa nội dung câu hỏi và `yccd`, sau đó ghép vào chỉ tiêu phù hợp nhất.
- Báo cảnh báo nếu: Có chỉ tiêu trong ma trận không tìm thấy câu hỏi tương ứng trong đề, hoặc câu hỏi trong đề không thuộc bất kỳ chỉ tiêu nào của ma trận.

### 4 Tiêu chí thực chiến bổ sung để "Đủ dùng 100% trong trường học"
1. **Xuất Đề thi hoàn chỉnh sau hiệu chỉnh (.docx sẵn sàng in ấn)**:
   - Ngoài xuất "Biên bản thẩm định", hệ thống tự động tổng hợp và xuất ra file **"Đề kiểm tra chính thức (.docx)"** và **"Hướng dẫn chấm chính thức (.docx)"** đã được thay thế các câu đã sửa đạt chuẩn, đúng format in ấn của Bộ/Sở.
2. **Cảnh báo Tổng thời lượng làm bài (Time Feasibility Check)**:
   - AI ước lượng tổng thời gian hoàn thành của học sinh (ví dụ: đề 45 phút, 60 phút hay 90 phút). Cảnh báo nếu các câu vận dụng quá dài khiến học sinh trung bình không kịp làm bài.
3. **Quản lý Hình vẽ / Đồ thị đính kèm**:
   - Với các câu môn Toán/KHTN có hình học, đồ thị: AI giữ nguyên mô tả hình ảnh hoặc đề xuất hình vẽ tương ứng trong phần gợi ý câu hỏi.
4. **Biên bản duyệt đề chuẩn mẫu trường học**:
   - Mẫu biên bản xuất ra có đầy đủ phần ký duyệt của Giáo viên ra đề, Tổ trưởng chuyên môn và ý kiến của Ban Giám hiệu.

## Rủi ro
1. **Rủi ro rò rỉ API Key nếu vẫn gửi qua request client**:
   - *Giải pháp*: Triển khai triệt để mô hình Backend Gateway. Trình duyệt không bao giờ nhìn thấy hoặc nhận lại chuỗi API key gốc. Mọi thao tác gọi Gemini đều do server xử lý qua cURL với key đã giải mã trong RAM của tiến trình backend.
2. **Rủi ro ma trận hoặc đặc tả quét dạng ảnh scan chất lượng kém hoặc bố cục bảng phức tạp**:
   - *Giải pháp*: Cho phép gửi đồng thời cả văn bản trích xuất (từ DOCX/PDF) và dữ liệu PDF nhị phân (base64) để Gemini Multimodal phân tích cấu trúc bảng trực quan. Khi thiếu dữ liệu hoặc không đọc được, AI chuyển trạng thái sang "Chưa đủ dữ liệu để kết luận" thay vì kết luận bừa.
3. **Rủi ro mất dấu phiên bản khi giáo viên sửa câu hỏi**:
   - *Giải pháp*: Xây dựng cấu trúc dữ liệu Snapshot rõ ràng theo từng version: mỗi lần chấp nhận sửa câu, tạo ra version mới lưu giữ toàn bộ snapshot câu hỏi cũ và mới, đồng thời bắt buộc hủy bỏ trạng thái "Đạt" của đề cũ cho đến khi hoàn thành thẩm định lại.

## Cách kiểm thử
1. **Kiểm thử bảo mật API Key**:
   - Đăng nhập tài khoản giáo viên, lưu API key từ giao diện `duyetde.html`.
   - Kiểm tra trực tiếp bảng `users` trong CSDL: Cột `gemini_keys` chứa chuỗi mã hóa, không thể đọc bằng mắt thường.
   - Mở Tab Network của trình duyệt: Xem response của `api/user_gemini_keys.php` -> Chỉ có metadata `masked_keys` (`AIzaSy...****`) và `count`, tuyệt đối không có key gốc.
2. **Kiểm thử AI Gateway & Xoay vòng Key (Rotation)**:
   - Cấu hình 1 key lỗi hạn ngạch (hoặc giả lập trả về 429) và 1 key chuẩn: Backend tự động bắt exception, ghi log cảnh báo và tự động đổi sang key tiếp theo để gọi thành công.
3. **Kiểm thử Logic Thẩm Định & State Machine**:
   - Nạp bộ dữ liệu thử nghiệm gồm Đề thi và Ma trận – Đặc tả môn Toán (hoặc môn khác):
     * Câu hỏi khớp đúng đặc tả -> Kết luận "Đạt".
     * Câu hỏi có lỗi chính tả/diễn đạt nhỏ -> Kết luận "Cần chỉnh sửa".
     * Câu hỏi sai mức độ (ví dụ đặc tả đòi Vận dụng nhưng câu hỏi là Nhận biết) -> Kết luận "Không đạt" kèm câu đề xuất viết lại.
4. **Kiểm thử Quy trình Hiệu chỉnh & Phiên bản (Proposal & Versioning)**:
   - Tại câu hỏi bị đánh giá "Không đạt": Xem nội dung đề xuất sửa của AI.
   - Bấm "Chấp nhận câu đề xuất" -> Kiểm tra hệ thống tự động sinh phiên bản đề v2, đánh dấu câu hỏi cần kiểm tra lại.
   - Bấm "Kiểm tra lại câu sửa" -> Hệ thống đối chiếu riêng câu đó với ma trận và chuyển trạng thái sang "Đạt".
5. **Kiểm thử Quyết định của Tổ trưởng & Xuất Báo Cáo DOCX**:
   - Tổ trưởng chọn kết luận "Có thể sử dụng" và nhập ý kiến -> Dữ liệu được lưu thành công vào CSDL.
   - Bấm nút "Xuất biên bản thẩm định .docx" và "Xuất đề thi hoàn chỉnh .docx" -> Tệp Word tải về máy tính định dạng chuẩn, đọc tốt trên Microsoft Word.
6. **Kiểm thử Tích hợp Phân Quyền**:
   - Đăng nhập admin, tắt quyền `duyetde` của tài khoản -> Tài khoản đó truy cập `duyetde.html` bị `access-control.js` chặn và chuyển hướng.
   - Bật quyền `duyetde` -> Mở được bình thường từ icon trên `index.html`.

## Tiêu chí nghiệm thu
- [ ] Giao diện `duyetde.html` hoạt động mượt mà, đầy đủ các phân khu khai báo hồ sơ, nạp tệp, chạy thẩm định, bảng đối chiếu, gợi ý sửa đề và thẩm duyệt của tổ trưởng.
- [ ] API Key của giáo viên được lưu trữ mã hóa trong CSDL, backend xử lý proxy gọi AI, không bao giờ lộ raw API key ra client, có che 4 ký tự cuối khi hiển thị.
- [ ] Hỗ trợ nạp đầy đủ Đề thi, Ma trận đề, Bảng đặc tả và Đáp án (PDF, DOCX).
- [ ] Phân loại trạng thái từng câu chính xác theo State Machine (Đạt / Cần chỉnh sửa / Không đạt / Chưa đủ dữ liệu).
- [ ] Chức năng gợi ý sửa đề tạo bản đề xuất độc lập (không ghi đè đề gốc), hiển thị nhận xét sai lệch, căn cứ ma trận, câu gốc, câu đề xuất AI, đáp án mới.
- [ ] Cơ chế Versioning tự động tạo phiên bản mới khi sửa câu, bắt buộc kiểm tra lại câu sửa trước khi công nhận kết quả.
- [ ] Tổ trưởng chuyên môn có thể đánh giá và kết luận cuối cùng (Có thể sử dụng / Cần chỉnh sửa / Không sử dụng).
- [ ] Xuất được biên bản thẩm định và đề thi hiệu chỉnh ra file `.docx`.
- [ ] Khai báo và kích hoạt đầy đủ trong `admin.html`, `access-control.js`, `api/helpers.php`, `index.html`.