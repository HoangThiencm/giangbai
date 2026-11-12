# -*- coding: utf-8 -*-
import os

DIR = "C:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/TEMP/10.11_Toan8"

def fix_file(filename, replacements):
    fpath = os.path.join(DIR, filename)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Fixed: {filename}")

fix_file("05_KHBD_Toan8_Bai18_ThuThapPhanLoaiDuLieu_Tiet29-30.md", [
    ("### Hoạt động 2.1: Các phương pháp thu thập dữ liệu (25 phút - Tiết 29)", "### Hoạt động 2.1: Các phương pháp thu thập dữ liệu (25 phút)"),
    ("### Hoạt động 2.2: Phân loại dữ liệu định tính và định lượng (25 phút - Tiết 30)", "### Hoạt động 2.2: Phân loại dữ liệu định tính và định lượng (25 phút)"),
])

fix_file("06_KHBD_Toan8_Bai19_BieuDienDuLieuBangBieuDo_Tiet31-32.md", [
    ("### Hoạt động 2.1: Biểu diễn dữ liệu bằng bảng thống kê và biểu đồ cột, đoạn thẳng (25 phút - Tiết 31)", "### Hoạt động 2.1: Biểu diễn dữ liệu bằng bảng thống kê và biểu đồ cột, đoạn thẳng (25 phút)"),
    ("### Hoạt động 2.2: Biểu diễn dữ liệu bằng biểu đồ hình quạt tròn (25 phút - Tiết 32)", "### Hoạt động 2.2: Biểu diễn dữ liệu bằng biểu đồ hình quạt tròn (25 phút)"),
])

fix_file("11_KHBD_Toan8_OnTapCuoiHK1_DaiSo_Tiet37-39.md", [
    (r"\Leftrightarrow", "suy ra/tương đương"),
])

fix_file("12_KHBD_Toan8_KiemTraTraBaiCuoiHK1_DaiSo_Tiet40-41.md", [
    ("## A. TIẾT 40: KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (45 phút)", "## A. HOẠT ĐỘNG 1: KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (45 phút)"),
    ("## B. TIẾT 41: TRẢ BÀI KIỂM TRA HỌC KÌ I VÀ SỬA BÀI (45 phút)", "## B. HOẠT ĐỘNG 2: TRẢ BÀI KIỂM TRA HỌC KÌ I VÀ SỬA BÀI (45 phút)"),
])

fix_file("17_KHBD_Toan8_HinhHoc_KiemTraTraBaiCuoiHK1_Tiet30-31.md", [
    ("## A. TIẾT 30: KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (HÌNH HỌC) (45 phút)", "## A. HOẠT ĐỘNG 1: KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (45 phút)"),
    ("## B. TIẾT 31: TRẢ BÀI KIỂM TRA HỌC KÌ I VÀ SỬA BÀI (HÌNH HỌC) (45 phút)", "## B. HOẠT ĐỘNG 2: TRẢ BÀI KIỂM TRA HỌC KÌ I VÀ SỬA BÀI (45 phút)"),
])
