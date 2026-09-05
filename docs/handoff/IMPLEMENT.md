# IMPLEMENT: Tái cấu trúc giao diện + Tab Sổ Dạy Thay riêng + Period Slots Builder

**Ngày implement**: 2026-09-06
**Coder**: Grok (xAI)
**Trạng thái**: DONE

## Tóm tắt

1. **Header 2 tầng**: Tầng 1 Brand + Lưu CSDL + Khai báo tổ + menu Công cụ/Tệp + Trang chủ. Tầng 2 gồm 5 tab làm việc và bộ chọn Đợt ở bên phải.
2. **Tab 2 `view-daythay`**: Sổ Dạy Thay - Bù toàn trang, thay hoàn toàn modal cũ. Form ghi nhận/sửa, thống kê tháng, nhật ký lọc, xuất Excel riêng, đồng bộ sang Chấm công.
3. **Period Slots Builder**: Chọn từng tiết 1–5 kèm lớp/môn; `period_count` tự tính; giữ tương thích dữ liệu cũ (`period`, `class_name`, `period_count`).

## Files

| File | Thay đổi |
|------|----------|
| `phancongtochuyenmon.html` | Tái cấu trúc header/tabs, view `view-daythay`, CSS sticky/slots, JS save/edit/excel/sync |
| `docs/handoff/IMPLEMENT.md` | Ghi nhận implement |
| `docs/handoff/.lock` | Khóa lại sau khi sửa |

Không sửa `api/phancong.php` hay schema MySQL.

## Chi tiết kỹ thuật

- Dữ liệu mới: `periods_detail: [{ period_num, class_name, subject, note }]`, đồng thời ghi `period_count`, `period`, `class_name` để bản cũ vẫn đọc được.
- Bản ghi cũ không có `periods_detail`: fallback parse chuỗi `period` hoặc tick tiết 1..N theo `period_count`.
- `autoSyncSubstitutePeriods()` vẫn ghi `teach_replace` / `makeup_periods` vào bảng chấm công (dùng `period_count || periods_detail.length || 1`).
- Tab Chấm công: nút **Xem chi tiết Sổ Dạy Thay (X lượt)** gọi `switchAppView('view-daythay')`.

## Kiểm thử Coder đã chạy

1. `node tests/smartquiz-smoke.js` → PASS (giữ `downloadExcelFile` + không lồng `</script>`).
2. Syntax check khối JS inline của `phancongtochuyenmon.html` → OK, không trùng `id`.

Chưa chạy được kiểm thử trình duyệt end-to-end (không có browser tool trong phiên này). `/verify` cần mở file trên trình duyệt theo mục *Cách kiểm thử* trong `PLAN.md`.
