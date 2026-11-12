# -*- coding: utf-8 -*-
import os

DIR = "C:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/TEMP/10.11_Toan9"

def fix_file(filename, replacements):
    fpath = os.path.join(DIR, filename)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Fixed: {filename}")

fix_file("03_KHBD_Toan9_LuyenTapChung_DaiSo_Tiet35.md", [
    (r"Không kết luận tập nghiệm $S = \{...\}$", "Không kết luận tập nghiệm hình thức"),
])

fix_file("05_KHBD_Toan9_OnTapCuoiHK1_DaiSo_Tiet38-39.md", [
    (r"Tuyệt đối không dùng dấu tương đương \Leftrightarrow tùy tiện và không kết luận tập nghiệm S = {...} hình thức.",
     "Tuyệt đối không dùng dấu tương đương tùy tiện và chỉ kết luận giá trị của biến rõ ràng."),
])

fix_file("08_KHBD_Toan9_HinhHoc_Bai16_ViTriTuongDoiDuongThangDuongTron_Tiet19-20.md", [
    (r"Cắt nhau \Leftrightarrow d < R; Tiếp xúc \Leftrightarrow d = R; Không giao nhau \Leftrightarrow d > R.",
     "Cắt nhau khi d < R; Tiếp xúc khi d = R; Không giao nhau khi d > R."),
])
