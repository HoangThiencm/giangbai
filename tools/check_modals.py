import os

paths = [
    'TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html'
]

for p in paths:
    if not os.path.exists(p):
        print(f"NOT FOUND: {p}")
        continue
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    style_end = c.find('</style>')
    style_content = c[:style_end] if style_end != -1 else ""
    print(f"=== {p} ===")
    print("  .edit-modal-backdrop in <style>:", '.edit-modal-backdrop' in style_content)
    print("  .selection-tooltip in <style>:", '.selection-tooltip' in style_content)
    print("  editModalBackdrop present:", 'id="editModalBackdrop"' in c)
    print("  editModalBackdrop inline display:none:", 'id="editModalBackdrop"' in c and 'display:none' in c[c.find('id="editModalBackdrop"'):c.find('>', c.find('id="editModalBackdrop"'))])
    print("  selectionTooltip present:", 'id="selectionTooltip"' in c)
    print("  selectionTooltip inline display:none:", 'id="selectionTooltip"' in c and 'display:none' in c[c.find('id="selectionTooltip"'):c.find('>', c.find('id="selectionTooltip"'))])
