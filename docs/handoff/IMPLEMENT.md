# IMPLEMENT — Hiển thị văn bản đã lưu

Trạng thái: đã sửa theo `docs/handoff/PLAN.md`. Sẵn sàng cho `/verify`.

## Đã làm
- `api/vanban.php`: schema marker `20260929-v2`; chuẩn hóa `sector`, `direction`, `academic_year` cũ; `action=list` cho admin xem toàn trường, giáo viên xem văn bản của mình và legacy (`owner_id = 0 OR owner_id IS NULL`); lĩnh vực hành chính gồm `sector` NULL/rỗng; `vbd_document` / `vbd_owned_documents` cùng quy tắc, vẫn giữ chuỗi `owner_id = ? AND id IN`.
- `vanban-app.js`: bộ lọc năm mặc định "Tất cả năm học", thêm "Chưa gán năm học" (`__empty__`); không ép `years[0]`; `direction` trống tính là văn bản đến trong danh sách, tab và thống kê.
- `vanban-hub.js`: thống kê hub dùng cùng fallback `direction`.
- `quanlyvanban.html`, `quanlyvanban-chuyenmon.html`, `quanlyvanban-hanhchinh.html`, `quanlyvanban-dang.html`: query `?v=20260929-showdocs` (trang Đảng gồm cả `access-control.js`).
- `tests/vanban-display-saved-smoke.js`: kiểm tra lọc năm, direction trống và các marker PHP.

## Kiểm thử
- `tests/vanban-chuyenmon-signature-smoke.js`: PASS
- `tests/vanban-display-saved-smoke.js`: PASS

Không commit.
