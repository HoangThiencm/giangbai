import sys
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding='utf-8')

class SlideChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides = []
        self.curr_slide = None
        self.curr_col = None

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get('class', '').split()
        if tag == 'section' and 'slide-item' in classes:
            self.curr_slide = {
                'id': attr_dict.get('id', ''),
                'index': attr_dict.get('data-slide-index', ''),
                'blocks': []
            }
            self.slides.append(self.curr_slide)
        elif self.curr_slide:
            if 'col-board' in classes:
                self.curr_col = 'board'
            elif 'col-task' in classes:
                self.curr_col = 'task'

            if 'content-block' in classes:
                self.curr_slide['blocks'].append({
                    'id': attr_dict.get('id', ''),
                    'col': self.curr_col,
                    'step': attr_dict.get('data-step', 'fixed'),
                    'title': attr_dict.get('data-title-vi', '')
                })

def check(fn):
    print("="*60)
    print("FILE:", fn)
    print("="*60)
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()
    p = SlideChecker()
    p.feed(html)
    for s in p.slides:
        steps = []
        for b in s['blocks']:
            steps.append((b['col'], b['step'], b['id'], b['title']))
        print(f"Slide {s['index']} ({s['id']}): {steps}")

if __name__ == '__main__':
    for fn in sys.argv[1:]:
        check(fn)
