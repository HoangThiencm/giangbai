# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Modal Cấu hình PPCT & Lịch nghỉ: `#baogiang-config-modal` được tạo đầy đủ với 2 phần (Khai báo/nạp PPCT và Ngoại lệ nghỉ/dạy bù), chuyển toàn bộ cấu hình, textarea, kho thư viện PPCT ra khỏi giao diện chính. ĐÚNG SCOPE.
- Nút mở modal trên thanh công cụ Tab 4: Đã thêm nút `[Cài đặt PPCT & Lịch nghỉ]` gọi `openBaoGiangConfigModal()`, dọn sạch mặt chính Tab 4 để tập trung vào Sổ báo giảng. ĐÚNG SCOPE.
- Thu gọn cảnh báo lệch số tiết: Hàm `baoGiangWarningsHtml()` chuyển danh sách cảnh báo thành thẻ collapsible `<details class="bg-warning-box">` (mặc định đóng, chỉ chiếm 1 dòng ~36px, vùng nội dung cuộn max-height: 180px). ĐÚNG SCOPE.
- Bảo toàn tương thích: Tất cả ID HTML (`bg-curriculum`, `bg-ppct-file`, `bg-scan-ppct`, `bg-ppct-status`, `bg-ppct-grade`, `bg-ppct-subject`, `bg-exceptions`, `bg-schedule`) được giữ nguyên vẹn. ĐÚNG SCOPE.
- Không thêm chức năng ngoài kế hoạch, không can thiệp file ngoài plan.

## Test đã chạy
- `node tests/baogiang-teacher-month-smoke.js` — PASS (kiểm tra modal chứa đủ ID, nút mở modal, cảnh báo PPCT bọc `<details>`).
- `node tests/baogiang-weekday-segment-smoke.js` — PASS (PPCT đa tuần, cảnh báo hai GV, khóa mốc Tuần 1).
- `node tests/baogiang-recognition-smoke.js` — PASS (scripts compile; PPCT success/retry, nạp JSON, parse PDF/legacy).
- `node tests/timetable-render-smoke.js` — PASS (render TKB GV, compact layout, email).
- `node tests/attendance-autosync-smoke.js` — PASS (đồng bộ Chấm công, bảo toàn dạy thay/bù, lưu CSDL).

## Pass / Fail từng tiêu chí
- Modal `#baogiang-config-modal` mở/đóng chuẩn: PASS.
- Giao diện chính Tab 4 gọn gàng, không bị tràn textarea/kho PPCT: PASS.
- Cảnh báo PPCT thu gọn 1 dòng trong `<details>`: PASS.
- Các chức năng tra cứu lịch theo tháng, giáo viên, in sổ, xuất Excel: PASS.
- Bộ test hồi quy 5 tệp smoke tests: PASS 100%.

## Bug
Không phát hiện bug còn tồn đọng.
