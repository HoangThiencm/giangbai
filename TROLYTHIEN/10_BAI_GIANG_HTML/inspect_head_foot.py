import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html", "r", encoding="utf-8") as f:
    html = f.read()

deck_pos = html.find('id="slideDeck"')
print("=== HTML BEFORE SLIDEDECK ===")
print(html[:deck_pos+20])

deck_end = html.find('<!-- END SLIDE 26 -->')
if deck_end == -1:
    deck_end = html.find('id="s26"')
    deck_end = html.find('</section>', deck_end) + 10

print("=== HTML AFTER LAST SLIDE ===")
print(html[deck_end:deck_end+2500])
