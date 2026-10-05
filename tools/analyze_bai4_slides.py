import subprocess
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
c = subprocess.check_output(['git', 'show', 'HEAD:TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html'], encoding='utf-8')
print("Bai 4 loaded, length:", len(c))

slides = c.split('<section class="slide-item')
print(f"Total slides in Bai 4: {len(slides) - 1}")

for i, s in enumerate(slides[1:], 1):
    m_id = re.search(r'id=["\']([^"\']+)["\']', s)
    s_id = m_id.group(1) if m_id else f"slide_{i}"
    m_steps = re.search(r'data-max-steps=["\']([^"\']+)["\']', s)
    max_steps = m_steps.group(1) if m_steps else "?"
    
    blocks = re.findall(r'<div[^>]*class=["\'][^"\']*content-block[^"\']*["\'][^>]*>', s)
    b_info = []
    for b in blocks:
        bid = (re.search(r'id=["\']([^"\']+)["\']', b) or [None, ''])[1]
        bstep = (re.search(r'data-step=["\']([^"\']+)["\']', b) or [None, ''])[1]
        btitle = (re.search(r'data-title-vi=["\']([^"\']+)["\']', b) or [None, ''])[1]
        b_info.append(f"{bid}(s={bstep})")
    print(f"Slide {i} ({s_id}, max={max_steps}): {', '.join(b_info)}")
