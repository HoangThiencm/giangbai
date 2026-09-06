# IMPLEMENT: Tab Thời khoá biểu GV toàn trang + nhận diện hàng loạt, lưu local liên tục

**Ngày implement**: 2026-09-07
**Coder**: Grok (xAI)
**Trạng thái**: DONE

## Tóm tắt

Tách TKB khỏi modal thành Tab `2. Thời khoá biểu GV` (`#view-timetable`): cột trái danh sách GV + trạng thái, cột phải workspace dán ảnh / AI / lưới tuần. AI nhận diện xong lưu ngay `localStorage`; lưu MySQL 1 lần bằng **Lưu tất cả lên CSDL**.

## Files

| File | Thay đổi |
|------|----------|
| `phancongtochuyenmon.html` | Tab mới, view 2 cột, bỏ modal TKB (tránh trùng ID), auto-save local, điều hướng GV |
| `docs/handoff/IMPLEMENT.md` | Ghi nhận implement |
| `docs/handoff/.lock` | Khóa lại |

Không sửa `api/phancong.php` / `api/khbd_gemini.php`.

## Chi tiết

- Tab: 1 Phân công · 2 TKB GV · 3 Sổ Dạy Thay · 4 Chấm công · 5 Tăng giờ · 6 Báo cáo.
- `openTeacherTimetableModal(id)` → `switchAppView('view-timetable')` + `selectTimetableTeacher(id)`.
- Paste Ctrl+V chỉ khi `#view-timetable` đang active.
- `applyAiTimetableResult` / sửa ô: `persistTeacherTimetable` + `saveToLocal({ autoSave: false })` + `hasUnsavedChanges`.
- Nút **GV tiếp theo** nhảy GV chưa có TKB; **Lưu tất cả lên CSDL** gọi `saveToDB()`.

## Kiểm thử Coder

1. JS parse OK; 134 ID duy nhất; không còn `#teacher-timetable-modal`.
2. `node tests/smartquiz-smoke.js` → PASS.

`/verify` theo *Cách kiểm thử* trong `PLAN.md`.
