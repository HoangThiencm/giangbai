with open('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("Bai 4 blackboardOverlay:", "blackboardOverlay" in text)
print("Bai 4 toggleBlackboard:", "toggleBlackboard" in text)
print("Bai 4 drawCanvas:", "drawCanvas" in text)
print("Bai 4 penPalette:", "penPalette" in text)
print("Bai 4 btnBlackboard:", "blackboard" in text)
