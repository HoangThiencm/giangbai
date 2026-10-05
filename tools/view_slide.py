import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def show_slide(fn, slide_id):
    with open(fn, 'r', encoding='utf-8') as f:
        text = f.read()
    pattern = rf'<section[^>]*id="{slide_id}"[\s\S]*?</section>'
    m = re.search(pattern, text)
    if not m and slide_id.isdigit():
        pattern2 = rf'<section[^>]*data-slide-index="{slide_id}"[\s\S]*?</section>'
        m = re.search(pattern2, text)
    if m:
        print(m.group(0))
    else:
        print(f"Slide {slide_id} not found in {fn}")


if __name__ == '__main__':
    fn = sys.argv[1] if len(sys.argv) > 1 else 'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html'
    sid = sys.argv[2] if len(sys.argv) > 2 else 's3'
    show_slide(fn, sid)
