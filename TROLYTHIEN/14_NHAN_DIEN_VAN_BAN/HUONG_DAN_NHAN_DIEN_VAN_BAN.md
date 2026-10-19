# Hướng dẫn nhận diện văn bản (OCR Thông minh)

File này là `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/HUONG_DAN_NHAN_DIEN_VAN_BAN.md`. Master Prompt nằm tại `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/PROMPT_NHAN_DIEN_VAN_BAN.md`.

Dùng khi chọn **14/ Nhận diện văn bản (OCR Thông minh)**.

Kết luận nghiệm thu: Đã có quy tắc kiểm soát; hiệu quả cần được xác minh qua bộ mẫu thử nghiệm.

## Đặt tệp đầu vào

1. Đưa PDF, ảnh scan hoặc ảnh chữ viết tay vào `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/Dau_vao/`.
2. Định dạng: `.pdf`, `.png`, `.jpg`, `.jpeg`.
3. Tên tệp ngắn, ví dụ `De_giua_ky_toan_6.pdf`, `Bai_viet_tay.jpg`.
4. Có thể kèm tệp cùng tên `.recognition.json` khi đã có kết quả đọc cấu trúc. Engine vẫn cắt ảnh đối chứng từ tệp gốc.

## Bảy quy tắc đầu ra

1. Toàn bộ đoạn văn và ô bảng dùng Times New Roman, cỡ 14pt.
2. Bảng giữ đúng số hàng, số cột, ô gộp và viền bốn cạnh.
3. Chữ gạch xóa giữ `strikethrough`. Ghi chú lề viết dạng `[Ghi chú lề: ...]`, không trộn vào câu chính.
4. Vùng PDF có lớp text lấy bằng PyMuPDF. Vùng scan, ảnh chụp, chữ viết tay và công thức đi qua Vision. Model mặc định `gemini-2.5-flash`. Khi gọi lỗi, fallback cùng họ model đã cấu hình, không bịa nội dung thay thế.
5. Công thức rõ và chuyển OMML thành công thì chèn Word Equation `m:oMath` cỡ 14pt. Công thức mờ hoặc lỗi OMML thì cắt ảnh từ bản gốc và ghi nhãn đỏ `[Công thức chưa đọc rõ / Lỗi chuyển đổi — Mã NDxx]`.
6. Năm tình huống in đậm, màu đỏ RGB 255, 0, 0, có mã `ND01`, `ND02`:
   - Nhiều cách đọc.
   - Đọc được một phần.
   - Không đọc được: bắt buộc kèm ảnh cắt vùng nguồn.
   - Nội dung bị lẹm mép giấy.
   - Nghi bản gốc sai số liệu hoặc chính tả: giữ nguyên chữ gốc màu đen, thêm dòng đỏ đề nghị kiểm tra.
7. Hình vẽ mặc định là ảnh cắt gốc. Chỉ tái tạo khi đủ tọa độ hoặc nhãn đỉnh và góc vuông. Khi tái tạo, file Word có cả hình tái tạo, ảnh cắt gốc và nhãn đỏ. Ảnh mờ chỉ giữ ảnh cắt và nhãn đỏ.

Trước khi xuất, đối soát từng vùng trên trang nguồn. Trang cuối của Word là bảng Audit Log. Cạnh file Word là JSON metadata.

## Năm điểm bổ sung

1. Model Vision chốt ở `gemini-2.5-flash`, có fallback khi lỗi kết nối hoặc từ chối.
2. JSON lưu `NDxx`, `page`, `bbox`, `type`, `raw_text`, `suggestion`.
3. Ảnh đối chứng cắt từ bản gốc. Bản tăng tương phản chỉ để đọc, không ghi đè gốc.
4. `m:oMath` đặt cỡ 14pt và nằm trong đoạn văn, không thay bằng ảnh khi chuyển đổi thành công.
5. Trạng thái mặc định là đã chuyển đổi, còn vị trí cần đối chiếu. Chỉ ghi đã được người dùng xác nhận khi có cờ xác nhận. Không kết luận đã nhận diện hoàn hảo nếu chưa qua bộ mẫu.

## Lệnh

```bash
python -m TROLYTHIEN.engine.nhan_dien_engine --input "TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/Dau_vao/ten_tep.pdf"
```

Kết quả: `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/Ket_qua/[Ten_File].docx` và `[Ten_File].json`.

## Chat

Hai hoặc ba dòng: đã xuất Word, đường dẫn, và câu "Đã có quy tắc kiểm soát; hiệu quả cần được xác minh qua bộ mẫu thử nghiệm".
