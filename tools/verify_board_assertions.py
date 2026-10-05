import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')


targets = [
    'TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html'
]

assertions = [
    ('btnBoard in controlBar', r'<button class="btn-ctrl" id="btnBoard" onclick="toggleBlackboard\(\)"'),
    ('btnTimer in controlBar', r'<button class="btn-ctrl" id="btnTimer" onclick="toggleTimerModal\(\)"'),
    ('btnCalc in controlBar', r'<button class="btn-ctrl" id="btnCalc" onclick="toggleCalculator\(\)"'),
    ('boardImageBox exists', r'<div id="boardImageBox" class="board-floating-image-box">'),
    ('boardImgHeader exists', r'<div class="float-photo-bar" id="boardImgHeader">'),
    ('boardImgResizeHandle exists', r'<div class="resize-handle-br" id="boardImgResizeHandle"'),
    ('boardFileInput exists', r'<input type="file" id="boardFileInput" accept="image/\*"'),
    ('boardPasteBtn exists', r'title="Dán ảnh từ Clipboard \(Ctrl\+V\)"'),
    ('setBoardImage function', r'function setBoardImage\(dataUrl\)'),
    ('handleBoardImageUpload function', r'function handleBoardImageUpload\(e\)'),
    ('initBoardImageInteractions function', r'function initBoardImageInteractions\(\)'),
    ('paste event listener', r'window\.addEventListener\(\'paste\','),
    ('no blackboard in contextMenu', lambda text: 'handleCtxAction(\'blackboard\')' not in text[text.find('id="contextMenu"'):text.find('</div>', text.find('id="contextMenu"')) + 600]),
]

all_passed = True
for t in targets:
    if not os.path.exists(t):
        continue
    with open(t, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"=== Testing {t} ===")

    for name, pattern in assertions:
        if callable(pattern):
            passed = pattern(content)
        else:
            passed = bool(re.search(pattern, content))
        if passed:
            print(f"  [PASS] {name}")
        else:
            print(f"  [FAIL] {name}")
            all_passed = False

if all_passed:
    print("\nALL ASSERTIONS PASSED PERFECTLY!")
else:
    print("\nSOME ASSERTIONS FAILED!")
    sys.exit(1)
