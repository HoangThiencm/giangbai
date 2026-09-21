# IMPLEMENT: Tab Game Giáo dục

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

- `taobaitap.html` và `backupcode viettailieu/taobaitap.html`: chuyển bộ chọn Chế độ sang ba cột và thêm tab Game Giáo dục.
- Tab mới mở `https://www.hoangthiencm.id.vn/trochoi.html` trong tab trình duyệt riêng với `noopener noreferrer`.
- `smartquiz.html`: đồng bộ liên kết Game Giáo dục sang URL đầy đủ, mở trong tab mới.
- Thêm `tests/taobaitap-game-tab-smoke.js`.

## Kiểm tra

Đã kiểm tra tĩnh đầy đủ các thuộc tính theo kế hoạch. Không thể chạy Node smoke test trong môi trường hiện tại vì Windows chặn `node.exe` do nhận diện nhầm là phần mềm không an toàn (`ResourceUnavailable`).
