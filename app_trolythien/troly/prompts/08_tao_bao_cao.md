# HƯỚNG DẪN TẠO BÁO CÁO & VĂN BẢN HÀNH CHÍNH (CHUẨN NĐ 30/2020)

Thư mục này dùng để chứa tài liệu căn cứ, biểu mẫu và dữ liệu đầu vào cho Trợ lý Hoàng Thiên soạn thảo Báo cáo và Văn bản hành chính.

---

## 1. Cách sử dụng đầu vào (`Dau_vao`)
Thầy/Cô hãy sao chép các tệp tài liệu liên quan vào thư mục này:
- **Tệp văn bản căn cứ:** Các thông tư, hướng dẫn, kế hoạch cấp trên (PDF, DOCX, TXT).
- **Tệp số liệu / dự thảo:** Bảng tổng hợp số liệu, biên bản cuộc họp, ghi chú nội dung, định hướng công tác tới.
- **Tệp văn bản mẫu:** Mẫu báo cáo các năm trước để AI kế thừa bố cục và cách hành văn.

---

## 2. Hai chức năng chuyên sâu mới cho Tổ Toán – Tin học:

### 🌟 CHỨC NĂNG 1: BIÊN BẢN HỌP TỔ TOÁN – TIN (3 PHẦN CHUẨN)
- **Cấu trúc bắt buộc:**
  + **I. Triển khai văn bản:** Đọc tất cả các văn bản đầu vào do Thầy cung cấp; triển khai ngắn gọn, súc tích trọng tâm của từng văn bản. Nếu cần thiết thì cân nhắc phân công cho các giáo viên thực hiện văn bản đó.
  + **II. Đánh giá công tác giai đoạn:** Đánh giá tình hình chuyên môn qua các mặt: KHBD, nề nếp giảng dạy, sổ đầu bài, ngày giờ công, công tác dạy thay, kiểm tra thường xuyên/định kỳ...
  + **III. Công tác tới:** Bám sát định hướng của Thầy Tổ trưởng để cụ thể hóa công việc; cân nhắc để phân công giáo viên trong tổ thực hiện từng nhiệm vụ rõ ràng.
- **Quy chuẩn chi tiết:** Xem tại [08_bien_ban_hop_to.md](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/app_trolythien/troly/prompts/08_bien_ban_hop_to.md).

### 🌟 CHỨC NĂNG 2: KẾ HOẠCH & BÁO CÁO HOẠT ĐỘNG TỔ THEO THÁNG (FORM THCS TRẦN PHÚ)
- **Cấu trúc chuẩn form thực tế của nhà trường:**
  + **Tiêu đề:** `BÁO CÁO HOẠT ĐỘNG TỔ TOÁN – TIN HỌC THÁNG .../...` (hoặc `KẾ HOẠCH VÀ BÁO CÁO HOẠT ĐỘNG TỔ...`).
  + **Căn cứ:** Căn cứ chỉ đạo định hướng nhà trường và tình hình thực tế hoạt động chuyên môn của tổ.
  + **I. Đánh giá công tác qua:** 1. Chủ nhiệm; 2. Ngày giờ công (chi tiết dạy thay: người dạy thay, tiết dạy thay); 3. Hoạt động tổ chuyên môn (PCCM, KHGD phụ lục 1,2,3, NLS 20%, AI 12 tiết, VioEdu khối 6-9, tập huấn CSDL ngành, tiến độ KHBD...); 4. Công tác khác (khai giảng, lao động, phổ cập...).
  + **II. Kế hoạch trọng tâm trong thời gian tới:** 1. Chủ nhiệm; 2. Ngày giờ công; 3. Hoạt động tổ chuyên môn (đề cương, đề kiểm tra định kỳ, quy chế cho điểm, nộp KHBD CSDL ngành, kiểm tra nội bộ...); 4. Công tác khác.
  + **III. Đánh giá thi đua trong tháng:** Bảng biểu đóng khung kín 4 cạnh viền ngoài và các đường kẻ trong, đúng 7 cột: `| STT | HỌ VÀ TÊN | CHỨC VỤ | TỰ XẾP LOẠI | TỰ NHẬN XÉT | TỔ XẾP LOẠI | GHI CHÚ |`. Dòng 1 là Thầy Hoàng Tấn Thiên (Tổ trưởng, loại A); các dòng tiếp theo là khung danh sách giáo viên trong tổ (Thầy sẽ cung cấp danh sách sau).
  + **IV. Đề xuất, kiến nghị trong thời gian tới:** Ghi "Không" hoặc đề xuất cụ thể.
  + **Chữ ký cuối văn bản:** Ban giám hiệu (cột trái) | Tổ trưởng: Hoàng Tấn Thiên (cột phải).
- **Quy chuẩn chi tiết:** Xem tại [08_ke_hoach_thang_to.md](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/app_trolythien/troly/prompts/08_ke_hoach_thang_to.md).

---

## 3. Quy tắc bắt buộc: In đỏ nội dung chưa chắc chắn
- 🔴 **BẮT BUỘC:** Mọi thông tin, số liệu, danh sách phân công, tiết dạy thay hoặc nội dung chưa chắc chắn / chưa chốt số liệu trong đầu vào **PHẢI ĐƯỢC IN CHỮ MÀU ĐỎ** (`<w:color w:val="FF0000"/>` hoặc `RGBColor(255, 0, 0)`) trong file Word `.docx` để Thầy Tổ trưởng dễ dàng rà soát và hoàn thiện.
- Trong bản nháp hiển thị dạng: `[CHỮ ĐỎ: nội dung]` hoặc `<span style="color:red">nội dung</span>`.

---

## 4. Các loại văn bản khác (Theo chuẩn Nghị định 30/2020/NĐ-CP):
- **BÁO CÁO CHUYÊN MÔN:** Định kỳ, đột xuất, sơ kết, tổng kết.
- **KẾ HOẠCH CHUYÊN MÔN:** Năm học, ôn tập, ngoại khóa.
- **TỜ TRÌNH, QUYẾT ĐỊNH, CÔNG VĂN, THÔNG BÁO.**
- **SÁNG KIẾN KINH NGHIỆM:** Xem tại [09_viet_sang_kien.md](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/app_trolythien/troly/prompts/09_viet_sang_kien.md).

---

## 5. Thể thức văn bản chuẩn bắt buộc
1. **Thể thức:** Tuân thủ 100% Nghị định 30/2020/NĐ-CP về Quốc hiệu, Tiêu ngữ, Tên cơ quan, Số hiệu, Địa danh ngày tháng, Trích yếu, Nội dung, Chữ ký và Nơi nhận.
2. **Nguyên tắc hành chính hiện hành (Mô hình chính quyền 2 cấp):**
   - 🔴 **TUYỆT ĐỐI KHÔNG** dùng các cơ quan cấp huyện bãi bỏ: không dùng "Phòng Giáo dục và Đào tạo", "UBND huyện", "HĐND huyện", "Huyện ủy", "Công đoàn cơ sở", "Liên đoàn Lao động" trong các văn bản ban hành mới.
   - Cơ quan ban hành hiện hành: Trường THCS Trần Phú, UBND Xã/Phường.
3. **Phông chữ & Định dạng:** Times New Roman 13pt, dãn dòng 1.2, lề trang 20-20-30-15. Toàn bộ bảng biểu đóng khung kín 4 cạnh viền ngoài và các đường kẻ trong (single 0.5pt, đen, có `cantSplit`, `tblHeader`).

---

## 6. Công cụ trực tuyến hỗ trợ & Kết quả
- **Gemini Canvas Tạo báo cáo:** [https://gemini.google.com/app/7bc03567b9f738fb?hl=vi](https://gemini.google.com/app/7bc03567b9f738fb?hl=vi)
- **Công cụ web nội bộ:** [backupcode viettailieu/taobaocao.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/backupcode%20viettailieu/taobaocao.html)
- **Kết quả xuất ra:** Tự động lưu file Word `.docx` tại [TROLYTHIEN/8_TAO_BAO_CAO/Ket_qua/](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/8_TAO_BAO_CAO/Ket_qua/)
