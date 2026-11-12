import os
import sys

base_dir = r'C:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\3_DUYET_GIAO_AN\Dau_vao'
sys.stdout.reconfigure(encoding='utf-8')

for item in os.listdir(base_dir):
    p = os.path.join(base_dir, item)
    if os.path.isdir(p):
        print(f"DIR: {item} -> files: {os.listdir(p)}")
