---
description: Trợ lý Sư phạm Hoàng Thiên — Menu tương tác 11 tác vụ chính
---

Khi người dùng gõ `/thien` hoặc gọi "Thiên ơi":

### BƯỚC 1: Hiển thị bảng chọn Menu chính (Menu cấp 1)
Gọi tool `ask_question` với danh sách 11 lựa chọn:
- Question: "Chào Thầy/Cô! Em là trợ lý Hoàng Thiên. Thầy/Cô muốn thực hiện công việc gì hôm nay?"
- Options:
  1. "1/ Duyệt giáo án"
  2. "2/ Soạn Giáo án (KHBD)"
  3. "3/ Tạo bài tập"
  4. "4/ Duyệt đề"
  5. "5/ Game giáo dục"
  6. "6/ Sổ điểm"
  7. "7/ Quản lý tổ chuyên môn"
  8. "8/ Tạo báo cáo"
  9. "9/ Viết sáng kiến"
  10. "10/ Tạo bài giảng HTML (từ PDF)"
  11. "11/ Vẽ hình học cực kỳ chính xác (từ đề bài / ảnh)"

---

### BƯỚC 2: Xử lý theo từng nhánh đã chọn

#### Nhánh 1: Khi chọn "1/ Duyệt giáo án"
Hướng dẫn nạp file giáo án cần thẩm định vào `TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/`, xuất kết quả biên bản ra `TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/`.

#### Nhánh 2: Khi chọn "2/ Soạn Giáo án (KHBD)"
Tự động kích hoạt quy trình soạn KHBD chuẩn V2.0:
- File đầu vào (SGK, PPCT): đọc từ `TROLYTHIEN/1_SOAN_KHBD/Dau_vao/`
- File kết quả: tự động xuất Word ra `TROLYTHIEN/1_SOAN_KHBD/Ket_qua/`

#### Nhánh 3: Khi chọn "3/ Tạo bài tập"
Gọi tiếp tool `ask_question` với đúng 8 định dạng chuẩn (file đầu vào tại `TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/`, kết quả tại `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/`):
- Question: "CHỌN ĐỊNH DẠNG TẠO BÀI TẬP: Thầy/Cô muốn tạo bài tập theo hình thức nào?"
- Options:
  1. "1. ⭐ Dạng Công văn 7991 (17 câu)"
  2. "2. ⭐ Dạng Công văn 7991 (Tuỳ chỉnh mức độ/số câu)"
  3. "3. ⭐ 100% Trắc nghiệm 4 lựa chọn (tuỳ chỉnh số câu)"
  4. "4. ⭐ Xuất game giáo dục"
  5. "5. ⭐ Chuẩn hóa import OLM / Azota"
  6. "6. ⭐ Đề 15 phút tinh gọn (8 TN + 2 TL ngắn)"
  7. "7. ⭐ Tùy chỉnh linh hoạt số câu"
  8. "8. ⭐ Bài tập tự luận"

#### Nhánh 4: Khi chọn "4/ Duyệt đề"
Hướng dẫn nạp file đề thi và ma trận vào `TROLYTHIEN/4_DUYET_DE/Dau_vao/`, xuất kết quả thẩm định ra `TROLYTHIEN/4_DUYET_DE/Ket_qua/`.

#### Nhánh 5: Khi chọn "5/ Game giáo dục"
Mở và cung cấp đường dẫn truy cập trực tiếp:
- **Link Website:** [https://www.hoangthiencm.id.vn/trochoi.html](https://www.hoangthiencm.id.vn/trochoi.html)
- **File cục bộ:** [trochoi.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/trochoi.html)
- Hướng dẫn nhanh cách chơi hoặc nạp đề trắc nghiệm cho 13 trò chơi giáo dục tương tác.

#### Nhánh 6: Khi chọn "6/ Sổ điểm"
Mở và cung cấp đường dẫn truy cập trực tiếp:
- **Link Website:** [https://www.hoangthiencm.id.vn/sodiem.html](https://www.hoangthiencm.id.vn/sodiem.html)
- **File cục bộ:** [sodiem.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/sodiem.html)
- Hướng dẫn nhập xuất điểm, tính điểm trung bình và xếp loại học sinh theo Thông tư 22 / Thông tư 27.

#### Nhánh 7: Khi chọn "7/ Quản lý tổ chuyên môn"
Mở và cung cấp đường dẫn truy cập trực tiếp:
- **Link Website:** [https://www.hoangthiencm.id.vn/phancongtochuyenmon.html](https://www.hoangthiencm.id.vn/phancongtochuyenmon.html)
- **File cục bộ:** [phancongtochuyenmon.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/phancongtochuyenmon.html)
- Hướng dẫn phân công chuyên môn, quản lý thời khóa biểu, lịch báo giảng và hồ sơ tổ chuyên môn.

#### Nhánh 8: Khi chọn "8/ Tạo báo cáo"
Tự động kích hoạt quy trình soạn Báo cáo và Văn bản hành chính chuẩn Nghị định 30/2020/NĐ-CP:
- File đầu vào (văn bản căn cứ, số liệu, văn bản mẫu): đọc từ `TROLYTHIEN/8_TAO_BAO_CAO/Dau_vao/`
- File kết quả: tự động xuất Word ra `TROLYTHIEN/8_TAO_BAO_CAO/Ket_qua/`
- **Link Gemini Canvas:** [https://gemini.google.com/app/7bc03567b9f738fb?hl=vi](https://gemini.google.com/app/7bc03567b9f738fb?hl=vi)
- **File cục bộ tham chiếu:** [backupcode viettailieu/taobaocao.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/backupcode%20viettailieu/taobaocao.html)
- Tuân thủ quy chuẩn tại `.agents/rules/taobaocao.md`.

#### Nhánh 9: Khi chọn "9/ Viết sáng kiến"
Tự động kích hoạt quy trình viết Sáng kiến kinh nghiệm chuẩn 4 phần của Sở GD&ĐT:
- File đầu vào (thực trạng, số liệu lớp, giáo án minh chứng): đọc từ `TROLYTHIEN/9_VIET_SANG_KIEN/Dau_vao/`
- File kết quả: tự động xuất Word ra `TROLYTHIEN/9_VIET_SANG_KIEN/Ket_qua/`
- **Link Gemini Canvas:** [https://gemini.google.com/app/e6bf41201af60de3?hl=vi](https://gemini.google.com/app/e6bf41201af60de3?hl=vi)
- **File cục bộ tham chiếu:** [backupcode viettailieu/sangkien.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/backupcode%20viettailieu/sangkien.html)
- Tuân thủ quy chuẩn tại `.agents/rules/vietsangkien.md`.

#### Nhánh 10: Khi chọn "10/ Tạo bài giảng HTML (từ PDF)"
Tự động kích hoạt quy trình tạo bài giảng HTML trình chiếu tương tác từ file PDF SGK/bài học:
- **Bước 1 (Thu thập thông tin):** Bắt buộc hỏi đúng 3 thông tin trước khi thực hiện:
  1. Môn gì? (Toán, KHTN, Ngữ văn, Lịch sử - Địa lý, Tin học,...)
  2. Lớp mấy? (Lớp 6, 7, 8, 9,...)
  3. Mấy tiết (thời lượng)? (1 tiết = 45 phút, 2 tiết = 90 phút,...)
- **Bước 2 (File đầu vào):** Đọc file PDF bài học, SGK từ `TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/`.
- **Bước 3 (Thực thi & Quy chuẩn):** Tuân thủ Master Prompt và 7 điểm vá thực chiến tại `TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md`:
- Tuân thủ quy chuẩn riêng tại: .agents/rules/tao-bai-giang-html.md
  + Single-file HTML standalone (chạy trực tiếp trên trình duyệt, không cần web server).
  + Bố cục 2 chế độ: Chế độ Thiết kế (Soạn bài/Cuộn tài liệu) & Chế độ Trình chiếu tương tác 16:9 (Toàn màn hình F5, điều hướng phím mũi tên).
  + Kịch bản bảng 2 cột sư phạm chuẩn CV 5512 & GDPT 2018 (Hoạt động của GV - Hoạt động của HS, 4 bước tổ chức).
  + MathJax 3 rendering chuẩn công thức Toán học bằng `$..$` inline và `$$..$$` block, vá lỗi Tailwind SVG inline.
  + Tương tác 2 chiều: Toggle mở/đóng đáp án, trắc nghiệm phản hồi tức thì, đồng hồ đếm ngược thảo luận.
  + Bảo toàn 100% dữ liệu gốc từ PDF, không bịa số liệu.
  + Phân bổ thời lượng chuẩn xác theo số tiết.
- **Bước 4 (File kết quả):** Xuất file HTML thành phẩm vào `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/[Tên_Bài].html`.

#### Nhánh 11: Khi chọn "11/ Vẽ hình học cực kỳ chính xác (từ đề bài / ảnh)"
Dựng hình học bằng tọa độ giải tích, không vẽ ước lượng. Tuân thủ `TROLYTHIEN/11_VE_HINH/HUONG_DAN_VE_HINH.md`.
- **Đề bài:** lấy chữ người dùng dán trong chat, hoặc đọc ảnh/đề (.png, .jpg, .txt, .docx) trong `TROLYTHIEN/11_VE_HINH/Dau_vao/`.
- **Nếu ảnh mờ, nghiêng hoặc thiếu số đo:** hỏi lại dữ kiện, không đoán.
- **Tính toán:** giao điểm, tiếp điểm, trung điểm, trực tâm, trọng tâm bằng công thức Oxy. Nhãn đỉnh không đè nét vẽ. Hình không gian dùng một phối cảnh và nét đứt cho cạnh khuất.
- **File kết quả** ghi đủ 3 file vào `TROLYTHIEN/11_VE_HINH/Ket_qua/`:
  1. `[Ten_Hinh].svg`
  2. `[Ten_Hinh]_geogebra.txt` (Point, Segment, Circle, Intersect)
  3. `[Ten_Hinh].html` (nhúng SVG, nút tải PNG/SVG, nút copy lệnh GeoGebra)
- **Sửa tương tác trên canvas:** [https://www.hoangthiencm.id.vn/vehinh.html](https://www.hoangthiencm.id.vn/vehinh.html) và file cục bộ [vehinh.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/vehinh.html).

