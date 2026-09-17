# IMPLEMENT: Hai chế độ soạn Canvas KHBD

Đã triển khai đúng `docs/handoff/PLAN.md`.

- Thêm bộ chọn **Soạn chi tiết** (mặc định) và **Soạn rút gọn**; lựa chọn được lưu bằng `khbd_generation_mode`.
- Chế độ rút gọn chạy sáu bước I, II, A–D và bỏ III.E cùng hình minh họa SGK; chế độ chi tiết giữ nguyên luồng đầy đủ.
- Bổ sung hợp đồng prompt rút gọn 4–6 trang: kịch bản 4 bước ngắn gọn, bảng 2 cột, bài mẫu ngắn, bốn nhiệm vụ tự học ở D và giữ marker NLS/AI.
- Tab tạo riêng nhận chế độ từ ngữ cảnh sinh nội dung. Đồng bộ giao diện và luồng 1-Click cho cả hai tệp Canvas.
- Mở rộng smoke test kiểm tra bộ chọn, mặc định chi tiết, lưu trạng thái và nhánh không tạo minh họa khi rút gọn.

Kiểm thử:

- `git diff --check` — PASS.
- Không thể chạy các smoke test Node trong môi trường hiện tại vì Windows chặn `node.exe` của runtime với cảnh báo tệp có thể không an toàn.

Không thêm chức năng ngoài plan. Cần `/verify` trên Antigravity để xác nhận hai chế độ và xuất Word thực tế.
