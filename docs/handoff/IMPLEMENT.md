# IMPLEMENT: Hero/Theo dõi vào Modal Setting + 3 tab Canvas phân quyền Admin

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Module 1 — Modal Setting 2 tab (`js/user-ai-settings.js` + `index.html`)

- Modal mở rộng `max-w-5xl`; thanh tab:
  - Tab 1 `#tabBtnOverview` / `#userAiTabOverview`: mount `#teacherLotrinhPanel` (hero Xin chào, lớp phụ trách, hành động theo dõi, AI stats).
  - Tab 2 `#tabBtnKeys` / `#userAiTabKeys`: form model Gemini/fallback, key Gemini & Mistral, nạp file, test/lưu/xóa.
- Thêm `UserAiSettings.switchTab('overview'|'keys')`; `openModal(tabName)` chọn tab.
- `#heroKeyStatus` gọi `openModal('keys')`; navbar `#btnOpenUserAiSettings` vẫn `openModal()`.
- `setupTeacherLotrinhHub()` gọi `UserAiSettings.ensureModal()` rồi render hero vào panel trong modal; `#teacherLotrinhHub` trên trang chủ giữ `hidden` (tools deck nổi bật).

## Module 2 — 3 Canvas + phân quyền

- `api/helpers.php`: `page_catalog`, `teacher_workspace_page_ids`, `teacher_feature_keys_for_pages` thêm `canvas_soankhbd`, `canvas_soanlotrinh`, `canvas_sangkien`.
- `global_config.json` `features`: 3 key = `true`.
- `admin.html`: `CLIENT_FEATURE_CHECKS`, `FEATURE_NAMES`, `USER_FEATURE_GROUPS`, `hostingPages`, `teacherFeatureGroups`, checkbox `cfg_canvas_*`.
- `index.html`: `TOOL_PAGE_LINKS` + 3 thẻ bento (Indigo/Teal/Pink); gỡ thẻ cũ `vietsangkien`.

## Smoke mới

- `tests/canvas-tabs-permissions-smoke.js`: đăng ký 3 tab (helpers/admin/index/config), bỏ `vietsangkien`, modal 2 tab + `ensureModal` + `heroKeyStatus` → keys.

## Test đã chạy

- `node tests/canvas-tabs-permissions-smoke.js` — PASS
- `node tests/teacher-permissions-smoke.js` — PASS
- `node tests/user-ai-settings-smoke.js` — PASS
- `node tests/duyetgiaoan-integration-smoke.js` — PASS

Không thêm chức năng ngoài plan. Browser MCP không có trong session — chưa verify click UI trực tiếp; hợp đồng static đã PASS. Cần `/verify` trên Antigravity.
