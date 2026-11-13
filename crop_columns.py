from PIL import Image
import os

im = Image.open(r'C:\Users\HoangThien\.gemini\antigravity\brain\df0c4170-f71a-4fda-8d62-f50f3f1c24a6\.user_uploaded\media_1793871190002_09290cb7.jpg')
w, h = im.size

classes = [
    '61_Nguyet', '62_Thao', '63_Duy', '64_Nhan', '65_VuHang', '66_Linh',
    '71_Binh', '72_KTrang', '73_Hoi', '74_OTrang', '75_Quynh', '76_Hai',
    '81_Sang', '82_Hai', '83_Vu', '84_Tri', '85_VHang',
    '91_PDung', '92_Thu', '93_LDung', '94_Tuoi', '95_Hoa', '96_ThuHuong', '97_Vang'
]

os.makedirs(r'C:\Users\HoangThien\.gemini\antigravity\brain\df0c4170-f71a-4fda-8d62-f50f3f1c24a6\scratch\columns', exist_ok=True)

# Let's calculate the exact x boundaries for each of the 24 columns
# Left table edge starts at 30.7, right at 984.0
x_borders = [30.7 + i * (984.0 - 30.7) / 24.0 for i in range(25)]

for i in range(24):
    x1 = int(round(x_borders[i]))
    x2 = int(round(x_borders[i+1]))
    crop_img = im.crop((x1, 50, x2, h))
    crop_img.save(rf'C:\Users\HoangThien\.gemini\antigravity\brain\df0c4170-f71a-4fda-8d62-f50f3f1c24a6\scratch\columns\{classes[i]}.png')

print('All 24 column crops saved!')
