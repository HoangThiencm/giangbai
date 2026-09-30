from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

deck = soup.find(id="slideDeck")
if deck:
    children = [c for c in deck.children if getattr(c, 'name', None)]
    print(f"Total children of slideDeck: {len(children)}")
    for i, c in enumerate(children):
        classes = c.get("class", [])
        data_id = c.get("data-slide-id", "")
        heading = c.find(class_="slide-heading-text")
        h_text = heading.get_text(strip=True) if heading else (c.find("h1") or c.find("h2") or "")
        if hasattr(h_text, 'get_text'): h_text = h_text.get_text(strip=True)
        print(f"Slide {i+1}: class={classes}, id={data_id}, heading={h_text}")
