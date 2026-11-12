from PIL import Image, ImageEnhance
import os

col_dir = r'C:\Users\HoangThien\.gemini\antigravity\brain\df0c4170-f71a-4fda-8d62-f50f3f1c24a6\scratch\columns'
out_dir = r'C:\Users\HoangThien\.gemini\antigravity\brain\df0c4170-f71a-4fda-8d62-f50f3f1c24a6\scratch\columns_enhanced'
os.makedirs(out_dir, exist_ok=True)

for fname in os.listdir(col_dir):
    if not fname.endswith('.png'):
        continue
    p = os.path.join(col_dir, fname)
    im = Image.open(p)
    # Upscale 3x
    im_large = im.resize((im.width * 3, im.height * 3), Image.Resampling.LANCZOS)
    enhancer = ImageEnhance.Contrast(im_large)
    im_enh = enhancer.enhance(1.8)
    im_enh.save(os.path.join(out_dir, fname))

print('Enhanced columns saved!')
