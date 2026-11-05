# -*- coding: utf-8 -*-
"""
CÔNG CỤ DỌN DẸP FILE RÁC & VỆ SINH THƯ MỤC TỰ ĐỘNG (ZERO-RESIDUE CLEANER)
Trợ lý Sư phạm Hoàng Thiên • Trường THCS Trần Phú
Bản vá: Version 2.0.0

Chức năng:
- Quét và loại bỏ toàn bộ file rác sinh ra trong quá trình duyệt đề và thẩm định hồ sơ:
  + Ảnh render trang trung gian: page_*.png, v*_page_*.png, fixed_page_*.png...
  + Tệp thử nghiệm nháp: test_*.docx, test_*.pdf, test_*.py, *.ps1...
  + Thư mục bóc tách trang PDF tạm: de_cuong_*_pages/
- Bảo vệ an toàn tuyệt đối 100%:
  + Toàn bộ biên bản phản biện, đề cương chính thức (.docx, .pdf, .md)
  + Thư mục chữ ký giáo viên chính thức (chu_ky/)
  + Thư mục hình vẽ hình học (hinh_ve/)
  + Thư mục lưu trữ phiên bản lịch sử (DD.MM/)
"""

import os
import sys
import re
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DUYET_DE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "4_DUYET_DE"))
KET_QUA_DIR = os.path.join(DUYET_DE_DIR, "Ket_qua")
DAU_VAO_DIR = os.path.join(DUYET_DE_DIR, "Dau_vao")

# Mẫu tên file rác cần dọn dẹp
GARBAGE_FILE_PATTERNS = [
    r'^(?:v\d+_)?page_\d+\.png$',
    r'^fixed_page_\d+\.png$',
    r'^test_.*\.(?:docx|pdf|png|py)$',
    r'^convert_test\.ps1$',
    r'^rebuild_from_.*\.py$',
]

# Thư mục tạm trong Dau_vao cần dọn
GARBAGE_DIR_PATTERNS = [
    r'^de_cuong_.*_pages$',
    r'^.*_temp_pages$',
]

# File script dev cần di dời vào engine (không để tại Ket_qua)
SCRIPTS_TO_MOVE_TO_ENGINE = [
    "build_all_figures_toan7.py",
    "build_de_cuong_toan7_official.py",
    "build_phan_bien_toan7.py"
]

def is_garbage_file(filename: str) -> bool:
    for pattern in GARBAGE_FILE_PATTERNS:
        if re.match(pattern, filename, re.IGNORECASE):
            return True
    return False

def is_garbage_dir(dirname: str) -> bool:
    for pattern in GARBAGE_DIR_PATTERNS:
        if re.match(pattern, dirname, re.IGNORECASE):
            return True
    return False

def clean_duyet_de(dry_run: bool = False):
    print("=" * 65)
    print("QUY TRÌNH VỆ SINH THƯ MỤC ZERO-RESIDUE: PHÂN HỆ DUYỆT ĐỀ")
    print(f"Thư mục: {DUYET_DE_DIR}")
    print(f"Chế độ: {'KIỂM TRA (DRY RUN)' if dry_run else 'THỰC THI (CLEANUP)'}")
    print("=" * 65)
    
    deleted_files = 0
    deleted_dirs = 0
    moved_scripts = 0

    # 1. Di dời các builder scripts từ Ket_qua sang engine
    engine_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    for s_name in SCRIPTS_TO_MOVE_TO_ENGINE:
        src = os.path.join(KET_QUA_DIR, s_name)
        dst = os.path.join(engine_dir, s_name)
        if os.path.exists(src):
            if not dry_run:
                shutil.move(src, dst)
            moved_scripts += 1
            print(f"📦 [DI DỜI VỀ ENGINE] {s_name}")

    # 2. Quét dọn file rác trong Ket_qua
    if os.path.exists(KET_QUA_DIR):
        for fname in os.listdir(KET_QUA_DIR):
            fpath = os.path.join(KET_QUA_DIR, fname)
            if os.path.isfile(fpath) and is_garbage_file(fname):
                if not dry_run:
                    os.remove(fpath)
                deleted_files += 1
                print(f"🗑️ [XÓA FILE RÁC] Ket_qua/{fname}")

    # 3. Quét dọn thư mục tạm trong Dau_vao
    if os.path.exists(DAU_VAO_DIR):
        for dname in os.listdir(DAU_VAO_DIR):
            dpath = os.path.join(DAU_VAO_DIR, dname)
            if os.path.isdir(dpath) and is_garbage_dir(dname):
                if not dry_run:
                    shutil.rmtree(dpath)
                deleted_dirs += 1
                print(f"🗑️ [XÓA THƯ MỤC TẠM] Dau_vao/{dname}")

    print("-" * 65)
    print(f"TỔNG KẾT VỆ SINH:")
    print(f"   • File rác đã dọn: {deleted_files}")
    print(f"   • Thư mục tạm đã dọn: {deleted_dirs}")
    print(f"   • Script đã quy hoạch về engine: {moved_scripts}")
    print("=" * 65)
    return deleted_files, deleted_dirs, moved_scripts

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    clean_duyet_de(dry_run=is_dry)
