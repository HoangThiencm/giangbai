# -*- coding: utf-8 -*-
"""
Script sinh 9 KHBD Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp (Tiết 31 - 46) - Toán 9 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan9"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    # 24: Bài 27 (Tiết 31-32)
    {
        "filename": "24_KHBD_Toan9_Bai27_GocNoiTiep_Tiet31-32.md",
        "md": """TIẾT 31, 32 - BÀI 27: GÓC NỘI TIẾP
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa góc nội tiếp: Góc có đỉnh nằm trên đường tròn và hai cạnh chứa hai dây cung của đường tròn đó.
- Nắm vững định lí về số đo của góc nội tiếp: Trong một đường tròn, số đo của góc nội tiếp bằng nửa số đo của cung bị chắn: $\\widehat{BAC} = \\frac{1}{2} \\text{sđ}\\overparen{BC}$.
- Nắm vững các hệ quả quan trọng của góc nội tiếp:
  + Trong một đường tròn, các góc nội tiếp cùng chắn một cung hoặc chắn các cung bằng nhau thì bằng nhau.
  + Góc nội tiếp (nhỏ hơn hoặc bằng $90^\\circ$) có số đo bằng nửa số đo của góc ở tâm cùng chắn một cung.
  + Góc nội tiếp chắn nửa đường tròn là góc vuông ($90^\\circ$).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự vẽ hình chính xác bằng compa và thước kẻ, đo góc kiểm chứng định lí.
- Giao tiếp và hợp tác: Làm việc nhóm chứng minh định lí trong trường hợp tâm $O$ nằm trên một cạnh của góc.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng suy luận logic, vận dụng tính chất tam giác cân có đỉnh tại tâm $O$.
- Năng lực giải quyết vấn đề toán học: Tính số đo các góc và cung bị chắn trong đường tròn.

## 3. Về phẩm chất
- Rèn tính cẩn thận, vẽ hình chính xác và rõ ràng.
- Say mê khám phá các quy luật hình học tròn xoay.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2 Kết nối tri thức, KHBD, compa, thước đo góc bảng, máy chiếu.
2. Học sinh: SGK, compa, thước kẻ, thước đo góc, vở ghi.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại góc ở tâm và đặt vấn đề về góc có đỉnh nằm trên đường tròn.
b) Nội dung: Góc ở tâm có đỉnh tại tâm $O$. Nếu đỉnh của góc di chuyển ra nằm trên đường tròn thì góc đó có tên gọi là gì và số đo liên hệ thế nào với cung bị chắn?
c) Sản phẩm: Dự đoán của HS về góc nội tiếp và số đo bằng nửa góc ở tâm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình vẽ góc $\\widehat{BOC}$ (góc ở tâm) và góc $\\widehat{BAC}$ có đỉnh $A$ nằm trên đường tròn $(O)$. Hỏi tên gọi và mối liên hệ số đo giữa chúng.<br>- **HS:** Quan sát hình vẽ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh theo cặp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đỉnh $A$ nằm trên đường tròn, số đo góc $A$ nhỏ hơn góc ở tâm $O$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Góc $\\widehat{BAC}$ gọi là góc nội tiếp của đường tròn $(O)$. Bài học hôm nay ta nghiên cứu định lí và các tính chất của góc nội tiếp. | Đặt vấn đề: Định nghĩa và tính chất của góc nội tiếp trong đường tròn. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Định nghĩa góc nội tiếp và Định lí số đo (35 phút)
a) Mục tiêu: Nắm vững định nghĩa góc nội tiếp và định lí số đo bằng nửa số đo cung bị chắn.
b) Nội dung: Khái niệm góc nội tiếp, cung bị chắn và chứng minh định lí trong trường hợp tâm $O$ nằm trên cạnh góc.
c) Sản phẩm: Vở ghi bài và hình vẽ chứng minh trường hợp 1.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Góc nội tiếp là góc có đỉnh nằm trên đường tròn và hai cạnh chứa hai dây cung. Cung nằm bên trong góc gọi là cung bị chắn.<br>Phát biểu định lí: Trong một đường tròn, số đo của góc nội tiếp bằng nửa số đo của cung bị chắn:<br>$$\\widehat{BAC} = \\frac{1}{2} \\text{sđ}\\overparen{BC}$$<br>- **HS:** Vẽ hình và ghi nhớ định nghĩa.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Chứng minh trường hợp $O$ thuộc cạnh $AC$: Tam giác $OAB$ cân tại $O$ ($OA = OB = R$) nên $\\widehat{OBA} = \\widehat{OAB}$. Góc ở tâm $\\widehat{BOC}$ là góc ngoài tại đỉnh $O$ của $\\Delta OAB$ nên $\\widehat{BOC} = \\widehat{OAB} + \\widehat{OBA} = 2\\widehat{BAC}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Suy ra $\\widehat{BAC} = \\frac{1}{2} \\widehat{BOC} = \\frac{1}{2} \\text{sđ}\\overparen{BC}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và chốt định lí cho cả 3 trường hợp ($O$ nằm trên cạnh, $O$ nằm trong góc, $O$ nằm ngoài góc). | **1. Định nghĩa và Định lí:**<br>- Định nghĩa: Góc có đỉnh trên đường tròn, 2 cạnh chứa 2 dây cung.<br>- Định lí: Trong một đường tròn, số đo góc nội tiếp bằng nửa số đo cung bị chắn:<br>$$\\widehat{BAC} = \\frac{1}{2} \\text{sđ}\\overparen{BC}$$ |

### Hoạt động 2.2: Các hệ quả của góc nội tiếp (30 phút)
a) Mục tiêu: Nắm vững và áp dụng 4 hệ quả của góc nội tiếp (đặc biệt góc chắn nửa đường tròn là góc vuông).
b) Nội dung: Phát biểu các hệ quả và giải thích hệ quả góc vuông.
c) Sản phẩm: Bảng hệ quả trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu 4 hệ quả trong một đường tròn:<br>a) Các góc nội tiếp cùng chắn một cung hoặc chắn các cung bằng nhau thì bằng nhau.<br>b) Các góc nội tiếp bằng nhau thì chắn các cung bằng nhau.<br>c) Góc nội tiếp ($\\le 90^\\circ$) có số đo bằng nửa góc ở tâm cùng chắn một cung.<br>d) Góc nội tiếp chắn nửa đường tròn là góc vuông ($90^\\circ$).<br>- **HS:** Ghi chép và vẽ hình minh họa.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giải thích vì sao góc chắn nửa đường tròn bằng $90^\\circ$: Vì cung nửa đường tròn có số đo $180^\\circ$, nên góc nội tiếp chắn nó bằng $\\frac{1}{2} \\cdot 180^\\circ = 90^\\circ$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Hệ quả góc vuông là công cụ cực kì quan trọng để chứng minh tam giác vuông và tiếp tuyến. | **2. Các hệ quả:**<br>- Các góc nội tiếp cùng chắn một cung thì bằng nhau.<br>- Góc nội tiếp chắn nửa đường tròn là góc vuông:<br>Cho $AB$ là đường kính của $(O)$, điểm $C \\in (O)$ ($C \\neq A, B$). Khi đó $\\widehat{ACB} = 90^\\circ$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Vận dụng hệ quả góc nội tiếp tính số đo góc và chứng minh tam giác vuông.
b) Nội dung: Cho đường tròn $(O)$, đường kính $AB$. Lấy điểm $C$ trên $(O)$ sao cho $\\widehat{CAB} = 30^\\circ$.
1) Tính số đo góc $\\widehat{ACB}$ và $\\widehat{ABC}$.
2) Tính số đo cung nhỏ $\\overparen{AC}$ và cung nhỏ $\\overparen{BC}$.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập tính góc và số đo cung với hình vẽ đường kính $AB$.<br>- **HS:** Vẽ hình vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vì $AB$ là đường kính nên $\\widehat{ACB} = 90^\\circ$ (góc nội tiếp chắn nửa đường tròn).<br>Trong $\\Delta ABC$ vuông tại $C$: $\\widehat{ABC} = 90^\\circ - 30^\\circ = 60^\\circ$.<br>Số đo cung nhỏ $\\overparen{BC} = 2\\widehat{CAB} = 2 \\cdot 30^\\circ = 60^\\circ$.<br>Số đo cung nhỏ $\\overparen{AC} = 2\\widehat{ABC} = 2 \\cdot 60^\\circ = 120^\\circ$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán tính góc và cung căn bản. | **Bài giải:**<br>1) Vì $AB$ là đường kính của $(O)$ nên:<br>$$\\widehat{ACB} = 90^\\circ\\text{ (góc nội tiếp chắn nửa đường tròn)}$$<br>Xét $\\Delta ABC$ vuông tại $C$, ta có:<br>$$\\widehat{ABC} = 90^\\circ - \\widehat{CAB} = 90^\\circ - 30^\\circ = 60^\\circ$$<br><br>2) Theo định lí góc nội tiếp:<br>$$\\text{sđ}\\overparen{BC} = 2\\widehat{CAB} = 2 \\cdot 30^\\circ = 60^\\circ$$<br>$$\\text{sđ}\\overparen{AC} = 2\\widehat{ABC} = 2 \\cdot 60^\\circ = 120^\\circ$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng tính chất góc vuông chắn nửa đường tròn xác định tâm đường tròn khi chỉ có eke.
b) Nội dung: Làm thế nào để tìm tâm của một chiếc đĩa tròn chỉ bằng một chiếc eke học sinh?
c) Sản phẩm: Đặt đỉnh góc vuông của eke lên mép đĩa, hai cạnh eke cắt mép đĩa tại hai điểm, nối hai điểm đó được một đường kính. Lặp lại với vị trí khác, giao điểm hai đường kính là tâm đĩa.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đố vui: Tìm tâm đĩa tròn bằng eke góc vuông.<br>- **HS:** Suy nghĩ ứng dụng góc nội tiếp $90^\\circ$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đặt góc vuông eke vào đường tròn, dây nối hai đầu cạnh eke chính là đường kính.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giao điểm 2 đường kính là tâm đường tròn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò chuẩn bị bài Đường tròn ngoại tiếp/nội tiếp tam giác. | Ứng dụng thực tế: Xác định tâm đường tròn bằng thước eke vuông. |
"""
    },

    # 25: Bài 28 (Tiết 33-34)
    {
        "filename": "25_KHBD_Toan9_Bai28_DuongTronNgoaiTiepVaNoiTiepTamGiac_Tiet33-34.md",
        "md": """TIẾT 33, 34 - BÀI 28: ĐƯỜNG TRÒN NGOẠI TIẾP VÀ ĐƯỜNG TRÒN NỘI TIẾP CỦA MỘT TAM GIÁC
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa đường tròn ngoại tiếp tam giác: Đường tròn đi qua cả ba đỉnh của tam giác. Tâm là giao điểm của ba đường trung trực của tam giác.
- Nắm vững công thức bán kính đường tròn ngoại tiếp tam giác đều cạnh $a$: $R = \\frac{a\\sqrt{3}}{3}$; tam giác vuông có cạnh huyền $c$: $R = \\frac{c}{2}$.
- Nhận biết định nghĩa đường tròn nội tiếp tam giác: Đường tròn tiếp xúc với cả ba cạnh của tam giác. Tâm là giao điểm của ba đường phân giác trong của tam giác.
- Nắm vững công thức bán kính đường tròn nội tiếp tam giác đều cạnh $a$: $r = \\frac{a\\sqrt{3}}{6}$; tam giác bất kì: $r = \\frac{S}{p}$ ($S$ là diện tích, $p$ là nửa chu vi).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự sử dụng compa dựng đường trung trực và đường phân giác để xác định tâm ngoại tiếp, nội tiếp.
- Giao tiếp và hợp tác: Cùng nhóm so sánh tâm đường tròn ngoại tiếp và nội tiếp trong tam giác đều (chúng trùng nhau tại trọng tâm).

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Suy luận mối quan hệ $R = 2r$ trong tam giác đều.
- Năng lực giải quyết vấn đề toán học: Tính bán kính $R$ và $r$ của tam giác vuông và tam giác đều.

## 3. Về phẩm chất
- Rèn luyện kỹ năng vẽ hình bằng compa chính xác, nét vẽ sắc sảo, sạch đẹp.
- Say mê khám phá vẻ đẹp đối xứng tuyệt hảo của tam giác đều nội tiếp, ngoại tiếp đường tròn.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, compa bảng, thước kẻ, máy chiếu.
2. Học sinh: SGK, compa, thước kẻ, vở ghi.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại tính chất giao điểm ba đường trung trực và ba đường phân giác của tam giác đã học ở lớp 7.
b) Nội dung: Điểm cách đều 3 đỉnh của tam giác là giao điểm của 3 đường gì? Điểm cách đều 3 cạnh của tam giác là giao điểm của 3 đường gì?
c) Sản phẩm: Cách đều 3 đỉnh: Giao 3 đường trung trực; Cách đều 3 cạnh: Giao 3 đường phân giác.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi nhắc lại kiến thức đường trung trực và phân giác tam giác.<br>- **HS:** Xung phong trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trung trực cách đều 3 đỉnh, phân giác cách đều 3 cạnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Điểm cách đều 3 đỉnh là tâm đường tròn đi qua 3 đỉnh (đường tròn ngoại tiếp). Điểm cách đều 3 cạnh là tâm đường tròn tiếp xúc 3 cạnh (đường tròn nội tiếp). | Dẫn nhập vào khái niệm đường tròn ngoại tiếp và nội tiếp tam giác. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Đường tròn ngoại tiếp tam giác (35 phút)
a) Mục tiêu: Nắm vững định nghĩa, cách xác định tâm, bán kính $R$ cho tam giác thường, tam giác vuông và tam giác đều.
b) Nội dung: Định nghĩa, dựng hình và các công thức tính $R$.
c) Sản phẩm: Vở ghi bài định nghĩa và hình vẽ dựng đường tròn ngoại tiếp.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Đường tròn đi qua ba đỉnh của một tam giác gọi là đường tròn ngoại tiếp tam giác, tam giác gọi là tam giác nội tiếp đường tròn.<br>- Tâm $O$: Giao điểm của ba đường trung trực của tam giác.<br>- Bán kính $R = OA = OB = OC$.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Xác định tâm $O$ và bán kính $R$ khi:<br>1) $\\Delta ABC$ vuông tại $A$: Tâm $O$ là trung điểm cạnh huyền $BC$, $R = \\frac{BC}{2}$.<br>2) $\\Delta ABC$ đều cạnh $a$: Tâm $O$ trùng với trọng tâm, $R = \\frac{2}{3} h = \\frac{2}{3} \\cdot \\frac{a\\sqrt{3}}{2} = \\frac{a\\sqrt{3}}{3}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng dùng compa dựng đường tròn ngoại tiếp tam giác vuông.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt vị trí tâm ngoại tiếp đối với tam giác nhọn (nằm trong), tam giác vuông (trên cạnh huyền), tam giác tù (nằm ngoài tam giác). | **1. Đường tròn ngoại tiếp tam giác:**<br>- Đi qua 3 đỉnh của tam giác.<br>- Tâm: Giao điểm 3 đường trung trực.<br>- Tam giác vuông: Tâm là trung điểm cạnh huyền, $R = \\frac{c}{2}$.<br>- Tam giác đều cạnh $a$: $R = \\frac{a\\sqrt{3}}{3}$. |

### Hoạt động 2.2: Đường tròn nội tiếp tam giác (30 phút)
a) Mục tiêu: Nắm vững định nghĩa, cách xác định tâm $I$, bán kính $r$ cho tam giác thường, tam giác đều và công thức $S = p \\cdot r$.
b) Nội dung: Định nghĩa, dựng đường phân giác và công thức tính $r$.
c) Sản phẩm: Vở ghi bài và hình vẽ dựng đường tròn nội tiếp tam giác.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Đường tròn tiếp xúc với ba cạnh của tam giác gọi là đường tròn nội tiếp tam giác, tam giác gọi là tam giác ngoại tiếp đường tròn.<br>- Tâm $I$: Giao điểm ba đường phân giác trong của tam giác.<br>- Bán kính $r$: Khoảng cách từ tâm $I$ đến một cạnh.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Với $\\Delta ABC$ đều cạnh $a$: Tâm $I$ trùng tâm $O$ ngoại tiếp, $r = \\frac{1}{3} h = \\frac{a\\sqrt{3}}{6}$.<br>Nhận xét: $R = 2r$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng dựng đường tròn nội tiếp tam giác đều.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Trong tam giác đều, tâm đường tròn ngoại tiếp và nội tiếp trùng nhau tại một điểm. | **2. Đường tròn nội tiếp tam giác:**<br>- Tiếp xúc với 3 cạnh của tam giác.<br>- Tâm $I$: Giao điểm 3 đường phân giác trong.<br>- Bán kính $r = \\frac{S}{p}$ ($S$ là diện tích, $p$ là nửa chu vi).<br>- Tam giác đều cạnh $a$: $r = \\frac{a\\sqrt{3}}{6}$. Ta có $R = 2r$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Tính bán kính đường tròn ngoại tiếp và nội tiếp của một tam giác vuông.
b) Nội dung: Cho tam giác $ABC$ vuông tại $A$ có $AB = 6\\text{ cm}, AC = 8\\text{ cm}$.
1) Tính bán kính $R$ của đường tròn ngoại tiếp $\\Delta ABC$.
2) Tính diện tích $S$ và nửa chu vi $p$, từ đó tính bán kính $r$ của đường tròn nội tiếp $\\Delta ABC$.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập tính $R$ và $r$ cho tam giác vuông $6, 8, 10\\text{ cm}$.<br>- **HS:** Tính cạnh huyền $BC = 10\\text{ cm}$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $R = \\frac{BC}{2} = 5\\text{ cm}$.<br>$S = \\frac{1}{2} \\cdot 6 \\cdot 8 = 24\\text{ cm}^2$.<br>Nửa chu vi: $p = \\frac{6 + 8 + 10}{2} = 12\\text{ cm}$.<br>Bán kính nội tiếp: $r = \\frac{S}{p} = \\frac{24}{12} = 2\\text{ cm}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, lưu ý công thức nhanh cho tam giác vuông: $r = \\frac{a + b - c}{2} = \\frac{6 + 8 - 10}{2} = 2\\text{ cm}$. | **Bài giải:**<br>1) Áp dụng định lí Pythagore: $BC = \\sqrt{6^2 + 8^2} = 10\\text{ (cm)}$.<br>Bán kính đường tròn ngoại tiếp $\\Delta ABC$ là:<br>$$R = \\frac{BC}{2} = \\frac{10}{2} = 5\\text{ (cm)}$$<br><br>2) Diện tích tam giác là:<br>$$S = \\frac{1}{2} AB \\cdot AC = \\frac{1}{2} \\cdot 6 \\cdot 8 = 24\\text{ (cm}^2\\text{)}$$<br>Nửa chu vi tam giác là:<br>$$p = \\frac{6 + 8 + 10}{2} = 12\\text{ (cm)}$$<br>Bán kính đường tròn nội tiếp $\\Delta ABC$ là:<br>$$r = \\frac{S}{p} = \\frac{24}{12} = 2\\text{ (cm)}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tính tỉ số diện tích hình tròn ngoại tiếp và hình tròn nội tiếp của tam giác đều.
b) Nội dung: Tính tỉ số $\\frac{S_{(O; R)}}{S_{(I; r)}}$ của tam giác đều cạnh $a$.
c) Sản phẩm: Kết quả $\\frac{\\pi R^2}{\\pi r^2} = \\left(\\frac{R}{r}\\right)^2 = 2^2 = 4$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tam giác đều có $R = 2r$. Diện tích hình tròn ngoại tiếp gấp mấy lần hình tròn nội tiếp?<br>- **HS:** Tính tỉ số diện tích.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tỉ số bằng $2^2 = 4$ lần.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò chuẩn bị cho tiết Luyện tập chung. | Diện tích hình tròn ngoại tiếp tam giác đều gấp 4 lần diện tích hình tròn nội tiếp. |
"""
    },

    # 26: Tiết 35-36: Luyện tập chung (Mindmap: mindmap_toan9_hinh_tiet35_36.png)
    {
        "filename": "26_KHBD_Toan9_LuyenTapChung_Tiet35-36.md",
        "md": """TIẾT 35, 36 - LUYỆN TẬP CHUNG: GÓC NỘI TIẾP VÀ ĐƯỜNG TRÒN NGOẠI TIẾP, NỘI TIẾP TAM GIÁC
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và rèn luyện thành thạo kỹ năng:
  + Vận dụng định lí và các hệ quả của góc nội tiếp để chứng minh các góc bằng nhau, tính số đo góc và chứng minh các tam giác đồng dạng.
  + Nhận biết góc nội tiếp chắn nửa đường tròn là góc vuông để chứng minh vuông góc và tam giác vuông.
  + Xác định tâm và tính bán kính đường tròn ngoại tiếp, đường tròn nội tiếp của tam giác vuông và tam giác đều.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa kiến thức góc nội tiếp và đường tròn tam giác bằng sơ đồ tư duy.
- Giao tiếp và hợp tác: Làm việc nhóm giải quyết bài toán hình học tổng hợp nhiều bước.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng nhìn nhận hình vẽ, khai thác các cung bị chắn để liên kết các góc bằng nhau.
- Năng lực giải quyết vấn đề toán học: Trình bày bài toán hình học chặt chẽ, mạch lạc.

## 3. Về phẩm chất
- Cẩn thận, tỉ mỉ khi vẽ hình bằng compa và thước kẻ.
- Tự giác, tích cực tham gia xây dựng bài học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI, máy chiếu, bảng phụ ghi bài tập.
2. Học sinh: SGK, vở ghi, compa, thước kẻ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại các tính chất cốt lõi của góc nội tiếp và đường tròn ngoại tiếp.
b) Nội dung: Trả lời nhanh: Góc nội tiếp chắn nửa đường tròn bằng bao nhiêu độ? Bán kính ngoại tiếp tam giác vuông tính thế nào?
c) Sản phẩm: Bằng $90^\\circ$; Bán kính bằng nửa cạnh huyền.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu 2 câu hỏi khởi động nhanh.<br>- **HS:** Xung phong trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc nhanh các tính chất.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá đúng và chuyển sang sơ đồ tư duy. | Tái hiện các tính chất cốt lõi của bài 27 và bài 28. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (25 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức bằng sơ đồ tư duy (25 phút)
a) Mục tiêu: Khái quát hóa toàn bộ kiến thức Bài 27 và Bài 28 bằng sơ đồ tư duy trực quan 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI Góc nội tiếp & Đường tròn tam giác.
c) Sản phẩm: Sơ đồ tư duy được hệ thống trong vở của học sinh.

![Sơ đồ tư duy Luyện tập chung Góc nội tiếp và Đường tròn tam giác Tiết 35 - 36](khbd-ill:mindmap-toan9-hinh-tiet35-36)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI Góc nội tiếp và Đường tròn tam giác. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 4 nhánh:<br>1) Góc nội tiếp (định lí số đo, góc chắn nửa đường tròn vuông).<br>2) Tính chất cùng chắn (các góc cùng chắn 1 cung thì bằng nhau).<br>3) Đường tròn ngoại tiếp tam giác (tâm là giao 3 trung trực, tam giác vuông, tam giác đều).<br>4) Đường tròn nội tiếp tam giác (tâm là giao 3 phân giác, $r = \\frac{S}{p}$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS phân tích mối quan hệ giữa các nhánh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại kiến thức trọng tâm và các lưu ý khi chứng minh hình học. | **Hệ thống kiến thức trọng tâm:**<br>1. Góc nội tiếp: $\\widehat{BAC} = \\frac{1}{2} \\text{sđ}\\overparen{BC}$. Góc chắn nửa đường tròn bằng $90^\\circ$.<br>2. Cùng chắn một cung thì bằng nhau.<br>3. Ngoại tiếp: Giao 3 trung trực. Tam giác vuông có $R = \\frac{c}{2}$.<br>4. Nội tiếp: Giao 3 phân giác, $r = \\frac{S}{p}$. Tam giác đều có $R = 2r$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
a) Mục tiêu: Giải bài toán hình học tổng hợp về đường kính và góc nội tiếp.
b) Nội dung: Cho tam giác $ABC$ có ba góc nhọn nội tiếp đường tròn $(O)$. Kẻ đường kính $AD$. Kẻ đường cao $AH$ của $\\Delta ABC$ ($H \\in BC$).
1) Chứng minh $\\Delta ABH \\backsim \\Delta ADC$.
2) Chứng minh $AB \\cdot AC = AH \\cdot AD$.
3) Gọi $M$ là trung điểm của $BC$. Chứng minh $OM \\parallel AH$ và suy ra tính chất đường nối tâm.
c) Sản phẩm: Lời giải hoàn chỉnh 3 câu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập hình học tổng hợp với đường kính $AD$.<br>- **HS:** Vẽ hình cẩn thận bằng compa và thước kẻ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:**<br>1) Vì $AD$ là đường kính nên $\\widehat{ACD} = 90^\\circ$ (góc nội tiếp chắn nửa đường tròn).<br>Xét $\\Delta ABH$ (vuông tại $H$) và $\\Delta ADC$ (vuông tại $C$) có: $\\widehat{ABH} = \\widehat{ADC}$ (hai góc nội tiếp cùng chắn cung $\\overparen{AC}$).<br>Do đó $\\Delta ABH \\backsim \\Delta ADC$ (góc nhọn).<br>2) Suy ra $\\frac{AB}{AD} = \\frac{AH}{AC} \\Rightarrow AB \\cdot AC = AH \\cdot AD$.<br>3) Kẻ đường trung trực $OM \\perp BC$. Vì $AH \\perp BC$ nên $OM \\parallel AH$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán hệ thức $AB \\cdot AC = 2R \\cdot AH$ kinh điển trong hình học 9. | **Bài giải:**<br>1) Vì $AD$ là đường kính của $(O)$ nên:<br>$$\\widehat{ACD} = 90^\\circ\\text{ (góc nội tiếp chắn nửa đường tròn)}$$<br>Xét $\\Delta ABH$ (vuông tại $H$) và $\\Delta ADC$ (vuông tại $C$) có:<br>$$\\widehat{ABH} = \\widehat{ADC}\\text{ (hai góc nội tiếp cùng chắn }\\overparen{AC}\\text{)}$$<br>Do đó $\\Delta ABH \\backsim \\Delta ADC$ (góc nhọn).<br><br>2) Vì $\\Delta ABH \\backsim \\Delta ADC$ nên:<br>$$\\frac{AB}{AD} = \\frac{AH}{AC} \\Rightarrow AB \\cdot AC = AH \\cdot AD$$<br>(Nếu $AD = 2R$ thì $AB \\cdot AC = 2R \\cdot AH$).<br><br>3) Vì $M$ là trung điểm của dây $BC$ nên $OM \\perp BC$ (đường kính đi qua trung điểm dây không đi qua tâm).<br>Mặt khác $AH \\perp BC$ (theo giả thiết).<br>Do đó $OM \\parallel AH$ (vì cùng vuông góc với $BC$). |

## D. VẬN DỤNG VÀ DẶN DÒ (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Chuẩn bị cho bài học Tứ giác nội tiếp quan trọng bậc nhất của hình học 9.
b) Nội dung: Xem trước khái niệm tứ giác nội tiếp và dấu hiệu tổng hai góc đối diện.
c) Sản phẩm: HS ghi nhận nhiệm vụ tự học ở nhà.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò xem trước Bài 29: Tứ giác nội tiếp.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc lướt SGK bài 29.<br><br>**+ Bước 3: Kết thúc buổi học**<br>- Cả lớp chào giáo viên. | Dặn dò chuẩn bị bài Tứ giác nội tiếp. |
"""
    },

    # 27: Bài 29 (Tiết 37-38)
    {
        "filename": "27_KHBD_Toan9_Bai29_TuGiacNoiTiep_Tiet37-38.md",
        "md": """TIẾT 37, 38 - BÀI 29: TỨ GIÁC NỘI TIẾP
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa tứ giác nội tiếp: Tứ giác có bốn đỉnh cùng nằm trên một đường tròn gọi là tứ giác nội tiếp đường tròn (đường tròn gọi là đường tròn ngoại tiếp tứ giác).
- Nắm vững định lí thuận: Trong một tứ giác nội tiếp, tổng số đo hai góc đối diện bằng $180^\\circ$: $\\widehat{A} + \\widehat{C} = 180^\\circ;\\; \\widehat{B} + \\widehat{D} = 180^\\circ$.
- Nắm vững các dấu hiệu nhận biết tứ giác nội tiếp kinh điển:
  + Dấu hiệu 1: Tứ giác có tổng hai góc đối diện bằng $180^\\circ$.
  + Dấu hiệu 2: Tứ giác có góc ngoài tại một đỉnh bằng góc trong của đỉnh đối diện.
  + Dấu hiệu 3: Tứ giác có hai đỉnh kề nhau cùng nhìn cạnh chứa hai đỉnh còn lại dưới hai góc bằng nhau.
  + Dấu hiệu 4: Tứ giác có bốn đỉnh cùng cách đều một điểm $O$.
- Vận dụng các dấu hiệu để chứng minh một tứ giác nội tiếp đường tròn.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác vẽ hình chính xác, phát hiện các góc vuông và góc bằng nhau trên hình vẽ.
- Giao tiếp và hợp tác: Làm việc nhóm phân tích các hướng tiếp cận chứng minh tứ giác nội tiếp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng suy luận logic, vận dụng nhuần nhuyễn tính chất góc nội tiếp.
- Năng lực giải quyết vấn đề toán học: Giải các bài toán hình học trọng tâm trong các đề thi tuyển sinh vào lớp 10.

c) Năng lực số (NLS) và AI:
- ***3.1.TC2a: HS sử dụng phần mềm GeoGebra để vẽ hình chính xác và sơ đồ hóa các tính chất hình học bài Tứ giác; 9.D1.1: Sử dụng AI gợi ý các dấu hiệu nhận biết tứ giác nội tiếp cho bài toán cụ thể (Áp dụng: tiết 1, 2).***

## 3. Về phẩm chất
- Rèn luyện tính kiên nhẫn, tư duy cẩn trọng, không ngộ nhận hình vẽ.
- Tinh thần vượt khó khi đối diện bài toán hình học phẳng phức tạp.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, compa, thước kẻ, phần mềm GeoGebra minh họa 4 đỉnh trên đường tròn, máy chiếu.
2. Học sinh: SGK, compa, thước kẻ, máy tính cầm tay, vở ghi.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kích hoạt tư duy: Liệu mọi tứ giác có đường tròn đi qua 4 đỉnh như tam giác không?
b) Nội dung: Vẽ một hình vuông, một hình chữ nhật, một hình bình hành. Hình nào có một đường tròn đi qua cả 4 đỉnh?
c) Sản phẩm: HS nhận xét: Hình vuông và hình chữ nhật luôn có đường tròn đi qua 4 đỉnh, hình bình hành (không phải chữ nhật) thì không.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Mọi tam giác đều có đường tròn ngoại tiếp. Vậy mọi tứ giác có đường tròn ngoại tiếp không?<br>- **HS:** Thử nghiệm vẽ hình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hình chữ nhật có giao điểm 2 đường chéo cách đều 4 đỉnh nên có đường tròn đi qua 4 đỉnh. Hình thoi hay hình bình hành nói chung thì không.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tứ giác có 4 đỉnh cùng nằm trên một đường tròn gọi là tứ giác nội tiếp. Bài học hôm nay ta nghiên cứu điều kiện để một tứ giác là tứ giác nội tiếp. | Đặt vấn đề: Điều kiện để một tứ giác nội tiếp đường tròn. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Định nghĩa và Định lí tổng hai góc đối (35 phút)
a) Mục tiêu: Nắm vững định nghĩa tứ giác nội tiếp và định lí tổng hai góc đối diện bằng $180^\\circ$.
b) Nội dung: Khái niệm tứ giác nội tiếp; chứng minh định lí bằng góc nội tiếp.
c) Sản phẩm: Vở ghi bài định nghĩa và lời giải chứng minh định lí.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Một tứ giác có bốn đỉnh cùng nằm trên một đường tròn được gọi là tứ giác nội tiếp đường tròn.<br>Phát biểu định lí: Trong một tứ giác nội tiếp, tổng số đo hai góc đối diện bằng $180^\\circ$:<br>$$\\widehat{A} + \\widehat{C} = 180^\\circ;\\quad \\widehat{B} + \\widehat{D} = 180^\\circ$$<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Chứng minh: $\\widehat{A} = \\frac{1}{2} \\text{sđ}\\overparen{BCD}$, $\\widehat{C} = \\frac{1}{2} \\text{sđ}\\overparen{BAD}$.<br>Cộng lại: $\\widehat{A} + \\widehat{C} = \\frac{1}{2} (\\text{sđ}\\overparen{BCD} + \\text{sđ}\\overparen{BAD}) = \\frac{1}{2} \\cdot 360^\\circ = 180^\\circ$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chứng minh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và chốt định lí. | **1. Định nghĩa và Định lí:**<br>- Định nghĩa: Tứ giác có 4 đỉnh nằm trên một đường tròn gọi là tứ giác nội tiếp.<br>- Định lí thuận: Trong tứ giác nội tiếp, tổng hai góc đối diện bằng $180^\\circ$:<br>$$\\widehat{A} + \\widehat{C} = 180^\\circ;\\quad \\widehat{B} + \\widehat{D} = 180^\\circ$$ |

### Hoạt động 2.2: Bốn dấu hiệu nhận biết tứ giác nội tiếp (30 phút)
a) Mục tiêu: Nắm vững và phân biệt 4 dấu hiệu nhận biết tứ giác nội tiếp.
b) Nội dung: Phát biểu chi tiết 4 dấu hiệu và nhận diện qua các mô hình hình học.
c) Sản phẩm: Bảng 4 dấu hiệu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 4 dấu hiệu nhận biết tứ giác nội tiếp:<br>1) Tứ giác có tổng hai góc đối bằng $180^\\circ$ (phổ biến nhất: có 2 góc đối vuông $\\widehat{A} = \\widehat{C} = 90^\\circ$).<br>2) Tứ giác có góc ngoài tại một đỉnh bằng góc trong của đỉnh đối diện.<br>3) Tứ giác có hai đỉnh kề nhau cùng nhìn cạnh chứa hai đỉnh còn lại dưới hai góc bằng nhau (phổ biến: cùng nhìn dưới góc $90^\\circ$).<br>4) Tứ giác có 4 đỉnh cùng cách đều một điểm $O$.<br>- **HS:** Ghi chép và vẽ hình tương ứng với từng dấu hiệu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận dạng dấu hiệu khi hai đường cao tam giác cắt nhau.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu ví dụ các tứ giác nội tiếp tạo bởi hai đường cao.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Dấu hiệu 1 và dấu hiệu 3 là hai dấu hiệu chiếm tới $90\\%$ các bài thi vào 10. | **2. Bốn dấu hiệu nhận biết tứ giác nội tiếp:**<br>- Dấu hiệu 1: Tổng hai góc đối bằng $180^\\circ$ ($\\widehat{B} + \\widehat{D} = 180^\\circ$).<br>- Dấu hiệu 2: Góc ngoài tại một đỉnh bằng góc trong đỉnh đối diện.<br>- Dấu hiệu 3: Hai đỉnh kề cùng nhìn một đoạn thẳng dưới hai góc bằng nhau.<br>- Dấu hiệu 4: Bốn đỉnh cùng cách đều điểm $O$.<br>*Tích hợp NLS & AI:* Dùng GeoGebra vẽ hình động và tham khảo AI gợi ý hướng phân tích dấu hiệu. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Vận dụng dấu hiệu nhận biết chứng minh tứ giác nội tiếp trong bài toán hai đường cao.
b) Nội dung: Cho tam giác nhọn $ABC$, các đường cao $BD$ và $CE$ cắt nhau tại $H$.
1) Chứng minh tứ giác $ADHE$ nội tiếp đường tròn. Xác định tâm của đường tròn đó.
2) Chứng minh tứ giác $BCDE$ nội tiếp đường tròn.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập hình học kinh điển với 2 đường cao.<br>- **HS:** Vẽ hình cẩn thận vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:**<br>1) Tứ giác $ADHE$ có $\\widehat{ADH} = 90^\\circ$ (do $BD \\perp AC$) và $\\widehat{AEH} = 90^\\circ$ (do $CE \\perp AB$).<br>Tổng hai góc đối: $\\widehat{ADH} + \\widehat{AEH} = 90^\\circ + 90^\\circ = 180^\\circ$. Vậy $ADHE$ nội tiếp đường tròn đường kính $AH$ (tâm là trung điểm của $AH$).<br>2) Xét tứ giác $BCDE$ có: $\\widehat{BDC} = 90^\\circ$ và $\\widehat{BEC} = 90^\\circ$.<br>Hai đỉnh kề nhau $D$ và $E$ cùng nhìn cạnh $BC$ dưới góc $90^\\circ$. Do đó tứ giác $BCDE$ nội tiếp đường tròn đường kính $BC$ (tâm là trung điểm của $BC$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày 2 câu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa bài giải mẫu mực và phân biệt rõ hai dấu hiệu đã áp dụng. | **Bài giải:**<br>1) Vì $BD \\perp AC$ và $CE \\perp AB$ nên:<br>$$\\widehat{ADH} = 90^\\circ;\\quad \\widehat{AEH} = 90^\\circ$$<br>Xét tứ giác $ADHE$ có:<br>$$\\widehat{ADH} + \\widehat{AEH} = 90^\\circ + 90^\\circ = 180^\\circ$$<br>Mà hai góc này ở vị trí đối nhau.<br>Vậy tứ giác $ADHE$ nội tiếp đường tròn đường kính $AH$ (tâm là trung điểm của $AH$).<br><br>2) Xét tứ giác $BCDE$ có:<br>$$\\widehat{BDC} = \\widehat{BEC} = 90^\\circ$$<br>Mà hai đỉnh $D$ và $E$ là hai đỉnh kề nhau cùng nhìn cạnh $BC$ dưới góc $90^\\circ$.<br>Vậy tứ giác $BCDE$ nội tiếp đường tròn đường kính $BC$ (tâm là trung điểm của $BC$). |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Từ tứ giác $BCDE$ nội tiếp suy ra hai góc bằng nhau: $\\widehat{ADE} = \\widehat{ABC}$.
b) Nội dung: Chứng minh góc ngoài tại đỉnh $D$ của tứ giác nội tiếp $BCDE$ bằng góc trong đỉnh đối diện $B$.
c) Sản phẩm: Lời giải ngắn trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Vì sao từ tứ giác $BCDE$ nội tiếp suy ra ngay $\\widehat{ADE} = \\widehat{ABC}$?<br>- **HS:** Nhớ lại tính chất cùng bù với $\\widehat{EDC}$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $\\widehat{ADE} + \\widehat{EDC} = 180^\\circ$ (kề bù) và $\\widehat{ABC} + \\widehat{EDC} = 180^\\circ$ (hai góc đối). Suy ra $\\widehat{ADE} = \\widehat{ABC}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò chuẩn bị bài Đa giác đều tiếp theo. | Khai thác tính chất góc của tứ giác nội tiếp để suy ra góc bằng nhau. |
"""
    },

    # 28: Bài 30 (Tiết 39-40)
    {
        "filename": "28_KHBD_Toan9_Bai30_DaGiacDeu_Tiet39-40.md",
        "md": """TIẾT 39, 40 - BÀI 30: ĐA GIÁC ĐỀU
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa đa giác đều: Đa giác có tất cả các cạnh bằng nhau và tất cả các góc bằng nhau (tam giác đều, hình vuông, ngũ giác đều, lục giác đều, bát giác đều,...).
- Nắm vững công thức tính số đo mỗi góc của $n$-giác đều ($n \\ge 3$):
  $$\\alpha = \\frac{(n - 2) \\cdot 180^\\circ}{n}$$
- Nắm vững định lí về đường tròn ngoại tiếp và nội tiếp đa giác đều: Bất kì đa giác đều nào cũng có một và chỉ một đường tròn ngoại tiếp, một và chỉ một đường tròn nội tiếp. Tâm của hai đường tròn này trùng nhau và gọi là tâm của đa giác đều.
- Biết cách vẽ đa giác đều đơn giản (tam giác đều, hình vuông, lục giác đều) bằng compa và thước thẳng.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tính toán số đo góc của đa giác đều và thực hành vẽ lục giác đều bằng bán kính compa.
- Giao tiếp và hợp tác: Cùng nhóm tìm kiếm các hình ảnh đa giác đều trong tự nhiên và nghệ thuật (tổ ong hình lục giác, hoa tuyết, hoa văn thổ cẩm).

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng chia đa giác đều thành các tam giác cân bằng nhau có chung đỉnh tại tâm.
- Năng lực giải quyết vấn đề toán học: Tính cạnh, chu vi và diện tích của đa giác đều theo bán kính $R$.

## 3. Về phẩm chất
- Nâng cao cảm thụ thẩm mỹ về sự cân đối, hài hòa của các hình đa giác đều.
- Cẩn thận, tỉ mỉ khi sử dụng dụng cụ vẽ hình học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, compa, thước kẻ, máy chiếu trình chiếu hình ảnh tổ ong, gạch lát sàn đa giác đều.
2. Học sinh: SGK, compa, thước kẻ, máy tính cầm tay, vở ghi.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kích hoạt sự quan sát hình ảnh cấu trúc lục giác đều của tổ ong trong tự nhiên.
b) Nội dung: Vì sao loài ong lại xây tổ hình lục giác đều mà không phải hình vuông hay hình tam giác đều?
c) Sản phẩm: HS nhận xét: Hình lục giác đều ghép khít nhau không có khe hở và tiết kiệm sáp nhất, chứa được nhiều mật nhất.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh tổ ong và lát gạch lục giác. Hỏi: Đa giác này có đặc điểm gì đặc biệt?<br>- **HS:** Quan sát và liên hệ kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận theo cặp: Các cạnh bằng nhau và các góc bằng nhau.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Hình lục giác có các cạnh bằng nhau và các góc bằng nhau là một ví dụ về đa giác đều. Hôm nay ta tìm hiểu về đa giác đều. | Dẫn nhập vào khái niệm đa giác đều qua hình ảnh tổ ong tự nhiên. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Định nghĩa và Số đo góc của đa giác đều (35 phút)
a) Mục tiêu: Nắm vững định nghĩa và công thức tính số đo mỗi góc của $n$-giác đều.
b) Nội dung: Phát biểu định nghĩa; công thức $\\alpha = \\frac{(n - 2) \\cdot 180^\\circ}{n}$.
c) Sản phẩm: Bảng số đo góc của tam giác đều, hình vuông, ngũ giác đều, lục giác đều trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Đa giác đều là đa giác có tất cả các cạnh bằng nhau và tất cả các góc bằng nhau.<br>Tổng các góc của $n$-giác là $(n - 2) \\cdot 180^\\circ$. Do các góc bằng nhau nên số đo mỗi góc là:<br>$$\\alpha = \\frac{(n - 2) \\cdot 180^\\circ}{n}$$<br>- **HS:** Ghi chép công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính số đo mỗi góc của:<br>- Tam giác đều ($n = 3$): $\\frac{(3 - 2) \\cdot 180^\\circ}{3} = 60^\\circ$.<br>- Hình vuông ($n = 4$): $90^\\circ$.<br>- Ngũ giác đều ($n = 5$): $\\frac{3 \\cdot 180^\\circ}{5} = 108^\\circ$.<br>- Lục giác đều ($n = 6$): $\\frac{4 \\cdot 180^\\circ}{6} = 120^\\circ$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa bảng số đo góc của các đa giác đều quen thuộc. | **1. Định nghĩa và Số đo góc:**<br>- Đa giác đều: Các cạnh bằng nhau và các góc bằng nhau.<br>- Số đo mỗi góc của $n$-giác đều là:<br>$$\\alpha = \\frac{(n - 2) \\cdot 180^\\circ}{n}$$<br>- Ví dụ: Ngũ giác đều có góc $108^\\circ$, lục giác đều có góc $120^\\circ$. |

### Hoạt động 2.2: Đường tròn ngoại tiếp và nội tiếp đa giác đều (30 phút)
a) Mục tiêu: Hiểu định lí về tính đồng tâm của đường tròn ngoại tiếp và nội tiếp đa giác đều, biết cách vẽ lục giác đều bằng compa.
b) Nội dung: Phát biểu định lí; thực hành vẽ lục giác đều nội tiếp $(O; R)$ bằng cách giữ nguyên khẩu độ compa bằng $R$ chia đường tròn thành 6 cung bằng nhau.
c) Sản phẩm: Hình vẽ lục giác đều chuẩn xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định lí: Bất kì đa giác đều nào cũng có một và chỉ một đường tròn ngoại tiếp, một và chỉ một đường tròn nội tiếp. Tâm của hai đường tròn này trùng nhau gọi là tâm của đa giác đều.<br>Hướng dẫn cách vẽ lục giác đều:<br>- Vẽ đường tròn $(O; R)$.<br>- Giữ nguyên bán kính $R$ của compa, chấm liên tiếp 6 điểm trên đường tròn.<br>- Nối 6 điểm đó lại ta được lục giác đều.<br>- **HS:** Thực hành vẽ bằng compa.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thao tác quay compa và nối các đỉnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Vì sao cạnh lục giác đều bằng bán kính $R$? Vì tam giác tạo bởi tâm và 2 đỉnh liên tiếp là tam giác đều ($60^\\circ$).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt cách vẽ lục giác đều tuyệt đẹp. | **2. Đường tròn ngoại tiếp và nội tiếp:**<br>- Mọi đa giác đều có một đường tròn ngoại tiếp và một đường tròn nội tiếp cùng tâm.<br>- Cạnh của lục giác đều nội tiếp $(O; R)$ đúng bằng bán kính: $a = R$.<br>- Bán kính nội tiếp của lục giác đều: $r = \\frac{R\\sqrt{3}}{2}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Tính chu vi và diện tích của lục giác đều nội tiếp đường tròn bán kính $R = 6\\text{ cm}$.
b) Nội dung: Cho lục giác đều $ABCDEF$ nội tiếp đường tròn $(O; 6\\text{ cm})$.
1) Tính độ dài cạnh và chu vi của lục giác đều.
2) Tính diện tích của lục giác đều.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập tính chu vi và diện tích lục giác đều với $R = 6\\text{ cm}$.<br>- **HS:** Nhận đề và tính toán.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cạnh $a = R = 6\\text{ cm}$. Chu vi $C = 6 \\times 6 = 36\\text{ cm}$.<br>Lục giác đều gồm 6 tam giác đều cạnh $6\\text{ cm}$.<br>Diện tích 1 tam giác đều: $S_1 = \\frac{6^2 \\sqrt{3}}{4} = 9\\sqrt{3}\\text{ cm}^2$.<br>Diện tích lục giác đều: $S = 6 \\times 9\\sqrt{3} = 54\\sqrt{3} \\approx 93{,}53\\text{ cm}^2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa bài giải mẫu mực trên bảng. | **Bài giải:**<br>1) Vì lục giác đều nội tiếp đường tròn bán kính $R = 6\\text{ cm}$ nên độ dài cạnh của lục giác đều là:<br>$$a = R = 6\\text{ (cm)}$$<br>Chu vi của lục giác đều là:<br>$$C = 6a = 6 \\cdot 6 = 36\\text{ (cm)}$$<br><br>2) Lục giác đều được tạo bởi 6 tam giác đều bằng nhau có cạnh bằng $6\\text{ cm}$.<br>Diện tích của một tam giác đều là:<br>$$S_1 = \\frac{a^2 \\sqrt{3}}{4} = \\frac{6^2 \\sqrt{3}}{4} = 9\\sqrt{3}\\text{ (cm}^2\\text{)}$$<br>Diện tích của lục giác đều là:<br>$$S = 6 \\cdot S_1 = 6 \\cdot 9\\sqrt{3} = 54\\sqrt{3}\\text{ (cm}^2\\text{)} \\approx 93{,}53\\text{ (cm}^2\\text{)}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng vẽ họa tiết ngôi sao 6 cánh bằng cách nối xen kẽ các đỉnh của lục giác đều.
b) Nội dung: Nối 3 đỉnh $A, C, E$ được 1 tam giác đều; nối $B, D, F$ được 1 tam giác đều. Hai tam giác này lồng nhau tạo thành ngôi sao 6 cánh David.
c) Sản phẩm: Hình vẽ ngôi sao 6 cánh trang trí trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn tạo hoa văn ngôi sao 6 cánh từ lục giác đều.<br>- **HS:** Thao tác nối các đỉnh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ hình trang trí nhanh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giơ vở khoe sản phẩm hình vẽ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò chuẩn bị cho tiết Luyện tập chung. | Vẽ hoa văn trang trí ngôi sao 6 cánh từ đa giác đều. |
"""
    },

    # 29: Tiết 41-42: Luyện tập chung (Mindmap: mindmap_toan9_hinh_tiet41_42.png)
    {
        "filename": "29_KHBD_Toan9_LuyenTapChung_Tiet41-42.md",
        "md": """TIẾT 41, 42 - LUYỆN TẬP CHUNG: TỨ GIÁC NỘI TIẾP VÀ ĐA GIÁC ĐỀU
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và rèn luyện thành thạo kỹ năng:
  + Vận dụng 4 dấu hiệu nhận biết để chứng minh tứ giác nội tiếp đường tròn.
  + Khai thác các tính chất của tứ giác nội tiếp để suy ra các góc bằng nhau, chứng minh các cặp đường thẳng song song, vuông góc, đồng quy hoặc thẳng hàng.
  + Tính toán góc, cạnh, chu vi, diện tích và bán kính đường tròn ngoại tiếp, nội tiếp đa giác đều.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức Tứ giác nội tiếp và Đa giác đều bằng sơ đồ tư duy.
- Giao tiếp và hợp tác: Hợp tác nhóm thảo luận tìm tòi lời giải các bài toán hình học phân loại cao.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng tư duy phản biện, lập luận hình học nhiều tầng nấc.
- Năng lực giải quyết vấn đề toán học: Giải bài toán hình học phẳng tổng hợp 3 câu chuẩn cấu trúc đề thi tuyển sinh vào lớp 10.

## 3. Về phẩm chất
- Rèn tính cẩn thận, vẽ hình chính xác và rõ ràng bằng compa, eke.
- Tinh thần kiên trì, say mê chinh phục các bài toán hình học hay.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI, máy chiếu, bảng phụ ghi bài tập.
2. Học sinh: SGK, vở ghi, compa, thước kẻ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại 4 dấu hiệu nhận biết tứ giác nội tiếp kinh điển.
b) Nội dung: Trả lời nhanh: Kể tên 4 dấu hiệu nhận biết một tứ giác là tứ giác nội tiếp.
c) Sản phẩm: HS đọc đủ 4 dấu hiệu: Tổng 2 góc đối $180^\\circ$; Góc ngoài bằng góc trong đối diện; 2 đỉnh kề cùng nhìn một đoạn thẳng dưới góc bằng nhau; 4 đỉnh cách đều 1 điểm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi gọi tên 4 dấu hiệu tứ giác nội tiếp.<br>- **HS:** Xung phong trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc to 4 dấu hiệu trước lớp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương và chuyển sang sơ đồ tư duy tổng hợp. | Tái hiện 4 dấu hiệu nhận biết tứ giác nội tiếp. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (25 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức bằng sơ đồ tư duy (25 phút)
a) Mục tiêu: Hệ thống toàn diện kiến thức Tứ giác nội tiếp và Đa giác đều bằng sơ đồ tư duy trực quan 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI Tứ giác nội tiếp & Đa giác đều.
c) Sản phẩm: Sơ đồ tư duy được hệ thống trong vở của học sinh.

![Sơ đồ tư duy Luyện tập chung Tứ giác nội tiếp và Đa giác đều Tiết 41 - 42](khbd-ill:mindmap-toan9-hinh-tiet41-42)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI Tứ giác nội tiếp và Đa giác đều. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 4 nhánh:<br>1) Định nghĩa tứ giác nội tiếp và định lí tổng hai góc đối bằng $180^\\circ$.<br>2) Bốn dấu hiệu nhận biết tứ giác nội tiếp kinh điển.<br>3) Đa giác đều: Định nghĩa, công thức góc $\\alpha = \\frac{(n-2)180^\\circ}{n}$, ngoại tiếp và nội tiếp cùng tâm.<br>4) Ứng dụng chứng minh hình học và tính toán.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS phân tích mối liên hệ giữa các nhánh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại kiến thức trọng tâm và các kĩ năng vẽ đường tròn phụ hỗ trợ chứng minh. | **Hệ thống kiến thức trọng tâm:**<br>1. Tứ giác nội tiếp: Tổng 2 góc đối bằng $180^\\circ$.<br>2. Bốn dấu hiệu nhận biết: Tổng góc đối $180^\\circ$, góc ngoài bằng góc đối trong, cùng nhìn một cạnh, cách đều 1 điểm.<br>3. Đa giác đều: Các góc bằng $\\frac{(n-2)180^\\circ}{n}$. Mọi đa giác đều có đường tròn ngoại tiếp và nội tiếp cùng tâm.<br>4. Phương pháp khai thác góc nội tiếp sau khi đã chứng minh tứ giác nội tiếp. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
a) Mục tiêu: Giải bài toán hình học phẳng tổng hợp chuẩn đề thi vào lớp 10.
b) Nội dung: Cho đường tròn $(O)$, điểm $M$ nằm ngoài $(O)$. Kẻ hai tiếp tuyến $MA, MB$ với $(O)$ ($A, B$ là tiếp điểm). Kẻ cát tuyến $MCD$ không đi qua $O$ ($C$ nằm giữa $M$ và $D$).
1) Chứng minh tứ giác $MAOB$ nội tiếp đường tròn. Xác định tâm của đường tròn đó.
2) Chứng minh $MA^2 = MC \\cdot MD$.
3) Gọi $H$ là giao điểm của $AB$ và $MO$. Chứng minh tứ giác $CHOD$ nội tiếp đường tròn.
c) Sản phẩm: Lời giải chi tiết 3 câu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài toán tiếp tuyến và cát tuyến kinh điển.<br>- **HS:** Vẽ hình cẩn thận bằng compa và thước kẻ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:**<br>1) Vì $MA, MB$ là tiếp tuyến nên $\\widehat{MAO} = 90^\\circ, \\widehat{MBO} = 90^\\circ$.<br>Tổng hai góc đối: $\\widehat{MAO} + \\widehat{MBO} = 90^\\circ + 90^\\circ = 180^\\circ$. Tứ giác $MAOB$ nội tiếp đường tròn đường kính $MO$ (tâm là trung điểm của $MO$).<br>2) Xét $\\Delta MAC$ và $\\Delta MDA$ có: góc $M$ chung và $\\widehat{MAC} = \\widehat{MDA}$ (góc tạo bởi tiếp tuyến và dây cung bằng góc nội tiếp cùng chắn $\\overparen{AC}$). Do đó $\\Delta MAC \\backsim \\Delta MDA$ (g.g) $\\Rightarrow \\frac{MA}{MD} = \\frac{MC}{MA} \\Rightarrow MA^2 = MC \\cdot MD$.<br>3) Theo tính chất tiếp tuyến: $MO \\perp AB$ tại $H$ và $MA^2 = MH \\cdot MO$ (hệ thức lượng trong tam giác vuông $MAO$).<br>Từ đó: $MH \\cdot MO = MC \\cdot MD \\Rightarrow \\frac{MC}{MO} = \\frac{MH}{MD}$.<br>Xét $\\Delta MCH$ và $\\Delta MOD$ có góc $M$ chung và $\\frac{MC}{MO} = \\frac{MH}{MD}$. Do đó $\\Delta MCH \\backsim \\Delta MOD$ (c.g.c).<br>Suy ra $\\widehat{MHC} = \\widehat{MDO}$.<br>Vì góc ngoài $\\widehat{MHC}$ bằng góc trong đối diện $\\widehat{CDO}$ nên tứ giác $CHOD$ nội tiếp đường tròn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán mẫu mực thi vào 10 ứng dụng cả dấu hiệu 1 và dấu hiệu 2 của tứ giác nội tiếp. | **Bài giải:**<br>1) Vì $MA, MB$ là hai tiếp tuyến của $(O)$ nên:<br>$$MA \\perp OA \\Rightarrow \\widehat{MAO} = 90^\\circ$$<br>$$MB \\perp OB \\Rightarrow \\widehat{MBO} = 90^\\circ$$<br>Xét tứ giác $MAOB$ có:<br>$$\\widehat{MAO} + \\widehat{MBO} = 90^\\circ + 90^\\circ = 180^\\circ$$<br>Vậy tứ giác $MAOB$ nội tiếp đường tròn đường kính $MO$ (tâm là trung điểm của $MO$).<br><br>2) Xét $\\Delta MAC$ và $\\Delta MDA$ có:<br>- $\\widehat{M}$ chung;<br>- $\\widehat{MAC} = \\widehat{MDA}$ (cùng chắn cung $\\overparen{AC}$).<br>Do đó $\\Delta MAC \\backsim \\Delta MDA$ (g.g).<br>Suy ra:<br>$$\\frac{MA}{MD} = \\frac{MC}{MA} \\Rightarrow MA^2 = MC \\cdot MD$$<br><br>3) Ta có $MO$ là đường trung trực của $AB$, nên $MO \\perp AB$ tại $H$.<br>Áp dụng hệ thức lượng cho $\\Delta MAO$ vuông tại $A$, đường cao $AH$:<br>$$MA^2 = MH \\cdot MO$$<br>Kết hợp với câu 2 suy ra:<br>$$MC \\cdot MD = MH \\cdot MO \\Rightarrow \\frac{MC}{MO} = \\frac{MH}{MD}$$<br>Xét $\\Delta MCH$ và $\\Delta MOD$ có:<br>- $\\widehat{M}$ chung;<br>- $\\frac{MC}{MO} = \\frac{MH}{MD}$.<br>Do đó $\\Delta MCH \\backsim \\Delta MOD$ (c.g.c).<br>Suy ra $\\widehat{MHC} = \\widehat{MDO}$.<br>Do góc ngoài tại đỉnh $H$ bằng góc trong đối diện tại đỉnh $D$, nên tứ giác $CHOD$ nội tiếp đường tròn. |

## D. VẬN DỤNG VÀ DẶN DÒ (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Nhắc nhở dặn dò chuẩn bị cho tiết Bài tập cuối chương IX tiếp theo.
b) Nội dung: Ôn lại toàn bộ các định lí, hệ quả và dấu hiệu của chương IX.
c) Sản phẩm: HS ghi nhận nhiệm vụ tự học ở nhà.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò xem lại toàn bộ bài tập cuối chương IX trong SGK.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự hệ thống lại các dạng bài tập hình học.<br><br>**+ Bước 3: Kết thúc buổi học**<br>- Cả lớp chào giáo viên. | Dặn dò chuẩn bị cho tiết Bài tập cuối chương IX. |
"""
    },

    # 30: Tiết 43-44: Bài tập cuối chương IX (Mindmap: mindmap_toan9_hinh_tiet43_44.png)
    {
        "filename": "30_KHBD_Toan9_BaiTapCuoiChuong9_Tiet43-44.md",
        "md": """TIẾT 43, 44 - BÀI TẬP CUỐI CHƯƠNG IX
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Ôn tập và củng cố toàn diện kiến thức Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp:
  + Góc nội tiếp, định lí số đo và các hệ quả (đặc biệt góc nội tiếp chắn nửa đường tròn là góc vuông).
  + Đường tròn ngoại tiếp và nội tiếp của một tam giác (đặc biệt tam giác vuông và tam giác đều).
  + Tứ giác nội tiếp: Định nghĩa, định lí tổng hai góc đối bằng $180^\\circ$ và 4 dấu hiệu nhận biết kinh điển.
  + Đa giác đều: Định nghĩa, số đo góc $\\alpha = \\frac{(n-2)180^\\circ}{n}$, ngoại tiếp và nội tiếp đa giác đều.
- Rèn luyện kỹ năng tổng hợp giải các bài toán trắc nghiệm và tự luận cuối chương trong SGK.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tổng kết kiến thức toàn bộ chương IX dưới dạng sơ đồ tư duy hoàn chỉnh.
- Giao tiếp và hợp tác: Tự tin trao đổi các phương pháp chứng minh hình học khác nhau trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng suy luận logic, phát hiện các tứ giác nội tiếp tiềm ẩn trong hình vẽ.
- Năng lực giải quyết vấn đề toán học: Hoàn thành bài toán hình học tổng hợp sát cấu trúc đề thi tuyển sinh vào lớp 10.

## 3. Về phẩm chất
- Rèn thói quen vẽ hình chính xác, rõ ràng bằng compa và thước kẻ.
- Tinh thần nghiêm túc ôn tập chuẩn bị cho bài Kiểm tra đánh giá giữa Học kì II phần Hình học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI tổng kết Chương IX, máy chiếu.
2. Học sinh: SGK, vở ghi, compa, thước kẻ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Khởi động ôn tập bằng trò chơi giải nhanh các câu hỏi trắc nghiệm kiến thức cốt lõi Chương IX.
b) Nội dung: Trả lời nhanh 3 câu hỏi về góc nội tiếp, tứ giác nội tiếp và đa giác đều.
c) Sản phẩm: Câu trả lời chính xác của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu 3 câu hỏi trắc nghiệm ôn tập nhanh Chương IX.<br>- **HS:** Xung phong trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trả lời chính xác về góc vuông, tổng góc đối $180^\\circ$, và số đo góc lục giác đều $120^\\circ$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương và chuyển sang sơ đồ tư duy tổng kết. | Tái hiện nhanh các kiến thức cốt lõi Chương IX. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (25 phút)
### Hoạt động 2.1: Tổng kết Chương IX bằng sơ đồ tư duy (25 phút)
a) Mục tiêu: Khái quát hóa toàn bộ cấu trúc kiến thức Chương IX: Đường tròn ngoại tiếp và nội tiếp.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI tổng kết Chương IX.
c) Sản phẩm: Sơ đồ tư duy được hoàn thiện trong vở ghi của học sinh.

![Sơ đồ tư duy Bài tập cuối chương IX Tiết 43 - 44](khbd-ill:mindmap-toan9-hinh-tiet43-44)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI tổng kết toàn bộ Chương IX. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trình bày 4 nhánh:<br>1) Góc với đường tròn (góc ở tâm, góc nội tiếp, góc chắn nửa đường tròn vuông).<br>2) Tam giác và đường tròn (ngoại tiếp - giao trung trực, nội tiếp - giao phân giác).<br>3) Tứ giác nội tiếp (định lí thuận, 4 dấu hiệu nhận biết).<br>4) Đa giác đều (công thức góc, vẽ lục giác đều, họa tiết ứng dụng).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ trình bày tổng quan chương.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt sơ đồ và nhấn mạnh các dạng toán điển hình. | **Tổng kết toàn bộ Chương IX:**<br>1. Góc nội tiếp: Định lí và 4 hệ quả.<br>2. Đường tròn ngoại tiếp và nội tiếp tam giác.<br>3. Tứ giác nội tiếp: Định lí tổng góc đối $180^\\circ$ và 4 dấu hiệu nhận biết.<br>4. Đa giác đều: Số đo góc $\\alpha = \\frac{(n-2)180^\\circ}{n}$, ngoại tiếp/nội tiếp.<br>5. Ứng dụng thi vào 10: Chứng minh tứ giác nội tiếp và hệ thức hình học. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
a) Mục tiêu: Giải bài tập tổng hợp cuối chương trong SGK Toán 9 Tập 2.
b) Nội dung: Cho tam giác nhọn $ABC$ ($AB < AC$) nội tiếp đường tròn $(O)$. Các đường cao $AD, BE, CF$ cắt nhau tại trực tâm $H$.
1) Chứng minh các tứ giác $BCEF$ và $AFHE$ nội tiếp đường tròn.
2) Chứng minh $H$ là tâm đường tròn nội tiếp tam giác $DEF$.
3) Gọi $K$ là điểm đối xứng của $H$ qua $BC$. Chứng minh $K$ nằm trên đường tròn $(O)$.
c) Sản phẩm: Lời giải chi tiết 3 câu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập hình học tổng hợp với tam giác nhọn và ba đường cao.<br>- **HS:** Vẽ hình cẩn thận bằng compa và thước kẻ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:**<br>1) $\\widehat{BFC} = \\widehat{BEC} = 90^\\circ \\Rightarrow BCEF$ nội tiếp (cùng nhìn $BC$ dưới góc $90^\\circ$). Tứ giác $AFHE$ có $\\widehat{AFH} + \\widehat{AEH} = 90^\\circ + 90^\\circ = 180^\\circ \\Rightarrow AFHE$ nội tiếp.<br>2) Vì $BCEF$ nội tiếp nên $\\widehat{FEB} = \\widehat{FCB}$. Vì $AFHE$ nội tiếp nên $\\widehat{FEH} = \\widehat{FAH}$. Mà $\\widehat{FAH} = \\widehat{FCB}$ (cùng phụ với $\\widehat{B}$). Suy ra $\\widehat{FEB} = \\widehat{FEH} \\Rightarrow EH$ là phân giác của $\\widehat{DEF}$. Tương tự $DH, FH$ là phân giác $\\Rightarrow H$ là tâm đường tròn nội tiếp $\\Delta DEF$.<br>3) $\\widehat{BKC} = \\widehat{BHC}$ (do tính chất đối xứng qua $BC$). Mà $\\widehat{BHC} + \\widehat{BAC} = 180^\\circ$ (do $AFHE$ nội tiếp và $\\widehat{BHC} = \\widehat{EHF}$). Suy ra $\\widehat{BKC} + \\widehat{BAC} = 180^\\circ \\Rightarrow ABKC$ nội tiếp $\\Rightarrow K \\in (O)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa bài giải mẫu mực đỉnh cao của hình học 9. | **Bài giải:**<br>1) Xét tứ giác $BCEF$ có:<br>$$\\widehat{BFC} = \\widehat{BEC} = 90^\\circ$$<br>Hai đỉnh kề $F$ và $E$ cùng nhìn cạnh $BC$ dưới góc $90^\\circ$. Vậy tứ giác $BCEF$ nội tiếp đường tròn đường kính $BC$.<br>Tứ giác $AFHE$ có:<br>$$\\widehat{AFH} + \\widehat{AEH} = 90^\\circ + 90^\\circ = 180^\\circ$$<br>Vậy tứ giác $AFHE$ nội tiếp đường tròn đường kính $AH$.<br><br>2) Vì $BCEF$ nội tiếp nên $\\widehat{FEB} = \\widehat{FCB}$ (cùng chắn $\\overparen{FB}$).<br>Vì $AFHE$ nội tiếp nên $\\widehat{FEH} = \\widehat{FAH}$ (cùng chắn $\\overparen{FH}$).<br>Mặt khác $\\widehat{FAH} = \\widehat{FCB}$ (cùng phụ với $\\widehat{ABC}$).<br>Suy ra $\\widehat{FEB} = \\widehat{FEH}$, tức là $EB$ (hay $EH$) là tia phân giác của $\\widehat{FED}$.<br>Chứng minh hoàn toàn tương tự ta có $DH, FH$ lần lượt là các tia phân giác của $\\widehat{EDF}$ và $\\widehat{DFE}$.<br>Vậy $H$ là giao điểm ba đường phân giác trong của $\\Delta DEF$, tức là $H$ là tâm đường tròn nội tiếp $\\Delta DEF$.<br><br>3) Vì $K$ đối xứng với $H$ qua $BC$ nên $\\Delta KBC = \\Delta HBC$ (c.c.c), suy ra $\\widehat{BKC} = \\widehat{BHC}$.<br>Trong tứ giác $AFHE$ có $\\widehat{EHF} + \\widehat{BAC} = 180^\\circ$.<br>Mà $\\widehat{BHC} = \\widehat{EHF}$ (hai góc đối đỉnh), do đó:<br>$$\\widehat{BKC} + \\widehat{BAC} = 180^\\circ$$<br>Suy ra tứ giác $ABKC$ là tứ giác nội tiếp.<br>Mà $A, B, C \\in (O)$, nên điểm $K$ cũng thuộc đường tròn $(O)$. |

## D. VẬN DỤNG VÀ DẶN DÒ (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Chuẩn bị cho tiết Ôn tập giữa Học kì II phần Hình học tiếp theo.
b) Nội dung: Rà soát lại các dấu hiệu nhận biết tứ giác nội tiếp và cách chứng minh điểm thuộc đường tròn.
c) Sản phẩm: HS ghi nhận nhiệm vụ tự học ở nhà.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò chuẩn bị cho tiết Ôn tập giữa HKII Hình học: Xem lại các bài toán chứng minh tứ giác nội tiếp.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự ôn luyện lại các chứng minh.<br><br>**+ Bước 3: Kết thúc buổi học**<br>- Cả lớp chào giáo viên. | Dặn dò chuẩn bị tiết Ôn tập giữa HKII Hình học. |
"""
    },

    # 31: Tiết 45: Ôn tập giữa HK2 Hình học (Mindmap: mindmap_toan9_hinh_tiet45.png)
    {
        "filename": "31_KHBD_Toan9_OnTapGiuaHK2_HinhHoc_Tiet45.md",
        "md": """TIẾT 45 - ÔN TẬP VÀ KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Hình học trọng tâm nửa đầu Học kì II môn Toán 9 (Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp):
  + Góc nội tiếp và hệ quả góc chắn nửa đường tròn vuông.
  + Đường tròn ngoại tiếp và nội tiếp tam giác.
  + Bốn dấu hiệu nhận biết tứ giác nội tiếp kinh điển.
  + Đa giác đều, công thức tính góc và tính chất đối xứng.
- Chuẩn bị đầy đủ kiến thức và tâm thế tự tin cho bài Kiểm tra đánh giá giữa Học kì II phần Hình học (Tiết 46).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự ôn luyện các định lí, tính chất và xem lại các dạng bài tập trọng tâm.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp chứng minh hình học và sửa lỗi vẽ hình trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Trình bày bài toán hình học có lập luận chặt chẽ, luôn ghi rõ căn cứ định lí hoặc hệ quả.
- Năng lực giải quyết vấn đề toán học: Phân bổ thời gian hợp lí khi làm bài kiểm tra giữa kì.

## 3. Về phẩm chất
- Cẩn thận, chính xác trong từng nét vẽ compa và từng bước suy luận hình học.
- Tự tin, nghiêm túc trước kì kiểm tra đánh giá giữa kì.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, đề cương ôn tập giữa HK2 phần Hình học, sơ đồ tư duy vector 300 DPI, máy chiếu.
2. Học sinh: SGK, vở ghi, compa, thước kẻ, máy tính cầm tay, đề cương ôn tập.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tạo tâm thế tập trung và rà soát ma trận đề kiểm tra giữa kì phần Hình học.
b) Nội dung: GV giới thiệu cấu trúc điểm phần Hình học trong đề kiểm tra giữa HK2 (chiếm khoảng 3,0 - 3,5 điểm trong thang điểm 10).
c) Sản phẩm: HS nắm rõ cấu trúc đề thi để có chiến lược làm bài hiệu quả.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu ma trận đề thi giữa kì phần Hình học: Gồm câu hỏi nhận biết góc nội tiếp, thông hiểu tứ giác nội tiếp và bài toán tự luận hình học phẳng 2 - 3 câu.<br>- **HS:** Lắng nghe và ghi chú trọng tâm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trao đổi cặp đôi về các định lí hay nhầm lẫn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu lại các dấu hiệu nhận biết tứ giác nội tiếp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuyển sang phần sơ đồ tư duy ôn tập tổng quát. | Nắm vững ma trận và định hướng ôn tập kiểm tra giữa HK2 Hình học. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức Hình học giữa HK2 bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ các kiến thức then chốt của Chương IX bằng sơ đồ tư duy 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI Ôn tập giữa HK2 Hình học 9.
c) Sản phẩm: Sơ đồ tư duy được hệ thống trong vở của học sinh.

![Sơ đồ tư duy Ôn tập giữa HK2 Hình học Tiết 45](khbd-ill:mindmap-toan9-hinh-tiet45)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI Ôn tập giữa HK2 Hình học 9. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 4 nhánh:<br>1) Góc nội tiếp (chắn nửa đường tròn vuông, cùng chắn 1 cung).<br>2) Chứng minh tứ giác nội tiếp (tổng góc đối $180^\\circ$, hai đỉnh kề cùng nhìn 1 cạnh).<br>3) Hệ thức lượng đường tròn (phương tích cát tuyến, tiếp tuyến).<br>4) Đường tròn ngoại tiếp/nội tiếp tam giác và đa giác đều.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS nhắc lại cách phân biệt hai dấu hiệu nhận biết tứ giác nội tiếp phổ biến nhất.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại những lỗi thường gặp: Thiếu giải thích góc vuông, vẽ hình sai tỉ lệ dẫn đến ngộ nhận. | **Hệ thống kiến thức ôn tập giữa HK2:**<br>1. Góc nội tiếp: $\\widehat{A} = \\frac{1}{2} \\text{sđ}\\overparen{BC}$. Góc chắn nửa đường tròn bằng $90^\\circ$.<br>2. Bốn dấu hiệu nhận biết tứ giác nội tiếp.<br>3. Đường tròn ngoại tiếp và nội tiếp tam giác vuông, tam giác đều.<br>4. Phương pháp chứng minh tiếp tuyến và hệ thức hình học. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài toán mẫu sát với cấu trúc đề kiểm tra giữa kì.
b) Nội dung: Cho đường tròn $(O; R)$, đường kính $AB$. Lấy điểm $C$ trên $(O)$ sao cho $AC = R$. Tiếp tuyến tại $C$ của $(O)$ cắt tiếp tuyến tại $A$ của $(O)$ ở điểm $M$.
1) Chứng minh tam giác $ABC$ vuông và tính độ dài cạnh $BC$ theo $R$.
2) Chứng minh tứ giác $MAOC$ nội tiếp đường tròn.
3) Chứng minh $MB$ đi qua trung điểm của đoạn thẳng $AC$ (hoặc tính độ dài $OM$).
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập hình học tổng hợp sát cấu trúc đề kiểm tra.<br>- **HS:** Vẽ hình chính xác vào vở bằng compa.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện giải từng câu:<br>1) Vì $C \\in (O)$ đường kính $AB$ nên $\\widehat{ACB} = 90^\\circ$. Trong tam giác vuông $ABC$: $BC = \\sqrt{AB^2 - AC^2} = \\sqrt{(2R)^2 - R^2} = R\\sqrt{3}$.<br>2) Vì $MA$ là tiếp tuyến tại $A$ nên $\\widehat{MAO} = 90^\\circ$. Vì $MC$ là tiếp tuyến tại $C$ nên $\\widehat{MCO} = 90^\\circ$. Tứ giác $MAOC$ có $\\widehat{MAO} + \\widehat{MCO} = 90^\\circ + 90^\\circ = 180^\\circ$, suy ra $MAOC$ nội tiếp đường tròn đường kính $MO$.<br>3) Theo tính chất hai tiếp tuyến cắt nhau: $MO$ là phân giác của $\\widehat{AOC}$. Mà $\\Delta AOC$ đều ($OA = OC = AC = R$) nên $\\widehat{AOC} = 60^\\circ \\Rightarrow \\widehat{AOM} = 30^\\circ$. Trong tam giác vuông $MAO$: $OM = \\frac{OA}{\\cos 30^\\circ} = \\frac{R}{\\frac{\\sqrt{3}}{2}} = \\frac{2R\\sqrt{3}}{3}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, lưu ý cách trình bày chặt chẽ để đạt điểm tối đa. | **Bài giải:**<br>1) Vì $C$ thuộc đường tròn đường kính $AB$ nên:<br>$$\\widehat{ACB} = 90^\\circ\\text{ (góc nội tiếp chắn nửa đường tròn)}$$<br>Suy ra $\\Delta ABC$ vuông tại $C$.<br>Áp dụng định lí Pythagore trong $\\Delta ABC$ vuông tại $C$:<br>$$BC = \\sqrt{AB^2 - AC^2} = \\sqrt{(2R)^2 - R^2} = \\sqrt{4R^2 - R^2} = R\\sqrt{3}$$<br><br>2) Vì $MA, MC$ là các tiếp tuyến của $(O)$ nên:<br>$$MA \\perp OA \\Rightarrow \\widehat{MAO} = 90^\\circ$$<br>$$MC \\perp OC \\Rightarrow \\widehat{MCO} = 90^\\circ$$<br>Xét tứ giác $MAOC$ có:<br>$$\\widehat{MAO} + \\widehat{MCO} = 90^\\circ + 90^\\circ = 180^\\circ$$<br>Mà hai góc này ở vị trí đối nhau.<br>Vậy tứ giác $MAOC$ nội tiếp đường tròn đường kính $MO$ (tâm là trung điểm của $MO$).<br><br>3) Xét $\\Delta AOC$ có $OA = OC = AC = R$, suy ra $\\Delta AOC$ là tam giác đều.<br>Do đó $\\widehat{AOC} = 60^\\circ$.<br>Theo tính chất hai tiếp tuyến cắt nhau, tia $OM$ là phân giác của $\\widehat{AOC}$, suy ra:<br>$$\\widehat{AOM} = \\frac{\\widehat{AOC}}{2} = \\frac{60^\\circ}{2} = 30^\\circ$$<br>Trong $\\Delta MAO$ vuông tại $A$:<br>$$OM = \\frac{OA}{\\cos 30^\\circ} = \\frac{R}{\\frac{\\sqrt{3}}{2}} = \\frac{2R\\sqrt{3}}{3}$$ |

## D. VẬN DỤNG VÀ DẶN DÒ (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Hướng dẫn học sinh chuẩn bị dụng cụ cho tiết kiểm tra giữa kì.
b) Nội dung: Dặn dò chuẩn bị đầy đủ thước kẻ, compa, bút mực cho tiết kiểm tra tiếp theo.
c) Sản phẩm: Học sinh ghi nhận đầy đủ yêu cầu dặn dò.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò chuẩn bị compa, thước kẻ, bút mực cho tiết kiểm tra giữa HKII Hình học.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự kiểm tra lại compa.<br><br>**+ Bước 3: Kết thúc tiết học**<br>- Cả lớp chào giáo viên. | Dặn dò chuẩn bị tiết Kiểm tra giữa Học kì II Hình học. |
"""
    },

    # 32: Tiết 46: Kiểm tra giữa HK2 Hình học
    {
        "filename": "32_KHBD_Toan9_KiemTraGiuaHK2_HinhHoc_Tiet46.md",
        "md": """TIẾT 46 - KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá mức độ đạt chuẩn kiến thức kĩ năng của học sinh trong nửa đầu Học kì II môn Toán 9 (phần Hình học - Chương IX: Đường tròn ngoại tiếp và đường tròn nội tiếp):
  + Nhận biết góc nội tiếp, góc chắn nửa đường tròn vuông.
  + Chứng minh tứ giác nội tiếp đường tròn bằng các dấu hiệu nhận biết kinh điển.
  + Tính số đo góc, độ dài đoạn thẳng và hệ thức hình học trong đường tròn.
- Đánh giá khả năng vẽ hình chính xác bằng compa và thước kẻ, trình bày bài toán hình học khoa học.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Ý thức tự giác, trung thực, nghiêm túc làm bài kiểm tra độc lập, không gian lận.
- Giải quyết vấn đề: Phân tích đề bài, lựa chọn phương pháp chứng minh tối ưu.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng lập luận logic, suy diễn hình học chặt chẽ.
- Năng lực tính toán: Tính toán chính xác độ dài cạnh và số đo góc.

## 3. Về phẩm chất
- Trung thực, thẳng thắn trong kiểm tra đánh giá.
- Rèn tính cẩn trọng, kỷ luật và tinh thần vượt khó.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo đúng ma trận và đặc tả đề kiểm tra giữa kì, đáp án và biểu điểm chi tiết.
2. Học sinh: Dụng cụ vẽ hình (compa, thước thẳng có chia vạch, eke), bút mực, giấy kiểm tra.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG VÀ PHÁT ĐỀ (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ổn định phòng thi, phổ biến quy chế và phát đề kiểm tra cho học sinh.
b) Nội dung: GV điểm danh, nhắc nhở quy chế thi và phát đề.
c) Sản phẩm: 100% học sinh nhận đề và ghi đầy đủ thông tin vào giấy làm bài.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Ổn định chỗ ngồi, kiểm tra trật tự, nhắc nhở nghiêm cấm mọi hành vi gian lận.<br>- **HS:** Cất toàn bộ tài liệu và chuẩn bị dụng cụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Phát đề kiểm tra.<br>- **HS:** Kiểm tra độ rõ của đề, ghi thông tin cá nhân.<br><br>**+ Bước 3: Bắt đầu làm bài**<br>- **GV:** Ghi thời gian làm bài lên bảng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giám sát phòng thi nghiêm túc. | Phát đề kiểm tra và ổn định phòng thi. |

## B. TIẾN HÀNH LÀM BÀI KIỂM TRA (HOẠT ĐỘNG 2) (35 phút)
### Ma trận và Đề kiểm tra Hình học giữa HK2 (35 phút)
a) Mục tiêu: Học sinh làm bài kiểm tra độc lập, đạt kết quả cao nhất theo năng lực.
b) Nội dung: Đề gồm 2 phần: Trắc nghiệm (3 điểm) và Tự luận (7 điểm).
c) Sản phẩm: Bài làm hoàn chỉnh trên giấy thi của từng học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Làm bài độc lập**<br>- **HS:** Làm bài nghiêm túc, vẽ hình chính xác vào giấy thi bằng compa.<br>- **GV:** Giám thị bao quát lớp thi.<br><br>**+ Bước 2: Theo dõi thời gian**<br>- **GV:** Nhắc nhở thời gian làm bài (còn 15 phút, còn 5 phút).<br>- **HS:** Soát lại bài làm, kiểm tra kĩ kí hiệu góc vuông.<br><br>**+ Bước 3: Hoàn thành bài làm**<br>- **HS:** Sắp xếp lại tờ giấy thi, chuẩn bị nộp bài.<br><br>**+ Bước 4: Hết giờ làm bài**<br>- **GV:** Thu bài kiểm tra của cả lớp. | **Nội dung đề kiểm tra minh họa:**<br>**Phần I. Trắc nghiệm (3 điểm):**<br>- Câu 1: Số đo góc nội tiếp bằng nửa số đo cung bị chắn.<br>- Câu 2: Tứ giác nội tiếp có tổng hai góc đối bằng $180^\\circ$.<br>- Câu 3: Mỗi góc của lục giác đều bằng $120^\\circ$.<br><br>**Phần II. Tự luận (7 điểm):**<br>Cho tam giác nhọn $ABC$ ($AB < AC$) nội tiếp đường tròn $(O)$. Hai đường cao $BE$ và $CF$ cắt nhau tại trực tâm $H$.<br>a) (3,0 điểm) Chứng minh tứ giác $BFEC$ nội tiếp đường tròn. Xác định tâm của đường tròn đó.<br>b) (2,5 điểm) Chứng minh tứ giác $AFHE$ nội tiếp và $\\widehat{AFE} = \\widehat{ACB}$.<br>c) (1,5 điểm) Kẻ đường kính $AK$ của đường tròn $(O)$. Chứng minh tứ giác $BHCK$ là hình bình hành. |

## C. THU BÀI VÀ NHẬN XÉT (HOẠT ĐỘNG 3) (5 phút)
a) Mục tiêu: Thu đủ số lượng bài thi và nhận xét nền nếp buổi kiểm tra.
b) Nội dung: Thu bài theo hàng, kiểm đếm đủ số bài thi và giải tỏa căng thẳng cho học sinh.
c) Sản phẩm: Thu đủ 100% bài kiểm tra của cả lớp.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Thu bài kiểm tra của học sinh theo thứ tự bàn học.<br>- **HS:** Nộp bài trật tự, nghiêm túc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Kiểm đếm khớp số bài thi với sĩ số.<br><br>**+ Bước 3: Nhận xét giờ kiểm tra**<br>- **GV:** Tuyên dương ý thức làm bài nghiêm túc, tự giác của cả lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dặn dò chuẩn bị cho Chương X: Các hình khối trong thực tiễn tiếp theo. | Thu đủ số bài kiểm tra và nhận xét nền nếp phòng thi. |
"""
    },
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print(f"Hoàn tất tạo đợt 4 (9 bài Chương IX Tiết 31 - 46) Toán 9 HK2!")
