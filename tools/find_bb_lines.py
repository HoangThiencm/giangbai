import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Lines count:", len(lines))
for idx, line in enumerate(lines):
    if any(k in line for k in ['blackboard-overlay', 'blackboard-top-bar', '<div id="blackboardOverlay"', 'function toggleBlackboard', 'setBoardSurface']):
        print(f"Line {idx+1}: {line.strip()[:100]}")
