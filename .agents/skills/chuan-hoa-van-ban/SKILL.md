---
name: chuan-hoa-van-ban
description: >-
  Chuẩn hóa thể thức và kỹ thuật trình bày văn bản hành chính nhà nước theo Nghị định số 30/2020/NĐ-CP
  và văn bản của Đảng theo Hướng dẫn số 05-HD/VPTW (2026). Tự động thiết lập phông chữ Times New Roman,
  cỡ chữ 13pt đồng nhất, thụt đầu dòng 1.27cm, dãn dòng 1.2, định lề A4, đóng khung kín bảng biểu 4 cạnh,
  chuẩn hóa căn cứ pháp lý, chữ ký số điện tử và quy trình sao văn bản.
---

# KỸ NĂNG CHUẨN HÓA VĂN BẢN (NGHỊ ĐỊNH 30/2020/NĐ-CP & HƯỚNG DẪN 05-HD/VPTW)

Sử dụng kỹ năng này khi người dùng yêu cầu:
- "Chuẩn hoá theo NĐ 30 CP" hoặc "chuẩn hoá văn bản hành chính".
- "Soạn thảo văn bản của Đảng" hoặc "chuẩn hóa theo Hướng dẫn 05-HD/VPTW".

---

## 1. NGUYÊN TẮC CỐT LÕI CỦA NGHỊ ĐỊNH SỐ 30/2020/NĐ-CP (HÀNH CHÍNH NHÀ NƯỚC)

1. **Phông chữ:** `Times New Roman`, bảng mã Unicode chuẩn TCVN 6909:2001.
2. **Cỡ chữ nội dung:** **ĐỒNG NHẤT 13pt** (Không để lẫn lộn các đoạn 11.5pt, 12pt, 12.5pt và 13pt làm mất cân đối).
3. **Thụt đầu dòng đoạn văn:** **BẮT BUỘC 1,27 cm (0.5 inch)** (`first_line_indent = Inches(0.5)`) cho tất cả các đoạn văn, điều, khoản, điểm và từng dòng Căn cứ ban hành.
4. **Căn lề & Dãn dòng:**
   - Căn đều hai bên (`JUSTIFY`).
   - Dãn dòng cố định **1.2 dòng** (`line_spacing = 1.2`).
   - Dãn cách đoạn: `space_before = 2pt`, `space_after = 3pt`.
5. **Định lề trang A4 chuẩn:**
   - Lề trên (Top): `20 mm` (0.79 inch)
   - Lề dưới (Bottom): `20 mm` (0.79 inch)
   - Lề trái (Left): `30 mm` (1.18 inch)
   - Lề phải (Right): `15 mm` (0.59 inch)
6. **Đóng khung bảng biểu:**
   - Đóng khung kín 4 cạnh viền ngoài và các đường chia ô bên trong (`top`, `bottom`, `left`, `right`, `insideH`, `insideV` đều là đường đơn `single`, màu đen, độ dày 0.5pt).
   - Thiết lập `cantSplit` chống xé dòng giữa 2 trang và `tblHeader` lặp lại dòng tiêu đề khi sang trang.
   - Cỡ chữ trong ô bảng: 10 – 11.5pt để không bị tràn dòng.
7. **Căn cứ ban hành:**
   - Chữ in thường, kiểu chữ **nghiêng**, cỡ chữ **13pt**, thụt đầu dòng **1,27 cm**.
   - Dòng căn cứ cuối cùng kết thúc bằng dấu phẩy (,), các dòng trước kết thúc bằng dấu chấm phẩy (;).
8. **Dàn trang:**
   - Thu nhỏ hình ảnh sơ đồ (`width = Inches(5.4)`) để ảnh nằm trọn trong trang, không đẩy sang trang mới làm thủng trang.

---

## 2. NGUYÊN TẮC CỐT LÕI CỦA HƯỚNG DẪN SỐ 05-HD/VPTW (2026) (VĂN BẢN CỦA ĐẢNG)

Ban hành ngày 27/5/2026 theo **Quy định số 399-QĐ/TW** ngày 09/01/2026 của Ban Bí thư Trung ương Đảng (thay thế Hướng dẫn 36-HD/VPTW năm 2018).

### 1. Bố cục tiêu đề văn bản Đảng:
- **Góc trên bên phải:**
  + Dòng 1: `ĐẢNG CỘNG SẢN VIỆT NAM` (chữ in hoa, cỡ **13 – 14pt**, đứng, **đậm**, căn giữa).
  + Dòng 2: `Địa danh, ngày ... tháng ... năm ...` (chữ in thường, cỡ **13 – 14pt**, kiểu chữ **nghiêng**, căn giữa).
- **Góc trên bên trái:**
  + Dòng 1: Tên Cấp ủy cấp trên trực tiếp (in hoa, cỡ 12 - 13pt, đứng).
  + Dòng 2: Tên Cơ quan ban hành (in hoa, cỡ 12 - 13pt, đứng, **đậm**, có đường kẻ ngang bên dưới).
  + Dòng 3: `Số: ...-QĐ/ĐU`, `Số: ...-BC/CB` (chữ in thường, cỡ 13pt, đứng).

### 2. Chuẩn hóa đồng bộ văn bản giấy và văn bản điện tử:
- Văn bản điện tử có chữ ký số hợp lệ có giá trị pháp lý tương đương văn bản giấy ký tay đóng dấu.
- **Chữ ký số cá nhân người ký:** Hình ảnh chữ ký màu **xanh**, định dạng `.png` nền trong suốt, hiển thị trên dòng họ tên.
- **Chữ ký số cơ quan Đảng (Con dấu điện tử):** Hình ảnh con dấu màu **đỏ**, định dạng `.png` nền trong suốt, trùm lên khoảng 1/3 hình ảnh chữ ký về phía bên trái.
- **Quy trình sao sang văn bản điện tử:** Số hóa (quét scan) văn bản giấy gốc sang định dạng PDF (độ phân giải tối thiểu 300 dpi) và áp dụng chữ ký số của cơ quan sao.

### 3. Quy tắc viết tắt tên cơ quan Đảng trên môi trường số:
- Chi bộ: `CB`
- Đảng ủy / Đảng bộ cơ sở: `ĐU` / `ĐB`
- Ban Thường vụ: `BTV`
- Ban Chấp hành: `BCH`
- Thường trực Đảng ủy: `TT.ĐU`
- Ủy ban Kiểm tra: `UBKT`
- Ban Tuyên giáo: `BTG`
- Ban Tổ chức: `BTC`
- Văn phòng: `VP`

---

## 3. CHECKLIST KIỂM TRA NHANH TRƯỚC KHI XUẤT BẢN WORD
- [ ] Phông chữ 100% `Times New Roman`.
- [ ] Không có đoạn văn nào bị lệch cỡ chữ (toàn bộ nội dung là 13pt).
- [ ] Tất cả các đoạn văn, điều, khoản và dòng Căn cứ đều có `first_line_indent = Inches(0.5)`.
- [ ] Dãn dòng 1.2, căn đều hai bên (`JUSTIFY`).
- [ ] Bảng biểu dữ liệu có đủ 4 viền ngoài và các đường trong (`set_table_borders`).
- [ ] Bảng Header (tiêu ngữ) và Chữ ký chân trang không có viền.
- [ ] Số liệu cần rà soát được đánh dấu in đậm, màu đỏ (`[RED]...[/RED]`).
