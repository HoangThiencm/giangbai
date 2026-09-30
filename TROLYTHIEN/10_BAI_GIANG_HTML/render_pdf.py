import fitz # PyMuPDF
import os

pdf_path = r"TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/12_BAI 12_MỘT SỐ HỆ THỨC VỀ CẠNH VÀ GÓC TRONG TAM GIÁC VUÔNG.pdf"
doc = fitz.open(pdf_path)
out_dir = r"TROLYTHIEN/10_BAI_GIANG_HTML/pdf_pages"
os.makedirs(out_dir, exist_ok=True)

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    img_path = os.path.join(out_dir, f"page_{i+1}.png")
    pix.save(img_path)
    print(f"Saved {img_path} ({pix.width}x{pix.height})")
