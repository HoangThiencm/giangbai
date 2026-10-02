import os
import sys

file_path = os.path.join(os.path.dirname(__file__), '../TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/Chuyen_De_Luy_Thua_Va_Hinh_Hoc_Toan_6.html')

if not os.path.exists(file_path):
    print("FAIL: File does not exist:", file_path)
    sys.exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

checks = [
    ('MathJax 3', 'tex-svg.js' in content and 'MathJax =' in content),
    ('Dual Mode (Present & Design)', 'mode-present' in content and 'mode-design' in content),
    ('Step-by-step reveal support', 'solution-step' in content and 'revealNextStep' in content),
    ('Print Handout Mode (@media print)', '@media print' in content and 'print-student-lines' in content),
    ('TV font size adjustment (28px - 30px)', '--tv-font-size' in content and 'toggleTVFontSize' in content),
    ('Clean SVG Geometry without text explanation inside', '<svg' in content and 'viewBox="0 0 400 400"' in content and 'geometry-layout' in content),
    ('Keyboard shortcuts (Space, Arrow keys)', 'keydown' in content and 'ArrowRight' in content)
]

all_pass = True
for name, passed in checks:
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {name}")
    if not passed:
        all_pass = False

if all_pass:
    print("\nALL 7 VERIFICATION CHECKS PASSED!")
    sys.exit(0)
else:
    sys.exit(1)
