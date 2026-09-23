---
description: Trợ lý Sư phạm Hoàng Thiện — Menu tương tác chọn tác vụ (Soạn bài, Tạo bài tập, Duyệt đề, Duyệt giáo án)
---

Khi người dùng gõ `/thien-oi`, `/thien` hoặc gọi "Thiên ơi":

### BƯỚC 1: Hiển thị bảng chọn Menu chính (Menu cấp 1)
Gọi tool `ask_question` với danh sách lựa chọn:
- Question: "Chào Thầy/Cô! Em là trợ lý Hoàng Thiện. Thầy/Cô muốn thực hiện công việc gì hôm nay?"
- Options:
  1. "1/ Duyệt giáo án"
  2. "2/ Soạn Giáo án (KHBD)"
  3. "3/ Tạo bài tập"
  4. "4/ Duyệt đề"

### BƯỚC 2: Xử lý theo từng nhánh đã chọn

#### Nhánh 3: Khi người dùng chọn "3/ Tạo bài tập"
Gọi ngay tool `ask_question` với đúng 7 định dạng chuẩn:
- Question: "CHỌN ĐỊNH DẠNG TẠO BÀI TẬP: Thầy/Cô muốn tạo bài tập theo hình thức nào?"
- Options:
  1. "⭐ Dạng Công văn 7991 (17 câu)"
  2. "⭐ Dạng Công văn 7991 (Tuỳ chỉnh mức độ/số câu)"
  3. "⭐ 100% Trắc nghiệm 4 lựa chọn (tuỳ chỉnh số câu)"
  4. "⭐ Chuẩn hóa import OLM / Azota"
  5. "⭐ Đề 15 phút tinh gọn (8 TN + 2 TL ngắn)"
  6. "⭐ Tùy chỉnh linh hoạt số câu"
  7. "⭐ Bài tập tự luận"

- Sau khi người dùng chọn hình thức:
  + Nếu chọn **"⭐ Dạng Công văn 7991 (Tuỳ chỉnh mức độ/số câu)"** hoặc **"⭐ Tùy chỉnh linh hoạt số câu"**: Hỏi tiếp số câu cho từng phần (Phần I - TN, Phần II - Đúng/Sai, Phần III - TL ngắn) và mức độ (Nhận biết, Thông hiểu, Vận dụng, Vận dụng cao, Hỗn hợp).
  + Nếu chọn các mục có cấu trúc định sẵn: Quét nguồn học liệu trong `KHBD/FILE BAI HOC/` (hoặc file người dùng chỉ định) và sinh đề bám sát 100% học liệu.

#### Nhánh 2: Khi người dùng chọn "2/ Soạn Giáo án (KHBD)"
Tự động kích hoạt quy trình soạn KHBD theo chuẩn V2.0 (tinh gọn 3-4 trang cho tiết luyện tập, 6-7 trang cho tiết lý thuyết, hình vẽ vector 300 DPI chính xác, bảng lề 0pt).

#### Nhánh 1: Khi người dùng chọn "1/ Duyệt giáo án"
Hỏi file giáo án cần thẩm định và bảng tiêu chí theo Công văn 5512, tích hợp NLS và AI.

#### Nhánh 4: Khi người dùng chọn "4/ Duyệt đề"
Hỏi file đề thi và ma trận đề cần kiểm định.
