# IMPLEMENT: Thêm Nút Cài Đặt AI & Đăng Ký Khóa API Trên Trang Chủ Người Dùng

**Ngày implement**: 2026-09-03
**Coder**: Grok (xAI)
**Trạng thái**: DONE — 6 smoke tests PLAN yêu cầu đều PASS

## Tóm tắt thay đổi

### Bước 1: Module `js/user-ai-settings.js` (tạo mới)
- `window.UserAiSettings` với `ensureModal`, `openModal`, `closeModal`, `handleFile`, `testGeminiKeys`, `saveSettings`, `deleteKeys`, `updateBadge`.
- Modal `#userAiSettingsModal`: Tailwind, responsive, backdrop blur.
- Dropdown module Gemini (`gemini-2.5-flash`, `gemini-3-flash-preview`, `gemini-2.5-pro`, …) lưu cả `default_gemini_module` và `khbd_gemini_model`.
- Textarea Gemini + Mistral, nạp từ file `.txt`.
- Lưu `POST api/user_gemini_keys.php`; đồng bộ `global_gemini_keys`, `global_mistral_keys` và cache theo tài khoản.
- Kiểm tra key: `POST action=test`; xóa key: `DELETE`.
- 401 hiện "Vui lòng đăng nhập lại" thay vì lỗi mơ hồ.
- Ẩn nút với vai trò `student`.

### Bước 2: Tích hợp `index.html`
- Navbar: nút `#btnOpenUserAiSettings` — "Cài đặt AI & Key", icon `fa-sliders-h`, cạnh Đăng xuất.
- Hero giáo viên (`renderTeacherLotrinhPanel`): badge `#heroKeyStatus` dưới "Xin chào, {teacherName}".
- Nhúng `<script src="js/user-ai-settings.js"></script>` trước script khởi tạo hub.

### Bước 3: Kiểm thử
- Tạo `tests/user-ai-settings-smoke.js`.
- Chạy đủ suite PLAN: user-ai-settings, khbd-user-ai-keys, matrande, kttx, xaydungphuluc, duyetgiaoan.

## Files đã sửa / tạo

| File | Thay đổi |
|------|----------|
| `js/user-ai-settings.js` | Tạo mới — modal & logic cài đặt AI / API Key |
| `index.html` | Nút navbar, badge hero, nhúng script |
| `tests/user-ai-settings-smoke.js` | Tạo mới — smoke test tính năng |

Không đụng bảng `users`, không đổi AES-256-CBC, không đổi luồng học sinh.

## Kết quả kiểm thử

```
user-ai-settings smoke: passed
khbd user AI keys smoke: passed
matrande smoke: Word templates and account Gemini key synchronization passed
kttx smoke: Word templates and account Gemini key synchronization passed
PASS xaydungphuluc smoke: PPCT 7-column form, independent table ingest, no admin-header leak, density ranges and auto-hiding progress UI are present.
duyetgiaoan smoke: passed
```

Không chạy được kiểm thử trình duyệt end-to-end (không có browser tool trong phiên này). Luồng đăng nhập giáo viên → bấm Cài đặt AI & Key → lưu/test key thuộc bước `/verify`.
