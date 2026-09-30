import re

with open(r"TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's search for slide tags
slides = re.findall(r'<div[^>]*class="[^"]*slide[^"]*"[^>]*>', html)
print("Slide tags count:", len(slides))
for s in slides[:10]:
    print(s)
