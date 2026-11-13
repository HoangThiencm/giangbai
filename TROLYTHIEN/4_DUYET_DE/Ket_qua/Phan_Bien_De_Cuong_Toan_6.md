# BÁO CÁO THẨM ĐỊNH VÀ PHẢN BIỆN CHUYÊN MÔN
## ĐỀ CƯƠNG ÔN TẬP KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KỲ I — MÔN TOÁN 6
### NĂM HỌC 2026 - 2027

---

**Đơn vị:** TRƯỜNG THCS TRẦN PHÚ — TỔ TOÁN - TIN  
**Thời gian thực hiện:** Ngày 15 tháng 10 năm 2026  
**Đối tượng thẩm định:** Tệp tài liệu `Đề_cương_Toán_6_ 2026-2027.pdf` (03 trang, do cô Nguyễn Thị Thảo biên soạn)  
**Người thẩm định:** Trợ lý Sư phạm Hoàng Thiên (Tổ trưởng chuyên môn)  

---

### I. THÔNG TIN HỒ SƠ THẨM ĐỊNH

- **Tên hồ sơ:** Đề cương ôn tập kiểm tra giữa học kỳ I môn Toán 6 (Năm học 2026 – 2027).
- **Phạm vi kiến thức:** Tuần 1 đến tuần 8 theo Chương trình GDPT 2018 (Số và Đại số; Hình học trực quan).
- **Cấu trúc tài liệu gốc:** Gồm 9 bài tập Phần A (Số học) và 6 bài tập Phần B (Hình học).

---

### II. PHÂN TÍCH CHI TIẾT CÁC ĐIỂM NÓNG CHUYÊN MÔN & SƯ PHẠM

#### 1. Bài 8 Số học — LỖI SAI TOÁN HỌC TRẦM TRỌNG (BÀI TOÁN BỊ VÔ NGHIỆM)
- **Đề bài gốc:**
  > *"Một thư viện nhận về một lượng sách tham khảo mới trong khoảng từ 400 đến 550 cuốn. Khi xếp số sách này thành từng bó 15 cuốn, 20 cuốn hoặc 25 cuốn thì đều vừa khít không thừa cuốn nào. Tính chính xác số sách tham khảo mà thư viện nhận về."*
- **Phân tích giải tích chuẩn xác:**
  + Gọi số sách tham khảo là $x$ ($x \in \mathbb{N}^*$, $400 \le x \le 550$).
  + Do $x \ \vdots \ 15$, $x \ \vdots \ 20$, $x \ \vdots \ 25 \Rightarrow x \in \mathrm{BC}(15, 20, 25)$.
  + Ta có:
    $$15 = 3 \cdot 5; \quad 20 = 2^2 \cdot 5; \quad 25 = 5^2$$
    $$\Rightarrow \mathrm{BCNN}(15, 20, 25) = 2^2 \cdot 3 \cdot 5^2 = 4 \cdot 3 \cdot 25 = 300$$
  + Tập hợp các bội chung là:
    $$\mathrm{BC}(15, 20, 25) = \mathrm{B}(300) = \{0; 300; 600; 900; 1200; \dots\}$$
  + **Đối chiếu khoảng điều kiện:** Trong khoảng từ $400$ đến $550$ **HOÀN TOÀN KHÔNG CÓ BẤT KỲ BỘI NÀO CỦA 300!**
- ❌ **Hậu quả:** Bài toán bị **vô nghiệm 100%**. Học sinh lớp 6 tìm ra $\mathrm{BCNN} = 300$ nhưng không tìm được số sách thỏa mãn, dẫn đến bế tắc và hoang mang.
- 🛠️ **Phương án vá chuyên môn:**
  + **Cách 1 (Khuyến nghị):** Sửa khoảng số sách thành *"từ **500 đến 700 cuốn**"* $\Rightarrow$ Cho ra đáp số duy nhất là **$600$ cuốn** (thỏa mãn $500 \le 600 \le 700$).
  + **Cách 2:** Giữ nguyên khoảng $400 - 550$, sửa số cuốn từng bó thành *12 cuốn, 15 cuốn hoặc 18 cuốn* ($\mathrm{BCNN}(12, 15, 18) = 180 \Rightarrow$ số sách là **$540$ cuốn**).

---

#### 2. Bài 2 Hình học — PHÂN TÍCH ĐỊNH LƯỢNG HÌNH VẼ & BỘ BA SỐ PYTHAGORE
- **Đề bài & kích thước trên hình vẽ:**
  > *"Ông An có mảnh đất được tô màu theo hình bên dưới. Em hãy giúp ông An tính diện tích và chu vi của mảnh đất đó?"*
  + Mảnh đất hình chữ nhật: Chiều dài $17\text{ m}$, chiều rộng $9\text{ m}$. Cạnh đáy dưới chia thành: $4\text{ m} + 9\text{ m} + 4\text{ m} = 17\text{ m}$.
  + Phần bị khoét ở cạnh đáy dưới: Hình thang cân có đáy lớn $9\text{ m}$, đáy nhỏ $3\text{ m}$, và **hai cạnh bên ghi rõ là $5\text{ m}$**.
  + Mũi tên thẳng đứng ở phần tô màu xanh phía trên có kích thước **$5\text{ m}$**, biểu thị khoảng cách từ mép trên mảnh đất đến đáy nhỏ của hình thang cân.
- **Đối soát hình học định lượng:**
  + Chiều cao của hình thang cân:
    $$h = 9\text{ m} - 5\text{ m} = 4\text{ m}$$
  + Độ dài đoạn hình chiếu của mỗi cạnh bên xuống đáy lớn:
    $$d = \frac{9 - 3}{2} = 3\text{ m}$$
  + Xét tam giác vuông tạo bởi chiều cao $h = 4\text{ m}$, hình chiếu $d = 3\text{ m}$ và cạnh bên $c = 5\text{ m}$:
    $$3^2 + 4^2 = 9 + 16 = 25 = 5^2$$
    *(Khớp chuẩn xác 100% bộ ba số Pythagore kinh điển $3 - 4 - 5$)*.
  + **Kết luận:** Hình vẽ **HOÀN TOÀN CHÍNH XÁC VÀ TỒN TẠI VỀ MẶT HÌNH HỌC EUCLID**. Cạnh bên của hình thang cân đúng bằng $5\text{ m}$.
- **Lời giải và đáp số chuẩn mực:**
  + Diện tích hình chữ nhật ban đầu:
    $$S_{\text{HCN}} = 17 \cdot 9 = 153\text{ m}^2$$
  + Diện tích phần đất bị khoét (hình thang cân):
    $$S_{\text{hình thang}} = \frac{(9 + 3) \cdot 4}{2} = 24\text{ m}^2$$
  + Diện tích mảnh đất của ông An:
    $$S_{\text{mảnh đất}} = S_{\text{HCN}} - S_{\text{hình thang}} = 153 - 24 = 129\text{ m}^2$$
  + Chu vi mảnh đất của ông An (tính theo đường bao viền ngoài):
    $$C = 17 + 9 + 4 + 5 + 3 + 5 + 4 + 9 = 56\text{ m}$$
- 💡 **Lưu ý sư phạm quan trọng khi giảng dạy học sinh lớp 6:**
  + Chiều cao của hình thang là $4\text{ m}$ (được suy ra gián tiếp từ $9 - 5 = 4\text{ m}$).
  + Học sinh lớp 6 rất dễ nhầm lẫn lấy ngay số đo cạnh bên $5\text{ m}$ hoặc số đo khoảng cách $5\text{ m}$ ở phía trên làm chiều cao hình thang, dẫn đến tính sai: $S = \frac{(9 + 3) \cdot 5}{2} = 30\text{ m}^2$. Giáo viên cần lưu ý hướng dẫn học sinh bước quan sát hình để tính chiều cao gián tiếp này.

---

#### 3. Bài 3 Hình học — LỆCH CHUẨN CHƯƠNG TRÌNH TOÁN 6 GDPT 2018
- **Bất cập:** Bài toán yêu cầu tính diện tích miếng bìa hình tam giác thường có đáy $6\text{ cm}$, chiều cao $4\text{ cm}$ ($S = \frac{1}{2} \cdot 6 \cdot 4 = 12\text{ cm}^2$). Công thức tam giác thường là kiến thức của Lớp 5 Tiểu học. Trong học kỳ 1 Toán 6 GDPT 2018 chỉ kiểm tra: Tam giác đều, hình vuông, lục giác đều, hình chữ nhật, hình thoi, hình bình hành, hình thang cân.
- 🛠️ **Phương án vá:** Thay bằng bài toán tính diện tích **hình thoi** có hai đường chéo $6\text{ cm}$ và $8\text{ cm}$ ($S = \frac{1}{2} \cdot 6 \cdot 8 = 24\text{ cm}^2$) hoặc bài toán hình bình hành bám sát ma trận kiểm tra.

---

#### 4. Bài 9 Số học — BẪY SO SÁNH GIẢ TẠO TRONG BÀI TOÁN CHI PHÍ THỰC TẾ
- **Tính toán chi phí khi mua 15 chiếc bánh:**
  + *Cửa hàng 1 (mua 4 tặng 1, giá 30k/chiếc):* Mua 15 chiếc gồm 3 nhóm 5 chiếc, chỉ phải trả tiền $3 \times 4 = 12$ chiếc:
    $$12 \times 30\,000 = 360\,000\text{ đồng}$$
  + *Cửa hàng 2 (5 chiếc đầu giá 28k, từ chiếc thứ 6 giá 22k):*
    $$5 \times 28\,000 + 10 \times 22\,000 = 140\,000 + 220\,000 = 360\,000\text{ đồng}$$
- **Bất cập:** Cả hai cửa hàng đều có chi phí **đúng bằng $360\,000$ đồng**. Câu hỏi *"Nên mua ở cửa hàng nào để chi phí bỏ ra là ít nhất?"* khiến học sinh lúng túng khi kết luận.
- 🛠️ **Phương án vá:** Sửa thành mua **16 chiếc bánh** (Cửa hàng 1 tốn $400\,000$ đ, Cửa hàng 2 tốn $382\,000$ đ $\Rightarrow$ chọn Cửa hàng 2) hoặc yêu cầu tính tiền mỗi cửa hàng và nêu lý do chọn.

---

#### 5. Thể thức và kỹ thuật trình bày
- **Màu chữ:** Các số liệu tại Bài 7, 9 số học và Bài 4, 6 hình học mang **màu chữ xanh dương** do sao chép từ mạng. Cần chuyển 100% về màu đen tự động (Black).
- **Ký hiệu tập hợp Bài 1a:** Sửa $E = \{x \in N / 15 < x \le 21\}$ thành $E = \{x \in \mathbb{N} \mid 15 < x \le 21\}$.
- **Đánh số thứ tự Bài 5:** Sửa câu $f)$ thành $f.$ cho đồng bộ với $a. \ b. \ c. \ d. \ e.$

---

### III. BẢNG TỔNG HỢP VÁ LỖI ĐỐI CHIẾU

| Vị trí bài | Đề cương gốc (Cô Thảo biên soạn) | Phương án chuẩn hóa chuyên môn | Đánh giá sư phạm |
| :--- | :--- | :--- | :--- |
| **Bài 8 (Số học)** | Sách từ $400$ đến $550$ cuốn; xếp bó $15, 20, 25$. ($\mathrm{BCNN} = 300 \Rightarrow$ VÔ NGHIỆM) | Sửa khoảng thành: **$500$ đến $700$ cuốn**. | **Vá lỗi vô nghiệm!** Đáp số chuẩn duy nhất: **$600$ cuốn**. |
| **Bài 2 (Hình học)**| Kích thước cạnh bên $5\text{ m}$, đáy $9\text{ m}$ và $3\text{ m}$, khoảng cách trên $5\text{ m}$. | Giữ nguyên hình vẽ chuẩn. Bổ sung hướng dẫn tính chiều cao: $h = 9 - 5 = 4\text{ m}$. | Số liệu chuẩn xác bộ ba Pythagore ($3-4-5$). $S = 129\text{ m}^2$, $C = 56\text{ m}$. |
| **Bài 3 (Hình học)**| Tính diện tích tam giác thường (đáy 6cm, cao 4cm). | Thay bằng tính diện tích **hình thoi** có hai đường chéo $6\text{ cm}$ và $8\text{ cm}$. | Bám sát 100% chuẩn KT-KN Lớp 6 GDPT 2018. |
| **Bài 9 (Số học)** | Mua 15 bánh; cả hai cửa hàng đều bằng $360\,000$ đ. | Sửa thành mua **16 bánh** (hoặc yêu cầu tính cả 2 nơi và nêu lý do chọn). | Loại bỏ bẫy so sánh giả, kết luận rõ ràng. |
| **Toàn văn bản** | Lẫn chữ màu xanh, ký hiệu tập hợp sai dấu. | Phông Times New Roman 13pt, 100% màu đen; công thức Word Equation $\mathrm{m:oMath}$. | Đồng bộ thể thức trang trọng của nhà trường. |

---

### IV. HỒ SƠ THẨM ĐỊNH ĐÃ BAN HÀNH

Hồ sơ đã được lưu trữ và tích hợp công thức Word Equation $\mathrm{m:oMath}$ chuẩn mực tại:
1. **Bản Word hành chính chính thức (A4 chuẩn thể thức THCS Trần Phú):**  
   👉 [Phan_Bien_De_Cuong_Toan_6.docx](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/4_DUYET_DE/Ket_qua/Phan_Bien_De_Cuong_Toan_6.docx)
2. **Bản Markdown chi tiết lưu trữ hệ thống:**  
   👉 [Phan_Bien_De_Cuong_Toan_6.md](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/4_DUYET_DE/Ket_qua/Phan_Bien_De_Cuong_Toan_6.md)
