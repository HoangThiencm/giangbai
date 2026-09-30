import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html", "r", encoding="utf-8") as f:
    html = f.read()

h1_pos = html.find('KHỞI ĐỘNG — TÌNH HUỐNG THỰC TẾ')
h2_pos = html.find('1. PHƯƠNG TRÌNH TÍCH — HOẠT ĐỘNG KHÁM PHÁ')

# find slide container start
slide_start = html.rfind('<section', 0, h1_pos)
if slide_start == -1:
    slide_start = html.rfind('<div', 0, h1_pos - 100)

slide2_start = html.rfind('<section', 0, h2_pos)
if slide2_start == -1:
    slide2_start = html.rfind('<div', 0, h2_pos - 100)

slide_1_html = html[slide_start:slide2_start]
with open("TROLYTHIEN/10_BAI_GIANG_HTML/slide_1_sample.html", "w", encoding="utf-8") as sf:
    sf.write(slide_1_html)

print("Slide 1 saved. Start index:", slide_start, "End index:", slide2_start)
print("First 200 chars of slide 1:")
print(slide_1_html[:200])
