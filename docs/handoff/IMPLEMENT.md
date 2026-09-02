# IMPLEMENT: Tích hợp rà soát & hiệu chỉnh đề kiểm tra (`duyetde`) + mã hóa API key

## Đã làm

1. **Bảo mật API key (AES-256-CBC)** trong `api/helpers.php` và `api/user_gemini_keys.php`:
   - Thêm `encrypt_user_api_key()` / `decrypt_user_api_key()` dùng `openssl_encrypt`/`openssl_decrypt`, thuật toán `AES-256-CBC`, secret suy từ `API_KEY_ENCRYPTION_SECRET` hoặc `ADMIN_KEY`.
   - Lưu key dạng envelope JSON `{v, alg, updated_at, keys:[enc:v1:...]}`.
   - Key cũ plaintext được tự nhận diện và nâng cấp khi GET/POST.
   - GET không trả raw key: chỉ `count`, `masked_keys` (`AIzaSy...****`), `updated_at`.
   - POST `action=add` thêm key, `action=test` kiểm tra key trên máy chủ, DELETE xóa danh sách.
   - Mỗi user chỉ đọc/ghi key của session mình.

2. **AI Gateway** `api/duyetde_ai.php`:
   - Lấy key đã giải mã từ CSDL theo session, gọi Gemini qua cURL.
   - `call_gemini_with_rotation()` xoay vòng khi 429/403/quota/resource exhausted.
   - `generate_solution`, `evaluate_exam`, `recheck_question` (alias `recheck_single_question`).
   - Gửi đồng thời văn bản trích xuất và PDF base64 (multimodal). Chuẩn hóa 4 trạng thái: Đạt / Cần chỉnh sửa / Không đạt / Chưa đủ dữ liệu để kết luận.

3. **Lưu hồ sơ & phiên bản** `api/duyetde.php`:
   - `ensure_duyetde_sessions()` tạo bảng đúng schema PLAN.
   - list / chi tiết / lưu-cập nhật / xóa / nộp tổ trưởng (`submit`) / quyết định (`decide`: Có thể sử dụng / Cần chỉnh sửa / Không sử dụng).

4. **Giao diện** `duyetde.html` — 5 phân khu:
   - Hồ sơ đợt duyệt + quản lý API key (masked, thêm, test, xóa).
   - Nạp Đề thi, Ma trận, Bảng đặc tả (bắt buộc) và Đáp án (tùy chọn) PDF/DOCX qua `pdf.js` + `mammoth.js`; KaTeX cho công thức.
   - Thanh tiến trình 2 pha, thống kê, bảng đối chiếu màu theo state machine.
   - Gợi ý sửa độc lập: Chấp nhận / Tự chỉnh sửa / Giữ gốc; mỗi lần sửa tạo vN, gắn cờ kiểm tra lại, hủy trạng thái Đạt của đề.
   - Tổ trưởng kết luận + xuất biên bản và đề hoàn chỉnh `.docx` (`docx.js`).

5. **Phân quyền**:
   - `admin.html`: `cfg_duyetde`, `CLIENT_FEATURE_CHECKS`, `FEATURE_NAMES`, `USER_FEATURE_GROUPS`, `hostingPages`, `teacherFeatureGroups`.
   - `access-control.js`: `'duyetde.html': 'duyetde'` và `duyetde: 'duyetde.html'`.
   - `api/helpers.php`: `page_catalog()`, `teacher_workspace_page_ids()`, `teacher_feature_keys_for_pages()`, `teacher_default_workspace_extras()`.
   - `index.html`: thẻ "Rà soát & Hiệu chỉnh Đề Kiểm Tra" (`fa-file-shield`, nhãn CV 5512 · Ma trận – Đặc tả).

6. Ghi `LOCK` vào `docs/handoff/.lock`.

## File đã sửa / tạo

- `duyetde.html` (tạo mới)
- `api/duyetde.php` (tạo mới)
- `api/duyetde_ai.php` (tạo mới)
- `api/user_gemini_keys.php`
- `api/helpers.php`
- `access-control.js`
- `admin.html`
- `index.html`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock` (LOCK)

## Kiểm thử

- `node tests/khbd-user-ai-keys-smoke.js` — PASS
- `node tests/duyetgiaoan-integration-smoke.js` — PASS
- `node tests/duyetgiaoan-smoke.js` — PASS
- `node tests/matrande-smoke.js` — PASS
- Không có PHP CLI trên máy này nên chưa `php -l`.
- Không verify trên trình duyệt (không có browser tools / PHP server trong phiên này).

## Phạm vi

- Không sửa `matrande.html`, `soankhbd.html`, `duyetgiaoan.html`, `thitructuyen.html`.
- Không sửa `docs/handoff/PLAN.md`.
- Không commit.

## Lưu ý

- GET `api/user_gemini_keys.php` không còn trả mảng `keys` gốc. Các công cụ cũ gọi Gemini từ trình duyệt vẫn dùng key đã cache local hoặc key user nhập trực tiếp; module `duyetde` gọi AI qua backend proxy.
- `me.php` / `public_user()` vẫn giải mã key phía server để tương thích KHBD; client `duyetde` không đọc raw key từ GET.
