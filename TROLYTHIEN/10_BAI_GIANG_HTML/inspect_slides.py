import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open(r"TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html", "r", encoding="utf-8") as f:
    html = f.read()

deck_pos = html.find('id="slideDeck"')
print("Found slideDeck at:", deck_pos)
deck_substr = html[deck_pos:deck_pos+5000]

# Let's find tags directly under slideDeck
# Check for <section or <div or whatever is used for slides
items = re.findall(r'<([a-zA-Z0-9]+)[^>]*class="([^"]*)"[^>]*data-slide-id="([^"]*)"', html)
print("Items with data-slide-id:", len(items))
for tag, cls, sid in items:
    print(f"Tag: <{tag}>, class='{cls}', data-slide-id='{sid}'")

headings = re.findall(r'class="slide-heading-text">([^<]*)</span>', html)
print("Headings found:", len(headings))
for i, h in enumerate(headings):
    print(f"Heading {i+1}: {h}")
