import re

with open(r"TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find all slides
slide_pattern = re.compile(r'<div class="slide-item[^"]*"[^>]*data-slide-id="([^"]*)"[^>]*>(.*?)</div>\s*<!-- END SLIDE', re.DOTALL)
matches = slide_pattern.findall(html)
print(f"Total slides found with comment marker: {len(matches)}")

if len(matches) == 0:
    # Alternative pattern
    slide_pattern2 = re.compile(r'(<div class="slide-item[^"]*"[^>]*data-slide-id="([^"]*)".*?)(?=(?:<div class="slide-item|$))', re.DOTALL)
    matches2 = slide_pattern2.findall(html)
    print(f"Total slides with pattern 2: {len(matches2)}")
    for i, (full, sid) in enumerate(matches2):
        title = re.search(r'class="slide-heading-text">([^<]*)<', full)
        t_text = title.group(1) if title else "No title"
        print(f"Slide {i+1} [ID: {sid}]: {t_text}")
else:
    for i, (sid, content) in enumerate(matches):
        title = re.search(r'class="slide-heading-text">([^<]*)<', content)
        t_text = title.group(1) if title else "No title"
        print(f"Slide {i+1} [ID: {sid}]: {t_text}")
