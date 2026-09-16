# IMPLEMENT: Sửa FAIL VERIFY — regex phân vai sticky và model Canvas

Đã sửa đúng 2 bug trong `docs/handoff/VERIFY.md`:

1. `formatKhbdRoleLine` dùng negative lookbehind `của` để tách lượt lời `GV:` / `HS:` sau ngoặc, hai chấm, `|`, ô bảng; không chèn `<br>- ` vào `Nhận xét của GV:`.
2. `canvas_soankhbd.html` đồng bộ model hệ thống `gemini-2.5-flash` (config, UI, fallback).

File: `js/khbd-app.js`, `canvas_soankhbd.html`, `backupcode viettailieu/canvas_soankhbd.html`, `tests/khbd-pedagogy-rate-smoke.js`.

## Lịch sử

# IMPLEMENT: Phụ lục E và định dạng phân vai

Đã xóa thời lượng Phụ lục E, chuyển thẻ br sang xuống dòng khi xuất Word và giới hạn định dạng GV/HS vào đầu lượt lời để không sửa cụm Nhận xét của GV.
