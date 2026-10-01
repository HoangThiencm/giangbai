# Hướng dẫn chuẩn hoá văn bản (Hành chính / Đảng)

File này là `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/HUONG_DAN_CHUAN_HOA_VAN_BAN.md`. Master Prompt nằm tại `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/PROMPT_CHUAN_HOA_VAN_BAN.md`.

Dùng khi chọn **12/ Chuẩn hoá văn bản (Hành chính / Đảng)** trong trợ lý `/thien`.

Nhánh này nhận tệp Word đã soạn và trả tệp Word đã chỉnh thể thức. Không soạn văn bản mới thay cho nội dung nguồn.

## Đặt tệp đầu vào

1. Lưu bản cần chuẩn hoá dưới dạng Word `.docx`.
2. Copy vào `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/Dau_vao/`.
3. Mỗi lần xử lý một tệp. Tên tệp không dấu, nối bằng gạch dưới, ví dụ `Ke_hoach_nam_hoc.docx`.
4. Giữ nguyên bảng biểu trong Word. Không chuyển bảng thành ảnh.

Tệp nguồn thường lệch phông (Calibri, Arial, Times New Roman), lệch cỡ chữ (11pt, 12pt, 13pt), thụt dòng bằng phím Space, dãn dòng không đều, bảng hở viền hoặc bị xé sang trang, sai Quốc hiệu - Tiêu ngữ hoặc sai tiêu đề Đảng.

## Quy trình thẩm định

1. Đọc toàn bộ đoạn văn và mọi ô bảng trong tệp `.docx`.
2. Áp dụng `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/PROMPT_CHUAN_HOA_VAN_BAN.md`.
3. Nhận diện ngay: văn bản hành chính theo Nghị định 30/2020/NĐ-CP, hoặc văn bản Đảng theo Quy định 399-QĐ/TW và Hướng dẫn 05-HD/VPTW.
4. Sửa chính tả, dấu câu, thể thức, căn cứ còn hiệu lực và thẩm quyền ký.
5. Cảnh báo mô hình chính quyền 2 cấp nếu văn bản ban hành mới còn tên cơ quan cấp huyện đã bãi bỏ: Phòng Giáo dục và Đào tạo, UBND huyện, HĐND huyện, Huyện ủy.
6. Giữ nguyên số liệu. Chỗ thiếu ghi `[cần xác minh]`, không điền số, ngày, số hiệu giả.

Phản hồi trong chat đủ 5 phần:

1. Kết luận nhận diện
2. Bản văn đã chuẩn hoá
3. Bảng các lỗi đã chỉnh
4. Nội dung cần xác minh
5. Cảnh báo pháp lý/thẩm quyền

## Nhận tệp thành phẩm

File Word hoàn chỉnh nằm tại:

`TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/Ket_qua/[Ten_File]_Chuan_Hoa.docx`

Ví dụ `Ke_hoach_nam_hoc.docx` cho ra `Ke_hoach_nam_hoc_Chuan_Hoa.docx`.

Kỹ thuật in của tệp kết quả:

- Phông Times New Roman, nội dung 13pt.
- Thụt đầu dòng 1,27 cm.
- Khổ A4, lề trên 20 mm, dưới 20 mm, trái 30 mm, phải 15 mm.
- Bảng đóng khung 4 cạnh. Hàng không bị xé trang (`cantSplit`). Dòng tiêu đề lặp khi sang trang (`tblHeader`).
