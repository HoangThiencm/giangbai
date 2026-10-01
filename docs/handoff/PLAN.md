# PLAN: ĐIỀU CHỈNH CHUẨN HOÁ THỂ THỨC NHÁNH 12 (SỬA LỖI HEADER, TIÊU ĐỀ, ĐƯỜNG KẺ VECTOR THẬT, BẢNG BIỂU VÀ LƯỢC BỎ BÁO CÁO DÀI TRONG CHAT)

## Hiện trạng
1. **Phần hiển thị Chat quá dài**:
   - Hiện tại AI xuất báo cáo 5 phần dài hàng trăm dòng trong khung chat gây mất thời gian cho người dùng. Người dùng chỉ cần tệp Word đã được chuẩn hoá chính xác trong `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/Ket_qua/` để mở ra in ấn, trình ký ngay.
2. **Lỗi nghiêm trọng phần Tiêu đề và Quốc hiệu (Hình ảnh 1)**:
   - Trong bảng Header: Cột Quốc hiệu và Cột Cơ quan ban hành bị chia tỷ lệ độ rộng không chuẩn, kèm lề ô mặc định (cell margins padding) khiến:
     + `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM` bị ngắt gãy chữ "NAM" xuống dòng thứ hai (`... VIỆT` / `NAM`). Đây là lỗi thể thức nghiêm trọng nhất trong văn bản hành chính Việt Nam (Quốc hiệu bắt buộc phải nằm trọn vẹn trên 1 dòng duy nhất).
     + `ỦY BAN NHÂN DÂN XÃ XUÂN ĐÔNG` bị ngắt gãy chữ "ĐÔNG" xuống dòng thứ hai (`... XÃ XUÂN` / `ĐÔNG`).
3. **Lỗi kỹ thuật tạo đường kẻ ngang (Line vs Underline / Text dashes)**:
   - Các đường kẻ ngang dưới Tiêu ngữ, Tên cơ quan và Trích yếu hiện tại đang dùng chuỗi ký tự gạch ngang Unicode `────` hoặc gạch chân Underline (U). Khi mở trên Microsoft Word, chúng hiển thị như văn bản bị gạch chân, đứt đoạn, khoảng cách chữ không đều và không phải là một đường kẻ đồ họa (graphic vector line) sắc nét chuẩn văn thư.
   - Dưới trích yếu KẾ HOẠCH hiện tại đang bị thiếu hoàn toàn đường kẻ ngang nét liền theo quy định tại Nghị định 30/2020/NĐ-CP (Phụ lục I, Mục II, Điểm 6b).
4. **Lỗi khoảng cách dãn đoạn**:
   - Khoảng cách giữa Trích yếu và Căn cứ đầu tiên bị hở toang hoác do chèn paragraph rỗng `p_sp2` không đúng quy chuẩn kỹ thuật văn bản.
5. **Vấn đề cỡ chữ trong bảng biểu (11pt vs 13pt)**:
   - Theo Nghị định 30/2020/NĐ-CP: Lời văn 13 - 14pt; bảng biểu được phép dùng từ 10 - 12pt tùy độ rộng cột. Với bảng lộ trình 4 cột của Trường THCS Trần Phú, cỡ 11pt hơi nhỏ, cần nâng lên 11.5 - 12pt để rõ nét, dễ đọc và cân đối thị giác.

## Phạm vi
1. **Tinh gọn phản hồi Chat**:
   - Bỏ toàn bộ việc xuất báo cáo 5 phần dài dòng trong khung chat.
   - Khi chạy Nhánh 12, AI chỉ thông báo ngắn gọn 2-3 dòng: Xác nhận đã chuẩn hóa xong tệp Word, cung cấp link mở tệp tại `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/Ket_qua/[Ten_File]_Chuan_Hoa.docx`, kèm ghi chú những điểm pháp lý trọng yếu cần rà soát (nếu có).
2. **Sửa dứt điểm lỗi bố cục Header (Quốc hiệu & Tên cơ quan)**:
   - Căn chỉnh lại độ rộng cột bảng Header 2 cột: Cột phải (Quốc hiệu - Tiêu ngữ) mở rộng lên 100mm, cột trái (Tên cơ quan) 65mm.
   - Đặt toàn bộ lề ô (cell padding/margins) của bảng Header về 0 (`top=0, bottom=0, left=0, right=0`) để tận dụng tối đa chiều ngang trang in.
   - Cỡ chữ: Quốc hiệu in hoa đứng đậm 12pt; Tiêu ngữ in thường đứng đậm 12.5 - 13pt; Tên cơ quan cấp trên in hoa đứng 11.5 - 12pt; Tên đơn vị in hoa đứng đậm 12pt. Bảo đảm `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM` và `ỦY BAN NHÂN DÂN XÃ XUÂN ĐÔNG` nằm trọn vẹn 100% trên 1 dòng duy nhất.
3. **Thay thế toàn bộ chuỗi ký tự gạch chân bằng đường kẻ Vector Line chuẩn xác**:
   - Tuyệt đối không dùng ký tự `────` hay định dạng Underline (U) của đoạn văn.
   - Áp dụng kỹ thuật vẽ đường kẻ ngang chuẩn Microsoft Word (VML line `v:line` hoặc drawing vector line có độ dày chuẩn 0.75pt - 1pt, màu đen `#000000`, căn giữa):
     + Dưới Tiêu ngữ: Đường kẻ có độ dài bằng chính xác độ dài dòng chữ Tiêu ngữ (~35 - 40mm).
     + Dưới Tên đơn vị: Đường kẻ có độ dài bằng 1/3 đến 1/2 độ dài dòng chữ (~25 - 30mm).
     + Dưới Trích yếu Kế hoạch: Bổ sung đường kẻ có độ dài bằng 1/3 đến 1/2 độ dài dòng chữ trích yếu (~40 - 50mm).
4. **Chuẩn hóa khoảng cách dãn đoạn**:
   - Xóa bỏ hoàn toàn paragraph rỗng `p_sp2`.
   - Thiết lập dãn cách chuẩn `space_before = 4pt`, `space_after = 6pt` cho dòng trích yếu và đường kẻ, tạo sự liền mạch, trang trọng với phần Căn cứ.
5. **Chuẩn hóa Căn cứ và Thân văn bản**:
   - Các dòng Căn cứ: Times New Roman 13pt, nghiêng, thụt đầu dòng 1,27 cm (Inches(0.5)), dòng cuối kết thúc bằng dấu phẩy (,), các dòng trước kết thúc bằng dấu chấm phẩy (;).
   - Đoạn văn thân bài: Đồng nhất 13pt, thụt đầu dòng 1,27 cm, căn đều hai bên (`JUSTIFY`), dãn dòng 1.2 lines, dãn đoạn `space_before = 2pt`, `space_after = 3pt`.
6. **Chuẩn hóa Bảng biểu Lộ trình (Mục IV)**:
   - Đóng khung kín 4 cạnh viền ngoài và các đường chia ô (0.5pt black).
   - Khóa thuộc tính `cantSplit` cho 100% các hàng (chống xé đôi dòng sang 2 trang) và `tblHeader` cho dòng tiêu đề.
   - Nâng cỡ chữ trong bảng lên 11.5pt (Times New Roman), căn giữa cột Giai đoạn và Thời gian, căn đều/trái cột Nội dung và Sản phẩm.
7. **Chuẩn hóa Nơi nhận & Chữ ký (Footer)**:
   - Bảng 2 cột không viền: Cột trái chứa Nơi nhận (tiêu đề 12pt nghiêng đậm, các mục 11pt đứng); Cột phải chứa chức danh HIỆU TRƯỞNG (13pt hoa đậm), khoảng trống ký 40-45pt, họ tên Bùi Ngọc Nam (13pt hoa/thường đậm).

## Ngoài phạm vi
- Không thay đổi nội dung chuyên môn và các số liệu giáo dục gốc của văn bản.
- Không sửa mã nguồn của các nhánh 1 đến 11.

## File dự kiến tác động
1. `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/PROMPT_CHUAN_HOA_VAN_BAN.md` (cập nhật quy chuẩn kỹ thuật header 1 dòng, đường kẻ vector line chuẩn thay vì underline/text dash, đường kẻ trích yếu, lược bỏ báo cáo chat dài).
2. `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/HUONG_DAN_CHUAN_HOA_VAN_BAN.md` (cập nhật hướng dẫn người dùng tập trung nhận file docx).
3. `.agents/workflows/thien.md` (cập nhật kịch bản Nhánh 12: xuất file docx, phản hồi ngắn gọn).
4. `.agents/rules/tro-ly-thien.md` (cập nhật quy chuẩn Nhánh 12).
5. `tools/standardize_kh_dayhoc.py` (tái sinh tệp Word `.docx` với các thông số chuẩn xác 100%: header 1 dòng, đường kẻ vector thực thụ, đường kẻ trích yếu, nâng cỡ chữ bảng).
6. `TROLYTHIEN/12_CHUAN_HOA_VAN_BAN/Ket_qua/KH_TO_CHUC_DAY_HOC_TRUC_TUYEN_2026_2027_TRANPHU_Chuan_Hoa.docx` (file kết quả Word đã sửa hoàn hảo).
7. `tests/trolythien-chuan-hoa-van-ban-smoke.js` (cập nhật test khớp với quy chuẩn mới).

## Các bước thực hiện
1. **Bước 1: Cập nhật thuật toán tạo Word trong `tools/standardize_kh_dayhoc.py`**
   - Thiết lập bảng Header: Cột phải 100mm, cột trái 65mm, cell margins padding = 0 dxa. Cỡ chữ Quốc hiệu 12pt đứng đậm, đảm bảo `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM` và `ỦY BAN NHÂN DÂN XÃ XUÂN ĐÔNG` tuyệt đối không bị xuống dòng.
   - Thay thế toàn bộ ký tự `────` bằng đường kẻ vector đồ họa thực thụ (`v:line` hoặc drawing shape line chuẩn OpenXML) dày 0.75pt, nét liền, màu đen, căn giữa.
   - Thêm đường kẻ ngang vector dưới trích yếu Kế hoạch (độ dài 1/3 - 1/2 trích yếu, ~45mm).
   - Xóa bỏ đoạn văn trống `p_sp2`, căn chỉnh khoảng cách giữa trích yếu và căn cứ chuẩn xác (`space_after = Pt(6)`).
   - Nâng cỡ chữ bảng lên 11.5pt, căn chỉnh đệm ô thoáng đẹp.
   - Xuất lại file Word `.docx` hoàn hảo vào `Ket_qua/`.
2. **Bước 2: Cập nhật Master Prompt `PROMPT_CHUAN_HOA_VAN_BAN.md`**
   - Bổ sung quy tắc bắt buộc: Quốc hiệu và Tên cơ quan cấp trên không bao giờ được bẻ gãy từ sang dòng thứ hai (phải căn chỉnh độ rộng cột và cỡ chữ 12pt).
   - Bổ sung quy tắc bắt buộc: Các đường kẻ ngang phải là đối tượng đồ họa (graphic vector line), cấm dùng Underline hay chuỗi ký tự gạch nối Unicode.
   - Bổ sung quy tắc: Dưới trích yếu nội dung văn bản có tên loại (Kế hoạch, Báo cáo, Quyết định, Tờ trình) bắt buộc có đường kẻ ngang 1/3 đến 1/2 nét liền.
   - Lược bỏ yêu cầu chat trả 5 phần dài dòng; quy định chat chỉ trả thông báo ngắn gọn 2-3 dòng kèm link tệp `.docx` và các lưu ý pháp lý quan trọng nhất.
3. **Bước 3: Cập nhật `HUONG_DAN_CHUAN_HOA_VAN_BAN.md`, `thien.md` và `tro-ly-thien.md`**
   - Đồng bộ quy trình xử lý tinh gọn: Nhận file Word $\rightarrow$ Chuẩn hoá thể thức $\rightarrow$ Xuất file Word tại `Ket_qua/` $\rightarrow$ Báo link hoàn thành trong chat.
4. **Bước 4: Cập nhật và chạy Smoke test**
   - Cập nhật assertions trong `tests/trolythien-chuan-hoa-van-ban-smoke.js`.
   - Chạy test đảm bảo PASS 100%.

## Rủi ro
- Độ rộng cột bảng Header nếu chỉnh quá tay có thể làm lệch số hiệu văn bản bên trái.
  *Giải pháp:* Phân bổ chính xác tỷ lệ 65mm : 100mm trên tổng khổ in 165mm của trang A4 lề 30-15mm, xóa padding ô, đảm bảo vừa vặn tuyệt đối.

## Cách kiểm thử
1. Chạy `python tools/standardize_kh_dayhoc.py` và kiểm tra cấu trúc XML / Word docx của file tạo ra (không có paragraph nào bị wrap sai, kiểm tra độ dài các run).
2. Chạy `node tests/trolythien-chuan-hoa-van-ban-smoke.js`.
3. Chạy `node tests/trolythien-bai-giang-html-smoke.js`.
4. Chạy `node tests/trolythien-vehinh-smoke.js`.

## Tiêu chí nghiệm thu
1. Trong file Word `KH_TO_CHUC_DAY_HOC_TRUC_TUYEN_2026_2027_TRANPHU_Chuan_Hoa.docx`:
   - Quốc hiệu `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM` nằm trọn vẹn trên 1 dòng duy nhất.
   - Tên cơ quan `ỦY BAN NHÂN DÂN XÃ XUÂN ĐÔNG` nằm trọn vẹn trên 1 dòng duy nhất.
   - Các đường kẻ ngang là đường vẽ vector line thực thụ (không phải ký tự text hay gạch chân Underline), nét thanh mảnh sắc nét (0.75pt).
   - Có đường kẻ ngang nét liền dưới trích yếu Kế hoạch (độ dài 1/3 đến 1/2 dòng chữ).
   - Khoảng cách từ trích yếu đến dòng Căn cứ đầu tiên chuẩn mực, không bị hở toang hoác.
   - Cỡ chữ trong bảng lộ trình đạt 11.5pt, rõ nét, dễ đọc, đóng khung 4 cạnh kín, chống xé dòng.
2. Quy trình Trợ lý Thiên không còn tuôn báo cáo dài dòng trong chat; chỉ trả lời ngắn gọn kèm đường dẫn tệp Word.
3. Tất cả các smoke test đều PASS.
