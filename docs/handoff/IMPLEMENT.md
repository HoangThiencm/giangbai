# IMPLEMENT

Máy tính trợ giảng không còn form web. Mọi thao tác giải toán bằng phím trên thân máy, kết quả hiện trên màn hình LCD. Đã cập nhật file mẫu và Bài 12.

Bổ sung: `S⇔D` đổi kết quả từ phân số sang thập phân rồi bấm lại thì về phân số. `1/2+1/3` ra `5/6`, `S⇔D` ra `0.833333`, `S⇔D` nữa ra `5/6`. `sin 30` ra `0.5`, `S⇔D` ra `1/2`, bấm lại ra `0.5`. Khi máy đang mở, gõ số và phép tính trên bàn phím; Enter là `=`, Backspace là xóa. Enter lúc máy đóng vẫn mở lời giải.

## Đã làm

- `TROLYTHIEN/2_TAO_BAI_TAP/templates/master_bai_day_html_template.html`
- `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/Bai_12_He_Thuc_Canh_Va_Goc_Tam_Giac_Vuong_Toan_9.html`

28 bài và hình SVG không đổi. Nút `⛶ Toàn màn hình` vẫn nằm trên thanh, ngoài menu Tiện ích. Thanh vẫn một hàng, cao 54px. File mẫu giữ các chỗ `__JUMP_OPTIONS__`, `__TOTAL_SLIDES__`, `__SLIDES_HTML__`, `__PRINT_HTML__`, `__ORIGINAL_SVGS_JSON__`.

1. Đã xóa tab và mọi thẻ `<input>` trong widget. Thân máy còn màn LCD và bàn phím.
2. `MENU` hoặc `MODE` mở LCD:
   - `1: Tính toán (COMP)`
   - `9: Phương trình / Hệ PT (EQN)`
   - `8: Bảng giá trị (TABLE)`
3. Bấm `9` rồi `1` hỏi số ẩn từ 2 đến 4. Hệ 2 ẩn hiện ma trận `[a1]x+[b1]y=[c1]` trên LCD. Phím số và `=` nạp từng ô. `=` tiếp theo ra `x =`, rồi `=` hoặc `▼` ra `y =`. Hệ 3 và 4 ẩn dùng cùng cách nhập, mỗi lần một phương trình. `AC` ở màn kết quả quay lại bảng hệ số. `ON` hoặc `MENU` rồi `1` về tính toán.
4. Bấm `9` rồi `2` hỏi bậc 2 hoặc 3. Bậc 2 nhập a, b, c. Với `1`, `=`, `(−)`, `5`, `=`, `6`, `=`, rồi `=` nữa thì LCD ra `x1 = 3`, `=` tiếp ra `x2 = 2`, `=` tiếp ra đỉnh parabol. Δ âm thì báo vô nghiệm thực, rồi vẫn có trang đỉnh. Bậc 3 tìm nghiệm thực (Cardano, có đối chiếu đa thức).
5. Bấm `8` nhập `f(x)` bằng bàn phím. `ALPHA` chèn `x`. Rồi `Start?`, `End?`, `Step?`. Bảng `x | f(x)` cuộn bằng `▲` `▼`. Phím `∫` và `d/dx` cũng mở bảng này.
6. Chế độ tính giữ phân số, căn, sin/cos/tan, độ-phút-giây, `S⇔D`, giai thừa, `%`, Abs, π, e, Ans, `M+`.

## Kiểm thử

- Cú pháp script hai file: PASS. Widget không còn `<input>` hay tab form. Bài 12 còn 28 đề, kể cả hình chữ nhật ABCD.
- Chuỗi phím `MENU 9 2 2` rồi `1 = (−) 5 = 6 = =` ra `x1 = 3`, `=` tiếp ra `x2 = 2`, `=` tiếp ra đỉnh `x = 2.5`, `y = -0.25`. `MENU 1` về màn tính.
- `sin 30 =` ra `0.5`. `1/2 + 1/3 =` ra `5/6`, `S⇔D` ra `0.833333`.
- Hệ `2x+y=5`, `x−y=1`: `x = 2`, `▼` ra `y = 1`. `AC` quay lại ma trận.
- `x³−6x²+11x−6=0` ra `x1 = 1`, `x2 = 2`, `x3 = 3`.
- Bảng `x^2` từ 1 đến 3 bước 1 ra `1 | 1`, `2 | 4`, `3 | 9`. `ON` về màn tính.
- Edge headless mở Bài 12: `data-lesson-boot="ok"`, thanh cao 54px. Chưa bấm phím bằng chuột trên màn hình thật.

## Chưa làm

- Không commit, không push.
