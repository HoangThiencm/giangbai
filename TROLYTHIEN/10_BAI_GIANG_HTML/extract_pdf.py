import sys
import os
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/12_BAI 12_MỘT SỐ HỆ THỨC VỀ CẠNH VÀ GÓC TRONG TAM GIÁC VUÔNG.pdf"
reader = pypdf.PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}")

full_text = []
for i, page in enumerate(reader.pages):
    print(f"--- PAGE {i+1} ---")
    txt = page.extract_text() or ""
    print(txt[:300] + "..." if len(txt) > 300 else txt)
    full_text.append(f"=== PAGE {i+1} ===\n" + txt)

with open("TROLYTHIEN/10_BAI_GIANG_HTML/pdf_extracted.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(full_text))

print("\nExtracted text saved to TROLYTHIEN/10_BAI_GIANG_HTML/pdf_extracted.txt")
