from PIL import Image
import numpy as np

im = Image.open(r'C:\Users\HoangThien\.gemini\antigravity\brain\df0c4170-f71a-4fda-8d62-f50f3f1c24a6\.user_uploaded\media_1793871190002_09290cb7.jpg')
w, h = im.size

# Let's see: row 0 to 80 has the title and table headers.
# Let's crop the header from y=50 to 90
header = im.crop((0, 50, w, 90))
header.save(r'C:\Users\HoangThien\.gemini\antigravity\brain\df0c4170-f71a-4fda-8d62-f50f3f1c24a6\scratch\table_header.png')

# The classes are:
# 61, 62, 63, 64, 65, 66 (6 classes)
# 71, 72, 73, 74, 75, 76 (6 classes)
# 81, 82, 83, 84, 85     (5 classes)
# 91, 92, 93, 94, 95, 96, 97 (7 classes)
# Total = 24 classes.
# Let's find the column borders by looking at vertical grid lines!
arr = np.array(im.convert('L'))
# Check row 100 to 200 for dark vertical grid lines
sub = arr[100:250, :]
col_mean = sub.mean(axis=0)

# Vertical grid lines are dark lines across rows
# Let's find columns where col_mean is low or has sharp dips
grid_lines = []
for x in range(1, w-1):
    if col_mean[x] < 180 and col_mean[x] < col_mean[x-1] and col_mean[x] <= col_mean[x+1]:
        grid_lines.append(x)

print(f'Detected grid lines count: {len(grid_lines)}, positions: {grid_lines}')
