# -*- coding: utf-8 -*-
"""
HỆ THỐNG XỬ LÝ & TÁI TẠO BỘ CHỮ KÝ GIÁO VIÊN SIÊU NÉT (BẢN VÁ ĐẬM MÀU CHUYÊN DỤNG CHO WORD)
Trợ lý Sư phạm Hoàng Thiên • Trường THCS Trần Phú
Bản vá: Version 2.0.0

Đặc tính nâng cấp:
1. Xóa 100% phông nền (trong suốt RGBA)
2. Công nghệ làm dày nét (Stroke Boldening Engine): Giữ nguyên 100% hình thái nét ký gốc nhưng tăng độ đậm đà, không bị mờ nhạt khi co nhỏ trong bảng biểu Microsoft Word.
3. Màu xanh mực bút ký chính thức: Deep Royal Navy Blue (RGB: 0, 36, 150)
4. Độ phân giải cao High-Res 1600px, 300 DPI - Sắc nét như vector khi in ấn và xuất PDF.
5. Xuất đồng thời tên tiếng Việt có dấu chuẩn và ASCII không dấu.
"""

import os
import sys
from collections import deque
from PIL import Image, ImageFilter, ImageEnhance

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

IN_DIR = os.path.abspath("TROLYTHIEN/4_DUYET_DE/Dau_vao/CHU KY GV")
OUT_DIR = os.path.abspath("TROLYTHIEN/4_DUYET_DE/Ket_qua/chu_ky")
os.makedirs(OUT_DIR, exist_ok=True)

TARGET_WIDTH = 1600
BLUE_INK = (0, 36, 150)  # Xanh mực đậm đà, sắc nét tuyệt đối trong Word
DPI = (300, 300)

def remove_small_components(mask, min_size=250):
    """Xóa triệt để các chấm nhiễu, hạt bụi li ti của nền giấy cũ."""
    w, h = mask.size
    pix = mask.load()
    visited = set()
    for y in range(h):
        for x in range(w):
            if pix[x, y] > 0 and (x, y) not in visited:
                comp = []
                q = deque([(x, y)])
                visited.add((x, y))
                while q:
                    cx, cy = q.popleft()
                    comp.append((cx, cy))
                    for nx, ny in [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1), 
                                   (cx+1, cy+1), (cx-1, cy-1), (cx+1, cy-1), (cx-1, cy+1)]:
                        if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited and pix[nx, ny] > 0:
                            visited.add((nx, ny))
                            q.append((nx, ny))
                if len(comp) < min_size:
                    for cx, cy in comp:
                        pix[cx, cy] = 0
    return mask

def export_bold_signature(alpha, teacher_vn_name, teacher_ascii_name, dilate_pixels=7, contrast_boost=2.5):
    """Xuất chữ ký đậm đà, sắc nét với độ phân giải cao và metadata 300 DPI."""
    bbox = alpha.getbbox()
    if not bbox:
        print(f"Warning: Bounding box empty for {teacher_vn_name}")
        return
    
    pad = 15
    w, h = alpha.size
    bbox = (max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(w, bbox[2] + pad), min(h, bbox[3] + pad))
    alpha_cropped = alpha.crop(bbox)
    
    scale = TARGET_WIDTH / float(alpha_cropped.width)
    target_h = int(alpha_cropped.height * scale)
    alpha_scaled = alpha_cropped.resize((TARGET_WIDTH, target_h), Image.Resampling.LANCZOS)
    
    # Kỹ thuật làm đậm nét cao cấp tại không gian phân giải cao
    if dilate_pixels > 0:
        alpha_dilated = alpha_scaled.filter(ImageFilter.MaxFilter(dilate_pixels))
        alpha_smooth = alpha_dilated.filter(ImageFilter.GaussianBlur(0.8))
        alpha_final = ImageEnhance.Contrast(alpha_smooth).enhance(contrast_boost)
    else:
        alpha_final = ImageEnhance.Contrast(alpha_scaled).enhance(contrast_boost)
        
    res = Image.new('RGBA', (TARGET_WIDTH, target_h), (*BLUE_INK, 0))
    res.putalpha(alpha_final)
    
    f_vn = os.path.join(OUT_DIR, f"{teacher_vn_name}.png")
    f_ascii = os.path.join(OUT_DIR, f"{teacher_ascii_name}.png")
    
    res.save(f_vn, dpi=DPI)
    res.save(f_ascii, dpi=DPI)
    print(f"✓ Đã nâng cấp chữ ký SIÊU ĐẬM NÉT: {teacher_vn_name} ({TARGET_WIDTH}x{target_h}px, 300 DPI)")

def process_all_teachers():
    print("=" * 70)
    print("NÂNG CẤP BỘ CHỮ KÝ GIÁO VIÊN: ĐẬM RÕ, SẮC NÉT TRONG SUỐT CHO WORD")
    print("=" * 70)
    
    # 1. Thầy Thiên
    im = Image.open(os.path.join(IN_DIR, "Chữ ký Thiên.png"))
    gray = im.convert('L')
    orig_a = im.split()[3] if im.mode == 'RGBA' else Image.new('L', im.size, 255)
    alpha = Image.new('L', im.size, 0)
    for y in range(im.height):
        for x in range(im.width):
            g = gray.getpixel((x, y))
            oa = orig_a.getpixel((x, y))
            if oa < 10 or g > 240:
                val = 0
            elif g < 150:
                val = oa
            else:
                val = int(oa * ((240 - g) / (240 - 150)))
            alpha.putpixel((x, y), val)
    export_bold_signature(alpha, "Thầy Thiên", "Thay_Thien", dilate_pixels=7, contrast_boost=2.5)

    # 2. Cô Bình
    im = Image.open(os.path.join(IN_DIR, "Co Binh.jpg"))
    gray = im.convert('L')
    alpha = Image.new('L', im.size, 0)
    for y in range(im.height):
        for x in range(im.width):
            g = gray.getpixel((x, y))
            if g > 235:
                a = 0
            elif g < 140:
                a = 255
            else:
                a = int(((235 - g) / (235 - 140)) * 255)
            alpha.putpixel((x, y), a)
    export_bold_signature(alpha, "Cô Bình", "Co_Binh", dilate_pixels=5, contrast_boost=2.5)

    # 3. Cô Thảo
    im = Image.open(os.path.join(IN_DIR, "Co Thao.jpg"))
    crop_box = (180, 120, min(im.width, 1278), min(im.height, 840))
    im = im.crop(crop_box)
    gray = im.convert('L')
    bg = gray.filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.BoxBlur(10))
    alpha = Image.new('L', im.size, 0)
    for y in range(im.height):
        for x in range(im.width):
            b = max(1, bg.getpixel((x, y)))
            g = gray.getpixel((x, y))
            d = (b - g) / float(b)
            if d < 0.20:
                a = 0
            elif d > 0.35:
                a = 255
            else:
                a = int(((d - 0.20) / (0.35 - 0.20)) * 255)
            alpha.putpixel((x, y), a)
    alpha = remove_small_components(alpha, min_size=250)
    export_bold_signature(alpha, "Cô Thảo", "Co_Thao", dilate_pixels=5, contrast_boost=2.5)

    # 4. Thầy Danh (Đặc biệt xử lý đậm đà theo yêu cầu người dùng)
    im = Image.open(os.path.join(IN_DIR, "Thay Danh.png"))
    gray = im.convert('L')
    alpha = Image.new('L', im.size, 0)
    for y in range(im.height):
        for x in range(im.width):
            g = gray.getpixel((x, y))
            if g > 240:
                a = 0
            elif g < 180:
                a = 255
            else:
                a = int(((240 - g) / (240 - 180)) * 255)
            alpha.putpixel((x, y), a)
    export_bold_signature(alpha, "Thầy Danh", "Thay_Danh", dilate_pixels=7, contrast_boost=2.5)

    # 5. Thầy Hải
    im = Image.open(os.path.join(IN_DIR, "Thay Hai.jpg"))
    im = im.crop((150, 480, 800, 750))
    gray = im.convert('L')
    bg = gray.filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.BoxBlur(10))
    alpha = Image.new('L', im.size, 0)
    for y in range(im.height):
        for x in range(im.width):
            b = max(1, bg.getpixel((x, y)))
            g = gray.getpixel((x, y))
            d = (b - g) / float(b)
            if d < 0.22:
                a = 0
            elif d > 0.40:
                a = 255
            else:
                a = int(((d - 0.22) / (0.40 - 0.22)) * 255)
            alpha.putpixel((x, y), a)
    alpha = remove_small_components(alpha, min_size=300)
    export_bold_signature(alpha, "Thầy Hải", "Thay_Hai", dilate_pixels=7, contrast_boost=2.5)

    # 6. Thầy Sáng
    im = Image.open(os.path.join(IN_DIR, "thay sang.jpg"))
    gray = im.convert('L')
    alpha = Image.new('L', im.size, 0)
    for y in range(im.height):
        for x in range(im.width):
            g = gray.getpixel((x, y))
            if g > 235:
                a = 0
            elif g < 150:
                a = 255
            else:
                a = int(((235 - g) / (235 - 150)) * 255)
            alpha.putpixel((x, y), a)
    alpha = remove_small_components(alpha, min_size=250)
    export_bold_signature(alpha, "Thầy Sáng", "Thay_Sang", dilate_pixels=5, contrast_boost=2.5)

    print("-" * 70)
    print(f"Hoàn tất cập nhật bộ chữ ký siêu nét vào: {OUT_DIR}")

if __name__ == '__main__':
    process_all_teachers()
