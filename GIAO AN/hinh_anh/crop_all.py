from PIL import Image

p1 = Image.open('GIAO AN/hinh_anh/page_1_stitched.png')
p2 = Image.open('GIAO AN/hinh_anh/page_2_stitched.png')
p3 = Image.open('GIAO AN/hinh_anh/page_3_stitched.png')
p4 = Image.open('GIAO AN/hinh_anh/page_4_stitched.png')

# Page 1:
# H.3.1: Hoạt động mở đầu (Hình 3.1a và 3.1b)
# Bounded by: x ~ 560 to 980, y ~ 980 to 1420
h3_1 = p1.crop((560, 990, 980, 1420))
h3_1.save('GIAO AN/hinh_anh/hinh_3_1.png')

# Page 2:
# H.3.2: Hình 3.2 a, b, c, d
# In top half (y ~ 320 to 620, x ~ 100 to 960)
h3_2 = p2.crop((110, 320, 960, 620))
h3_2.save('GIAO AN/hinh_anh/hinh_3_2.png')

# H.3.3: Hình 3.3 (Bốn điểm E, F, G, H)
# y ~ 1000 to 1220, x ~ 390 to 630
h3_3 = p2.crop((390, 1000, 630, 1220))
h3_3.save('GIAO AN/hinh_anh/hinh_3_3.png')

# Page 3:
# H.3.4: Hình 3.4 (Tứ giác ABCD)
# Top of page 3: y ~ 160 to 420, x ~ 230 to 520
h3_4 = p3.crop((230, 160, 520, 420))
h3_4.save('GIAO AN/hinh_anh/hinh_3_4.png')

# H.3.5: Hình 3.5 (Tứ giác ABCD chia tam giác)
# y ~ 450 to 680, x ~ 630 to 960
h3_5 = p3.crop((630, 450, 960, 680))
h3_5.save('GIAO AN/hinh_anh/hinh_3_5.png')

# H.3.6: Hình 3.6 (Ví dụ: tính góc D)
# y ~ 810 to 1080, x ~ 720 to 970
h3_6 = p3.crop((720, 810, 970, 1080))
h3_6.save('GIAO AN/hinh_anh/hinh_3_6.png')

# H.3.7: Hình 3.7 (Luyện tập 2: góc F)
# y ~ 1130 to 1420, x ~ 680 to 970
h3_7 = p3.crop((680, 1130, 970, 1420))
h3_7.save('GIAO AN/hinh_anh/hinh_3_7.png')

# Page 4:
# H.3.8: Bài 3.1 (Hình 3.8a, b)
# y ~ 190 to 460, x ~ 110 to 960
h3_8 = p4.crop((110, 190, 960, 460))
h3_8.save('GIAO AN/hinh_anh/hinh_3_8.png')

# H.3.9: Bài 3.2 (Hình 3.9)
# y ~ 470 to 680, x ~ 580 to 960
h3_9 = p4.crop((580, 470, 960, 680))
h3_9.save('GIAO AN/hinh_anh/hinh_3_9.png')

# H.3.10: Bài 3.3 (Hình 3.10 Cái diều)
# y ~ 690 to 990, x ~ 180 to 860
h3_10 = p4.crop((180, 690, 860, 990))
h3_10.save('GIAO AN/hinh_anh/hinh_3_10.png')

# H_em_co_biet: Lát nền phẳng
# y ~ 1040 to 1400, x ~ 370 to 920
h_ecb = p4.crop((370, 1040, 920, 1400))
h_ecb.save('GIAO AN/hinh_anh/hinh_em_co_biet.png')

print("All figures cropped and saved successfully!")
