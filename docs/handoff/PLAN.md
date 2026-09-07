# PLAN: Sửa Lỗi Tương Phản Màu Sắc (Mờ/Tối Chữ) trong Khung Cấu hình NLS Tự Động

## Hiện trạng
1. **Lỗi hiển thị khung `#nlsAdaptiveOptions`**:
   - Khung thông tin tùy chọn phân bổ NLS theo tiết & AI (`• Bài 1 tiết: 2 mã NLS...`) hiển thị nền tối (`#1e293b`) trong khi giao diện tổng thể đang ở chế độ Sáng (nền trắng).
   - Chữ bên trong khung (`• Bài 1 tiết: 2 mã NLS`, `• Bài từ 2 tiết có AI: 2 mã NLS`, select `2–3 mã`) dùng màu mực đen/xám đậm (`#172033`).
   - Chữ màu đen trên nền đen/xanh đen tạo ra độ tương phản cực kỳ thấp, người dùng nhìn vào thấy mờ câm, không đọc được nội dung.
2. **Nguyên nhân kỹ thuật**:
   - Thẻ `<div id="nlsAdaptiveOptions" class="mt-2 text-xs space-y-1 p-2 rounded border bg-slate-50 dark:bg-slate-800">` sử dụng class `dark:bg-slate-800` của Tailwind CDN.
   - Tailwind CDN theo mặc định kích hoạt class `dark:` dựa trên `prefers-color-scheme: dark` của hệ điều hành / trình duyệt, trong khi toàn bộ ứng dụng quản lý chế độ Dark/Light bằng class `.dark` thủ công gắn trên thẻ `<html>` thông qua các biến CSS (`--paper`, `--card`, `--ink`, `--line`).
   - Kết quả: Khi máy tính người dùng có tùy chọn Dark mode của Windows, Tailwind tự động tô nền `#nlsAdaptiveOptions` thành `slate-800` (đen tối), nhưng CSS biến của ứng dụng vẫn đang ở Light mode (`--ink: #172033` - chữ đen). Chữ đen trên nền đen gây mờ và không đọc được.

## Phạm vi
- Cập nhật định kiểu (styling) của `#nlsAdaptiveOptions` và select `#nlsNoAiDensity` trên cả hai tệp:
  + `xaydungphuluc.html`
  + `backupcode viettailieu/canvas_xaydungphuluc.html`
- Cập nhật smoke tests trong `tests/xaydungphuluc-smoke.js` và `tests/canvas-xaydungphuluc-smoke.js`.

## Ngoài phạm vi
- Không thay đổi logic phân bổ NLS, không đổi cấu trúc PPCT hay logic sinh AI.

## File dự kiến tác động
- `xaydungphuluc.html`
- `backupcode viettailieu/canvas_xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `tests/canvas-xaydungphuluc-smoke.js`

## Các bước thực hiện

### Bước 1: Chuẩn hóa kiểu dáng `#nlsAdaptiveOptions` theo biến CSS hệ thống
1. Trong cả `xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`:
   - Thay thế class Tailwind xung đột `bg-slate-50 dark:bg-slate-800` bằng inline style dùng trực tiếp các biến CSS theme hoặc tông nền thương hiệu dịu nhẹ, đảm bảo tương thích 100% cả Light mode và Dark mode:
     ```html
     <div id="nlsAdaptiveOptions" class="mt-2 text-xs space-y-1 p-2.5 rounded-lg border" style="background:var(--paper);border-color:var(--line);color:var(--ink);">
       <div>• Bài 1 tiết: <b style="color:var(--brand)">2 mã NLS</b></div>
       <div>• Bài từ 2 tiết có AI: <b style="color:var(--brand)">2 mã NLS</b></div>
       <label class="flex items-center gap-2">
         <span>• Bài từ 2 tiết không có AI:</span>
         <select id="nlsNoAiDensity" class="field text-xs py-0.5 px-1.5 w-auto" style="background:var(--card);color:var(--ink);border-color:var(--line);">
           <option value="2-3" selected>2–3 mã</option>
           <option value="2">2 mã</option>
         </select>
       </label>
     </div>
     ```
   - Trong chế độ Sáng: Nền `var(--paper)` (`#f4f8fb`) sáng rõ, chữ `var(--ink)` (`#172033`) đen đậm tương phản tuyệt đối, các số lượng mã nổi bật màu thương hiệu `var(--brand)`.
   - Trong chế độ Tối: Nền `var(--paper)` (`#101827`) tối, chữ `var(--ink)` (`#e7edf4`) trắng sáng rõ nét.
   - Ô chọn `nlsNoAiDensity` có nền `var(--card)` và chữ `var(--ink)`, không bị đen chữ trên nền đen.

### Bước 2: Cập nhật Smoke Test và Kiểm thử
1. Cập nhật `tests/xaydungphuluc-smoke.js` và `tests/canvas-xaydungphuluc-smoke.js`:
   - Xác minh không còn class `dark:bg-slate-800` gây xung đột trong `#nlsAdaptiveOptions`.
   - Xác minh `#nlsAdaptiveOptions` sử dụng các biến giao diện `var(--paper)` và `var(--ink)`.
2. Chạy kiểm thử:
   - `node tests/canvas-xaydungphuluc-smoke.js`
   - `node tests/xaydungphuluc-smoke.js`
   - `node tests/xaydungphuluc-integration-smoke.js`

## Rủi ro
- Không có. Đây là chỉnh sửa CSS giao diện thuần túy để đồng bộ với hệ thống theme biến CSS của trang.

## Cách kiểm thử
1. `node tests/canvas-xaydungphuluc-smoke.js` -> PASS.
2. `node tests/xaydungphuluc-smoke.js` -> PASS.
3. Mở giao diện `xaydungphuluc.html` trên trình duyệt ở cả chế độ máy tính Light mode và Dark mode:
   - Khung chữ `#nlsAdaptiveOptions` luôn hiển thị rõ ràng, sắc nét, dễ đọc 100%.
   - Chuyển đổi nút "◐ Giao diện" thấy khung chuyển đổi màu sắc đồng bộ, mượt mà.

## Tiêu chí nghiệm thu
- Khung tùy chọn NLS tự động hiển thị rõ ràng, độ tương phản cao, không còn hiện tượng chữ đen chìm trên nền tối.
- Hoạt động hoàn hảo ở cả Light mode và Dark mode trên cả bản web và Gemini Canvas.
- Toàn bộ smoke test đều PASS.
