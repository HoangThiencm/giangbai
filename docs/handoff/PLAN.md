# PLAN

## Hiện trạng
1. **Thiết kế máy tính chưa đúng bản chất máy tính Casio vật lý:**
   - Phiên bản vừa triển khai đã tách máy tính thành các tab và đưa các form HTML bên ngoài với các thẻ `<input type="number">` cùng các nút web thông thường để giải phương trình và hệ phương trình.
   - Điều này làm mất đi tính sư phạm và mục đích trợ giảng trực quan: Giáo viên cần một máy tính mô phỏng **hoàn toàn giống máy tính cầm tay vật lý**, nơi mọi thao tác bấm phím (chọn Menu, nhập hệ số, xem nghiệm) đều diễn ra bằng cách **dùng chuột bấm trực tiếp lên các phím của máy tính**, và mọi nội dung, ma trận hệ số, kết quả đều hiển thị trực tiếp trên **MÀN HÌNH LCD CỦA MÁY TÍNH**. Học sinh quan sát giáo viên bấm phím nào thì trên tay học sinh sẽ bấm đúng phím đó trên máy Casio thật.
2. **Cập nhật Template:**
   - Cần đồng bộ hóa triệt để kiến trúc mô phỏng phím bấm vật lý này vào file mẫu `TROLYTHIEN/2_TAO_BAI_TAP/templates/master_bai_day_html_template.html` và file bài giảng `Bai_12_He_Thuc_Canh_Va_Goc_Tam_Giac_Vuong_Toan_9.html`.

## Phạm vi
1. **Loại bỏ hoàn toàn form HTML và thẻ `<input>` bên ngoài:**
   - Xóa bỏ toàn bộ các tab form web và các ô `<input>` text/number rời rạc.
   - Thân máy tính trở thành một khối thống nhất mô phỏng 100% máy tính vật lý Casio fx-580VN X ClassWiz (gồm Màn hình LCD và Bàn phím bấm chuột).
2. **Xây dựng Máy trạng thái (State Machine) điều khiển Màn hình LCD & Phím bấm Casio chân thực:**
   - **Chế độ 1 - Tính toán cơ bản (COMP - MENU 1):**
     + Nhập biểu thức tự nhiên qua phím bấm bằng chuột.
     + Phân số 2 tầng, căn bậc hai, căn bậc ba, sin, cos, tan, nghịch đảo sin⁻¹, cos⁻¹, tan⁻¹, độ-phút-giây (`°′″`), `S⇔D`, giai thừa, phần trăm, giá trị tuyệt đối, hằng số $\pi, e$, `Ans`, `M+`.
   - **Chế độ 2 - Màn hình chọn MENU (Bấm phím `MENU` / `MODE`):**
     + Màn hình LCD hiển thị danh mục các chế độ chuẩn Casio:
       `1: Tính toán (COMP)`
       `9: Phương trình / Hệ PT (EQN)`
       `8: Bảng giá trị (TABLE)`
     + Giáo viên bấm phím số `1`, `9`, `8` trên bàn phím Casio bằng chuột để chuyển chế độ.
   - **Chế độ 3 - Giải Hệ phương trình (MENU 9 → Bấm 1):**
     + Màn hình LCD hỏi số ẩn: `Hệ PT: Số ẩn? (2 ~ 4)`. Bấm phím `2` chọn hệ 2 ẩn.
     + Màn hình LCD hiển thị giao diện ma trận hệ số 2 dòng:
       `[ a1 ]x + [ b1 ]y = [ c1 ]`
       `[ a2 ]x + [ b2 ]y = [ c2 ]`
       Ô đang chọn có dấu nhấp nháy hoặc nền sáng.
     + Giáo viên click chuột vào các phím số và phím `=`: Ví dụ bấm `2` rồi `=` thì $a_1 = 2$ và con trỏ tự động nhảy sang ô tiếp theo $b_1$.
     + Sau khi nhập xong hệ số cuối cùng, bấm phím `=` máy tính hiển thị:
       `x = [giá trị]`
       Bấm phím `=` hoặc `▼` hiển thị:
       `y = [giá trị]`
     + Bấm phím `AC` quay lại bảng hệ số để sửa; bấm `MENU` `1` hoặc `ON` quay về tính toán thông thường.
   - **Chế độ 4 - Giải Phương trình Bậc hai & Bậc ba (MENU 9 → Bấm 2):**
     + Màn hình LCD hỏi bậc: `Phương trình: Bậc? (2 ~ 3)`. Bấm `2` chọn bậc hai, bấm `3` chọn bậc ba.
     + Nếu chọn bậc hai: LCD hiển thị `ax² + bx + c = 0` với các ô nhập $a, b, c$.
     + Giáo viên bấm các phím số và phím `=` để nạp hệ số.
     + Bấm `=` màn hình hiển thị:
       `x1 = [nghiệm 1]` (hoặc vô nghiệm nếu $\Delta < 0$)
       Bấm tiếp `=` hoặc `▼`:
       `x2 = [nghiệm 2]`
       Bấm tiếp `=` hiển thị tọa độ đỉnh Parabol ($x$ cực trị, $y$ cực trị) chuẩn như Casio fx-580VN X!
   - **Chế độ 5 - Bảng giá trị TABLE (MENU 8):**
     + Màn hình LCD hiển thị `f(x) = ...`. Giáo viên bấm phím nhập biểu thức và bấm `=`.
     + Màn hình LCD lần lượt hỏi `Start?`, `End?`, `Step?`.
     + Sau đó hiển thị bảng 2 cột `x | f(x)` cho phép cuộn bằng phím `▲ ▼`.
3. **Giữ nguyên nút Toàn màn hình độc lập:**
   - Nút `⛶ Toàn màn hình` tiếp tục nằm độc lập ngoài thanh công cụ `top-control-bar`, giữ thanh 1 hàng duy nhất (`height: 54px; flex-wrap: nowrap`).
4. **Đồng bộ hóa tuyệt đối vào Template và File Bài 12:**
   - Cập nhật cả 2 file:
     + `TROLYTHIEN/2_TAO_BAI_TAP/templates/master_bai_day_html_template.html`
     + `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/Bai_12_He_Thuc_Canh_Va_Goc_Tam_Giac_Vuong_Toan_9.html`

## Ngoài phạm vi
- Không dùng bất kỳ thẻ input form HTML nào trong widget máy tính.
- Không sửa đổi 28 bài tập Toán 9 trong slide.

## File dự kiến tác động
- `TROLYTHIEN/2_TAO_BAI_TAP/templates/master_bai_day_html_template.html`
- `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/Bai_12_He_Thuc_Canh_Va_Goc_Tam_Giac_Vuong_Toan_9.html`

## Các bước thực hiện
1. **Thiết kế lại Màn hình LCD Casio đa năng:**
   - Mở rộng container màn hình `.casio-screen` để hiển thị linh hoạt các view:
     + Màn hình tính toán tự nhiên 2 dòng (`casio-view-comp`).
     + Màn hình danh sách Menu (`casio-view-menu`).
     + Màn hình ma trận nhập hệ số phương trình & hệ phương trình (`casio-view-matrix`).
     + Màn hình thông báo kết quả nghiệm (`casio-view-eqn-res`).
     + Màn hình bảng giá trị (`casio-view-table`).
2. **Lập trình Máy trạng thái tương tác bàn phím (Keypad Event Dispatcher):**
   - Viết logic bắt sự kiện phím Casio theo trạng thái (`activeMode`):
     + Khi ở `MENU`: nhận phím `1`, `8`, `9`.
     + Khi ở `EQN_CHOOSE`: nhận phím `1` (Hệ PT), `2` (Phương trình).
     + Khi ở `MATRIX_INPUT`: phím số và dấu âm nhập vào ô hiện tại, phím `=` lưu và chuyển ô kế tiếp, phím `AC` xóa trắng ô.
     + Khi ở `EQN_RESULT`: phím `▲ ▼` hoặc `=` duyệt qua các nghiệm $x_1, x_2$, cực trị; phím `AC` trở về nhập hệ số.
     + Phím `ON` hoặc `MENU 1`: lập tức quay về trạng thái COMP.
3. **Tích hợp các thuật toán giải toán vào máy trạng thái:**
   - Giải phương trình bậc 2 (tính $\Delta$, nghiệm phân biệt, nghiệm kép, vô nghiệm, tọa độ đỉnh).
   - Giải phương trình bậc 3 (công thức Cardano nghiệm thực).
   - Giải hệ 2 phương trình bậc nhất 2 ẩn (định thức Cramer $D, D_x, D_y$).
   - Tính bảng giá trị $f(x)$.
4. **Cập nhật đồng bộ Template và Bài 12:**
   - Thay thế toàn bộ mã widget máy tính cũ bằng bộ mô phỏng máy tính vật lý thuần bàn phím mới.
5. **Kiểm thử nghiệm thu:**
   - Kiểm tra toàn bộ quy trình bấm phím bằng chuột trên máy tính Casio ảo, đảm bảo không có bất kỳ thẻ input HTML nào.

## Rủi ro
- **Rủi ro giao diện màn hình ma trận bị tràn trên màn hình LCD nhỏ:**
  - *Giải pháp:* Thiết kế font LCD dot-matrix co giãn linh hoạt hoặc hiển thị dạng dòng trượt `a = ?` -> bấm `=` -> `b = ?` -> bấm `=` -> `c = ?` cực kỳ rõ nét và dễ nhìn từ xa trên Tivi lớp học.

## Cách kiểm thử
- Mở máy tính Casio:
  + Kiểm tra: Không còn bất kỳ thẻ `<input>` nào hay các tab form web bên ngoài. Toàn bộ máy là 1 khối vật lý gồm Màn hình LCD và Bàn phím nút bấm.
  + Bấm chuột phím `MENU` -> Màn hình LCD hiện Menu chọn.
  + Bấm chuột phím số `9` -> Màn hình hiện `1: He PT`, `2: PT`.
  + Bấm phím số `2` -> Màn hình hỏi bậc -> bấm `2` -> Màn hình hiện bảng nhập hệ số $a, b, c$.
  + Bấm chuột các phím: `1`, `=`, `(-)`, `5`, `=`, `6`, `=` -> Bấm tiếp `=` màn hình hiển thị `x1 = 3`, bấm `=` tiếp hiển thị `x2 = 2`.
  + Bấm `MENU 1` -> Màn hình trở về tính toán thường.
  + Thử tính năng tính toán thông thường: bấm `sin 30 =` ra `0.5`, bấm `1/2 + 1/3 =` ra `5/6`.
- Kiểm tra file `master_bai_day_html_template.html` và file Bài 12 đồng bộ hoàn toàn.

## Tiêu chí nghiệm thu
- 100% tương tác giải toán diễn ra bằng cách dùng chuột click trực tiếp các phím của máy tính Casio, hiển thị kết quả trên màn hình LCD mô phỏng.
- Hoàn toàn loại bỏ form HTML và thẻ `<input>`.
- Giao diện và luồng bấm phím chuẩn xác như máy tính cầm tay Casio fx-580VN X ngoài đời.
- Cả file mẫu Template và bài dạy Bài 12 đều được cập nhật hoàn chỉnh.
