# -*- coding: utf-8 -*-
import sys
import re
import math

sys.stdout.reconfigure(encoding='utf-8')

def check_equations_toan6():
    print("\n--- KIỂM TRA TÌM X TOÁN 6 ---")
    with open('TROLYTHIEN/engine/builder_de_cuong_toan6.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        m = re.search(r'\"([a-z]\))\s*\$([^\"]+=[^\"]+)\$\"', line)
        if m:
            item_id = m.group(1)
            eq = m.group(2)
            # Check simple forms:
            # e.g., 2x - 15 = 45, 3x = 75, etc.
            # Let's inspect equations that might have non-integer solution
            pass

def check_all_grades():
    for g in [6, 7, 8, 9]:
        fn = f'TROLYTHIEN/engine/builder_de_cuong_toan{g}.py'
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n==================== TOÁN {g} ====================")
        # Check all answer entries against questions if possible
        # Or look for common traps
        # Let's find all exercises in Phần I and Phần II
        pass

if __name__ == '__main__':
    check_all_grades()
