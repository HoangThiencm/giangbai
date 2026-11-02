# Duyệt đề kiểm tra
**Phiên bản: VERSION 2.0.0 (BẢN VÁ KỶ LUẬT DUYỆT ĐỀ & ZERO-RESIDUE)**

Phân hệ `4_DUYET_DE` áp dụng quy chuẩn tại file `TROLYTHIEN/4_DUYET_DE/HUONG_DAN_DUYET_DE.md` và tuân thủ Công văn 7991/BGDĐT-GDTrH, Công văn 5512 và Nghị định 30/2020/NĐ-CP.

## Nhiệm vụ

Thẩm định đề giáo viên đưa (tệp hoặc chữ dán). Không viết một đề mới thay cho việc duyệt, trừ khi giáo viên yêu cầu phương án chỉnh từng câu.

## Việc cần làm

- Đối chiếu ma trận theo các mức nhận biết, thông hiểu, vận dụng, vận dụng cao khi đề theo Công văn 7991/BGDĐT-GDTrH.
- Kiểm tra đáp án, thang điểm và số điểm có khớp câu hỏi.
- Chỉ ra lỗi chính tả, lệch chuyên môn, câu mơ hồ, phương án nhiễu không hợp lệ.
- Không bịa căn cứ ngoài đề và công văn đã nêu. Thiếu đáp án thì ghi rõ «đề không kèm đáp án».
- Chữ ký giáo viên và tổ trưởng lấy trực tiếp từ kho chữ ký trong suốt siêu nét tại `TROLYTHIEN/4_DUYET_DE/Ket_qua/chu_ky/`.

## Đầu ra

Một file biên bản `.docx` hoặc `.md`. Với mỗi câu: đạt, hoặc cần sửa kèm phương án chỉnh ngắn. Không sửa mã nguồn website.

## Kỷ luật vệ sinh thư mục bắt buộc (Zero-Residue Policy)

- Tuyệt đối không để lại file rác, ảnh chụp trang PDF tạm (`page_*.png`, `v*_page_*.png`) hay file test nháp trong thư mục `Ket_qua` và `Dau_vao`.
- Sau khi hoàn thành xuất biên bản hoặc đề cương chuẩn hóa, bắt buộc chạy công cụ dọn rác tự động:
  `python TROLYTHIEN/engine/clean_temp_files.py` để làm sạch toàn bộ môi trường lưu trữ.
