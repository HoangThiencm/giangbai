# IMPLEMENT: matrande.html — Xuất Word + đồng bộ Gemini API Key

## Đã làm

1. **Sửa lỗi xuất Word** trong `matrande.html`:
   - Xóa thẻ `<script src="js/security-guard.js"></script>` khỏi template HTML của `exportWord` và `exportWordRaw`.
   - Khối `<script type="text/babel">` không còn bị HTML parser đóng sớm; hai hàm xuất Word giữ `<meta charset='utf-8'>` và namespace Word/OMML.

2. **Tự động đồng bộ Gemini API Key theo tài khoản**:
   - Thêm `normalizeGeminiKeys`, `readCachedGeminiKeys`, `syncUserKeysFromServer()`.
   - `syncUserKeysFromServer()` gọi `GET api/user_gemini_keys.php` với `credentials: 'include'` và `cache: 'no-store'`.
   - Khi React mount, `useEffect` nạp key, ghi cache `localStorage('global_gemini_keys')` nếu server trả key, fallback cache khi mất mạng/lỗi.
   - Giao diện hiển thị số lượng key đã nạp (`🔑 Đã nạp N Gemini API Key từ tài khoản/từ bộ nhớ tạm`).

3. **Kiểm thử** `tests/matrande-smoke.js`:
   - Babel script nguyên vẹn, không có thẻ `<script>` lồng trong template Word.
   - `exportWord` / `exportWordRaw` có charset UTF-8 và blob `application/msword`.
   - Có `syncUserKeysFromServer` + nạp key khi mount + fallback cache.

## File đã sửa / tạo

- `matrande.html`
- `tests/matrande-smoke.js` (tạo mới)
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock` (LOCK)

## Kiểm thử

- `node tests/matrande-smoke.js` — PASS
- `node tests/kttx-smoke.js` — PASS
- `node tests/xaydungphuluc-smoke.js` — PASS

Không verify trên trình duyệt (không có browser tools trong phiên này).

## Bổ sung: quyền Duyệt Giáo Án AI cho từng giáo viên

- Thêm `duyetgiaoan` vào `CLIENT_FEATURE_CHECKS`, `USER_FEATURE_GROUPS` và nhóm quyền trang của giáo viên trong `admin.html`.
- Khi tạo/sửa/cấp toàn quyền giáo viên, `teacherFeatureFlagsFromPages()` nay đồng bộ `duyetgiaoan: true/false` vào `user_features` theo `allowed_pages`; checkbox cũng xuất hiện trong nhóm Công cụ giảng dạy.
- `node tests/duyetgiaoan-integration-smoke.js` — PASS.
- `node tests/duyetgiaoan-smoke.js` — PASS.
- `git diff --check` — PASS.
