import os, sys, fitz

sys.stdout.reconfigure(encoding='utf-8')
folder = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/LE THI BINH"
f_hh8 = [f for f in os.listdir(folder) if '1791212409278' in f][0]
doc = fitz.open(os.path.join(folder, f_hh8))
page5 = doc[4] # page 5

pix = page5.get_pixmap(dpi=150)
pix.save("TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/debug_p5_hh8.png")
print("Saved page 5 rendering to TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/debug_p5_hh8.png")

# Also check Page 4 and Page 6
pix4 = doc[3].get_pixmap(dpi=150)
pix4.save("TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/debug_p4_hh8.png")

# Also check HH7 Page 4, 5
f_hh7 = [f for f in os.listdir(folder) if '1791212408808' in f][0]
doc7 = fitz.open(os.path.join(folder, f_hh7))
pix7_4 = doc7[3].get_pixmap(dpi=150)
pix7_4.save("TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/debug_p4_hh7.png")
pix7_5 = doc7[4].get_pixmap(dpi=150)
pix7_5.save("TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/debug_p5_hh7.png")
print("Saved HH7 debug renderings.")
