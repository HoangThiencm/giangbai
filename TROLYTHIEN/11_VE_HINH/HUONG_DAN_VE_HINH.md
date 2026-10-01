# Hướng dẫn vẽ hình học cực kỳ chính xác (Nhánh 11)

File này là `TROLYTHIEN/11_VE_HINH/HUONG_DAN_VE_HINH.md`.

Dùng khi người dùng chọn **11/ Vẽ hình học cực kỳ chính xác (từ đề bài / ảnh)** trong trợ lý `/thien`.

## Đầu vào

- Chữ đề bài dán trong chat.
- Hoặc file trong `TROLYTHIEN/11_VE_HINH/Dau_vao/`: ảnh `.png`, `.jpg`, đề `.txt`, `.docx`.
- Đọc hết giả thiết, kết luận, số đo, ký hiệu trên ảnh. Ảnh mờ, nghiêng, thiếu sáng hoặc thiếu dữ kiện: dừng và hỏi người dùng xác nhận, không đoán số đo.

## Tọa độ giải tích

Dựng trên hệ trục Oxy. Không vẽ ước lượng.

- Chọn một đỉnh làm gốc. Cạnh đáy nằm ngang khi đề không buộc hướng khác.
- Trung điểm M của BC: `M = ((B.x+C.x)/2, (B.y+C.y)/2)`.
- Điểm trọng tâm G của ABC: `G = ((A.x+B.x+C.x)/3, (A.y+B.y+C.y)/3)`.
- Chân đường cao: đường cao kẻ từ A xuống BC là giao của đường thẳng qua A vuông góc với BC và đường thẳng BC.
- Giao của hai đường cao là trực tâm.
- Tiếp điểm, giao đường tròn: giải hệ phương trình, lấy đúng nghiệm theo đề.
- Giữ tỉ lệ thật: hình vuông cạnh bằng nhau và góc vuông; hình thoi bốn cạnh bằng nhau; hình thang cân hai đáy song song và hai cạnh bên đối xứng.

## Ký hiệu GDPT 2018

- Cạnh là đoạn thẳng, không phải đường thẳng vô hạn.
- Góc vuông: dấu vuông nhỏ nằm trong góc.
- Cạnh bằng nhau: vạch ngang trên cạnh. Góc bằng nhau: cùng số cung.
- Nhãn đỉnh A, B, C đặt lệch ra ngoài hình, không đè lên nét vẽ.
- Hình không gian (chóp, lăng trụ): một góc nhìn phối cảnh cố định. Cạnh nhìn thấy nét liền. Cạnh khuất nét đứt.

## Bốn file kết quả

Ghi vào `TROLYTHIEN/11_VE_HINH/Ket_qua/`. Tên không dấu cách, ví dụ `Tam_giac_ABC`.

1. `[Ten_Hinh].png` — ảnh PNG độ phân giải cao nền trắng sắc nét, chèn trực tiếp ngay vào Word, PowerPoint, bài kiểm tra, Zalo mà không cần đổi đuôi.
2. `[Ten_Hinh].svg` — SVG độc lập, có `viewBox`, nền trắng, nét đen, vector sắc nét không vỡ hạt.
3. `[Ten_Hinh]_geogebra.txt` — mỗi dòng một lệnh GeoGebra: `Point`, `Segment`, `Circle`, `Intersect`, `Polygon`, `PerpendicularLine`, `Midpoint`. Cạnh dùng `Segment`, không dùng `Line` vô hạn. Đường phụ đặt tên `aux_` rồi `SetVisibleInView(aux_, 1, false)`. Không ghi chú thích `//` hay `#`.
4. `[Ten_Hinh].html` — một file mở bằng trình duyệt, nhúng đúng SVG, có nút tải PNG, nút tải SVG và nút copy lệnh GeoGebra.

## Sửa trên canvas

Khi cần kéo điểm hoặc vẽ lại bằng tay, mở:

- https://www.hoangthiencm.id.vn/vehinh.html
- file:///c:/Users/HoangThien/Documents/GitHub/giangbai/vehinh.html

Model khuyên dùng trên trang đó là `gemini-2.5-flash`.
