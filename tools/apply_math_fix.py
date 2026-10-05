import sys

sys.stdout.reconfigure(encoding='utf-8')

fp = r'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html'

with open(fp, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace }\night)$ (ASCII 10 + ight)$ with }\right)$
old_pattern = "}\night)$"
new_pattern = r"}\right)$"

count = content.count(old_pattern)
print(f"Occurrences of broken right: {count}")
content = content.replace(old_pattern, new_pattern)

with open(fp, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated Bai_12 successfully.")
