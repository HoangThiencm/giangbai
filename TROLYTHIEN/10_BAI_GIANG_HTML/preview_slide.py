import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open(r"TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find slides by splitting on slide boundaries or finding the slide container
# Let's inspect around Heading 1
h1_pos = html.find('KHỞI ĐỘNG — TÌNH HUỐNG THỰC TẾ')
slide1_start = html.rfind('<div class="slide-item', 0, h1_pos)
slide2_pos = html.find('1. PHƯƠNG TRÌNH TÍCH — HOẠT ĐỘNG KHÁM PHÁ')
slide2_start = html.rfind('<div class="slide-item', 0, slide2_pos)

print("Slide 1 content preview:")
print(html[slide1_start:slide2_start])
