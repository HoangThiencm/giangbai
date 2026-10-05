import os
import glob
import sys
import fitz  # PyMuPDF

sys.stdout.reconfigure(encoding='utf-8')

pdf_files = glob.glob('TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/*12*.pdf')
if not pdf_files:
    print("No PDF file found for lesson 12!")
    sys.exit(1)

pdf_path = pdf_files[0]
print(f"Reading: {pdf_path}")

doc = fitz.open(pdf_path)
print(f"Total pages: {len(doc)}")

full_text = ""
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    full_text += f"\n--- PAGE {page_num + 1} ---\n" + text

with open('TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/bai12_extracted_text.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)

print("Saved extracted text to TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/bai12_extracted_text.txt")
print(full_text[:2000])
