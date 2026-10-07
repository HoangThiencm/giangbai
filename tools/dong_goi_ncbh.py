# -*- coding: utf-8 -*-
"""
Module đóng gói ZIP trọn bộ hồ sơ Nghiên cứu bài học
"""

import os
import sys
import zipfile
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

source_dir = os.path.abspath("TROLYTHIEN/NCBH_DINH_LY_THALES_TOAN_8")
zip_name = "Bo_Ho_So_NCBH_Dinh_Ly_Thales_Lop_8.zip"
zip_path_in_folder = os.path.join(source_dir, zip_name)
zip_path_root = os.path.abspath(zip_name)

# Đóng gói zip
with zipfile.ZipFile(zip_path_in_folder, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.zip'):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, source_dir)
            zipf.write(full_path, rel_path)

# Sao chép sang thư mục gốc để dễ tìm kiếm
shutil.copy2(zip_path_in_folder, zip_path_root)
print("ĐÃ ĐÓNG GÓI THÀNH CÔNG:")
print(f"1. {zip_path_in_folder}")
print(f"2. {zip_path_root}")
