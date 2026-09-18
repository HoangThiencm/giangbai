# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Chuyển giao diện hero / theo dõi giáo viên (như trong ảnh) vào bên trong modal setting (`UserAiSettings.openModal()`):
  - Modal được mở rộng kích thước `max-w-5xl`.
  - Bổ sung thanh tab chuyển đổi: Tab 1 "Tổng quan & Theo dõi" chứa container `#teacherLotrinhPanel`; Tab 2 "Cài đặt AI & API Key" chứa form cấu hình model và API keys.
  - Thêm phương thức `UserAiSettings.switchTab()` và hỗ trợ `openModal(tabName)`. Nút `#heroKeyStatus` chuyển thẳng sang tab `keys`.
  - Trên trang chủ `index.html`, `#teacherLotrinhHub` giữ ẩn (`hidden`) để bộ công cụ bento hiển thị trực tiếp ở đầu trang.
- [x] Thêm 3 tab Canvas mới với link mở tab mới (`target="_blank"`):
  - `CANVAS_SOANKHBD`: `https://gemini.google.com/app/74fb6bf46c11076a?hl=vi` (key `canvas_soankhbd`)
  - `CANVAS_SOẠN LỘ TRÌNH`: `https://gemini.google.com/app/0fdb1756f609d61f?hl=vi` (key `canvas_soanlotrinh`)
  - `CANVAS_SÁNG KIẾN`: `https://gemini.google.com/app/e6bf41201af60de3?hl=vi` (key `canvas_sangkien`)
- [x] Tích hợp phân quyền Admin đầy đủ:
  - Khai báo trang trong `page_catalog()`, `teacher_workspace_page_ids()`, `teacher_feature_keys_for_pages()` tại `api/helpers.php`.
  - Bật cấu hình mặc định trong `global_config.json` (`features`).
  - Quản trị bật/tắt toàn cục và cấp quyền theo tài khoản giáo viên trong `admin.html` (`CLIENT_FEATURE_CHECKS`, `FEATURE_NAMES`, `USER_FEATURE_GROUPS`, `hostingPages`, `teacherFeatureGroups`, `cfg_canvas_*`).
  - Lọc quyền chặt chẽ trên `index.html` qua `TOOL_PAGE_LINKS` và `applyTeacherAllowedPagesVisibility()`.
  - Dọn sạch thẻ cũ `vietsangkien` không quản trị quyền.

## Test đã chạy
- `node tests/canvas-tabs-permissions-smoke.js` — PASS 100%
- `node tests/teacher-permissions-smoke.js` — PASS 100%
- `node tests/user-ai-settings-smoke.js` — PASS 100%
- `node tests/duyetgiaoan-integration-smoke.js` — PASS 100%
- `node tests/nghiencuubaihoc-smoke.js` — PASS 100%

## Pass / Fail từng tiêu chí
1. Modal Setting 2 tab (Tổng quan & Theo dõi / Cài đặt AI & Key): PASS
2. Tích hợp giao diện hero/stats vào `#teacherLotrinhPanel` trong modal: PASS
3. Giữ `#teacherLotrinhHub` ẩn trên homepage: PASS
4. Đăng ký `canvas_soankhbd` link Gemini Canvas + quyền Admin: PASS
5. Đăng ký `canvas_soanlotrinh` link Gemini Canvas + quyền Admin: PASS
6. Đăng ký `canvas_sangkien` link Gemini Canvas + quyền Admin: PASS
7. Mở liên kết `target="_blank"` và styling bento card: PASS
8. Không có regression trên các smoke test phân quyền và cài đặt AI: PASS

## Bug
- Không phát hiện lỗi.
