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
- **Bản vẽ tinh gọn tuyệt đối (Clean Diagram):** Tuyệt đối KHÔNG viết tiêu đề bài toán, KHÔNG chèn hộp chú thích, KHÔNG viết lời giải hoặc bình luận bên trong khung hình vẽ (SVG/PNG). Bản vẽ chỉ chứa thuần túy các yếu tố hình học (điểm, đoạn thẳng, đường cong, góc, ký hiệu bằng nhau và nhãn chữ cái A, B, C...) để giáo viên chèn trực tiếp vào đề thi/PowerPoint mà không bị rối mắt. Lời giải nếu có chỉ xuất ra ngoài (trong chat hoặc file HTML preview).

## File kết quả đầu ra

Ghi vào `TROLYTHIEN/11_VE_HINH/Ket_qua/`.
**Quy tắc đặt tên file theo Tên bài tập (Naming Convention):**
Tên file BẮT BUỘC đặt theo tên bài tập / câu hỏi trong đề của giáo viên, không dấu, nối bằng gạch dưới `_` để dễ quan sát và quản lý (ví dụ: `Bai_1_Hinh_Binh_Hanh_ABCD.png`, `Bai_2_Tam_Giac_ABC_Vuong_Tai_A.png`, `Cau_3_Hinh_Chop_S_ABCD.png`...).

- **Chỉ xuất ĐÚNG 1 file ảnh PNG duy nhất:** `Bai_X_[Ten_Hinh].png` — ảnh PNG độ phân giải cao 300 DPI, nền trắng sắc nét, chèn trực tiếp ngay vào Word, PowerPoint, đề kiểm tra mà không vỡ hạt.
- Tuyệt đối KHÔNG tự ý sinh các file phụ (`.svg`, `.html`, `_geogebra.txt`) để tránh làm chậm tiến trình và không làm rác thư mục, trừ khi giáo viên có yêu cầu riêng.

## Dọn dẹp file rác
Bất cứ khi nào giáo viên muốn làm sạch các file cache, file tách PDF tạm thời:
- Gọi trợ lý: *"Thiên ơi, dọn dẹp file rác"*
- Hoặc click đúp chạy file `tools/Don_Dep_File_Rac.bat` (hoặc `python tools/don_dep_file_rac.py`).
Hệ thống sẽ quét sạch toàn bộ cache và thư mục nháp, bảo toàn 100% tài liệu và sản phẩm hình vẽ trong `Ket_qua/`.

## Sửa trên canvas

Khi cần kéo điểm hoặc vẽ lại bằng tay, mở:

- https://www.hoangthiencm.id.vn/vehinh.html
- file:///c:/Users/HoangThien/Documents/GitHub/giangbai/vehinh.html

Model khuyên dùng trên trang đó là `gemini-2.5-flash`.
