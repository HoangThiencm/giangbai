# PLAN

## Hiện trạng
1. **Hệ trục tọa độ và lưới ô vuông gây rối hình học thuần túy**:
   - Khi công cụ "Vẽ hình AI" (`vehinh.html` & `app.js`) sinh mã GeoGebra và nạp vào applet hoặc xuất mã `Execute(...)`: GeoGebra tự động bật cả trục hoành, trục tung với dãy số âm/dương cùng lưới tọa độ dày đặc.
   - Hình vẽ hình học phẳng (tam giác, đường tròn, tiếp tuyến...) trông như đồ thị giải tích, rất rối mắt và mất tính trực quan sư phạm.
2. **"Rác nhãn" (Label Clutter)**:
   - GeoGebra mặc định hiển thị nhãn cho **toàn bộ** đối tượng mới sinh ra. Tên biến của đường tròn (`c`), các đoạn thẳng và đường thẳng (`f, g, m, j, p, r, k...`) tự động nổi lên chi chít, che khuất các đỉnh chính ($A, B, C, M, H, O, D$).
3. **Đường thẳng vô tận (`Line`) xé nát khung hình**:
   - Khi cần vẽ đường thẳng đi qua 2 điểm hoặc tiếp tuyến/đường vuông góc, AI thường sinh lệnh `Line(...)` hoặc `PerpendicularLine(...)`.
   - Các đường này kéo dài vô tận về cả 2 phía ra tận mép màn hình, cắt ngang dọc hình vẽ thay vì chỉ là các đoạn thẳng (`Segment(...)`) nối giữa các điểm.
4. **Đối tượng trung gian và điểm gốc tọa độ tạm**:
   - Điểm gốc mốc tính toán (ví dụ `m = (0, 0)`) bị hiển thị nổi bật như một điểm trong đề bài dù học sinh không cần thấy.
   - Các đường phụ chỉ dùng để tìm giao điểm không được ẩn đi sau khi lấy xong điểm.

## Phạm vi
- Tối ưu hóa toàn diện công cụ nạp và xuất mã GeoGebra trên trang Vẽ hình (`vehinh.html` & `app.js`):
  + **Tự động hóa bằng JavaScript trong `app.js`**:
    * Trong hàm `runCommandsOnGeoGebra(commandsArray)`: Tự động tắt hệ trục (`setAxesVisible(1, false, false, false)`) và tắt lưới (`setGridVisible(1, false)`).
    * Duyệt toàn bộ đối tượng trong applet (`getAllObjectNames()`): Chỉ giữ lại nhãn cho đối tượng kiểu `point` (điểm) và `text` (chữ). Tự động tắt nhãn (`showLabel(name, false)`) cho toàn bộ đoạn thẳng, đường thẳng, đường tròn, góc, đa giác.
    * Tự động ẩn các đường phụ (`aux_...`, `temp_...`) và điểm gốc tọa độ tạm (`Origin`, `temp_origin`) nếu không thuộc đề bài.
    * Ngoại lệ thông minh: Nếu đề bài có từ khóa "đồ thị", "hàm số", "hệ trục", "tọa độ", "parabol" thì giữ lại hệ trục $Oxy$.
  + **Tự động hóa khi Sao chép lệnh GeoGebra (`Execute(...)`)**:
    * Trong hàm `formatGeoGebraExecuteCommand(commandsArray)`: Tự động chèn 2 lệnh chuẩn `ShowAxes(false)` và `ShowGrid(false)` vào đầu danh sách lệnh để khi người dùng dán vào GeoGebra Desktop hay Web ngoài thì hình vẫn luôn sạch sẽ.
  + **Nâng cấp System Prompt AI trong `app.js`**:
    * Bổ sung quy tắc vàng cho khối lệnh `<geogebra>...</geogebra>`:
      1. Hai lệnh đầu tiên luôn là `ShowAxes(false)` và `ShowGrid(false)`.
      2. Mọi cạnh và đường nối bắt buộc dùng `Segment(A, B)`, tuyệt đối không dùng `Line(A, B)` trừ khi đề bài yêu cầu đường thẳng vô hạn.
      3. Quy tắc giao điểm **"DỰNG → LẤY → ẨN → NỐI"**: Khi cần tìm giao điểm (cát tuyến, tiếp tuyến, đường vuông góc, đường kéo dài): dựng đường phụ với tiền tố `aux_...`, lấy giao điểm bằng `Intersect(...)`, lập tức gọi `SetVisibleInView(aux_..., 1, false)` để ẩn đường thẳng vô tận, rồi vẽ lại bằng `Segment(...)` nối từ điểm gốc đến giao điểm.
      4. Thêm lệnh `ShowLabel(..., false)` cho đường tròn và đoạn thẳng, chỉ giữ nhãn chữ in hoa cho các điểm ($A, B, C, O, M...$).
      5. Ẩn điểm gốc tọa độ giả lập `SetVisibleInView(Origin, 1, false)`.

## Ngoài phạm vi
- Không can thiệp vào cơ chế vẽ 2D Fabric.js trên Canvas bên trái (giữ nguyên logic Fabric.js).
- Không sửa đổi backend `api/vehinh_ai.php` (chỉ điều chỉnh prompt phía client gửi lên).

## File dự kiến tác động
- `app.js`: Cập nhật hàm `runCommandsOnGeoGebra`, `formatGeoGebraExecuteCommand`, và bổ sung quy tắc GeoGebra trong `systemPrompt`.
- `vehinh.html`: Cập nhật thẻ version cache buster của `app.js?v=...`.

## Các bước thực hiện
1. **Cập nhật hàm `formatGeoGebraExecuteCommand` trong `app.js`**:
   - Tự động bổ sung `ShowAxes(false)` và `ShowGrid(false)` ở đầu mảng lệnh nếu chưa có.
2. **Cập nhật hàm `runCommandsOnGeoGebra` trong `app.js`**:
   - Thêm lệnh API tắt hệ trục và tắt lưới của GeoGebra Applet.
   - Thêm vòng lặp quét danh sách đối tượng sau khi `evalCommand` hoàn tất: tắt nhãn toàn bộ đối tượng trừ điểm và chữ cái.
   - Tự động ẩn các đối tượng có tiền tố `aux_`, `temp_` hoặc `Origin`.
3. **Cập nhật `systemPrompt` trong `app.js` (Phần 3: GeoGebra)**:
   - Viết lại chỉ dẫn sinh mã GeoGebra chuẩn sư phạm:
     + Bắt buộc `ShowAxes(false)`, `ShowGrid(false)`.
     + Bắt buộc dùng `Segment` thay vì `Line`.
     + Áp dụng quy tắc "Dựng → Lấy → Ẩn → Nối" cho mọi bài toán tìm giao điểm/tiếp tuyến.
     + Ẩn nhãn toàn bộ đoạn thẳng, đường tròn, chỉ giữ nhãn điểm.
4. **Kiểm thử trên giao diện thực tế**:
   - Chạy thử các câu lệnh hình học: tiếp tuyến cắt nhau, cát tuyến, đường cao tam giác.
   - Kiểm tra cả 2 luồng: Nạp trực tiếp vào Applet GeoGebra trên web và Sao chép lệnh `Execute(...)` dán vào GeoGebra độc lập.

## Rủi ro
- *Rủi ro bài toán Đại số / Đồ thị hàm số*: Với bài vẽ đồ thị $y = ax + b$ hoặc Parabol, nếu tắt hệ trục thì đồ thị mất gốc tọa độ.
  + *Giải pháp*: Trong `runCommandsOnGeoGebra`, kiểm tra nội dung prompt hoặc lệnh: nếu có vẽ hàm số (`Function`, `y =`, `x^2`) hoặc có từ khóa "đồ thị", "hệ trục" thì giữ nguyên hệ trục tọa độ.
- *Rủi ro lệnh `Intersect` bị lỗi khi ẩn đường phụ*: GeoGebra duy trì cây phụ thuộc (dependency tree) bằng tên đối tượng, việc ẩn hình (`SetVisibleInView` hoặc `setVisible(false)`) chỉ ẩn hiển thị trực quan chứ không xóa đối tượng, nên giao điểm vẫn được bảo toàn 100%.

## Cách kiểm thử
1. **Kiểm thử trực tiếp trên Applet GeoGebra trong trang `vehinh.html`**:
   - Nhập đề bài hình học (ví dụ: *Cho đường tròn (O; R) và điểm M nằm ngoài đường tròn. Kẻ hai tiếp tuyến MA, MB và cát tuyến MCD...*).
   - Bấm "Tạo hình vẽ":
     + Xác nhận hệ trục tọa độ và lưới ô vuông đã hoàn toàn biến mất.
     + Xác nhận không còn các chữ cái rác $c, f, g, m, j, p, r, k$ trên đường tròn và đoạn thẳng.
     + Xác nhận chỉ còn hiển thị nhãn các điểm chính: $A, B, C, D, M, H, O$.
     + Xác nhận các tiếp tuyến và cát tuyến là các đoạn thẳng gọn gàng, không có đường thẳng nào kéo dài vô hạn ra mép màn hình.
2. **Kiểm thử bài toán giao điểm (Dựng - Lấy - Ẩn - Nối)**:
   - Thử nghiệm bài toán: *Cho tam giác ABC, đường cao AH và trung tuyến BM cắt nhau tại K*.
   - Xác nhận đường cao $AH$ và trung tuyến $BM$ kết thúc tại $H$ và $M$, không bị kéo dài vô tận qua cạnh tam giác.
3. **Kiểm thử Sao chép lệnh**:
   - Bấm nút "Sao chép lệnh GeoGebra".
   - Mở GeoGebra Web (geogebra.org/classic) hoặc GeoGebra 5/6 trên máy tính, dán lệnh vào ô Input: hình vẽ hiển thị sạch đẹp, không có hệ trục và không có nhãn rác.

## Tiêu chí nghiệm thu
- Hình học phẳng nạp vào GeoGebra hoàn toàn sạch sẽ, thoáng đãng, không có trục tọa độ và lưới ô vuông.
- Chỉ hiển thị nhãn của các điểm hình học ($A, B, C...$), loại bỏ 100% nhãn rác của đoạn thẳng/đường tròn/góc.
- Các đường phụ phục vụ tìm giao điểm được ẩn tự động, chỉ hiển thị đoạn thẳng nối thực tế.
- Lệnh sao chép `Execute(...)` hoạt động chuẩn trên mọi môi trường GeoGebra.


