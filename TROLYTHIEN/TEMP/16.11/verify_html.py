import re

path = r"TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/16.11/Toan_6_Bai_21_Hinh_Co_Truc_Doi_Xung.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

print("File size:", len(html))
print("Has iff:", bool(re.search(r"(\\iff|\\Leftrightarrow|<=>)", html)))
print("Cards count:", len(re.findall(r"class=[\"\']slide-card", html)))
print("Jump options count:", len(re.findall(r"<option value=", html)))
print("Print items count:", len(re.findall(r"class=[\"\']print-item[\"\']", html)))
print("Has Rubric:", "SELF-ASSESSMENT RUBRIC" in html)
print("Has MathJax:", "mathjax" in html.lower())
