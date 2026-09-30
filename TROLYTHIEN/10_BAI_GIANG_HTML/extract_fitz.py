import sys
import os
import fitz # PyMuPDF

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/12_BAI 12_MỘT SỐ HỆ THỨC VỀ CẠNH VÀ GÓC TRONG TAM GIÁC VUÔNG.pdf"
doc = fitz.open(pdf_path)
print(f"Total pages: {len(doc)}")

full_text = []
for i, page in enumerate(doc):
    print(f"=== PAGE {i+1} ===")
    txt = page.get_text()
    print(f"Length: {len(txt)}")
    if len(txt) > 0:
        print(txt[:300])
    full_text.append(f"=== PAGE {i+1} ===\n" + txt)

    # Check images on page
    images = page.get_images()
    print(f"Images count on page {i+1}: {len(images)}")

with open("TROLYTHIEN/10_BAI_GIANG_HTML/pdf_extracted_fitz.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(full_text))
