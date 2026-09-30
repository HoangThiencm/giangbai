with open(r"TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html", "r", encoding="utf-8") as f:
    html = f.read()

h1_pos = html.find('KHỞI ĐỘNG — TÌNH HUỐNG THỰC TẾ')
print(html[h1_pos-500:h1_pos])
