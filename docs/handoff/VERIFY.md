# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Tính năng 1: Kéo thả tiết học (Drag & Drop) trên lưới TKB Sáng và Chiều (`phancongtochuyenmon.html`):
  + Đã thêm thuộc tính `draggable="true"` cho các ô có dữ liệu.
  + Đã bắt sự kiện `ondragstart`, `ondragover`, `ondragleave`, `ondrop`.
  + Đã xử lý di chuyển sang ô trống và hộp thoại lựa chọn Hoán đổi (Swap) / Ghi đè (Overwrite) khi ô đích đã có tiết.
  + Tự động lưu local, vẽ lại lưới và đồng bộ phân công giảng dạy khi bật tự động: ĐÚNG PHẠM VI.
- Tính năng 2: Thêm Tab "9. Đánh giá xếp loại" với xếp loại A, B, C, D và Ghi chú (`phancongtochuyenmon.html`):
  + Đã thêm nút tab `tab-nav-danhgia` và container `view-danhgia`.
  + Bảng đầy đủ các cột: STT, Họ và tên, Chức vụ, Số tiết/tuần, Số liệu chấm công tham khảo, Dropdown xếp loại A, B, C, D (kèm mã màu trực quan), Input Ghi chú.
  + Các nút tiện ích: Xếp nhanh tất cả là A, Gợi ý theo chấm công, Xuất file Excel, Lưu CSDL: ĐÚNG PHẠM VI.
  + Cấu trúc dữ liệu lưu trong `state.evaluations.records[monthKey][teacherId] = { rating, note }`, đồng bộ LocalStorage và CSDL: ĐÚNG PHẠM VI.
- Test tự động trong `tests/timetable-render-smoke.js`: ĐÚNG PHẠM VI.
- Không sửa ngoài phạm vi, không tác động file khác.

## Test đã chạy
1. `node tests/timetable-render-smoke.js` → PASS (exit 0)
   - Kiểm thử sự hiện diện của nút tab `tab-nav-danhgia` và container `view-danhgia`.
   - Kiểm thử thuộc tính `draggable="true"` trên ô tiết có dữ liệu.
   - Kiểm thử logic di chuyển tiết sang ô trống (`action = 'move'`) xóa ô nguồn và điền ô đích, kể cả khác buổi (`morning` sang `afternoon`).
   - Kiểm thử logic hoán đổi vị trí 2 tiết (`action = 'swap'`) đổi chỗ chính xác giữa ô nguồn và ô đích.
   - Kiểm thử lưu trữ xếp loại A–D và ghi chú theo từng giáo viên và từng tháng.
   - Kiểm thử tự động lưu local và đánh dấu chưa lưu CSDL (`hasUnsavedChanges = true`).
   - Toàn bộ các ca kiểm thử TKB trước đó (nhận diện Tiết 7, dải tiết 6–9/7–9, modal khung tiết...) tiếp tục PASS 100%.

## Pass / Fail từng tiêu chí
- Kéo thả di chuyển ô tiết sang ô trống: PASS
- Kéo thả hoán đổi hoặc ghi đè khi ô đích đã có tiết: PASS
- Tab 9 Đánh giá xếp loại hiển thị 4 mức chuẩn A, B, C, D: PASS
- Có cột Ghi chú cho từng giáo viên: PASS
- Lưu trữ trạng thái đánh giá và đồng bộ CSDL: PASS
- Smoke test `tests/timetable-render-smoke.js`: PASS

## Bug
(Không có)
