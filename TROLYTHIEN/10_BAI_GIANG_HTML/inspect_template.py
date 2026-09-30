import re

with open(r"TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html", "r", encoding="utf-8") as f:
    html = f.read()

print("HTML Length:", len(html))

# Extract style
style_match = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
if style_match:
    style_content = style_match.group(1)
    print("Style length:", len(style_content))
    with open("TROLYTHIEN/10_BAI_GIANG_HTML/template_style.css", "w", encoding="utf-8") as sf:
        sf.write(style_content)

# Extract script
script_matches = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL)
print("Scripts count:", len(script_matches))
for i, s in enumerate(script_matches):
    print(f"Script {i+1} len: {len(s)}")
    if len(s) > 500:
        with open(f"TROLYTHIEN/10_BAI_GIANG_HTML/template_script_{i+1}.js", "w", encoding="utf-8") as sf:
            sf.write(s)

# Extract 1 sample slide
slide_match = re.search(r"(<div[^>]*class=\"slide-item.*?)(?=<div[^>]*class=\"slide-item|</div>\s*</div>\s*<div class=\"present-toolbar)", html, re.DOTALL)
if slide_match:
    print("Found slide sample len:", len(slide_match.group(1)))
    with open("TROLYTHIEN/10_BAI_GIANG_HTML/sample_slide.html", "w", encoding="utf-8") as sf:
        sf.write(slide_match.group(1)[:3000])

print("Extracted template info.")
