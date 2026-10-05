---
description: Trợ lý Sư phạm Hoàng Thiên — Menu tương tác 13 tác vụ chính
---

Khi người dùng gõ `/thien` hoặc gọi "Thiên ơi":

### BƯỚC 1: Hiển thị bảng chọn Menu chính (Menu cấp 1)
Gọi tool `ask_question` với danh sách 13 lựa chọn:
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
  12. "12/ Chuẩn hoá văn bản (Hành chính / Đảng)"
  13. "13/ Chuyển ghi âm thành văn bản (iPhone / MP3)"

---

### BƯỚC 2: Xử lý theo từng nhánh đã chọn

#### Nhánh 1: Khi chọn "1/ Duyệt giáo án"
Tự động kích hoạt quy trình thẩm định Kế hoạch bài dạy theo chuẩn CV 5512 & Quy định chuyên môn nghiêm ngặt trường THCS Trần Phú:
- **File đầu vào:** Đọc các tệp tham chiếu `Phu-luc-3-...docx` tại thư mục gốc `TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/` và thư mục riêng từng giáo viên (ví dụ `HỒ ĐĂNG DANH/`, `TRAN SANG/`...).
- **Quy chuẩn thẩm định nghiêm ngặt:**
  + Thể thức: Times New Roman 13pt (in đứng), A4, lề trên 1.5cm, dưới 1.5cm, trái 2.0cm, phải 1.5cm, dãn dòng 0/3/Single, Header & Footer đúng mẫu THCS Trần Phú.
  + Tiến độ: Khớp 100% phân môn và số tiết theo Phụ lục 3 (thiếu tiết không lý do chính đáng -> Trả hồ sơ).
  + Tích hợp NLS/AI/STEM: Khớp 1-1 mã và mô tả với Phụ lục 3; **bắt buộc phải in đậm, nghiêng** (chưa in đậm nghiêng -> Trả hồ sơ).
  + Toán học & Ký hiệu (LỖI ĐỎ): Sai kiến thức hoặc **LỖI FONT CÔNG THỨC / BIẾN DẠNG KÝ HIỆU GÓC** (dấu chấm trên đầu đỉnh ẋOz, ký tự vuông/perpendicular đè lên chữ D┴, A┴...) $\rightarrow$ **BẮT BUỘC TRẢ HỒ SƠ 100%! TUYỆT ĐỐI CẤM DUYỆT!**
- **Đầu ra 3 nhóm tệp độc lập tại `TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/`:**
  1. `Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_[X].docx` & `.md`: Biên bản hành chính trang trọng toàn tổ (cuốn chiếu append từng GV, không chèn mẫu copy-paste hệ thống).
  2. `Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_[X].docx` & `.md`: Tệp chuyên dụng để Tổ trưởng Copy & Paste vào phần mềm duyệt giáo án (vnEdu, SMAS, K12).
  3. `Phieu_Nhan_Xet_Ho_So_[TenGV]_Thang_[X].docx`: Phiếu gửi riêng từng giáo viên (khung xanh cho Duyệt, khung đỏ cho Trả hồ sơ).
- Tuân thủ quy chuẩn riêng tại `.agents/rules/duyet-giao-an.md` và Master Prompt tại `TROLYTHIEN/3_DUYET_GIAO_AN/PROMPT_DUYET_GIAO_AN.md`.

#### Nhánh 2: Khi chọn "2/ Soạn Giáo án (KHBD)"
Tự động kích hoạt quy trình soạn KHBD chuẩn V2.0:
- File đầu vào (SGK, PPCT): đọc từ `TROLYTHIEN/1_SOAN_KHBD/Dau_vao/`
- File kết quả: tự động xuất Word ra `TROLYTHIEN/1_SOAN_KHBD/Ket_qua/`
- **Tích hợp NLS và AI:** Trong các hoạt động dạy học có năng lực số, năng lực AI thì **bắt buộc phải in đậm, in nghiêng phần tích hợp** (khớp chuẩn duyệt giáo án).

#### Nhánh 3: Khi chọn "3/ Tạo bài tập"
Gọi tiếp tool `ask_question` với đúng 10 định dạng chuẩn (file đầu vào tại `TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/`, kết quả tại `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/`):
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
  9. "9. ⭐ Xuất bài dạy HTML (Dạy thêm, phụ đạo, bồi dưỡng - Phân dạng & Giải từng bước)"
  10. "10. ✂️ Tự động cắt PDF SGK thành từng bài học (Chuẩn xác 100% từng bài)"

*Khi chọn lựa chọn 9:* Tự động kích hoạt quy trình tạo bài dạy HTML phân dạng chuyên biệt cho dạy thêm, dạy kèm, phụ đạo và bồi dưỡng (tuân thủ `.agents/rules/tao-bai-day-html.md`).
*Khi chọn lựa chọn 10:* Tự động kích hoạt quy trình cắt PDF SGK thành từng bài học chuẩn xác 100% (tuân thủ `.agents/rules/tro-ly-thien.md`).


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
- **File kết quả** đặt tên theo Tên bài tập (ví dụ `Bai_1_Hinh_Binh_Hanh_ABCD`), ghi đủ 4 file vào `TROLYTHIEN/11_VE_HINH/Ket_qua/`:
  1. `Bai_X_[Ten_Hinh].png` (ảnh nét cao chèn trực tiếp Word/PowerPoint)
  2. `Bai_X_[Ten_Hinh].svg`
  3. `Bai_X_[Ten_Hinh]_geogebra.txt` (Point, Segment, Circle, Intersect)
  4. `Bai_X_[Ten_Hinh].html` (nhúng SVG, nút tải PNG/SVG, nút copy lệnh GeoGebra)
- **Sửa tương tác trên canvas:** [https://www.hoangthiencm.id.vn/vehinh.html](https://www.hoangthiencm.id.vn/vehinh.html) và file cục bộ [vehinh.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/vehinh.html).
- **Dọn dẹp file rác:** Khi người dùng yêu cầu dọn rác/làm sạch cache, kích hoạt `python tools/don_dep_file_rac.py` (hoặc chạy `tools/Don_Dep_File_Rac.bat`).

#### Nhánh 12: Khi chọn "12/ Chuẩn hoá văn bản (Hành chính / Đảng)"
Chuẩn hoá tệp Word đã có, không soạn văn bản mới. Đọc `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/HUONG_DAN_CHUAN_HOA_VAN_BAN.md` và áp dụng nguyên văn Master Prompt tại `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/PROMPT_CHUAN_HOA_VAN_BAN.md`.
- **File đầu vào:** đọc trực tiếp tệp Word `.docx` trong `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/Dau_vao/`. Trích toàn bộ đoạn văn và bảng biểu, giữ nguyên số liệu.
- **Thẩm định:** phân loại Hành chính (Nghị định 30/2020/NĐ-CP) hoặc Đảng (Quy định 399-QĐ/TW và Hướng dẫn 05-HD/VPTW) ngay ở bước nhận diện. Kiểm tra chính tả, dấu câu, căn cứ, thẩm quyền. Cảnh báo nếu văn bản còn tên cơ quan cấp huyện đã bãi bỏ trong mô hình chính quyền 2 cấp.
- **Chat:** không xuất báo cáo 5 phần. Chỉ 2–3 dòng: đã chuẩn hoá xong, đường dẫn tệp Word, ghi chú pháp lý trọng yếu nếu có.
- **File kết quả:** xuất Word `.docx` vào `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/Ket_qua/[Ten_File]_Chuan_Hoa.docx`. Kỹ thuật in: Times New Roman 13pt, thụt đầu dòng 1,27 cm, lề A4, bảng đóng khung 4 cạnh, `cantSplit`, `tblHeader`. Header cột trái 65 mm, cột phải 100 mm, lề ô 0. Quốc hiệu và tên cơ quan mỗi cụm một dòng. Đường kẻ `v:line` 0.75pt dưới tiêu ngữ, tên đơn vị và trích yếu. Bảng số liệu 11,5pt.

#### Nhánh 13: Khi chọn "13/ Chuyển ghi âm thành văn bản (iPhone / MP3)"
Bóc tách tệp ghi âm giọng nói thành văn bản trung thực (Verbatim transcript), độ chính xác 90–95%, không tự ý thay đổi câu từ hoặc uốn nắn theo thuật ngữ sách vở. Đọc `TROLYTHIEN/13_CHUYEN_GHI_AM/HUONG_DAN_CHUYEN_GHI_AM.md` và áp dụng nguyên văn Master Prompt tại `TROLYTHIEN/13_CHUYEN_GHI_AM/PROMPT_CHUYEN_GHI_AM.md`.
- **File đầu vào:** đọc trực tiếp tệp âm thanh `.m4a` (từ iPhone), `.mp3`, `.wav`, `.aac` trong `TROLYTHIEN/13_CHUYEN_GHI_AM/Dau_vao/`.
- **Nguyên tắc bóc tách:** Giữ nguyên từng từ của người phát biểu, tự động phân tích ngữ cảnh để sửa lỗi chính tả chuẩn xác (phát âm vùng miền, dấu hỏi/ngã, từ đồng âm), tự động ngắt câu, đặt dấu chấm phẩy, xuống dòng chia đoạn theo nhịp phát biểu hoặc theo từng người nói. Giữ nguyên số liệu, tên riêng.
- **File kết quả:** tự động xuất đồng thời 2 file vào `TROLYTHIEN/13_CHUYEN_GHI_AM/Ket_qua/`:
  1. `[Ten_File].docx`: tệp Word chuẩn A4, phông Times New Roman 13pt, dãn dòng 1.2, thụt đầu dòng 1.27 cm, căn đều, có tiêu đề và ngày giờ.
  2. `[Ten_File].txt`: tệp văn bản thuần UTF-8 gọn nhẹ để sao chép nhanh.
- **Chat:** phản hồi ngắn 2–3 dòng: đã bóc tách xong, đường dẫn tệp Word và Text, trích dẫn 1 câu mở đầu để nhận diện nội dung.

