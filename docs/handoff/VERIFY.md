# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Sửa quy tắc CSS `.nav-chip`: loại bỏ màu chữ xám trắng cũ `#e2e8f0`, chuyển sang nền `#f1f5f9` và chữ sẫm `#334155` rõ nét trên nền navbar sáng `index.html`.
- Sửa huy hiệu Cổng Học Sinh trong JS: gán lớp `text-emerald-800` và thuộc tính màu tường minh `style.color = '#065f46'`, icon `text-emerald-600`. Chữ hiển thị đậm, độ tương phản sắc nét trên nền `bg-emerald-50`, không còn bị điệp màu nền.
- Sửa chip giáo viên `Cập nhật đồng bộ` trong HTML: chuyển sang `bg-slate-100 text-slate-700 border-slate-200` và icon `text-indigo-500`, hiển thị rõ ràng trên nền sáng.
- Bổ sung smoke test tự động `tests/nav-chip-contrast-smoke.js` kiểm tra toàn diện hợp đồng CSS, JS và HTML.

## Test đã chạy
- `node tests/nav-chip-contrast-smoke.js`: PASS (100%)
- `node tests/teacher-permissions-smoke.js`: PASS (100%)

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Huy hiệu "Cổng Học Sinh" có chữ màu xanh ngọc bích sẫm `#065f46` (`text-emerald-800`), tương phản cao, không bị chìm/điệp với màu nền: PASS
- Tiêu chí 2: Chip giáo viên "Cập nhật đồng bộ" có chữ xám sẫm `#334155` (`text-slate-700`) trên nền xám nhạt `bg-slate-100`, không còn tình trạng chữ trắng trên nền trắng: PASS
- Tiêu chí 3: Bộ kiểm thử tự động `tests/nav-chip-contrast-smoke.js` và `tests/teacher-permissions-smoke.js` vượt qua 100%: PASS

## Bug
Không có.
