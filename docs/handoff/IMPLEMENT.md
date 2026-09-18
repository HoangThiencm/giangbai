# IMPLEMENT: Chuẩn hóa tiêu đề Hoạt động 4 → "HOẠT ĐỘNG 4: VẬN DỤNG"

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

### `js/khbd-prompts.js`
- `GENERATE_ACTIVITY_D` / `GENERATE_ACTIVITIES_AD`: tiêu đề `## D. HOẠT ĐỘNG 4: VẬN DỤNG ({time_budget_D})`.
- Nhãn pha: `PHA D — VẬN DỤNG:` (bỏ `& HƯỚNG DẪN TỰ HỌC`).

### HTML tab D
- `soankhbd.html`, `canvas_soanbaigiang.html`: nút `D. Vận dụng`.

### `js/khbd-app.js`
- `ACTIVITY_TITLES.D` đã sẵn `short: "D. Vận dụng"`, `full: "D. HOẠT ĐỘNG 4: VẬN DỤNG"` — không cần sửa thêm.

### Tests
- `tests/khbd-tabs-reorganized-smoke.js`: match tab HTML, `ACTIVITY_TITLES.D.short`, fixture/assert markdown D mới.
- `tests/khbd-activities-ad-standard-smoke.js`: match prompt AD/D + fixture/assert full plan.
- `tests/khbd-table-columns-smoke.js`: fixture tiêu đề D mới.

## Test đã chạy

- `node tests/khbd-tabs-reorganized-smoke.js` — PASS
- `node tests/khbd-activities-ad-standard-smoke.js` — PASS
- `node tests/khbd-table-columns-smoke.js` — PASS
- `node tests/canvas-tabs-permissions-smoke.js` — PASS

Không mở rộng scope (không đụng backupcode ngoài PLAN). Cần `/verify` trên Antigravity.
