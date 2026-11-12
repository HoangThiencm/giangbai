import sys
from PIL import Image

# Let's inspect the TKB image
# The image has 24 columns for classes:
# 61, 62, 63, 64, 65, 66 (6 columns)
# 71, 72, 73, 74, 75, 76 (6 columns)
# 81, 82, 83, 84, 85     (5 columns)
# 91, 92, 93, 94, 95, 96, 97 (7 columns)
# Total columns = 24.
# Left margin for Thứ / Tiết columns.

# Let's inspect the layout of the image
im = Image.open(r'C:\Users\HoangThien\.gemini\antigravity\brain\df0c4170-f71a-4fda-8d62-f50f3f1c24a6\.user_uploaded\media_1793871190002_09290cb7.jpg')
w, h = im.size
print(f'Width: {w}, Height: {h}')
