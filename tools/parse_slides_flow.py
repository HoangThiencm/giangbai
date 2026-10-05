import sys
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding='utf-8')

class SlideParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides = []
        self.curr_slide = None
        self.curr_col = None
        self.curr_block = None

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get('class', '').split()

        if tag == 'section' and 'slide-item' in classes:
            self.curr_slide = {
                'id': attr_dict.get('id', ''),
                'index': attr_dict.get('data-slide-index', ''),
                'left_blocks': [],
                'right_blocks': []
            }
            self.slides.append(self.curr_slide)

        elif self.curr_slide:
            if 'col-board' in classes:
                self.curr_col = 'left'
            elif 'col-task' in classes:
                self.curr_col = 'right'

            if 'content-block' in classes:
                block_info = {
                    'id': attr_dict.get('id', ''),
                    'step': attr_dict.get('data-step', 'fixed'),
                    'title': attr_dict.get('data-title-vi', ''),
                    'col': self.curr_col
                }
                if self.curr_col == 'left':
                    self.curr_slide['left_blocks'].append(block_info)
                elif self.curr_col == 'right':
                    self.curr_slide['right_blocks'].append(block_info)

    def handle_endtag(self, tag):
        pass

def inspect_slides(filepath):
    print(f"\n======================================================================")
    print(f"FILE: {filepath}")
    print(f"======================================================================")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    parser = SlideParser()
    parser.feed(html)

    for s in parser.slides:
        print(f"\n--- Slide {s['index']} ({s['id']}) ---")
        print("  [CỘT TRÁI - Ghi bảng]:")
        for b in s['left_blocks']:
            print(f"    • {b['id']} (step={b['step']}): {b['title']}")
        print("  [CỘT PHẢI - Hoạt động]:")
        for b in s['right_blocks']:
            print(f"    • {b['id']} (step={b['step']}): {b['title']}")

        # Sequence
        all_blocks = []
        for b in s['left_blocks']:
            if b['step'] != 'fixed' and b['step'].isdigit():
                all_blocks.append((int(b['step']), 'TRÁI', b['id'], b['title']))
        for b in s['right_blocks']:
            if b['step'] != 'fixed' and b['step'].isdigit():
                all_blocks.append((int(b['step']), 'PHẢI', b['id'], b['title']))
        all_blocks.sort(key=lambda x: x[0])
        flow = " ➔ ".join([f"{col}[bước {st}: {tit}]" for st, col, bid, tit in all_blocks])
        print("  TIẾN TRÌNH:", flow)

inspect_slides('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html')
