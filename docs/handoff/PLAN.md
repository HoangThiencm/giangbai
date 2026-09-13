# PLAN

## Hiện trạng
- `canvas_xaydungphuluc.html` hiện tại gọi cố định qua endpoint duy nhất: `CANVAS_ENDPOINT = 'https://hoangthiencm.id.vn/api/canvas_gemini.php'` với model cố định `gemini-3-flash-preview` ở phía máy chủ bằng system key của Admin.
- Các hàm quản lý key trên Canvas (`openKeyModal`, `saveKeys`, `checkKeys`, `updateKeyBadge`) hiện đang bị vô hiệu hóa với thông báo: *"Gemini Canvas được hệ thống cấp sẵn."*
- Canvas đã có sẵn cơ chế nhận diện tài khoản giáo viên qua `canvasDraftAccount` (lưu trong `localStorage`/`memoryStorage` với key `canvas_xdpl_user` hoặc lấy từ `#teacher`), gửi qua Header `X-User-Account` và tham số `user_account` tới `api/user_phuluc_draft.php`.
- CSDL `users` đã có cột `gemini_keys` lưu trữ danh sách API keys đã mã hóa của người dùng (quản lý bởi `api/user_gemini_keys.php`).
- Môi trường Google Canvas chạy trong iframe sandbox nghiêm ngặt: cấm gọi trực tiếp `generativelanguage.googleapis.com` hoặc các endpoint session-cookie truyền thống (như đã được ràng buộc trong `tests/canvas-xaydungphuluc-smoke.js`).
- Các tác vụ hiện tại chưa được phân tầng: tác vụ bóc tách văn bản lớn (đọc file SGK hàng chục ngàn từ, nhận diện PPCT) và tác vụ tư duy sư phạm sâu (sinh Phụ lục 1, 2, 3) đều đi chung một model cố định.

## Phạm vi
1. **Kết nối tài khoản & Hiển thị số lượng API Key trên Canvas**:
   - Mở rộng `api/canvas_gemini.php` hỗ trợ action `key_status` (qua GET hoặc POST) nhận `user_account` (qua query hoặc header `X-User-Account`).
   - Truy vấn CSDL `users`, giải mã và đếm số lượng `gemini_keys` hợp lệ của tài khoản.
   - Trả về payload an toàn: `{ ok: true, user_account: ..., gemini_key_count: N, masked_keys: [...] }` (tuyệt đối không lộ key thô ra client).
   - Trên giao diện `canvas_xaydungphuluc.html`:
     - Header hiển thị Badge kết nối trực quan kèm số lượng key:
       - Có key: `⚡ Gemini 3.8 Flash · [account] ([N] keys)` (màu xanh/tím nổi bật).
       - Chưa có key/chưa kết nối: `🛡 Gemini 3 Flash Preview · Nội bộ (0 key cá nhân)`.
     - Cho phép click badge mở Modal Quản lý API Key / Kết nối tài khoản để kiểm tra trạng thái, xem masked keys và đổi tài khoản kết nối.
2. **Thiết kế Đa tầng (Multi-tier Hybrid Routing)**:
   - **Tầng 1 - Nặng Token / I/O-heavy (Đọc SGK & Nhận diện PPCT)**:
     - `recognizePpctWithAi` và `buildSgkKnowledgeBase` / `readStagedSgk`: gửi request với `tier: 'heavy_io'`.
     - Backend `api/canvas_gemini.php` xử lý bằng model hệ thống nội bộ `gemini-3-flash-preview` (dùng system keys của Admin). Giữ trọn vẹn quota cá nhân cho giáo viên.
   - **Tầng 2 - Tư duy cao / High-reasoning (Sinh Phụ lục 1, 2, 3)**:
     - `callGemini` khi sinh Phụ lục (trong `generateSelected`): gửi request với `tier: 'high_reasoning'`, `preferred_model: 'gemini-3.8-flash'`.
     - Backend `api/canvas_gemini.php`:
       - Đọc danh sách key của user từ DB (`users.gemini_keys`).
       - Gọi `gemini-3.8-flash` với key của user.
       - **Tự động xoay key (Key Rotation)**: Nếu gặp lỗi HTTP 429 (ResourceExhausted / Quota Exceeded), tự động chuyển sang key kế tiếp của user.
       - **Fallback an toàn (Graceful Fallback)**: Nếu tất cả key của user bị lỗi/hết hạn mức hoặc tài khoản chưa có key, tự động chuyển về system key với `gemini-3-flash-preview`.
       - Trả về kết quả kèm thông tin định tuyến: `{ ok: true, body: ..., model: '...', tier: 'user_key'|'fallback_system'|'system_key', key_index: i, total_user_keys: N }`.
   - **Thông báo & Nhật ký (Log & Toast)**:
     - Ghi nhận trạng thái rõ ràng trên khung log của Canvas:
       - Ví dụ: `[AI] Đang sinh Phụ lục 1 bằng Gemini 3.8 Flash (Key cá nhân 1/3)...`
       - Khi xoay key: `[AI] Key cá nhân 1 chạm hạn mức, tự động chuyển sang key 2/3...`
       - Khi fallback: `[AI] Key cá nhân tạm hết hạn mức, tự động chuyển về Gemini 3 Flash Preview nội bộ.`
3. **Bảo toàn kiểm thử & Chuẩn sandbox**:
   - Cập nhật `tests/canvas-xaydungphuluc-smoke.js` để kiểm thử logic đa tầng, hiển thị badge số lượng key và cơ chế fallback mà vẫn đảm bảo 100% tuân thủ sandbox (không gọi trực tiếp domain bị cấm từ client).

## Ngoài phạm vi
- Không thay đổi bất kỳ logic sư phạm hay quy tắc nghiệp vụ nào đã ổn định của Phụ lục 1, 2, 3 (không thay đổi thuật toán phân bổ NLS/AI, bảo toàn bảng PPCT, cấu trúc 7 cột/8 cột, công thức KaTeX, bộ xuất Word `exportDocx`).
- Không sửa file `xaydungphuluc.html` (chỉ áp dụng cho bản Canvas `canvas_xaydungphuluc.html` và backend `api/canvas_gemini.php`).
- Không sửa đổi cấu trúc bảng CSDL `users` (tận dụng cột `gemini_keys` đã có).

## File dự kiến tác động
- `api/canvas_gemini.php`: Bổ sung xử lý `action=key_status` kiểm tra số lượng key user; bổ sung định tuyến đa tầng (`tier: 'heavy_io' | 'high_reasoning'`), xoay vòng key user cho `gemini-3.8-flash` và fallback về `gemini-3-flash-preview`.
- `canvas_xaydungphuluc.html`:
  - Thêm badge hiển thị số lượng key và trạng thái kết nối tài khoản trên Header.
  - Cập nhật hàm `updateCanvasKeyBadge`, `openKeyModal`, `fetchCanvasKeyStatus`.
  - Phân loại tham số `tier` và `preferred_model` trong `requestGemini` và `callGemini`.
  - Hiển thị thông báo trạng thái xoay key và fallback trên giao diện và log.
- `tests/canvas-xaydungphuluc-smoke.js`: Cập nhật các khẳng định kiểm thử về multi-tier routing, badge hiển thị key count và đảm bảo toàn bộ bộ test cũ tiếp tục PASS.

## Các bước thực hiện
### Bước 1: Nâng cấp Backend `api/canvas_gemini.php`
1. Đón nhận `X-User-Account` từ Header hoặc `user_account` từ query/body. Giải mã URI an toàn.
2. Thêm endpoint kiểm tra trạng thái key:
   - Nếu `action === 'key_status'` (hoặc qua GET `?action=key_status&user_account=...`):
     - Truy vấn `users` theo `username` hoặc prefix email.
     - Đọc và giải mã `gemini_keys` bằng `parse_stored_api_keys`.
     - Trả về JSON:
       ```json
       {
         "ok": true,
         "user_account": "...",
         "key_count": N,
         "masked_keys": ["AIzaSy...****"],
         "has_user_keys": true
       }
       ```
3. Nâng cấp luồng xử lý gọi Gemini trong `canvas_gemini.php`:
   - Tiếp nhận `$body['tier']` (`'heavy_io'` hoặc `'high_reasoning'`) và `$body['preferred_model']` (mặc định `'gemini-3.8-flash'` cho high-reasoning).
   - Nếu `$tier === 'high_reasoning'` và có `user_account`:
     - Lấy danh sách keys người dùng `$userKeys`.
     - Lặp qua `$userKeys`, gọi API tới `gemini-3.8-flash`.
     - Nếu trả về 200: trả về ngay với metadata `{ ok: true, body: ..., model: 'gemini-3.8-flash', tier: 'user_key', key_index: $idx + 1, total_user_keys: count($userKeys) }`.
     - Nếu trả về 429 hoặc lỗi quota: ghi nhận lỗi, tiếp tục vòng lặp sang key kế tiếp của user.
   - Nếu toàn bộ key của user hết hạn mức HOẶC tác vụ là `heavy_io` HOẶC không có user keys:
     - Fallback sang danh sách `$runtime['gemini_keys']` hệ thống với model `gemini-3-flash-preview`.
     - Trả về metadata `{ ok: true, body: ..., model: 'gemini-3-flash-preview', tier: 'system_key', fallback_used: true }`.

### Bước 2: Nâng cấp Frontend `canvas_xaydungphuluc.html`
1. Khai báo các biến trạng thái:
   - `let canvasUserKeyCount = 0, canvasUserMaskedKeys = [];`
2. Viết hàm `syncCanvasUserKeyStatus(account)`:
   - Gửi fetch tới `CANVAS_ENDPOINT + '?action=key_status&user_account=' + encodeURIComponent(account)`.
   - Lưu `canvasUserKeyCount` và gọi `updateCanvasKeyBadge()`.
3. Nâng cấp hiển thị Badge trên Header:
   - Thay thẻ span tĩnh trên Header bằng element tương tác có id `canvasKeyBadge`:
     - Khi `canvasUserKeyCount > 0`: hiển thị `⚡ Gemini 3.8 Flash · [account] ([count] keys)` với nút bấm mở Modal Key.
     - Khi `0 keys`: hiển thị `🛡 Gemini 3 Flash Preview (Nội bộ)` + nút `[Kết nối Key]`.
4. Cập nhật Modal `#keyModal`:
   - Hiển thị tài khoản giáo viên đang kết nối.
   - Hiển thị số lượng API Key đã nạp trên hệ thống và danh sách các key đã được che mờ (`masked_keys`).
   - Có nút "Kiểm tra & Đồng bộ lại" để cập nhật ngay khi giáo viên vừa thêm key trên trang cá nhân.
5. Phân tầng gọi API trong các hàm:
   - `recognizePpctWithAi`: gọi qua `callGemini(prompt, { tier: 'heavy_io' })`.
   - `buildSgkKnowledgeBase`: gọi qua `callAiJson(prompt, { tier: 'heavy_io' })`.
   - `generateSelected` (sinh Phụ lục 1, 2, 3): gọi qua `callGemini(prompt, { tier: 'high_reasoning', preferredModel: 'gemini-3.8-flash' })`.
6. Cập nhật `readGeminiResponse` và hiển thị nhật ký:
   - Bóc tách `envelope.tier`, `envelope.model`, `envelope.fallback_used`.
   - Nếu `tier === 'user_key'`: log `✓ Sử dụng Gemini 3.8 Flash (Key cá nhân ${envelope.key_index}/${envelope.total_user_keys})`.
   - Nếu `fallback_used`: log và thông báo nhẹ `⚠ Key cá nhân chạm hạn mức, đã tự động chuyển về Gemini 3 Flash Preview nội bộ.`

### Bước 3: Cập nhật Smoke Test
1. Mở rộng `tests/canvas-xaydungphuluc-smoke.js`:
   - Xác nhận có `canvasKeyBadge`, hàm `updateCanvasKeyBadge`, hàm `syncCanvasUserKeyStatus`.
   - Xác nhận tham số `tier` được truyền đúng ở các luồng I/O và reasoning.
   - Kiểm thử contract của `canvas_gemini.php` khi nhận `action=key_status` và khi gọi với `tier`.
   - Đảm bảo kiểm thử cũ không bị vi phạm (giữ nguyên không gọi trực tiếp domain ngoài từ client).

## Rủi ro
- **Rủi ro 1: Vi phạm CSP/CORS của Google Canvas Sandbox.**
  - *Biện pháp*: Giữ nguyên nguyên tắc toàn bộ yêu cầu đều đi qua proxy `CANVAS_ENDPOINT` (`api/canvas_gemini.php`), client không gọi trực tiếp Google AI hay CSDL.
- **Rủi ro 2: Key cá nhân của user bị cạn quota (429) làm gián đoạn việc soạn giáo án.**
  - *Biện pháp*: Vòng lặp xoay key tự động; nếu hết toàn bộ lập tức trượt nhẹ nhàng (Graceful Fallback) về hệ thống nội bộ `gemini-3-flash-preview`.
- **Rủi ro 3: Model 3.8 Flash trả về cú pháp JSON khác lạ.**
  - *Biện pháp*: Đã có `safeParseAiJson` đã qua kiểm nghiệm nhiều cấp (tự escape newline, tab, khôi phục markdown, bọc LaTeX) đảm bảo phân tích an toàn.

## Cách kiểm thử
1. Chạy smoke test tự động: `node tests/canvas-xaydungphuluc-smoke.js`.
2. Kiểm tra các kịch bản thực tế:
   - Kịch bản A: Tài khoản có 2 keys -> Gọi thành công với `gemini-3.8-flash`, badge hiển thị `(2 keys)`.
   - Kịch bản B: Key 1 bị lỗi 429 -> Hệ thống tự động chuyển sang Key 2 để hoàn tất yêu cầu.
   - Kịch bản C: Tất cả key cá nhân đều 429 hoặc tài khoản không có key -> Tự động fallback sang `gemini-3-flash-preview` nội bộ, thông báo rõ ràng cho giáo viên.
   - Kịch bản D: Tác vụ đọc SGK hoặc nhận diện PPCT -> Luôn chạy trên `gemini-3-flash-preview` nội bộ để tiết kiệm token.
3. Kiểm tra xuất file Word: Đảm bảo bảng Phụ lục 1, 2, 3 giữ nguyên 100% định dạng, merge tiêu đề, công thức toán và mã NLS/AI.

## Tiêu chí nghiệm thu
- [ ] Giao diện Canvas hiển thị trực quan số lượng API key của tài khoản người dùng (`N keys`).
- [ ] Cho phép kết nối và kiểm tra đồng bộ API key của tài khoản giáo viên.
- [ ] Tác vụ đọc SGK và nhận diện PPCT chạy qua tầng nội bộ `gemini-3-flash-preview` (`tier: 'heavy_io'`).
- [ ] Tác vụ sinh nội dung Phụ lục 1, 2, 3 ưu tiên chạy `gemini-3.8-flash` với key cá nhân (`tier: 'high_reasoning'`).
- [ ] Khi key cá nhân gặp lỗi 429, tự động xoay sang key kế tiếp; nếu hết thì tự động fallback về model nội bộ.
- [ ] Giữ nguyên 100% logic sư phạm, bảng dữ liệu và tính năng xuất file Word.
- [ ] Lệnh kiểm thử `node tests/canvas-xaydungphuluc-smoke.js` PASS 100%.
