# QUY CHUẨN SOẠN THẢO BÁO CÁO VÀ VĂN BẢN HÀNH CHÍNH (TẠO BÁO CÁO)

Áp dụng cho mọi tác vụ soạn thảo báo cáo, kế hoạch, tờ trình, quyết định hành chính trong Trợ lý Hoàng Thiên. Tham chiếu trực tiếp từ chuẩn `taobaocao.html`.

## 1. Nguồn dữ liệu đầu vào & Kết quả
- **Đầu vào:** Tự động đọc dữ liệu trong thư mục `TROLYTHIEN/8_TAO_BAO_CAO/Dau_vao/`:
  + Tệp văn bản căn cứ pháp lý, chỉ đạo cấp trên (PDF, Word, TXT).
  + Tệp số liệu thực tế, định hướng công tác tới, hoặc dự thảo nội dung.
  + Tệp văn bản mẫu của đơn vị.
  + Tệp hướng dẫn chuẩn: `TROLYTHIEN/8_TAO_BAO_CAO/Dau_vao/HUONG_DAN_TAO_BAO_CAO.md`.
- **Kết quả:** Tự động xuất file Word `.docx` hoàn chỉnh lưu tại `TROLYTHIEN/8_TAO_BAO_CAO/Ket_qua/`.

## 2. NGUYÊN TẮC BẮT BUỘC TỪ NHÀ TRƯỜNG: "KẾ HOẠCH GỐI ĐẦU & ĐỐI CHIẾU ĐÁNH GIÁ LIÊN HOÀN"
> ⚠️ **CHỈ ĐẠO CỦA NHÀ TRƯỜNG:**
> "Triển khai ở tháng trước sẽ có đánh giá ở tháng sau. Ví dụ muốn dạy tiết Nghiên cứu bài học (NCBH) trong tháng 11 thì trong tháng 10 phải có phân công nhiệm vụ GV dạy. Muốn thực hiện bài học STEM trong tháng 11 thì tháng 10 cũng phải phân công nhiệm vụ chuẩn bị."

- **Đánh giá công tác qua / Đánh giá giai đoạn:** Bắt buộc đối chiếu kết quả thực hiện các nhiệm vụ đã phân công từ tháng trước (tiết NCBH, hoạt động STEM, nộp đề kiểm tra, hồ sơ chuyên môn...).
- **Công tác tới / Kế hoạch trọng tâm:** Bắt buộc có mục **"Phân công nhiệm vụ gối đầu cho tháng tiếp theo"** (Phân công người dạy minh họa NCBH, người hỗ trợ; phân công GV phụ trách bài học STEM, học liệu; phân công ra đề kiểm tra).

## 3. Thể thức văn bản chuẩn Nghị định 30/2020/NĐ-CP & Hướng dẫn 05-HD/VPTW (Văn bản Đảng)
- **Phông chữ & Cỡ chữ:** Bắt buộc `Times New Roman`. Toàn bộ phần nội dung văn bản, căn cứ, điều, khoản, điểm dùng **đồng nhất cỡ chữ 13pt** (không dùng lẫn lộn 11.5pt hay 12.5pt).
- **Thụt đầu dòng đoạn văn:** Bắt buộc **lùi đầu dòng 1,27 cm (0.5 inch)** cho tất cả các đoạn văn, điều, khoản, điểm và từng dòng Căn cứ ban hành.
- **Căn lề & Dãn dòng:** Căn đều hai bên (`JUSTIFY`), dãn dòng cố định **1.2 dòng** (`line_spacing = 1.2`), dãn đoạn `space_before = 2pt`, `space_after = 3pt`.
- **Định lề trang A4:** Trên 20mm, Dưới 20mm, Trái 30mm, Phải 15mm.
- **Đóng khung bảng biểu:** Toàn bộ bảng dữ liệu phải **đóng khung kín 4 cạnh viền ngoài và các đường kẻ bên trong** (`top`, `bottom`, `left`, `right`, `insideH`, `insideV` đều là đường đơn `single`, màu đen, độ dày 0.5pt). Bỏ hẳn kiểu bảng hở viền trái/phải. Kèm thuộc tính chống xé dòng (`cantSplit`) và lặp lại dòng tiêu đề khi sang trang (`tblHeader`).
- **Căn cứ ban hành:** Chữ in thường, kiểu chữ nghiêng, cỡ 13pt, thụt đầu dòng 1.27cm; dòng cuối kết thúc bằng dấu phẩy (,), các dòng trước kết thúc bằng dấu chấm phẩy (;).
<<<<<<< Updated upstream
- Chi tiết xem tại quy tắc: `.agents/rules/chuan_hoa_van_ban_nd30_vptw.md`.

## 4. Quy tắc bắt buộc về cơ quan hành chính (Mô hình chính quyền 2 cấp)
=======
- **Văn bản của Đảng (Hướng dẫn số 05-HD/VPTW năm 2026):**
  + Tiêu đề góc phải: `ĐẢNG CỘNG SẢN VIỆT NAM` (in hoa, đậm, cỡ 13-14), dòng dưới là Địa danh, ngày tháng (nghiêng).
  + Góc trái: Cấp ủy cấp trên / Cơ quan ban hành (in hoa, đậm, có gạch ngang dưới).
- Chi tiết xem tại quy tắc: `.agents/rules/chuan_hoa_van_ban_nd30_vptw.md`.

## 3. Quy tắc bắt buộc về cơ quan hành chính (Mô hình chính quyền 2 cấp)
>>>>>>> Stashed changes
- 🔴 **TUYỆT ĐỐI CẤM:** Không nhắc đến hoặc tạo nội dung liên quan đến các cơ quan cấp huyện đã bãi bỏ:
  + Cấm dùng: "Phòng Giáo dục và Đào tạo", "Phòng GD&ĐT", "UBND huyện", "HĐND huyện", "Huyện ủy", "Ban thanh tra nhân dân", "Công đoàn cơ sở", "Liên đoàn Lao động".
- **Cơ quan ban hành hiện hành:** Chỉ sử dụng cơ quan Nhà trường (ví dụ "TRƯỜNG THCS TRẦN PHÚ - TỔ TOÁN - TIN HỌC") hoặc UBND Xã/Phường quản lý trực tiếp.
- Đối với văn bản lịch sử trích dẫn: Giữ nguyên tên cơ quan trong văn bản trích dẫn.

<<<<<<< Updated upstream
## 5. Hai chức năng đặc thù Tổ Toán – Tin học (Trường THCS Trần Phú)

### 5.1. Biên bản họp tổ Toán – Tin (3 phần chuẩn):
- **I. Triển khai văn bản:** Đọc tất cả các văn bản đầu vào; tóm tắt ngắn gọn súc tích nội dung cốt lõi và số hiệu/ngày. Nếu cần thiết thì cân nhắc phân công cho các giáo viên thực hiện văn bản đó.
- **II. Đánh giá công tác giai đoạn:** Đánh giá các mặt công tác chuyên môn; **đối chiếu và nhận xét việc thực hiện các nhiệm vụ NCBH/STEM đã phân công từ tháng trước**; KHBD (tích hợp NLS/AI), nề nếp giảng dạy, sổ đầu bài, ngày giờ công, công tác dạy thay, quy chế chuyên môn...
- **III. Công tác tới:** Bám sát định hướng của Thầy Tổ trưởng; **bắt buộc phân công gối đầu cho tháng tiếp theo** (GV dạy minh họa NCBH, GV phụ trách bài học STEM, phân công ra đề kiểm tra...).

### 5.2. Kế hoạch & Báo cáo hoạt động tổ theo tháng (Form THCS Trần Phú):
- **Bố cục 4 phần chuẩn ảnh:**
  + **I. Đánh giá công tác qua:** 1. Chủ nhiệm; 2. Ngày giờ công (kèm chi tiết dạy thay); 3. Hoạt động tổ chuyên môn (đối chiếu tiết NCBH và bài học STEM đã phân công tháng trước; PCCM, KHGD phụ lục 1,2,3, NLS 20%, AI 12 tiết, VioEdu khối 6-9, tập huấn CSDL ngành, tiến độ KHBD...); 4. Công tác khác.
  + **II. Kế hoạch trọng tâm trong thời gian tới:** 1. Chủ nhiệm; 2. Ngày giờ công; 3. Hoạt động tổ chuyên môn (phân công gối đầu tháng tới: phân công GV dạy minh họa NCBH, phân công bài học STEM, ra đề kiểm tra định kỳ...); 4. Công tác khác.
=======
## 4. Hai chức năng đặc thù Tổ Toán – Tin học (Trường THCS Trần Phú)

### 4.1. Biên bản họp tổ Toán – Tin (3 phần chuẩn):
- **I. Triển khai văn bản:** Đọc tất cả các văn bản đầu vào; tóm tắt ngắn gọn súc tích nội dung cốt lõi và số hiệu/ngày. Nếu cần thiết thì cân nhắc phân công cho các giáo viên thực hiện văn bản đó.
- **II. Đánh giá công tác giai đoạn:** Đánh giá các mặt công tác chuyên môn: KHBD (tích hợp NLS/AI), nề nếp giảng dạy, sổ đầu bài, ngày giờ công, công tác dạy thay, quy chế chuyên môn...
- **III. Công tác tới:** Bám sát định hướng của Thầy Tổ trưởng; cân nhắc phân công giáo viên trong tổ thực hiện từng nhiệm vụ cụ thể rõ ràng.

### 4.2. Kế hoạch & Báo cáo hoạt động tổ theo tháng (Form THCS Trần Phú):
- **Bố cục 4 phần chuẩn ảnh:**
  + **I. Đánh giá công tác qua:** 1. Chủ nhiệm; 2. Ngày giờ công (kèm chi tiết dạy thay); 3. Hoạt động tổ chuyên môn (PCCM, KHGD phụ lục 1,2,3, NLS 20%, AI 12 tiết, VioEdu khối 6-9, tập huấn CSDL ngành, tiến độ KHBD...); 4. Công tác khác.
  + **II. Kế hoạch trọng tâm trong thời gian tới:** 1. Chủ nhiệm; 2. Ngày giờ công; 3. Hoạt động tổ chuyên môn; 4. Công tác khác.
>>>>>>> Stashed changes
  + **III. Đánh giá thi đua trong tháng:** Bảng biểu đóng khung kín 4 cạnh viền ngoài và các đường kẻ trong, 7 cột: `| STT | HỌ VÀ TÊN | CHỨC VỤ | TỰ XẾP LOẠI | TỰ NHẬN XÉT | TỔ XẾP LOẠI | GHI CHÚ |`. Dòng 1 là Thầy Hoàng Tấn Thiên (Tổ trưởng, loại A); các dòng tiếp theo là khung danh sách giáo viên trong tổ (Thầy sẽ cung cấp sau).
  + **IV. Đề xuất, kiến nghị trong thời gian tới:** Ghi "Không" hoặc đề xuất cụ thể.
  + **Chữ ký cuối:** Ban giám hiệu (trái) và Tổ trưởng Hoàng Tấn Thiên (phải).

<<<<<<< Updated upstream
## 6. Quy tắc in đỏ bắt buộc cho nội dung chưa chắc chắn
- 🔴 **BẮT BUỘC:** Tất cả các nội dung, số liệu, danh sách phân công NCBH/STEM dự kiến, người dạy thay, tiết dạy thay hoặc kết quả thi đua chưa chắc chắn / chưa có trong hồ sơ đầu vào **PHẢI ĐƯỢC IN CHỮ MÀU ĐỎ** (`<w:color w:val="FF0000"/>` hoặc `RGBColor(255, 0, 0)`) trong file Word `.docx` để Thầy Tổ trưởng dễ dàng rà soát và hoàn thiện.
- Trong bản nháp hiển thị: `[CHỮ ĐỎ: nội dung]` hoặc `<span style="color:red">nội dung</span>`.

## 7. Công cụ trực tuyến liên kết
=======
## 5. Quy tắc in đỏ bắt buộc cho nội dung chưa chắc chắn
- 🔴 **BẮT BUỘC:** Tất cả các nội dung, số liệu, danh sách phân công, người dạy thay, tiết dạy thay hoặc kết quả thi đua chưa chắc chắn / chưa có trong hồ sơ đầu vào **PHẢI ĐƯỢC IN CHỮ MÀU ĐỎ** (`<w:color w:val="FF0000"/>` hoặc `RGBColor(255, 0, 0)`) trong file Word `.docx` để Thầy Tổ trưởng dễ dàng rà soát và hoàn thiện.
- Trong bản nháp hiển thị: `[CHỮ ĐỎ: nội dung]` hoặc `<span style="color:red">nội dung</span>`.

## 6. Công cụ trực tuyến liên kết
>>>>>>> Stashed changes
- **Gemini Canvas Tạo báo cáo:** [https://gemini.google.com/app/7bc03567b9f738fb?hl=vi](https://gemini.google.com/app/7bc03567b9f738fb?hl=vi)
- **Công cụ web nội bộ:** [backupcode viettailieu/taobaocao.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/backupcode%20viettailieu/taobaocao.html)
