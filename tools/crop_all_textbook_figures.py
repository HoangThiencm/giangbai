# -*- coding: utf-8 -*-
"""
Cắt chính xác toàn bộ các hình vẽ SGK xuất hiện trong 4 bài học Toán 9:
- Bài 12: Hình 4.11, 4.17, 4.18, 4.22, 4.23, 4.24
- Luyện tập chung: Hình 4.25, 4.26, 4.27, 4.29, 4.31
- Cuối chương IV: Hình 4.32, 4.35, 4.36, 4.38
- Bài 13: Hình 5.1, 5.2, 5.3, 5.4, 5.5
"""
import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

RENDER_DIR = "tools/temp_render_crops"
OUT_DIR = "TROLYTHIEN/engine/hinh_ve_sgk"
os.makedirs(OUT_DIR, exist_ok=True)

# Tọa độ bounding box (left, top, right, bottom) trên trang 2481 x 3508
CROP_SPECS = {
    # === BÀI 12 (01_page_*.png) ===
    # Hình 4.11 (Lâu đài) - Trang 1
    "hinh_sgk_4_11_lau_dai.png": ("01_page_1.png", (250, 1500, 2250, 2400)),
    # Hình 4.17 (Tòa tháp 8,6m) - Trang 3
    "hinh_sgk_4_17_toa_thap.png": ("01_page_3.png", (1500, 750, 2350, 1350)),
    # Hình 4.18 (Bóng cây 25m) - Trang 3
    "hinh_sgk_4_18_bong_cay.png": ("01_page_3.png", (1500, 1600, 2350, 2280)),
    # Hình 4.22 (Xe chở rác) - Trang 5
    "hinh_sgk_4_22_xe_cho_rac.png": ("01_page_5.png", (200, 750, 1050, 1420)),
    # Hình 4.23 (Mái nhà kho) - Trang 5
    "hinh_sgk_4_23_mai_nha_kho.png": ("01_page_5.png", (1100, 750, 2300, 1420)),
    # Hình 4.24 (Cái cây qua gương) - Trang 5
    "hinh_sgk_4_24_guong_phang.png": ("01_page_5.png", (700, 2350, 1850, 3250)),

    # === LUYỆN TẬP CHUNG (02_page_*.png) ===
    # Hình 4.25 (Tam giác vuông AB=5, AC=12) - Trang 1
    "hinh_sgk_4_25_tam_giac_vuong.png": ("02_page_1.png", (1600, 360, 2350, 780)),
    # Hình 4.26 (Bức tường hình thang) - Trang 1
    "hinh_sgk_4_26_buc_tuong_hinh_thang.png": ("02_page_1.png", (1600, 1550, 2350, 2150)),
    # Hình 4.27 (Dòng sông 50m) - Trang 2
    "hinh_sgk_4_27_dong_song.png": ("02_page_2.png", (1680, 780, 2360, 1300)),
    # Hình 4.29 (Hồ nước góc 120°) - Trang 2 (CHÍNH TRONG ẢNH USER)
    "hinh_sgk_4_29_ho_nuoc.png": ("02_page_2.png", (1600, 1800, 2350, 2300)),
    # Hình 4.31 (Tàu ngầm lặn góc 21°) - Trang 2 (CHÍNH TRONG ẢNH USER)
    "hinh_sgk_4_31_tau_ngam.png": ("02_page_2.png", (1680, 2820, 2360, 3280)),

    # === BÀI TẬP CUỐI CHƯƠNG IV (03_page_*.png) ===
    # Hình 4.32 (Tam giác vuông 3, 4, 5) - Trang 1
    "hinh_sgk_4_32_trac_nghiem.png": ("03_page_1.png", (1600, 480, 2300, 950)),
    # Hình 4.35 (Túp lều 1,8m, 4,4m) - Trang 1
    "hinh_sgk_4_35_tup_leu.png": ("03_page_1.png", (250, 2750, 2250, 3320)),
    # Hình 4.36 (Cây gãy góc 20°, 5m) - Trang 2
    "hinh_sgk_4_36_cay_gay.png": ("03_page_2.png", (250, 520, 2250, 1350)),
    # Hình 4.38 (Đố vui Trái Đất Eratosthenes) - Trang 2
    "hinh_sgk_4_38_trai_dat.png": ("03_page_2.png", (1500, 1850, 2350, 2750)),

    # === BÀI 13 (04_page_*.png) ===
    # Hình 5.1 (Điểm trong, ngoài, trên đường tròn) - Trang 2
    "hinh_sgk_5_1_vi_tri_diem.png": ("04_page_2.png", (1700, 650, 2350, 1200)),
    # Hình 5.2 (Đường kính AB) - Trang 2
    "hinh_sgk_5_2_duong_kinh_ab.png": ("04_page_2.png", (1700, 1550, 2350, 2050)),
    # Hình 5.3 (Đối xứng tâm) - Trang 3
    "hinh_sgk_5_3_doi_xung_tam.png": ("04_page_3.png", (400, 780, 2300, 1300)),
    # Hình 5.4 (Đối xứng trục) - Trang 3
    "hinh_sgk_5_4_doi_xung_truc.png": ("04_page_3.png", (400, 1580, 2300, 2120)),
    # Hình 5.5 (Điểm đối xứng qua tâm và trục) - Trang 4
    "hinh_sgk_5_5_tim_diem_doi_xung.png": ("04_page_4.png", (1700, 480, 2350, 1050))
}

print("Bắt đầu cắt toàn bộ hình ảnh SGK theo tọa độ chuẩn...")
for filename, (page_file, box) in CROP_SPECS.items():
    page_path = os.path.join(RENDER_DIR, page_file)
    if not os.path.exists(page_path):
        print(f"❌ Không tìm thấy: {page_path}")
        continue
    img = Image.open(page_path)
    cropped = img.crop(box)
    out_file = os.path.join(OUT_DIR, filename)
    cropped.save(out_file)
    print(f"✓ Đã lưu: {filename} ({cropped.size[0]}x{cropped.size[1]})")

print("\nHoàn tất cắt toàn bộ 17 hình ảnh SGK!")
