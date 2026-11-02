# Hướng dẫn chuyển ghi âm thành văn bản (iPhone / MP3)

File này là `TROLYTHIEN/13_CHUYEN_GHI_AM/HUONG_DAN_CHUYEN_GHI_AM.md`. Master Prompt nằm tại `TROLYTHIEN/13_CHUYEN_GHI_AM/PROMPT_CHUYEN_GHI_AM.md`.

Dùng khi chọn **13/ Chuyển ghi âm thành văn bản (iPhone / MP3)** trong trợ lý `/thien` hoặc gọi "Thiên ơi, bóc tách ghi âm".

Nhánh này bóc tách âm thanh thành văn bản trung thực, tự nhiên, đạt độ chính xác từ 90% đến 95%. Không tự ý gọt giũa hay ép theo thuật ngữ sách vở nếu người nói không nói.

## Đặt tệp đầu vào

1. Chuyển tệp ghi âm từ điện thoại iPhone (ứng dụng Ghi âm - Voice Memos), Android, máy ghi âm hoặc máy tính vào thư mục:
   `TROLYTHIEN/13_CHUYEN_GHI_AM/Dau_vao/`
2. Hỗ trợ đầy đủ các định dạng phổ biến:
   - `.m4a` (định dạng ghi âm chuẩn của iPhone)
   - `.mp3`
   - `.wav`
   - `.aac`
3. Mỗi lần xử lý một hoặc nhiều tệp. Tên tệp viết không dấu hoặc có dấu nối, ví dụ: `Ghi_am_hop_to.m4a`, `Du_gio_tiet_toan.mp3`.

## Quy trình bóc tách

1. Trợ lý đọc trực tiếp tệp âm thanh trong `TROLYTHIEN/13_CHUYEN_GHI_AM/Dau_vao/`.
2. Áp dụng `TROLYTHIEN/13_CHUYEN_GHI_AM/PROMPT_CHUYEN_GHI_AM.md`.
3. Bóc tách nguyên văn trung thực theo đúng lời nói của người phát biểu (độ chính xác 90–95%).
4. Dựa theo ngữ cảnh thực tế của cuộc nói chuyện (sư phạm, hành chính, đạo tràng, đời sống) để tự động sửa lỗi chính tả chuẩn xác (sửa phát âm địa phương hỏi/ngã, s/x, tr/ch, d/gi, n/l và từ đồng âm) nhưng không làm biến đổi ý của người nói.
5. Tự động ngắt câu, đặt dấu chấm, phẩy và chia đoạn tự nhiên theo nhịp nói giúp nội dung mạch lạc, dễ đọc.
6. Nếu nhận diện được nhiều người phát biểu (như Chủ trì cuộc họp, các giáo viên đóng góp ý kiến), tự động xuống dòng phân biệt người nói.

## Nhận tệp thành phẩm

Kết quả được tự động xuất đồng thời 2 tệp vào thư mục:

`TROLYTHIEN/13_CHUYEN_GHI_AM/Ket_qua/`

1. **Tệp Word `.docx` hoàn chỉnh:**
   - Tên tệp: `[Ten_File].docx`
   - Tiêu chuẩn in ấn: Phông Times New Roman 13pt, căn đều hai bên (JUSTIFY), dãn dòng 1.2, thụt đầu dòng 1.27 cm, lề A4 chuẩn (Top 20mm, Bottom 20mm, Left 30mm, Right 15mm).
   - Có tiêu đề tên tệp ghi âm và ngày giờ bóc tách.
2. **Tệp văn bản thuần `.txt`:**
   - Tên tệp: `[Ten_File].txt`
   - Nội dung gọn nhẹ, hỗ trợ sao chép nhanh sang Zalo, email hoặc dán vào văn bản khác.

## Phản hồi chat ngắn

Chat phản hồi ngắn gọn 2–3 dòng:
1. Đã bóc tách xong tệp ghi âm.
2. Đường dẫn tệp `.docx` và `.txt` trong `TROLYTHIEN/13_CHUYEN_GHI_AM/Ket_qua/`.
3. Trích dẫn 1–2 câu mở đầu để người dùng nhận diện nội dung.
