# HƯỚNG DẪN TỰ ĐỘNG CẮT PDF SÁCH GIÁO KHOA THEO BÀI HỌC (CHUẨN XÁC 100%)
**Trợ lý Sư phạm Hoàng Thiên • Nhánh 3: Tạo bài tập • Chức năng 10**

---

## 🎯 Mục đích & Cam kết
Giúp Thầy/Cô đưa nguyên cuốn Sách giáo khoa (SGK) hoặc Sách bài tập (SBT) PDF (từ 50 - 250 trang) vào hệ thống và **tự động cắt thành từng file bài học riêng biệt chuẩn xác 100%**, không cần Thầy/Cô phải mất thời gian ngồi dò xem lại từng trang.

---

## 🛡️ Cơ chế đảm bảo CHÍNH XÁC TUYỆT ĐỐI (Không cắt nhầm trang)
Hệ thống giải quyết triệt để các vấn đề cố hữu của các công cụ cắt PDF thông thường:
1. **Triệt tiêu độ lệch số trang (Page Offset):** Tự động đọc Mục lục và đối chiếu số trang in dưới chân trang với chỉ số trang vật lý của file PDF (bỏ qua bìa, lời nói đầu, hướng dẫn sử dụng sách).
2. **Bắt trọn vẹn ranh giới bài học & Độc lập hóa 100% "Luyện tập chung":**
   - **Bài lý thuyết (`Bài 1...`, `Bài 2...`):** Trang bắt đầu là trang xuất hiện tiêu đề bài; trang kết thúc là trang ngay trước khi xuất hiện bài tiếp theo hoặc ngay trước khi xuất hiện bài *Luyện tập chung* / *Bài tập cuối chương*. **TUYỆT ĐỐI KHÔNG gộp phần Luyện tập chung vào bài lý thuyết trước đó!**
   - **Bài "Luyện tập chung" (BẮT BUỘC CẮT FILE RIÊNG):** Trong chương trình GDPT 2018 và phân phối chương trình (PPCT), *Luyện tập chung* là một bài học độc lập (thường từ 1 - 2 tiết). Bắt buộc phải được cắt thành file PDF riêng biệt với quy tắc đặt tên: `[Mon][Lop]_Chuong_[X]_Luyen_tap_chung_Trang_[A-B].pdf`.
   - **Bài "Bài tập cuối chương" & "Hoạt động thực hành trải nghiệm":** Tương tự, bắt buộc phải xuất thành từng file PDF riêng biệt, không được bỏ sót hay nuốt vào bài khác.
   - **Xử lý bài học ngắn chỉ có 1 trang:** Đối với các bài *Luyện tập chung* hoặc *Bài tập cuối chương* chỉ chiếm đúng 1 trang in duy nhất, hệ thống xác định `start_page == end_page` (tổng số trang là 1), trích xuất trọn vẹn trang đó, tuyệt đối không được bỏ qua.
3. **Nhận diện đầy đủ 4 nhóm đề mục bài học:**
   - Nhóm 1: `Bài \d+` (Bài 1, Bài 2, Bài 3...)
   - Nhóm 2: `Luyện tập chung` / `Luyện tập`
   - Nhóm 3: `Bài tập cuối chương` / `Ôn tập chương`
   - Nhóm 4: `Hoạt động thực hành trải nghiệm`
4. **Bảo toàn 100% chất lượng gốc:** Sử dụng PyMuPDF trích xuất trực tiếp các trang PDF gốc, không qua nén giảm chất lượng ảnh, không làm vỡ nét công thức hay hình vẽ.

---

## 📁 Cách sử dụng cực kỳ đơn giản:

### Bước 1: Nạp file SGK
- Đặt file PDF cuốn SGK/SBT vào thư mục:  
  👉 `TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/`  
  *(Ví dụ: `SGK_Toan_6_Tap_1_KNTT.pdf` hoặc `SBT_Toan_8_Tap_2_CanhDieu.pdf`)*

### Bước 2: Kích hoạt Trợ lý Thiên
- Gõ `/thien` $\rightarrow$ Chọn **"3/ Tạo bài tập"** $\rightarrow$ Chọn mục **"10. ✂️ Tự động cắt PDF SGK thành từng bài học (Chuẩn xác 100% từng bài)"**.
- *Hoặc chat trực tiếp:* *"Thiên ơi, cắt cuốn SGK trong thư mục Dau_vao thành từng bài cho tôi"*.

### Bước 3: Nhận kết quả
File PDF từng bài học sẽ được tự động xuất ra ngay ngắn và sạch sẽ tại:
👉 `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/PDF_Tung_Bai/`  
Thầy/Cô có thể sử dụng trực tiếp các file bài lẻ này để lưu trữ hoặc nạp vào tạo đề thi, bài tập khi cần.
