import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    text = f.read()

from verify_bb_extract import j1_start, j1_end, j2_start, j2_end

print("=== JS1 (first 200 chars) ===")
print(text[j1_start:j1_start+200])
print("=== JS1 (last 200 chars) ===")
print(text[j1_end-200:j1_end])

print("\n=== JS2 (first 200 chars) ===")
print(text[j2_start:j2_start+200])
print("=== JS2 (last 200 chars) ===")
print(text[j2_end-200:j2_end])
