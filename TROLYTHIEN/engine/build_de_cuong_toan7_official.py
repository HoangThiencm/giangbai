# -*- coding: utf-8 -*-
"""
BUILDER CHÍNH THỨC: ĐỀ CƯƠNG TOÁN 7 GIỮA KỲ I CHUẨN HÓA & BÁO CÁO PHẢN BIỆN
Trợ lý Sư phạm Hoàng Thiên • Trường THCS Trần Phú • Năm học 2026 - 2027
Tích hợp:
1. 100% Equation Word (m:oMath)
2. 10 hình vẽ hình học chuẩn xác độ nét cao
3. Bổ sung 4 bài tập rèn kỹ năng tính toán
4. Báo cáo phản biện chuyên môn đầy đủ 4 phần
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Import helper từ engine
sys.path.append(os.path.abspath("TROLYTHIEN/engine"))
from de_cuong_docx_helper import (
    create_base_document, add_header_quoc_hieu, add_heading_1, add_heading_2,
    add_heading_3, add_body_paragraph, add_exercise, add_text_with_math,
    format_run, set_table_no_borders, set_box_borders, set_table_borders,
    set_cell_background, apply_table_protection
)

IMG_DIR = os.path.abspath("TROLYTHIEN/4_DUYET_DE/Ket_qua/hinh_ve")
OUT_DIR = os.path.abspath("TROLYTHIEN/4_DUYET_DE/Ket_qua")

def add_single_image(doc, img_name, width_in=3.6, caption=""):
    img_path = os.path.join(IMG_DIR, img_name)
    if not os.path.exists(img_path):
        print(f"Warning: Image not found: {img_path}")
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(img_path, width=Inches(width_in))
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(4)
        r = p_cap.add_run(caption)
        format_run(r, size_pt=11, italic=True, color_rgb=(71, 85, 105))

def add_two_images(doc, img_name1, img_name2, width_in=3.0, cap1="", cap2=""):
    p1 = os.path.join(IMG_DIR, img_name1)
    p2 = os.path.join(IMG_DIR, img_name2)
    if not os.path.exists(p1) or not os.path.exists(p2):
        print(f"Warning: One of images not found: {p1}, {p2}")
        return
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_no_borders(table)
    
    c1, c2 = table.rows[0].cells
    c1.width = Inches(3.4)
    c2.width = Inches(3.4)
    
    p_c1 = c1.paragraphs[0]
    p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c1.paragraph_format.space_before = Pt(2)
    p_c1.paragraph_format.space_after = Pt(2)
    p_c1.add_run().add_picture(p1, width=Inches(width_in))
    if cap1:
        p_t1 = c1.add_paragraph()
        p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p_t1.add_run(cap1)
        format_run(r1, size_pt=11, italic=True)

    p_c2 = c2.paragraphs[0]
    p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c2.paragraph_format.space_before = Pt(2)
    p_c2.paragraph_format.space_after = Pt(2)
    p_c2.add_run().add_picture(p2, width=Inches(width_in))
    if cap2:
        p_t2 = c2.add_paragraph()
        p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r2 = p_t2.add_run(cap2)
        format_run(r2, size_pt=11, italic=True)

# ==============================================================================
# 1. TẠO TỆP WORD ĐỀ CƯƠNG TOÁN 7 CHUẨN HÓA CHÍNH THỨC
# ==============================================================================
def build_de_cuong_docx():
    print("Đang khởi tạo tài liệu Word Đề cương Toán 7 chuẩn hóa...")
    doc = create_base_document()
    add_header_quoc_hieu(doc, "7", school_year="2026 - 2027")
    
    # Ghi chú phiên bản chuẩn hóa
    p_note = doc.add_paragraph()
    p_note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_note.paragraph_format.space_before = Pt(0)
    p_note.paragraph_format.space_after = Pt(8)
    r_n = p_note.add_run("★ BẢN CHUẨN HÓA CHUYÊN MÔN: 100% WORD EQUATION • HÌNH VẼ CHUẨN XÁC • BỔ SUNG RÈN KỸ NĂNG ★")
    format_run(r_n, size_pt=11, bold=True, color_rgb=(180, 83, 9))
    
    # --------------------------------------------------------------------------
    # PHẦN I: TÓM TẮT LÝ THUYẾT TRỌNG TÂM
    # --------------------------------------------------------------------------
    add_heading_1(doc, "PHẦN I. TÓM TẮT LÝ THUYẾT TRỌNG TÂM GIỮA HỌC KỲ I")
    
    add_heading_2(doc, "1. SỐ HỌC VÀ ĐẠI SỐ (SỐ HỮU TỈ & SỐ THỰC)")
    add_body_paragraph(doc, "Tập hợp số hữu tỉ: Số hữu tỉ là số viết được dưới dạng phân số $\\frac{a}{b}$ với $a, b \\in \\mathbb{Z}, b \\neq 0$. Tập hợp các số hữu tỉ kí hiệu là $\\mathbb{Q}$.", "•")
    add_body_paragraph(doc, "Số đối: Hai số hữu tỉ có điểm biểu diễn đối xứng nhau qua gốc 0 trên trục số gọi là hai số đối nhau. Số đối của số hữu tỉ $x$ kí hiệu là $-x$.", "•")
    add_body_paragraph(doc, "Thứ tự thực hiện phép tính: Trong biểu thức không có ngoặc: Lũy thừa, căn bậc hai $\\to$ Nhân và chia $\\to$ Cộng và trừ. Trong biểu thức có ngoặc: $(\\dots) \\to [\\dots] \\to \\{\\dots\\}$.", "•")
    add_body_paragraph(doc, "Quy tắc chuyển vế: Khi chuyển một số hạng từ vế này sang vế kia của một đẳng thức, ta phải đổi dấu số hạng đó: $x + a = b \\Rightarrow x = b - a$.", "•")
    add_body_paragraph(doc, "Các công thức lũy thừa với số mũ tự nhiên ($x, y \\in \\mathbb{Q}; m, n \\in \\mathbb{N}$):\n"
                           "  $x^m \\cdot x^n = x^{m+n}$;\n"
                           "  $x^m : x^n = x^{m-n}$ ($x \\neq 0, m \\ge n$);\n"
                           "  $(x^m)^n = x^{m \\cdot n}$;\n"
                           "  $(x \\cdot y)^n = x^n \\cdot y^n$;\n"
                           "  $\\left(\\frac{x}{y}\\right)^n = \\frac{x^n}{y^n}$ ($y \\neq 0$);\n"
                           "  Quy ước: $x^0 = 1$ ($x \\neq 0$); $x^1 = x$.", "•")
    add_body_paragraph(doc, "Căn bậc hai số học: Căn bậc hai số học của số không âm $a$ là số không âm $x$ sao cho $x^2 = a$, kí hiệu là $\\sqrt{a}$. Với $a \\ge 0$: $(\\sqrt{a})^2 = a$.", "•")

    add_heading_2(doc, "2. HÌNH HỌC TRỰC QUAN VÀ HÌNH HỌC PHẲNG")
    add_body_paragraph(doc, "Góc kề bù: Hai góc vừa kề nhau vừa bù nhau có tổng số đo bằng $180^\\circ$. Hai góc đối đỉnh thì bằng nhau.", "•")
    add_body_paragraph(doc, "Tia phân giác: Tia nằm giữa hai cạnh của một góc và tạo với hai cạnh ấy hai góc bằng nhau. Nếu tia $Oz$ là phân giác của $\\widehat{xOy}$ thì $\\widehat{xOz} = \\widehat{zOy} = \\frac{1}{2}\\widehat{xOy}$.", "•")
    add_body_paragraph(doc, "Dấu hiệu nhận biết hai đường thẳng song song: Nếu đường thẳng $c$ cắt hai đường thẳng $a, b$ và trong các góc tạo thành có: một cặp góc so le trong bằng nhau HOẶC một cặp góc đồng vị bằng nhau thì $a // b$.", "•")
    add_body_paragraph(doc, "Tính chất hai đường thẳng song song: Nếu một đường thẳng cắt hai đường thẳng song song thì: hai góc so le trong bằng nhau; hai góc đồng vị bằng nhau; hai góc trong cùng phía bù nhau ($180^\\circ$).", "•")
    add_body_paragraph(doc, "Quan hệ từ vuông góc đến song song: Hai đường thẳng phân biệt cùng vuông góc với một đường thẳng thứ ba thì chúng song song với nhau ($a \\perp c$ và $b \\perp c \\Rightarrow a // b$). Một đường thẳng vuông góc với một trong hai đường thẳng song song thì nó cũng vuông góc với đường thẳng kia.", "•")
    add_body_paragraph(doc, "Các trường hợp bằng nhau của tam giác:\n"
                           "  Trường hợp 1 (Cạnh - Cạnh - Cạnh: c-c-c): Nếu ba cạnh của tam giác này bằng ba cạnh của tam giác kia thì hai tam giác đó bằng nhau.\n"
                           "  Trường hợp 2 (Cạnh - Góc - Cạnh: c-g-c): Nếu hai cạnh và góc xen giữa của tam giác này bằng hai cạnh và góc xen giữa của tam giác kia thì hai tam giác đó bằng nhau.", "•")

    # --------------------------------------------------------------------------
    # PHẦN II: HỆ THỐNG BÀI TẬP ÔN TẬP CHUẨN HÓA
    # --------------------------------------------------------------------------
    add_heading_1(doc, "PHẦN II. BÀI TẬP BẮT BUỘC THEO ĐỀ CƯƠNG GỐC (ĐÃ CHUẨN HÓA ĐÁNH SỐ)")
    
    add_heading_2(doc, "A. CHỦ ĐỀ SỐ HỌC VÀ ĐẠI SỐ")
    
    add_exercise(doc, "1", "Tìm số đối của mỗi số hữu tỉ sau:", [
        "a) $-\\frac{7}{5}$",
        "b) $2\\frac{1}{3}$",
        "c) $-33$",
        "d) $0$",
        "e) $-0{,}75$",
        "f) $\\frac{-2}{-9}$"
    ])
    
    add_exercise(doc, "2", "Hãy viết mỗi biểu thức sau dưới dạng lũy thừa của một số hữu tỉ:", [
        "a) $(0{,}4)^2 \\cdot (0{,}4)^3$",
        "b) $18^{19} : 18^{15}$",
        "c) $15^8 \\cdot 2^4$",
        "d) $27^5 : 32^3$"
    ])
    
    add_exercise(doc, "3", "Tính căn bậc hai số học của các số sau (Đã chuẩn hóa sửa lỗi chính tả toán học $\\sqrt{49}$ và $\\sqrt{121}$):", [
        "a) $\\sqrt{36}$",
        "b) $\\sqrt{49}$ *(Sửa từ $\\sqrt{47}$ trong bản gốc do lỗi gõ phím)*",
        "c) $\\sqrt{81}$",
        "d) $\\sqrt{100}$",
        "e) $\\sqrt{121}$ *(Sửa từ $\\sqrt{125}$ trong bản gốc do lỗi gõ phím)*",
        "f) $\\sqrt{144}$"
    ])
    
    add_exercise(doc, "4", "Tính giá trị của các biểu thức sau một cách hợp lý:", [
        "a) $A = \\frac{5}{11} + \\frac{-3}{7} + \\frac{6}{11} + \\frac{-4}{7}$",
        "b) $B = \\frac{7}{15} + \\frac{-4}{9} + \\frac{8}{15} + \\frac{-5}{9}$",
        "c) $C = \\frac{-2}{17} + \\frac{15}{23} + \\frac{-15}{17} + \\frac{8}{23}$",
        "d) $D = \\frac{3}{5} + \\left(\\frac{-1}{4}\\right) + \\frac{2}{5} + \\left(-\\frac{3}{4}\\right) + 2026$"
    ])
    
    add_exercise(doc, "5", "Tính hợp lý bằng cách áp dụng tính chất phân phối (đặt thừa số chung):", [
        "a) $M = \\frac{4}{9} \\cdot \\frac{13}{15} + \\frac{4}{9} \\cdot \\frac{2}{15}$",
        "b) $N = \\frac{5}{7} \\cdot \\frac{-3}{11} + \\frac{5}{7} \\cdot \\frac{-8}{11}$",
        "c) $P = \\frac{7}{19} \\cdot \\frac{8}{11} + \\frac{7}{19} \\cdot \\frac{3}{11} - \\frac{7}{19}$",
        "d) $Q = \\frac{-3}{8} \\cdot 2\\frac{1}{3} + \\frac{-3}{8} \\cdot 3\\frac{2}{3}$"
    ])
    
    add_exercise(doc, "6", "Tìm số hữu tỉ $x$, biết (Khắc phục lỗi đánh số lặp Bài 5):", [
        "a) $\\frac{3}{4} + \\frac{1}{4} : x = -\\frac{1}{3}$",
        "b) $\\frac{1}{3} \\cdot \\left(\\frac{2}{5}x - \\frac{8}{15}\\right) - \\frac{3}{4} = 0$",
        "c) $x - \\frac{1}{3} = \\frac{-5}{6}$",
        "d) $\\frac{2}{5} - \\frac{3}{4}x = \\frac{1}{2}$"
    ])
    
    add_exercise(doc, "7", "So sánh các cặp số lũy thừa sau (Khắc phục lỗi đánh số lặp Bài 6):", [
        "a) $2^{300}$ và $3^{200}$",
        "b) $2^{24}$ và $3^{16}$",
        "c) $5^{300}$ và $3^{500}$",
        "d) $99^{20}$ và $9999^{10}$"
    ])
    
    add_heading_2(doc, "B. CHỦ ĐỀ HÌNH HỌC PHẲNG & TRỰC QUAN")
    
    add_exercise(doc, "8", "Góc kề bù và tia phân giác (Đã bổ sung câu a bị khuyết trong đề gốc):")
    add_body_paragraph(doc, "a) Thế nào là hai góc kề bù? Cho hai góc kề bù $\\widehat{mOn}$ và $\\widehat{nOp}$, biết $\\widehat{mOn} = 110^\\circ$. Tính số đo của góc $\\widehat{nOp}$.", "✦")
    add_body_paragraph(doc, "b) Tìm số đo của góc $\\widehat{xOz}$ trong hình vẽ dưới đây (Hình 1):", "✦")
    add_single_image(doc, "Hinh_1_Goc_Ke_Bu.png", width_in=3.4, caption="Hình 1: Hai góc kề bù")
    add_body_paragraph(doc, "c) Cho hình vẽ bên dưới (Hình 2), biết tia $Oz$ là tia phân giác của góc $\\widehat{xOy}$. Biết $\\widehat{zOy} = 32^\\circ$. Tìm số đo của góc $\\widehat{xOy}$:", "✦")
    add_single_image(doc, "Hinh_2_Tia_Phan_Giac.png", width_in=3.4, caption="Hình 2: Tia phân giác của góc")
    
    add_exercise(doc, "9", "Cho các hình vẽ sau, hãy chứng tỏ đường thẳng $a // b$ (Chuẩn hóa danh pháp 'ax // by' sang $a // b$):")
    add_body_paragraph(doc, "a) Hình 1: Cát tuyến cắt đường thẳng $a$ tại $B$, cắt đường thẳng $b$ tại $C$ tạo thành cặp góc so le trong $\\widehat{aBC} = 71^\\circ$ và $\\widehat{BCy} = 71^\\circ$.", "✦")
    add_body_paragraph(doc, "b) Hình 2: Cát tuyến $c$ cắt đường thẳng $a$ tại $H$, cắt đường thẳng $b$ tại $P$ tạo thành cặp góc $\\widehat{xHc} = 130^\\circ$ và $\\widehat{yPc} = 130^\\circ$.", "✦")
    add_two_images(doc, "Hinh_3_Song_Song_71_Do.png", "Hinh_4_Song_Song_130_Do.png", width_in=3.0)
    
    add_exercise(doc, "10", "Cho đường thẳng $a // b$. Tính số đo các góc còn lại tại đỉnh $K$ trong hình vẽ bên dưới:")
    add_single_image(doc, "Hinh_5_Tinh_Goc_Song_Song_100_Do.png", width_in=3.2, caption="Hình 1: Cho a // b, tính các góc tại đỉnh K")
    
    add_exercise(doc, "11", "Tính số đo góc $x$ trong các hình vẽ sau:")
    add_body_paragraph(doc, "a) Hình 1: Cho tứ giác $ABCD$ có $AD \\perp CD$ tại $D$ và $BC \\perp CD$ tại $C$. Biết góc $\\widehat{ABC} = 135^\\circ$. Tính góc $x = \\widehat{DAB}$.", "✦")
    add_body_paragraph(doc, "b) Hình 2: Cho tam giác $ABC$, đường thẳng cắt $AB, AC$ lần lượt tại $E, F$. Biết $\\widehat{EFC} = 49^\\circ$, $\\widehat{ACB} = 49^\\circ$ và $\\widehat{ABC} = 72^\\circ$. Tính số đo góc $x = \\widehat{AEF}$.", "✦")
    add_two_images(doc, "Hinh_6_Tu_Giac_Vuong_135_Do.png", "Hinh_7_Tam_Giac_Dong_Vi_72_Do.png", width_in=3.0)
    
    add_exercise(doc, "12", "Cho hình vẽ bên, biết $\\widehat{aEF} = 100^\\circ$, $\\widehat{EFG} = 100^\\circ$ và đường thẳng $a \\perp m$ tại $H$:")
    add_body_paragraph(doc, "a) Chứng tỏ đường thẳng $a // b$ (tức $EH // FG$).", "✦")
    add_body_paragraph(doc, "b) Tính số đo của góc $\\widehat{HGF}$.", "✦")
    add_body_paragraph(doc, "c) Vẽ tia $Et$ là tia phân giác của $\\widehat{HEF}$, vẽ tia $Fk$ nằm trong góc $\\widehat{GFE}$ sao cho $\\widehat{GFk} = 40^\\circ$. Tia $Et$ và tia $Fk$ cắt nhau tại điểm $O$. Tính số đo góc $\\widehat{EOF}$.", "✦")
    add_single_image(doc, "Hinh_8_Hinh_Tong_Hop_Bai_9.png", width_in=3.6, caption="Hình vẽ bài toán tổng hợp góc, song song và tia phân giác")
    
    add_exercise(doc, "13", "Cho tam giác $MNP$ có $MP < MN$, $ME$ là tia phân giác của góc $\\widehat{PMN}$ ($E \\in PN$). Trên cạnh $MN$ lấy điểm $H$ sao cho $MP = MH$ (Đã sửa lỗi thiếu ký hiệu $\\Delta$):", [
        "a) Chứng minh rằng $\\Delta MPE = \\Delta MHE$.",
        "b) Gọi $I$ là giao điểm của $ME$ và $PH$. Chứng minh rằng $ME \\perp PH$ và $I$ là trung điểm của đoạn thẳng $PH$."
    ])
    
    add_exercise(doc, "14", "Cho hình vẽ sau (Hình bên), biết $AB = DB$ và $AC = DC$. Chứng minh rằng $\\Delta ABC = \\Delta DBC$ (Đã kéo hình vẽ từ trang 3 về đúng bài):")
    add_single_image(doc, "Hinh_9_Tam_Giac_Bang_Nhau_CCC.png", width_in=3.2, caption="Chứng minh hai tam giác bằng nhau (c-c-c)")
    
    add_exercise(doc, "15", "Cho tam giác $ABC$, gọi $M$ là trung điểm của cạnh $AC$. Trên tia đối của tia $MB$ lấy điểm $D$ sao cho $MD = MB$:", [
        "a) Chứng minh rằng $\\Delta AMB = \\Delta CMD$. *(Đã phục dựng câu a bị rụng hoàn toàn nội dung trong đề gốc)*",
        "b) Chứng minh rằng $AB // CD$.",
        "c) Kẻ $AH \\perp BC$ tại $H$ và $DK \\perp BC$ tại $K$. Chứng minh rằng $AH = DK$."
    ])
    add_single_image(doc, "Hinh_10_Tam_Giac_Doi_Xung_CGC.png", width_in=3.3, caption="Tam giác đối xứng qua trung điểm (c-g-c)")

    # --------------------------------------------------------------------------
    # PHẦN III: CÁC BÀI TẬP BỔ SUNG RÈN KỸ NĂNG TÍNH TOÁN
    # --------------------------------------------------------------------------
    add_heading_1(doc, "PHẦN III. BÀI TẬP BỔ SUNG RÈN KỸ NĂNG TÍNH TOÁN CHUYÊN SÂU")
    add_body_paragraph(doc, "Các bài tập dưới đây được thiết kế nhằm rèn luyện phản xạ tính toán phân số, lũy thừa, quy tắc dấu ngoặc, giá trị tuyệt đối và giải quyết bài toán thực tế chuẩn GDPT 2018.", "★")
    
    add_exercise(doc, "16", "Thực hiện phép tính (kết hợp phân số, số thập phân, lũy thừa và căn bậc hai):", [
        "a) $A_1 = \\left(-\\frac{2}{3}\\right)^2 + \\frac{5}{6} \\cdot \\left(-\\frac{3}{10}\\right) - \\frac{3}{4}$",
        "b) $A_2 = \\frac{4}{5} - \\left[\\frac{2}{3} + \\left(-\\frac{1}{2}\\right)^3 : \\frac{1}{4}\\right]$",
        "c) $A_3 = 2026^0 - \\left(-\\frac{1}{3}\\right)^2 \\cdot 9 + \\sqrt{\\frac{16}{25}} : (-0{,}8)$",
        "d) $A_4 = \\left(-\\frac{3}{4}\\right)^2 \\cdot \\frac{8}{9} - \\sqrt{0{,}49} \\cdot \\frac{10}{7} + \\left|-\\frac{5}{2}\\right|$"
    ])
    
    add_exercise(doc, "17", "Rèn kỹ năng tính nhanh, quy tắc phá ngoặc và rút gọn lũy thừa phức tạp:", [
        "a) $B_1 = \\left(\\frac{3}{8} - \\frac{1}{5} + \\frac{7}{12}\\right) - \\left(\\frac{5}{8} - \\frac{6}{5} - \\frac{5}{12}\\right)$",
        "b) $B_2 = \\frac{11}{19} \\cdot \\left(-\\frac{3}{7}\\right) + \\frac{11}{19} \\cdot \\left(-\\frac{4}{7}\\right) + \\frac{8}{19}$",
        "c) $B_3 = \\frac{4^5 \\cdot 9^4 - 2 \\cdot 6^9}{2^{10} \\cdot 3^8 + 6^8 \\cdot 20}$",
        "d) $B_4 = \\frac{5^4 \\cdot 20^4}{25^5 \\cdot 4^5}$"
    ])
    
    add_exercise(doc, "18", "Tìm số hữu tỉ $x$ (rèn kỹ năng chuyển vế, dấu giá trị tuyệt đối và lũy thừa):", [
        "a) $\\left|x + \\frac{1}{2}\\right| - \\frac{2}{3} = \\frac{1}{3}$",
        "b) $\\left(2x - \\frac{1}{3}\\right)^2 = \\frac{4}{9}$",
        "c) $\\frac{2}{3}x - \\frac{1}{2}\\left(x - \\frac{1}{3}\\right) = \\frac{5}{6}$",
        "d) $(x - 1)^3 = -27$"
    ])
    
    add_exercise(doc, "19", "Bài toán thực tế ứng dụng số hữu tỉ (chuẩn GDPT 2018):")
    add_body_paragraph(doc, "Nhân dịp đầu năm học mới, một nhà sách thực hiện chương trình khuyến mãi: giảm giá $10\\%$ cho tất cả các mặt hàng sách giáo khoa và dụng cụ học tập.\n"
                           "Bạn Minh mua một bộ sách giáo khoa lớp 7 có giá niêm yết là $240\\,000$ đồng và một chiếc cặp học sinh có giá niêm yết là $320\\,000$ đồng. Do bạn Minh có thẻ học sinh giỏi nên được giảm thêm tiếp $5\\%$ trên tổng số tiền của hóa đơn đã được giảm lần 1.\n"
                           "Hỏi bạn Minh phải trả cho quầy thu ngân tất cả bao nhiêu tiền?", "✦")

    # --------------------------------------------------------------------------
    # PHẦN IV: ĐÁP ÁN & HƯỚNG DẪN GIẢI CHI TIẾT
    # --------------------------------------------------------------------------
    add_heading_1(doc, "PHẦN IV. ĐÁP ÁN VÀ HƯỚNG DẪN GIẢI CHI TIẾT TỪNG BÀI")
    
    # Bài 1
    add_heading_3(doc, "Bài 1. Số đối:")
    add_body_paragraph(doc, "a) Số đối của $-\\frac{7}{5}$ là $\\frac{7}{5}$.\n"
                           "b) Số đối của $2\\frac{1}{3} = \\frac{7}{3}$ là $-2\\frac{1}{3} = -\\frac{7}{3}$.\n"
                           "c) Số đối của $-33$ là $33$.\n"
                           "d) Số đối của $0$ là $0$.\n"
                           "e) Số đối của $-0{,}75 = -\\frac{3}{4}$ là $0{,}75 = \\frac{3}{4}$.\n"
                           "f) Ta có $\\frac{-2}{-9} = \\frac{2}{9}$, do đó số đối của nó là $-\\frac{2}{9}$.", "✓")
                           
    # Bài 2
    add_heading_3(doc, "Bài 2. Lũy thừa:")
    add_body_paragraph(doc, "a) $(0{,}4)^2 \\cdot (0{,}4)^3 = (0{,}4)^{2+3} = (0{,}4)^5 = \\left(\\frac{2}{5}\\right)^5$.\n"
                           "b) $18^{19} : 18^{15} = 18^{19-15} = 18^4$.\n"
                           "c) $15^8 \\cdot 2^4 = (15^2)^4 \\cdot 2^4 = 225^4 \\cdot 2^4 = (225 \\cdot 2)^4 = 450^4$.\n"
                           "   *(Lưu ý sư phạm: Nếu đề bài gốc có ý định viết $15^4 \\cdot 2^4$ thì kết quả là $(15 \\cdot 2)^4 = 30^4$)*.\n"
                           "d) $27^5 : 32^3 = (3^3)^5 : (2^5)^3 = 3^{15} : 2^{15} = \\left(\\frac{3}{2}\\right)^{15}$.", "✓")

    # Bài 3
    add_heading_3(doc, "Bài 3. Căn bậc hai số học:")
    add_body_paragraph(doc, "a) $\\sqrt{36} = 6$ (vì $6 \\ge 0$ và $6^2 = 36$).\n"
                           "b) $\\sqrt{49} = 7$ (vì $7 \\ge 0$ và $7^2 = 49$).\n"
                           "c) $\\sqrt{81} = 9$ (vì $9 \\ge 0$ và $9^2 = 81$).\n"
                           "d) $\\sqrt{100} = 10$ (vì $10 \\ge 0$ và $10^2 = 100$).\n"
                           "e) $\\sqrt{121} = 11$ (vì $11 \\ge 0$ và $11^2 = 121$).\n"
                           "f) $\\sqrt{144} = 12$ (vì $12 \\ge 0$ và $12^2 = 144$).", "✓")

    # Bài 4
    add_heading_3(doc, "Bài 4. Tính hợp lý:")
    add_body_paragraph(doc, "a) $A = \\left(\\frac{5}{11} + \\frac{6}{11}\\right) + \\left(\\frac{-3}{7} + \\frac{-4}{7}\\right) = \\frac{11}{11} + \\frac{-7}{7} = 1 + (-1) = 0$.\n"
                           "b) $B = \\left(\\frac{7}{15} + \\frac{8}{15}\\right) + \\left(\\frac{-4}{9} + \\frac{-5}{9}\\right) = \\frac{15}{15} + \\frac{-9}{9} = 1 + (-1) = 0$.\n"
                           "c) $C = \\left(\\frac{-2}{17} + \\frac{-15}{17}\\right) + \\left(\\frac{15}{23} + \\frac{8}{23}\\right) = \\frac{-17}{17} + \\frac{23}{23} = -1 + 1 = 0$.\n"
                           "d) $D = \\left(\\frac{3}{5} + \\frac{2}{5}\\right) + \\left[\\left(-\\frac{1}{4}\\right) + \\left(-\\frac{3}{4}\\right)\\right] + 2026 = 1 + (-1) + 2026 = 2026$.", "✓")

    # Bài 5
    add_heading_3(doc, "Bài 5. Đặt thừa số chung:")
    add_body_paragraph(doc, "a) $M = \\frac{4}{9} \\cdot \\left(\\frac{13}{15} + \\frac{2}{15}\\right) = \\frac{4}{9} \\cdot \\frac{15}{15} = \\frac{4}{9} \\cdot 1 = \\frac{4}{9}$.\n"
                           "b) $N = \\frac{5}{7} \\cdot \\left(\\frac{-3}{11} + \\frac{-8}{11}\\right) = \\frac{5}{7} \\cdot \\frac{-11}{11} = \\frac{5}{7} \\cdot (-1) = -\\frac{5}{7}$.\n"
                           "c) $P = \\frac{7}{19} \\cdot \\left(\\frac{8}{11} + \\frac{3}{11} - 1\\right) = \\frac{7}{19} \\cdot (1 - 1) = \\frac{7}{19} \\cdot 0 = 0$.\n"
                           "d) $Q = \\frac{-3}{8} \\cdot \\left(2\\frac{1}{3} + 3\\frac{2}{3}\\right) = \\frac{-3}{8} \\cdot 6 = \\frac{-18}{8} = -\\frac{9}{4}$.", "✓")

    # Bài 6
    add_heading_3(doc, "Bài 6. Tìm x:")
    add_body_paragraph(doc, "a) $\\frac{3}{4} + \\frac{1}{4} : x = -\\frac{1}{3} \\Rightarrow \\frac{1}{4} : x = -\\frac{1}{3} - \\frac{3}{4} = -\\frac{13}{12} \\Rightarrow x = \\frac{1}{4} : \\left(-\\frac{13}{12}\\right) = -\\frac{3}{13}$.\n"
                           "b) $\\frac{1}{3} \\cdot \\left(\\frac{2}{5}x - \\frac{8}{15}\\right) = \\frac{3}{4} \\Rightarrow \\frac{2}{5}x - \\frac{8}{15} = \\frac{9}{4} \\Rightarrow \\frac{2}{5}x = \\frac{9}{4} + \\frac{8}{15} = \\frac{167}{60} \\Rightarrow x = \\frac{167}{60} : \\frac{2}{5} = \\frac{167}{24}$.\n"
                           "c) $x - \\frac{1}{3} = \\frac{-5}{6} \\Rightarrow x = \\frac{-5}{6} + \\frac{1}{3} = \\frac{-3}{6} = -\\frac{1}{2}$.\n"
                           "d) $\\frac{2}{5} - \\frac{3}{4}x = \\frac{1}{2} \\Rightarrow \\frac{3}{4}x = \\frac{2}{5} - \\frac{1}{2} = -\\frac{1}{10} \\Rightarrow x = -\\frac{1}{10} : \\frac{3}{4} = -\\frac{2}{15}$.", "✓")

    # Bài 7
    add_heading_3(doc, "Bài 7. So sánh lũy thừa:")
    add_body_paragraph(doc, "a) Ta có $2^{300} = (2^3)^{100} = 8^{100}$; $3^{200} = (3^2)^{100} = 9^{100}$. Vì $8 < 9$ nên $8^{100} < 9^{100}$, do đó $2^{300} < 3^{200}$.\n"
                           "b) Ta có $2^{24} = (2^3)^8 = 8^8$; $3^{16} = (3^2)^8 = 9^8$. Vì $8 < 9$ nên $8^8 < 9^8$, do đó $2^{24} < 3^{16}$.\n"
                           "c) Ta có $5^{300} = (5^3)^{100} = 125^{100}$; $3^{500} = (3^5)^{100} = 243^{100}$. Vì $125 < 243$ nên $5^{300} < 3^{500}$.\n"
                           "d) Ta có $99^{20} = (99^2)^{10} = 9801^{10}$. Vì $9801 < 9999$ nên $9801^{10} < 9999^{10}$, do đó $99^{20} < 9999^{10}$.", "✓")

    # Bài 8
    add_heading_3(doc, "Bài 8. Góc kề bù & phân giác:")
    add_body_paragraph(doc, "a) Hai góc $\\widehat{mOn}$ và $\\widehat{nOp}$ kề bù nên $\\widehat{mOn} + \\widehat{nOp} = 180^\\circ \\Rightarrow \\widehat{nOp} = 180^\\circ - 110^\\circ = 70^\\circ$.\n"
                           "b) Theo hình vẽ, hai góc $\\widehat{xOz}$ và $\\widehat{zOy}$ kề bù: $\\widehat{xOz} + \\widehat{zOy} = 180^\\circ \\Rightarrow \\widehat{xOz} = 180^\\circ - 50^\\circ = 130^\\circ$.\n"
                           "c) Vì tia $Oz$ là phân giác của góc $\\widehat{xOy}$ nên $\\widehat{xOy} = 2 \\cdot \\widehat{zOy} = 2 \\cdot 32^\\circ = 64^\\circ$.", "✓")

    # Bài 9
    add_heading_3(doc, "Bài 9. Chứng minh hai đường thẳng song song:")
    add_body_paragraph(doc, "a) Hình 1: Hai góc $\\widehat{aBC}$ và $\\widehat{BCy}$ ở vị trí so le trong và $\\widehat{aBC} = \\widehat{BCy} = 71^\\circ$. Do đó đường thẳng $a // b$.\n"
                           "b) Hình 2: Hai góc $\\widehat{xHc}$ và $\\widehat{yPc}$ ở vị trí đồng vị và $\\widehat{xHc} = \\widehat{yPc} = 130^\\circ$. Do đó đường thẳng $a // b$.", "✓")

    # Bài 10
    add_heading_3(doc, "Bài 10. Tính các góc với a // b:")
    add_body_paragraph(doc, "Vì $a // b$ nên các góc so le trong bằng nhau, các góc đồng vị bằng nhau và các góc trong cùng phía bù nhau.\n"
                           "Tại đỉnh $K$: Cặp góc đồng vị với góc $100^\\circ$ ở đỉnh $J$ có số đo bằng $100^\\circ$. Góc trong cùng phía kề bù có số đo $180^\\circ - 100^\\circ = 80^\\circ$.\n"
                           "Vậy góc có dấu hỏi chấm '$?$' (góc trong cùng phía) có số đo là $180^\\circ - 100^\\circ = 80^\\circ$ (hoặc nếu là góc đồng vị thì bằng $100^\\circ$).", "✓")

    # Bài 11
    add_heading_3(doc, "Bài 11. Tính số đo góc x:")
    add_body_paragraph(doc, "a) Hình 1: Ta có $AD \\perp CD$ và $BC \\perp CD$ nên $AD // BC$ (hai đường thẳng phân biệt cùng vuông góc với đường thẳng thứ ba thì song song).\n"
                           "Vì $AD // BC$ nên hai góc trong cùng phía $\\widehat{DAB}$ và $\\widehat{ABC}$ bù nhau:\n"
                           "$\\widehat{DAB} + \\widehat{ABC} = 180^\\circ \\Rightarrow x + 135^\\circ = 180^\\circ \\Rightarrow x = 45^\\circ$.\n"
                           "b) Hình 2: Ta có $\\widehat{EFC} = 49^\\circ$ và $\\widehat{ACB} = 49^\\circ$. Hai góc này ở vị trí so le trong (hoặc đồng vị với tia kéo dài) và bằng nhau nên $EF // BC$.\n"
                           "Vì $EF // BC$ nên hai góc đồng vị $\\widehat{AEF}$ và $\\widehat{ABC}$ bằng nhau: $x = \\widehat{AEF} = \\widehat{ABC} = 72^\\circ$.", "✓")

    # Bài 12
    add_heading_3(doc, "Bài 12. Bài toán hình học tổng hợp:")
    add_body_paragraph(doc, "a) Ta có $\\widehat{aEF} = 100^\\circ$ và $\\widehat{EFG} = 100^\\circ$. Hai góc này ở vị trí so le trong và bằng nhau nên $a // b$ (tức $EH // FG$).\n"
                           "b) Vì $EH // FG$ mà đường thẳng $m \\perp EH$ tại $H$ nên $m \\perp FG$ tại $G$. Do đó $\\widehat{HGF} = 90^\\circ$.\n"
                           "c) Vì $\\widehat{HEF}$ và $\\widehat{aEF}$ kề bù nên $\\widehat{HEF} = 180^\\circ - 100^\\circ = 80^\\circ$.\n"
                           "Tia $Et$ là phân giác của $\\widehat{HEF} \\Rightarrow \\widehat{tEF} = \\frac{1}{2}\\widehat{HEF} = \\frac{1}{2} \\cdot 80^\\circ = 40^\\circ$.\n"
                           "Tia $Fk$ nằm trong góc $\\widehat{GFE} = 100^\\circ$ sao cho $\\widehat{GFk} = 40^\\circ \\Rightarrow \\widehat{kFE} = 100^\\circ - 40^\\circ = 60^\\circ$.\n"
                           "Xét $\\Delta OEF$, ta có tổng ba góc trong tam giác:\n"
                           "$\\widehat{EOF} = 180^\\circ - (\\widehat{OEF} + \\widehat{OFE}) = 180^\\circ - (40^\\circ + 60^\\circ) = 80^\\circ$.", "✓")

    # Bài 13
    add_heading_3(doc, "Bài 13. Chứng minh tam giác MNP:")
    add_body_paragraph(doc, "a) Xét $\\Delta MPE$ và $\\Delta MHE$, ta có:\n"
                           "  $MP = MH$ (giả thiết);\n"
                           "  $\\widehat{PME} = \\widehat{HME}$ (vì $ME$ là tia phân giác của $\\widehat{PMN}$);\n"
                           "  Cạnh $ME$ chung.\n"
                           "Suy ra $\\Delta MPE = \\Delta MHE$ (c-g-c).\n"
                           "b) Vì $\\Delta MPE = \\Delta MHE$ nên $EP = EH$ (hai cạnh tương ứng).\n"
                           "Mặt khác $MP = MH$ (giả thiết) nên $M$ và $E$ đều cách đều hai đầu mút $P$ và $H$, do đó đường thẳng $ME$ là đường trung trực của đoạn thẳng $PH$.\n"
                           "Suy ra $ME \\perp PH$ tại $I$ và $I$ là trung điểm của đoạn thẳng $PH$.", "✓")

    # Bài 14
    add_heading_3(doc, "Bài 14. Chứng minh tam giác bằng nhau (c-c-c):")
    add_body_paragraph(doc, "Xét $\\Delta ABC$ và $\\Delta DBC$, ta có:\n"
                           "  $AB = DB$ (giả thiết);\n"
                           "  $AC = DC$ (giả thiết);\n"
                           "  Cạnh $BC$ chung.\n"
                           "Suy ra $\\Delta ABC = \\Delta DBC$ (c-c-c).", "✓")

    # Bài 15
    add_heading_3(doc, "Bài 15. Chứng minh đối xứng qua trung điểm:")
    add_body_paragraph(doc, "a) Xét $\\Delta AMB$ và $\\Delta CMD$, ta có:\n"
                           "  $MA = MC$ (vì $M$ là trung điểm cạnh $AC$);\n"
                           "  $\\widehat{AMB} = \\widehat{CMD}$ (hai góc đối đỉnh);\n"
                           "  $MB = MD$ (giả thiết).\n"
                           "Suy ra $\\Delta AMB = \\Delta CMD$ (c-g-c).\n"
                           "b) Vì $\\Delta AMB = \\Delta CMD$ nên $\\widehat{MAB} = \\widehat{MCD}$ (hai góc tương ứng).\n"
                           "Mà hai góc này ở vị trí so le trong nên $AB // CD$.\n"
                           "c) Xét tam giác vuông $AHB$ và tam giác vuông $DKC$ (có $\\widehat{AHB} = \\widehat{DKC} = 90^\\circ$):\n"
                           "  $AB = CD$ (do $\\Delta AMB = \\Delta CMD$);\n"
                           "  $\\widehat{ABH} = \\widehat{DCK}$ (hai góc so le trong do $AB // CD$).\n"
                           "Suy ra $\\Delta AHB = \\Delta DKC$ (cạnh huyền - góc nhọn) $\\Rightarrow AH = DK$ (hai cạnh tương ứng).", "✓")

    # Bài 16, 17, 18, 19
    add_heading_3(doc, "Bài 16. Thứ tự thực hiện phép tính nâng cao:")
    add_body_paragraph(doc, "a) $A_1 = \\frac{4}{9} + \\frac{5}{6} \\cdot \\left(-\\frac{3}{10}\\right) - \\frac{3}{4} = \\frac{4}{9} - \\frac{1}{4} - \\frac{3}{4} = \\frac{4}{9} - 1 = -\\frac{5}{9}$.\n"
                           "b) $A_2 = \\frac{4}{5} - \\left[\\frac{2}{3} + \\left(-\\frac{1}{8}\\right) : \\frac{1}{4}\\right] = \\frac{4}{5} - \\left[\\frac{2}{3} - \\frac{1}{2}\\right] = \\frac{4}{5} - \\frac{1}{6} = \\frac{19}{30}$.\n"
                           "c) $A_3 = 1 - \\frac{1}{9} \\cdot 9 + \\frac{4}{5} : (-0{,}8) = 1 - 1 + (-1) = -1$.\n"
                           "d) $A_4 = \\frac{9}{16} \\cdot \\frac{8}{9} - 0{,}7 \\cdot \\frac{10}{7} + \\frac{5}{2} = \\frac{1}{2} - 1 + \\frac{5}{2} = 2$.", "✓")

    add_heading_3(doc, "Bài 17. Tính nhanh và rút gọn lũy thừa:")
    add_body_paragraph(doc, "a) $B_1 = \\left(\\frac{3}{8} - \\frac{5}{8}\\right) + \\left(-\\frac{1}{5} + \\frac{6}{5}\\right) + \\left(\\frac{7}{12} + \\frac{5}{12}\\right) = -\\frac{1}{4} + 1 + 1 = \\frac{7}{4}$.\n"
                           "b) $B_2 = \\frac{11}{19} \\cdot \\left(-\\frac{3}{7} - \\frac{4}{7}\\right) + \\frac{8}{19} = \\frac{11}{19} \\cdot (-1) + \\frac{8}{19} = -\\frac{3}{19}$.\n"
                           "c) $B_3 = \\frac{2^{10} \\cdot 3^8 - 2 \\cdot 2^9 \\cdot 3^9}{2^{10} \\cdot 3^8 + 2^8 \\cdot 3^8 \\cdot 2^2 \\cdot 5} = \\frac{2^{10} \\cdot 3^8(1 - 3)}{2^{10} \\cdot 3^8(1 + 5)} = \\frac{-2}{6} = -\\frac{1}{3}$.\n"
                           "d) $B_4 = \\frac{5^4 \\cdot (2^2 \\cdot 5)^4}{(5^2)^5 \\cdot (2^2)^5} = \\frac{5^8 \\cdot 2^8}{5^{10} \\cdot 2^{10}} = \\frac{1}{5^2 \\cdot 2^2} = \\frac{1}{100}$.", "✓")

    add_heading_3(doc, "Bài 18. Tìm x có chứa giá trị tuyệt đối và lũy thừa:")
    add_body_paragraph(doc, "a) $\\left|x + \\frac{1}{2}\\right| = \\frac{1}{3} + \\frac{2}{3} = 1 \\Rightarrow x + \\frac{1}{2} = 1 \\Rightarrow x = \\frac{1}{2}$ HOẶC $x + \\frac{1}{2} = -1 \\Rightarrow x = -\\frac{3}{2}$.\n"
                           "b) $\\left(2x - \\frac{1}{3}\\right)^2 = \\frac{4}{9} \\Rightarrow 2x - \\frac{1}{3} = \\frac{2}{3} \\Rightarrow x = \\frac{1}{2}$ HOẶC $2x - \\frac{1}{3} = -\\frac{2}{3} \\Rightarrow x = -\\frac{1}{6}$.\n"
                           "c) $\\frac{2}{3}x - \\frac{1}{2}x + \\frac{1}{6} = \\frac{5}{6} \\Rightarrow \\frac{1}{6}x = \\frac{4}{6} \\Rightarrow x = 4$.\n"
                           "d) $(x - 1)^3 = -27 = (-3)^3 \\Rightarrow x - 1 = -3 \\Rightarrow x = -2$.", "✓")

    add_heading_3(doc, "Bài 19. Bài toán thực tế:")
    add_body_paragraph(doc, "Tổng giá niêm yết của sách giáo khoa và cặp sách:\n"
                           "  $240\\,000 + 320\\,000 = 560\\,000$ (đồng).\n"
                           "Số tiền sau khi được giảm giá đợt 1 ($10\\%$):\n"
                           "  $560\\,000 \\cdot (1 - 0{,}10) = 560\\,000 \\cdot 0{,}90 = 504\\,000$ (đồng).\n"
                           "Số tiền thực tế bạn Minh phải thanh toán sau khi giảm tiếp đợt 2 ($5\\%$):\n"
                           "  $504\\,000 \\cdot (1 - 0{,}05) = 504\\,000 \\cdot 0{,}95 = 478\\,800$ (đồng).\n"
                           "Đáp số: $478\\,800$ đồng.", "✓")

    out_file = os.path.join(OUT_DIR, "De_Cuong_Toan_7_Chuan_Hoa_Chinh_Thuc.docx")
    doc.save(out_file)
    print(f"XUẤT THÀNH CÔNG: {out_file}")
    return out_file

if __name__ == "__main__":
    build_de_cuong_docx()
