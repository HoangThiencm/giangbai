#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Công cụ dọn dẹp file rác và bộ nhớ đệm tạm thời cho Dự án GiangBai / Trợ lý Thiên.
Chỉ xóa các file rác thực sự:
  - Cache Python: __pycache__, *.pyc, *.pyo
  - Thư mục ảnh tạm khi tách trang PDF: TROLYTHIEN/**/pdf_pages/
  - Thư mục chạy thử nghiệm: scratch/
  - File khóa handoff thừa: docs/handoff/.lock
  - File tiến trình tạm của hệ thống trong temp Windows
BẢO TỒN NGUYÊN VẸN:
  - Toàn bộ kết quả giáo án, bài giảng, hình vẽ, đề thi trong TROLYTHIEN/**/Ket_qua/
  - Toàn bộ tài liệu gốc trong TROLYTHIEN/**/Dau_vao/
  - Mã nguồn hệ thống và tài liệu hướng dẫn
"""

import os
import sys
import shutil
import glob
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def don_dep_du_an():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print("=" * 65)
    print("🧹 BẮT ĐẦU DỌN DẸP FILE RÁC & CACHE DỰ ÁN TRỢ LÝ THIÊN")
    print(f"📁 Thư mục gốc: {root_dir}")
    print("=" * 65)

    count_files = 0
    count_dirs = 0
    bytes_freed = 0

    # 1. Dọn dẹp __pycache__ và *.pyc trên toàn dự án
    for root, dirs, files in os.walk(root_dir):
        if 'node_modules' in root or '.git' in root:
            continue
        for d in list(dirs):
            if d == '__pycache__':
                full_dir = os.path.join(root, d)
                try:
                    for f in os.listdir(full_dir):
                        fp = os.path.join(full_dir, f)
                        if os.path.isfile(fp):
                            bytes_freed += os.path.getsize(fp)
                            count_files += 1
                    shutil.rmtree(full_dir, ignore_errors=True)
                    count_dirs += 1
                    print(f"  [Đã xóa thư mục cache]: {os.path.relpath(full_dir, root_dir)}")
                except Exception as e:
                    pass
        for f in files:
            if f.endswith(('.pyc', '.pyo', '.pyd')):
                full_file = os.path.join(root, f)
                try:
                    bytes_freed += os.path.getsize(full_file)
                    os.remove(full_file)
                    count_files += 1
                except Exception:
                    pass

    # 2. Dọn dẹp thư mục pdf_pages tạm thời trong TROLYTHIEN
    troly_dir = os.path.join(root_dir, 'TROLYTHIEN')
    if os.path.isdir(troly_dir):
        for root, dirs, _ in os.walk(troly_dir):
            for d in list(dirs):
                if d == 'pdf_pages':
                    full_dir = os.path.join(root, d)
                    try:
                        shutil.rmtree(full_dir, ignore_errors=True)
                        count_dirs += 1
                        print(f"  [Đã xóa thư mục tách PDF tạm]: {os.path.relpath(full_dir, root_dir)}")
                    except Exception:
                        pass

    # 3. Dọn dẹp thư mục scratch (chỉ giữ lại .gitkeep)
    scratch_dir = os.path.join(root_dir, 'scratch')
    if os.path.isdir(scratch_dir):
        for item in os.listdir(scratch_dir):
            if item == '.gitkeep':
                continue
            item_path = os.path.join(scratch_dir, item)
            try:
                if os.path.isfile(item_path):
                    bytes_freed += os.path.getsize(item_path)
                    os.remove(item_path)
                    count_files += 1
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
                    count_dirs += 1
            except Exception:
                pass
        print(f"  [Đã làm sạch thư mục nháp]: scratch/")

    # 4. Xóa file khóa docs/handoff/.lock nếu còn sót
    lock_file = os.path.join(root_dir, 'docs', 'handoff', '.lock')
    if os.path.isfile(lock_file):
        try:
            os.remove(lock_file)
            count_files += 1
            print("  [Đã gỡ file khóa handoff]: docs/handoff/.lock")
        except Exception:
            pass

    # 5. Xóa file log tiến trình thi online / AI trong temp
    temp_dir = tempfile.gettempdir()
    for temp_pattern in ['giangbai_exam_ai_progress_*.txt', 'giangbai_*.tmp']:
        for tp in glob.glob(os.path.join(temp_dir, temp_pattern)):
            try:
                os.remove(tp)
                count_files += 1
            except Exception:
                pass

    print("-" * 65)
    kb_freed = bytes_freed / 1024
    print(f"✨ HOÀN TẤT DỌN DẸP AN TOÀN!")
    print(f"  - Số file rác đã xóa: {count_files}")
    print(f"  - Số thư mục cache đã dọn: {count_dirs}")
    print(f"  - Dung lượng giải phóng: {kb_freed:.2f} KB")
    print(f"  - Toàn bộ tài liệu giáo án, bài giảng và hình vẽ trong TROLYTHIEN/ được giữ nguyên vẹn 100%.")
    print("=" * 65)

if __name__ == '__main__':
    don_dep_du_an()
