# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `api/phancong.php` — ĐÚNG SCOPE (`PHANCONG_SCHEMA_VERSION = '20261126-v4'`, bảng `phancong_weekly_timetables`, `action=get_week_timetable`, bảo toàn khóa chuỗi `(string)$tid` cho ID giáo viên dạng số, kiểm tra `$dataJson` đúng sau `json_encode`, tính khoảng ngày tuần ưu tiên `bao_giang.start_date`, tự động lưu trữ TKB tuần trước khi ghi đè).
- `phancongtochuyenmon.html` — ĐÚNG SCOPE (bộ chọn tuần nổi bật trên `#tt-workspace-header` mặc định tuần hiện tại, tự động đồng bộ CSDL `autoSave: true`, chụp snapshot `W(week - 1)` chính xác kể cả khi đã có `W1`/`W5`, nhập bù tuần cũ `W11` không ghi đè `W12`, Sổ Dạy Thay lấy đúng TKB theo ngày/nguồn CSDL, xóa sạch tiết cũ khi đổi sang ngày không có tiết hoặc cùng buổi khác tuần, đồng bộ đầy đủ danh sách GV, Lịch báo giảng và Email TKB theo tuần).
- `tests/daythay-suggest-smoke.js` — ĐÚNG SCOPE (bổ sung đầy đủ kiểm thử E2E chuyển đổi Tuần 12 ↔ Tuần 11, nạp lại/xóa tiết `#period-slots-builder`, badge nguồn CSDL, cảnh báo fallback và chọn nguồn `phase:...`).
- `tests/timetable-render-smoke.js` — ĐÚNG SCOPE (bổ sung đầy đủ kiểm thử snapshot `W11` khi đã có `W1`/`W5`, nhập bù `W11` bảo toàn `W12` và phân công lớp `W12`, đếm tiết theo tuần trên danh sách GV và kiểm tra tĩnh `api/phancong.php`).
- `docs/handoff/IMPLEMENT.md` — ĐÚNG SCOPE.

## Test đã chạy
1. `node tests/daythay-suggest-smoke.js` -> PASS (`EXIT=0`)
2. `node tests/timetable-render-smoke.js` -> PASS (`EXIT=0`)
3. `node tests/baogiang-teacher-month-smoke.js` -> PASS (`EXIT=0`)
4. `node tests/baogiang-weekday-segment-smoke.js` -> PASS (`EXIT=0`)
5. `node tests/baogiang-mail-smoke.js` -> PASS (`EXIT=0`)
6. `node tests/attendance-autosync-smoke.js` -> PASS (`EXIT=0`)
7. Kiểm tra cú pháp toàn bộ `<script>` trong `phancongtochuyenmon.html` (`vm.Script`) & cấu trúc `api/phancong.php` -> PASS
8. `git diff --check` -> PASS

## Pass / Fail từng tiêu chí
1. **Tiêu chí 1 (CSDL lưu trữ độc lập TKB theo tuần & autoSave):** **PASS**
2. **Tiêu chí 2 (Không mất TKB tuần trước khi sang tuần mới):** **PASS**
3. **Tiêu chí 3 (Quay lại nhập Dạy thay ở Tuần 11 lấy đúng CSDL Tuần 11):** **PASS**
4. **Tiêu chí 4 (Đồng bộ đầy đủ danh sách GV, Lịch báo giảng & Email TKB theo tuần):** **PASS**
5. **Tiêu chí 5 (Bổ sung và chạy PASS toàn bộ kiểm thử tự động Bước 5):** **PASS**

## Bug
Không có.
