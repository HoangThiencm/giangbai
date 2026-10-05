import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html', 'r', encoding='utf-8') as f:
    c = f.read()

deck_start = c.find('<div class="slide-deck"')
deck_end = c.find('</section>\n    \n  </div>')
if deck_end == -1: deck_end = c.find('id="casioWidget"')
if deck_end == -1: deck_end = c.find('<div class="blank-screen"')
deck = c[deck_start:deck_end]

print("Deck length:", len(deck))

# 1. Control chars in deck:
for byte_val, name in [(7, '\\a'), (8, '\\b'), (12, '\\f'), (9, '\\t'), (11, '\\v')]:
    char = chr(byte_val)
    if char in deck:
        print(f"  FOUND control char {name} ({deck.count(char)} times) in slide deck!")
        for m in re.finditer(re.escape(char), deck):
            start = max(0, m.start() - 20)
            end = min(len(deck), m.end() + 20)
            print("    Context:", repr(deck[start:end]))

# 2. Look for suspicious Greek letters or common math words:
for word in ['alpha', 'beta', 'gamma', 'delta', 'theta', 'circ', 'approx', 'sqrt', 'frac', 'sin', 'cos', 'tan', 'cot']:
    bad_word = word[1:] # e.g. 'lpha', 'eta', 'irc'
    for m in re.finditer(rf'[\$\s\b]{bad_word}\b', deck):
        s = max(0, m.start() - 10)
        e = min(len(deck), m.end() + 20)
        print(f"  Suspicious missing backslash for {word}: {repr(deck[s:e])}")
