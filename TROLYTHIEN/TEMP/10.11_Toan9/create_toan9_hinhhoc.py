# -*- coding: utf-8 -*-
"""
Script sinh 7 tệp KHBD Hình học 9 (Tuần 13 - 18):
- 08_KHBD_Toan9_HinhHoc_Bai16_ViTriTuongDoiDuongThangDuongTron_Tiet19-20.md
- 09_KHBD_Toan9_HinhHoc_Bai17_ViTriTuongDoiHaiDuongTron_Tiet21-22.md
- 10_KHBD_Toan9_HinhHoc_LuyenTapChung_Tiet23.md (Mindmap: mindmap_toan9_hinh_tiet23.png)
- 11_KHBD_Toan9_HinhHoc_BaiTapCuoiChuong5_Tiet24-25.md (Mindmap: mindmap_toan9_hinh_tiet24_25.png)
- 12_KHBD_Toan9_HinhHoc_OnTapCuoiHK1_Tiet26-27.md (Mindmap: mindmap_toan9_hinh_tiet26_27.png)
- 13_KHBD_Toan9_HinhHoc_KiemTraCuoiHK1_Tiet28.md
- 14_KHBD_Toan9_HinhHoc_HDTN_TinhChieuCaoKhoangCach_STEM_Tiet29-30.md
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "C:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/TEMP/10.11_Toan9"
os.makedirs(OUT_DIR, exist_ok=True)

# 08. Bài 16: Vị trí tương đối của đường thẳng và đường tròn (Tiết 19, 20)
md_08 = """Tiết 19, 20 - BÀI 16: VỊ TRÍ TƯƠNG ĐỐI CỦA ĐƯỜNG THẲNG VÀ ĐƯỜNG TRÒN
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nắm vững 3 vị trí tương đối của đường thẳng và đường tròn: Đường thẳng cắt đường tròn (2 điểm chung), Đường thẳng tiếp xúc đường tròn (1 điểm chung duy nhất), Đường thẳng và đường tròn không giao nhau (0 điểm chung).
- Nắm vững hệ thức liên hệ giữa khoảng cách $d$ từ tâm đến đường thẳng và bán kính $R$: Cắt nhau $\\Leftrightarrow d < R$; Tiếp xúc $\\Leftrightarrow d = R$; Không giao nhau $\\Leftrightarrow d > R$.
- Nắm vững định nghĩa và tính chất của tiếp tuyến của đường tròn: Tiếp tuyến vuông góc với bán kính tại tiếp điểm.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát mô hình chuyển động của đường thẳng đối với đường tròn.
- Giao tiếp và hợp tác: Tự tin trao đổi các phương pháp chứng minh một đường thẳng là tiếp tuyến.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Suy luận mối quan hệ giữa số điểm chung và hệ thức giữa $d$ và $R$.
- Năng lực giải quyết vấn đề toán học: Vận dụng định lí Pythagore và tỉ số lượng giác để tính khoảng cách $d$ và độ dài dây cung.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 1.2.TC2a: Sử dụng hình ảnh động và mô phỏng số học để quan sát trực quan hiện tượng tiếp xúc của đường thẳng và đường tròn.***

## 3. Về phẩm chất
- Cẩn thận, tỉ mỉ trong việc vẽ đường vuông góc từ tâm đến đường thẳng và xác định tiếp điểm.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, compa, thước thẳng chia khoảng, êke vuông, bài trình chiếu GeoGebra mô phỏng chuyển động mặt trời mọc (tiếp xúc đường chân trời).
2. Học sinh: SGK Toán 9 tập 1, vở ghi, bộ dụng cụ vẽ hình (thước, compa, êke).

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Gợi mở hình ảnh thực tế về vị trí của đường thẳng và đường tròn (mặt trời nhô lên trên đường chân trời trên biển).
b) Nội dung: Quan sát hình ảnh mặt trời buổi sáng: Lúc chưa nhô lên, lúc vừa chạm mặt biển, lúc đã nhô lên một nửa.
c) Sản phẩm: Câu trả lời mô tả số điểm chung giữa đường chân trời và mặt trời.
d) Tổ chức thực hiện: GV chiếu hình ảnh thực tế, dẫn dắt học sinh vào 3 vị trí tương đối giữa đường thẳng và đường tròn.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC (50 phút)
### Hoạt động 2.1: Ba vị trí tương đối của đường thẳng và đường tròn (25 phút)
a) Mục tiêu: Phân biệt 3 vị trí tương đối dựa vào số điểm chung và so sánh khoảng cách $d$ với bán kính $R$.
b) Nội dung: Đọc mục 1 SGK trang 96 - 98; vẽ hình và hoàn thành bảng hệ thức giữa $d$ và $R$.
c) Sản phẩm: Bảng tổng hợp 3 vị trí tương đối trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho đường tròn $(O; R)$ và đường thẳng $\\Delta$. Kẻ $OH \\perp \\Delta$ ($H \\in \\Delta$). Đặt $OH = d$.<br>- **GV:** Yêu cầu HS so sánh $d$ và $R$ trong 3 trường hợp:<br>1. $\\Delta$ cắt $(O)$ tại 2 điểm $A, B$.<br>2. $\\Delta$ tiếp xúc $(O)$ tại $C$.<br>3. $\\Delta$ và $(O)$ không có điểm chung.<br>- **HS:** Vẽ hình và đo đạc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét: Khi $\\Delta$ đi qua 2 điểm $A, B$ thì trong tam giác vuông $OHA$, $OH < OA = R$ nên $d < R$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS lên bảng hoàn thành bảng tổng kết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt bảng chuẩn kiến thức. | **1. Ba vị trí tương đối:**<br>- **Đường thẳng cắt đường tròn:** Có 2 điểm chung ($d < R$). Đường thẳng gọi là cát tuyến. Khi đó dây $AB = 2\\sqrt{R^2 - d^2}$.<br>- **Đường thẳng tiếp xúc đường tròn:** Có 1 điểm chung duy nhất ($d = R$). Đường thẳng gọi là tiếp tuyến, điểm chung gọi là tiếp điểm.<br>- **Đường thẳng và đường tròn không giao nhau:** Không có điểm chung ($d > R$). |

### Hoạt động 2.2: Dấu hiệu nhận biết tiếp tuyến của đường tròn (25 phút)
a) Mục tiêu: Nắm vững định lí dấu hiệu nhận biết tiếp tuyến và vận dụng vào chứng minh.
b) Nội dung: Đọc mục 2 SGK trang 98 - 99; làm Luyện tập 2.
c) Sản phẩm: Lời giải bài toán chứng minh một đường thẳng là tiếp tuyến.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định lí: Nếu một đường thẳng đi qua một điểm của đường tròn và vuông góc với bán kính đi qua điểm đó thì đường thẳng đó là một tiếp tuyến của đường tròn.<br>- **GV:** Giao bài toán: Cho $\\Delta ABC$ vuông tại $A$, đường cao $AH$. Vẽ đường tròn $(A; AH)$. Chứng minh $BC$ là tiếp tuyến của đường tròn $(A)$.<br>- **HS:** Vẽ hình và phân tích.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét: $H$ thuộc $(A; AH)$ vì $AH = R$, và $BC \\perp AH$ tại $H$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khắc sâu: Cần đủ 2 yếu tố: Điểm thuộc đường tròn và vuông góc bán kính tại điểm đó. | **2. Dấu hiệu nhận biết tiếp tuyến:**<br>- **Định lí:** Nếu đường thẳng $a$ đi qua điểm $C \\in (O)$ và $a \\perp OC$ tại $C$ thì $a$ là tiếp tuyến của $(O)$.<br><br>**Chứng minh $BC$ là tiếp tuyến của $(A; AH)$:**<br>- Điểm $H$ nằm trên đường tròn $(A; AH)$ vì khoảng cách từ $A$ đến $H$ bằng bán kính $AH$.<br>- Mặt khác, $BC \\perp AH$ tại $H$ (vì $AH$ là đường cao của $\\Delta ABC$).<br>- Do đó $BC$ là tiếp tuyến của đường tròn $(A; AH)$ tại tiếp điểm $H$. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (20 phút)
a) Mục tiêu: Rèn luyện kỹ năng tính khoảng cách và xác định vị trí tương đối.
b) Nội dung: Giải bài tập 5.12, 5.13 SGK trang 100.
c) Sản phẩm: Lời giải chính xác trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập 5.12: Cho $(O; 5\\text{ cm})$ và đường thẳng $a$ có khoảng cách đến $O$ là $d$. Xác định vị trí tương đối của $a$ và $(O)$ khi: a) $d = 3\\text{ cm}$; b) $d = 5\\text{ cm}$; c) $d = 6\\text{ cm}$.<br>- **HS:** So sánh $d$ với $R = 5\\text{ cm}$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trả lời nhanh từng trường hợp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đứng dậy đọc kết quả.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại kết quả đúng. | **Bài 5.12 (SGK tr.100):**<br>Ta có $R = 5\\text{ cm}$:<br>a) $d = 3\\text{ cm} < R \\Rightarrow$ Đường thẳng $a$ cắt đường tròn $(O)$ tại 2 điểm phân biệt.<br>b) $d = 5\\text{ cm} = R \\Rightarrow$ Đường thẳng $a$ tiếp xúc với đường tròn $(O)$.<br>c) $d = 6\\text{ cm} > R \\Rightarrow$ Đường thẳng $a$ và đường tròn $(O)$ không giao nhau. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (15 phút)
- **Tích hợp NLS 1.2.TC2a:** GV hướng dẫn học sinh quan sát mô phỏng trên GeoGebra: Khi quay một chiếc bánh xe trên mặt đường nằm ngang, mặt đường luôn là tiếp tuyến của bánh xe và tiếp điểm là điểm đặt của lực ma sát giúp xe di chuyển. Dặn dò học sinh chuẩn bị Bài 17: Vị trí tương đối của hai đường tròn.
"""

# 09. Bài 17: Vị trí tương đối của hai đường tròn (Tiết 21, 22)
md_09 = """Tiết 21, 22 - BÀI 17: VỊ TRÍ TƯƠNG ĐỐI CỦA HAI ĐƯỜNG TRÒN
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nắm vững 3 vị trí tương đối của hai đường tròn: Hai đường tròn cắt nhau (2 điểm chung), Hai đường tròn tiếp xúc nhau (tiếp xúc ngoài và tiếp xúc trong - 1 điểm chung duy nhất), Hai đường tròn không giao nhau (ở ngoài nhau, đựng nhau, đồng tâm - 0 điểm chung).
- Nắm vững hệ thức liên hệ giữa đoạn nối tâm $d = OO'$ và các bán kính $R, r$ ($R \\ge r$).
- Hiểu tính chất của đường nối tâm: Là trục đối xứng của hình gồm hai đường tròn; Nếu hai đường tròn cắt nhau thì đường nối tâm là đường trung trực của dây chung; Nếu tiếp xúc nhau thì tiếp điểm nằm trên đường nối tâm.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa mối quan hệ giữa số điểm chung và hệ thức khoảng cách đoạn nối tâm.
- Giao tiếp và hợp tác: Hợp tác nhóm vẽ hình và đo đạc vị trí tương đối của các cặp bánh răng cơ khí.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Suy luận tính chất đối xứng của đường nối tâm qua phép đối xứng trục.
- Năng lực giải quyết vấn đề toán học: Vận dụng tính chất đường trung trực chứng minh hai tam giác bằng nhau hoặc tam giác vuông.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 3.1.TC2a: Sử dụng phần mềm GeoGebra thay đổi khoảng cách hai tâm $O, O'$ để quan sát sự chuyển tiếp giữa các vị trí tương đối.***

## 3. Về phẩm chất
- Cẩn thận, kiên nhẫn trong việc dựng hình chính xác hai đường tròn và tiếp tuyến chung.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, mô hình hai vòng tròn lồng nhau, thước kẻ, compa, bảng phụ ghi hệ thức nối tâm.
2. Học sinh: SGK Toán 9 tập 1, vở ghi, compa, thước kẻ.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Xuất phát từ hình ảnh hai bánh răng ăn khớp nhau hoặc biểu tượng 5 vòng tròn Olympic.
b) Nội dung: Quan sát biểu tượng Olympic và nêu các vị trí của từng cặp vòng tròn (cắt nhau, không giao nhau).
c) Sản phẩm: Nhận biết được số điểm chung giữa các vòng tròn có thể là 0, 1 hoặc 2.
d) Tổ chức thực hiện: GV chiếu hình ảnh lá cờ Olympic, dẫn dắt học sinh tìm hiểu các vị trí tương đối của hai đường tròn.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC (50 phút)
### Hoạt động 2.1: Ba vị trí tương đối và hệ thức giữa đoạn nối tâm với các bán kính (30 phút)
a) Mục tiêu: Lập bảng hệ thức giữa $d = OO'$ và $R, r$ ($R \\ge r$) ứng với từng vị trí.
b) Nội dung: Khảo sát mục 1 SGK trang 101 - 103; điền bảng hệ thống.
c) Sản phẩm: Bảng tổng hợp vị trí tương đối của hai đường tròn.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho $(O; R)$ và $(O'; r)$ với $R \\ge r$. Gọi $d = OO'$.<br>- **GV:** Hướng dẫn HS xét các trường hợp:<br>1. Hai đường tròn cắt nhau tại $A, B$: Bất đẳng thức tam giác trong $\\Delta OAO'$.<br>2. Tiếp xúc ngoài và tiếp xúc trong.<br>3. Ở ngoài nhau và đựng nhau.<br>- **HS:** Làm việc theo nhóm 4 em.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trong $\\Delta OAO'$ có $OA = R, O'A = r, OO' = d$. Theo BĐT tam giác: $R - r < d < R + r$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện nhóm lên điền vào bảng trên bảng phụ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại bảng hệ thức chuẩn. | **1. Hệ thức giữa đoạn nối tâm $d$ và bán kính $R, r$ ($R \\ge r$):**<br>- **Cắt nhau:** Có 2 điểm chung $\\Rightarrow R - r < d < R + r$.<br>- **Tiếp xúc ngoài:** Có 1 điểm chung $\\Rightarrow d = R + r$.<br>- **Tiếp xúc trong:** Có 1 điểm chung $\\Rightarrow d = R - r > 0$.<br>- **Ở ngoài nhau:** Có 0 điểm chung $\\Rightarrow d > R + r$.<br>- **Đựng nhau:** Có 0 điểm chung $\\Rightarrow d < R - r$. (Đặc biệt $d = 0$: Đồng tâm). |

### Hoạt động 2.2: Tính chất của đường nối tâm (20 phút)
a) Mục tiêu: Nắm vững tính chất của đường nối tâm đối với dây chung và tiếp điểm.
b) Nội dung: Đọc mục 2 SGK trang 103 - 104; làm Luyện tập 2.
c) Sản phẩm: Lời chứng minh đường nối tâm là trung trực của dây chung.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho $(O)$ và $(O')$ cắt nhau tại $A$ và $B$.<br>- **GV:** Hỏi: Vì sao $OO'$ là đường trung trực của đoạn thẳng $AB$?<br>- **HS:** Nhớ lại định nghĩa đường trung trực.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ta có $OA = OB = R \\Rightarrow O$ thuộc trung trực của $AB$. Tương tự $O'A = O'B = r \\Rightarrow O'$ thuộc trung trực của $AB$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày lập luận.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Do đó đường thẳng $OO'$ là đường trung trực của dây chung $AB$. | **2. Tính chất đường nối tâm:**<br>- Đường nối tâm $OO'$ là trục đối xứng của hình gồm cả hai đường tròn $(O)$ và $(O')$.<br>- **Định lí:**<br>+ Nếu hai đường tròn cắt nhau tại $A$ và $B$ thì $OO'$ là đường trung trực của đoạn thẳng $AB$.<br>+ Nếu hai đường tròn tiếp xúc nhau tại $A$ thì tiếp điểm $A$ nằm trên đường thẳng $OO'$. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (20 phút)
a) Mục tiêu: Vận dụng giải bài toán tính độ dài dây chung.
b) Nội dung: Cho $(O; 20\\text{ cm})$ và $(O'; 15\\text{ cm})$ cắt nhau tại $A$ và $B$. Biết $OO' = 25\\text{ cm}$. Tính độ dài dây chung $AB$.
c) Sản phẩm: Lời giải chi tiết tìm ra $AB = 24\\text{ cm}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn: Kiểm tra xem $\\Delta OAO'$ có phải là tam giác vuông không? (Định lí Pythagore đảo).<br>- **HS:** Tính $20^2 + 15^2 = 400 + 225 = 625 = 25^2$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Gọi $H$ là giao điểm của $OO'$ và $AB$. Vì $OO' \\perp AB$ tại $H$ nên $AH$ là đường cao của $\\Delta OAO'$ vuông tại $A$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS tính: $AH = \\frac{OA \\cdot O'A}{OO'} = \\frac{20 \\cdot 15}{25} = 12\\text{ cm}$. Suy ra $AB = 2AH = 24\\text{ cm}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt cách kết hợp hệ thức lượng tam giác vuông vào đường tròn. | **Lời giải:**<br>- Xét $\\Delta OAO'$, ta có:<br>$OA^2 + O'A^2 = 20^2 + 15^2 = 400 + 225 = 625$.<br>$OO'^2 = 25^2 = 625$.<br>Suy ra $OA^2 + O'A^2 = OO'^2$, do đó $\\Delta OAO'$ vuông tại $A$.<br>- Gọi $H$ là giao điểm của $OO'$ và $AB$. Vì $OO'$ là trung trực của $AB$ nên $OO' \\perp AB$ tại trung điểm $H$ của $AB$.<br>- Trong tam giác vuông $OAO'$ có đường cao $AH$:<br>$AH \\cdot OO' = OA \\cdot O'A \\Rightarrow AH = \\frac{20 \\cdot 15}{25} = 12\\text{ cm}$.<br>- Vì $H$ là trung điểm của $AB$ nên:<br>$AB = 2AH = 2 \\cdot 12 = 24\\text{ cm}$. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (15 phút)
- **Tích hợp NLS 3.1.TC2a:** Hướng dẫn học sinh sử dụng thanh trượt (`Slider`) trong GeoGebra để gán cho khoảng cách $d$ biến thiên từ $0$ đến $40$, quan sát trực quan các trạng thái: Đựng nhau $\\rightarrow$ Tiếp xúc trong $\\rightarrow$ Cắt nhau $\\rightarrow$ Tiếp xúc ngoài $\\rightarrow$ Ngoài nhau. Dặn dò chuẩn bị tiết Luyện tập chung Chương V.
"""

# 10. Luyện tập chung (Hình học - Tiết 23)
md_10 = """Tiết 23 - LUYỆN TẬP CHUNG: VỊ TRÍ TƯƠNG ĐỐI CỦA ĐƯỜNG THẲNG VÀ ĐƯỜNG TRÒN
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố toàn bộ các định lí về vị trí tương đối của đường thẳng và đường tròn, tính chất hai tiếp tuyến cắt nhau và vị trí tương đối của hai đường tròn.
- Vận dụng thành thạo tính chất tiếp tuyến và đường nối tâm để giải các bài toán chứng minh vuông góc, thẳng hàng và tính độ dài đoạn thẳng.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa các định lí và hệ thức vị trí tương đối qua sơ đồ tư duy.
- Giao tiếp và hợp tác: Tự tin trao đổi các phương pháp chứng minh tiếp tuyến trong nhóm bạn.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Xây dựng sơ đồ suy luận ngược để chứng minh tiếp tuyến của đường tròn.
- Năng lực giải quyết vấn đề toán học: Phối hợp hệ thức lượng trong tam giác vuông với tính chất hai tiếp tuyến cắt nhau.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 1.2.TC2a: Tìm kiếm các tài liệu bài tập hình học tương tác và hình ảnh động trực tuyến để hỗ trợ giải toán hình học.***

## 3. Về phẩm chất
- Cẩn thận, chính xác trong từng nét vẽ tiếp tuyến và từng bước suy diễn hình học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy Luyện tập chung Chương V, compa, thước thẳng, phiếu học tập nhóm.
2. Học sinh: SGK Toán 9 tập 1, vở ghi, bộ dụng cụ vẽ hình đầy đủ.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (4 phút)
a) Mục tiêu: Kích hoạt kiến thức về tính chất hai tiếp tuyến cắt nhau.
b) Nội dung: Nêu tính chất của hai tiếp tuyến của đường tròn $(O)$ cắt nhau tại điểm $M$.
c) Sản phẩm: Trả lời: $MA = MB$, $MO$ là tia phân giác của góc $\\widehat{AMB}$, $OM$ là tia phân giác của góc $\\widehat{AOB}$.
d) Tổ chức thực hiện: GV gọi 1 HS nhắc lại, cả lớp nhận xét và vào bài luyện tập.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (33 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức bằng sơ đồ tư duy (8 phút)
a) Mục tiêu: Hệ thống hóa toàn diện các vị trí tương đối và tính chất tiếp tuyến qua sơ đồ tư duy.
b) Nội dung: Trình chiếu và phân tích Sơ đồ tư duy Vị trí tương đối đường thẳng và đường tròn.
c) Sản phẩm: Sơ đồ tư duy được vẽ và khắc sâu trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy hệ thống hóa Chương V.<br>- **GV:** Yêu cầu HS nêu 4 nhánh chính: Đường thẳng & đường tròn; Tính chất tiếp tuyến; Vị trí hai đường tròn; Tính chất đường nối tâm.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhắc lại hệ thức so sánh $d$ với $R$ và $R \\pm r$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy thuyết minh toàn bộ sơ đồ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Đường nối tâm luôn là trục đối xứng và là đường trung trực của dây chung. | **SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: VỊ TRÍ TƯƠNG ĐỐI ĐƯỜNG THẲNG VÀ ĐƯỜNG TRÒN**<br><br>*(Sơ đồ tư duy hệ thống hóa hiển thị dưới đây)* |

![Sơ đồ tư duy Luyện tập chung Hình học 9](khbd-ill:mindmap-toan9-hinh-tiet23)

### Hoạt động 2.2: Luyện tập bài toán chứng minh tiếp tuyến và tính độ dài (25 phút)
a) Mục tiêu: Vận dụng tính chất hai tiếp tuyến cắt nhau để chứng minh tam giác vuông và tính đoạn thẳng.
b) Nội dung: Giải bài tập 5.17 SGK trang 106.
c) Sản phẩm: Lời giải chi tiết và hình vẽ chính xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập: Từ điểm $M$ ở ngoài $(O; R)$, vẽ hai tiếp tuyến $MA, MB$ ($A, B$ là các tiếp điểm). Đoạn thẳng $MO$ cắt $AB$ tại $H$.<br>a) Chứng minh $MO \\perp AB$ tại $H$.<br>b) Biết $R = 6\\text{ cm}, MO = 10\\text{ cm}$. Tính độ dài $MA, AB$.<br>- **HS:** Vẽ hình và phân tích.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Áp dụng định lí Pythagore trong $\\Delta MAO$ vuông tại $A$ để tính $MA$. Sau đó dùng hệ thức lượng tính $AH$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày câu a và câu b.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Uốn nắn cách trình bày và chuẩn hóa lời giải. | **Bài giải chi tiết:**<br>**a) Chứng minh $MO \\perp AB$:**<br>- Theo tính chất hai tiếp tuyến cắt nhau, ta có $MA = MB$.<br>Suy ra $M$ thuộc đường trung trực của đoạn thẳng $AB$.<br>- Lại có $OA = OB = R$, suy ra $O$ thuộc đường trung trực của $AB$.<br>- Do đó $MO$ là đường trung trực của đoạn thẳng $AB$, suy ra $MO \\perp AB$ tại $H$ và $H$ là trung điểm của $AB$.<br><br>**b) Tính độ dài $MA, AB$:**<br>- Vì $MA$ là tiếp tuyến của $(O)$ nên $MA \\perp OA$ tại $A$.<br>- Áp dụng định lí Pythagore trong $\\Delta MAO$ vuông tại $A$:<br>$MA = \\sqrt{MO^2 - OA^2} = \\sqrt{10^2 - 6^2} = \\sqrt{64} = 8\\text{ cm}$.<br>- Áp dụng hệ thức lượng trong $\\Delta MAO$ vuông tại $A$ có đường cao $AH$:<br>$AH \\cdot MO = MA \\cdot OA \\Rightarrow AH = \\frac{8 \\cdot 6}{10} = 4{,}8\\text{ cm}$.<br>- Vì $H$ là trung điểm của $AB$ nên:<br>$AB = 2AH = 2 \\cdot 4{,}8 = 9{,}6\\text{ cm}$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
- **Tích hợp NLS 1.2.TC2a:** Hướng dẫn học sinh tra cứu các dạng bài tập hình học liên quan đến tiếp tuyến chung của hai đường tròn trên các trang học liệu số để rèn luyện thêm kỹ năng vẽ đường phụ. Dặn dò chuẩn bị 2 tiết Bài tập cuối chương V.
"""

# 11. Bài tập cuối chương V (Hình học - Tiết 24, 25)
md_11 = """Tiết 24, 25 - BÀI TẬP CUỐI CHƯƠNG V (ĐƯỜNG TRÒN)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Chương V môn Toán 9: Sự xác định đường tròn và tính chất đối xứng; Đường kính và dây cung; Vị trí tương đối của đường thẳng và đường tròn, tính chất hai tiếp tuyến cắt nhau; Độ dài cung tròn, diện tích hình quạt tròn và hình vành khuyên.
- Khắc sâu các phương pháp giải bài toán tổng hợp về đường tròn: Chứng minh tiếp tuyến, chứng minh các điểm cùng thuộc một đường tròn, tính chu vi và diện tích các hình liên quan đến đường tròn.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác tổng kết toàn bộ lý thuyết và sơ đồ tư duy Chương V.
- Giải quyết vấn đề và sáng tạo: Lựa chọn nhiều hướng tiếp cận để chứng minh một bài toán hình học đường tròn.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Chuỗi lập luận hình học có căn cứ, suy diễn logic từ giả thiết đến kết luận.
- Năng lực mô hình hóa toán học: Tính diện tích mặt cắt hình vành khuyên của ống dẫn nước hoặc diện tích cánh quạt xoay.

c) Năng lực số (NLS):
- Năng lực số: Biết dùng máy tính bỏ túi tính toán chính xác giá trị lượng giác và các công thức chứa số $\\pi$.

## 3. Về phẩm chất
- Rèn luyện tính cẩn trọng, chính xác trong từng câu chữ lập luận và sự gọn gàng, thẩm mĩ trong hình vẽ.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy tổng hợp Chương V, hệ thống bài tập trắc nghiệm và tự luận phân loại cuối chương V.
2. Học sinh: SGK Toán 9 tập 1, vở ghi, bộ dụng cụ vẽ hình đầy đủ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Khởi động và kiểm tra nhanh công thức diện tích hình quạt tròn và hình vành khuyên.
b) Nội dung: Nêu công thức tính diện tích hình quạt tròn bán kính $R$, cung $n^\\circ$ và diện tích hình vành khuyên giới hạn bởi hai đường tròn đồng tâm bán kính $R, r$.
c) Sản phẩm: Công thức: $S_{\\text{qt}} = \\frac{\\pi R^2 n}{360}$; $S_{\\text{vk}} = \\pi(R^2 - r^2)$.
d) Tổ chức thực hiện: GV gọi 1 HS nêu nhanh, cả lớp nhận xét và vào bài học ôn tập.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (75 phút)
### Hoạt động 2.1: Hệ thống hóa toàn diện kiến thức Chương V qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Khái quát toàn bộ bức tranh kiến thức hình học Chương V một cách trực quan.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy tổng kết Chương V: Đường tròn.
c) Sản phẩm: Bản ghi nhớ sơ đồ tư duy trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy tổng kết Chương V: Đường tròn.<br>- **GV:** Yêu cầu HS nêu 4 nhánh chính: Sự xác định đường tròn; Đường kính & Dây cung; Tiếp tuyến của đường tròn; Cung và hình quạt tròn.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết lại các định lí quan hệ giữa đường kính và dây cung.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy thuyết minh toàn bộ sơ đồ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Đường kính vuông góc với dây thì đi qua trung điểm của dây là một định lí được sử dụng rất thường xuyên. | **SƠ ĐỒ TƯ DUY TỔNG KẾT CHƯƠNG V: ĐƯỜNG TRÒN**<br><br>*(Sơ đồ tư duy hệ thống hóa hiển thị dưới đây)* |

![Sơ đồ tư duy Bài tập cuối chương V Hình học 9](khbd-ill:mindmap-toan9-hinh-tiet24_25)

### Hoạt động 2.2: Giải các bài tập trắc nghiệm cuối chương V (15 phút)
a) Mục tiêu: Củng cố kỹ năng làm bài trắc nghiệm hình học nhanh và chuẩn xác.
b) Nội dung: Giải các câu hỏi trắc nghiệm 5.18 đến 5.21 SGK trang 107.
c) Sản phẩm: Đáp án chọn đúng và lời giải thích ngắn gọn của học sinh.
d) Tổ chức thực hiện: GV chiếu câu hỏi, học sinh trả lời và giải thích lý do loại trừ phương án sai.

### Hoạt động 2.3: Giải bài toán tự luận tổng hợp về đường tròn (45 phút)
a) Mục tiêu: Rèn luyện bài toán hình học tổng hợp thường gặp trong đề thi tuyển sinh vào lớp 10.
b) Nội dung: Giải bài tập 5.23 SGK trang 108.
c) Sản phẩm: Lời giải hoàn chỉnh và hình vẽ chính xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho đường tròn $(O)$, đường kính $AB$. Lấy điểm $C \\in (O)$ sao cho $AC < BC$. Kẻ tiếp tuyến tại $A$ của $(O)$. Tia $BC$ cắt tiếp tuyến tại $D$. Kẻ $CH \\perp AB$ ($H \\in AB$).<br>a) Chứng minh $\\Delta ABC$ vuông tại $C$.<br>b) Chứng minh $DA^2 = DC \\cdot DB$.<br>- **HS:** Vẽ hình và ghi GT - KL.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét: Tam giác $ABC$ nội tiếp đường tròn có cạnh $AB$ là đường kính nên vuông tại $C$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chứng minh từng câu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Uốn nắn cách trình bày hệ thức lượng trong tam giác vuông $DAB$. | **Bài 5.23 (SGK tr.108):**<br>**a) Chứng minh $\\Delta ABC$ vuông tại $C$:**<br>- Điểm $C$ nằm trên đường tròn đường kính $AB$ nên $\\widehat{ACB} = 90^\\circ$.<br>- Do đó $\\Delta ABC$ vuông tại $C$.<br><br>**b) Chứng minh $DA^2 = DC \\cdot DB$:**<br>- Vì $AD$ là tiếp tuyến tại $A$ của đường tròn $(O)$ nên $AD \\perp AB$ tại $A$, suy ra $\\Delta DAB$ vuông tại $A$.<br>- Ta có $\\widehat{ACB} = 90^\\circ$ nên $AC \\perp BD$ tại $C$, do đó $AC$ là đường cao của $\\Delta DAB$ vuông tại $A$.<br>- Áp dụng hệ thức lượng trong tam giác vuông $DAB$:<br>$DA^2 = DC \\cdot DB$ (đpcm). |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (10 phút)
- **Vận dụng thực tiễn:** Tính diện tích phần kim loại cần dùng để sản xuất một chiếc long đen (vành khuyên kim loại) có đường kính ngoài $30\\text{ mm}$ và đường kính lỗ tròn trong $14\\text{ mm}$. Áp dụng công thức $S = \\pi(R^2 - r^2) = \\pi(15^2 - 7^2) = 176\\pi \\approx 552{,}9\\text{ mm}^2$. Dặn dò chuẩn bị cho 2 tiết Ôn tập cuối học kì I môn Toán 9 (Hình học).
"""

# 12. Ôn tập cuối HKI (Hình học - Tiết 26, 27)
md_12 = """Tiết 26, 27 - ÔN TẬP CUỐI HỌC KÌ I (HÌNH HỌC)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn diện các kiến thức Hình học kì I Toán 9:
  + Chương IV: Hệ thức lượng trong tam giác vuông (Các hệ thức về cạnh và đường cao, tỉ số lượng giác của góc nhọn, giải tam giác vuông và ứng dụng thực tế).
  + Chương V: Đường tròn (Định nghĩa, đường kính và dây cung, các vị trí tương đối của đường thẳng và đường tròn, tính chất hai tiếp tuyến cắt nhau).
- Rèn luyện kỹ năng vẽ hình phụ trợ (kẻ đường kính, kẻ tiếp tuyến), trình bày bài toán hình học theo sơ đồ lập luận logic, chặt chẽ.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức hình học qua sơ đồ tư duy toàn diện HKI.
- Giao tiếp và hợp tác: Tự tin trao đổi các bước chứng minh hình học trước tập thể lớp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát mối liên hệ mật thiết giữa hệ thức lượng tam giác vuông và các tính chất tiếp tuyến đường tròn.
- Năng lực giải quyết vấn đề toán học: Vận dụng linh hoạt tỉ số lượng giác và định lí đường tròn vào bài toán đo đạc thực tế.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 1.2.TC2a: Tìm kiếm và giải thử các đề thi học kì I trực tuyến để rèn luyện tốc độ làm bài thi.***

## 3. Về phẩm chất
- Trung thực, kiên trì, chính xác trong vẽ hình và trình bày lời giải chứng minh hình học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy Ôn tập tổng hợp Hình học HKI, thước kẻ, êke, compa, đề cương ôn tập bám sát cấu trúc đề thi.
2. Học sinh: SGK Toán 9 tập 1, vở ghi, dụng cụ vẽ hình đầy đủ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Xác định rõ mục tiêu ôn tập phần Hình học kì I để đạt kết quả tối ưu trong kì kiểm tra cuối HKI.
b) Nội dung: Điểm lại tỉ lệ điểm số phần Hình học trong đề thi HKI (Hệ thức lượng và Đường tròn).
c) Sản phẩm: Tâm thế tự tin, quyết tâm ôn tập nghiêm túc của học sinh.
d) Tổ chức thực hiện: GV quán triệt nội dung trọng tâm, nhắc nhở các lỗi sai thường gặp khi vẽ hình và vào bài học.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (75 phút)
### Hoạt động 2.1: Khái quát mạng lưới kiến thức Hình học HKI qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa hai chương Hình học cốt lõi (Chương IV và Chương V) trên một sơ đồ tư duy khoa học.
b) Nội dung: Trình chiếu và phân tích Sơ đồ tư duy Ôn tập học kì I: Hình học 9.
c) Sản phẩm: Sơ đồ tư duy được vẽ và khắc sâu trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Ôn tập Hình học HKI.<br>- **GV:** Yêu cầu HS nêu 4 nhánh chính: Chương IV (Hệ thức lượng); Giải tam giác vuông; Chương V (Đường tròn); Chứng minh hình học.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết lại 5 hệ thức cạnh - đường cao và 4 tỉ số lượng giác $\\sin, \\cos, \\tan, \\cot$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS đọc thuộc lòng các hệ thức lượng trong tam giác vuông.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Tam giác vuông có đường cao hạ từ đỉnh góc vuông là chiếc cầu nối giữa Chương IV và Chương V. | **SƠ ĐỒ TƯ DUY ÔN TẬP HỌC KÌ I: HÌNH HỌC 9**<br><br>*(Sơ đồ tư duy hệ thống hóa hiển thị dưới đây)* |

![Sơ đồ tư duy Ôn tập Học kì I Hình học Toán 9](khbd-ill:mindmap-toan9-hinh-tiet26_27)

### Hoạt động 2.2: Rèn luyện giải tam giác vuông và ứng dụng thực tế (25 phút)
a) Mục tiêu: Thành thạo tính cạnh và góc của tam giác vuông trong bài toán đo chiều cao vật thể.
b) Nội dung: Giải bài toán ứng dụng thực tế đo chiều cao tháp trong đề cương.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Một người đứng cách chân một tòa tháp $30\\text{ m}$, nhìn lên đỉnh tháp dưới một góc nâng $42^\\circ$. Mắt người cách mặt đất $1{,}6\\text{ m}$. Tính chiều cao của tòa tháp (làm tròn đến hàng phần mười).<br>- **HS:** Vẽ hình minh họa mô hình tam giác vuông.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Gọi chiều cao tháp là $h = AB + 1{,}6$. Trong tam giác vuông $ABC$: $AB = BC \\cdot \\tan(42^\\circ)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS bấm máy tính: $AB = 30 \\cdot \\tan(42^\\circ) \\approx 30 \\cdot 0{,}9004 \\approx 27{,}01\\text{ m}$. Suy ra $h \\approx 27{,}01 + 1{,}6 \\approx 28{,}6\\text{ m}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Uốn nắn cách làm tròn số và kết luận bài toán thực tế. | **Bài toán thực tế:**<br>- Mô hình hóa bài toán bằng $\\Delta ABC$ vuông tại $B$ với $BC = 30\\text{ m}$, $\\widehat{ACB} = 42^\\circ$.<br>- Trong tam giác vuông $ABC$, ta có:<br>$AB = BC \\cdot \\tan(\\widehat{ACB}) = 30 \\cdot \\tan(42^\\circ) \\approx 27{,}01\\text{ m}$.<br>- Chiều cao của tòa tháp là:<br>$H = AB + 1{,}6 \\approx 27{,}01 + 1{,}6 = 28{,}61 \\approx 28{,}6\\text{ m}$.<br>- Vậy tòa tháp cao khoảng $28{,}6\\text{ m}$. |

### Hoạt động 2.3: Rèn luyện bài toán chứng minh tiếp tuyến và hệ thức hình học (35 phút)
a) Mục tiêu: Vận dụng phối hợp tiếp tuyến và tam giác đồng dạng.
b) Nội dung: Giải bài toán hình học tổng hợp trong đề cương ôn tập.
c) Sản phẩm: Lời giải chi tiết và hình vẽ chính xác của học sinh.
d) Tổ chức thực hiện:
- GV giao bài toán cho đường tròn $(O)$, điểm $M$ ngoài đường tròn, vẽ tiếp tuyến $MA, MB$ và cát tuyến $MCD$. HS chứng minh $MA^2 = MC \\cdot MD$ và $MO \\perp AB$. GV chuẩn hóa lời giải trên bảng.

## C. HOẠT ĐỘNG 3: VẬN DỤNG (10 phút)
- **Tích hợp NLS 1.2.TC2a:** Hướng dẫn học sinh tra cứu các đề thi học kì I môn Toán 9 các năm trước trên các cổng thông tin giáo dục điện tử để luyện tập thêm bài tập hình học tổng hợp. Dặn dò chuẩn bị chu đáo dụng cụ vẽ hình (compa, êke, thước chia mm) cho buổi kiểm tra cuối HKI.
"""

# 13. Kiểm tra cuối HKI (Hình học - Tiết 28)
md_13 = """Tiết 28 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá chuẩn xác mức độ tiếp thu và năng lực vận dụng kiến thức Hình học Học kì I Toán 9: Hệ thức lượng trong tam giác vuông, Tỉ số lượng giác và Hình học đường tròn.
- Phân loại học sinh, phát hiện các điểm sai sót trong kĩ năng vẽ hình và lập luận chứng minh hình học để có kế hoạch bồi dưỡng trong Học kì II.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Nghiêm túc, tự giác, độc lập hoàn thành bài kiểm tra theo đúng thời gian quy định.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học; Năng lực giải quyết vấn đề toán học: Diễn đạt rõ ràng, vẽ hình chuẩn xác, trình bày bài toán hình học mạch lạc, có căn cứ.

## 3. Về phẩm chất
- Trung thực, tự trọng, có trách nhiệm với kết quả rèn luyện của bản thân.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo ma trận đề HKI phần Hình học, đáp án và thang điểm chi tiết.
2. Học sinh: Bút viết, máy tính cầm tay, bộ dụng cụ vẽ hình (thước thẳng chia vạch, êke, compa), giấy nháp.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: ỔN ĐỊNH LỚP VÀ PHÁT ĐỀ (3 phút)
- GV kiểm tra sĩ số, phổ biến nội quy phòng thi, yêu cầu học sinh cất tài liệu vào ngăn bàn.
- GV phát đề kiểm tra đến từng học sinh.

## B. HOẠT ĐỘNG 2: HỌC SINH LÀM BÀI KIỂM TRA (40 phút)
- Học sinh làm bài nghiêm túc, độc lập theo đúng thời gian quy định.
- Giáo viên quan sát, bao quát phòng thi, nhắc nhở học sinh giữ trật tự.

## C. HOẠT ĐỘNG 3: THU BÀI VÀ DẶN DÒ (2 phút)
- GV cho học sinh dừng bút, kiểm tra lại thông tin họ tên, lớp trên bài làm.
- GV thu bài và kiểm đếm đủ số bài theo sĩ số. Dặn dò chuẩn bị dụng cụ cho tiết Hoạt động thực hành trải nghiệm STEM: Tính chiều cao và khoảng cách.
"""

# 14. HĐTN: Tính chiều cao và xác định khoảng cách (STEM - Tiết 29, 30)
md_14 = """Tiết 29, 30 - HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: TÍNH CHIỀU CAO VÀ XÁC ĐỊNH KHOẢNG CÁCH (KHBD STEM)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Vận dụng các hệ thức lượng và tỉ số lượng giác của góc nhọn trong tam giác vuông vào việc giải quyết các bài toán đo đạc thực tế ngoài trời:
  + Đo chiều cao của một vật thể cao không thể trèo lên đỉnh đo trực tiếp (cột cờ trường, cây xanh cổ thụ, cột đèn cao áp, tòa nhà).
  + Xác định khoảng cách giữa hai vị trí trên mặt đất mà ở giữa có vật cản không thể căng dây đo trực tiếp (khoảng cách giữa hai bờ hồ, hai điểm bị ngăn bởi bụi cây hoặc mương nước).
- Làm quen và thành thạo chế tạo, sử dụng thiết bị đo góc nghiêng đơn giản (giác kế đứng / thước đo góc nghiêng cầm tay tự chế).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thiết kế và chế tạo giác kế đo góc đứng từ bìa cứng, ống hút và dây dọi.
- Giao tiếp và hợp tác: Làm việc nhóm hiệu quả ngoài hiện trường, phân công rõ ràng các vai trò: người ngắm góc, người đo khoảng cách mặt đất, người ghi chép số liệu, người tính toán.

b) Năng lực đặc thù môn Toán & Năng lực STEM:
- Năng lực mô hình hóa toán học: Chuyển đổi hiện trường thực tế thành mô hình tam giác vuông với các yếu tố đã đo được.
- Năng lực giải quyết vấn đề toán học: Tính toán chiều cao và khoảng cách bằng công thức lượng giác: $h = d \\cdot \\tan(\\alpha) + h_0$.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 3.1.TC2a: Sử dụng ứng dụng đo góc nghiêng (Clinometer) hoặc la bàn số trên điện thoại thông minh để kiểm chứng số liệu đo được từ giác kế tự chế.***

## 3. Về phẩm chất
- Tinh thần đồng đội, kiên trì, cẩn trọng, an toàn khi thao tác ngoài trời và yêu thích ứng dụng thực tế của Toán học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy STEM, thước dây cuộn dài $30\\text{ m}$, máy kinh vĩ quang học (nếu có) hoặc giác kế đứng mẫu, cọc tiêu.
2. Học sinh: Mỗi nhóm chuẩn bị:
  + 01 Giác kế đứng tự chế (gồm thước đo độ $180^\\circ$ dán lên bìa cứng, ống hút nhựa ngắm thẳng, sợi chỉ buộc viên chì làm dây dọi).
  + Thước cuộn dài $5\\text{ m}$, máy tính cầm tay, sổ tay ghi số liệu thực địa.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU - XÁC ĐỊNH NHIỆM VỤ THỰC ĐỊA STEM (10 phút)
a) Mục tiêu: Đặt ra nhiệm vụ thực tế đo chiều cao cột cờ trường học và đo khoảng cách qua một bồn hoa lớn trong sân trường mà không dẫm lên hoa.
b) Nội dung: GV chia lớp thành 4 nhóm, phổ biến nhiệm vụ đo đạc tại sân trường, giới thiệu nguyên lí hoạt động của giác kế ngắm góc.
c) Sản phẩm: Bảng phân công nhiệm vụ chi tiết của 4 nhóm học sinh.
d) Tổ chức thực hiện: GV giao nhiệm vụ, kiểm tra thiết bị giác kế tự chế của các nhóm và hướng dẫn học sinh di chuyển an toàn ra sân trường.

## B. HOẠT ĐỘNG 2: NGHIÊN CỨU KIẾN THỨC NỀN VÀ THỰC HÀNH ĐO ĐẠC (40 phút)
### Hoạt động 2.1: Ôn tập mô hình toán học đo chiều cao và khoảng cách (10 phút)
a) Mục tiêu: Khắc sâu công thức tính chiều cao khi ngắm từ xa một góc $\\alpha$.
b) Nội dung: Ôn lại công thức $h = AB + h_0 = d \\cdot \\tan(\\alpha) + h_0$, trong đó $d$ là khoảng cách từ vị trí đứng ngắm đến chân vật, $h_0$ là chiều cao từ mắt người ngắm đến mặt đất.
c) Sản phẩm: Công thức tính toán được ghi nhớ trong sổ tay của từng nhóm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Vẽ sơ đồ mô hình tam giác vuông lên bảng di động ngoài sân trường.<br>- **GV:** Giải thích: Tại sao phải cộng thêm chiều cao $h_0$ của mắt người ngắm?<br>- **HS:** Thảo luận nhanh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét: Thước đo góc đặt ngang tầm mắt, tia ngắm tạo tam giác vuông lơ lửng trên mặt đất nên phải cộng thêm độ cao từ mắt xuống đất.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS nêu công thức chuẩn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa quy trình: Đo 3 lần lấy trung bình cộng để giảm sai số. | **Mô hình toán học:**<br>- Gọi $C$ là đỉnh cột cờ, $D$ là chân cột cờ.<br>- Người ngắm đứng tại vị trí cách chân cột cờ một khoảng $d$, mắt ở độ cao $h_0$.<br>- Ngắm lên đỉnh cột cờ dưới một góc nghiêng $\\alpha$.<br>- Ta có: $CD = d \\cdot \\tan(\\alpha) + h_0$. |

### Hoạt động 2.2: Các nhóm thực hành đo đạc ngoài hiện trường sân trường (30 phút)
a) Mục tiêu: Các nhóm tự chọn vị trí đặt giác kế, dùng thước cuộn đo khoảng cách $d$, ngắm đọc góc $\\alpha$, ghi chép vào bảng số liệu.
b) Nội dung: Thực hành đo chiều cao cột cờ và đo khoảng cách hai điểm qua bồn hoa.
c) Sản phẩm: Bảng số liệu thực địa gồm 3 lần đo góc và khoảng cách của mỗi nhóm.
d) Tổ chức thực hiện:
- GV đi vòng quanh các nhóm, hướng dẫn cách ngắm ống hút sao cho đỉnh cột cờ nằm đúng giữa tâm ống, đọc vạch dây dọi chỉ trên thước đo độ.

## C. HOẠT ĐỘNG 3: TÍNH TOÁN XỬ LÝ SỐ LIỆU VÀ BÁO CÁO KẾT QUẢ (30 phút)
### Hoạt động 3.1: Xử lý số liệu và tính toán bằng máy tính cầm tay (15 phút)
a) Mục tiêu: Tính góc trung bình $\\bar{\\alpha}$, khoảng cách trung bình $\\bar{d}$ và tính ra chiều cao cột cờ.
b) Nội dung: Các nhóm tập trung tại lớp học, sử dụng máy tính bấm công thức và tính sai số.
c) Sản phẩm: Bản báo cáo kết quả đo đạc hoàn chỉnh của nhóm.
d) Tổ chức thực hiện: Học sinh làm việc nhóm, điền kết quả vào bảng báo cáo.

### Hoạt động 3.2: Thuyết trình và đối chiếu kết quả thực nghiệm (15 phút)
a) Mục tiêu: Đại diện các nhóm báo cáo kết quả và giải thích nguyên nhân chênh lệch sai số giữa các nhóm.
b) Nội dung: 4 nhóm dán bảng báo cáo lên bảng lớp, so sánh kết quả với chiều cao thực tế của cột cờ trường do Ban giám hiệu cung cấp.
c) Sản phẩm: Điểm số đánh giá hoạt động trải nghiệm STEM của các nhóm.
d) Tổ chức thực hiện: GV công bố chiều cao thật của cột cờ (ví dụ $10{,}5\\text{ m}$). Nhóm nào có sai số dưới $5\\%$ được tuyên dương đạt chuẩn xuất sắc.

## D. HOẠT ĐỘNG 4: VẬN DỤNG VÀ ĐÁNH GIÁ (10 phút)
- **Tích hợp NLS 3.1.TC2a:** GV hướng dẫn học sinh tải ứng dụng Clinometer trên điện thoại di động thông minh: Đặt cạnh điện thoại ngắm theo đỉnh vật thể, cảm biến gia tốc kế của điện thoại sẽ đo góc nghiêng tức thì với độ chính xác cao đến từng phút. Dặn dò học sinh tự đo chiều cao cây xanh hoặc ban công nhà mình vào dịp cuối tuần.
"""

tasks = [
    ("08_KHBD_Toan9_HinhHoc_Bai16_ViTriTuongDoiDuongThangDuongTron_Tiet19-20.md", md_08),
    ("09_KHBD_Toan9_HinhHoc_Bai17_ViTriTuongDoiHaiDuongTron_Tiet21-22.md", md_09),
    ("10_KHBD_Toan9_HinhHoc_LuyenTapChung_Tiet23.md", md_10),
    ("11_KHBD_Toan9_HinhHoc_BaiTapCuoiChuong5_Tiet24-25.md", md_11),
    ("12_KHBD_Toan9_HinhHoc_OnTapCuoiHK1_Tiet26-27.md", md_12),
    ("13_KHBD_Toan9_HinhHoc_KiemTraCuoiHK1_Tiet28.md", md_13),
    ("14_KHBD_Toan9_HinhHoc_HDTN_TinhChieuCaoKhoangCach_STEM_Tiet29-30.md", md_14),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo: {filename}")
