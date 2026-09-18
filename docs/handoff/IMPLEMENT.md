# IMPLEMENT: Liên thông 1-Click + cuốn chiếu chống AI + CDN fallback PPDH

Đã triển khai đúng `docs/handoff/PLAN.md` (bản mở rộng: đề cũ + CDN catalog).

## Thay đổi

### Đã có từ vòng trước (giữ nguyên, vẫn đúng PLAN)
- `taobaitap.html` / backup: `mapToThiTrucTuyenPayload`, `startOnlineExam`, nút **🚀 THI TRỰC TUYẾN**.
- `thitructuyen.html`: nạp `thitructuyen_pending_import`, preset 15/20/30/45p, checkbox cuốn chiếu + watermark, UI 1 câu/lần + watermark + localStorage tiến trình.
- Cờ anti-AI lưu qua `matrixConfig` (không sửa `api/exam.php`).

### Bổ sung theo PLAN mới
#### `thitructuyen.html` — Sửa đề cũ
- `handleEdit`: khôi phục `anti_ai_one_by_one` / `anti_ai_watermark` từ `info.matrixConfig` khi mở đề cũ, để giáo viên chỉnh 15 phút / bật cờ rồi **Lưu Đề**.

#### `canvas_soankhbd.html` — CDN fallback PPDH
- `ensureKhbdPedagogyCatalogFallback`: nếu `KHBD_PEDAGOGY_CATALOG` vẫn undefined:
  - local/`localhost` → `js/khbd-pedagogy-catalog.js`
  - hosting → `https://cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-pedagogy-catalog.js`

### Tests
- `tests/taobaitap-thitructuyen-bridge-smoke.js`: thêm assert Sửa đề cũ khôi phục cờ.
- `tests/canvas-soankhbd-smoke.js`: assert CDN jsDelivr fallback.

## Test đã chạy

- `node tests/taobaitap-thitructuyen-bridge-smoke.js` — PASS
- `node tests/canvas-soankhbd-smoke.js` — PASS
- `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js` — PASS
- `node tests/taobaitap-plan-smoke.js` — PASS

Không mở rộng sang `api/exam.php` / prompt AI. Cần `/verify` trên Antigravity.
