# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `js/khbd-prompts.js`: Đã cập nhật tiêu đề Hoạt động 4 thành `## D. HOẠT ĐỘNG 4: VẬN DỤNG ({time_budget_D})` và đổi nhãn pha thành `PHA D — VẬN DỤNG:` trong `GENERATE_ACTIVITY_D` và `GENERATE_ACTIVITIES_AD`.
- `soankhbd.html`: Đã cập nhật nút tab thành `D. Vận dụng`.
- `canvas_soanbaigiang.html`: Đã cập nhật nút tab thành `D. Vận dụng`.
- `js/khbd-app.js`: Giữ nguyên `ACTIVITY_TITLES.D` chuẩn hóa `{ short: "D. Vận dụng", full: "D. HOẠT ĐỘNG 4: VẬN DỤNG" }`.
- `tests/khbd-tabs-reorganized-smoke.js`: Đã đồng bộ assertion và fixture.
- `tests/khbd-activities-ad-standard-smoke.js`: Đã đồng bộ assertion và fixture.
- `tests/khbd-table-columns-smoke.js`: Đã đồng bộ fixture.
- Không sửa file ngoài scope, không đụng backupcode.

## Test đã chạy
- `node tests/khbd-tabs-reorganized-smoke.js` — PASS
- `node tests/khbd-activities-ad-standard-smoke.js` — PASS
- `node tests/khbd-table-columns-smoke.js` — PASS
- `node tests/canvas-tabs-permissions-smoke.js` — PASS

## Pass / Fail từng tiêu chí
- [PASS] Tiêu đề prompt AI Hoạt động D đã bỏ cụm `& HƯỚNG DẪN TỰ HỌC`.
- [PASS] Nút tab D trên giao diện HTML hiển thị thống nhất `D. Vận dụng`.
- [PASS] Toàn bộ kịch bản smoke test liên quan đến subtab A-F và tiến trình A-D đều PASS 100%.

## Bug
Không phát hiện bug.
