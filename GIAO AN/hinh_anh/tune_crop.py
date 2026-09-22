from PIL import Image

p1 = Image.open('GIAO AN/hinh_anh/page_1_stitched.png')
p2 = Image.open('GIAO AN/hinh_anh/page_2_stitched.png')
p3 = Image.open('GIAO AN/hinh_anh/page_3_stitched.png')
p4 = Image.open('GIAO AN/hinh_anh/page_4_stitched.png')

# Page 1:
# H.3.1: Hoạt động mở đầu (Hình 3.1a và 3.1b)
# x from 550 to 1020, y from 975 to 1420
h3_1 = p1.crop((550, 975, 1020, 1420))
h3_1.save('GIAO AN/hinh_anh/hinh_3_1.png')

# Page 2:
# H.3.2: a, b, c, d
# x from 80 to 1020, y from 350 to 625
h3_2 = p2.crop((80, 350, 1020, 625))
h3_2.save('GIAO AN/hinh_anh/hinh_3_2.png')

# H.3.3: 4 điểm E, F, G, H
# x from 380 to 650, y from 1000 to 1230
h3_3 = p2.crop((380, 1000, 650, 1230))
h3_3.save('GIAO AN/hinh_anh/hinh_3_3.png')

# Page 3:
# H.3.4: Tứ giác ABCD (Luyện tập 1)
# x from 220 to 530, y from 170 to 420
h3_4 = p3.crop((220, 170, 530, 420))
h3_4.save('GIAO AN/hinh_anh/hinh_3_4.png')

# H.3.5: Tứ giác ABCD có đường chéo BD
# x from 580 to 1020, y from 440 to 710
h3_5 = p3.crop((580, 440, 1020, 710))
h3_5.save('GIAO AN/hinh_anh/hinh_3_5.png')

# H.3.6: Ví dụ (tính góc D)
# x from 700 to 1020, y from 820 to 1100
h3_6 = p3.crop((700, 820, 1020, 1100))
h3_6.save('GIAO AN/hinh_anh/hinh_3_6.png')

# H.3.7: Luyện tập 2 (góc F)
# x from 670 to 1020, y from 1140 to 1430
h3_7 = p3.crop((670, 1140, 1020, 1430))
h3_7.save('GIAO AN/hinh_anh/hinh_3_7.png')

# Page 4:
# H.3.8: Bài 3.1
# x from 80 to 1020, y from 200 to 470
h3_8 = p4.crop((80, 200, 1020, 470))
h3_8.save('GIAO AN/hinh_anh/hinh_3_8.png')

# H.3.9: Bài 3.2
# x from 550 to 1020, y from 470 to 680
h3_9 = p4.crop((550, 470, 1020, 680))
h3_9.save('GIAO AN/hinh_anh/hinh_3_9.png')

# H.3.10: Bài 3.3 (Hình cái diều)
# x from 160 to 880, y from 680 to 990
h3_10 = p4.crop((160, 680, 880, 990))
h3_10.save('GIAO AN/hinh_anh/hinh_3_10.png')

# H. Em có biết: Lát nền phẳng
# x from 370 to 950, y from 1040 to 1400
h_ecb = p4.crop((370, 1040, 950, 1400))
h_ecb.save('GIAO AN/hinh_anh/hinh_em_co_biet.png')

print("All tuned figures cropped successfully!")
