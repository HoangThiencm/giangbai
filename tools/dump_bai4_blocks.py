import sys
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding='utf-8')

class BlockDetailParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides = []
        self.curr_slide = None
        self.curr_col = None
        self.in_block = False
        self.curr_block = None

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get('class', '').split()

        if tag == 'section' and 'slide-item' in classes:
            self.curr_slide = {
                'id': attr_dict.get('id', ''),
                'index': int(attr_dict.get('data-slide-index', '0')),
                'blocks': []
            }
            self.slides.append(self.curr_slide)

        elif self.curr_slide:
            if 'col-board' in classes:
                self.curr_col = 'board'
            elif 'col-task' in classes:
                self.curr_col = 'task'

            if 'content-block' in classes:
                self.curr_block = {
                    'id': attr_dict.get('id', ''),
                    'col': self.curr_col,
                    'step': attr_dict.get('data-step', 'fixed'),
                    'title_vi': attr_dict.get('data-title-vi', ''),
                    'title_en': attr_dict.get('data-title-en', '')
                }
                self.curr_slide['blocks'].append(self.curr_block)

def inspect(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()
    p = BlockDetailParser()
    p.feed(html)
    print(f"\n==================== {fn} ====================")
    for s in p.slides:
        print(f"\n--- Slide {s['index']} ({s['id']}) ---")
        for b in s['blocks']:
            print(f"  [{b['col'].upper():5s}] id={b['id']:8s} step={b['step']:5s} | {b['title_vi']}")

inspect('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html')
