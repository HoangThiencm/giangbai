import os
from PIL import Image

im13 = Image.open('GIAO AN/FILE BAI HOC/extracted_pages/page_3_Im13.jpg')
im14 = Image.open('GIAO AN/FILE BAI HOC/extracted_pages/page_3_Im14.jpg')
im17 = Image.open('GIAO AN/FILE BAI HOC/extracted_pages/page_4_Im17.jpg')
im18 = Image.open('GIAO AN/FILE BAI HOC/extracted_pages/page_4_Im18.jpg')

im13.save('GIAO AN/hinh_anh/test_im13.png')
im14.save('GIAO AN/hinh_anh/test_im14.png')
im17.save('GIAO AN/hinh_anh/test_im17.png')
im18.save('GIAO AN/hinh_anh/test_im18.png')
print("Saved test images")
