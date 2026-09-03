# PLAN: Thêm Nút Cài Đặt AI & Đăng Ký Khóa API (Gemini & Mistral) Trên Trang Chủ Người Dùng

## Hiện trạng
1. **Chưa có nơi quản lý API Key tập trung trên trang chủ giáo viên (`index.html`)**:
   - Hiện tại, người dùng sau khi đăng nhập (với vai trò `teacher`) sẽ được đưa về trang chủ `index.html`.
   - Trên `index.html`, thanh điều hướng chỉ có nút "Đăng xuất" và chip "Cập nhật đồng bộ"; hoàn toàn KHÔNG có giao diện hay nút Cài đặt (Setting) nào để người dùng biết mình có thể đăng ký, nhập hoặc cập nhật khóa API (Gemini, Mistral) hay lựa chọn model AI mặc định.
   - Muốn cài đặt API key, giáo viên phải tự tìm và mở các trang công cụ con như `soankhbd.html` hoặc `xaydungphuluc.html` hoặc `duyetde.html`. Điều này gây bất tiện lớn và khiến người dùng thắc mắc: *"vấn đề là tài khoản user sẽ đăng ký API ở đâu?"*.
2. **Chưa có giao diện chọn Module / Model Gemini mặc định trên trang chủ**:
   - Các công cụ trên hệ thống (`smartquiz.html`, `matrande.html`, `kttx.html`, `thitructuyen.html`, `soankhbd.html`, `trochoi.compiled.js`) đều hỗ trợ nhiều model (`gemini-2.5-flash`, `gemini-3-flash-preview`, `gemini-2.5-pro`...) và đọc từ `localStorage.getItem('default_gemini_module')`.
   - Hiện tại giáo viên không có nơi thiết lập model ưu tiên ngay từ trang chủ.
3. **Cơ sở hạ tầng backend đã hoàn toàn sẵn sàng**:
   - `api/user_gemini_keys.php` đã hoàn thiện đầy đủ các chức năng: nạp key qua `GET` (trả về cả `keys`, `mistral_keys`, `masked_keys`), lưu key mã hóa qua `POST`, kiểm tra key qua `POST action=test`, xóa key qua `DELETE`.
   - `access-control.js` đã đồng bộ `global_gemini_keys` và `global_mistral_keys` cho toàn bộ hệ thống khi có phiên đăng nhập.
   - Do đó, chỉ cần bổ sung giao diện Cài đặt AI & API Key trên trang chủ `index.html` kết nối trực tiếp với backend `api/user_gemini_keys.php`.

## Phạm vi
1. **Xây dựng module giao diện `js/user-ai-settings.js`**:
   - Cung cấp component quản lý cài đặt AI cho người dùng (`window.UserAiSettings`):
     * Modal Cài đặt (`#userAiSettingsModal`) với thiết kế hiện đại (Tailwind CSS, responsive trên mobile/tablet/desktop, backdrop blur).
     * **Khai báo Module Gemini**: Dropdown lựa chọn model (`gemini-2.5-flash`, `gemini-3-flash-preview`, `gemini-2.5-pro`...) lưu vào `default_gemini_module` và `khbd_gemini_model`.
     * **Nhập Gemini API Keys**: Textarea nhập nhiều key, hỗ trợ nút nạp từ tệp `.txt`, nút kiểm tra tính hợp lệ của key trực tiếp từ máy chủ.
     * **Nhập Mistral API Keys**: Textarea nhập key Mistral dùng cho OCR/đọc SGK, hỗ trợ nạp từ tệp `.txt`.
     * **Lưu lên CSDL**: Gọi `api/user_gemini_keys.php` (POST) lưu an toàn vào DB tài khoản người dùng, đồng thời lưu vào `localStorage` (`global_gemini_keys`, `global_mistral_keys`, `default_gemini_module`, `khbd_gemini_model`).
     * **Xóa key**: Hỗ trợ nút xóa toàn bộ key khỏi CSDL (`DELETE`) khi cần.
     * **Hiển thị trạng thái**: Trực quan hóa số lượng key Gemini / Mistral hiện tại, thời gian lưu gần nhất.
2. **Tích hợp nút Setting trên trang chủ `index.html`**:
   - Bổ sung nút **"Cấu hình AI & Key"** (icon `fas fa-sliders-h`) trên thanh điều hướng (navbar) cạnh nút Đăng xuất.
   - Bổ sung nút / badge trạng thái API Key trên bảng điều khiển Hero chào mừng (`Xin chào, {teacherName}`) để giáo viên nhìn thấy ngay tình trạng key của mình khi vào trang chủ.
   - Nhúng `<script src="js/user-ai-settings.js"></script>` vào `index.html` và tự động khởi tạo badge trạng thái.
3. **Tạo bài kiểm thử tự động**:
   - Tạo file `tests/user-ai-settings-smoke.js` kiểm tra sự hiện diện của nút Setting, modal, các trường nhập liệu, cơ chế gọi API và các smoke test liên quan.

## Ngoài phạm vi
- Không thay đổi bảng `users` trong CSDL hay cơ chế mã hóa AES-256-CBC trong `api/helpers.php`.
- Không can thiệp vào tài khoản học sinh (`student`), vì học sinh không sử dụng API key cá nhân.

## File dự kiến tác động
- `js/user-ai-settings.js` [TẠO MỚI: Modal & Logic quản lý Cài đặt AI & API Key cá nhân của người dùng]
- `index.html` [SỬA: Thêm nút Setting trên navbar và hero panel, nhúng `js/user-ai-settings.js`]
- `tests/user-ai-settings-smoke.js` [TẠO MỚI: Kiểm thử smoke cho tính năng Cài đặt AI trên trang chủ]
- `docs/handoff/PLAN.md` [GHI ĐÈ KẾ HOẠCH]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]

## Các bước thực hiện
1. **Bước 1: Xây dựng module `js/user-ai-settings.js`**:
   - Định nghĩa đối tượng `window.UserAiSettings`:
     * `ensureModal()`: Tạo cấu trúc HTML modal nếu chưa có trong DOM.
     * `openModal()`: Nạp dữ liệu hiện tại từ `api/user_gemini_keys.php` và `localStorage` (model), điền vào các ô textarea/dropdown, mở modal.
     * `closeModal()`: Đóng modal.
     * `handleFile(file, type)`: Nạp nội dung từ tệp text vào textarea tương ứng.
     * `testGeminiKeys()`: Gửi request `POST api/user_gemini_keys.php` với `action=test`, hiển thị kết quả kiểm tra từng key (hợp lệ / lỗi).
     * `saveSettings()`: Lấy dữ liệu từ textarea Gemini, Mistral và model dropdown; gửi `POST api/user_gemini_keys.php`; cập nhật `default_gemini_module`, `global_gemini_keys`, `global_mistral_keys`; cập nhật badge và hiển thị toast thành công.
     * `deleteKeys()`: Xác nhận và gửi `DELETE api/user_gemini_keys.php`, dọn dẹp localStorage và UI.
     * `updateBadge()`: Cập nhật tóm tắt trạng thái key trên giao diện trang chủ (`#heroKeyStatus`).
2. **Bước 2: Tích hợp vào `index.html`**:
   - Thêm nút bấm Cài đặt AI trên Navbar:
     `<button type="button" onclick="UserAiSettings.openModal()" id="btnOpenUserAiSettings" class="inline-flex items-center gap-2 rounded-full border border-indigo-200 bg-indigo-50 px-4 py-2 text-sm font-bold text-indigo-700 shadow-sm transition hover:bg-indigo-100 hover:border-indigo-300"><i class="fas fa-sliders-h text-indigo-600"></i> Cài đặt AI & Key</button>`
   - Thêm nút / chip trạng thái trong khối Hero giáo viên (`renderTeacherLotrinhPanel`).
   - Nhúng `<script src="js/user-ai-settings.js"></script>` vào cuối thẻ `<body>` trước script khởi tạo.
3. **Bước 3: Tạo bài kiểm thử `tests/user-ai-settings-smoke.js`**:
   - Kiểm tra `index.html` có chứa nút gọi `UserAiSettings.openModal()` và thẻ nhúng script.
   - Kiểm tra `js/user-ai-settings.js` định nghĩa đầy đủ các trường: chọn module gemini (`default_gemini_module`), nhập Gemini keys, Mistral keys, gọi `api/user_gemini_keys.php`.
   - Chạy toàn bộ smoke test suite để đảm bảo không hồi quy:
     * `node tests/user-ai-settings-smoke.js`
     * `node tests/khbd-user-ai-keys-smoke.js`
     * `node tests/matrande-smoke.js`
     * `node tests/kttx-smoke.js`
     * `node tests/xaydungphuluc-smoke.js`
     * `node tests/duyetgiaoan-smoke.js`

## Rủi ro
- **Rủi ro đè cấu hình**: Lưu ý rằng `localStorage` chứa cả `default_gemini_module` và `khbd_gemini_model`; module settings cần đồng bộ cả 2 key này để các công cụ khác nhau đều nhận diện chung 1 model mà giáo viên đã chọn.
- **Rủi ro phiên đăng nhập**: Nếu chưa đăng nhập hoặc session hết hạn, hiển thị thông báo yêu cầu đăng nhập lại thay vì báo lỗi mơ hồ.

## Cách kiểm thử
- Chạy smoke tests bằng Node.js:
  ```powershell
  node tests/user-ai-settings-smoke.js
  node tests/khbd-user-ai-keys-smoke.js
  node tests/matrande-smoke.js
  node tests/kttx-smoke.js
  node tests/xaydungphuluc-smoke.js
  node tests/duyetgiaoan-smoke.js
  ```
- Kiểm tra luồng người dùng trên giao diện:
  1. Đăng nhập tài khoản giáo viên, mở `index.html`.
  2. Bấm nút "Cài đặt AI & Key" trên thanh điều hướng hoặc trên banner chào mừng.
  3. Modal mở ra, hiển thị đúng model đang chọn và danh sách key đã lưu trong CSDL.
  4. Chọn model mới, thêm/sửa key Gemini và Mistral, bấm "Kiểm tra Key" -> thấy kết quả test.
  5. Bấm "Lưu lên CSDL" -> thấy thông báo thành công, badge cập nhật, các trang công cụ khác tự động nhận diện key mới.

## Tiêu chí nghiệm thu
1. Trên trang chủ `index.html` của mỗi user (giáo viên), có nút Cài đặt AI & Key rõ ràng, dễ thấy trên navbar và hero banner.
2. Bấm nút sẽ mở modal cài đặt hoàn chỉnh cho phép:
   - Khai báo / lựa chọn module Gemini (`gemini-2.5-flash`, `gemini-3-flash-preview`, `gemini-2.5-pro`...).
   - Nhập danh sách Gemini API Keys (bằng tay hoặc nạp từ file `.txt`).
   - Nhập danh sách Mistral API Keys (bằng tay hoặc nạp từ file `.txt`).
   - Kiểm tra key hợp lệ trực tiếp.
   - Lưu an toàn lên CSDL máy chủ thông qua `api/user_gemini_keys.php`.
3. Dữ liệu sau khi lưu được đồng bộ tự động tới toàn bộ các trang công cụ trên hệ thống.
4. Toàn bộ smoke test suite (bao gồm `user-ai-settings-smoke.js`) PASS 100%.