# PLAN: Đồng Bộ Trực Tiếp API Key (Gemini & Mistral) Của Người Dùng Từ CSDL Máy Chủ (api/user_gemini_keys.php) Cho Trang Xây Dựng Phụ Lục

## Hiện trạng
1. **Nguyên Nhân Gây Lỗi Không Nhận Diện API Key Giữa Soạn KHBD và Soạn Phụ Lục**:
   - Trong [soankhbd.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/soankhbd.html), tài khoản người dùng lưu trữ danh sách API Key (ví dụ 6 key Gemini + 2 key Mistral) trực tiếp trên máy chủ CSDL thông qua endpoint [api/user_gemini_keys.php](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/api/user_gemini_keys.php), đồng thời đồng bộ vào `localStorage.getItem('khbd_user_gemini_keys_' + userEmail)`.
   - Trong [xaydungphuluc.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/xaydungphuluc.html), hàm `loadKeys()` trước đây chỉ quét một số khóa cứng trong `localStorage` trên trình duyệt và **hoàn toàn không gọi API máy chủ `api/user_gemini_keys.php`** để tải key về.
   - Khi người dùng đăng nhập tài khoản trên máy khác, hoặc mở tab mới mà `userEmail` chưa được nạp, hoặc trình duyệt chưa kịp lưu localStorage: `xaydungphuluc.html` không thấy key của người dùng, dẫn đến việc lấy key mặc định hệ thống hoặc báo không có key.
   - `xaydungphuluc.html` cũng chưa hỗ trợ đọc và lưu danh sách `mistral_keys` (dùng cho OCR SGK) từ CSDL.

## Phạm vi
1. **Đồng Bộ Hai Chiều Trực Tiếp Với Máy Chủ CSDL ([api/user_gemini_keys.php](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/api/user_gemini_keys.php))**:
   - Hàm `syncUserKeysFromServer()` trong `xaydungphuluc.html`:
     + Tự động gửi `fetch('api/user_gemini_keys.php', { method: 'GET', credentials: 'include' })` ngay khi tải trang (`DOMContentLoaded`) và khi mở Modal Key.
     + Khi máy chủ trả về `{ ok: true, keys: [...], mistral_keys: [...] }`:
       * Tự động nạp toàn bộ danh sách key Gemini của người dùng vào `apiKeys` (ví dụ 6 key).
       * Tự động nạp toàn bộ danh sách key Mistral của người dùng vào `mistralKeys` (ví dụ 2 key).
       * Đồng bộ lưu vào `localStorage` theo đúng định dạng tài khoản: `khbd_user_gemini_keys_${userEmail}` và `khbd_user_mistral_keys_${userEmail}`.
       * Cập nhật badge hiển thị chi tiết: `🔑 6 Gemini · 2 Mistral` (hoặc `🔑 X key cá nhân`).
2. **Lưu Đồng Bộ Lên CSDL Khi Người Dùng Thêm / Sửa Key**:
   - Modal Quản lý API Key trên `xaydungphuluc.html` hỗ trợ 2 ô nhập:
     * Ô 1: **Gemini API Key** (soạn phụ lục, phân tích PPCT).
     * Ô 2: **Mistral API Key** (đọc SGK / OCR).
   - Khi bấm **Lưu lên CSDL**: Tự động gửi `POST api/user_gemini_keys.php` với body `{ keys: [...], mistral_keys: [...] }` để cập nhật đồng thời lên CSDL máy chủ và localStorage. Nhờ đó, sửa key ở `soankhbd.html` hay `xaydungphuluc.html` đều dùng chung 100% dữ liệu.
3. **Quét Vét Toàn Bộ Nguồn LocalStorage Khi Offline / Không Có Mạng**:
   - Dự phòng quét tất cả các biến: `khbd_user_gemini_keys_${userEmail}`, `khbd_gemini_api_keys`, `xdpl_gemini_api_keys`, `gemini_api_keys`, `global_gemini_keys` để không bao giờ bị mất key.
4. **Cập Nhật Bộ Kiểm Thử Tự Động ([tests/xaydungphuluc-smoke.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/tests/xaydungphuluc-smoke.js))**:
   - Thêm bài kiểm tra assert xác nhận `xaydungphuluc.html` có cơ chế `syncUserKeysFromServer`, gọi `api/user_gemini_keys.php`, hỗ trợ `mistral_keys` và badge hiển thị số lượng key chính xác.

## Ngoài phạm vi
- Không can thiệp các file ngoài `xaydungphuluc.html` và file test liên quan.

## File dự kiến tác động
- `xaydungphuluc.html` [TÍCH HỢP ĐỒNG BỘ HAI CHIỀU VỚI API CSDL `api/user_gemini_keys.php`, QUẢN LÝ GEMINI VÀ MISTRAL KEYS ĐỒNG NHẤT VỚI SOANKHBD]
- `tests/xaydungphuluc-smoke.js` [BỔ SUNG SMOKE TEST CHO ĐỒNG BỘ CSDL API KEYS]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Nâng Cấp Logic Quản Lý Key trong `xaydungphuluc.html`**:
   - Thêm biến `mistralKeys = []`.
   - Viết hàm `syncUserKeysFromServer()` gọi `GET api/user_gemini_keys.php` với `credentials: 'include'` để kéo key từ CSDL về ngay khi mở trang.
   - Cập nhật hàm `loadKeys()` để kết hợp cả key từ CSDL máy chủ và localStorage.
2. **Bước 2: Nâng Cấp Modal Quản Lý Key**:
   - Hỗ trợ 2 textarea: `Gemini API Keys` và `Mistral API Keys`.
   - Nút **Lưu lên CSDL** gửi `POST api/user_gemini_keys.php` với `credentials: 'include'`.
   - Cập nhật badge: `🔑 ${apiKeys.length} Gemini · ${mistralKeys.length} Mistral`.
3. **Bước 3: Chạy và Hoàn Thiện Kiểm Thử**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`, xác nhận PASS 100%.

## Rủi ro
- **Rủi ro**: Trường hợp môi trường chạy không có session cookie PHP (ví dụ mở file tĩnh qua file:///):
  - *Giải pháp*: Hàm `syncUserKeysFromServer()` bắt lỗi êm dịu (try/catch no-throw) và tự động chuyển về đọc các key có sẵn trong `localStorage`.

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy `node tests/xaydungphuluc-smoke.js`:
     + Xác nhận có hàm gọi `api/user_gemini_keys.php`.
     + Xác nhận có quản lý `mistralKeys` đồng bộ với `soankhbd.html`.
2. **Kiểm thử thủ công trên trình duyệt**:
   - Mở `soankhbd.html`, lưu 6 key Gemini và 2 key Mistral lên CSDL.
   - Chuyển sang `xaydungphuluc.html` $\rightarrow$ Quan sát badge hiển thị ngay: `🔑 6 Gemini · 2 Mistral`.
   - Bấm `🔑 Quản lý API Key` $\rightarrow$ Thấy đủ 6 key Gemini và 2 key Mistral được điền tự động.

## Tiêu chí nghiệm thu
1. `xaydungphuluc.html` tự động đồng bộ và nhận diện đầy đủ 100% các key Gemini và Mistral của tài khoản người dùng từ CSDL máy chủ (`api/user_gemini_keys.php`).
2. Sửa hoặc lưu key tại bất kỳ trang nào (`soankhbd.html` hoặc `xaydungphuluc.html`) thì trang còn lại tự động cập nhật đồng nhất.
3. Toàn bộ smoke test tự động đều PASS 100%.
