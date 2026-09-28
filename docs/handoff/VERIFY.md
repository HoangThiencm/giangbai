# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Tự động đảo Key khi gặp lỗi 503 High Demand**:
   - `api/khbd_gemini.php`: hàm `khbd_gemini_should_rotate` đã bổ sung mã HTTP `503` và các từ khóa `high demand`, `overloaded`, `unavailable`. Khi Google quá tải tạm thời ở một key, hệ thống tự động chuyển sang API key Free kế tiếp trong danh sách, giữ nguyên model đang chọn mà không dừng ngang. -> ĐẠT
2. **Tối ưu danh sách Model cho tài khoản Free**:
   - `phancongtochuyenmon.html`: Modal `#gemini-model-modal` đã loại bỏ hoàn toàn `gemini-2.5-pro` và `gemini-1.5-flash`. Chỉ giữ các bản Flash tối ưu cho gói Free (`gemini-2.5-flash` mặc định, `gemini-3.7-flash`, `gemini-3-flash-preview` và tùy chỉnh). -> ĐẠT
3. **Đưa nút Cài đặt AI ra vị trí nổi bật**:
   - Nút mở modal hiện diện trực tiếp trên **Top Navbar** (`#top-nav-ai-model-label`, cạnh nút "Khai báo tổ") và trên **Thanh công cụ TKB** (`#tt-toolbar-model-label`, dưới bảng TKB). -> ĐẠT
   - Hàm `updateAiModelLabels(model)` cập nhật đồng bộ nhãn tại cả 3 vị trí (Navbar, Toolbar và thẻ import). -> ĐẠT

## Test đã chạy
- `node tests/timetable-render-smoke.js`: PASS
  + Xác nhận `api/khbd_gemini.php` tự động đảo key khi 503 High Demand.
  + Xác nhận modal chỉ còn các bản Flash, không còn Pro/1.5.
  + Xác nhận nút Cài đặt AI trên Top Navbar và Toolbar TKB.
- `node tests/taobaitap-diversity-smoke.js`: PASS
- `node tests/baogiang-mail-smoke.js`: PASS
- `node tests/baogiang-teacher-month-smoke.js`: PASS

## Pass / Fail từng tiêu chí
1. Xử lý lỗi 503 High Demand bằng cách tự động đảo Key: PASS
2. Loại bỏ các model không dùng cho tài khoản Free: PASS
3. Đưa nút Cài đặt Model AI ra Top Navbar và Toolbar TKB: PASS
4. Đồng bộ nhãn hiển thị tại các vị trí: PASS
5. Toàn bộ test suite liên quan: PASS

## Bug
Không phát hiện bug mới.
