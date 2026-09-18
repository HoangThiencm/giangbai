# IMPLEMENT: Liên thông 1-Click + cuốn chiếu + CDN PPDH + chống trang trắng

Đã triển khai đúng `docs/handoff/PLAN.md` (kèm mục **Khắc phục trang trắng**).

## Thay đổi mới (White Screen Fix)

### `access-control.js`
- Miễn kiểm tra token khi `thitructuyen` mở với `from=taobaitap` (cùng với link học sinh `mode=student&examId`).

### `thitructuyen.html`
- `userEmail` fallback `giaovien@giangbai.local` khi `from=taobaitap` hoặc còn `thitructuyen_pending_import` — tránh màn "Phiên đăng nhập hết hạn"/trắng.
- Guard `typeof Sortable !== "undefined"` trước `new Sortable` — CDN lỗi không sập React.
- `HybridExamCreator`: đồng bộ `examInfo` (title, duration 15, anti-AI) từ `initialData.info` khi App truyền đề 1-Click.
- Pending import trong creator chỉ chạy fallback nếu `initialData` chưa có questions (tránh race xóa localStorage 2 lần).

## Đã có từ vòng trước (vẫn đúng PLAN)
- Nút **🚀 THI TRỰC TUYẾN**, `mapToThiTrucTuyenPayload`, pending import, preset 15/20/30/45p.
- Cuốn chiếu 1 câu/lần + watermark + localStorage tiến trình.
- Sửa đề cũ khôi phục cờ anti-AI từ `matrixConfig`.
- CDN jsDelivr fallback catalog PPDH trên `canvas_soankhbd.html`.

## Test đã chạy

- `node tests/taobaitap-thitructuyen-bridge-smoke.js` — PASS
- `node tests/canvas-soankhbd-smoke.js` — PASS
- `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js` — PASS
- `node tests/taobaitap-plan-smoke.js` — PASS

Không sửa `api/exam.php` / prompt AI. Cần `/verify` trên Antigravity.
