# IMPLEMENT

Trạng thái: ĐÃ LÀM

## File đã đổi

- `app.js`
- `vehinh.html`

## Nội dung chính

1. **Nâng cấp System Prompt AI (`app.js`)**:
   - Bổ sung quy tắc 2 lệnh đầu tiên luôn là `ShowAxes(false)` và `ShowGrid(false)` (trừ bài toán đồ thị hàm số / hệ trục Oxy).
   - Nghiêm cấm dùng `Line(A, B)` vô hạn kéo dài xuyên màn hình cho các cạnh; bắt buộc dùng `Segment(A, B)`.
   - Thiết lập chuẩn quy tắc dựng hình sư phạm "DỰNG → LẤY → ẨN → NỐI": Dựng đường thẳng phụ mang tiền tố `aux_` (ví dụ `aux_l = Line(...)`), tìm giao điểm `Intersect(...)`, ẩn ngay đường phụ `SetVisibleInView(aux_l, 1, false)`, rồi nối lại bằng đoạn thẳng thực tế `Segment(...)`.
   - Thêm lệnh `ShowLabel(..., false)` cho đường tròn, đoạn thẳng, đường thẳng; chỉ giữ lại nhãn chữ in hoa cho các điểm ($A, B, C, O, M...$).
   - Tự động ẩn gốc tọa độ phụ trợ `Origin`: `SetVisibleInView(Origin, 1, false)`.

2. **Cập nhật nhận diện và xử lý lệnh GeoGebra (`app.js`)**:
   - Mở rộng hàm `splitGeoGebraBlocks` nhận diện đầy đủ các lệnh điều khiển hiển thị GeoGebra: `ShowAxes`, `ShowGrid`, `ShowLabel`, `SetVisibleInView`, `SetColor`, `SetLineThickness`, `CenterView`, `ZoomIn`... và các phép gán biến phụ `aux_... = ...`.
   - Bổ sung hàm `isGeoGebraCoordinateRequested`: kiểm tra thông minh từ khóa đề bài hoặc lệnh vẽ để phân biệt bài toán hình học thuần túy (cần tắt trục) với bài toán đồ thị / tọa độ Oxy (cần giữ trục).
   - Cập nhật hàm `formatGeoGebraExecuteCommand`: tự động chèn `ShowAxes(false)` và `ShowGrid(false)` vào khối lệnh `Execute({...})` khi người dùng sao chép lệnh dán vào GeoGebra Desktop hoặc Web.

3. **Cập nhật hàm nạp trực tiếp vào GeoGebra (`runCommandsOnGeoGebra` & `cleanUpGeoGebraObjects` trong `app.js`)**:
   - Tự động gọi API tắt trục và tắt lưới của GeoGebra Applet trước và sau khi thực thi lệnh.
   - Bổ sung hàm `cleanUpGeoGebraObjects`: duyệt toàn bộ đối tượng trong Applet (`getAllObjectNames()`), tự động ẩn nhãn rác của các đoạn thẳng, đường thẳng, đường tròn, đa giác, góc (`showLabel(name, false)`) và chỉ giữ lại nhãn cho điểm (`point`) và chữ (`text`).
   - Tự động ẩn hoàn toàn các đối tượng phụ `aux_...`, `temp_...`, `Origin`, `temp_origin` (`setVisible(name, false)`).
   - Tự động dọn dẹp nhãn 2 lần (ngay lập tức và sau 150ms) để đảm bảo không sót bất kỳ đối tượng bất đồng bộ nào.

4. **Cập nhật Cache Buster (`vehinh.html`)**:
   - Đổi thẻ nạp script thành `app.js?v=20260911-geogebra-clean`.

## Test đã thực hiện

- Kiểm tra luồng xử lý chuỗi lệnh và Regex `splitGeoGebraBlocks`.
- Kiểm tra cơ chế tự chèn `ShowAxes(false)` và `ShowGrid(false)` trong `formatGeoGebraExecuteCommand`.
- Kiểm tra bộ lọc `cleanUpGeoGebraObjects` ẩn nhãn không phải điểm và ẩn đối tượng phụ `aux_`.
- Kiểm tra điều kiện ngoại lệ khi đề bài chứa từ khóa đồ thị hàm số / hệ trục tọa độ.

## Vấn đề còn lại

- Không có.
